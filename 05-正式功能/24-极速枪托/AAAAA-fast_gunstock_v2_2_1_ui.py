# AAAAA-fast_gunstock_v2_2_1_ui.py
# 极速枪托 v2.2.1 安全防打断版 UI
# 修复：不能使用 self.state，因为会覆盖 Tkinter 自带 state() 方法。

import os
import time
import threading
from datetime import datetime

import customtkinter as ctk
import frida
import psutil

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JS_FILE = os.path.join(BASE_DIR, "AAAAA-fast_gunstock_v2_2_1_safe.js")
GAME_PROCESS_NAME = "UnityCrossFire.exe"

COLOR_GREEN = "#2ecc71"
COLOR_RED = "#e74c3c"
COLOR_ORANGE = "#f39c12"
COLOR_BG = "#1a1a2e"
COLOR_CARD = "#16213e"


class FastGunstockSafeUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("极速枪托 v2.2.1 安全防打断版")
        self.geometry("760x760")
        self.minsize(690, 680)

        self.session = None
        self.script = None
        self.connected = False
        self.connecting = False
        self.polling = False
        self.closing = False

        self.rpc_lock = threading.Lock()
        self.params_dirty = False

        # 不能叫 self.state。
        # Tkinter / CustomTkinter 有 state() 方法，覆盖后会导致 TypeError: 'dict' object is not callable。
        self.game_state = {}
        self.game_state_lock = threading.Lock()

        self._build_ui()
        self.after(700, self._auto_connect)

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

        ctk.CTkLabel(self, text="极速枪托 v2.2.1 安全防打断版", font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, padx=18, pady=(16, 2), sticky="ew")
        ctk.CTkLabel(self, text="修复 self.state 崩溃；拖动滑块不会连续写入游戏；不 replace 右键入口", font=ctk.CTkFont(size=12), text_color="#aaa").grid(row=1, column=0, padx=18, pady=(0, 8), sticky="ew")

        top = ctk.CTkFrame(self, corner_radius=8, fg_color=COLOR_BG)
        top.grid(row=2, column=0, padx=16, pady=4, sticky="ew")
        top.grid_columnconfigure(1, weight=1)

        self.dot_label = ctk.CTkLabel(top, text="●", font=ctk.CTkFont(size=18), text_color="#888")
        self.dot_label.grid(row=0, column=0, padx=(12, 4), pady=8)
        self.conn_label = ctk.CTkLabel(top, text="等待游戏启动...", font=ctk.CTkFont(size=14))
        self.conn_label.grid(row=0, column=1, padx=4, pady=8, sticky="w")
        self.pid_label = ctk.CTkLabel(top, text="", font=ctk.CTkFont(size=11), text_color="#888")
        self.pid_label.grid(row=0, column=2, padx=12, pady=8, sticky="e")

        control = ctk.CTkFrame(self, corner_radius=8, fg_color=COLOR_CARD)
        control.grid(row=3, column=0, padx=16, pady=4, sticky="ew")
        control.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(control, text="功能开关", font=ctk.CTkFont(size=13, weight="bold")).grid(row=0, column=0, padx=(12, 6), pady=(12, 8), sticky="w")
        self.switch = ctk.CTkSwitch(control, text="关闭", command=self._toggle_feature, progress_color=COLOR_GREEN, switch_width=52, switch_height=24)
        self.switch.grid(row=0, column=1, padx=4, pady=(12, 8), sticky="w")
        self.switch.configure(state="disabled")

        self.apply_button = ctk.CTkButton(control, text="应用参数", width=110, height=30, command=self._apply_params_clicked, fg_color="#2980b9", hover_color="#3498db")
        self.apply_button.grid(row=0, column=2, padx=(6, 12), pady=(12, 8))
        self.apply_button.configure(state="disabled")

        self.early_slider, self.early_value = self._add_slider(control, 1, "提前伤害延迟", 30, 300, 27, 120, "ms", self._on_slider_changed)
        self.unlock_slider, self.unlock_value = self._add_slider(control, 2, "伤害后解锁延迟", 0, 200, 40, 40, "ms", self._on_slider_changed)
        self.timeout_slider, self.timeout_value = self._add_slider(control, 3, "保护超时", 300, 1500, 24, 650, "ms", self._on_slider_changed)
        self.attack_slider, self.attack_value = self._add_slider(control, 4, "attackIndex", 0, 5, 5, 0, "", self._on_slider_changed)

        self.dirty_label = ctk.CTkLabel(control, text="参数未修改", font=ctk.CTkFont(size=11), text_color="#888")
        self.dirty_label.grid(row=5, column=0, columnspan=3, padx=12, pady=(4, 10), sticky="w")

        hint = ctk.CTkFrame(self, corner_radius=8, fg_color=COLOR_BG)
        hint.grid(row=4, column=0, padx=16, pady=4, sticky="ew")
        hint.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(hint, text="推荐：提前伤害 120ms，伤害后解锁 40ms，保护超时 650ms。稳定后再降到 100 / 90 / 80ms。拖动滑块只是改界面数值，必须点击“应用参数”才写入脚本。", font=ctk.CTkFont(size=12), text_color="#ddd", wraplength=690, justify="left").grid(row=0, column=0, padx=12, pady=10, sticky="w")

        info = ctk.CTkFrame(self, corner_radius=8, fg_color=COLOR_BG)
        info.grid(row=5, column=0, padx=16, pady=4, sticky="ew")
        info.grid_columnconfigure((0, 1, 2), weight=1)
        self.enable_text = self._add_info_cell(info, 0, 0, "功能状态", "关闭")
        self.hook_text = self._add_info_cell(info, 0, 1, "Hook 状态", "未安装")
        self.guard_text = self._add_info_cell(info, 0, 2, "保护窗口", "未保护")
        self.counter_text = ctk.CTkLabel(info, text="右键: 0 / 放行: 0 / 保护: 0 / 提前伤害: 0 / 自然伤害: 0 / 解锁: 0", font=ctk.CTkFont(size=11), text_color="#aaa")
        self.counter_text.grid(row=2, column=0, columnspan=3, padx=8, pady=(4, 8), sticky="ew")

        log_frame = ctk.CTkFrame(self, corner_radius=8)
        log_frame.grid(row=6, column=0, padx=16, pady=(8, 12), sticky="nsew")
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)
        header = ctk.CTkFrame(log_frame, fg_color="transparent")
        header.grid(row=0, column=0, padx=8, pady=(6, 2), sticky="ew")
        ctk.CTkLabel(header, text="运行日志", font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")
        ctk.CTkButton(header, text="清空", width=50, height=22, font=ctk.CTkFont(size=10), fg_color="#444", hover_color="#555", command=self._clear_log).pack(side="right")
        self.log_box = ctk.CTkTextbox(log_frame, font=ctk.CTkFont(size=11))
        self.log_box.grid(row=1, column=0, padx=8, pady=(2, 8), sticky="nsew")
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _add_slider(self, parent, row, name, min_v, max_v, steps, default, unit, callback):
        ctk.CTkLabel(parent, text=name, font=ctk.CTkFont(size=13)).grid(row=row, column=0, padx=(12, 6), pady=6, sticky="w")
        slider = ctk.CTkSlider(parent, from_=min_v, to=max_v, number_of_steps=steps, command=callback)
        slider.set(default)
        slider.grid(row=row, column=1, padx=4, pady=6, sticky="ew")
        slider.configure(state="disabled")
        value_label = ctk.CTkLabel(parent, text=str(int(default)) + unit, width=70, font=ctk.CTkFont(size=13, weight="bold"), text_color="#aaa")
        value_label.grid(row=row, column=2, padx=(6, 12), pady=6)
        return slider, value_label

    def _add_info_cell(self, parent, row, col, title, value):
        cell = ctk.CTkFrame(parent, corner_radius=6, fg_color=COLOR_CARD)
        cell.grid(row=row, column=col, padx=6, pady=8, sticky="ew")
        ctk.CTkLabel(cell, text=title, font=ctk.CTkFont(size=11), text_color="#888").pack(pady=(6, 0))
        label = ctk.CTkLabel(cell, text=value, font=ctk.CTkFont(size=13, weight="bold"))
        label.pack(pady=(0, 6))
        return label

    def _auto_connect(self):
        if not self.connected and not self.connecting:
            threading.Thread(target=self._find_and_connect, daemon=True).start()
        if not self.connected:
            self.after(1500, self._auto_connect)

    def _find_game_pid(self):
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if proc.info["name"] == GAME_PROCESS_NAME:
                    return proc.info["pid"]
            except Exception:
                pass
        return None

    def _find_and_connect(self):
        pid = self._find_game_pid()
        if not pid:
            self._safe_config(self.conn_label, text="等待游戏启动...")
            self._safe_config(self.dot_label, text_color="#888")
            return
        self._connect(pid)

    def _connect(self, pid):
        if self.connecting:
            return
        self.connecting = True
        self._safe_log("检测到游戏 PID: " + str(pid) + "，正在连接...")
        try:
            self.session = frida.attach(pid)
            if not os.path.exists(JS_FILE):
                self._safe_log("JS 文件不存在: " + JS_FILE)
                self.connecting = False
                return
            with open(JS_FILE, "r", encoding="utf-8") as f:
                code = f.read()
            self.script = self.session.create_script(code)
            self.script.on("message", self._on_js_message)
            self.script.load()
            self.connected = True
            self.connecting = False
            self._safe_config(self.dot_label, text_color=COLOR_GREEN)
            self._safe_config(self.conn_label, text="已连接 - " + GAME_PROCESS_NAME)
            self._safe_config(self.pid_label, text="PID: " + str(pid))
            self.after(0, self._enable_controls)
            self._safe_log("脚本已加载。先点“应用参数”，再打开功能开关。")
            self._start_polling()
        except frida.ProcessNotFoundError:
            self._safe_log("游戏进程已退出")
            self.connecting = False
        except frida.ServerNotStartedError:
            self._safe_log("Frida Server 未运行，请先启动 frida-server")
            self.connecting = False
        except Exception as exc:
            self._safe_log("连接异常: " + str(exc))
            self.connecting = False

    def _enable_controls(self):
        self.switch.configure(state="normal")
        self.apply_button.configure(state="normal")
        self.early_slider.configure(state="normal")
        self.unlock_slider.configure(state="normal")
        self.timeout_slider.configure(state="normal")
        self.attack_slider.configure(state="normal")

    def _disable_controls(self):
        self.switch.configure(state="disabled")
        self.switch.deselect()
        self.switch.configure(text="关闭")
        self.apply_button.configure(state="disabled")
        self.early_slider.configure(state="disabled")
        self.unlock_slider.configure(state="disabled")
        self.timeout_slider.configure(state="disabled")
        self.attack_slider.configure(state="disabled")

    def _on_slider_changed(self, _value):
        early = int(round(float(self.early_slider.get()) / 10.0) * 10)
        unlock = int(round(float(self.unlock_slider.get()) / 5.0) * 5)
        timeout = int(round(float(self.timeout_slider.get()) / 50.0) * 50)
        attack = int(round(float(self.attack_slider.get())))
        self.early_value.configure(text=str(early) + "ms")
        self.unlock_value.configure(text=str(unlock) + "ms")
        self.timeout_value.configure(text=str(timeout) + "ms")
        self.attack_value.configure(text=str(attack))
        self.params_dirty = True
        self.dirty_label.configure(text="参数已修改，尚未应用到脚本", text_color=COLOR_ORANGE)

    def _collect_params(self):
        return {
            "提前伤害延迟ms": int(round(float(self.early_slider.get()) / 10.0) * 10),
            "伤害后解锁延迟ms": int(round(float(self.unlock_slider.get()) / 5.0) * 5),
            "保护超时ms": int(round(float(self.timeout_slider.get()) / 50.0) * 50),
            "attackIndex": int(round(float(self.attack_slider.get()))),
        }

    def _apply_params_clicked(self):
        if not self.connected or not self.script:
            return
        self.apply_button.configure(state="disabled", text="应用中...")
        threading.Thread(target=self._apply_params_worker, daemon=True).start()

    def _apply_params_worker(self):
        try:
            params = self._collect_params()
            with self.rpc_lock:
                result = self.script.exports_sync.setparams(params)
            msg = result.get("message", str(result)) if isinstance(result, dict) else str(result)
            queued = bool(result.get("queued", False)) if isinstance(result, dict) else False
            self._safe_log("参数应用结果: " + msg)
            self.params_dirty = False
            if queued:
                self._safe_config(self.dirty_label, text="参数已暂存，本次攻击结束后自动应用", text_color=COLOR_ORANGE)
            else:
                self._safe_config(self.dirty_label, text="参数已应用", text_color=COLOR_GREEN)
        except Exception as exc:
            self._safe_log("应用参数失败: " + str(exc))
            self._safe_config(self.dirty_label, text="参数应用失败", text_color=COLOR_RED)
        finally:
            self.after(0, lambda: self.apply_button.configure(state="normal", text="应用参数"))

    def _toggle_feature(self):
        if not self.connected or not self.script:
            self.switch.deselect()
            return
        if self.switch.get():
            self.switch.configure(text="开启")
            threading.Thread(target=self._enable_worker, daemon=True).start()
        else:
            self.switch.configure(text="关闭")
            threading.Thread(target=self._disable_worker, daemon=True).start()

    def _enable_worker(self):
        try:
            params = self._collect_params()
            with self.rpc_lock:
                self.script.exports_sync.setparams(params)
                ok = self.script.exports_sync.enable()
            self._safe_log("开启返回: " + str(ok))
        except Exception as exc:
            self._safe_log("开启失败: " + str(exc))
            self.after(0, self.switch.deselect)
            self.after(0, lambda: self.switch.configure(text="关闭"))

    def _disable_worker(self):
        try:
            with self.rpc_lock:
                ok = self.script.exports_sync.disable()
            self._safe_log("关闭返回: " + str(ok))
        except Exception as exc:
            self._safe_log("关闭失败: " + str(exc))

    def _start_polling(self):
        self.polling = True
        threading.Thread(target=self._poll_loop, daemon=True).start()

    def _stop_polling(self):
        self.polling = False

    def _poll_loop(self):
        while self.polling and self.connected and self.script:
            try:
                with self.rpc_lock:
                    status = self.script.exports_sync.status()
                if isinstance(status, dict):
                    with self.game_state_lock:
                        self.game_state.update(status)
                    self.after(0, self._update_status_ui)
            except frida.InvalidOperationError:
                self._safe_log("脚本已失效")
                self._disconnect()
                return
            except Exception:
                pass
            time.sleep(0.5)

    def _update_status_ui(self):
        with self.game_state_lock:
            enabled = bool(self.game_state.get("已开启", False))
            installed = bool(self.game_state.get("已安装", False))
            guarding = bool(self.game_state.get("正在保护", False))
            damaged = bool(self.game_state.get("当前已出伤害", False))
            right = self.game_state.get("右键进入次数", 0)
            allowed = self.game_state.get("首次放行次数", 0)
            protected = self.game_state.get("过早右键保护次数", 0)
            early = self.game_state.get("提前伤害次数", 0)
            natural = self.game_state.get("自然伤害次数", 0)
            unlock = self.game_state.get("解锁次数", 0)
            dup = self.game_state.get("重复自然伤害观察次数", 0)
        self.enable_text.configure(text="开启" if enabled else "关闭", text_color=COLOR_GREEN if enabled else COLOR_RED)
        self.hook_text.configure(text="已安装" if installed else "未安装", text_color=COLOR_GREEN if installed else COLOR_ORANGE)
        if guarding and not damaged:
            self.guard_text.configure(text="等待伤害", text_color=COLOR_ORANGE)
        elif guarding and damaged:
            self.guard_text.configure(text="等待解锁", text_color=COLOR_ORANGE)
        else:
            self.guard_text.configure(text="可攻击", text_color=COLOR_GREEN)
        self.counter_text.configure(text=(
            "右键: " + str(right)
            + " / 放行: " + str(allowed)
            + " / 保护: " + str(protected)
            + " / 提前伤害: " + str(early)
            + " / 自然伤害: " + str(natural)
            + " / 重复观察: " + str(dup)
            + " / 解锁: " + str(unlock)
        ))

    def _disconnect(self):
        self._stop_polling()
        if self.script:
            try:
                with self.rpc_lock:
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
        self.connected = False
        self._safe_config(self.dot_label, text_color="#888")
        self._safe_config(self.conn_label, text="已断开")
        self._safe_config(self.pid_label, text="")
        self.after(0, self._disable_controls)
        self._safe_log("已断开连接")

    def _on_js_message(self, message, data):
        if message.get("type") == "send":
            payload = message.get("payload")
            if isinstance(payload, dict) and payload.get("type") == "日志":
                level = payload.get("level", "信息")
                module = payload.get("module", "")
                msg = payload.get("message", "")
                self._safe_log("[" + level + "][" + module + "] " + msg)
            else:
                self._safe_log("[JS] " + str(payload))
        elif message.get("type") == "error":
            self._safe_log("[JS错误] " + message.get("description", str(message)))

    def _safe_config(self, widget, **kwargs):
        try:
            self.after(0, lambda: widget.configure(**kwargs))
        except Exception:
            pass

    def _safe_log(self, text):
        try:
            self.after(0, lambda: self._append_log(text))
        except Exception:
            pass

    def _append_log(self, text):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end", "[" + ts + "] " + text + "\n")
        self.log_box.see("end")

    def _clear_log(self):
        self.log_box.delete("1.0", "end")

    def _on_close(self):
        if self.closing:
            return
        self.closing = True
        self._disconnect()
        self.destroy()


if __name__ == "__main__":
    app = FastGunstockSafeUI()
    app.mainloop()
