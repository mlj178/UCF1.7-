# 游戏修改器控制台 - 全功能整合包 v1.2
# 在 v1.1 基础上新增：聚怪功能（一键将所有Bot传送至佣兵出生点）
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
  // 模块 6: 无限弹匣 + 快速换弹
  // 原理: 1) 替换 get_isInfinityAmmo 始终返回 true
  //       2) 替换 get_ReloadSpeed 为本地玩家返回2倍加速值
  // ====================================================================
  var ammoPlusModule = (function() {
    var enabled = false;
    var getIsInfinityAmmoAddr = null;
    var getReloadSpeedAddr = null;
    var isMyPlayer = null;
    var reloadLogCount = 0;
    var ammoLogCount = 0;

    return {
      enable: function() {
        if (enabled) return;
        var mod = getGameAssembly();
        if (!mod) { sendLog('error', '无限弹匣', '无 GameAssembly.dll'); return; }

        var base = mod.base;
        getIsInfinityAmmoAddr = base.add(0xB17120);
        getReloadSpeedAddr = base.add(0xB170E0);
        isMyPlayer = new NativeFunction(base.add(0xB55FD0), 'bool', ['pointer']);

        reloadLogCount = 0;
        ammoLogCount = 0;

        sendLog('info', '无限弹匣', 'get_isInfinityAmmo @ ' + getIsInfinityAmmoAddr);
        sendLog('info', '无限弹匣', 'get_ReloadSpeed @ ' + getReloadSpeedAddr);

        Interceptor.replace(getIsInfinityAmmoAddr, new NativeCallback(function(self) {
          ammoLogCount++;
          if (ammoLogCount <= 5) {
            sendLog('info', '无限弹匣', '返回 true (调用#' + ammoLogCount + ')');
          }
          return 1;
        }, 'int', ['pointer']));

        Interceptor.replace(getReloadSpeedAddr, new NativeCallback(function(self) {
          try {
            var owner = self.add(0x8).readPointer();
            if (!owner || owner.isNull()) return 2.0;
            if (isMyPlayer(owner)) {
              reloadLogCount++;
              if (reloadLogCount <= 5) {
                sendLog('info', '无限弹匣', '本地玩家换弹加速 2.0x (#' + reloadLogCount + ')');
              }
              return 2.0;
            }
            return 1.0;
          } catch(e) {
            return 2.0;
          }
        }, 'float', ['pointer']));

        enabled = true;
        sendLog('success', '无限弹匣', '已启用 — 无限子弹 + 2x快速换弹');
        sendStatus('ammoplus', true);
      },
      disable: function() {
        if (!enabled) return;
        if (getIsInfinityAmmoAddr) { try { Interceptor.revert(getIsInfinityAmmoAddr); } catch(e) {} }
        if (getReloadSpeedAddr) { try { Interceptor.revert(getReloadSpeedAddr); } catch(e) {} }
        getIsInfinityAmmoAddr = null;
        getReloadSpeedAddr = null;
        isMyPlayer = null;
        enabled = false;
        sendLog('info', '无限弹匣', '已禁用');
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
    var trackedPlayers = {};
    var trackedBots = {};
    var botUpdateSeen = {};

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

    function trackFromBot(botPtr) {
      var key = botPtr.toString();
      if (botUpdateSeen[key]) return;
      botUpdateSeen[key] = true;
      var player = rp(botPtr, O.Bot_thisPlayer);
      var pValid = player && !player.isNull() && isValid(player);
      trackedBots[key] = { bot: botPtr, player: pValid ? player : null, hasPlayer: pValid };
      if (pValid) {
        var pk = player.toString();
        if (!trackedPlayers[pk]) trackedPlayers[pk] = player;
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

      try {
        var ap = gm.add(O.GM_allPlayers).readPointer();
        if (ap && !ap.isNull()) {
          var t = ap.add(0xC).readU32();
          for (var i = 0; i < t; i++) {
            try {
              var pp = ap.add(0x10 + i * 8).readPointer();
              if (isValid(pp)) {
                var pk = pp.toString();
                if (!trackedPlayers[pk]) trackedPlayers[pk] = pp;
              }
            } catch(e) {}
          }
        }
      } catch(e) {}

      var bKeys = Object.keys(trackedBots);
      for (var bi = 0; bi < bKeys.length; bi++) {
        var e = trackedBots[bKeys[bi]];
        if (e.hasPlayer && e.player) {
          var pk = e.player.toString();
          if (!trackedPlayers[pk]) trackedPlayers[pk] = e.player;
        }
      }

      sendLog('info', '聚怪', '追踪: ' + Object.keys(trackedPlayers).length + ' Player | ' + bKeys.length + ' Bot组件');

      var self = 0, real = 0, dead = 0, botOk = 0, botFail = 0;
      var pKeys = Object.keys(trackedPlayers);
      var log = [];

      for (var pi = 0; pi < pKeys.length; pi++) {
        var pp = trackedPlayers[pKeys[pi]];
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
        sendLog('success', '聚怪', '已启用 — 双路径扫描 + v14传送模式');
        sendStatus('gather', true);
      },
      disable: function() {
        if (!enabled) return;
        for (var i = 0; i < hooks.length; i++) { try { hooks[i].detach(); } catch(e) {} }
        hooks = [];
        gm = null; mm = null;
        trackedPlayers = {};
        trackedBots = {};
        botUpdateSeen = {};
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
  // 模块管理
  // ====================================================================
  var modules = {
    knife: knifeModule,
    time: timeModule,
    recoil: recoilModule,
    ammo: ammoModule,
    movespeed: moveSpeedModule,
    ammoplus: ammoPlusModule,
    range: rangeModule,
    gather: gatherModule
  };

  function onToggle(data) {
    var featureName = data.feature;
    var enable = data.enable;

    if (featureName === 'knife_speed') {
      knifeModule.setSpeed(enable);
    } else if (featureName === 'movespeed_speed') {
      moveSpeedModule.setSpeed(enable);
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

  rpc.exports = {
    gather: function() {
      var result = gatherModule.gather();
      send(JSON.stringify({ type: 'gather_result', data: result }));
      return JSON.stringify(result);
    }
  };

  sendLog('info', '系统', '游戏修改器 Agent v1.2 已加载');
  sendLog('info', '系统', '原有功能: 快刀v16 | 无限时间 | 无后座力v14 | 无限子弹plan4');
  sendLog('info', '系统', 'v1.1新增: 滑板鞋3x/6x | 无限弹匣+快速换弹 | 剑气化丝50x');
  sendLog('info', '系统', 'v1.2新增: 聚怪功能');
  sendLog('info', '系统', '快刀支持速度切换: 3x / 5x / 10x');
  sendLog('info', '系统', '请先附加到游戏进程，然后开启对应功能');
  sendLog('info', '系统', '架构: ' + Process.arch + ', 平台: ' + Process.platform);

  setTimeout(function() { getGameAssembly(); }, 100);
})();
"""


class GameModifierApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("游戏修改器控制台 - 全功能整合包 v1.2")
        self.geometry("800x920+10+10")
        self.resizable(False, False)
        self.minsize(800, 920)
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
            'ammo': False,
            'movespeed': False,
            'ammoplus': False,
            'range': False,
            'gather': False
        }
        self._knife_speed = 5.0
        self._movespeed = 3.0
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()
        self._log("游戏修改器控制台 v1.2 — 全功能整合包（v1.1功能 + 新增聚怪）")
        self._log("正在检测游戏进程...")

        threading.Thread(target=self._auto_connect_bg, daemon=True).start()

    def _build_ui(self):
        # ── 顶部：状态栏 ──
        self.status_frame = ctk.CTkFrame(self, corner_radius=8, fg_color="#2b2b2b")
        self.status_frame.pack(fill="x", padx=12, pady=(12, 6))
        self.status_dot = ctk.CTkLabel(self.status_frame, text="⚫", font=("Arial", 18))
        self.status_dot.pack(side="left", padx=(12, 4))
        self.status_label = ctk.CTkLabel(self.status_frame, text="等待游戏启动...", font=("Microsoft YaHei", 14))
        self.status_label.pack(side="left", padx=4)
        self.pid_label = ctk.CTkLabel(self.status_frame, text="", font=("Microsoft YaHei", 11), text_color="#888")
        self.pid_label.pack(side="right", padx=12)

        # ── 提示条 ──
        self.hint_frame = ctk.CTkFrame(self, corner_radius=6, fg_color="#2a2a00")
        self.hint_frame.pack(fill="x", padx=12, pady=(2, 8))
        self.hint_label = ctk.CTkLabel(self.hint_frame,
                                       text="① 启动游戏 → ② 进入任意模式 → ③ 打开本工具 → ④ 开启功能开关",
                                       font=("Microsoft YaHei", 11), text_color="#ffcc00", wraplength=760)
        self.hint_label.pack(padx=8, pady=4)

        # ── 功能选择区（使用 Scrollable 框架以容纳所有功能）─
        self.sel_scroll = ctk.CTkScrollableFrame(self, corner_radius=8, height=700)
        self.sel_scroll.pack(fill="x", padx=12, pady=4)

        # ========== 原有功能 1: 快刀 ==========
        knife_frame = ctk.CTkFrame(self.sel_scroll, corner_radius=6, fg_color="#3a1a1a")
        knife_frame.pack(fill="x", padx=4, pady=(4, 4))
        top1 = ctk.CTkFrame(knife_frame, fg_color="transparent")
        top1.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top1, text="🔪 快刀", font=("Microsoft YaHei", 15, "bold"),
                     text_color="#ff6666").pack(side="left", padx=4)
        self.knife_speed_var = ctk.StringVar(value="5")
        self.knife_speed_combo = ctk.CTkComboBox(top1, values=["3", "5", "10"],
                                                  variable=self.knife_speed_var,
                                                  font=("Microsoft YaHei", 12),
                                                  height=30, width=100, state="readonly",
                                                  command=self._on_knife_speed_change)
        self.knife_speed_combo.pack(side="left", padx=8)
        ctk.CTkLabel(top1, text="x 速度", font=("Microsoft YaHei", 11),
                     text_color="#cc8888").pack(side="left")
        self.knife_switch = ctk.CTkSwitch(top1, text="", font=("Microsoft YaHei", 12),
                                           width=50, command=lambda: self._toggle_feature('knife'))
        self.knife_switch.pack(side="right", padx=12)
        desc1 = ctk.CTkTextbox(knife_frame, font=("Microsoft YaHei", 20), height=88,
                                fg_color="#2a1010", text_color="#cc9999", wrap="word")
        desc1.pack(fill="x", padx=8, pady=(2, 6))
        desc1.insert("0.0", "【说明】提升近战武器挥刀速度。3x~10x=刀锋如电，疾速连击。仅对玩家生效。")
        desc1.configure(state="disabled")

        # ========== 原有功能 2: 无限时间 ==========
        time_frame = ctk.CTkFrame(self.sel_scroll, corner_radius=6, fg_color="#1a2a1a")
        time_frame.pack(fill="x", padx=4, pady=4)
        top2 = ctk.CTkFrame(time_frame, fg_color="transparent")
        top2.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top2, text="⏰ 无限时间", font=("Microsoft YaHei", 15, "bold"),
                     text_color="#66ff66").pack(side="left", padx=4)
        self.time_switch = ctk.CTkSwitch(top2, text="", font=("Microsoft YaHei", 12),
                                          width=50, command=lambda: self._toggle_feature('time'))
        self.time_switch.pack(side="right", padx=12)
        desc2 = ctk.CTkTextbox(time_frame, font=("Microsoft YaHei", 20), height=88,
                                fg_color="#0e1a0e", text_color="#99dd99", wrap="word")
        desc2.pack(fill="x", padx=8, pady=(2, 6))
        desc2.insert("0.0", "【说明】锁定游戏时间为 99:59，永不结束。适用于所有限时模式，无需担心时间耗尽。")
        desc2.configure(state="disabled")

        # ========== 原有功能 3: 无后座力 ==========
        recoil_frame = ctk.CTkFrame(self.sel_scroll, corner_radius=6, fg_color="#1a1a3a")
        recoil_frame.pack(fill="x", padx=4, pady=4)
        top3 = ctk.CTkFrame(recoil_frame, fg_color="transparent")
        top3.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top3, text="🎯 无后座力", font=("Microsoft YaHei", 15, "bold"),
                     text_color="#6688ff").pack(side="left", padx=4)
        self.recoil_switch = ctk.CTkSwitch(top3, text="", font=("Microsoft YaHei", 12),
                                            width=50, command=lambda: self._toggle_feature('recoil'))
        self.recoil_switch.pack(side="right", padx=12)
        desc3 = ctk.CTkTextbox(recoil_frame, font=("Microsoft YaHei", 20), height=88,
                                fg_color="#10102a", text_color="#9999dd", wrap="word")
        desc3.pack(fill="x", padx=8, pady=(2, 6))
        desc3.insert("0.0", "【说明】消除所有枪械后座力。弹道稳如磐石，压枪不再需要，远距离连射精准无误。")
        desc3.configure(state="disabled")

        # ========== 原有功能 4: 无限子弹 ==========
        ammo_frame = ctk.CTkFrame(self.sel_scroll, corner_radius=6, fg_color="#3a2a1a")
        ammo_frame.pack(fill="x", padx=4, pady=4)
        top4 = ctk.CTkFrame(ammo_frame, fg_color="transparent")
        top4.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top4, text="🔫 无限子弹", font=("Microsoft YaHei", 15, "bold"),
                     text_color="#ffaa44").pack(side="left", padx=4)
        self.ammo_switch = ctk.CTkSwitch(top4, text="", font=("Microsoft YaHei", 12),
                                          width=50, command=lambda: self._toggle_feature('ammo'))
        self.ammo_switch.pack(side="right", padx=12)
        desc4 = ctk.CTkTextbox(ammo_frame, font=("Microsoft YaHei", 20), height=88,
                                fg_color="#2a1a0e", text_color="#ddbb99", wrap="word")
        desc4.pack(fill="x", padx=8, pady=(2, 6))
        desc4.insert("0.0", "【说明】子弹永不消耗（替换 ConsumeAmmo）。射击不消耗弹匣子弹，无限火力压制。")
        desc4.configure(state="disabled")

        # ========== 新增功能 5: 滑板鞋 ==========
        move_frame = ctk.CTkFrame(self.sel_scroll, corner_radius=6, fg_color="#1a2a3a")
        move_frame.pack(fill="x", padx=4, pady=4)
        top5 = ctk.CTkFrame(move_frame, fg_color="transparent")
        top5.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top5, text="👟 滑板鞋", font=("Microsoft YaHei", 15, "bold"),
                     text_color="#66aaff").pack(side="left", padx=4)
        self.move_speed_var = ctk.StringVar(value="3")
        self.move_speed_combo = ctk.CTkComboBox(top5, values=["3", "6"],
                                                 variable=self.move_speed_var,
                                                 font=("Microsoft YaHei", 12),
                                                 height=30, width=80, state="readonly",
                                                 command=self._on_move_speed_change)
        self.move_speed_combo.pack(side="left", padx=8)
        ctk.CTkLabel(top5, text="x 速度", font=("Microsoft YaHei", 11),
                     text_color="#88aadd").pack(side="left")
        self.move_switch = ctk.CTkSwitch(top5, text="", font=("Microsoft YaHei", 12),
                                          width=50, command=lambda: self._toggle_feature('movespeed'))
        self.move_switch.pack(side="right", padx=12)
        desc5 = ctk.CTkTextbox(move_frame, font=("Microsoft YaHei", 20), height=88,
                                fg_color="#0e1a28", text_color="#99bbdd", wrap="word")
        desc5.pack(fill="x", padx=8, pady=(2, 6))
        desc5.insert("0.0", "【说明】提升角色移动速度。3x=健步如飞，灵活走位；6x=如履平地，战场穿梭。仅对玩家生效。")
        desc5.configure(state="disabled")

        # ========== 新增功能 6: 无限弹匣+快速换弹 ==========
        ammoplus_frame = ctk.CTkFrame(self.sel_scroll, corner_radius=6, fg_color="#3a1a2a")
        ammoplus_frame.pack(fill="x", padx=4, pady=4)
        top6 = ctk.CTkFrame(ammoplus_frame, fg_color="transparent")
        top6.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top6, text="[弹匣] 无限弹匣 + 快速换弹", font=("Microsoft YaHei", 15, "bold"),
                     text_color="#ff88cc").pack(side="left", padx=4)
        ammoplus_font = ctk.CTkFont(family="Microsoft YaHei", size=12)
        self.ammoplus_switch = ctk.CTkSwitch(top6, text="", font=ammoplus_font,
                                              width=50, command=lambda: self._toggle_feature('ammoplus'))
        self.ammoplus_switch.pack(side="right", padx=12)
        desc6 = ctk.CTkTextbox(ammoplus_frame, font=("Microsoft YaHei", 20), height=88,
                                fg_color="#2a0e1a", text_color="#dd99bb", wrap="word")
        desc6.pack(fill="x", padx=8, pady=(2, 6))
        desc6.insert("0.0", "【说明】无限弹匣=子弹永不耗尽，无需拾取弹药；快速换弹=换弹速度提升2倍，持续火力压制。全模式通用。")
        desc6.configure(state="disabled")

        # ========== 新增功能 7: 剑气化丝 ==========
        range_frame = ctk.CTkFrame(self.sel_scroll, corner_radius=6, fg_color="#1a2a1a")
        range_frame.pack(fill="x", padx=4, pady=4)
        top7 = ctk.CTkFrame(range_frame, fg_color="transparent")
        top7.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top7, text="⚔️ 剑气化丝", font=("Microsoft YaHei", 15, "bold"),
                     text_color="#66ff88").pack(side="left", padx=4)
        range_font = ctk.CTkFont(family="Microsoft YaHei", size=12)
        self.range_switch = ctk.CTkSwitch(top7, text="", font=range_font,
                                           width=50, command=lambda: self._toggle_feature('range'))
        self.range_switch.pack(side="right", padx=12)
        desc7 = ctk.CTkTextbox(range_frame, font=("Microsoft YaHei", 20), height=88,
                                fg_color="#0e1a0e", text_color="#99dd99", wrap="word")
        desc7.pack(fill="x", padx=8, pady=(2, 6))
        desc7.insert("0.0", "【说明】扩大近战武器攻击距离至50倍。刀气化丝，十步杀一人，千里不留行。全模式通用，仅对玩家生效。")
        desc7.configure(state="disabled")

        # ========== v1.2 新增功能 8: 聚怪 ==========
        gather_frame = ctk.CTkFrame(self.sel_scroll, corner_radius=6, fg_color="#1a1a1a")
        gather_frame.pack(fill="x", padx=4, pady=4)
        top8 = ctk.CTkFrame(gather_frame, fg_color="transparent")
        top8.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top8, text="👾 聚怪", font=("Microsoft YaHei", 15, "bold"),
                     text_color="#ffaa00").pack(side="left", padx=4)
        self.gather_switch = ctk.CTkSwitch(top8, text="启用追踪", font=("Microsoft YaHei", 12),
                                            width=50, command=lambda: self._toggle_feature('gather'))
        self.gather_switch.pack(side="right", padx=12)
        # 聚怪操作按钮
        gather_btn_frame = ctk.CTkFrame(gather_frame, fg_color="transparent")
        gather_btn_frame.pack(fill="x", padx=8, pady=(2, 2))
        self.gather_btn = ctk.CTkButton(gather_btn_frame, text="📍 一键聚怪 — 把所有 Bot 传送到佣兵出生点",
                                          font=("Microsoft YaHei", 14, "bold"),
                                          height=45, command=self._gather,
                                          fg_color="#b45309", hover_color="#92400e")
        self.gather_btn.pack(fill="x", padx=4, pady=4)
        desc8 = ctk.CTkTextbox(gather_frame, font=("Microsoft YaHei", 20), height=88,
                                fg_color="#0e0e0e", text_color="#ddbb88", wrap="word")
        desc8.pack(fill="x", padx=8, pady=(2, 6))
        desc8.insert("0.0", "【说明】将所有 Bot（人机）传送到佣兵出生点（硬编码 SP_GR 坐标）。双路径追踪确保不漏 Bot，传送后 Bot 可自由移动。仅对 Bot 生效。")
        desc8.configure(state="disabled")

        # ── 连接按钮 ──
        btn_frame = ctk.CTkFrame(self, corner_radius=8)
        btn_frame.pack(fill="x", padx=12, pady=(2, 6))
        self.connect_btn = ctk.CTkButton(btn_frame, text="🔗 连接游戏", font=("Microsoft YaHei", 13),
                                          height=40, command=self._connect, fg_color="#2a6e2a")
        self.connect_btn.pack(fill="x", padx=12, pady=10)

        # ── 日志 ──
        log_lbl = ctk.CTkLabel(self, text="── 日志 ──", font=("Microsoft YaHei", 11), text_color="#666")
        log_lbl.pack(anchor="w", padx=16, pady=(2, 2))
        self.log_box = ctk.CTkTextbox(self, font=("Consolas", 11), wrap="word", height=200)
        self.log_box.pack(fill="both", padx=12, pady=(2, 12), expand=True)
        self.log_box.configure(state="disabled")

    def _on_knife_speed_change(self, value):
        try:
            speed = float(value)
            self._knife_speed = speed
            if self.script:
                self._send_toggle('knife_speed', speed)
            self._log(f"🔪 快刀速度已切换: {speed}x")
        except:
            pass

    def _on_move_speed_change(self, value):
        try:
            speed = float(value)
            self._movespeed = speed
            if self.script:
                self._send_toggle('movespeed_speed', speed)
            self._log(f"👟 滑板鞋速度已切换: {speed}x")
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
        elif feature == 'movespeed' and enabled:
            self._send_toggle('movespeed', True)
            self._send_toggle('movespeed_speed', self._movespeed)
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
            'gather': self.gather_switch
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
            'gather': self.gather_switch
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
                          text="📍 一键聚怪 — 把所有 Bot 传送到佣兵出生点"))

        threading.Thread(target=do_gather, daemon=True).start()

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

            script.on('message', on_msg)
            script.load()
            self.session = session
            self.script = script
            self._pid = pid
            self._ready = True

            self._log("✅ 已连接到游戏进程！")
            self._log("点击功能按钮开启修改")
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

    def _update_feature_button(self, feature):
        pass

    def _on_close(self):
        self._stop = True
        self._cleanup()
        self.destroy()


if __name__ == "__main__":
    app = GameModifierApp()
    app.mainloop()
