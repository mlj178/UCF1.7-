"""角色变身的四按钮单功能测试 UI。"""

from pathlib import Path
import queue
import threading

import customtkinter as ctk
import frida
import psutil


FEATURE_ID = "role_transform"
PROCESS_NAME = "UnityCrossFire.exe"
SCRIPT_PATH = Path(__file__).with_name("AAAAA-role_transform_min.js")
ROLE_ACTIONS = {
    "local_hero": "本地玩家：选择英雄",
    "local_terminator": "本地玩家：选择超级终结者",
    "bot_hero": "所有 Bot：随机英雄",
    "bot_terminator": "所有 Bot：随机超级终结者",
}


class RoleTransformApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("多人生化角色变身")
        self.geometry("620x470")
        self.session = None
        self.script = None
        self.connected = False
        self.connecting = False
        self.rpc_busy = False
        self.closing = False
        self.rpc_lock = threading.Lock()
        self.ui_queue = queue.Queue()

        ctk.CTkLabel(
            self,
            text="多人生化角色变身",
            font=("Microsoft YaHei", 20, "bold"),
        ).pack(pady=(16, 4))
        self.connection_label = ctk.CTkLabel(
            self, text="等待 UnityCrossFire.exe 启动..."
        )
        self.connection_label.pack(pady=(0, 10))

        controls = ctk.CTkFrame(self)
        controls.pack(fill="x", padx=18, pady=6)
        for action, label in ROLE_ACTIONS.items():
            ctk.CTkButton(
                controls,
                text=label,
                command=lambda selected=action: self.trigger_action(selected),
            ).pack(fill="x", padx=16, pady=5)

        ctk.CTkButton(self, text="读取状态", command=self.status).pack(pady=6)
        self.log_box = ctk.CTkTextbox(self, height=190)
        self.log_box.pack(fill="both", expand=True, padx=18, pady=(8, 16))
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.after(100, self._drain_ui_queue)
        self._schedule_connect()

    def log(self, text):
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")

    def _post(self, event, *args):
        self.ui_queue.put((event, args))

    def _drain_ui_queue(self):
        try:
            while True:
                event, args = self.ui_queue.get_nowait()
                if event == "waiting":
                    self.connection_label.configure(text=args[0])
                elif event == "connected":
                    self._on_connected(*args)
                elif event == "connect_error":
                    self.connection_label.configure(text="连接失败，正在重试...")
                    self.log("连接失败: " + str(args[0]))
                elif event == "retry_connect":
                    self.after(1200, self._schedule_connect)
                elif event == "log":
                    self.log(args[0])
                elif event == "rpc_done":
                    self.rpc_busy = False
                    self.log(args[0])
                elif event == "rpc_error":
                    self.rpc_busy = False
                    self.log("操作失败: " + str(args[0]))
                elif event == "destroy":
                    self.destroy()
                    return
        except queue.Empty:
            pass
        if not self.closing:
            self.after(100, self._drain_ui_queue)

    @staticmethod
    def _find_game_pid():
        wanted = PROCESS_NAME.lower()
        for process in psutil.process_iter(["pid", "name"]):
            try:
                if (process.info.get("name") or "").lower() == wanted:
                    return process.info["pid"]
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None

    def _schedule_connect(self):
        if self.closing or self.connected or self.connecting:
            return
        self.connecting = True
        threading.Thread(target=self._connect_worker, daemon=True).start()

    def _connect_worker(self):
        session = None
        script = None
        try:
            pid = self._find_game_pid()
            if pid is None:
                self._post("waiting", "等待 UnityCrossFire.exe 启动...")
                return
            self._post("waiting", "正在连接游戏，PID {}...".format(pid))
            session = frida.attach(pid)
            source = SCRIPT_PATH.read_text(encoding="utf-8")
            script = session.create_script(source)
            script.on("message", self.on_message)
            script.load()
            if self.closing:
                self._safe_detach(script, session)
                return
            with self.rpc_lock:
                if self.closing:
                    self._safe_detach(script, session)
                    return
                self.session = session
                self.script = script
                self.connected = True
            self._post("connected", pid)
        except Exception as exc:
            self._post("connect_error", exc)
        finally:
            self.connecting = False
            if not self.closing and not self.connected:
                self._post("retry_connect")

    def _on_connected(self, pid):
        if self.closing:
            return
        self.connection_label.configure(
            text="已连接 UnityCrossFire.exe，PID {}".format(pid)
        )
        self.log("脚本已加载，正在安装主线程动作钩子")
        self._run_rpc("enable")

    def on_message(self, message, _data):
        if message.get("type") == "send":
            payload = message.get("payload", {})
            self._post(
                "log",
                "[{}] {}".format(
                    payload.get("level", "info"),
                    payload.get("message", payload),
                ),
            )
        elif message.get("type") == "error":
            self._post("log", str(message))

    def trigger_action(self, action):
        if self.connected:
            self._run_rpc("trigger", action)
        else:
            self.connection_label.configure(text="等待连接游戏后执行变身...")
            self._schedule_connect()

    def status(self):
        if self.connected:
            self._run_rpc("status")

    def _run_rpc(self, method, *args):
        if self.rpc_busy or not self.script or self.closing:
            return
        self.rpc_busy = True
        threading.Thread(
            target=self._rpc_worker,
            args=(method, args),
            daemon=True,
        ).start()

    def _rpc_worker(self, method, args):
        try:
            script = self.script
            with self.rpc_lock:
                if self.closing or script is None or script is not self.script:
                    return
                result = getattr(script.exports_sync, method)(*args)
            self._post("rpc_done", "{}: {}".format(method, result))
        except Exception as exc:
            self._post("rpc_error", exc)

    @staticmethod
    def _safe_detach(script, session):
        try:
            if script:
                script.unload()
        except Exception:
            pass
        try:
            if session:
                session.detach()
        except Exception:
            pass

    def close(self):
        if self.closing:
            return
        self.closing = True
        script, session = self.script, self.session
        self.script = None
        self.session = None
        self.connected = False
        threading.Thread(
            target=self._shutdown_worker,
            args=(script, session),
            daemon=True,
        ).start()
        self.destroy()

    def _shutdown_worker(self, script, session):
        try:
            with self.rpc_lock:
                self._safe_detach(script, session)
        except Exception:
            pass


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    RoleTransformApp().mainloop()
