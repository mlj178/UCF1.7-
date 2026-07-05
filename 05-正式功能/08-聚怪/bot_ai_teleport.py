# -*- coding: utf-8 -*-
"""
bot_ai_teleport.py
简化单功能测试器：只配合 bot_ai_teleport.js 使用。

作用：
1. attach UnityCrossFire.exe
2. 加载 bot_ai_teleport.js
3. 调用 JS RPC：enable / disable / status / cleanup / set_config / probe / teleport

依赖：
pip install frida

可选：
不依赖 customtkinter，使用 Python 标准库 tkinter。
"""

import json
import threading
import traceback
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

try:
    import frida
except Exception:
    frida = None


DEFAULT_PROCESS_NAME = "UnityCrossFire.exe"
DEFAULT_JS_NAME = "bot_ai_teleport.js"


class BotAiTeleportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BOT AI Teleport - JS/PY 简化版")
        self.root.geometry("900x620")

        self.session = None
        self.script = None
        self.exports = None
        self.log_file = Path(__file__).with_name("bot_ai_teleport_runtime_log.txt")

        self.process_var = tk.StringVar(value=DEFAULT_PROCESS_NAME)
        self.js_path_var = tk.StringVar(value=str(Path(__file__).with_name(DEFAULT_JS_NAME)))

        self.x_var = tk.StringVar(value="13.6")
        self.y_var = tk.StringVar(value="14.1")
        self.z_var = tk.StringVar(value="0.1")
        self.batch_var = tk.StringVar(value="64")
        self.ai_first_var = tk.BooleanVar(value=True)
        self.fallback_var = tk.BooleanVar(value=True)
        self.execute_on_update_var = tk.BooleanVar(value=True)
        self.graph_y_offset_var = tk.StringVar(value="0.05")
        self.ground_to_node_var = tk.BooleanVar(value=True)
        self.spread_cluster_var = tk.BooleanVar(value=True)
        self.path_setting_var = tk.BooleanVar(value=False)
        self.restick_airborne_var = tk.BooleanVar(value=True)
        self.monitor_enabled_var = tk.BooleanVar(value=True)
        self.diag_enabled_var = tk.BooleanVar(value=True)
        self.cluster_spacing_var = tk.StringVar(value="0.75")
        self.airborne_threshold_var = tk.StringVar(value="1.8")
        self.monitor_interval_var = tk.StringVar(value="1000")

        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _build_ui(self):
        pad = {"padx": 8, "pady": 5}

        top = ttk.LabelFrame(self.root, text="连接")
        top.pack(fill="x", padx=10, pady=8)

        ttk.Label(top, text="进程名").grid(row=0, column=0, sticky="w", **pad)
        ttk.Entry(top, textvariable=self.process_var, width=32).grid(row=0, column=1, sticky="ew", **pad)

        ttk.Label(top, text="JS路径").grid(row=1, column=0, sticky="w", **pad)
        ttk.Entry(top, textvariable=self.js_path_var).grid(row=1, column=1, sticky="ew", **pad)
        ttk.Button(top, text="选择JS", command=self.choose_js).grid(row=1, column=2, sticky="ew", **pad)
        ttk.Button(top, text="连接并加载", command=self.attach_and_load).grid(row=0, column=2, sticky="ew", **pad)

        top.grid_columnconfigure(1, weight=1)

        cfg = ttk.LabelFrame(self.root, text="聚怪参数")
        cfg.pack(fill="x", padx=10, pady=8)

        ttk.Label(cfg, text="X").grid(row=0, column=0, sticky="w", **pad)
        ttk.Entry(cfg, textvariable=self.x_var, width=12).grid(row=0, column=1, sticky="w", **pad)
        ttk.Label(cfg, text="Y").grid(row=0, column=2, sticky="w", **pad)
        ttk.Entry(cfg, textvariable=self.y_var, width=12).grid(row=0, column=3, sticky="w", **pad)
        ttk.Label(cfg, text="Z").grid(row=0, column=4, sticky="w", **pad)
        ttk.Entry(cfg, textvariable=self.z_var, width=12).grid(row=0, column=5, sticky="w", **pad)

        ttk.Label(cfg, text="每次处理Bot数(0=全部)").grid(row=1, column=0, sticky="w", **pad)
        ttk.Entry(cfg, textvariable=self.batch_var, width=12).grid(row=1, column=1, sticky="w", **pad)

        ttk.Checkbutton(cfg, text="优先AI Teleport", variable=self.ai_first_var).grid(row=1, column=2, columnspan=2, sticky="w", **pad)
        ttk.Checkbutton(cfg, text="允许Transform兜底", variable=self.fallback_var).grid(row=1, column=4, columnspan=2, sticky="w", **pad)
        ttk.Checkbutton(cfg, text="在Player.Update链路执行", variable=self.execute_on_update_var).grid(row=2, column=0, columnspan=3, sticky="w", **pad)
        ttk.Checkbutton(cfg, text="贴到GraphNode地面", variable=self.ground_to_node_var).grid(row=2, column=3, columnspan=2, sticky="w", **pad)
        ttk.Label(cfg, text="地面Y偏移").grid(row=2, column=5, sticky="w", **pad)
        ttk.Entry(cfg, textvariable=self.graph_y_offset_var, width=8).grid(row=2, column=6, sticky="w", **pad)

        ttk.Checkbutton(cfg, text="分散聚怪", variable=self.spread_cluster_var).grid(row=3, column=0, columnspan=2, sticky="w", **pad)
        ttk.Label(cfg, text="分散间距").grid(row=3, column=2, sticky="w", **pad)
        ttk.Entry(cfg, textvariable=self.cluster_spacing_var, width=8).grid(row=3, column=3, sticky="w", **pad)
        ttk.Checkbutton(cfg, text="立即PathSetting", variable=self.path_setting_var).grid(row=3, column=4, columnspan=2, sticky="w", **pad)
        ttk.Checkbutton(cfg, text="升高后二次贴地", variable=self.restick_airborne_var).grid(row=4, column=0, columnspan=2, sticky="w", **pad)
        ttk.Label(cfg, text="升高阈值").grid(row=4, column=2, sticky="w", **pad)
        ttk.Entry(cfg, textvariable=self.airborne_threshold_var, width=8).grid(row=4, column=3, sticky="w", **pad)
        ttk.Checkbutton(cfg, text="每秒监控日志", variable=self.monitor_enabled_var).grid(row=4, column=4, columnspan=2, sticky="w", **pad)
        ttk.Checkbutton(cfg, text="状态差分诊断", variable=self.diag_enabled_var).grid(row=4, column=6, columnspan=2, sticky="w", **pad)
        ttk.Label(cfg, text="监控ms").grid(row=5, column=0, sticky="w", **pad)
        ttk.Entry(cfg, textvariable=self.monitor_interval_var, width=8).grid(row=5, column=1, sticky="w", **pad)

        actions = ttk.LabelFrame(self.root, text="操作")
        actions.pack(fill="x", padx=10, pady=8)

        buttons = [
            ("开启 enable", self.enable),
            ("探测 probe", self.probe),
            ("聚怪一次 teleport", self.teleport),
            ("状态 status", self.status),
            ("立即监控 monitor", self.monitor_now),
            ("差分诊断 diag", self.diag_now),
            ("关闭 disable", self.disable),
            ("清理 cleanup", self.cleanup),
        ]
        for i, (text, cmd) in enumerate(buttons):
            ttk.Button(actions, text=text, command=cmd).grid(row=0, column=i, sticky="ew", **pad)
            actions.grid_columnconfigure(i, weight=1)

        log_frame = ttk.LabelFrame(self.root, text="日志")
        log_frame.pack(fill="both", expand=True, padx=10, pady=8)

        self.log_text = tk.Text(log_frame, wrap="word")
        self.log_text.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scroll.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=scroll.set)

    def log(self, msg):
        text = str(msg)
        self.log_text.insert("end", text + "\n")
        self.log_text.see("end")
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ") + text + "\n")
        except Exception:
            pass
        self.root.update_idletasks()

    def choose_js(self):
        path = filedialog.askopenfilename(
            title="选择 bot_ai_teleport.js",
            filetypes=[("JavaScript", "*.js"), ("All files", "*.*")]
        )
        if path:
            self.js_path_var.set(path)

    def on_message(self, message, data):
        try:
            if message.get("type") == "send":
                payload = message.get("payload")
                self.log("[JS] " + self.format_result(payload))
            elif message.get("type") == "error":
                self.log("[JS ERROR] " + str(message))
            else:
                self.log("[JS MSG] " + str(message))
        except Exception:
            self.log(traceback.format_exc())

    def attach_and_load(self):
        self.run_threaded(self._attach_and_load)

    def attach_by_name_or_pid(self, process_name):
        """
        如果存在多个 UnityCrossFire.exe，frida.attach("UnityCrossFire.exe") 会报 ambiguous name。
        这里自动枚举同名进程，选择 PID 最大的一个，并把候选 PID 写进日志。
        也可以直接在进程名输入框里填 PID。
        """
        if process_name.isdigit():
            pid = int(process_name)
            self.log(f"attach pid: {pid}")
            return frida.attach(pid)

        device = frida.get_local_device()
        matches = []
        try:
            for p in device.enumerate_processes():
                if p.name.lower() == process_name.lower():
                    matches.append(p)
        except Exception:
            matches = []

        if len(matches) == 1:
            self.log(f"attach: {matches[0].name} pid={matches[0].pid}")
            return device.attach(matches[0].pid)

        if len(matches) > 1:
            matches_sorted = sorted(matches, key=lambda p: p.pid)
            info = ", ".join([f"{p.name}(pid={p.pid})" for p in matches_sorted])
            chosen = matches_sorted[-1]
            self.log("检测到多个同名进程：" + info)
            self.log(f"自动选择 PID 最大的进程：{chosen.pid}")
            return device.attach(chosen.pid)

        self.log(f"attach by name: {process_name}")
        return frida.attach(process_name)

    def _attach_and_load(self):
        if frida is None:
            messagebox.showerror("缺少依赖", "没有安装 frida，请先运行：pip install frida")
            return

        process_name = self.process_var.get().strip() or DEFAULT_PROCESS_NAME
        js_path = Path(self.js_path_var.get().strip())

        if not js_path.exists():
            messagebox.showerror("JS不存在", f"找不到JS文件：{js_path}")
            return

        try:
            self.log(f"attach request: {process_name}")
            self.session = self.attach_by_name_or_pid(process_name)

            js_code = js_path.read_text(encoding="utf-8")
            self.script = self.session.create_script(js_code)
            self.script.on("message", self.on_message)
            self.script.load()

            self.exports = getattr(self.script, "exports_sync", None)
            if self.exports is None:
                self.exports = self.script.exports

            self.log("JS loaded OK，现在可以点击 enable / probe / teleport。")
            self.log(f"运行日志会同步写入：{self.log_file}")
            self.status()
        except Exception:
            self.log(traceback.format_exc())
            messagebox.showerror("连接失败", "attach或加载JS失败，详情看日志。")

    def config(self):
        return {
            "target": {
                "x": float(self.x_var.get()),
                "y": float(self.y_var.get()),
                "z": float(self.z_var.get()),
            },
            "batchSize": int(float(self.batch_var.get())),
            "processAllOnRpc": True,
            "syncBotPathFields": True,
            "aiFirst": bool(self.ai_first_var.get()),
            "transformFallback": bool(self.fallback_var.get()),
            "groundToNearestNode": bool(self.ground_to_node_var.get()),
            "useGraphNodeXZ": False,
            "graphYOffset": float(self.graph_y_offset_var.get()),
            "writeNativeTransformCache": False,
            "positionDebug": True,
            "spreadCluster": bool(self.spread_cluster_var.get()),
            "clusterSpacing": float(self.cluster_spacing_var.get()),
            "clusterMaxRadius": 4.2,
            "pathSettingAfterTeleport": bool(self.path_setting_var.get()),
            "verifyAfterMs": 600,
            "airborneThreshold": float(self.airborne_threshold_var.get()),
            "restickAirborne": bool(self.restick_airborne_var.get()),
            "maxRegroundPerBot": 1,
            "monitorEnabled": bool(self.monitor_enabled_var.get()),
            "monitorIntervalMs": int(float(self.monitor_interval_var.get())),
            "monitorMaxBots": 64,
            "monitorDetail": True,
            "driftThreshold": 2.0,
            "diagEnabled": bool(self.diag_enabled_var.get()),
            "diagMaxBots": 64,
            "diagDetailLimit": 64,
            "executeOnPlayerUpdate": bool(self.execute_on_update_var.get()),
        }

    def require_exports(self):
        if self.exports is None:
            self.log("JS还没有加载：请先点击“连接并加载”，等日志出现 JS loaded OK 后再操作。")
            return False
        return True

    def call_rpc(self, name, *args):
        if not self.require_exports():
            return {"ok": False, "error": "js_not_loaded"}
        try:
            fn = getattr(self.exports, name)
        except AttributeError:
            fn = getattr(self.exports, name.replace("_", ""))
        return fn(*args)

    def enable(self):
        self.run_threaded(lambda: self._call_with_config("enable"))

    def disable(self):
        self.run_threaded(lambda: self._call_simple("disable"))

    def cleanup(self):
        self.run_threaded(lambda: self._call_simple("cleanup"))

    def status(self):
        self.run_threaded(lambda: self._call_simple("status"))

    def probe(self):
        self.run_threaded(lambda: self._call_with_config("probe"))

    def monitor_now(self):
        def job():
            cfg = self.config()
            self.call_rpc("set_config", cfg)
            try:
                result = self.call_rpc("monitor_now")
            except Exception:
                result = self.call_rpc("monitornow")
            self.log("monitor_now => " + self.format_result(result))
        self.run_threaded(job)

    def diag_now(self):
        def job():
            cfg = self.config()
            self.call_rpc("set_config", cfg)
            try:
                result = self.call_rpc("diag_now")
            except Exception:
                result = self.call_rpc("diagnow")
            self.log("diag_now => " + self.format_result(result))
        self.run_threaded(job)

    def teleport(self):
        def job():
            cfg = self.config()
            self.call_rpc("set_config", cfg)
            result = self.call_rpc("teleport", cfg["target"])
            self.log("teleport => " + self.format_result(result))
        self.run_threaded(job)

    def _call_simple(self, name):
        result = self.call_rpc(name)
        self.log(f"{name} => " + self.format_result(result))

    def _call_with_config(self, name):
        cfg = self.config()
        self.call_rpc("set_config", cfg)
        result = self.call_rpc(name)
        self.log(f"{name} => " + self.format_result(result))

    def format_result(self, obj):
        try:
            return json.dumps(obj, ensure_ascii=False, indent=2)
        except Exception:
            return str(obj)

    def run_threaded(self, fn):
        def wrapper():
            try:
                fn()
            except Exception:
                self.log(traceback.format_exc())
        threading.Thread(target=wrapper, daemon=True).start()

    def on_close(self):
        try:
            if self.exports is not None:
                try:
                    self.exports.cleanup()
                except Exception:
                    pass
            if self.session is not None:
                try:
                    self.session.detach()
                except Exception:
                    pass
        finally:
            self.root.destroy()


def main():
    root = tk.Tk()
    app = BotAiTeleportApp(root)
    app.log("启动完成：先进入游戏/房间，再点击“连接并加载”。")
    root.mainloop()


if __name__ == "__main__":
    main()
