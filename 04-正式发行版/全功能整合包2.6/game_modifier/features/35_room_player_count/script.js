// Configurable total room size for UnityCrossFire 1.7.1 (x86).
// Enable and choose a value before clicking the game's Start Game button.
(function () {
  'use strict';

  var FEATURE_ID = '35_room_player_count';
  var enabled = false;
  var patchApplied = false;
  var totalPlayers = 50;
  var gameAssembly = null;
  var maxTotalPlayers = null;
  var lastWrittenBots = null;
  var adoptedPatch = false;
  var profilePatchedByThisScript = false;
  var activePatchProfile = 'none';
  var diagnosticTimer = null;
  var lastDiagnostic = '';

  // The build already routes every GenerateBotClient invocation through this
  // code cave.  Patching the cave avoids Frida trampolines inside the hot
  // function and therefore preserves the game's stack/calling convention.
  var BOT_CAVE_RVA = 0xB30F3C;
  var BOT_MODE_BRANCH_OFFSET = 7;   // 75 05: only override GameMode 6
  var BOT_COUNT_IMM_OFFSET = 10;    // imm32 following BF
  // Nano/terminator modes naturally skip the dropdown-index conversion here.
  // Normal modes do not, so their configured EDI count gets overwritten unless
  // this conditional jump is made unconditional.
  var BOT_CONVERSION_BRANCH_RVA = 0xB25C68; // 75 0F -> EB 0F
  var BOT_NAME_CAVE_RVA = 0xB67F07;
  var BOT_NAME_BRANCH_OFFSET = 21;  // 74 05: skip RemoveAt only in mode 6

  // Exact, reversible conversion from the verified original 30-player build
  // to its matching 100-player v3 build. Every range is checked before any
  // write; unknown or mixed binaries are never modified.
  var BASE_30_TO_V3_PROFILE = [
    [0x12AF7F, 'cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc', '50 6a 00 56 e8 48 2e a4 00 83 c4 08 58 84 c0 74 0e b8 00 00 c8 42 66 0f 6e c0 e9 4d b9 a3 00 f3 0f 10 80 ec 00 00 00 e9 40 b9 a3 00'],
    [0x154FBA, 'cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc', '56 57 8b f8 8b b7 ec 00 00 00 6a 00 68 0a 00 00 00 8d 46 30 50 e8 4c 95 6a 00 83 c4 0c 6a 00 68 e7 03 00 00 8d 46 44 50 e8 39 95 6a 00 83 c4 0c e9 5c ba 46 00'],
    [0x2BF6F8, 'cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc', '8b 06 6a 00 6a 01 6a 00 68 a6 0d 00 00 50 e8 85 bc 83 00 83 c4 14 e9 a7 5c e9 ff'],
    [0x3D18E2, 'cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc', '83 c4 0c 51 6a 00 ff 75 08 e8 e0 46 78 00 83 c4 08 84 c0 74 0e d9 c0 d8 c0 d8 c1 d8 c1 d8 c1 d8 c8 dd d9 59 5d c3'],
    [0x5C0E4B, 'cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc', '6a 00 57 e8 1d 62 5a 00 83 c4 08 5f 5e e9 b1 e8 cf ff'],
    [0x72BE79, 'cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc', '6a 00 56 e8 4f a1 42 00 83 c4 08 84 c0 74 05 e9 fb 5a 42 00 80 be 70 00 00 00 00 75 05 e9 7a 5b 42 00 e9 e8 5a 42 00'],
    [0x9DA472, 'cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc', '50 6a 00 56 e8 55 3d 19 00 83 c4 08 58 84 c0 74 0e b8 00 00 c8 42 66 0f 6e c0 e9 9d c8 18 00 f3 0f 10 80 f0 00 00 00 e9 90 c8 18 00'],
    [0xAF9C69, '1e', '64'], [0xAFAD8D, '1e', '64'], [0xAFD066, '1e', '64'],
    [0xB25C56, '8b 40 5c 6a', 'e9 e1 b2 00'], [0xB25D3F, 'e8 4c 68 f0 ff', 'e9 c3 21 04 00'],
    [0xB30F3C, 'cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc', '8b 40 5c 83 78 04 06 75 05 bf 32 00 00 00 6a 00 e9 0a 4d ff ff'],
    [0xB43D76, '3b 41 0c 73 0b 8b 44 81 10 5d c3 e9 da 3f 62 ff 6a 00 e8 73 3c 62 ff 50 e8 9d 3f 62 ff', '83 f8 1d 7e 05 b8 1d 00 00 00 8b 44 81 10 5d c3 90 90 90 90 90 90 90 90 90 90 90 90 90'],
    [0xB44895, '8b 87 cc 00 00 00', 'e9 5e ae 77 ff 90'],
    [0xB67F07, 'cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc cc', 'e8 00 00 00 00 59 81 c1 30 14 2c 00 8b 09 8b 49 5c 83 79 04 06 74 05 e8 6d 46 ec ff e9 1c de fb ff'],
    [0xB74657, '3b 48 0c 0f 83 34 01 00 00 8b 53 18 8b 4c 88 10', '83 f9 1d 7e 03 6a 1d 59 8b 53 18 8b 4c 88 10 90']
  ];

  // Runtime diagnostics.  The room/TAB list is separate from the Player[]
  // owned by GameManager, so counting the latter tells us whether a mode is
  // failing while creating players, spawning them, or only drawing models.
  var GAME_MANAGER_METHOD_INFO_RVA = 0xE1CE64;
  var GM_ALL_PLAYERS_OFFSET = 0x1C;
  var GM_PLAYERS_BL_OFFSET = 0x20;
  var GM_PLAYERS_BL_ALIVE_OFFSET = 0x24;
  var GM_PLAYERS_GR_OFFSET = 0x28;
  var GM_PLAYERS_GR_ALIVE_OFFSET = 0x2C;
  var PLAYER_CHARACTER_CONTAINER_OFFSET = 0x58;
  var PLAYER_CURRENT_CHARACTER_OFFSET = 0x5C;

  function log(level, message) {
    try { send({ type: 'log', level: level, module: '房间人数', message: message, audience: 'user' }); } catch (_) {}
  }

  function status(value) {
    try { send({ type: 'status', feature: FEATURE_ID, enabled: value }); } catch (_) {}
  }

  function normalize(value) {
    var n = Number(value);
    if (!isFinite(n)) n = 50;
    n = Math.round(n);
    return Math.max(2, Math.min(100, n));
  }

  function readListCount(owner, offset) {
    try {
      var list = owner.add(offset).readPointer();
      if (!list || list.isNull()) return 0;
      return list.add(0xC).readS32();
    } catch (_) {
      return -1;
    }
  }

  function getGameManager() {
    try {
      // Resolve every time. Never invoke Unity APIs from the diagnostic timer
      // or retain the previous room's destroyed GameManager.
      var method = gameAssembly.base.add(GAME_MANAGER_METHOD_INFO_RVA).readPointer();
      var klass = method.add(0xC).readPointer();
      var rgctx = klass.add(0x60).readPointer();
      var singleton = rgctx.readPointer();
      var fields = singleton.add(0x5C).readPointer();
      var instance = fields.readPointer();
      if (instance.isNull() || instance.add(8).readPointer().isNull()) return null;
      return instance;
    } catch (_) {
      return null;
    }
  }

  function collectEntityDiagnostic() {
    var gm = getGameManager();
    if (!gm) return null;
    try {
      var players = gm.add(GM_ALL_PLAYERS_OFFSET).readPointer();
      if (!players || players.isNull()) return null;
      var capacity = players.add(0xC).readU32();
      if (capacity < 1 || capacity > 256) return null;
      var created = 0;
      var containers = 0;
      var models = 0;
      // UnityCrossFire 1.7.1 is x86: managed reference arrays use 4-byte
      // element slots starting at +0x10.
      for (var i = 0; i < capacity; i++) {
        var player = players.add(0x10 + i * 4).readPointer();
        if (!player || player.isNull()) continue;
        created++;
        try {
          var container = player.add(PLAYER_CHARACTER_CONTAINER_OFFSET).readPointer();
          if (container && !container.isNull()) containers++;
        } catch (_) {}
        try {
          var model = player.add(PLAYER_CURRENT_CHARACTER_OFFSET).readPointer();
          if (model && !model.isNull()) models++;
        } catch (_) {}
      }
      return {
        capacity: capacity,
        created: created,
        containers: containers,
        models: models,
        bl: readListCount(gm, GM_PLAYERS_BL_OFFSET),
        blAlive: readListCount(gm, GM_PLAYERS_BL_ALIVE_OFFSET),
        gr: readListCount(gm, GM_PLAYERS_GR_OFFSET),
        grAlive: readListCount(gm, GM_PLAYERS_GR_ALIVE_OFFSET)
      };
    } catch (_) {
      return null;
    }
  }

  function dumpEntityDiagnostic() {
    if (!enabled || !gameAssembly) return;
    var d = collectEntityDiagnostic();
    if (!d) return;
    var summary = '数组容量=' + d.capacity +
      '，已创建实体=' + d.created +
      '，角色容器=' + d.containers +
      '，角色模型=' + d.models +
      '，队伍人数=' + d.bl + '/' + d.gr +
      '，存活人数=' + d.blAlive + '/' + d.grAlive;
    if (summary === lastDiagnostic) return;
    lastDiagnostic = summary;
    log('info', '实体诊断：' + summary);
  }

  function startEntityDiagnostic() {
    if (diagnosticTimer) return;
    lastDiagnostic = '';
    dumpEntityDiagnostic();
    diagnosticTimer = setInterval(dumpEntityDiagnostic, 1000);
  }

  function stopEntityDiagnostic() {
    if (diagnosticTimer) {
      clearInterval(diagnosticTimer);
      diagnosticTimer = null;
    }
    lastDiagnostic = '';
  }

  function readBytes(rva, length) {
    var result = [];
    for (var i = 0; i < length; i++) result.push(gameAssembly.base.add(rva + i).readU8());
    return result;
  }

  function hexBytes(hex) {
    return hex.split(' ').map(function (value) { return parseInt(value, 16); });
  }

  function bytesEqual(actual, expectedHex) {
    var expected = hexBytes(expectedHex);
    if (actual.length !== expected.length) return false;
    for (var i = 0; i < expected.length; i++) {
      if (actual[i] !== expected[i]) return false;
    }
    return true;
  }

  function profileState() {
    var base = true;
    var v3 = true;
    for (var i = 0; i < BASE_30_TO_V3_PROFILE.length; i++) {
      var entry = BASE_30_TO_V3_PROFILE[i];
      var actual = readBytes(entry[0], hexBytes(entry[1]).length);
      if (!bytesEqual(actual, entry[1])) base = false;
      if (!bytesEqual(actual, entry[2])) v3 = false;
    }
    if (base) return 'base';
    if (v3) return 'v3';
    return 'unknown';
  }

  function writeProfileBytes(kind) {
    var index = kind === 'v3' ? 2 : 1;
    for (var i = 0; i < BASE_30_TO_V3_PROFILE.length; i++) {
      var entry = BASE_30_TO_V3_PROFILE[i];
      var address = gameAssembly.base.add(entry[0]);
      var value = hexBytes(entry[index]);
      if (!Memory.protect(address, value.length, 'rwx')) {
        throw new Error('内存保护设置失败 RVA 0x' + entry[0].toString(16));
      }
    }
    for (var j = 0; j < BASE_30_TO_V3_PROFILE.length; j++) {
      var writeEntry = BASE_30_TO_V3_PROFILE[j];
      gameAssembly.base.add(writeEntry[0]).writeByteArray(hexBytes(writeEntry[index]));
    }
    var expected = kind === 'v3' ? 'v3' : 'base';
    if (profileState() !== expected) throw new Error('人数基础补丁写入后校验失败');
  }

  function applyBaselineProfile() {
    var state = profileState();
    if (state === 'v3') {
      activePatchProfile = 'prepatched_v3';
      return { patchedByThisScript: false, profile: activePatchProfile };
    }
    if (state !== 'base') {
      throw new Error('当前 GameAssembly.dll 不是已验证的原始30人版或100人v3版，已拒绝写入');
    }
    try {
      writeProfileBytes('v3');
    } catch (error) {
      // All ranges were first made writable before any byte was changed.
      // Restore the verified baseline if an individual write or readback fails.
      try { writeProfileBytes('base'); } catch (_) {}
      throw error;
    }
    profilePatchedByThisScript = true;
    activePatchProfile = 'baseline_30_auto_patched';
    log('info', '已识别原始30人版，已在本次游戏进程中临时加载100人基础补丁');
    return { patchedByThisScript: true, profile: activePatchProfile };
  }

  function restoreBaselineProfile() {
    if (!profilePatchedByThisScript) return true;
    if (profileState() !== 'v3') {
      log('error', '人数基础补丁已被其他修改器改变，未覆盖其设置；请重启游戏');
      return false;
    }
    writeProfileBytes('base');
    profilePatchedByThisScript = false;
    activePatchProfile = 'none';
    return true;
  }

  function expectPattern(rva, hex) {
    var pattern = hex.split(' '), actual = readBytes(rva, pattern.length);
    for (var i = 0; i < pattern.length; i++) {
      if (pattern[i] !== '??' && actual[i] !== parseInt(pattern[i], 16)) {
        throw new Error('代码校验失败 RVA 0x' + rva.toString(16) + '，实际字节 ' +
          actual.map(function (n) { return ('0' + n.toString(16)).slice(-2); }).join(' '));
      }
    }
  }

  function inspectLayout() {
    // Full, position-independent code-cave anchors plus both jump destinations.
    // Accept only known intact states, never arbitrary NOP/branch combinations.
    expectPattern(BOT_CAVE_RVA, '8b 40 5c 83 78 04 06 ?? ?? bf ?? ?? ?? ?? 6a 00 e9 0a 4d ff ff');
    expectPattern(BOT_NAME_CAVE_RVA, 'e8 00 00 00 00 59 81 c1 30 14 2c 00 8b 09 8b 49 5c 83 79 04 06 ?? 05 e8 6d 46 ec ff e9 1c de fb ff');
    var jumps = [[0xB25C56, BOT_CAVE_RVA], [0xB25D3F, BOT_NAME_CAVE_RVA]];
    for (var i = 0; i < jumps.length; i++) {
      var at = gameAssembly.base.add(jumps[i][0]);
      if (at.readU8() !== 0xE9 || at.add(1).readS32() !== jumps[i][1] - jumps[i][0] - 5) {
        throw new Error('人数代码入口不匹配 RVA 0x' + jumps[i][0].toString(16));
      }
    }
    expectPattern(0xAF9C67, '83 fe ?? 0f 8c 70 ff ff ff');
    expectPattern(0xAFAD8B, '83 ff ?? 7c 80');
    expectPattern(0xAFD065, '6a ?? ff 35');
    var limits = [0xAF9C69, 0xAFAD8D, 0xAFD066].map(function (rva) {
      return gameAssembly.base.add(rva).readU8();
    });
    if (limits[0] !== limits[1] || limits[1] !== limits[2] ||
        (limits[0] !== 70 && limits[0] !== 100)) {
      throw new Error('角色容量不匹配：' + limits.join('/') + '；需要已验证的100人v3基础补丁状态');
    }
    var bot = readBytes(BOT_CAVE_RVA + BOT_MODE_BRANCH_OFFSET, 2);
    var conversion = readBytes(BOT_CONVERSION_BRANCH_RVA, 2);
    var name = gameAssembly.base.add(BOT_NAME_CAVE_RVA + BOT_NAME_BRANCH_OFFSET).readU8();
    var bots = gameAssembly.base.add(BOT_CAVE_RVA + BOT_COUNT_IMM_OFFSET).readU32();
    var pristine = bot[0] === 0x75 && bot[1] === 0x05 && conversion[0] === 0x75 &&
      conversion[1] === 0x0F && name === 0x74 && bots === 50;
    var active = bot[0] === 0x90 && bot[1] === 0x90 && conversion[0] === 0xEB &&
      conversion[1] === 0x0F && name === 0xEB && bots >= 1 && bots < limits[0];
    if (!pristine && !active) throw new Error('人数补丁状态不完整或被其他修改器覆盖，请关闭所有修改器并重启配套游戏');
    return { capacity: limits[0], active: active, bot: bot, conversion: conversion[0], name: name, bots: bots };
  }

  function resultFailure(reason, message) {
    log('error', message);
    if (gameAssembly && gameAssembly.path) log('info', '当前加载模块：' + gameAssembly.path);
    return { ok: false, reason: reason, message: message, max_total_players: maxTotalPlayers,
      total_players: totalPlayers };
  }

  function capacityError(requested) {
    if (requested <= maxTotalPlayers) return null;
    return resultFailure('capacity_exceeded', '这份游戏最多支持 ' + maxTotalPlayers +
      ' 人，不能设为 ' + requested + ' 人。');
  }

  function writeState(value) {
    var bot = gameAssembly.base.add(BOT_CAVE_RVA + BOT_MODE_BRANCH_OFFSET);
    var count = gameAssembly.base.add(BOT_CAVE_RVA + BOT_COUNT_IMM_OFFSET);
    var conversion = gameAssembly.base.add(BOT_CONVERSION_BRANCH_RVA);
    var name = gameAssembly.base.add(BOT_NAME_CAVE_RVA + BOT_NAME_BRANCH_OFFSET);
    // Request all protections before the first write; install the active branch last.
    [[bot, 2], [count, 4], [conversion, 1], [name, 1]].forEach(function (entry) {
      if (!Memory.protect(entry[0], entry[1], 'rwx')) throw new Error('内存保护设置失败');
    });
    count.writeU32(value.bots);
    name.writeU8(value.name);
    conversion.writeU8(value.conversion);
    bot.writeByteArray(value.bot);
  }

  function successResult() {
    return { ok: true, enabled: enabled, total_players: totalPlayers, bots: totalPlayers - 1,
      max_total_players: maxTotalPlayers, patch_applied: patchApplied, adopted_existing_patch: adoptedPatch,
      patch_profile: activePatchProfile, profile_patched_by_this_script: profilePatchedByThisScript };
  }

  function enable(config) {
    var requested = normalize(config && Object.prototype.hasOwnProperty.call(config, 'total_players') ?
      config.total_players : totalPlayers);
    totalPlayers = requested;
    enabled = true;
    log('info', '已开启；请点击“应用人数”后写入当前设置。');
    status(true);
    return successResult();
  }

  function installPatch(requested) {
    gameAssembly = Process.findModuleByName('GameAssembly.dll');
    maxTotalPlayers = null;
    if (!gameAssembly || Process.pointerSize !== 4) {
      return resultFailure('unsupported_process', '未检测到兼容的32位游戏，请等已连接后重试');
    }
    var before;
    var profile;
    try {
      profile = applyBaselineProfile();
      before = inspectLayout();
      maxTotalPlayers = before.capacity;
    } catch (e) {
      try { restoreBaselineProfile(); } catch (_) {}
      return resultFailure('incompatible_game', '当前 GameAssembly.dll 与人数补丁不匹配：' + (e.message || e));
    }
    var tooLarge = capacityError(requested);
    if (tooLarge) return tooLarge;
    try {
      writeState({ bot: [0x90, 0x90], conversion: 0xEB, name: 0xEB, bots: requested - 1 });
      var after = inspectLayout();
      if (!after.active || after.bots !== requested - 1) throw new Error('写入后校验失败');
    } catch (e) {
      try { writeState(before); } catch (_) {}
      try { restoreBaselineProfile(); } catch (_) {}
      return resultFailure('patch_failed', '安装人数补丁失败：' + (e.message || e));
    }
    totalPlayers = requested;
    lastWrittenBots = requested - 1;
    adoptedPatch = before.active || !profile.patchedByThisScript;
    patchApplied = true;
    startEntityDiagnostic();
    if (profile.patchedByThisScript) log('info', '当前游戏已临时适配为100人版；断开连接后会恢复原始30人版。');
    else if (adoptedPatch) log('info', '检测到已安装的人数补丁，已重新接管；请勿同时运行多份修改器');
    log('success', '已启用：总人数 ' + totalPlayers + '（玩家1 + 机器人' + (totalPlayers - 1) +
      '），游戏容量 ' + maxTotalPlayers + '。请开始新对局。');
    status(true);
    return successResult();
  }

  function applyConfig(config) {
    var requested = normalize(config && Object.prototype.hasOwnProperty.call(config, 'total_players') ?
      config.total_players : totalPlayers);
    if (!enabled) {
      return resultFailure('feature_disabled', '请先开启全模式房间人数功能，再点击应用人数');
    }
    if (!patchApplied) return installPatch(requested);
    var layout;
    try {
      layout = inspectLayout();
      maxTotalPlayers = layout.capacity;
    } catch (e) {
      stopEntityDiagnostic();
      enabled = false;
      status(false);
      return resultFailure('patch_conflict', '人数补丁被改变：' + (e.message || e));
    }
    var tooLarge = capacityError(requested);
    if (tooLarge) return tooLarge;
    if (!layout.active) {
      // A previous script's cleanup may have restored the known pristine state.
      stopEntityDiagnostic();
      patchApplied = false;
      return installPatch(requested);
    }
    var count = gameAssembly.base.add(BOT_CAVE_RVA + BOT_COUNT_IMM_OFFSET);
    try {
      if (!Memory.protect(count, 4, 'rwx')) throw new Error('内存保护设置失败');
      count.writeU32(requested - 1);
      if (count.readU32() !== requested - 1) throw new Error('写入后人数校验失败');
    } catch (e) {
      try { count.writeU32(layout.bots); } catch (_) {}
      return resultFailure('write_failed', '写入房间人数失败：' + (e.message || e));
    }
    totalPlayers = requested;
    lastWrittenBots = requested - 1;
    log('info', '已设为总人数 ' + totalPlayers + '（机器人 ' + (totalPlayers - 1) + '），下局开局生效');
    return successResult();
  }

  function disable() {
    stopEntityDiagnostic();
    var restored = true;
    if (patchApplied && gameAssembly) {
      try {
        var layout = inspectLayout();
        if (layout.active && layout.bots === lastWrittenBots) {
          // Both verified builds have exactly this disk baseline. An orphaned
          // prior patch can therefore be cleanly disabled after being adopted.
          writeState({ bot: [0x75, 0x05], conversion: 0x75, name: 0x74, bots: 50 });
          if (!restoreBaselineProfile()) restored = false;
        } else if (layout.active) {
          restored = false;
          log('error', '人数已被另一份修改器改变，未覆盖其设置；请关闭所有修改器后重启游戏');
        }
      } catch (e) {
        restored = false;
        log('error', '人数补丁恢复失败，请重启游戏：' + (e.message || e));
      }
    }
    enabled = false;
    patchApplied = false;
    lastWrittenBots = null;
    adoptedPatch = false;
    if (restored && profilePatchedByThisScript && !restoreBaselineProfile()) restored = false;
    status(false);
    if (restored) log('info', '已禁用；下一局恢复游戏原本人数逻辑。');
    return { ok: restored, enabled: false };
  }

  rpc.exports = {
    enable: enable,
    disable: disable,
    setconfig: applyConfig,
    setConfig: applyConfig,
    set_config: applyConfig,
    status: function () { return { enabled: enabled, total_players: totalPlayers, bots: totalPlayers - 1,
      patch_applied: patchApplied,
      max_total_players: maxTotalPlayers, adopted_existing_patch: adoptedPatch,
      patch_profile: activePatchProfile, profile_patched_by_this_script: profilePatchedByThisScript,
      version: 'room-count-100-hotfix4' }; },
    cleanup: disable,
    dispose: disable
  };
})();
