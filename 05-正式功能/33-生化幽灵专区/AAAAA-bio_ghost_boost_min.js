// Bio Ghost Boost v1 - 33 single-feature build
// Scope: local player only, and only while the local player is a biochemical ghost.
(function () {
    'use strict';

    var MODULE_NAME = 'GameAssembly.dll';
    var CALL_CONV = 'mscdecl';

    var DamageType = {
        Infect: 4
    };

    var RVA = {
        Entity_OnEntityHurt: 0x00B3F470,
        Player_OnEntityHurt: 0x00B516B0,
        Player_get_isMyPlayer: 0x00B55FD0,
        PropertyModifier_Get: 0x00B17590,
        PlayerWeapons_get_KnifeSpeed: 0x00B170A0,
        WPN_Knife_GetKnifeAttackData: 0x00B63EC0,
        Player_Update: 0x00B551D0,
        Player_OnDestroy: 0x00B511C0,
        GameManager_OnDestroy: 0x00AEBD40,
        Skill_EndCold: 0x00AE1BC0
    };

    var OFF = {
        Entity_isGhostEntity: 0x30,
        Entity_isNoHitFeedback: 0x31,
        Player_Modifier_MoveSpeedRatio: 0x8C,
        Player_velData: 0x90,
        Player_skills: 0xB0,
        PlayerWeapons_owner: 0x08,
        PlayerVelocity_velocity: 0x0C,
        PlayerSkills_all: 0x08,
        Skill_coldFinishTime: 0x1C,
        Skill_coldTime: 0x24,
        Damage_attacker: 0x00,
        Damage_victim: 0x04,
        Damage_damage: 0x08,
        Damage_type: 0x34,
        KnifeAttackData_range: 0x04
    };

    var Runtime = {
        feature_id: '33_bio_ghost_boost',
        enabled: false,
        initialized: false,
        module: null,
        base: ptr(0),
        attachHooks: [],
        replaceAddrs: [],
        localPlayerPtr: ptr(0),
        playerHurtDepth: 0,
        lastSkillTick: 0,
        config: {
            damage_taken_multiplier: 0.5,
            attack_damage_multiplier: 1.5,
            move_speed_multiplier: 1.4,
            knife_speed_multiplier: 1.5,
            knife_range_multiplier: 1.4,
            skill_no_cooldown: true,
            knockback_multiplier: 0.5,
            include_infect_damage: false,
            use_no_hit_feedback_when_zero_knockback: true,
            diagnostic_log: true
        },
        stats: {
            damageEvents: 0,
            damageChanged: 0,
            moveChanged: 0,
            knifeSpeedChanged: 0,
            knifeRangeChanged: 0,
            skillColdEnded: 0,
            knockbackChanged: 0,
            localGhostHits: 0,
            localPlayerSeen: 0,
            localGhostSeen: 0,
            lastIsGhostValue: false,
            errors: 0,
            lastDecision: '',
            lastError: ''
        }
    };

    var native = {
        ready: false,
        isMyPlayer: null,
        originalPropertyModifierGet: null,
        originalKnifeSpeed: null,
        endCold: null
    };

    var LogLimiter = {};

    function log(level, message) {
        try {
            send({ type: 'log', level: level, module: Runtime.feature_id, message: message });
        } catch (_) {}
    }

    function logLimited(key, level, message, waitMs) {
        var now = Date.now();
        var wait = waitMs || 1000;
        if (!LogLimiter[key] || now - LogLimiter[key] >= wait) {
            LogLimiter[key] = now;
            log(level, message);
        }
    }

    function sendStatus(enabled) {
        try { send({ type: 'status', feature: Runtime.feature_id, enabled: enabled }); } catch (_) {}
    }

    function setError(label, error) {
        Runtime.stats.errors += 1;
        Runtime.stats.lastError = label + (error && error.message ? ': ' + error.message : '');
        logLimited('error:' + label, 'error', Runtime.stats.lastError, 1500);
    }

    function isNull(p) {
        if (p === null || p === undefined) return true;
        try { return p.isNull(); } catch (_) { return true; }
    }

    function readPtr(addr) {
        try {
            if (!addr || addr.isNull()) return ptr(0);
            var value = addr.readPointer();
            return value && !value.isNull() ? value : ptr(0);
        } catch (_) {
            return ptr(0);
        }
    }

    function readU8(addr) {
        try { return addr.readU8(); } catch (_) { return 0; }
    }

    function writeU8(addr, value) {
        try { addr.writeU8(value ? 1 : 0); return true; } catch (_) { return false; }
    }

    function readF32(addr) {
        try { return addr.readFloat(); } catch (_) { return NaN; }
    }

    function writeF32(addr, value) {
        try { addr.writeFloat(value); return true; } catch (_) { return false; }
    }

    function clampFloat(value, minValue, maxValue) {
        var n = Number(value);
        if (!isFinite(n)) return minValue;
        if (n < minValue) return minValue;
        if (n > maxValue) return maxValue;
        return n;
    }

    function isReadableObject(p) {
        try {
            if (isNull(p)) return false;
            var klass = p.readPointer();
            return !isNull(klass);
        } catch (_) {
            return false;
        }
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
        if (!findGameAssembly()) return false;

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
            native.originalPropertyModifierGet = new NativeFunction(
                Runtime.base.add(RVA.PropertyModifier_Get),
                'float',
                ['pointer', 'pointer']
            );
            native.originalKnifeSpeed = new NativeFunction(
                Runtime.base.add(RVA.PlayerWeapons_get_KnifeSpeed),
                'float',
                ['pointer']
            );
            native.endCold = new NativeFunction(
                Runtime.base.add(RVA.Skill_EndCold),
                'void',
                ['pointer']
            );
            native.ready = true;
            return true;
        } catch (error) {
            setError('initNativeFunctions failed', error);
            native.ready = false;
            return false;
        }
    }

    function isLocalPlayer(playerPtr) {
        if (isNull(playerPtr) || !isReadableObject(playerPtr)) return false;
        if (!isNull(Runtime.localPlayerPtr) && Runtime.localPlayerPtr.equals(playerPtr)) return true;
        if (!native.ready && !initNativeFunctions()) return false;
        try {
            var result = !!native.isMyPlayer(playerPtr, ptr(0));
            if (result) rememberLocalPlayer(playerPtr);
            return result;
        } catch (error) {
            setError('Player.get_isMyPlayer failed', error);
            return false;
        }
    }

    function rememberLocalPlayer(playerPtr) {
        if (isNull(playerPtr)) return;
        if (!isNull(Runtime.localPlayerPtr) && Runtime.localPlayerPtr.equals(playerPtr)) return;
        Runtime.localPlayerPtr = playerPtr;
        Runtime.stats.localPlayerSeen += 1;
        logLimited('local_player_seen', 'info', 'local player captured: ' + playerPtr, 1000);
    }

    function isGhostEntity(entityPtr) {
        if (isNull(entityPtr) || !isReadableObject(entityPtr)) return false;
        return readU8(entityPtr.add(OFF.Entity_isGhostEntity)) !== 0;
    }

    function isLocalGhostPlayer(playerPtr) {
        if (!isLocalPlayer(playerPtr)) return false;
        var isGhost = isGhostEntity(playerPtr);
        Runtime.stats.lastIsGhostValue = isGhost;
        if (isGhost) Runtime.stats.localGhostSeen += 1;
        return isGhost;
    }

    function readDamageEvent(eventPtr) {
        try {
            if (isNull(eventPtr)) return null;
            return {
                attacker: readPtr(eventPtr.add(OFF.Damage_attacker)),
                victim: readPtr(eventPtr.add(OFF.Damage_victim)),
                damage: eventPtr.add(OFF.Damage_damage).readFloat(),
                type: eventPtr.add(OFF.Damage_type).readS32()
            };
        } catch (error) {
            setError('readDamageEvent failed', error);
            return null;
        }
    }

    function eventDataFromOnEntityHurtStack(context) {
        return context.esp.add(8);
    }

    function applyDamagePolicy(eventPtr, source) {
        Runtime.stats.damageEvents += 1;
        if (!Runtime.enabled) return false;

        var data = readDamageEvent(eventPtr);
        if (!data || !isFinite(data.damage) || data.damage <= 0) {
            Runtime.stats.lastDecision = 'skip_invalid_damage';
            return false;
        }

        if (data.type === DamageType.Infect && !Runtime.config.include_infect_damage) {
            Runtime.stats.lastDecision = 'skip_infect';
            return false;
        }

        var newDamage = data.damage;
        var changed = false;
        var attackerIsLocalGhost = isLocalGhostPlayer(data.attacker);
        var victimIsLocalGhost = isLocalGhostPlayer(data.victim);

        if (attackerIsLocalGhost) {
            newDamage *= clampFloat(Runtime.config.attack_damage_multiplier, 0.1, 10.0);
            changed = true;
        }

        if (victimIsLocalGhost) {
            newDamage *= clampFloat(Runtime.config.damage_taken_multiplier, 0.1, 3.0);
            changed = true;
        }

        if (!changed) {
            Runtime.stats.lastDecision = 'skip_not_local_ghost';
            return false;
        }

        newDamage = clampFloat(newDamage, 0.0, 999999.0);
        try {
            eventPtr.add(OFF.Damage_damage).writeFloat(newDamage);
            Runtime.stats.damageChanged += 1;
            Runtime.stats.lastDecision = source + ': damage ' + data.damage.toFixed(2) + ' -> ' + newDamage.toFixed(2);
            if (Runtime.config.diagnostic_log) logLimited('damage', 'info', Runtime.stats.lastDecision, 500);
            return true;
        } catch (error) {
            setError('write damage failed', error);
            return false;
        }
    }

    function readVec3(addr) {
        try {
            return {
                x: addr.readFloat(),
                y: addr.add(4).readFloat(),
                z: addr.add(8).readFloat()
            };
        } catch (_) {
            return null;
        }
    }

    function writeVec3(addr, vec) {
        try {
            addr.writeFloat(vec.x);
            addr.add(4).writeFloat(vec.y);
            addr.add(8).writeFloat(vec.z);
            return true;
        } catch (_) {
            return false;
        }
    }

    function captureKnockbackState(eventPtr) {
        if (!Runtime.enabled) return null;
        var data = readDamageEvent(eventPtr);
        if (!data || !isLocalGhostPlayer(data.victim)) return null;

        var velData = readPtr(data.victim.add(OFF.Player_velData));
        if (isNull(velData)) return null;

        var velocityAddr = velData.add(OFF.PlayerVelocity_velocity);
        var before = readVec3(velocityAddr);
        if (!before) return null;

        var state = {
            victim: data.victim,
            velocityAddr: velocityAddr,
            before: before,
            changedNoHitFeedback: false,
            oldNoHitFeedback: readU8(data.victim.add(OFF.Entity_isNoHitFeedback))
        };

        var multiplier = clampFloat(Runtime.config.knockback_multiplier, 0.0, 3.0);
        if (multiplier <= 0.01 && Runtime.config.use_no_hit_feedback_when_zero_knockback) {
            state.changedNoHitFeedback = writeU8(data.victim.add(OFF.Entity_isNoHitFeedback), 1);
        }

        Runtime.stats.localGhostHits += 1;
        return state;
    }

    function scaleKnockbackVelocity(state) {
        if (!state || !state.velocityAddr || !state.before) return false;

        var multiplier = clampFloat(Runtime.config.knockback_multiplier, 0.0, 3.0);
        var after = readVec3(state.velocityAddr);
        if (!after) return false;

        var scaled = {
            x: state.before.x + (after.x - state.before.x) * multiplier,
            y: state.before.y + (after.y - state.before.y) * multiplier,
            z: state.before.z + (after.z - state.before.z) * multiplier
        };

        if (!writeVec3(state.velocityAddr, scaled)) return false;
        Runtime.stats.knockbackChanged += 1;
        if (Runtime.config.diagnostic_log) {
            logLimited('knockback', 'info', 'knockback velocity scaled to ' + multiplier.toFixed(1) + 'x', 800);
        }
        return true;
    }

    function finishKnockbackState(state) {
        if (!state) return;
        try {
            scaleKnockbackVelocity(state);
        } catch (error) {
            setError('scaleKnockbackVelocity failed', error);
        }
        if (state.changedNoHitFeedback && !isNull(state.victim)) {
            writeU8(state.victim.add(OFF.Entity_isNoHitFeedback), state.oldNoHitFeedback);
        }
    }

    function scanAndEndCold(playerPtr) {
        if (!Runtime.enabled || !Runtime.config.skill_no_cooldown || !native.endCold) return;
        if (!isLocalGhostPlayer(playerPtr)) return;

        var playerSkills = readPtr(playerPtr.add(OFF.Player_skills));
        if (isNull(playerSkills)) return;

        var skillArray = readPtr(playerSkills.add(OFF.PlayerSkills_all));
        if (isNull(skillArray)) return;

        var length = 0;
        try { length = skillArray.add(0x0C).readS32(); } catch (_) { return; }
        if (!length || length <= 0 || length > 20) return;

        for (var i = 0; i < length; i++) {
            var skill = readPtr(skillArray.add(0x10 + 4 * i));
            if (isNull(skill) || !isReadableObject(skill)) continue;

            var coldFinish = readF32(skill.add(OFF.Skill_coldFinishTime));
            var coldTime = readF32(skill.add(OFF.Skill_coldTime));
            if (!isFinite(coldFinish) || !isFinite(coldTime)) continue;

            try {
                native.endCold(skill);
                Runtime.stats.skillColdEnded += 1;
            } catch (_) {}
        }
    }

    function attachHook(name, rva, callbacks) {
        var hook = Interceptor.attach(Runtime.base.add(rva), callbacks);
        Runtime.attachHooks.push({ name: name, hook: hook });
    }

    function replaceHook(name, rva, callback, returnType, argTypes) {
        var addr = Runtime.base.add(rva);
        Interceptor.replace(addr, new NativeCallback(callback, returnType, argTypes));
        Runtime.replaceAddrs.push({ name: name, addr: addr });
    }

    function captureLocalPlayerHook() {
        attachHook('Player.get_isMyPlayer captureLocalPlayerHook', RVA.Player_get_isMyPlayer, {
            onEnter: function (args) {
                this.playerPtr = args[0];
            },
            onLeave: function (retval) {
                try {
                    if ((retval.toUInt32() & 0xFF) === 0) return;
                    rememberLocalPlayer(this.playerPtr);
                } catch (error) {
                    setError('captureLocalPlayerHook failed', error);
                }
            }
        });
    }

    function installHooks() {
        captureLocalPlayerHook();

        attachHook('Player.OnEntityHurt', RVA.Player_OnEntityHurt, {
            onEnter: function () {
                Runtime.playerHurtDepth += 1;
                this.depthEntered = true;
                try {
                    var eventPtr = eventDataFromOnEntityHurtStack(this.context);
                    this.knockbackState = captureKnockbackState(eventPtr);
                    applyDamagePolicy(eventPtr, 'Player.OnEntityHurt');
                } catch (error) {
                    setError('Player.OnEntityHurt failed', error);
                }
            },
            onLeave: function () {
                finishKnockbackState(this.knockbackState);
                if (this.depthEntered) Runtime.playerHurtDepth = Math.max(0, Runtime.playerHurtDepth - 1);
            }
        });

        attachHook('Entity.OnEntityHurt', RVA.Entity_OnEntityHurt, {
            onEnter: function () {
                if (Runtime.playerHurtDepth > 0) return;
                try {
                    applyDamagePolicy(eventDataFromOnEntityHurtStack(this.context), 'Entity.OnEntityHurt');
                } catch (error) {
                    setError('Entity.OnEntityHurt failed', error);
                }
            }
        });

        replaceHook('PropertyModifier.Get', RVA.PropertyModifier_Get, function (self, player) {
            var result = native.originalPropertyModifierGet(self, player);
            try {
                if (!Runtime.enabled || isNull(player) || !isLocalGhostPlayer(player)) return result;
                var moveMod = readPtr(player.add(OFF.Player_Modifier_MoveSpeedRatio));
                if (isNull(moveMod) || !self.equals(moveMod)) return result;

                var multiplier = clampFloat(Runtime.config.move_speed_multiplier, 0.5, 4.0);
                Runtime.stats.moveChanged += 1;
                return clampFloat(result * multiplier, 0.05, 20.0);
            } catch (error) {
                setError('PropertyModifier.Get callback failed', error);
                return result;
            }
        }, 'float', ['pointer', 'pointer']);

        replaceHook('PlayerWeapons.get_KnifeSpeed', RVA.PlayerWeapons_get_KnifeSpeed, function (self) {
            var result = native.originalKnifeSpeed(self);
            try {
                if (!Runtime.enabled || isNull(self)) return result;
                var owner = readPtr(self.add(OFF.PlayerWeapons_owner));
                if (!isLocalGhostPlayer(owner)) return result;

                var multiplier = clampFloat(Runtime.config.knife_speed_multiplier, 0.5, 6.0);
                Runtime.stats.knifeSpeedChanged += 1;
                return clampFloat(result * multiplier, 0.05, 30.0);
            } catch (error) {
                setError('get_KnifeSpeed callback failed', error);
                return result;
            }
        }, 'float', ['pointer']);

        attachHook('WPN_Knife.GetKnifeAttackData', RVA.WPN_Knife_GetKnifeAttackData, {
            onEnter: function (args) {
                try {
                    this.wpnSelf = args[1];
                    this.owner = readPtr(args[1].add(0x30));
                } catch (_) {
                    this.owner = ptr(0);
                }
            },
            onLeave: function (retval) {
                if (!Runtime.enabled || !isLocalGhostPlayer(this.owner)) return;
                try {
                    var rangeAddr = retval.add(OFF.KnifeAttackData_range);
                    var originalRange = rangeAddr.readFloat();
                    if (!isFinite(originalRange) || originalRange <= 0.1 || originalRange > 500.0) return;

                    var multiplier = clampFloat(Runtime.config.knife_range_multiplier, 0.5, 5.0);
                    rangeAddr.writeFloat(originalRange * multiplier);
                    Runtime.stats.knifeRangeChanged += 1;
                } catch (error) {
                    setError('GetKnifeAttackData callback failed', error);
                }
            }
        });

        attachHook('Player.Update', RVA.Player_Update, {
            onEnter: function (args) {
                if (!Runtime.enabled || !Runtime.config.skill_no_cooldown) return;
                var now = Date.now();
                if (now - Runtime.lastSkillTick < 200) return;
                Runtime.lastSkillTick = now;
                scanAndEndCold(args[0]);
            }
        });

        attachHook('Player.OnDestroy', RVA.Player_OnDestroy, {
            onEnter: function () {
                Runtime.lastSkillTick = 0;
            }
        });

        attachHook('GameManager.OnDestroy', RVA.GameManager_OnDestroy, {
            onEnter: function () {
                Runtime.playerHurtDepth = 0;
                Runtime.lastSkillTick = 0;
            }
        });
    }

    function cleanupHooks() {
        for (var i = 0; i < Runtime.attachHooks.length; i++) {
            try { Runtime.attachHooks[i].hook.detach(); } catch (_) {}
        }
        Runtime.attachHooks = [];

        for (var j = Runtime.replaceAddrs.length - 1; j >= 0; j--) {
            try { Interceptor.revert(Runtime.replaceAddrs[j].addr); } catch (_) {}
        }
        Runtime.replaceAddrs = [];
        Runtime.initialized = false;
        Runtime.localPlayerPtr = ptr(0);
        native.ready = false;
        native.isMyPlayer = null;
        native.originalPropertyModifierGet = null;
        native.originalKnifeSpeed = null;
        native.endCold = null;
    }

    function initializeFeature() {
        if (Runtime.initialized) return true;
        if (!initNativeFunctions()) return false;
        try {
            installHooks();
            Runtime.initialized = true;
            return true;
        } catch (error) {
            setError('installHooks failed', error);
            cleanupHooks();
            return false;
        }
    }

    function updateConfig(config) {
        config = config || {};
        if (config.damage_taken_multiplier !== undefined) Runtime.config.damage_taken_multiplier = clampFloat(config.damage_taken_multiplier, 0.1, 3.0);
        if (config.attack_damage_multiplier !== undefined) Runtime.config.attack_damage_multiplier = clampFloat(config.attack_damage_multiplier, 0.1, 10.0);
        if (config.move_speed_multiplier !== undefined) Runtime.config.move_speed_multiplier = clampFloat(config.move_speed_multiplier, 0.5, 4.0);
        if (config.knife_speed_multiplier !== undefined) Runtime.config.knife_speed_multiplier = clampFloat(config.knife_speed_multiplier, 0.5, 6.0);
        if (config.knife_range_multiplier !== undefined) Runtime.config.knife_range_multiplier = clampFloat(config.knife_range_multiplier, 0.5, 5.0);
        if (config.knockback_multiplier !== undefined) Runtime.config.knockback_multiplier = clampFloat(config.knockback_multiplier, 0.0, 3.0);
        if (config.skill_no_cooldown !== undefined) Runtime.config.skill_no_cooldown = !!config.skill_no_cooldown;
        if (config.include_infect_damage !== undefined) Runtime.config.include_infect_damage = !!config.include_infect_damage;
        if (config.use_no_hit_feedback_when_zero_knockback !== undefined) Runtime.config.use_no_hit_feedback_when_zero_knockback = !!config.use_no_hit_feedback_when_zero_knockback;
        if (config.diagnostic_log !== undefined) Runtime.config.diagnostic_log = !!config.diagnostic_log;
        return getStatus();
    }

    function enableFeature(config) {
        updateConfig(config);
        if (!initializeFeature()) return getStatus();
        Runtime.enabled = true;
        sendStatus(true);
        log('success', 'bio ghost boost enabled');
        return getStatus();
    }

    function disableFeature() {
        Runtime.enabled = false;
        cleanupHooks();
        sendStatus(false);
        log('info', 'bio ghost boost disabled');
        return getStatus();
    }

    function cleanupFeature() {
        Runtime.enabled = false;
        cleanupHooks();
        Runtime.playerHurtDepth = 0;
        Runtime.lastSkillTick = 0;
        sendStatus(false);
        return getStatus();
    }

    function getStatus() {
        if (!Runtime.module) findGameAssembly();
        return {
            feature_id: Runtime.feature_id,
            enabled: Runtime.enabled,
            initialized: Runtime.initialized,
            module_found: Runtime.module !== null,
            hook_count: Runtime.attachHooks.length + Runtime.replaceAddrs.length,
            config: Runtime.config,
            damage_events: Runtime.stats.damageEvents,
            damage_changed: Runtime.stats.damageChanged,
            move_changed: Runtime.stats.moveChanged,
            knife_speed_changed: Runtime.stats.knifeSpeedChanged,
            knife_range_changed: Runtime.stats.knifeRangeChanged,
            skill_cold_ended: Runtime.stats.skillColdEnded,
            knockback_changed: Runtime.stats.knockbackChanged,
            local_ghost_hits: Runtime.stats.localGhostHits,
            local_player_seen: Runtime.stats.localPlayerSeen,
            local_ghost_seen: Runtime.stats.localGhostSeen,
            last_is_ghost_value: Runtime.stats.lastIsGhostValue,
            errors: Runtime.stats.errors,
            last_decision: Runtime.stats.lastDecision,
            last_error: Runtime.stats.lastError
        };
    }

    rpc.exports = {
        enable: function (config) {
            return enableFeature(config || {});
        },
        disable: function () {
            return disableFeature();
        },
        setConfig: function (config) {
            return updateConfig(config || {});
        },
        set_config: function (config) {
            return updateConfig(config || {});
        },
        setconfig: function (config) {
            return updateConfig(config || {});
        },
        status: function () {
            return getStatus();
        },
        cleanup: function () {
            return cleanupFeature();
        }
    };
})();
