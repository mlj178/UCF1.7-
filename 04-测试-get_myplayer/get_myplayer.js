// get_myplayer.js - 获取玩家及相关实例地址 (完整版)
// 功能：自动打印所有玩家相关类的实例地址

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
    
    function readPointerSafe(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            return addr.readPointer();
        } catch (e) {
            return null;
        }
    }

    function readIntSafe(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            return addr.readS32();
        } catch (e) {
            return null;
        }
    }

    function readFloatSafe(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            return addr.readFloat();
        } catch (e) {
            return null;
        }
    }

    function readStringSafe(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            var strPtr = addr.readPointer();
            if (!strPtr || strPtr.isNull()) return null;
            var len = strPtr.add(-4).readS32();
            if (len < 0 || len > 100) return null;
            return strPtr.readUtf8String(len);
        } catch (e) {
            return null;
        }
    }

    function readU8Safe(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            return addr.readU8();
        } catch (e) {
            return null;
        }
    }

    var RVA_PLAYER_IS_MY = 0xB55FD0;

    var myPlayerAddress = null;
    var allPlayers = {};

    var instances = {};

    sendLog('info', '系统', '开始 Hook 相关函数...');

    try {
        var addrPlayerIsMy = base.add(RVA_PLAYER_IS_MY);
        var originalIsMy = new NativeFunction(addrPlayerIsMy, 'bool', ['pointer', 'pointer']);
        
        Interceptor.replace(addrPlayerIsMy, new NativeCallback(function (playerPtr, methodInfo) {
            try {
                var result = originalIsMy(playerPtr, methodInfo);
                
                if (playerPtr && !playerPtr.isNull()) {
                    allPlayers[playerPtr.toString()] = result;
                    
                    if (result && !myPlayerAddress) {
                        myPlayerAddress = playerPtr;
                        instances.player = playerPtr;
                        instances.entity = playerPtr;
                        setTimeout(function() {
                            printAllInstances(playerPtr);
                        }, 1000);
                    }
                }
                
                return result;
            } catch (e) {
                return false;
            }
        }, 'bool', ['pointer', 'pointer']));

        sendLog('success', 'Hook', 'Player$$get_isMyPlayer');
    } catch (e) {
        sendLog('error', 'Hook', 'Player$$get_isMyPlayer 失败: ' + e);
    }

    function printAllInstances(playerPtr) {
        sendLog('info', '', '');
        sendLog('success', '╔══════════════════════════════════════════════════════════════════════╗', '');
        sendLog('success', '║                         玩家实例地址汇总                              ║', '');
        sendLog('success', '╚══════════════════════════════════════════════════════════════════════╝', '');

        collectPlayerClass(playerPtr);
        collectEntityClass(playerPtr);
        collectPlayerWeaponsClass();
        collectClientDataClass();
        collectPlayerDataClass();
        collectWeaponClass();
        collectRecoilClass();
        collectPlayerCameraManagerClass();
        collectPlayerSkillsClass();
        collectNano4TDataClass();
        collectNanoRoleSelectClass();
        collectWeaponBagClass();
        collectPlayerInputClass();
        collectHealthDataClass();
        collectBuffClass();
        collectBotClass(playerPtr);
        collectWeaponDataClasses();

        printSummary();
    }

    function collectPlayerClass(playerPtr) {
        sendLog('info', '', '');
        sendLog('info', '┌────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【Player 类】 - 玩家核心类                                        │', '');
        sendLog('info', '├────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + playerPtr, '');

        var fields = [
            { offset: 0x10, type: 'PlayerCameraManager', key: 'cameraManager' },
            { offset: 0x18, type: 'Recoil', key: 'recoil' },
            { offset: 0x50, type: 'PropertyModifier', key: 'modifierMoveSpeed' },
            { offset: 0x58, type: 'PlayerVelocity', key: 'velData' },
            { offset: 0x60, type: 'NanoRoleSelect', key: 'nanoRoleSelect' },
            { offset: 0x68, type: 'Nano4T_Data', key: 'nano4TData' },
            { offset: 0x6C, type: 'PlayerSkills', key: 'playerSkills' },
            { offset: 0x70, type: 'WeaponBag', key: 'weaponBag' },
            { offset: 0x78, type: 'PlayerInput', key: 'playerInput' },
            { offset: 0x80, type: 'PlayerData', key: 'playerData' },
            { offset: 0x88, type: 'ClientData', key: 'clientData' },
            { offset: 0x90, type: 'PlayerWeapons', key: 'playerWeapons' },
            { offset: 0x98, type: 'WPN_Gun.AmmoData', key: 'mapGunAmmo1' },
            { offset: 0xA0, type: 'WPN_Gun.AmmoData', key: 'mapGunAmmo2' }
        ];

        fields.forEach(function(field) {
            var fieldPtr = readPointerSafe(playerPtr.add(field.offset));
            if (fieldPtr && !fieldPtr.isNull()) {
                instances[field.key] = fieldPtr;
                sendLog('info', '│  [0x' + padHex(field.offset) + '] ' + padRight(field.type, 24) + ' → ' + fieldPtr, '');
            }
        });

        sendLog('info', '│', '');
        sendLog('info', '│  【Player - Buff 相关字段】', '');
        var buffInfinityAmmo = readU8Safe(playerPtr.add(0xC8));
        if (buffInfinityAmmo !== null) {
            sendLog('info', '│  [0xC8] Buff_InfinityAmmo (bool) → ' + (buffInfinityAmmo ? 'true' : 'false'), '');
        }
        var buffJumpDisabled = readU8Safe(playerPtr.add(0xB8));
        if (buffJumpDisabled !== null) {
            sendLog('info', '│  [0xB8] Buff_JumpDisabled (bool) → ' + (buffJumpDisabled ? 'true' : 'false'), '');
        }
        var buffCameraRotDisabled = readU8Safe(playerPtr.add(0xB0));
        if (buffCameraRotDisabled !== null) {
            sendLog('info', '│  [0xB0] Buff_CameraRotDisabled (bool) → ' + (buffCameraRotDisabled ? 'true' : 'false'), '');
        }

        sendLog('info', '└────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectEntityClass(playerPtr) {
        sendLog('info', '', '');
        sendLog('info', '┌────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【Entity 类】 - 实体基类 (Player 继承此类)                        │', '');
        sendLog('info', '├────────────────────────────────────────────────────────────────────┤', '');
        sendLog('info', '│  实例地址: ' + playerPtr + ' (与 Player 相同)', '');

        var baseMoveSpeed = readFloatSafe(playerPtr.add(0x10));
        if (baseMoveSpeed !== null) {
            sendLog('info', '│  [0x10] baseMoveSpeed (float)    → ' + baseMoveSpeed, '');
        }

        var healthDataPtr = readPointerSafe(playerPtr.add(0x18));
        if (healthDataPtr && !healthDataPtr.isNull()) {
            instances.healthData = healthDataPtr;
            sendLog('info', '│  [0x18] HealthData              → ' + healthDataPtr, '');
        }

        var team = readIntSafe(playerPtr.add(0x20));
        if (team !== null) {
            sendLog('info', '│  [0x20] team (int)              → ' + team + ' (' + (team === 0 ? '黑名单' : '保卫者') + ')', '');
        }

        var isInvincible = readU8Safe(playerPtr.add(0x1C));
        if (isInvincible !== null) {
            sendLog('info', '│  [0x1C] isInvincible (bool)     → ' + (isInvincible ? 'true' : 'false'), '');
        }

        var buffsPtr = readPointerSafe(playerPtr.add(0x40));
        if (buffsPtr && !buffsPtr.isNull()) {
            instances.buffs = buffsPtr;
            sendLog('info', '│  [0x40] buffs (List<Buff>)      → ' + buffsPtr, '');
        }

        sendLog('info', '└────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectPlayerWeaponsClass() {
        if (!instances.playerWeapons) return;

        sendLog('info', '', '');
        sendLog('info', '┌────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【PlayerWeapons 类】 - 武器管理器                                 │', '');
        sendLog('info', '├────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + instances.playerWeapons, '');

        var fields = [
            { offset: 0x10, type: 'Player (owner)' },
            { offset: 0x18, type: 'List<Weapon> (all)' },
            { offset: 0x20, type: 'int (curSlot)' },
            { offset: 0x24, type: 'int (lastSlot)' },
            { offset: 0x28, type: 'Weapon (inUse/当前武器)', key: 'currentWeapon' },
            { offset: 0x30, type: 'Weapon[] (current)' },
            { offset: 0x38, type: 'Weapon[] (normal)' },
            { offset: 0x40, type: 'Weapon[] (special)' },
            { offset: 0x48, type: 'Weapon (temporaryWpn)' },
            { offset: 0x50, type: 'Weapon (F_KeyWpn)' },
            { offset: 0x58, type: 'Weapon (mapWpn)' },
            { offset: 0x68, type: 'PropertyModifier (ReloadSpeed)' },
            { offset: 0x70, type: 'PropertyModifier (KnifeRange)' },
            { offset: 0x78, type: 'PropertyModifier (KnifeSpeed)' }
        ];

        fields.forEach(function(field) {
            try {
                if (field.type.indexOf('int') >= 0) {
                    var val = readIntSafe(instances.playerWeapons.add(field.offset));
                    if (val !== null) {
                        sendLog('info', '│  [0x' + padHex(field.offset) + '] ' + padRight(field.type, 28) + ' → ' + val, '');
                    }
                } else {
                    var fieldPtr = readPointerSafe(instances.playerWeapons.add(field.offset));
                    if (fieldPtr && !fieldPtr.isNull()) {
                        if (field.key) {
                            instances[field.key] = fieldPtr;
                            sendLog('success', '│  [0x' + padHex(field.offset) + '] ' + padRight(field.type, 28) + ' → ' + fieldPtr, '');
                        } else {
                            sendLog('info', '│  [0x' + padHex(field.offset) + '] ' + padRight(field.type, 28) + ' → ' + fieldPtr, '');
                        }
                    }
                }
            } catch (e) {}
        });

        sendLog('info', '└────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectClientDataClass() {
        if (!instances.clientData) return;

        sendLog('info', '', '');
        sendLog('info', '┌────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【ClientData 类】 - 客户端数据                                    │', '');
        sendLog('info', '├────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + instances.clientData, '');

        var fields = [
            { offset: 0x10, name: 'defaultWpnBagID', type: 'int' },
            { offset: 0x18, name: 'nickName', type: 'string' },
            { offset: 0x20, name: 'level', type: 'int' },
            { offset: 0x24, name: 'joinTeam', type: 'int' },
            { offset: 0x28, name: 'isBot', type: 'bool' },
            { offset: 0x2C, name: 'vipLevel', type: 'int' },
            { offset: 0x30, name: 'character', type: 'int' }
        ];

        fields.forEach(function(field) {
            try {
                if (field.type === 'string') {
                    var val = readStringSafe(instances.clientData.add(field.offset));
                    if (val) {
                        sendLog('success', '│  [0x' + padHex(field.offset) + '] ' + padRight(field.name, 20) + ' (string) → ' + val, '');
                    }
                } else if (field.type === 'int') {
                    var val = readIntSafe(instances.clientData.add(field.offset));
                    if (val !== null) {
                        sendLog('info', '│  [0x' + padHex(field.offset) + '] ' + padRight(field.name, 20) + ' (int)   → ' + val, '');
                    }
                } else if (field.type === 'bool') {
                    var val = readU8Safe(instances.clientData.add(field.offset));
                    if (val !== null) {
                        sendLog('info', '│  [0x' + padHex(field.offset) + '] ' + padRight(field.name, 20) + ' (bool)  → ' + (val ? 'true' : 'false'), '');
                    }
                }
            } catch (e) {}
        });

        sendLog('info', '└────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectPlayerDataClass() {
        if (!instances.playerData) return;

        sendLog('info', '', '');
        sendLog('info', '┌────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【PlayerData 类】 - 玩家数据                                      │', '');
        sendLog('info', '├────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + instances.playerData, '');

        var fields = [
            { offset: 0x10, name: 'playerID', type: 'int' },
            { offset: 0x14, name: 'rank', type: 'int' },
            { offset: 0x18, name: 'spawnCount', type: 'int' },
            { offset: 0x40, name: 'kill', type: 'SubscribeableProperty<int>' },
            { offset: 0x48, name: 'death', type: 'SubscribeableProperty<int>' },
            { offset: 0x50, name: 'score', type: 'SubscribeableProperty<int>' },
            { offset: 0x58, name: 'aceSign', type: 'SubscribeableProperty<AceSign>' },
            { offset: 0x60, name: 'nanoRole', type: 'SubscribeableProperty<NanoRole>' },
            { offset: 0x80, name: 'revengeTarget', type: 'Player' }
        ];

        fields.forEach(function(field) {
            try {
                if (field.type === 'int') {
                    var val = readIntSafe(instances.playerData.add(field.offset));
                    if (val !== null) {
                        sendLog('info', '│  [0x' + padHex(field.offset) + '] ' + padRight(field.name, 16) + ' (' + padRight(field.type, 28) + ') → ' + val, '');
                    }
                } else {
                    var val = readPointerSafe(instances.playerData.add(field.offset));
                    if (val && !val.isNull()) {
                        sendLog('info', '│  [0x' + padHex(field.offset) + '] ' + padRight(field.name, 16) + ' (' + padRight(field.type, 28) + ') → ' + val, '');
                    }
                }
            } catch (e) {}
        });

        sendLog('info', '└────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectWeaponClass() {
        if (!instances.currentWeapon) return;

        sendLog('info', '', '');
        sendLog('info', '┌────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【Weapon / WPN_Gun 类】 - 当前武器                                │', '');
        sendLog('info', '├────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + instances.currentWeapon, '');

        var fields = [
            { offset: 0x10, name: 'owner', type: 'Player' },
            { offset: 0x18, name: 'data', type: 'WeaponData', key: 'weaponData' },
            { offset: 0x28, name: 'realData', type: 'WeaponData_Gun', key: 'weaponDataGun' },
            { offset: 0x30, name: 'ammoData', type: 'WPN_Gun.AmmoData', key: 'ammoData' },
            { offset: 0x38, name: 'ReloadCheck_Listener', type: 'Func<bool>' },
            { offset: 0x40, name: 'lastShootTime', type: 'float' },
            { offset: 0x44, name: 'recoilDataID', type: 'int' },
            { offset: 0x50, name: 'nextAllowedShootTime', type: 'float' }
        ];

        fields.forEach(function(field) {
            try {
                if (field.type === 'float') {
                    var val = readFloatSafe(instances.currentWeapon.add(field.offset));
                    if (val !== null) {
                        sendLog('info', '│  [0x' + padHex(field.offset) + '] ' + padRight(field.name, 24) + ' (float) → ' + val, '');
                    }
                } else if (field.type === 'int') {
                    var val = readIntSafe(instances.currentWeapon.add(field.offset));
                    if (val !== null) {
                        sendLog('info', '│  [0x' + padHex(field.offset) + '] ' + padRight(field.name, 24) + ' (int)   → ' + val, '');
                    }
                } else {
                    var val = readPointerSafe(instances.currentWeapon.add(field.offset));
                    if (val && !val.isNull()) {
                        if (field.key) instances[field.key] = val;
                        sendLog('info', '│  [0x' + padHex(field.offset) + '] ' + padRight(field.name, 24) + ' (' + field.type + ') → ' + val, '');
                    }
                }
            } catch (e) {}
        });

        if (instances.ammoData) {
            sendLog('info', '│', '');
            sendLog('info', '│  【WPN_Gun.AmmoData 子类】', '');
            var clipAmmo = readIntSafe(instances.ammoData.add(0x10));
            var totalAmmo = readIntSafe(instances.ammoData.add(0x14));
            if (clipAmmo !== null) {
                sendLog('info', '│        [0x10] clipAmmo (int)    → ' + clipAmmo, '');
            }
            if (totalAmmo !== null) {
                sendLog('info', '│        [0x14] totalAmmo (int)   → ' + totalAmmo, '');
            }
        }

        sendLog('info', '└────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectRecoilClass() {
        if (!instances.recoil) return;

        sendLog('info', '', '');
        sendLog('info', '┌────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【Recoil 类】 - 后坐力控制器                                      │', '');
        sendLog('info', '├────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + instances.recoil, '');

        var shootPosture = readIntSafe(instances.recoil.add(0x10));
        if (shootPosture !== null) {
            sendLog('info', '│  [0x10] shootPosture (int)      → ' + shootPosture, '');
        }

        var addYaw = readFloatSafe(instances.recoil.add(0x40));
        var addPitch = readFloatSafe(instances.recoil.add(0x44));
        if (addYaw !== null) {
            sendLog('info', '│  [0x40] addYaw (float)          → ' + addYaw, '');
        }
        if (addPitch !== null) {
            sendLog('info', '│  [0x44] addPitch (float)        → ' + addPitch, '');
        }

        var shoot = readU8Safe(instances.recoil.add(0xB0));
        if (shoot !== null) {
            sendLog('info', '│  [0xB0] shoot (bool)            → ' + (shoot ? 'true' : 'false'), '');
        }

        sendLog('info', '└────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectPlayerCameraManagerClass() {
        if (!instances.cameraManager) return;

        sendLog('info', '', '');
        sendLog('info', '┌────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【PlayerCameraManager 类】 - 相机管理器                          │', '');
        sendLog('info', '├────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + instances.cameraManager, '');

        var fields = [
            { offset: 0x10, name: 'mapCamera', type: 'CinemachineVirtualCamera' },
            { offset: 0x18, name: 'modelCamera', type: 'Camera' },
            { offset: 0x20, name: 'modelContainer', type: 'Transform' },
            { offset: 0x38, name: 'zoomFovScale', type: 'float' },
            { offset: 0x50, name: 'extraMapFov', type: 'float' },
            { offset: 0x54, name: 'extraPvFov', type: 'float' }
        ];

        fields.forEach(function(field) {
            try {
                if (field.type === 'float') {
                    var val = readFloatSafe(instances.cameraManager.add(field.offset));
                    if (val !== null) {
                        sendLog('info', '│  [0x' + padHex(field.offset) + '] ' + padRight(field.name, 20) + ' (float) → ' + val, '');
                    }
                } else {
                    var val = readPointerSafe(instances.cameraManager.add(field.offset));
                    if (val && !val.isNull()) {
                        sendLog('info', '│  [0x' + padHex(field.offset) + '] ' + padRight(field.name, 20) + ' (' + field.type + ') → ' + val, '');
                    }
                }
            } catch (e) {}
        });

        sendLog('info', '└────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectPlayerSkillsClass() {
        if (!instances.playerSkills) return;

        sendLog('info', '', '');
        sendLog('info', '┌────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【PlayerSkills 类】 - 技能管理器                                  │', '');
        sendLog('info', '├────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + instances.playerSkills, '');

        var allSkillsPtr = readPointerSafe(instances.playerSkills.add(0x10));
        if (allSkillsPtr && !allSkillsPtr.isNull()) {
            instances.allSkills = allSkillsPtr;
            sendLog('info', '│  [0x10] all (Skill[])           → ' + allSkillsPtr, '');
        }

        var ownerPtr = readPointerSafe(instances.playerSkills.add(0x18));
        if (ownerPtr && !ownerPtr.isNull()) {
            sendLog('info', '│  [0x18] owner (Player)          → ' + ownerPtr, '');
        }

        sendLog('info', '└────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectNano4TDataClass() {
        if (!instances.nano4TData) return;

        sendLog('info', '', '');
        sendLog('info', '┌────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【Nano4T_Data 类】 - 纳米4T数据                                   │', '');
        sendLog('info', '├────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + instances.nano4TData, '');

        var fields = [
            { offset: 0x10, name: 'humanLayer', type: 'SubscribeableProperty<int>' },
            { offset: 0x18, name: 'nanoLayer', type: 'SubscribeableProperty<int>' },
            { offset: 0x20, name: 'pickUpBoxCount', type: 'SubscribeableProperty<int>' }
        ];

        fields.forEach(function(field) {
            var val = readPointerSafe(instances.nano4TData.add(field.offset));
            if (val && !val.isNull()) {
                sendLog('info', '│  [0x' + padHex(field.offset) + '] ' + padRight(field.name, 20) + ' → ' + val, '');
            }
        });

        sendLog('info', '└────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectNanoRoleSelectClass() {
        if (!instances.nanoRoleSelect) return;

        sendLog('info', '', '');
        sendLog('info', '┌────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【NanoRoleSelect 类】 - 纳米角色选择器                            │', '');
        sendLog('info', '├────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + instances.nanoRoleSelect, '');

        var ownerPtr = readPointerSafe(instances.nanoRoleSelect.add(0x10));
        if (ownerPtr && !ownerPtr.isNull()) {
            sendLog('info', '│  [0x10] owner (Player)          → ' + ownerPtr, '');
        }

        var tableType = readIntSafe(instances.nanoRoleSelect.add(0x18));
        if (tableType !== null) {
            sendLog('info', '│  [0x18] tableType (int)         → ' + tableType, '');
        }

        sendLog('info', '└────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectWeaponBagClass() {
        if (!instances.weaponBag) return;

        sendLog('info', '', '');
        sendLog('info', '┌────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【WeaponBag 类】 - 武器背包                                       │', '');
        sendLog('info', '├────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + instances.weaponBag, '');

        var fields = [
            { offset: 0x10, name: 'wpnBags', type: 'int[][]' },
            { offset: 0x18, name: 'wpnData', type: 'WeaponData[]' }
        ];

        fields.forEach(function(field) {
            var val = readPointerSafe(instances.weaponBag.add(field.offset));
            if (val && !val.isNull()) {
                sendLog('info', '│  [0x' + padHex(field.offset) + '] ' + padRight(field.name, 16) + ' (' + field.type + ') → ' + val, '');
            }
        });

        sendLog('info', '└────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectPlayerInputClass() {
        if (!instances.playerInput) return;

        sendLog('info', '', '');
        sendLog('info', '┌────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【PlayerInput 类】 - 输入控制器                                   │', '');
        sendLog('info', '├────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + instances.playerInput, '');

        var rightMouse = readIntSafe(instances.playerInput.add(0x10));
        if (rightMouse !== null) {
            sendLog('info', '│  [0x10] RightMouse (int)        → ' + rightMouse, '');
        }

        var jumpButton = readIntSafe(instances.playerInput.add(0x14));
        if (jumpButton !== null) {
            sendLog('info', '│  [0x14] JumpButton (int)        → ' + jumpButton, '');
        }

        sendLog('info', '└────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectHealthDataClass() {
        if (!instances.healthData) return;

        sendLog('info', '', '');
        sendLog('info', '┌────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【HealthData 类】 - 生命值数据                                    │', '');
        sendLog('info', '├────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + instances.healthData, '');

        sendLog('info', '│  [0x10] currentHealth (ObscuredInt)', '');
        sendLog('info', '│  [0x18] maxHealth (ObscuredInt)', '');
        sendLog('info', '│  [0x20] tempHealth (ObscuredInt)', '');

        var invinsibleEndTime = readFloatSafe(instances.healthData.add(0x28));
        if (invinsibleEndTime !== null) {
            sendLog('info', '│  [0x28] invinsibleEndTime (float) → ' + invinsibleEndTime, '');
        }

        sendLog('info', '└────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectBuffClass() {
        if (!instances.buffs) return;

        sendLog('info', '', '');
        sendLog('info', '┌────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【Buff 类】 - Buff列表                                            │', '');
        sendLog('info', '├────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + instances.buffs, '');

        try {
            var count = readIntSafe(instances.buffs.add(0x18));
            if (count !== null) {
                sendLog('info', '│  Buff 数量: ' + count, '');
            }
        } catch (e) {}

        sendLog('info', '└────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectBotClass(playerPtr) {
        sendLog('info', '', '');
        sendLog('info', '┌────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【Bot 类】 - Bot控制器 (如果是Bot)                                │', '');
        sendLog('info', '├────────────────────────────────────────────────────────────────────┤', '');

        try {
            var botPtr = readPointerSafe(playerPtr.add(0xF8));
            if (botPtr && !botPtr.isNull()) {
                instances.bot = botPtr;
                sendLog('success', '│  实例地址: ' + botPtr, '');

                var abilityPtr = readPointerSafe(botPtr.add(0x10));
                if (abilityPtr && !abilityPtr.isNull()) {
                    instances.botAbility = abilityPtr;
                    sendLog('info', '│  [0x10] ability (BotAbility)    → ' + abilityPtr, '');
                }

                var thisPlayerPtr = readPointerSafe(botPtr.add(0x28));
                if (thisPlayerPtr && !thisPlayerPtr.isNull()) {
                    sendLog('info', '│  [0x28] thisPlayer (Player)     → ' + thisPlayerPtr, '');
                }
            } else {
                sendLog('info', '│  (当前玩家不是Bot，无Bot实例)', '');
            }
        } catch (e) {
            sendLog('info', '│  (当前玩家不是Bot，无Bot实例)', '');
        }

        sendLog('info', '└────────────────────────────────────────────────────────────────────┘', '');
    }

    function collectWeaponDataClasses() {
        if (!instances.weaponDataGun) return;

        sendLog('info', '', '');
        sendLog('info', '┌────────────────────────────────────────────────────────────────────┐', '');
        sendLog('info', '│  【WeaponData_Gun 类】 - 枪械数据                                  │', '');
        sendLog('info', '├────────────────────────────────────────────────────────────────────┤', '');
        sendLog('success', '│  实例地址: ' + instances.weaponDataGun, '');

        var fields = [
            { offset: 0x18, name: 'clip', type: 'int' },
            { offset: 0x1C, name: 'ammo', type: 'int' },
            { offset: 0x20, name: 'clip_Nano', type: 'int' },
            { offset: 0x24, name: 'ammo_Nano', type: 'int' },
            { offset: 0x2C, name: 'shotsPerMinute', type: 'float' },
            { offset: 0x30, name: 'fireAnimMultiplier', type: 'float' },
            { offset: 0x34, name: 'reloadAnimRatio', type: 'float' },
            { offset: 0x80, name: 'range', type: 'float' },
            { offset: 0x84, name: 'ammoDamage', type: 'float' },
            { offset: 0xB8, name: 'zoomAction', type: 'ZoomAction', key: 'zoomAction' }
        ];

        fields.forEach(function(field) {
            try {
                if (field.type === 'int') {
                    var val = readIntSafe(instances.weaponDataGun.add(field.offset));
                    if (val !== null) {
                        sendLog('info', '│  [0x' + padHex(field.offset) + '] ' + padRight(field.name, 20) + ' (int)   → ' + val, '');
                    }
                } else if (field.type === 'float') {
                    var val = readFloatSafe(instances.weaponDataGun.add(field.offset));
                    if (val !== null) {
                        sendLog('info', '│  [0x' + padHex(field.offset) + '] ' + padRight(field.name, 20) + ' (float) → ' + val, '');
                    }
                } else {
                    var val = readPointerSafe(instances.weaponDataGun.add(field.offset));
                    if (val && !val.isNull()) {
                        if (field.key) instances[field.key] = val;
                        sendLog('info', '│  [0x' + padHex(field.offset) + '] ' + padRight(field.name, 20) + ' (' + field.type + ') → ' + val, '');
                    }
                }
            } catch (e) {}
        });

        sendLog('info', '└────────────────────────────────────────────────────────────────────┘', '');
    }

    function printSummary() {
        sendLog('info', '', '');
        sendLog('success', '╔══════════════════════════════════════════════════════════════════════╗', '');
        sendLog('success', '║                         实例地址汇总表                               ║', '');
        sendLog('success', '╠══════════════════════════════════════════════════════════════════════╣', '');

        var summary = [
            { name: 'Player', key: 'player', desc: '玩家实例' },
            { name: 'Entity', key: 'entity', desc: '实体基类' },
            { name: 'ClientData', key: 'clientData', desc: '客户端数据' },
            { name: 'PlayerData', key: 'playerData', desc: '玩家数据' },
            { name: 'PlayerInput', key: 'playerInput', desc: '输入控制' },
            { name: 'PlayerWeapons', key: 'playerWeapons', desc: '武器管理器' },
            { name: 'WeaponBag', key: 'weaponBag', desc: '武器背包' },
            { name: 'PlayerSkills', key: 'playerSkills', desc: '技能管理' },
            { name: 'NanoRoleSelect', key: 'nanoRoleSelect', desc: '纳米角色选择' },
            { name: 'Nano4T_Data', key: 'nano4TData', desc: '纳米4T数据' },
            { name: 'PlayerCameraManager', key: 'cameraManager', desc: '相机管理' },
            { name: 'Recoil', key: 'recoil', desc: '后坐力' },
            { name: 'HealthData', key: 'healthData', desc: '生命值数据' },
            { name: 'Buff列表', key: 'buffs', desc: 'Buff列表' },
            { name: '当前武器', key: 'currentWeapon', desc: 'Weapon/WPN_Gun' },
            { name: 'AmmoData', key: 'ammoData', desc: '弹药数据' },
            { name: 'WeaponData', key: 'weaponData', desc: '武器数据' },
            { name: 'WeaponData_Gun', key: 'weaponDataGun', desc: '枪械数据' },
            { name: 'Bot', key: 'bot', desc: 'Bot控制器' },
            { name: 'BotAbility', key: 'botAbility', desc: 'Bot能力' }
        ];

        summary.forEach(function(item) {
            var addr = instances[item.key];
            if (addr) {
                sendLog('info', '║  ' + padRight(item.name, 20) + ' │ ' + padRight(item.desc, 12) + ' │ ' + addr, '');
            }
        });

        sendLog('success', '╚══════════════════════════════════════════════════════════════════════╝', '');
    }

    function padHex(num) {
        return num.toString(16).toUpperCase().padStart(2, '0');
    }

    function padRight(str, len) {
        if (!str) str = '';
        return str.toString().padEnd(len, ' ');
    }

    function listAllPlayers() {
        sendLog('info', '', '');
        sendLog('info', '══════════════════════════════════════════════════════════════', '');
        sendLog('info', '                    所有 Player 实例列表                       ', '');
        sendLog('info', '══════════════════════════════════════════════════════════════', '');
        
        var playerKeys = Object.keys(allPlayers);
        sendLog('info', '共 ' + playerKeys.length + ' 个 Player 实例:', '');
        
        playerKeys.forEach(function(key) {
            var isMy = allPlayers[key] ? '✅ [玩家]' : '❌ [Bot]';
            sendLog(allPlayers[key] ? 'success' : 'info', '  ' + key + ' ' + isMy, '');
        });
    }

    globalThis.getPlayer = function () { return instances.player; };
    globalThis.getClientData = function () { return instances.clientData; };
    globalThis.getPlayerData = function () { return instances.playerData; };
    globalThis.getPlayerWeapons = function () { return instances.playerWeapons; };
    globalThis.getCurrentWeapon = function () { return instances.currentWeapon; };
    globalThis.getAmmoData = function () { return instances.ammoData; };
    globalThis.getRecoil = function () { return instances.recoil; };
    globalThis.getCameraManager = function () { return instances.cameraManager; };
    globalThis.getHealthData = function () { return instances.healthData; };
    globalThis.getPlayerSkills = function () { return instances.playerSkills; };
    globalThis.getWeaponData = function () { return instances.weaponDataGun; };
    globalThis.getBot = function () { return instances.bot; };
    globalThis.getBotAbility = function () { return instances.botAbility; };

    globalThis.listAll = listAllPlayers;

    globalThis.refresh = function () {
        if (instances.player) {
            printAllInstances(instances.player);
        } else {
            sendLog('warn', '刷新', '尚未捕获玩家地址');
        }
    };

    globalThis.getInstances = function () {
        return instances;
    };

    sendLog('success', '系统', '✅ 脚本已加载');
    sendLog('info', '系统', '进入游戏后自动打印实例地址');
    sendLog('info', '系统', '命令: listAll() - 列出所有 Player 实例');
    sendLog('info', '系统', '命令: refresh() - 刷新当前玩家信息');
    sendLog('info', '系统', '命令: getInstances() - 获取所有实例对象');
})();
