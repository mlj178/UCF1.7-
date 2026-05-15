(function () {
    'use strict';

    function sendLog(level, module, message) {
        send({ type: 'log', level: level, module: module, message: message });
    }

    var gameAssembly = Process.findModuleByName("GameAssembly.dll");
    if (!gameAssembly) {
        sendLog('error', '系统', '未找到 GameAssembly.dll');
        return;
    }

    sendLog('info', '系统', 'GameAssembly.dll: base=' + gameAssembly.base);
    var base = gameAssembly.base;

    function readPtr(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            var v = addr.readPointer();
            return (v && !v.isNull()) ? v : null;
        } catch (e) { return null; }
    }

    function readI32(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            return addr.readS32();
        } catch (e) { return null; }
    }

    function readF32(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            return addr.readFloat();
        } catch (e) { return null; }
    }

    function readU8(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            return addr.readU8();
        } catch (e) { return null; }
    }

    function readStr(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            var p = addr.readPointer();
            if (!p || p.isNull()) return null;
            var len = p.add(-4).readS32();
            if (len < 0 || len > 200) return null;
            return p.readUtf8String(len);
        } catch (e) { return null; }
    }

    function hex(n) { return '0x' + n.toString(16).toUpperCase(); }
    function pad(s, n) { return (s || '').toString().padEnd(n, ' '); }

    var RVA_PLAYER_IS_MY = 0xB55FD0;

    var myPlayerPtr = null;
    var allPlayers = {};
    var inst = {};

    sendLog('info', '系统', '开始 Hook Player$$get_isMyPlayer ...');

    try {
        var addrIsMy = base.add(RVA_PLAYER_IS_MY);
        var origIsMy = new NativeFunction(addrIsMy, 'bool', ['pointer', 'pointer']);

        Interceptor.replace(addrIsMy, new NativeCallback(function (playerPtr, methodInfo) {
            try {
                var result = origIsMy(playerPtr, methodInfo);
                if (playerPtr && !playerPtr.isNull()) {
                    allPlayers[playerPtr.toString()] = result;
                    if (result && !myPlayerPtr) {
                        myPlayerPtr = playerPtr;
                        inst.player = playerPtr;
                        setTimeout(function () { printAll(playerPtr); }, 1500);
                    }
                }
                return result;
            } catch (e) { return false; }
        }, 'bool', ['pointer', 'pointer']));

        sendLog('success', 'Hook', 'Player$$get_isMyPlayer OK');
    } catch (e) {
        sendLog('error', 'Hook', 'Player$$get_isMyPlayer 失败: ' + e);
    }

    function printAll(pp) {
        sendLog('info', '', '');
        sendLog('success', '╔══════════════════════════════════════════════════════════════════════════╗', '');
        sendLog('success', '║                    玩家实例地址汇总 (偏移已修正)                         ║', '');
        sendLog('success', '╚══════════════════════════════════════════════════════════════════════════╝', '');

        collectEntity(pp);
        collectPlayer(pp);
        collectClientData(pp);
        collectPlayerData(pp);
        collectPlayerInput(pp);
        collectPlayerWeapons(pp);
        collectWeaponBag(pp);
        collectPlayerSkills(pp);
        collectNanoRoleSelect(pp);
        collectNano4TData(pp);
        collectPlayerCameraManager(pp);
        collectRecoil(pp);
        collectHealthData(pp);
        collectBuffList(pp);
        collectBot(pp);
        collectCharacterEffect(pp);
        collectNano4TAttribute();
        collectNano4TAttributeAsset();
        collectSkillArray();
        collectCurrentWeapon();

        printSummary();
    }

    function collectEntity(pp) {
        sendLog('info', '', '');
        sendLog('info', '┌──────────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【Entity 类】 实体基类 (Player 继承此类)                                │', '');
        sendLog('info', '├──────────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + pp + ' (与Player相同)', '');

        var v;
        v = readF32(pp.add(0xC));
        if (v !== null) sendLog('info', '│  [0x0C] baseMoveSpeed (float)       → ' + v, '');

        v = readF32(pp.add(0x10));
        if (v !== null) sendLog('info', '│  [0x10] speedPenalty (float)        → ' + v, '');

        v = readF32(pp.add(0x14));
        if (v !== null) sendLog('info', '│  [0x14] damageRate (float)          → ' + v, '');

        v = readU8(pp.add(0x18));
        if (v !== null) sendLog('info', '│  [0x18] isInvincible (bool)         → ' + (v ? 'true' : 'false'), '');

        v = readPtr(pp.add(0x1C));
        if (v) { inst.healthData = v; sendLog('success', '│  [0x1C] HealthData                  → ' + v, ''); }

        v = readI32(pp.add(0x20));
        if (v !== null) sendLog('info', '│  [0x20] team (int)                  → ' + v + (v === 0 ? ' (黑名单)' : ' (保卫者)'), '');

        v = readPtr(pp.add(0x28));
        if (v) sendLog('info', '│  [0x28] characterAnimator           → ' + v, '');

        v = readPtr(pp.add(0x2C));
        if (v) sendLog('info', '│  [0x2C] characterController         → ' + v, '');

        v = readU8(pp.add(0x30));
        if (v !== null) sendLog('info', '│  [0x30] isGhostEntity (bool)        → ' + (v ? 'true' : 'false'), '');

        v = readPtr(pp.add(0x34));
        if (v) { inst.buffs = v; sendLog('success', '│  [0x34] buffs (List<Buff>)          → ' + v, ''); }

        sendLog('info', '└──────────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectPlayer(pp) {
        sendLog('info', '', '');
        sendLog('info', '┌──────────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【Player 类】 玩家核心类 (继承Entity)                                   │', '');
        sendLog('info', '├──────────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + pp, '');

        var v;
        v = readPtr(pp.add(0x48));
        if (v) { inst.cameraManager = v; sendLog('success', '│  [0x48] PlayerCameraManager         → ' + v, ''); }

        v = readPtr(pp.add(0x54));
        if (v) { inst.recoil = v; sendLog('success', '│  [0x54] Recoil                      → ' + v, ''); }

        v = readPtr(pp.add(0x58));
        if (v) sendLog('info', '│  [0x58] characterContainer (Transform) → ' + v, '');

        v = readPtr(pp.add(0x5C));
        if (v) sendLog('info', '│  [0x5C] currentCharacter (CharacterModel) → ' + v, '');

        v = readU8(pp.add(0x70));
        if (v !== null) sendLog('info', '│  [0x70] isGrounded (bool)           → ' + (v ? 'true' : 'false'), '');

        v = readPtr(pp.add(0x8C));
        if (v) sendLog('info', '│  [0x8C] Modifier_MoveSpeedRatio     → ' + v, '');

        v = readPtr(pp.add(0x90));
        if (v) { inst.velData = v; sendLog('info', '│  [0x90] PlayerVelocity (velData)    → ' + v, ''); }

        v = readPtr(pp.add(0x94));
        if (v) { inst.clientData = v; sendLog('success', '│  [0x94] ClientData                  → ' + v, ''); }

        v = readPtr(pp.add(0x98));
        if (v) { inst.playerData = v; sendLog('success', '│  [0x98] PlayerData                  → ' + v, ''); }

        v = readPtr(pp.add(0x9C));
        if (v) { inst.playerInput = v; sendLog('success', '│  [0x9C] PlayerInput                 → ' + v, ''); }

        v = readPtr(pp.add(0xA0));
        if (v) { inst.playerWeapons = v; sendLog('success', '│  [0xA0] PlayerWeapons (wpns)        → ' + v, ''); }

        v = readPtr(pp.add(0xA4));
        if (v) { inst.weaponBag = v; sendLog('success', '│  [0xA4] WeaponBag                   → ' + v, ''); }

        v = readPtr(pp.add(0xA8));
        if (v) { inst.nanoRoleSelect = v; sendLog('success', '│  [0xA8] NanoRoleSelect              → ' + v, ''); }

        v = readPtr(pp.add(0xAC));
        if (v) { inst.nano4TData = v; sendLog('success', '│  [0xAC] Nano4T_Data                 → ' + v, ''); }

        v = readPtr(pp.add(0xB0));
        if (v) { inst.playerSkills = v; sendLog('success', '│  [0xB0] PlayerSkills (skills)       → ' + v, ''); }

        v = readU8(pp.add(0xB8));
        if (v !== null) sendLog('info', '│  [0xB8] isSniper (bool)             → ' + (v ? 'true' : 'false'), '');

        v = readPtr(pp.add(0x108));
        if (v) sendLog('info', '│  [0x108] mapTrigger (MapTrigger)     → ' + v, '');

        sendLog('info', '└──────────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectClientData(pp) {
        var p = inst.clientData;
        if (!p) return;
        sendLog('info', '', '');
        sendLog('info', '┌──────────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【ClientData 类】 客户端数据                                            │', '');
        sendLog('info', '├──────────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + p, '');

        var v;
        v = readI32(p.add(0x8));
        if (v !== null) sendLog('info', '│  [0x08] defaultWpnBagID (int)       → ' + v, '');

        v = readPtr(p.add(0xC));
        if (v) sendLog('info', '│  [0x0C] wpnBags (int[][])           → ' + v, '');

        v = readStr(p.add(0x10));
        if (v) sendLog('success', '│  [0x10] nickName (string)           → ' + v, '');

        v = readI32(p.add(0x14));
        if (v !== null) sendLog('info', '│  [0x14] level (int)                 → ' + v, '');

        v = readI32(p.add(0x18));
        if (v !== null) sendLog('info', '│  [0x18] joinTeam (Team/int)         → ' + v, '');

        v = readU8(p.add(0x1C));
        if (v !== null) sendLog('info', '│  [0x1C] isBot (bool)               → ' + (v ? 'true' : 'false'), '');

        v = readI32(p.add(0x20));
        if (v !== null) sendLog('info', '│  [0x20] vipLevel (int)              → ' + v, '');

        v = readI32(p.add(0x24));
        if (v !== null) sendLog('info', '│  [0x24] character (int)             → ' + v, '');

        sendLog('info', '└──────────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectPlayerData(pp) {
        var p = inst.playerData;
        if (!p) return;
        sendLog('info', '', '');
        sendLog('info', '┌──────────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【PlayerData 类】 玩家数据                                              │', '');
        sendLog('info', '├──────────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + p, '');

        var v;
        v = readI32(p.add(0x14));
        if (v !== null) sendLog('info', '│  [0x14] playerID (int)              → ' + v, '');

        v = readStr(p.add(0x18));
        if (v) sendLog('info', '│  [0x18] orignalCharacterName (string) → ' + v, '');

        v = readI32(p.add(0x1C));
        if (v !== null) sendLog('info', '│  [0x1C] rank (int)                  → ' + v, '');

        v = readI32(p.add(0x20));
        if (v !== null) sendLog('info', '│  [0x20] spawnCount (int)            → ' + v, '');

        v = readPtr(p.add(0x4C));
        if (v) sendLog('success', '│  [0x4C] kill (SubscribeableProperty<int>) → ' + v, '');

        v = readPtr(p.add(0x50));
        if (v) sendLog('success', '│  [0x50] death (SubscribeableProperty<int>) → ' + v, '');

        v = readPtr(p.add(0x54));
        if (v) sendLog('info', '│  [0x54] survival (SubscribeableProperty<int>) → ' + v, '');

        v = readPtr(p.add(0x58));
        if (v) sendLog('success', '│  [0x58] score (SubscribeableProperty<int>) → ' + v, '');

        v = readPtr(p.add(0x5C));
        if (v) sendLog('info', '│  [0x5C] aceSign (SubscribeableProperty<AceSign>) → ' + v, '');

        v = readPtr(p.add(0x60));
        if (v) sendLog('info', '│  [0x60] nanoRole (SubscribeableProperty<NanoRole>) → ' + v, '');

        v = readPtr(p.add(0x68));
        if (v) sendLog('info', '│  [0x68] revengeTarget (Player)      → ' + v, '');

        sendLog('info', '└──────────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectPlayerInput(pp) {
        var p = inst.playerInput;
        if (!p) return;
        sendLog('info', '', '');
        sendLog('info', '┌──────────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【PlayerInput 类】 输入控制器                                           │', '');
        sendLog('info', '├──────────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + p, '');

        var v;
        v = readI32(p.add(0x8));
        if (v !== null) sendLog('info', '│  [0x08] RightMouse (KeyInputState)  → ' + v, '');

        v = readI32(p.add(0xC));
        if (v !== null) sendLog('info', '│  [0x0C] JumpButton (KeyInputState)  → ' + v, '');

        sendLog('info', '└──────────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectPlayerWeapons(pp) {
        var p = inst.playerWeapons;
        if (!p) return;
        sendLog('info', '', '');
        sendLog('info', '┌──────────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【PlayerWeapons 类】 武器管理器                                         │', '');
        sendLog('info', '├──────────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + p, '');

        var v;
        v = readPtr(p.add(0x8));
        if (v) sendLog('info', '│  [0x08] owner (Player)              → ' + v, '');

        v = readPtr(p.add(0xC));
        if (v) sendLog('info', '│  [0x0C] all (List<Weapon>)          → ' + v, '');

        v = readI32(p.add(0x10));
        if (v !== null) sendLog('info', '│  [0x10] curSlot (int)               → ' + v, '');

        v = readI32(p.add(0x14));
        if (v !== null) sendLog('info', '│  [0x14] lastSlot (int)              → ' + v, '');

        v = readPtr(p.add(0x18));
        if (v) { inst.currentWeapon = v; sendLog('success', '│  [0x18] inUse (Weapon/当前武器)     → ' + v, ''); }

        v = readPtr(p.add(0x1C));
        if (v) sendLog('info', '│  [0x1C] current (Weapon[])          → ' + v, '');

        v = readPtr(p.add(0x20));
        if (v) sendLog('info', '│  [0x20] normal (Weapon[])           → ' + v, '');

        v = readPtr(p.add(0x24));
        if (v) sendLog('info', '│  [0x24] special (Weapon[])          → ' + v, '');

        v = readPtr(p.add(0x28));
        if (v) sendLog('info', '│  [0x28] temporaryWpn (Weapon)      → ' + v, '');

        v = readPtr(p.add(0x2C));
        if (v) sendLog('info', '│  [0x2C] F_KeyWpn (Weapon)          → ' + v, '');

        v = readPtr(p.add(0x30));
        if (v) sendLog('info', '│  [0x30] mapWpn (Weapon)            → ' + v, '');

        v = readPtr(p.add(0x3C));
        if (v) sendLog('info', '│  [0x3C] Modifier_ReloadSpeed       → ' + v, '');

        v = readPtr(p.add(0x40));
        if (v) sendLog('info', '│  [0x40] Modifier_KnifeRange        → ' + v, '');

        v = readPtr(p.add(0x44));
        if (v) sendLog('info', '│  [0x44] Modifier_KnifeSpeed        → ' + v, '');

        sendLog('info', '└──────────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectWeaponBag(pp) {
        var p = inst.weaponBag;
        if (!p) return;
        sendLog('info', '', '');
        sendLog('info', '┌──────────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【WeaponBag 类】 武器背包                                               │', '');
        sendLog('info', '├──────────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + p, '');

        var v;
        v = readPtr(p.add(0x8));
        if (v) sendLog('info', '│  [0x08] disabled (ObscuredBool)     → ' + v, '');

        v = readPtr(p.add(0x20));
        if (v) sendLog('info', '│  [0x20] available (bool[])          → ' + v, '');

        v = readPtr(p.add(0x24));
        if (v) sendLog('info', '│  [0x24] weaponID (int[][])          → ' + v, '');

        v = readI32(p.add(0x28));
        if (v !== null) sendLog('info', '│  [0x28] currentBagID (int)          → ' + v, '');

        sendLog('info', '└──────────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectPlayerSkills(pp) {
        var p = inst.playerSkills;
        if (!p) return;
        sendLog('info', '', '');
        sendLog('info', '┌──────────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【PlayerSkills 类】 技能管理器                                          │', '');
        sendLog('info', '├──────────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + p, '');

        var v;
        v = readPtr(p.add(0x8));
        if (v) { inst.skillArray = v; sendLog('info', '│  [0x08] all (Skill[])               → ' + v, ''); }

        v = readPtr(p.add(0xC));
        if (v) sendLog('info', '│  [0x0C] owner (Player)              → ' + v, '');

        sendLog('info', '└──────────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectNanoRoleSelect(pp) {
        var p = inst.nanoRoleSelect;
        if (!p) return;
        sendLog('info', '', '');
        sendLog('info', '┌──────────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【NanoRoleSelect 类】 纳米角色选择器                                    │', '');
        sendLog('info', '├──────────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + p, '');

        var v;
        v = readPtr(p.add(0x8));
        if (v) sendLog('info', '│  [0x08] owner (Player)              → ' + v, '');

        v = readI32(p.add(0xC));
        if (v !== null) sendLog('info', '│  [0x0C] tableType (NanoRoleSelect.Type) → ' + v, '');

        v = readF32(p.add(0x10));
        if (v !== null) sendLog('info', '│  [0x10] closeTime (float)           → ' + v, '');

        sendLog('info', '└──────────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectNano4TData(pp) {
        var p = inst.nano4TData;
        if (!p) return;
        sendLog('info', '', '');
        sendLog('info', '┌──────────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【Nano4T_Data 类】 纳米4T数据                                           │', '');
        sendLog('info', '├──────────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + p, '');

        var v;
        v = readPtr(p.add(0x8));
        if (v) sendLog('info', '│  [0x08] humanLayer (SubscribeableProperty<int>) → ' + v, '');

        v = readPtr(p.add(0xC));
        if (v) sendLog('info', '│  [0x0C] nanoLayer (SubscribeableProperty<int>) → ' + v, '');

        v = readPtr(p.add(0x10));
        if (v) sendLog('info', '│  [0x10] pickUpBoxCount (SubscribeableProperty<int>) → ' + v, '');

        v = readU8(p.add(0x14));
        if (v !== null) sendLog('info', '│  [0x14] canUseGrave (bool)          → ' + (v ? 'true' : 'false'), '');

        v = readI32(p.add(0x18));
        if (v !== null) sendLog('info', '│  [0x18] graveCount (int)            → ' + v, '');

        sendLog('info', '└──────────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectPlayerCameraManager(pp) {
        var p = inst.cameraManager;
        if (!p) return;
        sendLog('info', '', '');
        sendLog('info', '┌──────────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【PlayerCameraManager 类】 相机管理器                                   │', '');
        sendLog('info', '├──────────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + p, '');

        var v;
        v = readPtr(p.add(0xC));
        if (v) sendLog('info', '│  [0x0C] mapCamera (CinemachineVirtualCamera) → ' + v, '');

        v = readPtr(p.add(0x10));
        if (v) sendLog('info', '│  [0x10] modelCamera (Camera)        → ' + v, '');

        v = readF32(p.add(0x3C));
        if (v !== null) sendLog('info', '│  [0x3C] modelDefaultFOV (float)     → ' + v, '');

        sendLog('info', '└──────────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectRecoil(pp) {
        var p = inst.recoil;
        if (!p) return;
        sendLog('info', '', '');
        sendLog('info', '┌──────────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【Recoil 类】 后坐力控制器 (TypeDefIndex: 5559)                         │', '');
        sendLog('info', '├──────────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + p, '');

        var v;
        v = readPtr(p.add(0xC));
        if (v) sendLog('info', '│  [0x0C] shootPosture               → ' + v, '');

        v = readF32(p.add(0x68));
        if (v !== null) sendLog('info', '│  [0x68] addYaw (float)              → ' + v, '');

        v = readF32(p.add(0x6C));
        if (v !== null) sendLog('info', '│  [0x6C] addPitch (float)            → ' + v, '');

        v = readF32(p.add(0x70));
        if (v !== null) sendLog('info', '│  [0x70] addYaw_Target (float)       → ' + v, '');

        v = readF32(p.add(0x74));
        if (v !== null) sendLog('info', '│  [0x74] addPitch_Target (float)     → ' + v, '');

        sendLog('info', '└──────────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectHealthData(pp) {
        var p = inst.healthData;
        if (!p) return;
        sendLog('info', '', '');
        sendLog('info', '┌──────────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【HealthData 类】 生命值数据                                            │', '');
        sendLog('info', '├──────────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + p, '');

        sendLog('info', '│  [0x08] currentHealth (ObscuredInt)', '');
        sendLog('info', '│  [0x1C] maxHealth (ObscuredInt)', '');
        sendLog('info', '│  [0x30] tempHealth (ObscuredInt)', '');

        var v = readF32(p.add(0x44));
        if (v !== null) sendLog('info', '│  [0x44] invinsibleEndTime (float)   → ' + v, '');

        sendLog('info', '└──────────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectBuffList(pp) {
        var p = inst.buffs;
        if (!p) return;
        sendLog('info', '', '');
        sendLog('info', '┌──────────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【Buff 类】 Buff列表 (List<Buff>)                                       │', '');
        sendLog('info', '├──────────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  List实例地址: ' + p, '');

        var v = readI32(p.add(0x18));
        if (v !== null) sendLog('info', '│  Buff 数量 (list._size): ' + v, '');

        var itemsPtr = readPtr(p.add(0x10));
        if (itemsPtr) {
            var count = v || 0;
            if (count > 0 && count < 20) {
                for (var i = 0; i < count; i++) {
                    var buffPtr = readPtr(itemsPtr.add(0x4 * i + 0x8));
                    if (buffPtr) {
                        var buffName = readStr(buffPtr.add(0x8));
                        var endTime = readF32(buffPtr.add(0x10));
                        sendLog('info', '│  Buff[' + i + ']: ' + buffPtr + (buffName ? ' name=' + buffName : '') + (endTime !== null ? ' endTime=' + endTime : ''), '');
                    }
                }
            }
        }

        sendLog('info', '└──────────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectBot(pp) {
        sendLog('info', '', '');
        sendLog('info', '┌──────────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【Bot 类】 Bot控制器 (MonoBehaviour, TypeDefIndex: 5095)                │', '');
        sendLog('info', '├──────────────────────────────────────────────────────────────────────────┤', '');
        sendLog('info', '│  Bot是独立MonoBehaviour组件，与Player挂载在同一GameObject上', '');
        sendLog('info', '│  Player类无直接字段引用Bot，需通过GetComponent获取', '');
        sendLog('info', '│  本地玩家(isMyPlayer=true)不会有Bot组件', '');

        try {
            var il2cpp_class_from_name = new NativeFunction(
                Module.findExportByName('GameAssembly.dll', 'il2cpp_class_from_name'),
                'pointer', ['pointer', 'pointer', 'pointer']
            );
            var il2cpp_domain_get = new NativeFunction(
                Module.findExportByName('GameAssembly.dll', 'il2cpp_domain_get'),
                'pointer', []
            );
            var il2cpp_domain_get_assemblies = new NativeFunction(
                Module.findExportByName('GameAssembly.dll', 'il2cpp_domain_get_assemblies'),
                'pointer', ['pointer', 'pointer']
            );
            var il2cpp_assembly_get_image = new NativeFunction(
                Module.findExportByName('GameAssembly.dll', 'il2cpp_assembly_get_image'),
                'pointer', ['pointer']
            );
            var il2cpp_class_get_methods = new NativeFunction(
                Module.findExportByName('GameAssembly.dll', 'il2cpp_class_get_methods'),
                'pointer', ['pointer', 'pointer']
            );
            var il2cpp_method_get_name = new NativeFunction(
                Module.findExportByName('GameAssembly.dll', 'il2cpp_method_get_name'),
                'pointer', ['pointer']
            );

            var domain = il2cpp_domain_get();
            var sizePtr = Memory.alloc(4);
            var assemblies = il2cpp_domain_get_assemblies(domain, sizePtr);
            var asmCount = sizePtr.readU32();

            var botClass = null;
            for (var ai = 0; ai < asmCount; ai++) {
                var image = il2cpp_assembly_get_image(assemblies.add(Process.pointerSize * ai).readPointer());
                if (image.isNull()) continue;
                var ns = Memory.allocUtf8String('');
                var name = Memory.allocUtf8String('Bot');
                var cls = il2cpp_class_from_name(image, ns, name);
                if (!cls.isNull()) { botClass = cls; break; }
            }

            if (botClass && !botClass.isNull()) {
                sendLog('success', '│  Bot类元数据: ' + botClass, '');

                var il2cpp_class_get_static_field_data = new NativeFunction(
                    Module.findExportByName('GameAssembly.dll', 'il2cpp_class_get_static_field_data'),
                    'pointer', ['pointer']
                );
                var staticData = il2cpp_class_get_static_field_data(botClass);
                if (!staticData.isNull()) {
                    var stopAllBot = readU8(staticData.add(0xC));
                    if (stopAllBot !== null) sendLog('info', '│  [静态 0xC] stopAllBot (bool)       → ' + (stopAllBot ? 'true' : 'false'), '');
                }
            }
        } catch (e) {
            sendLog('info', '│  il2cpp API调用失败: ' + e.message, '');
        }

        sendLog('info', '│', '');
        sendLog('info', '│  Bot实例字段参考 (仅Bot玩家有):', '');
        sendLog('info', '│  [0x0C] ability (BotAbility struct)', '');
        sendLog('info', '│  [0x24] thisPlayer (Player)', '');
        sendLog('info', '│  [0x28] enemyInfo (BotEnemyInfo)', '');
        sendLog('info', '│  [0x3C] nextAttackTime (float)', '');
        sendLog('info', '│  [0x58] actionList (List<BotActionBase>)', '');
        sendLog('info', '└──────────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectNano4TAttribute() {
        sendLog('info', '', '');
        sendLog('info', '┌──────────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【Nano4T_Attribute 类】 纳米4T属性 (TypeDefIndex: 5223)                 │', '');
        sendLog('info', '├──────────────────────────────────────────────────────────────────────────┤', '');
        sendLog('info', '│  Nano4T_Attribute为普通class(非MonoBehaviour)，通过Nano4T_AttributeAsset引用', '');
        sendLog('info', '│  字段: [0x08] attributeName (string)', '');
        sendLog('info', '│  字段: [0x0C] id (int)', '');
        sendLog('info', '│  字段: [0x10] image (Sprite)', '');
        sendLog('info', '│  字段: [0x14] description (string)', '');
        sendLog('info', '│  常量: Gene=0, Terminator=1, Upgrade=2, Strong=3, Armor=4, Nail=5,', '');
        sendLog('info', '│        InfectExp=6, Hot=7, EvilBox=8, Grave=9, Savior=10, KillNano=11,', '');
        sendLog('info', '│        Grenade=12, Supply=13, Ammo=14, Reload=15, Shield=16, SPAgent=17,', '');
        sendLog('info', '│        HeroBox=18, Critical=19', '');
        sendLog('info', '│  静态字段: None (Nano4T_Attribute) @ 0x0', '');
        sendLog('info', '└──────────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectNano4TAttributeAsset() {
        sendLog('info', '', '');
        sendLog('info', '┌──────────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【Nano4T_AttributeAsset 类】 纳米4T属性资源 (ScriptableObject, TDI:5227)│', '');
        sendLog('info', '├──────────────────────────────────────────────────────────────────────────┤', '');
        sendLog('info', '│  ScriptableObject，通过Resources.Load加载，非Player直接引用', '');
        sendLog('info', '│  字段: [0x0C] normalRound (Group struct)', '');
        sendLog('info', '│  字段: [0x10] battleRound (Group struct)', '');
        sendLog('info', '│  字段: [0x14] attributes (Nano4T_Attribute[])', '');
        sendLog('info', '│  字段: [0x18] SkillBtn_GoldShield (GameObject)', '');
        sendLog('info', '│  字段: [0x1C] SFX_GoldShield (GameObject)', '');
        sendLog('info', '│  字段: [0x20] FX_GoldShield (GameObject)', '');
        sendLog('info', '│  内嵌结构体 Group: [0x08] nano (RandomItem), [0x0C] human (RandomItem)', '');
        sendLog('info', '└──────────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectSkillArray() {
        var p = inst.playerSkills;
        if (!p) return;
        sendLog('info', '', '');
        sendLog('info', '┌──────────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【Skill 类】 技能 (abstract class, TypeDefIndex: 5486)                  │', '');
        sendLog('info', '├──────────────────────────────────────────────────────────────────────────┤', '');

        var v;
        v = readPtr(p.add(0x8));
        if (v) {
            inst.skillArray = v;
            sendLog('success', '│  [0x08] all (Skill[])              → ' + v, '');

            try {
                var arrLen = v.add(0x18).readS32();
                if (arrLen >= 0 && arrLen < 10) {
                    var arrData = v.add(0x20).readPointer();
                    if (arrData && !arrData.isNull()) {
                        for (var i = 0; i < arrLen; i++) {
                            var skillPtr = readPtr(arrData.add(4 * i));
                            if (skillPtr) {
                                var skillName = readStr(skillPtr.add(0x8));
                                var skillBtn = readPtr(skillPtr.add(0xC));
                                var disabled = readU8(skillPtr.add(0x10));
                                sendLog('info', '│    Skill[' + i + ']: ' + skillPtr +
                                    (skillName ? ' name=' + skillName : '') +
                                    ' disabled=' + (disabled ? 'true' : 'false'), '');
                            }
                        }
                    }
                }
            } catch (e) {
                sendLog('info', '│  Skill数组遍历失败: ' + e.message, '');
            }
        } else {
            sendLog('info', '│  all (Skill[]) 为空', '');
        }

        v = readPtr(p.add(0xC));
        if (v) sendLog('info', '│  [0x0C] owner (Player)             → ' + v, '');

        sendLog('info', '│', '');
        sendLog('info', '│  Skill基类字段: [0x08] name, [0x0C] skillBtn, [0x10] disabled', '');
        sendLog('info', '│  Skill子类: SkillKnife, Skill_Grenade, Skill_SentryGun 等', '');
        sendLog('info', '└──────────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectCharacterEffect(pp) {
        sendLog('info', '', '');
        sendLog('info', '┌──────────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【CharacterEffect 类】 角色特效 (MonoBehaviour, TypeDefIndex: 5125)    │', '');
        sendLog('info', '├──────────────────────────────────────────────────────────────────────────┤', '');
        sendLog('info', '│  CharacterEffect是独立MonoBehaviour组件，与Player挂载在同一GameObject', '');
        sendLog('info', '│  Player类无直接字段引用CharacterEffect，需通过GetComponent获取', '');
        sendLog('info', '│', '');
        sendLog('info', '│  实例字段参考:', '');
        sendLog('info', '│  [0x0C] datas (FxData[])', '');
        sendLog('info', '│  [0x10] owner (Player)', '');
        sendLog('info', '│  [0x14] fxList (List<EffectObj>)', '');
        sendLog('info', '│  [0x18] isFxEnable (bool)', '');
        sendLog('info', '└──────────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectCurrentWeapon() {
        var p = inst.currentWeapon;
        if (!p) return;
        sendLog('info', '', '');
        sendLog('info', '┌──────────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【Weapon 类】 当前武器基类 (继承CFAnimator)                             │', '');
        sendLog('info', '├──────────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + p, '');

        var v;
        v = readPtr(p.add(0x68));
        if (v) { inst.weaponData = v; sendLog('success', '│  [0x68] data (WeaponData)           → ' + v, ''); }

        v = readU8(p.add(0x78));
        if (v !== null) sendLog('info', '│  [0x78] fireBtnPressed (bool)       → ' + (v ? 'true' : 'false'), '');

        v = readPtr(p.add(0xD0));
        if (v) { inst.mapGun = v; sendLog('info', '│  [0xD0] bindMapTrigger (MapGun)     → ' + v, ''); }

        sendLog('info', '', '');
        sendLog('info', '│  【WPN_Gun 类】 枪械 (继承Weapon, TypeDefIndex: 5577)', '');
        v = readPtr(p.add(0xEC));
        if (v) { inst.weaponDataGun = v; sendLog('success', '│  [0xEC] realData (WeaponData_Gun)   → ' + v, ''); }

        v = readU8(p.add(0xF0));
        if (v !== null) sendLog('info', '│  [0xF0] isSemiGun (bool)            → ' + (v ? 'true' : 'false'), '');

        v = readPtr(p.add(0xF4));
        if (v) { inst.ammoData = v; sendLog('success', '│  [0xF4] ammoData (WPN_Gun.AmmoData) → ' + v, ''); }

        v = readF32(p.add(0xFC));
        if (v !== null) sendLog('info', '│  [0xFC] lastShootTime (float)       → ' + v, '');

        v = readI32(p.add(0x100));
        if (v !== null) sendLog('info', '│  [0x100] recoilDataID (int)         → ' + v, '');

        v = readF32(p.add(0x110));
        if (v !== null) sendLog('success', '│  [0x110] nextAllowedShootTime (float) → ' + v, '');

        v = readI32(p.add(0x124));
        if (v !== null) sendLog('info', '│  [0x124] zoomIndex (int)            → ' + v, '');

        sendLog('info', '', '');
        sendLog('info', '│  【WPN_Knife 类】 近战武器 (继承Weapon, TypeDefIndex: 5580)', '');
        v = readF32(p.add(0xEC));
        if (v !== null) sendLog('info', '│  [0xEC] combo1_AnimSpeed (float)    → ' + v, '');

        sendLog('info', '└──────────────────────────────────────────────────────────────────────────┘', '');
    }

    function printSummary() {
        sendLog('info', '', '');
        sendLog('success', '╔══════════════════════════════════════════════════════════════════════════╗', '');
        sendLog('success', '║                         实例地址汇总表                                   ║', '');
        sendLog('success', '╠══════════════════════════════════════════════════════════════════════════╣', '');

        var rows = [
            { cat: '核心', name: 'Player', key: 'player', desc: '玩家实例' },
            { cat: '核心', name: 'Entity', key: 'player', desc: '实体基类(同Player)' },
            { cat: '核心', name: 'ClientData', key: 'clientData', desc: '客户端数据' },
            { cat: '核心', name: 'PlayerData', key: 'playerData', desc: '玩家数据' },
            { cat: '核心', name: 'PlayerInput', key: 'playerInput', desc: '输入控制' },
            { cat: '武器', name: 'PlayerWeapons', key: 'playerWeapons', desc: '武器管理器' },
            { cat: '武器', name: 'WeaponBag', key: 'weaponBag', desc: '武器背包' },
            { cat: '武器', name: 'Weapon (当前)', key: 'currentWeapon', desc: '当前武器' },
            { cat: '武器', name: 'WeaponData', key: 'weaponData', desc: '武器数据' },
            { cat: '武器', name: 'AmmoData', key: 'ammoData', desc: '弹药数据' },
            { cat: '技能', name: 'PlayerSkills', key: 'playerSkills', desc: '技能管理' },
            { cat: '技能', name: 'Skill[]', key: 'skillArray', desc: '技能数组' },
            { cat: '技能', name: 'NanoRoleSelect', key: 'nanoRoleSelect', desc: '纳米角色选择' },
            { cat: '技能', name: 'Nano4T_Data', key: 'nano4TData', desc: '纳米4T数据' },
            { cat: '视觉', name: 'PlayerCameraManager', key: 'cameraManager', desc: '相机管理' },
            { cat: '视觉', name: 'Recoil', key: 'recoil', desc: '后坐力' },
            { cat: '生命', name: 'HealthData', key: 'healthData', desc: '生命值数据' },
            { cat: '生命', name: 'Buff列表', key: 'buffs', desc: 'List<Buff>' }
        ];

        var lastCat = '';
        rows.forEach(function (r) {
            if (r.cat !== lastCat) {
                sendLog('info', '║  ── ' + r.cat + ' ──', '');
                lastCat = r.cat;
            }
            var addr = inst[r.key];
            if (addr) {
                sendLog('info', '║  ' + pad(r.name, 22) + ' │ ' + pad(r.desc, 14) + ' │ ' + addr, '');
            }
        });

        sendLog('success', '╚══════════════════════════════════════════════════════════════════════════╝', '');
    }

    globalThis.getPlayer = function () { return inst.player; };
    globalThis.getClientData = function () { return inst.clientData; };
    globalThis.getPlayerData = function () { return inst.playerData; };
    globalThis.getPlayerWeapons = function () { return inst.playerWeapons; };
    globalThis.getCurrentWeapon = function () { return inst.currentWeapon; };
    globalThis.getAmmoData = function () { return inst.ammoData; };
    globalThis.getRecoil = function () { return inst.recoil; };
    globalThis.getCameraManager = function () { return inst.cameraManager; };
    globalThis.getHealthData = function () { return inst.healthData; };
    globalThis.getPlayerSkills = function () { return inst.playerSkills; };
    globalThis.getWeaponData = function () { return inst.weaponDataGun; };
    globalThis.getGameManager = function () { return inst.gameManager; };
    globalThis.getMapManager = function () { return inst.mapManager; };
    globalThis.getPlayerController = function () { return inst.playerController; };
    globalThis.getInstances = function () { return inst; };

    globalThis.listAll = function () {
        sendLog('info', '', '');
        sendLog('info', '══════════════════════════════════════════════════════════════', '');
        sendLog('info', '                    所有 Player 实例列表                       ', '');
        sendLog('info', '══════════════════════════════════════════════════════════════', '');
        var keys = Object.keys(allPlayers);
        sendLog('info', '共 ' + keys.length + ' 个 Player 实例:', '');
        keys.forEach(function (k) {
            var isMy = allPlayers[k] ? '✅ [玩家]' : '❌ [Bot]';
            sendLog(allPlayers[k] ? 'success' : 'info', '  ' + k + ' ' + isMy, '');
        });
    };

    globalThis.refresh = function () {
        if (inst.player) {
            printAll(inst.player);
        } else {
            sendLog('warn', '刷新', '尚未捕获玩家地址');
        }
    };

    sendLog('success', '系统', '✅ 脚本已加载 (偏移已根据dump.cs修正)');
    sendLog('info', '系统', '进入游戏后自动打印实例地址');
    sendLog('info', '系统', '命令: listAll() - 列出所有Player实例');
    sendLog('info', '系统', '命令: refresh() - 刷新当前玩家信息');
    sendLog('info', '系统', '命令: getInstances() - 获取所有实例对象');
})();
