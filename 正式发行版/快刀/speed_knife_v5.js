// speed_knife_v5.js - 快刀功能（轻击+重击同时加速）
// 使用方法：frida -p <PID> -l speed_knife_v5.js
//
// 功能说明：
//   - 同时 Hook OnSpecialBtnDown、PlayKnifeAttackAnim、AnimSpeedSetting 三个函数
//   - 修改 combo1_AnimSpeed (0xEC) 控制轻击速度
//   - 修改 WeaponData_Knife->attackSpeed.z (data@0x68 -> 0xF0) 控制重击速度
//   - 每 16ms 定时器持续写入，防止被游戏逻辑覆盖
//   - 自动检测玩家武器（前两把武器）
//   - 完整的日志系统和安全防护
//
// 配置参数：
//   SPEED_MULTIPLIER  - 速度倍数，默认 3.0

(function() {
    var SPEED_MULTIPLIER = 3.0;
    var COMBO1_ANIM_SPEED_OFFSET = 0xEC;
    var WEAPON_DATA_OFFSET = 0x68;
    var ATTACK_SPEED_Z_OFFSET = 0xF0;

    console.log("[*] ════════════════════════════════════════════");
    console.log("[*]  SPEED KNIFE V5 - COMBO1 + BIGSHOT MODE   ");
    console.log("[*] ════════════════════════════════════════════");
    console.log("[*] Speed Multiplier: " + SPEED_MULTIPLIER);
    console.log("[*] Combo1 offset: 0x" + COMBO1_ANIM_SPEED_OFFSET.toString(16));
    console.log("[*] WeaponData offset: 0x" + WEAPON_DATA_OFFSET.toString(16));
    console.log("[*] AttackSpeed.z offset: 0x" + ATTACK_SPEED_Z_OFFSET.toString(16));
    console.log("[*] ════════════════════════════════════════════");

    var gameAssembly = Process.findModuleByName("GameAssembly.dll");
    if (!gameAssembly) {
        console.log("[-] GameAssembly.dll not found!");
        return;
    }

    var playerWeapons = {};
    var playerWeaponCount = 0;
    var MAX_PLAYER_WEAPONS = 2;

    var logCount = 0;
    var MAX_LOGS = 50;

    function isReadablePointer(p) {
        if (!p || p.isNull()) return false;
        try {
            return Process.findRangeByAddress(p) !== null;
        } catch (e) {
            return false;
        }
    }

    function isPlayerWeapon(weaponPtr) {
        if (!weaponPtr || weaponPtr.isNull()) return false;
        var key = weaponPtr.toString();
        if (playerWeapons[key]) return true;
        if (playerWeaponCount < MAX_PLAYER_WEAPONS) {
            playerWeapons[key] = true;
            playerWeaponCount++;
            console.log("[+] Player weapon #" + playerWeaponCount + " detected: " + weaponPtr);
            return true;
        }
        return false;
    }

    function setCombo1Speed(weaponPtr) {
        if (!weaponPtr || weaponPtr.isNull()) return false;
        try {
            var addr = weaponPtr.add(COMBO1_ANIM_SPEED_OFFSET);
            if (!isReadablePointer(addr)) return false;
            var oldValue = addr.readFloat();
            addr.writeFloat(SPEED_MULTIPLIER);
            return true;
        } catch (e) {
            return false;
        }
    }

    function setBigshotSpeed(weaponPtr) {
        if (!weaponPtr || weaponPtr.isNull()) return false;
        try {
            var dataPtrAddr = weaponPtr.add(WEAPON_DATA_OFFSET);
            if (!isReadablePointer(dataPtrAddr)) return false;
            var dataPtr = dataPtrAddr.readPointer();
            if (!dataPtr || dataPtr.isNull()) return false;

            var attackSpeedZAddr = dataPtr.add(ATTACK_SPEED_Z_OFFSET);
            if (!isReadablePointer(attackSpeedZAddr)) return false;
            var oldValue = attackSpeedZAddr.readFloat();
            attackSpeedZAddr.writeFloat(SPEED_MULTIPLIER);

            logCount++;
            if (logCount <= MAX_LOGS) {
                console.log("[+] [BIGSHOT] attackSpeed.z: " + oldValue.toFixed(2) + " -> " + SPEED_MULTIPLIER + " @ data=" + dataPtr);
            }
            return true;
        } catch (e) {
            return false;
        }
    }

    function setAllSpeeds(weaponPtr, source) {
        var combo1Ok = setCombo1Speed(weaponPtr);
        var bigshotOk = setBigshotSpeed(weaponPtr);

        if (combo1Ok && logCount <= MAX_LOGS) {
            logCount++;
            console.log("[+] [" + source + "] combo1_AnimSpeed -> " + SPEED_MULTIPLIER + " @ " + weaponPtr);
        }
    }

    function hookFunction(addr, name) {
        try {
            Interceptor.attach(addr, {
                onEnter: function(args) {
                    var thisPtr = args[0];
                    if (!isReadablePointer(thisPtr)) return;
                    if (!isPlayerWeapon(thisPtr)) return;
                    setAllSpeeds(thisPtr, name);
                }
            });
            console.log("[+] Hooked WPN_Knife::" + name + " @ " + addr);
        } catch (e) {
            console.log("[-] Failed to hook " + name + ": " + e);
        }
    }

    var onSpecialBtnDownAddr = gameAssembly.base.add(0xB64240);
    var playKnifeAttackAnimAddr = gameAssembly.base.add(0xB642B0);
    var animSpeedSettingAddr = gameAssembly.base.add(0xB63BD0);

    hookFunction(onSpecialBtnDownAddr, "OnSpecialBtnDown");
    hookFunction(playKnifeAttackAnimAddr, "PlayKnifeAttackAnim");
    hookFunction(animSpeedSettingAddr, "AnimSpeedSetting");

    setInterval(function() {
        var keys = Object.keys(playerWeapons);
        if (keys.length === 0) return;
        var count = 0;
        for (var i = 0; i < keys.length; i++) {
            var weaponPtr = ptr(keys[i]);
            setAllSpeeds(weaponPtr, "TIMER");
            count++;
        }
        if (count > 0 && logCount <= MAX_LOGS) {
            logCount++;
            console.log("[*] Timer refreshed " + count + " weapon(s)");
        }
    }, 16);

    setInterval(function() {
        var keys = Object.keys(playerWeapons);
        if (keys.length > 10) {
            playerWeapons = {};
            playerWeaponCount = 0;
            console.log("[*] Weapon cache cleared");
        }
    }, 10000);

    console.log("\n[+] ════════════════════════════════════════════");
    console.log("[+] ✅ SPEED KNIFE V5 SCRIPT LOADED");
    console.log("[+] Return to game and swing your knife!");
    console.log("[+] Both Combo1 and Bigshot speed will be modified!");
    console.log("[+] ════════════════════════════════════════════");
})();
