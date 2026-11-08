// AAAAA-fast_reload.js — 快速换弹（GUN / 榴弹模式 / RPG，倍率可调）
//
// 独立版脚本（不依赖整合包运行时）：frida -n <游戏进程> -l AAAAA-fast_reload.js
// 2.8 整合包内的同源实现：04-正式发行版/全功能整合包2.8/game_modifier/features/05_ammoplus/script.js
// 原理/逆向过程见同目录《无限弹匣+快速换弹-经验总结.md》
//
// 三条路径（缺一不可）：
//   1) 普通枪械：WPN_Gun.Reload 每帧算 GetAnimSpeed(reloadAnimRatio) × PlayerWeapons.ReloadSpeed
//      再 CFAnimator.SetFloat("ReloadSpeed", v) → 在这里把 v 乘倍率。
//   2) 步枪的榴弹模式（CFAnimator.changeMode+0x54）：换弹动画名被改写为 "reload_A"，
//      不吃 "ReloadSpeed" 参数 → 改为把武器/手部 Animator.speed 设为倍率。
//   3) WPN_RPG（火箭筒/AT4）：换弹入口 OnReloadBtnDown 从不写 "ReloadSpeed" → 同样改 Animator.speed。

console.log("[*] ======================================");
console.log("[*]  FAST RELOAD (GUN / GRENADE MODE / RPG)");
console.log("[*]  快速换弹 - 全武器通用");
console.log("[*] ======================================");

(function () {
    // ======== 可调参数（1.0 = 原速，5.0 = 最快）========
    var RELOAD_MULTIPLIER = 4.0;
    // =================================================

    var RELOAD_PARAM = 'ReloadSpeed';

    var mod = Process.findModuleByName("GameAssembly.dll");
    if (!mod) {
        console.log("[-] GameAssembly.dll not found!");
        return;
    }
    var base = mod.base;

    var isMyWeapon = new NativeFunction(base.add(0xB6E1D0), 'bool', ['pointer', 'pointer']);
    var animatorSetSpeed = new NativeFunction(base.add(0xAA8C30), 'void', ['pointer', 'float', 'pointer']);

    function readPtr(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            var v = addr.readPointer();
            return (v && !v.isNull()) ? v : null;
        } catch (e) { return null; }
    }

    function readIl2CppString(p) {
        try {
            if (!p || p.isNull()) return '';
            var len = p.add(8).readS32();
            if (len <= 0 || len > 64) return '';
            var out = '';
            for (var i = 0; i < len; i++) out += String.fromCharCode(p.add(12 + i * 2).readU16());
            return out;
        } catch (e) { return ''; }
    }

    function isReloadParamName(namePtr) {
        try {
            if (!namePtr || namePtr.isNull()) return false;
            if (namePtr.add(8).readS32() !== RELOAD_PARAM.length) return false;
            var chars = namePtr.add(12);
            for (var i = 0; i < RELOAD_PARAM.length; i++) {
                if (chars.add(i * 2).readU16() !== RELOAD_PARAM.charCodeAt(i)) return false;
            }
            return true;
        } catch (e) { return false; }
    }

    // WPN_RPG：Weapon.data(+0x68) 与 WPN_RPG.realData(+0xF0) 是同一个 WD_RPG 实例
    function isRpgWeapon(weapon) {
        try {
            if (!weapon || weapon.isNull()) return false;
            var realData = readPtr(weapon.add(0xF0));
            if (!realData) return false;
            var data = readPtr(weapon.add(0x68));
            if (!data) return false;
            return data.equals(realData);
        } catch (e) { return false; }
    }

    // 榴弹模式：CFAnimator.changeMode(+0x54)
    function isGrenadeMode(weapon) {
        try {
            if (!weapon || weapon.isNull()) return false;
            return weapon.add(0x54).readU8() !== 0;
        } catch (e) { return false; }
    }

    function collectAnimators(weapon) {
        var list = [];
        var weaponAnimator = readPtr(weapon.add(0x40));
        if (weaponAnimator) list.push(weaponAnimator);
        var owner = readPtr(weapon.add(0x30));
        var model = owner ? readPtr(owner.add(0x5C)) : null;
        var handAnimator = model ? readPtr(model.add(0x4C)) : null;
        if (handAnimator) list.push(handAnimator);
        return list;
    }

    var speedTargets = [];
    var speedRestoreTimer = null;

    function restoreAnimatorSpeed() {
        for (var i = 0; i < speedTargets.length; i++) {
            try { animatorSetSpeed(speedTargets[i], 1.0, ptr(0)); } catch (e) {}
        }
        speedTargets = [];
        if (speedRestoreTimer) { try { clearTimeout(speedRestoreTimer); } catch (e) {} speedRestoreTimer = null; }
    }

    function applyAnimatorSpeed(weapon) {
        if (RELOAD_MULTIPLIER <= 1.001) { restoreAnimatorSpeed(); return false; }
        var list = collectAnimators(weapon);
        if (!list.length) return false;
        for (var i = 0; i < list.length; i++) animatorSetSpeed(list[i], RELOAD_MULTIPLIER, ptr(0));
        speedTargets = list;
        if (speedRestoreTimer) { try { clearTimeout(speedRestoreTimer); } catch (e) {} }
        speedRestoreTimer = setTimeout(function () { restoreAnimatorSpeed(); }, 5000);
        return true;
    }

    // ---------- 1) 普通枪械：乘 "ReloadSpeed" 参数 ----------
    var setFloatAddr = base.add(0xB34E40);
    var originalSetFloat = new NativeFunction(setFloatAddr, 'void', ['pointer', 'pointer', 'float', 'int', 'pointer']);
    var gunCount = 0;

    Interceptor.replace(setFloatAddr, new NativeCallback(function (self, name, value, character, method) {
        try {
            if (isReloadParamName(name) && isMyWeapon(self, ptr(0)) &&
                !isGrenadeMode(self) && !isRpgWeapon(self)) {
                gunCount++;
                if (gunCount <= 5) {
                    console.log("[GUN] ReloadSpeed " + value.toFixed(2) + " -> " +
                        (value * RELOAD_MULTIPLIER).toFixed(2) + " (" + RELOAD_MULTIPLIER.toFixed(1) + "x)");
                }
                value = value * RELOAD_MULTIPLIER;
            }
        } catch (e) {}
        return originalSetFloat(self, name, value, character, method);
    }, 'void', ['pointer', 'pointer', 'float', 'int', 'pointer']));

    // ---------- 2) 榴弹模式：改动画器速度 ----------
    var grenadeCount = 0;
    Interceptor.attach(base.add(0xB62CB0), {          // WPN_Gun.Reload
        onEnter: function (args) {
            try {
                var weapon = args[0];
                if (!weapon || weapon.isNull()) return;
                if (!isMyWeapon(weapon, ptr(0))) return;
                if (isRpgWeapon(weapon) || !isGrenadeMode(weapon)) return;
                if (applyAnimatorSpeed(weapon)) {
                    grenadeCount++;
                    if (grenadeCount <= 5) {
                        console.log("[GRENADE] reload animator speed -> " + RELOAD_MULTIPLIER.toFixed(1) + "x");
                    }
                }
            } catch (e) {}
        }
    });

    Interceptor.attach(base.add(0xB627A0), {          // WPN_Gun.OnAnimationEnd
        onEnter: function (args) {
            try {
                if (!speedTargets.length) return;
                if (readIl2CppString(args[2]) === 'reload') restoreAnimatorSpeed();
            } catch (e) {}
        }
    });

    Interceptor.attach(base.add(0xB5FCF0), {          // WPN_GrenadeGun.OnSpecialBtnDown（切模式）
        onEnter: function () {
            try { if (speedTargets.length) restoreAnimatorSpeed(); } catch (e) {}
        }
    });

    // ---------- 3) RPG / AT4：改动画器速度 ----------
    var rpgCount = 0;
    Interceptor.attach(base.add(0xB67AF0), {          // WPN_RPG.OnReloadBtnDown
        onEnter: function (args) {
            try {
                var weapon = args[0];
                if (!weapon || weapon.isNull()) return;
                if (!isMyWeapon(weapon, ptr(0))) return;
                if (!isRpgWeapon(weapon)) return;
                if (applyAnimatorSpeed(weapon)) {
                    rpgCount++;
                    if (rpgCount <= 5) {
                        console.log("[RPG] reload animator speed -> " + RELOAD_MULTIPLIER.toFixed(1) + "x (" + speedTargets.length + " animator)");
                    }
                }
            } catch (e) {}
        }
    });

    Interceptor.attach(base.add(0xB67640), {          // WPN_RPG.OnAnimationEnd
        onEnter: function (args) {
            try {
                if (!speedTargets.length) return;
                if (readIl2CppString(args[2]) === 'reload') restoreAnimatorSpeed();
            } catch (e) {}
        }
    });

    Interceptor.attach(base.add(0xB67030), {          // WPN_RPG.Deploy
        onEnter: function () {
            try { if (speedTargets.length) restoreAnimatorSpeed(); } catch (e) {}
        }
    });

    console.log("[+] CFAnimator.SetFloat @ " + setFloatAddr + " hooked (普通枪械)");
    console.log("[+] WPN_Gun.Reload @ " + base.add(0xB62CB0) + " hooked (榴弹模式)");
    console.log("[+] WPN_RPG.OnReloadBtnDown @ " + base.add(0xB67AF0) + " hooked (RPG/AT4)");
    console.log("[+] Multiplier: " + RELOAD_MULTIPLIER.toFixed(1) + "x (1.0 ~ 5.0)");
    console.log("[+] TEST SCRIPT ACTIVE - 进入任意模式即可生效");
})();
