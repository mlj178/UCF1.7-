# 游戏修改器控制台 - 四合一修改器 v1.0
# pip install customtkinter frida psutil pynput

import customtkinter as ctk
import frida
import threading
import time
import psutil
import json
import os
import sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

FRIDA_JS = r"""
(function() {
  'use strict';

  var MAX_LOGS_PER_MODULE = 10;
  var moduleLogCounts = {};

  function sendLog(level, module, message) {
    if (!moduleLogCounts[module]) moduleLogCounts[module] = 0;
    if (moduleLogCounts[module] >= MAX_LOGS_PER_MODULE) return;
    if (module !== '系统' && moduleLogCounts[module] === MAX_LOGS_PER_MODULE - 1) {
      moduleLogCounts[module]++;
      send({ type: 'log', level: 'info', module: module, message: message + ' (后续日志已静默)' });
      return;
    }
    moduleLogCounts[module]++;
    send({ type: 'log', level: level, module: module, message: message });
  }

  function sendStatus(feature, enabled) {
    send({ type: 'status', feature: feature, enabled: enabled });
  }

  function getGameAssembly() {
    try {
      var mod = Process.findModuleByName('GameAssembly.dll');
      if (!mod) {
        sendLog('error', '系统', '未找到 GameAssembly.dll');
        return null;
      }
      sendLog('info', '系统', 'GameAssembly.dll: base=' + mod.base + ' size=' + mod.size);
      return mod;
    } catch(e) { sendLog('error', '系统', '获取模块失败: ' + e.message); return null; }
  }

  // ====================================================================
  // 模块 1: 快刀 v16 (NativeCallback Replace)
  // ====================================================================
  var knifeModule = (function() {
    var enabled = false;
    var currentSpeed = 5.0;
    var isMyPlayer = null;
    var originalGetKnifeSpeed = null;
    var getKnifeSpeedAddr = null;
    var logCount = 0;

    return {
      setSpeed: function(speed) {
        currentSpeed = speed;
        sendLog('info', '快刀', '速度已切换: ' + speed + 'x');
      },
      enable: function() {
        if (enabled) return;
        var mod = getGameAssembly();
        if (!mod) { sendLog('error', '快刀', '无 GameAssembly.dll'); return; }

        var base = mod.base;
        var isMyPlayerAddr = base.add(0xB55FD0);
        getKnifeSpeedAddr = base.add(0xB170A0);

        sendLog('info', '快刀', 'isMyPlayer @ ' + isMyPlayerAddr);
        sendLog('info', '快刀', 'get_KnifeSpeed @ ' + getKnifeSpeedAddr);

        isMyPlayer = new NativeFunction(isMyPlayerAddr, 'bool', ['pointer']);
        originalGetKnifeSpeed = new NativeFunction(getKnifeSpeedAddr, 'float', ['pointer']);

        logCount = 0;

        Interceptor.replace(getKnifeSpeedAddr, new NativeCallback(function(self) {
          try {
            var owner = self.add(0x8).readPointer();
            if (!owner || owner.isNull()) {
              return originalGetKnifeSpeed(self);
            }

            if (isMyPlayer(owner)) {
              logCount++;
              if (logCount <= 10) {
                sendLog('info', '快刀', '[KnifeSpeed] Player detected, returning ' + currentSpeed);
              }
              return currentSpeed;
            }

            return originalGetKnifeSpeed(self);
          } catch(e) {
            sendLog('error', '快刀', 'Error: ' + e.message);
            return originalGetKnifeSpeed(self);
          }
        }, 'float', ['pointer']));

        enabled = true;
        sendLog('success', '快刀', '已启用 (v16 NativeCallback, Speed=' + currentSpeed + 'x)');
        sendStatus('knife', true);
      },
      disable: function() {
        if (!enabled) return;
        if (getKnifeSpeedAddr) {
          try { Interceptor.revert(getKnifeSpeedAddr); } catch(e) {}
        }
        isMyPlayer = null;
        originalGetKnifeSpeed = null;
        getKnifeSpeedAddr = null;
        enabled = false;
        sendLog('info', '快刀', '已禁用');
        sendStatus('knife', false);
      }
    };
  })();

  // ====================================================================
  // 模块 2: 无限时间
  // ====================================================================
  var timeModule = (function() {
    var hooks = [];
    var intervalId = null;
    var enabled = false;
    var modeBaseInstance = null;

    function safeModifyTime(instance, minute, second) {
      try {
        if (!instance || instance.equals(ptr(0))) return false;
        if (instance.compare(ptr(0x10000)) < 0) return false;
        instance.add(0x34).writeS32(minute);
        instance.add(0x38).writeS32(second);
        return true;
      } catch(e) { return false; }
    }

    function readCurrentTime(instance) {
      try {
        if (!instance || instance.equals(ptr(0))) return null;
        var minute = instance.add(0x34).readS32();
        var second = instance.add(0x38).readS32();
        if (minute < 0 || minute > 200 || second < 0 || second > 59) return null;
        return { minute: minute, second: second };
      } catch(e) { return null; }
    }

    return {
      enable: function() {
        if (enabled) return;
        var mod = getGameAssembly();
        if (!mod) { sendLog('error', '无限时间', '无 GameAssembly.dll'); return; }

        var base = mod.base;

        var h1 = Interceptor.attach(base.add(0xAF6930), {
          onEnter: function(args) {
            var instance = args[0];
            if (!modeBaseInstance || !instance.equals(modeBaseInstance)) {
              modeBaseInstance = instance;
              sendLog('info', '无限时间', '新 ModeBase 实例: ' + instance);
            }
            if (modeBaseInstance) {
              var ct = readCurrentTime(modeBaseInstance);
              if (ct && ct.minute < 90) safeModifyTime(modeBaseInstance, 99, 59);
            }
          }
        });
        hooks.push(h1);

        var h2 = Interceptor.attach(base.add(0xAFAA40), {
          onEnter: function() { modeBaseInstance = null; }
        });
        hooks.push(h2);

        var h3 = Interceptor.attach(base.add(0xAEF8A0), {
          onEnter: function(args) {
            var newInstance = args[0];
            if (!modeBaseInstance || !newInstance.equals(modeBaseInstance)) {
              modeBaseInstance = newInstance;
              sendLog('info', '无限时间', 'Nano 新实例: ' + modeBaseInstance);
            }
            var ct = readCurrentTime(modeBaseInstance);
            if (ct && ct.minute < 90) safeModifyTime(modeBaseInstance, 99, 59);
          }
        });
        hooks.push(h3);

        var h4 = Interceptor.attach(base.add(0xAF1920), {
          onEnter: function() { modeBaseInstance = null; }
        });
        hooks.push(h4);

        intervalId = setInterval(function() {
          if (modeBaseInstance) {
            var ct = readCurrentTime(modeBaseInstance);
            if (ct && ct.minute < 90) safeModifyTime(modeBaseInstance, 99, 59);
          }
        }, 1000);

        enabled = true;
        sendLog('success', '无限时间', '已启用 (' + hooks.length + ' Hook + 1s 定时器)');
        sendStatus('time', true);
      },
      disable: function() {
        if (!enabled) return;
        for (var i = 0; i < hooks.length; i++) hooks[i].detach();
        hooks = [];
        if (intervalId) { clearInterval(intervalId); intervalId = null; }
        modeBaseInstance = null; enabled = false;
        sendLog('info', '无限时间', '已禁用');
        sendStatus('time', false);
      }
    };
  })();

  // ====================================================================
  // 模块 3: 无后座力 v14
  // ====================================================================
  var recoilModule = (function() {
    var replacedAddr = null;
    var callbackFunc = null;
    var enabled = false;
    var suppressCount = 0;

    return {
      enable: function() {
        if (enabled) return;
        var mod = getGameAssembly();
        if (!mod) { sendLog('error', '无后座力', '无 GameAssembly.dll'); return; }

        var base = mod.base;
        replacedAddr = base.add(0xB19980);
        sendLog('info', '无后座力', 'Recoil$$OnGunShot @ ' + replacedAddr);

        suppressCount = 0;

        callbackFunc = new NativeCallback(function(recoilThis, methodInfo) {
          suppressCount++;
          try {
            recoilThis.add(0x68).writeFloat(0.0);
            recoilThis.add(0x6C).writeFloat(0.0);
            recoilThis.add(0x70).writeFloat(0.0);
            recoilThis.add(0x74).writeFloat(0.0);
          } catch (e) {}

          if (suppressCount <= 3) {
            sendLog('info', '无后座力', '[Suppress #' + suppressCount + '] ' + recoilThis);
          } else if (suppressCount === 4) {
            sendLog('info', '无后座力', '...suppressing silently');
          }
        }, 'void', ['pointer', 'pointer']);

        try {
          Interceptor.replace(replacedAddr, callbackFunc);
          sendLog('success', '无后座力', '已替换 Recoil.OnGunShot');
        } catch(e) {
          sendLog('error', '无后座力', '替换失败: ' + e.message);
          return;
        }

        enabled = true;
        sendLog('success', '无后座力', 'v14 已启用 (replace OnGunShot + zero 4 fields)');
        sendStatus('recoil', true);
      },
      disable: function() {
        if (!enabled) return;
        if (replacedAddr) { try { Interceptor.revert(replacedAddr); } catch(e) {} }
        callbackFunc = null; replacedAddr = null;
        enabled = false;
        sendLog('info', '无后座力', '已禁用');
        sendStatus('recoil', false);
      }
    };
  })();

  // ====================================================================
  // 模块 4: 无限子弹 plan4
  // ====================================================================
  var ammoModule = (function() {
    var enabled = false;
    var consumeAmmoAddr = null;
    var consumeBaseAddr = null;
    var callbackConsume = null;
    var callbackBase = null;

    return {
      enable: function() {
        if (enabled) return;
        var mod = getGameAssembly();
        if (!mod) { sendLog('error', '无限子弹', '无 GameAssembly.dll'); return; }

        var base = mod.base;
        consumeAmmoAddr = base.add(0xB61140);
        consumeBaseAddr = base.add(0xB6C310);

        sendLog('info', '无限子弹', 'WPN_Gun.ConsumeAmmo @ ' + consumeAmmoAddr);
        sendLog('info', '无限子弹', 'Weapon.ConsumeAmmo @ ' + consumeBaseAddr);

        try {
          callbackConsume = new NativeCallback(function(thisPtr, methodInfo) {
            return 1;
          }, 'bool', ['pointer', 'pointer']);

          Interceptor.replace(consumeAmmoAddr, callbackConsume);
          sendLog('success', '无限子弹', '已替换 WPN_Gun.ConsumeAmmo');
        } catch (e) {
          sendLog('error', '无限子弹', '替换 WPN_Gun.ConsumeAmmo 失败: ' + e.message);
        }

        try {
          callbackBase = new NativeCallback(function(thisPtr, methodInfo) {
            return 1;
          }, 'bool', ['pointer', 'pointer']);

          Interceptor.replace(consumeBaseAddr, callbackBase);
          sendLog('success', '无限子弹', '已替换 Weapon.ConsumeAmmo');
        } catch (e) {
          sendLog('info', '无限子弹', '替换 Weapon.ConsumeAmmo 失败(可忽略): ' + e.message);
        }

        enabled = true;
        sendLog('success', '无限子弹', 'plan4 已启用 (Zero ammo consumption)');
        sendStatus('ammo', true);
      },
      disable: function() {
        if (!enabled) return;
        if (consumeAmmoAddr) { try { Interceptor.revert(consumeAmmoAddr); } catch(e) {} }
        if (consumeBaseAddr) { try { Interceptor.revert(consumeBaseAddr); } catch(e) {} }
        callbackConsume = null;
        callbackBase = null;
        consumeAmmoAddr = null;
        consumeBaseAddr = null;
        enabled = false;
        sendLog('info', '无限子弹', '已禁用');
        sendStatus('ammo', false);
      }
    };
  })();

  // ====================================================================
  // 模块管理
  // ====================================================================
  var modules = {
    knife: knifeModule,
    time: timeModule,
    recoil: recoilModule,
    ammo: ammoModule
  };

  function onToggle(data) {
    var featureName = data.feature;
    var enable = data.enable;

    if (featureName === 'knife_speed') {
      knifeModule.setSpeed(enable);
    } else if (modules[featureName]) {
      var actionText = enable ? '已开启' : '已关闭';
      sendLog('success', '系统', featureName + ' ' + actionText);
      if (enable) {
        modules[featureName].enable();
      } else {
        modules[featureName].disable();
      }
    } else {
      sendLog('error', '系统', '未知功能: ' + featureName);
    }

    recv('toggle', onToggle);
  }

  recv('toggle', onToggle);

  sendLog('info', '系统', '游戏修改器 Agent v7 已加载');
  sendLog('info', '系统', '可用功能: 快刀v16 | 无限时间 | 无后座力v14 | 无限子弹plan4');
  sendLog('info', '系统', '快刀支持速度切换: 3x / 5x / 10x');
  sendLog('info', '系统', '请先附加到游戏进程，然后开启对应功能');
  sendLog('info', '系统', '架构: ' + Process.arch + ', 平台: ' + Process.platform);

  setTimeout(function() { getGameAssembly(); }, 100);
})();
"""

class GameModifierApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("游戏修改器控制台 - 四合一修改器 v1.0")
        self.geometry("700x750")
        self.resizable(False, False)
        self.session = None
        self.script = None
        self._connecting = False
        self._ready = False
        self._lock = threading.Lock()
        self._stop = False
        self._pid = None
        self._features = {
            'knife': False,
            'time': False,
            'recoil': False,
            'ammo': False
        }
        self._knife_speed = 5.0
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()
        self._log("游戏修改器控制台 v1.0")
        self._log("正在检测游戏进程...")

        threading.Thread(target=self._auto_connect_bg, daemon=True).start()

    def _build_ui(self):
        # 状态栏
        self.status_frame = ctk.CTkFrame(self, corner_radius=8, fg_color="#2b2b2b")
        self.status_frame.pack(fill="x", padx=12, pady=(12,6))
        self.status_dot = ctk.CTkLabel(self.status_frame, text="⚫", font=("Arial", 18))
        self.status_dot.pack(side="left", padx=(12,4))
        self.status_label = ctk.CTkLabel(self.status_frame, text="等待游戏启动...", font=("Microsoft YaHei", 14))
        self.status_label.pack(side="left", padx=4)
        self.pid_label = ctk.CTkLabel(self.status_frame, text="", font=("Microsoft YaHei", 11), text_color="#888")
        self.pid_label.pack(side="right", padx=12)

        # 提示条
        self.hint_frame = ctk.CTkFrame(self, corner_radius=6, fg_color="#2a2a00")
        self.hint_frame.pack(fill="x", padx=12, pady=(2,8))
        self.hint_label = ctk.CTkLabel(self.hint_frame,
            text="① 启动游戏 → ② 进入任意模式 → ③ 打开本工具 → ④ 开启功能开关",
            font=("Microsoft YaHei", 11), text_color="#ffcc00", wraplength=650)
        self.hint_label.pack(padx=8, pady=4)

        # 功能选择区
        sel_frame = ctk.CTkFrame(self, corner_radius=8)
        sel_frame.pack(fill="x", padx=12, pady=4)

        # 快刀 + 速度选择
        knife_frame = ctk.CTkFrame(sel_frame, corner_radius=6, fg_color="#3a1a1a")
        knife_frame.pack(fill="x", padx=8, pady=(8,4))
        ctk.CTkLabel(knife_frame, text="🔪 快刀", font=("Microsoft YaHei", 14, "bold"),
                     text_color="#ff6666").pack(side="left", padx=12, pady=8)
        self.knife_speed_var = ctk.StringVar(value="5")
        self.knife_speed_combo = ctk.CTkComboBox(knife_frame, values=["3", "5", "10"],
                                                  variable=self.knife_speed_var, font=("Microsoft YaHei", 12),
                                                  height=30, width=80, state="readonly",
                                                  command=self._on_knife_speed_change)
        self.knife_speed_combo.pack(side="left", padx=8)
        ctk.CTkLabel(knife_frame, text="x 速度", font=("Microsoft YaHei", 11), text_color="#cc8888").pack(side="left")
        self.knife_switch = ctk.CTkSwitch(knife_frame, text="", font=("Microsoft YaHei", 12),
                                           width=50, command=lambda: self._toggle_feature('knife'))
        self.knife_switch.pack(side="right", padx=12)

        # 无限时间
        time_frame = ctk.CTkFrame(sel_frame, corner_radius=6, fg_color="#1a2a1a")
        time_frame.pack(fill="x", padx=8, pady=4)
        ctk.CTkLabel(time_frame, text="⏰ 无限时间", font=("Microsoft YaHei", 14, "bold"),
                     text_color="#66ff66").pack(side="left", padx=12, pady=8)
        self.time_switch = ctk.CTkSwitch(time_frame, text="", font=("Microsoft YaHei", 12),
                                          width=50, command=lambda: self._toggle_feature('time'))
        self.time_switch.pack(side="right", padx=12)

        # 无后座力
        recoil_frame = ctk.CTkFrame(sel_frame, corner_radius=6, fg_color="#1a1a3a")
        recoil_frame.pack(fill="x", padx=8, pady=4)
        ctk.CTkLabel(recoil_frame, text="🎯 无后座力", font=("Microsoft YaHei", 14, "bold"),
                     text_color="#6688ff").pack(side="left", padx=12, pady=8)
        self.recoil_switch = ctk.CTkSwitch(recoil_frame, text="", font=("Microsoft YaHei", 12),
                                            width=50, command=lambda: self._toggle_feature('recoil'))
        self.recoil_switch.pack(side="right", padx=12)

        # 无限子弹
        ammo_frame = ctk.CTkFrame(sel_frame, corner_radius=6, fg_color="#3a2a1a")
        ammo_frame.pack(fill="x", padx=8, pady=(4,8))
        ctk.CTkLabel(ammo_frame, text="🔫 无限子弹", font=("Microsoft YaHei", 14, "bold"),
                     text_color="#ffaa44").pack(side="left", padx=12, pady=8)
        self.ammo_switch = ctk.CTkSwitch(ammo_frame, text="", font=("Microsoft YaHei", 12),
                                          width=50, command=lambda: self._toggle_feature('ammo'))
        self.ammo_switch.pack(side="right", padx=12)

        # 连接按钮
        btn_frame = ctk.CTkFrame(self, corner_radius=8)
        btn_frame.pack(fill="x", padx=12, pady=(2,6))
        self.connect_btn = ctk.CTkButton(btn_frame, text="🔗 连接游戏", font=("Microsoft YaHei", 13),
                                          height=40, command=self._connect, fg_color="#2a6e2a")
        self.connect_btn.pack(fill="x", padx=12, pady=10)

        # 日志
        log_lbl = ctk.CTkLabel(self, text="── 日志 ──", font=("Microsoft YaHei", 11), text_color="#666")
        log_lbl.pack(anchor="w", padx=16, pady=(2,2))
        self.log_box = ctk.CTkTextbox(self, font=("Consolas", 11), wrap="word", height=220)
        self.log_box.pack(fill="both", padx=12, pady=(2,12), expand=True)
        self.log_box.configure(state="disabled")

    def _on_knife_speed_change(self, value):
        try:
            speed = float(value)
            self._knife_speed = speed
            if self._features['knife'] and self.script:
                self._send_toggle('knife_speed', speed)
            self._log(f"快刀速度已切换: {speed}x")
        except:
            pass

    def _toggle_feature(self, feature):
        if not self._ready:
            self._log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            self.after(0, lambda f=feature: self._reset_switch(f))
            return

        enabled = not self._features[feature]
        self._features[feature] = enabled

        if feature == 'knife' and enabled:
            self._send_toggle('knife', True)
            self._send_toggle('knife_speed', self._knife_speed)
        else:
            self._send_toggle(feature, enabled)

        self._update_switch(feature)

    def _reset_switch(self, feature):
        switch_map = {
            'knife': self.knife_switch,
            'time': self.time_switch,
            'recoil': self.recoil_switch,
            'ammo': self.ammo_switch
        }
        switch_map[feature].configure(variable=ctk.BooleanVar(value=False))

    def _update_switch(self, feature):
        enabled = self._features[feature]
        switch_map = {
            'knife': self.knife_switch,
            'time': self.time_switch,
            'recoil': self.recoil_switch,
            'ammo': self.ammo_switch
        }
        switch = switch_map[feature]
        if enabled:
            switch.select()
        else:
            switch.deselect()

    def _send_toggle(self, feature, enable):
        try:
            self.script.post({'type': 'toggle', 'feature': feature, 'enable': enable})
        except Exception as e:
            self._log(f"❌ 发送指令失败: {e}")

    def _log(self, msg):
        ts = time.strftime("%H:%M:%S")
        self.after(0, lambda: self._log_ui(ts, msg))

    def _log_ui(self, ts, msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{ts}] {msg}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _set_status(self, color, text):
        dot_map = {"green":"🟢","yellow":"🟡","red":"🔴","gray":"⚫"}
        self.status_dot.configure(text=dot_map.get(color,"⚫"))
        self.status_label.configure(text=text)

    def _find_pid(self):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and 'unitycrossfire' in proc.info['name'].lower():
                    return proc.info['pid']
            except:
                pass
        return None

    def _auto_connect_bg(self):
        time.sleep(2)
        while not self._stop:
            if self._connecting:
                time.sleep(5)
                continue
            pid = self._find_pid()
            if pid and not self._ready:
                self._do_connect(pid)
            time.sleep(5)

    def _connect(self):
        if self._connecting:
            return
        self._cleanup()
        threading.Thread(target=self._connect_bg, daemon=True).start()

    def _connect_bg(self):
        pid = self._find_pid()
        if not pid:
            self._log("⚠ 未检测到游戏进程，请先启动 UnityCrossFire.exe")
            return
        self._do_connect(pid)

    def _do_connect(self, pid):
        with self._lock:
            if self._connecting:
                return
            self._connecting = True

        self._log(f"检测到游戏 PID:{pid}，正在连接...")
        try:
            session = frida.attach(pid)
            script = session.create_script(FRIDA_JS)

            def on_msg(msg, data):
                if msg['type'] != 'send':
                    return
                payload = msg['payload']
                if isinstance(payload, str):
                    try:
                        payload = json.loads(payload)
                    except:
                        return

                t = payload.get('type', '')

                if t == 'log':
                    level = payload.get('level', 'info')
                    module = payload.get('module', '')
                    message = payload.get('message', '')
                    icon_map = {'success': '✅', 'error': '❌', 'info': 'ℹ️', 'warn': '⚠️'}
                    icon = icon_map.get(level, 'ℹ️')
                    self._log(f"{icon} [{module}] {message}")

                elif t == 'status':
                    feature = payload.get('feature', '')
                    enabled = payload.get('enabled', False)
                    self._features[feature] = enabled
                    self.after(0, lambda f=feature: self._update_feature_button(f))

            script.on('message', on_msg)
            script.load()
            self.session = session
            self.script = script
            self._pid = pid
            self._ready = True

            self._log("✅ 已连接到游戏进程！")
            self._log("点击功能按钮或使用快捷键开启修改")
            self.after(0, lambda p=pid: self._on_connected(p))

        except frida.ProcessNotFoundError:
            self._log("⚠ 游戏进程已退出")
            self.after(0, lambda: self._set_status("red", "未连接"))
        except Exception as e:
            self._log(f"❌ 连接失败: {e}")
            self.after(0, lambda: self._set_status("red", "未连接"))
        finally:
            self._connecting = False

    def _on_connected(self, pid):
        self._set_status("green", "已连接")
        self.pid_label.configure(text=f"PID: {pid}")
        self.hint_label.configure(text="✅ 已连接！点击功能按钮开启修改",
                                   text_color="#88ff88")
        self.hint_frame.configure(fg_color="#1a3a1a")

    def _cleanup(self):
        try:
            if self.script:
                self.script.unload()
                self.script = None
            if self.session:
                self.session.detach()
                self.session = None
        except:
            pass
        self._ready = False
        self._features = {k: False for k in self._features}

    def _on_close(self):
        self._stop = True
        self._cleanup()
        self.destroy()

if __name__ == "__main__":
    app = GameModifierApp()
    app.mainloop()
