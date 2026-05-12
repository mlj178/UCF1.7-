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

    var base = gameAssembly.base;
    sendLog('info', '系统', 'GameAssembly.dll base=' + base);

    function readPtr(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            var v = addr.readPointer();
            return (v && !v.isNull()) ? v : null;
        } catch (e) { return null; }
    }

    function readI32(addr) {
        try { return addr ? addr.readS32() : null; } catch (e) { return null; }
    }

    function readF32(addr) {
        try { return addr ? addr.readFloat() : null; } catch (e) { return null; }
    }

    function readU8(addr) {
        try { return addr ? addr.readU8() : null; } catch (e) { return null; }
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

    // 只 hook isMyPlayer 来捕获本地玩家指针
    var myPlayerPtr = null;
    var inst = {};

    try {
        var addrIsMy = base.add(0xB55FD0);
        var origIsMy = new NativeFunction(addrIsMy, 'bool', ['pointer', 'pointer']);

        Interceptor.replace(addrIsMy, new NativeCallback(function (playerPtr, methodInfo) {
            try {
                var result = origIsMy(playerPtr, methodInfo);
                if (result && !myPlayerPtr) {
                    myPlayerPtr = playerPtr;
                    inst.player = playerPtr;
                    setTimeout(function () { printPlayerInfo(playerPtr); }, 2000);
                }
                return result;
            } catch (e) { return false; }
        }, 'bool', ['pointer', 'pointer']));

        sendLog('success', 'Hook', 'Player$$get_isMyPlayer OK');
    } catch (e) {
        sendLog('error', 'Hook', 'Player$$get_isMyPlayer 失败: ' + e);
    }

    // ======================== 打印本地玩家信息 ========================
    function printPlayerInfo(pp) {
        sendLog('info', '', '========== 游戏修改器 v1.3 —— 玩家实例诊断 ==========');

        // --- 1. 验证：确认是本地玩家，不是 Bot ---
        var cd = readPtr(pp.add(0x94));
        if (cd) { inst.clientData = cd; }
        var isBot = cd ? readU8(cd.add(0x1C)) : null;

        sendLog('info', '诊断', '玩家实例: ' + pp);
        sendLog('info', '诊断', 'ClientData: ' + cd + (isBot !== null ? (isBot ? ' [是Bot]' : ' [本地玩家]') : ''));

        var nick = cd ? readStr(cd.add(0x10)) : null;
        if (nick) sendLog('info', '诊断', '昵称: ' + nick);

        // --- 2. 收集各子实例地址 ---
        // Player 字段 (dump.cs TypeDefIndex: 5171)
        inst.cameraManager = readPtr(pp.add(0x48));
        inst.recoil = readPtr(pp.add(0x54));
        inst.velData = readPtr(pp.add(0x90));
        inst.playerData = readPtr(pp.add(0x98));
        inst.playerInput = readPtr(pp.add(0x9C));
        inst.playerWeapons = readPtr(pp.add(0xA0));
        inst.weaponBag = readPtr(pp.add(0xA4));
        inst.nanoRoleSelect = readPtr(pp.add(0xA8));
        inst.nano4TData = readPtr(pp.add(0xAC));
        inst.playerSkills = readPtr(pp.add(0xB0));

        // Entity 基类字段 (dump.cs TypeDefIndex: 5161)
        inst.healthData = readPtr(pp.add(0x1C));
        inst.buffs = readPtr(pp.add(0x34));

        // 修改器核心: 速度修正器
        inst.modifierMoveSpeed = readPtr(pp.add(0x8C));

        sendLog('info', '', '--- 子实例地址 ---');
        sendLog('info', '实例', 'PlayerCameraManager   [Player+0x48]: ' + (inst.cameraManager || 'null'));
        sendLog('info', '实例', 'Recoil                [Player+0x54]: ' + (inst.recoil || 'null'));
        sendLog('info', '实例', 'Modifier_MoveSpeedRatio[Player+0x8C]: ' + (inst.modifierMoveSpeed || 'null'));
        sendLog('info', '实例', 'ClientData            [Player+0x94]: ' + (inst.clientData || 'null'));
        sendLog('info', '实例', 'PlayerData            [Player+0x98]: ' + (inst.playerData || 'null'));
        sendLog('info', '实例', 'PlayerInput           [Player+0x9C]: ' + (inst.playerInput || 'null'));
        sendLog('info', '实例', 'PlayerWeapons         [Player+0xA0]: ' + (inst.playerWeapons || 'null'));
        sendLog('info', '实例', 'WeaponBag             [Player+0xA4]: ' + (inst.weaponBag || 'null'));
        sendLog('info', '实例', 'NanoRoleSelect        [Player+0xA8]: ' + (inst.nanoRoleSelect || 'null'));
        sendLog('info', '实例', 'Nano4T_Data           [Player+0xAC]: ' + (inst.nano4TData || 'null'));
        sendLog('info', '实例', 'PlayerSkills          [Player+0xB0]: ' + (inst.playerSkills || 'null'));
        sendLog('info', '实例', 'HealthData            [Entity+0x1C]: ' + (inst.healthData || 'null'));
        sendLog('info', '实例', 'Buff列表              [Entity+0x34]: ' + (inst.buffs || 'null'));
        sendLog('info', '实例', 'PlayerVelocity        [Player+0x90]: ' + (inst.velData || 'null'));

        // --- 3. ClientData 详情 ---
        if (cd) {
            sendLog('info', '', '--- ClientData 详情 (TDI:5120) ---');
            sendLog('info', 'CD', 'defaultWpnBagID [+0x08]: ' + readI32(cd.add(0x8)));
            sendLog('info', 'CD', 'nickName      [+0x10]: ' + (readStr(cd.add(0x10)) || ''));
            sendLog('info', 'CD', 'level         [+0x14]: ' + readI32(cd.add(0x14)));
            sendLog('info', 'CD', 'joinTeam      [+0x18]: ' + readI32(cd.add(0x18)));
            sendLog('info', 'CD', 'isBot         [+0x1C]: ' + (readU8(cd.add(0x1C)) ? 'true' : 'false'));
            sendLog('info', 'CD', 'vipLevel      [+0x20]: ' + readI32(cd.add(0x20)));
            sendLog('info', 'CD', 'character     [+0x24]: ' + readI32(cd.add(0x24)));
        }

        // --- 4. PlayerData 详情 ---
        var pd = inst.playerData;
        if (pd) {
            sendLog('info', '', '--- PlayerData 详情 (TDI:5146) ---');
            sendLog('info', 'PD', 'playerID          [+0x14]: ' + readI32(pd.add(0x14)));
            sendLog('info', 'PD', 'orignalCharName   [+0x18]: ' + (readStr(pd.add(0x18)) || ''));
            sendLog('info', 'PD', 'rank              [+0x1C]: ' + readI32(pd.add(0x1C)));
            sendLog('info', 'PD', 'spawnCount        [+0x20]: ' + readI32(pd.add(0x20)));
            sendLog('info', 'PD', 'kill              [+0x4C]: ' + (readPtr(pd.add(0x4C)) || 'null'));
            sendLog('info', 'PD', 'death             [+0x50]: ' + (readPtr(pd.add(0x50)) || 'null'));
            sendLog('info', 'PD', 'score             [+0x58]: ' + (readPtr(pd.add(0x58)) || 'null'));
        }

        // --- 5. PlayerWeapons 详情 (修改器核心) ---
        var pw = inst.playerWeapons;
        if (pw) {
            sendLog('info', '', '--- PlayerWeapons 详情 (TDI:5156) ---');
            var owner = readPtr(pw.add(0x8));
            sendLog('info', 'PW', 'owner (Player)        [+0x08]: ' + (owner || 'null'));
            sendLog('info', 'PW', 'curSlot               [+0x10]: ' + readI32(pw.add(0x10)));
            sendLog('info', 'PW', 'lastSlot              [+0x14]: ' + readI32(pw.add(0x14)));
            inst.currentWeapon = readPtr(pw.add(0x18));
            sendLog('info', 'PW', 'inUse (当前武器)       [+0x18]: ' + (inst.currentWeapon || 'null'));
            sendLog('info', 'PW', 'Modifier_ReloadSpeed  [+0x3C]: ' + (readPtr(pw.add(0x3C)) || 'null'));
            sendLog('info', 'PW', 'Modifier_KnifeRange   [+0x40]: ' + (readPtr(pw.add(0x40)) || 'null'));
            sendLog('info', 'PW', 'Modifier_KnifeSpeed   [+0x44]: ' + (readPtr(pw.add(0x44)) || 'null'));

            // 方法 RVA (用于 Hook)
            sendLog('info', 'PW', 'get_KnifeSpeed    (RVA 0xB170A0): ' + base.add(0xB170A0));
            sendLog('info', 'PW', 'get_ReloadSpeed   (RVA 0xB170E0): ' + base.add(0xB170E0));
            sendLog('info', 'PW', 'get_isInfinityAmmo(RVA 0xB17120): ' + base.add(0xB17120));
        }

        // --- 6. Recoul 详情 (修改器核心) ---
        var rc = inst.recoil;
        if (rc) {
            sendLog('info', '', '--- Recoil 详情 (TDI:5559) ---');
            sendLog('info', 'Rec', 'addYaw        [+0x68]: ' + readF32(rc.add(0x68)));
            sendLog('info', 'Rec', 'addPitch      [+0x6C]: ' + readF32(rc.add(0x6C)));
            sendLog('info', 'Rec', 'addYaw_Target [+0x70]: ' + readF32(rc.add(0x70)));
            sendLog('info', 'Rec', 'addPitch_Target[+0x74]: ' + readF32(rc.add(0x74)));
            sendLog('info', 'Rec', 'OnGunShot     (RVA 0xB19980): ' + base.add(0xB19980));
        }

        // --- 7. 当前武器详情 ---
        var wp = inst.currentWeapon;
        if (wp) {
            sendLog('info', '', '--- 当前武器 (Weapon) 详情 ---');
            var wpnData = readPtr(wp.add(0x68));
            sendLog('info', 'Wpn', 'data (WeaponData)     [+0x68]: ' + (wpnData || 'null'));

            // 检查是 WPN_Gun 还是 WPN_Knife
            var isGun = readPtr(wp.add(0xF4)); // WPN_Gun.ammoData
            var isKnife = readU8(wp.add(0x78)) !== undefined; // 通用检测

            if (isGun) {
                sendLog('info', 'Wpn', '[WPN_Gun] ammoData      [+0xF4]: ' + isGun);
                sendLog('info', 'Wpn', '[WPN_Gun] recoilDataID   [+0x100]: ' + readI32(wp.add(0x100)));
                sendLog('info', 'Wpn', '[WPN_Gun] ConsumeAmmo(RVA 0xB61140): ' + base.add(0xB61140));
                sendLog('info', 'Wpn', 'Weapon.ConsumeAmmo    (RVA 0xB6C310): ' + base.add(0xB6C310));

                var wdg = readPtr(wp.add(0xEC));
                if (wdg) {
                    sendLog('info', 'Wpn', '  realData (WeaponData_Gun) [+0xEC]: ' + wdg);
                }
            } else {
                sendLog('info', 'Wpn', '[WPN_Knife] GetKnifeAttackData(RVA 0xB63EC0): ' + base.add(0xB63EC0));
            }
        }

        // --- 8. HealthData 详情 ---
        var hd = inst.healthData;
        if (hd) {
            sendLog('info', '', '--- HealthData 详情 (TDI:5140) ---');
            sendLog('info', 'HP', 'currentHealth [+0x08]: ' + readI32(hd.add(0x8))); // ObscuredInt 简化
            sendLog('info', 'HP', 'maxHealth     [+0x1C]: ' + readI32(hd.add(0x1C)));
            sendLog('info', 'HP', 'tempHealth    [+0x30]: ' + readI32(hd.add(0x30)));
            sendLog('info', 'HP', 'invinsibleEnd [+0x44]: ' + readF32(hd.add(0x44)));
        }

        // --- 9. Entity 关键字段 ---
        sendLog('info', '', '--- Entity 基类字段 (TDI:5161) ---');
        sendLog('info', 'Ent', 'baseMoveSpeed [+0x0C]: ' + readF32(pp.add(0xC)));
        sendLog('info', 'Ent', 'speedPenalty  [+0x10]: ' + readF32(pp.add(0x10)));
        sendLog('info', 'Ent', 'damageRate    [+0x14]: ' + readF32(pp.add(0x14)));
        sendLog('info', 'Ent', 'isInvincible  [+0x18]: ' + (readU8(pp.add(0x18)) ? 'true' : 'false'));
        sendLog('info', 'Ent', 'team          [+0x20]: ' + readI32(pp.add(0x20)));
        sendLog('info', 'Ent', 'isGhostEntity [+0x30]: ' + (readU8(pp.add(0x30)) ? 'true' : 'false'));

        // --- 10. Modifier 系统 (PropertyModifier) ---
        sendLog('info', '', '--- PropertyModifier 系统 ---');
        sendLog('info', 'Mod', 'PropertyModifier.Get  (RVA 0xB17590): ' + base.add(0xB17590));
        sendLog('info', 'Mod', 'Player.get_MoveSpeedRatio 路径: Player[+0x8C]->PropertyModifier.Get(Player)');

        // --- 11. ModeBase / 时间系统 ---
        sendLog('info', '', '--- ModeBase 时间系统 ---');
        sendLog('info', 'Time', 'ModeBase.restGameTime minute [+0x34]');
        sendLog('info', 'Time', 'ModeBase.restGameTime second [+0x38]');
        sendLog('info', 'Time', 'UpdateTimeUI (RVA 0xAF6930)');
        sendLog('info', 'Time', 'GameRoundEnd  (RVA 0xAFAA40)');
        sendLog('info', 'Time', 'OnTimeOut     (RVA 0xAF1920)');

        printSingletons();
        printSummary();

        sendLog('info', '', '========== 诊断完成 ==========');
    }

    // ======================== 全局/单例信息 ========================
    function printSingletons() {
        sendLog('info', '', '--- 全局单例 ---');

        // 尝试通过 il2cpp API 获取单例
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
            var il2cpp_class_get_static_field_data = new NativeFunction(
                Module.findExportByName('GameAssembly.dll', 'il2cpp_class_get_static_field_data'),
                'pointer', ['pointer']
            );

            var singletonGetter = new NativeFunction(base.add(0x4A8170), 'pointer', ['pointer']);
            var domain = il2cpp_domain_get();
            var sizePtr = Memory.alloc(4);
            var assemblies = il2cpp_domain_get_assemblies(domain, sizePtr);

            function findClass(name) {
                var asmCount = sizePtr.readU32();
                for (var ai = 0; ai < asmCount; ai++) {
                    var asmPtr = assemblies.add(Process.pointerSize * ai).readPointer();
                    var image = il2cpp_assembly_get_image(asmPtr);
                    if (image.isNull()) continue;
                    var ns = Memory.allocUtf8String('');
                    var nm = Memory.allocUtf8String(name);
                    var cls = il2cpp_class_from_name(image, ns, nm);
                    if (!cls.isNull()) return cls;
                }
                return null;
            }

            // GameManager 单例 (RVA 0xE1CE64)
            try {
                var methodInfo = base.add(0xE1CE64).readPointer();
                var gm = singletonGetter(methodInfo);
                if (gm && !gm.isNull()) {
                    sendLog('info', 'Singleton', 'GameManager: ' + gm);
                    var ap = readPtr(gm.add(0x1C));
                    if (ap) {
                        var total = readI32(ap.add(0x18)) || 0;
                        sendLog('info', 'Singleton', '  allPlayers[+0x1C]: ' + ap + ' (count=' + total + ')');
                    }
                }
            } catch (e) { sendLog('info', 'Singleton', 'GameManager: 获取失败'); }

            // GameManager 静态类
            var gmClass = findClass('GameManager');
            if (gmClass) {
                var staticData = il2cpp_class_get_static_field_data(gmClass);
                if (!staticData.isNull()) {
                    sendLog('info', 'Singleton', 'GameManager 静态字段 @ ' + staticData);
                }
            }

        } catch (e) {
            sendLog('info', 'Singleton', 'il2cpp API失败: ' + e.message);
        }
    }

    // ======================== 汇总 ========================
    function printSummary() {
        sendLog('info', '', '--- 实例汇总 ---');
        var rows = [
            ['Player', inst.player],
            ['Entity(=Player)', inst.player],
            ['ClientData', inst.clientData],
            ['PlayerData', inst.playerData],
            ['PlayerInput', inst.playerInput],
            ['PlayerWeapons', inst.playerWeapons],
            ['Weapon(当前)', inst.currentWeapon],
            ['Recoil', inst.recoil],
            ['HealthData', inst.healthData],
            ['PlayerCameraManager', inst.cameraManager],
            ['PlayerSkills', inst.playerSkills],
            ['NanoRoleSelect', inst.nanoRoleSelect],
            ['Nano4T_Data', inst.nano4TData],
            ['Modifier_MoveSpeed', inst.modifierMoveSpeed],
            ['PlayerVelocity', inst.velData]
        ];

        for (var i = 0; i < rows.length; i++) {
            var name = rows[i][0];
            var addr = rows[i][1];
            sendLog('info', '汇总', (name + '                 ').substring(0, 22) + ' ' + (addr || 'null'));
        }
    }

    // 导出全局函数
    globalThis.getPlayer = function () { return inst.player; };
    globalThis.getInstances = function () { return inst; };
    globalThis.refresh = function () {
        if (inst.player) printPlayerInfo(inst.player);
        else sendLog('warn', '刷新', '尚无玩家实例');
    };

    sendLog('info', '系统', '✅ 修改器v1.3诊断脚本已加载');
    sendLog('info', '系统', '进入游戏后自动打印本地玩家信息');
    sendLog('info', '系统', '命令: refresh() 重新打印');
    sendLog('info', '系统', '命令: getInstances() 获取实例对象');
})();
