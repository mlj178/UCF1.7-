# isBot 修改器 — Python UI 启动器
# 功能: 将玩家的 ClientData.isBot 修改为 true/false

import customtkinter as ctk
import frida
import threading
import time
import psutil
import os
import sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

JS_PATH = get_resource_path("set_isbot_true.js")


class IsBotModifierApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("isBot 修改器")
        self.geometry("480x400")
        self.resizable(False, False)

        self.session = None
        self.script = None
        self._ready = False
        self._stop = False

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._build_ui()

        threading.Thread(target=self._auto_connect_bg, daemon=True).start()

    def _build_ui(self):
        status_frame = ctk.CTkFrame(self, corner_radius=8, fg_color="#2b2b2b")
        status_frame.pack(fill="x", padx=12, pady=(12, 6))

        self.status_dot = ctk.CTkLabel(status_frame, text="⚫", font=("Arial", 18))
        self.status_dot.pack(side="left", padx=(12, 4))

        self.status_label = ctk.CTkLabel(status_frame, text="等待游戏启动...", font=("Microsoft YaHei", 14))
        self.status_label.pack(side="left", padx=4)

        self.pid_label = ctk.CTkLabel(status_frame, text="", font=("Microsoft YaHei", 11), text_color="#888")
        self.pid_label.pack(side="right", padx=12)

        btn_frame = ctk.CTkFrame(self, corner_radius=8)
        btn_frame.pack(fill="x", padx=12, pady=(12, 4))

        self.modify_btn = ctk.CTkButton(
            btn_frame, text="🤖 修改 isBot = True",
            font=("Microsoft YaHei", 16, "bold"), height=50,
            command=self._modify_isbot,
            fg_color="#dc2626", hover_color="#b91c1c"
        )
        self.modify_btn.pack(fill="x", padx=16, pady=8)

        sub_frame = ctk.CTkFrame(btn_frame, fg_color="transparent")
        sub_frame.pack(fill="x", padx=16, pady=(0, 8))

        self.restore_btn = ctk.CTkButton(
            sub_frame, text="↩️ 恢复 isBot = False",
            font=("Microsoft YaHei", 11), height=28,
            command=self._restore_isbot,
            fg_color="#be185d", hover_color="#9d174d"
        )
        self.restore_btn.pack(side="left", padx=(0, 6))

        self.stop_btn = ctk.CTkButton(
            sub_frame, text="⏹ 关闭", font=("Microsoft YaHei", 11), height=28,
            command=self._stop_isbot,
            fg_color="#555555", hover_color="#333333", width=60
        )
        self.stop_btn.pack(side="left", padx=6)

        self.connect_btn = ctk.CTkButton(
            sub_frame, text="🔗 重连", font=("Microsoft YaHei", 11), height=28,
            command=self._connect,
            fg_color="#2a6e2a", hover_color="#1e5a1e", width=80
        )
        self.connect_btn.pack(side="left", padx=6)

        log_lbl = ctk.CTkLabel(self, text="── 日志 ──", font=("Microsoft YaHei", 11), text_color="#666")
        log_lbl.pack(anchor="w", padx=16, pady=(8, 2))

        self.log_box = ctk.CTkTextbox(self, font=("Consolas", 11), wrap="word", height=200)
        self.log_box.pack(fill="both", padx=12, pady=(2, 12), expand=True)
        self.log_box.configure(state="disabled")

        self._set_buttons(False)
        self._log("isBot 修改器 v2.0")
        self._log("正在检测游戏进程...")

    def _log(self, msg):
        ts = time.strftime("%H:%M:%S")
        self.after(0, lambda: self._log_ui(ts, msg))

    def _log_ui(self, ts, msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{ts}] {msg}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _set_buttons(self, enabled):
        self.after(0, lambda: self._set_buttons_ui(enabled))

    def _set_buttons_ui(self, enabled):
        state = "normal" if enabled else "disabled"
        self.modify_btn.configure(state=state, fg_color="#dc2626" if enabled else "#333333")
        self.restore_btn.configure(state=state)

    def _set_status(self, color, text):
        self.after(0, lambda: self._set_status_ui(color, text))

    def _set_status_ui(self, color, text):
        dot_map = {"green": "🟢", "yellow": "🟡", "red": "🔴", "gray": "⚫"}
        self.status_dot.configure(text=dot_map.get(color, "⚫"))
        self.status_label.configure(text=text)

    def _set_pid(self, pid):
        self.after(0, lambda: self.pid_label.configure(text=f"PID: {pid}"))

    def _on_message(self, message, data):
        try:
            if message.get("type") == "send":
                payload = message.get("payload", {})
                if isinstance(payload, dict):
                    level = payload.get("level", "info")
                    module = payload.get("module", "")
                    msg = payload.get("message", "")
                    icon_map = {"success": "✅", "error": "❌", "info": "", "warn": "⚠️"}
                    icon = icon_map.get(level, "")
                    display = f"{icon} [{module}] {msg}" if icon else f"[{module}] {msg}"
                    self._log(display)
            elif message.get("type") == "error":
                self._log(f"❌ Frida: {message.get('description', '')[:120]}")
        except Exception:
            pass

    def _find_pid(self):
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    name = (proc.info['name'] or '')
                    if name == 'UnityCrossFire.exe':
                        return proc.info['pid']
                except Exception:
                    pass
        except Exception:
            pass
        return None

    def _auto_connect_bg(self):
        try:
            time.sleep(2)
            while not self._stop:
                if self._ready:
                    time.sleep(30)
                    continue
                pid = self._find_pid()
                if pid:
                    self._log(f"检测到游戏进程 PID={pid}")
                    self._connect_to_pid_bg(pid)
                    time.sleep(60)
                else:
                    time.sleep(3)
        except Exception as e:
            self._log(f"自动连接错误: {e}")

    def _connect(self):
        pid = self._find_pid()
        if not pid:
            self._log("❌ 未找到游戏进程")
            return
        threading.Thread(target=self._connect_to_pid_bg, args=(pid,), daemon=True).start()

    def _connect_to_pid_bg(self, pid):
        if self._ready:
            return
        try:
            self._set_pid(pid)
            self._log(f"正在附加到 PID={pid}...")
            self.session = frida.attach(pid)
            self._log(f"✓ Frida 已附加")

            if not os.path.exists(JS_PATH):
                self._log(f"❌ JS 文件不存在")
                self._set_status("red", "JS文件缺失")
                return

            with open(JS_PATH, "r", encoding="utf-8") as f:
                js_code = f.read()

            self.script = self.session.create_script(js_code)
            self.script.on("message", self._on_message)
            self.script.load()

            self._ready = True
            self._set_buttons(True)
            self._set_status("green", "已就绪")
            self._log("✓ 脚本已注入，30ms 轮询保持中")

        except Exception as e:
            self._log(f"❌ 连接失败: {e}")
            self._set_status("red", "连接失败")

    def _modify_isbot(self):
        if not self._ready or not self.script:
            self._log("❌ 脚本未就绪")
            return

        self._log("🤖 设置 isBot = true ...")
        self._set_status("yellow", "修改中")

        def do_modify():
            try:
                ret = self.script.exports.modify()
                self._log(f"modify 返回: {ret}")
                self._set_status("green", "已开启")
            except Exception as e:
                self._log(f"❌ 修改失败: {e}")
                self._set_status("red", "修改失败")

        threading.Thread(target=do_modify, daemon=True).start()

    def _stop_isbot(self):
        if not self._ready or not self.script:
            self._log("❌ 脚本未就绪")
            return

        self._log("⏹ 关闭功能，恢复 isBot = false ...")

        def do_stop():
            try:
                ret = self.script.exports.stop()
                self._log(f"stop 返回: {ret}")
                self._set_status("gray", "已关闭")
            except Exception as e:
                self._log(f"❌ 关闭失败: {e}")
                self._set_status("red", "关闭失败")

        threading.Thread(target=do_stop, daemon=True).start()

    def _restore_isbot(self):
        if not self._ready or not self.script:
            self._log("❌ 脚本未就绪")
            return

        self._log("↩️ 设置 isBot = false ...")
        self._set_status("yellow", "恢复中")

        def do_restore():
            try:
                ret = self.script.exports.restore()
                self._log(f"restore 返回: {ret}")
                self._set_status("yellow", "已恢复")
            except Exception as e:
                self._log(f"❌ 恢复失败: {e}")
                self._set_status("red", "恢复失败")

        threading.Thread(target=do_restore, daemon=True).start()

    def _on_close(self):
        self._stop = True
        def cleanup():
            try:
                if self.script:
                    self.script.unload()
                if self.session:
                    self.session.detach()
            except Exception:
                pass
            self.after(0, self.destroy)
        threading.Thread(target=cleanup, daemon=True).start()


if __name__ == "__main__":
    try:
        app = IsBotModifierApp()
        app.mainloop()
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("按任意键退出...")
