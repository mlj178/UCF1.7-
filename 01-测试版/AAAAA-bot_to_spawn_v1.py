# Bot 出生点集合器 v1 — 多人生化模式
# 功能: 一键将所有Bot(人机)传送到各自队伍的出生点
# 依赖: pip install customtkinter frida-tools psutil

import customtkinter as ctk
import frida
import threading
import time
import json
import psutil
import os
import sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JS_PATH = os.path.join(SCRIPT_DIR, "AAAAA-bot_to_spawn_v14.js")


class BotToSpawnApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bot 出生点集合器 v49")
        self.geometry("520x460")
        self.resizable(False, False)

        self.session = None
        self.script = None
        self._ready = False
        self._stop = False

        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()

        threading.Thread(target=self._auto_connect_bg, daemon=True).start()

    def _build_ui(self):
        # --- 状态栏 ---
        status_frame = ctk.CTkFrame(self, corner_radius=8, fg_color="#2b2b2b")
        status_frame.pack(fill="x", padx=12, pady=(12, 6))

        self.status_dot = ctk.CTkLabel(status_frame, text="⚫", font=("Arial", 18))
        self.status_dot.pack(side="left", padx=(12, 4))

        self.status_label = ctk.CTkLabel(
            status_frame, text="等待游戏启动...",
            font=("Microsoft YaHei", 14)
        )
        self.status_label.pack(side="left", padx=4)

        self.pid_label = ctk.CTkLabel(
            status_frame, text="",
            font=("Microsoft YaHei", 11), text_color="#888"
        )
        self.pid_label.pack(side="right", padx=12)

        # --- 提示条 ---
        hint_frame = ctk.CTkFrame(self, corner_radius=6, fg_color="#2a2a00")
        hint_frame.pack(fill="x", padx=12, pady=(2, 8))
        hint_label = ctk.CTkLabel(
            hint_frame,
            text="① 启动游戏 → ② 进入任意模式房间 → ③ 点击下方按钮",
            font=("Microsoft YaHei", 11), text_color="#ffcc00", wraplength=440
        )
        hint_label.pack(padx=8, pady=4)

        # --- 主按钮 ---
        btn_frame = ctk.CTkFrame(self, corner_radius=8)
        btn_frame.pack(fill="x", padx=12, pady=(8, 6))

        self.teleport_btn = ctk.CTkButton(
            btn_frame,
            text="📍 集合人机到出生点",
            font=("Microsoft YaHei", 16, "bold"),
            height=50,
            command=self._teleport,
            fg_color="#2563eb",
            hover_color="#1d4ed8"
        )
        self.teleport_btn.pack(fill="x", padx=16, pady=12)

        self.connect_btn = ctk.CTkButton(
            btn_frame,
            text="🔗 连接游戏",
            font=("Microsoft YaHei", 12),
            height=34,
            command=self._connect,
            fg_color="#2a6e2a",
            hover_color="#1e5a1e"
        )
        self.connect_btn.pack(fill="x", padx=16, pady=(0, 10))

        # --- 日志 ---
        log_lbl = ctk.CTkLabel(
            self, text="── 日志 ──",
            font=("Microsoft YaHei", 11), text_color="#666"
        )
        log_lbl.pack(anchor="w", padx=16, pady=(2, 2))

        self.log_box = ctk.CTkTextbox(
            self, font=("Consolas", 11), wrap="word", height=150
        )
        self.log_box.pack(fill="both", padx=12, pady=(2, 12), expand=True)
        self.log_box.configure(state="disabled")

        self._set_buttons(False)
        self._log("Bot 出生点集合器 v49")
        self._log("正在检测游戏进程...")

    # ============================================================
    # 日志 & UI 辅助
    # ============================================================
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
        color = "#2563eb" if enabled else "#333333"
        self.teleport_btn.configure(state=state, fg_color=color)

    def _set_status(self, color, text):
        dot_map = {"green": "🟢", "yellow": "🟡", "red": "🔴", "gray": "⚫"}
        self.status_dot.configure(text=dot_map.get(color, "⚫"))
        self.status_label.configure(text=text)

    # ============================================================
    # 进程查找
    # ============================================================
    def _find_pid(self):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                name = (proc.info['name'] or '').lower()
                if 'unitycrossfire' in name or 'crossfire' in name:
                    return proc.info['pid']
            except Exception:
                pass
        return None

    # ============================================================
    # 自动连接 (后台线程)
    # ============================================================
    def _auto_connect_bg(self):
        time.sleep(3)
        while not self._stop:
            if self._ready:
                time.sleep(30)
                continue
            pid = self._find_pid()
            if pid:
                self._log(f"检测到游戏进程 PID={pid}")
                self.after(0, lambda: self._connect_to_pid(pid))
                time.sleep(60)
            else:
                time.sleep(3)

    def _connect(self):
        pid = self._find_pid()
        if not pid:
            self._log("❌ 未找到游戏进程")
            return
        self._connect_to_pid(pid)

    def _connect_to_pid(self, pid):
        if self._ready:
            return
        try:
            self.pid_label.configure(text=f"PID: {pid}")
            self.session = frida.attach(pid)
            self._log(f"✓ Frida 已附加到 PID={pid}")

            with open(JS_PATH, "r", encoding="utf-8") as f:
                js_code = f.read()

            self.script = self.session.create_script(js_code)
            self.script.on("message", self._on_message)
            self.script.load()

            # 注入后立即启用按钮，不依赖GM/MM消息
            # 在房间大厅即可触发GenerateBotClient补丁
            self._ready = True
            self._set_buttons(True)
            self._set_status("yellow", "脚本已就绪")
            self._log("✓ 脚本已注入，按钮已启用")
            self._log("  → 进房间时自动打补丁(15→30)")
            self._log("  → 进游戏后点击传送")
        except Exception as e:
            self._log(f"❌ 连接失败: {e}")
            self._set_status("red", "连接失败")

    # ============================================================
    # Frida 消息处理
    # ============================================================
    def _on_message(self, message, data):
        if message['type'] == 'error':
            self._log(f"❌ [JS Error] {message.get('stack', message)}")
            return

        if message['type'] == 'send':
            try:
                payload = message.get('payload', '')
                if isinstance(payload, str) and payload.startswith('{'):
                    info = json.loads(payload)
                    msg_type = info.get('t', '') or info.get('type', '')

                    if msg_type == 'done':
                        count = info.get('count', 0)
                        bl = info.get('bl', 0)
                        gr = info.get('gr', 0)
                        dead = info.get('dead', 0)
                        fail = info.get('fail', 0)
                        self._log(f"✅ {info.get('msg', '传送完成')}")
                        self._log(f"   成功: {count} (BL={bl}, GR={gr}) | 死亡跳过: {dead} | 失败: {fail}")
                        self._set_status("green", f"已传送 {count} 个Bot")

                    elif msg_type == 'error':
                        self._log(f"⚠️ {info.get('msg', '')}")

                    elif msg_type == 'gm':
                        addr = info.get('addr', '')
                        mode = info.get('mode', -1)
                        mode_names = {3: '多人生化3人', 4: '多人生化4人', 5: '多人生化6人', 6: '多人生化4人-终结者'}
                        mode_name = mode_names.get(mode, f'未知({mode})')
                        self._log(f"✓ GameManager 已就绪 (模式: {mode_name})")
                        self._ready = True
                        self._set_status("green", "就绪 — 可以传送")
                        self._set_buttons(True)

                    elif msg_type == 'mm':
                        self._log("✓ MapManager 已就绪 (出生点已加载)")

                    elif msg_type == 'patch':
                        status = info.get('s', '')
                        msg = info.get('m', '')
                        if status == 'ok':
                            self._log(f"🔧 [补丁] {msg}")
                            self._set_status("yellow", "Bot补丁已生效")
                        else:
                            self._log(f"⚠️ [补丁] {msg}")
                    else:
                        self._log(str(payload))
                else:
                    self._log(str(payload))
            except Exception:
                self._log(str(message.get('payload', '')))

    # ============================================================
    # 传送按钮
    # ============================================================
    def _teleport(self):
        if not self.script:
            self._log("⚠️ 请先连接游戏")
            return
        try:
            self.script.exports_sync.teleport()
            self._log("📤 已发送传送指令，等待下一帧执行...")
        except Exception as e:
            self._log(f"❌ 传送失败: {e}")

    # ============================================================
    # 关闭
    # ============================================================
    def _on_close(self):
        self._stop = True
        try:
            if self.script:
                self.script.unload()
        except Exception:
            pass
        try:
            if self.session:
                self.session.detach()
        except Exception:
            pass
        self.destroy()


if __name__ == "__main__":
    app = BotToSpawnApp()
    app.mainloop()
