import customtkinter as ctk
import threading
import os


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

JS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "get_skill_common.js")


class Launcher(ctk.CTk):
    def __init__(self):
        super().__init__()
        print("[debug] __init__ start")
        self.title("英雄技能无冷却")
        self.geometry("520x520")
        self.minsize(520, 520)

        self.session = None
        self.script = None
        self.connected = False
        self._detect_running = False

        # 重库惰性引用
        self._frida = None
        self._psutil = None

        # 启动前验证 JS 文件
        if not os.path.isfile(JS_PATH):
            print(f"[debug] JS_FILE_NOT_FOUND: {JS_PATH}")

        self._build_ui()
        print("[debug] UI built, scheduling detect...")
        self.after(500, self._start_detect)
        print("[debug] __init__ end")

    @property
    def psutil(self):
        if self._psutil is None:
            import psutil as m
            self._psutil = m
        return self._psutil

    @property
    def frida(self):
        if self._frida is None:
            import frida as m
            self._frida = m
        return self._frida

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self, text="英雄技能无冷却", font=("Arial", 20, "bold")).grid(row=0, column=0, pady=(20, 5))

        main = ctk.CTkFrame(self)
        main.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(2, weight=1)

        sf = ctk.CTkFrame(main)
        sf.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        sf.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(sf, text="游戏状态:", font=("Arial", 13)).grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.status_label = ctk.CTkLabel(sf, text="检测中...", text_color="gray", font=("Arial", 13))
        self.status_label.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        self.connect_btn = ctk.CTkButton(sf, text="连接", width=70, command=self._toggle_connect)
        self.connect_btn.grid(row=0, column=2, padx=5, pady=8)

        wf = ctk.CTkFrame(main)
        wf.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        wf.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(wf, text="技能无冷却:", font=("Arial", 15, "bold")).grid(row=0, column=0, padx=5, pady=15, sticky="w")
        self.cd_switch = ctk.CTkSwitch(wf, text="", command=self._toggle_cd, switch_width=50)
        self.cd_switch.grid(row=0, column=1, padx=5, pady=15, sticky="e")
        self.cd_switch.configure(state="disabled")

        lf = ctk.CTkFrame(main)
        lf.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        lf.grid_rowconfigure(0, weight=1)
        lf.grid_columnconfigure(0, weight=1)
        self.log_box = ctk.CTkTextbox(lf, font=("Consolas", 11))
        self.log_box.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.log_box.configure(state="disabled")

        bf = ctk.CTkFrame(main)
        bf.grid(row=3, column=0, padx=10, pady=(5, 10), sticky="ew")
        ctk.CTkButton(bf, text="清空日志", command=self._clear_log).pack(side="left", padx=5)
        self.pid_label = ctk.CTkLabel(bf, text="", font=("Arial", 10))
        self.pid_label.pack(side="right", padx=5)

    def _log(self, msg):
        try:
            self.log_box.configure(state="normal")
            self.log_box.insert("end", msg + "\n")
            self.log_box.see("end")
            self.log_box.configure(state="disabled")
        except:
            pass

    def _clear_log(self):
        try:
            self.log_box.configure(state="normal")
            self.log_box.delete("1.0", "end")
            self.log_box.configure(state="disabled")
        except:
            pass

    # ── 进程检测（子线程扫描，避免阻塞 UI） ──
    def _start_detect(self):
        if self.connected:
            return
        self._detect_running = True
        self._poll_detect()

    def _poll_detect(self):
        if self.connected:
            self._detect_running = False
            return

        def scan():
            try:
                pid = self._find_pid()
                self.after(0, lambda p=pid: self._on_scan_result(p))
            except Exception as e:
                self.after(0, lambda: self._log(f"[!] 检测异常: {e}"))

        threading.Thread(target=scan, daemon=True).start()

    def _on_scan_result(self, pid):
        if self.connected:
            self._detect_running = False
            return
        if pid:
            self._on_game_found(pid)
            self._detect_running = False
        else:
            self.after(2000, self._poll_detect)

    def _find_pid(self):
        for p in self.psutil.process_iter():
            try:
                if p.name() and "UnityCrossFire" in p.name():
                    return p.pid
            except:
                pass
        return None

    def _on_game_found(self, pid):
        self._update_status("游戏运行中", "#4CAF50", pid)
        if not self.connected:
            self._do_connect(pid)

    def _update_status(self, text, color, pid=None):
        try:
            self.status_label.configure(text=text, text_color=color)
            self.pid_label.configure(text=f"PID: {pid}" if pid else "")
        except:
            pass

    # ── 连接（带超时） ──
    def _toggle_connect(self):
        if self.connected:
            self._disconnect()
        else:
            pid = self._find_pid()
            if pid:
                self._do_connect(pid)
            else:
                self._log("[-] 未找到游戏进程")

    def _do_connect(self, pid):
        self._log(f"[*] 连接进程 PID={pid} ...")
        t = threading.Thread(target=self._connect_task, args=(pid,), daemon=True)
        t.start()

    def _connect_task(self, pid):
        timeout_timer = None
        try:
            session = [None]
            load_ok = [False]
            error_msg = [None]

            def do_attach():
                try:
                    session[0] = self.frida.attach(pid)
                except Exception as e:
                    error_msg[0] = str(e)

            attach_thread = threading.Thread(target=do_attach, daemon=True)
            attach_thread.start()
            attach_thread.join(timeout=5)

            if session[0] is None:
                if error_msg[0]:
                    raise Exception(error_msg[0])
                raise Exception("frida.attach 超时 (5s)")

            with open(JS_PATH, "r", encoding="utf-8") as f:
                code = f.read()
            script = session[0].create_script(code)

            def on_msg(msg, data):
                try:
                    if msg["type"] == "send":
                        p = msg["payload"]
                        if isinstance(p, dict) and p.get("type") == "log":
                            lv = p.get("level", "info")
                            md = p.get("module", "")
                            ms = p.get("message", "")
                            icon = {"success": "[+]", "error": "[-]", "warn": "[!]", "info": "[*]"}
                            text = f"{icon.get(lv, '[*]')} [{md}] {ms}"
                            self.after(0, lambda t=text: self._log(t))
                except:
                    pass

            script.on("message", on_msg)

            # script.load() 超时控制
            def do_load():
                try:
                    script.load()
                    load_ok[0] = True
                except Exception as e:
                    error_msg[0] = str(e)

            load_thread = threading.Thread(target=do_load, daemon=True)
            load_thread.start()
            load_thread.join(timeout=5)

            if not load_ok[0]:
                try:
                    session[0].detach()
                except:
                    pass
                raise Exception(f"script.load 超时或失败: {error_msg[0]}")

            self.session = session[0]
            self.script = script
            self.connected = True
            self.after(0, lambda p=pid: self._on_connected(p))

        except Exception as e:
            self._log(f"[-] 连接失败: {e}")
            self.after(0, lambda: self._update_status("连接失败", "#F44336"))

    def _on_connected(self, pid):
        try:
            self.connect_btn.configure(text="断开")
            self.cd_switch.configure(state="normal")
            self._update_status("已连接", "#4CAF50", pid)
            self._log("[+] 连接成功")
        except:
            pass

    def _disconnect(self):
        try:
            if self.script:
                self.script.unload()
        except:
            pass
        try:
            if self.session:
                self.session.detach()
        except:
            pass
        self.script = None
        self.session = None
        self.connected = False
        try:
            self.cd_switch.configure(state="disabled")
            self.cd_switch.deselect()
            self.connect_btn.configure(text="连接")
            self._update_status("已断开", "gray")
        except:
            pass
        self._log("[*] 已断开")
        self.after(1000, self._start_detect)

    # ── 开关（子线程执行 RPC，不阻塞 UI） ──
    def _toggle_cd(self):
        if not self.connected or not self.script:
            return
        enable = self.cd_switch.get()

        def task():
            try:
                self.script.exports_sync.no_cd(enable)
                self.after(0, lambda: self._log(f"[+] 无冷却 {'开启' if enable else '关闭'}"))
            except Exception as e:
                self.after(0, lambda: self._log(f"[-] 开关失败: {e}"))

        threading.Thread(target=task, daemon=True).start()

    def destroy(self):
        try:
            if self.script:
                self.script.unload()
        except:
            pass
        try:
            if self.session:
                self.session.detach()
        except:
            pass
        super().destroy()


if __name__ == "__main__":
    try:
        Launcher().mainloop()
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("按 Enter 退出...")
