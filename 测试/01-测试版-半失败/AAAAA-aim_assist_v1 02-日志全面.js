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
    var aimSmoothness = 0.6;
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
    var physicsLinecastFn = null;

    // 锁定目标缓存
    var lockedTarget = null;
    var lockedTargetTime = 0;

    var RVA = {
      P_isMyPlayer:   0xB55FD0,
      E_isDead:       0xB400E0,
      Input_GetMouse: 0xACFB20,
      SingletonGet:   0x4A8170,
      GM_Singleton:   0xE1CE64,
      GetTransform:   0x32CF40,
      GetPosition:    0x3F42B0,
      Bot_Update:     0xB33370,
      PhysicsLinecast: 0xABBF80,
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

    // 可见性检测：DLL 方案，不做 Linecast，FOV 内就算可见
    function isVisible(start, end) {
      return true;
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

      // 诊断：打印 myPlayer 关键字段 + 扫描归一化候选视角字段
      if (frameCount <= 60) {
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
            // 在 camMgr、mapCamera、modelCamera 中寻找归一化候选字段
            var scanTargets = [
              { ptr: mcm, name: 'camMgr' },
            ];
            var mapCam = mcm.readPointer();
            if (mapCam && !mapCam.isNull()) scanTargets.push({ ptr: mapCam, name: 'mapCam' });
            var modelCam = mcm.add(4).readPointer();
            if (modelCam && !modelCam.isNull()) scanTargets.push({ ptr: modelCam, name: 'modelCam' });
            for (var si = 0; si < scanTargets.length; si++) {
              var obj = scanTargets[si];
              for (var off2 = 0; off2 <= 0x80; off2 += 4) {
                try {
                  var v = obj.ptr.add(off2).readFloat();
                  // 候选条件：值在 -π~π 或 0~2π 范围内，且绝对值适中
                  if ((v > -3.2 && v < 3.2) || (v > 0 && v < 6.3)) {
                    if (Math.abs(v) > 0.001) {
                      sendLog('info', '候选', obj.name + '+0x' + off2.toString(16) + ' = ' + v.toFixed(4) + ' (' + (v*180/Math.PI).toFixed(2) + '°)');
                    }
                  }
                } catch(e2) {}
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
      var eyePos = { x: myPos.x, y: myPos.y + 1.5, z: myPos.z };

      // ========== 步骤 6: 角度最近 + 可见性 + 锁定目标 ==========
      var maxYawDiff = 30 * Math.PI / 180;
      var maxPitchDiff = 20 * Math.PI / 180;
      var curYawDeg = myPlayer.add(OFF.P_camRot).readFloat();
      var curPitchDeg = myPlayer.add(OFF.P_camRot + 4).readFloat();
      sendLog('info', '调试', '当前视角: yaw=' + curYawDeg.toFixed(2) + '° pitch=' + curPitchDeg.toFixed(2) + '°');

      // 先扫描所有可见敌人，打日志
      var visibleEnemies = [];
      for (var si = 0; si < enemies.length; si++) {
        var ePos_tmp = getPlayerPos(enemies[si], '扫描');
        if (!ePos_tmp) continue;
        // 立即按 aimBone 调整 Y 轴，后续所有计算和检测都用调整后的坐标
        if (aimBone === 'chest') ePos_tmp.y += 0.8;
        else if (aimBone === 'head') ePos_tmp.y += 1.2;
        var dx_tmp = ePos_tmp.x - eyePos.x, dz_tmp = ePos_tmp.z - eyePos.z;
        var yaw_tmp = Math.atan2(dx_tmp, dz_tmp);
        var dist2d_tmp = Math.sqrt(dx_tmp*dx_tmp + dz_tmp*dz_tmp);
        var pitch_tmp = Math.atan2(ePos_tmp.y - eyePos.y, dist2d_tmp);
        var cyRad_tmp = curYawDeg * Math.PI / 180;
        var cpRad_tmp = curPitchDeg * Math.PI / 180;
        var yawD_tmp = yaw_tmp - cyRad_tmp;
        if (yawD_tmp > Math.PI) yawD_tmp -= 2*Math.PI; if (yawD_tmp < -Math.PI) yawD_tmp += 2*Math.PI;
        var pitchD_tmp = pitch_tmp - cpRad_tmp;
        if (pitchD_tmp > Math.PI) pitchD_tmp -= 2*Math.PI; if (pitchD_tmp < -Math.PI) pitchD_tmp += 2*Math.PI;
        var visible = isVisible(eyePos, ePos_tmp);
        sendLog('info', '敌人', '敌人' + (si+1) + ' 坐标=[' + ePos_tmp.x.toFixed(1) + ',' + ePos_tmp.y.toFixed(1) + ',' + ePos_tmp.z.toFixed(1) + '] 屏幕角度: yaw=' + (yawD_tmp*180/Math.PI).toFixed(1) + '° pitch=' + (pitchD_tmp*180/Math.PI).toFixed(1) + '° 可见=' + (visible?'是':'否'));
        visibleEnemies.push({ptr: enemies[si], pos: ePos_tmp, yawDiff: yawD_tmp, pitchDiff: pitchD_tmp, visible: visible, angDist: Math.sqrt(yawD_tmp*yawD_tmp + pitchD_tmp*pitchD_tmp)});
      }

      // 检查锁定目标是否仍然有效
      if (lockedTarget) {
        try {
          var stillDead = isDeadFn(lockedTarget, ptr(0));
          var tPos = getPlayerPos(lockedTarget, '锁定');
          if (stillDead || !tPos) {
            sendLog('debug', '调试', '锁定目标已死亡或丢失');
            lockedTarget = null;
          } else {
            // 按 aimBone 调整 Y 轴，与瞄准点一致
            if (aimBone === 'chest') tPos.y += 0.8;
            else if (aimBone === 'head') tPos.y += 1.2;
            // 检查是否仍在 FOV 内
            var dx2 = tPos.x - eyePos.x, dy2 = tPos.y - eyePos.y, dz2 = tPos.z - eyePos.z;
            var tYaw = Math.atan2(dx2, dz2);
            var tDist2d = Math.sqrt(dx2*dx2 + dz2*dz2);
            var tPitch = Math.atan2(dy2, tDist2d);
            var cyRad = curYawDeg * Math.PI / 180;
            var cpRad = curPitchDeg * Math.PI / 180;
            var yawDif = tYaw - cyRad;
            if (yawDif > Math.PI) yawDif -= 2*Math.PI;
            if (yawDif < -Math.PI) yawDif += 2*Math.PI;
            var pitchDif = tPitch - cpRad;
            if (Math.abs(yawDif) > maxYawDiff || Math.abs(pitchDif) > maxPitchDiff) {
              sendLog('debug', '调试', '锁定目标移出视野');
              lockedTarget = null;
            }
            // 检查可见性
            if (lockedTarget && !isVisible(eyePos, tPos)) {
              sendLog('debug', '调试', '锁定目标被遮挡，解除锁定');
              lockedTarget = null;
            }
          }
        } catch(e) { lockedTarget = null; }
      }

      // 如果没有锁定目标，从可见敌人中选角度最近的
      var best = null;
      var bestAngleDeg = Number.MAX_VALUE;
      if (!lockedTarget) {
        for (var vi = 0; vi < visibleEnemies.length; vi++) {
          var ve = visibleEnemies[vi];
          // FOV 过滤
          if (Math.abs(ve.yawDiff) > maxYawDiff || Math.abs(ve.pitchDiff) > maxPitchDiff) continue;
          if (!ve.visible) continue;
          var angDeg = ve.angDist * 180 / Math.PI;
          sendLog('info', '调试', '候选: 敌人' + (vi+1) + ' 角度距离=' + angDeg.toFixed(1) + '°');
          if (angDeg < bestAngleDeg) {
            bestAngleDeg = angDeg;
            best = ve.ptr;
          }
        }
        if (best) {
          lockedTarget = best;
          sendLog('info', '调试', '锁定新目标，角度距离=' + bestAngleDeg.toFixed(1) + '°');
        }
      } else {
        best = lockedTarget;
      }

      targetEnemy = best;
      if (!targetEnemy) {
        sendLog('info', '调试', '视野内无敌人或全部不可见，不控制准星');
        return;
      }

      // ========== 步骤 7: 获取目标位置并计算角度 ==========
      var ePos = getPlayerPos(targetEnemy, '目标');
      if (!ePos) {
        sendLog('error', '调试', '无法获取目标位置');
        return;
      }
      sendLog('info', '调试', '目标坐标: [' + ePos.x.toFixed(1) + ',' + ePos.y.toFixed(1) + ',' + ePos.z.toFixed(1) + ']');
      if (aimBone === 'chest') ePos.y += 0.8;
      else if (aimBone === 'head') ePos.y += 1.2;

      var angles = calcAngles(eyePos, ePos);
      if (!angles) {
        sendLog('warn', '调试', '角度计算返回 null');
        return;
      }
      var targetYawDeg = angles.yaw * 180 / Math.PI;
      var targetPitchDeg = angles.pitch * 180 / Math.PI;
      sendLog('info', '调试', '目标角度: yaw=' + targetYawDeg.toFixed(2) + '° pitch=' + targetPitchDeg.toFixed(2) + '°');
      sendLog('info', '调试', '角度差: yaw=' + (targetYawDeg - curYawDeg).toFixed(2) + '° pitch=' + (targetPitchDeg - curPitchDeg).toFixed(2) + '°');

      // ========== 步骤 8: 平滑 + 写入度数 + 重置 Recoil ==========
      try {
        var smoothYaw = curYawDeg + (targetYawDeg - curYawDeg) * aimSmoothness;
        var smoothPitch = curPitchDeg + (targetPitchDeg - curPitchDeg) * aimSmoothness;
        sendLog('info', '调试', '平滑后写入: yaw=' + smoothYaw.toFixed(2) + '° pitch=' + smoothPitch.toFixed(2) + '°');

        myPlayer.add(OFF.P_camRot).writeFloat(smoothYaw);
        myPlayer.add(OFF.P_camRot + 4).writeFloat(smoothPitch);

        // 重置 recoil 标志位
        var recoil = myPlayer.add(0x54).readPointer();
        if (recoil && !recoil.isNull()) {
          recoil.add(0x10).writeU32(0);
          recoil.add(0x24).writeU32(0);
          recoil.add(0x40).writeU32(0);
          recoil.add(0x54).writeU32(0);
        }

        var afterYaw = myPlayer.add(OFF.P_camRot).readFloat();
        var afterPitch = myPlayer.add(OFF.P_camRot + 4).readFloat();
        sendLog('info', '调试', '写入确认: yaw=' + afterYaw.toFixed(2) + '° pitch=' + afterPitch.toFixed(2) + '°');

        logCount++;
      } catch(e) {
        sendLog('error', '自瞄', '写入失败: ' + e.message);
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
              myPlayer = null; targetEnemy = null; lockedTarget = null; logCount = 0; lastEnemyCount = 0;
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

        // Physics.Linecast: bool(Vector3 start, Vector3 end, int layerMask, MethodInfo* method)
        physicsLinecastFn = new NativeFunction(base.add(RVA.PhysicsLinecast), 'bool', ['pointer', 'pointer', 'int', 'pointer']);

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
        sendLog('success', '自瞄', '已启用（DLL 方案：绝对度数写入 + Recoil 标志位重置）');
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
          compGetTransform = null; transformGetPos = null; physicsLinecastFn = null;
          myPlayer = null; targetEnemy = null; lockedTarget = null; enabled = false;
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
