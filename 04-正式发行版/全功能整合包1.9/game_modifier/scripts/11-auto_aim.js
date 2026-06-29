// aim.js - 自瞄 v2 — 基于 UnityCrossFire.dll 逆向方案
// 双定时器(aimLoop 16ms + targetScanner 30ms) + 角度计算 + FOV过滤 + 平滑插值 + 后坐力清零

modules.aim = (function() {
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
      if (!mod) {
        sendBothLog('error', '自瞄', '自瞄暂未就绪，请重新连接游戏后重试', 'AutoAim GameAssembly.dll not found');
        return;
      }
      if (!initNativeFunctions()) {
        sendBothLog('error', '自瞄', '自瞄初始化失败，请稍后重试', 'AutoAim NativeFunction init failed');
        return;
      }
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
