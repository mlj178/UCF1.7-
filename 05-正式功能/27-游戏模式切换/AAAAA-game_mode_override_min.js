// AAAAA-game_mode_override_min.js
// feature_id: game_mode_override
// Windows x86 IL2CPP minimum implementation.

(function () {
  'use strict';

  var RVA = {
    MapAsset_ApplyGameSetting: 0x00AE82B0,
    UI_GameRoom_OnStartGameBtnDown: 0x00B25F40,
    MapManager_Awake: 0x00AEB2B0,
    MapManager_GetSpawnPoint: 0x00AEB6E0,
    GameManager_TypeInfo: 0x00E2933C,
    WriteBarrier: 0x001677F0
  };

  var OFF = {
    Il2CppClass_static_fields: 0x5C,
    UI_GameRoom_mapDatas: 0x2C,
    MapAsset_gameMode: 0x0C,
    MapAsset_gameModePrefab: 0x10,
    GameManager_gameMode: 0x04,
    GameManager_weaponLimited: 0x08,
    GameManager_gameModePrefab: 0x10,
    MapManager_SP_BL: 0x10,
    MapManager_SP_GR: 0x14,
    MapManager_SP_Netural: 0x18,
    Array_length: 0x0C,
    Array_items: 0x10
  };

  var MODES = {
    team_death: { label: '团队竞技', gameMode: 0, weaponLimited: 0 },
    special: { label: '特殊战', gameMode: 2, weaponLimited: 0 },
    death_match: { label: '个人竞技', gameMode: 1, weaponLimited: 0 },
    nano3: { label: '生化3', gameMode: 3, weaponLimited: 0 },
    nano4: { label: '多人生化（生化4）', gameMode: 4, weaponLimited: 0 },
    nano6: { label: '生化6', gameMode: 5, weaponLimited: 0 },
    nano4_terminator: { label: '生化4终结者', gameMode: 6, weaponLimited: 0 },
    sniper: { label: '狙击战', gameMode: 0, weaponLimited: 3 },
    handgun: { label: '手枪战', gameMode: 0, weaponLimited: 2 }
  };

  var Runtime = {
    enabled: false,
    modeKey: 'team_death',
    gameRoom: null,
    mapManager: null,
    startDepth: 0,
    hooks: [],
    hookInstalled: false,
    applyCount: 0,
    neutralSpawnFallbackCount: 0,
    neutralSpawnFallbackLast: null,
    lastError: null,
    lastApplied: null,
    base: null,
    writeBarrier: null
  };

  function sendLog(level, message) {
    try {
      console.log('[game_mode_override][' + level + '] ' + message);
      send({ type: 'log', level: level, module: 'game_mode_override', message: message });
    } catch (_) {
    }
  }

  function fail(message, error) {
    Runtime.lastError = message + (error && error.message ? ': ' + error.message : '');
    sendLog('error', Runtime.lastError);
    return { ok: false, msg: Runtime.lastError };
  }

  function readPointer(addr) {
    try {
      if (!addr || addr.isNull()) return null;
      var value = addr.readPointer();
      return value && !value.isNull() ? value : null;
    } catch (_) {
      return null;
    }
  }

  function readS32(addr) {
    try {
      if (!addr || addr.isNull()) return null;
      return addr.readS32();
    } catch (_) {
      return null;
    }
  }

  function getGameAssembly() {
    if (Runtime.base) return Runtime.base;
    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) return null;
    Runtime.base = mod.base;
    return Runtime.base;
  }

  function resolveGameManagerStaticFields() {
    var base = getGameAssembly();
    if (!base) return null;
    var klass = readPointer(base.add(RVA.GameManager_TypeInfo));
    if (!klass) return null;
    return readPointer(klass.add(OFF.Il2CppClass_static_fields));
  }

  function findTargetMapAsset(gameRoom, targetGameMode) {
    if (!gameRoom || gameRoom.isNull()) return null;
    var mapDatas = readPointer(gameRoom.add(OFF.UI_GameRoom_mapDatas));
    if (!mapDatas) return null;

    var length = readS32(mapDatas.add(OFF.Array_length));
    if (length === null || length < 1 || length > 64) return null;

    for (var i = 0; i < length; i++) {
      var asset = readPointer(mapDatas.add(OFF.Array_items + i * Process.pointerSize));
      if (!asset) continue;
      var gameMode = readS32(asset.add(OFF.MapAsset_gameMode));
      if (gameMode === targetGameMode) return asset;
    }
    return null;
  }

  function getArrayLength(arrayPtr) {
    var length = readS32(arrayPtr.add(OFF.Array_length));
    if (length === null || length < 1 || length > 4096) return 0;
    return length;
  }

  function pickFallbackSpawnArray(mapManager) {
    var bl = readPointer(mapManager.add(OFF.MapManager_SP_BL));
    var gr = readPointer(mapManager.add(OFF.MapManager_SP_GR));
    var blLength = bl ? getArrayLength(bl) : 0;
    var grLength = gr ? getArrayLength(gr) : 0;

    if (blLength >= grLength && blLength > 0) {
      return { ptr: bl, source: 'SP_BL', length: blLength };
    }
    if (grLength > 0) {
      return { ptr: gr, source: 'SP_GR', length: grLength };
    }
    return null;
  }

  function ensureDeathMatchNeutralSpawnFallback(reason) {
    if (!Runtime.enabled || Runtime.modeKey !== 'death_match') return false;
    if (!Runtime.mapManager || Runtime.mapManager.isNull()) return false;

    var neutralField = Runtime.mapManager.add(OFF.MapManager_SP_Netural);
    var neutral = readPointer(neutralField);
    if (neutral && getArrayLength(neutral) > 0) return false;

    var fallback = pickFallbackSpawnArray(Runtime.mapManager);
    if (!fallback) {
      Runtime.neutralSpawnFallbackLast = 'SP_Netural 为空，且 SP_BL/SP_GR 也不可用';
      sendLog('warn', Runtime.neutralSpawnFallbackLast);
      return false;
    }

    if (!writeManagedReference(neutralField, fallback.ptr)) {
      Runtime.neutralSpawnFallbackLast = 'SP_Netural 兜底写入失败';
      sendLog('warn', Runtime.neutralSpawnFallbackLast);
      return false;
    }

    Runtime.neutralSpawnFallbackCount += 1;
    Runtime.neutralSpawnFallbackLast = fallback.source + '[' + fallback.length + '] via ' + reason;
    sendLog('warn', '个人竞技中立出生点缺失，已临时借用 ' + fallback.source + '（' + fallback.length + ' 个）');
    return true;
  }

  function writeManagedReference(fieldAddr, value) {
    if (!fieldAddr || fieldAddr.isNull() || !value || value.isNull()) return false;
    fieldAddr.writePointer(value);
    Runtime.writeBarrier(fieldAddr, value);
    return fieldAddr.readPointer().equals(value);
  }

  function applySelectedMode() {
    if (!Runtime.enabled) return { ok: true, changed: false, msg: '功能未启用' };

    var selected = MODES[Runtime.modeKey];
    if (!selected) return fail('未知模式: ' + Runtime.modeKey);

    var targetAsset = findTargetMapAsset(Runtime.gameRoom, selected.gameMode);
    if (!targetAsset) return fail('找不到目标模式 MapAsset: ' + selected.label);

    var targetPrefab = readPointer(targetAsset.add(OFF.MapAsset_gameModePrefab));
    if (!targetPrefab) return fail('目标模式 gameModePrefab 为空: ' + selected.label);

    var staticFields = resolveGameManagerStaticFields();
    if (!staticFields) return fail('GameManager.static_fields 尚未初始化');

    try {
      staticFields.add(OFF.GameManager_gameMode).writeS32(selected.gameMode);
      staticFields.add(OFF.GameManager_weaponLimited).writeS32(selected.weaponLimited);
      if (!writeManagedReference(staticFields.add(OFF.GameManager_gameModePrefab), targetPrefab)) {
        return fail('gameModePrefab 写入校验失败');
      }

      var modeReadBack = staticFields.add(OFF.GameManager_gameMode).readS32();
      var limitReadBack = staticFields.add(OFF.GameManager_weaponLimited).readS32();
      if (modeReadBack !== selected.gameMode || limitReadBack !== selected.weaponLimited) {
        return fail('模式字段写入校验失败');
      }

      Runtime.applyCount += 1;
      Runtime.lastError = null;
      Runtime.lastApplied = {
        key: Runtime.modeKey,
        label: selected.label,
        gameMode: selected.gameMode,
        weaponLimited: selected.weaponLimited,
        prefab: targetPrefab.toString(),
        count: Runtime.applyCount
      };
      sendLog('success', '下一局模式已替换为 ' + selected.label);
      return { ok: true, changed: true, msg: '已替换为 ' + selected.label };
    } catch (e) {
      return fail('覆盖 GameManager 模式失败', e);
    }
  }

  function installHooks() {
    if (Runtime.hookInstalled) return true;
    var base = getGameAssembly();
    if (!base) return false;

    if (Process.pointerSize !== 4) {
      fail('仅支持 32 位游戏进程，pointerSize=' + Process.pointerSize);
      return false;
    }

    try {
      Runtime.writeBarrier = new NativeFunction(
        base.add(RVA.WriteBarrier),
        'void',
        ['pointer', 'pointer'],
        'mscdecl'
      );

      Runtime.hooks.push(Interceptor.attach(base.add(RVA.UI_GameRoom_OnStartGameBtnDown), {
        onEnter: function (args) {
          Runtime.gameRoom = args[0];
          Runtime.mapManager = null;
          Runtime.startDepth += 1;
        },
        onLeave: function () {
          Runtime.startDepth = Math.max(0, Runtime.startDepth - 1);
        }
      }));

      Runtime.hooks.push(Interceptor.attach(base.add(RVA.MapAsset_ApplyGameSetting), {
        onLeave: function () {
          if (Runtime.enabled && Runtime.startDepth > 0) applySelectedMode();
        }
      }));

      Runtime.hooks.push(Interceptor.attach(base.add(RVA.MapManager_Awake), {
        onEnter: function (args) {
          Runtime.mapManager = args[0];
        }
      }));

      Runtime.hooks.push(Interceptor.attach(base.add(RVA.MapManager_GetSpawnPoint), {
        onEnter: function (args) {
          var team = args[1].toInt32();
          if (team === 2) ensureDeathMatchNeutralSpawnFallback('GetSpawnPoint');
        }
      }));

      Runtime.hookInstalled = true;
      Runtime.lastError = null;
      sendLog('success', 'Hook 已安装，等待点击游戏的开始按钮');
      return true;
    } catch (e) {
      while (Runtime.hooks.length) {
        try {
          Runtime.hooks.pop().detach();
        } catch (_) {
        }
      }
      Runtime.hookInstalled = false;
      fail('Hook 安装失败', e);
      return false;
    }
  }

  function statusObject() {
    var selected = MODES[Runtime.modeKey];
    return {
      ok: Runtime.hookInstalled,
      featureId: 'game_mode_override',
      enabled: Runtime.enabled,
      modeKey: Runtime.modeKey,
      modeLabel: selected ? selected.label : Runtime.modeKey,
      hookInstalled: Runtime.hookInstalled,
      applyCount: Runtime.applyCount,
      lastApplied: Runtime.lastApplied,
      neutralSpawnFallbackCount: Runtime.neutralSpawnFallbackCount,
      neutralSpawnFallbackLast: Runtime.neutralSpawnFallbackLast,
      lastError: Runtime.lastError,
      pointerSize: Process.pointerSize
    };
  }

  function cleanupRuntime() {
    Runtime.enabled = false;
    while (Runtime.hooks.length) {
      try {
        Runtime.hooks.pop().detach();
      } catch (_) {
      }
    }
    Runtime.hookInstalled = false;
    Runtime.gameRoom = null;
    Runtime.mapManager = null;
    Runtime.startDepth = 0;
    sendLog('info', 'cleanup 完成；不修改已经开始的当前对局');
    return statusObject();
  }

  rpc.exports = {
    setconfig: function (config) {
      config = config || {};
      if (config.mode_key !== undefined) {
        if (!MODES[config.mode_key]) return fail('不支持的 mode_key: ' + config.mode_key);
        Runtime.modeKey = config.mode_key;
      }
      if (config.enabled !== undefined) Runtime.enabled = !!config.enabled;
      Runtime.lastError = null;
      return statusObject();
    },

    enable: function () {
      Runtime.enabled = true;
      Runtime.lastError = null;
      return statusObject();
    },

    disable: function () {
      Runtime.enabled = false;
      return statusObject();
    },

    status: function () {
      return statusObject();
    },

    cleanup: function () {
      return cleanupRuntime();
    },

    dispose: function () {
      return cleanupRuntime();
    }
  };

  installHooks();
})();
