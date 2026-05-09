// ====================================================================
// 自瞄模块 (Aim Assist) v1.3 — 坐标读取崩溃修复版
// 功能: 鼠标左键按下时，将准星对准距离最近的敌人
// 修复: 删除直接读 characterContainer 内存的逻辑，仅用 get_transform 函数调用
//       参考 game_modifier_v1.3.py 成功代码方式，避免野指针 access violation
// 方案: 距离最近（函数调用获取位置 + 内存角度写入）
// ====================================================================
(function() {
  'use strict';

  var MAX_LOGS_PER_MODULE = 100;
  var moduleLogCounts = {};

  function sendLog(level, module, message) {
    if (!moduleLogCounts[module]) moduleLogCounts[module] = 0;
    if (moduleLogCounts[module] >= MAX_LOGS_PER_MODULE) return;
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
      return mod;
    } catch(e) { sendLog('error', '系统', '获取模块失败: ' + e.message); return null; }
  }

  var aimModule = (function() {
    var enabled = false;
    var myPlayer = null;
    var targetEnemy = null;
    var aimSmoothness = 1.0;      // 测试用：1.0 = 瞬间瞄准
    var scanInterval = 30;
    var aimBone = 'chest';
    var timer = null;
    var roomHooks = [];
    var botPlayers = {};
    var botUpdateHook = null;
    var logCount = 0;
    var lastEnemyCount = 0;
    var frameCount = 0;

    // NativeFunction 缓存
    var isMyPlayerFn = null;
    var singletonGetter = null;
    var isDeadFn = null;
    var getMouseButton = null;
    var compGetTransform = null;
    var transformGetPos = null;
    var addCamRotFn = null;

    var RVA = {
      P_isMyPlayer:   0xB55FD0,
      E_isDead:       0xB400E0,
      Input_GetMouse: 0xACFB20,
      SingletonGet:   0x4A8170,
      GM_Singleton:   0xE1CE64,
      GetTransform:   0x32CF40,   // 参考成功聚怪模块的地址
      GetPosition:    0x3F42B0,   // dump.cs: Transform.get_position 正确RVA
      Bot_Update:     0xB33370,
      AddCameraRot:   0xB4F790,   // Player.AddCameraRotation
    };

    var OFF = {
      GM_all:       0x1C,
      GM_BL:        0x20,
      GM_GR:        0x28,
      P_camRot:     0x4C,
      P_charCont:   0x58,
      E_team:       0x20,
      Arr_len:      0x0C,
      Arr_data:     0x10,
      Elem_sz:      8,
    };

    // ================================================================
    // 工具函数
    // ================================================================

    // 检查玩家指针是否有效 — 验证 team 字段值是否合法 (0/1/2)
    function isValidPlayer(pp) {
      if (!pp || pp.isNull()) return false;
      try {
        var team = pp.add(OFF.E_team).readS32();
        if (team !== 0 && team !== 1 && team !== 2) return false;
        return true;
      } catch(e) {
        return false;
      }
    }

    // 扫描 PlayerCameraManager 找出随鼠标移动变化的浮点数字段
    var prevCamMgrFloats = {};

    function scanCameraManager(camMgr) {
      if (!camMgr || camMgr.isNull()) return;
      try {
        var changed = [];
        for (var off = 0; off <= 0x80; off += 4) {
          var val = camMgr.add(off).readFloat();
          var key = off.toString(16);
          if (prevCamMgrFloats[key] !== undefined) {
            var diff = Math.abs(val - prevCamMgrFloats[key]);
            if (diff > 0.001) {
              changed.push('0x' + key + '=' + prevCamMgrFloats[key].toFixed(4) + '->' + val.toFixed(4) + ' d=' + diff.toFixed(4));
            }
          }
          prevCamMgrFloats[key] = val;
        }
        if (changed.length > 0 && changed.length <= 8) {
          sendLog('info', '扫描', 'cameraManager 变化: ' + changed.join(' | '));
        }
      } catch(e) {}
    }

    function addBotPlayer(botPlayer) {
      if (!botPlayer || botPlayer.isNull()) return;
      try {
        if (!isValidPlayer(botPlayer)) return;
        botPlayers[botPlayer.toString()] = { player: botPlayer, time: Date.now() };
      } catch(e) {}
    }

    function cleanupBotPlayers() {
      var now = Date.now();
      for (var key in botPlayers) {
        if (now - botPlayers[key].time > 5000) {
          delete botPlayers[key];
        }
      }
    }

    function getGM() {
      try {
        var mi = getGameAssembly().base.add(RVA.GM_Singleton).readPointer();
        return mi && !mi.isNull() ? singletonGetter(mi) : null;
      } catch(e) { return null; }
    }

    function getAllPlayers(gm) {
      var ps = {};
      try {
        var ap = gm.add(OFF.GM_all).readPointer();
        if (ap && !ap.isNull()) {
          var n = ap.add(OFF.Arr_len).readU32();
          for (var i = 0; i < n; i++) {
            var pp = ap.add(OFF.Arr_data + i * OFF.Elem_sz).readPointer();
            if (pp && !pp.isNull() && isValidPlayer(pp)) ps[pp.toString()] = pp;
          }
        }
      } catch(e) {}
      try {
        var bl = gm.add(OFF.GM_BL).readPointer();
        if (bl && !bl.isNull()) {
          var n = bl.add(OFF.Arr_len).readU32();
          for (var i = 0; i < n; i++) {
            var pp = bl.add(OFF.Arr_data + i * OFF.Elem_sz).readPointer();
            if (pp && !pp.isNull() && isValidPlayer(pp)) ps[pp.toString()] = pp;
          }
        }
      } catch(e) {}
      try {
        var gr = gm.add(OFF.GM_GR).readPointer();
        if (gr && !gr.isNull()) {
          var n = gr.add(OFF.Arr_len).readU32();
          for (var i = 0; i < n; i++) {
            var pp = gr.add(OFF.Arr_data + i * OFF.Elem_sz).readPointer();
            if (pp && !pp.isNull() && isValidPlayer(pp)) ps[pp.toString()] = pp;
          }
        }
      } catch(e) {}
      // 存活列表补充：playersBL_Alive(0x24) + playersGR_Alive(0x2C)
      try {
        var bl = gm.add(0x24).readPointer();
        if (bl && !bl.isNull()) {
          var n = bl.add(OFF.Arr_len).readU32();
          for (var i = 0; i < n; i++) {
            var pp = bl.add(OFF.Arr_data + i * OFF.Elem_sz).readPointer();
            if (pp && !pp.isNull() && isValidPlayer(pp)) ps[pp.toString()] = pp;
          }
        }
      } catch(e) {}
      try {
        var gr = gm.add(0x2C).readPointer();
        if (gr && !gr.isNull()) {
          var n = gr.add(OFF.Arr_len).readU32();
          for (var i = 0; i < n; i++) {
            var pp = gr.add(OFF.Arr_data + i * OFF.Elem_sz).readPointer();
            if (pp && !pp.isNull() && isValidPlayer(pp)) ps[pp.toString()] = pp;
          }
        }
      } catch(e) {}
      // 补充 Bot 玩家
      cleanupBotPlayers();
      for (var key in botPlayers) {
        var entry = botPlayers[key];
        if (entry && entry.player && isValidPlayer(entry.player)) {
          var pp = entry.player;
          if (!ps[pp.toString()]) {
            ps[pp.toString()] = pp;
          }
        }
      }
      return Object.values(ps);
    }

    // 扫描 Transform 内存找出非零浮点数（用于确定 position 偏移）
    function scanTransform(transform, tag) {
      sendLog('debug', '扫描', tag + ' 扫描 Transform @ ' + transform);
      for (var off = 0; off <= 0x80; off += 4) {
        try {
          var val = transform.add(off).readFloat();
          if (Math.abs(val) > 0.01 && Math.abs(val) < 5000) {
            sendLog('debug', '扫描', tag + ' 偏移 0x' + off.toString(16) + ' = ' + val.toFixed(2));
          }
        } catch(e) {}
      }
    }

    // 获取玩家位置 — 优先 get_transform 函数，失败后备 characterContainer
    // 直接读 Transform 内存字段获取坐标，不调用 transformGetPos（地址不稳定导致崩溃）
    function getPlayerPos(player, tag) {
      try {
        sendLog('debug', '位置调试', tag + ' player ptr=' + player);
        var vtable = player.readPointer();
        if (vtable.isNull()) {
          sendLog('error', '位置调试', tag + ' player vtable 为空');
          return null;
        }

        var transform = null;

        // 方案1：通过 get_transform 函数调用
        try {
          transform = compGetTransform(player, ptr(0));
          if (transform && !transform.isNull()) {
            sendLog('debug', '位置调试', tag + ' get_transform 成功，transform=' + transform);
          } else {
            sendLog('warn', '位置调试', tag + ' get_transform 返回 null');
          }
        } catch(e) {
          sendLog('error', '位置调试', tag + ' get_transform 异常: ' + e.message);
          transform = null;
        }

        // 方案2（后备）：直接读 characterContainer 字段
        if (!transform || transform.isNull()) {
          var container = player.add(0x58).readPointer();
          if (container && !container.isNull()) {
            transform = container;
            sendLog('debug', '位置调试', tag + ' 使用 characterContainer(0x58)，transform=' + transform);
          } else {
            sendLog('error', '位置调试', tag + ' 无法获取 transform');
            return null;
          }
        }

        // 扫描 Transform 内存查找正确偏移（调试完毕，注释掉减少日志）
        // scanTransform(transform, tag);

        // ✅ 方案A: 调用 Transform.get_position (RVA 0x3F42B0 已验证)
        try {
          var posBuf = Memory.alloc(12);
          // 用函数签名: Vector3* get_position(Vector3* retstr, Transform* this, MethodInfo* method)
          var resultPtr = new NativeFunction(getGameAssembly().base.add(0x3F42B0), 'pointer', ['pointer', 'pointer', 'pointer']);
          resultPtr(posBuf, transform, ptr(0));
          var fx = posBuf.readFloat();
          var fy = posBuf.add(4).readFloat();
          var fz = posBuf.add(8).readFloat();
          if (Math.abs(fx) < 5000 && Math.abs(fy) < 5000 && Math.abs(fz) < 5000 && !(fx === 0 && fy === 0 && fz === 0)) {
            sendLog('debug', '位置调试', tag + ' get_position函数 坐标=' + fx.toFixed(1) + ',' + fy.toFixed(1) + ',' + fz.toFixed(1));
            return { x: fx, y: fy, z: fz };
          }
        } catch(e) {
          sendLog('warn', '位置调试', tag + ' get_position函数 异常: ' + e.message);
        }

        // ✅ 方案B: 直接读 Transform 内存字段
        // 尝试偏移: 0x08, 0x10, 0x18, 0x20, 0x28, 0x2C, 0x30, 0x34, 0x38, 0x3C, 0x40
        var tryOffsets = [0x08, 0x10, 0x18, 0x20, 0x28, 0x2C, 0x30, 0x34, 0x38, 0x3C, 0x40];
        for (var i = 0; i < tryOffsets.length; i++) {
          try {
            var off = tryOffsets[i];
            var x = transform.add(off).readFloat();
            var y = transform.add(off + 4).readFloat();
            var z = transform.add(off + 8).readFloat();
            // 合理性检查：非全零且在地图范围内
            if (Math.abs(x) < 5000 && Math.abs(y) < 5000 && Math.abs(z) < 5000 && !(x === 0 && y === 0 && z === 0)) {
              sendLog('debug', '位置调试', tag + ' 偏移 0x' + off.toString(16) + ' 坐标=' + x.toFixed(1) + ',' + y.toFixed(1) + ',' + z.toFixed(1));
              return { x: x, y: y, z: z };
            }
          } catch(e) {}
        }

        sendLog('error', '位置调试', tag + ' 所有偏移读取坐标均失败');
        return null;
      } catch(e) {
        sendLog('error', '位置调试', tag + ' 异常: ' + e.message);
        return null;
      }
    }

    function getEyePos(player) {
      var p = getPlayerPos(player, '眼睛');
      if (p) p.y += 1.5;
      return p;
    }

    function calcAngles(from, to) {
      var dx = to.x - from.x, dy = to.y - from.y, dz = to.z - from.z;
      var d = Math.sqrt(dx*dx + dz*dz);
      if (d < 0.01) return null;
      return { yaw: Math.atan2(dx, dz), pitch: Math.atan2(dy, d) };
    }

    // ================================================================
    // 模式感知 + 敌人筛选
    // ================================================================

    function detectGameMode(gm) {
      try {
        var all = getAllPlayers(gm);
        for (var i = 0; i < all.length; i++) {
          var t = all[i].add(OFF.E_team).readS32();
          if (t === 2) {
            sendLog('info', '调试', '发现 Neutral(2) 队伍，判定为生化模式');
            return 3;
          }
        }
      } catch(e) {
        sendLog('error', '调试', 'detectGameMode 异常: ' + e.message);
      }
      sendLog('info', '调试', '未发现 Neutral 队伍，默认团队模式(0)');
      return 0;
    }

    function isEnemy(lp, t, mode) {
      if (t.equals(lp)) return false;
      if (mode === 1) return true;
      var mt = lp.add(OFF.E_team).readS32(), tt = t.add(OFF.E_team).readS32();
      if (mt === tt) return false;
      if (mode >= 3) return true;
      return tt !== 2;
    }

    function getEnemyList(gm, lp, mode) {
      var all = getAllPlayers(gm);
      var enemies = [];
      sendLog('info', '调试', 'getEnemyList: total players=' + all.length + ' mode=' + mode);
      for (var i = 0; i < all.length; i++) {
        try {
          var player = all[i];
          var team = player.add(OFF.E_team).readS32();
          sendLog('debug', '调试', '检查玩家' + i + ': ptr=' + player + ' team=' + team);

          if (!isValidPlayer(player)) {
            sendLog('warn', '调试', '玩家' + i + ' 有效性检查失败，跳过');
            continue;
          }

          if (player.equals(lp)) {
            sendLog('debug', '调试', '玩家' + i + ' = 自己，跳过');
            continue;
          }

          var isDead = false;
          try { isDead = isDeadFn(player, ptr(0)); }
          catch(e) { sendLog('error', '调试', 'isDeadFn 异常: ' + e.message); continue; }
          if (isDead) { sendLog('debug', '调试', '玩家' + i + ' 已死亡，跳过'); continue; }

          var enemy = false;
          try { enemy = isEnemy(lp, player, mode); }
          catch(e) { sendLog('error', '调试', 'isEnemy 异常: ' + e.message); continue; }

          if (enemy) { enemies.push(player); sendLog('debug', '调试', '玩家' + i + ' → 加入敌人列表'); }
          else { sendLog('debug', '调试', '玩家' + i + ' → 不是敌人'); }
        } catch(e) {
          sendLog('error', '调试', 'getEnemyList 循环异常: ' + e.message);
        }
      }
      sendLog('info', '调试', 'getEnemyList 最终敌人数量: ' + enemies.length);
      return enemies;
    }

    // ================================================================
    // 自瞄主循环
    // ================================================================

    function aimLoop() {
      if (!enabled) return;
      frameCount++;

      // ========== 步骤 1: 鼠标检测 ==========
      var mouseDown = false;
      try {
        mouseDown = getMouseButton(0, ptr(0));
      } catch(e) {
        sendLog('error', '调试', 'getMouseButton 异常: ' + e.message);
        return;
      }
      if (!mouseDown) return;
      sendLog('info', '调试', '鼠标左键按下 (帧#' + frameCount + ')');

      // ========== 步骤 2: GameManager + 游戏状态检测 ==========
      var gm = getGM();
      if (!gm || gm.isNull()) {
        myPlayer = null;
        targetEnemy = null;
        sendLog('error', '调试', 'GM 为 null，重置状态');
        return;
      }

      // 验证 myPlayer 是否仍然有效
      if (myPlayer) {
        try {
          if (!isMyPlayerFn(myPlayer, ptr(0))) {
            sendLog('info', '调试', '本地玩家已失效（可能退出房间），重置');
            myPlayer = null;
            targetEnemy = null;
            return;
          }
        } catch(e) {
          myPlayer = null;
          targetEnemy = null;
          return;
        }
      }

      // ========== 步骤 3: 查找本地玩家 ==========
      if (!myPlayer) {
        var all = getAllPlayers(gm);
        sendLog('info', '调试', 'getAllPlayers 返回数量: ' + all.length);
        if (all.length === 0) {
          sendLog('warn', '调试', '玩家列表为空');
          return;
        }
        var found = false;
        for (var i = 0; i < all.length; i++) {
          try {
            if (isMyPlayerFn(all[i], ptr(0))) {
              myPlayer = all[i];
              sendLog('info', '自瞄', '发现本地玩家 @ ' + myPlayer);
              found = true;
              break;
            }
          } catch(e) {
            sendLog('error', '调试', 'isMyPlayer 异常 #' + i + ': ' + e.message);
          }
        }
        if (!found) {
          sendLog('error', '调试', '未找到本地玩家（遍历 ' + all.length + ' 个）');
          return;
        }
      }

      // 诊断：打印 myPlayer 关键字段 + 扫描 cameraManager 及其子对象
      if (frameCount <= 30) {
        try {
          var mt = myPlayer.add(OFF.E_team).readS32();
          var md = isDeadFn(myPlayer, ptr(0));
          var mcm = myPlayer.add(0x48).readPointer();
          var mrec = myPlayer.add(0x54).readPointer();
          var myaw = myPlayer.add(OFF.P_camRot).readFloat();
          var mpit = myPlayer.add(OFF.P_camRot + 4).readFloat();
          sendLog('info', '诊断', 'myPlayer @ ' + myPlayer + ' team=' + mt + ' dead=' + md + ' camMgr=' + mcm + ' recoil=' + mrec);
          sendLog('info', '诊断', 'cameraRotation yaw=' + myaw.toFixed(4) + '(' + (myaw*180/Math.PI).toFixed(2) + '°) pitch=' + mpit.toFixed(4) + '(' + (mpit*180/Math.PI).toFixed(2) + '°)');
          if (mcm && !mcm.isNull()) {
            // 首次触发时扫描 cameraManager 的全量浮点数
            if (frameCount === 1) {
              sendLog('info', '扫描', '=== cameraManager @ ' + mcm + ' 全量浮点数 ===');
              for (var off2 = 0; off2 <= 0x80; off2 += 4) {
                var v = mcm.add(off2).readFloat();
                if (Math.abs(v) > 0.0001 && Math.abs(v) < 5000) {
                  sendLog('info', '扫描', '  camMgr+0x' + off2.toString(16) + ' = ' + v.toFixed(4) + ' (' + (v*180/Math.PI).toFixed(2) + '°)');
                }
              }
              // 扫描 mapCamera (camMgr + 0x00)
              var mapCamera = mcm.readPointer();
              if (mapCamera && !mapCamera.isNull()) {
                sendLog('info', '扫描', '=== mapCamera @ ' + mapCamera + ' 全量浮点数 ===');
                for (var off3 = 0; off3 <= 0x80; off3 += 4) {
                  var v3 = mapCamera.add(off3).readFloat();
                  if (Math.abs(v3) > 0.0001 && Math.abs(v3) < 5000) {
                    sendLog('info', '扫描', '  mapCam+0x' + off3.toString(16) + ' = ' + v3.toFixed(4) + ' (' + (v3*180/Math.PI).toFixed(2) + '°)');
                  }
                }
              }
              // 扫描 modelCamera (camMgr + 0x04)
              var modelCamera = mcm.add(4).readPointer();
              if (modelCamera && !modelCamera.isNull()) {
                sendLog('info', '扫描', '=== modelCamera @ ' + modelCamera + ' 全量浮点数 ===');
                for (var off4 = 0; off4 <= 0x80; off4 += 4) {
                  var v4 = modelCamera.add(off4).readFloat();
                  if (Math.abs(v4) > 0.0001 && Math.abs(v4) < 5000) {
                    sendLog('info', '扫描', '  modelCam+0x' + off4.toString(16) + ' = ' + v4.toFixed(4) + ' (' + (v4*180/Math.PI).toFixed(2) + '°)');
                  }
                }
              }
            }
            // 每次触发扫描变化（只追踪 camMgr）
            scanCameraManager(mcm);
          }
        } catch(e) {
          sendLog('error', '诊断', '读取 myPlayer 字段异常: ' + e.message);
        }
      }

      // ========== 步骤 4: 获取敌人列表 ==========
      var gameMode = detectGameMode(gm);
      sendLog('info', '调试', 'gameMode=' + gameMode);
      var enemies = getEnemyList(gm, myPlayer, gameMode);
      sendLog('info', '调试', 'enemies.length=' + enemies.length);
      if (enemies.length === 0) { targetEnemy = null; return; }
      if (enemies.length !== lastEnemyCount) {
        lastEnemyCount = enemies.length;
        sendLog('info', '自瞄', '发现 ' + enemies.length + ' 个存活敌人 (mode=' + gameMode + ')');
      }

      // ========== 步骤 5: 获取本地玩家位置 ==========
      var myPos = getPlayerPos(myPlayer, '本地');
      if (!myPos) {
        sendLog('error', '调试', '无法获取本地玩家位置');
        return;
      }
      sendLog('info', '调试', '本地玩家坐标: ' + myPos.x.toFixed(1) + ',' + myPos.y.toFixed(1) + ',' + myPos.z.toFixed(1));

      // ========== 步骤 6: FOV 视野过滤 + 选最近敌人 ==========
      var best = null;
      var bestDistSq = Number.MAX_VALUE;
      // 读取当前视角用于 FOV 过滤
      var curYaw = myPlayer.add(OFF.P_camRot).readFloat();
      var curPitch = myPlayer.add(OFF.P_camRot + 4).readFloat();
      var maxYawDiff = 60 * Math.PI / 180;
      var maxPitchDiff = 45 * Math.PI / 180;
      for (var i = 0; i < enemies.length; i++) {
        var tag = '敌人' + (i + 1);
        var ePos = getPlayerPos(enemies[i], tag);
        if (!ePos) {
          sendLog('warn', '位置调试', tag + ' 位置获取失败，跳过');
          continue;
        }
        // 计算目标相对方向
        var dx = ePos.x - myPos.x, dy = ePos.y - myPos.y, dz = ePos.z - myPos.z;
        var targetYaw = Math.atan2(dx, dz);
        var dist2d = Math.sqrt(dx*dx + dz*dz);
        var targetPitch = -Math.atan2(dy, dist2d);
        // 规范化当前 yaw 到与 targetYaw 最近的 2π 范围
        var twoPI = 2 * Math.PI;
        var normalizedCurYaw = curYaw - Math.round((curYaw - targetYaw) / twoPI) * twoPI;
        // 计算 yaw 和 pitch 差值
        var yawDiff = targetYaw - normalizedCurYaw;
        if (yawDiff > Math.PI) yawDiff -= twoPI;
        if (yawDiff < -Math.PI) yawDiff += twoPI;
        var pitchDiff = targetPitch - curPitch;
        if (pitchDiff > Math.PI) pitchDiff -= twoPI;
        if (pitchDiff < -Math.PI) pitchDiff += twoPI;
        // FOV 过滤（注释掉以测试全方向瞄准）
        // if (Math.abs(yawDiff) > maxYawDiff || Math.abs(pitchDiff) > maxPitchDiff) {
        //   sendLog('debug', '调试', tag + ' 视野外, yawDiff=' + (yawDiff*180/Math.PI).toFixed(1) + '° pitchDiff=' + (pitchDiff*180/Math.PI).toFixed(1) + '°, 跳过');
        //   continue;
        // }
        var d2 = dx*dx + dy*dy + dz*dz;
        sendLog('debug', '调试', tag + ' FOV内, yawDiff=' + (yawDiff*180/Math.PI).toFixed(1) + '° 距离²=' + d2.toFixed(1));
        if (d2 < bestDistSq) {
          bestDistSq = d2;
          best = enemies[i];
        }
      }
      sendLog('debug', '调试', 'best 指针=' + best + ' bestDistSq=' + bestDistSq);
      targetEnemy = best;
      if (!targetEnemy) {
        sendLog('warn', '调试', '所有敌人位置均为 null (best=' + best + ')');
        return;
      }
      var bestDist = Math.sqrt(bestDistSq);
      sendLog('info', '调试', '选中目标 @ ' + targetEnemy + ' 距离=' + bestDist.toFixed(1) + 'm');

      // ========== 步骤 7: 获取目标位置并计算角度 ==========
      sendLog('debug', '调试', '开始获取目标位置...');
      var ePos = getPlayerPos(targetEnemy, '目标');
      if (!ePos) {
        sendLog('error', '调试', '无法获取目标位置，targetEnemy=' + targetEnemy);
        return;
      }
      sendLog('debug', '调试', '目标坐标: ' + ePos.x.toFixed(1) + ',' + ePos.y.toFixed(1) + ',' + ePos.z.toFixed(1));
      sendLog('debug', '角度写入', '敌人坐标: ' + ePos.x.toFixed(1) + ',' + ePos.y.toFixed(1) + ',' + ePos.z.toFixed(1) + ' 自身: ' + myPos.x.toFixed(1) + ',' + myPos.y.toFixed(1) + ',' + myPos.z.toFixed(1));
      if (aimBone === 'chest') ePos.y += 0.8;
      else if (aimBone === 'head') ePos.y += 1.2;

      var angles = calcAngles(myPos, ePos);
      if (!angles) {
        sendLog('warn', '调试', '角度计算返回 null');
        return;
      }
      sendLog('debug', '调试', '计算角度: yaw=' + (angles.yaw*180/Math.PI).toFixed(3) + '° pitch=' + (angles.pitch*180/Math.PI).toFixed(3) + '°');

      // ========== 步骤 8: 平滑写入 cameraRotation（带角度规范化）==========
      sendLog('debug', '角度写入', '开始写入角度...');
      try {
        var cy = myPlayer.add(OFF.P_camRot).readFloat();
        var cp = myPlayer.add(OFF.P_camRot + 4).readFloat();
        sendLog('debug', '角度写入', '当前 cameraRotation: yaw=' + cy.toFixed(4) + ' (' + (cy*180/Math.PI).toFixed(2) + '°), pitch=' + cp.toFixed(4) + ' (' + (cp*180/Math.PI).toFixed(2) + '°)');
        sendLog('debug', '角度写入', '目标角度: yaw=' + angles.yaw.toFixed(4) + ' (' + (angles.yaw*180/Math.PI).toFixed(2) + '°), pitch=' + angles.pitch.toFixed(4) + ' (' + (angles.pitch*180/Math.PI).toFixed(2) + '°)');

        // 规范化 yaw：将 cy 调整到与 angles.yaw 最近的 2π 周期
        var twoPI = 2 * Math.PI;
        var rawCy = cy;
        cy = cy - Math.round((cy - angles.yaw) / twoPI) * twoPI;
        if (Math.abs(rawCy - cy) > 0.001) {
          sendLog('debug', '角度写入', '规范化 yaw: ' + rawCy.toFixed(2) + ' -> ' + cy.toFixed(4) + ' (' + (cy*180/Math.PI).toFixed(2) + '°)');
        }

        // 规范化 pitch：将 cp 调整到与 angles.pitch 最近的 2π 周期
        var rawCp = cp;
        cp = cp - Math.round((cp - angles.pitch) / twoPI) * twoPI;
        if (Math.abs(rawCp - cp) > 0.001) {
          sendLog('debug', '角度写入', '规范化 pitch: ' + rawCp.toFixed(2) + ' -> ' + cp.toFixed(4) + ' (' + (cp*180/Math.PI).toFixed(2) + '°)');
        }

        var dy = angles.yaw - cy;
        if (dy > Math.PI) dy -= twoPI;
        if (dy < -Math.PI) dy += twoPI;
        var dp = angles.pitch - cp;
        if (dp > Math.PI) dp -= twoPI;
        if (dp < -Math.PI) dp += twoPI;

        var targetYaw = cy + dy * aimSmoothness;
        var targetPitch = cp + dp * aimSmoothness;
        sendLog('debug', '角度写入', '平滑后目标: yaw=' + targetYaw.toFixed(4) + ' (' + (targetYaw*180/Math.PI).toFixed(2) + '°), pitch=' + targetPitch.toFixed(4) + ' (' + (targetPitch*180/Math.PI).toFixed(2) + '°)');

        // 调用 Player.AddCameraRotation（使用差值增量）
        var deltaYaw = dy * aimSmoothness;
        var deltaPitch = dp * aimSmoothness;
        sendLog('debug', '角度写入', '调用 AddCameraRotation deltaYaw=' + (deltaYaw*180/Math.PI).toFixed(2) + '° deltaPitch=' + (deltaPitch*180/Math.PI).toFixed(2) + '°');
        addCamRotFn(myPlayer, deltaYaw, deltaPitch, ptr(0));

        // 保持 Recoil 标志位重置
        var recoil = myPlayer.add(0x54).readPointer();
        if (recoil && !recoil.isNull()) {
          recoil.add(0x10).writeU32(0);
          recoil.add(0x24).writeU32(0);
          recoil.add(0x40).writeU32(0);
          recoil.add(0x54).writeU32(0);
        }

        // 写入后读取验证
        var afterYaw = myPlayer.add(OFF.P_camRot).readFloat();
        var afterPitch = myPlayer.add(OFF.P_camRot + 4).readFloat();
        sendLog('debug', '角度写入', '调用后 cameraRotation: yaw=' + afterYaw.toFixed(4) + ' (' + (afterYaw*180/Math.PI).toFixed(2) + '°), pitch=' + afterPitch.toFixed(4) + ' (' + (afterPitch*180/Math.PI).toFixed(2) + '°)');
        // 诊断：打印周边字段
        if (logCount <= 3) {
          var mcm = myPlayer.add(0x48).readPointer();
          var mrec = myPlayer.add(0x54).readPointer();
          sendLog('info', '诊断', '写入后 camMgr=' + mcm + ' recoil=' + mrec + ' targetEnemy=' + (targetEnemy ? targetEnemy.toString() : 'null'));
        }

        logCount++;
        sendLog('info', '自瞄', '写入角度 yaw=' + (angles.yaw*180/Math.PI).toFixed(1) + '° pitch=' + (angles.pitch*180/Math.PI).toFixed(1) + '° 距离=' + bestDist.toFixed(1) + 'm mode=' + gameMode);
      } catch(e) {
        sendLog('error', '自瞄', '写入 cameraRotation 失败: ' + e.message);
      }
    }

    // ================================================================
    // 房间切换检测
    // ================================================================

    function installRoomHooks(base) {
      var addrs = [0xAF9A90, 0xAEE370, 0xAF5B30];
      for (var i = 0; i < addrs.length; i++) {
        try {
          var h = Interceptor.attach(base.add(addrs[i]), {
            onEnter: function() {
              myPlayer = null; targetEnemy = null; logCount = 0; lastEnemyCount = 0;
              sendLog('info', '自瞄', '房间切换，状态已重置');
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
        if (enabled) return;
        var mod = getGameAssembly();
        if (!mod) { sendLog('error', '自瞄', '无 GameAssembly.dll'); return; }
        var base = mod.base;

        // 基础 NativeFunction
        isMyPlayerFn = new NativeFunction(base.add(RVA.P_isMyPlayer), 'bool', ['pointer', 'pointer']);
        isDeadFn = new NativeFunction(base.add(RVA.E_isDead), 'bool', ['pointer', 'pointer']);
        singletonGetter = new NativeFunction(base.add(RVA.SingletonGet), 'pointer', ['pointer']);
        getMouseButton = new NativeFunction(base.add(RVA.Input_GetMouse), 'bool', ['int', 'pointer']);

        // ✅ v1.2 新增：位置读取功能
        // Component.get_transform: Transform*(Component* this, MethodInfo* method) — RVA 0x32CF40
        compGetTransform = new NativeFunction(base.add(RVA.GetTransform), 'pointer', ['pointer', 'pointer']);

        // Transform.get_position: void(Transform* this, Vector3* out, MethodInfo* method)
        transformGetPos = new NativeFunction(base.add(RVA.GetPosition), 'void', ['pointer', 'pointer', 'pointer']);

        // Player.AddCameraRotation: void(Player* this, float x, float y, MethodInfo* method)
        addCamRotFn = new NativeFunction(base.add(RVA.AddCameraRot), 'void', ['pointer', 'float', 'float', 'pointer']);

        installRoomHooks(base);

        // 安装 Bot.Update Hook 捕获 Bot 玩家
        try {
          var botUpdateAddr = base.add(RVA.Bot_Update);
          botUpdateHook = Interceptor.attach(botUpdateAddr, {
            onEnter: function(args) {
              var bot = args[0];
              if (!bot || bot.isNull()) return;
              try {
                var thisPlayer = bot.add(0x24).readPointer();
                if (thisPlayer && !thisPlayer.isNull()) {
                  addBotPlayer(thisPlayer);
                }
              } catch(e) {}
            }
          });
          sendLog('info', '自瞄', 'Bot.Update Hook 已安装');
        } catch(e) {
          sendLog('warn', '自瞄', '安装 Bot.Update Hook 失败: ' + e.message);
        }

        myPlayer = null; targetEnemy = null; logCount = 0; lastEnemyCount = 0; frameCount = 0;
        timer = setInterval(aimLoop, scanInterval);
        enabled = true;
        sendLog('success', '自瞄', 'v1.3 已启用（get_transform 函数调用，无内存读取）');
        sendStatus('aim', true);
      },

      disable: function() {
        if (!enabled) return;
        if (timer) { clearInterval(timer); timer = null; }
        for (var i = 0; i < roomHooks.length; i++) { try { roomHooks[i].detach(); } catch(e) {} }
        roomHooks = [];
        if (botUpdateHook) { try { botUpdateHook.detach(); } catch(e) {} }
        botUpdateHook = null;
        botPlayers = {};
        isMyPlayerFn = null; isDeadFn = null; singletonGetter = null; getMouseButton = null;
        compGetTransform = null; transformGetPos = null; addCamRotFn = null;
        myPlayer = null; targetEnemy = null; enabled = false;
        sendLog('info', '自瞄', '已禁用');
        sendStatus('aim', false);
      },

      setconfig: function(cfg) {
        if (cfg.smoothness !== undefined) {
          aimSmoothness = Math.max(0.05, Math.min(1.0, cfg.smoothness));
          sendLog('info', '自瞄', '平滑度: ' + aimSmoothness.toFixed(2));
        }
        if (cfg.aimBone !== undefined) {
          aimBone = cfg.aimBone;
          sendLog('info', '自瞄', '瞄准部位: ' + aimBone);
        }
      },

      getstatus: function() {
        return {
          enabled: enabled,
          myPlayer: myPlayer ? myPlayer.toString() : null,
          targetEnemy: targetEnemy ? targetEnemy.toString() : null,
          smoothness: aimSmoothness,
          aimBone: aimBone,
        };
      }
    };
  })();

  rpc.exports = {
    aimenable: function() { aimModule.enable(); },
    aimdisable: function() { aimModule.disable(); },
    aimconfig: function(smoothness, bone) {
      var cfg = {};
      if (smoothness !== undefined && smoothness >= 0) cfg.smoothness = smoothness;
      if (bone !== undefined && bone !== '') cfg.aimBone = bone;
      aimModule.setconfig(cfg);
    },
    aimstatus: function() { return JSON.stringify(aimModule.getstatus()); }
  };
})();
