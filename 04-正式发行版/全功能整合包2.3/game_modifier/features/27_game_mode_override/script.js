// AAAAA-game_mode_override_min.js
// feature_id: game_mode_override
// Windows x86 IL2CPP minimum implementation.

(function () {
  'use strict';

  var RVA = {
    MapAsset_ApplyGameSetting: 0x00AE82B0,
    UI_GameRoom_OnStartGameBtnDown: 0x00B25F40,
    UI_GameRoom_GenerateBotClient: 0x00B25B80,
    MapManager_Awake: 0x00AEB2B0,
    MapManager_GetSpawnPoint: 0x00AEB6E0,
    MapManager_GetSupplyBoxPoint: 0x00AEB8A0,
    GameManager_AddPlayers: 0x00AF9DE0,
    GameManager_AddPlayer: 0x00AF9A90,
    Player_Spawn: 0x00B53760,
    Player_OnEntityDeath: 0x00B51210,
    Player_Respawn: 0x00B527A0,
    ModeBase_UpdateTimeUI: 0x00AF6930,
    ModeBase_OnStartNewGameRound: 0x00AF5B30,
    ModeBase_Nano_OnStartNewGameRound: 0x00AF15D0,
    ModeBase_Nano_CheckRoundOver: 0x00AEF8A0,
    GameManager_GameRoundEnd: 0x00AFAA40,
    GameManager_DeathEventBroadcast: 0x00AFA400,
    MapManager_NewGameRoundStart: 0x00AEBCB0,
    ModeBase_Nano_DeathEvent: 0x00AEF9E0,
    Mode_Nano4_DeathEvent: 0x00B41920,
    Mode_Nano4_Terminator_DeathEvent: 0x00B437E0,
    Mode_Nano6_DeathEvent: 0x00B47A20,
    Mode_TeamDeath_DeathEvent: 0x00B4A400,
    StartGenerateSupplyBox: 0x00B45AA0,
    Mode_Nano4_Terminator_UpgrandeBoxGenerator: 0x00B45E00,
    UnityEngine_MonoBehaviour_StartCoroutine_Auto: 0x004E8830,
    ManagedObject_New: 0x00167D20,
    List_int_ctor: 0x00430E90,
    List_int_Add: 0x009EF780,
    GameManager_GiveWeapon: 0x00AFB390,
    GameManager_GiveWeaponByBag: 0x00AFB2A0,
    GameManager_GetWpnData: 0x00AFB130,
    GameManager_get_alivePlayerCount_BL: 0x00AFD930,
    GameManager_get_alivePlayerCount_GR: 0x00AFD9B0,
    GameManager_TypeInfo: 0x00E2933C,
    ModeBase_TypeInfo: 0x00E2CC54,
    ModeBase_Nano_TypeInfo: 0x00E2CC74,
    Mode_Nano4_Terminator_TypeInfo: 0x00E2CCB4,
    MapAsset_Nano_TypeInfo: 0x00E2C4F4,
    MapAsset_TeamDeath_TypeInfo: 0x00E2C534,
    UI_GameRoom_TypeInfo: 0x00E32C80,
    System_Collections_Generic_List_int_TypeInfo: 0x00E1F6D8,
    WriteBarrier: 0x001677F0
  };

  var OFF = {
    Il2CppClass_static_fields: 0x5C,
    UI_GameRoom_players: 0x00,
    UI_GameRoom_mapDatas: 0x2C,
    MapAsset_gameMode: 0x0C,
    MapAsset_gameModePrefab: 0x10,
    MapAsset_datas: 0x14,
    MapAsset_Map_size: 0x1C,
    MapAsset_Map_gameModePrefabOverride: 0x14,
    MapAsset_Map_weaponLimited: 0x18,
    GameManager_gameMode: 0x04,
    GameManager_weaponLimited: 0x08,
    GameManager_revengeEnable: 0x0C,
    GameManager_gameModePrefab: 0x10,
    GameManager_gameRoundOver: 0x20,
    ModeBase_targetRound: 0x00,
    ModeBase_targetScore: 0x04,
    ModeBase_gameTime_X: 0x08,
    ModeBase_gameTime_Y: 0x0C,
    ModeBase_respawnTime: 0x10,
    ModeBase_score_X: 0x0C,
    ModeBase_score_Y: 0x10,
    ModeBase_currentRound: 0x14,
    ModeBase_restGameTime_X: 0x34,
    ModeBase_restGameTime_Y: 0x38,
    ModeBase_playerCountBL: 0x48,
    ModeBase_playerCountGR: 0x4C,
    ModeBase_aliveCountBL: 0x50,
    ModeBase_aliveCountGR: 0x54,
    ModeBase_Nano_thisRoundPlayer: 0xA4,
    ModeBase_Nano_respawningPlayer: 0xAC,
    Mode_Nano4_Terminator_attributeAsset: 0xD8,
    Mode_Nano4_Terminator_attribute_Nano: 0xE0,
    Mode_Nano4_Terminator_attribute_Human: 0xE4,
    Nano4TAttributeAsset_attributes: 0x14,
    Nano4TAttribute_id: 0x0C,
    MapManager_SP_BL: 0x10,
    MapManager_SP_GR: 0x14,
    MapManager_SP_Netural: 0x18,
    MapManager_SP_SupplyBox: 0x1C,
    MapManager_SP_RedBox: 0x20,
    MapManager_SP_BlueBox: 0x24,
    MapManager_IDList_SupplyBox: 0x28,
    MapManager_IDList_RedBox: 0x2C,
    MapManager_IDList_BlueBox: 0x30,
    ClientData_defaultWpnBagID: 0x08,
    ClientData_wpnBags: 0x0C,
    ClientData_joinTeam: 0x18,
    ClientData_isBot: 0x1C,
    Entity_team: 0x20,
    Player_clientData: 0x94,
    Player_isRespawning: 0xD8,
    Weapon_data: 0x68,
    WeaponData_wpnIndex: 0x0C,
    WeaponData_wpnClass: 0x10,
    WeaponData_weaponName: 0x14,
    WeaponData_targetSlot: 0x8C,
    WeaponData_slotType: 0x90,
    Dropdown_m_Value: 0xC4,
    MapAsset_Nano_GameTime_Nano4_X: 0x00,
    MapAsset_Nano_GameTime_Nano4_Y: 0x04,
    MapAsset_Nano_GameTime_Nano4Terminator_X: 0x08,
    MapAsset_Nano_GameTime_Nano4Terminator_Y: 0x0C,
    MapAsset_Nano_RoundDatas: 0x10,
    MapAsset_TeamDeath_KillDatas: 0x00,
    MapAsset_TeamDeath_KillConditionTime_X: 0x08,
    MapAsset_TeamDeath_KillConditionTime_Y: 0x0C,
    MapAsset_TeamDeath_TimeDatas: 0x10,
    List_items: 0x08,
    List_size: 0x0C,
    Array_length: 0x0C,
    Array_items: 0x10
  };

  var MODES = {
    team_death: { label: '团队竞技', gameMode: 0, weaponLimited: 0 },
    special: { label: '刀战', gameMode: 2, weaponLimited: 1, weaponOnly: true, teamDeathOnNano: true },
    nano4: { label: '生化4（普通生化）', gameMode: 4, weaponLimited: 0 },
    nano6: { label: '生化6（剑客模式）', gameMode: 5, weaponLimited: 0 },
    nano4_terminator: { label: '生化4终结者（多人生化）', gameMode: 6, weaponLimited: 0 },
    sniper: { label: '狙击战', gameMode: 0, weaponLimited: 3, weaponOnly: true, teamDeathOnNano: true },
    handgun: { label: '手枪战', gameMode: 0, weaponLimited: 2, weaponOnly: true, teamDeathOnNano: true }
  };

  var SNIPER_BOT_FALLBACK_WEAPON_INDEX = 2568;
  var HANDGUN_BOT_FALLBACK_WEAPON_INDEX = 20;
  var KNIFE_BOT_FALLBACK_WEAPON_INDEX = 244;
  var TERMINATOR_SUPPLY_GHOST_ATTR_ID = 8;
  var TERMINATOR_SUPPLY_HUMAN_ATTR_ID = 18;
  var SUPPLY_BOX_TYPE_YELLOW = 0;
  var SUPPLY_BOX_TYPE_RED = 1;
  var SUPPLY_BOX_TYPE_BLUE = 2;
  var TERMINATOR_UPGRADE_BOX_RED_DELAY = 62;
  var TERMINATOR_UPGRADE_BOX_BLUE_DELAY = 91;
  var TERMINATOR_UPGRADE_BOX_RED_TEAM = 0;
  var TERMINATOR_UPGRADE_BOX_BLUE_TEAM = 1;

  var Runtime = {
    enabled: false,
    modeKey: 'team_death',
    gameRoom: null,
    mapManager: null,
    modeBase: null,
    lastDropdowns: null,
    lastMapID: null,
    lastSourceMapMode: null,
    deferModeApplyUntilBotGeneration: false,
    deferredModeApplyReason: null,
    startDepth: 0,
    hooks: [],
    hookInstalled: false,
    applyCount: 0,
    neutralSpawnFallbackCount: 0,
    neutralSpawnFallbackLast: null,
    teamSpawnFallbackCount: 0,
    teamSpawnFallbackLast: null,
    supplyBoxSpawnFallbackCount: 0,
    supplyBoxSpawnFallbackLast: null,
    supplyBoxPipelineDiagnostics: 0,
    supplyBoxPipelineLast: null,
    supplyBoxPointRequests: 0,
    supplyBoxPointLast: null,
    ruleSyncCount: 0,
    ruleSyncLast: null,
    terminatorSupplyCompatHits: 0,
    terminatorSupplyCompatLast: null,
    terminatorSupplyAttrLoadCount: 0,
    terminatorSupplyAttrPtrs: {},
    upgradeBoxGeneratorNativeCount: 0,
    upgradeBoxGeneratorNativeKeys: {},
    upgradeBoxGeneratorNativeLast: null,
    upgradeBoxGeneratorFallbackCount: 0,
    upgradeBoxGeneratorFallbackKeys: {},
    upgradeBoxGeneratorFallbackLast: null,
    botSniperOverrideHits: 0,
    botSniperOverrideLast: null,
    lastError: null,
    lastApplied: null,
    probe: {
      enabled: false,
      level: 'basic',
      generateBotHits: 0,
      addPlayersHits: 0,
      addPlayerHits: 0,
      spawnHits: 0,
      respawnHits: 0,
      getSpawnPointMissingHits: 0,
      lifecycleHits: 0,
      deathEventHits: 0,
      roundBoundaryHits: 0,
      weaponBagHits: 0,
      giveWeaponHits: 0,
      giveWeaponByBagHits: 0,
      weaponMismatchHits: 0,
      lastLifecycleKey: null,
      lastLifecycleLogMs: 0,
      recent: [],
      last: null
    },
    base: null,
    writeBarrier: null,
    aliveCountBL: null,
    aliveCountGR: null,
    getWpnData: null,
    createUpgradeBoxGenerator: null,
    startCoroutineAuto: null,
    objectNew: null,
    listIntCtor: null,
    listIntAdd: null,
    weaponDataCache: {},
    weaponProbe: {
      giveWeaponByBagDepth: 0,
      grantsByPlayer: {},
      grantOrder: []
    }
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

  function readU8(addr) {
    try {
      if (!addr || addr.isNull()) return null;
      return addr.readU8();
    } catch (_) {
      return null;
    }
  }

  function readFloat(addr) {
    try {
      if (!addr || addr.isNull()) return null;
      return addr.readFloat();
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

  function resolveStaticFields(typeInfoRva) {
    var base = getGameAssembly();
    if (!base) return null;
    var klass = readPointer(base.add(typeInfoRva));
    if (!klass) return null;
    return readPointer(klass.add(OFF.Il2CppClass_static_fields));
  }

  function resolveGameManagerStaticFields() {
    return resolveStaticFields(RVA.GameManager_TypeInfo);
  }

  function resolveModeBaseStaticFields() {
    return resolveStaticFields(RVA.ModeBase_TypeInfo);
  }

  function resolveMapAssetNanoStaticFields() {
    return resolveStaticFields(RVA.MapAsset_Nano_TypeInfo);
  }

  function resolveMapAssetTeamDeathStaticFields() {
    return resolveStaticFields(RVA.MapAsset_TeamDeath_TypeInfo);
  }

  function modeLabelByValue(gameMode, weaponLimited) {
    if (weaponLimited === 1) return '当前地图规则 + 刀限制';
    if (weaponLimited === 3) return '当前地图规则 + 狙击限制';
    if (weaponLimited === 2) return '当前地图规则 + 手枪限制';

    for (var key in MODES) {
      if (!Object.prototype.hasOwnProperty.call(MODES, key)) continue;
      var mode = MODES[key];
      if (mode.gameMode === gameMode && mode.useTargetMapWeaponLimited) return mode.label;
      if (mode.gameMode === gameMode && mode.weaponLimited === weaponLimited) return mode.label;
    }
    return '未知(' + gameMode + '/' + weaponLimited + ')';
  }

  function teamLabel(team) {
    if (team === 0) return 'BL(0)';
    if (team === 1) return 'GR(1)';
    if (team === 2) return 'Neutral(2)';
    if (team === null || team === undefined) return 'unknown';
    return 'team(' + team + ')';
  }

  function isNanoGameModeValue(gameMode) {
    return gameMode >= 3 && gameMode <= 6;
  }

  function currentModeLooksNano() {
    var mode = summarizeGameManagerMode();
    return mode && mode.ready && isNanoGameModeValue(mode.gameMode);
  }

  function safePtrText(ptr) {
    try {
      if (!ptr || ptr.isNull()) return 'null';
      return ptr.toString();
    } catch (_) {
      return 'unknown';
    }
  }

  function readIl2CppString(strPtr, maxLen) {
    try {
      if (!strPtr || strPtr.isNull()) return null;
      var length = readS32(strPtr.add(0x08));
      if (length === null || length < 0 || length > 512) return null;
      var count = Math.min(length, maxLen || 64);
      var text = strPtr.add(0x0C).readUtf16String(count);
      if (length > count) text += '...';
      return text;
    } catch (_) {
      return null;
    }
  }

  function weaponClassLabel(wpnClass) {
    if (wpnClass === 0) return 'Rifle(0)';
    if (wpnClass === 1) return 'Sniper(1)';
    if (wpnClass === 2) return 'MachineGun(2)';
    if (wpnClass === 3) return 'SubmachineGun(3)';
    if (wpnClass === 4) return 'ShotGun(4)';
    if (wpnClass === 5) return 'Pistol(5)';
    if (wpnClass === 6) return 'Knife(6)';
    if (wpnClass === 7) return 'Grenade(7)';
    if (wpnClass === 8) return 'FlashBang(8)';
    if (wpnClass === 9) return 'SmokeGrenade(9)';
    if (wpnClass === null || wpnClass === undefined) return 'unknown';
    return 'class(' + wpnClass + ')';
  }

  function expectedWeaponClassForSelectedMode() {
    if (Runtime.modeKey === 'sniper') return 1;
    if (Runtime.modeKey === 'handgun') return 5;
    if (Runtime.modeKey === 'special') return 6;
    return null;
  }

  function fallbackWeaponIndexForSelectedMode() {
    if (Runtime.modeKey === 'sniper') return SNIPER_BOT_FALLBACK_WEAPON_INDEX;
    if (Runtime.modeKey === 'handgun') return HANDGUN_BOT_FALLBACK_WEAPON_INDEX;
    if (Runtime.modeKey === 'special') return KNIFE_BOT_FALLBACK_WEAPON_INDEX;
    return null;
  }

  function summarizeWeaponData(dataPtr, requestedIndex) {
    var result = {
      ok: false,
      requestedIndex: requestedIndex,
      dataPtr: safePtrText(dataPtr),
      wpnIndex: requestedIndex,
      wpnClass: null,
      classLabel: 'unknown',
      targetSlot: null,
      slotType: null,
      name: null
    };
    if (!dataPtr || dataPtr.isNull()) return result;

    result.ok = true;
    result.wpnIndex = readS32(dataPtr.add(OFF.WeaponData_wpnIndex));
    if (result.wpnIndex === null) result.wpnIndex = requestedIndex;
    result.wpnClass = readS32(dataPtr.add(OFF.WeaponData_wpnClass));
    result.classLabel = weaponClassLabel(result.wpnClass);
    result.targetSlot = readS32(dataPtr.add(OFF.WeaponData_targetSlot));
    result.slotType = readS32(dataPtr.add(OFF.WeaponData_slotType));
    result.name = readIl2CppString(readPointer(dataPtr.add(OFF.WeaponData_weaponName)), 48);
    return result;
  }

  function lookupWeaponDataByIndex(weaponIndex) {
    if (weaponIndex === null || weaponIndex === undefined || weaponIndex < 0) {
      return summarizeWeaponData(null, weaponIndex);
    }
    var cacheKey = String(weaponIndex);
    if (Runtime.weaponDataCache[cacheKey]) return Runtime.weaponDataCache[cacheKey];

    var result = summarizeWeaponData(null, weaponIndex);
    try {
      if (Runtime.getWpnData) {
        var outData = Memory.alloc(Process.pointerSize);
        outData.writePointer(ptr(0));
        var ok = Runtime.getWpnData(weaponIndex, outData, ptr(0));
        var dataPtr = readPointer(outData);
        if (ok && dataPtr) result = summarizeWeaponData(dataPtr, weaponIndex);
      }
    } catch (e) {
      result.error = e.message || String(e);
    }

    if (result.ok) Runtime.weaponDataCache[cacheKey] = result;
    return result;
  }

  function summarizeWeaponObject(weaponPtr, requestedIndex) {
    var result = summarizeWeaponData(null, requestedIndex);
    result.weaponPtr = safePtrText(weaponPtr);
    if (!weaponPtr || weaponPtr.isNull()) return result;

    var dataPtr = readPointer(weaponPtr.add(OFF.Weapon_data));
    result = summarizeWeaponData(dataPtr, requestedIndex);
    result.weaponPtr = safePtrText(weaponPtr);
    return result;
  }

  function weaponProbeText(weapon) {
    if (!weapon) return 'weapon=unknown';
    var text = 'weaponIndex=' + weapon.wpnIndex + ', class=' + weapon.classLabel;
    if (weapon.name) text += ', name=' + weapon.name;
    if (weapon.targetSlot !== null) text += ', targetSlot=' + weapon.targetSlot;
    if (weapon.slotType !== null) text += ', slotType=' + weapon.slotType;
    return text;
  }

  function getListSize(listPtr) {
    var size = readS32(listPtr.add(OFF.List_size));
    if (size === null || size < 0 || size > 4096) return null;
    return size;
  }

  function clampArrayIndex(index, length, defaultIndex) {
    if (length < 1) return null;
    if (index === null || index === undefined || index < 0) return defaultIndex < length ? defaultIndex : 0;
    if (index >= length) return length - 1;
    return index;
  }

  function readIntArrayElement(arrayPtr, index, fallbackValues, defaultIndex) {
    var fallbackLength = fallbackValues ? fallbackValues.length : 0;
    if (arrayPtr) {
      var length = getArrayLength(arrayPtr);
      var chosen = clampArrayIndex(index, length, defaultIndex || 0);
      if (chosen !== null) {
        var value = readS32(arrayPtr.add(OFF.Array_items + chosen * 4));
        if (value !== null) return { value: value, source: 'static[' + chosen + ']' };
      }
    }

    var fallbackChosen = clampArrayIndex(index, fallbackLength, defaultIndex || 0);
    if (fallbackChosen === null) return { value: null, source: 'missing' };
    return { value: fallbackValues[fallbackChosen], source: 'fallback[' + fallbackChosen + ']' };
  }

  function readVector2ArrayElement(arrayPtr, index, fallbackValues, defaultIndex) {
    var fallbackLength = fallbackValues ? fallbackValues.length : 0;
    if (arrayPtr) {
      var length = getArrayLength(arrayPtr);
      var chosen = clampArrayIndex(index, length, defaultIndex || 0);
      if (chosen !== null) {
        var base = arrayPtr.add(OFF.Array_items + chosen * 8);
        var x = readS32(base);
        var y = readS32(base.add(4));
        if (x !== null && y !== null) return { value: { minute: x, second: y }, source: 'static[' + chosen + ']' };
      }
    }

    var fallbackChosen = clampArrayIndex(index, fallbackLength, defaultIndex || 0);
    if (fallbackChosen === null) return { value: null, source: 'missing' };
    return { value: fallbackValues[fallbackChosen], source: 'fallback[' + fallbackChosen + ']' };
  }

  function readDropdownValue(dropdownsPtr, index, fallback) {
    try {
      if (!dropdownsPtr || dropdownsPtr.isNull()) return fallback;
      var length = readS32(dropdownsPtr.add(OFF.Array_length));
      if (length === null || index < 0 || index >= length) return fallback;
      var dropdown = readPointer(dropdownsPtr.add(OFF.Array_items + index * Process.pointerSize));
      if (!dropdown) return fallback;
      var value = readS32(dropdown.add(OFF.Dropdown_m_Value));
      return value === null ? fallback : value;
    } catch (_) {
      return fallback;
    }
  }

  function readAlivePlayerCountsFromGameManager() {
    try {
      if (!Runtime.aliveCountBL || !Runtime.aliveCountGR) return { bl: null, gr: null };
      return {
        bl: Runtime.aliveCountBL(ptr(0)),
        gr: Runtime.aliveCountGR(ptr(0))
      };
    } catch (e) {
      return { bl: null, gr: null, error: e.message || String(e) };
    }
  }

  function resolveRoomPlayersList() {
    var staticFields = resolveStaticFields(RVA.UI_GameRoom_TypeInfo);
    if (!staticFields) return null;
    return readPointer(staticFields.add(OFF.UI_GameRoom_players));
  }

  function summarizeClientDataList(listPtr) {
    var summary = {
      ptr: safePtrText(listPtr),
      size: null,
      bots: 0,
      humans: 0,
      nullItems: 0,
      teams: { bl: 0, gr: 0, neutral: 0, other: 0 },
      sampled: 0
    };
    if (!listPtr) return summary;

    var size = getListSize(listPtr);
    summary.size = size;
    if (size === null || size < 1) return summary;

    var items = readPointer(listPtr.add(OFF.List_items));
    if (!items) return summary;

    var arrayLength = readS32(items.add(OFF.Array_length));
    if (arrayLength === null || arrayLength < 1 || arrayLength > 4096) return summary;

    var count = Math.min(size, arrayLength, 64);
    for (var i = 0; i < count; i++) {
      var clientData = readPointer(items.add(OFF.Array_items + i * Process.pointerSize));
      if (!clientData) {
        summary.nullItems += 1;
        continue;
      }
      summary.sampled += 1;

      var isBot = readU8(clientData.add(OFF.ClientData_isBot));
      if (isBot) summary.bots += 1;
      else summary.humans += 1;

      var joinTeam = readS32(clientData.add(OFF.ClientData_joinTeam));
      if (joinTeam === 0) summary.teams.bl += 1;
      else if (joinTeam === 1) summary.teams.gr += 1;
      else if (joinTeam === 2) summary.teams.neutral += 1;
      else summary.teams.other += 1;
    }
    return summary;
  }

  function summarizeRoomPlayers() {
    return summarizeClientDataList(resolveRoomPlayersList());
  }

  function weaponClassShort(wpnClass) {
    if (wpnClass === 0) return 'Rifle';
    if (wpnClass === 1) return 'Sniper';
    if (wpnClass === 2) return 'MG';
    if (wpnClass === 3) return 'SMG';
    if (wpnClass === 4) return 'ShotGun';
    if (wpnClass === 5) return 'Pistol';
    if (wpnClass === 6) return 'Knife';
    if (wpnClass === 7) return 'Grenade';
    if (wpnClass === 8) return 'Flash';
    if (wpnClass === 9) return 'Smoke';
    return 'unknown';
  }

  function formatClassCounts(counts) {
    var parts = [];
    for (var key in counts) {
      if (!Object.prototype.hasOwnProperty.call(counts, key)) continue;
      parts.push(key + '=' + counts[key]);
    }
    return parts.length ? parts.join(',') : 'none';
  }

  function readIntArrayItems(arrayPtr, limit) {
    var result = [];
    if (!arrayPtr) return result;
    var length = getArrayLength(arrayPtr);
    var count = Math.min(length, limit || 16);
    for (var i = 0; i < count; i++) {
      var value = readS32(arrayPtr.add(OFF.Array_items + i * 4));
      result.push(value);
    }
    return result;
  }

  function summarizeClientWeaponBags(clientData) {
    var summary = {
      ok: false,
      ptr: safePtrText(clientData),
      defaultBagID: null,
      activeBagIndexGuess: null,
      bagCount: 0,
      bags: [],
      activeMain: null,
      mainClassCounts: {},
      reason: null
    };
    if (!clientData) {
      summary.reason = 'clientData 为空';
      return summary;
    }

    summary.defaultBagID = readS32(clientData.add(OFF.ClientData_defaultWpnBagID));
    var wpnBags = readPointer(clientData.add(OFF.ClientData_wpnBags));
    if (!wpnBags) {
      summary.reason = 'ClientData.wpnBags 为空';
      return summary;
    }

    var outerLength = getArrayLength(wpnBags);
    summary.bagCount = outerLength;
    if (outerLength < 1) {
      summary.reason = 'ClientData.wpnBags 长度为 0';
      return summary;
    }

    var bagLimit = Math.min(outerLength, 12);
    for (var i = 0; i < bagLimit; i++) {
      var inner = readPointer(wpnBags.add(OFF.Array_items + i * Process.pointerSize));
      var ids = readIntArrayItems(inner, 8);
      var weapons = [];
      for (var j = 0; j < ids.length; j++) {
        var weapon = lookupWeaponDataByIndex(ids[j]);
        weapons.push(weapon);
        if (j === 0) {
          var classKey = weaponClassShort(weapon.wpnClass);
          summary.mainClassCounts[classKey] = (summary.mainClassCounts[classKey] || 0) + 1;
        }
      }
      summary.bags.push({ index: i, ptr: safePtrText(inner), ids: ids, weapons: weapons });
    }

    var active = null;
    if (summary.defaultBagID !== null && summary.defaultBagID >= 1 && summary.defaultBagID <= summary.bags.length) active = summary.defaultBagID - 1;
    else if (summary.defaultBagID !== null && summary.defaultBagID >= 0 && summary.defaultBagID < summary.bags.length) active = summary.defaultBagID;
    else active = 0;
    summary.activeBagIndexGuess = active;
    if (summary.bags[active] && summary.bags[active].weapons.length) summary.activeMain = summary.bags[active].weapons[0];
    summary.ok = true;
    return summary;
  }

  function formatWeaponSlot(weapon) {
    if (!weapon) return 'unknown';
    return weapon.wpnIndex + '/' + weaponClassShort(weapon.wpnClass);
  }

  function formatBagSummary(bag) {
    if (!bag) return 'bag=unknown';
    var slots = [];
    for (var i = 0; i < bag.weapons.length; i++) slots.push(formatWeaponSlot(bag.weapons[i]));
    return bag.index + '[' + slots.join(',') + ']';
  }

  function probeRoomBotWeaponBags(stage) {
    if (!Runtime.enabled || !Runtime.probe.enabled) return;
    var expectedClass = expectedWeaponClassForSelectedMode();
    if (expectedClass === null && Runtime.probe.level !== 'verbose') return;

    var listPtr = resolveRoomPlayersList();
    var summary = {
      stage: stage,
      expectedClass: expectedClass,
      expectedClassLabel: weaponClassLabel(expectedClass),
      bots: 0,
      sampled: 0,
      activeMainClassCounts: {},
      mismatch: 0,
      unknown: 0,
      samples: []
    };
    Runtime.probe.weaponBagHits += 1;

    var size = listPtr ? getListSize(listPtr) : null;
    var items = listPtr ? readPointer(listPtr.add(OFF.List_items)) : null;
    var arrayLength = items ? readS32(items.add(OFF.Array_length)) : null;
    var count = size !== null && arrayLength !== null ? Math.min(size, arrayLength, 64) : 0;
    var sampleLimit = Runtime.probe.level === 'verbose' ? 24 : 8;

    for (var i = 0; i < count; i++) {
      var clientData = readPointer(items.add(OFF.Array_items + i * Process.pointerSize));
      if (!clientData) continue;
      var isBot = readU8(clientData.add(OFF.ClientData_isBot));
      if (!isBot) continue;

      summary.bots += 1;
      var bagInfo = summarizeClientWeaponBags(clientData);
      var joinTeam = readS32(clientData.add(OFF.ClientData_joinTeam));
      var activeClass = bagInfo.activeMain ? bagInfo.activeMain.wpnClass : null;
      var activeKey = weaponClassShort(activeClass);
      summary.activeMainClassCounts[activeKey] = (summary.activeMainClassCounts[activeKey] || 0) + 1;
      if (activeClass === null || activeClass === undefined) summary.unknown += 1;
      else if (expectedClass !== null && activeClass !== expectedClass) {
        summary.mismatch += 1;
        Runtime.probe.weaponMismatchHits += 1;
      }

      if (summary.samples.length < sampleLimit) {
        var bagTexts = [];
        for (var b = 0; b < bagInfo.bags.length; b++) bagTexts.push(formatBagSummary(bagInfo.bags[b]));
        summary.samples.push({
          roomIndex: i,
          team: teamLabel(joinTeam),
          defaultBagID: bagInfo.defaultBagID,
          activeBagIndexGuess: bagInfo.activeBagIndexGuess,
          activeMain: bagInfo.activeMain,
          bags: bagTexts.join(';')
        });
      }
      summary.sampled += 1;
    }

    Runtime.probe.lastWeaponBag = summary;
    var mode = summarizeGameManagerMode();
    sendLog(
      'info',
      '[weapon] ' + stage + ' | ' + (mode.ready ? mode.label : 'mode=not-ready') +
      ' | bot背包 bots=' + summary.bots +
      ', sampled=' + summary.sampled +
      ', activeMainClass=' + formatClassCounts(summary.activeMainClassCounts) +
      ', expected=' + summary.expectedClassLabel +
      ', mismatch=' + summary.mismatch +
      ', unknown=' + summary.unknown
    );

    for (var s = 0; s < summary.samples.length; s++) {
      var sample = summary.samples[s];
      sendLog(
        'info',
        '[weapon] ' + stage + '.sample | #' + sample.roomIndex +
        ' team=' + sample.team +
        ', defaultBagID=' + sample.defaultBagID +
        ', activeGuess=' + sample.activeBagIndexGuess +
        ', activeMain=' + weaponProbeText(sample.activeMain) +
        ' | bags=' + sample.bags
      );
    }
  }

  function summarizeSpawnArrays() {
    var result = { mapManager: safePtrText(Runtime.mapManager), bl: 0, gr: 0, neutral: 0 };
    if (!Runtime.mapManager || Runtime.mapManager.isNull()) return result;

    var bl = readPointer(Runtime.mapManager.add(OFF.MapManager_SP_BL));
    var gr = readPointer(Runtime.mapManager.add(OFF.MapManager_SP_GR));
    var neutral = readPointer(Runtime.mapManager.add(OFF.MapManager_SP_Netural));
    result.bl = bl ? getArrayLength(bl) : 0;
    result.gr = gr ? getArrayLength(gr) : 0;
    result.neutral = neutral ? getArrayLength(neutral) : 0;
    return result;
  }

  function spawnLengthForTeam(spawns, team) {
    if (team === 0) return spawns.bl;
    if (team === 1) return spawns.gr;
    if (team === 2) return spawns.neutral;
    return null;
  }

  function summarizeGameManagerMode() {
    var staticFields = resolveGameManagerStaticFields();
    if (!staticFields) return { ready: false };
    var gameMode = readS32(staticFields.add(OFF.GameManager_gameMode));
    var weaponLimited = readS32(staticFields.add(OFF.GameManager_weaponLimited));
    var roundOver = readU8(staticFields.add(OFF.GameManager_gameRoundOver));
    return {
      ready: true,
      gameMode: gameMode,
      weaponLimited: weaponLimited,
      label: modeLabelByValue(gameMode, weaponLimited),
      prefab: safePtrText(readPointer(staticFields.add(OFF.GameManager_gameModePrefab))),
      gameRoundOver: roundOver === null ? null : !!roundOver
    };
  }

  function summarizeModeBaseStatic() {
    var staticFields = resolveModeBaseStaticFields();
    if (!staticFields) return { ready: false };
    return {
      ready: true,
      targetRound: readS32(staticFields.add(OFF.ModeBase_targetRound)),
      targetScore: readS32(staticFields.add(OFF.ModeBase_targetScore)),
      gameTime: {
        minute: readS32(staticFields.add(OFF.ModeBase_gameTime_X)),
        second: readS32(staticFields.add(OFF.ModeBase_gameTime_Y))
      },
      respawnTime: readFloat(staticFields.add(OFF.ModeBase_respawnTime))
    };
  }

  function summarizeModeBaseInstance(modePtr, includeNanoExtra) {
    var result = {
      ptr: safePtrText(modePtr),
      currentRound: null,
      score: { left: null, right: null },
      restGameTime: { minute: null, second: null },
      playerCount: { bl: null, gr: null },
      aliveCount: { bl: null, gr: null },
      gameManagerAliveCount: { bl: null, gr: null },
      nano: null
    };
    result.gameManagerAliveCount = readAlivePlayerCountsFromGameManager();
    if (!modePtr || modePtr.isNull()) return result;

    result.currentRound = readS32(modePtr.add(OFF.ModeBase_currentRound));
    result.score.left = readS32(modePtr.add(OFF.ModeBase_score_X));
    result.score.right = readS32(modePtr.add(OFF.ModeBase_score_Y));
    result.restGameTime.minute = readS32(modePtr.add(OFF.ModeBase_restGameTime_X));
    result.restGameTime.second = readS32(modePtr.add(OFF.ModeBase_restGameTime_Y));
    result.playerCount.bl = readS32(modePtr.add(OFF.ModeBase_playerCountBL));
    result.playerCount.gr = readS32(modePtr.add(OFF.ModeBase_playerCountGR));
    result.aliveCount.bl = readS32(modePtr.add(OFF.ModeBase_aliveCountBL));
    result.aliveCount.gr = readS32(modePtr.add(OFF.ModeBase_aliveCountGR));

    if (includeNanoExtra) {
      var respawning = readPointer(modePtr.add(OFF.ModeBase_Nano_respawningPlayer));
      result.nano = {
        thisRoundPlayer: readS32(modePtr.add(OFF.ModeBase_Nano_thisRoundPlayer)),
        respawningPlayerSize: respawning ? getListSize(respawning) : null,
        respawningPlayerPtr: safePtrText(respawning)
      };
    }

    return result;
  }

  function summarizePlayer(playerPtr) {
    var result = {
      ptr: safePtrText(playerPtr),
      team: null,
      teamLabel: 'unknown',
      isRespawning: null,
      clientData: 'null',
      clientJoinTeam: null,
      clientJoinTeamLabel: 'unknown',
      clientIsBot: null
    };
    if (!playerPtr || playerPtr.isNull()) return result;

    var team = readS32(playerPtr.add(OFF.Entity_team));
    result.team = team;
    result.teamLabel = teamLabel(team);
    var respawning = readU8(playerPtr.add(OFF.Player_isRespawning));
    result.isRespawning = respawning === null ? null : !!respawning;

    var clientData = readPointer(playerPtr.add(OFF.Player_clientData));
    result.clientData = safePtrText(clientData);
    if (clientData) {
      var joinTeam = readS32(clientData.add(OFF.ClientData_joinTeam));
      var isBot = readU8(clientData.add(OFF.ClientData_isBot));
      result.clientJoinTeam = joinTeam;
      result.clientJoinTeamLabel = teamLabel(joinTeam);
      result.clientIsBot = isBot === null ? null : !!isBot;
    }
    return result;
  }

  function rememberProbe(stage, extra) {
    if (!Runtime.probe.enabled) return;

    var snapshot = {
      stage: stage,
      enabled: Runtime.enabled,
      selected: Runtime.modeKey,
      mode: summarizeGameManagerMode(),
      players: summarizeRoomPlayers(),
      spawns: summarizeSpawnArrays(),
      extra: extra || {}
    };
    Runtime.probe.last = snapshot;
    Runtime.probe.recent.push(snapshot);
    if (Runtime.probe.recent.length > 12) Runtime.probe.recent.shift();
  }

  function shortPlayerSummary(players) {
    if (!players) return 'players=unknown';
    return 'players=' + players.size +
      ', bots=' + players.bots +
      ', humans=' + players.humans +
      ', teams[BL/GR/N]=' + players.teams.bl + '/' + players.teams.gr + '/' + players.teams.neutral;
  }

  function shortSpawnSummary(spawns) {
    if (!spawns) return 'spawns=unknown';
    return 'spawns[BL/GR/N]=' + spawns.bl + '/' + spawns.gr + '/' + spawns.neutral;
  }

  function probeBotPipeline(stage, extra) {
    if (!Runtime.enabled || !Runtime.probe.enabled) return;
    rememberProbe(stage, extra);

    var last = Runtime.probe.last;
    var mode = last.mode && last.mode.ready ? last.mode.label : 'mode=not-ready';
    sendLog(
      'info',
      '[probe] ' + stage + ' | ' + mode + ' | ' +
      shortPlayerSummary(last.players) + ' | ' +
      shortSpawnSummary(last.spawns) +
      (extra && extra.note ? ' | ' + extra.note : '')
    );
  }

  function lifecycleKey(snapshot) {
    var mode = snapshot.mode || {};
    var rule = snapshot.rule || {};
    var inst = snapshot.instance || {};
    var nano = inst.nano || {};
    return [
      mode.gameMode,
      mode.weaponLimited,
      mode.gameRoundOver,
      rule.targetRound,
      rule.targetScore,
      rule.respawnTime,
      inst.currentRound,
      inst.score ? inst.score.left : null,
      inst.score ? inst.score.right : null,
      inst.aliveCount ? inst.aliveCount.bl : null,
      inst.aliveCount ? inst.aliveCount.gr : null,
      inst.gameManagerAliveCount ? inst.gameManagerAliveCount.bl : null,
      inst.gameManagerAliveCount ? inst.gameManagerAliveCount.gr : null,
      nano.respawningPlayerSize
    ].join('|');
  }

  function shortLifecycleSummary(snapshot) {
    var mode = snapshot.mode && snapshot.mode.ready ? snapshot.mode.label : 'mode=not-ready';
    var over = snapshot.mode && snapshot.mode.ready ? snapshot.mode.gameRoundOver : null;
    var rule = snapshot.rule || {};
    var inst = snapshot.instance || {};
    var nano = inst.nano || null;
    var text = mode +
      ' | roundOver=' + over +
      ' | targetRound=' + rule.targetRound +
      ', targetScore=' + rule.targetScore +
      ', respawnTime=' + rule.respawnTime +
      ' | currentRound=' + inst.currentRound +
      ', score=' + (inst.score ? inst.score.left + '/' + inst.score.right : 'unknown') +
      ', alive=' + (inst.gameManagerAliveCount ? inst.gameManagerAliveCount.bl + '/' + inst.gameManagerAliveCount.gr : 'unknown') +
      ', cachedAlive=' + (inst.aliveCount ? inst.aliveCount.bl + '/' + inst.aliveCount.gr : 'unknown');
    if (nano) text += ', respawning=' + nano.respawningPlayerSize + ', thisRoundPlayer=' + nano.thisRoundPlayer;
    return text;
  }

  function probeLifecycle(stage, modePtr, includeNanoExtra, extra, forceLog) {
    if (!Runtime.enabled || !Runtime.probe.enabled) return;
    if (modePtr && !modePtr.isNull()) Runtime.modeBase = modePtr;

    var snapshot = {
      stage: stage,
      mode: summarizeGameManagerMode(),
      rule: summarizeModeBaseStatic(),
      instance: summarizeModeBaseInstance(modePtr || Runtime.modeBase, !!includeNanoExtra),
      extra: extra || {}
    };
    Runtime.probe.lifecycleHits += 1;
    Runtime.probe.lastLifecycle = snapshot;

    var now = Date.now();
    var key = lifecycleKey(snapshot);
    var shouldLog = !!forceLog ||
      key !== Runtime.probe.lastLifecycleKey ||
      (Runtime.probe.level === 'verbose' && now - Runtime.probe.lastLifecycleLogMs > 3000);
    if (!shouldLog) return;

    Runtime.probe.lastLifecycleKey = key;
    Runtime.probe.lastLifecycleLogMs = now;
    sendLog(
      'info',
      '[life] ' + stage + ' | ' + shortLifecycleSummary(snapshot) +
      (extra && extra.note ? ' | ' + extra.note : '')
    );
  }

  function isMainWeaponClass(wpnClass) {
    return wpnClass >= 0 && wpnClass <= 4;
  }

  function isRelevantWeaponLimitMismatch(expectedClass, wpnClass) {
    if (expectedClass === null || expectedClass === undefined || wpnClass === null || wpnClass === undefined) return false;
    if (expectedClass === 1) return isMainWeaponClass(wpnClass) && wpnClass !== 1;
    if (expectedClass === 5) return wpnClass >= 0 && wpnClass <= 5 && wpnClass !== 5;
    return wpnClass !== expectedClass;
  }

  function resetWeaponGrantProbe() {
    Runtime.weaponProbe.giveWeaponByBagDepth = 0;
    Runtime.weaponProbe.grantsByPlayer = {};
    Runtime.weaponProbe.grantOrder = [];
  }

  function resetWeaponGrantForPlayer(playerPtr) {
    var key = safePtrText(playerPtr);
    delete Runtime.weaponProbe.grantsByPlayer[key];

    var order = Runtime.weaponProbe.grantOrder;
    for (var i = order.length - 1; i >= 0; i--) {
      if (order[i] === key) order.splice(i, 1);
    }
  }

  function nextWeaponGrantSeqForPlayer(playerPtr) {
    var key = safePtrText(playerPtr);
    var store = Runtime.weaponProbe.grantsByPlayer[key];
    return store ? store.grants.length + 1 : 1;
  }

  function maybeOverrideLimitedBotGrant(args) {
    var originalWeaponIndex = args[1].toInt32();
    var result = {
      changed: false,
      originalWeaponIndex: originalWeaponIndex,
      effectiveWeaponIndex: originalWeaponIndex,
      grantSeq: null,
      player: null,
      originalWeapon: null,
      reason: null
    };

    if (!Runtime.enabled) {
      result.reason = 'disabled';
      return result;
    }

    var expectedClass = expectedWeaponClassForSelectedMode();
    var fallbackWeaponIndex = fallbackWeaponIndexForSelectedMode();
    if (expectedClass === null || fallbackWeaponIndex === null) {
      result.reason = 'not-weapon-limited-mode';
      return result;
    }

    var player = summarizePlayer(args[0]);
    result.player = player;
    if (player.clientIsBot !== true) {
      result.reason = 'not-bot';
      return result;
    }

    var grantSeq = nextWeaponGrantSeqForPlayer(args[0]);
    result.grantSeq = grantSeq;
    var reason = Runtime.modeKey + '-bot-first-grant';
    if (grantSeq !== 1) {
      var originalWeapon = lookupWeaponDataByIndex(originalWeaponIndex);
      result.originalWeapon = originalWeapon;
      if (!isRelevantWeaponLimitMismatch(expectedClass, originalWeapon.wpnClass)) {
        result.reason = 'not-weapon-limit-mismatch';
        return result;
      }
      reason = Runtime.modeKey + '-bot-weapon-limit-mismatch';
    }

    args[1] = ptr(fallbackWeaponIndex);
    result.changed = true;
    result.effectiveWeaponIndex = fallbackWeaponIndex;
    result.reason = reason;
    Runtime.botSniperOverrideHits += 1;
    Runtime.botSniperOverrideLast = result;

    if (Runtime.probe.enabled) {
      sendLog(
        'warn',
        '[weapon] BotWeaponLimitOverride | player=' + player.ptr +
        ', team=' + player.teamLabel +
        ', grantSeq=' + grantSeq +
        ', reason=' + reason +
        ', original=' + originalWeaponIndex +
        ' -> ' + fallbackWeaponIndex
      );
    }
    return result;
  }

  function rememberWeaponGrant(player, requestedWeaponIndex, weapon, mismatch, directCall) {
    var playerKey = player && player.ptr ? player.ptr : 'unknown';
    var store = Runtime.weaponProbe.grantsByPlayer[playerKey];
    if (!store) {
      store = {
        player: player,
        grants: [],
        knownMainWeapons: 0,
        firstKnownMain: null,
        firstGrant: null,
        mismatch: 0,
        directCalls: 0
      };
      Runtime.weaponProbe.grantsByPlayer[playerKey] = store;
      Runtime.weaponProbe.grantOrder.push(playerKey);
    }

    var seq = store.grants.length + 1;
    var grant = {
      seq: seq,
      requestedIndex: requestedWeaponIndex,
      weapon: weapon,
      mismatch: !!mismatch,
      direct: !!directCall
    };
    store.grants.push(grant);
    if (!store.firstGrant) store.firstGrant = grant;
    if (isMainWeaponClass(weapon.wpnClass)) {
      store.knownMainWeapons += 1;
      if (!store.firstKnownMain) store.firstKnownMain = grant;
    }
    if (mismatch) store.mismatch += 1;
    if (directCall) store.directCalls += 1;
    return grant;
  }

  function addCount(bucket, label) {
    bucket[label] = (bucket[label] || 0) + 1;
  }

  function probeWeaponGrantSummary(stage) {
    if (!Runtime.enabled || !Runtime.probe.enabled) return;
    var expectedClass = expectedWeaponClassForSelectedMode();
    if (expectedClass === null && Runtime.probe.level !== 'verbose') return;

    var totalPlayers = 0;
    var botPlayers = 0;
    var totalGrants = 0;
    var firstGrantCounts = {};
    var firstKnownMainCounts = {};
    var seqCounts = {};
    var mismatchPlayers = 0;
    var unknownFirstGrant = 0;
    var samples = [];
    var sampleLimit = Runtime.probe.level === 'verbose' ? 24 : 10;

    for (var i = 0; i < Runtime.weaponProbe.grantOrder.length; i++) {
      var key = Runtime.weaponProbe.grantOrder[i];
      var store = Runtime.weaponProbe.grantsByPlayer[key];
      if (!store) continue;
      totalPlayers += 1;
      if (store.player && store.player.clientIsBot) botPlayers += 1;
      totalGrants += store.grants.length;
      if (store.mismatch > 0) mismatchPlayers += 1;

      var first = store.firstGrant;
      var firstKnown = store.firstKnownMain;
      if (first && first.weapon) {
        addCount(firstGrantCounts, weaponClassShort(first.weapon.wpnClass));
        if (first.weapon.wpnClass === null || first.weapon.wpnClass === undefined) unknownFirstGrant += 1;
      }
      if (firstKnown && firstKnown.weapon) addCount(firstKnownMainCounts, weaponClassShort(firstKnown.weapon.wpnClass));

      for (var g = 0; g < store.grants.length; g++) {
        var grant = store.grants[g];
        var seqKey = 'seq' + grant.seq;
        if (!seqCounts[seqKey]) seqCounts[seqKey] = {};
        addCount(seqCounts[seqKey], weaponClassShort(grant.weapon.wpnClass));
      }

      if (samples.length < sampleLimit) {
        var grants = [];
        for (var s = 0; s < store.grants.length; s++) {
          var item = store.grants[s];
          grants.push('#' + item.seq + ':' + item.requestedIndex + '/' + weaponClassShort(item.weapon.wpnClass));
        }
        samples.push({
          player: key,
          team: store.player ? store.player.teamLabel : 'unknown',
          firstKnownMain: firstKnown ? weaponProbeText(firstKnown.weapon) : 'none',
          mismatch: store.mismatch,
          grants: grants.join(',')
        });
      }
    }

    Runtime.probe.lastWeaponGrantSummary = {
      stage: stage,
      totalPlayers: totalPlayers,
      botPlayers: botPlayers,
      totalGrants: totalGrants,
      firstGrantCounts: firstGrantCounts,
      firstKnownMainCounts: firstKnownMainCounts,
      seqCounts: seqCounts,
      mismatchPlayers: mismatchPlayers,
      unknownFirstGrant: unknownFirstGrant,
      samples: samples
    };

    var seqText = [];
    for (var seqName in seqCounts) {
      if (!Object.prototype.hasOwnProperty.call(seqCounts, seqName)) continue;
      seqText.push(seqName + '[' + formatClassCounts(seqCounts[seqName]) + ']');
    }

    sendLog(
      'info',
      '[weapon] ' + stage +
      ' | grantSummary players=' + totalPlayers +
      ', bots=' + botPlayers +
      ', grants=' + totalGrants +
      ', firstGrant=' + formatClassCounts(firstGrantCounts) +
      ', firstKnownMain=' + formatClassCounts(firstKnownMainCounts) +
      ', mismatchPlayers=' + mismatchPlayers +
      ', unknownFirstGrant=' + unknownFirstGrant +
      ' | ' + seqText.join(' ')
    );

    for (var j = 0; j < samples.length; j++) {
      var sample = samples[j];
      sendLog(
        'info',
        '[weapon] ' + stage + '.sample | player=' + sample.player +
        ', team=' + sample.team +
        ', mismatch=' + sample.mismatch +
        ', firstKnownMain=' + sample.firstKnownMain +
        ' | grants=' + sample.grants
      );
    }
  }

  function probeWeaponGrant(stage, playerPtr, requestedWeaponIndex, weaponPtr, directCall) {
    if (!Runtime.enabled || !Runtime.probe.enabled) return;
    var expectedClass = expectedWeaponClassForSelectedMode();
    if (expectedClass === null && Runtime.probe.level !== 'verbose') return;

    var player = summarizePlayer(playerPtr);
    if (!player.clientIsBot && Runtime.probe.level !== 'verbose') return;

    var weapon = summarizeWeaponObject(weaponPtr, requestedWeaponIndex);
    var mismatch = isRelevantWeaponLimitMismatch(expectedClass, weapon.wpnClass);
    if (mismatch) Runtime.probe.weaponMismatchHits += 1;
    var grant = rememberWeaponGrant(player, requestedWeaponIndex, weapon, mismatch, directCall);

    var sideNote = '';
    if (expectedClass !== null && !mismatch && weapon.wpnClass !== expectedClass) sideNote = ', limitCheck=ignored-sidearm-or-unknown';
    else if (mismatch) sideNote = ', limitCheck=MISMATCH expected=' + weaponClassLabel(expectedClass);
    else if (expectedClass !== null) sideNote = ', limitCheck=ok';

    if (stage === 'GameManager.GiveWeapon.leave') Runtime.probe.giveWeaponHits += 1;
    if (stage === 'GameManager.GiveWeaponByBag.leave') Runtime.probe.giveWeaponByBagHits += 1;

    sendLog(
      mismatch ? 'warn' : 'info',
      '[weapon] ' + stage +
      ' | bot=' + player.clientIsBot +
      ', team=' + player.teamLabel +
      ', grantSeq=' + grant.seq +
      ', requestedIndex=' + requestedWeaponIndex +
      ', direct=' + !!directCall +
      ' | ' + weaponProbeText(weapon) +
      sideNote
    );
  }

  function terminatorSupplyCompatIsActive() {
    return !!(
      Runtime.enabled &&
      Runtime.modeKey === 'nano4_terminator' &&
      Runtime.lastApplied &&
      Runtime.lastApplied.key === Runtime.modeKey &&
      Runtime.lastApplied.gameMode === MODES.nano4_terminator.gameMode
    );
  }

  function resolveTerminatorTypeInfo() {
    var base = getGameAssembly();
    if (!base) return null;
    return readPointer(base.add(RVA.Mode_Nano4_Terminator_TypeInfo));
  }

  function isTerminatorModeInstance(modeInstance) {
    if (!modeInstance || modeInstance.isNull()) return false;
    var typeInfo = resolveTerminatorTypeInfo();
    if (!typeInfo) return false;
    var instanceClass = readPointer(modeInstance);
    return !!(instanceClass && instanceClass.equals(typeInfo));
  }

  function loadTerminatorAttributePointers(modeInstance) {
    var result = {
      ok: false,
      count: 0,
      hasGhostSupply: false,
      hasHumanSupply: false
    };
    if (!modeInstance || modeInstance.isNull()) return result;

    var attributeAsset = readPointer(modeInstance.add(OFF.Mode_Nano4_Terminator_attributeAsset));
    if (!attributeAsset) return result;

    var attrs = readPointer(attributeAsset.add(OFF.Nano4TAttributeAsset_attributes));
    if (!attrs) return result;

    var length = readS32(attrs.add(OFF.Array_length));
    if (length === null || length < 1 || length > 128) return result;

    var map = {};
    var count = Math.min(length, 64);
    for (var i = 0; i < count; i++) {
      var attr = readPointer(attrs.add(OFF.Array_items + i * Process.pointerSize));
      if (!attr) continue;
      var id = readS32(attr.add(OFF.Nano4TAttribute_id));
      if (id === null) continue;
      map[id] = attr;
      result.count += 1;
    }

    Runtime.terminatorSupplyAttrPtrs = map;
    Runtime.terminatorSupplyAttrLoadCount += 1;
    result.ok = result.count > 0;
    result.hasGhostSupply = !!map[TERMINATOR_SUPPLY_GHOST_ATTR_ID];
    result.hasHumanSupply = !!map[TERMINATOR_SUPPLY_HUMAN_ATTR_ID];
    return result;
  }

  function writeTerminatorRoundAttribute(modeInstance, fieldOffset, attrId) {
    var attr = Runtime.terminatorSupplyAttrPtrs[attrId];
    if (!attr || attr.isNull()) return false;

    var field = modeInstance.add(fieldOffset);
    var current = readPointer(field);
    if (current && current.equals(attr)) return false;

    return writeManagedReference(field, attr);
  }

  function ensureTerminatorSupplyAttributeChain(modeInstance, reason) {
    if (!terminatorSupplyCompatIsActive()) return { ok: true, changed: false, skipped: true };
    if (!isTerminatorModeInstance(modeInstance)) return { ok: true, changed: false, skipped: true };

    var attrs = loadTerminatorAttributePointers(modeInstance);
    if (!attrs.ok) return { ok: false, changed: false, msg: '多人生化 attributeAsset 未就绪' };

    var ghostChanged = writeTerminatorRoundAttribute(
      modeInstance,
      OFF.Mode_Nano4_Terminator_attribute_Nano,
      TERMINATOR_SUPPLY_GHOST_ATTR_ID
    );
    var humanChanged = writeTerminatorRoundAttribute(
      modeInstance,
      OFF.Mode_Nano4_Terminator_attribute_Human,
      TERMINATOR_SUPPLY_HUMAN_ATTR_ID
    );

    Runtime.terminatorSupplyCompatHits += 1;
    Runtime.terminatorSupplyCompatLast = {
      reason: reason || 'manual',
      action: 'attributeChain',
      attrCount: attrs.count,
      ghostAttrId: TERMINATOR_SUPPLY_GHOST_ATTR_ID,
      humanAttrId: TERMINATOR_SUPPLY_HUMAN_ATTR_ID,
      ghostChanged: !!ghostChanged,
      humanChanged: !!humanChanged,
      count: Runtime.terminatorSupplyCompatHits
    };

    if (ghostChanged || humanChanged) {
      sendLog('warn', '多人生化补给箱链路已补齐：attribute_Nano=终结者出现，attribute_Human=英雄出现 via ' + (reason || 'manual'));
    }

    return { ok: true, changed: !!(ghostChanged || humanChanged), attrs: attrs };
  }

  function upgradeBoxGeneratorKey(modeInstance) {
    var currentRound = readS32(modeInstance.add(OFF.ModeBase_currentRound));
    if (currentRound === null) currentRound = 'unknown';
    return safePtrText(modeInstance) + ':' + currentRound;
  }

  function markNativeUpgradeBoxGeneratorStarted(modeInstance, reason) {
    if (!terminatorSupplyCompatIsActive()) return { ok: true, changed: false, skipped: true };
    if (!isTerminatorModeInstance(modeInstance)) return { ok: true, changed: false, skipped: true };

    var key = upgradeBoxGeneratorKey(modeInstance);
    Runtime.upgradeBoxGeneratorNativeKeys[key] = true;
    Runtime.upgradeBoxGeneratorNativeCount += 1;
    Runtime.upgradeBoxGeneratorNativeLast = {
      reason: reason || 'manual',
      key: key,
      count: Runtime.upgradeBoxGeneratorNativeCount
    };
    return { ok: true, changed: true, key: key };
  }

  function ensureTerminatorUpgradeBoxGeneratorsStarted(modeInstance, reason) {
    if (!terminatorSupplyCompatIsActive()) return { ok: true, changed: false, skipped: true };
    if (!isTerminatorModeInstance(modeInstance)) return { ok: true, changed: false, skipped: true };
    if (!Runtime.createUpgradeBoxGenerator || !Runtime.startCoroutineAuto) {
      return { ok: false, changed: false, msg: 'UpgradeBox generator native functions are not initialized' };
    }

    var key = upgradeBoxGeneratorKey(modeInstance);
    if (Runtime.upgradeBoxGeneratorNativeKeys[key]) return { ok: true, changed: false, skipped: true, source: 'native' };
    if (Runtime.upgradeBoxGeneratorFallbackKeys[key]) return { ok: true, changed: false, skipped: true, source: 'fallback' };

    try {
      ensureTerminatorSupplyPointFallbacks(reason || 'ensureTerminatorUpgradeBoxGeneratorsStarted');
      ensureTerminatorSupplyAttributeChain(modeInstance, reason || 'ensureTerminatorUpgradeBoxGeneratorsStarted');

      var redGenerator = Runtime.createUpgradeBoxGenerator(modeInstance, TERMINATOR_UPGRADE_BOX_RED_DELAY, TERMINATOR_UPGRADE_BOX_RED_TEAM, ptr(0));
      var blueGenerator = Runtime.createUpgradeBoxGenerator(modeInstance, TERMINATOR_UPGRADE_BOX_BLUE_DELAY, TERMINATOR_UPGRADE_BOX_BLUE_TEAM, ptr(0));
      if (!redGenerator || redGenerator.isNull() || !blueGenerator || blueGenerator.isNull()) {
        return { ok: false, changed: false, msg: 'UpgradeBox generator creation returned null' };
      }

      Runtime.startCoroutineAuto(modeInstance, redGenerator, ptr(0));
      Runtime.startCoroutineAuto(modeInstance, blueGenerator, ptr(0));
      Runtime.upgradeBoxGeneratorFallbackKeys[key] = true;
      Runtime.upgradeBoxGeneratorFallbackCount += 1;
      Runtime.upgradeBoxGeneratorFallbackLast = {
        reason: reason || 'manual',
        key: key,
        redDelay: TERMINATOR_UPGRADE_BOX_RED_DELAY,
        blueDelay: TERMINATOR_UPGRADE_BOX_BLUE_DELAY,
        redTeam: TERMINATOR_UPGRADE_BOX_RED_TEAM,
        blueTeam: TERMINATOR_UPGRADE_BOX_BLUE_TEAM,
        count: Runtime.upgradeBoxGeneratorFallbackCount
      };
      sendLog('warn', 'Nano4T UpgradeBox generator fallback started via ' + (reason || 'manual'));
      return { ok: true, changed: true, last: Runtime.upgradeBoxGeneratorFallbackLast };
    } catch (e) {
      return fail('Start Nano4T UpgradeBox generator fallback failed', e);
    }
  }

  function shouldDeferNanoModeApplyUntilBotGeneration(selected) {
    return !!(
      selected &&
      Runtime.lastSourceMapMode === 1 &&
      selected.gameMode >= 4 && selected.gameMode <= 6
    );
  }

  function markDeferredModeApply(reason) {
    Runtime.deferModeApplyUntilBotGeneration = true;
    Runtime.deferredModeApplyReason = reason || 'unknown';
    Runtime.lastApplied = null;
    sendLog('info', '个人竞技图切生化，延迟到 bot 生成后再套用目标模式 via ' + Runtime.deferredModeApplyReason);
    return { ok: true, changed: false, deferred: true };
  }

  function applyDeferredModeAfterBotGeneration(reason) {
    if (!Runtime.enabled || !Runtime.deferModeApplyUntilBotGeneration) return { ok: true, changed: false };
    Runtime.deferModeApplyUntilBotGeneration = false;
    var result = applySelectedMode();
    if (result && result.ok === false) {
      Runtime.deferModeApplyUntilBotGeneration = true;
      return result;
    }
    Runtime.deferredModeApplyReason = null;
    sendLog('info', '个人竞技图切生化：bot 生成后已套用目标模式 via ' + (reason || 'manual'));
    return result || { ok: true, changed: true };
  }

  function nanoRulesAreActiveForCurrentStart() {
    return !!(
      Runtime.lastApplied &&
      Runtime.lastApplied.key === Runtime.modeKey &&
      Runtime.lastApplied.sourceMapMode === 1 &&
      Runtime.lastApplied.gameMode >= 4 && Runtime.lastApplied.gameMode <= 6
    );
  }

  function normalizeRoomBotTeamsForNanoRules(reason) {
    if (!Runtime.enabled || !nanoRulesAreActiveForCurrentStart()) return { changed: 0 };

    var listPtr = resolveRoomPlayersList();
    if (!listPtr) return { changed: 0 };

    var size = getListSize(listPtr);
    var items = readPointer(listPtr.add(OFF.List_items));
    if (size === null || size < 1 || !items) return { changed: 0 };

    var arrayLength = readS32(items.add(OFF.Array_length));
    if (arrayLength === null || arrayLength < 1 || arrayLength > 4096) return { changed: 0 };

    var count = Math.min(size, arrayLength, 64);
    var changed = 0;
    var nextTeam = 0;
    for (var i = 0; i < count; i++) {
      var clientData = readPointer(items.add(OFF.Array_items + i * Process.pointerSize));
      if (!clientData) continue;
      var isBot = readU8(clientData.add(OFF.ClientData_isBot));
      if (!isBot) continue;

      var joinTeam = readS32(clientData.add(OFF.ClientData_joinTeam));
      var desiredTeam = nextTeam;
      nextTeam = nextTeam === 0 ? 1 : 0;

      if (joinTeam !== desiredTeam) {
        clientData.add(OFF.ClientData_joinTeam).writeS32(desiredTeam);
        changed += 1;
      }
    }

    if (changed > 0) {
      sendLog('warn', '个人竞技图切生化时已将 bot 分配到 BL/GR：' + changed + ' 个 via ' + (reason || 'manual'));
    }
    return { changed: changed };
  }

  function ensureNanoRuleSpawnFallbacks(reason) {
    if (!Runtime.enabled || !nanoRulesAreActiveForCurrentStart()) return false;
    var bl = ensureTeamSpawnFallbackFromNeutral(0, reason);
    var gr = ensureTeamSpawnFallbackFromNeutral(1, reason);
    return !!(bl || gr);
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

  function resolveTargetMapRuleEntry(targetAsset, mapID) {
    var result = {
      ready: false,
      mapID: mapID,
      prefabOverride: null,
      prefabOverrideText: 'null',
      weaponLimited: null,
      weaponLimitedSource: 'missing',
      reason: null
    };

    if (!targetAsset || targetAsset.isNull()) {
      result.reason = 'targetAsset 为空';
      return result;
    }
    if (mapID === null || mapID === undefined || mapID < 0) {
      result.reason = 'mapID 无效';
      return result;
    }

    var datas = readPointer(targetAsset.add(OFF.MapAsset_datas));
    if (!datas) {
      result.reason = 'MapAsset.datas 为空';
      return result;
    }

    var length = readS32(datas.add(OFF.Array_length));
    if (length === null || length < 1 || length > 512) {
      result.reason = 'MapAsset.datas 长度异常: ' + length;
      return result;
    }
    if (mapID >= length) {
      result.reason = 'mapID 超出目标 MapAsset.datas: ' + mapID + '/' + length;
      return result;
    }

    var entry = datas.add(OFF.Array_items + mapID * OFF.MapAsset_Map_size);
    var prefabOverride = readPointer(entry.add(OFF.MapAsset_Map_gameModePrefabOverride));
    var weaponLimited = readS32(entry.add(OFF.MapAsset_Map_weaponLimited));
    result.ready = true;
    result.prefabOverride = prefabOverride;
    result.prefabOverrideText = safePtrText(prefabOverride);
    result.weaponLimited = weaponLimited;
    result.weaponLimitedSource = 'targetAsset.datas[' + mapID + '].weaponLimited';
    return result;
  }

  function getArrayLength(arrayPtr) {
    var length = readS32(arrayPtr.add(OFF.Array_length));
    if (length === null || length < 1 || length > 4096) return 0;
    return length;
  }

  function supplyBoxTypeLabel(type) {
    if (type === SUPPLY_BOX_TYPE_YELLOW) return 'Yellow(0)';
    if (type === SUPPLY_BOX_TYPE_RED) return 'Red(1)';
    if (type === SUPPLY_BOX_TYPE_BLUE) return 'Blue(2)';
    return 'Type(' + type + ')';
  }

  function summarizeSupplyPointPair(pointOffset, listOffset) {
    var pointPtr = Runtime.mapManager ? readPointer(Runtime.mapManager.add(pointOffset)) : null;
    var listPtr = Runtime.mapManager ? readPointer(Runtime.mapManager.add(listOffset)) : null;
    return {
      pointPtr: safePtrText(pointPtr),
      pointCount: pointPtr ? getArrayLength(pointPtr) : 0,
      idListPtr: safePtrText(listPtr),
      idCount: listPtr ? getListSize(listPtr) : null
    };
  }

  function summarizeSupplyPointState(reason) {
    return {
      reason: reason || 'manual',
      active: terminatorSupplyCompatIsActive(),
      modeKey: Runtime.modeKey,
      lastApplied: Runtime.lastApplied,
      mapManager: safePtrText(Runtime.mapManager),
      supply: summarizeSupplyPointPair(OFF.MapManager_SP_SupplyBox, OFF.MapManager_IDList_SupplyBox),
      red: summarizeSupplyPointPair(OFF.MapManager_SP_RedBox, OFF.MapManager_IDList_RedBox),
      blue: summarizeSupplyPointPair(OFF.MapManager_SP_BlueBox, OFF.MapManager_IDList_BlueBox),
      generatorNativeCount: Runtime.upgradeBoxGeneratorNativeCount,
      generatorFallbackCount: Runtime.upgradeBoxGeneratorFallbackCount,
      pointRequests: Runtime.supplyBoxPointRequests
    };
  }

  function logSupplyBoxPipeline(stage, extra) {
    if (!Runtime.enabled || Runtime.modeKey !== 'nano4_terminator') return;
    Runtime.supplyBoxPipelineDiagnostics += 1;
    var snapshot = summarizeSupplyPointState(stage);
    snapshot.stage = stage;
    snapshot.extra = extra || null;
    snapshot.count = Runtime.supplyBoxPipelineDiagnostics;
    Runtime.supplyBoxPipelineLast = snapshot;
    sendLog('warn', '[SupplyBoxDiag] ' + stage + ' ' + JSON.stringify(snapshot));
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

  function readSpawnArrayByKey(mapManager, key) {
    var offset = null;
    var source = null;
    if (key === 'neutral') {
      offset = OFF.MapManager_SP_Netural;
      source = 'SP_Netural';
    } else if (key === 'supply') {
      offset = OFF.MapManager_SP_SupplyBox;
      source = 'SP_SupplyBox';
    } else if (key === 'bl') {
      offset = OFF.MapManager_SP_BL;
      source = 'SP_BL';
    } else if (key === 'gr') {
      offset = OFF.MapManager_SP_GR;
      source = 'SP_GR';
    }
    if (offset === null) return null;

    var ptrValue = readPointer(mapManager.add(offset));
    var length = ptrValue ? getArrayLength(ptrValue) : 0;
    if (length < 1) return null;
    return { ptr: ptrValue, source: source, length: length };
  }

  function pickSupplyPointFallbackSpawnArray(mapManager, preferences) {
    for (var i = 0; i < preferences.length; i++) {
      var found = readSpawnArrayByKey(mapManager, preferences[i]);
      if (found) return found;
    }
    return null;
  }

  function terminatorSupplyPointFallbackIsActive() {
    return !!(
      Runtime.enabled &&
      Runtime.modeKey === 'nano4_terminator' &&
      Runtime.lastApplied &&
      Runtime.lastApplied.key === Runtime.modeKey &&
      Runtime.lastApplied.gameMode === MODES.nano4_terminator.gameMode
    );
  }

  function isUsablePointer(value) {
    try {
      return !!(value && !value.isNull() && value.compare(ptr('0x10000')) >= 0);
    } catch (_) {
      return false;
    }
  }

  function isNullOrLikelyArrayPointer(value) {
    if (!value || value.isNull()) return true;
    if (!isUsablePointer(value)) return false;
    var length = readS32(value.add(OFF.Array_length));
    return length !== null && length >= 0 && length <= 4096;
  }

  function isUsableMapManagerForSupplyFallback(mapManager, reason) {
    if (!isUsablePointer(mapManager)) return false;

    var sourceOffsets = [
      OFF.MapManager_SP_BL,
      OFF.MapManager_SP_GR,
      OFF.MapManager_SP_Netural,
      OFF.MapManager_SP_SupplyBox
    ];
    var hasFallbackSource = false;

    for (var i = 0; i < sourceOffsets.length; i++) {
      var fieldValue = readPointer(mapManager.add(sourceOffsets[i]));
      if (!isNullOrLikelyArrayPointer(fieldValue)) {
        Runtime.supplyBoxSpawnFallbackLast = 'SupplyBox fallback skipped: cached MapManager shape invalid at 0x' + sourceOffsets[i].toString(16) + ' via ' + (reason || 'manual');
        sendLog('warn', Runtime.supplyBoxSpawnFallbackLast);
        return false;
      }
      if (fieldValue && getArrayLength(fieldValue) > 0) hasFallbackSource = true;
    }

    if (!hasFallbackSource) {
      Runtime.supplyBoxSpawnFallbackLast = 'SupplyBox fallback skipped: no usable BL/GR/Neutral/Supply source via ' + (reason || 'manual');
      sendLog('warn', Runtime.supplyBoxSpawnFallbackLast);
      return false;
    }

    return true;
  }

  function ensureSupplyPointArray(fieldOffset, fieldName, fallback, reason) {
    if (!Runtime.mapManager || Runtime.mapManager.isNull()) return false;
    var targetField = Runtime.mapManager.add(fieldOffset);
    var current = readPointer(targetField);
    if (current && getArrayLength(current) > 0) return false;

    if (!fallback) {
      Runtime.supplyBoxSpawnFallbackLast = fieldName + ' 为空，且没有可借用的出生点';
      sendLog('warn', Runtime.supplyBoxSpawnFallbackLast);
      return false;
    }

    if (!writeManagedReference(targetField, fallback.ptr)) {
      Runtime.supplyBoxSpawnFallbackLast = fieldName + ' 兜底写入失败';
      sendLog('warn', Runtime.supplyBoxSpawnFallbackLast);
      return false;
    }

    Runtime.supplyBoxSpawnFallbackCount += 1;
    Runtime.supplyBoxSpawnFallbackLast = fieldName + ' <- ' + fallback.source + '[' + fallback.length + '] via ' + reason;
    sendLog('warn', fieldName + ' 补给点缺失，已临时借用 ' + fallback.source + '（' + fallback.length + ' 个）');
    return true;
  }

  function resolveListIntTypeInfo() {
    var base = getGameAssembly();
    if (!base) return null;
    return readPointer(base.add(RVA.System_Collections_Generic_List_int_TypeInfo));
  }

  function ensureSupplyPointIndexList(listFieldOffset, listFieldName, pointArrayOffset, pointArrayName, reason) {
    if (!Runtime.mapManager || Runtime.mapManager.isNull()) return false;

    var points = readPointer(Runtime.mapManager.add(pointArrayOffset));
    var pointCount = points ? getArrayLength(points) : 0;
    if (pointCount < 1) return false;

    var listField = Runtime.mapManager.add(listFieldOffset);
    var listPtr = readPointer(listField);
    var currentSize = listPtr ? getListSize(listPtr) : null;
    if (currentSize !== null && currentSize > 0) return false;

    var shouldCreateList = !listPtr || currentSize === null;
    if (shouldCreateList) {
      if (!Runtime.objectNew || !Runtime.listIntCtor) return false;
      var listTypeInfo = resolveListIntTypeInfo();
      if (!listTypeInfo) return false;
      listPtr = Runtime.objectNew(listTypeInfo);
      if (!listPtr || listPtr.isNull()) return false;
      Runtime.listIntCtor(listPtr, ptr(0));
      if (!writeManagedReference(listField, listPtr)) return false;
    }

    if (!Runtime.listIntAdd) return false;
    for (var i = 0; i < pointCount; i++) {
      Runtime.listIntAdd(listPtr, i, ptr(0));
    }

    Runtime.supplyBoxSpawnFallbackCount += 1;
    Runtime.supplyBoxSpawnFallbackLast = listFieldName + ' <- ' + pointArrayName + '[0..' + (pointCount - 1) + '] via ' + (reason || 'manual');
    sendLog('warn', listFieldName + ' 已按 ' + pointArrayName + ' 补齐索引列表：' + pointCount + ' 个');
    return true;
  }

  function ensureTerminatorSupplyPointFallbacks(reason) {
    if (!terminatorSupplyPointFallbackIsActive()) return false;
    if (!Runtime.mapManager || Runtime.mapManager.isNull()) return false;
    if (!isUsableMapManagerForSupplyFallback(Runtime.mapManager, reason || 'manual')) return false;

    var yellowFallback = pickSupplyPointFallbackSpawnArray(Runtime.mapManager, ['neutral', 'bl', 'gr']);
    var redFallback = pickSupplyPointFallbackSpawnArray(Runtime.mapManager, ['bl', 'supply', 'neutral', 'gr']);
    var blueFallback = pickSupplyPointFallbackSpawnArray(Runtime.mapManager, ['gr', 'supply', 'neutral', 'bl']);

    var changed = 0;
    if (ensureSupplyPointArray(OFF.MapManager_SP_SupplyBox, 'SP_SupplyBox', yellowFallback, reason || 'manual')) changed += 1;
    if (ensureSupplyPointArray(OFF.MapManager_SP_RedBox, 'SP_RedBox', redFallback, reason || 'manual')) changed += 1;
    if (ensureSupplyPointArray(OFF.MapManager_SP_BlueBox, 'SP_BlueBox', blueFallback, reason || 'manual')) changed += 1;
    if (ensureSupplyPointIndexList(OFF.MapManager_IDList_SupplyBox, 'IDList_SupplyBox', OFF.MapManager_SP_SupplyBox, 'SP_SupplyBox', reason || 'manual')) changed += 1;
    if (ensureSupplyPointIndexList(OFF.MapManager_IDList_RedBox, 'IDList_RedBox', OFF.MapManager_SP_RedBox, 'SP_RedBox', reason || 'manual')) changed += 1;
    if (ensureSupplyPointIndexList(OFF.MapManager_IDList_BlueBox, 'IDList_BlueBox', OFF.MapManager_SP_BlueBox, 'SP_BlueBox', reason || 'manual')) changed += 1;
    return changed > 0;
  }

  function ensureTeamSpawnFallbackFromNeutral(team, reason) {
    if (!Runtime.enabled) return false;
    if (team !== 0 && team !== 1) return false;
    if (!Runtime.mapManager || Runtime.mapManager.isNull()) return false;

    var targetFieldOffset = team === 0 ? OFF.MapManager_SP_BL : OFF.MapManager_SP_GR;
    var targetName = team === 0 ? 'SP_BL' : 'SP_GR';
    var targetField = Runtime.mapManager.add(targetFieldOffset);
    var current = readPointer(targetField);
    if (current && getArrayLength(current) > 0) return false;

    var neutral = readPointer(Runtime.mapManager.add(OFF.MapManager_SP_Netural));
    var neutralLength = neutral ? getArrayLength(neutral) : 0;
    if (neutralLength < 1) {
      Runtime.teamSpawnFallbackLast = targetName + ' 为空，且 SP_Netural 也不可用';
      sendLog('warn', Runtime.teamSpawnFallbackLast);
      return false;
    }

    if (!writeManagedReference(targetField, neutral)) {
      Runtime.teamSpawnFallbackLast = targetName + ' 兜底写入失败';
      sendLog('warn', Runtime.teamSpawnFallbackLast);
      return false;
    }

    Runtime.teamSpawnFallbackCount += 1;
    Runtime.teamSpawnFallbackLast = targetName + ' <- SP_Netural[' + neutralLength + '] via ' + reason;
    sendLog('warn', targetName + ' 出生点缺失，已临时借用 SP_Netural（' + neutralLength + ' 个）');
    return true;
  }

  function ensureNeutralSpawnFallbackFromTeam(reason) {
    if (!Runtime.enabled) return false;
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
    sendLog('warn', '中立出生点缺失，已临时借用 ' + fallback.source + '（' + fallback.length + ' 个）');
    return true;
  }

  function writeManagedReference(fieldAddr, value) {
    if (!fieldAddr || fieldAddr.isNull() || !value || value.isNull()) return false;
    fieldAddr.writePointer(value);
    Runtime.writeBarrier(fieldAddr, value);
    return fieldAddr.readPointer().equals(value);
  }

  function shouldTeamDeathWeaponOnlyOverride(selected, beforeMode) {
    if (!selected || !beforeMode) return false;
    if (!selected.teamDeathOnNano) return false;
    if (Runtime.lastSourceMapMode !== null && Runtime.lastSourceMapMode !== undefined) {
      return isNanoGameModeValue(Runtime.lastSourceMapMode);
    }
    return beforeMode.ready && isNanoGameModeValue(beforeMode.gameMode);
  }

  function shouldUseTeamRulesForWeaponOnly(selected) {
    if (!selected || !selected.weaponOnly) return false;
    return !!(
      Runtime.lastApplied &&
      Runtime.lastApplied.key === Runtime.modeKey &&
      Runtime.lastApplied.forceTeamRules
    );
  }

  function teamRulesAreActiveForCurrentStart() {
    return !!(
      Runtime.lastApplied &&
      Runtime.lastApplied.key === Runtime.modeKey &&
      Runtime.lastApplied.gameMode === MODES.team_death.gameMode
    );
  }

  function normalizeRoomBotTeamsForTeamRules(reason) {
    if (!Runtime.enabled || !teamRulesAreActiveForCurrentStart()) return { changed: 0 };

    var listPtr = resolveRoomPlayersList();
    if (!listPtr) return { changed: 0 };

    var size = getListSize(listPtr);
    var items = readPointer(listPtr.add(OFF.List_items));
    if (size === null || size < 1 || !items) return { changed: 0 };

    var arrayLength = readS32(items.add(OFF.Array_length));
    if (arrayLength === null || arrayLength < 1 || arrayLength > 4096) return { changed: 0 };

    var count = Math.min(size, arrayLength, 64);
    var changed = 0;
    var nextTeam = 0;
    for (var i = 0; i < count; i++) {
      var clientData = readPointer(items.add(OFF.Array_items + i * Process.pointerSize));
      if (!clientData) continue;
      var isBot = readU8(clientData.add(OFF.ClientData_isBot));
      if (!isBot) continue;

      var joinTeam = readS32(clientData.add(OFF.ClientData_joinTeam));
      var desiredTeam = nextTeam;
      nextTeam = nextTeam === 0 ? 1 : 0;

      if (joinTeam !== desiredTeam) {
        clientData.add(OFF.ClientData_joinTeam).writeS32(desiredTeam);
        changed += 1;
      }
    }

    if (changed > 0) {
      sendLog('warn', '团队规则下已将 Neutral bot 分配到 BL/GR：' + changed + ' 个 via ' + (reason || 'manual'));
    }
    return { changed: changed };
  }

  function ensureTeamRuleSpawnFallbacks(reason) {
    if (!Runtime.enabled || !teamRulesAreActiveForCurrentStart()) return false;
    var bl = ensureTeamSpawnFallbackFromNeutral(0, reason);
    var gr = ensureTeamSpawnFallbackFromNeutral(1, reason);
    return !!(bl || gr);
  }

  function applyTeamDeathWeaponOnlyMode(selected, beforeMode) {
    var targetAsset = findTargetMapAsset(Runtime.gameRoom, MODES.team_death.gameMode);
    if (!targetAsset) return fail('找不到团队竞技 MapAsset: ' + selected.label);

    var basePrefab = readPointer(targetAsset.add(OFF.MapAsset_gameModePrefab));
    var targetEntry = resolveTargetMapRuleEntry(targetAsset, Runtime.lastMapID);
    var targetPrefab = targetEntry.ready && targetEntry.prefabOverride ? targetEntry.prefabOverride : basePrefab;
    var prefabSource = targetEntry.ready && targetEntry.prefabOverride ? 'teamDeath.datas[' + Runtime.lastMapID + '].gameModePrefabOverride' : 'teamDeath.gameModePrefab';
    if (!targetPrefab) return fail('团队竞技 gameModePrefab 为空: ' + selected.label);

    var staticFields = resolveGameManagerStaticFields();
    if (!staticFields) return fail('GameManager.static_fields 尚未初始化');

    try {
      staticFields.add(OFF.GameManager_gameMode).writeS32(MODES.team_death.gameMode);
      staticFields.add(OFF.GameManager_weaponLimited).writeS32(selected.weaponLimited);
      if (!writeManagedReference(staticFields.add(OFF.GameManager_gameModePrefab), targetPrefab)) {
        return fail('团队刀战 gameModePrefab 写入校验失败');
      }

      var modeReadBack = staticFields.add(OFF.GameManager_gameMode).readS32();
      var limitReadBack = staticFields.add(OFF.GameManager_weaponLimited).readS32();
      if (modeReadBack !== MODES.team_death.gameMode || limitReadBack !== selected.weaponLimited) {
        return fail('团队刀战模式字段写入校验失败');
      }

      Runtime.applyCount += 1;
      Runtime.lastError = null;
      Runtime.lastApplied = {
        key: Runtime.modeKey,
        label: selected.label,
        gameMode: MODES.team_death.gameMode,
        originalGameMode: beforeMode.gameMode,
        sourceMapMode: Runtime.lastSourceMapMode,
        preservedGameMode: false,
        forceTeamRules: true,
        weaponLimited: selected.weaponLimited,
        weaponLimitedSource: 'weapon-limited-on-nano team death override',
        mapID: Runtime.lastMapID,
        mapEntry: targetEntry,
        prefab: targetPrefab.toString(),
        prefabSource: prefabSource,
        before: beforeMode,
        count: Runtime.applyCount
      };
      sendLog('success', '下一局已套用 ' + selected.label + '：生化类地图改为团队竞技规则，weaponLimited=' + selected.weaponLimited);
      return { ok: true, changed: true, msg: '已套用' + selected.label + '（生化地图转团队人头规则）' };
    } catch (e) {
      return fail('覆盖团队刀战模式失败', e);
    }
  }

  function applyWeaponOnlyMode(selected) {
    var staticFields = resolveGameManagerStaticFields();
    if (!staticFields) return fail('GameManager.static_fields 尚未初始化');

    try {
      var beforeMode = summarizeGameManagerMode();
      if (shouldTeamDeathWeaponOnlyOverride(selected, beforeMode)) return applyTeamDeathWeaponOnlyMode(selected, beforeMode);

      staticFields.add(OFF.GameManager_weaponLimited).writeS32(selected.weaponLimited);

      var limitReadBack = staticFields.add(OFF.GameManager_weaponLimited).readS32();
      if (limitReadBack !== selected.weaponLimited) {
        return fail('武器限制字段写入校验失败');
      }

      var afterMode = summarizeGameManagerMode();
      Runtime.applyCount += 1;
      Runtime.lastError = null;
      Runtime.lastApplied = {
        key: Runtime.modeKey,
        label: selected.label,
        gameMode: afterMode.gameMode,
        preservedGameMode: true,
        weaponLimited: selected.weaponLimited,
        weaponLimitedSource: 'weapon-only overlay',
        mapID: Runtime.lastMapID,
        prefab: afterMode.prefab,
        prefabSource: 'preserved GameManager.gameModePrefab',
        before: beforeMode,
        count: Runtime.applyCount
      };
      sendLog('success', '下一局已套用 ' + selected.label + '：保留当前地图模式，只覆盖 weaponLimited=' + selected.weaponLimited);
      return { ok: true, changed: true, msg: '已套用 ' + selected.label + '（保留地图规则）' };
    } catch (e) {
      return fail('覆盖 GameManager 武器限制失败', e);
    }
  }

  function applySelectedMode() {
    if (!Runtime.enabled) return { ok: true, changed: false, msg: '功能未启用' };

    var selected = MODES[Runtime.modeKey];
    if (!selected) return fail('未知模式: ' + Runtime.modeKey);
    if (selected.weaponOnly) return applyWeaponOnlyMode(selected);

    var targetAsset = findTargetMapAsset(Runtime.gameRoom, selected.gameMode);
    if (!targetAsset) return fail('找不到目标模式 MapAsset: ' + selected.label);

    var basePrefab = readPointer(targetAsset.add(OFF.MapAsset_gameModePrefab));
    var targetEntry = resolveTargetMapRuleEntry(targetAsset, Runtime.lastMapID);
    var targetPrefab = targetEntry.ready && targetEntry.prefabOverride ? targetEntry.prefabOverride : basePrefab;
    var prefabSource = targetEntry.ready && targetEntry.prefabOverride ? 'targetAsset.datas[' + Runtime.lastMapID + '].gameModePrefabOverride' : 'targetAsset.gameModePrefab';
    if (!targetPrefab) return fail('目标模式 gameModePrefab 为空: ' + selected.label);

    var weaponLimited = selected.weaponLimited;
    var weaponLimitedSource = 'mode option';
    if (selected.useTargetMapWeaponLimited && targetEntry.ready && targetEntry.weaponLimited !== null) {
      weaponLimited = targetEntry.weaponLimited;
      weaponLimitedSource = targetEntry.weaponLimitedSource;
    }

    var staticFields = resolveGameManagerStaticFields();
    if (!staticFields) return fail('GameManager.static_fields 尚未初始化');

    try {
      staticFields.add(OFF.GameManager_gameMode).writeS32(selected.gameMode);
      staticFields.add(OFF.GameManager_weaponLimited).writeS32(weaponLimited);
      if (!writeManagedReference(staticFields.add(OFF.GameManager_gameModePrefab), targetPrefab)) {
        return fail('gameModePrefab 写入校验失败');
      }

      var modeReadBack = staticFields.add(OFF.GameManager_gameMode).readS32();
      var limitReadBack = staticFields.add(OFF.GameManager_weaponLimited).readS32();
      if (modeReadBack !== selected.gameMode || limitReadBack !== weaponLimited) {
        return fail('模式字段写入校验失败');
      }

      Runtime.applyCount += 1;
      Runtime.lastError = null;
      Runtime.lastApplied = {
        key: Runtime.modeKey,
        label: selected.label,
        gameMode: selected.gameMode,
        sourceMapMode: Runtime.lastSourceMapMode,
        weaponLimited: weaponLimited,
        weaponLimitedSource: weaponLimitedSource,
        mapID: Runtime.lastMapID,
        mapEntry: targetEntry,
        prefab: targetPrefab.toString(),
        prefabSource: prefabSource,
        count: Runtime.applyCount
      };
      sendLog('success', '下一局模式已替换为 ' + selected.label + '，weaponLimited=' + weaponLimited + '（' + weaponLimitedSource + '）');
      return { ok: true, changed: true, msg: '已替换为 ' + selected.label };
    } catch (e) {
      return fail('覆盖 GameManager 模式失败', e);
    }
  }

  function buildNanoRule(selected, dropdownsPtr) {
    var nanoFields = resolveMapAssetNanoStaticFields();
    var roundIndex = readDropdownValue(dropdownsPtr, 1, 2);
    var roundArray = nanoFields ? readPointer(nanoFields.add(OFF.MapAsset_Nano_RoundDatas)) : null;
    var round = readIntArrayElement(roundArray, roundIndex, [9, 11, 13, 15, 17], 2);
    var time;

    if (nanoFields && selected.gameMode === 6) {
      time = {
        value: {
          minute: readS32(nanoFields.add(OFF.MapAsset_Nano_GameTime_Nano4Terminator_X)),
          second: readS32(nanoFields.add(OFF.MapAsset_Nano_GameTime_Nano4Terminator_Y))
        },
        source: 'static.nano4Terminator'
      };
    } else if (nanoFields) {
      time = {
        value: {
          minute: readS32(nanoFields.add(OFF.MapAsset_Nano_GameTime_Nano4_X)),
          second: readS32(nanoFields.add(OFF.MapAsset_Nano_GameTime_Nano4_Y))
        },
        source: 'static.nano4'
      };
    }

    if (!time || !time.value || time.value.minute === null || time.value.second === null) {
      time = selected.gameMode === 6
        ? { value: { minute: 3, second: 30 }, source: 'fallback.nano4Terminator' }
        : { value: { minute: 2, second: 30 }, source: 'fallback.nano4' };
    }

    return {
      kind: 'nano',
      targetRound: round.value || 13,
      targetScore: 0,
      gameTime: time.value,
      respawnTime: 3.0,
      revengeEnable: 0,
      roundSource: round.source,
      timeSource: time.source,
      dropdownRoundIndex: roundIndex
    };
  }

  function shouldUseFixedTeamTimeLimit() {
    var teamDeathModeSelected = Runtime.modeKey === 'team_death';
    var weaponModeForcedToTeamRules = !!(Runtime.lastApplied && Runtime.lastApplied.forceTeamRules);
    return !!(
      Runtime.lastApplied &&
      Runtime.lastApplied.key === Runtime.modeKey &&
      (teamDeathModeSelected || weaponModeForcedToTeamRules) &&
      isNanoGameModeValue(Runtime.lastApplied.sourceMapMode)
    );
  }

  function buildTeamRule(dropdownsPtr) {
    if (shouldUseFixedTeamTimeLimit()) {
      return {
        kind: 'time',
        targetRound: 0,
        targetScore: 0,
        gameTime: { minute: 12, second: 0 },
        respawnTime: 3.0,
        revengeEnable: 1,
        winType: 1,
        valueIndex: 3,
        scoreSource: 'fixed.timeWin',
        timeSource: 'fixed.teamDeathFromNanoTimeLimit'
      };
    }

    var teamFields = resolveMapAssetTeamDeathStaticFields();
    var winType = readDropdownValue(dropdownsPtr, 0, 0);
    var valueIndex = readDropdownValue(dropdownsPtr, 1, winType === 1 ? 0 : 3);
    var killArray = teamFields ? readPointer(teamFields.add(OFF.MapAsset_TeamDeath_KillDatas)) : null;
    var timeArray = teamFields ? readPointer(teamFields.add(OFF.MapAsset_TeamDeath_TimeDatas)) : null;
    var timeWin = winType === 1;
    var score = { value: 0, source: 'timeWin' };
    var time;

    if (timeWin) {
      time = readVector2ArrayElement(timeArray, valueIndex, [
        { minute: 5, second: 0 },
        { minute: 8, second: 0 },
        { minute: 10, second: 0 },
        { minute: 12, second: 0 }
      ], 0);
    } else {
      score = readIntArrayElement(killArray, valueIndex, [40, 60, 80, 100, 150], 3);
      if (teamFields) {
        time = {
          value: {
            minute: readS32(teamFields.add(OFF.MapAsset_TeamDeath_KillConditionTime_X)),
            second: readS32(teamFields.add(OFF.MapAsset_TeamDeath_KillConditionTime_Y))
          },
          source: 'static.killConditionTime'
        };
      }
      if (!time || !time.value || time.value.minute === null || time.value.second === null) {
        time = { value: { minute: 20, second: 0 }, source: 'fallback.killConditionTime' };
      }
    }

    return {
      kind: 'score',
      targetRound: 0,
      targetScore: score.value,
      gameTime: time.value,
      respawnTime: 3.0,
      revengeEnable: 1,
      winType: winType,
      valueIndex: valueIndex,
      scoreSource: score.source,
      timeSource: time.source
    };
  }

  function applySelectedModeRules(reason) {
    if (!Runtime.enabled) return { ok: true, changed: false, msg: '功能未启用' };

    var selected = MODES[Runtime.modeKey];
    if (!selected) return fail('未知模式: ' + Runtime.modeKey);
    if (selected.weaponOnly && !shouldUseTeamRulesForWeaponOnly(selected)) {
      Runtime.ruleSyncLast = {
        reason: reason || 'manual',
        key: Runtime.modeKey,
        label: selected.label,
        skipped: true,
        msg: '武器限制模式沿用地图原规则',
        gameManager: summarizeGameManagerMode(),
        readback: summarizeModeBaseStatic()
      };
      return { ok: true, changed: false, msg: '武器限制模式沿用地图原规则' };
    }

    var gmFields = resolveGameManagerStaticFields();
    var modeFields = resolveModeBaseStaticFields();
    if (!gmFields || !modeFields) return fail('规则静态字段尚未初始化');

    var rule = isNanoGameModeValue(selected.gameMode)
      ? buildNanoRule(selected, Runtime.lastDropdowns)
      : buildTeamRule(Runtime.lastDropdowns);

    try {
      gmFields.add(OFF.GameManager_revengeEnable).writeU8(rule.revengeEnable ? 1 : 0);
      gmFields.add(OFF.GameManager_gameRoundOver).writeU8(0);
      modeFields.add(OFF.ModeBase_targetRound).writeS32(rule.targetRound);
      modeFields.add(OFF.ModeBase_targetScore).writeS32(rule.targetScore);
      modeFields.add(OFF.ModeBase_gameTime_X).writeS32(rule.gameTime.minute);
      modeFields.add(OFF.ModeBase_gameTime_Y).writeS32(rule.gameTime.second);
      modeFields.add(OFF.ModeBase_respawnTime).writeFloat(rule.respawnTime);

      Runtime.ruleSyncCount += 1;
      Runtime.ruleSyncLast = {
        reason: reason || 'manual',
        key: Runtime.modeKey,
        label: selected.label,
        rule: rule,
        readback: summarizeModeBaseStatic(),
        gameManager: summarizeGameManagerMode()
      };
      sendLog(
        'success',
        '模式规则已同步为 ' + selected.label +
        '（' + rule.kind +
        ', targetRound=' + rule.targetRound +
        ', targetScore=' + rule.targetScore +
        ', gameTime=' + rule.gameTime.minute + ':' + rule.gameTime.second +
        '）'
      );
      return { ok: true, changed: true, msg: '规则已同步', rule: Runtime.ruleSyncLast };
    } catch (e) {
      return fail('覆盖模式规则失败', e);
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
      Runtime.getWpnData = new NativeFunction(
        base.add(RVA.GameManager_GetWpnData),
        'bool',
        ['int', 'pointer', 'pointer'],
        'mscdecl'
      );
      Runtime.createUpgradeBoxGenerator = new NativeFunction(
        base.add(RVA.Mode_Nano4_Terminator_UpgrandeBoxGenerator),
        'pointer',
        ['pointer', 'int', 'int', 'pointer'],
        'mscdecl'
      );
      Runtime.startCoroutineAuto = new NativeFunction(
        base.add(RVA.UnityEngine_MonoBehaviour_StartCoroutine_Auto),
        'pointer',
        ['pointer', 'pointer', 'pointer'],
        'mscdecl'
      );
      Runtime.objectNew = new NativeFunction(
        base.add(RVA.ManagedObject_New),
        'pointer',
        ['pointer'],
        'mscdecl'
      );
      Runtime.listIntCtor = new NativeFunction(
        base.add(RVA.List_int_ctor),
        'void',
        ['pointer', 'pointer'],
        'mscdecl'
      );
      Runtime.listIntAdd = new NativeFunction(
        base.add(RVA.List_int_Add),
        'void',
        ['pointer', 'int', 'pointer'],
        'mscdecl'
      );

      Runtime.hooks.push(Interceptor.attach(base.add(RVA.UI_GameRoom_OnStartGameBtnDown), {
        onEnter: function (args) {
          Runtime.gameRoom = args[0];
          Runtime.mapManager = null;
          Runtime.modeBase = null;
          Runtime.lastDropdowns = null;
          Runtime.lastMapID = null;
          Runtime.lastSourceMapMode = null;
          Runtime.deferModeApplyUntilBotGeneration = false;
          Runtime.deferredModeApplyReason = null;
          Runtime.terminatorSupplyCompatLast = null;
          Runtime.terminatorSupplyAttrPtrs = {};
          Runtime.supplyBoxSpawnFallbackLast = null;
          Runtime.supplyBoxPipelineDiagnostics = 0;
          Runtime.supplyBoxPipelineLast = null;
          Runtime.supplyBoxPointRequests = 0;
          Runtime.supplyBoxPointLast = null;
          Runtime.upgradeBoxGeneratorNativeKeys = {};
          Runtime.upgradeBoxGeneratorNativeLast = null;
          Runtime.upgradeBoxGeneratorFallbackKeys = {};
          Runtime.upgradeBoxGeneratorFallbackLast = null;
          resetWeaponGrantProbe();
          Runtime.startDepth += 1;
        },
        onLeave: function () {
          if (Runtime.enabled && Runtime.startDepth > 0) {
            applySelectedModeRules('OnStartGameBtnDown.leave.rules');
          }
          Runtime.startDepth = Math.max(0, Runtime.startDepth - 1);
        }
      }));

      Runtime.hooks.push(Interceptor.attach(base.add(RVA.MapAsset_ApplyGameSetting), {
        onEnter: function (args) {
          if (Runtime.enabled && Runtime.startDepth > 0) {
            Runtime.lastMapID = args[1].toInt32();
            Runtime.lastDropdowns = args[2];
            Runtime.lastSourceMapMode = readS32(args[0].add(OFF.MapAsset_gameMode));
          }
        },
        onLeave: function () {
          if (Runtime.enabled && Runtime.startDepth > 0) {
            var selected = MODES[Runtime.modeKey];
            if (shouldDeferNanoModeApplyUntilBotGeneration(selected)) markDeferredModeApply('ApplyGameSetting.leave');
            else applySelectedMode();
            normalizeRoomBotTeamsForTeamRules('ApplyGameSetting.leave');
            normalizeRoomBotTeamsForNanoRules('ApplyGameSetting.leave');
          }
        }
      }));

      Runtime.hooks.push(Interceptor.attach(base.add(RVA.ModeBase_Nano_OnStartNewGameRound), {
        onEnter: function (args) {
          if (Runtime.enabled) {
            ensureTerminatorSupplyPointFallbacks('ModeBase_Nano.OnStartNewGameRound.enter');
            ensureTerminatorSupplyAttributeChain(args[0], 'ModeBase_Nano.OnStartNewGameRound.enter');
            logSupplyBoxPipeline('ModeBase_Nano.OnStartNewGameRound.afterSupplyFallback', { modeInstance: safePtrText(args[0]) });
          }
        }
      }));

      Runtime.hooks.push(Interceptor.attach(base.add(RVA.StartGenerateSupplyBox), {
        onEnter: function (args) {
          if (Runtime.enabled) {
            ensureTerminatorSupplyPointFallbacks('StartGenerateSupplyBox.enter');
            ensureTerminatorSupplyAttributeChain(args[0], 'StartGenerateSupplyBox.enter');
            this.modeInstance = args[0];
            logSupplyBoxPipeline('StartGenerateSupplyBox.enter.afterSupplyFallback', { modeInstance: safePtrText(args[0]) });
          }
        },
        onLeave: function () {
          if (Runtime.enabled && this.modeInstance) {
            ensureTerminatorUpgradeBoxGeneratorsStarted(this.modeInstance, 'StartGenerateSupplyBox.leave');
            logSupplyBoxPipeline('StartGenerateSupplyBox.leave.afterGeneratorCheck', { modeInstance: safePtrText(this.modeInstance) });
          }
        }
      }));

      Runtime.hooks.push(Interceptor.attach(base.add(RVA.Mode_Nano4_Terminator_UpgrandeBoxGenerator), {
        onEnter: function (args) {
          if (Runtime.enabled) {
            markNativeUpgradeBoxGeneratorStarted(args[0], 'UpgrandeBoxGenerator.enter');
            logSupplyBoxPipeline('UpgrandeBoxGenerator.enter', {
              modeInstance: safePtrText(args[0]),
              generateNeedTime: args[1].toInt32(),
              team: args[2].toInt32()
            });
          }
        }
      }));

      Runtime.hooks.push(Interceptor.attach(base.add(RVA.UI_GameRoom_GenerateBotClient), {
        onLeave: function () {
          if (Runtime.enabled) {
            applyDeferredModeAfterBotGeneration('GenerateBotClient.leave');
            normalizeRoomBotTeamsForTeamRules('GenerateBotClient.leave');
            normalizeRoomBotTeamsForNanoRules('GenerateBotClient.leave');
          }
        }
      }));

      Runtime.hooks.push(Interceptor.attach(base.add(RVA.GameManager_AddPlayers), {
        onEnter: function () {
          if (Runtime.enabled) {
            applyDeferredModeAfterBotGeneration('GameManager.AddPlayers.enter');
            normalizeRoomBotTeamsForTeamRules('GameManager.AddPlayers.enter');
            normalizeRoomBotTeamsForNanoRules('GameManager.AddPlayers.enter');
            ensureTeamRuleSpawnFallbacks('GameManager.AddPlayers.enter');
            ensureNanoRuleSpawnFallbacks('GameManager.AddPlayers.enter');
            resetWeaponGrantProbe();
          }
        }
      }));

      Runtime.hooks.push(Interceptor.attach(base.add(RVA.MapManager_Awake), {
        onEnter: function (args) {
          if (!Runtime.enabled) return;
          Runtime.mapManager = args[0];
          ensureTeamRuleSpawnFallbacks('MapManager.Awake');
          ensureNanoRuleSpawnFallbacks('MapManager.Awake');
          ensureTerminatorSupplyPointFallbacks('MapManager.Awake');
          logSupplyBoxPipeline('MapManager.Awake.afterSupplyFallback', { mapManager: safePtrText(args[0]) });
        }
      }));

      Runtime.hooks.push(Interceptor.attach(base.add(RVA.MapManager_GetSupplyBoxPoint), {
        onEnter: function (args) {
          if (!Runtime.enabled) return;
          this.supplyBoxType = args[1].toInt32();
          Runtime.supplyBoxPointRequests += 1;
          Runtime.supplyBoxPointLast = {
            stage: 'enter',
            type: this.supplyBoxType,
            typeLabel: supplyBoxTypeLabel(this.supplyBoxType),
            count: Runtime.supplyBoxPointRequests
          };
          logSupplyBoxPipeline('GetSupplyBoxPoint.enter', Runtime.supplyBoxPointLast);
          try {
            ensureTerminatorSupplyPointFallbacks('GetSupplyBoxPoint.enter');
          } catch (e) {
            fail('SupplyBox point fallback failed at GetSupplyBoxPoint.enter', e);
          }
        },
        onLeave: function (retval) {
          if (!Runtime.enabled || this.supplyBoxType === undefined) return;
          var resultIndex = retval.toInt32();
          Runtime.supplyBoxPointLast = {
            stage: 'leave',
            type: this.supplyBoxType,
            typeLabel: supplyBoxTypeLabel(this.supplyBoxType),
            resultIndex: resultIndex,
            count: Runtime.supplyBoxPointRequests
          };
          logSupplyBoxPipeline('GetSupplyBoxPoint.leave', Runtime.supplyBoxPointLast);
        }
      }));

      Runtime.hooks.push(Interceptor.attach(base.add(RVA.MapManager_GetSpawnPoint), {
        onEnter: function (args) {
          if (!Runtime.enabled) return;
          Runtime.mapManager = args[0];
          var team = args[1].toInt32();
          if (team === 2) ensureNeutralSpawnFallbackFromTeam('GetSpawnPoint');
          else ensureTeamSpawnFallbackFromNeutral(team, 'GetSpawnPoint');
        }
      }));

      Runtime.hooks.push(Interceptor.attach(base.add(RVA.GameManager_GiveWeaponByBag), {
        onEnter: function (args) {
          Runtime.weaponProbe.giveWeaponByBagDepth += 1;
          maybeOverrideLimitedBotGrant(args);
        },
        onLeave: function () {
          Runtime.weaponProbe.giveWeaponByBagDepth = Math.max(0, Runtime.weaponProbe.giveWeaponByBagDepth - 1);
        }
      }));

      Runtime.hooks.push(Interceptor.attach(base.add(RVA.Player_Spawn), {
        onEnter: function (args) {
          if (Runtime.enabled) resetWeaponGrantForPlayer(args[0]);
        }
      }));

      Runtime.hooks.push(Interceptor.attach(base.add(RVA.Player_Respawn), {
        onEnter: function (args) {
          if (Runtime.enabled) resetWeaponGrantForPlayer(args[0]);
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
      teamSpawnFallbackCount: Runtime.teamSpawnFallbackCount,
      teamSpawnFallbackLast: Runtime.teamSpawnFallbackLast,
      supplyBoxSpawnFallbackCount: Runtime.supplyBoxSpawnFallbackCount,
      supplyBoxSpawnFallbackLast: Runtime.supplyBoxSpawnFallbackLast,
      supplyBoxPipelineDiagnostics: Runtime.supplyBoxPipelineDiagnostics,
      supplyBoxPipelineLast: Runtime.supplyBoxPipelineLast,
      supplyBoxPointRequests: Runtime.supplyBoxPointRequests,
      supplyBoxPointLast: Runtime.supplyBoxPointLast,
      ruleSyncCount: Runtime.ruleSyncCount,
      ruleSyncLast: Runtime.ruleSyncLast,
      terminatorSupplyCompatHits: Runtime.terminatorSupplyCompatHits,
      terminatorSupplyCompatLast: Runtime.terminatorSupplyCompatLast,
      terminatorSupplyAttrLoadCount: Runtime.terminatorSupplyAttrLoadCount,
      upgradeBoxGeneratorNativeCount: Runtime.upgradeBoxGeneratorNativeCount,
      upgradeBoxGeneratorNativeLast: Runtime.upgradeBoxGeneratorNativeLast,
      upgradeBoxGeneratorFallbackCount: Runtime.upgradeBoxGeneratorFallbackCount,
      upgradeBoxGeneratorFallbackLast: Runtime.upgradeBoxGeneratorFallbackLast,
      botSniperOverrideHits: Runtime.botSniperOverrideHits,
      botSniperOverrideLast: Runtime.botSniperOverrideLast,
      probe: {
        enabled: Runtime.probe.enabled,
        level: Runtime.probe.level,
        probeLevel: Runtime.probe.level,
        generateBotHits: Runtime.probe.generateBotHits,
        addPlayersHits: Runtime.probe.addPlayersHits,
        addPlayerHits: Runtime.probe.addPlayerHits,
        spawnHits: Runtime.probe.spawnHits,
        respawnHits: Runtime.probe.respawnHits,
        getSpawnPointMissingHits: Runtime.probe.getSpawnPointMissingHits,
        lifecycleHits: Runtime.probe.lifecycleHits,
        deathEventHits: Runtime.probe.deathEventHits,
        roundBoundaryHits: Runtime.probe.roundBoundaryHits,
        weaponBagHits: Runtime.probe.weaponBagHits,
        giveWeaponHits: Runtime.probe.giveWeaponHits,
        giveWeaponByBagHits: Runtime.probe.giveWeaponByBagHits,
        weaponMismatchHits: Runtime.probe.weaponMismatchHits,
        lastWeaponBag: Runtime.probe.lastWeaponBag,
        lastWeaponGrantSummary: Runtime.probe.lastWeaponGrantSummary,
        lastLifecycle: Runtime.probe.lastLifecycle,
        last: Runtime.probe.last,
        recent: Runtime.probe.recent
      },
      lastError: Runtime.lastError,
      pointerSize: Process.pointerSize
    };
  }

  function resetProbe() {
    Runtime.probe.generateBotHits = 0;
    Runtime.probe.addPlayersHits = 0;
    Runtime.probe.addPlayerHits = 0;
    Runtime.probe.spawnHits = 0;
    Runtime.probe.respawnHits = 0;
    Runtime.probe.getSpawnPointMissingHits = 0;
    Runtime.probe.lifecycleHits = 0;
    Runtime.probe.deathEventHits = 0;
    Runtime.probe.roundBoundaryHits = 0;
    Runtime.probe.weaponBagHits = 0;
    Runtime.probe.giveWeaponHits = 0;
    Runtime.probe.giveWeaponByBagHits = 0;
    Runtime.probe.weaponMismatchHits = 0;
    Runtime.probe.lastWeaponBag = null;
    Runtime.probe.lastWeaponGrantSummary = null;
    resetWeaponGrantProbe();
    Runtime.probe.lastLifecycle = null;
    Runtime.probe.lastLifecycleKey = null;
    Runtime.probe.lastLifecycleLogMs = 0;
    Runtime.probe.recent = [];
    Runtime.probe.last = null;
    Runtime.ruleSyncLast = null;
    Runtime.supplyBoxSpawnFallbackCount = 0;
    Runtime.supplyBoxSpawnFallbackLast = null;
    Runtime.supplyBoxPipelineDiagnostics = 0;
    Runtime.supplyBoxPipelineLast = null;
    Runtime.supplyBoxPointRequests = 0;
    Runtime.supplyBoxPointLast = null;
    Runtime.terminatorSupplyCompatHits = 0;
    Runtime.terminatorSupplyCompatLast = null;
    Runtime.terminatorSupplyAttrLoadCount = 0;
    Runtime.terminatorSupplyAttrPtrs = {};
    Runtime.upgradeBoxGeneratorNativeCount = 0;
    Runtime.upgradeBoxGeneratorNativeKeys = {};
    Runtime.upgradeBoxGeneratorNativeLast = null;
    Runtime.upgradeBoxGeneratorFallbackCount = 0;
    Runtime.upgradeBoxGeneratorFallbackKeys = {};
    Runtime.upgradeBoxGeneratorFallbackLast = null;
    Runtime.botSniperOverrideHits = 0;
    Runtime.botSniperOverrideLast = null;
    return statusObject();
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
    Runtime.modeBase = null;
    Runtime.lastDropdowns = null;
    Runtime.lastMapID = null;
    Runtime.lastSourceMapMode = null;
    Runtime.deferModeApplyUntilBotGeneration = false;
    Runtime.deferredModeApplyReason = null;
    Runtime.terminatorSupplyCompatLast = null;
    Runtime.terminatorSupplyAttrPtrs = {};
    Runtime.supplyBoxSpawnFallbackLast = null;
    Runtime.supplyBoxPipelineLast = null;
    Runtime.supplyBoxPointLast = null;
    Runtime.upgradeBoxGeneratorNativeKeys = {};
    Runtime.upgradeBoxGeneratorNativeLast = null;
    Runtime.upgradeBoxGeneratorFallbackKeys = {};
    Runtime.upgradeBoxGeneratorFallbackLast = null;
    Runtime.startDepth = 0;
    Runtime.getWpnData = null;
    Runtime.createUpgradeBoxGenerator = null;
    Runtime.startCoroutineAuto = null;
    Runtime.objectNew = null;
    Runtime.listIntCtor = null;
    Runtime.listIntAdd = null;
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

    setConfig: function (config) {
      return rpc.exports.setconfig(config || {});
    },

    set_config: function (config) {
      return rpc.exports.setconfig(config || {});
    },

    enable: function (config) {
      if (config) {
        var configResult = rpc.exports.setconfig(config);
        if (configResult && configResult.ok === false) return configResult;
      }
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
