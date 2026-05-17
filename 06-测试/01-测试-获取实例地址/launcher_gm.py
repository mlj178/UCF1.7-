import customtkinter as ctk
import frida
import psutil
import threading
import os
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GameManagerUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("GameManager 静态字段获取工具")
        self.geometry("1000x750")
        self.resizable(True, True)
        
        self.session = None
        self.script = None
        self.is_running = False
        
        self.setup_ui()
        
    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        control_frame = ctk.CTkFrame(self)
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        title_label = ctk.CTkLabel(
            control_frame, 
            text="🎮 GameManager 静态字段获取工具", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky="w")
        
        ctk.CTkLabel(control_frame, text="进程PID:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.pid_entry = ctk.CTkEntry(control_frame, width=150)
        self.pid_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        self.find_btn = ctk.CTkButton(control_frame, text="查找进程", command=self.find_process, width=100)
        self.find_btn.grid(row=1, column=2, padx=5, pady=5)
        
        self.auto_var = ctk.BooleanVar(value=True)
        auto_check = ctk.CTkCheckBox(control_frame, text="自动连接", variable=self.auto_var)
        auto_check.grid(row=1, column=3, padx=10, pady=5)
        
        ctk.CTkLabel(control_frame, text="脚本路径:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.script_entry = ctk.CTkEntry(control_frame, width=600)
        self.script_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, "get_all_instances.js")
        self.script_entry.insert(0, script_path)
        
        btn_frame = ctk.CTkFrame(control_frame)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10, sticky="w")
        
        self.start_btn = ctk.CTkButton(btn_frame, text="▶ 启动", command=self.start_script, width=100)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = ctk.CTkButton(btn_frame, text="⏹ 停止", command=self.stop_script, width=100, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        ctk.CTkButton(btn_frame, text="清空日志", command=self.clear_log, width=100).grid(row=0, column=2, padx=5)
        
        ctk.CTkButton(btn_frame, text="保存结果", command=self.save_result, width=100).grid(row=0, column=3, padx=5)
        
        log_frame = ctk.CTkFrame(self)
        log_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)
        
        tab_label = ctk.CTkLabel(log_frame, text="📋 日志输出", font=ctk.CTkFont(size=14, weight="bold"))
        tab_label.grid(row=0, column=0, pady=5, sticky="w")
        
        self.log_text = ctk.CTkTextbox(log_frame, font=ctk.CTkFont(family="Consolas", size=11))
        self.log_text.grid(row=1, column=0, sticky="nsew")
        
        self.status_var = ctk.StringVar(value="就绪")
        status_bar = ctk.CTkLabel(self, textvariable=self.status_var, anchor="w")
        status_bar.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        if self.auto_var.get():
            self.after(1000, self.auto_connect)
            
    def find_process(self):
        pid = self._find_pid()
        if pid:
            self.pid_entry.delete(0, "end")
            self.pid_entry.insert(0, str(pid))
            self.log(f"[+] 找到游戏进程: PID = {pid}", "success")
        else:
            self.log("[-] 未找到 UnityCrossFire.exe 进程", "error")
            
    def _find_pid(self):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and 'unitycrossfire' in proc.info['name'].lower():
                    return proc.info['pid']
            except:
                pass
        return None
        
    def auto_connect(self):
        if not self.is_running:
            pid = self._find_pid()
            if pid:
                self.pid_entry.delete(0, "end")
                self.pid_entry.insert(0, str(pid))
                self.log(f"[+] 自动找到进程: PID = {pid}", "info")
                
    def start_script(self):
        if self.is_running:
            return
            
        pid_str = self.pid_entry.get().strip()
        if not pid_str:
            self.log("[-] 请输入进程PID", "error")
            return
            
        try:
            pid = int(pid_str)
        except ValueError:
            self.log("[-] PID格式错误", "error")
            return
            
        script_path = self.script_entry.get().strip()
        if not os.path.exists(script_path):
            self.log(f"[-] 脚本文件不存在: {script_path}", "error")
            return
            
        self.is_running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.status_var.set("正在连接...")
        
        thread = threading.Thread(target=self._run_frida, args=(pid, script_path))
        thread.daemon = True
        thread.start()
        
    def _run_frida(self, pid, script_path):
        try:
            self.log(f"[*] 正在连接进程 PID={pid}...", "info")
            self.session = frida.attach(pid)
            
            with open(script_path, 'r', encoding='utf-8') as f:
                script_code = f.read()
                
            self.script = self.session.create_script(script_code)
            self.script.on('message', self._on_message)
            self.script.load()
            
            self.log(f"[+] 成功连接进程 PID={pid}", "success")
            self.status_var.set(f"已连接 PID={pid}")
            
        except Exception as e:
            self.log(f"[-] 连接失败: {e}", "error")
            self.is_running = False
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            self.status_var.set("连接失败")
            
    def _on_message(self, message, data):
        try:
            if isinstance(message, dict):
                if message.get('type') == 'send':
                    payload = message.get('payload', {})
                    if payload.get('type') == 'log':
                        level = payload.get('level', 'info')
                        category = payload.get('category', '')
                        msg = payload.get('message', '')
                        
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        
                        if level == 'error':
                            icon = '❌'
                        elif level == 'success':
                            icon = '✅'
                        elif level == 'warning':
                            icon = '⚠️'
                        else:
                            icon = 'ℹ️'
                        
                        if category == '分类':
                            log_line = f"\n{msg}"
                        elif category == '系统':
                            log_line = f"[{timestamp}] {icon} {msg}"
                        else:
                            log_line = f"[{timestamp}] {icon} [{category:8s}] {msg}"
                            
                        self.log(log_line, level)
                    else:
                        self.log(f"[SEND] {payload}", "info")
                else:
                    self.log(f"[MSG] {message}", "info")
        except Exception as e:
            self.log(f"[ERROR] 消息处理失败: {e}", "error")
            
    def stop_script(self):
        if self.script:
            self.script.unload()
            self.script = None
        if self.session:
            self.session.detach()
            self.session = None
            
        self.is_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_var.set("已停止")
        self.log("[*] 已停止脚本", "info")
        
    def clear_log(self):
        self.log_text.delete("1.0", "end")
        
    def save_result(self):
        content = self.log_text.get("1.0", "end")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        result_file = os.path.join(script_dir, f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(content)
        self.log(f"[+] 结果已保存: {result_file}", "success")
        
    def log(self, message, level="info"):
        def _log():
            self.log_text.insert("end", message + "\n")
            self.log_text.see("end")
            
        self.after(0, _log)

if __name__ == "__main__":
    app = GameManagerUI()
    app.mainloop()
