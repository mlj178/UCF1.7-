# 游戏修改器控制台 - 全功能整合包 v1.5
# 在 v1.3 基础上新增：UI界面升级、收藏功能、快捷键、音效设置、主题切换
# pip install customtkinter frida psutil pynput keyboard
# 注意编码问题，我的编码是uft-8，中文不要乱编码
import customtkinter as ctk
from PIL import Image
import frida
import threading
import time
import psutil
import json
import os
import sys
import winsound
import keyboard
import pygame
import functools

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# 获取应用根目录（兼容脚本和 exe 两种运行方式）
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
    RESOURCE_DIR = os.path.join(sys._MEIPASS, "资源")
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    RESOURCE_DIR = os.path.join(APP_DIR, "资源")

# 数据存储目录
DATA_DIR = os.path.join(APP_DIR, "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 功能定义
FEATURES_INFO = {
    'knife': {'name': '快刀', 'icon': '🔪', 'category': 'weapon'},
    'time': {'name': '无限时间', 'icon': '⏰', 'category': 'player'},
    'recoil': {'name': '无后座力', 'icon': '🎯', 'category': 'weapon'},
    'ammo': {'name': '无限子弹', 'icon': '🔫', 'category': 'weapon'},
    'movespeed': {'name': '滑板鞋', 'icon': '👟', 'category': 'player'},
    'ammoplus': {'name': '快速换弹', 'icon': '⚡', 'category': 'weapon'},
    'range': {'name': '剑气化丝', 'icon': '⚔️', 'category': 'weapon'},
    'gather': {'name': '聚怪', 'icon': '👾', 'category': 'other'},
    'gravity': {'name': '轻重力', 'icon': '🌌', 'category': 'player'},
    'aim': {'name': '自瞄', 'icon': '🎯', 'category': 'weapon'},
    'godmode': {'name': '金刚不坏', 'icon': '🛡️', 'category': 'player'},
    'speedgun': {'name': '射速变快', 'icon': '⚡', 'category': 'weapon'},
    'isbot': {'name': '天机傀儡', 'icon': '🧠', 'category': 'other'},
    'skillcd': {'name': '技能无冷却', 'icon': '✨', 'category': 'player'}
}

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
  // 说明: 替换 PlayerWeapons.get_KnifeSpeed，为本地玩家返回指定的速度倍数
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
        if (enabled) {
          sendLog('info', '快刀', '速度已切换: ' + speed + 'x（实时生效）');
        } else {
          sendLog('info', '快刀', '速度已预选: ' + speed + 'x（开启后生效）');
        }
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
        sendLog('success', '快刀', '已启用 (v16, Speed=' + currentSpeed + 'x) — 仅对玩家生效');
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
  // 说明: 锁定游戏时间为 99:59，永不结束
  // ====================================================================
  var timeModule = (function() {
    var hooks = [];
    var intervalId = null;
    var enabled = false;
    var modeBaseInstance = null;
    var pauseUntil = 0;

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
            if (Date.now() < pauseUntil) return;
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
            if (Date.now() < pauseUntil) return;
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
          if (Date.now() < pauseUntil) return;
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
      },
      pauseFor: function(ms) {
        pauseUntil = Date.now() + ms;
      }
    };
  })();

  // ====================================================================
  // 模块 3: 无后座力 v14
  // 说明: 替换 Recoil.OnGunShot，将后座力相关字段归零
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
  // 说明: 替换 ConsumeAmmo 函数，消耗子弹时返回 true 但不扣弹
  // ====================================================================
  var ammoModule = (function() {
    var enabled = false;
    var hooks = [];

    return {
      enable: function() {
        if (enabled) return;
        var mod = Process.findModuleByName('GameAssembly.dll');
        if (!mod) { sendLog('error', '无限子弹', 'GameAssembly.dll 未找到'); return; }
        var base = mod.base;

        // === 替换 WPN_Gun.ConsumeAmmo ===
        try {
          var addrConsumeAmmo = base.add(0xB61140);
          Interceptor.replace(addrConsumeAmmo, new NativeCallback(function(thisPtr, methodInfo) {
            return 1;
          }, 'bool', ['pointer', 'pointer']));
          hooks.push({ type: 'replace', addr: addrConsumeAmmo });
          sendLog('info', '无限子弹', 'WPN_Gun.ConsumeAmmo 已替换');
        } catch (e) {
          sendLog('error', '无限子弹', '替换 WPN_Gun.ConsumeAmmo 失败: ' + e);
        }

        // === 替换 Weapon.ConsumeAmmo（基类，兜底） ===
        try {
          var addrConsumeBase = base.add(0xB6C310);
          Interceptor.replace(addrConsumeBase, new NativeCallback(function(thisPtr, methodInfo) {
            return 1;
          }, 'bool', ['pointer', 'pointer']));
          hooks.push({ type: 'replace', addr: addrConsumeBase });
          sendLog('info', '无限子弹', 'Weapon.ConsumeAmmo 已替换');
        } catch (e) {
          sendLog('info', '无限子弹', '替换 Weapon.ConsumeAmmo 失败: ' + e);
        }

        // === RPG/AT4 无限子弹 ===
        try {
          var addrRpgFire = base.add(0xB670A0);
          var addrRpgFillAmmo = base.add(0xB67070);
          var rpgFillAmmoFn = new NativeFunction(addrRpgFillAmmo, 'void', ['pointer', 'pointer']);
          
          Interceptor.attach(addrRpgFire, {
            onEnter: function(args) {
              try {
                var self = args[0];
                if (self && !self.isNull()) {
                  rpgFillAmmoFn(self, ptr(0));
                }
              } catch (e) {}
            }
          });
          hooks.push({ type: 'attach', addr: addrRpgFire });
          sendLog('info', '无限子弹', 'RPG/AT4 无限子弹已启用');
        } catch (e) {
          sendLog('error', '无限子弹', 'RPG/AT4 初始化失败: ' + e);
        }

        enabled = true;
        sendLog('success', '无限子弹', '已启用 (Zero ammo consumption)');
        sendStatus('ammo', true);
      },
      disable: function() {
        if (!enabled) return;
        for (var i = 0; i < hooks.length; i++) {
          try {
            if (hooks[i].type === 'replace') {
              Interceptor.revert(hooks[i].addr);
            } else {
              hooks[i].addr.detach();
            }
          } catch(e) {}
        }
        hooks = [];
        enabled = false;
        sendLog('info', '无限子弹', '已禁用');
        sendStatus('ammo', false);
      }
    };
  })();

  // ====================================================================
  // 模块 5: 滑板鞋 (Move Speed)
  // 原理: Hook PropertyModifier.Get (RVA 0xB17590)
  //       拦截 MoveSpeedRatio Modifier 的查询，为本地玩家返回倍数后的值
  //       内存路径: player + 0x8C → Modifier_MoveSpeedRatio
  // ====================================================================
  var moveSpeedModule = (function() {
    var enabled = false;
    var currentSpeed = 3.0;
    var hookAddr = null;
    var isMyPlayerFn = null;
    var originalFn = null;
    var logCount = 0;

    return {
      setSpeed: function(speed) {
        currentSpeed = speed;
        if (enabled) {
          sendLog('info', '滑板鞋', '速度已切换: ' + speed + 'x（实时生效）');
        } else {
          sendLog('info', '滑板鞋', '速度已预选: ' + speed + 'x（开启后生效）');
        }
      },
      enable: function() {
        if (enabled) return;
        var mod = getGameAssembly();
        if (!mod) { sendLog('error', '滑板鞋', '无 GameAssembly.dll'); return; }

        var base = mod.base;
        hookAddr = base.add(0xB17590);
        isMyPlayerFn = new NativeFunction(base.add(0xB55FD0), 'bool', ['pointer']);
        originalFn = new NativeFunction(hookAddr, 'float', ['pointer', 'pointer']);
        logCount = 0;

        Interceptor.replace(hookAddr, new NativeCallback(function(self, player) {
          var result = originalFn(self, player);
          if (player && !player.isNull() && isMyPlayerFn(player)) {
            var moveMod = player.add(0x8C).readPointer();
            if (moveMod && !moveMod.isNull() && self.equals(moveMod)) {
              logCount++;
              if (logCount <= 10)
                sendLog('info', '滑板鞋', '原值=' + result.toFixed(3) + ' 修改后=' + currentSpeed.toFixed(1) + 'x');
              return currentSpeed;
            }
          }
          return result;
        }, 'float', ['pointer', 'pointer']));

        enabled = true;
        sendLog('success', '滑板鞋', '已启用 (' + currentSpeed + 'x) — 仅对玩家生效');
        sendStatus('movespeed', true);
      },
      disable: function() {
        if (!enabled || !hookAddr) return;
        Interceptor.revert(hookAddr);
        enabled = false;
        sendLog('info', '滑板鞋', '已禁用');
        sendStatus('movespeed', false);
      }
    };
  })();

  // ====================================================================
  // 模块 6: 快速换弹
  // 原理: 替换 get_ReloadSpeed，为本地玩家返回2倍加速
  // ====================================================================
  var reloadSpeedModule = (function() {
    var enabled = false;
    var getReloadSpeedAddr = null;
    var isMyPlayer = null;
    var reloadLogCount = 0;

    return {
      enable: function() {
        if (enabled) return;
        var mod = getGameAssembly();
        if (!mod) { sendLog('error', '快速换弹', '无 GameAssembly.dll'); return; }

        var base = mod.base;
        getReloadSpeedAddr = base.add(0xB170E0);
        isMyPlayer = new NativeFunction(base.add(0xB55FD0), 'bool', ['pointer']);
        reloadLogCount = 0;

        sendLog('info', '快速换弹', 'get_ReloadSpeed @ ' + getReloadSpeedAddr);

        Interceptor.replace(getReloadSpeedAddr, new NativeCallback(function(self) {
          try {
            var owner = self.add(0x8).readPointer();
            if (!owner || owner.isNull()) return 4.0;
            if (isMyPlayer(owner)) {
              reloadLogCount++;
              if (reloadLogCount <= 5) {
                sendLog('info', '快速换弹', '本地玩家换弹加速 4.0x (#' + reloadLogCount + ')');
              }
              return 4.0;
            }
            return 1.0;
          } catch(e) {
            return 4.0;
          }
        }, 'float', ['pointer']));

        enabled = true;
        sendLog('success', '快速换弹', '已启用 — 2x快速换弹');
        sendStatus('ammoplus', true);
      },
      disable: function() {
        if (!enabled) return;
        if (getReloadSpeedAddr) { try { Interceptor.revert(getReloadSpeedAddr); } catch(e) {} }
        getReloadSpeedAddr = null;
        isMyPlayer = null;
        enabled = false;
        sendLog('info', '快速换弹', '已禁用');
        sendStatus('ammoplus', false);
      }
    };
  })();

  // ====================================================================
  // 模块 7: 剑气化丝 (Knife Range)
  // 原理: 1) attach get_KnifeSpeed 捕获本地玩家指针
  //       2) Hook WPN_Knife.GetKnifeAttackData，将攻击距离乘以50倍
  // ====================================================================
  var rangeModule = (function() {
    var enabled = false;
    var KNIFE_RANGE_MULTIPLIER = 50.0;
    var myPlayer = null;
    var myPlayerFound = false;
    var callCount = 0;
    var rangeLogCount = 0;
    var isMyPlayerFn = null;
    var getKnifeSpeedAddr = null;
    var getKnifeSpeedHook = null;
    var getKnifeAttackDataAddr = null;
    var cleanupAddrs = [];
    var hookHandles = [];

    return {
      enable: function() {
        if (enabled) return;
        var mod = getGameAssembly();
        if (!mod) { sendLog('error', '剑气化丝', '无 GameAssembly.dll'); return; }

        var base = mod.base;
        isMyPlayerFn = new NativeFunction(base.add(0xB55FD0), 'bool', ['pointer']);
        myPlayer = null;
        myPlayerFound = false;
        callCount = 0;
        rangeLogCount = 0;
        hookHandles = [];

        // 步骤1: attach get_KnifeSpeed 捕获 myPlayer（仅观察，不替换，与快刀共存）
        try {
          getKnifeSpeedAddr = base.add(0xB170A0);
          getKnifeSpeedHook = Interceptor.attach(getKnifeSpeedAddr, {
            onEnter: function(args) { this._self = args[0]; },
            onLeave: function(retval) {
              if (myPlayerFound) return;
              try {
                var owner = this._self.add(0x8).readPointer();
                if (owner && !owner.isNull() && isMyPlayerFn(owner)) {
                  myPlayer = owner;
                  myPlayerFound = true;
                  sendLog('info', '剑气化丝', '捕获本地玩家 @ ' + myPlayer);
                }
              } catch(e) {}
            }
          });
          sendLog('info', '剑气化丝', 'get_KnifeSpeed attach @ ' + getKnifeSpeedAddr + ' (兼容模式)');
        } catch(e) {
          sendLog('warn', '剑气化丝', 'get_KnifeSpeed hook失败: ' + e.message);
        }

        // 步骤2: Hook GetKnifeAttackData 修改攻击距离（attach方式，与快刀共存）
        try {
          getKnifeAttackDataAddr = base.add(0xB63EC0);
          var h = Interceptor.attach(getKnifeAttackDataAddr, {
            onEnter: function(args) {
              this.wpnSelf = args[1];
              this.attackIdx = args[2].toInt32();
              try { this.owner = args[1].add(0x30).readPointer(); } catch(e) { this.owner = null; }
            },
            onLeave: function(retval) {
              callCount++;
              try {
                var orig = retval.add(0x4).readFloat();
                var isOwnerMine = myPlayerFound && this.owner && !this.owner.isNull() && this.owner.equals(myPlayer);
                if (!isOwnerMine) return;
                if (!(orig > 0.3 && orig < 500)) return;

                retval.add(0x4).writeFloat(orig * KNIFE_RANGE_MULTIPLIER);
                var after = retval.add(0x4).readFloat();

                rangeLogCount++;
                if (rangeLogCount <= 10) {
                  sendLog('info', '剑气化丝', '攻击距离 ' + orig.toFixed(2) + ' → ' + after.toFixed(2) + ' (' + KNIFE_RANGE_MULTIPLIER + 'x)');
                }
              } catch(e) {
                if (callCount <= 5) sendLog('error', '剑气化丝', '异常: ' + e.message);
              }
            }
          });
          hookHandles.push(h);
          sendLog('info', '剑气化丝', 'Hook GetKnifeAttackData @ ' + getKnifeAttackDataAddr);
        } catch(e) { sendLog('error', '剑气化丝', 'Hook 失败: ' + e.message); }

        // 房间切换检测
        cleanupAddrs = [0xAFAA40, 0xAF5B30, 0xAF15D0];
        for (var i = 0; i < cleanupAddrs.length; i++) {
          try {
            var h = Interceptor.attach(base.add(cleanupAddrs[i]), {
              onEnter: function() {
                myPlayer = null;
                myPlayerFound = false;
                callCount = 0;
                rangeLogCount = 0;
                sendLog('info', '剑气化丝', '房间切换，状态重置');
              }
            });
            hookHandles.push(h);
          } catch(e) {}
        }

        enabled = true;
        sendLog('success', '剑气化丝', '已启用 (' + KNIFE_RANGE_MULTIPLIER + 'x) — 仅对玩家生效');
        sendStatus('range', true);
      },
      disable: function() {
        if (!enabled) return;
        if (getKnifeSpeedHook) { try { getKnifeSpeedHook.detach(); } catch(e) {} }
        for (var i = 0; i < hookHandles.length; i++) { try { hookHandles[i].detach(); } catch(e) {} }
        getKnifeSpeedAddr = null;
        getKnifeSpeedHook = null;
        getKnifeAttackDataAddr = null;
        hookHandles = [];
        myPlayer = null;
        myPlayerFound = false;
        enabled = false;
        sendLog('info', '剑气化丝', '已禁用');
        sendStatus('range', false);
      },
      setRange: function(multiplier) {
        KNIFE_RANGE_MULTIPLIER = multiplier;
        sendLog('info', '剑气化丝', '攻击距离倍率已更新: ' + multiplier + 'x');
      }
    };
  })();

  // ====================================================================
  // 模块 8: 聚怪 (Bot Gathering) — v1.2
  // 原理: 双路径扫描 + CC.disable → set_position → CC.enable
  //       路径A: 扫描 GM.allPlayers[30] 找到已注册的 Player
  //       路径B: Hook Bot.Update 捕获所有 Bot 组件实例
  //       硬编码 SP_GR(佣兵)出生点坐标 (13.6, 14.1, 0.1)
  //       与原版 AAAAA-bot_to_spawn_v24.js 完全一致
  // ====================================================================
  var gatherModule = (function() {
    var enabled = false;
    var gm = null;
    var mm = null;
    var spawn = { x: 13.6, y: 14.1, z: 0.1 };
    var ntp = false;
    var tn = 0;
    // 临时集合：仅缓存 Bot.Update 捕获到的 Player 指针，带时间戳，传送后立即清空
    var recentBotPlayers = {};

    var R = {
      GM_AddP:   0xAF9A90,
      MM_MapGun: 0xAEBB70,
      P_Update:  0xB551D0,
      P_isMy:    0xB55FD0,
      E_isDead:  0xB400E0,
      E_getCC:   0x1CF180,
      C_setEn:   0xAB86B0,
      getTrans:  0x32CF40,
      setPosInj: 0x3F4810,
      Bot_Update: 0xB33370,
      SingGetInst: 0x4A8170,
    };

    var SING = {
      GM: 0xE1CE64,
      MM: 0xE1D9E8,
    };

    var O = {
      GM_allPlayers: 0x1C,
      MM_SP_GR: 0x14,
      MM_SP_BL: 0x10,
      P_cameraManager: 0x48,
      P_charContainer: 0x58,
      P_clientData: 0x94,
      CD_isBot: 0x1C,
      CD_team:  0x18,
      Bot_thisPlayer: 0x24,
    };

    var isMy   = null;
    var isDead = null;
    var getCC  = null;
    var cSE    = null;
    var gt     = null;
    var spi    = null;
    var posBuf = null;
    var singletonGetter = null;
    var hooks = [];

    function rp(a, o) { try { return a.add(o).readPointer(); } catch(e) { return null; } }

    function isValid(pp) {
      if (!pp || pp.isNull()) return false;
      try { var vt = pp.readPointer(); return vt && !vt.isNull(); } catch(e) { return false; }
    }

    function isHuman(pp) {
      var cd = rp(pp, O.P_clientData);
      if (cd && !cd.isNull()) {
        try {
          var b = cd.add(O.CD_isBot).readU8();
          if (b === 1) return false;
          if (b === 0) return true;
        } catch(e) {}
      }
      if (rp(pp, O.P_cameraManager)) return true;
      return false;
    }

    // 只做临时记录，不持久化，不跨传送累积
    function trackFromBot(botPtr) {
      var player = rp(botPtr, O.Bot_thisPlayer);
      if (player && !player.isNull() && isValid(player)) {
        var pk = player.toString();
        recentBotPlayers[pk] = { player: player, time: Date.now() };
      }
    }

    function teleportEntity(ppOrBot, isBot) {
      try {
        var tr = gt(ppOrBot, ptr(0));
        if (!tr || tr.isNull()) {
          if (!isBot) tr = rp(ppOrBot, O.P_charContainer);
          else tr = null;
        }
        if (!tr || tr.isNull()) return 'T=null';

        var cc = getCC(ppOrBot, ptr(0));
        if (cc && !cc.isNull()) cSE(cc, 0, ptr(0));

        spi(tr, posBuf, ptr(0));
        try {
          var np = tr.add(0x10).readPointer();
          if (np) {
            np.add(0x38).writeFloat(spawn.x);
            np.add(0x3C).writeFloat(spawn.y);
            np.add(0x40).writeFloat(spawn.z);
          }
        } catch(e) {}

        if (cc && !cc.isNull()) cSE(cc, 1, ptr(0));
        return 'OK';
      } catch(e) { return 'ERR:' + e.message; }
    }

    function getGM() {
      if (gm) return gm;
      try {
        var methodInfo = getGameAssembly().base.add(SING.GM).readPointer();
        gm = singletonGetter(methodInfo);
      } catch(e) {}
      if (gm && !gm.isNull()) { sendLog('info', '聚怪', '✅ GM: ' + gm); return gm; }
      try {
        var classPtr = getGameAssembly().base.add(SING.GM).readPointer();
        if (classPtr && !classPtr.isNull()) {
          gm = classPtr.add(0xC).readPointer();
        }
      } catch(e) {}
      if (gm && !gm.isNull()) sendLog('info', '聚怪', '✅ GM: ' + gm);
      return gm;
    }

    function getMM() {
      if (mm) return mm;
      try {
        var methodInfo = getGameAssembly().base.add(SING.MM).readPointer();
        mm = singletonGetter(methodInfo);
      } catch(e) {}
      if (mm && !mm.isNull()) sendLog('info', '聚怪', '✅ MM: ' + mm);
      return mm;
    }

    function executeTeleport() {
      tn++;
      sendLog('info', '聚怪', '');
      sendLog('info', '聚怪', '╔══ 传送 #' + tn + ' ══╗');
      getGM(); getMM();
      if (!gm || !mm) { sendLog('error', '聚怪', 'GM/MM 未就绪'); return; }

      sendLog('info', '聚怪', '出生点: (' + spawn.x.toFixed(1) + ',' + spawn.y.toFixed(1) + ',' + spawn.z.toFixed(1) + ')');
      posBuf.writeFloat(spawn.x); posBuf.add(4).writeFloat(spawn.y); posBuf.add(8).writeFloat(spawn.z);

      // 路径A：从 allPlayers 动态获取当前存活玩家
      var playersToMove = {};
      var now = Date.now();
      try {
        var ap = gm.add(O.GM_allPlayers).readPointer();
        if (ap && !ap.isNull()) {
          var t = ap.add(0xC).readU32();
          for (var i = 0; i < t; i++) {
            try {
              var pp = ap.add(0x10 + i * 8).readPointer();
              if (isValid(pp)) {
                playersToMove[pp.toString()] = pp;
              }
            } catch(e) {}
          }
        }
      } catch(e) {}

      // 路径B：从 recentBotPlayers 补充（Bot.Update 临时记录）
      var botKeys = Object.keys(recentBotPlayers);
      var botAdded = 0;
      for (var bi = 0; bi < botKeys.length; bi++) {
        var entry = recentBotPlayers[botKeys[bi]];
        // 检查时效性（超过 5 秒的忽略）
        if (now - entry.time > 5000) continue;
        var pp = entry.player;
        // 重新验证指针是否仍然有效（防止 Bot 被销毁后访问野指针）
        try {
          if (pp && !pp.isNull()) {
            pp.readPointer(); // 快速探针，抛异常即失效
            var pk = pp.toString();
            if (!playersToMove[pk]) {
              playersToMove[pk] = pp;
              botAdded++;
            }
          }
        } catch(e) {}
      }

      sendLog('info', '聚怪', '追踪: ' + Object.keys(playersToMove).length + ' Player (allPlayers) + ' + botAdded + ' (Bot补充)');

      var self = 0, real = 0, dead = 0, botOk = 0, botFail = 0;
      var pKeys = Object.keys(playersToMove);
      var log = [];

      for (var pi = 0; pi < pKeys.length; pi++) {
        var pp = playersToMove[pKeys[pi]];
        try {
          if (isMy(pp, ptr(0))) { self++; continue; }
          if (isHuman(pp)) { real++; continue; }
          if (isDead(pp, ptr(0))) { dead++; continue; }
          var r = teleportEntity(pp, false);
          if (r === 'OK') botOk++;
          else botFail++;
          log.push('#' + pi + ': Bot→' + r);
        } catch(e) { botFail++; }
      }

      for (var j = 0; j < log.length; j++) sendLog('info', '聚怪', '  ' + log[j]);

      sendLog('info', '聚怪', '');
      sendLog('info', '聚怪', '┌─ ' + pKeys.length + '人 ──────────────────┐');
      sendLog('info', '聚怪', '│  自己=' + self + ' 真人=' + real + '  Bot死=' + dead + ' Bot活=' + botOk);
      if (botFail > 0) sendLog('info', '聚怪', '│  失败=' + botFail);
      sendLog('info', '聚怪', '└──────────────────────────────────────────┘');
      sendLog('info', '聚怪', '╚══════╝');

      // 传送结束：立即清空临时集合，确保野指针不会残留到下一次
      recentBotPlayers = {};

      send(JSON.stringify({type:'done',n:tn,bots:botOk,fail:botFail}));
    }

    return {
      enable: function() {
        if (enabled) return;
        var mod = getGameAssembly();
        if (!mod) { sendLog('error', '聚怪', '无 GameAssembly.dll'); return; }

        var base = mod.base;

        isMy   = new NativeFunction(base.add(R.P_isMy),  'bool',   ['pointer','pointer']);
        isDead = new NativeFunction(base.add(R.E_isDead), 'bool',   ['pointer','pointer']);
        getCC  = new NativeFunction(base.add(R.E_getCC), 'pointer', ['pointer','pointer']);
        cSE    = new NativeFunction(base.add(R.C_setEn), 'void',    ['pointer','int','pointer']);
        gt     = new NativeFunction(base.add(R.getTrans), 'pointer', ['pointer','pointer']);
        spi    = new NativeFunction(base.add(R.setPosInj),'void',   ['pointer','pointer','pointer']);
        posBuf = Memory.alloc(16);
        singletonGetter = new NativeFunction(base.add(R.SingGetInst), 'pointer', ['pointer']);

        posBuf.writeFloat(spawn.x);
        posBuf.add(4).writeFloat(spawn.y);
        posBuf.add(8).writeFloat(spawn.z);

        try {
          var h = Interceptor.attach(base.add(R.Bot_Update), {
            onEnter: function(args) { trackFromBot(args[0]); }
          });
          hooks.push(h);
          sendLog('info', '聚怪', 'Bot.Update Hook 已安装');
        } catch(e) { sendLog('error', '聚怪', 'Bot.Update Hook 失败: ' + e.message); }

        try {
          var h2 = Interceptor.attach(base.add(R.GM_AddP), {
            onEnter: function(a) { if (!gm) { gm = a[0]; sendLog('info', '聚怪', '✅ GM: ' + gm); } }
          });
          hooks.push(h2);
        } catch(e) { sendLog('error', '聚怪', 'AddPlayer Hook 失败: ' + e.message); }

        try {
          var h3 = Interceptor.attach(base.add(R.MM_MapGun), {
            onEnter: function(a) {
              if (mm) return;
              mm = a[0]; sendLog('info', '聚怪', '✅ MM: ' + mm);
              sendLog('info', '聚怪', '  出生点坐标: (' + spawn.x.toFixed(1) + ',' + spawn.y.toFixed(1) + ',' + spawn.z.toFixed(1) + ') - 硬编码 SP_GR');
            }
          });
          hooks.push(h3);
        } catch(e) { sendLog('error', '聚怪', 'MapGunInit Hook 失败: ' + e.message); }

        try {
          var h4 = Interceptor.attach(base.add(R.P_Update), {
            onEnter: function(a) {
              if (!ntp) return; ntp = false;
              if (!gm || !mm) { sendLog('warn', '聚怪', '未就绪'); return; }
              executeTeleport();
            }
          });
          hooks.push(h4);
        } catch(e) { sendLog('error', '聚怪', 'Player.Update Hook 失败: ' + e.message); }

        enabled = true;
        sendLog('success', '聚怪', '已启用 — 动态列表模式（每次传送重新扫描，无野指针残留）');
        sendStatus('gather', true);
      },
      disable: function() {
        if (!enabled) return;
        for (var i = 0; i < hooks.length; i++) { try { hooks[i].detach(); } catch(e) {} }
        hooks = [];
        gm = null; mm = null;
        recentBotPlayers = {};
        enabled = false;
        sendLog('info', '聚怪', '已禁用');
        sendStatus('gather', false);
      },
      gather: function() {
        if (!enabled) { return { ok: false, msg: '聚怪未启用' }; }
        getGM(); getMM();
        if (!gm || !mm) { return { ok: false, msg: 'GM/MM 未就绪' }; }
        ntp = true;
        sendLog('info', '聚怪', '★ ★ ★ 传送 ★ ★ ★');
        return { ok: true, msg: '传送指令已发送' };
      }
    };
  })();

  // ====================================================================
  // 模块 9: 轻重力/高跳 (Gravity + Jump Modifier)
  // 说明: 通过定时器遍历玩家列表，修改 velocity.y 实现重力缩放和高跳
  // 来源: AAAAA-gravity_modifier-v8.js (已验证可行，逻辑未更改)
  // ====================================================================
  var gravityJumpModule = (function() {
    var enabled = false;
    var isMyPlayer = null;
    var state = {
      enabled: false,
      mode: 'player_only',
      gravityScale: 1.0,
      jumpScale: 1.0
    };
    var gm = null;
    var timer = null;
    var gmHook = null;
    var singletonGetter = null;
    var loopCount = 0;
    var lastLogTime = 0;
    var playerState = {};

    function hasGm() {
      if (!gm) return false;
      try {
        var v = gm.add(0x1C).readPointer();
        return v && !v.isNull();
      } catch(e) { return false; }
    }

    function tryGetGM() {
      if (gm) return;
      try {
        var methodInfo = getGameAssembly().base.add(0xE1CE64).readPointer();
        var temp = singletonGetter(methodInfo);
        if (temp && !temp.isNull()) {
          gm = temp;
          playerState = {};
        }
      } catch(e) {}
    }

    function loop() {
      if (!state.enabled) return;

      if (!hasGm()) {
        tryGetGM();
        if (!hasGm()) {
          gm = null;
          playerState = {};
          return;
        }
      }

      try {
        var ap = gm.add(0x1C).readPointer();
        if (!ap || ap.isNull()) return;
        var total = ap.add(0xC).readU32();
        if (total < 1 || total > 64) return;

        loopCount++;

        for (var i = 0; i < total; i++) {
          var pp = ap.add(0x10 + i * 8).readPointer();
          if (!pp || pp.isNull()) continue;
          if (state.mode !== 'all' && !isMyPlayer(pp)) continue;

          var key = pp.toString();

          var isGrounded = pp.add(0x70).readU8() !== 0;

          var vd = pp.add(0x90).readPointer();
          if (!vd || vd.isNull()) continue;
          var curY = vd.add(0x10).readFloat();

          var prev = playerState[key];
          var lastGrounded = prev ? prev.lastGrounded : true;

          if (lastGrounded && !isGrounded && curY > 0.1 && state.jumpScale !== 1.0) {
            vd.add(0x10).writeFloat(curY * state.jumpScale);
          }

          if (curY < -0.1 && state.gravityScale < 1.0) {
            vd.add(0x10).writeFloat(curY * state.gravityScale);
          }

          playerState[key] = { lastGrounded: isGrounded };
        }

        var now = Date.now();
        if (now - lastLogTime > 4000) {
          lastLogTime = now;
          var playerPP = null;
          for (var i = 0; i < total; i++) {
            var ppp = ap.add(0x10 + i * 8).readPointer();
            if (ppp && !ppp.isNull() && isMyPlayer(ppp)) { playerPP = ppp; break; }
          }
          if (playerPP) {
            var pvd = playerPP.add(0x90).readPointer();
            if (pvd) {
              var vy = pvd.add(0x10).readFloat();
              var pg = playerPP.add(0x70).readU8() !== 0;
              sendLog('info', '轻重力', 'vy=' + vy.toFixed(3) + ' gnd=' + pg + ' grav=' + state.gravityScale.toFixed(2) + ' jump=' + state.jumpScale.toFixed(2));
            }
          }
        }
      } catch(_) {}
    }

    return {
      enable: function() {
        if (enabled) return;
        var mod = getGameAssembly();
        if (!mod) { sendLog('error', '轻重力', '无 GameAssembly.dll'); return; }
        var base = mod.base;
        isMyPlayer = new NativeFunction(base.add(0xB55FD0), 'bool', ['pointer']);
        singletonGetter = new NativeFunction(base.add(0x4A8170), 'pointer', ['pointer']);

        try {
          gmHook = Interceptor.attach(base.add(0xAF9A90), {
            onEnter: function(args) {
              var newGm = args[0];
              if (newGm && !newGm.isNull()) {
                gm = newGm;
                playerState = {};
              }
            }
          });
        } catch(e) {}

        // 主动获取已存在的 GameManager 实例（进入对局后立即生效）
        tryGetGM();
        timer = setInterval(loop, 50);
        state.enabled = true;
        enabled = true;
        sendLog('success', '轻重力', '已启用 (重力=' + state.gravityScale.toFixed(1) + ', 跳跃=' + state.jumpScale.toFixed(1) + ', 模式=' + state.mode + ')');
        sendStatus('gravity', true);
      },
      disable: function() {
        if (!enabled) return;
        if (timer) { clearInterval(timer); timer = null; }
        if (gmHook) { try { gmHook.detach(); } catch(e) {} gmHook = null; }
        state.enabled = false;
        gm = null;
        playerState = {};
        enabled = false;
        sendLog('info', '轻重力', '已禁用');
        sendStatus('gravity', false);
      },
      setconfig: function(g, j, m) {
        state.mode = m || 'player_only';
        state.gravityScale = g;
        state.jumpScale = j;
        if (state.gravityScale < 0) state.gravityScale = 0;
        if (state.gravityScale > 1) state.gravityScale = 1;
        if (state.jumpScale < 1.0) state.jumpScale = 1.0;
        if (state.jumpScale > 5.0) state.jumpScale = 5.0;
        // 只有模块已启用时，才根据实际值决定 loop 是否工作
        // 如果所有值都是默认值(1.0/1.0)，让 loop 退出避免空转
        if (enabled) {
          state.enabled = (state.gravityScale < 1.0 || state.jumpScale !== 1.0);
        } else {
          state.enabled = false;
        }
        sendLog('info', '轻重力', '配置已更新: 重力=' + state.gravityScale.toFixed(1) + ', 跳跃=' + state.jumpScale.toFixed(1) + ', 模式=' + state.mode);
        return { ok: true };
      },
      resetall: function() {
        state.enabled = false;
        state.gravityScale = 1.0;
        state.jumpScale = 1.0;
        if (timer) { clearInterval(timer); timer = null; }
        if (gmHook) { try { gmHook.detach(); } catch(e) {} gmHook = null; }
        gm = null;
        playerState = {};
        enabled = false;
        sendLog('info', '轻重力', '已重置');
        sendStatus('gravity', false);
        return { ok: true };
      },
      getstatus: function() {
        return { enabled: state.enabled, gravityScale: state.gravityScale, jumpScale: state.jumpScale, haveGM: hasGm() };
      }
    };
  })();

  // ====================================================================
  // 模块 10: 回合跳过 (Round Skip)
  // 说明: 将 ModeBase.restGameTime 设为 0:00 触发回合结束
  // 来源: AAAAA-skip_round.js (已验证可行，逻辑未更改)
  // 冲突处理: 写入 0:00 前调用 timeModule.pauseFor(1000) 暂停无限时间 1 秒
  // ====================================================================
  var roundSkipModule = (function() {
    var modeBaseInstance = null;
    var skipCount = 0;
    var skipErrorCount = 0;
    var roundActive = false;
    var currentRound = 0;
    var inHook = false;
    var skipGuard = false;
    var hooks = [];
    var logs = [];

    function pad2(n) { return n < 10 ? "0" + n : "" + n; }

    function addLog(level, message) {
      logs.push({ level: level, message: message });
      sendLog(level, '回合跳过', message);
    }

    function isValidInstance(instance) {
      try {
        if (!instance || instance.equals(ptr(0))) return false;
        if (instance.compare(ptr(0x10000)) < 0) return false;
        instance.readU8();
        return true;
      } catch (e) {
        return false;
      }
    }

    function skipRound() {
      if (skipGuard) {
        addLog('warn', 'skipGuard active, skipping');
        return { ok: false, reason: 'guard_active' };
      }

      var instance = modeBaseInstance;
      if (!isValidInstance(instance)) {
        skipErrorCount++;
        addLog('error', 'skipRound: no valid instance (err:' + skipErrorCount + ')');
        return { ok: false, reason: 'no_instance' };
      }

      var minute = 0, second = 0;
      try {
        minute = instance.add(0x34).readS32();
        second = instance.add(0x38).readS32();
      } catch (e) {
        skipErrorCount++;
        addLog('error', 'skipRound: read failed (err:' + skipErrorCount + ')');
        return { ok: false, reason: 'read_failed' };
      }

      if (minute === 0 && second === 0) {
        addLog('warn', 'skipRound: time already 0:00');
        return { ok: false, reason: 'already_zero' };
      }

      try {
        skipGuard = true;

        // 暂停无限时间 1 秒，防止 timeModule 将 0:00 覆盖回 99:59
        try { timeModule.pauseFor(1000); } catch(e) {}

        instance.add(0x34).writeS32(0);
        instance.add(0x38).writeS32(0);
        skipCount++;
        roundActive = false;
        addLog('info', 'SKIP! ' + minute + ':' + pad2(second) + ' -> 0:00 (total:' + skipCount + ')');
        send({ type: 'round_skipped', from: minute + ':' + pad2(second), count: skipCount });
        skipGuard = false;
        return { ok: true };
      } catch (e) {
        skipGuard = false;
        skipErrorCount++;
        addLog('error', 'skipRound: write failed ' + e + ' (err:' + skipErrorCount + ')');
        return { ok: false, reason: 'write_failed' };
      }
    }

    function installHooks() {
      var mod = getGameAssembly();
      if (!mod) { addLog('error', '无 GameAssembly.dll'); return false; }
      var base = mod.base;
      addLog('info', '安装 Hook... Base: ' + base);

      try {
        var h1 = Interceptor.attach(base.add(0xAF6930), {
          onEnter: function(args) {
            if (inHook) return;
            inHook = true;
            var instance = args[0];
            if (!isValidInstance(instance)) { inHook = false; return; }
            var isNew = !modeBaseInstance || !instance.equals(modeBaseInstance);
            if (isNew) {
              modeBaseInstance = instance;
              try { currentRound = instance.add(0x14).readS32(); } catch(e) {}
              roundActive = true;
              addLog('info', '新回合 #' + currentRound);
            }
            inHook = false;
          },
          onLeave: function(retval) { inHook = false; }
        });
        hooks.push(h1);
        addLog('info', 'Hooked UpdateTimeUI (0xAF6930)');
      } catch(e) { addLog('error', 'Hook UpdateTimeUI 失败: ' + e); }

      try {
        var h2 = Interceptor.attach(base.add(0xAFAA40), {
          onEnter: function(args) {
            addLog('info', 'GameRoundEnd');
            modeBaseInstance = null;
            roundActive = false;
          }
        });
        hooks.push(h2);
        addLog('info', 'Hooked GameRoundEnd (0xAFAA40)');
      } catch(e) { addLog('error', 'Hook GameRoundEnd 失败: ' + e); }

      try {
        var h3 = Interceptor.attach(base.add(0xAF1920), {
          onEnter: function(args) {
            addLog('info', 'OnTimeOut');
            roundActive = false;
          }
        });
        hooks.push(h3);
        addLog('info', 'Hooked OnTimeOut (0xAF1920)');
      } catch(e) { addLog('error', 'Hook OnTimeOut 失败: ' + e); }

      addLog('info', '所有 Hook 安装完成');
      return true;
    }

    return {
      enable: function() {
        if (hooks.length > 0) return;
        installHooks();
      },
      disable: function() {
        for (var i = 0; i < hooks.length; i++) { try { hooks[i].detach(); } catch(e) {} }
        hooks = [];
        modeBaseInstance = null;
        roundActive = false;
        addLog('info', '已卸载');
      },
      skipround: function() {
        var result = skipRound();
        return { ok: result.ok, reason: result.reason };
      },
      getstatus: function() {
        var timeStr = null;
        if (isValidInstance(modeBaseInstance)) {
          try {
            var m = modeBaseInstance.add(0x34).readS32();
            var s = modeBaseInstance.add(0x38).readS32();
            if (m >= 0 && m <= 200 && s >= 0 && s <= 59) timeStr = m + ":" + pad2(s);
          } catch(e) {}
        }
        return {
          ok: true,
          roundActive: roundActive,
          currentRound: currentRound,
          skipCount: skipCount,
          skipErrorCount: skipErrorCount,
          hasInstance: !!modeBaseInstance,
          restGameTime: timeStr
        };
      },
      reset: function() {
        modeBaseInstance = null;
        roundActive = false;
        currentRound = 0;
        skipCount = 0;
        skipErrorCount = 0;
        skipGuard = false;
        inHook = false;
        logs = [];
        return { ok: true };
      }
    };
  })();

  // ====================================================================
  // 模块 11: 自瞄 v2 — 基于 UnityCrossFire.dll 逆向方案
  // ====================================================================
  var aimModule = (function() {
    var enabled = false;
    var myPlayer = null;
    var targetEnemy = null;
    var timer = null;
    var roomHooks = [];
    var frameCount = 0;

    var CONFIG = {
      aimKey:          0,
      aimBone:         7,
      smoothness:      1.0,
      maxAimDistance:  200.0,
      maxAngleFOV:     30.0,
      visibilityCheck: false,
      autoAim:         false,
      debugLog:        true,
    };

    var singletonGetter = null;
    var compGetTransform = null;
    var transformGetPos = null;
    var isMyPlayerFn = null;
    var isDeadFn = null;
    var getTeamFn = null;
    var addCamRotFn = null;
    var getMouseBtnFn = null;
    var linecastFn = null;

    var aimTimer = null;
    var scanTimer = null;
    var debugTimer = null;
    var cachedTarget = null;
    var scanYawDeg = 0;
    var scanPitchDeg = 0;

    var RVA_AIM = {
      SingletonGet:                    0x4A8170,
      GM_Singleton_MethodInfo:         0xE1CE64,
      Component_get_transform:         0x32CF40,
      Transform_get_position:          0x3F42B0,
      Player_get_isMyPlayer:           0xB55FD0,
      Entity_get_isDead:               0xB400E0,
      Entity_get_team:                 0x1E0070,
      Player_AddCameraRotation:        0xB4F790,
      Input_GetMouseButton:            0xACFB20,
      Physics_Linecast:                0xAB9B80,
    };

    var OFF_AIM = {
      GM_allPlayers:      0x1C,
      GM_playersBL:       0x20,
      GM_playersGR:       0x28,
      E_team:             0x20,
      P_cameraRotation:   0x4C,
      P_recoil:           0x54,
      P_characterContainer: 0x58,
      Arr_len:            0x0C,
      Arr_data:           0x10,
      List_items:         0x08,
      List_size:          0x0C,
      ptrSize:            4,
    };

    function getGM() {
      try {
        var base = getGameAssembly().base;
        var mi = base.add(RVA_AIM.GM_Singleton_MethodInfo).readPointer();
        if (mi.isNull()) {
          return singletonGetter(ptr(0));
        }
        var gm = singletonGetter(mi);
        if (gm.isNull()) return null;
        return gm;
      } catch(e) { return null; }
    }

    function initNativeFunctions() {
      var mod = getGameAssembly();
      if (!mod) return false;
      var base = mod.base;

      try { singletonGetter = new NativeFunction(base.add(RVA_AIM.SingletonGet), 'pointer', ['pointer']); } catch(e) { return false; }
      try { compGetTransform = new NativeFunction(base.add(RVA_AIM.Component_get_transform), 'pointer', ['pointer', 'pointer']); } catch(e) { return false; }
      try { transformGetPos = new NativeFunction(base.add(RVA_AIM.Transform_get_position), 'void', ['pointer', 'pointer', 'pointer']); } catch(e) { return false; }
      try { isMyPlayerFn = new NativeFunction(base.add(RVA_AIM.Player_get_isMyPlayer), 'bool', ['pointer', 'pointer']); } catch(e) { return false; }
      try { isDeadFn = new NativeFunction(base.add(RVA_AIM.Entity_get_isDead), 'bool', ['pointer', 'pointer']); } catch(e) { return false; }
      try { getTeamFn = new NativeFunction(base.add(RVA_AIM.Entity_get_team), 'int32', ['pointer', 'pointer']); } catch(e) { getTeamFn = null; }
      try { addCamRotFn = new NativeFunction(base.add(RVA_AIM.Player_AddCameraRotation), 'void', ['pointer', 'float', 'float', 'pointer']); } catch(e) { return false; }
      try { getMouseBtnFn = new NativeFunction(base.add(RVA_AIM.Input_GetMouseButton), 'bool', ['int32', 'pointer']); } catch(e) { getMouseBtnFn = null; }
      try { linecastFn = new NativeFunction(base.add(RVA_AIM.Physics_Linecast), 'bool', ['pointer', 'pointer', 'int32', 'pointer']); } catch(e) { linecastFn = null; }

      return true;
    }

    function isValidPlayer(pp) {
      if (!pp || pp.isNull()) return false;
      try {
        var team = pp.add(OFF_AIM.E_team).readS32();
        return (team === 0 || team === 1 || team === 2);
      } catch(e) { return false; }
    }

    function readList(listPtr) {
      var result = [];
      if (!listPtr || listPtr.isNull()) return result;
      try {
        var items = listPtr.add(OFF_AIM.List_items).readPointer();
        if (!items || items.isNull()) return result;
        var count = listPtr.add(OFF_AIM.List_size).readS32();
        for (var i = 0; i < count; i++) {
          var elem = items.add(OFF_AIM.Arr_data + i * OFF_AIM.ptrSize).readPointer();
          if (elem && !elem.isNull()) result.push(elem);
        }
      } catch(e) {}
      return result;
    }

    function readArray(arrPtr) {
      var result = [];
      if (!arrPtr || arrPtr.isNull()) return result;
      try {
        var len = arrPtr.add(OFF_AIM.Arr_len).readU32();
        for (var i = 0; i < len; i++) {
          var elem = arrPtr.add(OFF_AIM.Arr_data + i * OFF_AIM.ptrSize).readPointer();
          if (elem && !elem.isNull()) result.push(elem);
        }
      } catch(e) {}
      return result;
    }

    function getAllPlayers(gm) {
      var map = {};
      var arr = readArray(gm.add(OFF_AIM.GM_allPlayers).readPointer());
      for (var i = 0; i < arr.length; i++) {
        if (isValidPlayer(arr[i])) map[arr[i].toString()] = arr[i];
      }
      var bl = readList(gm.add(OFF_AIM.GM_playersBL).readPointer());
      for (var i = 0; i < bl.length; i++) {
        if (isValidPlayer(bl[i])) map[bl[i].toString()] = bl[i];
      }
      var gr = readList(gm.add(OFF_AIM.GM_playersGR).readPointer());
      for (var i = 0; i < gr.length; i++) {
        if (isValidPlayer(gr[i])) map[gr[i].toString()] = gr[i];
      }
      return Object.values(map);
    }

    function getPlayerPos(player) {
      if (!player || player.isNull()) return null;
      try {
        var transform = compGetTransform(player, ptr(0));
        if (transform && !transform.isNull()) {
          var posBuf = Memory.alloc(12);
          transformGetPos(posBuf, transform, ptr(0));
          var x = posBuf.readFloat();
          var y = posBuf.add(4).readFloat();
          var z = posBuf.add(8).readFloat();
          if (Math.abs(x) < 5000 && Math.abs(y) < 5000 && Math.abs(z) < 5000) {
            return { x: x, y: y, z: z };
          }
        }
        var container = player.add(OFF_AIM.P_characterContainer).readPointer();
        if (container && !container.isNull()) {
          var x = container.add(0x38).readFloat();
          var y = container.add(0x3C).readFloat();
          var z = container.add(0x40).readFloat();
          if (Math.abs(x) < 5000 && Math.abs(y) < 5000 && Math.abs(z) < 5000) {
            return { x: x, y: y, z: z };
          }
        }
      } catch(e) {}
      return null;
    }

    function getBonePos(player, boneIndex) {
      var pos = getPlayerPos(player);
      if (!pos) return null;
      var yOffsets = [1.65, 1.45, 1.05, 0.85, 0.75];
      var yOff = yOffsets[boneIndex % yOffsets.length] || 1.05;
      pos.y += yOff;
      return pos;
    }

    function checkVisibility(from, to) {
      if (!linecastFn) return true;
      try {
        var buf1 = Memory.alloc(12);
        buf1.writeFloat(from.x); buf1.add(4).writeFloat(from.y); buf1.add(8).writeFloat(from.z);
        var buf2 = Memory.alloc(12);
        buf2.writeFloat(to.x); buf2.add(4).writeFloat(to.y); buf2.add(8).writeFloat(to.z);
        return !linecastFn(buf1, buf2, -1, ptr(0));
      } catch(e) { return true; }
    }

    function targetScanner() {
      if (!enabled) return;
      var gm = getGM();
      if (!gm || gm.isNull()) return;

      if (!myPlayer || myPlayer.isNull()) {
        var all = getAllPlayers(gm);
        for (var i = 0; i < all.length; i++) {
          try { if (isMyPlayerFn(all[i], ptr(0))) { myPlayer = all[i]; break; } } catch(e) {}
        }
        if (!myPlayer) { cachedTarget = null; return; }
      }

      try { if (!isMyPlayerFn(myPlayer, ptr(0))) { myPlayer = null; cachedTarget = null; return; } } catch(e) { myPlayer = null; cachedTarget = null; return; }
      try { if (isDeadFn(myPlayer, ptr(0))) return; } catch(e) { return; }

      var myPos = getBonePos(myPlayer, CONFIG.aimBone);
      if (!myPos) return;

      scanYawDeg = myPlayer.add(OFF_AIM.P_cameraRotation).readFloat();
      scanPitchDeg = myPlayer.add(OFF_AIM.P_cameraRotation + 4).readFloat();

      var allPlayers = getAllPlayers(gm);
      var myTeam = 0;
      try {
        if (getTeamFn) myTeam = getTeamFn(myPlayer, ptr(0));
        else myTeam = myPlayer.add(OFF_AIM.E_team).readS32();
      } catch(e) {}

      var best = null;
      var bestAngleDeg = 999999;

      for (var i = 0; i < allPlayers.length; i++) {
        var p = allPlayers[i];
        try {
          if (p.equals(myPlayer)) continue;
          if (isDeadFn(p, ptr(0))) continue;
          var team = getTeamFn ? getTeamFn(p, ptr(0)) : p.add(OFF_AIM.E_team).readS32();
          var isEnemy = (myTeam === 2) || (team === 2) || (myTeam !== team);
          if (!isEnemy) continue;

          var targetPos = getBonePos(p, CONFIG.aimBone);
          if (!targetPos) continue;

          if (CONFIG.visibilityCheck) {
            if (!checkVisibility(myPos, targetPos)) continue;
          }

          var dx = targetPos.x - myPos.x;
          var dy = targetPos.y - myPos.y;
          var dz = targetPos.z - myPos.z;
          var dist = Math.sqrt(dx*dx + dy*dy + dz*dz);
          if (dist > CONFIG.maxAimDistance) continue;

          var targetYawDeg = Math.atan2(dx, dz) * 180.0 / Math.PI;
          var targetPitchDeg = Math.atan2(dy, Math.sqrt(dx*dx + dz*dz)) * 180.0 / Math.PI;

          var yawDiff = targetYawDeg - scanYawDeg;
          var pitchDiff = targetPitchDeg - scanPitchDeg;
          if (yawDiff > 180) yawDiff -= 360;
          if (yawDiff < -180) yawDiff += 360;
          if (pitchDiff > 180) pitchDiff -= 360;
          if (pitchDiff < -180) pitchDiff += 360;
          var angleDeg = Math.sqrt(yawDiff*yawDiff + pitchDiff*pitchDiff);

          if (angleDeg > CONFIG.maxAngleFOV) continue;

          if (angleDeg < bestAngleDeg) {
            bestAngleDeg = angleDeg;
            best = { player: p, pos: targetPos, targetYawDeg: targetYawDeg, targetPitchDeg: targetPitchDeg, angleDeg: angleDeg, dist: dist };
          }
        } catch(e) {}
      }

      cachedTarget = best;
    }

    function writeAimbot() {
      if (!enabled || !myPlayer || !cachedTarget) return;

      try {
        var curYawDeg = myPlayer.add(OFF_AIM.P_cameraRotation).readFloat();
        var curPitchDeg = myPlayer.add(OFF_AIM.P_cameraRotation + 4).readFloat();
        var userYawDelta = curYawDeg - scanYawDeg;
        var userPitchDelta = curPitchDeg - scanPitchDeg;
        if (userYawDelta > 180) userYawDelta -= 360;
        if (userYawDelta < -180) userYawDelta += 360;
        if (userPitchDelta > 180) userPitchDelta -= 360;
        if (userPitchDelta < -180) userPitchDelta += 360;
        var userAngleDelta = Math.sqrt(userYawDelta*userYawDelta + userPitchDelta*userPitchDelta);

        if (userAngleDelta > CONFIG.maxAngleFOV * 0.5) {
          cachedTarget = null;
          return;
        }

        var targetYawDeg = cachedTarget.targetYawDeg;
        var targetPitchDeg = cachedTarget.targetPitchDeg;

        var finalYawDeg = targetYawDeg;
        var finalPitchDeg = targetPitchDeg;
        if (CONFIG.smoothness < 1.0 && CONFIG.smoothness > 0.0) {
          var yawDiff = targetYawDeg - curYawDeg;
          var pitchDiff = targetPitchDeg - curPitchDeg;
          if (yawDiff > 180) yawDiff -= 360;
          if (yawDiff < -180) yawDiff += 360;
          if (pitchDiff > 180) pitchDiff -= 360;
          if (pitchDiff < -180) pitchDiff += 360;
          finalYawDeg = curYawDeg + yawDiff * CONFIG.smoothness;
          finalPitchDeg = curPitchDeg + pitchDiff * CONFIG.smoothness;
        }

        myPlayer.add(OFF_AIM.P_cameraRotation).writeFloat(finalYawDeg);
        myPlayer.add(OFF_AIM.P_cameraRotation + 4).writeFloat(finalPitchDeg);

        var recoil = myPlayer.add(OFF_AIM.P_recoil).readPointer();
        if (recoil && !recoil.isNull()) {
          recoil.add(0x10).writeU32(0);
          recoil.add(0x24).writeU32(0);
          recoil.add(0x40).writeU32(0);
          recoil.add(0x54).writeU32(0);
        }

        frameCount++;
      } catch(e) {}
    }

    function aimLoop() {
      if (!enabled) return;

      if (!CONFIG.autoAim) {
        if (!getMouseBtnFn) return;
        try {
          var btnDown = getMouseBtnFn(CONFIG.aimKey, ptr(0));
          if (!btnDown) return;
        } catch(e) { return; }
      }

      if (!myPlayer) return;
      if (!cachedTarget) return;

      writeAimbot();
    }

    function installRoomHooks(base) {
      var addrs = [0xAF9A90, 0xAEE370, 0xAF5B30];
      for (var i = 0; i < addrs.length; i++) {
        try {
          var h = Interceptor.attach(base.add(addrs[i]), {
            onEnter: function() {
              myPlayer = null;
              targetEnemy = null;
              frameCount = 0;
            }
          });
          roomHooks.push(h);
        } catch(e) {}
      }
    }

    return {
      enable: function() {
        if (enabled) return;
        var mod = getGameAssembly();
        if (!mod) { sendLog('error', '自瞄', '无 GameAssembly.dll'); return; }
        if (!initNativeFunctions()) { sendLog('error', '自瞄', 'NativeFunction 初始化失败'); return; }
        installRoomHooks(mod.base);
        aimTimer = setInterval(aimLoop, 16);
        scanTimer = setInterval(targetScanner, 30);
        enabled = true;
        sendLog('success', '自瞄', '已启用');
        sendStatus('aim', true);
      },
      disable: function() {
        if (!enabled) return;
        if (aimTimer) { clearInterval(aimTimer); aimTimer = null; }
        if (scanTimer) { clearInterval(scanTimer); scanTimer = null; }
        if (debugTimer) { clearInterval(debugTimer); debugTimer = null; }
        for (var i = 0; i < roomHooks.length; i++) { try { roomHooks[i].detach(); } catch(e) {} }
        roomHooks = [];
        myPlayer = null;
        targetEnemy = null;
        enabled = false;
        sendLog('info', '自瞄', '已禁用');
        sendStatus('aim', false);
      },
      isEnabled: function() { return enabled; },
      setConfig: function(cfg) {
        if (cfg.smoothness !== undefined) CONFIG.smoothness = cfg.smoothness;
        if (cfg.maxAimDistance !== undefined) CONFIG.maxAimDistance = cfg.maxAimDistance;
        if (cfg.maxAngleFOV !== undefined) CONFIG.maxAngleFOV = cfg.maxAngleFOV;
        if (cfg.visibilityCheck !== undefined) CONFIG.visibilityCheck = cfg.visibilityCheck;
        if (cfg.autoAim !== undefined) CONFIG.autoAim = cfg.autoAim;
      },
      getConfig: function() {
        return { smoothness: CONFIG.smoothness, maxAngleFOV: CONFIG.maxAngleFOV, maxAimDistance: CONFIG.maxAimDistance, autoAim: CONFIG.autoAim, visibilityCheck: CONFIG.visibilityCheck };
      }
    };
  })();

  // ====================================================================
  // 模块 12: 金刚不坏 — Hook Entity.OnEntityHurt
  // ====================================================================
  var godModeModule = (function() {
    var enabled = false;
    var hurtHook = null;
    var playerHurtHook = null;
    var refreshTimer = null;
    var cachedMyPlayer = null;
    var isMyPlayerFn = null;
    var isDeadFn = null;
    var singletonGetter = null;

    var RVA = {
      SingletonGet:                    0x4A8170,
      GM_Singleton_MethodInfo:         0xE1CE64,
      Player_get_isMyPlayer:           0xB55FD0,
      Entity_get_isDead:               0xB400E0,
      Entity_get_team:                 0x1E0070,
      Entity_OnEntityHurt:             0xB3F470,
      Component_get_transform:         0x32CF40,
      Transform_get_position:          0x3F42B0,
    };

    var OFF = {
      GM_allPlayers:      0x1C,
      GM_playersBL:       0x20,
      GM_playersGR:       0x28,
      E_team:             0x20,
      Arr_len:            0x0C,
      Arr_data:           0x10,
      List_items:         0x08,
      List_size:          0x0C,
      ptrSize:            4,
      Dmg_type:           0x08,
    };

    function initNativeFunctions() {
      var mod = getGameAssembly();
      if (!mod) return false;
      var base = mod.base;
      try {
        singletonGetter = new NativeFunction(base.add(RVA.SingletonGet), 'pointer', ['pointer']);
      } catch(e) { sendLog('error', 'HP', 'singletonGetter 失败: ' + e.message); return false; }
      try {
        isMyPlayerFn = new NativeFunction(base.add(RVA.Player_get_isMyPlayer), 'bool', ['pointer', 'pointer']);
      } catch(e) { sendLog('error', 'HP', 'isMyPlayerFn 失败: ' + e.message); return false; }
      try {
        isDeadFn = new NativeFunction(base.add(RVA.Entity_get_isDead), 'bool', ['pointer', 'pointer']);
      } catch(e) { sendLog('error', 'HP', 'isDeadFn 失败: ' + e.message); return false; }
      sendLog('success', 'HP', 'NativeFunction 全部就绪');
      return true;
    }

    function getGM() {
      try {
        var base = getGameAssembly().base;
        var mi = base.add(RVA.GM_Singleton_MethodInfo).readPointer();
        if (mi.isNull()) return singletonGetter(ptr(0));
        var gm = singletonGetter(mi);
        if (gm.isNull()) return null;
        return gm;
      } catch(e) { return null; }
    }

    function readList(listPtr) {
      var result = [];
      if (!listPtr || listPtr.isNull()) return result;
      try {
        var items = listPtr.add(OFF.List_items).readPointer();
        if (!items || items.isNull()) return result;
        var count = listPtr.add(OFF.List_size).readS32();
        for (var i = 0; i < count; i++) {
          var elem = items.add(OFF.Arr_data + i * OFF.ptrSize).readPointer();
          if (elem && !elem.isNull()) result.push(elem);
        }
      } catch(e) {}
      return result;
    }

    function readArray(arrPtr) {
      var result = [];
      if (!arrPtr || arrPtr.isNull()) return result;
      try {
        var len = arrPtr.add(OFF.Arr_len).readU32();
        for (var i = 0; i < len; i++) {
          var elem = arrPtr.add(OFF.Arr_data + i * OFF.ptrSize).readPointer();
          if (elem && !elem.isNull()) result.push(elem);
        }
      } catch(e) {}
      return result;
    }

    function isValidPlayer(pp) {
      if (!pp || pp.isNull()) return false;
      try {
        var team = pp.add(OFF.E_team).readS32();
        return (team === 0 || team === 1 || team === 2);
      } catch(e) { return false; }
    }

    function getAllPlayers(gm) {
      var map = {};
      var arr = readArray(gm.add(OFF.GM_allPlayers).readPointer());
      for (var i = 0; i < arr.length; i++) {
        if (isValidPlayer(arr[i])) map[arr[i].toString()] = arr[i];
      }
      var bl = readList(gm.add(OFF.GM_playersBL).readPointer());
      for (var i = 0; i < bl.length; i++) {
        if (isValidPlayer(bl[i])) map[bl[i].toString()] = bl[i];
      }
      var gr = readList(gm.add(OFF.GM_playersGR).readPointer());
      for (var i = 0; i < gr.length; i++) {
        if (isValidPlayer(gr[i])) map[gr[i].toString()] = gr[i];
      }
      return Object.values(map);
    }

    function findMyPlayer() {
      try {
        var gm = getGM();
        if (!gm || gm.isNull()) return null;
        var all = getAllPlayers(gm);
        for (var i = 0; i < all.length; i++) {
          try { if (isMyPlayerFn(all[i], ptr(0))) return all[i]; } catch(e) {}
        }
      } catch(e) {}
      return null;
    }

    function installHooks(base) {
      var entityHurtAddr = base.add(RVA.Entity_OnEntityHurt);
      var diagCount = 0;
      var hookHandler = {
        onEnter: function(args) {
          var entity = args[0];
          if (!entity || entity.isNull()) return;
          if (!cachedMyPlayer || cachedMyPlayer.isNull()) return;
          var isMyPlayer = entity.equals(cachedMyPlayer);
          if (isMyPlayer) {
            var espPtr = ptr(this.context.esp.toString());
            var structStart = espPtr.add(8);
            var typeFieldAddr = structStart.add(OFF.Dmg_type);
            var oldType = typeFieldAddr.readS32();
            typeFieldAddr.writeS32(4);
            if (moduleLogCounts['HP'] < 30) {
              sendLog('info', 'HP', '玩家掉血已拦截! (oldType=' + oldType + ')');
            }
          }
        }
      };
      hurtHook = Interceptor.attach(entityHurtAddr, hookHandler);
      sendLog('success', 'HP', 'Entity_OnEntityHurt Hook 已安装 (RVA: 0xB3F470)');
      var playerHurtAddr = base.add(0xB516B0);
      try {
        playerHurtHook = Interceptor.attach(playerHurtAddr, hookHandler);
        sendLog('success', 'HP', 'Player_OnEntityHurt 兜底Hook已安装 (RVA: 0xB516B0)');
      } catch(e) { sendLog('warn', 'HP', 'Player_OnEntityHurt Hook失败: ' + e.message + ' (不影响)'); }
    }

    function startRefresh() {
      if (refreshTimer) return;
      refreshTimer = setInterval(function() {
        if (!cachedMyPlayer || cachedMyPlayer.isNull()) {
          var found = findMyPlayer();
          if (found && !found.isNull()) {
            cachedMyPlayer = found;
            sendLog('info', 'HP', '已找到玩家: ' + found);
          }
        }
        if (cachedMyPlayer && !cachedMyPlayer.isNull()) {
          try {
            var gm = getGM();
            if (gm && !gm.isNull()) {
              var all = getAllPlayers(gm);
              var found = false;
              for (var i = 0; i < all.length; i++) {
                if (all[i].equals(cachedMyPlayer)) { found = true; break; }
              }
              if (!found) {
                sendLog('info', 'HP', '玩家已离开（房间切换），重置');
                cachedMyPlayer = null;
              }
            }
          } catch(e) { cachedMyPlayer = null; }
        }
      }, 2000);
    }

    function stopRefresh() {
      if (refreshTimer) {
        clearInterval(refreshTimer);
        refreshTimer = null;
      }
    }

    return {
      enable: function() {
        if (enabled) {
          sendLog('info', 'HP', '无敌模式已启用，跳过');
          return;
        }
        var mod = getGameAssembly();
        if (!mod) { sendLog('error', 'HP', '未找到 GameAssembly.dll'); return; }
        if (!initNativeFunctions()) { sendLog('error', 'HP', 'NativeFunction 初始化失败'); return; }
        cachedMyPlayer = findMyPlayer();
        if (cachedMyPlayer) {
          sendLog('info', 'HP', '已找到玩家: ' + cachedMyPlayer);
        } else {
          sendLog('info', 'HP', '等待玩家出现（自动刷新中）...');
        }
        installHooks(mod.base);
        startRefresh();
        enabled = true;
        sendLog('success', 'HP', '无敌模式已启用!');
        sendStatus('godmode', true);
      },
      disable: function() {
        if (!enabled) return;
        if (hurtHook) { try { hurtHook.detach(); } catch(e) {} hurtHook = null; }
        if (playerHurtHook) { try { playerHurtHook.detach(); } catch(e) {} playerHurtHook = null; }
        stopRefresh();
        cachedMyPlayer = null;
        enabled = false;
        sendLog('info', 'HP', '无敌模式已禁用');
        sendStatus('godmode', false);
      },
      isEnabled: function() { return enabled; },
      getStatus: function() {
        return {
          enabled: enabled,
          hookInstalled: hurtHook !== null,
          myPlayer: cachedMyPlayer ? cachedMyPlayer.toString() : null,
        };
      }
    };
  })();

  // ====================================================================
  // 模块 13: 射速变快 — 终极武器修改
  // ====================================================================
  var speedGunModule = (function() {
    var enabled = false;
    var hooks = [];
    var isMyWeaponFn = null;
    var getCharAnim = null;
    var setAnimSpeed = null;
    var isPlayerShooting = false;

    return {
      enable: function() {
        if (enabled) return;
        var mod = getGameAssembly();
        if (!mod) { sendLog('error', '射速', '未找到 GameAssembly.dll'); return; }
        var base = mod.base;

        try {
          isMyWeaponFn = new NativeFunction(base.add(0xB6E1D0), "bool", ["pointer", "pointer"]);
          getCharAnim = new NativeFunction(base.add(0xB35310), "pointer", ["pointer", "pointer"]);
          setAnimSpeed = new NativeFunction(base.add(0xAA8C30), "void", ["pointer", "float", "pointer"]);
        } catch(e) {
          sendLog('error', '射速', 'NativeFunction 初始化失败: ' + e.message);
          return;
        }

        // 1) WPN_Gun.AnimSpeedSetting — 枪械(背包)动画加速
        try {
          hooks.push(Interceptor.attach(base.add(0xB60B00), {
            onEnter: function(args) { this.self = args[0]; },
            onLeave: function(retVal) {
              if (!this.self) return;
              try {
                if (isMyWeaponFn(this.self, ptr(0))) {
                  var anim = getCharAnim(this.self, ptr(0));
                  if (!anim.isNull()) {
                    setAnimSpeed(anim, 10.0, ptr(0));
                  }
                }
              } catch(e) {}
            }
          }));
        } catch(e) { sendLog('warn', '射速', 'WPN_Gun.AnimSpeedSetting Hook失败: ' + e.message); }

        // 1.5) WPN_RPG.AnimSpeedSetting — RPG/AT4 动画加速
        try {
          hooks.push(Interceptor.attach(base.add(0xB66CA0), {
            onEnter: function(args) { this.self = args[0]; },
            onLeave: function(retVal) {
              if (!this.self) return;
              try {
                if (isMyWeaponFn(this.self, ptr(0))) {
                  var anim = getCharAnim(this.self, ptr(0));
                  if (!anim.isNull()) {
                    setAnimSpeed(anim, 10.0, ptr(0));
                  }
                }
              } catch(e) {}
            }
          }));
        } catch(e) { sendLog('warn', '射速', 'WPN_RPG.AnimSpeedSetting Hook失败: ' + e.message); }

        // 1.6) WPN_GrenadeGun.AnimSpeedSetting — 榴弹枪动画加速
        try {
          hooks.push(Interceptor.attach(base.add(0xB5F7A0), {
            onEnter: function(args) {
              this.self = args[0];
              try {
                if (isMyWeaponFn(this.self, ptr(0))) {
                  var realData = this.self.add(0xEC).readPointer();
                  if (!realData.isNull()) {
                    realData.add(0xD0).writeFloat(10.0);
                  }
                }
              } catch(e) {}
            },
            onLeave: function(retVal) {
              if (!this.self) return;
              try {
                if (isMyWeaponFn(this.self, ptr(0))) {
                  var anim = getCharAnim(this.self, ptr(0));
                  if (!anim.isNull()) {
                    setAnimSpeed(anim, 10.0, ptr(0));
                  }
                }
              } catch(e) {}
            }
          }));
        } catch(e) { sendLog('warn', '射速', 'WPN_GrenadeGun.AnimSpeedSetting Hook失败: ' + e.message); }

        // 2) GunShoot — 清除射击间隔 + 半自动 => 全自动
        try {
          hooks.push(Interceptor.attach(base.add(0xB624C0), {
            onEnter: function(args) {
              this.self = args[0];
              try {
                if (isMyWeaponFn(this.self, ptr(0))) {
                  isPlayerShooting = true;
                }
              } catch(e) {}
            },
            onLeave: function(retVal) {
              if (!this.self) return;
              try {
                if (isMyWeaponFn(this.self, ptr(0))) {
                  this.self.add(0x110).writeFloat(0.0);   // nextAllowedShootTime
                  this.self.add(0x108).writeS32(0);       // semiGunFireLinkState = None
                }
              } catch(e) {}
              isPlayerShooting = false;
            }
          }));
        } catch(e) { sendLog('warn', '射速', 'GunShoot Hook失败: ' + e.message); }

        // 2.5) WPN_Gun.get_isSemiGun — 半自动→全自动
        try {
          hooks.push(Interceptor.attach(base.add(0xB63AD0), {
            onLeave: function(retVal) { retVal.replace(0); }
          }));
        } catch(e) { sendLog('warn', '射速', 'get_isSemiGun Hook失败: ' + e.message); }

        // 3) WPN_Gun.OnGenerateFromOwner — 补给箱枪械创建时加速
        try {
          hooks.push(Interceptor.attach(base.add(0xB62900), {
            onEnter: function(args) { this.self = args[0]; },
            onLeave: function(retVal) {
              if (!this.self) return;
              try {
                if (isMyWeaponFn(this.self, ptr(0))) {
                  var anim = getCharAnim(this.self, ptr(0));
                  if (!anim.isNull()) {
                    setAnimSpeed(anim, 10.0, ptr(0));
                  }
                }
              } catch(e) {}
            }
          }));
        } catch(e) { sendLog('warn', '射速', 'OnGenerateFromOwner Hook失败: ' + e.message); }

        // 4) WPN_RPG.OnGenerateFromOwner — 补给箱RPG/AT4创建时加速
        try {
          hooks.push(Interceptor.attach(base.add(0xB67740), {
            onEnter: function(args) { this.self = args[0]; },
            onLeave: function(retVal) {
              if (!this.self) return;
              try {
                if (isMyWeaponFn(this.self, ptr(0))) {
                  var anim = getCharAnim(this.self, ptr(0));
                  if (!anim.isNull()) {
                    setAnimSpeed(anim, 10.0, ptr(0));
                  }
                  var realData = this.self.add(0xF0).readPointer();
                  if (!realData.isNull()) {
                    realData.add(0xF0).writeFloat(10.0);
                    realData.add(0xEC).writeFloat(10.0);
                  }
                }
              } catch(e) {}
            }
          }));
        } catch(e) { sendLog('warn', '射速', 'RPG OnGenerateFromOwner Hook失败: ' + e.message); }

        // 5) WPN_RPG.OnFireBtnPressed — RPG/AT4 半自动绕过
        try {
          hooks.push(Interceptor.attach(base.add(0xB67700), {
            onEnter: function(args) { this.self = args[0]; },
            onLeave: function(retVal) {
              if (!this.self) return;
              try {
                if (isMyWeaponFn(this.self, ptr(0))) {
                  this.self.add(0xF8).writeS32(1);       // fireState = Firing
                  var realData = this.self.add(0xF0).readPointer();
                  if (!realData.isNull()) {
                    realData.add(0xF0).writeFloat(10.0); // WD_RPG.fireAnimRate
                    realData.add(0xEC).writeFloat(10.0); // WD_RPG.reloadAnimRate
                  }
                }
              } catch(e) {}
            }
          }));
        } catch(e) { sendLog('warn', '射速', 'RPG OnFireBtnPressed Hook失败: ' + e.message); }

        // 6) Recoil.OnGunShot — 清零后坐力
        try {
          hooks.push(Interceptor.attach(base.add(0xB19980), {
            onEnter: function(args) { this.self = args[0]; },
            onLeave: function(retVal) {
              if (!isPlayerShooting || !this.self) return;
              this.self.add(0x68).writeFloat(0.0);
              this.self.add(0x6C).writeFloat(0.0);
              this.self.add(0x70).writeFloat(0.0);
              this.self.add(0x74).writeFloat(0.0);
              this.self.add(0xA8).writeS32(0);
            }
          }));
        } catch(e) { sendLog('warn', '射速', 'Recoil.OnGunShot Hook失败: ' + e.message); }

        // 7) Recoil.GetCurrentPerturb — 强制 0 扩散
        try {
          hooks.push(Interceptor.attach(base.add(0xB19420), {
            onLeave: function(retVal) { retVal.replace(0.0); }
          }));
        } catch(e) { sendLog('warn', '射速', 'Recoil.GetCurrentPerturb Hook失败: ' + e.message); }

        enabled = true;
        sendLog('success', '射速', '射速变快已启用');
        sendStatus('speedgun', true);
      },
      disable: function() {
        if (!enabled) return;
        for (var i = 0; i < hooks.length; i++) {
          try { hooks[i].detach(); } catch(e) {}
        }
        hooks = [];
        enabled = false;
        sendLog('info', '射速', '射速变快已禁用');
        sendStatus('speedgun', false);
      },
      isEnabled: function() { return enabled; }
    };
  })();

  // ====================================================================
  // 模块 14: 生化模式-英雄技能无冷却
  // ====================================================================
  var skillCdModule = (function() {
    var enabled = false;
    var myPlayerPtr = null;
    var _endColdFn = null;
    var _noCdTimer = null;
    var hooks = [];

    function readPtr(addr) {
        try { if (!addr || addr.isNull()) return null; var v = addr.readPointer(); return (v && !v.isNull()) ? v : null; } catch (e) { return null; }
    }
    function readI32(addr) { try { return addr ? addr.readS32() : null; } catch (e) { return null; } }
    function readF32(addr) { try { return addr ? addr.readFloat() : null; } catch (e) { return null; } }
    function readU8(addr) { try { return addr ? addr.readU8() : null; } catch (e) { return null; } }

    function scanSkillSteps(pp) {
        var ps = readPtr(pp.add(0xB0));
        if (!ps) { sendLog('error', '技能CD', 'PlayerSkills 为空'); return; }
        var arr = readPtr(ps.add(0x08));
        if (!arr) { sendLog('error', '技能CD', 'Skill[] 为空'); return; }
        var len = readI32(arr.add(0x0C));
        if (!len || len <= 0 || len > 20) return;
        var found = 0;
        for (var i = 0; i < len; i++) {
            var sp = readPtr(arr.add(0x10 + 4 * i));
            if (!sp) continue;
            var coldFinish = readF32(sp.add(0x1C));
            var coldTime = readF32(sp.add(0x24));
            if (coldFinish !== null || coldTime !== null) {
                found++;
            }
        }
        if (found > 0) {
            sendLog('info', '技能CD', '找到 ' + found + ' 个技能');
        }
    }

    function scanAndEndCold() {
        if (!myPlayerPtr) return;
        var ps = readPtr(myPlayerPtr.add(0xB0));
        if (!ps) return;
        var arr = readPtr(ps.add(0x08));
        if (!arr) return;
        var len = readI32(arr.add(0x0C));
        if (!len || len <= 0 || len > 20) return;

        var called = 0; 
        for (var i = 0; i < len; i++) {
            var sp = readPtr(arr.add(0x10 + 4 * i));
            if (!sp) continue;
            var coldFinish = readF32(sp.add(0x1C));
            var coldTime = readF32(sp.add(0x24));
            if (coldFinish !== null || coldTime !== null) {
                try {
                    _endColdFn(sp);
                    called++;
                } catch (e) {}
            }
        }
    }

    return {
        enable: function() {
            if (enabled) return;
            var mod = getGameAssembly();
            if (!mod) { sendLog('error', '技能CD', '未找到 GameAssembly.dll'); return; }
            var base = mod.base;

            // 初始化 EndCold 函数
            try {
                _endColdFn = new NativeFunction(base.add(0xAE1BC0), 'void', ['pointer']);
                sendLog('info', '技能CD', 'EndCold 函数就绪 (RVA 0xAE1BC0)');
            } catch (e) {
                sendLog('error', '技能CD', 'EndCold 创建失败: ' + e);
                return;
            }

            // Hook isMyPlayer 来捕获玩家指针（支持房间切换时自动更新）
            try {
                var addrIsMy = base.add(0xB55FD0);
                var origIsMy = new NativeFunction(addrIsMy, 'bool', ['pointer', 'pointer']);
                Interceptor.replace(addrIsMy, new NativeCallback(function (playerPtr, methodInfo) {
                    try {
                        var result = origIsMy(playerPtr, methodInfo);
                        if (result) {
                            // 检测指针是否变化（房间切换时会有新指针）
                            if (!myPlayerPtr || !myPlayerPtr.equals(playerPtr)) {
                                myPlayerPtr = playerPtr;
                                scanSkillSteps(playerPtr);
                                sendLog('info', '技能CD', '玩家指针已更新: ' + playerPtr);
                            }
                        }
                        return result;
                    } catch (e) { return false; }
                }, 'bool', ['pointer', 'pointer']));
                hooks.push({ type: 'replace', addr: addrIsMy, orig: origIsMy });
                sendLog('success', '技能CD', 'isMyPlayer Hook OK');
            } catch (e) { sendLog('error', '技能CD', 'isMyPlayer Hook 失败: ' + e); }

            // 兜底 Hook Player.Update 来捕获玩家（支持房间切换时自动更新）
            try {
                var addrUpdate = base.add(0xB551D0);
                hooks.push(Interceptor.attach(addrUpdate, {
                    onEnter: function (args) {
                        var p = args[0];
                        if (!p || p.isNull()) return;
                        var cd = readPtr(p.add(0x94));
                        if (!cd) return;
                        if (readU8(cd.add(0x1C))) return;
                        // 检测指针是否变化
                        if (!myPlayerPtr || !myPlayerPtr.equals(p)) {
                            myPlayerPtr = p;
                            scanSkillSteps(p);
                        }
                    }
                }));
                sendLog('success', '技能CD', 'Player.Update Hook OK');
            } catch (e) { sendLog('warn', '技能CD', 'Player.Update Hook 失败: ' + e); }

            // 兜底 Hook get_nickName 来捕获玩家（支持房间切换时自动更新）
            try {
                var addrNick = base.add(0xB50810);
                hooks.push(Interceptor.attach(addrNick, {
                    onEnter: function (args) {
                        var p = args[0];
                        if (!p || p.isNull()) return;
                        var cd = readPtr(p.add(0x94));
                        if (!cd) return;
                        if (readU8(cd.add(0x1C))) return;
                        // 检测指针是否变化
                        if (!myPlayerPtr || !myPlayerPtr.equals(p)) {
                            myPlayerPtr = p;
                            scanSkillSteps(p);
                        }
                    }
                }));
                sendLog('success', '技能CD', 'get_nickName Hook OK');
            } catch (e) { sendLog('warn', '技能CD', 'get_nickName Hook 失败: ' + e); }

            // 立即执行一次，然后设置定时器
            scanAndEndCold();
            _noCdTimer = setInterval(scanAndEndCold, 200);

            enabled = true;
            sendLog('success', '技能CD', '已开启 — 每 200ms 调用 EndCold()');
            sendStatus('skillcd', true);
        },
        disable: function() {
            if (!enabled) return;

            // 还原所有 Hook
            for (var i = 0; i < hooks.length; i++) {
                try {
                    if (hooks[i].type === 'replace') {
                        Interceptor.revert(hooks[i].addr);
                    } else {
                        hooks[i].detach();
                    }
                } catch(e) {}
            }
            hooks = [];

            // 清理定时器
            if (_noCdTimer) {
                clearInterval(_noCdTimer);
                _noCdTimer = null;
            }

            // 重置状态
            myPlayerPtr = null;
            enabled = false;
            sendLog('info', '技能CD', '已关闭');
            sendStatus('skillcd', false);
        },
        isEnabled: function() { return enabled; }
    };
  })();

  // ====================================================================
  // 模块 15: 天机傀儡 — 修改 ClientData.isBot (v2)
  // ====================================================================
  var isBotModule = (function() {
    var enabled = false;
    var localPlayer = null;
    var clientData = null;
    var dumped = false;
    var logCount = 0;
    var MAX_LOG = 15;
    var hookInstalled = false;
    var retryInterval = null;
    var addrIsMy = null;

    var RVA_IS_MY_PLAYER = 0xB55FD0;
    var OFF_CLIENT = 0x94;
    var OFF_ISBOT = 0x1C;
    var OFF_NICK = 0x10;

    function log(level, msg) {
      if (logCount >= MAX_LOG && level !== 'error') return;
      logCount++;
      send({ type: 'log', level: level, module: 'isBot', message: msg });
    }

    function readStr(ptr) {
      try {
        var obj = ptr.readPointer();
        if (!obj || obj.isNull()) return '?';
        var len = obj.add(-4).readS32();
        if (len < 0 || len > 64) return '?';
        return obj.readUtf8String(len);
      } catch(e) { return '?'; }
    }

    function dump() {
      if (!clientData) return;
      var bot = clientData.add(OFF_ISBOT).readU8();
      var nick = readStr(clientData.add(OFF_NICK));
      log('info', localPlayer + '|' + clientData + '|0x1C:' + bot + '|nick:' + nick);
    }

    function writeBot(val) {
      if (!clientData) return false;
      try {
        clientData.add(OFF_ISBOT).writeU8(val);
        var after = clientData.add(OFF_ISBOT).readU8();
        log('info', 'isBot=' + after + ' (写入' + val + ')');
        return true;
      } catch(e) { return false; }
    }

    function tryWriteBotOnCapture() {
      if (clientData) {
        writeBot(1);
        sendLog('info', '天机傀儡', 'Bot 模式已应用');
        if (retryInterval) {
          clearInterval(retryInterval);
          retryInterval = null;
        }
        return true;
      }
      return false;
    }

    function installHook() {
      if (hookInstalled) return;
      var mod = getGameAssembly();
      if (!mod) { sendLog('error', '天机傀儡', '未找到 GameAssembly.dll'); return; }

      var base = mod.base;
      addrIsMy = base.add(RVA_IS_MY_PLAYER);
      var origIsMy = new NativeFunction(addrIsMy, 'bool', ['pointer', 'pointer']);

      Interceptor.replace(addrIsMy, new NativeCallback(function (playerPtr, methodInfo) {
        var result = origIsMy(playerPtr, methodInfo);
        if (result && !localPlayer) {
          localPlayer = playerPtr;
          var cd = playerPtr.add(OFF_CLIENT).readPointer();
          if (cd) {
            clientData = cd;
            dumped = true;
            setTimeout(dump, 2000);
            tryWriteBotOnCapture();
          }
        }
        return result;
      }, 'bool', ['pointer', 'pointer']));

      hookInstalled = true;
    }

    function uninstallHook() {
      if (hookInstalled && addrIsMy) {
        try { Interceptor.revert(addrIsMy); } catch(e) {}
        hookInstalled = false;
        addrIsMy = null;
      }
    }

    return {
      enable: function() {
        if (enabled) return;

        installHook();

        // 如果 clientData 已捕获，立刻写 bot=1
        if (tryWriteBotOnCapture()) {
          enabled = true;
          sendLog('success', '天机傀儡', '已启用');
          sendStatus('isbot', true);
          return;
        }

        // 否则轮询等待 clientData（最多等 10 秒）
        var retries = 0;
        retryInterval = setInterval(function() {
          if (clientData) {
            tryWriteBotOnCapture();
          }
          retries++;
          if (retries > 20) {
            clearInterval(retryInterval);
            retryInterval = null;
            sendLog('error', '天机傀儡', '等待本地玩家超时');
          }
        }, 500);

        enabled = true;
        sendLog('success', '天机傀儡', '已启用（等待本地玩家）');
        sendStatus('isbot', true);
      },
      disable: function() {
        if (!enabled) return;
        if (retryInterval) {
          clearInterval(retryInterval);
          retryInterval = null;
        }
        writeBot(0);
        uninstallHook();
        enabled = false;
        localPlayer = null;
        clientData = null;
        log('info', '已禁用');
        sendStatus('isbot', false);
      },
      isEnabled: function() { return enabled; },
      modify: function() {
        if (writeBot(1)) return JSON.stringify({ success: true, bot: 1 });
        return JSON.stringify({ success: false });
      },
      restore: function() {
        if (writeBot(0)) return JSON.stringify({ success: true, bot: 0 });
        return JSON.stringify({ success: false });
      },
      stop: function() {
        if (writeBot(0)) return JSON.stringify({ success: true, bot: 0 });
        return JSON.stringify({ success: false });
      },
      status: function() {
        return JSON.stringify({
          player: localPlayer ? localPlayer.toString() : null,
          cd: clientData ? clientData.toString() : null,
          bot: clientData ? clientData.add(OFF_ISBOT).readU8() : null
        });
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
    ammo: ammoModule,
    movespeed: moveSpeedModule,
    ammoplus: reloadSpeedModule,
    range: rangeModule,
    gather: gatherModule,
    gravity: gravityJumpModule,
    roundskip: roundSkipModule,
    aim: aimModule,
    godmode: godModeModule,
    speedgun: speedGunModule,
    isbot: isBotModule,
    skillcd: skillCdModule
  };

  // ====================================================================
  // 模块 16: 多人生化特性选择器 (Nano4T)
  // ====================================================================
  var nano4tModule = (function() {
    var nano4tBase = null;
    var NANO4T_ATTR_PTR = {};
    var NANO4T_WANTED_GHOST = 9;
    var NANO4T_WANTED_HUMAN = 19;
    var NANO4T_READY = false;
    var NANO4T_MODE_DESTROYED = false;
    var hookHandles = [];

    function rdPtr(a) { try { return a.readPointer(); } catch(e) { return ptr(0); } }
    function rdS32(a) { try { return a.readS32(); } catch(e) { return 0; } }

    function loadAttrs() {
      try {
        var fn = new NativeFunction(nano4tBase.add(0xB467A0), 'pointer', []);
        var n4 = fn();
        if (!n4 || n4.isNull()) return false;
        var aa = rdPtr(n4.add(0xD8));
        if (aa.isNull()) return false;
        var attrs = rdPtr(aa.add(0x14));
        if (attrs.isNull()) return false;
        var len = attrs.add(0x0C).readU32();
        NANO4T_ATTR_PTR = {};
        for (var i = 0; i < len && i < 50; i++) {
          var a = rdPtr(attrs.add(0x10 + i*4));
          if (!a.isNull()) NANO4T_ATTR_PTR[rdS32(a.add(0x0C))] = a;
        }
        return Object.keys(NANO4T_ATTR_PTR).length > 0;
      } catch(e) { return false; }
    }

    function clearHooks() {
      for (var i = 0; i < hookHandles.length; i++) {
        try { hookHandles[i].detach(); } catch(e) {}
      }
      hookHandles = [];
    }

    function installHooks() {
      clearHooks();
      hookHandles.push(Interceptor.attach(nano4tBase.add(0xB4C420), {
        onEnter: function(args) {
          this._isNano = !args[1].isNull();
        },
        onLeave: function(retval) {
          if (NANO4T_MODE_DESTROYED) return;
          var id = this._isNano ? NANO4T_WANTED_GHOST : NANO4T_WANTED_HUMAN;
          var p = NANO4T_ATTR_PTR[id];
          if (p && !p.isNull()) {
            try { retval.replace(p); } catch(e) {}
          }
        }
      }));
      hookHandles.push(Interceptor.attach(nano4tBase.add(0xB44320), {
        onEnter: function(args) {
          NANO4T_MODE_DESTROYED = true;
          NANO4T_READY = false;
          send(JSON.stringify({ type: 'nano4t_destroyed' }));
        }
      }));
    }

    return {
      init: function() {
        clearHooks();
        NANO4T_READY = false;
        NANO4T_MODE_DESTROYED = false;
        NANO4T_ATTR_PTR = {};
        var mod = Process.findModuleByName('GameAssembly.dll');
        if (!mod) {
          send(JSON.stringify({ type: 'nano4t_error', msg: '未检测到游戏进程' }));
          return;
        }
        nano4tBase = mod.base;
        var fn = new NativeFunction(nano4tBase.add(0xB467A0), 'pointer', []);
        var n4 = fn();
        if (!n4 || n4.isNull()) {
          send(JSON.stringify({ type: 'nano4t_error', msg: '未进入多人生化模式' }));
        } else if (!loadAttrs()) {
          send(JSON.stringify({ type: 'nano4t_error', msg: '未进入多人生化模式房间' }));
        } else {
          installHooks();
          NANO4T_READY = true;
          send(JSON.stringify({ type: 'nano4t_ready', ids: Object.keys(NANO4T_ATTR_PTR).sort() }));
        }
      },
      set: function(g, h) {
        NANO4T_WANTED_GHOST = g;
        NANO4T_WANTED_HUMAN = h;
        send(JSON.stringify({ type: 'nano4t_set', g: g, h: h }));
      },
      getCurrent: function() {
        var result;
        if (!NANO4T_READY || NANO4T_MODE_DESTROYED) {
          result = JSON.stringify({ type: 'nano4t_current', g: -1, h: -1, ok: false });
          send(result);
          return result;
        }
        try {
          var fn2 = new NativeFunction(nano4tBase.add(0xB467A0), 'pointer', []);
          var inst = fn2();
          if (!inst || inst.isNull()) {
            result = JSON.stringify({ type: 'nano4t_current', g: -1, h: -1, ok: true });
            send(result);
            return result;
          }
          var an = rdPtr(inst.add(0xE0));
          var ah = rdPtr(inst.add(0xE4));
          result = JSON.stringify({
            type: 'nano4t_current',
            g: an.isNull() ? -1 : rdS32(an.add(0x0C)),
            h: ah.isNull() ? -1 : rdS32(ah.add(0x0C)),
            ok: true
          });
          send(result);
          return result;
        } catch(e) {
          result = JSON.stringify({ type: 'nano4t_current', g: -1, h: -1, ok: true });
          send(result);
          return result;
        }
      },
      healthCheck: function() {
        var result;
        if (NANO4T_MODE_DESTROYED) {
          result = JSON.stringify({ type: 'nano4t_dead' });
          send(result);
          return result;
        }
        try {
          var fn2 = new NativeFunction(nano4tBase.add(0xB467A0), 'pointer', []);
          var inst = fn2();
          if (!inst || inst.isNull()) {
            NANO4T_MODE_DESTROYED = true;
            NANO4T_READY = false;
            result = JSON.stringify({ type: 'nano4t_dead' });
            send(result);
            return result;
          }
          var aa = rdPtr(inst.add(0xD8));
          if (aa.isNull()) {
            NANO4T_MODE_DESTROYED = true;
            NANO4T_READY = false;
            result = JSON.stringify({ type: 'nano4t_dead' });
            send(result);
            return result;
          }
          result = JSON.stringify({ type: 'nano4t_alive' });
          send(result);
          return result;
        } catch(e) {
          NANO4T_MODE_DESTROYED = true;
          NANO4T_READY = false;
          result = JSON.stringify({ type: 'nano4t_dead' });
          send(result);
          return result;
        }
      },
      destroy: function() {
        clearHooks();
        NANO4T_READY = false;
        NANO4T_MODE_DESTROYED = false;
        NANO4T_ATTR_PTR = {};
        nano4tBase = null;
      }
    };
  })();

  function onToggle(data) {
    try {
      var featureName = data.feature;
      var enable = data.enable;

      if (featureName === 'knife_speed') {
        knifeModule.setSpeed(enable);
      } else if (featureName === 'movespeed_speed') {
        moveSpeedModule.setSpeed(enable);
      } else if (featureName === 'gravity_config') {
        // gravity_config: { g, j, m }
        gravityJumpModule.setconfig(enable.g, enable.j, enable.m);
      } else if (featureName === 'range_config') {
        rangeModule.setRange(enable);
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
    } catch(e) {
      sendLog('error', '系统', 'toggle异常: ' + (e.message || e));
    } finally {
      recv('toggle', onToggle);
    }
  }

  recv('toggle', onToggle);

  rpc.exports = {
    gather: function() {
      var result = gatherModule.gather();
      send(JSON.stringify({ type: 'gather_result', data: result }));
      return JSON.stringify(result);
    },
    setGravityConfig: function(g, j, m) {
      return JSON.stringify(gravityJumpModule.setconfig(g, j, m));
    },
    resetGravity: function() {
      return JSON.stringify(gravityJumpModule.resetall());
    },
    getGravityStatus: function() {
      return JSON.stringify(gravityJumpModule.getstatus());
    },
    roundskip: function() {
      roundSkipModule.enable();
      return JSON.stringify(roundSkipModule.skipround());
    },
    getRoundStatus: function() {
      roundSkipModule.enable();
      return JSON.stringify(roundSkipModule.getstatus());
    },
    resetRound: function() {
      return JSON.stringify(roundSkipModule.reset());
    },
    setRange: function(multiplier) {
      rangeModule.setRange(multiplier);
      return JSON.stringify({ ok: true });
    },
    nano4tinit: function() {
      nano4tModule.init();
      return JSON.stringify({ ok: true });
    },
    nano4tset: function(g, h) {
      nano4tModule.set(g, h);
      return JSON.stringify({ ok: true });
    },
    nano4tgetcurrent: function() {
      return nano4tModule.getCurrent();
    },
    nano4thealthcheck: function() {
      return nano4tModule.healthCheck();
    }
  };

  sendLog('info', '系统', '游戏修改器 Agent v1.3 已加载');
  sendLog('info', '系统', '原有功能: 快刀v16 | 无限时间 | 无后座力v14 | 无限子弹plan4');
  sendLog('info', '系统', 'v1.1新增: 滑板鞋3x/6x | 快速换弹 | 剑气化丝50x');
  sendLog('info', '系统', 'v1.2新增: 聚怪功能');
  sendLog('info', '系统', 'v1.3新增: 轻重力/高跳 | 回合跳过');
  sendLog('info', '系统', '快刀支持速度切换: 3x / 5x / 10x');
  sendLog('info', '系统', '请先附加到游戏进程，然后开启对应功能');
  sendLog('info', '系统', '架构: ' + Process.arch + ', 平台: ' + Process.platform);

  setTimeout(function() { getGameAssembly(); }, 100);
})();
"""


class GameModifierApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("游戏修改器控制台 - 全功能整合包 v1.5")
        self.geometry("610x700+10+10")
        self.resizable(True, True)
        self.attributes('-topmost', True)
        self.attributes('-alpha', 0.92)
        self.session = None
        self.script = None
        self._connecting = False
        self._ready = False
        self._lock = threading.Lock()
        self._stop = False
        self._collapsed = False
        self._saved_geometry = "700x750+10+10"
        self._pid = None
        self._features = {
            'knife': False,
            'time': False,
            'recoil': False,
            'ammo': False,
            'movespeed': False,
            'ammoplus': False,
            'range': False,
            'gather': False,
            'gravity': False,
            'aim': False,
            'godmode': False,
            'speedgun': False,
            'isbot': False,
            'skillcd': False
        }
        self._knife_speed = 5.0
        self._movespeed = 3.0
        self._range_mult = 50.0
        self._gravity = 1.0
        self._jump = 1.0
        self._gravity_mode = 'player_only'
        self._skip_count = 0
        self._gravity_debounce_timer = None
        self._monitoring = True
        
        # 快捷键设置初始化
        self._hotkeys = self._load_hotkeys()
        self._hotkey_handles = []
        # 音效设置初始化
        self._sound_enabled = self._load_sound_enabled()
        self._sound_volume = self._load_sound_volume()
        
        # 设置窗口
        self.settings_window = None
        
        # 初始化 pygame.mixer
        self._init_pygame_mixer()
        
        # nano4t 多人生化特性选择器状态
        self._nano4t_ready = False
        _nano4t_cfg = self._load_nano4t_selector()
        self._nano4t_wanted_ghost = _nano4t_cfg.get('ghost', 9)
        self._nano4t_wanted_human = _nano4t_cfg.get('human', 19)
        self._nano4t_current_ghost = -1
        self._nano4t_current_human = -1
        self._nano4t_log_errors = False  # 仅手动点击按钮时输出错误日志
        
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()
        self._setup_hotkeys(silent=True)
        self._log("游戏修改器控制台 v1.5 — 全功能整合包")
        self._log("正在检测游戏进程...")

        threading.Thread(target=self._auto_connect_bg, daemon=True).start()
        threading.Thread(target=self._monitor_connection, daemon=True).start()
        threading.Thread(target=self._nano4t_auto_health_bg, daemon=True).start()

    def _build_ui(self):
        # 说明文字自动匹配高度：15号字体、两列卡片宽约290px，每行约18个中文字
        def _dh(s): return 28 if len(s) <= 18 else (38 if len(s) <= 30 else 48)

        # ── 顶部：状态栏 + 折叠按钮 + 设置按钮 ──
        self.status_frame = ctk.CTkFrame(self, corner_radius=8, fg_color="#2b2b2b")
        self.status_frame.pack(fill="x", padx=12, pady=(12, 6))
        self.status_dot = ctk.CTkLabel(self.status_frame, text="⚫", font=("Arial", 18))
        self.status_dot.pack(side="left", padx=(12, 4))
        self.status_label = ctk.CTkLabel(self.status_frame, text="等待游戏启动...", font=("Microsoft YaHei", 14))
        self.status_label.pack(side="left", padx=4)
        
        # 设置按钮
        self.settings_btn = ctk.CTkButton(self.status_frame, text="⚙ 设置", width=70, height=28,
                                           font=("Microsoft YaHei", 11), command=self._show_settings,
                                           fg_color="#3a3a3a", hover_color="#555555")
        self.settings_btn.pack(side="right", padx=(4, 8))
        
        self.collapse_btn = ctk.CTkButton(self.status_frame, text="▼ 折叠界面", width=100, height=28,
                                            font=("Microsoft YaHei", 12), command=self._toggle_collapse,
                                            fg_color="#3a3a3a", hover_color="#555555")
        self.collapse_btn.pack(side="right", padx=(4, 8))
        self.pid_label = ctk.CTkLabel(self.status_frame, text="", font=("Microsoft YaHei", 11), text_color="#888")
        self.pid_label.pack(side="right", padx=12)

        # ── 提示条 ──
        self.hint_frame = ctk.CTkFrame(self, corner_radius=6, fg_color="#2a2a00")
        self.hint_frame.pack(fill="x", padx=12, pady=(2, 8))
        self.hint_label = ctk.CTkLabel(self.hint_frame,
                                       text="① 启动游戏 → ② 进入任意模式 → ③ 打开本工具 → ④ 开启功能开关",
                                       font=("Microsoft YaHei", 11), text_color="#ffcc00", wraplength=760)
        self.hint_label.pack(padx=8, pady=4)

        # ── 功能选择区｜分类选项卡 ──
        self.tab_view = ctk.CTkTabview(self, corner_radius=8)
        self.tab_view.pack(fill="both", padx=12, pady=4, expand=True)
        tab_weapon = self.tab_view.add("武器")
        tab_player = self.tab_view.add("人物属性")
        tab_other = self.tab_view.add("其他")
        tab_nano4t = self.tab_view.add("多人生化Buff选择")

        # 每个选项卡内嵌可滚动容器
        tab_weapon_scroll = ctk.CTkScrollableFrame(tab_weapon, corner_radius=0, fg_color="transparent")
        tab_weapon_scroll.pack(fill="both", expand=True, padx=2, pady=2)
        tab_player_scroll = ctk.CTkScrollableFrame(tab_player, corner_radius=0, fg_color="transparent")
        tab_player_scroll.pack(fill="both", expand=True, padx=2, pady=2)
        tab_other_scroll = ctk.CTkScrollableFrame(tab_other, corner_radius=0, fg_color="transparent")
        tab_other_scroll.pack(fill="both", expand=True, padx=2, pady=2)
        
        # ===================== 多人生化 Tab =====================
        tab_nano4t_scroll = ctk.CTkScrollableFrame(tab_nano4t, corner_radius=0, fg_color="transparent")
        tab_nano4t_scroll.pack(fill="both", expand=True, padx=2, pady=2)
        
        # 状态栏 + 当前回合合并为一行
        self.nano4t_top_frame = ctk.CTkFrame(tab_nano4t_scroll, corner_radius=8, fg_color="#2b2b2b")
        self.nano4t_top_frame.pack(fill="x", padx=8, pady=(8,4))
        self.nano4t_top_frame.grid_columnconfigure(0, weight=0)
        self.nano4t_top_frame.grid_columnconfigure(1, weight=1)
        self.nano4t_top_frame.grid_columnconfigure(2, weight=0)
        self.nano4t_status_dot = ctk.CTkLabel(self.nano4t_top_frame, text="⚫", font=("Arial", 18))
        self.nano4t_status_dot.grid(row=0, column=0, padx=(12,4), pady=6)
        self.nano4t_status_label = ctk.CTkLabel(self.nano4t_top_frame, text="等待游戏启动...", font=("Microsoft YaHei", 14))
        self.nano4t_status_label.grid(row=0, column=1, padx=4, pady=6, sticky="w")
        self.nano4t_round_frame = ctk.CTkFrame(self.nano4t_top_frame, corner_radius=6, fg_color="#1a2a1a")
        self.nano4t_round_frame.grid(row=0, column=2, padx=(4,8), pady=6)
        self.nano4t_round_label = ctk.CTkLabel(self.nano4t_round_frame, text="当前回合: 等待进入多人生化模式...",
                                         font=("Microsoft YaHei", 11), text_color="#88aa88")
        self.nano4t_round_label.pack(padx=8, pady=4)
        
        # 下回合预测（单独一行）
        self.nano4t_next_label = ctk.CTkLabel(tab_nano4t_scroll, text="",
                                        font=("Microsoft YaHei", 11), text_color="#aaccaa")
        self.nano4t_next_label.pack(anchor="w", padx=16, pady=(0,0))
        
        # 特性定义
        self.NANO4T_ATTRS = {
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
        
        # 选择区 - 两列网格布局
        nano4t_sel_frame = ctk.CTkFrame(tab_nano4t_scroll, corner_radius=8)
        nano4t_sel_frame.pack(fill="x", padx=8, pady=2)
        nano4t_sel_frame.grid_columnconfigure(0, weight=1, uniform="n4col")
        nano4t_sel_frame.grid_columnconfigure(1, weight=1, uniform="n4col")
        
        # 幽灵方特性 (左列)
        nano4t_ghost_frame = ctk.CTkFrame(nano4t_sel_frame, corner_radius=6, fg_color="#3a1a1a", height=170)
        nano4t_ghost_frame.grid(row=0, column=0, sticky="nsew", padx=(8,4), pady=(6,4))
        nano4t_ghost_frame.grid_propagate(False)
        ctk.CTkLabel(nano4t_ghost_frame, text="👻 幽灵方特性", font=("Microsoft YaHei", 14, "bold"),
                     text_color="#ff6666").pack(anchor="w", padx=12, pady=(6,2))
        self.nano4t_ghost_var = ctk.StringVar(value=f"{self._nano4t_wanted_ghost}: {self.NANO4T_ATTRS[self._nano4t_wanted_ghost][0]}")
        self.nano4t_ghost_combo = ctk.CTkComboBox(nano4t_ghost_frame, values=[f"{i}: {self.NANO4T_ATTRS[i][0]}" for i in range(10)],
                                           variable=self.nano4t_ghost_var, font=("Microsoft YaHei", 13),
                                           dropdown_font=("Microsoft YaHei", 12), height=34, state="readonly",
                                           command=self._nano4t_on_ghost_select)
        self.nano4t_ghost_combo.pack(fill="x", padx=12, pady=(4,2))
        self.nano4t_ghost_desc = ctk.CTkLabel(nano4t_ghost_frame, text="效果: " + self.NANO4T_ATTRS[self._nano4t_wanted_ghost][1],
                                       font=("Microsoft YaHei", 11), text_color="#cc8888")
        self.nano4t_ghost_desc.pack(anchor="w", padx=12, pady=(2,6))
        
        # 人类方特性 (右列)
        nano4t_human_frame = ctk.CTkFrame(nano4t_sel_frame, corner_radius=6, fg_color="#1a1a3a", height=170)
        nano4t_human_frame.grid(row=0, column=1, sticky="nsew", padx=(4,8), pady=(6,4))
        nano4t_human_frame.grid_propagate(False)
        ctk.CTkLabel(nano4t_human_frame, text="🛡️ 人类方特性", font=("Microsoft YaHei", 14, "bold"),
                     text_color="#6688ff").pack(anchor="w", padx=12, pady=(6,2))
        self.nano4t_human_var = ctk.StringVar(value=f"{self._nano4t_wanted_human}: {self.NANO4T_ATTRS[self._nano4t_wanted_human][0]}")
        self.nano4t_human_combo = ctk.CTkComboBox(nano4t_human_frame, values=[f"{i}: {self.NANO4T_ATTRS[i][0]}" for i in range(10,20)],
                                           variable=self.nano4t_human_var, font=("Microsoft YaHei", 13),
                                           dropdown_font=("Microsoft YaHei", 12), height=34, state="readonly",
                                           command=self._nano4t_on_human_select)
        self.nano4t_human_combo.pack(fill="x", padx=12, pady=(4,2))
        self.nano4t_human_desc = ctk.CTkLabel(nano4t_human_frame, text="效果: " + self.NANO4T_ATTRS[self._nano4t_wanted_human][1],
                                       font=("Microsoft YaHei", 11), text_color="#8888cc")
        self.nano4t_human_desc.pack(anchor="w", padx=12, pady=(2,6))
        
        # 应用按钮
        nano4t_btn_frame = ctk.CTkFrame(tab_nano4t_scroll, corner_radius=8)
        nano4t_btn_frame.pack(fill="x", padx=8, pady=(2,4))
        self.nano4t_apply_btn = ctk.CTkButton(nano4t_btn_frame, text="✅ 应用", font=("Microsoft YaHei", 14, "bold"),
                                        height=38, command=self._nano4t_apply, fg_color="#333333", state="disabled")
        self.nano4t_apply_btn.pack(side="left", padx=(12,6), pady=8, expand=True)
        self.nano4t_connect_btn = ctk.CTkButton(nano4t_btn_frame, text="🔗 连接多人生化", font=("Microsoft YaHei", 13),
                                          height=38, command=self._nano4t_connect, fg_color="#2a6e2a")
        self.nano4t_connect_btn.pack(side="left", padx=(6,12), pady=8, expand=True)
        
        # ===================== 武器 Tab =====================
        # 两列网格布局
        for i in range(2):
            tab_weapon_scroll.grid_columnconfigure(i, weight=1, uniform="wcol")

        def make_feature_card(parent, row, col, colspan, color, feature_id, icon, name, desc, has_slider=False, slider_callback=None, slider_var=None, slider_range=None, title_color=None):
            # 统一背景色，增强区分度
            bg_color = "#3a3a3a"
            text_color = "#e0e0e0"
            hover_color = "#4a4a4a"
            # 使用指定的标题颜色，默认使用主题色
            title_text_color = title_color if title_color else text_color
            f = ctk.CTkFrame(parent, corner_radius=6, fg_color=bg_color, border_width=1, border_color="#555555", cursor="hand2")
            f.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)
            
            top_frame = ctk.CTkFrame(f, fg_color="transparent")
            top_frame.pack(fill="x", padx=8, pady=(6, 0))
            
            ctk.CTkLabel(top_frame, text=f"{icon} {name}", font=("Microsoft YaHei", 15, "bold"),
                         text_color=title_text_color).pack(side="left", padx=4)
            
            # 点击卡片切换功能
            f.bind("<Button-1>", lambda e: self._toggle_feature(feature_id))
            
            slider_label_ref = None
            if has_slider and slider_var and slider_range:
                slider = ctk.CTkSlider(top_frame, from_=slider_range[0], to=slider_range[1],
                                        variable=slider_var, number_of_steps=int((slider_range[1]-slider_range[0])*10),
                                        command=slider_callback, width=90)
                slider.pack(side="left", padx=4)
                slider_label_ref = ctk.CTkLabel(top_frame, text=f"{slider_var.get()}x", font=("Microsoft YaHei", 11),
                                             text_color=text_color, width=35)
                slider_label_ref.pack(side="left")
                slider_var.trace_add("write", lambda *args: slider_label_ref.configure(text=f"{slider_var.get():.1f}x"))
            
            switch = ctk.CTkSwitch(top_frame, text="", font=("Microsoft YaHei", 12),
                                    width=50, command=lambda: self._toggle_feature(feature_id))
            switch.pack(side="right", padx=6)
            
            # 根据列跨度动态调整换行宽度
            wrap_width = 280 * colspan
            desc_frame = ctk.CTkLabel(f, font=("Microsoft YaHei", 15),
                                       text=desc, text_color="#a0a0a0",
                                       wraplength=wrap_width, justify="left", anchor="w")
            desc_frame.pack(fill="x", padx=8, pady=(2, 6), expand=False)
            
            return f, switch, slider_label_ref
            
        def _adjust_color(hex_color, factor):
            r = int(min(255, max(0, int(hex_color[1:3], 16) * factor)))
            g = int(min(255, max(0, int(hex_color[3:5], 16) * factor)))
            b = int(min(255, max(0, int(hex_color[5:7], 16) * factor)))
            return f"#{r:02x}{g:02x}{b:02x}"
            
        def _get_text_color(hex_color):
            r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
            brightness = (r * 299 + g * 587 + b * 114) / 1000
            return "#ffffff" if brightness < 128 else "#000000"
        
        self._adjust_color = _adjust_color
        self._get_text_color = _get_text_color
        
        # 快刀卡片
        self.knife_speed_var = ctk.DoubleVar(value=5.0)
        knife_frame, self.knife_switch, self.knife_speed_label = make_feature_card(
            tab_weapon_scroll, 0, 0, 1, "#3a1a1a", 'knife', '🔪', '快刀',
            '提升挥刀速度（人类+生化幽灵通用）', has_slider=True, slider_callback=self._on_knife_speed_change,
            slider_var=self.knife_speed_var, slider_range=(1.0, 10.0),
            title_color="#FFB347"
        )

        # 无后座力卡片
        recoil_frame, self.recoil_switch, _ = make_feature_card(
            tab_weapon_scroll, 0, 1, 1, "#1a1a3a", 'recoil', '🎯', '无后座力',
            '消除所有枪械后座力', title_color="#6A9FB5"
        )

        # 无限子弹卡片
        ammo_frame, self.ammo_switch, _ = make_feature_card(
            tab_weapon_scroll, 1, 0, 1, "#3a2a1a", 'ammo', '🔫', '无限子弹',
            '子弹永不消耗', title_color="#E5B73B"
        )

        # 快速换弹卡片
        ammoplus_frame, self.ammoplus_switch, _ = make_feature_card(
            tab_weapon_scroll, 1, 1, 1, "#3a1a2a", 'ammoplus', '⚡', '快速换弹',
            '换弹速度加快', title_color="#D4AF37"
        )

        # 剑气化丝卡片
        self.range_var = ctk.DoubleVar(value=50.0)
        range_frame, self.range_switch, self.range_label = make_feature_card(
            tab_weapon_scroll, 2, 0, 2, "#1a2a1a", 'range', '⚔️', '剑气化丝',
            '扩大近战攻击距离（人类+生化幽灵通用）', has_slider=True, slider_callback=self._on_range_change,
            slider_var=self.range_var, slider_range=(1.0, 50.0),
            title_color="#AF69EF"
        )

        # 自瞄卡片
        aim_frame, self.aim_switch, _ = make_feature_card(
            tab_weapon_scroll, 3, 0, 1, "#2a1a3a", 'aim', '🎯', '自瞄',
            '自动瞄准敌方玩家', title_color="#FF6B6B"
        )

        # 射速变快卡片
        speedgun_frame, self.speedgun_switch, _ = make_feature_card(
            tab_weapon_scroll, 3, 1, 1, "#3a3a1a", 'speedgun', '⚡', '射速变快',
            '大幅提升枪械射速', title_color="#FFD93D"
        )

        # ===================== 人物属性 Tab =====================
        for i in range(2):
            tab_player_scroll.grid_columnconfigure(i, weight=1, uniform="pcol")

        # 滑板鞋卡片
        self.move_speed_var = ctk.DoubleVar(value=3.0)
        move_frame, self.move_switch, self.move_speed_label = make_feature_card(
            tab_player_scroll, 0, 0, 1, "#1a2a3a", 'movespeed', '👟', '滑板鞋',
            '提升移动速度', has_slider=True, slider_callback=self._on_move_speed_change,
            slider_var=self.move_speed_var, slider_range=(1.0, 6.0),
            title_color="#5FAD56"
        )

        # 无限时间卡片
        time_frame, self.time_switch, _ = make_feature_card(
            tab_player_scroll, 0, 1, 1, "#1a2a1a", 'time', '⏰', '无限时间',
            '设定时间为99:59', title_color="#4C9F9F"
        )

        # 轻重力/高跳卡片（特殊处理，包含额外控件）
        gravity_frame = ctk.CTkFrame(tab_player_scroll, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555", cursor="hand2")
        gravity_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=3, pady=3)
        
        gravity_frame.bind("<Button-1>", lambda e: self._toggle_feature('gravity'))
        
        top9 = ctk.CTkFrame(gravity_frame, fg_color="transparent")
        top9.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top9, text="🌌 轻重力/高跳", font=("Microsoft YaHei", 15, "bold"),
                     text_color="#F4A261").pack(side="left", padx=4)
        
        self.gravity_switch = ctk.CTkSwitch(top9, text="", font=("Microsoft YaHei", 12),
                                             width=50, command=lambda: self._toggle_feature('gravity'))
        self.gravity_switch.pack(side="right", padx=12)
        gravity_slider_frame = ctk.CTkFrame(gravity_frame, fg_color="transparent")
        gravity_slider_frame.pack(fill="x", padx=8, pady=(4, 0))
        ctk.CTkLabel(gravity_slider_frame, text="重力:", font=("Microsoft YaHei", 11),
                     text_color="#e0e0e0").pack(side="left", padx=(4, 2))
        self.gravity_var = ctk.DoubleVar(value=1.0)
        self.gravity_slider = ctk.CTkSlider(gravity_slider_frame, from_=0.0, to=1.0,
                                              variable=self.gravity_var, number_of_steps=10,
                                              command=self._on_gravity_change, width=100)
        self.gravity_slider.pack(side="left", padx=2)
        self.gravity_label = ctk.CTkLabel(gravity_slider_frame, text="1.0",
                                           font=("Microsoft YaHei", 11), text_color="#e0e0e0", width=28)
        self.gravity_label.pack(side="left", padx=(2, 6))
        ctk.CTkLabel(gravity_slider_frame, text="跳跃:", font=("Microsoft YaHei", 11),
                     text_color="#e0e0e0").pack(side="left", padx=(4, 2))
        self.jump_var = ctk.DoubleVar(value=1.0)
        self.jump_slider = ctk.CTkSlider(gravity_slider_frame, from_=1.0, to=5.0,
                                           variable=self.jump_var, number_of_steps=8,
                                           command=self._on_jump_change, width=100)
        self.jump_slider.pack(side="left", padx=2)
        self.jump_label = ctk.CTkLabel(gravity_slider_frame, text="1.0",
                                        font=("Microsoft YaHei", 11), text_color="#e0e0e0", width=28)
        self.jump_label.pack(side="left", padx=2)
        gravity_mode_frame = ctk.CTkFrame(gravity_frame, fg_color="transparent")
        gravity_mode_frame.pack(fill="x", padx=8, pady=(2, 2))
        ctk.CTkLabel(gravity_mode_frame, text="生效范围:", font=("Microsoft YaHei", 11),
                     text_color="#e0e0e0").pack(side="left", padx=(4, 4))
        self.gravity_mode_var = ctk.StringVar(value="仅自己")
        self.gravity_mode_combo = ctk.CTkComboBox(gravity_mode_frame, values=["仅自己", "全部玩家"],
                                                    variable=self.gravity_mode_var,
                                                    font=("Microsoft YaHei", 12),
                                                    height=30, width=120, state="readonly",
                                                    command=self._on_gravity_mode_change)
        self.gravity_mode_combo.pack(side="left", padx=4)
        desc9 = ctk.CTkLabel(gravity_frame, font=("Microsoft YaHei", 15),
                              text="调整重力与跳跃倍率",
                              text_color="#a0a0a0", wraplength=280, justify="left", anchor="w")
        desc9.pack(fill="x", expand=False, padx=5, pady=5)

        # 金刚不坏卡片
        godmode_frame, self.godmode_switch, _ = make_feature_card(
            tab_player_scroll, 2, 0, 2, "#3a1a1a", 'godmode', '🛡️', '金刚不坏',
            '角色受到攻击时不会受伤', title_color="#E74C3C"
        )

        # 技能无冷却卡片
        skillcd_frame, self.skillcd_switch, _ = make_feature_card(
            tab_player_scroll, 3, 0, 1, "#3a2a3a", 'skillcd', '✨', '技能无冷却',
            '生化模式，所有技能无冷却', title_color="#A855F7"
        )

        # ===================== 其他 Tab =====================
        for i in range(2):
            tab_other_scroll.grid_columnconfigure(i, weight=1, uniform="ocol")

        gather_frame = ctk.CTkFrame(tab_other_scroll, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555", cursor="hand2")
        gather_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=3, pady=3)
        
        gather_frame.bind("<Button-1>", lambda e: self._toggle_feature('gather'))
        
        top8 = ctk.CTkFrame(gather_frame, fg_color="transparent")
        top8.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top8, text="👾 聚怪", font=("Microsoft YaHei", 15, "bold"),
                     text_color="#E76F51").pack(side="left", padx=4)
        self.gather_switch = ctk.CTkSwitch(top8, text="启用追踪", font=("Microsoft YaHei", 12),
                                            width=50, command=lambda: self._toggle_feature('gather'))
        self.gather_switch.pack(side="right", padx=12)
        gather_btn_frame = ctk.CTkFrame(gather_frame, fg_color="transparent")
        gather_btn_frame.pack(fill="x", padx=8, pady=(2, 2))
        self.gather_btn = ctk.CTkButton(gather_btn_frame, text="📍 一键聚怪",
                                          font=("Microsoft YaHei", 14, "bold"),
                                          height=45, command=self._gather,
                                          fg_color="#b45309", hover_color="#92400e")
        self.gather_btn.pack(fill="x", padx=4, pady=4)
        desc8 = ctk.CTkLabel(gather_frame, font=("Microsoft YaHei", 15),
                              text="将所有人机聚集。一般用于多人生化模式",
                              text_color="#a0a0a0", wraplength=560, justify="left", anchor="w")
        desc8.pack(fill="x", expand=False, padx=5, pady=5)

        skip_frame = ctk.CTkFrame(tab_other_scroll, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555")
        skip_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=3, pady=3)
        top10 = ctk.CTkFrame(skip_frame, fg_color="transparent")
        top10.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top10, text="⏭️ 回合跳过", font=("Microsoft YaHei", 15, "bold"),
                     text_color="#e0e0e0").pack(side="left", padx=4)
        self.skip_count_label = ctk.CTkLabel(top10, text="已跳过: 0 回合",
                                              font=("Microsoft YaHei", 11), text_color="#a0a0a0")
        self.skip_count_label.pack(side="right", padx=12)
        skip_btn_frame = ctk.CTkFrame(skip_frame, fg_color="transparent")
        skip_btn_frame.pack(fill="x", padx=8, pady=(2, 2))
        self.skip_round_btn = ctk.CTkButton(skip_btn_frame, text="▶ 第一次跳过需要点击两次",
                                              font=("Microsoft YaHei", 14, "bold"),
                                              height=45, command=self._skip_round,
                                              fg_color="#b45309", hover_color="#92400e")
        self.skip_round_btn.pack(fill="x", padx=4, pady=4)
        desc10 = ctk.CTkLabel(skip_frame, font=("Microsoft YaHei", 15),
                               text="结束当前回合（需要等待几秒）",
                               text_color="#a0a0a0", wraplength=280, justify="left", anchor="w")
        desc10.pack(fill="x", expand=False, padx=5, pady=5)

        # 天机傀儡卡片
        isbot_frame, self.isbot_switch, _ = make_feature_card(
            tab_other_scroll, 1, 0, 2, "#1a3a3a", 'isbot', '🧠', '天机傀儡',
            '玩家由人机控制，化身机器傀儡（开启后，重新进入房间才能生效）', title_color="#00D4FF"
        )

        # ── 连接按钮 ──
        self.btn_frame = ctk.CTkFrame(self, corner_radius=8)
        self.btn_frame.pack(fill="x", padx=12, pady=(2, 6))
        self.connect_btn = ctk.CTkButton(self.btn_frame, text="🔗 连接游戏", font=("Microsoft YaHei", 13),
                                          height=40, command=self._connect, fg_color="#2a6e2a")
        self.connect_btn.pack(fill="x", padx=12, pady=10)

        # ── 底部提示 ──
        self.resize_hint = ctk.CTkLabel(self, text="↔️ 拖动边框调整大小", font=("Microsoft YaHei", 12),
                                         text_color="#bbbbbb")
        self.resize_hint.pack(fill="x", padx=12, pady=(2, 0))
        self.patriot_label = ctk.CTkLabel(self, text="科技强军，请党放心，强国有我！",
                                           font=("Microsoft YaHei", 15, "bold"),
                                           text_color="#de2910")
        self.patriot_label.pack(fill="x", padx=12, pady=(0, 4))

        # ── 日志 ──
        self.log_lbl = ctk.CTkLabel(self, text="── 日志 ──", font=("Microsoft YaHei", 11), text_color="#666")
        self.log_lbl.pack(anchor="w", padx=16, pady=(2, 2))
        self.log_box = ctk.CTkTextbox(self, font=("Consolas", 11), wrap="word", height=110)
        self.log_box.pack(fill="both", padx=12, pady=(2, 12), expand=True)
        self.log_box.configure(state="disabled")

    def _on_knife_speed_change(self, value):
        try:
            speed = round(float(value), 1)
            self._knife_speed = speed
            self.knife_speed_label.configure(text=f"{speed}x")
            if self.script:
                self._send_toggle('knife_speed', speed)
        except:
            pass

    def _on_move_speed_change(self, value):
        try:
            speed = round(float(value), 1)
            self._movespeed = speed
            self.move_speed_label.configure(text=f"{speed}x")
            if self.script:
                self._send_toggle('movespeed_speed', speed)
        except:
            pass

    def _on_range_change(self, value):
        try:
            mult = round(float(value), 0)
            self._range_mult = mult
            self.range_label.configure(text=f"{int(mult)}x")
            if self.script:
                self.script.post({'type': 'toggle', 'feature': 'range_config', 'enable': mult})
        except:
            pass

    def _toggle_collapse(self):
        self._collapsed = not self._collapsed
        if self._collapsed:
            self._saved_geometry = self.geometry()
            self.hint_frame.pack_forget()
            self.tab_view.pack_forget()
            self.btn_frame.pack_forget()
            self.resize_hint.pack_forget()
            self.patriot_label.pack_forget()
            if hasattr(self, 'log_lbl'):
                self.log_lbl.pack_forget()
            self.log_box.pack_forget()
            self.collapse_btn.configure(text="▲ 展开界面")
            self.geometry("400x62+10+10")
        else:
            self.hint_frame.pack(fill="x", padx=12, pady=(2, 8))
            self.tab_view.pack(fill="both", padx=12, pady=4, expand=True)
            self.btn_frame.pack(fill="x", padx=12, pady=(2, 6))
            self.resize_hint.pack(fill="x", padx=12, pady=(0, 2))
            self.patriot_label.pack(fill="x", padx=12, pady=(0, 4))
            self.log_lbl.pack(anchor="w", padx=16, pady=(2, 2))
            self.log_box.pack(fill="both", padx=12, pady=(2, 12), expand=True)
            self.collapse_btn.configure(text="▼ 折叠界面")
            self.geometry(self._saved_geometry)

    def _on_gravity_change(self, value):
        try:
            g = round(float(value), 1)
            self._gravity = g
            self.gravity_label.configure(text=str(g))
            if self.script:
                self._send_gravity_config()
            self._log(f"🌌 重力已调整: {g}")
        except:
            pass

    def _on_jump_change(self, value):
        try:
            j = round(float(value), 1)
            self._jump = j
            self.jump_label.configure(text=str(j))
            if self.script:
                self._send_gravity_config()
            self._log(f"🌌 跳跃已调整: {j}x")
        except:
            pass

    def _on_gravity_mode_change(self, value):
        try:
            mode_map = {"仅自己": "player_only", "全部玩家": "all"}
            self._gravity_mode = mode_map.get(value, "player_only")
            if self.script:
                self._send_gravity_config()
            self._log(f"🌌 生效范围已切换: {value}")
        except:
            pass

    def _send_gravity_config(self):
        # 防抖：取消上次未执行的发送，延迟 200ms 后只发送最终值
        if self._gravity_debounce_timer is not None:
            self.after_cancel(self._gravity_debounce_timer)
            self._gravity_debounce_timer = None
        self._gravity_debounce_timer = self.after(200, self._do_send_gravity_config)

    def _do_send_gravity_config(self):
        self._gravity_debounce_timer = None
        try:
            g = self._gravity
            j = self._jump
            m = self._gravity_mode
            self.script.post({'type': 'toggle', 'feature': 'gravity_config', 'enable': {'g': g, 'j': j, 'm': m}})
        except Exception as e:
            self._log(f"❌ 发送重力配置失败: {e}")

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
        elif feature == 'movespeed' and enabled:
            self._send_toggle('movespeed', True)
            self._send_toggle('movespeed_speed', self._movespeed)
        elif feature == 'gravity' and enabled:
            self._send_toggle('gravity', True)
            self._send_gravity_config()
        else:
            self._send_toggle(feature, enabled)

        self._update_switch(feature)

    def _reset_switch(self, feature):
        switch_map = {
            'knife': self.knife_switch,
            'time': self.time_switch,
            'recoil': self.recoil_switch,
            'ammo': self.ammo_switch,
            'movespeed': self.move_switch,
            'ammoplus': self.ammoplus_switch,
            'range': self.range_switch,
            'gather': self.gather_switch,
            'gravity': self.gravity_switch,
            'aim': self.aim_switch,
            'godmode': self.godmode_switch,
            'speedgun': self.speedgun_switch,
            'isbot': self.isbot_switch,
            'skillcd': self.skillcd_switch
        }
        switch_map[feature].configure(variable=ctk.BooleanVar(value=False))

    def _update_switch(self, feature):
        enabled = self._features[feature]
        switch_map = {
            'knife': self.knife_switch,
            'time': self.time_switch,
            'recoil': self.recoil_switch,
            'ammo': self.ammo_switch,
            'movespeed': self.move_switch,
            'ammoplus': self.ammoplus_switch,
            'range': self.range_switch,
            'gather': self.gather_switch,
            'gravity': self.gravity_switch,
            'aim': self.aim_switch,
            'godmode': self.godmode_switch,
            'speedgun': self.speedgun_switch,
            'isbot': self.isbot_switch,
            'skillcd': self.skillcd_switch
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

    def _gather(self):
        if not self._ready or not self.script:
            self._log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return
        if not self._features.get('gather'):
            self._log("⚠ 聚怪功能未启用，请先打开「启用追踪」开关")
            return

        self._log("📍 正在聚怪（传送所有 Bot 到佣兵出生点）...")
        self.gather_btn.configure(state="disabled", text="⏳ 聚怪中...")

        def do_gather():
            try:
                result = self.script.exports_sync.gather()
                try:
                    data = json.loads(result)
                except:
                    data = json.loads(result.replace("'", '"'))

                ok = data.get('ok', False)
                if not ok:
                    self._log(f"❌ 聚怪失败: {data.get('msg', '未知错误')}")
                    return

                total = data.get('total', 0)
                bots = data.get('bots', 0)
                fail = data.get('fail', 0)
                self_count = data.get('self', 0)
                real = data.get('real', 0)
                dead = data.get('dead', 0)

                self._log(f"✅ 聚怪完成!")
                self._log(f"   追踪总数: {total}  自己: {self_count}  真人: {real}  已死: {dead}")
                self._log(f"   成功传送: {bots}  失败: {fail}")

            except Exception as e:
                self._log(f"❌ 聚怪异常: {e}")
            finally:
                self.after(0, lambda: self.gather_btn.configure(state="normal",
                          text="📍 一键聚怪"))

        threading.Thread(target=do_gather, daemon=True).start()

    def _skip_round(self):
        if not self._ready or not self.script:
            self._log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return

        self._log("⏭️ 正在跳过当前回合...")
        self.skip_round_btn.configure(state="disabled", text="⏳ 跳转中...")

        def do_skip():
            try:
                result = self.script.exports_sync.roundskip()
                try:
                    data = json.loads(result)
                except:
                    data = json.loads(result.replace("'", '"'))

                ok = data.get('ok', False)
                if not ok:
                    reason = data.get('reason', '未知错误')
                    if reason == 'no_instance':
                        self._log("⚠ 未能获取到游戏回合实例，请确保已进入游戏模式")
                    elif reason == 'already_zero':
                        self._log("⚠ 回合时间已为 0:00，无需跳过")
                    elif reason == 'guard_active':
                        self._log("⚠ 跳过操作进行中，请稍候再试")
                    else:
                        self._log(f"❌ 跳过失败: {reason}")
                    return

                self._log("✅ 回合跳过成功！")
            except Exception as e:
                self._log(f"❌ 跳过异常: {e}")
            finally:
                self.after(0, lambda: self.skip_round_btn.configure(state="normal",
                          text="▶ 跳过当前回合"))

        threading.Thread(target=do_skip, daemon=True).start()

    def _log(self, msg):
        ts = time.strftime("%H:%M:%S")
        self.after(0, lambda: self._log_ui(ts, msg))

    def _log_ui(self, ts, msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{ts}] {msg}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _set_status(self, color, text):
        dot_map = {"green": "🟢", "yellow": "🟡", "red": "🔴", "gray": "⚫"}
        self.status_dot.configure(text=dot_map.get(color, "⚫"))
        self.status_label.configure(text=text)
        if color == "green":
            self.hint_frame.configure(fg_color="#1a3a1a")
            self.hint_label.configure(text_color="#88ff88")
            self.hint_label.configure(text="✅ 已连接！点击功能按钮开启修改")
        elif color == "red":
            self.hint_frame.configure(fg_color="#3a1a1a")
            self.hint_label.configure(text_color="#ff8888")
            self.hint_label.configure(text="连接断开，正在重连...")
        else:
            self.hint_frame.configure(fg_color="#2a2a00")
            self.hint_label.configure(text_color="#ffcc00")
            self.hint_label.configure(text="① 启动游戏 → ② 进入任意模式 → ③ 打开本工具 → ④ 开启功能开关")

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

                elif t == 'gather_result':
                    data = payload.get('data', {})
                    ok = data.get('ok', False)
                    if ok:
                        total = data.get('total', 0)
                        bots = data.get('bots', 0)
                        fail = data.get('fail', 0)
                        self._log(f"✅ 聚怪结果: 总追踪{total} | 传送成功{bots} 失败{fail}")
                    else:
                        self._log(f"❌ 聚怪失败: {data.get('msg', '未知')}")

                elif t == 'round_skipped':
                    count = payload.get('count', 0)
                    self._skip_count = count
                    self.after(0, lambda c=count: self.skip_count_label.configure(text=f"已跳过: {c} 回合"))
                    self._log(f"⏭️ 回合已跳过! (累计: {count})")

                elif t == 'round_end':
                    self._log(f"⏭️ 回合结束通知")
                
                # nano4t 多人生化特性选择器消息处理
                elif t == 'nano4t_ready':
                    ids = payload.get('ids', [])
                    self._nano4t_ready = True
                    self.after(0, lambda: self._nano4t_on_ready(len(ids)))
                
                elif t == 'nano4t_destroyed':
                    if self._nano4t_ready:
                        self._log("⚠ 检测到退出多人生化房间，特性系统已销毁")
                        self._log("  重新进入房间后将自动初始化")
                    self._nano4t_ready = False
                    self.after(0, lambda: (
                        self.nano4t_apply_btn.configure(state="disabled", fg_color="#333333"),
                        self._nano4t_set_status("yellow", "已退出房间"),
                        self.nano4t_next_label.configure(text=""),
                        self.nano4t_round_label.configure(text="当前回合: 等待进入多人生化模式...")
                    ))
                
                elif t == 'nano4t_error':
                    m = payload.get('msg', '')
                    self._nano4t_ready = False
                    if self._nano4t_log_errors:
                        self._nano4t_log_errors = False
                        if '未检测到游戏' in m:
                            self._log("⚠ [多人生化] 未检测到游戏进程")
                        elif '未进入多人生化模式' in m:
                            self._log("⚠ [多人生化] 检测到游戏，但尚未进入「多人生化模式」")
                            self._log("  请选择多人生化模式并进入房间")
                        elif '房间' in m:
                            self._log("⚠ [多人生化] 已在多人生化模式菜单，但尚未进入房间")
                        else:
                            self._log(f"❌ [多人生化] {m}")
                    self.after(0, lambda: self._nano4t_set_status("yellow", "未就绪"))
                
                elif t == 'nano4t_set':
                    g = int(payload.get('g', 0))
                    h = int(payload.get('h', 0))
                    self._nano4t_wanted_ghost = g
                    self._nano4t_wanted_human = h
                    self._log(f"✅ [多人生化] 已锁定: {self.NANO4T_ATTRS[g][0]} + {self.NANO4T_ATTRS[h][0]}，下一回合生效")
                    self.after(0, self._nano4t_refresh_next_label)
                
                elif t == 'nano4t_current':
                    g = int(payload.get('g', -1))
                    h = int(payload.get('h', -1))
                    self.after(0, lambda gg=g, hh=h: self._nano4t_update_round_label(gg, hh))
                
                elif t == 'nano4t_dead':
                    if self._nano4t_ready:
                        self._log("⚠ [多人生化] 模式实例已失效（退出房间或切换模式）")
                        self._nano4t_ready = False
                        self.after(0, lambda: (
                            self.nano4t_apply_btn.configure(state="disabled", fg_color="#333333"),
                            self._nano4t_set_status("yellow", "已退出房间"),
                            self.nano4t_next_label.configure(text=""),
                            self.nano4t_round_label.configure(text="当前回合: 等待进入多人生化模式...")
                        ))
                
                elif t == 'nano4t_alive':
                    if not self._nano4t_ready and self._ready:
                        self._log("ℹ️ [多人生化] 检测到已进入多人生化模式，正在初始化...")
                        threading.Thread(target=self._nano4t_auto_init_if_needed, daemon=True).start()

            script.on('message', on_msg)
            script.load()
            self.session = session
            self.script = script
            self._pid = pid
            self._ready = True

            self._log("✅ 已连接到游戏进程！")
            self._log("点击功能按钮开启修改")
            self._restore_features()
            self.after(0, lambda p=pid: self._on_connected(p))
            threading.Thread(target=self._nano4t_auto_init_bg, daemon=True).start()

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

    def _cleanup(self, keep_features=False):
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
        self._nano4t_ready = False
        self.after(0, lambda: self.nano4t_round_label.configure(text="当前回合: 等待进入多人生化模式..."))
        if not keep_features:
            self._features = {k: False for k in self._features}
            self._skip_count = 0
            self.after(0, lambda: self.skip_count_label.configure(text="已跳过: 0 回合"))

    def _update_feature_button(self, feature):
        pass

    def _on_disconnected(self):
        if not self._ready:
            return
        self._log("🔴 连接已断开，正在重连...")
        self._ready = False
        self._connecting = False
        self._cleanup(keep_features=True)
        pid_text = f"PID: {self._pid}" if self._pid else ""
        self.after(0, lambda: self.pid_label.configure(text=pid_text))
        self.after(0, lambda: self._set_status("red", "连接断开，正在重连..."))

    def _monitor_connection(self):
        while not self._stop:
            time.sleep(2)
            if not self._ready or not self.script:
                continue
            try:
                self.script.exports_sync.getGravityStatus()
            except frida.InvalidOperationError:
                self._on_disconnected()
            except frida.TransportError:
                self._on_disconnected()
            except Exception:
                pass

    def _restore_features(self):
        for feature in list(self._features.keys()):
            if self._features[feature]:
                self._restore_single_feature(feature)
        self._refresh_all_switches()

    def _restore_single_feature(self, feature):
        if feature == 'knife':
            self._send_toggle('knife', True)
            self._send_toggle('knife_speed', self._knife_speed)
        elif feature == 'movespeed':
            self._send_toggle('movespeed', True)
            self._send_toggle('movespeed_speed', self._movespeed)
        elif feature == 'range':
            self._send_toggle('range', True)
            self.script.post({'type': 'toggle', 'feature': 'range_config', 'enable': self._range_mult})
        elif feature == 'gravity':
            self._send_toggle('gravity', True)
            self._do_send_gravity_config()
        else:
            self._send_toggle(feature, True)

    def _refresh_all_switches(self):
        for feature in self._features:
            self._update_switch(feature)

    # ==================== 快捷键功能 ====================
    def _load_hotkeys(self):
        path = os.path.join(DATA_DIR, "hotkeys.json")
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        # 默认快捷键配置
        return {
            '1': None, '2': None, '3': None, '4': None, '5': None,
            '6': None, '7': None, '8': None, '9': None, '0': None
        }
    
    def _save_hotkeys(self):
        path = os.path.join(DATA_DIR, "hotkeys.json")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self._hotkeys, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self._log(f"❌ 保存快捷键失败: {e}")
    
    # ==================== Nano-4T 多人生化BUFF选择保存 ====================
    def _load_nano4t_selector(self):
        path = os.path.join(DATA_DIR, "Nano-4T-selector.json")
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {'ghost': 9, 'human': 19}
    
    def _save_nano4t_selector(self):
        path = os.path.join(DATA_DIR, "Nano-4T-selector.json")
        try:
            data = {
                'ghost': self._nano4t_wanted_ghost,
                'human': self._nano4t_wanted_human
            }
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self._log(f"❌ 保存多人生化BUFF选择失败: {e}")
    
    def _set_hotkey(self, position, feature_id):
        # 先移除该位置的旧绑定
        old_feature = self._hotkeys.get(position)
        if old_feature == feature_id:
            return True
        
        # 检查该功能是否已绑定到其他位置
        for pos, feat in self._hotkeys.items():
            if feat == feature_id:
                self._hotkeys[pos] = None
        
        self._hotkeys[position] = feature_id
        return True
    
    def _remove_hotkey(self, position):
        self._hotkeys[position] = None
    
    def _save_and_apply_hotkeys(self):
        # 保存并应用热键配置（延迟保存机制）
        self._save_hotkeys()
        self._setup_hotkeys()
    
    def _setup_hotkeys(self, silent=False):
        # 先逐个移除已绑定的热键句柄
        for handle in self._hotkey_handles:
            try:
                handle.unhook()
            except Exception as e:
                pass
        self._hotkey_handles = []
        
        # 按固定顺序重新绑定并保存句柄（确保位置和功能正确对应）
        positions = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        for pos in positions:
            feature = self._hotkeys.get(pos)
            if feature:
                try:
                    callback = functools.partial(self._toggle_feature_by_hotkey, feature)
                    handle = keyboard.add_hotkey(f'ctrl+{pos}', callback)
                    self._hotkey_handles.append(handle)
                    if not silent:
                        self._log(f"✅ 绑定快捷键 Ctrl+{pos} -> {feature}")
                except Exception as e:
                    if not silent:
                        self._log(f"❌ 绑定快捷键 Ctrl+{pos} 失败: {e}")
    
    def _toggle_feature_by_hotkey(self, feature):
        # 热键回调运行在非主线程，必须切换到主线程执行GUI操作
        callback = functools.partial(self._real_toggle_feature_by_hotkey, feature)
        self.after(0, callback)
    
    def _real_toggle_feature_by_hotkey(self, feature):
        if feature == 'gather':
            # 聚怪快捷键触发一键聚怪操作
            self._gather()
        elif feature in self._features:
            self._toggle_feature(feature)
            self._play_sound()
    
    def _validate_hotkey(self, position):
        if position not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            return False, "位置必须是 0-9 的数字"
        return True, ""
    
    # ==================== 音效功能 ====================
    def _load_sound_enabled(self):
        path = os.path.join(DATA_DIR, "settings.json")
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('sound_enabled', True)
            except:
                pass
        return True
    
    def _load_sound_volume(self):
        path = os.path.join(DATA_DIR, "settings.json")
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('sound_volume', 50)
            except:
                pass
        return 50
    
    def _save_sound_settings(self):
        path = os.path.join(DATA_DIR, "settings.json")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({
                    'sound_enabled': self._sound_enabled,
                    'sound_volume': self._sound_volume
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self._log(f"❌ 保存音效设置失败: {e}")
    
    def _init_pygame_mixer(self):
        self._audio_initialized = False
        self._sound_channel = None
        try:
            pygame.mixer.init()
            self._audio_initialized = True
            self._sound_channel = pygame.mixer.Channel(0)
        except Exception as e:
            self._log(f"⚠️ pygame.mixer 初始化失败，将使用系统蜂鸣音: {e}")

    def _play_sound(self):
        if not self._sound_enabled:
            return
        try:
            sound_path = os.path.join(RESOURCE_DIR, "音效1.MP3")
            if os.path.exists(sound_path) and self._audio_initialized:
                sound = pygame.mixer.Sound(sound_path)
                if self._sound_channel:
                    self._sound_channel.play(sound)
                else:
                    pygame.mixer.Sound.play(sound)
            else:
                winsound.Beep(800, 100)
        except Exception as e:
            try:
                winsound.Beep(800, 100)
            except:
                pass
    
    def _set_sound_enabled(self, enabled):
        self._sound_enabled = enabled
        self._save_sound_settings()
    
    def _set_sound_volume(self, volume):
        self._sound_volume = volume
        self._save_sound_settings()
    
    # ==================== 设置界面 ====================
    def _show_settings(self):
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.focus()
            return
        
        self.settings_window = ctk.CTkToplevel(self)
        self.settings_window.title("设置")
        self.settings_window.geometry("500x650")
        self.settings_window.resizable(False, False)
        self.settings_window.attributes('-topmost', True)
        self.settings_window.grab_set()
        
        tab_view = ctk.CTkTabview(self.settings_window, corner_radius=8)
        tab_view.pack(fill="both", expand=True, padx=12, pady=12)
        
        hotkey_tab = tab_view.add("快捷键")
        hotkey_frame = ctk.CTkScrollableFrame(hotkey_tab, corner_radius=0)
        hotkey_frame.pack(fill="both", expand=True, padx=4, pady=4)
        
        ctk.CTkLabel(hotkey_frame, text="快捷键绑定 (Ctrl+数字) - 功能互斥绑定", font=("Microsoft YaHei", 14, "bold")).pack(pady=(12, 6))
        
        feature_display_names = {v['icon'] + ' ' + v['name']: k for k, v in FEATURES_INFO.items()}
        
        combo_widgets = {}
        
        def get_available_features(exclude_pos=None):
            available = ["未绑定"]
            for display_name, feature_id in feature_display_names.items():
                is_bound = False
                for pos, feat in self._hotkeys.items():
                    if pos != exclude_pos and feat == feature_id:
                        is_bound = True
                        break
                if not is_bound:
                    available.append(display_name)
            return available
        
        def update_combo_options():
            for pos, combo in combo_widgets.items():
                current_value = combo.get()
                available = get_available_features(exclude_pos=pos)
                combo.configure(values=available)
                if current_value not in available:
                    combo.set("未绑定")
                    self._remove_hotkey(pos)
        
        for i, pos in enumerate(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']):
            row_frame = ctk.CTkFrame(hotkey_frame, fg_color="#2a2a2a")
            row_frame.pack(fill="x", padx=8, pady=3)
            
            ctk.CTkLabel(row_frame, text=f"Ctrl+{pos}", font=("Microsoft YaHei", 12), 
                         text_color="#aaa", width=60).pack(side="left", padx=8)
            
            feature_id = self._hotkeys.get(pos)
            feature_info = FEATURES_INFO.get(feature_id)
            feature_name = feature_info['icon'] + ' ' + feature_info['name'] if feature_info else "未绑定"
            
            combo_var = ctk.StringVar(value=feature_name)
            available_features = get_available_features(exclude_pos=pos)
            combo = ctk.CTkComboBox(row_frame, values=available_features,
                                    variable=combo_var, state="readonly", width=150)
            combo.pack(side="left", padx=8)
            combo.set(feature_name)
            
            combo_widgets[pos] = combo
            
            def on_combo_change(selected, position=pos):
                if selected and selected != "未绑定":
                    feature_id = feature_display_names[selected]
                    self._set_hotkey(position, feature_id)
                else:
                    self._remove_hotkey(position)
                update_combo_options()
            
            combo.configure(command=on_combo_change)
        
        def on_save():
            self._save_and_apply_hotkeys()
            self.settings_window.destroy()
        
        save_btn = ctk.CTkButton(self.settings_window, text="保存并应用", width=100,
                                 command=on_save, fg_color="#007acc", hover_color="#005a99")
        save_btn.pack(pady=(0, 12))
        
        self.settings_window.protocol("WM_DELETE_WINDOW", on_save)
        
        # 关于
        about_tab = tab_view.add("关于")
        about_frame = ctk.CTkScrollableFrame(about_tab, corner_radius=0)
        about_frame.pack(fill="both", expand=True, padx=4, pady=4)
        
        ctk.CTkLabel(about_frame, text="游戏修改器控制台 - 全功能整合包 v1.5", font=("Microsoft YaHei", 18, "bold")).pack(pady=(12, 4))
        ctk.CTkLabel(about_frame, text="版本: v1.5", font=("Microsoft YaHei", 12)).pack(pady=2)
        ctk.CTkLabel(about_frame, text="作者: 挂呱呱呱", font=("Microsoft YaHei", 12)).pack(pady=2)
        
        ctk.CTkLabel(about_frame, text="\nQQ群: 1095388251", font=("Microsoft YaHei", 12)).pack(pady=4)
        
        # B站链接（占位）
        b站_frame = ctk.CTkFrame(about_frame, fg_color="transparent")
        b站_frame.pack(pady=(12, 4))
        ctk.CTkLabel(b站_frame, text="B站: ", font=("Microsoft YaHei", 12)).pack(side="left")
        b站_btn = ctk.CTkButton(b站_frame, text="🔗 BiliBili", font=("Microsoft YaHei", 11),
                                width=100, command=self._open_bilibili)
        b站_btn.pack(side="left")
        
        # 赞赏码
        ctk.CTkLabel(about_frame, text="\n微信赞赏码:", font=("Microsoft YaHei", 12)).pack(pady=4)
        donate_image_path = os.path.join(RESOURCE_DIR, "微信赞赏码.png")
        if os.path.exists(donate_image_path):
            try:
                donate_image = Image.open(donate_image_path)
                donate_image = donate_image.resize((225, 225), Image.LANCZOS)
                donate_photo = ctk.CTkImage(light_image=donate_image, dark_image=donate_image, size=(225, 225))
                donate_label = ctk.CTkLabel(about_frame, image=donate_photo, text="")
                donate_label.pack(pady=4)
            except Exception as e:
                donate_label = ctk.CTkLabel(about_frame, text=f"加载图片失败: {e}", font=("Microsoft YaHei", 11),
                                             text_color="#888")
                donate_label.pack(pady=4)
        else:
            donate_label = ctk.CTkLabel(about_frame, text="赞赏码图片未找到", font=("Microsoft YaHei", 11),
                                         text_color="#888")
            donate_label.pack(pady=4)
    
    def _open_bilibili(self):
        import webbrowser
        webbrowser.open("https://space.bilibili.com/481324794")
    
    def _on_close(self):
        self._stop = True
        # 清理所有热键句柄
        for handle in self._hotkey_handles:
            try:
                handle.unhook()
            except Exception as e:
                pass
        self._hotkey_handles = []
        self._cleanup()
        self.destroy()

    # ==================== nano4t 多人生化特性选择器方法 ====================
    
    def _nano4t_on_ghost_select(self, value):
        gid = int(value.split(":")[0])
        self.nano4t_ghost_desc.configure(text="效果: " + self.NANO4T_ATTRS[gid][1])
        self._nano4t_wanted_ghost = gid
        self._save_nano4t_selector()
        if self._nano4t_ready:
            self.nano4t_next_label.configure(text="💡 请点击「应用」按钮生效")

    def _nano4t_on_human_select(self, value):
        hid = int(value.split(":")[0])
        self.nano4t_human_desc.configure(text="效果: " + self.NANO4T_ATTRS[hid][1])
        self._nano4t_wanted_human = hid
        self._save_nano4t_selector()
        if self._nano4t_ready:
            self.nano4t_next_label.configure(text="💡 请点击「应用」按钮生效")

    def _nano4t_refresh_next_label(self):
        if self._nano4t_ready:
            g = self._nano4t_wanted_ghost
            h = self._nano4t_wanted_human
            self.nano4t_next_label.configure(
                text=f"下一回合已锁定: 👻 {self.NANO4T_ATTRS[g][0]}  |  🛡️ {self.NANO4T_ATTRS[h][0]}")
        else:
            self.nano4t_next_label.configure(text="")

    def _nano4t_set_status(self, color, text):
        dot_map = {"green": "🟢", "yellow": "🟡", "red": "🔴", "gray": "⚫"}
        self.nano4t_status_dot.configure(text=dot_map.get(color, "⚫"))
        self.nano4t_status_label.configure(text=text)

    def _nano4t_on_ready(self, count):
        self._nano4t_set_status("green", "已就绪")
        self.nano4t_apply_btn.configure(state="normal", fg_color="#2563eb")
        self._log(f"✅ [多人生化] 已就绪！共 {count} 种特性")
        self._log("[多人生化] 用法: 下拉选择 → 点击应用 → 下一回合自动生效")
        self.nano4t_next_label.configure(text="💡 请选择特性后点击「应用」按钮")
        threading.Thread(target=self._nano4t_get_current_bg, daemon=True).start()
        threading.Thread(target=self._nano4t_auto_getcurrent_bg, daemon=True).start()

    def _nano4t_update_round_label(self, g, h):
        self._nano4t_current_ghost = g
        self._nano4t_current_human = h
        if g >= 0 and h >= 0:
            txt = f"当前回合: 👻 {self.NANO4T_ATTRS[g][0]}  |  🛡️ {self.NANO4T_ATTRS[h][0]}"
        elif self._nano4t_ready:
            txt = "当前回合: 等待回合开始..."
        else:
            txt = "当前回合: 等待进入游戏..."
        self.nano4t_round_label.configure(text=txt)

    def _nano4t_connect(self):
        if not self._ready:
            self._log("⚠ [多人生化] 请先连接游戏")
            return
        self._nano4t_log_errors = True
        self._log("[多人生化] 正在初始化多人生化特性系统...")
        threading.Thread(target=self._nano4t_connect_bg, daemon=True).start()

    def _nano4t_connect_bg(self):
        try:
            self.script.exports_sync.nano4tinit()
        except Exception as e:
            self._log(f"❌ [多人生化] 连接失败: {e}")

    def _nano4t_apply(self):
        if not self._nano4t_ready:
            self._log("⚠ [多人生化] 尚未就绪，请先进入「多人生化模式」房间")
            return
        try:
            gid = int(self.nano4t_ghost_var.get().split(":")[0])
            hid = int(self.nano4t_human_var.get().split(":")[0])
            threading.Thread(target=lambda: self._nano4t_apply_bg(gid, hid), daemon=True).start()
        except Exception as e:
            self._log(f"❌ [多人生化] 参数错误: {e}")

    def _nano4t_apply_bg(self, gid, hid):
        try:
            self.script.exports_sync.nano4tset(gid, hid)
        except frida.InvalidOperationError:
            self._log("⚠ [多人生化] 连接已断开，请重新进入房间后点击「连接多人生化」")
            self._nano4t_ready = False
            self.nano4t_apply_btn.configure(state="disabled", fg_color="#333333")
            self.after(0, lambda: self._nano4t_set_status("yellow", "已断开"))
        except Exception as e:
            self._log(f"❌ [多人生化] 应用失败: {e}")

    def _nano4t_auto_init_bg(self):
        time.sleep(2)
        if self.script and self._ready and not self._nano4t_ready:
            try:
                self.script.exports_sync.nano4tinit()
            except Exception:
                pass

    def _nano4t_get_current_bg(self):
        if not self.script or not self._nano4t_ready:
            return
        try:
            self.script.exports.nano4tgetcurrent()
        except Exception as e:
            pass

    def _nano4t_auto_health_bg(self):
        time.sleep(2)
        while not self._stop:
            time.sleep(2)
            if not self.script:
                continue
            if self._nano4t_ready:
                try:
                    self.script.exports.nano4thealthcheck()
                except Exception:
                    pass
            else:
                try:
                    self.script.exports_sync.nano4tinit()
                except Exception:
                    pass

    def _nano4t_auto_getcurrent_bg(self):
        time.sleep(3)
        while not self._stop:
            time.sleep(5)
            if self._nano4t_ready and self.script:
                try:
                    self.script.exports.nano4tgetcurrent()
                except Exception as e:
                    pass

    def _nano4t_auto_init_if_needed(self):
        if self.script and self._ready and not self._nano4t_ready:
            try:
                self.script.exports_sync.nano4tinit()
            except Exception:
                pass


if __name__ == "__main__":
    app = GameModifierApp()
    app.mainloop()
