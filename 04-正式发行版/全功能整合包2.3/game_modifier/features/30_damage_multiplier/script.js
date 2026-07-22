// ============================================================
// AAAAA-damage_multiplier_min.js
//
// feature_id: "damage_multiplier"
// 功能目标：提高本地玩家造成的最终生命伤害。
//
// 实现原理：
//   1. Hook Entity.OnEntityHurt / Player.OnEntityHurt。
//   2. 在 x86 cdecl 栈上定位按值传入的 DamageEventData。
//   3. 只在 attacker 或其 owner 为本地玩家、victim 非本地玩家时，
//      修改 DamageEventData.damage。
//   4. 记录 WPN_Missile.SetOwner / SentryGun.SetData，用于导弹、RPG、
//      榴弹和炮台这类特殊来源的归属判断。
//
// RVA / 字段来源：dump.cs + script.json + 现有功能脚本交叉验证
//   Entity_OnEntityHurt:        0x00B3F470
//   Player_OnEntityHurt:        0x00B516B0
//   Player_get_isMyPlayer:      0x00B55FD0
//   SentryGun_SetData:          0x00B1E030
//   WPN_Missile_SetOwner:       0x00B66390
//   DamageEventData.attacker:   0x00
//   DamageEventData.victim:     0x04
//   DamageEventData.damage:     0x08
//   DamageEventData.type:       0x34
//   DamageEventData.damageTag:  0x38
//   DamageEventData.wpnIndex:   0x3C
//   DamageEventData.wpnSprIndex:0x40
//   DamageEventData.ignoreDmgRate: 0x44
// ============================================================

(function () {
    'use strict';

    var MODULE_NAME = 'GameAssembly.dll';
    var CALL_CONV = 'mscdecl';

    var DamageType = {
        Invalid: 0,
        Gun: 1,
        Knife: 2,
        Grenade: 3,
        Infect: 4,
        Other: 5
    };

    var RVA = {
        Entity_OnEntityHurt: 0x00B3F470,
        Player_OnEntityHurt: 0x00B516B0,
        Player_get_isMyPlayer: 0x00B55FD0,
        SentryGun_SetData: 0x00B1E030,
        WPN_Missile_SetOwner: 0x00B66390
    };

    var OFF = {
        Dmg_attacker: 0x00,
        Dmg_victim: 0x04,
        Dmg_damage: 0x08,
        Dmg_type: 0x34,
        Dmg_damageTag: 0x38,
        Dmg_wpnIndex: 0x3C,
        Dmg_wpnSprIndex: 0x40,
        Dmg_ignoreDmgRate: 0x44
    };

    var Runtime = {
        feature_id: "damage_multiplier",
        enabled: false,
        initialized: false,
        module: null,
        base: ptr(0),
        hooks: [],
        playerHurtDepth: 0,
        missileOwners: {},
        sentryOwners: {},
        ownerTtlMs: 15000,
        config: {
            multiplier: 2.0,
            min_multiplier: 1.0,
            max_multiplier: 20.0,
            max_damage: 999999.0,
            skip_local_victim: true,
            include_infect: false,
            allow_other_damage_type: true,
            enable_owner_mapping: true,
            diagnostic_log: true
        },
        stats: {
            totalHurtEvents: 0,
            entityHurtEvents: 0,
            playerHurtEvents: 0,
            multipliedEvents: 0,
            skippedDisabled: 0,
            skippedPlayerBaseDepth: 0,
            skippedInvalidEvent: 0,
            skippedInvalidDamage: 0,
            skippedDamageType: 0,
            skippedInfect: 0,
            skippedNotLocalAttacker: 0,
            skippedLocalVictim: 0,
            missileOwnerHits: 0,
            sentryOwnerHits: 0,
            missileOwnerRecords: 0,
            sentryOwnerRecords: 0,
            errorCount: 0,
            cleanupCount: 0,
            lastOriginalDamage: 0.0,
            lastNewDamage: 0.0,
            lastDamageType: 0,
            lastDamageTag: 0,
            lastWpnIndex: -1,
            lastWpnSprIndex: -1,
            lastIgnoreDmgRate: false,
            lastSource: "",
            lastDecision: "",
            lastError: ""
        }
    };

    var native = {
        ready: false,
        isMyPlayer: null
    };

    var LogLimiter = {};

    function log(level, message) {
        try {
            var text = '[' + Runtime.feature_id + '][' + level + '] ' + message;
            console.log(text);
            send({ type: 'log', level: level, module: Runtime.feature_id, message: message });
        } catch (_) {
        }
    }

    function logLimited(key, level, message, intervalMs) {
        var now = Date.now();
        var wait = intervalMs || 1000;
        if (!LogLimiter[key] || now - LogLimiter[key] >= wait) {
            LogLimiter[key] = now;
            log(level, message);
        }
    }

    function setError(label, error) {
        Runtime.stats.errorCount += 1;
        Runtime.stats.lastError = label + (error && error.message ? ': ' + error.message : '');
        logLimited('error:' + label, 'error', Runtime.stats.lastError, 1500);
    }

    function isNull(p) {
        if (p === null || p === undefined) return true;
        try { return p.isNull(); } catch (_) { return true; }
    }

    function isReadablePtr(p) {
        try {
            if (isNull(p)) return false;
            p.readPointer();
            return true;
        } catch (_) {
            return false;
        }
    }

    function clampFloat(value, minValue, maxValue) {
        var n = Number(value);
        if (!isFinite(n)) return minValue;
        if (n < minValue) return minValue;
        if (n > maxValue) return maxValue;
        return n;
    }

    function findGameAssembly() {
        if (Runtime.module) return Runtime.module;
        var mod = Process.findModuleByName(MODULE_NAME);
        if (!mod) {
            Runtime.stats.lastError = MODULE_NAME + ' not found';
            return null;
        }
        Runtime.module = mod;
        Runtime.base = mod.base;
        return mod;
    }

    function initNativeFunctions() {
        if (native.ready) return true;
        var mod = findGameAssembly();
        if (!mod) return false;

        if (Process.arch !== 'ia32' || Process.pointerSize !== 4) {
            Runtime.stats.lastError = 'unsupported process: arch=' + Process.arch + ', pointerSize=' + Process.pointerSize;
            log('error', Runtime.stats.lastError);
            return false;
        }

        try {
            native.isMyPlayer = new NativeFunction(
                Runtime.base.add(RVA.Player_get_isMyPlayer),
                'bool',
                ['pointer', 'pointer'],
                CALL_CONV
            );
            native.ready = true;
            return true;
        } catch (error) {
            setError('initNativeFunctions failed', error);
            native.ready = false;
            return false;
        }
    }

    function isLocalPlayer(entityPtr) {
        if (!native.ready && !initNativeFunctions()) return false;
        if (isNull(entityPtr)) return false;
        try {
            return !!native.isMyPlayer(entityPtr, ptr(0));
        } catch (error) {
            setError('Player.get_isMyPlayer failed', error);
            return false;
        }
    }

    function ptrKey(p) {
        try { return p.toString(); } catch (_) { return '0x0'; }
    }

    function pruneOwners(map) {
        var now = Date.now();
        Object.keys(map).forEach(function (key) {
            if (!map[key] || map[key].expiresAt <= now) delete map[key];
        });
    }

    function rememberOwner(map, objectPtr, ownerPtr, kind) {
        if (!Runtime.config.enable_owner_mapping) return;
        if (isNull(objectPtr) || isNull(ownerPtr)) return;
        pruneOwners(map);
        map[ptrKey(objectPtr)] = {
            owner: ownerPtr,
            expiresAt: Date.now() + Runtime.ownerTtlMs
        };
        if (kind === 'missile') Runtime.stats.missileOwnerRecords += 1;
        if (kind === 'sentry') Runtime.stats.sentryOwnerRecords += 1;
    }

    function getRememberedOwner(map, objectPtr) {
        if (!Runtime.config.enable_owner_mapping || isNull(objectPtr)) return ptr(0);
        pruneOwners(map);
        var item = map[ptrKey(objectPtr)];
        if (!item) return ptr(0);
        return item.owner || ptr(0);
    }

    function resolveEffectiveAttacker(attacker) {
        if (isNull(attacker)) return ptr(0);
        if (isLocalPlayer(attacker)) return attacker;

        var missileOwner = getRememberedOwner(Runtime.missileOwners, attacker);
        if (!isNull(missileOwner) && isLocalPlayer(missileOwner)) {
            Runtime.stats.missileOwnerHits += 1;
            return missileOwner;
        }

        var sentryOwner = getRememberedOwner(Runtime.sentryOwners, attacker);
        if (!isNull(sentryOwner) && isLocalPlayer(sentryOwner)) {
            Runtime.stats.sentryOwnerHits += 1;
            return sentryOwner;
        }

        return ptr(0);
    }

    function isSupportedDamageType(type) {
        if (type === DamageType.Gun || type === DamageType.Knife || type === DamageType.Grenade) return true;
        if (type === DamageType.Other && Runtime.config.allow_other_damage_type) return true;
        return false;
    }

    function readDamageEvent(eventPtr) {
        if (isNull(eventPtr) || !isReadablePtr(eventPtr)) return null;
        try {
            return {
                attacker: eventPtr.add(OFF.Dmg_attacker).readPointer(),
                victim: eventPtr.add(OFF.Dmg_victim).readPointer(),
                damage: eventPtr.add(OFF.Dmg_damage).readFloat(),
                type: eventPtr.add(OFF.Dmg_type).readS32(),
                damageTag: eventPtr.add(OFF.Dmg_damageTag).readS32(),
                wpnIndex: eventPtr.add(OFF.Dmg_wpnIndex).readS32(),
                wpnSprIndex: eventPtr.add(OFF.Dmg_wpnSprIndex).readS32(),
                ignoreDmgRate: eventPtr.add(OFF.Dmg_ignoreDmgRate).readU8() !== 0
            };
        } catch (error) {
            setError('read DamageEventData failed', error);
            return null;
        }
    }

    function recordLast(data, source, decision, newDamage) {
        Runtime.stats.lastOriginalDamage = data ? data.damage : 0.0;
        Runtime.stats.lastNewDamage = newDamage === undefined ? 0.0 : newDamage;
        Runtime.stats.lastDamageType = data ? data.type : 0;
        Runtime.stats.lastDamageTag = data ? data.damageTag : 0;
        Runtime.stats.lastWpnIndex = data ? data.wpnIndex : -1;
        Runtime.stats.lastWpnSprIndex = data ? data.wpnSprIndex : -1;
        Runtime.stats.lastIgnoreDmgRate = data ? data.ignoreDmgRate : false;
        Runtime.stats.lastSource = source || "";
        Runtime.stats.lastDecision = decision || "";
    }

    function formatFloat(value) {
        if (!isFinite(value)) return String(value);
        return value.toFixed(3);
    }

    function logDamageDiagnostic(data, source, multiplier, newDamage, effectiveAttacker, victim, victimIsLocal) {
        if (!Runtime.config.diagnostic_log) return;

        var truncDamage = newDamage < 0 ? Math.ceil(newDamage) : Math.floor(newDamage);
        var message = 'damage_diag source=' + source +
            ' raw_damage=' + formatFloat(data.damage) +
            ' multiplier=' + formatFloat(multiplier) +
            ' new_damage=' + formatFloat(newDamage) +
            ' trunc=' + truncDamage +
            ' floor=' + Math.floor(newDamage) +
            ' round=' + Math.round(newDamage) +
            ' ceil=' + Math.ceil(newDamage) +
            ' below_one=' + (newDamage > 0 && newDamage < 1) +
            ' type=' + data.type +
            ' tag=' + data.damageTag +
            ' wpn=' + data.wpnIndex +
            ' spr=' + data.wpnSprIndex +
            ' attacker=' + ptrKey(data.attacker) +
            ' effective_attacker=' + ptrKey(effectiveAttacker) +
            ' victim=' + ptrKey(victim) +
            ' victim_is_local=' + victimIsLocal +
            ' ignoreDmgRate=' + data.ignoreDmgRate;

        logLimited('damage_diagnostic', 'info', message, 300);
    }

    function multiplyDamageEvent(eventPtr, source) {
        Runtime.stats.totalHurtEvents += 1;
        if (!Runtime.enabled) {
            Runtime.stats.skippedDisabled += 1;
            return false;
        }

        var data = readDamageEvent(eventPtr);
        if (!data) {
            Runtime.stats.skippedInvalidEvent += 1;
            recordLast(null, source, 'invalid_event');
            return false;
        }

        if (!isFinite(data.damage) || data.damage <= 0) {
            Runtime.stats.skippedInvalidDamage += 1;
            recordLast(data, source, 'invalid_damage');
            return false;
        }

        if (data.type === DamageType.Infect && !Runtime.config.include_infect) {
            Runtime.stats.skippedInfect += 1;
            recordLast(data, source, 'skip_infect');
            return false;
        }

        if (!isSupportedDamageType(data.type)) {
            Runtime.stats.skippedDamageType += 1;
            recordLast(data, source, 'skip_damage_type');
            return false;
        }

        var effectiveAttacker = resolveEffectiveAttacker(data.attacker);
        if (isNull(effectiveAttacker)) {
            Runtime.stats.skippedNotLocalAttacker += 1;
            recordLast(data, source, 'skip_not_local_attacker');
            return false;
        }

        var victim = data.victim;
        var victimIsLocal = isLocalPlayer(victim);
        if (Runtime.config.skip_local_victim && victimIsLocal) {
            Runtime.stats.skippedLocalVictim += 1;
            recordLast(data, source, 'skip_local_victim');
            return false;
        }

        var multiplier = clampFloat(
            Runtime.config.multiplier,
            Runtime.config.min_multiplier,
            Runtime.config.max_multiplier
        );
        var newDamage = data.damage * multiplier;
        if (newDamage > Runtime.config.max_damage) newDamage = Runtime.config.max_damage;
        if (newDamage < 0) newDamage = 0;
        logDamageDiagnostic(data, source, multiplier, newDamage, effectiveAttacker, victim, victimIsLocal);

        try {
            var damageAddr = eventPtr.add(OFF.Dmg_damage);
            damageAddr.writeFloat(newDamage);
            Runtime.stats.multipliedEvents += 1;
            recordLast(data, source, 'multiplied', newDamage);
            if (Runtime.config.diagnostic_log) {
                logLimited(
                    'multiplied',
                    'info',
                    source + ' damage ' + data.damage.toFixed(2) + ' -> ' + newDamage.toFixed(2) +
                    ', type=' + data.type + ', wpn=' + data.wpnIndex,
                    500
                );
            }
            return true;
        } catch (error) {
            setError('write damage failed', error);
            recordLast(data, source, 'write_failed');
            return false;
        }
    }

    function eventDataFromOnEntityHurtStack(context) {
        // x86 cdecl: [ESP+4] = this, [ESP+8] = DamageEventData.attacker.
        return context.esp.add(8);
    }

    function attachHook(name, rva, callbacks) {
        var addr = Runtime.base.add(rva);
        var hook = Interceptor.attach(addr, callbacks);
        Runtime.hooks.push({ name: name, hook: hook });
        log('success', name + ' hook installed at ' + addr);
    }

    function attachHooks() {
        attachHook('Player.OnEntityHurt', RVA.Player_OnEntityHurt, {
            onEnter: function () {
                Runtime.playerHurtDepth += 1;
                Runtime.stats.playerHurtEvents += 1;
                this.depthEntered = true;
                try {
                    multiplyDamageEvent(eventDataFromOnEntityHurtStack(this.context), 'Player.OnEntityHurt');
                } catch (error) {
                    setError('Player.OnEntityHurt onEnter failed', error);
                }
            },
            onLeave: function () {
                if (this.depthEntered) Runtime.playerHurtDepth = Math.max(0, Runtime.playerHurtDepth - 1);
            }
        });

        attachHook('Entity.OnEntityHurt', RVA.Entity_OnEntityHurt, {
            onEnter: function () {
                Runtime.stats.entityHurtEvents += 1;
                if (Runtime.playerHurtDepth > 0) {
                    Runtime.stats.skippedPlayerBaseDepth += 1;
                    return;
                }
                try {
                    multiplyDamageEvent(eventDataFromOnEntityHurtStack(this.context), 'Entity.OnEntityHurt');
                } catch (error) {
                    setError('Entity.OnEntityHurt onEnter failed', error);
                }
            }
        });

        attachHook('WPN_Missile.SetOwner', RVA.WPN_Missile_SetOwner, {
            onEnter: function (args) {
                try {
                    rememberOwner(Runtime.missileOwners, args[0], args[1], 'missile');
                } catch (error) {
                    setError('WPN_Missile.SetOwner failed', error);
                }
            }
        });

        attachHook('SentryGun.SetData', RVA.SentryGun_SetData, {
            onEnter: function (args) {
                try {
                    rememberOwner(Runtime.sentryOwners, args[0], args[1], 'sentry');
                } catch (error) {
                    setError('SentryGun.SetData failed', error);
                }
            }
        });
    }

    function cleanupHooks() {
        Runtime.hooks.forEach(function (item) {
            try { item.hook.detach(); } catch (_) {}
        });
        Runtime.hooks = [];
    }

    function resetRuntimeStats() {
        Object.keys(Runtime.stats).forEach(function (key) {
            if (typeof Runtime.stats[key] === 'number') Runtime.stats[key] = 0;
            else if (typeof Runtime.stats[key] === 'boolean') Runtime.stats[key] = false;
            else Runtime.stats[key] = "";
        });
        Runtime.stats.lastWpnIndex = -1;
        Runtime.stats.lastWpnSprIndex = -1;
    }

    function initializeFeature() {
        if (Runtime.initialized) return true;
        if (!initNativeFunctions()) return false;
        try {
            attachHooks();
            Runtime.initialized = true;
            return true;
        } catch (error) {
            setError('initializeFeature failed', error);
            cleanupHooks();
            Runtime.initialized = false;
            return false;
        }
    }

    function enableFeature() {
        if (!initializeFeature()) return getStatus();
        Runtime.enabled = true;
        log('success', 'damage multiplier enabled, multiplier=' + Runtime.config.multiplier);
        return getStatus();
    }

    function disableFeature() {
        Runtime.enabled = false;
        log('info', 'damage multiplier disabled');
        return getStatus();
    }

    function cleanupFeature() {
        Runtime.enabled = false;
        cleanupHooks();
        Runtime.initialized = false;
        Runtime.playerHurtDepth = 0;
        Runtime.missileOwners = {};
        Runtime.sentryOwners = {};
        Runtime.stats.cleanupCount += 1;
        log('info', 'cleanup complete');
        return getStatus();
    }

    function updateConfig(config) {
        config = config || {};
        if (config.multiplier !== undefined) {
            Runtime.config.multiplier = clampFloat(
                config.multiplier,
                Runtime.config.min_multiplier,
                Runtime.config.max_multiplier
            );
        }
        [
            'skip_local_victim',
            'include_infect',
            'allow_other_damage_type',
            'enable_owner_mapping',
            'diagnostic_log'
        ].forEach(function (key) {
            if (config[key] !== undefined) Runtime.config[key] = !!config[key];
        });
        if (config.max_damage !== undefined) {
            Runtime.config.max_damage = clampFloat(config.max_damage, 1.0, 99999999.0);
        }
        return getStatus();
    }

    function getStatus() {
        return {
            feature_id: Runtime.feature_id,
            enabled: Runtime.enabled,
            initialized: Runtime.initialized,
            module_found: Runtime.module !== null,
            multiplier: Runtime.config.multiplier,
            skip_local_victim: Runtime.config.skip_local_victim,
            include_infect: Runtime.config.include_infect,
            allow_other_damage_type: Runtime.config.allow_other_damage_type,
            enable_owner_mapping: Runtime.config.enable_owner_mapping,
            diagnostic_log: Runtime.config.diagnostic_log,
            total_hurt_events: Runtime.stats.totalHurtEvents,
            entity_hurt_events: Runtime.stats.entityHurtEvents,
            player_hurt_events: Runtime.stats.playerHurtEvents,
            multiplied_events: Runtime.stats.multipliedEvents,
            skipped_disabled: Runtime.stats.skippedDisabled,
            skipped_player_base_depth: Runtime.stats.skippedPlayerBaseDepth,
            skipped_invalid_event: Runtime.stats.skippedInvalidEvent,
            skipped_invalid_damage: Runtime.stats.skippedInvalidDamage,
            skipped_damage_type: Runtime.stats.skippedDamageType,
            skipped_infect: Runtime.stats.skippedInfect,
            skipped_not_local_attacker: Runtime.stats.skippedNotLocalAttacker,
            skipped_local_victim: Runtime.stats.skippedLocalVictim,
            missile_owner_hits: Runtime.stats.missileOwnerHits,
            sentry_owner_hits: Runtime.stats.sentryOwnerHits,
            missile_owner_records: Runtime.stats.missileOwnerRecords,
            sentry_owner_records: Runtime.stats.sentryOwnerRecords,
            error_count: Runtime.stats.errorCount,
            cleanup_count: Runtime.stats.cleanupCount,
            last_original_damage: Runtime.stats.lastOriginalDamage,
            last_new_damage: Runtime.stats.lastNewDamage,
            last_damage_type: Runtime.stats.lastDamageType,
            last_damage_tag: Runtime.stats.lastDamageTag,
            last_wpn_index: Runtime.stats.lastWpnIndex,
            last_wpn_spr_index: Runtime.stats.lastWpnSprIndex,
            last_ignore_dmg_rate: Runtime.stats.lastIgnoreDmgRate,
            last_source: Runtime.stats.lastSource,
            last_decision: Runtime.stats.lastDecision,
            last_error: Runtime.stats.lastError
        };
    }

    rpc.exports = {
        enable: function (config) {
            updateConfig(config);
            return enableFeature();
        },
        disable: function () {
            return disableFeature();
        },
        status: function () {
            if (!Runtime.module) findGameAssembly();
            return getStatus();
        },
        cleanup: function (payload) {
            return cleanupFeature();
        },
        setConfig: function (config) {
            return updateConfig(config);
        },
        set_config: function (config) {
            return updateConfig(config);
        },
        setconfig: function (config) {
            return updateConfig(config);
        }
    };
})();
