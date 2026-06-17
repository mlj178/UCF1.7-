# Bot 出生点集合器 v24 — Python UI 启动器
# 功能: 一键将所有Bot(人机)传送到佣兵出生点(SP_GR)
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

def get_resource_path(relative_path):
    """获取资源文件路径，支持 PyInstaller 打包"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

JS_PATH = get_resource_path("AAAAA-bot_to_spawn_v24.js")


class BotToSpawnApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bot 集合器 v24 — 佣兵出生点传送")
        self.geometry("560x520")
        self.resizable(False, False)

        self.session = None
        self.script = None
        self._ready = False
        self._stop = False

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._build_ui()

        threading.Thread(target=self._auto_connect_bg, daemon=True).start()

    # ============================================================
    # UI 构建
    # ============================================================
    def _build_ui(self):
        # 状态栏
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

        # 统计信息栏
        info_frame = ctk.CTkFrame(self, corner_radius=6, fg_color="#1a2a1a")
        info_frame.pack(fill="x", padx=12, pady=(2, 6))

        self.info_label = ctk.CTkLabel(
            info_frame,
            text="等待连接...",
            font=("Microsoft YaHei", 11), text_color="#88cc88", wraplength=480
        )
        self.info_label.pack(padx=8, pady=4)

        # 主按钮
        btn_frame = ctk.CTkFrame(self, corner_radius=8)
        btn_frame.pack(fill="x", padx=12, pady=(6, 4))

        self.teleport_btn = ctk.CTkButton(
            btn_frame,
            text="📍 集合所有 BOT 到佣兵出生点",
            font=("Microsoft YaHei", 16, "bold"),
            height=50,
            command=self._teleport,
            fg_color="#2563eb",
            hover_color="#1d4ed8"
        )
        self.teleport_btn.pack(fill="x", padx=16, pady=8)

        # 辅助按钮行
        sub_frame = ctk.CTkFrame(btn_frame, fg_color="transparent")
        sub_frame.pack(fill="x", padx=16, pady=(0, 8))

        self.connect_btn = ctk.CTkButton(
            sub_frame,
            text="🔗 重新连接",
            font=("Microsoft YaHei", 11),
            height=28,
            command=self._connect,
            fg_color="#2a6e2a",
            hover_color="#1e5a1e",
            width=100
        )
        self.connect_btn.pack(side="left", padx=(0, 6))

        self.refresh_btn = ctk.CTkButton(
            sub_frame,
            text="🔄 刷新状态",
            font=("Microsoft YaHei", 11),
            height=28,
            command=self._refresh_status,
            fg_color="#6b21a8",
            hover_color="#581c87",
            width=100
        )
        self.refresh_btn.pack(side="left", padx=6)

        self.diag_btn = ctk.CTkButton(
            sub_frame,
            text="🔍 诊断",
            font=("Microsoft YaHei", 11),
            height=28,
            command=self._run_diag,
            fg_color="#b45309",
            hover_color="#92400e",
            width=80
        )
        self.diag_btn.pack(side="left", padx=6)

        # 日志
        log_lbl = ctk.CTkLabel(
            self, text="── 日志 ──",
            font=("Microsoft YaHei", 11), text_color="#666"
        )
        log_lbl.pack(anchor="w", padx=16, pady=(4, 2))

        self.log_box = ctk.CTkTextbox(
            self, font=("Consolas", 11), wrap="word", height=200
        )
        self.log_box.pack(fill="both", padx=12, pady=(2, 12), expand=True)
        self.log_box.configure(state="disabled")

        self._set_buttons(False)
        self._log("Bot 集合器 v24 — 双路径扫描模式")
        self._log("正在检测游戏进程...")

    # ============================================================
    # 日志 & UI
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

    def _set_info(self, text):
        self.info_label.configure(text=text)

    # ============================================================
    # Frida 消息处理
    # ============================================================
    def _on_message(self, message, data):
        if message.get("type") == "send":
            try:
                payload = json.loads(message["payload"])
                msg_type = payload.get("t")
                if msg_type == "gm":
                    self._log(f"✅ GameManager 已捕获: {payload.get('addr')}")
                elif msg_type == "mm":
                    self._log(f"✅ MapManager 已捕获: {payload.get('addr')}")
                    self._set_info("已就绪 — 等待传送指令")
                    self._set_status("green", "脚本就绪")
                elif msg_type == "done":
                    n = payload.get("n", 0)
                    bots = payload.get("bots", 0)
                    fails = payload.get("fail", 0)
                    info = f"传送 #{n}: {bots} 个 Bot 成功"
                    if fails:
                        info += f" | 失败={fails}"
                    self._log(f"✅ {info}")
                    self._set_info(info)
                    self._set_status("green", "就绪")
                    self._set_buttons(True)
                elif msg_type == "err":
                    self._log(f"⚠️ {payload.get('msg')}")
                # TEMP DEBUG: comment out this block when allPlayers logging is no longer needed.
                elif msg_type == "allplayers":
                    entries = payload.get("entries", [])
                    self._log(
                        f"allPlayers[{payload.get('total', len(entries))}] = "
                        f"[{', '.join(str(entry) for entry in entries)}]"
                    )
                # TEMP DEBUG: comment out this block when Player ClientData logging is no longer needed.
                elif msg_type == "player_clientdata":
                    entries = payload.get("entries", [])
                    self._log(f"Player ClientData[{payload.get('total', len(entries))}]:")
                    for index, entry in enumerate(entries):
                        self._log(
                            f"  #{index} source={entry.get('source')} "
                            f"player={entry.get('player')} "
                            f"clientData={entry.get('clientData')} "
                            f"isBot={entry.get('isBot')}"
                        )
            except json.JSONDecodeError:
                pass
        elif message.get("type") == "error":
            desc = message.get("description", "未知错误")
            self._log(f"❌ Frida 错误: {desc[:100]}")

    # ============================================================
    # 进程查找
    # ============================================================
    def _find_pid(self):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                name = (proc.info['name'] or '').lower()
                if 'unitycrossfire' in name:
                    return proc.info['pid']
            except Exception:
                pass
        return None

    # ============================================================
    # 自动连接 (后台线程)
    # ============================================================
    def _auto_connect_bg(self):
        time.sleep(2)
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

            if not os.path.exists(JS_PATH):
                self._log(f"❌ JS 文件不存在: {JS_PATH}")
                self._set_status("red", "JS文件缺失")
                return

            with open(JS_PATH, "r", encoding="utf-8") as f:
                js_code = f.read()

            self.script = self.session.create_script(js_code)
            self.script.on("message", self._on_message)
            self.script.load()

            self._ready = True
            self._set_buttons(True)
            self._set_status("yellow", "脚本已注入")
            self._set_info("脚本已加载 — 等待 GM/MM 捕获...")
            self._log("✓ v24 脚本已注入, 双路径扫描模式")
            self._log("  → 路径A: allPlayers[30] 扫描")
            self._log("  → 路径B: Bot.Update 实时跟踪")
            self._log("  → 进入房间后自动捕获出生点")

        except Exception as e:
            self._log(f"❌ 连接失败: {e}")
            self._set_status("red", "连接失败")

    # ============================================================
    # 传送
    # ============================================================
    def _teleport(self):
        if not self._ready or not self.script:
            self._log("❌ 脚本未就绪")
            return

        self._set_buttons(False)
        self._set_status("yellow", "传送中...")
        self._set_info("正在传送所有 Bot 到佣兵出生点...")
        self._log("📍 发送传送指令...")

        def do_teleport():
            try:
                result = self.script.exports.teleport()
                self._log(f"  返回: {result}")
            except Exception as e:
                self._log(f"❌ 传送失败: {e}")
                self.after(0, lambda: self._set_buttons(True))
                self.after(0, lambda: self._set_status("red", "传送失败"))

        threading.Thread(target=do_teleport, daemon=True).start()

    # ============================================================
    # 刷新状态
    # ============================================================
    def _refresh_status(self):
        if not self._ready or not self.script:
            self._log("❌ 脚本未就绪")
            return

        def do_status():
            try:
                st = self.script.exports.status()
                self._log(f"📊 状态: GM={st.get('gm')} MM={st.get('mm')} SP={st.get('spawn')}")
                self._log(f"  跟踪 Player={st.get('players')} Bot组件={st.get('bots')}")
                info = f"Player跟踪={st.get('players')} | Bot组件={st.get('bots')}"
                if st.get('gm') and st.get('mm'):
                    self._set_status("green", "就绪")
                self._set_info(info)
            except Exception as e:
                self._log(f"❌ 状态查询失败: {e}")

        threading.Thread(target=do_status, daemon=True).start()

    # ============================================================
    # 诊断
    # ============================================================
    def _run_diag(self):
        if not self._ready or not self.script:
            self._log("❌ 脚本未就绪")
            return

        self._log("🔍 正在诊断...")

        def do_diag():
            try:
                self.script.exports.diag()
                self._log("✓ 诊断完成, 请查看日志")
            except Exception as e:
                self._log(f"❌ 诊断失败: {e}")

        threading.Thread(target=do_diag, daemon=True).start()

    # ============================================================
    # 关闭
    # ============================================================
    def _on_close(self):
        self._stop = True
        try:
            if self.script:
                self.script.unload()
            if self.session:
                self.session.detach()
        except Exception:
            pass
        self.destroy()


if __name__ == "__main__":
    app = BotToSpawnApp()
    app.mainloop()
