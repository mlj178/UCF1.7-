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
  var MAX_PLAYERS_PER_GATHER = 64;
  var MAX_RECENT_BOT_PLAYERS = 64;
  var GATHER_FRAME_BUDGET_MS = 12;
  var GATHER_DIAG_TAG = '[GATHER_DIAG_TEMP]';
  var GATHER_DIAG_INTERVAL_MS = 1000;

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
    P_charContainer: 0x58,
    P_clientData: 0x94, CD_isBot: 0x1C, CD_team: 0x18,
    Bot_thisPlayer: 0x24,
  };

  var isMy = null, isDead = null, getCC = null, cSE = null, gt = null, spi = null;
  var posBuf = null, singletonGetter = null, hooks = [];
  var diagnosticsTimer = null;

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
    return false;
  }

  function trackFromBot(botPtr) {
    var player = rp(botPtr, O.Bot_thisPlayer);
    if (player && !player.isNull() && isValid(player)) {
      recentBotPlayers[player.toString()] = { player: player, time: Date.now() };
    }
  }

  function gatherBudgetUsed(startTime) {
    return Date.now() - startTime >= GATHER_FRAME_BUDGET_MS;
  }

  function diagNum(value) {
    try {
      if (value === null || value === undefined || !isFinite(value)) return 'na';
      return value.toFixed(2);
    } catch (_) { return 'na'; }
  }

  function readPlayerPosition(pp) {
    try {
      var tr = gt(pp, ptr(0));
      if (!tr || tr.isNull()) tr = rp(pp, O.P_charContainer);
      if (!tr || tr.isNull()) return null;
      var np = tr.add(0x10).readPointer();
      if (!np || np.isNull()) return null;
      return {
        x: np.add(0x38).readFloat(),
        y: np.add(0x3C).readFloat(),
        z: np.add(0x40).readFloat()
      };
    } catch (_) { return null; }
  }

  function readVelocityY(pp) {
    try {
      var vd = pp.add(0x90).readPointer();
      if (!vd || vd.isNull()) return null;
      return vd.add(0x10).readFloat();
    } catch (_) { return null; }
  }

  function readGrounded(pp) {
    try { return pp.add(0x70).readU8() !== 0; } catch (_) { return null; }
  }

  function appendBotDiagnostic(result, seen, pp, source, now) {
    if (!isValid(pp)) { result.invalid++; return; }
    var key = pp.toString();
    if (seen[key]) return;
    seen[key] = true;
    var self = false, human = false, dead = false;
    try { self = !!isMy(pp, ptr(0)); } catch (_) {}
    try { human = isHuman(pp); } catch (_) {}
    try { dead = !!isDead(pp, ptr(0)); } catch (_) {}
    if (self) { result.self++; return; }
    if (human) { result.human++; return; }
    if (dead) result.dead++;
    result.bot++;
    var pos = readPlayerPosition(pp);
    var grounded = readGrounded(pp);
    var vy = readVelocityY(pp);
    var age = source === 'recent' && recentBotPlayers[key] ? (now - recentBotPlayers[key].time) : 0;
    result.samples.push(
      source + ':' + key +
      ' pos=(' + (pos ? [diagNum(pos.x), diagNum(pos.y), diagNum(pos.z)].join(',') : 'null') + ')' +
      ' grounded=' + grounded +
      ' vy=' + diagNum(vy) +
      ' dead=' + dead +
      ' ageMs=' + age
    );
  }

  function collectGatherDiagnostics() {
    var now = Date.now();
    var result = {
      gmReady: !!gm,
      mmReady: !!mm,
      ntp: !!ntp,
      teleportCount: tn,
      allPlayers: -1,
      recent: Object.keys(recentBotPlayers).length,
      self: 0,
      human: 0,
      bot: 0,
      dead: 0,
      invalid: 0,
      samples: []
    };
    var seen = {};
    try {
      if (gm) {
        var ap = gm.add(O.GM_allPlayers).readPointer();
        if (ap && !ap.isNull()) {
          var total = ap.add(0xC).readU32();
          result.allPlayers = total;
          var limit = Math.min(total, MAX_PLAYERS_PER_GATHER);
          for (var i = 0; i < limit; i++) {
            try {
              var pp = ap.add(0x10 + i * 8).readPointer();
              appendBotDiagnostic(result, seen, pp, 'allPlayers', now);
            } catch (_) { result.invalid++; }
          }
        }
      }
    } catch (_) {}

    var keys = Object.keys(recentBotPlayers);
    var limitRecent = Math.min(keys.length, MAX_RECENT_BOT_PLAYERS);
    for (var ri = 0; ri < limitRecent; ri++) {
      try {
        var entry = recentBotPlayers[keys[ri]];
        if (entry && entry.player) appendBotDiagnostic(result, seen, entry.player, 'recent', now);
      } catch (_) { result.invalid++; }
    }
    return result;
  }

  function dumpGatherDiagnostics() {
    if (!enabled) return;
    var d = collectGatherDiagnostics();
    sendLogFile(
      'debug',
      '聚怪诊断',
      GATHER_DIAG_TAG +
      ' enabled=' + enabled +
      ' gm=' + d.gmReady +
      ' mm=' + d.mmReady +
      ' ntp=' + d.ntp +
      ' teleport=' + d.teleportCount +
      ' allPlayers=' + d.allPlayers +
      ' recent=' + d.recent +
      ' bot=' + d.bot +
      ' dead=' + d.dead +
      ' human=' + d.human +
      ' self=' + d.self +
      ' invalid=' + d.invalid +
      ' samples=' + (d.samples.length ? d.samples.join(' | ') : 'none')
    );
  }

  function startGatherDiagnostics() {
    if (diagnosticsTimer) return;
    dumpGatherDiagnostics();
    diagnosticsTimer = setInterval(dumpGatherDiagnostics, GATHER_DIAG_INTERVAL_MS);
  }

  function stopGatherDiagnostics() {
    if (!diagnosticsTimer) return;
    clearInterval(diagnosticsTimer);
    diagnosticsTimer = null;
  }

  function writePosition(target) {
    posBuf.writeFloat(target.x);
    posBuf.add(4).writeFloat(target.y);
    posBuf.add(8).writeFloat(target.z);
  }

  function teleportEntity(ppOrBot, isBot) {
    try {
      var tr = gt(ppOrBot, ptr(0));
      if (!tr || tr.isNull()) { if (!isBot) tr = rp(ppOrBot, O.P_charContainer); else tr = null; }
      if (!tr || tr.isNull()) return 'T=null';
      var cc = getCC(ppOrBot, ptr(0));
      if (cc && !cc.isNull()) cSE(cc, 0, ptr(0));
      writePosition(spawn);
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
    writePosition(spawn);

    var playersToMove = {};
    var now = Date.now();
    var gatherStart = now;
    try {
      var ap = gm.add(O.GM_allPlayers).readPointer();
      if (ap && !ap.isNull()) {
        var t = ap.add(0xC).readU32();
        if (t > MAX_PLAYERS_PER_GATHER) {
          sendDevLog('warn', '聚怪', '聚怪玩家列表数量异常: ' + t + '，本次最多扫描 ' + MAX_PLAYERS_PER_GATHER, 'GatherEnemies capped oversized allPlayers count');
        }
        var scanLimit = Math.min(t, MAX_PLAYERS_PER_GATHER);
        for (var i = 0; i < scanLimit; i++) {
          if (gatherBudgetUsed(gatherStart)) {
            sendDevLog('warn', '聚怪', '聚怪本帧预算已用尽，已停止继续扫描玩家列表', 'GatherEnemies scan budget exhausted');
            break;
          }
          try { var pp = ap.add(0x10 + i * 8).readPointer(); if (isValid(pp)) playersToMove[pp.toString()] = pp; } catch(e) {}
        }
      }
    } catch(e) {}

    var botKeys = Object.keys(recentBotPlayers);
    var botAdded = 0;
    if (botKeys.length > MAX_RECENT_BOT_PLAYERS) {
      sendDevLog('warn', '聚怪', '聚怪Bot缓存数量异常: ' + botKeys.length + '，本次最多补充 ' + MAX_RECENT_BOT_PLAYERS, 'GatherEnemies capped oversized bot cache');
    }
    var botLimit = Math.min(botKeys.length, MAX_RECENT_BOT_PLAYERS);
    for (var bi = 0; bi < botLimit; bi++) {
      if (gatherBudgetUsed(gatherStart)) {
        sendDevLog('warn', '聚怪', '聚怪本帧预算已用尽，已停止继续补充Bot缓存', 'GatherEnemies bot budget exhausted');
        break;
      }
      var entry = recentBotPlayers[botKeys[bi]];
      if (now - entry.time > 5000) continue;
      var pp = entry.player;
      try { if (pp && !pp.isNull()) { pp.readPointer(); var pk = pp.toString(); if (!playersToMove[pk]) { playersToMove[pk] = pp; botAdded++; } } } catch(e) {}
    }

    sendLog('info', '聚怪', '追踪: ' + Object.keys(playersToMove).length + ' Player + ' + botAdded + ' (Bot补充)');
    var self = 0, real = 0, dead = 0, botOk = 0, botFail = 0;
    var pKeys = Object.keys(playersToMove);
    for (var pi = 0; pi < pKeys.length; pi++) {
      if (gatherBudgetUsed(gatherStart)) {
        sendDevLog('warn', '聚怪', '聚怪本帧预算已用尽，已停止继续传送Bot', 'GatherEnemies teleport budget exhausted');
        break;
      }
      var pp = playersToMove[pKeys[pi]];
      try {
        if (isMy(pp, ptr(0))) { self++; continue; }
        if (isHuman(pp)) { real++; continue; }
        if (isDead(pp, ptr(0))) { dead++; continue; }
        var r = teleportEntity(pp, false);
        if (r === 'OK') botOk++; else botFail++;
      } catch(e) { botFail++; }
    }

    sendLog('info', '聚怪', '自己=' + self + ' 真人=' + real + ' Bot死=' + dead + ' Bot活=' + botOk);
    if (botFail > 0) sendLog('info', '聚怪', '失败=' + botFail);
    recentBotPlayers = {};
    send({
      type: 'plugin_event',
      feature: 'gather',
      event: 'done',
      payload: { n: tn, bots: botOk, fail: botFail },
      audience: 'both'
    });
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
      writePosition(spawn);

      try { var h = Interceptor.attach(base.add(R.Bot_Update), { onEnter: function(args) { trackFromBot(args[0]); } }); hooks.push(h); } catch(e) {}
      try { var h2 = Interceptor.attach(base.add(R.GM_AddP), { onEnter: function(a) { if (!gm) { gm = a[0]; } } }); hooks.push(h2); } catch(e) {}
      try { var h3 = Interceptor.attach(base.add(R.MM_MapGun), { onEnter: function(a) { if (mm) return; mm = a[0]; } }); hooks.push(h3); } catch(e) {}
      try { var h4 = Interceptor.attach(base.add(R.P_Update), { onEnter: function(a) { if (!ntp) return; ntp = false; if (!gm || !mm) return; executeTeleport(); } }); hooks.push(h4); } catch(e) {}
      try { var h5 = Interceptor.attach(base.add(R.ModeBase_ExitGame), { onEnter: function() { clearRoomState('ModeBase.ExitGame'); } }); hooks.push(h5); } catch(e) {}
      try { var h6 = Interceptor.attach(base.add(R.GameManager_OnDestroy), { onEnter: function() { clearRoomState('GameManager.OnDestroy'); } }); hooks.push(h6); } catch(e) {}

      enabled = true;
      startGatherDiagnostics();
      sendLog('success', '聚怪', '已启用 — 动态列表模式');
      sendStatus('gather', true);
    },
    disable: function() {
      if (!enabled) return;
      stopGatherDiagnostics();
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
    send({
      type: 'plugin_event',
      feature: 'gather',
      event: 'result',
      payload: result,
      audience: 'both'
    });
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
  cleanup: __pluginCleanup,
  gather: function(payload) {
    return __pluginApplyConfig({ trigger: true });
  }
};

