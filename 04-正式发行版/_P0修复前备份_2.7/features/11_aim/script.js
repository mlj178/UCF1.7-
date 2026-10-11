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
// aimLoop 16ms + 相机主线程目标扫描 + 角度计算 + FOV过滤 + 平滑插值 + 后坐力清零

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
    aimBone:         BONE.CHEST,
    smoothness:      1.0,
    maxAimDistance:  200.0,
    maxAngleFOV:     60.0,
    nearestDistanceBand: 2.0,
    pitchMin:        -88.0,
    pitchMax:         88.0,
    localEyeHeight:  1.55,
    neckToHeadOffset: 0.20,
    cameraCacheMaxAgeMs: 250,
    targetScanIntervalMs: 30,
    maxCameraPlayerDistance: 4.0,
    maxBoneRootDistance: 3.0,
    visibilityOriginClearance: 0.20,
    visibilityTargetExtraDistance: 0.50,
    visibilityLayerMask: 25,
    visibilityHitBoxLayer: 3,
    selectionVisibilityLayerMask: 17,
    selectionVisibilityTargetClearance: 0.10,
    selectionVisibilityQueryTriggerInteraction: 1,
    shotVisibilityQueryTriggerInteraction: 2,
    visibilitySelfSkipEpsilon: 0.05,
    visibilityMaxSelfSkips: 4,
    chestMultipointHorizontalOffset: 0.18,
    chestMultipointVerticalOffset: 0.22,
    manualOverrideInputFloorDeg: 0.05,
    manualOverrideThresholdDeg: 3.0,
    manualOverrideAccumWindowMs: 120,
    manualOverridePauseMs: 150,
    lastWrittenAimMaxAgeMs: 100,
    targetSwitchAngleAdvantageDeg: 2.0,
    diagnosticLogIntervalMs: 1000,
    visibilityCheck: true,
  };

  var singletonGetter = null;
  var compGetTransform = null;
  var componentGetAnimator = null;
  var transformGetPos = null;
  var transformGetForward = null;
  var colliderGetBounds = null;
  var animatorGetBoneTransform = null;
  var brainGetOutputCamera = null;
  var isMyPlayerFn = null;
  var isDeadFn = null;
  var getTeamFn = null;
  var addCamRotFn = null;
  var getMouseBtnFn = null;
  var physicsGetDefaultSceneInjected = null;
  var physicsInternalRaycastInjected = null;
  var objectFindByInstanceId = null;
  var componentGetGameObject = null;
  var gameObjectGetLayer = null;
  var componentGetEntityInParent = null;
  var colliderBoundsBuffer = null;
  var PHYSICS_NATIVE_OPTIONS = { abi: 'mscdecl', scheduling: 'exclusive' };

  var aimTimer = null;
  var cachedTarget = null;
  var scanYawDeg = 0;
  var scanPitchDeg = 0;
  var lastAimDiagnosticAtMs = 0;
  var lastAimScanDiagnosticAtMs = 0;
  var lastShotDiagnosticAtMs = 0;
  var lastBoneDiagnosticAtMs = 0;
  var lastTargetScanAtMs = 0;
  var manualOverrideUntilMs = 0;
  var manualAimAccumulator = { accumulatedDeg: 0.0, lastInputAtMs: 0 };
  var lastWrittenAim = { valid: false, yawDeg: 0.0, pitchDeg: 0.0, lastWriteAtMs: 0 };
  var lastVisibilityReason = 'not_checked';
  var lastVisibilityHitLayer = -1;
  var lastVisibilityHitDistance = null;
  var lastVisibilityColliderInstanceId = 0;
  var aimCamera = { valid: false, position: null, forward: null, transform: null, lastUpdateMs: 0 };

  function resetAimState(reason) {
    cachedTarget = null;
    targetEnemy = null;
    aimCamera.valid = false;
    aimCamera.position = null;
    aimCamera.forward = null;
    aimCamera.transform = null;
    aimCamera.lastUpdateMs = 0;
    manualOverrideUntilMs = 0;
    manualAimAccumulator.accumulatedDeg = 0.0;
    manualAimAccumulator.lastInputAtMs = 0;
    lastWrittenAim.valid = false;
    lastTargetScanAtMs = 0;
    if (reason && reason.indexOf('local_') === 0) myPlayer = null;
  }

  var RVA_AIM = {
    SingletonGet:                    0x4A8170,
    GM_Singleton_MethodInfo:         0xE1CE64,
    Component_get_transform:         0x32CF40,
    Component_GetComponent_Animator: 0x252BD0,
    Component_GetComponent_Animator_MethodInfo: 0xE21AC4,
    Transform_get_position_Injected: 0x3F4280,
    Transform_get_forward_Injected:  0x3F3F20,
    Collider_get_bounds_Injected:    0xAB85E0,
    Animator_GetBoneTransform:       0xAA82B0,
    Animator_GetBoneTransform_MethodInfo: 0xE225D4,
    Brain_PushStateToUnityCamera:    0x82B750,
    Brain_get_OutputCamera:          0x82CDB0,
    Player_get_isMyPlayer:           0xB55FD0,
    Entity_get_isDead:               0xB400E0,
    Entity_get_team:                 0x1E0070,
    Player_AddCameraRotation:        0xB4F790,
    Recoil_GetShootRay:                     0xB195C0,
    Input_GetMouseButton:            0xACFB20,
    Physics_get_defaultPhysicsScene_Injected: 0xABB6F0,
    PhysicsScene_Internal_Raycast_Injected:   0xAB8C20,
    Object_FindObjectFromInstanceID:          0x4E9570,
    Component_get_gameObject:                 0x32CEB0,
    GameObject_get_layer:                     0x331FB0,
    Component_GetComponentInParent_Entity:    0x252B20,
    Component_GetComponentInParent_Entity_MethodInfo: 0xE22508,
  };

  var OFF_AIM = {
    GM_allPlayers:      0x1C,
    GM_playersBL:       0x20,
    GM_playersGR:       0x28,
    E_team:             0x20,
    P_cameraRotation:   0x4C,
    P_recoil:           0x54,
    P_characterContainer: 0x58,
    P_currentCharacter: 0x5C,
    CM_spine:           0x5C,
    CM_spine1:          0x60,
    CM_neck:            0x64,
    CM_helmet:          0x6C,
    Helmet_collider:    0x10,
    RaycastHit_ColliderInstanceId: 0x28,
    RaycastHit_Distance: 0x1C,
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
    try { transformGetPos = new NativeFunction(base.add(RVA_AIM.Transform_get_position_Injected), 'void', ['pointer', 'pointer', 'pointer']); } catch(e) { return false; }
    try { transformGetForward = new NativeFunction(base.add(RVA_AIM.Transform_get_forward_Injected), 'void', ['pointer', 'pointer', 'pointer']); } catch(e) { transformGetForward = null; }
    try { colliderGetBounds = new NativeFunction(base.add(RVA_AIM.Collider_get_bounds_Injected), 'void', ['pointer', 'pointer', 'pointer']); } catch(e) { colliderGetBounds = null; }
    try { animatorGetBoneTransform = new NativeFunction(base.add(RVA_AIM.Animator_GetBoneTransform), 'pointer', ['pointer', 'int32', 'pointer']); } catch(e) { animatorGetBoneTransform = null; }
    try { brainGetOutputCamera = new NativeFunction(base.add(RVA_AIM.Brain_get_OutputCamera), 'pointer', ['pointer', 'pointer']); } catch(e) { brainGetOutputCamera = null; }
    try { isMyPlayerFn = new NativeFunction(base.add(RVA_AIM.Player_get_isMyPlayer), 'bool', ['pointer', 'pointer']); } catch(e) { return false; }
    try { isDeadFn = new NativeFunction(base.add(RVA_AIM.Entity_get_isDead), 'bool', ['pointer', 'pointer']); } catch(e) { return false; }
    try { getTeamFn = new NativeFunction(base.add(RVA_AIM.Entity_get_team), 'int32', ['pointer', 'pointer']); } catch(e) { getTeamFn = null; }
    try { addCamRotFn = new NativeFunction(base.add(RVA_AIM.Player_AddCameraRotation), 'void', ['pointer', 'float', 'float', 'pointer']); } catch(e) { return false; }
    try { getMouseBtnFn = new NativeFunction(base.add(RVA_AIM.Input_GetMouseButton), 'bool', ['int32', 'pointer']); } catch(e) { getMouseBtnFn = null; }
    try { physicsGetDefaultSceneInjected = new NativeFunction(base.add(RVA_AIM.Physics_get_defaultPhysicsScene_Injected), 'void', ['pointer', 'pointer'], PHYSICS_NATIVE_OPTIONS); } catch(e) { physicsGetDefaultSceneInjected = null; }
    try { objectFindByInstanceId = new NativeFunction(base.add(RVA_AIM.Object_FindObjectFromInstanceID), 'pointer', ['int32', 'pointer']); } catch(e) { objectFindByInstanceId = null; }
    try { componentGetGameObject = new NativeFunction(base.add(RVA_AIM.Component_get_gameObject), 'pointer', ['pointer', 'pointer']); } catch(e) { componentGetGameObject = null; }
    try { gameObjectGetLayer = new NativeFunction(base.add(RVA_AIM.GameObject_get_layer), 'int32', ['pointer', 'pointer']); } catch(e) { gameObjectGetLayer = null; }
    try { componentGetEntityInParent = new NativeFunction(base.add(RVA_AIM.Component_GetComponentInParent_Entity), 'pointer', ['pointer', 'pointer']); } catch(e) { componentGetEntityInParent = null; }
    try {
      physicsInternalRaycastInjected = new NativeFunction(
        base.add(RVA_AIM.PhysicsScene_Internal_Raycast_Injected),
        'bool',
        ['pointer', 'pointer', 'float', 'pointer', 'int', 'int', 'pointer'],
        PHYSICS_NATIVE_OPTIONS
      );
    } catch(e) { physicsInternalRaycastInjected = null; }

    try {
      colliderBoundsBuffer = Memory.alloc(24);
    } catch(e) {
      colliderBoundsBuffer = null;
    }

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

  function distance3d(a, b) {
    if (!a || !b) return 999999.0;
    var dx = a.x - b.x;
    var dy = a.y - b.y;
    var dz = a.z - b.z;
    return Math.sqrt(dx*dx + dy*dy + dz*dz);
  }

  function clampPitchDeg(value) {
    if (!isFinite(value)) return 0.0;
    if (value < CONFIG.pitchMin) return CONFIG.pitchMin;
    if (value > CONFIG.pitchMax) return CONFIG.pitchMax;
    return value;
  }

  function readTransformPosition(transform) {
    if (!transform || transform.isNull()) return null;
    try {
      var posBuf = Memory.alloc(12);
      transformGetPos(transform, posBuf, ptr(0));
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
      if (transformPos) {
        transformPos.positionSource = 'player_transform';
        return transformPos;
      }

      var container = player.add(OFF_AIM.P_characterContainer).readPointer();
      var containerPos = readTransformPosition(container);
      if (containerPos) {
        containerPos.positionSource = 'container_transform';
        return containerPos;
      }

      if (container && !container.isNull()) {
        var rawPos = {
          x: container.add(0x38).readFloat(),
          y: container.add(0x3C).readFloat(),
          z: container.add(0x40).readFloat(),
        };
        if (isValidPos(rawPos)) {
          rawPos.positionSource = 'container_raw';
          return rawPos;
        }
      }
    } catch(e) {}
    return null;
  }

  function readColliderBoundsCenter(collider) {
    if (!collider || collider.isNull() || !colliderGetBounds || !colliderBoundsBuffer) return null;
    try {
      colliderGetBounds(collider, colliderBoundsBuffer, ptr(0));
      var pos = {
        x: colliderBoundsBuffer.readFloat(),
        y: colliderBoundsBuffer.add(4).readFloat(),
        z: colliderBoundsBuffer.add(8).readFloat(),
      };
      var ex = colliderBoundsBuffer.add(12).readFloat();
      var ey = colliderBoundsBuffer.add(16).readFloat();
      var ez = colliderBoundsBuffer.add(20).readFloat();
      if (!isValidPos(pos)) return null;
      if (!isFinite(ex) || !isFinite(ey) || !isFinite(ez)) return null;
      if (ex < 0.01 || ey < 0.01 || ez < 0.01) return null;
      if (ex > 2.0 || ey > 2.0 || ez > 2.0) return null;
      return pos;
    } catch(e) {
      return null;
    }
  }

  function getCharacterHeadPos(player) {
    if (!player || player.isNull()) return null;
    try {
      var root = getPlayerPos(player);
      if (!root) return null;

      var character = player.add(OFF_AIM.P_currentCharacter).readPointer();
      if (!character || character.isNull()) return null;

      var helmet = character.add(OFF_AIM.CM_helmet).readPointer();
      if (helmet && !helmet.isNull()) {
        var helmetCollider = helmet.add(OFF_AIM.Helmet_collider).readPointer();
        var pos = readColliderBoundsCenter(helmetCollider);
        if (pos && distance3d(root, pos) <= CONFIG.maxBoneRootDistance) {
          pos.rootSource = root.positionSource || 'unknown';
          pos.source = 'helmet_bounds';
          return pos;
        }
      }

      var neck = character.add(OFF_AIM.CM_neck).readPointer();
      var neckPos = readTransformPosition(neck);
      if (neckPos) {
        neckPos.y += CONFIG.neckToHeadOffset;
        if (distance3d(root, neckPos) <= CONFIG.maxBoneRootDistance) {
          neckPos.rootSource = root.positionSource || 'unknown';
          neckPos.source = 'character_neck';
          return neckPos;
        }
      }
    } catch(e) {}
    return null;
  }

  function getCharacterChestPos(player) {
    if (!player || player.isNull()) return null;
    try {
      var root = getPlayerPos(player);
      if (!root) return null;

      var character = player.add(OFF_AIM.P_currentCharacter).readPointer();
      if (!character || character.isNull()) return null;

      var spine1 = character.add(OFF_AIM.CM_spine1).readPointer();
      var spine1Pos = readTransformPosition(spine1);
      if (spine1Pos && distance3d(root, spine1Pos) <= CONFIG.maxBoneRootDistance) {
        spine1Pos.rootSource = root.positionSource || 'unknown';
        spine1Pos.source = 'character_spine1';
        return spine1Pos;
      }

      var spine = character.add(OFF_AIM.CM_spine).readPointer();
      var spinePos = readTransformPosition(spine);
      if (spinePos && distance3d(root, spinePos) <= CONFIG.maxBoneRootDistance) {
        spinePos.rootSource = root.positionSource || 'unknown';
        spinePos.source = 'character_spine';
        return spinePos;
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

  function emitBoneReadDiagnostic(reason, player, boneIndex, error, animatorSource) {
    var now = Date.now();
    if ((now - lastBoneDiagnosticAtMs) < CONFIG.diagnosticLogIntervalMs) return;
    lastBoneDiagnosticAtMs = now;

    var playerId = 'unknown';
    try { if (player) playerId = player.toString(); } catch (_) {}
    try {
      send({
        type: 'plugin_event',
        feature: 'aim',
        event: 'aim_debug_sample',
        payload: {
          stage: 'bone_read',
          reason: reason || 'unknown',
          animatorSource: animatorSource || 'player',
          requestedBoneIndex: boneIndex,
          humanBoneIndex: toHumanBodyBone(boneIndex),
          player: playerId,
          error: error || ''
        }
      });
    } catch (_) {}
  }

  function getRealBonePos(player, boneIndex) {
    if (!player) {
      emitBoneReadDiagnostic('invalid_player', player, boneIndex, 'player=null');
      return null;
    }
    try {
      if (player.isNull()) {
        emitBoneReadDiagnostic('invalid_player', player, boneIndex, 'player=isNull');
        return null;
      }
    } catch(e) {
      emitBoneReadDiagnostic('invalid_player', player, boneIndex, e.message || String(e));
      return null;
    }
    if (!componentGetAnimator || !animatorGetBoneTransform) {
      var nativeStatus = 'componentGetAnimator=' + !!componentGetAnimator + ',animatorGetBoneTransform=' + !!animatorGetBoneTransform;
      emitBoneReadDiagnostic('native_unavailable', player, boneIndex, nativeStatus);
      return null;
    }
    try {
      var componentMethodInfo = getMethodInfo(RVA_AIM.Component_GetComponent_Animator_MethodInfo);
      var animator = null;
      var animatorSource = 'none';
      var animatorAttempts = 'currentCharacter,player';
      var currentCharacter = null;
      var currentCharacterError = '';
      try {
        currentCharacter = player.add(OFF_AIM.P_currentCharacter).readPointer();
        if (currentCharacter && !currentCharacter.isNull()) {
          animator = componentGetAnimator(currentCharacter, componentMethodInfo);
          if (animator && !animator.isNull()) animatorSource = 'currentCharacter';
        }
      } catch(e) {
        currentCharacterError = e.message || String(e);
        animator = null;
      }

      var playerAnimatorError = '';
      if (!animator || animator.isNull()) {
        try {
          animator = componentGetAnimator(player, componentMethodInfo);
          if (animator && !animator.isNull()) animatorSource = 'player';
        } catch(e) {
          playerAnimatorError = e.message || String(e);
          animator = null;
        }
      }
      if (!animator || animator.isNull()) {
        var componentStatus =
          'componentMethodInfo=' + (componentMethodInfo && !componentMethodInfo.isNull()) +
          ',attempts=' + animatorAttempts +
          ',currentCharacter=' + !!(currentCharacter && !currentCharacter.isNull()) +
          ',currentCharacterError=' + currentCharacterError +
          ',playerError=' + playerAnimatorError;
        emitBoneReadDiagnostic('animator_missing', player, boneIndex, componentStatus, 'none');
        return null;
      }

      var boneMethodInfo = getMethodInfo(RVA_AIM.Animator_GetBoneTransform_MethodInfo);
      var boneTransform = animatorGetBoneTransform(animator, toHumanBodyBone(boneIndex), boneMethodInfo);
      if (!boneTransform || boneTransform.isNull()) {
        var boneStatus = 'boneMethodInfo=' + (boneMethodInfo && !boneMethodInfo.isNull());
        emitBoneReadDiagnostic('bone_transform_missing', player, boneIndex, boneStatus, animatorSource);
        return null;
      }

      var pos = readTransformPosition(boneTransform);
      if (!pos) {
        emitBoneReadDiagnostic('bone_position_invalid', player, boneIndex, 'readTransformPosition=null', animatorSource);
        return null;
      }
      if (!isBoneNearPlayer(player, pos)) {
        emitBoneReadDiagnostic('bone_root_check_failed', player, boneIndex, 'maxDistance=' + CONFIG.maxBoneRootDistance, animatorSource);
        return null;
      }
      pos.source = 'real_bone';
      return pos;
    } catch(e) {
      emitBoneReadDiagnostic('bone_read_exception', player, boneIndex, e.message || String(e), 'unknown');
      return null;
    }
  }

  function isBoneNearPlayer(player, bonePos) {
    var root = getPlayerPos(player);
    if (!root || !bonePos) return false;
    bonePos.rootSource = root.positionSource || 'unknown';
    return distance3d(root, bonePos) <= CONFIG.maxBoneRootDistance;
  }

  function getFallbackBonePos(player, boneIndex) {
    var pos = getPlayerPos(player);
    if (!pos) return null;
    var yOff = BONE_Y_OFFSET[boneIndex];
    if (yOff === undefined) yOff = BONE_Y_OFFSET[BONE.CHEST];
    pos.rootSource = pos.positionSource || 'unknown';
    pos.y += yOff;
    pos.source = 'fallback';
    return pos;
  }

  function getAimPoint(player, boneIndex) {
    var characterHead = boneIndex === BONE.HEAD ? getCharacterHeadPos(player) : null;
    var characterChest = boneIndex === BONE.CHEST ? getCharacterChestPos(player) : null;
    return characterHead || characterChest || getRealBonePos(player, boneIndex) || getFallbackBonePos(player, boneIndex);
  }

  function getLocalAimOrigin(player) {
    var basePos = getPlayerPos(player);
    if (!basePos) return null;
    basePos.rootSource = basePos.positionSource || 'unknown';
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
    var localEye = getLocalAimOrigin(player);
    if (!localEye) return null;

    if (
      aimCamera.valid &&
      aimCamera.position &&
      (now - aimCamera.lastUpdateMs) <= CONFIG.cameraCacheMaxAgeMs &&
      distance3d(aimCamera.position, localEye) <= CONFIG.maxCameraPlayerDistance
    ) {
      return {
        x: aimCamera.position.x,
        y: aimCamera.position.y,
        z: aimCamera.position.z,
        source: 'camera',
        rootSource: localEye.rootSource || 'unknown',
        forward: aimCamera.forward
      };
    }

    localEye.source = 'player_eye';
    return localEye;
  }

  function normalizeAngleDeg(value) {
    while (value > 180) value -= 360;
    while (value < -180) value += 360;
    return value;
  }

  function readCameraRotation(player) {
    var yawDeg = player.add(OFF_AIM.P_cameraRotation).readFloat();
    var storedPitchDeg = player.add(OFF_AIM.P_cameraRotation + 4).readFloat();
    return {
      yawDeg: yawDeg,
      pitchDeg: storedPitchDeg,
      storedPitchDeg: storedPitchDeg,
    };
  }

  function writeCameraRotation(player, yawDeg, pitchDeg) {
    player.add(OFF_AIM.P_cameraRotation).writeFloat(yawDeg);
    player.add(OFF_AIM.P_cameraRotation + 4).writeFloat(pitchDeg);
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
      rawPitchDeg: pitch,
      targetPitchDeg: clampPitchDeg(pitch),
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

  function chooseTargetCandidate(candidates, distanceBand) {
    if (!candidates || candidates.length === 0) return null;

    var minDistance = Infinity;
    for (var i = 0; i < candidates.length; i++) {
      var distance = candidates[i].selectionDistance;
      if (!isFinite(distance)) distance = candidates[i].dist;
      if (isFinite(distance) && distance < minDistance) minDistance = distance;
    }
    if (!isFinite(minDistance)) return candidates[0];

    var bandLimit = minDistance + Math.max(0.0, distanceBand || 0.0);
    var best = null;
    var bestAngle = Infinity;
    var bestDistance = Infinity;
    for (var j = 0; j < candidates.length; j++) {
      var candidate = candidates[j];
      var candidateDistance = candidate.selectionDistance;
      if (!isFinite(candidateDistance)) candidateDistance = candidate.dist;
      if (!isFinite(candidateDistance) || candidateDistance > bandLimit) continue;
      var candidateAngle = isFinite(candidate.angleDeg) ? candidate.angleDeg : Infinity;
      if (
        !best ||
        candidateAngle < bestAngle ||
        (candidateAngle === bestAngle && candidateDistance < bestDistance)
      ) {
        best = candidate;
        bestAngle = candidateAngle;
        bestDistance = candidateDistance;
      }
    }
    return best || candidates[0];
  }

  function samePlayerPointer(a, b) {
    if (!a || !b) return false;
    if (a === b) return true;
    try { return a.equals(b); } catch (_) { return false; }
  }

  function chooseTargetCandidateWithHysteresis(candidates, distanceBand, currentPlayer, angleAdvantage) {
    var best = chooseTargetCandidate(candidates, distanceBand);
    if (!best || !currentPlayer) return best;

    var current = null;
    var minDistance = Infinity;
    for (var i = 0; i < candidates.length; i++) {
      var candidate = candidates[i];
      var candidateDistance = candidate.selectionDistance;
      if (!isFinite(candidateDistance)) candidateDistance = candidate.dist;
      if (isFinite(candidateDistance) && candidateDistance < minDistance) minDistance = candidateDistance;
      if (samePlayerPointer(candidate.player, currentPlayer)) current = candidate;
    }
    if (!current || !isFinite(minDistance)) return best;

    var currentDistance = current.selectionDistance;
    if (!isFinite(currentDistance)) currentDistance = current.dist;
    var bandLimit = minDistance + Math.max(0.0, distanceBand || 0.0);
    if (!isFinite(currentDistance) || currentDistance > bandLimit) return best;
    if (samePlayerPointer(best.player, currentPlayer)) return best;

    var currentAngle = isFinite(current.angleDeg) ? current.angleDeg : Infinity;
    var bestAngle = isFinite(best.angleDeg) ? best.angleDeg : Infinity;
    return bestAngle + Math.max(0.0, angleAdvantage || 0.0) < currentAngle ? best : current;
  }

  function calculateVisibilityRayDistance(targetDistance, originClearance, targetExtraDistance) {
    if (!isFinite(targetDistance) || targetDistance <= 0.0) return 0.0;
    var startGap = Math.max(0.0, originClearance || 0.0);
    var targetExtra = Math.max(0.0, targetExtraDistance || 0.0);
    return Math.max(0.0, targetDistance - startGap + targetExtra);
  }

  function calculateSelectionRayDistance(targetDistance, originClearance, targetClearance) {
    if (!isFinite(targetDistance) || targetDistance <= 0.0) return 0.0;
    var startGap = Math.max(0.0, originClearance || 0.0);
    var endGap = Math.max(0.0, targetClearance || 0.0);
    return Math.max(0.0, targetDistance - startGap - endGap);
  }

  function buildShotDirection(origin, target) {
    if (!origin || !target) return null;
    var dx = target.x - origin.x;
    var dy = target.y - origin.y;
    var dz = target.z - origin.z;
    var length = Math.sqrt(dx*dx + dy*dy + dz*dz);
    if (!isFinite(length) || length < 0.00001) return null;
    return { x: dx / length, y: dy / length, z: dz / length };
  }

  function buildChestAimPointCandidates(basePoint, horizontalOffset, verticalOffset) {
    if (!basePoint) return [];
    var h = Math.max(0.0, horizontalOffset || 0.0);
    var v = Math.max(0.0, verticalOffset || 0.0);
    var source = basePoint.source || 'unknown';
    return [
      { x: basePoint.x,     y: basePoint.y,     z: basePoint.z,     source: source, sampleIndex: 0 },
      { x: basePoint.x,     y: basePoint.y + v, z: basePoint.z,     source: source, sampleIndex: 1 },
      { x: basePoint.x,     y: basePoint.y - v, z: basePoint.z,     source: source, sampleIndex: 2 },
      { x: basePoint.x + h, y: basePoint.y,     z: basePoint.z,     source: source, sampleIndex: 3 },
      { x: basePoint.x - h, y: basePoint.y,     z: basePoint.z,     source: source, sampleIndex: 4 },
      { x: basePoint.x,     y: basePoint.y,     z: basePoint.z + h, source: source, sampleIndex: 5 },
      { x: basePoint.x,     y: basePoint.y,     z: basePoint.z - h, source: source, sampleIndex: 6 },
      { x: basePoint.x + h, y: basePoint.y + v, z: basePoint.z,     source: source, sampleIndex: 7 },
      { x: basePoint.x - h, y: basePoint.y + v, z: basePoint.z,     source: source, sampleIndex: 8 },
    ];
  }

  function updateManualAimAccumulator(state, deltaDeg, nowMs) {
    var accumulatedDeg = state && isFinite(state.accumulatedDeg) ? state.accumulatedDeg : 0.0;
    var lastInputAtMs = state && isFinite(state.lastInputAtMs) ? state.lastInputAtMs : 0;
    if ((nowMs - lastInputAtMs) > CONFIG.manualOverrideAccumWindowMs) accumulatedDeg = 0.0;
    if (isFinite(deltaDeg) && deltaDeg >= CONFIG.manualOverrideInputFloorDeg) {
      accumulatedDeg += deltaDeg;
      lastInputAtMs = nowMs;
    }
    return {
      accumulatedDeg: accumulatedDeg,
      lastInputAtMs: lastInputAtMs,
      shouldOverride: accumulatedDeg >= CONFIG.manualOverrideThresholdDeg,
    };
  }

  function detectManualAimOverride(currentRotation, nowMs) {
    if (!lastWrittenAim.valid) return false;
    if ((nowMs - lastWrittenAim.lastWriteAtMs) > CONFIG.lastWrittenAimMaxAgeMs) {
      lastWrittenAim.valid = false;
      manualAimAccumulator.accumulatedDeg = 0.0;
      return false;
    }

    var delta = angleDistanceDeg(
      currentRotation.yawDeg,
      currentRotation.pitchDeg,
      lastWrittenAim.yawDeg,
      lastWrittenAim.pitchDeg
    ).angleDeg;
    manualAimAccumulator = updateManualAimAccumulator(manualAimAccumulator, delta, nowMs);
    if (!manualAimAccumulator.shouldOverride) return false;

    var accumulatedDeg = manualAimAccumulator.accumulatedDeg;
    manualOverrideUntilMs = nowMs + CONFIG.manualOverridePauseMs;
    manualAimAccumulator = { accumulatedDeg: 0.0, lastInputAtMs: nowMs };
    lastWrittenAim.valid = false;
    cachedTarget = null;
    emitAimScanDiagnostic({ reason: 'manual_override', error: 'accumulatedDeg=' + accumulatedDeg });
    return true;
  }

  function emitAimDiagnostic(refreshed, currentRotation, finalYawDeg, finalPitchDeg) {
    var now = Date.now();
    if ((now - lastAimDiagnosticAtMs) < CONFIG.diagnosticLogIntervalMs) return;
    lastAimDiagnosticAtMs = now;

    try {
      send({
        type: 'plugin_event',
        feature: 'aim',
        event: 'aim_debug_sample',
        payload: {
          originSource: refreshed.from.source || 'unknown',
          originRootSource: refreshed.from.rootSource || 'unknown',
          targetSource: refreshed.pos.source || 'unknown',
          targetRootSource: refreshed.pos.rootSource || 'unknown',
          from: { x: refreshed.from.x, y: refreshed.from.y, z: refreshed.from.z },
          to: { x: refreshed.pos.x, y: refreshed.pos.y, z: refreshed.pos.z },
          dy: refreshed.dy,
          horizontalDistance: refreshed.hDist,
          targetYawDeg: refreshed.targetYawDeg,
          rawPitchDeg: refreshed.rawPitchDeg,
          targetPitchDeg: refreshed.targetPitchDeg,
          currentYawDeg: currentRotation.yawDeg,
          currentPitchDeg: currentRotation.pitchDeg,
          finalYawDeg: finalYawDeg,
          finalPitchDeg: finalPitchDeg,
          writtenYawDeg: finalYawDeg,
          writtenPitchDeg: finalPitchDeg,
          selectionVisibilityMode: 'wall_only'
        }
      });
    } catch (_) {}
  }

  function emitAimScanDiagnostic(scanStats) {
    var now = Date.now();
    if ((now - lastAimScanDiagnosticAtMs) < CONFIG.diagnosticLogIntervalMs) return;
    lastAimScanDiagnosticAtMs = now;

    try {
      send({
        type: 'plugin_event',
        feature: 'aim',
        event: 'aim_debug_sample',
        payload: {
          stage: 'target_scan',
          reason: scanStats.reason || 'no_ranked_candidate',
          players: scanStats.players || 0,
          enemies: scanStats.enemies || 0,
          aimPoints: scanStats.aimPoints || 0,
          inFov: scanStats.inFov || 0,
          visible: scanStats.visible || 0,
          candidates: scanStats.candidates || 0,
          firstAngleDeg: isFinite(scanStats.firstAngleDeg) ? scanStats.firstAngleDeg : null,
          firstSelectionDistance: isFinite(scanStats.firstSelectionDistance) ? scanStats.firstSelectionDistance : null,
          visibilityRejected: scanStats.visibilityRejected || 0,
          lastVisibilityReason: scanStats.lastVisibilityReason || '',
          lastVisibilityLayer: isFinite(scanStats.lastVisibilityLayer) ? scanStats.lastVisibilityLayer : -1,
          lastVisibilityHitDistance: isFinite(scanStats.lastVisibilityHitDistance) ? scanStats.lastVisibilityHitDistance : null,
          lastVisibilityColliderInstanceId: scanStats.lastVisibilityColliderInstanceId || 0,
          targets: scanStats.targets || [],
          error: scanStats.error || '',
          visibilityCheck: CONFIG.visibilityCheck
        }
      });
    } catch (_) {}
  }

  function emitShotRayDiagnostic(status, details) {
    var now = Date.now();
    if ((now - lastShotDiagnosticAtMs) < CONFIG.diagnosticLogIntervalMs) return;
    lastShotDiagnosticAtMs = now;
    details = details || {};
    try {
      send({
        type: 'plugin_event',
        feature: 'aim',
        event: 'aim_debug_sample',
        payload: {
          stage: 'shot_ray',
          status: status || 'unknown',
          target: details.target || '',
          targetSource: details.targetSource || '',
          sampleIndex: isFinite(details.sampleIndex) ? details.sampleIndex : -1,
          origin: details.origin || null,
          targetPoint: details.targetPoint || null,
          originalDirection: details.originalDirection || null,
          writtenDirection: details.writtenDirection || null,
          hitLayer: lastVisibilityHitLayer,
          hitDistance: isFinite(lastVisibilityHitDistance) ? lastVisibilityHitDistance : null,
          colliderInstanceId: lastVisibilityColliderInstanceId,
          error: details.error || ''
        }
      });
    } catch (_) {}
  }

  function refreshCachedTargetAim() {
    if (!myPlayer || !cachedTarget || !cachedTarget.player) return null;
    try {
      if (cachedTarget.player.isNull()) return null;
      if (isDeadFn(cachedTarget.player, ptr(0))) return null;

      var from = getAimOrigin(myPlayer);
      var to = getAimPoint(cachedTarget.player, CONFIG.aimBone);
      if (!from || !to) return null;

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

  function createPhysicsScratch() {
    if (!physicsGetDefaultSceneInjected || !physicsInternalRaycastInjected) return null;
    try {
      return {
        scene: Memory.alloc(4),
        ray: Memory.alloc(24),
        hit: Memory.alloc(0x2C),
      };
    } catch(e) {
      return null;
    }
  }

  function resolveRaycastHit(physicsScratch) {
    if (
      !physicsScratch ||
      !physicsScratch.hit ||
      !objectFindByInstanceId ||
      !componentGetGameObject ||
      !gameObjectGetLayer ||
      !componentGetEntityInParent
    ) return null;
    try {
      var colliderInstanceId = physicsScratch.hit.add(OFF_AIM.RaycastHit_ColliderInstanceId).readS32();
      if (!colliderInstanceId) return null;
      var collider = objectFindByInstanceId(colliderInstanceId, ptr(0));
      if (!collider || collider.isNull()) return null;
      var gameObject = componentGetGameObject(collider, ptr(0));
      if (!gameObject || gameObject.isNull()) return null;
      var colliderLayer = gameObjectGetLayer(gameObject, ptr(0));
      var entityMethodInfo = getMethodInfo(RVA_AIM.Component_GetComponentInParent_Entity_MethodInfo);
      var entity = componentGetEntityInParent(collider, entityMethodInfo);
      var hitDistance = physicsScratch.hit.add(OFF_AIM.RaycastHit_Distance).readFloat();
      return {
        colliderInstanceId: colliderInstanceId,
        colliderLayer: colliderLayer,
        hitDistance: hitDistance,
        entity: entity && !entity.isNull() ? entity : null,
      };
    } catch(e) {
      return null;
    }
  }

  function isTargetDamageHit(hitEntityMatchesTarget, colliderLayer, hitBoxLayer) {
    return hitEntityMatchesTarget === true && colliderLayer === hitBoxLayer;
  }

  function checkSelectionLineOfSight(from, to, physicsScratch) {
    if (
      !physicsGetDefaultSceneInjected ||
      !physicsInternalRaycastInjected ||
      !physicsScratch ||
      !physicsScratch.scene ||
      !physicsScratch.ray ||
      !physicsScratch.hit
    ) {
      lastVisibilityReason = 'native_unavailable';
      return false;
    }
    try {
      lastVisibilityHitLayer = -1;
      lastVisibilityHitDistance = null;
      lastVisibilityColliderInstanceId = 0;
      var direction = buildShotDirection(from, to);
      if (!direction) {
        lastVisibilityReason = 'distance_invalid';
        return false;
      }
      var targetDistance = distance3d(from, to);
      var rayDistance = calculateSelectionRayDistance(
        targetDistance,
        CONFIG.visibilityOriginClearance,
        CONFIG.selectionVisibilityTargetClearance
      );
      if (rayDistance <= 0.0) {
        lastVisibilityReason = 'line_clear';
        return true;
      }

      physicsScratch.ray.writeFloat(from.x + direction.x * CONFIG.visibilityOriginClearance);
      physicsScratch.ray.add(4).writeFloat(from.y + direction.y * CONFIG.visibilityOriginClearance);
      physicsScratch.ray.add(8).writeFloat(from.z + direction.z * CONFIG.visibilityOriginClearance);
      physicsScratch.ray.add(12).writeFloat(direction.x);
      physicsScratch.ray.add(16).writeFloat(direction.y);
      physicsScratch.ray.add(20).writeFloat(direction.z);
      physicsGetDefaultSceneInjected(physicsScratch.scene, ptr(0));

      var haveHit = physicsInternalRaycastInjected(
        physicsScratch.scene,
        physicsScratch.ray,
        rayDistance,
        physicsScratch.hit,
        CONFIG.selectionVisibilityLayerMask,
        CONFIG.selectionVisibilityQueryTriggerInteraction,
        ptr(0)
      );
      if (!haveHit) {
        lastVisibilityReason = 'line_clear';
        return true;
      }

      var hit = resolveRaycastHit(physicsScratch);
      if (hit) {
        lastVisibilityHitLayer = hit.colliderLayer;
        lastVisibilityHitDistance = hit.hitDistance;
        lastVisibilityColliderInstanceId = hit.colliderInstanceId;
      }
      lastVisibilityReason = 'blocked_environment';
      return false;
    } catch(e) {
      lastVisibilityReason = 'visibility_exception';
      return false;
    }
  }

  function checkShotRayHitsTarget(from, to, targetPlayer, physicsScratch) {
    if (
      !physicsGetDefaultSceneInjected ||
      !physicsInternalRaycastInjected ||
      !objectFindByInstanceId ||
      !componentGetGameObject ||
      !gameObjectGetLayer ||
      !componentGetEntityInParent ||
      !physicsScratch ||
      !physicsScratch.scene ||
      !physicsScratch.ray ||
      !physicsScratch.hit
    ) {
      lastVisibilityReason = 'native_unavailable';
      return false;
    }
    if (!targetPlayer) {
      lastVisibilityReason = 'target_missing';
      return false;
    }
    try {
      lastVisibilityHitLayer = -1;
      lastVisibilityHitDistance = null;
      lastVisibilityColliderInstanceId = 0;
      var dx = to.x - from.x;
      var dy = to.y - from.y;
      var dz = to.z - from.z;
      var targetDistance = Math.sqrt(dx*dx + dy*dy + dz*dz);
      if (!isFinite(targetDistance) || targetDistance < 0.05) {
        lastVisibilityReason = 'distance_invalid';
        return false;
      }

      var rayDistance = calculateVisibilityRayDistance(
        targetDistance,
        CONFIG.visibilityOriginClearance,
        CONFIG.visibilityTargetExtraDistance
      );
      if (rayDistance <= 0.0) {
        lastVisibilityReason = 'distance_invalid';
        return false;
      }

      var dirX = dx / targetDistance;
      var dirY = dy / targetDistance;
      var dirZ = dz / targetDistance;

      physicsGetDefaultSceneInjected(physicsScratch.scene, ptr(0));
      var travelled = 0.0;
      for (var skip = 0; skip <= CONFIG.visibilityMaxSelfSkips; skip++) {
        var remainingDistance = rayDistance - travelled;
        if (remainingDistance <= 0.0) {
          lastVisibilityReason = 'self_skip_exhausted';
          return false;
        }

        var originDistance = CONFIG.visibilityOriginClearance + travelled;
        physicsScratch.ray.writeFloat(from.x + dirX * originDistance);
        physicsScratch.ray.add(4).writeFloat(from.y + dirY * originDistance);
        physicsScratch.ray.add(8).writeFloat(from.z + dirZ * originDistance);
        physicsScratch.ray.add(12).writeFloat(dirX);
        physicsScratch.ray.add(16).writeFloat(dirY);
        physicsScratch.ray.add(20).writeFloat(dirZ);

        var haveHit = physicsInternalRaycastInjected(
          physicsScratch.scene,
          physicsScratch.ray,
          remainingDistance,
          physicsScratch.hit,
          CONFIG.visibilityLayerMask,
          CONFIG.shotVisibilityQueryTriggerInteraction,
          ptr(0)
        );
        if (!haveHit) {
          lastVisibilityReason = 'no_hit';
          return false;
        }

        var hit = resolveRaycastHit(physicsScratch);
        var hitEntity = hit ? hit.entity : null;
        if (hit) {
          lastVisibilityHitLayer = hit.colliderLayer;
          lastVisibilityHitDistance = hit.hitDistance;
          lastVisibilityColliderInstanceId = hit.colliderInstanceId;
        }
        var hitMatchesTarget = !!(hitEntity && hitEntity.equals(targetPlayer));
        if (isTargetDamageHit(hitMatchesTarget, hit ? hit.colliderLayer : -1, CONFIG.visibilityHitBoxLayer)) {
          lastVisibilityReason = 'target_hit';
          return true;
        }
        if (hitMatchesTarget) {
          lastVisibilityReason = 'target_non_hitbox';
          return false;
        }
        if (hitEntity && myPlayer && hitEntity.equals(myPlayer)) {
          var selfHitDistance = hit ? hit.hitDistance : 0.0;
          if (!isFinite(selfHitDistance) || selfHitDistance < 0.0) selfHitDistance = 0.0;
          travelled += selfHitDistance + CONFIG.visibilitySelfSkipEpsilon;
          lastVisibilityReason = 'self_skipped';
          continue;
        }

        lastVisibilityReason = hitEntity ? 'blocked_entity' : 'blocked_environment';
        return false;
      }
      lastVisibilityReason = 'self_skip_limit';
      return false;
    } catch(e) {
      lastVisibilityReason = 'visibility_exception';
      return false;
    }
  }

  function findShootableChestPoint(origin, targetPlayer, basePoint, physicsScratch) {
    var points = buildChestAimPointCandidates(
      basePoint,
      CONFIG.chestMultipointHorizontalOffset,
      CONFIG.chestMultipointVerticalOffset
    );
    for (var i = 0; i < points.length; i++) {
      if (checkShotRayHitsTarget(origin, points[i], targetPlayer, physicsScratch)) return points[i];
    }
    return null;
  }

  function writeRayDirection(rayBuffer, direction) {
    if (!rayBuffer || !direction) return false;
    try {
      rayBuffer.add(12).writeFloat(direction.x);
      rayBuffer.add(16).writeFloat(direction.y);
      rayBuffer.add(20).writeFloat(direction.z);
      return true;
    } catch(e) {
      return false;
    }
  }

  function redirectShootRay(rayBuffer) {
    if (!enabled || !rayBuffer || !cachedTarget || !cachedTarget.player) {
      emitShotRayDiagnostic('no_target');
      return false;
    }
    try {
      var targetPlayer = cachedTarget.player;
      if (targetPlayer.isNull() || isDeadFn(targetPlayer, ptr(0))) {
        emitShotRayDiagnostic('target_invalid');
        return false;
      }

      var origin = {
        x: rayBuffer.readFloat(),
        y: rayBuffer.add(4).readFloat(),
        z: rayBuffer.add(8).readFloat(),
      };
      var originalDirection = {
        x: rayBuffer.add(12).readFloat(),
        y: rayBuffer.add(16).readFloat(),
        z: rayBuffer.add(20).readFloat(),
      };
      if (!isValidPos(origin)) {
        emitShotRayDiagnostic('origin_invalid', { origin: origin });
        return false;
      }

      var basePoint = getAimPoint(targetPlayer, CONFIG.aimBone);
      if (!basePoint) {
        emitShotRayDiagnostic('aim_point_missing', { origin: origin });
        return false;
      }
      var physicsScratch = createPhysicsScratch();
      if (!physicsScratch) {
        emitShotRayDiagnostic('physics_scratch_missing', { origin: origin });
        return false;
      }
      var targetPoint = findShootableChestPoint(origin, targetPlayer, basePoint, physicsScratch);
      if (!targetPoint) {
        emitShotRayDiagnostic('no_shootable_hitbox', {
          target: targetPlayer.toString(),
          targetSource: basePoint.source || 'unknown',
          origin: origin,
          originalDirection: originalDirection,
        });
        return false;
      }

      var direction = buildShotDirection(origin, targetPoint);
      if (!direction || !writeRayDirection(rayBuffer, direction)) {
        emitShotRayDiagnostic('write_failed', {
          target: targetPlayer.toString(),
          targetSource: targetPoint.source || 'unknown',
          origin: origin,
          targetPoint: targetPoint,
          originalDirection: originalDirection,
        });
        return false;
      }

      cachedTarget.pos = targetPoint;
      emitShotRayDiagnostic('redirected', {
        target: targetPlayer.toString(),
        targetSource: targetPoint.source || 'unknown',
        sampleIndex: targetPoint.sampleIndex,
        origin: origin,
        targetPoint: { x: targetPoint.x, y: targetPoint.y, z: targetPoint.z },
        originalDirection: originalDirection,
        writtenDirection: direction,
      });
      return true;
    } catch(e) {
      emitShotRayDiagnostic('exception', { error: e.message || String(e) });
      return false;
    }
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

    try { if (!isMyPlayerFn(myPlayer, ptr(0))) { resetAimState('local_invalid_scan'); return; } } catch(e) { resetAimState('local_invalid_scan'); return; }
    try { if (isDeadFn(myPlayer, ptr(0))) { resetAimState('local_dead_scan'); return; } } catch(e) { resetAimState('local_dead_scan'); return; }

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
    var candidates = [];
    var physicsScratch = CONFIG.visibilityCheck ? createPhysicsScratch() : null;
    var scanStats = {
      players: allPlayers.length,
      enemies: 0,
      aimPoints: 0,
      inFov: 0,
      visible: 0,
      visibilityRejected: 0,
      lastVisibilityReason: '',
      lastVisibilityLayer: -1,
      lastVisibilityHitDistance: null,
      lastVisibilityColliderInstanceId: 0,
      targets: [],
    };

    for (var i = 0; i < allPlayers.length; i++) {
      var p = allPlayers[i];
      var detail = null;
      try {
        if (p.equals(myPlayer)) continue;
        var team = getTeamFn ? getTeamFn(p, ptr(0)) : p.add(OFF_AIM.E_team).readS32();
        var isEnemy = (myTeam === 2) || (team === 2) || (myTeam !== team);
        if (!isEnemy) continue;
        scanStats.enemies++;
        detail = {
          player: p.toString(),
          status: 'unknown',
          team: team,
          distance: null,
          angleDeg: null,
          targetSource: '',
        };

        if (isDeadFn(p, ptr(0))) {
          detail.status = 'dead';
          scanStats.targets.push(detail);
          continue;
        }

        var targetPos = getAimPoint(p, CONFIG.aimBone);
        if (!targetPos) {
          detail.status = 'aim_point_missing';
          scanStats.targets.push(detail);
          continue;
        }
        scanStats.aimPoints++;
        detail.targetSource = targetPos.source || 'unknown';

        var angles = calculateTargetAngles(myPos, targetPos);
        if (!angles) {
          detail.status = 'angle_invalid';
          scanStats.targets.push(detail);
          continue;
        }
        detail.distance = angles.dist;
        if (angles.dist > CONFIG.maxAimDistance) {
          detail.status = 'out_distance';
          scanStats.targets.push(detail);
          continue;
        }

        var fov = angleDistanceDeg(angles.targetYawDeg, angles.targetPitchDeg, scanYawDeg, scanPitchDeg);
        var angleDeg = fov.angleDeg;
        detail.angleDeg = angleDeg;

        if (angleDeg > CONFIG.maxAngleFOV) {
          detail.status = 'out_fov';
          scanStats.targets.push(detail);
          continue;
        }
        scanStats.inFov++;
        if (CONFIG.visibilityCheck && !checkSelectionLineOfSight(myPos, targetPos, physicsScratch)) {
          scanStats.visibilityRejected++;
          scanStats.lastVisibilityReason = lastVisibilityReason;
          scanStats.lastVisibilityLayer = lastVisibilityHitLayer;
          scanStats.lastVisibilityHitDistance = lastVisibilityHitDistance;
          scanStats.lastVisibilityColliderInstanceId = lastVisibilityColliderInstanceId;
          detail.status = 'blocked_environment';
          detail.visibilityReason = lastVisibilityReason;
          scanStats.targets.push(detail);
          continue;
        }
        scanStats.visible++;
        detail.status = 'candidate';
        scanStats.targets.push(detail);

        var selectionDistance = angles.dist;
        candidates.push({
          player: p,
          pos: targetPos,
          from: myPos,
          targetYawDeg: angles.targetYawDeg,
          targetPitchDeg: angles.targetPitchDeg,
          yawDiff: fov.yawDiff,
          pitchDiff: fov.pitchDiff,
          angleDeg: angleDeg,
          dist: angles.dist,
          selectionDistance: selectionDistance,
        });
      } catch(e) {
        if (detail) {
          detail.status = 'exception';
          detail.error = e.message || String(e);
          scanStats.targets.push(detail);
        }
      }
    }

    scanStats.candidates = candidates.length;
    if (candidates.length > 0) {
      scanStats.firstAngleDeg = candidates[0].angleDeg;
      scanStats.firstSelectionDistance = candidates[0].selectionDistance;
    }
    best = chooseTargetCandidateWithHysteresis(
      candidates,
      CONFIG.nearestDistanceBand,
      cachedTarget ? cachedTarget.player : null,
      CONFIG.targetSwitchAngleAdvantageDeg
    );
    cachedTarget = best;
    scanStats.reason = best ? 'selected' : 'no_ranked_candidate';
    if (best && best.player) {
      var selectedId = best.player.toString();
      for (var k = 0; k < scanStats.targets.length; k++) {
        if (scanStats.targets[k].player === selectedId) scanStats.targets[k].status = 'selected';
      }
    }
    emitAimScanDiagnostic(scanStats);
  }

  function runTargetScannerOnMainThread() {
    if (!enabled) return;
    var nowMs = Date.now();
    if ((nowMs - lastTargetScanAtMs) < CONFIG.targetScanIntervalMs) return;
    lastTargetScanAtMs = nowMs;
    targetScanner();
  }

  function writeAimbot() {
    if (!enabled || !myPlayer || !cachedTarget) return;

    try {
      if (!isMyPlayerFn(myPlayer, ptr(0))) { resetAimState('local_invalid_write'); return; }
      if (isDeadFn(myPlayer, ptr(0))) { resetAimState('local_dead_write'); return; }

      var nowMs = Date.now();
      if (nowMs < manualOverrideUntilMs) return;
      var currentRotation = readCameraRotation(myPlayer);
      if (detectManualAimOverride(currentRotation, nowMs)) return;
      var curYawDeg = currentRotation.yawDeg;
      var curPitchDeg = currentRotation.pitchDeg;

      var refreshed = refreshCachedTargetAim();
      if (!refreshed) {
        emitAimScanDiagnostic({ reason: 'refresh_failed' });
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
      lastWrittenAim.valid = true;
      lastWrittenAim.yawDeg = finalYawDeg;
      lastWrittenAim.pitchDeg = finalPitchDeg;
      lastWrittenAim.lastWriteAtMs = nowMs;
      emitAimDiagnostic(refreshed, currentRotation, finalYawDeg, finalPitchDeg);

      var recoil = myPlayer.add(OFF_AIM.P_recoil).readPointer();
      if (recoil && !recoil.isNull()) {
        recoil.add(0x10).writeU32(0);
        recoil.add(0x24).writeU32(0);
        recoil.add(0x40).writeU32(0);
        recoil.add(0x54).writeU32(0);
      }

      frameCount++;
    } catch(e) {
      emitAimScanDiagnostic({ reason: 'write_exception', error: e.message || String(e) });
    }
  }

  function aimLoop() {
    if (!enabled) return;

    if (!getMouseBtnFn) return;
    try {
      var btnDown = getMouseBtnFn(CONFIG.aimKey, ptr(0));
      if (!btnDown) {
        lastWrittenAim.valid = false;
        manualAimAccumulator.accumulatedDeg = 0.0;
        return;
      }
    } catch(e) {
      emitAimScanDiagnostic({ reason: 'mouse_read_failed', error: e.message || String(e) });
      return;
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
            resetAimState('room_change');
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
          runTargetScannerOnMainThread();
        }
      });
      roomHooks.push(cameraHook);
    } catch(e) {}

    try {
      var shootRayHook = Interceptor.attach(base.add(RVA_AIM.Recoil_GetShootRay), {
        onEnter: function(args) {
          this.retBuffer = args[0];
          this.localShot = false;
          if (!enabled || !myPlayer) return;
          try {
            var localRecoil = myPlayer.add(OFF_AIM.P_recoil).readPointer();
            this.localShot = !!(localRecoil && !localRecoil.isNull() && localRecoil.equals(args[1]));
          } catch(e) {}
        },
        onLeave: function() {
          if (!enabled || !this.localShot) return;
          redirectShootRay(this.retBuffer);
        }
      });
      roomHooks.push(shootRayHook);
    } catch(e) {
      sendDevLog('error', '自瞄', '真实射击射线 Hook 失败', 'Recoil.GetShootRay hook failed: ' + (e.message || String(e)));
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
      enabled = true;
      sendLog('success', '自瞄', '已启用');
      sendStatus('aim', true);
    },
    disable: function() {
      if (!enabled) return;
      if (aimTimer) { clearInterval(aimTimer); aimTimer = null; }
      for (var i = 0; i < roomHooks.length; i++) { try { roomHooks[i].detach(); } catch(e) {} }
      roomHooks = [];
      myPlayer = null;
      resetAimState('disable');
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

