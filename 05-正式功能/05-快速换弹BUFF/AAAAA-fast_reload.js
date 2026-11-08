// AAAAA-fast_reload.js — 快速换弹（GUN + RPG，倍率可调）
//
// 独立版脚本（不依赖整合包运行时）：frida -n <游戏进程> -l AAAAA-fast_reload.js
// 2.8 整合包内的同源实现：04-正式发行版/全功能整合包2.8/game_modifier/features/05_ammoplus/script.js
// 原理/逆向过程见同目录《无限弹匣+快速换弹-经验总结.md》
//
// 两条路径（GUN 和 RPG 的实现完全不同，不能只做一条）：
//   GUN：WPN_Gun.Reload 每次算出 GetAnimSpeed(reloadAnimRatio) × PlayerWeapons.ReloadSpeed，
//        再 CFAnimator.SetFloat("ReloadSpeed", v) 播放 "reload" 动画 → 在这里把 v 乘倍率。
//   RPG：WPN_RPG.OnReloadBtnDown(0xB67AF0) 只播放动画、从不写 "ReloadSpeed"
//        （那个参数只在 Deploy 的 AnimSpeedSetting 里写一次，且 RPG 的换弹动画不吃它），
//        → 换弹前直接改武器/手部 Animator.speed，动画结束复位 1.0。

console.log("[*] ======================================");
console.log("[*]  FAST RELOAD (GUN + RPG)");
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

    function collectRpgAnimators(weapon) {
        var list = [];
        var weaponAnimator = readPtr(weapon.add(0x40));
        if (weaponAnimator) list.push(weaponAnimator);
        var owner = readPtr(weapon.add(0x30));
        var model = owner ? readPtr(owner.add(0x5C)) : null;
        var handAnimator = model ? readPtr(model.add(0x4C)) : null;
        if (handAnimator) list.push(handAnimator);
        return list;
    }

    // ---------- GUN：乘 "ReloadSpeed" 参数 ----------
    var setFloatAddr = base.add(0xB34E40);
    var originalSetFloat = new NativeFunction(setFloatAddr, 'void', ['pointer', 'pointer', 'float', 'int', 'pointer']);
    var gunCount = 0;

    Interceptor.replace(setFloatAddr, new NativeCallback(function (self, name, value, character, method) {
        try {
            if (isReloadParamName(name) && isMyWeapon(self, ptr(0)) && !isRpgWeapon(self)) {
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

    // ---------- RPG：改动画器速度 ----------
    var rpgAnimators = [];
    var rpgRestoreTimer = null;
    var rpgCount = 0;

    function restoreRpgAnimators() {
        for (var i = 0; i < rpgAnimators.length; i++) {
            try { animatorSetSpeed(rpgAnimators[i], 1.0, ptr(0)); } catch (e) {}
        }
        rpgAnimators = [];
        if (rpgRestoreTimer) { try { clearTimeout(rpgRestoreTimer); } catch (e) {} rpgRestoreTimer = null; }
    }

    Interceptor.attach(base.add(0xB67AF0), {          // WPN_RPG.OnReloadBtnDown
        onEnter: function (args) {
            try {
                var weapon = args[0];
                if (!weapon || weapon.isNull()) return;
                if (!isMyWeapon(weapon, ptr(0))) return;
                if (!isRpgWeapon(weapon)) return;
                if (RELOAD_MULTIPLIER <= 1.001) { restoreRpgAnimators(); return; }
                var list = collectRpgAnimators(weapon);
                if (!list.length) return;
                for (var i = 0; i < list.length; i++) animatorSetSpeed(list[i], RELOAD_MULTIPLIER, ptr(0));
                rpgAnimators = list;
                rpgCount++;
                if (rpgCount <= 5) {
                    console.log("[RPG] reload animator speed -> " + RELOAD_MULTIPLIER.toFixed(1) + "x (" + list.length + " animator)");
                }
                if (rpgRestoreTimer) { try { clearTimeout(rpgRestoreTimer); } catch (e) {} }
                rpgRestoreTimer = setTimeout(function () { restoreRpgAnimators(); }, 5000);
            } catch (e) {}
        }
    });

    Interceptor.attach(base.add(0xB67640), {          // WPN_RPG.OnAnimationEnd
        onEnter: function (args) {
            try {
                if (!rpgAnimators.length) return;
                if (readIl2CppString(args[2]) === 'reload') restoreRpgAnimators();
            } catch (e) {}
        }
    });

    Interceptor.attach(base.add(0xB67030), {          // WPN_RPG.Deploy
        onEnter: function () {
            try { if (rpgAnimators.length) restoreRpgAnimators(); } catch (e) {}
        }
    });

    console.log("[+] CFAnimator.SetFloat @ " + setFloatAddr + " hooked (GUN)");
    console.log("[+] WPN_RPG.OnReloadBtnDown @ " + base.add(0xB67AF0) + " hooked (RPG)");
    console.log("[+] Multiplier: " + RELOAD_MULTIPLIER.toFixed(1) + "x (1.0 ~ 5.0)");
    console.log("[+] 覆盖：WPN_Gun 系（步枪/冲锋枪/狙击/手枪/霰弹/榴弹枪）+ WPN_RPG（火箭筒/AT4）");
    console.log("[+] TEST SCRIPT ACTIVE - 进入任意模式即可生效");
})();
