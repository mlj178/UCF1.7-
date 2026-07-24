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

// aim.js - 自瞄 v2 — 基于 UnityCrossFire.dll 逆向方案
// 双定时器(aimLoop 16ms + targetScanner 30ms) + 角度计算 + FOV过滤 + 平滑插值 + 后坐力清零

modules.aim = (function() {
  var BONE = {
    HEAD: 0,
    NECK: 3,
    CHEST: 7,
    PELVIS: 10,
    LEFT_HAND: 6,
    RIGHT_HAND: 11,
    LEFT_FOOT: 14,
    RIGHT_FOOT: 15,
  };

  var HUMAN_BONE = {};
  HUMAN_BONE.HEAD = 10;
  HUMAN_BONE.NECK = 9;
  HUMAN_BONE.CHEST = 8;
  HUMAN_BONE.HIPS = 0;
  HUMAN_BONE.LEFT_HAND = 17;
  HUMAN_BONE.RIGHT_HAND = 18;
  HUMAN_BONE.LEFT_FOOT = 5;
  HUMAN_BONE.RIGHT_FOOT = 6;

  var BONE_Y_OFFSET = {};
  BONE_Y_OFFSET[BONE.HEAD] = 1.65;
  BONE_Y_OFFSET[BONE.NECK] = 1.45;
  BONE_Y_OFFSET[BONE.CHEST] = 1.05;
  BONE_Y_OFFSET[BONE.PELVIS] = 0.85;
  BONE_Y_OFFSET[BONE.LEFT_HAND] = 0.75;
  BONE_Y_OFFSET[BONE.RIGHT_HAND] = 0.75;
  BONE_Y_OFFSET[BONE.LEFT_FOOT] = 0.20;
  BONE_Y_OFFSET[BONE.RIGHT_FOOT] = 0.20;

  var enabled = false;
  var myPlayer = null;
  var targetEnemy = null;
  var timer = null;
  var roomHooks = [];
  var frameCount = 0;

  var CONFIG = {
    aimKey:          0,
    aimBone:         BONE.NECK,
    smoothness:      1.0,
    maxAimDistance:  200.0,
    maxAngleFOV:     30.0,
    localEyeHeight:  1.55,
    cameraCacheMaxAgeMs: 250,
    visibilityCheck: false,
  };

  var singletonGetter = null;
  var compGetTransform = null;
  var componentGetAnimator = null;
  var transformGetPos = null;
  var transformGetForward = null;
  var animatorGetBoneTransform = null;
  var brainGetOutputCamera = null;
  var isMyPlayerFn = null;
  var isDeadFn = null;
  var getTeamFn = null;
  var addCamRotFn = null;
  var getMouseBtnFn = null;
  var linecastFn = null;

  var aimTimer = null;
  var scanTimer = null;
  var cachedTarget = null;
  var scanYawDeg = 0;
  var scanPitchDeg = 0;
  var aimCamera = { valid: false, position: null, forward: null, transform: null, lastUpdateMs: 0 };

  var RVA_AIM = {
    SingletonGet:                    0x4A8170,
    GM_Singleton_MethodInfo:         0xE1CE64,
    Component_get_transform:         0x32CF40,
    Component_GetComponent_Animator: 0x252BD0,
    Component_GetComponent_Animator_MethodInfo: 0xE21AC4,
    Transform_get_position:          0x3F42B0,
    Transform_get_position_Injected: 0x3F4280,
    Transform_get_forward_Injected:  0x3F3F20,
    Animator_GetBoneTransform:       0xAA82B0,
    Animator_GetBoneTransform_MethodInfo: 0xE225D4,
    Brain_PushStateToUnityCamera:    0x82B750,
    Brain_get_OutputCamera:          0x82CDB0,
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
    try { componentGetAnimator = new NativeFunction(base.add(RVA_AIM.Component_GetComponent_Animator), 'pointer', ['pointer', 'pointer']); } catch(e) { componentGetAnimator = null; }
    try { transformGetPos = new NativeFunction(base.add(RVA_AIM.Transform_get_position), 'void', ['pointer', 'pointer', 'pointer']); } catch(e) { return false; }
    try { transformGetForward = new NativeFunction(base.add(RVA_AIM.Transform_get_forward_Injected), 'void', ['pointer', 'pointer', 'pointer']); } catch(e) { transformGetForward = null; }
    try { animatorGetBoneTransform = new NativeFunction(base.add(RVA_AIM.Animator_GetBoneTransform), 'pointer', ['pointer', 'int32', 'pointer']); } catch(e) { animatorGetBoneTransform = null; }
    try { brainGetOutputCamera = new NativeFunction(base.add(RVA_AIM.Brain_get_OutputCamera), 'pointer', ['pointer', 'pointer']); } catch(e) { brainGetOutputCamera = null; }
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

  function isValidPos(pos) {
    return pos &&
      Math.abs(pos.x) < 5000 &&
      Math.abs(pos.y) < 5000 &&
      Math.abs(pos.z) < 5000;
  }

  function readTransformPosition(transform) {
    if (!transform || transform.isNull()) return null;
    try {
      var posBuf = Memory.alloc(12);
      transformGetPos(posBuf, transform, ptr(0));
      var pos = {
        x: posBuf.readFloat(),
        y: posBuf.add(4).readFloat(),
        z: posBuf.add(8).readFloat(),
      };
      return isValidPos(pos) ? pos : null;
    } catch(e) {
      return null;
    }
  }

  function readTransformForward(transform) {
    if (!transform || transform.isNull() || !transformGetForward) return null;
    try {
      var forwardBuf = Memory.alloc(12);
      transformGetForward(forwardBuf, transform, ptr(0));
      var x = forwardBuf.readFloat();
      var y = forwardBuf.add(4).readFloat();
      var z = forwardBuf.add(8).readFloat();
      var len = Math.sqrt(x*x + y*y + z*z);
      if (!isFinite(len) || len < 0.00001) return null;
      return { x: x / len, y: y / len, z: z / len };
    } catch(e) {
      return null;
    }
  }

  function getPlayerPos(player) {
    if (!player || player.isNull()) return null;
    try {
      var transform = compGetTransform(player, ptr(0));
      var transformPos = readTransformPosition(transform);
      if (transformPos) return transformPos;

      var container = player.add(OFF_AIM.P_characterContainer).readPointer();
      var containerPos = readTransformPosition(container);
      if (containerPos) return containerPos;

      if (container && !container.isNull()) {
        var rawPos = {
          x: container.add(0x38).readFloat(),
          y: container.add(0x3C).readFloat(),
          z: container.add(0x40).readFloat(),
        };
        if (isValidPos(rawPos)) return rawPos;
      }
    } catch(e) {}
    return null;
  }

  function getMethodInfo(rva) {
    try {
      var mod = getGameAssembly();
      if (!mod) return ptr(0);
      var methodInfo = mod.base.add(rva).readPointer();
      return methodInfo && !methodInfo.isNull() ? methodInfo : ptr(0);
    } catch(e) {
      return ptr(0);
    }
  }

  function toHumanBodyBone(boneIndex) {
    if (boneIndex === BONE.HEAD) return HUMAN_BONE.HEAD;
    if (boneIndex === BONE.NECK) return HUMAN_BONE.NECK;
    if (boneIndex === BONE.CHEST) return HUMAN_BONE.CHEST;
    if (boneIndex === BONE.PELVIS) return HUMAN_BONE.HIPS;
    if (boneIndex === BONE.LEFT_HAND) return HUMAN_BONE.LEFT_HAND;
    if (boneIndex === BONE.RIGHT_HAND) return HUMAN_BONE.RIGHT_HAND;
    if (boneIndex === BONE.LEFT_FOOT) return HUMAN_BONE.LEFT_FOOT;
    if (boneIndex === BONE.RIGHT_FOOT) return HUMAN_BONE.RIGHT_FOOT;
    return boneIndex;
  }

  function getRealBonePos(player, boneIndex) {
    if (!player || player.isNull() || !componentGetAnimator || !animatorGetBoneTransform) return null;
    try {
      var animator = componentGetAnimator(player, getMethodInfo(RVA_AIM.Component_GetComponent_Animator_MethodInfo));
      if (!animator || animator.isNull()) return null;

      var boneTransform = animatorGetBoneTransform(animator, toHumanBodyBone(boneIndex), getMethodInfo(RVA_AIM.Animator_GetBoneTransform_MethodInfo));
      if (!boneTransform || boneTransform.isNull()) return null;

      return readTransformPosition(boneTransform);
    } catch(e) {
      return null;
    }
  }

  function getFallbackBonePos(player, boneIndex) {
    var pos = getPlayerPos(player);
    if (!pos) return null;
    var yOff = BONE_Y_OFFSET[boneIndex];
    if (yOff === undefined) yOff = BONE_Y_OFFSET[BONE.CHEST];
    pos.y += yOff;
    return pos;
  }

  function getAimPoint(player, boneIndex) {
    return getRealBonePos(player, boneIndex) || getFallbackBonePos(player, boneIndex);
  }

  function getLocalAimOrigin(player) {
    var basePos = getPlayerPos(player);
    if (!basePos) return null;
    basePos.y += CONFIG.localEyeHeight;
    return basePos;
  }

  function cacheAimCamera(brain) {
    if (!brain || brain.isNull() || !brainGetOutputCamera) return false;
    try {
      var camera = brainGetOutputCamera(brain, ptr(0));
      if (!camera || camera.isNull()) return false;
      var cameraTransform = compGetTransform(camera, ptr(0));
      if (!cameraTransform || cameraTransform.isNull()) return false;

      var pos = readTransformPosition(cameraTransform);
      if (!pos) return false;

      aimCamera.valid = true;
      aimCamera.position = pos;
      aimCamera.forward = readTransformForward(cameraTransform);
      aimCamera.transform = cameraTransform;
      aimCamera.lastUpdateMs = Date.now();
      return true;
    } catch(e) {
      aimCamera.valid = false;
      return false;
    }
  }

  function getAimOrigin(player) {
    var now = Date.now();
    if (aimCamera.valid && aimCamera.position && (now - aimCamera.lastUpdateMs) <= CONFIG.cameraCacheMaxAgeMs) {
      return { x: aimCamera.position.x, y: aimCamera.position.y, z: aimCamera.position.z, source: 'camera', forward: aimCamera.forward };
    }

    var origin = getLocalAimOrigin(player);
    if (origin) origin.source = 'player_eye';
    return origin;
  }

  function normalizeAngleDeg(value) {
    while (value > 180) value -= 360;
    while (value < -180) value += 360;
    return value;
  }

  function toStoredPitchDeg(visualPitchDeg) {
    return -visualPitchDeg;
  }

  function fromStoredPitchDeg(storedPitchDeg) {
    return -storedPitchDeg;
  }

  function readCameraRotation(player) {
    var yawDeg = player.add(OFF_AIM.P_cameraRotation).readFloat();
    var storedPitchDeg = player.add(OFF_AIM.P_cameraRotation + 4).readFloat();
    return {
      yawDeg: yawDeg,
      pitchDeg: fromStoredPitchDeg(storedPitchDeg),
      storedPitchDeg: storedPitchDeg,
    };
  }

  function writeCameraRotation(player, yawDeg, pitchDeg) {
    player.add(OFF_AIM.P_cameraRotation).writeFloat(yawDeg);
    player.add(OFF_AIM.P_cameraRotation + 4).writeFloat(toStoredPitchDeg(pitchDeg));
  }

  function calculateTargetAngles(from, to) {
    var dx = to.x - from.x;
    var dy = to.y - from.y;
    var dz = to.z - from.z;
    var hDist = Math.sqrt(dx*dx + dz*dz);
    if (hDist < 0.01) return null;
    var yaw = Math.atan2(dx, dz) * 180.0 / Math.PI;
    var pitch = Math.atan2(dy, hDist) * 180.0 / Math.PI;
    return {
      targetYawDeg: yaw,
      targetPitchDeg: pitch,
      dist: Math.sqrt(dx*dx + dy*dy + dz*dz),
      dx: dx,
      dy: dy,
      dz: dz,
      hDist: hDist,
    };
  }

  function angleDistanceDeg(targetYawDeg, targetPitchDeg, curYawDeg, curPitchDeg) {
    var yawDiff = normalizeAngleDeg(targetYawDeg - curYawDeg);
    var pitchDiff = normalizeAngleDeg(targetPitchDeg - curPitchDeg);
    return {
      yawDiff: yawDiff,
      pitchDiff: pitchDiff,
      angleDeg: Math.sqrt(yawDiff*yawDiff + pitchDiff*pitchDiff),
    };
  }

  function refreshCachedTargetAim() {
    if (!myPlayer || !cachedTarget || !cachedTarget.player) return null;
    try {
      if (cachedTarget.player.isNull()) return null;
      if (isDeadFn(cachedTarget.player, ptr(0))) return null;

      var from = getAimOrigin(myPlayer);
      var to = getAimPoint(cachedTarget.player, CONFIG.aimBone);
      if (!from || !to) return null;
      if (CONFIG.visibilityCheck && !checkVisibility(from, to)) return null;

      var angles = calculateTargetAngles(from, to);
      if (!angles || angles.dist > CONFIG.maxAimDistance) return null;

      angles.player = cachedTarget.player;
      angles.pos = to;
      angles.from = from;
      return angles;
    } catch(e) {
      return null;
    }
  }

  function getBonePos(player, boneIndex) {
    return getAimPoint(player, boneIndex);
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

    var myPos = getAimOrigin(myPlayer);
    if (!myPos) return;

    var scanRotation = readCameraRotation(myPlayer);
    scanYawDeg = scanRotation.yawDeg;
    scanPitchDeg = scanRotation.pitchDeg;

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

        var targetPos = getAimPoint(p, CONFIG.aimBone);
        if (!targetPos) continue;

        if (CONFIG.visibilityCheck) {
          if (!checkVisibility(myPos, targetPos)) continue;
        }

        var angles = calculateTargetAngles(myPos, targetPos);
        if (!angles || angles.dist > CONFIG.maxAimDistance) continue;

        var fov = angleDistanceDeg(angles.targetYawDeg, angles.targetPitchDeg, scanYawDeg, scanPitchDeg);
        var angleDeg = fov.angleDeg;

        if (angleDeg > CONFIG.maxAngleFOV) continue;

        if (angleDeg < bestAngleDeg) {
          bestAngleDeg = angleDeg;
          best = {
            player: p,
            pos: targetPos,
            from: myPos,
            targetYawDeg: angles.targetYawDeg,
            targetPitchDeg: angles.targetPitchDeg,
            yawDiff: fov.yawDiff,
            pitchDiff: fov.pitchDiff,
            angleDeg: angleDeg,
            dist: angles.dist,
          };
        }
      } catch(e) {}
    }

    cachedTarget = best;
  }

  function writeAimbot() {
    if (!enabled || !myPlayer || !cachedTarget) return;

    try {
      var currentRotation = readCameraRotation(myPlayer);
      var curYawDeg = currentRotation.yawDeg;
      var curPitchDeg = currentRotation.pitchDeg;
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

      var refreshed = refreshCachedTargetAim();
      if (!refreshed) {
        cachedTarget = null;
        return;
      }

      var targetYawDeg = refreshed.targetYawDeg;
      var targetPitchDeg = refreshed.targetPitchDeg;
      cachedTarget.targetYawDeg = targetYawDeg;
      cachedTarget.targetPitchDeg = targetPitchDeg;
      cachedTarget.pos = refreshed.pos;
      cachedTarget.from = refreshed.from;
      cachedTarget.dist = refreshed.dist;

      var finalYawDeg = targetYawDeg;
      var finalPitchDeg = targetPitchDeg;
      if (CONFIG.smoothness < 1.0 && CONFIG.smoothness > 0.0) {
        var aimDiff = angleDistanceDeg(targetYawDeg, targetPitchDeg, curYawDeg, curPitchDeg);
        var yawDiff = aimDiff.yawDiff;
        var pitchDiff = aimDiff.pitchDiff;
        finalYawDeg = curYawDeg + yawDiff * CONFIG.smoothness;
        finalPitchDeg = curPitchDeg + pitchDiff * CONFIG.smoothness;
      }

      writeCameraRotation(myPlayer, finalYawDeg, finalPitchDeg);

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

    if (!getMouseBtnFn) return;
    try {
      var btnDown = getMouseBtnFn(CONFIG.aimKey, ptr(0));
      if (!btnDown) return;
    } catch(e) { return; }

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
            aimCamera.valid = false;
            frameCount = 0;
          }
        });
        roomHooks.push(h);
      } catch(e) {}
    }

    try {
      var cameraHook = Interceptor.attach(base.add(RVA_AIM.Brain_PushStateToUnityCamera), {
        onEnter: function(args) {
          this.brain = args[0];
        },
        onLeave: function() {
          cacheAimCamera(this.brain);
        }
      });
      roomHooks.push(cameraHook);
    } catch(e) {}
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
      for (var i = 0; i < roomHooks.length; i++) { try { roomHooks[i].detach(); } catch(e) {} }
      roomHooks = [];
      myPlayer = null;
      targetEnemy = null;
      aimCamera.valid = false;
      enabled = false;
      sendLog('info', '自瞄', '已禁用');
      sendStatus('aim', false);
    },
    isEnabled: function() { return enabled; },
    setConfig: function(cfg) {},
    getConfig: function() {
      return {
        aimOriginSource: aimCamera.valid ? 'camera' : 'player_eye',
        visibilityCheck: CONFIG.visibilityCheck,
        frameCount: frameCount,
      };
    }
  };
})();


// Plugin RPC wrapper. Hook internals above are copied unchanged from the legacy script.
var __pluginFeatureId = "aim";
var __pluginModuleName = "aim";
var __pluginEnabled = false;
var __pluginConfig = {};

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
  if (typeof module.setConfig === 'function') module.setConfig(__pluginConfig);

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
    else if (module && typeof module.getConfig === 'function') stats = module.getConfig();
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

