# 多人生化模式 回合特性选择器 v1.3
# pip install customtkinter frida-tools psutil

import customtkinter as ctk
import frida
import threading
import time
import psutil

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ATTRS = {
    0: ("基因变异", "缩短技能冷却时间", "ghost"),
    1: ("末日降临", "首波生化全部作为终结者登场", "ghost"),
    2: ("过度增长", "进化时获得额外HP", "ghost"),
    3: ("硬化", "减少受到的所有伤害", "ghost"),
    4: ("补给防御", "获取补给箱时增加防御力", "ghost"),
    5: ("钢铁利爪", "生化幽灵的攻击力与攻击范围增加", "ghost"),
    6: ("感染经验值", "成功感染后自身攻击力与HP都会增加", "ghost"),
    7: ("沸血", "获取补给箱时获得移速和攻速加成", "ghost"),
    8: ("终结者出现", "额外提供红色补给箱", "ghost"),
    9: ("不死契约", "死亡时出现墓碑，一段时间后复活", "ghost"),
    10: ("救世主", "回合开始时救世主英雄登场", "human"),
    11: ("致命一击", "击杀生化幽灵后攻击力增加", "human"),
    12: ("连发手雷", "提高手雷携带数量和攻击力", "human"),
    13: ("强力补给", "获取补给箱时增加攻击力（可叠加）", "human"),
    14: ("无限弹药", "无限弹药", "human"),
    15: ("快速装弹", "加快佣兵装弹速度", "human"),
    16: ("绝命生还", "所有佣兵均可使用特殊技能", "human"),
    17: ("特工", "所有佣兵均可使用特殊技能", "human"),
    18: ("英雄出现", "额外提供蓝色补给箱", "human"),
    19: ("致命攻击", "适用暴击伤害", "human"),
}

FridaJS = r"""
var base = null;
var ATTR_PTR = {};
var WANTED_GHOST = -1;  // -1表示未选择
var WANTED_HUMAN = -1;  // -1表示未选择
var ACTIVE = false;     // 激活开关
var READY = false;
var modeDestroyed = false;

function rdPtr(a) { try { return a.readPointer(); } catch(e) { return ptr(0); } }
function rdS32(a) { try { return a.readS32(); } catch(e) { return 0; } }

function loadAttrs() {
    try {
        var fn = new NativeFunction(base.add(0xB467A0), 'pointer', []);
        var n4 = fn();
        if (!n4 || n4.isNull()) return false;
        var aa = rdPtr(n4.add(0xD8));
        if (aa.isNull()) return false;
        var attrs = rdPtr(aa.add(0x14));
        if (attrs.isNull()) return false;
        var len = attrs.add(0x0C).readU32();
        ATTR_PTR = {};
        for (var i = 0; i < len && i < 50; i++) {
            var a = rdPtr(attrs.add(0x10 + i*4));
            if (!a.isNull()) ATTR_PTR[rdS32(a.add(0x0C))] = a;
        }
        return Object.keys(ATTR_PTR).length > 0;
    } catch(e) { return false; }
}

function installHooks() {
    Interceptor.attach(base.add(0xB4C420), {
        onEnter: function(args) {
            this._isNano = !args[1].isNull();
        },
        onLeave: function(retval) {
            if (modeDestroyed) return;
            if (!ACTIVE) return;  // 未激活，透传
            
            var id = this._isNano ? WANTED_GHOST : WANTED_HUMAN;
            if (id < 0) return;  // 未选择，透传
            
            var p = ATTR_PTR[id];
            if (p && !p.isNull()) {
                try { retval.replace(p); } catch(e) {}
            }
        }
    });
    Interceptor.attach(base.add(0xB44320), {
        onEnter: function(args) {
            modeDestroyed = true;
            READY = false;
            ACTIVE = false;  // 重置激活状态
            send(JSON.stringify({type:'destroyed'}));
        }
    });
}

var mod = Process.findModuleByName('GameAssembly.dll');
if (!mod) { send(JSON.stringify({type:'error',msg:'未检测到游戏进程'})); }
else {
    base = mod.base;
    var fn = new NativeFunction(base.add(0xB467A0), 'pointer', []);
    var n4 = fn();
    if (!n4 || n4.isNull()) {
        send(JSON.stringify({type:'error',msg:'未进入多人生化模式'}));
    } else if (!loadAttrs()) {
        send(JSON.stringify({type:'error',msg:'未进入多人生化模式房间'}));
    } else {
        installHooks();
        READY = true;
        send(JSON.stringify({type:'ready', ids:Object.keys(ATTR_PTR).sort()}));
    }
}

rpc.exports = {
    set: function(g, h) {
        WANTED_GHOST = g;
        WANTED_HUMAN = h;
        ACTIVE = true;  // 设置时激活
        send(JSON.stringify({type:'set', g:g, h:h}));
    },
    getcurrent: function() {
        if (!READY || modeDestroyed) return JSON.stringify({type:'current',g:-1,h:-1,ok:false});
        try {
            var fn2 = new NativeFunction(base.add(0xB467A0), 'pointer', []);
            var inst = fn2(); if (!inst||inst.isNull()) return JSON.stringify({type:'current',g:-1,h:-1,ok:true});
            var an = rdPtr(inst.add(0xE0)); var ah = rdPtr(inst.add(0xE4));
            return JSON.stringify({type:'current', g:an.isNull()?-1:rdS32(an.add(0x0C)), h:ah.isNull()?-1:rdS32(ah.add(0x0C)), ok:true});
        } catch(e) { return JSON.stringify({type:'current',g:-1,h:-1,ok:true}); }
    },
    healthcheck: function() {
        if (modeDestroyed) return JSON.stringify({type:'dead'});
        try {
            var fn2 = new NativeFunction(base.add(0xB467A0), 'pointer', []);
            var inst = fn2(); if (!inst||inst.isNull()) { modeDestroyed=true;READY=false;return JSON.stringify({type:'dead'});}
            var aa = rdPtr(inst.add(0xD8)); if (aa.isNull()) { modeDestroyed=true;READY=false;return JSON.stringify({type:'dead'});}
            return JSON.stringify({type:'alive'});
        } catch(e) { modeDestroyed=true;READY=false;return JSON.stringify({type:'dead'});}
    }
};
"""

class Nano4TSelector(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("多人生化模式 回合特性选择器 v1.3")
        self.geometry("620x720")
        self.resizable(False, False)
        self.session = None; self.script = None
        self._connecting = False; self._ready = False
        self._lock = threading.Lock(); self._stop = False
        self._wanted_ghost = -1; self._wanted_human = -1  # -1表示未选择
        self._activated = False  # 是否已激活
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # ----- 状态栏 -----
        self.status_frame = ctk.CTkFrame(self, corner_radius=8, fg_color="#2b2b2b")
        self.status_frame.pack(fill="x", padx=12, pady=(12,6))
        self.status_dot = ctk.CTkLabel(self.status_frame, text="⚫", font=("Arial", 18))
        self.status_dot.pack(side="left", padx=(12,4))
        self.status_label = ctk.CTkLabel(self.status_frame, text="等待游戏启动...", font=("Microsoft YaHei", 14))
        self.status_label.pack(side="left", padx=4)
        self.pid_label = ctk.CTkLabel(self.status_frame, text="", font=("Microsoft YaHei", 11), text_color="#888")
        self.pid_label.pack(side="right", padx=12)

        # ----- 当前回合 + 下回合预测 -----
        self.round_frame = ctk.CTkFrame(self, corner_radius=6, fg_color="#1a2a1a")
        self.round_frame.pack(fill="x", padx=12, pady=(2,2))
        self.round_label = ctk.CTkLabel(self.round_frame, text="当前回合: 等待游戏中...",
                                         font=("Microsoft YaHei", 12), text_color="#88aa88")
        self.round_label.pack(padx=10, pady=(6,0))
        self.next_label = ctk.CTkLabel(self.round_frame, text="",
                                        font=("Microsoft YaHei", 11), text_color="#aaccaa")
        self.next_label.pack(padx=10, pady=(0,6))

        # ----- 提示条 -----
        self.hint_frame = ctk.CTkFrame(self, corner_radius=6, fg_color="#2a2a00")
        self.hint_frame.pack(fill="x", padx=12, pady=(2,8))
        self.hint_label = ctk.CTkLabel(self.hint_frame,
            text="① 启动游戏 → ② 选择「多人生化模式」→ ③ 进入房间 → ④ 打开本工具",
            font=("Microsoft YaHei", 11), text_color="#ffcc00", wraplength=580)
        self.hint_label.pack(padx=8, pady=4)

        # ----- 选择区 -----
        sel_frame = ctk.CTkFrame(self, corner_radius=8)
        sel_frame.pack(fill="x", padx=12, pady=4)

        ghost_frame = ctk.CTkFrame(sel_frame, corner_radius=6, fg_color="#3a1a1a")
        ghost_frame.pack(fill="x", padx=8, pady=(8,4))
        ctk.CTkLabel(ghost_frame, text="👻 幽灵方特性", font=("Microsoft YaHei", 14, "bold"),
                     text_color="#ff6666").pack(anchor="w", padx=12, pady=(8,2))
        self.ghost_var = ctk.StringVar(value="9: 不死契约")
        self.ghost_combo = ctk.CTkComboBox(ghost_frame, values=[f"{i}: {ATTRS[i][0]}" for i in range(10)],
                                           variable=self.ghost_var, font=("Microsoft YaHei", 13),
                                           dropdown_font=("Microsoft YaHei", 12), height=34, state="readonly",
                                           command=self._on_ghost_select)
        self.ghost_combo.pack(fill="x", padx=12, pady=(4,2))
        self.ghost_desc = ctk.CTkLabel(ghost_frame, text="效果: " + ATTRS[9][1],
                                       font=("Microsoft YaHei", 11), text_color="#cc8888", wraplength=530)
        self.ghost_desc.pack(anchor="w", padx=12, pady=(2,8))

        human_frame = ctk.CTkFrame(sel_frame, corner_radius=6, fg_color="#1a1a3a")
        human_frame.pack(fill="x", padx=8, pady=(4,8))
        ctk.CTkLabel(human_frame, text="🛡️ 人类方特性", font=("Microsoft YaHei", 14, "bold"),
                     text_color="#6688ff").pack(anchor="w", padx=12, pady=(8,2))
        self.human_var = ctk.StringVar(value="19: 致命攻击")
        self.human_combo = ctk.CTkComboBox(human_frame, values=[f"{i}: {ATTRS[i][0]}" for i in range(10,20)],
                                           variable=self.human_var, font=("Microsoft YaHei", 13),
                                           dropdown_font=("Microsoft YaHei", 12), height=34, state="readonly",
                                           command=self._on_human_select)
        self.human_combo.pack(fill="x", padx=12, pady=(4,2))
        self.human_desc = ctk.CTkLabel(human_frame, text="效果: " + ATTRS[19][1],
                                       font=("Microsoft YaHei", 11), text_color="#8888cc", wraplength=530)
        self.human_desc.pack(anchor="w", padx=12, pady=(2,8))

        # ----- 按钮 -----
        btn_frame = ctk.CTkFrame(self, corner_radius=8)
        btn_frame.pack(fill="x", padx=12, pady=(2,6))
        self.apply_btn = ctk.CTkButton(btn_frame, text="✅ 应用", font=("Microsoft YaHei", 14, "bold"),
                                        height=40, command=self._apply)
        self.apply_btn.pack(side="left", padx=(12,6), pady=10, expand=True)
        self.connect_btn = ctk.CTkButton(btn_frame, text="🔗 连接游戏", font=("Microsoft YaHei", 13),
                                          height=40, command=self._connect, fg_color="#2a6e2a")
        self.connect_btn.pack(side="left", padx=(6,12), pady=10, expand=True)

        # ----- 日志 -----
        log_lbl = ctk.CTkLabel(self, text="── 日志 ──", font=("Microsoft YaHei", 11), text_color="#666")
        log_lbl.pack(anchor="w", padx=16, pady=(2,2))
        self.log_box = ctk.CTkTextbox(self, font=("Consolas", 11), wrap="word", height=180)
        self.log_box.pack(fill="both", padx=12, pady=(2,12), expand=True)
        self.log_box.configure(state="disabled")

        self._set_buttons(False)
        self._log("多人生化模式 回合特性选择器 v1.3")
        self._log("正在检测游戏进程...")

        threading.Thread(target=self._auto_connect_bg, daemon=True).start()
        threading.Thread(target=self._auto_health_bg, daemon=True).start()

    # ============================================================
    # 日志 & UI
    # ============================================================
    def _log(self, msg):
        ts = time.strftime("%H:%M:%S")
        self.after(0, lambda: self._log_ui(ts, msg))
    def _log_ui(self, ts, msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{ts}] {msg}\n")
        self.log_box.see("end"); self.log_box.configure(state="disabled")

    def _set_buttons(self, enabled):
        self.after(0, lambda: self._set_buttons_ui(enabled))
    def _set_buttons_ui(self, enabled):
        c = "#2563eb" if enabled else "#333333"
        self.apply_btn.configure(state="normal" if enabled else "disabled", fg_color=c)

    def _on_ghost_select(self, value):
        gid = int(value.split(":")[0])
        self.ghost_desc.configure(text="效果: " + ATTRS[gid][1])
        # 更新选择的值，但不激活，需要点击"应用"才激活
        self._refresh_next_label()

    def _on_human_select(self, value):
        hid = int(value.split(":")[0])
        self.human_desc.configure(text="效果: " + ATTRS[hid][1])
        # 更新选择的值，但不激活，需要点击"应用"才激活
        self._refresh_next_label()

    def _refresh_next_label(self):
        if self._ready and self._activated:
            g = self._wanted_ghost; h = self._wanted_human
            if g >= 0 and h >= 0:
                self.next_label.configure(
                    text=f"下一回合已锁定: 👻 {ATTRS[g][0]}  |  🛡️ {ATTRS[h][0]}")
            else:
                self.next_label.configure(text="请选择特性并点击「应用」")
        elif self._ready:
            self.next_label.configure(text="请选择特性并点击「应用」")
        else:
            self.next_label.configure(text="")

    def _set_status(self, color, text):
        dot_map = {"green":"🟢","yellow":"🟡","red":"🔴","gray":"⚫"}
        self.status_dot.configure(text=dot_map.get(color,"⚫"))
        self.status_label.configure(text=text)

    def _update_round_label(self, g, h):
        if g >= 0 and h >= 0:
            txt = f"当前回合: 👻 {ATTRS[g][0]}  |  🛡️ {ATTRS[h][0]}"
        elif self._ready:
            txt = "当前回合: 等待回合开始..."
        else:
            txt = "当前回合: 等待进入游戏..."
        self.after(0, lambda: self.round_label.configure(text=txt))

    # ============================================================
    # 进程查找
    # ============================================================
    def _find_pid(self):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and 'unitycrossfire' in proc.info['name'].lower():
                    return proc.info['pid']
            except: pass
        return None

    # ============================================================
    # 后台: 自动连接
    # ============================================================
    def _auto_connect_bg(self):
        time.sleep(2)
        while not self._stop:
            if self._connecting: time.sleep(5); continue
            pid = self._find_pid()
            if pid and not self._ready:
                self._do_connect(pid)
            time.sleep(5)

    def _connect(self):
        if self._connecting: return
        self._cleanup()
        threading.Thread(target=self._connect_bg, daemon=True).start()

    def _connect_bg(self):
        pid = self._find_pid()
        if not pid:
            self._log("⚠ 未检测到游戏进程，请先启动游戏")
            return
        self._do_connect(pid)

    # ============================================================
    # 后台: 健康检查 — 每15秒验证实例是否存活
    # ============================================================
    def _auto_health_bg(self):
        time.sleep(5)
        while not self._stop:
            time.sleep(15)
            if self._ready and self.script:
                try: self.script.exports.healthcheck()
                except: pass

    # ============================================================
    # Frida 连接
    # ============================================================
    def _do_connect(self, pid):
        with self._lock:
            if self._connecting: return
            self._connecting = True
        self._log(f"检测到游戏 PID:{pid}，正在连接...")
        try:
            session = frida.attach(pid)
            script = session.create_script(FridaJS)

            def on_msg(msg, data):
                if msg['type'] != 'send': return
                payload = msg['payload']
                if isinstance(payload, str):
                    try: payload = __import__('json').loads(payload)
                    except: return
                t = payload.get('type','')

                if t == 'ready':
                    ids = payload.get('ids',[])
                    self._ready = True
                    self._set_buttons(True)
                    self._log(f"✅ 已就绪！共 {len(ids)} 种特性")
                    self._log("用法: 下拉选择 → 点击应用 → 下一回合自动生效")
                    self._log("每次切换组合后需重新点「应用」")
                    self._refresh_next_label()
                    self.after(0, lambda p=pid: self._on_connected(p))

                elif t == 'destroyed':
                    self._log("⚠ 检测到退出房间，特性系统已销毁")
                    self._log("  重新进入房间后会自动连接")
                    self._ready = False
                    self._activated = False  # 重置激活状态
                    self._set_buttons(False)
                    self.after(0, lambda: self._set_status("yellow", "已退出房间"))
                    self.next_label.configure(text="")

                elif t == 'dead':
                    if self._ready:
                        self._log("⚠ 模式实例已失效（退出房间或切换模式）")
                        self._ready = False
                        self._activated = False  # 重置激活状态
                        self._set_buttons(False)
                        self.after(0, lambda: self._set_status("yellow", "已退出房间"))
                        self.next_label.configure(text="")

                elif t == 'error':
                    self._ready = False
                    self._set_buttons(False)
                    m = payload['msg']
                    if '未检测到游戏' in m: self._log("⚠ 未检测到游戏进程")
                    elif '未进入多人生化模式' in m:
                        self._log("⚠ 检测到游戏，但尚未进入「多人生化模式」")
                        self._log("  请选择多人生化模式并进入房间")
                    elif '房间' in m:
                        self._log("⚠ 已在多人生化模式菜单，但尚未进入房间，请点击开始游戏")
                    else: self._log(f"❌ {m}")
                    self.after(0, lambda: self._set_status("yellow", "未就绪"))

                elif t == 'set':
                    g = int(payload['g']); h = int(payload['h'])
                    self._wanted_ghost = g; self._wanted_human = h
                    self._activated = True  # 标记为已激活
                    self._log(f"✅ 已锁定: {ATTRS[g][0]} + {ATTRS[h][0]}，下一回合生效")
                    self._refresh_next_label()

                elif t == 'current':
                    self._update_round_label(int(payload['g']), int(payload['h']))

            script.on('message', on_msg)
            script.load()
            self.session = session; self.script = script
        except frida.ProcessNotFoundError:
            self._log("⚠ 游戏进程已退出")
            self.after(0, lambda: self._set_status("red", "未连接"))
        except Exception as e:
            self._log(f"❌ 连接失败: {e}")
            self.after(0, lambda: self._set_status("red", "未连接"))
        finally:
            self._connecting = False

    def _on_connected(self, pid):
        self._set_status("green", "已就绪")
        self.pid_label.configure(text=f"PID: {pid}")
        self.hint_label.configure(text="✅ 已就绪！当前未激活，游戏将正常运行。选择特性后点击「应用」→ 下一回合生效",
                                   text_color="#88ff88")
        self.hint_frame.configure(fg_color="#1a3a1a")

    # ============================================================
    # 应用
    # ============================================================
    def _apply(self):
        if not self._ready:
            self._log("⚠ 尚未就绪，请先进入「多人生化模式」房间")
            return
        try:
            gid = int(self.ghost_var.get().split(":")[0])
            hid = int(self.human_var.get().split(":")[0])
            threading.Thread(target=lambda: self._apply_bg(gid, hid), daemon=True).start()
        except Exception as e:
            self._log(f"❌ 参数错误: {e}")

    def _apply_bg(self, gid, hid):
        try:
            self.script.exports.set(gid, hid)
        except frida.InvalidOperationError:
            self._log("⚠ 连接已断开，请重新进入房间后自动重连")
            self._ready = False; self._set_buttons(False)
            self.after(0, lambda: self._set_status("yellow", "已断开"))
        except Exception as e:
            self._log(f"❌ 应用失败: {e}")

    # ============================================================
    # 清理
    # ============================================================
    def _cleanup(self):
        s = self.script; self.script = None
        ses = self.session; self.session = None
        self._ready = False
        self._set_buttons(False)
        self.next_label.configure(text="")
        if s:
            try: s.unload()
            except: pass
        if ses:
            try: ses.detach()
            except: pass

    def _on_close(self):
        self._stop = True
        self._cleanup()
        self.destroy()

if __name__ == "__main__":
    app = Nano4TSelector()
    app.mainloop()
