// speed_knife_v11.js - 全背包全模式快刀（轻击两段+重击加速）
// 用法：frida -p <PID> -l speed_knife_v11.js

(function() {
    var SPEED = 5.0;
    var COMBO1_OFFSET = 0xEC;         // 武器实例 combo1_AnimSpeed
    var DATA_FIELD_OFFSET = 0x68;     // Weapon.data
    var ATTACK_SPEED_OFFSET = 0xE8;   // WeaponData.attackSpeed 起始
    var ATTACK_SPEED_X = 0xE8;        // attackSpeed.x
    var ATTACK_SPEED_Y = 0xEC;        // attackSpeed.y (轻击第二段)
    var ATTACK_SPEED_Z = 0xF0;        // attackSpeed.z (重击)

    console.log("[*] SPEED KNIFE V11 (Full Combo: Light1, Light2, Heavy)");

    var mod = Process.findModuleByName("GameAssembly.dll");
    if (!mod) return;

    var base = mod.base;

    // Weapon.get_isMyWeapon (RVA 0xB6E1D0)
    var isMyWeapon = new NativeFunction(base.add(0xB6E1D0), "bool", ["pointer", "pointer"]);

    var logN = 0, MAX_LOG = 5;
    function maybeLog(s) { if (logN++ < MAX_LOG) console.log(s); }

    function isReadable(p) {
        return p && !p.isNull() && Process.findRangeByAddress(p) !== null;
    }

    function isValidSpeed(val) {
        return val > 0.1 && val < 15.0 && val !== SPEED;
    }

    // 写入 combo1_AnimSpeed (武器实例)
    function setCombo1Speed(weaponPtr, source) {
        try {
            var addr = weaponPtr.add(COMBO1_OFFSET);
            if (!isReadable(addr)) return;
            var cur = addr.readFloat();
            if (cur === SPEED) return;
            addr.writeFloat(SPEED);
            maybeLog("[+] [" + source + "] combo1: " + cur.toFixed(2) + " -> " + SPEED);
        } catch(e) {}
    }

    // 写入 data->attackSpeed 的 y 和 z 分量
    function setAttackSegmentSpeeds(weaponPtr) {
        try {
            var dataPtrAddr = weaponPtr.add(DATA_FIELD_OFFSET);
            if (!isReadable(dataPtrAddr)) return;
            var dataPtr = dataPtrAddr.readPointer();
            if (!isReadable(dataPtr)) return;

            // 写入 attackSpeed.y (Combo2 轻击第二段)
            var yAddr = dataPtr.add(ATTACK_SPEED_Y);
            if (isReadable(yAddr)) {
                var y = yAddr.readFloat();
                if (isValidSpeed(y)) {
                    yAddr.writeFloat(SPEED);
                }
            }

            // 写入 attackSpeed.z (重击)
            var zAddr = dataPtr.add(ATTACK_SPEED_Z);
            if (isReadable(zAddr)) {
                var z = zAddr.readFloat();
                if (isValidSpeed(z)) {
                    zAddr.writeFloat(SPEED);
                }
            }

            // 可选：写入 attackSpeed.x (虽然 combo1 已用，但以防万一)
            var xAddr = dataPtr.add(ATTACK_SPEED_X);
            if (isReadable(xAddr)) {
                var x = xAddr.readFloat();
                if (isValidSpeed(x)) {
                    xAddr.writeFloat(SPEED);
                }
            }
        } catch(e) {}
    }

    function hook(addr, name) {
        Interceptor.attach(addr, {
            onEnter(args) {
                var self = args[0];
                if (isMyWeapon(self, ptr(0))) {
                    setCombo1Speed(self, name);
                    setAttackSegmentSpeeds(self);
                }
            }
        });
        console.log("[+] Hooked " + name + " @ " + addr);
    }

    hook(base.add(0xB64240), "OnSpecialBtnDown");
    hook(base.add(0xB642B0), "PlayKnifeAttackAnim");
    hook(base.add(0xB63BD0), "AnimSpeedSetting");

    console.log("[+] V11 Loaded. Light1, Light2, Heavy all accelerated!");
})();