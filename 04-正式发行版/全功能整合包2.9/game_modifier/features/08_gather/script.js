// Local helpers for this feature only.
var modules = {};
var __localMaxLogsPerModule = 10;
var __localModuleLogCounts = {};

// ═══════════════════════ 聚怪诊断日志总开关 ═══════════════════════
// true  = 打开「人机飞天」全套诊断：TRACE / WATCH / ALERT / PATH_GUARD / GAME_JUMP /
//         GAME_SETPOS / BOT_JUMP / GAME_SPAWN / GAME_RESPAWN / NANO_RESPAWN /
//         NANO_INFECT / CLIMB_CLEAR / PATH_RESET / [GATHER_DIAG_TEMP]，
//         并挂上对应的只读观测 Hook（日志量约 3000 条 / 5 分钟）。
// false = 全部关闭：不挂观测 Hook、不做快照采样、不写任何「聚怪诊断」日志，
//         性能与日志都回到干净状态。
//         聚怪自身的功能日志（传送 #n / 追踪 / 自己=… Bot活=…）与全部修复逻辑不受影响。
// 以后若再出现异常，把这里改成 true 即可恢复完整证据链。
var GATHER_DIAG_ENABLED = false;

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
  // 唯一出口：诊断总开关关闭时，任何路径都写不出「聚怪诊断」日志。
  if (!GATHER_DIAG_ENABLED) return;
  try { send({ type: 'log_file', level: level, module: module, message: message, audience: 'dev' }); } catch (_) {}
}

// 聚怪专项诊断：独立模块名 + 原始 log_file 通道，绕过每模块 10 条上限，
// 全部落到 logs/game_modifier.log，便于离线分析“多人生化下 Bot 飞天”。
var GATHER_DIAG_MODULE = '聚怪诊断';
function sendGatherDiag(message) {
  if (!GATHER_DIAG_ENABLED) return;
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
    P_isClimbing: 0xB55D80,          // Player.get_isClimbing()（Bot.Move 里爬绳/爬梯分支的判据）
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
    P_autonomousJump: 0x68, Bot_nextJumpTime: 0xE8,
    P_climbStair: 0x114,             // Player+0x114 = 当前挂着的 ClimbStair 对象（Player.get_isClimbing 的判据）
    GM_staticFields: 0x5C, GM_myPlayer: 0x00, GM_gameMode: 0x04,
  };

  var isMy = null, isDead = null, getCC = null, cSE = null, gt = null, spi = null, playerSetPos = null;
  var getPosInj = null, nanoRoleFn = null, worldPosBuf = null, botPathSettingFn = null, isClimbFn = null;
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
    traceBudget: 16, setPosBudget: 20, jumpBudget: 12, lifeBudget: 20, headerBudget: 12, jumpProbeBudget: 8, climbLogBudget: 20,
    summaryBudget: 40, alertBudget: 30, watchLimit: 40, resetLogBudget: 30, guardBudget: 30,
    sampleIntervalMs: 250, sampleWindowMs: 3000, samplesPerBot: 8,
    watched: {}, watchKeys: [], watchActive: false, watchCount: 0,
    observeUntil: 0, selfSetPos: false, periodicBudget: 0,
    stats: { gathers: 0, traced: 0, watched: 0, gameSetPos: 0, jumps: 0, spawnCalls: 0, respawnCalls: 0, infectCalls: 0, alerts: 0, pathResets: 0, pathGuards: 0, gameJumps: 0, climbClears: 0 }
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
    var s = { world: null, raw: null, grounded: null, vy: null, cc: null, ghost: null, team: null, role: null, spawn: null, respawning: null, climb: null };
    try { var tr = readPlayerTransform(pp); s.world = readWorldPosition(tr); s.raw = readRawNativePosition(tr); } catch (e) {}
    try { s.grounded = readGrounded(pp); } catch (e) {}
    try { s.vy = readVelocityY(pp); } catch (e) {}
    try { var cc = getCC(pp, ptr(0)); s.cc = (cc && !cc.isNull()) ? cc.toString() : null; } catch (e) {}
    try { s.ghost = readU8(pp.add(O.Entity_isGhost)); } catch (e) {}
    try { s.team = readI32(pp.add(O.Entity_team)); } catch (e) {}
    try { s.role = readNanoRole(pp); } catch (e) {}
    try { s.spawn = readPlayerSpawnPos(pp); } catch (e) {}
    try { s.respawning = readU8(pp.add(O.P_isRespawning)); } catch (e) {}
    try { s.climb = isClimbFn ? (isClimbFn(pp, ptr(0)) ? 1 : 0) : null; } catch (e) {}
    return s;
  }

  function snapText(s) {
    if (!s) return 'null';
    return 'world=' + fmtVec(s.world) + ' raw=' + fmtVec(s.raw) + ' spawnPos=' + fmtVec(s.spawn) +
      ' role=' + s.role + '(human=' + isHumanRole(s.role) + ') ghost=' + s.ghost + ' team=' + s.team +
      ' grounded=' + s.grounded + ' vy=' + diagNum(s.vy) + ' resp=' + s.respawning + ' climb=' + s.climb + ' cc=' + (s.cc || 'null');
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
    if (!GATHER_DIAG_ENABLED || diag.headerBudget <= 0) return;
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
    if (!GATHER_DIAG_ENABLED) return;   // 总开关关闭：不采样、不建看门狗队列
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
      tl.push(rec.samples[i].t + 'ms:y=' + (w ? diagNum(w.y) : 'na') + '/vy=' + (s ? diagNum(s.vy) : 'na') + '/g=' + (s ? s.grounded : 'na') + '/cl=' + (s ? s.climb : 'na'));
    }
    var last = rec.samples.length ? rec.samples[rec.samples.length - 1].s : null;
    sendLogFile('debug', GATHER_DIAG_MODULE,
      'WATCH #' + rec.idx + ' src=' + rec.src + ' p=' + ptrText(rec.player) + ' role=' + (rec.first ? rec.first.role : 'na') +
      ' ghost=' + (rec.first ? rec.first.ghost : 'na') + ' y0=' + diagNum(rec.y0) + ' maxDy=' + diagNum(rec.maxDy) +
      ' lastWorld=' + fmtVec(last ? last.world : null) + ' lastRaw=' + fmtVec(last ? last.raw : null) +
      ' timeline=' + (tl.length ? tl.join(' ') : 'none'));
  }

  function pumpWatchQueue() {
    if (!GATHER_DIAG_ENABLED || !diag.watchActive) return;
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
              ' y=' + diagNum(snap.world.y) + ' -> ' + resetBotPathAfterTeleport(rec.player, rec.bot, 'guard'));
          }
          if (dy > 3 && diag.alertBudget > 0) {
            diag.alertBudget--; diag.stats.alerts++;
            sendLogFile('debug', GATHER_DIAG_MODULE,
              'ALERT #' + rec.idx + ' dy=' + diagNum(dy) + ' grounded=' + snap.grounded + ' vy=' + diagNum(snap.vy) +
              ' role=' + snap.role + ' ghost=' + snap.ghost + ' resp=' + snap.respawning + ' climb=' + snap.climb +
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
    if (!GATHER_DIAG_ENABLED) {
      // 总开关关闭：预算全部清零，快照采样与看门狗都不再进入
      diag.traceBudget = 0; diag.setPosBudget = 0; diag.jumpBudget = 0; diag.lifeBudget = 0;
      diag.jumpProbeBudget = 0; diag.climbLogBudget = 0; diag.summaryBudget = 0; diag.alertBudget = 0;
      diag.resetLogBudget = 0; diag.guardBudget = 0; diag.periodicBudget = 0;
      diag.watched = {}; diag.watchKeys = []; diag.watchActive = false; diag.watchCount = 0;
      diag.observeUntil = 0;
      return;
    }
    diag.traceBudget = 16; diag.setPosBudget = 20; diag.jumpBudget = 12; diag.lifeBudget = 20; diag.jumpProbeBudget = 8; diag.climbLogBudget = 20;
    diag.summaryBudget = 40; diag.alertBudget = 30; diag.resetLogBudget = 30; diag.guardBudget = 30;
    diag.watched = {}; diag.watchKeys = []; diag.watchActive = false; diag.watchCount = 0;
    diag.observeUntil = Date.now() + 5000;
    diag.periodicBudget = 40;
  }

  function diagObserving() {
    return GATHER_DIAG_ENABLED && enabled && Date.now() <= diag.observeUntil;
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

  // 周期诊断用的坐标：必须走官方 Transform.get_position(0x3F4280)。
  // 那套 native transform(+0x10)+0x38/0x3C/0x40 在本版本读出来恒为 (0,0,0)（日志里 raw= 那一列就是它），
  // 于是 [GATHER_DIAG_TEMP] 的 pos= 一直是 0，看不到「越飞越高」的连续轨迹。
  function readPlayerPosition(pp) {
    return readWorldPosition(readPlayerTransform(pp));
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
    if (!GATHER_DIAG_ENABLED || !enabled) return;
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
    if (!GATHER_DIAG_ENABLED || diagnosticsTimer) return;   // 总开关关闭：连 1 秒周期定时器都不建
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

  // 只把 Bot 的跳跃计时器写回 +Inf（游戏自己的"空闲"态）。**不再写 velData / autonomousJump**：
  // velData.y 是游戏每帧按重力演进的状态，外部每 100ms 清零会让 Bot 悬停、掉落变慢、表现成"不受重力影响 + 卡顿"。
  function disarmBotJump(playerPtr, botPtr) {
    var disarm = 0;
    try {
      if (botPtr && !botPtr.isNull() && isValid(botPtr)) { botPtr.add(O.Bot_nextJumpTime).writeU32(TIME_INF_BITS); disarm = 1; }
    } catch (e) {}
    return 'disarm=' + disarm;
  }

  // ═════════ 爬梯/爬绳状态复位：治「聚怪后人机斜着飞上天」 ═════════
  // 依据（IDA 反编译 + capstone 反汇编）：
  //   · Player.get_isClimbing(0x10B55D80) 的全部实现就是 return [Player+0x114] != null ——
  //     这个字段不是布尔量，而是 Player.climbStair 这个 Transform（全局元数据：get_climbStair/set_climbStair，
  //     MoveType 枚举里的 ClimbStair 就是它）。
  //   · 游戏自己「下梯子」的动作就是 Player.set_climbStair(0x10B56700) 里的 `mov [ecx+114h], eax`（再跟一个 GC 写屏障），
  //     所以这里写 0 与游戏自身的清除语义完全一致（写 NULL 的写屏障是空操作）。
  //   · Player.MoveByLocalDirection(0x10B50A00)：!grounded 且 get_isClimbing() 为真时走 0x10B50BDD 的爬升分支：
  //     读 [Player+0x114] 的 transform.position 与玩家自身 y 比较，决定 moveState（ebx=2/3），
  //     再在 jump table(0x10B50F3C) 里用 Transform.get_right()/get_up() 合成速度 ——
  //     函数在 0x10B50B98 直接把输入 x 覆盖成 0x40F00000 = 7.5f，于是水平 7.5 m/s + 竖直 4.25 m/s 的斜向直线，
  //     与日志里「vy 恒为 4.25、水平 8~9 m/s、越飞越高」完全吻合。
  //   · Player.FixedUpdate(0x10B50680) / Player.UpdateFallTime(0x10B54910)：!grounded && !isClimbing 才走坠落计时，
  //     所以爬升态「不受重力」。
  //   · 触发链：Bot 传送前就挂在梯子上（TRACE 的 before 快照 climb=1 / vy=4.25），聚怪用 SetPos 把它瞬移到出生点，
  //     但瞬移不会补发 OnTriggerExit —— [Player+0x114] 仍指向旧梯子，于是它继续沿梯子的方向飞。
  //     日志实证：12:43 那局 4 轮聚怪，每轮唯一 climb=1 的人机就是唯一飞天的那只（p=0x433b95c0）。
  // 修法：传送后把 [Player+0x114] 清 0 = 「你已经不在梯子上了」，爬升分支立刻失效，回到正常的路径行走 + 重力。
  function clearClimbState(playerPtr, tag) {
    try {
      if (!playerPtr || playerPtr.isNull() || !isValid(playerPtr)) return 'climb=na';
      var before = 0;
      try { before = (isClimbFn && isClimbFn(playerPtr, ptr(0))) ? 1 : 0; } catch (e) {}
      if (!before) return 'climb=0';
      var stair = null;
      try { stair = playerPtr.add(O.P_climbStair).readPointer(); } catch (e) {}
      playerPtr.add(O.P_climbStair).writeU32(0);
      var after = 0;
      try { after = (isClimbFn && isClimbFn(playerPtr, ptr(0))) ? 1 : 0; } catch (e) {}
      diag.stats.climbClears++;
      if (diag.climbLogBudget > 0) {
        diag.climbLogBudget--;
        sendLogFile('debug', GATHER_DIAG_MODULE,
          'CLIMB_CLEAR ' + (tag || '') + ' p=' + ptrText(playerPtr) + ' stair=' + ptrText(stair) +
          ' climb=' + before + '->' + after);
      }
      return 'climb=' + before + '->' + after;
    } catch (e) { return 'climb=ERR:' + e.message; }
  }

  // ═════════ 传送后复位：只「重算路径 + 复位跳跃闸门」，不碰任何路径进度字段 ═════════
  // 依据（capstone 反汇编 0x10B2FBE0 Bot.Move）：
  //   · path != null：edi = path->vectorPath(+0x2C) -> nextPathPos(+0xA0) = vectorPath[nextPathVectorID(+0x90)]，
  //     再算方向 -> Bot.GetMoveStateByDir(0x10B2E8A0) -> Player.MoveByLocalDirection(0x10B50A00)。
  //   · **path == null（0x10B2FC8F 起）**：只把当前位置写回 nextPathPos(+0xA0)/dirToNextNode(+0xAC)，
  //     然后 jmp 0x10B2FFC9；那条尾链传给 Player.MoveByLocalDirection 的方向仍是函数开头
  //     UnityEngine.Vector2Int.get_zero() 的 (0,0) —— 也就是「Bot 完全没有移动输入」，
  //     只能带着传送前的残余速度漂移。日志里异常人机 pathLen 恒为 0.00 正是这个状态。
  //   · Bot.PathSetting(0x10B31E90) 的起点 = 当前 transform.position，受 nextFindPathTime(+0xB8) 节流。
  // 因此这里**不再把 Bot.path 置空，也不再改 nextPathVectorID / nextPathPos / dirToNextNode / pathLength**，
  // 只做两件事：① 清节流并立刻让游戏从「当前位置」重算新路径（OnPathComplete 会自己替换旧 path）；
  //             ② nextJumpTime 写回 +Inf（写 0 = 立刻可跳 -> velData.y=JumpPower(10.5) 恒速飞天，是上一轮的坑）。
  function resetBotPathAfterTeleport(playerPtr, botPtr, tag) {
    try {
      var climbState = clearClimbState(playerPtr, tag || 'teleport');
      if (!botPtr || botPtr.isNull() || !isValid(botPtr)) return 'no_bot ' + climbState;
      var cur = readWorldPosition(readPlayerTransform(playerPtr)) || spawn;
      var oldLen = readF32(botPtr.add(0x84));
      var oldId = readI32(botPtr.add(0x90));
      var jumpState = disarmBotJump(playerPtr, botPtr);          // Bot.nextJumpTime = +Inf
      botPtr.add(0xB8).writeFloat(0);                            // nextFindPathTime = 0 -> 允许立刻重算
      if (botPathSettingFn) botPathSettingFn(botPtr, ptr(0));    // 起点 = 当前 transform.position
      diag.stats.pathResets++;
      if (diag.resetLogBudget > 0) {
        diag.resetLogBudget--;
        sendLogFile('debug', GATHER_DIAG_MODULE,
          'PATH_RESET p=' + ptrText(playerPtr) + ' bot=' + ptrText(botPtr) +
          ' from=' + fmtVec(cur) + ' oldPathLen=' + diagNum(oldLen) + ' oldNextId=' + oldId + ' jump[' + jumpState + '] ' + climbState + ' -> ok');
      }
      return 'ok ' + climbState;
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
        var wantSnapshot = GATHER_DIAG_ENABLED && ((diag.traceBudget > 0) || (diag.watchCount < diag.watchLimit));
        var beforeSnap = wantSnapshot ? readSnapshot(pp) : null;
        var r = teleportEntity(pp, false);
        var afterSnap = wantSnapshot ? readSnapshot(pp) : null;
        if (diag.traceBudget > 0) { diag.traceBudget--; traceTeleport(tn, pp, meta.src, r, beforeSnap, afterSnap, meta.bot); }
        registerWatch(pp, meta.src, beforeSnap, afterSnap, meta.bot);
        if (r.indexOf('OK') === 0) {
          botOk++;
          // 关键修复：传送后必须重新寻路，否则 Bot 会沿传送前的旧路径飞走
          resetBotPathAfterTeleport(pp, meta.bot);
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
      isClimbFn = new NativeFunction(base.add(R.P_isClimbing), 'bool', ['pointer','pointer'], 'mscdecl');
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
      } }); hooks.push(h5); } catch(e) {}
      try { var h6 = Interceptor.attach(base.add(R.ModeBase_ExitGame), { onEnter: function() { clearRoomState('ModeBase.ExitGame'); } }); hooks.push(h6); } catch(e) {}
      try { var h7 = Interceptor.attach(base.add(R.GameManager_GameRoundEnd), { onEnter: function() { clearRoomState('GameManager.GameRoundEnd'); } }); hooks.push(h7); } catch(e) {}
      try { var h8 = Interceptor.attach(base.add(R.GameManager_NewGameRoundStart), { onEnter: function() { clearRoomState('GameManager.NewGameRoundStart'); } }); hooks.push(h8); } catch(e) {}
      try { var h9 = Interceptor.attach(base.add(R.GameManager_OnDestroy), { onEnter: function() { clearRoomState('GameManager.OnDestroy'); } }); hooks.push(h9); } catch(e) {}

      // ── 观测型 Hook（只读，不改变游戏行为；预算用尽或不在观测窗口时直接返回）──
      // 目的：抓“聚怪之后，到底是谁把 Bot 又挪走了”。
      // 诊断总开关关闭时，attachDiag 直接跳过 —— 这 7 个 Hook 一个都不挂。
      function attachDiag(rva, spec) {
        if (!GATHER_DIAG_ENABLED) return;
        try { hooks.push(Interceptor.attach(base.add(rva), spec)); } catch (e) {}
      }

      attachDiag(R.P_SetPos, { onEnter: function(a) {
        try {
          if (!diagObserving() || diag.selfSetPos || diag.setPosBudget <= 0) return;
          diag.setPosBudget--; diag.stats.gameSetPos++;
          var esp = this.context.esp;
          sendLogFile('debug', GATHER_DIAG_MODULE, 'GAME_SETPOS p=' + ptrText(a[0]) +
            ' current=' + fmtVec(readWorldPosition(readPlayerTransform(a[0]))) +
            ' new=(' + diagNum(ptr(esp).add(8).readFloat()) + ',' + diagNum(ptr(esp).add(12).readFloat()) + ',' + diagNum(ptr(esp).add(16).readFloat()) + ')' +
            ' caller=' + this.returnAddress);
        } catch (e) {}
      } });

      attachDiag(R.Bot_Jump, { onEnter: function(a) {
        try {
          if (!diagObserving() || diag.jumpBudget <= 0) return;
          diag.jumpBudget--; diag.stats.jumps++;
          var bot = a[0];
          var pl = null; try { pl = rp(bot, O.Bot_thisPlayer); } catch (e) {}
          sendLogFile('debug', GATHER_DIAG_MODULE, 'BOT_JUMP bot=' + ptrText(bot) + ' p=' + ptrText(pl) +
            ' pos=' + fmtVec(pl ? readWorldPosition(readPlayerTransform(pl)) : null) +
            ' delay=' + diagNum(ptr(this.context.esp).add(8).readFloat()) + ' pathLen=' + diagNum(readF32(bot.add(0x84))));
        } catch (e) {}
      } });

      attachDiag(R.P_Spawn, { onEnter: diagLifeEnter, onLeave: function() { diagLifeLeave.call(this, 'GAME_SPAWN'); } });
      attachDiag(R.P_Respawn, { onEnter: diagLifeEnter, onLeave: function() { diagLifeLeave.call(this, 'GAME_RESPAWN'); } });
      attachDiag(R.ModeNano_RespawnPlayer, { onEnter: diagNanoRespawnEnter, onLeave: diagNanoRespawnLeave });
      attachDiag(R.ModeNano_InfectEvent, { onEnter: diagInfectEnter });

      // 观测型：Bot.Update / Bot.JumpCheck 会直接调 Player.OnJumpBtnDown 让 Bot 起跳；
      // 只对本轮聚怪相关对象记录「进/出的 vy 与 grounded」，用来确认「恒速 10.5 飞天 = 反复起跳」这条链。
      attachDiag(R.P_OnJumpBtnDown, {
        onEnter: function(a) {
          try {
            this.probePlayer = null;
            if (!diagObserving() || diag.jumpProbeBudget <= 0) return;
            var pp = a[0];
            if (!pp || pp.isNull() || !isValid(pp)) return;
            var key = pp.toString();
            if (!diag.watched[key] && !recentBotPlayers[key]) return;   // 只关心本轮聚怪相关对象
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
      });

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

