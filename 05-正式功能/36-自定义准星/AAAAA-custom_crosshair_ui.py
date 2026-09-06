import ast, json, pathlib, queue, threading, time, tkinter as tk
from datetime import datetime
import customtkinter as ctk
import frida, psutil

FEATURE_ID = "custom_crosshair"
GAME_PROCESS_NAME = "UnityCrossFire.exe"
SCRIPT_PATH = pathlib.Path(__file__).with_name("AAAAA-custom_crosshair_min.js")
LOG_PATH = pathlib.Path(__file__).with_name("custom_crosshair.log")
PROBE_PATH = pathlib.Path(__file__).with_name("custom_crosshair_probe.json")
DEFAULT_CONFIG = {"r":0.,"g":1.,"b":0.,"a":.9,"scale":1.,"offset_x":0.,"offset_y":0.}

class CustomCrosshairUI(ctk.CTk):
    def __init__(self):
        super().__init__(); self.title("\u81ea\u5b9a\u4e49\u51c6\u661f"); self.geometry("560x650")
        self.session=self.script=None; self.connected=self.closing=self.connecting=False; self.queue=queue.Queue()
        self.vars={k:tk.DoubleVar(value=v) for k,v in DEFAULT_CONFIG.items()}
        ctk.CTkLabel(self,text="\u81ea\u5b9a\u4e49\u51c6\u661f",font=("Microsoft YaHei",20,"bold")).pack(pady=12)
        for label,key,low,high in [("\u7ea2\u8272","r",0,1),("\u7eff\u8272","g",0,1),("\u84dd\u8272","b",0,1),("\u900f\u660e\u5ea6","a",0,1),("\u6574\u4f53\u5927\u5c0f","scale",.2,3),("\u6c34\u5e73\u504f\u79fb","offset_x",-300,300),("\u5782\u76f4\u504f\u79fb","offset_y",-300,300)]:
            row=ctk.CTkFrame(self); row.pack(fill="x",padx=18,pady=3); ctk.CTkLabel(row,text=label,width=80).pack(side="left"); ctk.CTkSlider(row,from_=low,to=high,variable=self.vars[key],command=lambda _:self.push_config()).pack(side="left",fill="x",expand=True,padx=8)
        self.status_label=ctk.CTkLabel(self,text="\u7b49\u5f85\u6e38\u620f\u542f\u52a8..."); self.status_label.pack(pady=8)
        self.probe_button=ctk.CTkButton(self,text="\u8fd0\u884c\u53ea\u8bfb\u63a2\u6d4b",command=self.run_probe,state="disabled"); self.probe_button.pack(pady=4)
        self.enable_button=ctk.CTkButton(self,text="\u5f00\u542f",command=self.enable,state="disabled"); self.enable_button.pack(side="left",padx=50)
        self.disable_button=ctk.CTkButton(self,text="\u5173\u95ed",command=self.disable,state="disabled"); self.disable_button.pack(side="right",padx=50)
        self.analyze_button=ctk.CTkButton(self,text="\u5206\u6790\u6700\u8fd1\u65e5\u5fd7",command=self.analyze_saved_log); self.analyze_button.pack(pady=5)
        self.log_box=ctk.CTkTextbox(self,height=150,wrap="word"); self.log_box.pack(fill="both",expand=True,padx=18,pady=(12,14)); self.log_box.insert("end","\u8fd0\u884c\u65e5\u5fd7\u4f1a\u663e\u793a\u5728\u8fd9\u91cc\u3002\n"); self.log_box.configure(state="disabled")
        self.protocol("WM_DELETE_WINDOW",self.close); self.after(100,self.drain_queue); self.after(300,self.start_connect)
    def config(self): return {k:round(v.get(),3) for k,v in self.vars.items()}
    def find_game_pid(self):
        for p in psutil.process_iter(["pid","name"]):
            try:
                if (p.info.get("name") or "").lower()==GAME_PROCESS_NAME.lower(): return p.info["pid"]
            except (psutil.NoSuchProcess,psutil.AccessDenied): pass
        return None
    def start_connect(self):
        if not self.closing and not self.connected and not self.connecting:
            self.connecting=True; threading.Thread(target=self._connect_worker,daemon=True).start()
    def _connect_worker(self):
        try:
            while not self.closing and not self.connected:
                pid=self.find_game_pid()
                if not pid: self.queue.put(("status","\u7b49\u5f85\u6e38\u620f\u542f\u52a8..."));time.sleep(1);continue
                self.queue.put(("status","\u6b63\u5728\u8fde\u63a5\u6e38\u620f...")); session=frida.attach(pid); session.on("detached",self._on_frida_detached)
                script=session.create_script(SCRIPT_PATH.read_text(encoding="utf-8")); script.on("message",self._on_message); script.load()
                self.session,self.script,self.connected=session,script,True; self.queue.put(("connected",pid));return
        except Exception as e: self.queue.put(("status","\u8fde\u63a5\u5931\u8d25\uff1a"+str(e)));time.sleep(2)
        finally:
            self.connecting=False
            if not self.closing and not self.connected: self.after(100,self.start_connect)
    def _on_frida_detached(self,reason,crash=None): self.connected=False;self.script=self.session=None;self.queue.put(("disconnected",str(reason)))
    def _on_message(self,message,data):
        if message.get("type")=="send":
            payload=message.get("payload",{})
            if isinstance(payload,dict) and payload.get("type")=="log":
                log_message=payload.get("message",""); self.queue.put(("log",log_message))
                if "HUD_Crosshair.Update first hit" in log_message: self.queue.put(("auto_probe",None))
        elif message.get("type")=="error": self.queue.put(("log","JS \u9519\u8bef\uff1a"+(message.get("stack") or message.get("description","unknown"))))
    def drain_queue(self):
        try:
            while True:
                kind,value=self.queue.get_nowait()
                if kind=="status": self.status_label.configure(text=value)
                elif kind=="connected": self.status_label.configure(text=f"\u5df2\u8fde\u63a5\u6e38\u620f (PID {value})");self.enable_button.configure(state="normal");self.disable_button.configure(state="normal");self.probe_button.configure(state="normal");self.append_log(f"\u5df2\u8fde\u63a5 PID {value}\uff0c\u8bf7\u8fdb\u5165\u5bf9\u5c40\u540e\u70b9\u51fb\u300c\u8fd0\u884c\u53ea\u8bfb\u63a2\u6d4b\u300d\u3002")
                elif kind=="log": self.append_log(value)
                elif kind=="auto_probe": self.run_probe()
                else: self.status_label.configure(text="\u8fde\u63a5\u5df2\u65ad\u5f00\uff0c\u6b63\u5728\u91cd\u8bd5...");self.enable_button.configure(state="disabled");self.disable_button.configure(state="disabled");self.probe_button.configure(state="disabled");self.after(1000,self.start_connect)
        except queue.Empty: pass
        if not self.closing:self.after(100,self.drain_queue)
    def push_config(self):
        if self.script and self.connected: threading.Thread(target=lambda:self.script.exports_sync.setconfig(self.config()),daemon=True).start()
    def enable(self):
        if self.script:self.push_config();threading.Thread(target=lambda:self.script.exports_sync.enable(),daemon=True).start()
    def disable(self):
        if self.script:threading.Thread(target=lambda:self.script.exports_sync.disable(),daemon=True).start()
    def append_log(self, message):
        line="[custom_crosshair] "+str(message); timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        with LOG_PATH.open("a", encoding="utf-8") as log_file: log_file.write(f"{timestamp} {line}\n")
        print(line,flush=True)
        self.log_box.configure(state="normal"); self.log_box.insert("end",line+"\n"); self.trim_log_box(); self.log_box.see("end"); self.log_box.configure(state="disabled")
    def trim_log_box(self):
        lines=self.log_box.get("1.0","end-1c").splitlines()
        if len(lines)>200: self.log_box.delete("1.0","end"); self.log_box.insert("end","\n".join(lines[-200:])+"\n")
    def run_probe(self):
        if not self.script or not self.connected: return
        self.append_log("\u6b63\u5728\u8fd0\u884c\u53ea\u8bfb\u63a2\u6d4b...")
        def worker():
            try:
                snapshot=self.script.exports_sync.debugdump(); PROBE_PATH.write_text(json.dumps(snapshot, ensure_ascii=False), encoding="utf-8")
                self.queue.put(("log",f"\u63a2\u6d4b\u5b8c\u6210\uff1aHUD={snapshot.get('hud')}\uff0c\u51fb\u4e2d={snapshot.get('hooks',{}).get('hookHits',0)}\uff0c\u8be6\u60c5\u5df2\u4fdd\u5b58\u5230 custom_crosshair_probe.json"))
            except Exception as e: self.queue.put(("log","\u63a2\u6d4b\u5931\u8d25\uff1a"+str(e)))
        threading.Thread(target=worker,daemon=True).start()
    def analyze_saved_log(self):
        if PROBE_PATH.exists(): probe=json.loads(PROBE_PATH.read_text(encoding="utf-8"))
        elif not LOG_PATH.exists(): self.append_log("\u65e5\u5fd7\u5206\u6790\uff1a\u8fd8\u6ca1\u6709\u751f\u6210\u63a2\u6d4b\u65e5\u5fd7\u3002"); return
        else:
            probes=[]
            for line in LOG_PATH.read_text(encoding="utf-8").splitlines():
                if "probe result: " in line:
                    try: probes.append(ast.literal_eval(line.split("probe result: ",1)[1]))
                    except (SyntaxError, ValueError): pass
            if not probes: self.append_log("\u65e5\u5fd7\u5206\u6790\uff1a\u627e\u4e0d\u5230\u5b8c\u6574\u7684\u63a2\u6d4b\u7ed3\u679c\u3002"); return
            probe=probes[-1]
        hooks=probe.get("hooks",{}); hits=hooks.get("hookHits",0); hud=probe.get("hud","NULL")
        if not probe.get("supported"): conclusion="\u65e5\u5fd7\u5206\u6790\uff1a\u76ee\u6807\u4e0d\u652f\u6301\uff0c\u7f3a\u5c11 GameAssembly.dll \u6216\u8fdb\u7a0b\u4e0d\u662f x86\u3002"
        elif hits == 0 or hud == "NULL": conclusion="\u65e5\u5fd7\u5206\u6790\uff1aHUD_Crosshair \u6ca1\u6709\u547d\u4e2d\uff0c\u5f53\u524d\u5bf9\u5c40\u5e76\u672a\u4f7f\u7528 dump \u4e2d\u7684\u51c6\u661f\u7c7b\uff0c\u6240\u4ee5\u4e0d\u4f1a\u6709\u4efb\u4f55\u6548\u679c\u3002"
        elif not probe.get("horizontal",{}).get("valid") or not probe.get("vertical",{}).get("valid"): conclusion="\u65e5\u5fd7\u5206\u6790\uff1aHUD \u5df2\u547d\u4e2d\uff0c\u4f46\u6a2a\u7ad6\u51c6\u661f\u5b57\u6bb5\u65e0\u6548\uff0c\u9700\u91cd\u65b0\u5b9a\u4f4d\u5f53\u524d\u7248\u672c\u7684\u5b57\u6bb5\u504f\u79fb\u3002"
        else: conclusion="\u65e5\u5fd7\u5206\u6790\uff1aHUD \u548c\u51c6\u661f\u5bf9\u8c61\u90fd\u5df2\u547d\u4e2d\uff0c\u4e0b\u4e00\u6b65\u4f9d\u636e\u65e5\u5fd7\u5b9a\u4f4d\u5199\u5165\u8c03\u7528\u5931\u8d25\u70b9\u3002"
        self.append_log(conclusion)
    def status(self): return self.script.exports_sync.status() if self.script else {"enabled":False}
    def close(self):
        self.closing=True
        try:
            if self.script:self.script.exports_sync.cleanup();self.script.unload()
            if self.session:self.session.detach()
        except Exception:pass
        self.destroy()
if __name__=="__main__":CustomCrosshairUI().mainloop()
