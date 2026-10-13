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

// 聚怪专项诊断：独立模块名 + 原始 log_file 通道，绕过每模块 10 条上限，
// 全部落到 logs/game_modifier.log，便于离线分析“多人生化下 Bot 飞天”。
var GATHER_DIAG_MODULE = '聚怪诊断';
function sendGatherDiag(message) {
  sendLogFile('debug', GATHER_DIAG_MODULE, message);
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
  var modeBase = null;
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
    P_SetPos: 0xB534C0,
    // ── 诊断用（只读/观测）RVA ──
    P_Spawn: 0xB53760,               // Player.Spawn()
    P_Respawn: 0xB527A0,             // Player.Respawn(float,float)
    P_getNanoRole: 0xB56200,         // Player.get_nanoRole()
    getPosInj: 0x3F4280,             // Transform.get_position_Injected(out Vector3, this)
    Bot_Jump: 0xB2FBC0,              // Bot.Jump(float delay)
    Bot_PathSetting: 0xB31E90,       // Bot.PathSetting()（路径起点=当前 transform 位置）
    P_OnJumpBtnDown: 0xB51780,       // Player.OnJumpBtnDown()（Bot.Update/JumpCheck 命中 grounded 分支时把 velData.y 写成 JumpPower）
    ModeNano_RespawnPlayer: 0xAF2670,// ModeBase_Nano.RespawnPlayer(Player,int,bool,bool)
    ModeNano_InfectEvent: 0xAF07A0,  // ModeBase_Nano.InfectEvent(Player ghost, Player soldier)
    GM_TypeInfo: 0xE2933C,           // GameManager TypeInfo（static_fields@0x5C）
    ModeBase_ExitGame: 0xAEE850,
    ModeBase_UpdateTimeUI: 0xAF6930,
    GameManager_GameRoundEnd: 0xAFAA40,
    GameManager_NewGameRoundStart: 0xAEBCB0,
    GameManager_OnDestroy: 0xAFB6F0,
  };

  var SING = { GM: 0xE1CE64, MM: 0xE1D9E8 };

  var O = {
    GM_allPlayers: 0x1C, MM_SP_GR: 0x14, MM_SP_BL: 0x10, MM_SP_Neutral: 0x18,
    P_charContainer: 0x58,
    P_clientData: 0x94, CD_isBot: 0x1C, CD_team: 0x18,
    Bot_thisPlayer: 0x24,
    // ── 诊断用字段偏移（dump.cs 核对）──
    Entity_team: 0x20, Entity_cc: 0x2C, Entity_isGhost: 0x30,
    P_isGrounded: 0x70, P_velData: 0x90, P_isRespawning: 0xD8, P_spawnPos: 0xBC,
    P_autonomousJump: 0x68, Bot_nextJumpTime: 0xE8, Bot_nextJumpStartNode: 0xC8, Bot_nextJumpLink: 0xCC,
    GM_staticFields: 0x5C, GM_myPlayer: 0x00, GM_gameMode: 0x04,
  };

  var isMy = null, isDead = null, getCC = null, cSE = null, gt = null, spi = null, playerSetPos = null;
  var getPosInj = null, nanoRoleFn = null, worldPosBuf = null, botPathSettingFn = null;
  var posBuf = null, singletonGetter = null, hooks = [];
  var diagnosticsTimer = null;

  // ═══════════════ 聚怪专项诊断：定位“多人生化模式聚怪后 Bot 飞天” ═══════════════
  // 只读观测，全部跑在游戏主线程（Player.Update / ModeBase.UpdateTimeUI 钩子内），不新增定时器线程。
  // 一次抓齐 6 组证据，用来区分 4 类候选根因：
  //   ① 硬编码出生点在该模式/地图不成立     —— 对照 MapManager 真实 SP_BL/SP_GR/SP_Neutral
  //   ② 世界坐标 vs 原始偏移(local)坐标分叉 —— get_position(官方世界) vs native+0x38/3C/40(现有那套)
  //   ③ Bot 的 A*/NanoGuard/JumpLink 旧路径把它往高处带 —— Bot.path 字段 + Bot.Jump 计数
  //   ④ 游戏自身在聚怪后重新置位           —— Player.SetPos / Spawn / Respawn / ModeBase_Nano.RespawnPlayer / InfectEvent
  var diag = {
    traceBudget: 16, setPosBudget: 20, jumpBudget: 12, lifeBudget: 20, headerBudget: 12, jumpProbeBudget: 20,
    summaryBudget: 40, alertBudget: 30, watchLimit: 40, resetLogBudget: 30, guardBudget: 30,
    sampleIntervalMs: 250, sampleWindowMs: 3000, samplesPerBot: 8,
    watched: {}, watchKeys: [], watchActive: false, watchCount: 0,
    observeUntil: 0, selfSetPos: false, periodicBudget: 0,
    stats: { gathers: 0, traced: 0, watched: 0, gameSetPos: 0, jumps: 0, spawnCalls: 0, respawnCalls: 0, infectCalls: 0, alerts: 0, pathResets: 0, pathGuards: 0, holdResets: 0, holdDrops: 0, gameJumps: 0 }
  };

  function ptrText(p) {
    try { return (p && !p.isNull()) ? p.toString() : 'null'; } catch (e) { return 'badptr'; }
  }

  function fmtVec(v) {
    if (!v) return 'null';
    return '(' + diagNum(v.x) + ',' + diagNum(v.y) + ',' + diagNum(v.z) + ')';
  }

  // 官方世界坐标（Transform.get_position 0x3F4280，sret 缓冲在第一个参数）。
  function readWorldPosition(tr) {
    try {
      if (!tr || tr.isNull() || !getPosInj) return null;
      getPosInj(tr, worldPosBuf, ptr(0));
      return { x: worldPosBuf.readFloat(), y: worldPosBuf.add(4).readFloat(), z: worldPosBuf.add(8).readFloat() };
    } catch (e) { return null; }
  }

  // 现有代码读取/回退写入用的那套：native transform(+0x10) 的 +0x38/0x3C/0x40。
  function readRawNativePosition(tr) {
    try {
      if (!tr || tr.isNull()) return null;
      var np = tr.add(0x10).readPointer();
      if (!np || np.isNull()) return null;
      return { x: np.add(0x38).readFloat(), y: np.add(0x3C).readFloat(), z: np.add(0x40).readFloat() };
    } catch (e) { return null; }
  }

  function readPlayerTransform(pp) {
    try {
      var tr = gt(pp, ptr(0));
      if (!tr || tr.isNull()) tr = rp(pp, O.P_charContainer);
      return (tr && !tr.isNull()) ? tr : null;
    } catch (e) { return null; }
  }

  function readPlayerSpawnPos(pp) {
    try { return { x: readF32(pp.add(O.P_spawnPos)), y: readF32(pp.add(O.P_spawnPos + 4)), z: readF32(pp.add(O.P_spawnPos + 8)) }; } catch (e) { return null; }
  }

  function readNanoRole(pp) {
    try { return nanoRoleFn ? nanoRoleFn(pp, ptr(0)) : null; } catch (e) { return null; }
  }

  function isHumanRole(role) {
    if (role === null || role === undefined) return 'na';
    return (role === 0 || (role >= 18 && role <= 27)) ? 1 : 0;
  }

  function readSnapshot(pp) {
    var s = { world: null, raw: null, grounded: null, vy: null, cc: null, ghost: null, team: null, role: null, spawn: null, respawning: null };
    try { var tr = readPlayerTransform(pp); s.world = readWorldPosition(tr); s.raw = readRawNativePosition(tr); } catch (e) {}
    try { s.grounded = readGrounded(pp); } catch (e) {}
    try { s.vy = readVelocityY(pp); } catch (e) {}
    try { var cc = getCC(pp, ptr(0)); s.cc = (cc && !cc.isNull()) ? cc.toString() : null; } catch (e) {}
    try { s.ghost = readU8(pp.add(O.Entity_isGhost)); } catch (e) {}
    try { s.team = readI32(pp.add(O.Entity_team)); } catch (e) {}
    try { s.role = readNanoRole(pp); } catch (e) {}
    try { s.spawn = readPlayerSpawnPos(pp); } catch (e) {}
    try { s.respawning = readU8(pp.add(O.P_isRespawning)); } catch (e) {}
    return s;
  }

  function snapText(s) {
    if (!s) return 'null';
    return 'world=' + fmtVec(s.world) + ' raw=' + fmtVec(s.raw) + ' spawnPos=' + fmtVec(s.spawn) +
      ' role=' + s.role + '(human=' + isHumanRole(s.role) + ') ghost=' + s.ghost + ' team=' + s.team +
      ' grounded=' + s.grounded + ' vy=' + diagNum(s.vy) + ' resp=' + s.respawning + ' cc=' + (s.cc || 'null');
  }

  function botPathText(botPtr) {
    try {
      if (!botPtr || botPtr.isNull() || !isValid(botPtr)) return 'null';
      return 'pathLen=' + diagNum(readF32(botPtr.add(0x84))) +
        ' nextPathPos=(' + diagNum(readF32(botPtr.add(0xA0))) + ',' + diagNum(readF32(botPtr.add(0xA4))) + ',' + diagNum(readF32(botPtr.add(0xA8))) + ')' +
        ' nextJumpTime=' + diagNum(readF32(botPtr.add(0xE8))) +
        ' blockedTime=' + diagNum(readF32(botPtr.add(0xEC))) +
        ' gNodeNear=' + ptrText(rp(botPtr, 0x88)) + ' gNodeNext=' + ptrText(rp(botPtr, 0x8C));
    } catch (e) { return 'ERR'; }
  }

  // 多人生化专属：Bot.nanoGuard(0xC4) → 守卫/逃脱状态 + 守卫点坐标（幽灵 Bot 的寻路目标）。
  function botGuardText(botPtr) {
    try {
      if (!botPtr || botPtr.isNull() || !isValid(botPtr)) return 'null';
      var ng = rp(botPtr, 0xC4);
      if (!ng || ng.isNull()) return 'null';
      var area = rp(ng, 0x10), pos = rp(ng, 0x14);
      var posWorld = null, areaEntrance = null;
      try { if (pos && !pos.isNull()) posWorld = readWorldPosition(readPlayerTransform(pos)); } catch (e) {}
      try {
        if (area && !area.isNull()) {
          var ep = rp(area, 0xC);
          if (ep && !ep.isNull() && ep.add(0xC).readU32() > 0) {
            areaEntrance = { x: ep.add(0x10).readFloat(), y: ep.add(0x14).readFloat(), z: ep.add(0x18).readFloat() };
          }
        }
      } catch (e) {}
      return 'ng=' + ptrText(ng) + ' arriveArea=' + readU8(ng.add(0xC)) + ' arrivePos=' + readU8(ng.add(0xD)) +
        ' escaping=' + readU8(ng.add(0x1C)) +
        ' escapePos=(' + diagNum(readF32(ng.add(0x20))) + ',' + diagNum(readF32(ng.add(0x24))) + ',' + diagNum(readF32(ng.add(0x28))) + ')' +
        ' guardPos=' + ptrText(pos) + ' guardPosWorld=' + fmtVec(posWorld) + ' areaEntrance0=' + fmtVec(areaEntrance);
    } catch (e) { return 'ERR'; }
  }

  // SpawnPoint[]：array.length@0xC，data@0x10，元素 16 字节 = Vector3 position + float rotation。
  function readSpawnArray(arrayPtr, maxCount) {
    var res = { len: 0, pts: [] };
    try {
      if (!arrayPtr || arrayPtr.isNull()) return res;
      res.len = arrayPtr.add(0xC).readU32();
      var n = Math.min(res.len, maxCount);
      for (var i = 0; i < n; i++) {
        var e = arrayPtr.add(0x10 + i * 0x10);
        res.pts.push({ x: e.readFloat(), y: e.add(4).readFloat(), z: e.add(8).readFloat() });
      }
    } catch (e) {}
    return res;
  }

  function spawnArrayText(arr) {
    if (!arr) return 'null';
    if (!arr.pts.length) return 'empty(n=' + arr.len + ')';
    var t = [];
    for (var i = 0; i < arr.pts.length; i++) t.push(fmtVec(arr.pts[i]));
    return 'n=' + arr.len + ' ' + t.join('');
  }

  function readGameMode() {
    try {
      var klass = getGameAssembly().base.add(R.GM_TypeInfo).readPointer();
      if (!klass || klass.isNull()) return null;
      var sf = klass.add(O.GM_staticFields).readPointer();
      if (!sf || sf.isNull()) return null;
      return readI32(sf.add(O.GM_gameMode));
    } catch (e) { return null; }
  }

  function dumpGatherHeader(reason) {
    if (diag.headerBudget <= 0) return;
    diag.headerBudget--;
    var spBl = null, spGr = null, spNu = null;
    try {
      if (mm && !mm.isNull()) {
        spBl = readSpawnArray(rp(mm, O.MM_SP_BL), 3);
        spGr = readSpawnArray(rp(mm, O.MM_SP_GR), 3);
        spNu = readSpawnArray(rp(mm, O.MM_SP_Neutral), 3);
      }
    } catch (e) {}
    sendLogFile('debug', GATHER_DIAG_MODULE,
      'GATHER_DIAG ' + reason + ' mode=' + readGameMode() + ' hardcodedSpawn=' + fmtVec(spawn) +
      ' gm=' + ptrText(gm) + ' mm=' + ptrText(mm) +
      ' SP_BL[' + spawnArrayText(spBl) + '] SP_GR[' + spawnArrayText(spGr) + '] SP_Neutral[' + spawnArrayText(spNu) + ']');
  }

  function traceTeleport(index, pp, src, result, before, after, botPtr) {
    diag.stats.traced++;
    sendLogFile('debug', GATHER_DIAG_MODULE,
      'TRACE #' + index + ' src=' + src + ' result=' + result + ' p=' + ptrText(pp) + ' bot=' + ptrText(botPtr) +
      ' | before ' + snapText(before) + ' | after ' + snapText(after) + ' | botPath ' + botPathText(botPtr) + ' | botGuard ' + botGuardText(botPtr));
  }

  function registerWatch(pp, src, before, after, botPtr) {
    try {
      var key = pp.toString();
      if (diag.watched[key] || diag.watchCount >= diag.watchLimit) return;
      diag.watchCount++;
      var y0 = (after && after.world) ? after.world.y : ((before && before.world) ? before.world.y : null);
      diag.watched[key] = {
        key: key, player: pp, bot: botPtr, src: src, idx: diag.watchCount,
        t0: Date.now(), nextAt: Date.now() + diag.sampleIntervalMs,
        y0: y0, maxDy: 0, samples: [], first: after || before
      };
      diag.watchKeys.push(key);
      diag.watchActive = true;
      diag.stats.watched++;
    } catch (e) {}
  }

  function emitWatchSummary(rec) {
    if (diag.summaryBudget <= 0) return;
    diag.summaryBudget--;
    var tl = [];
    for (var i = 0; i < rec.samples.length; i++) {
      var s = rec.samples[i].s;
      var w = s && s.world;
      tl.push(rec.samples[i].t + 'ms:y=' + (w ? diagNum(w.y) : 'na') + '/vy=' + (s ? diagNum(s.vy) : 'na') + '/g=' + (s ? s.grounded : 'na'));
    }
    var last = rec.samples.length ? rec.samples[rec.samples.length - 1].s : null;
    sendLogFile('debug', GATHER_DIAG_MODULE,
      'WATCH #' + rec.idx + ' src=' + rec.src + ' p=' + ptrText(rec.player) + ' role=' + (rec.first ? rec.first.role : 'na') +
      ' ghost=' + (rec.first ? rec.first.ghost : 'na') + ' y0=' + diagNum(rec.y0) + ' maxDy=' + diagNum(rec.maxDy) +
      ' lastWorld=' + fmtVec(last ? last.world : null) + ' lastRaw=' + fmtVec(last ? last.raw : null) +
      ' timeline=' + (tl.length ? tl.join(' ') : 'none'));
  }

  function pumpWatchQueue() {
    if (!diag.watchActive) return;
    var now = Date.now();
    var keep = [];
    for (var i = 0; i < diag.watchKeys.length; i++) {
      var key = diag.watchKeys[i];
      var rec = diag.watched[key];
      if (!rec) continue;
      if ((now - rec.t0 >= diag.sampleWindowMs) || (rec.samples.length >= diag.samplesPerBot)) {
        emitWatchSummary(rec);
        delete diag.watched[key];
        continue;
      }
      if (now >= rec.nextAt) {
        rec.nextAt = now + diag.sampleIntervalMs;
        var snap = readSnapshot(rec.player);
        rec.samples.push({ t: now - rec.t0, s: snap });
        if (snap && snap.world && rec.y0 !== null) {
          var dy = snap.world.y - rec.y0;
          if (dy > rec.maxDy) rec.maxDy = dy;
          // 看门狗：还在升空且已离地 -> 再复位一次寻路（只读以外的动作与传送后那次完全相同，幂等）
          if (dy > 2.5 && snap.grounded === false && diag.guardBudget > 0) {
            diag.guardBudget--;
            diag.stats.pathGuards++;
            sendLogFile('debug', GATHER_DIAG_MODULE,
              'PATH_GUARD #' + rec.idx + ' dy=' + diagNum(dy) + ' grounded=' + snap.grounded +
              ' y=' + diagNum(snap.world.y) + ' -> ' + resetBotPathAfterTeleport(rec.player, rec.bot));
          }
          if (dy > 3 && diag.alertBudget > 0) {
            diag.alertBudget--; diag.stats.alerts++;
            sendLogFile('debug', GATHER_DIAG_MODULE,
              'ALERT #' + rec.idx + ' dy=' + diagNum(dy) + ' grounded=' + snap.grounded + ' vy=' + diagNum(snap.vy) +
              ' role=' + snap.role + ' ghost=' + snap.ghost + ' resp=' + snap.respawning +
              ' world=' + fmtVec(snap.world) + ' raw=' + fmtVec(snap.raw) + ' p=' + ptrText(rec.player) +
              ' | botPath ' + botPathText(rec.bot) + ' | botGuard ' + botGuardText(rec.bot));
          }
        }
      }
      keep.push(key);
    }
    diag.watchKeys = keep;
    if (!keep.length) diag.watchActive = false;
  }

  function resetDiagWindows() {
    diag.traceBudget = 16; diag.setPosBudget = 20; diag.jumpBudget = 12; diag.lifeBudget = 20; diag.jumpProbeBudget = 20;
    diag.summaryBudget = 40; diag.alertBudget = 30; diag.resetLogBudget = 30; diag.guardBudget = 30;
    diag.watched = {}; diag.watchKeys = []; diag.watchActive = false; diag.watchCount = 0;
    diag.observeUntil = Date.now() + 5000;
    diag.periodicBudget = 40;
  }

  function diagObserving() {
    return enabled && Date.now() <= diag.observeUntil;
  }

  function diagLifeEnter(a) {
    try {
      if (!diagObserving() || diag.lifeBudget <= 0) return;
      var p = a[0];
      if (!p || p.isNull() || !isValid(p)) return;
      this.diagPlayer = p;
      this.diagTr = readPlayerTransform(p);
      this.diagBefore = readWorldPosition(this.diagTr);
    } catch (e) {}
  }

  function diagLifeLeave(tag) {
    try {
      var p = this.diagPlayer;
      if (!diagObserving() || !p || diag.lifeBudget <= 0) return;
      diag.lifeBudget--;
      if (tag === 'GAME_SPAWN') diag.stats.spawnCalls++; else diag.stats.respawnCalls++;
      sendLogFile('debug', GATHER_DIAG_MODULE, tag + ' p=' + ptrText(p) +
        ' before=' + fmtVec(this.diagBefore) + ' after=' + fmtVec(this.diagTr ? readWorldPosition(this.diagTr) : null) +
        ' spawnPos=' + fmtVec(readPlayerSpawnPos(p)) + ' role=' + readNanoRole(p) +
        ' ghost=' + readU8(p.add(O.Entity_isGhost)) + ' resp=' + readU8(p.add(O.P_isRespawning)));
    } catch (e) {}
  }

  function diagNanoRespawnEnter(a) {
    try {
      if (!diagObserving() || diag.lifeBudget <= 0) return;
      var p = a[1];
      if (!p || p.isNull() || !isValid(p)) return;
      this.diagPlayer = p;
      this.diagTr = readPlayerTransform(p);
      this.diagBefore = readWorldPosition(this.diagTr);
      this.diagExtra = readI32(ptr(this.context.esp).add(12));
    } catch (e) {}
  }

  function diagNanoRespawnLeave() {
    try {
      var p = this.diagPlayer;
      if (!diagObserving() || !p || diag.lifeBudget <= 0) return;
      diag.lifeBudget--; diag.stats.respawnCalls++;
      sendLogFile('debug', GATHER_DIAG_MODULE, 'NANO_RESPAWN p=' + ptrText(p) + ' respawnTime=' + this.diagExtra +
        ' before=' + fmtVec(this.diagBefore) + ' after=' + fmtVec(this.diagTr ? readWorldPosition(this.diagTr) : null) +
        ' spawnPos=' + fmtVec(readPlayerSpawnPos(p)) + ' role=' + readNanoRole(p));
    } catch (e) {}
  }

  function diagInfectEnter(a) {
    try {
      if (!diagObserving() || diag.lifeBudget <= 0) return;
      diag.lifeBudget--; diag.stats.infectCalls++;
      var ghost = a[1], soldier = a[2];
      var gTr = (ghost && !ghost.isNull()) ? readPlayerTransform(ghost) : null;
      var sTr = (soldier && !soldier.isNull()) ? readPlayerTransform(soldier) : null;
      sendLogFile('debug', GATHER_DIAG_MODULE, 'NANO_INFECT ghost=' + ptrText(ghost) +
        ' ghostRole=' + ((ghost && !ghost.isNull()) ? readNanoRole(ghost) : 'na') + ' ghostPos=' + fmtVec(gTr ? readWorldPosition(gTr) : null) +
        ' soldier=' + ptrText(soldier) + ' soldierPos=' + fmtVec(sTr ? readWorldPosition(sTr) : null));
    } catch (e) {}
  }

  function clearRoomState(reason) {
    gm = null; mm = null; modeBase = null; recentBotPlayers = {}; ntp = false;
    clearHold();
    resetDiagWindows();
    diag.watchActive = false; diag.watched = {}; diag.watchKeys = []; diag.observeUntil = 0;
    sendDevLog('info', 'Gather', 'Room cache cleared: ' + reason, 'GatherEnemies cleared cached room pointers');
  }

  function handleModeBaseSeen(modeBasePtr) {
    try {
      if (!modeBasePtr || modeBasePtr.isNull()) return;
      if (!modeBase || modeBase.isNull()) {
        modeBase = modeBasePtr;
        return;
      }
      if (!modeBasePtr.equals(modeBase)) {
        clearRoomState('mode_base_changed');
        modeBase = modeBasePtr;
      }
    } catch(e) {}
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
      recentBotPlayers[player.toString()] = { player: player, bot: botPtr, time: Date.now() };
    }
  }

  function gatherBudgetUsed(startTime) {
    return Date.now() - startTime >= GATHER_FRAME_BUDGET_MS;
  }

  function diagNum(value) {
    try {
      if (value === Infinity) return 'inf';       // Bot.nextJumpTime 的正常"空闲"态就是 +Inf
      if (value === -Infinity) return '-inf';
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
              var pp = ap.add(0x10 + i * Process.pointerSize).readPointer();
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
    // 限流：每秒一条的周期诊断最多打 periodicBudget 条，避免长时间挂机把日志刷满、
    // 把一次聚怪前后的 TRACE/WATCH 冲掉；每次聚怪会重置预算（每轮 40 条 ≈ 40 秒）。
    if (diag.periodicBudget <= 0) return;
    diag.periodicBudget--;
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

  var diagPending = false;
  function startGatherDiagnostics() {
    if (diagnosticsTimer) return;
    // P0：诊断内部有 Component.get_transform 等游戏原生调用，不能跑在 Frida JS 线程；
    // 定时器只置标志，真正执行放到主线程钩子（ModeBase.UpdateTimeUI）里。
    dumpGatherDiagnostics();
    diagnosticsTimer = setInterval(function () { diagPending = true; }, GATHER_DIAG_INTERVAL_MS);
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

  // ═════════ 跳跃状态复位：治「跳一下就永远往上飞」 ═════════
  // 依据（capstone 反汇编 0x10B33370 Bot.Update / 0x10B2F300 Bot.JumpCheck → 0x10B51780 Player.OnJumpBtnDown）：
  //   · Bot.Update 与 Bot.JumpCheck 在 Time.time >= Bot.nextJumpTime(+0xE8) 时直接调用 Player.OnJumpBtnDown()，
  //     调用完把 nextJumpTime 写成 +Inf(0x7F800000) —— +Inf 才是「跳跃计时器空闲」的正常态，
  //     所以把 +0xE8 写成 0 等于「立刻可跳」，是被传送的 Bot 反复起跳的直接原因。
  //   · Player.OnJumpBtnDown 命中 isGrounded(+0x70) 为真的分支时（0x10B5197E 起）：
  //     velData(+0x90 → +0x10) = Player.JumpPower（常量 0x41280000 = 10.5f），并把 autonomousJump(+0x68) 置 1。
  //   · 这个竖直速度对 Bot 不会被重力衰减（Bot 不走 PlayerController.Update 那套），
  //     于是「vy 恒为 10.50、y 线性升高、grounded=false」——正是日志里看到的飞天签名。
  var TIME_INF_BITS = 0x7f800000;

  // ① 把跳跃计时器写回 +Inf（绝不能写 0）；② 清掉残余竖直速度；③ 清掉 autonomousJump。
  function killJumpState(playerPtr, botPtr) {
    var vel = 0, disarm = 0, auton = 0;
    try {
      var vd = rp(playerPtr, O.P_velData);
      if (vd && !vd.isNull()) { vd.add(0x10).writeFloat(0); vel = 1; }
    } catch (e) {}
    try {
      if (readU8(playerPtr.add(O.P_autonomousJump))) { playerPtr.add(O.P_autonomousJump).writeU8(0); auton = 1; }
    } catch (e) {}
    try {
      if (botPtr && !botPtr.isNull() && isValid(botPtr)) { botPtr.add(O.Bot_nextJumpTime).writeU32(TIME_INF_BITS); disarm = 1; }
    } catch (e) {}
    return 'vel=' + vel + ',disarm=' + disarm + ',auton=' + auton;
  }

  // ═════════ 聚怪保持窗口（飞天兜底，与根因无关也能压住）═════════
  // 聚怪后数秒内，被传送的 Bot 只要又高过堆点：① 再杀一次竖直速度/跳跃闸门；② 仍然明显偏高时，
  // 用游戏自己的 Player.SetPos 把它压回堆点高度（只改 y，x/z 用当前值，不动阵营/感染/落点分配）。
  var hold = {
    active: false, until: 0, tickAt: 0, bots: {}, target: null,
    windowMs: 6000, tickMs: 100, softDy: 1.5, hardDy: 3.0, dropCooldownMs: 250,
    logBudget: 24, dropBudget: 60, drops: 0, resets: 0
  };

  function beginGatherHold() {
    hold.active = true;
    hold.until = Date.now() + hold.windowMs;
    hold.tickAt = 0;
    hold.logBudget = 24;
    hold.dropBudget = 60;
    hold.drops = 0;
    hold.resets = 0;
    hold.target = spawn;
    // 保证本轮聚怪期间 OnJumpBtnDown 探针处于观测窗口（probes 受 diagObserving() 门控）
    diag.observeUntil = Date.now() + 8000;
    diag.jumpProbeBudget = 20;
  }

  function clearHold() {
    hold.active = false; hold.bots = {}; hold.target = null; hold.until = 0; hold.tickAt = 0;
  }

  function registerHold(pp, botPtr) {
    try {
      if (!pp || pp.isNull() || !isValid(pp)) return;
      var key = pp.toString();
      var rec = hold.bots[key];
      if (!rec) { rec = { player: pp, bot: botPtr || null, logged: 0, lastDropAt: 0, drops: 0 }; hold.bots[key] = rec; }
      else if (botPtr && !botPtr.isNull()) rec.bot = botPtr;
      hold.active = true;
    } catch (e) {}
  }

  function pumpHold() {
    if (!hold.active) return;
    var now = Date.now();
    if (now > hold.until) {
      sendLogFile('debug', GATHER_DIAG_MODULE, 'HOLD_END drops=' + hold.drops + ' resets=' + hold.resets + ' watched=' + Object.keys(hold.bots).length);
      clearHold();
      return;
    }
    if (now < hold.tickAt) return;
    hold.tickAt = now + hold.tickMs;
    var ty = hold.target ? hold.target.y : spawn.y;
    var keys = Object.keys(hold.bots);
    for (var i = 0; i < keys.length; i++) {
      var key = keys[i];
      var rec = hold.bots[key];
      if (!rec || !rec.player) { delete hold.bots[key]; continue; }
      var pp = rec.player;
      try {
        if (!isValid(pp)) { delete hold.bots[key]; continue; }
        if (isDead(pp, ptr(0))) continue;
        var world = readWorldPosition(readPlayerTransform(pp));
        if (!world) continue;
        var dy = world.y - ty;
        if (dy <= hold.softDy) continue;
        var st = killJumpState(pp, rec.bot);
        hold.resets++; diag.stats.holdResets++;
        if (hold.logBudget > 0) {
          hold.logBudget--;
          sendLogFile('debug', GATHER_DIAG_MODULE, 'HOLD key=' + key + ' p=' + ptrText(pp) + ' dy=' + diagNum(dy) +
            ' y=' + diagNum(world.y) + ' vy=' + diagNum(readVelocityY(pp)) + ' grounded=' + readGrounded(pp) + ' ' + st +
            ' | botPath ' + botPathText(rec.bot));
        }
        if (dy > hold.hardDy && now - rec.lastDropAt >= hold.dropCooldownMs && hold.dropBudget > 0) {
          hold.dropBudget--; hold.drops++; rec.drops++; rec.lastDropAt = now; diag.stats.holdDrops++;
          var r = teleportPlayerBySetPos(pp, { x: world.x, y: ty, z: world.z });
          if (hold.logBudget > 0) {
            hold.logBudget--;
            sendLogFile('debug', GATHER_DIAG_MODULE, 'HOLD_DOWN p=' + ptrText(pp) + ' dy=' + diagNum(dy) + ' y=' + diagNum(world.y) + ' -> ' + r + ' drops=' + rec.drops);
          }
        }
      } catch (e) {}
    }
  }

  // ═════════ 寻路复位：治「传送后被 A* 旧路径拖着飞/越飞越高」 ═════════
  // 依据（IDA 0x10B2FBE0 Bot.Move / 0x10B31E90 Bot.PathSetting / 0x10B31950 Bot.OnPathComplete / dump.cs）：
  //   · Bot.Move 沿 path(+0x80)->vectorPath[nextPathVectorID(+0x90)] 取 nextPathPos(+0xA0)，朝它直线移动；
  //     这条 path 是按"传送前"的位置算出来的，传送后 Bot 会沿旧航点直线穿空跑过去 —— 观察到的"恒定 vy、匀速升高、飞出地图"。
  //   · Bot.Move 对 path == NULL 有安全分支：只把当前位置写回 nextPathPos/dirToNextNode 后返回，不会空指针
  //     （而且每个 Bot 出生后、第一条路径返回前本来就是 path == NULL，属正常状态）。
  //   · Bot.PathSetting 的路径起点 = 当前 transform.position，受 nextFindPathTime(+0xB8) 节流（0.25~0.5s）。
  // 所以传送后做三件事：① 断开旧路径（Bot.Move 立即停止沿旧航点移动）；
  // ② 把进度/起点/计时全部复位到当前位置；③ 清节流并立刻让游戏自己重新寻路（OnPathComplete 会重挂新路径）。
  function resetBotPathAfterTeleport(playerPtr, botPtr) {
    try {
      if (!botPtr || botPtr.isNull() || !isValid(botPtr)) return 'no_bot';
      var cur = readWorldPosition(readPlayerTransform(playerPtr)) || spawn;
      var oldLen = readF32(botPtr.add(0x84));
      var oldId = readI32(botPtr.add(0x90));
      botPtr.add(0x80).writePointer(ptr(0));    // Bot.path = null -> Bot.Move 走无路径安全分支
      botPtr.add(0x84).writeFloat(0);           // pathLength = 0
      botPtr.add(0x90).writeS32(0);             // nextPathVectorID = 0
      botPtr.add(0x94).writeFloat(cur.x);       // lastStartPoint = 当前位置
      botPtr.add(0x98).writeFloat(cur.y);
      botPtr.add(0x9C).writeFloat(cur.z);
      botPtr.add(0xA0).writeFloat(cur.x);       // nextPathPos = 当前位置（本帧也不会朝旧航点跑）
      botPtr.add(0xA4).writeFloat(cur.y);
      botPtr.add(0xA8).writeFloat(cur.z);
      botPtr.add(0xAC).writeFloat(0);           // dirToNextNode = 0
      botPtr.add(0xB0).writeFloat(0);
      botPtr.add(0xB4).writeFloat(0);
      botPtr.add(0xB8).writeFloat(0);           // nextFindPathTime = 0（清掉"0.25~0.5s 才重算"的节流）
      botPtr.add(0xEC).writeFloat(0);           // blockedTime = 0
      // 关键：nextJumpTime 必须写回 +Inf（空闲态），写 0 = 立刻触发 Bot 起跳 -> velData.y=JumpPower(10.5) 恒速飞天。
      // 同时清残余竖直速度与 autonomousJump，打断「跳起来下不来」的状态。
      var jumpState = killJumpState(playerPtr, botPtr);
      if (botPathSettingFn) botPathSettingFn(botPtr, ptr(0));   // 立刻从"当前位置"重新寻路
      diag.stats.pathResets++;
      if (diag.resetLogBudget > 0) {
        diag.resetLogBudget--;
        sendLogFile('debug', GATHER_DIAG_MODULE,
          'PATH_RESET p=' + ptrText(playerPtr) + ' bot=' + ptrText(botPtr) +
          ' from=' + fmtVec(cur) + ' oldPathLen=' + diagNum(oldLen) + ' oldNextId=' + oldId + ' jump[' + jumpState + '] -> ok');
      }
      return 'ok';
    } catch (e) { return 'ERR:' + e.message; }
  }

  function teleportPlayerBySetPos(player, target) {
    try {
      if (!isValid(player)) return 'SetPos=invalid';
      diag.selfSetPos = true;
      try { playerSetPos(player, target.x, target.y, target.z, ptr(0)); } finally { diag.selfSetPos = false; }
      return 'OK:SetPos';
    } catch(e) {
      diag.selfSetPos = false;
      return 'SetPos=ERR:' + e.message;
    }
  }

  function teleportEntity(ppOrBot, isBot) {
    try {
      if (!isBot) {
        var setPosResult = teleportPlayerBySetPos(ppOrBot, spawn);
        if (setPosResult === 'OK:SetPos') return setPosResult;
      }
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
      return 'OK:Transform';
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
    diag.stats.gathers++;
    resetDiagWindows();
    dumpGatherHeader('GATHER#' + tn);

    var playersToMove = {};
    var playerMeta = {};
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
          try {
            var pp = ap.add(0x10 + i * Process.pointerSize).readPointer();
            if (isValid(pp)) { var pk0 = pp.toString(); playersToMove[pk0] = pp; playerMeta[pk0] = { src: 'allPlayers', bot: null }; }
          } catch(e) {}
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
      try {
        if (pp && !pp.isNull()) {
          pp.readPointer(); var pk = pp.toString();
          if (!playersToMove[pk]) { playersToMove[pk] = pp; playerMeta[pk] = { src: 'recent', bot: entry.bot || null }; botAdded++; }
          else if (playerMeta[pk] && !playerMeta[pk].bot) { playerMeta[pk].bot = entry.bot || null; }
        }
      } catch(e) {}
    }

    sendLog('info', '聚怪', '追踪: ' + Object.keys(playersToMove).length + ' Player + ' + botAdded + ' (Bot补充)');
    beginGatherHold();
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
        var meta = playerMeta[pKeys[pi]] || { src: 'unknown', bot: null };
        // 观测快照：TRACE 明细有预算限制，但只要还在 watch 名额内就照常采样（ALERT 依赖它）。
        var wantSnapshot = (diag.traceBudget > 0) || (diag.watchCount < diag.watchLimit);
        var beforeSnap = wantSnapshot ? readSnapshot(pp) : null;
        var r = teleportEntity(pp, false);
        var afterSnap = wantSnapshot ? readSnapshot(pp) : null;
        if (diag.traceBudget > 0) { diag.traceBudget--; traceTeleport(tn, pp, meta.src, r, beforeSnap, afterSnap, meta.bot); }
        registerWatch(pp, meta.src, beforeSnap, afterSnap, meta.bot);
        if (r.indexOf('OK') === 0) {
          botOk++;
          // 关键修复：传送后必须重新寻路，否则 Bot 会沿传送前的旧路径飞走
          resetBotPathAfterTeleport(pp, meta.bot);
          registerHold(pp, meta.bot);
        } else botFail++;
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
      playerSetPos = new NativeFunction(base.add(R.P_SetPos), 'void', ['pointer','float','float','float','pointer'], 'mscdecl');
      getPosInj = new NativeFunction(base.add(R.getPosInj), 'void', ['pointer','pointer','pointer'], 'mscdecl');
      nanoRoleFn = new NativeFunction(base.add(R.P_getNanoRole), 'int', ['pointer','pointer'], 'mscdecl');
      botPathSettingFn = new NativeFunction(base.add(R.Bot_PathSetting), 'void', ['pointer','pointer'], 'mscdecl');
      worldPosBuf = Memory.alloc(16);
      posBuf = Memory.alloc(16);
      singletonGetter = new NativeFunction(base.add(R.SingGetInst), 'pointer', ['pointer']);
      writePosition(spawn);

      try { var h = Interceptor.attach(base.add(R.Bot_Update), { onEnter: function(args) { trackFromBot(args[0]); } }); hooks.push(h); } catch(e) {}
      try { var h2 = Interceptor.attach(base.add(R.GM_AddP), { onEnter: function(a) { if (!gm) { gm = a[0]; } } }); hooks.push(h2); } catch(e) {}
      try { var h3 = Interceptor.attach(base.add(R.MM_MapGun), { onEnter: function(a) { if (mm) return; mm = a[0]; } }); hooks.push(h3); } catch(e) {}
      try { var h4 = Interceptor.attach(base.add(R.P_Update), { onEnter: function(a) { if (!ntp) return; ntp = false; if (!gm || !mm) return; executeTeleport(); } }); hooks.push(h4); } catch(e) {}
      try { var h5 = Interceptor.attach(base.add(R.ModeBase_UpdateTimeUI), { onEnter: function(args) {
        handleModeBaseSeen(args[0]);
        if (diagPending) { diagPending = false; try { dumpGatherDiagnostics(); } catch (e) {} }
        if (diag.watchActive) { try { pumpWatchQueue(); } catch (e) {} }
        if (hold.active) { try { pumpHold(); } catch (e) {} }
      } }); hooks.push(h5); } catch(e) {}
      try { var h6 = Interceptor.attach(base.add(R.ModeBase_ExitGame), { onEnter: function() { clearRoomState('ModeBase.ExitGame'); } }); hooks.push(h6); } catch(e) {}
      try { var h7 = Interceptor.attach(base.add(R.GameManager_GameRoundEnd), { onEnter: function() { clearRoomState('GameManager.GameRoundEnd'); } }); hooks.push(h7); } catch(e) {}
      try { var h8 = Interceptor.attach(base.add(R.GameManager_NewGameRoundStart), { onEnter: function() { clearRoomState('GameManager.NewGameRoundStart'); } }); hooks.push(h8); } catch(e) {}
      try { var h9 = Interceptor.attach(base.add(R.GameManager_OnDestroy), { onEnter: function() { clearRoomState('GameManager.OnDestroy'); } }); hooks.push(h9); } catch(e) {}

      // ── 观测型 Hook（只读，不改变游戏行为；预算用尽或不在观测窗口时直接返回）──
      // 目的：抓“聚怪之后，到底是谁把 Bot 又挪走了”。
      try { var h10 = Interceptor.attach(base.add(R.P_SetPos), { onEnter: function(a) {
        try {
          if (!diagObserving() || diag.selfSetPos || diag.setPosBudget <= 0) return;
          diag.setPosBudget--; diag.stats.gameSetPos++;
          var esp = this.context.esp;
          sendLogFile('debug', GATHER_DIAG_MODULE, 'GAME_SETPOS p=' + ptrText(a[0]) +
            ' current=' + fmtVec(readWorldPosition(readPlayerTransform(a[0]))) +
            ' new=(' + diagNum(ptr(esp).add(8).readFloat()) + ',' + diagNum(ptr(esp).add(12).readFloat()) + ',' + diagNum(ptr(esp).add(16).readFloat()) + ')' +
            ' caller=' + this.returnAddress);
        } catch (e) {}
      } }); hooks.push(h10); } catch(e) {}

      try { var h11 = Interceptor.attach(base.add(R.Bot_Jump), { onEnter: function(a) {
        try {
          if (!diagObserving() || diag.jumpBudget <= 0) return;
          diag.jumpBudget--; diag.stats.jumps++;
          var bot = a[0];
          var pl = null; try { pl = rp(bot, O.Bot_thisPlayer); } catch (e) {}
          sendLogFile('debug', GATHER_DIAG_MODULE, 'BOT_JUMP bot=' + ptrText(bot) + ' p=' + ptrText(pl) +
            ' pos=' + fmtVec(pl ? readWorldPosition(readPlayerTransform(pl)) : null) +
            ' delay=' + diagNum(ptr(this.context.esp).add(8).readFloat()) + ' pathLen=' + diagNum(readF32(bot.add(0x84))));
        } catch (e) {}
      } }); hooks.push(h11); } catch(e) {}

      try { var h12 = Interceptor.attach(base.add(R.P_Spawn), { onEnter: diagLifeEnter, onLeave: function() { diagLifeLeave.call(this, 'GAME_SPAWN'); } }); hooks.push(h12); } catch(e) {}
      try { var h13 = Interceptor.attach(base.add(R.P_Respawn), { onEnter: diagLifeEnter, onLeave: function() { diagLifeLeave.call(this, 'GAME_RESPAWN'); } }); hooks.push(h13); } catch(e) {}
      try { var h14 = Interceptor.attach(base.add(R.ModeNano_RespawnPlayer), { onEnter: diagNanoRespawnEnter, onLeave: diagNanoRespawnLeave }); hooks.push(h14); } catch(e) {}
      try { var h15 = Interceptor.attach(base.add(R.ModeNano_InfectEvent), { onEnter: diagInfectEnter }); hooks.push(h15); } catch(e) {}

      // 观测型：Bot.Update / Bot.JumpCheck 会直接调 Player.OnJumpBtnDown 让 Bot 起跳；
      // 只对本轮聚怪相关对象记录「进/出的 vy 与 grounded」，用来确认「恒速 10.5 飞天 = 反复起跳」这条链。
      try { var h16 = Interceptor.attach(base.add(R.P_OnJumpBtnDown), {
        onEnter: function(a) {
          try {
            this.probePlayer = null;
            if (!diagObserving() || diag.jumpProbeBudget <= 0) return;
            var pp = a[0];
            if (!pp || pp.isNull() || !isValid(pp)) return;
            var key = pp.toString();
            if (!hold.bots[key] && !diag.watched[key]) return;
            diag.jumpProbeBudget--; diag.stats.gameJumps++;
            this.probePlayer = pp;
            this.probeGrounded = readGrounded(pp);
            this.probeVy = readVelocityY(pp);
            this.probeBot = null;
            sendLogFile('debug', GATHER_DIAG_MODULE, 'GAME_JUMP enter p=' + ptrText(pp) + ' grounded=' + this.probeGrounded +
              ' vyBefore=' + diagNum(this.probeVy) + ' caller=' + this.returnAddress);
          } catch (e) {}
        },
        onLeave: function() {
          try {
            var pp = this.probePlayer;
            if (!pp) return;
            sendLogFile('debug', GATHER_DIAG_MODULE, 'GAME_JUMP leave p=' + ptrText(pp) +
              ' vyAfter=' + diagNum(readVelocityY(pp)) + ' auton=' + readU8(pp.add(O.P_autonomousJump)) +
              ' grounded=' + readGrounded(pp));
          } catch (e) {}
        }
      }); hooks.push(h16); } catch(e) {}

      enabled = true;
      diag.periodicBudget = 10;
      startGatherDiagnostics();
      sendLog('success', '聚怪', '已启用 — 动态列表模式');
      sendStatus('gather', true);
    },
    disable: function() {
      if (!enabled) return;
      stopGatherDiagnostics();
      for (var i = 0; i < hooks.length; i++) { try { hooks[i].detach(); } catch(e) {} }
      hooks = []; gm = null; mm = null; modeBase = null; recentBotPlayers = {}; ntp = false;
      clearHold();
      resetDiagWindows(); diag.watchActive = false; diag.watched = {}; diag.watchKeys = []; diag.observeUntil = 0;
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

