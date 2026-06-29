// Plugin script compatibility prelude. The real hook code copied from scripts/ follows below.
if (typeof modules === 'undefined') { var modules = {}; }
if (typeof send === 'undefined') { var send = function(_) {}; }
if (typeof sendStatus === 'undefined') { var sendStatus = function(_, __) {}; }
if (typeof sendLog === 'undefined') { var sendLog = function(_, __, ___) {}; }
if (typeof sendDevLog === 'undefined') { var sendDevLog = function(_, __, ___, ____) {}; }
if (typeof sendUserLog === 'undefined') { var sendUserLog = function(_, __, ___) {}; }
if (typeof sendBothLog === 'undefined') { var sendBothLog = function(_, __, ___, ____) {}; }
if (typeof sendLogFile === 'undefined') { var sendLogFile = function(_, __, ___) {}; }
if (typeof registerCleanup === 'undefined') { var registerCleanup = function(_) { return false; }; }
if (typeof getGameAssembly === 'undefined') {
  var getGameAssembly = function() {
    try { return Process.findModuleByName('GameAssembly.dll'); } catch (_) { return null; }
  };
}

// gather.js - 聚怪 (Bot Gathering) v1.2
// 双路径扫描 + CC.disable → set_position → CC.enable

modules.gather = (function() {
  var enabled = false;
  var gm = null;
  var mm = null;
  var spawn = { x: 13.6, y: 14.1, z: 0.1 };
  var ntp = false;
  var tn = 0;
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
    ModeBase_ExitGame: 0xAEE850,
    GameManager_OnDestroy: 0xAFB6F0,
  };

  var SING = { GM: 0xE1CE64, MM: 0xE1D9E8 };

  var O = {
    GM_allPlayers: 0x1C, MM_SP_GR: 0x14, MM_SP_BL: 0x10,
    P_cameraManager: 0x48, P_charContainer: 0x58,
    P_clientData: 0x94, CD_isBot: 0x1C, CD_team: 0x18,
    Bot_thisPlayer: 0x24,
  };

  var isMy = null, isDead = null, getCC = null, cSE = null, gt = null, spi = null;
  var posBuf = null, singletonGetter = null, hooks = [];

  function clearRoomState(reason) {
    gm = null; mm = null; recentBotPlayers = {}; ntp = false;
    sendDevLog('info', 'Gather', 'Room cache cleared: ' + reason, 'GatherEnemies cleared cached room pointers');
  }

  function rp(a, o) { try { return a.add(o).readPointer(); } catch(e) { return null; } }

  function isValid(pp) {
    if (!pp || pp.isNull()) return false;
    try { var vt = pp.readPointer(); return vt && !vt.isNull(); } catch(e) { return false; }
  }

  function isHuman(pp) {
    var cd = rp(pp, O.P_clientData);
    if (cd && !cd.isNull()) {
      try { var b = cd.add(O.CD_isBot).readU8(); if (b === 1) return false; if (b === 0) return true; } catch(e) {}
    }
    if (rp(pp, O.P_cameraManager)) return true;
    return false;
  }

  function trackFromBot(botPtr) {
    var player = rp(botPtr, O.Bot_thisPlayer);
    if (player && !player.isNull() && isValid(player)) {
      recentBotPlayers[player.toString()] = { player: player, time: Date.now() };
    }
  }

  function teleportEntity(ppOrBot, isBot) {
    try {
      var tr = gt(ppOrBot, ptr(0));
      if (!tr || tr.isNull()) { if (!isBot) tr = rp(ppOrBot, O.P_charContainer); else tr = null; }
      if (!tr || tr.isNull()) return 'T=null';
      var cc = getCC(ppOrBot, ptr(0));
      if (cc && !cc.isNull()) cSE(cc, 0, ptr(0));
      spi(tr, posBuf, ptr(0));
      try {
        var np = tr.add(0x10).readPointer();
        if (np) { np.add(0x38).writeFloat(spawn.x); np.add(0x3C).writeFloat(spawn.y); np.add(0x40).writeFloat(spawn.z); }
      } catch(e) {}
      if (cc && !cc.isNull()) cSE(cc, 1, ptr(0));
      return 'OK';
    } catch(e) { return 'ERR:' + e.message; }
  }

  function getGM() {
    if (gm) return gm;
    try { var methodInfo = getGameAssembly().base.add(SING.GM).readPointer(); gm = singletonGetter(methodInfo); } catch(e) {}
    if (gm && !gm.isNull()) { sendLog('info', '聚怪', 'GM: ' + gm); return gm; }
    try { var classPtr = getGameAssembly().base.add(SING.GM).readPointer(); if (classPtr && !classPtr.isNull()) gm = classPtr.add(0xC).readPointer(); } catch(e) {}
    if (gm && !gm.isNull()) sendLog('info', '聚怪', 'GM: ' + gm);
    return gm;
  }

  function getMM() {
    if (mm) return mm;
    try { var methodInfo = getGameAssembly().base.add(SING.MM).readPointer(); mm = singletonGetter(methodInfo); } catch(e) {}
    if (mm && !mm.isNull()) sendLog('info', '聚怪', 'MM: ' + mm);
    return mm;
  }

  function executeTeleport() {
    tn++;
    sendLog('info', '聚怪', ''); sendLog('info', '聚怪', '传送 #' + tn);
    getGM(); getMM();
    if (!gm || !mm) {
      sendBothLog('warn', '聚怪', '聚怪暂未捕获房间信息，请进入房间后再试', 'GatherEnemies GM/MM not ready');
      return;
    }
    sendLog('info', '聚怪', '出生点: (' + spawn.x.toFixed(1) + ',' + spawn.y.toFixed(1) + ',' + spawn.z.toFixed(1) + ')');
    posBuf.writeFloat(spawn.x); posBuf.add(4).writeFloat(spawn.y); posBuf.add(8).writeFloat(spawn.z);

    var playersToMove = {};
    var now = Date.now();
    try {
      var ap = gm.add(O.GM_allPlayers).readPointer();
      if (ap && !ap.isNull()) {
        var t = ap.add(0xC).readU32();
        for (var i = 0; i < t; i++) { try { var pp = ap.add(0x10 + i * 8).readPointer(); if (isValid(pp)) playersToMove[pp.toString()] = pp; } catch(e) {} }
      }
    } catch(e) {}

    var botKeys = Object.keys(recentBotPlayers);
    var botAdded = 0;
    for (var bi = 0; bi < botKeys.length; bi++) {
      var entry = recentBotPlayers[botKeys[bi]];
      if (now - entry.time > 5000) continue;
      var pp = entry.player;
      try { if (pp && !pp.isNull()) { pp.readPointer(); var pk = pp.toString(); if (!playersToMove[pk]) { playersToMove[pk] = pp; botAdded++; } } } catch(e) {}
    }

    sendLog('info', '聚怪', '追踪: ' + Object.keys(playersToMove).length + ' Player + ' + botAdded + ' (Bot补充)');
    var self = 0, real = 0, dead = 0, botOk = 0, botFail = 0;
    var pKeys = Object.keys(playersToMove);
    for (var pi = 0; pi < pKeys.length; pi++) {
      var pp = playersToMove[pKeys[pi]];
      try {
        if (isMy(pp, ptr(0))) { self++; continue; }
        if (isHuman(pp)) { real++; continue; }
        if (isDead(pp, ptr(0))) { dead++; continue; }
        var r = teleportEntity(pp, false); if (r === 'OK') botOk++; else botFail++;
      } catch(e) { botFail++; }
    }

    sendLog('info', '聚怪', '自己=' + self + ' 真人=' + real + ' Bot死=' + dead + ' Bot活=' + botOk);
    if (botFail > 0) sendLog('info', '聚怪', '失败=' + botFail);
    recentBotPlayers = {};
    send(JSON.stringify({type:'done',n:tn,bots:botOk,fail:botFail}));
  }

  return {
    enable: function() {
      if (enabled) return;
      var mod = getGameAssembly();
      if (!mod) {
        sendBothLog('error', '聚怪', '聚怪暂未就绪，请重新连接游戏后重试', 'GatherEnemies GameAssembly.dll not found');
        return;
      }
      var base = mod.base;
      isMy = new NativeFunction(base.add(R.P_isMy), 'bool', ['pointer','pointer']);
      isDead = new NativeFunction(base.add(R.E_isDead), 'bool', ['pointer','pointer']);
      getCC = new NativeFunction(base.add(R.E_getCC), 'pointer', ['pointer','pointer']);
      cSE = new NativeFunction(base.add(R.C_setEn), 'void', ['pointer','int','pointer']);
      gt = new NativeFunction(base.add(R.getTrans), 'pointer', ['pointer','pointer']);
      spi = new NativeFunction(base.add(R.setPosInj), 'void', ['pointer','pointer','pointer']);
      posBuf = Memory.alloc(16);
      singletonGetter = new NativeFunction(base.add(R.SingGetInst), 'pointer', ['pointer']);
      posBuf.writeFloat(spawn.x); posBuf.add(4).writeFloat(spawn.y); posBuf.add(8).writeFloat(spawn.z);

      try { var h = Interceptor.attach(base.add(R.Bot_Update), { onEnter: function(args) { trackFromBot(args[0]); } }); hooks.push(h); } catch(e) {}
      try { var h2 = Interceptor.attach(base.add(R.GM_AddP), { onEnter: function(a) { if (!gm) { gm = a[0]; } } }); hooks.push(h2); } catch(e) {}
      try { var h3 = Interceptor.attach(base.add(R.MM_MapGun), { onEnter: function(a) { if (mm) return; mm = a[0]; } }); hooks.push(h3); } catch(e) {}
      try { var h4 = Interceptor.attach(base.add(R.P_Update), { onEnter: function(a) { if (!ntp) return; ntp = false; if (!gm || !mm) return; executeTeleport(); } }); hooks.push(h4); } catch(e) {}
      try { var h5 = Interceptor.attach(base.add(R.ModeBase_ExitGame), { onEnter: function() { clearRoomState('ModeBase.ExitGame'); } }); hooks.push(h5); } catch(e) {}
      try { var h6 = Interceptor.attach(base.add(R.GameManager_OnDestroy), { onEnter: function() { clearRoomState('GameManager.OnDestroy'); } }); hooks.push(h6); } catch(e) {}

      enabled = true;
      sendLog('success', '聚怪', '已启用 — 动态列表模式');
      sendStatus('gather', true);
    },
    disable: function() {
      if (!enabled) return;
      for (var i = 0; i < hooks.length; i++) { try { hooks[i].detach(); } catch(e) {} }
      hooks = []; gm = null; mm = null; recentBotPlayers = {}; ntp = false;
      enabled = false;
      sendLog('info', '聚怪', '已禁用');
      sendStatus('gather', false);
    },
    gather: function() {
      if (!enabled) return { ok: false, msg: '聚怪未启用' };
      getGM(); getMM();
      if (!gm || !mm) return { ok: false, msg: 'GM/MM 未就绪' };
      ntp = true;
      sendLog('info', '聚怪', '传送指令已发送');
      return { ok: true, msg: '传送指令已发送' };
    }
  };
})();


// Plugin RPC wrapper. Hook internals above are copied unchanged from the legacy script.
var __pluginFeatureId = "gather";
var __pluginModuleName = "gather";
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
  if (__pluginConfig.trigger && typeof module.gather === 'function') {
    __pluginConfig.trigger = false;
    var result = module.gather();
    send(JSON.stringify({ type: 'gather_result', data: result }));
    return result;
  }
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
