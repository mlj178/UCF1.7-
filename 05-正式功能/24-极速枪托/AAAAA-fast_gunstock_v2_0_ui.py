# AAAAA-fast_gunstock_v2_0_ui.py
# 极速枪托 v2.0 研究/重构版 UI
#
# 作用：
#   1. 连接 UnityCrossFire.exe。
#   2. 加载 AAAAA-fast_gunstock_v2_0_research.js。
#   3. 提供三种模式：trace_only / unlock_after_damage / early_damage_unlock。
#   4. 自动写 TXT 日志，便于把日志发给 ChatGPT 继续分析。

import os
import time
import threading
from datetime import datetime

import customtkinter as ctk
import frida
import psutil


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JS_FILE = os.path.join(BASE_DIR, "AAAAA-fast_gunstock_v2_0_research.js")
GAME_PROCESS_NAME = "UnityCrossFire.exe"
LOG_DIR = os.path.join(BASE_DIR, "logs")


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class FastGunstockV2App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("极速枪托 v2.0 研究版")
        self.geometry("760x760")
        self.minsize(700, 650)

        self.session = None
        self.script = None
        self.is_connected = False
        self._connecting = False
        self._polling = False
        self._closing = False
        self._state_lock = threading.Lock()

        os.makedirs(LOG_DIR, exist_ok=True)
        self.log_path = os.path.join(LOG_DIR, "fast_gunstock_v2_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt")

        self.game_state = {
            "enabled": False,
            "initialized": False,
            "hooksInstalled": False,
            "mode": "unlock_after_damage",
            "unlockMethod": "call_exit",
            "unlockDelayMs": 25,
            "earlyDamageDelayMs": 90,
            "earlyUnlockDelayMs": 15,
            "specialHits": 0,
            "attackDataHits": 0,
            "naturalDamageHits": 0,
            "earlyDamageCalls": 0,
            "originalExitHits": 0,
            "animationExitHits": 0,
            "unlockCalls": 0,
            "unlockWriteCalls": 0,
            "unlockFailures": 0,
            "skippedLocked": 0,
            "activeSessions": 0,
            "lastError": None,
            "lastEvent": None,
        }

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.after(500, self._auto_connect_thread)

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)

        title = ctk.CTkLabel(self, text="极速枪托 v2.0 研究版", font=ctk.CTkFont(size=24, weight="bold"))
        title.grid(row=0, column=0, padx=16, pady=(14, 2), sticky="ew")

        subtitle = ctk.CTkLabel(
            self,
            text="不再修改手部/角色 Animator，改为探针 + 伤害后解锁 + 可选提前伤害实验",
            font=ctk.CTkFont(size=12),
            text_color="#999",
        )
        subtitle.grid(row=1, column=0, padx=16, pady=(0, 10), sticky="ew")

        status_frame = ctk.CTkFrame(self, corner_radius=8)
        status_frame.grid(row=2, column=0, padx=16, pady=6, sticky="ew")
        status_frame.grid_columnconfigure(1, weight=1)

        self.status_dot = ctk.CTkLabel(status_frame, text="●", font=ctk.CTkFont(size=18), text_color="#888")
        self.status_dot.grid(row=0, column=0, padx=(12, 6), pady=8)
        self.status_label = ctk.CTkLabel(status_frame, text="等待游戏启动...", font=ctk.CTkFont(size=14))
        self.status_label.grid(row=0, column=1, padx=4, pady=8, sticky="w")
        self.pid_label = ctk.CTkLabel(status_frame, text="", text_color="#999")
        self.pid_label.grid(row=0, column=2, padx=12, pady=8, sticky="e")

        control = ctk.CTkFrame(self, corner_radius=8)
        control.grid(row=3, column=0, padx=16, pady=6, sticky="ew")
        control.grid_columnconfigure(1, weight=1)
        control.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(control, text="功能开关", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=12, pady=10, sticky="w")
        self.feature_switch = ctk.CTkSwitch(control, text="关闭", command=self.on_toggle_feature)
        self.feature_switch.grid(row=0, column=1, padx=8, pady=10, sticky="w")
        self.feature_switch.configure(state="disabled")

        ctk.CTkButton(control, text="手动解锁当前", command=self.on_force_unlock, width=120).grid(row=0, column=2, padx=8, pady=10, sticky="e")
        ctk.CTkButton(control, text="重新连接", command=self._manual_reconnect, width=100).grid(row=0, column=3, padx=12, pady=10, sticky="e")

        config_frame = ctk.CTkFrame(self, corner_radius=8)
        config_frame.grid(row=4, column=0, padx=16, pady=6, sticky="ew")
        config_frame.grid_columnconfigure(1, weight=1)
        config_frame.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(config_frame, text="模式").grid(row=0, column=0, padx=12, pady=8, sticky="w")
        self.mode_box = ctk.CTkComboBox(
            config_frame,
            values=["trace_only", "unlock_after_damage", "early_damage_unlock"],
            command=lambda _: self.apply_config_async(),
        )
        self.mode_box.set("unlock_after_damage")
        self.mode_box.grid(row=0, column=1, padx=8, pady=8, sticky="ew")

        ctk.CTkLabel(config_frame, text="解锁方式").grid(row=0, column=2, padx=12, pady=8, sticky="w")
        self.unlock_method_box = ctk.CTkComboBox(
            config_frame,
            values=["call_exit", "write_lock_zero", "call_exit_then_write"],
            command=lambda _: self.apply_config_async(),
        )
        self.unlock_method_box.set("call_exit")
        self.unlock_method_box.grid(row=0, column=3, padx=8, pady=8, sticky="ew")

        self.unlock_delay_var = ctk.IntVar(value=25)
        self.early_damage_delay_var = ctk.IntVar(value=90)
        self.early_unlock_delay_var = ctk.IntVar(value=15)
        self.early_attack_index_var = ctk.IntVar(value=0)

        self._add_slider(config_frame, 1, "自然伤害后解锁延迟", self.unlock_delay_var, 0, 200, "ms")
        self._add_slider(config_frame, 2, "提前伤害延迟", self.early_damage_delay_var, 10, 500, "ms")
        self._add_slider(config_frame, 3, "提前伤害后解锁延迟", self.early_unlock_delay_var, 0, 200, "ms")
        self._add_slider(config_frame, 4, "提前伤害 attackIndex", self.early_attack_index_var, 0, 5, "")

        note = ctk.CTkLabel(
            config_frame,
            text="建议顺序：1 trace_only 看链路时间；2 unlock_after_damage 看间隔；3 early_damage_unlock 只做离线实验。",
            text_color="#e0b15a",
            font=ctk.CTkFont(size=12),
        )
        note.grid(row=5, column=0, columnspan=4, padx=12, pady=(4, 10), sticky="w")

        metrics = ctk.CTkFrame(self, corner_radius=8)
        metrics.grid(row=5, column=0, padx=16, pady=6, sticky="ew")
        metrics.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.enabled_label = self._metric(metrics, 0, 0, "功能", "关闭")
        self.hook_label = self._metric(metrics, 0, 1, "Hook", "未安装")
        self.mode_label = self._metric(metrics, 0, 2, "模式", "-")
        self.active_label = self._metric(metrics, 0, 3, "活动会话", "0")
        self.count_label = ctk.CTkLabel(metrics, text="", font=ctk.CTkFont(size=12), text_color="#aaa")
        self.count_label.grid(row=1, column=0, columnspan=4, padx=8, pady=(2, 8), sticky="ew")

        self.last_event_label = ctk.CTkLabel(self, text="最近事件：-", font=ctk.CTkFont(size=12), text_color="#aaa")
        self.last_event_label.grid(row=6, column=0, padx=20, pady=(0, 4), sticky="w")

        log_frame = ctk.CTkFrame(self, corner_radius=8)
        log_frame.grid(row=7, column=0, padx=16, pady=(6, 14), sticky="nsew")
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(log_frame, fg_color="transparent")
        header.grid(row=0, column=0, padx=8, pady=(6, 2), sticky="ew")
        ctk.CTkLabel(header, text="运行日志", font=ctk.CTkFont(weight="bold")).pack(side="left")
        ctk.CTkButton(header, text="清空", width=60, command=self.clear_log).pack(side="right")

        self.log_box = ctk.CTkTextbox(log_frame, font=ctk.CTkFont(family="Consolas", size=11))
        self.log_box.grid(row=1, column=0, padx=8, pady=(0, 8), sticky="nsew")
        self._log("日志文件: " + self.log_path)

    def _add_slider(self, parent, row, label, var, from_, to, suffix):
        ctk.CTkLabel(parent, text=label).grid(row=row, column=0, padx=12, pady=6, sticky="w")
        slider = ctk.CTkSlider(
            parent,
            from_=from_,
            to=to,
            number_of_steps=max(1, to - from_),
            command=lambda value, v=var, s=suffix: self._on_slider(v, value),
        )
        slider.set(var.get())
        slider.grid(row=row, column=1, columnspan=2, padx=8, pady=6, sticky="ew")
        value_label = ctk.CTkLabel(parent, text=str(var.get()) + suffix, width=64)
        value_label.grid(row=row, column=3, padx=8, pady=6, sticky="w")
        var._label = value_label
        var._suffix = suffix

    def _on_slider(self, var, value):
        var.set(int(round(float(value))))
        var._label.configure(text=str(var.get()) + var._suffix)
        self.apply_config_async()

    def _metric(self, parent, row, col, title, value):
        frame = ctk.CTkFrame(parent, corner_radius=6)
        frame.grid(row=row, column=col, padx=6, pady=8, sticky="ew")
        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=11), text_color="#999").pack(pady=(6, 0))
        label = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=14, weight="bold"))
        label.pack(pady=(0, 6))
        return label

    def _find_game_pid(self):
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if proc.info.get("name") == GAME_PROCESS_NAME:
                    return proc.info.get("pid")
            except Exception:
                pass
        return None

    def _auto_connect_thread(self):
        if self.is_connected or self._connecting:
            return
        pid = self._find_game_pid()
        if pid:
            threading.Thread(target=self._connect, args=(pid,), daemon=True).start()
        else:
            self.after(1200, self._auto_connect_thread)

    def _manual_reconnect(self):
        self._disconnect()
        pid = self._find_game_pid()
        if not pid:
            self._log("未找到游戏进程: " + GAME_PROCESS_NAME)
            self.after(1200, self._auto_connect_thread)
            return
        threading.Thread(target=self._connect, args=(pid,), daemon=True).start()

    def _connect(self, pid):
        if self._connecting:
            return
        self._connecting = True
        self._log("检测到游戏 PID: " + str(pid) + "，正在连接...")

        try:
            if not os.path.exists(JS_FILE):
                self._log("JS 文件不存在: " + JS_FILE)
                return

            self.session = frida.attach(pid)
            with open(JS_FILE, "r", encoding="utf-8") as f:
                js_code = f.read()

            self.script = self.session.create_script(js_code)
            self.script.on("message", self.on_message)
            self.script.load()

            self.is_connected = True
            self._safe_config(self.status_dot, text_color="#2ecc71")
            self._safe_config(self.status_label, text="已连接 - " + GAME_PROCESS_NAME)
            self._safe_config(self.pid_label, text="PID: " + str(pid))
            self.after(0, self._enable_controls)
            self.apply_config_async()
            self._start_polling()
            self._log("脚本已加载。先用 trace_only 观察，再切换模式测试。")
        except Exception as exc:
            self._log("连接失败: " + str(exc))
            self._disconnect()
        finally:
            self._connecting = False

    def _enable_controls(self):
        self.feature_switch.configure(state="normal")

    def _disable_controls(self):
        self.feature_switch.configure(state="disabled")
        self.feature_switch.deselect()
        self.feature_switch.configure(text="关闭")

    def _build_config(self):
        return {
            "mode": self.mode_box.get(),
            "unlockMethod": self.unlock_method_box.get(),
            "unlockDelayMs": int(self.unlock_delay_var.get()),
            "earlyDamageDelayMs": int(self.early_damage_delay_var.get()),
            "earlyUnlockDelayMs": int(self.early_unlock_delay_var.get()),
            "earlyAttackIndex": int(self.early_attack_index_var.get()),
            "verboseTrace": True,
        }

    def apply_config_async(self):
        if not self.is_connected or not self.script:
            return
        threading.Thread(target=self._apply_config, daemon=True).start()

    def _apply_config(self):
        try:
            ok = self.script.exports_sync.setconfig(self._build_config())
            if ok:
                self._log("配置已应用: " + str(self._build_config()))
        except Exception as exc:
            self._log("配置失败: " + str(exc))

    def on_toggle_feature(self):
        if not self.is_connected or not self.script:
            self.feature_switch.deselect()
            return
        if self.feature_switch.get():
            self.feature_switch.configure(text="开启")
            threading.Thread(target=self._enable_feature, daemon=True).start()
        else:
            self.feature_switch.configure(text="关闭")
            threading.Thread(target=self._disable_feature, daemon=True).start()

    def _enable_feature(self):
        try:
            self.script.exports_sync.setconfig(self._build_config())
            ok = self.script.exports_sync.enable()
            self._log("enable() 返回: " + str(ok))
        except Exception as exc:
            self._log("开启失败: " + str(exc))
            self.after(0, self.feature_switch.deselect)

    def _disable_feature(self):
        try:
            ok = self.script.exports_sync.disable()
            self._log("disable() 返回: " + str(ok))
        except Exception as exc:
            self._log("关闭失败: " + str(exc))

    def on_force_unlock(self):
        if not self.is_connected or not self.script:
            return
        threading.Thread(target=self._force_unlock, daemon=True).start()

    def _force_unlock(self):
        try:
            count = self.script.exports_sync.forceunlock()
            self._log("forceunlock() 返回: " + str(count))
        except Exception as exc:
            self._log("手动解锁失败: " + str(exc))

    def _start_polling(self):
        if self._polling:
            return
        self._polling = True
        threading.Thread(target=self._poll_loop, daemon=True).start()

    def _poll_loop(self):
        while self._polling and self.is_connected and self.script:
            try:
                status = self.script.exports_sync.status()
                if isinstance(status, dict):
                    with self._state_lock:
                        self.game_state.update(status)
                    self.after(0, self._update_display)
            except frida.InvalidOperationError:
                self._log("脚本失效，准备断开")
                self._disconnect()
                return
            except Exception:
                pass
            time.sleep(0.5)

    def _update_display(self):
        with self._state_lock:
            s = dict(self.game_state)

        self.enabled_label.configure(text="开启" if s.get("enabled") else "关闭", text_color="#2ecc71" if s.get("enabled") else "#e74c3c")
        self.hook_label.configure(text="已安装" if s.get("hooksInstalled") else "未安装", text_color="#2ecc71" if s.get("hooksInstalled") else "#f39c12")
        self.mode_label.configure(text=str(s.get("mode", "-")))
        self.active_label.configure(text=str(s.get("activeSessions", 0)))

        self.count_label.configure(
            text=(
                "右键: {specialHits} / 攻击数据: {attackDataHits} / 自然伤害: {naturalDamageHits} / 提前伤害: {earlyDamageCalls} / "
                "原始退出: {originalExitHits} / 动画退出: {animationExitHits} / 解锁调用: {unlockCalls} / 写锁: {unlockWriteCalls} / 失败: {unlockFailures} / 锁中跳过: {skippedLocked}"
            ).format(**s)
        )
        self.last_event_label.configure(text="最近事件：" + str(s.get("lastEvent") or "-"))

    def _disconnect(self):
        self._polling = False
        if self.script:
            try:
                self.script.exports_sync.cleanup()
            except Exception:
                pass
            try:
                self.script.unload()
            except Exception:
                pass
            self.script = None
        if self.session:
            try:
                self.session.detach()
            except Exception:
                pass
            self.session = None

        self.is_connected = False
        self._safe_config(self.status_dot, text_color="#888")
        self._safe_config(self.status_label, text="已断开")
        self._safe_config(self.pid_label, text="")
        self.after(0, self._disable_controls)

    def on_message(self, message, data):
        if message.get("type") == "send":
            payload = message.get("payload")
            if isinstance(payload, dict) and payload.get("type") == "log":
                self._log("[{}][{}] {}".format(payload.get("level", "info"), payload.get("module", ""), payload.get("message", "")))
            else:
                self._log("[JS] " + str(payload))
        elif message.get("type") == "error":
            self._log("[JS错误] " + message.get("description", str(message)))

    def _safe_config(self, widget, **kwargs):
        try:
            self.after(0, lambda: widget.configure(**kwargs))
        except Exception:
            pass

    def _log(self, text):
        line = datetime.now().strftime("%H:%M:%S") + "  " + str(text)
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass
        try:
            self.log_box.insert("end", line + "\n")
            self.log_box.see("end")
        except Exception:
            pass

    def clear_log(self):
        try:
            self.log_box.delete("1.0", "end")
        except Exception:
            pass

    def on_close(self):
        if self._closing:
            return
        self._closing = True
        self._disconnect()
        self.destroy()


if __name__ == "__main__":
    app = FastGunstockV2App()
    app.mainloop()
