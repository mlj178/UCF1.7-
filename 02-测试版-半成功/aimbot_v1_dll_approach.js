// ====================================================================
// 自瞄模块 v2 — 基于 UnityCrossFire.dll 逆向方案（BUG修复版 + 射线检测优化）
// 参考: 02-小工具dll逆向分析 copy.md
//
// 核心思路（完全还原 DLL 方案）:
//   1. GetAsyncKeyState 检测热键（或 Input.GetMouseButton）
//   2. 获取 GameManager → 找到 myPlayer
//   3. 遍历 allPlayers/playersBL/playersGR
//   4. 排除: 自己(isMyPlayer) / 死亡(isDead) / 同队(team)
//   5. 获取目标位置: get_transform() → get_position()
//   6. 计算角度: yaw=atan2(dx,dz) pitch=atan2(dy,distance)  单位: 弧度
//   7. 平滑: curAng + (targetAng - curAng) * smoothFactor
//   8. 写入角度: AddCameraRotation(deltaYaw, deltaPitch)
//   9. 重置标志（防游戏拉回准星）
//
// 🐛 BUG FIX LIST:
//   FIX #1: getGM() 获取方式 — 必须先读 MethodInfo 指针
//   FIX #2: 标志重置 — 用 characterContainer(0x58) 而非 recoil(0x54)
//   FIX #3: readList() — 用 List._size(0x0C) 而非 Array.length
//   FIX #4: 新增独立 log 通道 — console.log 保证日志可观测
//
// 🚀 射线检测优化:
//   - 检查顺序: 距离 → 粗筛FOV → 射线检测 → 精确FOV
//   - 默认关闭，可通过配置开启
// ====================================================================
(function() {
  'use strict';

  // ================================================================
  // 日志系统（双通道: send() + console.log()）
  // ================================================================
  var MAX_LOGS_PER_MODULE = 100;
  var moduleLogCounts = {};

  function sendLog(level, module, message) {
    if (!moduleLogCounts[module]) moduleLogCounts[module] = 0;
    if (moduleLogCounts[module] >= MAX_LOGS_PER_MODULE) return;
    moduleLogCounts[module]++;
    var fullMsg = '[' + module + '] ' + message;
    console.log(fullMsg);
    send({ type: 'log', level: level, module: module, message: message });
  }

  function sendStatus(feature, enabled) {
    console.log('[状态] ' + feature + ' -> ' + (enabled ? '开' : '关'));
    send({ type: 'status', feature: feature, enabled: enabled });
  }

  // ================================================================
  // 获取 GameAssembly.dll
  // ================================================================
  var _gameAssembly = null;

  function getGameAssembly() {
    if (_gameAssembly) return _gameAssembly;
    try {
      var mod = Process.findModuleByName('GameAssembly.dll');
      if (!mod) {
        console.log('[系统] 未找到 GameAssembly.dll');
        return null;
      }
      _gameAssembly = mod;
      console.log('[系统] GameAssembly.dll: base=' + mod.base + ' size=' + mod.size);
      return mod;
    } catch(e) {
      console.log('[系统] 获取模块失败: ' + e.message);
      return null;
    }
  }

  // ================================================================
  // RVA 常量
  // ================================================================
  var RVA = {
    Component_get_transform:         0x32CF40,   // Transform* (Component*, MethodInfo*)
    Transform_get_position:          0x3F42B0,   // Vector3* (Vector3* ret, Transform*, MethodInfo*)
    Player_get_isMyPlayer:           0xB55FD0,   // bool (Player*, MethodInfo*)
    Entity_get_isDead:               0xB400E0,   // bool (Entity*, MethodInfo*)
    Entity_get_team:                 0x1E0070,   // Team/int32 (Entity*, MethodInfo*)
    Player_AddCameraRotation:        0xB4F790,   // void (Player*, float x, float y, MethodInfo*)
    Input_GetMouseButton:            0xACFB20,   // bool (int32 button, MethodInfo*)
    Physics_Linecast:                0xAB9D20,   // bool (Vector3 start, Vector3 end, int32 layerMask, MethodInfo*)
  };

  // ================================================================
  // 字段偏移
  // ================================================================
  var OFF = {
    // GameManager 字段
    GM_allPlayers:      0x1C,   // Player[]     ← 所有玩家数组
    GM_playersBL:       0x20,   // List<Player> ← 黑队列表
    GM_playersGR:       0x28,   // List<Player> ← 红队列表

    // Entity 字段
    E_team:             0x20,   // Team (int32)

    // Player 字段
    P_cameraRotation:   0x4C,   // Vector2 (x=yaw, y=pitch) [弧度]
    P_recoil:           0x54,   // Recoil pointer
    P_characterContainer: 0x58, // Transform (characterContainer)

    // IL2CPP 数组
    Arr_len:            0x0C,   // il2cpp_array_size_t
    Arr_data:           0x10,   // data start

    // IL2CPP List
    List_items:         0x08,   // T[] _items
    List_size:          0x0C,   // int _size  ← 实际元素数量！

    // 指针大小
    ptrSize:            4,
  };

  // ================================================================
  // 骨骼索引
  // ================================================================
  var BONE = {
    HEAD:  0,
    NECK:  3,
    CHEST: 7,
    PELVIS: 10,
    HAND:  6,
  };

  var BONE_Y_OFFSET = {};
  BONE_Y_OFFSET[BONE.HEAD]   = 1.65;
  BONE_Y_OFFSET[BONE.NECK]   = 1.45;
  BONE_Y_OFFSET[BONE.CHEST]  = 1.05;
  BONE_Y_OFFSET[BONE.PELVIS] = 0.85;
  BONE_Y_OFFSET[BONE.HAND]   = 0.75;

  // ================================================================
  // 自瞄模块
  // ================================================================
  var aimModule = (function() {
    var enabled = false;
    var myPlayer = null;
    var targetEnemy = null;
    var timer = null;
    var roomHooks = [];
    var frameCount = 0;

    // ——— 配置 ———
    var CONFIG = {
      aimKey:          0,      // 触发按键: 0=鼠标左键 (Input.GetMouseButton)
      aimBone:         BONE.CHEST,
      smoothness:      1.0,    // 1.0 = 瞬间瞄准
      maxAimDistance:  200.0,
      maxAngleFOV:     30.0,
      visibilityCheck: false,  // 🚀 默认关闭射线检测，可通过配置开启
      autoAim:         false,  // false=按按键才瞄, true=一直瞄
      debugLog:        true,   // true=输出详细调试日志
    };

    // ——— NativeFunction 缓存 ———
    var singletonGetter = null;     // Singleton<GameManager>.get_instance
    var compGetTransform = null;
    var transformGetPos = null;
    var isMyPlayerFn = null;
    var isDeadFn = null;
    var getTeamFn = null;
    var addCamRotFn = null;
    var getMouseBtnFn = null;
    var linecastFn = null;

    // ——— 定时器 ———
    var aimTimer = null;
    var scanTimer = null;
    var debugTimer = null;

    // ================================================================
    // 获取 GameManager 单例（参考 lock-health 成功方案）
    // ================================================================
    function getGM() {
      try {
        var base = getGameAssembly().base;
        var mi = base.add(0xE1CE64).readPointer();
        if (mi.isNull()) {
          return singletonGetter(ptr(0));
        }
        var gm = singletonGetter(mi);
        if (gm.isNull()) return null;
        return gm;
      } catch(e) {
        return null;
      }
    }

    // ================================================================
    // 房间切换 Hook
    // ================================================================
    function installRoomHooks(base) {
      var addrs = [0xAEE370, 0xAF5B30];
      for (var i = 0; i < addrs.length; i++) {
        try {
          (function(addr) {
            var h = Interceptor.attach(base.add(addr), {
              onEnter: function() {
                myPlayer = null;
                targetEnemy = null;
                cachedTarget = null;
                frameCount = 0;
                console.log('[状态] 🔄 房间切换，状态重置');
              }
            });
            roomHooks.push(h);
          })(addrs[i]);
        } catch(e) {}
      }
    }

    // ================================================================
    // 初始化 NativeFunction
    // ================================================================
    function initNativeFunctions() {
      var mod = getGameAssembly();
      if (!mod) return false;
      var base = mod.base;

      try {
        compGetTransform = new NativeFunction(base.add(RVA.Component_get_transform), 'pointer', ['pointer', 'pointer']);
      } catch(e) { console.log('[初始化] compGetTransform 失败: ' + e.message); return false; }

      try {
        transformGetPos = new NativeFunction(base.add(RVA.Transform_get_position), 'void', ['pointer', 'pointer', 'pointer']);
      } catch(e) { console.log('[初始化] transformGetPos 失败: ' + e.message); return false; }

      try {
        isMyPlayerFn = new NativeFunction(base.add(RVA.Player_get_isMyPlayer), 'bool', ['pointer', 'pointer']);
      } catch(e) { console.log('[初始化] isMyPlayerFn 失败: ' + e.message); return false; }

      try {
        isDeadFn = new NativeFunction(base.add(RVA.Entity_get_isDead), 'bool', ['pointer', 'pointer']);
      } catch(e) { console.log('[初始化] isDeadFn 失败: ' + e.message); return false; }

      try {
        getTeamFn = new NativeFunction(base.add(RVA.Entity_get_team), 'int32', ['pointer', 'pointer']);
      } catch(e) { console.log('[初始化] getTeamFn 失败(将用内存读): ' + e.message); getTeamFn = null; }

      try {
        addCamRotFn = new NativeFunction(base.add(RVA.Player_AddCameraRotation), 'void', ['pointer', 'float', 'float', 'pointer']);
      } catch(e) { console.log('[初始化] addCamRotFn 失败: ' + e.message); return false; }

      try {
        getMouseBtnFn = new NativeFunction(base.add(RVA.Input_GetMouseButton), 'bool', ['int32', 'pointer']);
      } catch(e) { console.log('[初始化] getMouseBtnFn 失败: ' + e.message); getMouseBtnFn = null; }

      try {
        linecastFn = new NativeFunction(base.add(RVA.Physics_Linecast), 'bool', ['pointer', 'pointer', 'int32', 'int32', 'pointer']);
// 参数说明: start (Vector3*), end (Vector3*), layerMask, queryTriggerInteraction, method
        // 测试调用：传入空指针看是否会崩溃（可选）
        console.log('[初始化] linecastFn 已加载，地址=' + base.add(RVA.Physics_Linecast));
      } catch(e) { console.log('[初始化] linecastFn 失败: ' + e.message); linecastFn = null; }

      console.log('[初始化] 全部 NativeFunction 就绪');

      // 初始化 Singleton<GameManager>.get_instance
      try {
        singletonGetter = new NativeFunction(base.add(0x4A8170), 'pointer', ['pointer']);
      } catch(e) {
        console.log('[初始化] singletonGetter 失败: ' + e.message);
        return false;
      }

      return true;
    }

    // ================================================================
    // 工具函数
    // ================================================================

    function isValidPlayer(pp) {
      if (!pp || pp.isNull()) return false;
      try {
        var team = pp.add(OFF.E_team).readS32();
        return (team === 0 || team === 1 || team === 2);
      } catch(e) {
        return false;
      }
    }

    // 🐛 FIX #3: readList — 用 List._size (0x0C) 而非 Array.len
    function readList(listPtr) {
      var result = [];
      if (!listPtr || listPtr.isNull()) return result;
      try {
        var items = listPtr.add(OFF.List_items).readPointer();
        if (!items || items.isNull()) return result;
        var count = listPtr.add(OFF.List_size).readS32();  // 实际元素数量
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

    // 获取所有玩家（去重）
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

    // 获取玩家位置
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
        var container = player.add(OFF.P_characterContainer).readPointer();
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
      var yOff = BONE_Y_OFFSET[boneIndex];
      if (yOff !== undefined) pos.y += yOff;
      return pos;
    }

    function calcAngles(from, to) {
      var dx = to.x - from.x;
      var dy = to.y - from.y;
      var dz = to.z - from.z;
      var hDist = Math.sqrt(dx*dx + dz*dz);
      if (hDist < 0.01) return null;
      return { yaw: Math.atan2(dx, dz), pitch: Math.atan2(dy, hDist) };
    }

    function normalizeAngle(a) {
      while (a > Math.PI) a -= 2 * Math.PI;
      while (a < -Math.PI) a += 2 * Math.PI;
      return a;
    }
    
    function checkVisibility(from, to) { 
      if (!linecastFn) { 
        if (CONFIG.debugLog && frameCount < 3) 
          console.log('[射线] ❌ linecastFn 为空，默认可见'); 
        return true; 
      } 
      try { 
        var start = Memory.alloc(12); 
        start.writeFloat(from.x); 
        start.add(4).writeFloat(from.y); 
        start.add(8).writeFloat(from.z); 
     
        var end = Memory.alloc(12); 
        end.writeFloat(to.x); 
        end.add(4).writeFloat(to.y); 
        end.add(8).writeFloat(to.z); 
     
        var layerMask = -1;               // 所有层 
        var queryTriggerInteraction = 0;  // 忽略触发器 
        var method = ptr(0);              // MethodInfo* 
     
        var hitAnything = linecastFn(start, end, layerMask, queryTriggerInteraction, method); 
        var visible = !hitAnything; 
     
        if (CONFIG.debugLog && frameCount < 20) { 
          console.log('[射线] 起点=(' + from.x.toFixed(1) + ',' + from.y.toFixed(1) + ',' + from.z.toFixed(1) + 
                      ') 终点=(' + to.x.toFixed(1) + ',' + to.y.toFixed(1) + ',' + to.z.toFixed(1) + 
                      ') 碰撞=' + hitAnything + ' 可见=' + visible); 
        } 
        return visible; 
      } catch(e) { 
        if (CONFIG.debugLog && frameCount < 3) 
          console.log('[射线] 异常: ' + e.message); 
        return true; 
      } 
    }

    // ——— 目标缓存（成功脚本的 dword_1005A6C8 模式） ———
    var cachedTarget = null;
    var scanYawDeg = 0;    // 扫描时的视角，用于检测用户是否主动转视角
    var scanPitchDeg = 0;

    // ================================================================
    // 目标扫描器（优化顺序：距离 → 粗筛FOV → 射线检测 → 精确FOV）
    // ================================================================
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

      try {
        if (!isMyPlayerFn(myPlayer, ptr(0))) { myPlayer = null; cachedTarget = null; return; }
      } catch(e) { myPlayer = null; cachedTarget = null; return; }

      try { if (isDeadFn(myPlayer, ptr(0))) return; } catch(e) { return; }

      var myPos = getBonePos(myPlayer, BONE.CHEST);
      if (!myPos) return;

      // 保存扫描时的视角（用于检测用户是否主动转视角）
      scanYawDeg = myPlayer.add(OFF.P_cameraRotation).readFloat();
      scanPitchDeg = myPlayer.add(OFF.P_cameraRotation + 4).readFloat();

      var allPlayers = getAllPlayers(gm);
      var myTeam = 0;
      try {
        if (getTeamFn) myTeam = getTeamFn(myPlayer, ptr(0));
        else myTeam = myPlayer.add(OFF.E_team).readS32();
      } catch(e) {}

      var best = null;
      var bestAngleDeg = 999999;

      for (var i = 0; i < allPlayers.length; i++) {
        var p = allPlayers[i];
        try {
          if (p.equals(myPlayer)) continue;
          if (isDeadFn(p, ptr(0))) continue;
          var team = getTeamFn ? getTeamFn(p, ptr(0)) : p.add(OFF.E_team).readS32();
          if (team === myTeam) continue;

          // 1. 获取目标骨骼位置
          var targetPos = getBonePos(p, CONFIG.aimBone);
          if (!targetPos) continue;

          // 2. 距离检查（廉价）
          var dx = targetPos.x - myPos.x;
          var dy = targetPos.y - myPos.y;
          var dz = targetPos.z - myPos.z;
          var dist = Math.sqrt(dx*dx + dy*dy + dz*dz);
          if (dist > CONFIG.maxAimDistance) continue;

          // 3. 粗筛角度 FOV（扩大 20°，避免频繁射线检测）
          var targetYawDeg = Math.atan2(dx, dz) * 180.0 / Math.PI;
          var targetPitchDeg = Math.atan2(dy, Math.sqrt(dx*dx + dz*dz)) * 180.0 / Math.PI;
          var yawDiffRaw = targetYawDeg - scanYawDeg;
          var pitchDiffRaw = targetPitchDeg - scanPitchDeg;
          if (yawDiffRaw > 180) yawDiffRaw -= 360;
          if (yawDiffRaw < -180) yawDiffRaw += 360;
          if (pitchDiffRaw > 180) pitchDiffRaw -= 360;
          if (pitchDiffRaw < -180) pitchDiffRaw += 360;
          var rawAngleDeg = Math.sqrt(yawDiffRaw*yawDiffRaw + pitchDiffRaw*pitchDiffRaw);
          // 粗筛阈值 = 最大FOV + 20°
          var coarseFOV = CONFIG.maxAngleFOV + 20.0;
          if (rawAngleDeg > coarseFOV) continue;

          // 4. 🚀 射线检测（仅当启用时，较昂贵，放在最后）
          if (CONFIG.visibilityCheck) {
            if (!checkVisibility(myPos, targetPos)) {
              continue;   // 墙体遮挡，跳过该敌人
            }
          }

          // 5. 精确角度差（用于最终选择最佳目标）
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
            best = {
              player: p,
              pos: targetPos,
              targetYawDeg: targetYawDeg,
              targetPitchDeg: targetPitchDeg,
              angleDeg: angleDeg,
              dist: dist,
            };
          }
        } catch(e) {
          if (frameCount < 5) console.log('[扫描] 敌人#' + i + ' 异常: ' + e.message);
        }
      }

      if (best) {
        cachedTarget = best;
        if (frameCount < 5) {
          console.log('[扫描] ✅ 目标: yaw=' + best.targetYawDeg.toFixed(1) + '° pitch=' + best.targetPitchDeg.toFixed(1) + '° 角差=' + best.angleDeg.toFixed(1) + '° 距离=' + best.dist.toFixed(1) + 'm');
        }
      } else {
        cachedTarget = null;
      }
    }

    // ================================================================
    // DLL 方案: 写角度到内存
    // ================================================================
    function writeAimbot() {
      if (!enabled || !myPlayer || !cachedTarget) return;

      try {
        // 检测用户是否主动转动了视角（与扫描时的视角对比）
        var curYawDeg = myPlayer.add(OFF.P_cameraRotation).readFloat();
        var curPitchDeg = myPlayer.add(OFF.P_cameraRotation + 4).readFloat();
        var userYawDelta = curYawDeg - scanYawDeg;
        var userPitchDelta = curPitchDeg - scanPitchDeg;
        if (userYawDelta > 180) userYawDelta -= 360;
        if (userYawDelta < -180) userYawDelta += 360;
        if (userPitchDelta > 180) userPitchDelta -= 360;
        if (userPitchDelta < -180) userPitchDelta += 360;
        var userAngleDelta = Math.sqrt(userYawDelta*userYawDelta + userPitchDelta*userPitchDelta);

        // 如果用户主动转了超过 FOV 的一半，释放目标让 scanner 重新选
        if (userAngleDelta > CONFIG.maxAngleFOV * 0.5) {
          cachedTarget = null;
          return;
        }

        var targetYawDeg = cachedTarget.targetYawDeg;
        var targetPitchDeg = cachedTarget.targetPitchDeg;

        // 平滑: cur + (target-cur) * factor (度空间)
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

        // DLL: 直接写内存 (度)
        myPlayer.add(OFF.P_cameraRotation).writeFloat(finalYawDeg);
        myPlayer.add(OFF.P_cameraRotation + 4).writeFloat(finalPitchDeg);

        // DLL: 重置 Recoil 标志
        var recoil = myPlayer.add(OFF.P_recoil).readPointer();
        if (recoil && !recoil.isNull()) {
          recoil.add(0x10).writeU32(0);
          recoil.add(0x24).writeU32(0);
          recoil.add(0x40).writeU32(0);
          recoil.add(0x54).writeU32(0);
        }

        frameCount++;
        if (frameCount <= 5) {
          console.log('[自瞄] ✅ 写入 #' + frameCount + ' 目标=' + targetYawDeg.toFixed(1) + '°/' + targetPitchDeg.toFixed(1) + '° 当前=' + curYawDeg.toFixed(1) + '°/' + curPitchDeg.toFixed(1) + '°');
        }
      } catch(e) {
        console.log('[自瞄] 写入异常: ' + e.message);
      }
    }

    // ================================================================
    // 自瞄主循环（仅按键检测 + 调用 writeAimbot）
    // ================================================================
    var diagCount = 0;

    function aimLoop() {
      if (!enabled) return;

      if (!CONFIG.autoAim) {
        if (!getMouseBtnFn) {
          if (frameCount === 0) console.log('[自瞄] ❌ getMouseBtnFn 未初始化');
          return;
        }
        try {
          var btnDown = getMouseBtnFn(CONFIG.aimKey, ptr(0));
          if (!btnDown) return;
        } catch(e) {
          if (diagCount < 3) { diagCount++; console.log('[自瞄] ❌ getMouseBtnFn 异常: ' + e.message); }
          return;
        }
      }

      if (!myPlayer) return;
      if (!cachedTarget) return;

      writeAimbot();
    }

    // ================================================================
    // 调试扫描（每 2 秒输出完整数据）
    // ================================================================
    function debugScan() {
      if (!CONFIG.debugLog || !enabled) return;

      var gm = getGM();
      if (!gm || gm.isNull()) return;

      if (!myPlayer || myPlayer.isNull()) {
        var all = getAllPlayers(gm);
        for (var i = 0; i < all.length; i++) {
          try { if (isMyPlayerFn(all[i], ptr(0))) { myPlayer = all[i]; break; } } catch(e) {}
        }
        if (!myPlayer) return;
      }

      var myPos = getBonePos(myPlayer, BONE.CHEST);
      if (!myPos) return;

      var curYawDeg = myPlayer.add(OFF.P_cameraRotation).readFloat();
      var curPitchDeg = myPlayer.add(OFF.P_cameraRotation + 4).readFloat();

      console.log('');
      console.log('========== 📊 自瞄调试数据 ==========');
      console.log('[调试] 我的坐标: (' + myPos.x.toFixed(1) + ', ' + myPos.y.toFixed(1) + ', ' + myPos.z.toFixed(1) + ')');
      console.log('[调试] 当前视角: yaw=' + curYawDeg.toFixed(2) + '°  pitch=' + curPitchDeg.toFixed(2) + '°');

      var allPlayers = getAllPlayers(gm);
      var myTeam = 0;
      try {
        if (getTeamFn) myTeam = getTeamFn(myPlayer, ptr(0));
        else myTeam = myPlayer.add(OFF.E_team).readS32();
      } catch(e) {}

      var enemies = [];
      for (var i = 0; i < allPlayers.length; i++) {
        var p = allPlayers[i];
        try {
          if (p.equals(myPlayer)) continue;
          if (isDeadFn(p, ptr(0))) continue;
          var team = getTeamFn ? getTeamFn(p, ptr(0)) : p.add(OFF.E_team).readS32();
          if (team === myTeam) continue;
          enemies.push(p);
        } catch(e) {}
      }

      if (enemies.length === 0) {
        console.log('[调试] ❌ 没有敌人');
        console.log('========================================');
        return;
      }

      console.log('[调试] 敌人总数: ' + enemies.length);
      console.log('');

      for (var i = 0; i < enemies.length; i++) {
        try {
          var enemyPos = getBonePos(enemies[i], CONFIG.aimBone);
          if (!enemyPos) { console.log('[调试] 敌人#' + i + ' 坐标获取失败'); continue; }

          var dx = enemyPos.x - myPos.x;
          var dy = enemyPos.y - myPos.y;
          var dz = enemyPos.z - myPos.z;
          var dist = Math.sqrt(dx*dx + dy*dy + dz*dz);

          var angles = calcAngles(myPos, enemyPos);
          if (!angles) { console.log('[调试] 敌人#' + i + ' 角度计算失败'); continue; }

          var targetYawDeg = angles.yaw * 180.0 / Math.PI;
          var targetPitchDeg = angles.pitch * 180.0 / Math.PI;

          var yawDiffDeg = targetYawDeg - curYawDeg;
          var pitchDiffDeg = targetPitchDeg - curPitchDeg;
          if (yawDiffDeg > 180) yawDiffDeg -= 360;
          if (yawDiffDeg < -180) yawDiffDeg += 360;
          if (pitchDiffDeg > 180) pitchDiffDeg -= 360;
          if (pitchDiffDeg < -180) pitchDiffDeg += 360;
          var fovDeg = Math.sqrt(yawDiffDeg*yawDiffDeg + pitchDiffDeg*pitchDiffDeg);

          // 临时去掉 visibilityCheck 的限制，强制测试射线检测
          var visible = checkVisibility(myPos, enemyPos);

          console.log('[调试] 敌人#' + i + ' ptr=' + enemies[i] +
            ' 坐标=(' + enemyPos.x.toFixed(1) + ', ' + enemyPos.y.toFixed(1) + ', ' + enemyPos.z.toFixed(1) + ')' +
            ' 距离=' + dist.toFixed(1) + 'm' +
            ' 可见=' + visible);
          console.log('[调试]   → 目标: ' + targetYawDeg.toFixed(1) + '° 当前: ' + curYawDeg.toFixed(1) + '° 差: ' + yawDiffDeg.toFixed(1) + '° FOV=' + fovDeg.toFixed(1) + '°');
        } catch(e) {
          console.log('[调试] 敌人#' + i + ' 异常: ' + e.message);
        }
      }
      console.log('========================================');
      console.log('');
    }

    // ================================================================
    // 房间切换 Hook
    // ================================================================
    function installRoomHooks(base) {
      var addrs = [0xAF9A90, 0xAEE370, 0xAF5B30];
      for (var i = 0; i < addrs.length; i++) {
        try {
          var h = Interceptor.attach(base.add(addrs[i]), {
            onEnter: function() {
              myPlayer = null;
              targetEnemy = null;
              frameCount = 0;
              console.log('[自瞄] 房间切换，状态重置');
            }
          });
          roomHooks.push(h);
        } catch(e) {}
      }
    }

    // ================================================================
    // 公开接口
    // ================================================================
    return {
      enable: function() {
        if (enabled) {
          console.log('[自瞄] 已启用，跳过');
          return;
        }
        var mod = getGameAssembly();
        if (!mod) {
          console.log('[自瞄] 无 GameAssembly.dll');
          return;
        }

        if (!initNativeFunctions()) {
          console.log('[自瞄] NativeFunction 初始化失败');
          return;
        }

        installRoomHooks(mod.base);

        aimTimer = setInterval(aimLoop, 16);
        scanTimer = setInterval(targetScanner, 30);
        if (CONFIG.debugLog) {
          debugTimer = setInterval(debugScan, 2000);
        }

        enabled = true;
        console.log('[自瞄] ✅ 已启用 (触发键=' + CONFIG.aimKey +
          ' 平滑=' + CONFIG.smoothness +
          ' FOV=' + CONFIG.maxAngleFOV + '°' +
          ' 距离=' + CONFIG.maxAimDistance + 'm)');
        console.log('[自瞄] 💡 进入游戏房间后，按鼠标左键(开枪)触发自瞄');
        sendLog('success', '自瞄', '已启用');
        sendStatus('自瞄', true);
      },

      disable: function() {
        if (!enabled) return;
        if (aimTimer) { clearInterval(aimTimer); aimTimer = null; }
        if (scanTimer) { clearInterval(scanTimer); scanTimer = null; }
        if (debugTimer) { clearInterval(debugTimer); debugTimer = null; }
        for (var i = 0; i < roomHooks.length; i++) {
          try { roomHooks[i].detach(); } catch(e) {}
        }
        roomHooks = [];
        myPlayer = null;
        targetEnemy = null;
        enabled = false;
        console.log('[自瞄] ❌ 已禁用');
        sendLog('info', '自瞄', '已禁用');
        sendStatus('自瞄', false);
      },

      toggle: function() {
        if (enabled) this.disable();
        else this.enable();
      },

      isEnabled: function() { return enabled; },

      setConfig: function(cfg) {
        if (cfg.aimKey !== undefined) CONFIG.aimKey = cfg.aimKey;
        if (cfg.smoothness !== undefined) CONFIG.smoothness = cfg.smoothness;
        if (cfg.maxAimDistance !== undefined) CONFIG.maxAimDistance = cfg.maxAimDistance;
        if (cfg.maxAngleFOV !== undefined) CONFIG.maxAngleFOV = cfg.maxAngleFOV;
        if (cfg.visibilityCheck !== undefined) CONFIG.visibilityCheck = cfg.visibilityCheck;
        if (cfg.autoAim !== undefined) CONFIG.autoAim = cfg.autoAim;
        if (cfg.debugLog !== undefined) {
          CONFIG.debugLog = cfg.debugLog;
          if (enabled) {
            if (CONFIG.debugLog && !debugTimer) {
              debugTimer = setInterval(debugScan, 2000);
              console.log('[自瞄] 📊 调试扫描已启动');
            } else if (!CONFIG.debugLog && debugTimer) {
              clearInterval(debugTimer);
              debugTimer = null;
              console.log('[自瞄] 📊 调试扫描已关闭');
            }
          }
        }
        if (cfg.aimBone !== undefined) {
          if (cfg.aimBone === 'head') CONFIG.aimBone = BONE.HEAD;
          else if (cfg.aimBone === 'neck') CONFIG.aimBone = BONE.NECK;
          else if (cfg.aimBone === 'chest') CONFIG.aimBone = BONE.CHEST;
          else if (cfg.aimBone === 'pelvis') CONFIG.aimBone = BONE.PELVIS;
          else CONFIG.aimBone = cfg.aimBone;
        }
        console.log('[自瞄] 配置更新: ' + JSON.stringify(cfg));
      },

      getTarget: function() { return cachedTarget ? cachedTarget.player : null; },
      getConfig: function() {
        return {
          smoothness: CONFIG.smoothness,
          aimBone: CONFIG.aimBone,
          maxAngleFOV: CONFIG.maxAngleFOV,
          maxAimDistance: CONFIG.maxAimDistance,
          autoAim: CONFIG.autoAim,
          visibilityCheck: CONFIG.visibilityCheck,
          debugLog: CONFIG.debugLog,
          frameCount: frameCount,
        };
      },
    };
  })();

  // ================================================================
  // rpc.exports
  // ================================================================
  rpc.exports = {
    aimEnable: function() { aimModule.enable(); return 'ok'; },
    aim_enable: function() { aimModule.enable(); return 'ok'; },
    aimDisable: function() { aimModule.disable(); return 'ok'; },
    aim_disable: function() { aimModule.disable(); return 'ok'; },
    aimToggle: function() { aimModule.toggle(); return aimModule.isEnabled() ? 'enabled' : 'disabled'; },
    aim_toggle: function() { aimModule.toggle(); return aimModule.isEnabled() ? 'enabled' : 'disabled'; },
    aimStatus: function() { return aimModule.isEnabled() ? 'enabled' : 'disabled'; },
    aim_status: function() { return aimModule.isEnabled() ? 'enabled' : 'disabled'; },
    aimSetConfig: function(jsonStr) {
      try { aimModule.setConfig(JSON.parse(jsonStr)); return 'ok'; }
      catch(e) { return 'error: ' + e.message; }
    },
    aim_set_config: function(jsonStr) {
      try { aimModule.setConfig(JSON.parse(jsonStr)); return 'ok'; }
      catch(e) { return 'error: ' + e.message; }
    },
    aimGetStatus: function() {
      var cfg = aimModule.getConfig();
      return JSON.stringify({
        enabled: aimModule.isEnabled(),
        targetEnemy: aimModule.getTarget() ? aimModule.getTarget().toString() : null,
        smoothness: cfg.smoothness,
        aimBone: cfg.aimBone,
        maxAngleFOV: cfg.maxAngleFOV,
        maxAimDistance: cfg.maxAimDistance,
        autoAim: cfg.autoAim,
        visibilityCheck: cfg.visibilityCheck,
        debugLog: cfg.debugLog,
        frameCount: cfg.frameCount,
      });
    },
    aim_get_status: function() {
      var cfg = aimModule.getConfig();
      return JSON.stringify({
        enabled: aimModule.isEnabled(),
        targetEnemy: aimModule.getTarget() ? aimModule.getTarget().toString() : null,
        smoothness: cfg.smoothness,
        aimBone: cfg.aimBone,
        maxAngleFOV: cfg.maxAngleFOV,
        maxAimDistance: cfg.maxAimDistance,
        autoAim: cfg.autoAim,
        visibilityCheck: cfg.visibilityCheck,
        debugLog: cfg.debugLog,
        frameCount: cfg.frameCount,
      });
    },
  };

  // 自动启用
  console.log('[自瞄] 脚本加载完成，正在自动启用...');
  aimModule.enable();
})();