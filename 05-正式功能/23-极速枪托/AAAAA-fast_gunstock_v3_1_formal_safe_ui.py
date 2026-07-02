# AAAAA-fast_gunstock_v3_1_formal_safe_ui.py
# 极速枪托 v3.1 正式功能安全版 UI
# 固定参数：100ms / 40ms / 900ms / attackIndex=0
# 不暴露危险参数，不提供预设，不整合 1.8 controller。

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
JS_FILE = os.path.join(BASE_DIR, "AAAAA-fast_gunstock_v3_1_formal_safe.js")
LOG_FILE = os.path.join(BASE_DIR, "fast_gunstock_v3_1_formal_safe_log.txt")
GAME_PROCESS_NAME = "UnityCrossFire.exe"

GREEN = "#2ecc71"
RED = "#e74c3c"
ORANGE = "#f39c12"
BG = "#1a1a2e"
CARD = "#16213e"


class FormalFastGunstockUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("极速枪托 v3.1 正式功能安全版")
        self.geometry("850x780")
        self.minsize(760, 680)

        self.session = None
        self.script = None
        self.connected = False
        self.connecting = False
        self.polling = False
        self.closing = False

        self.rpc_lock = threading.Lock()
        self.game_state = {}
        self.game_state_lock = threading.Lock()

        self._build_ui()
        self._write_log_line("===== 极速枪托 v3.1 正式功能安全版启动 =====")
        self.after(800, self._auto_connect)

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

        ctk.CTkLabel(
            self,
            text="极速枪托 v3.1 正式功能安全版",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).grid(row=0, column=0, padx=18, pady=(16, 2), sticky="ew")

        ctk.CTkLabel(
            self,
            text="固定参数：提前伤害 100ms / 解锁 40ms / 最大保护 900ms / attackIndex 0。安全模式 attach-only，不碰动画。",
            font=ctk.CTkFont(size=12),
            text_color="#aaa",
            wraplength=810,
        ).grid(row=1, column=0, padx=18, pady=(0, 8), sticky="ew")

        top = ctk.CTkFrame(self, corner_radius=8, fg_color=BG)
        top.grid(row=2, column=0, padx=16, pady=4, sticky="ew")
        top.grid_columnconfigure(1, weight=1)

        self.dot = ctk.CTkLabel(top, text="●", font=ctk.CTkFont(size=18), text_color="#888")
        self.dot.grid(row=0, column=0, padx=(12, 4), pady=8)

        self.conn = ctk.CTkLabel(top, text="等待游戏启动...", font=ctk.CTkFont(size=14))
        self.conn.grid(row=0, column=1, padx=4, pady=8, sticky="w")

        self.pid = ctk.CTkLabel(top, text="", font=ctk.CTkFont(size=11), text_color="#888")
        self.pid.grid(row=0, column=2, padx=12, pady=8, sticky="e")

        control = ctk.CTkFrame(self, corner_radius=8, fg_color=CARD)
        control.grid(row=3, column=0, padx=16, pady=4, sticky="ew")
        control.grid_columnconfigure((0, 1, 2), weight=1)

        self.sw = ctk.CTkSwitch(control, text="功能关闭", command=self._toggle, progress_color=GREEN)
        self.sw.grid(row=0, column=0, padx=12, pady=12, sticky="w")
        self.sw.configure(state="disabled")

        self.force_btn = ctk.CTkButton(
            control,
            text="强制恢复状态",
            width=130,
            command=self._force_clicked,
            fg_color="#8e44ad",
            hover_color="#9b59b6",
        )
        self.force_btn.grid(row=0, column=2, padx=12, pady=12, sticky="e")
        self.force_btn.configure(state="disabled")

        fixed = ctk.CTkFrame(self, corner_radius=8, fg_color=BG)
        fixed.grid(row=4, column=0, padx=16, pady=4, sticky="ew")
        fixed.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self._fixed_cell(fixed, 0, 0, "提前伤害", "100ms")
        self._fixed_cell(fixed, 0, 1, "伤害后解锁", "40ms")
        self._fixed_cell(fixed, 0, 2, "最大保护", "900ms")
        self._fixed_cell(fixed, 0, 3, "attackIndex", "0")

        ctk.CTkLabel(
            fixed,
            text="解锁时调用 OnKnifeAttackExit：固定开启；解锁时清 knifeAttackAnim：固定开启。",
            font=ctk.CTkFont(size=12),
            text_color="#ddd",
        ).grid(row=1, column=0, columnspan=4, padx=10, pady=(2, 10), sticky="ew")

        info = ctk.CTkFrame(self, corner_radius=8, fg_color=BG)
        info.grid(row=5, column=0, padx=16, pady=4, sticky="ew")
        info.grid_columnconfigure((0, 1, 2), weight=1)

        self.enabled_text = self._cell(info, 0, 0, "功能状态", "关闭")
        self.hook_text = self._cell(info, 0, 1, "Hook 状态", "未安装")
        self.phase_text = self._cell(info, 0, 2, "当前阶段", "空闲")

        self.count_text = ctk.CTkLabel(
            info,
            text="右键:0 / 放行:0 / 防打断:0 / 提前伤害:0 / 自然:0 / 重复自然:0 / 解锁:0",
            font=ctk.CTkFont(size=11),
            text_color="#aaa",
        )
        self.count_text.grid(row=2, column=0, columnspan=3, padx=8, pady=(4, 8), sticky="ew")

        log_frame = ctk.CTkFrame(self, corner_radius=8)
        log_frame.grid(row=6, column=0, padx=16, pady=(8, 12), sticky="nsew")
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)

        head = ctk.CTkFrame(log_frame, fg_color="transparent")
        head.grid(row=0, column=0, padx=8, pady=(6, 2), sticky="ew")

        ctk.CTkLabel(head, text="运行日志", font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")
        ctk.CTkButton(
            head,
            text="清空",
            width=50,
            height=22,
            fg_color="#555",
            hover_color="#666",
            command=self._clear_log,
        ).pack(side="right")

        self.log_box = ctk.CTkTextbox(log_frame, font=ctk.CTkFont(size=11))
        self.log_box.grid(row=1, column=0, padx=8, pady=(2, 8), sticky="nsew")

        self.protocol("WM_DELETE_WINDOW", self._close)

    def _fixed_cell(self, parent, row, col, title, value):
        box = ctk.CTkFrame(parent, corner_radius=6, fg_color=CARD)
        box.grid(row=row, column=col, padx=8, pady=(10, 4), sticky="ew")
        ctk.CTkLabel(box, text=title, font=ctk.CTkFont(size=11), text_color="#888").pack(pady=(6, 0))
        ctk.CTkLabel(box, text=value, font=ctk.CTkFont(size=14, weight="bold"), text_color=GREEN).pack(pady=(0, 6))

    def _cell(self, parent, row, col, title, value):
        box = ctk.CTkFrame(parent, corner_radius=6, fg_color=CARD)
        box.grid(row=row, column=col, padx=6, pady=8, sticky="ew")
        ctk.CTkLabel(box, text=title, font=ctk.CTkFont(size=11), text_color="#888").pack(pady=(6, 0))
        label = ctk.CTkLabel(box, text=value, font=ctk.CTkFont(size=13, weight="bold"))
        label.pack(pady=(0, 6))
        return label

    def _auto_connect(self):
        if not self.connected and not self.connecting:
            threading.Thread(target=self._find_connect, daemon=True).start()
        if not self.connected and not self.closing:
            self.after(1500, self._auto_connect)

    def _find_pid(self):
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if proc.info["name"] == GAME_PROCESS_NAME:
                    return proc.info["pid"]
            except Exception:
                pass
        return None

    def _find_connect(self):
        pid = self._find_pid()
        if not pid:
            self._safe_cfg(self.conn, text="等待游戏启动...")
            self._safe_cfg(self.dot, text_color="#888")
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
            self.script.on("message", self._on_msg)
            self.script.load()

            self.connected = True
            self.connecting = False

            self._safe_cfg(self.dot, text_color=GREEN)
            self._safe_cfg(self.conn, text="已连接 - " + GAME_PROCESS_NAME)
            self._safe_cfg(self.pid, text="PID: " + str(pid))
            self.after(0, self._enable_ctrl)

            self._safe_log("脚本已加载，可以打开功能。")
            self._start_poll()

        except frida.ProcessNotFoundError:
            self._safe_log("游戏进程已退出")
            self.connecting = False
        except frida.ServerNotStartedError:
            self._safe_log("Frida Server 未运行，请先启动 frida-server")
            self.connecting = False
        except Exception as exc:
            self._safe_log("连接异常: " + str(exc))
            self.connecting = False

    def _enable_ctrl(self):
        for w in [self.sw, self.force_btn]:
            try:
                w.configure(state="normal")
            except Exception:
                pass

    def _disable_ctrl(self):
        for w in [self.sw, self.force_btn]:
            try:
                w.configure(state="disabled")
            except Exception:
                pass
        try:
            self.sw.deselect()
            self.sw.configure(text="功能关闭")
        except Exception:
            pass

    def _force_clicked(self):
        if not self.connected or not self.script:
            return
        threading.Thread(target=self._force_worker, daemon=True).start()

    def _force_worker(self):
        try:
            with self.rpc_lock:
                ok = self.script.exports_sync.forceclear()
            self._safe_log("强制恢复返回: " + str(ok))
        except Exception as exc:
            self._safe_log("强制恢复失败: " + str(exc))

    def _toggle(self):
        if not self.connected or not self.script:
            self.sw.deselect()
            return

        if self.sw.get():
            self.sw.configure(text="功能开启")
            threading.Thread(target=self._enable_worker, daemon=True).start()
        else:
            self.sw.configure(text="功能关闭")
            threading.Thread(target=self._disable_worker, daemon=True).start()

    def _enable_worker(self):
        try:
            with self.rpc_lock:
                ok = self.script.exports_sync.enable()
            self._safe_log("开启返回: " + str(ok))
        except Exception as exc:
            self._safe_log("开启失败: " + str(exc))
            self.after(0, self.sw.deselect)
            self.after(0, lambda: self.sw.configure(text="功能关闭"))

    def _disable_worker(self):
        try:
            with self.rpc_lock:
                ok = self.script.exports_sync.disable()
            self._safe_log("关闭返回: " + str(ok))
        except Exception as exc:
            self._safe_log("关闭失败: " + str(exc))

    def _start_poll(self):
        self.polling = True
        threading.Thread(target=self._poll_loop, daemon=True).start()

    def _stop_poll(self):
        self.polling = False

    def _poll_loop(self):
        while self.polling and self.connected and self.script and not self.closing:
            try:
                with self.rpc_lock:
                    status = self.script.exports_sync.status()
                if isinstance(status, dict):
                    with self.game_state_lock:
                        self.game_state.update(status)
                    self.after(0, self._update_ui)
            except frida.InvalidOperationError:
                self._safe_log("脚本已失效")
                self._disconnect()
                return
            except Exception:
                pass
            time.sleep(0.5)

    def _update_ui(self):
        with self.game_state_lock:
            enabled = bool(self.game_state.get("enabled", False))
            installed = bool(self.game_state.get("installed", False))
            phase = self.game_state.get("phase", "空闲")

            right = self.game_state.get("rightHits", 0)
            allowed = self.game_state.get("firstAllowed", 0)
            guarded = self.game_state.get("guardedRights", 0)
            early = self.game_state.get("earlyDamageCalls", 0)
            natural = self.game_state.get("naturalDamageHits", 0)
            dup = self.game_state.get("duplicateNaturalHits", 0)
            unlocks = self.game_state.get("unlocks", 0)

        self.enabled_text.configure(text="开启" if enabled else "关闭", text_color=GREEN if enabled else RED)
        self.hook_text.configure(text="已安装" if installed else "未安装", text_color=GREEN if installed else ORANGE)
        self.phase_text.configure(text=str(phase), text_color=ORANGE if phase != "空闲" else GREEN)

        self.count_text.configure(
            text=(
                "右键:" + str(right)
                + " / 放行:" + str(allowed)
                + " / 防打断:" + str(guarded)
                + " / 提前伤害:" + str(early)
                + " / 自然:" + str(natural)
                + " / 重复自然:" + str(dup)
                + " / 解锁:" + str(unlocks)
            )
        )

    def _disconnect(self):
        self._stop_poll()

        script = self.script
        session = self.session
        self.script = None
        self.session = None
        self.connected = False

        self._safe_cfg(self.dot, text_color="#888")
        self._safe_cfg(self.conn, text="正在后台断开...")
        self._safe_cfg(self.pid, text="")
        self.after(0, self._disable_ctrl)

        threading.Thread(target=self._disconnect_worker, args=(script, session), daemon=True).start()

    def _disconnect_worker(self, script, session):
        try:
            if script:
                try:
                    script.exports_sync.forceclear()
                except Exception:
                    pass
                try:
                    script.exports_sync.disable()
                except Exception:
                    pass
                try:
                    script.exports_sync.cleanup()
                except Exception:
                    pass
                try:
                    script.unload()
                except Exception:
                    pass
        except Exception:
            pass

        try:
            if session:
                session.detach()
        except Exception:
            pass

        self._safe_log("后台断开完成")
        self._safe_cfg(self.conn, text="已断开")

    def _on_msg(self, message, data):
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

    def _safe_cfg(self, widget, **kwargs):
        try:
            self.after(0, lambda: widget.configure(**kwargs))
        except Exception:
            pass

    def _safe_log(self, text):
        try:
            self.after(0, lambda: self._append_log(text))
        except Exception:
            pass

    def _write_log_line(self, text):
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(text + "\n")
        except Exception:
            pass

    def _append_log(self, text):
        ts = datetime.now().strftime("%H:%M:%S")
        line = "[" + ts + "] " + text
        self.log_box.insert("end", line + "\n")
        self.log_box.see("end")
        self._write_log_line(line)

    def _clear_log(self):
        self.log_box.delete("1.0", "end")
        try:
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                f.write("===== 日志已清空 " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " =====\n")
        except Exception:
            pass

    def _close(self):
        if self.closing:
            return

        self.closing = True
        self._stop_poll()

        script = self.script
        session = self.session
        self.script = None
        self.session = None
        self.connected = False

        threading.Thread(target=self._disconnect_worker, args=(script, session), daemon=True).start()

        try:
            self.after(80, self.destroy)
        except Exception:
            try:
                self.destroy()
            except Exception:
                pass

        def hard_exit():
            try:
                os._exit(0)
            except Exception:
                pass

        timer = threading.Timer(2.0, hard_exit)
        timer.daemon = True
        timer.start()


if __name__ == "__main__":
    app = FormalFastGunstockUI()
    app.mainloop()
