# launcher.py - 终极武器修改启动器 (模块化版本)
# 功能：UI界面启动 Frida 脚本，支持独立功能开关

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import frida
import psutil
import threading
import os
import re

class LauncherUI:
    def __init__(self, root):
        self.root = root
        self.root.title("终极武器修改 - Launcher (模块化)")
        self.root.geometry("750x600")
        self.root.resizable(True, True)
        
        self.session = None
        self.script = None
        self.is_running = False
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="🔫 终极武器修改工具", font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10))
        
        input_frame = ttk.LabelFrame(main_frame, text="配置", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        pid_frame = ttk.Frame(input_frame)
        pid_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(pid_frame, text="进程PID:").pack(side=tk.LEFT)
        self.pid_entry = ttk.Entry(pid_frame, width=20)
        self.pid_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(pid_frame, text="查找进程", command=self.find_process).pack(side=tk.LEFT, padx=5)
        
        self.auto_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(pid_frame, text="自动连接", variable=self.auto_var).pack(side=tk.LEFT, padx=10)
        
        script_frame = ttk.Frame(input_frame)
        script_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(script_frame, text="脚本路径:").pack(side=tk.LEFT)
        self.script_entry = ttk.Entry(script_frame, width=50)
        self.script_entry.pack(side=tk.LEFT, padx=5)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, "AAAAA-speed_gun_final.js")
        self.script_entry.insert(0, script_path)
        
        feature_frame = ttk.LabelFrame(main_frame, text="功能开关", padding="10")
        feature_frame.pack(fill=tk.X, pady=10)
        
        self.feature_vars = {}
        features = [
            ("animSpeed", "动画加速 x10", True),
            ("infiniteFireRate", "无限射速", True),
            ("noRecoil", "无后坐力", True),
            ("noSpread", "无扩散", True),
        ]
        
        row_frame = None
        for i, (key, label, default) in enumerate(features):
            if i % 3 == 0:
                row_frame = ttk.Frame(feature_frame)
                row_frame.pack(fill=tk.X, pady=2)
            
            var = tk.BooleanVar(value=default)
            self.feature_vars[key] = var
            cb = ttk.Checkbutton(row_frame, text=label, variable=var, width=18)
            cb.pack(side=tk.LEFT, padx=10, pady=2)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.start_btn = ttk.Button(btn_frame, text="▶ 启动", command=self.start_script, width=15)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(btn_frame, text="⏹ 停止", command=self.stop_script, width=15, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="清空日志", command=self.clear_log, width=15).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="全选", command=self.select_all_features, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="全不选", command=self.deselect_all_features, width=10).pack(side=tk.LEFT, padx=5)
        
        log_frame = ttk.LabelFrame(main_frame, text="日志输出", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, font=("Consolas", 10))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        if self.auto_var.get():
            self.root.after(1000, self.auto_connect)
            
    def select_all_features(self):
        for var in self.feature_vars.values():
            var.set(True)
            
    def deselect_all_features(self):
        for var in self.feature_vars.values():
            var.set(False)
            
    def find_process(self):
        pid = self._find_pid()
        if pid:
            self.pid_entry.delete(0, tk.END)
            self.pid_entry.insert(0, str(pid))
            self.log(f"[+] 找到游戏进程: PID = {pid}")
        else:
            messagebox.showwarning("提示", "未找到 UnityCrossFire.exe 进程")
            
    def _find_pid(self):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and 'unitycrossfire' in proc.info['name'].lower():
                    return proc.info['pid']
            except:
                pass
        return None
        
    def auto_connect(self):
        if self.is_running:
            return
        pid = self._find_pid()
        if pid:
            self.pid_entry.delete(0, tk.END)
            self.pid_entry.insert(0, str(pid))
            self.log(f"[+] 自动检测到游戏进程: PID = {pid}")
            self.start_script()
        else:
            self.log("[*] 未检测到游戏进程，等待中...")
            if self.auto_var.get():
                self.root.after(3000, self.auto_connect)
                
    def start_script(self):
        pid_str = self.pid_entry.get().strip()
        script_path = self.script_entry.get().strip()
        
        if not pid_str:
            pid = self._find_pid()
            if pid:
                pid_str = str(pid)
                self.pid_entry.delete(0, tk.END)
                self.pid_entry.insert(0, pid_str)
            else:
                messagebox.showwarning("提示", "请输入进程PID或启动游戏")
                return
        
        try:
            pid = int(pid_str)
        except ValueError:
            messagebox.showwarning("提示", "PID 必须是数字")
            return
            
        if not os.path.exists(script_path):
            messagebox.showwarning("提示", "脚本文件不存在")
            return
            
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_var.set("连接中...")
        
        config = {key: var.get() for key, var in self.feature_vars.items()}
        
        thread = threading.Thread(target=self._do_connect, args=(pid, script_path, config), daemon=True)
        thread.start()
        
    def _generate_js_code(self, script_path, config):
        with open(script_path, 'r', encoding='utf-8') as f:
            js_code = f.read()
        
        for key, value in config.items():
            pattern = rf'{key}:\s*(true|false)'
            replacement = f'{key}: {str(value).lower()}'
            js_code = re.sub(pattern, replacement, js_code)
        
        return js_code
        
    def _do_connect(self, pid, script_path, config):
        try:
            self.log(f"[*] 正在连接进程 PID: {pid}...")
            
            js_code = self._generate_js_code(script_path, config)
            
            self.session = frida.attach(pid)
            self.script = self.session.create_script(js_code)
            
            def on_message(msg, data):
                if msg['type'] == 'send':
                    self.log(str(msg['payload']))
                elif msg['type'] == 'log':
                    self.log(msg.get('description', str(msg)))
                    
            self.script.on('message', on_message)
            self.script.load()
            
            self.log("[+] ✅ 已连接到游戏进程！")
            self.log("[+] 已启用功能：")
            for key, var in self.feature_vars.items():
                status = "✅" if var.get() else "❌"
                feature_names = {
                    "animSpeed": "动画加速",
                    "infiniteFireRate": "无限射速",
                    "semiToFullAuto": "半自动→全自动",
                    "noRecoil": "无后坐力",
                    "noSpread": "无扩散",
                    "keepZoom": "狙击镜保持"
                }
                self.log(f"    {status} {feature_names.get(key, key)}")
            self.root.after(0, lambda: self.status_var.set("已连接"))
            
        except frida.ProcessNotFoundError:
            self.log("[-] ❌ 进程不存在或已退出")
            self.root.after(0, self.on_script_end)
        except Exception as e:
            self.log(f"[-] ❌ 连接失败: {e}")
            self.root.after(0, self.on_script_end)
            
    def stop_script(self):
        if self.script:
            try:
                self.script.unload()
            except:
                pass
        if self.session:
            try:
                self.session.detach()
            except:
                pass
        self.script = None
        self.session = None
        self.log("[*] 已断开连接")
        self.on_script_end()
        
    def on_script_end(self):
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("已断开")
        
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
        
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

def main():
    root = tk.Tk()
    app = LauncherUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
