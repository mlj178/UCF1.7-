// plan5_buff_infinite_ammo.js
// 方案5：复用游戏原生 InfinityAmmoBuff 的标志位（推荐方案 A）
// 并补充 WPN_RPG / AT4 / Nano AT4（它们不读 Player.Buff_InfinityAmmo）。
//
// 结论：游戏里的“无限弹药 buff”没有预制体依赖，也不是多人生化模式专属。
// 它只是每帧把 Player.Buff_InfinityAmmo(+0x128) 置 true；
// 真正的弹药逻辑在 WPN_Gun.CanReload / ReloadOver 里读这个标志：
//   - 备弹为 0 时也允许换弹；
//   - 换弹完成直接把 clip 填到 maxClip，不扣备弹。
//
// WPN_RPG 的补充（RPG/AT4/Nano AT4）：
//   - CanReload：备弹为 0 时仍允许自动换弹；
//   - OnReloadBtnDown：手动换弹时临时补 1 发备弹让原逻辑启动，随后把 clip 填满并恢复备弹；
//   - Reload / ReloadOver：自动/动画事件路径兜底把 clip 填满。
//   填满 clip 后，后续 AmmoData.Reload 的 need=0，不会扣备弹。
//
// 关键地址（UnityCrossFire 1.7.1 / GameAssembly.dll，基址 + RVA）：
//   Player.UpdateBuffProperty   0xB547F0（先清 0，再调用 RefBool 回调）
//   Player.get_isMyPlayer       0xB55FD0
//   Weapon.get_isMyWeapon       0xB6E1D0
//   WPN_Gun.CanReload           0xB60E30（读 owner.Buff_InfinityAmmo）
//   WPN_Gun.ReloadOver          0xB62C10（buff 分支：clip = maxClip）
//   WPN_RPG.CanReload           0xB66E80
//   WPN_RPG.OnReloadBtnDown     0xB67AF0
//   WPN_RPG.Reload              0xB67C40
//   WPN_RPG.ReloadOver          0xB67BC0
//   AmmoData.get_isMaxClip      0xB6EEA0
//   AmmoData.get_canReload      0xB6EBD0
//   CFAnimator.get_isAnimEmptyTag 0xB35350
//
// 用法：frida -n UnityCrossFire.exe -l plan5_buff_infinite_ammo.js
// 默认只作用于本地玩家；把 SCOPE 改成 'all_players' 可让所有人机也无限备弹。
// 注意：这是“无限备弹”，打空弹夹后仍会换弹，只是换弹不消耗备弹、备弹为 0 也能换。
// RPG/AT4 实际弹药无限，HUD 也做了无限弹药图标覆盖。

(function () {
    var SCOPE = 'player_only'; // 'player_only' | 'all_players'
    var enabled = true;
    var hooks = [];

    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) {
        console.log('[-] GameAssembly.dll not found');
        return;
    }
    var base = mod.base;

    var isMyPlayer;
    var isMyWeapon;
    var ammoIsMaxClip;
    var ammoCanReload;
    var isAnimEmptyTag;
    try {
        isMyPlayer = new NativeFunction(base.add(0xB55FD0), 'bool', ['pointer', 'pointer']);
        isMyWeapon = new NativeFunction(base.add(0xB6E1D0), 'bool', ['pointer', 'pointer']);
        ammoIsMaxClip = new NativeFunction(base.add(0xB6EEA0), 'bool', ['pointer', 'pointer']);
        ammoCanReload = new NativeFunction(base.add(0xB6EBD0), 'bool', ['pointer', 'pointer']);
        isAnimEmptyTag = new NativeFunction(base.add(0xB35350), 'bool', ['pointer', 'pointer']);
    } catch (e) {
        console.log('[-] NativeFunction init failed: ' + e);
        return;
    }

    function isReadablePtr(p) {
        try {
            if (!p || p.isNull()) return false;
            p.readPointer();
            return true;
        } catch (e) {
            return false;
        }
    }

    function shouldAffect(weaponPtr) {
        if (!weaponPtr || weaponPtr.isNull()) return false;
        if (SCOPE === 'all_players') return true;
        try {
            if (isMyWeapon(weaponPtr, ptr(0))) return true;
        } catch (e1) {}
        try {
            // Weapon : CFAnimator : Model；owner 是 Model.owner(+0x30)。
            var owner = weaponPtr.add(0x30).readPointer();
            if (owner && !owner.isNull() && isReadablePtr(owner)) {
                return !!isMyPlayer(owner, ptr(0));
            }
        } catch (e2) {}
        return false;
    }

    function writeObscuredInt(fieldPtr, value) {
        try {
            if (!fieldPtr || fieldPtr.isNull()) return false;
            var key = fieldPtr.readS32();
            var encrypted = value ^ key;
            fieldPtr.add(0x4).writeS32(encrypted);
            fieldPtr.add(0x8).writeU8(1);
            fieldPtr.add(0xC).writeS32(value);
            fieldPtr.add(0x10).writeU8(0);
            return fieldPtr.add(0x4).readS32() === encrypted;
        } catch (e) {
            return false;
        }
    }

    function readRpgAmmo(weaponPtr) {
        try {
            var ammo = weaponPtr.add(0xEC).readPointer();
            if (!ammo || ammo.isNull() || !isReadablePtr(ammo)) return null;
            return ammo;
        } catch (e) {
            return null;
        }
    }

    // 20 字节 ObscuredInt 原样拷贝 maxClip -> clip。
    function copyAmmoClipToMax(ammoPtr) {
        try {
            if (!ammoPtr || ammoPtr.isNull() || !isReadablePtr(ammoPtr)) return false;
            var maxClipBytes = ammoPtr.add(0x30).readByteArray(0x14);
            if (!maxClipBytes) return false;
            ammoPtr.add(0x08).writeByteArray(maxClipBytes);
            return true;
        } catch (e) {
            return false;
        }
    }

    // il2cpp 对象 -> 类名（Il2CppClass.name 在 klass+0x8）。
    function classNameOf(objPtr) {
        try {
            if (!objPtr || objPtr.isNull()) return '';
            var klass = objPtr.readPointer();
            if (!klass || klass.isNull()) return '';
            var namePtr = klass.add(0x8).readPointer();
            if (!namePtr || namePtr.isNull()) return '';
            return namePtr.readUtf8String() || '';
        } catch (e) {
            return '';
        }
    }

    // 仅用于 HUD 判断：优先按类名识别 WPN_RPG（AT4 / Nano AT4 同一组件），
    // 不依赖 +0xF4(gunfire) 等序列化字段。类名读取失败时退回字段探测。
    function looksLikeRpgByFields(weaponPtr) {
        try {
            if (!weaponPtr || weaponPtr.isNull()) return false;
            var ammo = weaponPtr.add(0xEC).readPointer();
            var realData = weaponPtr.add(0xF0).readPointer();
            var gunfire = weaponPtr.add(0xF4).readPointer();
            if (!ammo || ammo.isNull() || !realData || realData.isNull()) return false;
            if (!isReadablePtr(ammo) || !isReadablePtr(realData) || !isReadablePtr(gunfire)) return false;
            return true;
        } catch (e) {
            return false;
        }
    }

    function isRpgWeapon(weaponPtr) {
        try {
            if (!weaponPtr || weaponPtr.isNull()) return false;
            var cls = classNameOf(weaponPtr);
            if (cls) return cls.indexOf('WPN_RPG') === 0;
            return looksLikeRpgByFields(weaponPtr);
        } catch (e) {
            return false;
        }
    }

    // 1) 原生 Buff_InfinityAmmo 标志位（普通 WPN_Gun 枪械）
    hooks.push(Interceptor.attach(base.add(0xB547F0), {
        onEnter: function (args) {
            this.player = args[0];
        },
        onLeave: function () {
            if (!enabled) return;
            var player = this.player;
            if (!player || player.isNull()) return;
            try {
                if (SCOPE !== 'all_players' && !isMyPlayer(player, ptr(0))) return;
                player.add(0x128).writeU8(1);
            } catch (e) {}
        }
    }));

    // 1.5) 仅 UI：WPN_RPG/AT4 的 HUD 无限弹药图标
    // HUD_Weapon.Update 只读 PlayerWeapons.get_isInfinityAmmo，放行这一个返回值即可。
    hooks.push(Interceptor.attach(base.add(0xB17120), {
        onEnter: function (args) {
            this.wpns = args[0];
        },
        onLeave: function (retval) {
            try {
                if (!enabled) return;
                var wpns = this.wpns;
                if (!wpns || wpns.isNull()) return;
                var inUse = wpns.add(0x18).readPointer();
                if (!inUse || inUse.isNull()) return;
                if ((retval.toInt32() & 0xff) !== 0) return;
                if (!isRpgWeapon(inUse)) return;
                if (!shouldAffect(inUse)) return;
                retval.replace(1);
            } catch (e) {}
        }
    }));

    // 2) WPN_RPG.CanReload：备弹为 0 时仍允许自动换弹
    hooks.push(Interceptor.attach(base.add(0xB66E80), {
        onEnter: function (args) {
            this.weapon = args[0];
        },
        onLeave: function (retval) {
            try {
                if (!enabled || retval.toInt32() !== 0) return;
                var self = this.weapon;
                if (!self || !shouldAffect(self)) return;
                var ammo = readRpgAmmo(self);
                if (!ammo) return;
                if (ammoIsMaxClip(ammo, ptr(0))) return;
                if (!isAnimEmptyTag(self, ptr(0))) return;
                retval.replace(1);
            } catch (e) {}
        }
    }));

    // 3) WPN_RPG.OnReloadBtnDown：手动换弹时临时补 1 发备弹让原逻辑启动，随后填满 clip 并恢复备弹
    hooks.push(Interceptor.attach(base.add(0xB67AF0), {
        onEnter: function (args) {
            this.weapon = args[0];
            this.ammo = null;
            this.injected = false;
            try {
                if (!enabled) return;
                var self = this.weapon;
                if (!self || !shouldAffect(self)) return;
                var ammo = readRpgAmmo(self);
                if (!ammo) return;
                if (ammoIsMaxClip(ammo, ptr(0))) return;
                if (!isAnimEmptyTag(self, ptr(0))) return;
                this.ammo = ammo;
                if (!ammoCanReload(ammo, ptr(0))) {
                    if (writeObscuredInt(ammo.add(0x1C), 1)) {
                        this.injected = true;
                    } else {
                        this.ammo = null;
                    }
                }
            } catch (e) {
                this.ammo = null;
            }
        },
        onLeave: function () {
            var ammo = this.ammo;
            if (!ammo) return;
            try {
                copyAmmoClipToMax(ammo);
                if (this.injected) writeObscuredInt(ammo.add(0x1C), 0);
            } catch (e) {}
        }
    }));

    // 4) WPN_RPG.Reload：自动换弹路径启动时把 clip 填满
    hooks.push(Interceptor.attach(base.add(0xB67C40), {
        onEnter: function (args) {
            this.weapon = args[0];
        },
        onLeave: function () {
            try {
                if (!enabled) return;
                var self = this.weapon;
                if (!self || !shouldAffect(self)) return;
                var ammo = readRpgAmmo(self);
                if (!ammo) return;
                if (!ammoIsMaxClip(ammo, ptr(0))) copyAmmoClipToMax(ammo);
            } catch (e) {}
        }
    }));

    // 5) WPN_RPG.ReloadOver：动画事件换弹完成路径兜底填满
    hooks.push(Interceptor.attach(base.add(0xB67BC0), {
        onEnter: function (args) {
            try {
                if (!enabled) return;
                var self = args[0];
                if (!self || !shouldAffect(self)) return;
                var ammo = readRpgAmmo(self);
                if (!ammo) return;
                if (!ammoIsMaxClip(ammo, ptr(0))) copyAmmoClipToMax(ammo);
            } catch (e) {}
        }
    }));

    console.log('[+] plan5 active: Player.Buff_InfinityAmmo = 1 every frame');
    console.log('[+] WPN_Gun.CanReload / ReloadOver use infinite reserve ammo');
    console.log('[+] WPN_RPG / AT4 / Nano AT4 supplemented');
    console.log('[+] scope = ' + SCOPE);

    rpc.exports = {
        setenabled: function (value) {
            enabled = !!value;
            console.log('[+] enabled = ' + enabled);
            return enabled;
        },
        setscope: function (value) {
            SCOPE = value === 'all_players' ? 'all_players' : 'player_only';
            console.log('[+] scope = ' + SCOPE);
            return SCOPE;
        },
        status: function () {
            return { enabled: enabled, scope: SCOPE, hooks: hooks.length };
        },
        unload: function () {
            for (var i = 0; i < hooks.length; i++) {
                try { hooks[i].detach(); } catch (e) {}
            }
            hooks = [];
            return true;
        }
    };
})();