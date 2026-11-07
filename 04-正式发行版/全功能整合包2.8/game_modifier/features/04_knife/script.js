// Local helpers for this feature only.
var modules = {};
var __localMaxLogsPerModule = 10;
var __localModuleLogCounts = {};

function sendRoutedLog(level, module, message, audience, devDetail) {
  try {
    if (!__localModuleLogCounts[module]) __localModuleLogCounts[module] = 0;
    if (__localModuleLogCounts[module] >= __localMaxLogsPerModule) return;
    if (module !== '??' && __localModuleLogCounts[module] === __localMaxLogsPerModule - 1) {
      __localModuleLogCounts[module]++;
      send({ type: 'log', level: 'info', module: module, message: message + ' (???????)', audience: audience || 'dev', dev_detail: devDetail || '' });
      return;
    }
    __localModuleLogCounts[module]++;
    send({ type: 'log', level: level, module: module, message: message, audience: audience || 'dev', dev_detail: devDetail || '' });
  } catch (_) {}
}

function sendUserLog(level, module, message) {
  sendRoutedLog(level, module, message, 'user', '');
}

function sendDevLog(level, module, message, devDetail) {
  sendRoutedLog(level, module, message, 'dev', devDetail || '');
}

function sendBothLog(level, module, message, devDetail) {
  sendRoutedLog(level, module, message, 'both', devDetail || '');
}

function sendLog(level, module, message) {
  sendDevLog(level, module, message);
}

function sendLogFile(level, module, message) {
  try { send({ type: 'log_file', level: level, module: module, message: message, audience: 'dev' }); } catch (_) {}
}

function sendStatus(feature, enabled) {
  try { send({ type: 'status', feature: feature, enabled: enabled }); } catch (_) {}
}

var __localGameAssemblyCache = null;
var __localGameAssemblyLogged = false;

function getGameAssembly() {
  try {
    if (__localGameAssemblyCache) return __localGameAssemblyCache;
    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) {
      sendDevLog('error', '??', '??? GameAssembly.dll', 'GameAssembly.dll not found');
      return null;
    }
    __localGameAssemblyCache = mod;
    if (!__localGameAssemblyLogged) {
      __localGameAssemblyLogged = true;
      sendDevLog('info', '??', 'GameAssembly.dll: base=' + mod.base + ' size=' + mod.size, 'GameAssembly module located');
    }
    return mod;
  } catch (e) {
    sendDevLog('error', '??', '??????: ' + e.message, 'getGameAssembly failed: ' + e.message);
    return null;
  }
}

function readPtr(addr) {
  try { if (!addr || addr.isNull()) return null; var v = addr.readPointer(); return (v && !v.isNull()) ? v : null; } catch (_) { return null; }
}

function readI32(addr) { try { return addr ? addr.readS32() : null; } catch (_) { return null; } }
function readF32(addr) { try { return addr ? addr.readFloat() : null; } catch (_) { return null; } }
function readU8(addr) { try { return addr ? addr.readU8() : null; } catch (_) { return null; } }

var __localCleanupCallbacks = [];
function registerCleanup(callback) {
  if (typeof callback !== 'function') return false;
  __localCleanupCallbacks.push(callback);
  return true;
}

// knife.js - 快刀模块 v16 (NativeCallback Replace)
// 替换 PlayerWeapons.get_KnifeSpeed，为本地玩家返回指定的速度倍数

modules.knife = (function() {
  var enabled = false;
  var currentSpeed = 5.0;
  // 幽灵/终结者的攻击动画同时写在角色 Animator 上，速度过高会连招重播产生残影，单独限速
  var ghostSpeedCap = 2.5;
  var isMyPlayer = null;
  var originalGetKnifeSpeed = null;
  var getNanoRole = null;
  var isHumanRole = null;
  var getKnifeSpeedAddr = null;
  var logCount = 0;

  // ===== 左键状态防卡死（修复"打到人后攻击动画无限重播"）=====
  // 攻击循环的唯一开关是 Weapon._fireBtnPressed(+0x78)：
  //   WPN_Knife.Update             : isUsing && fireBtnPressed && currentAnimTag==Empty -> PlayKnifeAttackAnim(Combo1)
  //   WPN_Knife.OnKnifeAttackAnimEnd: fireBtnPressed -> 继续 Combo1/Combo2
  // 它由 PlayerController.UseWeapon 每帧用 Input.GetKey(Mouse0=323) 刷新（Weapon.OnFireBtnPressed/UnPressed）。
  // 一旦游戏侧左键状态卡在"按下"，攻击就会自己一直转下去（连招自我重播）；这里用 OS 级物理按键状态兜底纠正。
  //
  // ⚠ 必须在 Hook 的 onLeave 里写 0，不能在 onEnter 里写：
  //   Weapon.OnFireBtnPressed(+0xB6CDA0) 的函数体就是 `this->fields._fireBtnPressed = 1;`
  //   （IDA 反编译 0x10B6CDA0，全文一句话）。写在 onEnter 的 0 会被紧跟着的本体覆盖。
  //   ==> 2026-10 排查记录（两道独立的坑，缺一不可）：
  //      坑 1（onEnter 被本体覆盖，已修）;
  //      坑 2（致命）：physicalLeftDown() 里的 new NativeFunction(fn,'short',...) 在 Frida 17
  //         直接抛 "invalid type specified"，被 catch 吞掉后恒返回 null，于是这道兜底
  //         一次都没执行过 —— 详见下面 readOsMouseLeft() 的注释与实测探针。
  var fireBtnHook = null;
  var knifeUpdateHook = null;
  var playKnifeAnimHook = null;
  var asyncKeyStateFn = null;
  var getIsUsing = null;
  var stormClears = 0;

  // 诊断通道：直接 send({type:'log_file'})，不受 sendRoutedLog「每模块 10 条」上限约束。
  // （上一轮排查就是被这个上限挡住的：guard 的告警一条都没写进文件，看着像"没触发"。）
  var diag = { total: 0, lastBeat: 0, beats: 0, animWhileUp: 0, keyed: {} };

  function sendDiag(message) {
    try {
      if (diag.total >= 200) return;
      diag.total++;
      send({ type: 'log_file', level: 'info', module: '快刀诊断', message: message + ' [#d' + diag.total + ']', audience: 'dev' });
    } catch (e) {}
  }

  // 同一个 key 只写前 limit 条，避免刷屏
  function diagByKey(key, message, limit) {
    var n = diag.keyed[key] || 0;
    if (n >= limit) return;
    diag.keyed[key] = n + 1;
    sendDiag(message + ' [' + key + ' x' + (n + 1) + ']');
  }

  // il2cpp 对象 -> 类名（Il2CppClass.name 在 klass+0x8）；用来确认打的是不是 WPN_Knife 族
  function classNameOf(obj) {
    try {
      if (!obj || obj.isNull()) return 'null';
      var klass = obj.readPointer();
      if (!klass || klass.isNull()) return '?';
      var namePtr = klass.add(0x8).readPointer();
      if (!namePtr || namePtr.isNull()) return '?';
      return namePtr.readCString(48) || '?';
    } catch (e) { return '?'; }
  }

  // 把返回地址翻译成「模块名+偏移」，用来指认"谁在调用它"
  function callerOf(addr) {
    try {
      if (!addr || addr.isNull()) return '?';
      var m = Process.findModuleByAddress(addr);
      if (m) return m.name + '+0x' + addr.sub(m.base).toString(16);
      var r = Process.findRangeByAddress(addr);
      return r ? ('anon@' + r.base + '+0x' + addr.sub(r.base).toString(16)) : ('raw:' + addr);
    } catch (e) { return 'err'; }
  }

  // System.String -> JS 字符串（length@+0x8, UTF-16 chars@+0xC）
  function csStringOf(p) {
    try {
      if (!p || p.isNull()) return 'null';
      var len = p.add(0x8).readS32();
      if (len < 0 || len > 48) return 'len' + len;
      var out = '';
      for (var i = 0; i < len; i++) {
        var c = p.add(0xC + i * 2).readU16();
        out += (c >= 32 && c < 127) ? String.fromCharCode(c) : '.';
      }
      return out;
    } catch (e) { return 'err'; }
  }

  // OS 级物理按键：{ok:true,down:bool} / {ok:false,reason}
  //
  // ⚠⚠ 类型名必须是 'uint16'。Frida 17 里 'short' 不是合法类型名，
  //    new NativeFunction(fn, 'short', ['int']) 会抛 "invalid type specified"，
  //    异常被下面的 catch 吞掉 -> physicalLeftDown() 恒返回 null ->
  //    clearStuckFireBtn 第一道门 `if (physicalLeftDown() !== false) return false;` 永远成立，
  //    **这道兜底从写出来那天起一次都没执行过**（两轮修复都白做，就卡在这里）。
  //    实测：06-测试/frida-revert-probe/probe_async_keystate.py
  //      short=THROW(invalid type specified) | int16=OK | uint16=OK
  function readOsKeyState(vk) {
    try {
      if (!asyncKeyStateFn) {
        var fn = null;
        try { if (typeof Module.getGlobalExportByName === 'function') fn = Module.getGlobalExportByName('GetAsyncKeyState'); } catch (e) {}
        if (!fn) {
          var u = Process.findModuleByName('user32.dll') || Process.findModuleByName('USER32.dll');
          if (u) { try { fn = u.findExportByName('GetAsyncKeyState'); } catch (e) {} }
        }
        if (!fn) return { ok: false, reason: 'no_export' };
        asyncKeyStateFn = new NativeFunction(fn, 'uint16', ['int']);
      }
      // 最高位（0x8000）为 1 表示当前按下
      return { ok: true, down: ((asyncKeyStateFn(vk) & 0x8000) !== 0) };
    } catch (e) {
      return { ok: false, reason: 'throw:' + e.message };
    }
  }

  // VK_LBUTTON = 0x01
  function readOsMouseLeft() { return readOsKeyState(0x01); }
  // VK_RBUTTON = 0x02 —— 重击（combo3）走的是右键/特殊键
  function readOsMouseRight() { return readOsKeyState(0x02); }

  // 备选链路：原实现想用 UnityEngine.Input.GetKey(KeyCode.Mouse0) 兜底，**实测不可用，已移除**。
  // 2026-10 实测日志（13:12:02 自检）：
  //   Input.GetKey(Mouse0)=FAIL(throw:access violation accessing 0x4)
  // 原因：`UnityEngine.Input.GetKey` 是 icall 包装壳（0xACFA60 -> il2cpp_resolve_icall），
  // 从 Hook 里调用它会走进 il2cpp 的 icall 解析路径并抛访问违例。
  // 在游戏进程里制造一次访问违例（哪怕被 Frida 捕获）是不可接受的：解析路径上的锁可能就此不被释放，
  // 后续任何一次 il2cpp_resolve_icall 都会永久阻塞 —— 表现就是"游戏停止响应"。
  // 结论：OS 链路读不到时**什么都不做**（宁可不纠正），也不去碰游戏自己的输入状态。
  //
  // true=物理左键按下 / false=已松开 / null=读不到（此时绝不动游戏状态）
  function physicalLeftDown() {
    var os = readOsMouseLeft();
    if (os.ok) return os.down;
    diagByKey('os_fail', '物理按键读取失败(' + os.reason + ')，本次放弃纠正（不使用 Input.GetKey 兜底）', 3);
    return null;
  }

  // true=物理右键按下 / false=已松开 / null=读不到
  function physicalRightDown() {
    var os = readOsMouseRight();
    if (os.ok) return os.down;
    diagByKey('os_fail_r', '物理右键读取失败(' + os.reason + ')', 3);
    return null;
  }

  // 诊断输出用：把三种状态分开打印，避免"按下/读不到"合并后无法判断真相
  function keyStateText(state) {
    if (state === false) return '松开';
    if (state === true) return '按下';
    return '读不到(null)';
  }

  // 物理左键已松开、但游戏侧 +0x78 仍是 1 时撤销它，打断"连招自我重播"
  // 顺序刻意从便宜到贵：先读字段，再判身份，避免对每个 WPN_Knife 实例都调游戏函数
  function clearStuckFireBtn(w, tag) {
    try {
      if (!w || w.isNull()) return false;
      if (w.add(0x78).readU8() !== 1) return false;        // 没卡就不用管
      var down = physicalLeftDown();
      if (down !== false) {                                // true=确实按着 / null=读不到，都不动
        diagByKey('key_' + (down === null ? 'unknown' : 'down'),
          'fireBtnPressed=1 但物理左键=' + (down === null ? '读不到' : '按下') + '，按设计不动（' + tag + '）', 2);
        return false;
      }
      var owner = readPtr(w.add(0x30));                    // Weapon._owner（Model_Fields+0x28 -> 对象+0x30）
      if (!owner || !isMyPlayer) {
        diagByKey('no_owner', 'fireBtnPressed=1 但拿不到 Weapon._owner（' + tag + '）', 2);
        return false;
      }
      if (!isMyPlayer(owner, ptr(0))) {                    // 只纠正本地玩家的武器
        diagByKey('not_mine', 'fireBtnPressed=1 但不是本地玩家的武器（' + tag + '）', 2);
        return false;
      }
      w.add(0x78).writeU8(0);
      stormClears++;
      if (stormClears <= 8 || stormClears % 25 === 0) {
        sendDiag('已撤销 fireBtnPressed #' + stormClears + '（' + tag + '，weapon=' + w
          + '，klass=' + classNameOf(w) + '，owner=' + classNameOf(owner) + '）');
      }
      return true;
    } catch (e) { return false; }
  }

  // ===== 重击（右键/特殊键）防卡死：修复"没人按键却在不断放重击动画" =====
  //
  // IDA 实证（0x10B64240，全文 0x70 字节，反汇编如下）：
  //   WPN_Knife.OnSpecialBtnDown(this):
  //       if (Weapon.get_isUsing(this) && this->_currentAnimTag == string.Empty)
  //           this->klass->vtable.PlayKnifeAttackAnim(this, 3);      // 3 = 重击（combo3）
  //   —— **函数体里没有任何状态位、没有冷却**：谁调它、只要武器空闲就立刻起一次重击。
  //
  // 而 PlayerController.UseWeapon(0x10B13450) 的原文是：
  //       if (wpns->inUse) {
  //           if (Input.GetKeyDown(324)) inUse->OnSpecialBtnDown();
  //           if (Input.GetKey(324))     inUse->OnSpecialBtnDown();   // ← 按住时每帧都调
  //           else                       inUse->OnSpecialBtnUp();
  //           ... 左键同理(323) ...
  //       }
  //   一旦游戏侧右键状态卡在"按下"，重击就会一击接一击无限重播（节奏 = clip 时长 ≈1.1s）。
  //
  // 日志实证（本轮 user 测试）：
  //   13:56:38→13:56:54、13:57:42、13:58:08 反复出现
  //     「combo=3 由 GameAssembly.dll+0xb642a1 触发（fireBtn=0，左键=松开）」
  //   0xb642a1 正是 WPN_Knife.OnSpecialBtnDown 里 `call PlayKnifeAttackAnim` 之后的返回地址。
  //
  // 修法与左键同源：**以物理按键为准**。物理右键没按，就把这次"重击起手"拦掉。
  // 为什么必须拦而不是"清状态位"：这个函数根本没有状态位可清（它只读不写）。
  var specialAddr = null;
  var specialOrig = null;
  var specialBlocks = 0;

  return {
    setSpeed: function(speed) {
      currentSpeed = speed;
      if (enabled) {
        sendLog('info', '快刀', '速度已切换: ' + speed + 'x（实时生效）');
      } else {
        sendLog('info', '快刀', '速度已预选: ' + speed + 'x（开启后生效）');
      }
    },
    setGhostCap: function(cap) {
      var v = parseFloat(cap);
      if (isFinite(v) && v > 0) {
        ghostSpeedCap = v;
        sendLog('info', '快刀', '生化幽灵/终结者速度上限: ' + ghostSpeedCap + 'x（防止连招残影）');
      }
    },
    enable: function() {
      if (enabled) return;
      var mod = getGameAssembly();
      if (!mod) { sendBothLog('error', '快刀', '快刀暂未就绪，请重新连接游戏后重试', 'Knife GameAssembly.dll not found'); return; }

      var base = mod.base;
      var isMyPlayerAddr = base.add(0xB55FD0);
      getKnifeSpeedAddr = base.add(0xB170A0);
      var getNanoRoleAddr = base.add(0xB56200);
      var isHumanRoleAddr = base.add(0xB4E960);

      sendLog('info', '快刀', 'isMyPlayer @ ' + isMyPlayerAddr);
      sendLog('info', '快刀', 'get_KnifeSpeed @ ' + getKnifeSpeedAddr);
      sendLog('info', '快刀', 'get_nanoRole @ ' + getNanoRoleAddr + ' / IsHuman @ ' + isHumanRoleAddr);

      isMyPlayer = new NativeFunction(isMyPlayerAddr, 'bool', ['pointer', 'pointer']);
      originalGetKnifeSpeed = new NativeFunction(getKnifeSpeedAddr, 'float', ['pointer']);
      getNanoRole = new NativeFunction(getNanoRoleAddr, 'int', ['pointer', 'pointer']);
      isHumanRole = new NativeFunction(isHumanRoleAddr, 'bool', ['int', 'pointer']);
      // Weapon.get_isUsing @ 0xB6E260：WPN_Knife.Update 起手条件的第一项，心跳里要用
      getIsUsing = new NativeFunction(base.add(0xB6E260), 'bool', ['pointer', 'pointer']);

      logCount = 0;
      stormClears = 0;
      specialBlocks = 0;
      diag.total = 0;
      diag.beats = 0;
      diag.lastBeat = 0;
      diag.animWhileUp = 0;
      diag.keyed = {};

      // 自检：把左键读取链的结果写进日志。
      // 下次排查时只要看到这行是 up/down 就说明链路正常；看到 FAIL(...) 就是又断了。
      var osProbe = readOsMouseLeft();
      sendDiag('左键读取链自检: GetAsyncKeyState=' + (osProbe.ok ? (osProbe.down ? 'down' : 'up') : ('FAIL(' + osProbe.reason + ')'))
        + ' | WPN_Knife.Update@' + base.add(0xB64610) + ' OnFireBtnPressed@' + base.add(0xB6CDA0)
        + ' PlayKnifeAttackAnim@' + base.add(0xB642B0));

      // 兜底 A：游戏置位 fireBtnPressed 时，等本体写完（onLeave）再按 OS 物理按键核对并撤销
      if (!fireBtnHook) {
        try {
          fireBtnHook = Interceptor.attach(base.add(0xB6CDA0), {
            onEnter: function (args) {
              this.w = args[0];              // 参数只能在 onEnter 取；真正的判断/写回放到 onLeave
            },
            onLeave: function () {
              try {
                if (!enabled) return;
                clearStuckFireBtn(this.w, 'OnFireBtnPressed');
              } catch (e) {}
            }
          });
        } catch (e) {
          sendDevLog('warn', '快刀', 'fireBtnPressed 兜底钩子安装失败: ' + e.message, 'OnFireBtnPressed hook failed');
        }
      }

      // 兜底 B：每帧再核对一次装备中的刀/爪（WPN_Knife.Update）。
      // 即使游戏侧不再走 OnFireBtnPressed（卡住的旧武器、切枪后未刷新等），也能在本帧内打断连招循环。
      // onEnter 里撤销最有效：紧接着的函数体会再读一次 +0x78，读到 0 就不会重启连招。
      if (!knifeUpdateHook) {
        try {
          knifeUpdateHook = Interceptor.attach(base.add(0xB64610), {
            onEnter: function (args) {
              try {
                if (!enabled) return;
                clearStuckFireBtn(args[0], 'WPN_Knife.Update');

                // 心跳（只对本地玩家的刀/爪，每 3s 一行，最多 30 行）：
                // 确认 Hook 活着，并把卡住时的字段状态一并留下证据
                var now = Date.now();
                if (now - diag.lastBeat < 3000 || diag.beats >= 30) return;
                var w = args[0];
                if (!w || w.isNull()) return;
                var owner = readPtr(w.add(0x30));
                if (!owner || !isMyPlayer || !isMyPlayer(owner, ptr(0))) return;
                diag.beats++;
                diag.lastBeat = now;
                var role = getNanoRole ? getNanoRole(owner, ptr(0)) : -1;
                var human = isHumanRole ? isHumanRole(role, ptr(0)) : true;
                var key = physicalLeftDown();
                var keyR = physicalRightDown();
                sendDiag('心跳: role=' + role + ' human=' + human
                  + ' fireBtn=' + w.add(0x78).readU8()
                  + ' using=' + (getIsUsing ? (getIsUsing(w, ptr(0)) ? 1 : 0) : '?')
                  + ' tag=' + csStringOf(readPtr(w.add(0x4C)))
                  + ' anim=' + csStringOf(readPtr(w.add(0x48)))
                  + ' combo1AnimSpeed=' + readF32(w.add(0xEC))
                  + ' 左键=' + (key === null ? '读不到' : (key ? '按下' : '松开'))
                  + ' 右键=' + (keyR === null ? '读不到' : (keyR ? '按下' : '松开'))
                  + ' klass=' + classNameOf(w) + ' w=' + w);
              } catch (e) {}
            }
          });
        } catch (e) {
          sendDevLog('warn', '快刀', 'WPN_Knife.Update 兜底钩子安装失败: ' + e.message, 'WPN_Knife.Update hook failed');
        }
      }

      // 兜底 C（只观测、不改游戏状态）：量出"物理左键已松开、游戏还在播近战攻击动画"的次数，
      // 并把**调用者**（returnAddress -> 模块+偏移）记下来 —— 这是"谁在重播连招"的唯一直接证据。
      // 2026-10 实测：combo=3 是在 fireBtnPressed=0、左键已松开的情况下播的，
      // 说明连招循环不由 fireBtnPressed 驱动，必须查出真正的调用方。
      if (!playKnifeAnimHook) {
        try {
          playKnifeAnimHook = Interceptor.attach(base.add(0xB642B0), {
            onEnter: function (args) {
              try {
                if (!enabled) return;
                var w = args[0];
                if (!w || w.isNull()) return;
                var owner = readPtr(w.add(0x30));
                if (!owner || !isMyPlayer || !isMyPlayer(owner, ptr(0))) return;   // 只看本地玩家的武器
                var combo = args[1].toInt32();
                // combo3 = 重击（右键/OnSpecialBtnDown），combo1/2 = 轻击连招（左键）。
                // 判"异常"必须用对应的那颗键，否则会把正常重击误报成异常（上一轮日志里就有这个误报）。
                var expectDown = (combo >= 3) ? physicalRightDown() : physicalLeftDown();
                var keyName = (combo >= 3) ? '物理右键' : '物理左键';
                if (combo >= 3 && diag.combo3 === undefined) diag.combo3 = 0;
                if (combo >= 3) diag.combo3++;
                if (combo >= 3 && diag.combo3 <= 6) {
                  sendDiag('combo=' + combo + ' 由 ' + callerOf(this.returnAddress) + ' 触发'
                    + '（weapon=' + w + '，klass=' + classNameOf(w) + '，fireBtn=' + w.add(0x78).readU8()
                    + '，' + keyName + '=' + keyStateText(expectDown) + '）');
                }
                if (expectDown !== false) return;                                  // 对应的键真的按着 -> 正常
                diag.animWhileUp++;
                if (diag.animWhileUp <= 8) {
                  sendDiag('异常：' + keyName + '已松开，游戏仍在播放近战攻击动画 combo=' + combo
                    + '，调用者=' + callerOf(this.returnAddress)
                    + '（weapon=' + w + '，klass=' + classNameOf(w) + '，fireBtn=' + w.add(0x78).readU8() + '）');
                }
              } catch (e) {}
            }
          });
        } catch (e) {
          sendDevLog('warn', '快刀', 'PlayKnifeAttackAnim 诊断钩子安装失败: ' + e.message, 'PlayKnifeAttackAnim probe hook failed');
        }
      }

      // 兜底 D：重击（右键/OnSpecialBtnDown）防卡死。
      // WPN_Knife.OnSpecialBtnDown(0xB64240) 是重击的唯一入口，且它没有任何状态位可清，
      // 所以只能在这里拦：物理右键没按 -> 不起手。
      if (!specialAddr) {
        try {
          specialAddr = base.add(0xB64240);
          // 必须在 Interceptor.replace 之前建好 NativeFunction，之后才能调到原函数
          specialOrig = new NativeFunction(specialAddr, 'void', ['pointer', 'pointer']);
          (function (addr, orig) {
            Interceptor.replace(addr, new NativeCallback(function (w, method) {
              var allow = true;
              try {
                if (enabled && w && !w.isNull()) {
                  var owner2 = readPtr(w.add(0x30));
                  if (owner2 && isMyPlayer && isMyPlayer(owner2, ptr(0))) {
                    if (physicalRightDown() === false) {          // true=真按着 / null=读不到 -> 都放行
                      allow = false;
                      specialBlocks++;
                      if (specialBlocks <= 8 || specialBlocks % 25 === 0) {
                        sendDiag('拦掉重击起手 #' + specialBlocks + '（物理右键=松开，WPN_Knife.OnSpecialBtnDown；'
                          + 'fireBtn=' + w.add(0x78).readU8()
                          + '，tag=' + csStringOf(readPtr(w.add(0x4C)))
                          + '，klass=' + classNameOf(w) + '）');
                      }
                    }
                  }
                }
              } catch (e) {}
              if (allow) {
                try { orig(w, method); } catch (e2) {}
              }
            }, 'void', ['pointer', 'pointer']));
          })(specialAddr, specialOrig);
        } catch (e) {
          specialAddr = null;
          specialOrig = null;
          sendDevLog('warn', '快刀', '重击(OnSpecialBtnDown)拦截安装失败: ' + e.message, 'OnSpecialBtnDown gate failed');
        }
      }

      Interceptor.replace(getKnifeSpeedAddr, new NativeCallback(function(self) {
        try {
          var owner = self.add(0x8).readPointer();
          if (!owner || owner.isNull()) {
            return originalGetKnifeSpeed(self);
          }

          if (isMyPlayer(owner, ptr(0))) {
            var role = getNanoRole ? getNanoRole(owner, ptr(0)) : 0;
            var human = isHumanRole ? isHumanRole(role, ptr(0)) : true;
            var value = currentSpeed;

            // 幽灵/终结者（NanoRole 1..17）仍然生效，但限速：
            // 它们用的是 WPN_Knife 子类，KnifeSpeed 会被 CFAnimator.SetFloat 同时写进角色 Animator，
            // 速度过高时连招(Combo1/Combo2)反复重播、刀光/爪痕叠加 = 攻击残影
            if (!human && value > ghostSpeedCap) value = ghostSpeedCap;

            logCount++;
            if (logCount <= 10) {
              sendLog('info', '快刀', '[KnifeSpeed] role=' + role + ' human=' + human + ' -> ' + value + 'x');
            }
            return value;
          }

          return originalGetKnifeSpeed(self);
        } catch(e) {
          sendDevLog('error', '快刀', '快刀 Hook 回调异常: ' + e.message, 'KnifeSpeed callback error');
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
      if (fireBtnHook) { try { fireBtnHook.detach(); } catch (e) {} fireBtnHook = null; }
      if (knifeUpdateHook) { try { knifeUpdateHook.detach(); } catch (e) {} knifeUpdateHook = null; }
      if (playKnifeAnimHook) { try { playKnifeAnimHook.detach(); } catch (e) {} playKnifeAnimHook = null; }
      if (specialAddr) { try { Interceptor.revert(specialAddr); } catch (e) {} specialAddr = null; }
      specialOrig = null;
      isMyPlayer = null;
      originalGetKnifeSpeed = null;
      getNanoRole = null;
      isHumanRole = null;
      getIsUsing = null;
      getKnifeSpeedAddr = null;
      enabled = false;
      sendLog('info', '快刀', '已禁用');
      sendStatus('knife', false);
    }
  };
})();


// Plugin RPC wrapper. Hook internals above are copied unchanged from the legacy script.
var __pluginFeatureId = "knife";
var __pluginModuleName = "knife";
var __pluginEnabled = false;
var __pluginConfig = {"speed": 5.0, "ghost_cap": 2.5};

function __pluginModule() {
  return modules[__pluginModuleName];
}

function __pluginApplyConfig(config) {
  if (config) {
    for (var key in config) {
      if (Object.prototype.hasOwnProperty.call(config, key)) __pluginConfig[key] = config[key];
    }
  }
  var module = __pluginModule();
  if (!module) return { ok: false, reason: 'module_not_loaded', config: __pluginConfig };
  var speed = __pluginConfig.speed;
  if (typeof speed !== 'number') speed = __pluginConfig.value;
  if (typeof speed === 'number' && typeof module.setSpeed === 'function') module.setSpeed(speed);
  var cap = __pluginConfig.ghost_cap;
  if (typeof cap === 'number' && typeof module.setGhostCap === 'function') module.setGhostCap(cap);
  return { ok: true, config: __pluginConfig };
}

function __pluginEnable(config) {
  if (config) __pluginApplyConfig(config);
  var module = __pluginModule();
  if (!module || typeof module.enable !== 'function') return { ok: false, reason: 'enable_missing' };
  var result = module.enable();
  __pluginEnabled = true;
  return result || { ok: true, enabled: true };
}

function __pluginDisable() {
  var module = __pluginModule();
  if (module && typeof module.disable === 'function') module.disable();
  __pluginEnabled = false;
  return { ok: true, enabled: false };
}

function __pluginStatus() {
  var module = __pluginModule();
  var stats = {};
  try {
    if (module && typeof module.getstatus === 'function') stats = module.getstatus();
    else if (module && typeof module.getStatus === 'function') stats = module.getStatus();
  } catch (_) {}
  return { enabled: __pluginEnabled, config: __pluginConfig, stats: stats };
}

function __pluginCleanup(payload) {
  __pluginDisable();
  return { ok: true, reason: payload && payload.reason ? payload.reason : 'cleanup' };
}

rpc.exports = {
  enable: __pluginEnable,
  disable: __pluginDisable,
  setConfig: __pluginApplyConfig,
  status: __pluginStatus,
  cleanup: __pluginCleanup
};

