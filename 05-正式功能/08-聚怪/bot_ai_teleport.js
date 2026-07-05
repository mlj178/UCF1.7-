// ============================================================
// bot_ai_teleport.js
// feature_id: bot_ai_teleport
// 功能: BOT 聚怪 / BOT AI Teleport 测试版
//
// 核心原则:
// 1) Hook Bot.Update 只负责收集 Bot 与 Bot.thisPlayer(+0x24) 映射。
// 2) 真正瞬移优先走 Pathfinding.RichAI/AIBase.Teleport(pos, true)。
// 3) Teleport 失败时才使用 Player/Bot Transform + CharacterController 兜底。
// 4) 不高频硬刷位置；RPC teleport() 只提交一次任务，任务在 Player.Update 主线程链路执行。
// 5) 按单功能生命周期规范实现 enable / disable / status / cleanup / setConfig。
//
// 重要 RVA / 字段：
// - Bot.Update:                    0x00B33370
// - Bot.thisPlayer:                0x24
// - RichAI.Teleport:               0x00460480
// - RichAI.SearchPath:             0x00460450
// - AIBase.Teleport:               0x00436720
// - AIBase.SearchPath:             0x00436290
// - AIBase.CancelCurrentPathRequest:0x00434A80
// - Bot.UpdateNearestGraphNode:    0x00B33260
// - Bot.PathSetting:               0x00B31E90
// ============================================================

(function () {
    'use strict';

    const FEATURE_ID = 'bot_ai_teleport';
    const NULL = ptr(0);
    const ABI = 'mscdecl'; // Unity 2020 / IL2CPP / Windows x86
    const Vec3 = ['float', 'float', 'float'];

    const Runtime = {
        feature_id: FEATURE_ID,
        enabled: false,
        initialized: false,
        generation: 0,
        hooks: [],
        timers: [],
        config: {
            target: { x: 13.6, y: 14.1, z: 0.1 },
            batchSize: 64,
            processAllOnRpc: true,
            syncBotPathFields: true,
            aiFirst: true,
            useRichAI: true,
            useAIBase: true,
            useIAstarAIProbe: true,
            callSearchPath: true,
            callBotRefresh: true,
            transformFallback: true,
            groundToNearestNode: true,
            // v5: 只用 GraphNode 修正 Y，X/Z 保留每个 Bot 的分散偏移，避免 29 个 Bot 完全重叠。
            useGraphNodeXZ: false,
            graphYOffset: 0.05,
            writeNativeTransformCache: false,
            positionDebug: true,
            // v5: 分散聚怪，减少 CharacterController 互相顶高。
            spreadCluster: true,
            clusterSpacing: 0.75,
            clusterMaxRadius: 4.2,
            // v5: 默认不立刻 PathSetting，先避免 Bot 重新寻路把自己拉走/拉高。
            pathSettingAfterTeleport: false,
            // v5: 传送后延迟检查高度，超过阈值自动二次贴地一次。
            verifyAfterMs: 600,
            airborneThreshold: 1.8,
            restickAirborne: true,
            maxRegroundPerBot: 1,
            // v6: 每秒输出 Bot/Player/路径/GraphNode/跳跃状态，专门分析飞天原因。
            monitorEnabled: true,
            monitorIntervalMs: 1000,
            monitorMaxBots: 64,
            monitorDetail: true,
            driftThreshold: 2.0,
            // v8: 自动做 pre/post/delayed 状态差分，找出 teleport 后到底哪些字段被游戏改回。
            diagEnabled: true,
            diagMaxBots: 64,
            diagDetailLimit: 64,
            executeOnPlayerUpdate: true,
            debug: false,
            logIntervalMs: 1200
        },
        module: null,
        base: NULL,
        funcs: {},
        il2cpp: {},
        types: {},
        cache: {
            gm: NULL,
            mm: NULL,
            trackedBots: {},
            trackedPlayers: {},
            pendingTeleport: false,
            pendingReason: '',
            lastPlayerUpdateTs: 0,
            lastMonitorTs: 0,
            lastTeleportSeq: 0,
            diagSnapshots: {}
        },
        originals: {},
        stats: {
            hookHits: 0,
            botUpdateHits: 0,
            playerUpdateHits: 0,
            botsTracked: 0,
            playersTracked: 0,
            teleportRequests: 0,
            teleportRuns: 0,
            aiTeleportOk: 0,
            richAiOk: 0,
            aiBaseOk: 0,
            fallbackOk: 0,
            skippedSelf: 0,
            skippedHuman: 0,
            skippedDead: 0,
            skippedInvalid: 0,
            skippedNoAi: 0,
            failed: 0,
            invalidPurged: 0,
            airborneReground: 0,
            monitorTicks: 0,
            highObserved: 0,
            driftObserved: 0,
            diagRuns: 0,
            diagPathRecreated: 0,
            diagNextPosChanged: 0,
            diagMovedFromFinal: 0,
            errorCount: 0,
            cleanupCount: 0,
            lastError: '',
            lastResetReason: '',
            lastSummary: ''
        }
    };

    const R = {
        GM_AddP: 0x00AF9A90,
        MM_MapGun: 0x00AEBB70,
        P_Update: 0x00B551D0,
        P_isMy: 0x00B55FD0,
        E_isDead: 0x00B400E0,
        E_getCC: 0x001CF180,
        C_setEn: 0x00AB86B0,
        Component_get_transform: 0x0032CF40,
        Component_get_gameObject: 0x0032CEB0,
        Component_GetComponent_Type: 0x0032CD50,
        GameObject_GetComponent_Type: 0x00331C10,
        Transform_set_position_Injected: 0x003F4810,
        Transform_get_position_Injected: 0x003F4280,
        Bot_Update: 0x00B33370,
        Bot_UpdateNearestGraphNode: 0x00B33260,
        Bot_PathSetting: 0x00B31E90,
        RichAI_Teleport: 0x00460480,
        RichAI_SearchPath: 0x00460450,
        AIBase_CancelCurrentPathRequest: 0x00434A80,
        AIBase_SetPath: 0x00436380,
        AIBase_SearchPath: 0x00436290,
        AIBase_Teleport: 0x00436720
    };

    const TYPEINFO_RVA = {
        RichAI: 0x00E2FDB4,
        AIBase: 0x00E249C8,
        IAstarAI: 0x00E29EE8
    };

    const O = {
        GM_allPlayers: 0x1C,
        P_cameraManager: 0x48,
        P_charContainer: 0x58,
        P_clientData: 0x94,
        CD_team: 0x18,
        CD_isBot: 0x1C,
        Bot_thisPlayer: 0x24,
        Bot_seeker: 0x78,
        Bot_path: 0x80,
        Bot_pathLength: 0x84,
        Bot_gNode_Nearset: 0x88,
        Bot_gNode_Next: 0x8C,
        Bot_nextPathVectorID: 0x90,
        Bot_lastStartPoint: 0x94,
        Bot_nextPathPos: 0xA0,
        Bot_dirToNextNode: 0xAC,
        Bot_nextFindPathTime: 0xB8,
        Bot_interpolator: 0xBC,
        Bot_Destination_Listener: 0xC0,
        Bot_nextJumpStartNode: 0xC8,
        Bot_nextJumpLink: 0xCC,
        Bot_nextJumpTime: 0xE8,
        Bot_blockedTime: 0xEC,
        Bot_crouchEndTime: 0xF0,
        AIBase_simulatedPosition: 0x40,
        AIBase_velocity2D: 0x68,
        AIBase_verticalVelocity: 0x70,
        AIBase_seeker: 0x74,
        AIBase_tr: 0x78,
        AIBase_controller: 0x84,
        AIBase_destination: 0xCC,
        AIBase_isStopped: 0xD8
    };

    const logLimiter = {};
    const posBuf = Memory.alloc(16);

    function nowMs() { return Date.now(); }

    function log(msg) {
        console.log('[' + FEATURE_ID + '] ' + msg);
    }

    function warn(msg) {
        console.warn('[' + FEATURE_ID + '] ' + msg);
    }

    function err(msg) {
        console.error('[' + FEATURE_ID + '] ' + msg);
    }

    function logOnce(key, msg, intervalMs) {
        const iv = intervalMs || Runtime.config.logIntervalMs || 1000;
        const n = nowMs();
        if (!logLimiter[key] || n - logLimiter[key] >= iv) {
            log(msg);
            logLimiter[key] = n;
        }
    }

    function recordError(where, e) {
        Runtime.stats.errorCount++;
        Runtime.stats.lastError = where + ': ' + (e && e.message ? e.message : String(e));
        logOnce('err:' + where, 'ERROR ' + Runtime.stats.lastError, 1500);
        if (Runtime.stats.errorCount >= 12) {
            Runtime.enabled = false;
            resetRuntime('too_many_errors');
            warn('disabled because too many errors');
        }
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

    function safeReadPointer(base, offset) {
        try {
            if (!isReadablePtr(base)) return NULL;
            const p = base.add(offset).readPointer();
            if (!p || p.isNull()) return NULL;
            return p;
        } catch (e) {
            Runtime.stats.skippedInvalid++;
            return NULL;
        }
    }

    function safeReadU8(base, offset, defVal) {
        try {
            if (!isReadablePtr(base)) return defVal;
            return base.add(offset).readU8();
        } catch (e) {
            return defVal;
        }
    }

    function safeReadS32(base, offset, defVal) {
        try {
            if (!isReadablePtr(base)) return defVal;
            return base.add(offset).readS32();
        } catch (e) {
            return defVal;
        }
    }

    function safeWritePointer(base, offset, value) {
        try {
            if (!isReadablePtr(base)) return false;
            base.add(offset).writePointer(value || NULL);
            return true;
        } catch (e) {
            Runtime.stats.skippedInvalid++;
            return false;
        }
    }

    function safeWriteS32(base, offset, value) {
        try {
            if (!isReadablePtr(base)) return false;
            base.add(offset).writeS32(value | 0);
            return true;
        } catch (e) {
            Runtime.stats.skippedInvalid++;
            return false;
        }
    }

    function safeWriteFloat(base, offset, value) {
        try {
            if (!isReadablePtr(base)) return false;
            base.add(offset).writeFloat(Number(value) || 0);
            return true;
        } catch (e) {
            Runtime.stats.skippedInvalid++;
            return false;
        }
    }

    function safeWriteVec3Field(base, offset, v) {
        try {
            if (!isReadablePtr(base)) return false;
            base.add(offset).writeFloat(Number(v.x) || 0);
            base.add(offset + 4).writeFloat(Number(v.y) || 0);
            base.add(offset + 8).writeFloat(Number(v.z) || 0);
            return true;
        } catch (e) {
            Runtime.stats.skippedInvalid++;
            return false;
        }
    }

    function vec3Zero() {
        return { x: 0, y: 0, z: 0 };
    }

    function vec3ToString(v) {
        if (!v) return '(null)';
        if (!isFinite(Number(v.x)) || !isFinite(Number(v.y)) || !isFinite(Number(v.z))) return '(bad)';
        return '(' + Number(v.x).toFixed(2) + ',' + Number(v.y).toFixed(2) + ',' + Number(v.z).toFixed(2) + ')';
    }

    function sameVec3(a, b) {
        if (!a || !b) return false;
        return Math.abs(Number(a.x) - Number(b.x)) < 0.001 &&
               Math.abs(Number(a.y) - Number(b.y)) < 0.001 &&
               Math.abs(Number(a.z) - Number(b.z)) < 0.001;
    }

    function readVec3(buf) {
        try {
            return { x: buf.readFloat(), y: buf.add(4).readFloat(), z: buf.add(8).readFloat() };
        } catch (e) {
            return null;
        }
    }

    function graphNodeToVec3(node) {
        // Pathfinding.GraphNode.position 是 Int3，offset 0x14，精度 1000。
        try {
            if (!isReadablePtr(node)) return null;
            const ix = node.add(0x14).readS32();
            const iy = node.add(0x18).readS32();
            const iz = node.add(0x1C).readS32();
            if (Math.abs(ix) > 100000000 || Math.abs(iy) > 100000000 || Math.abs(iz) > 100000000) return null;
            return { x: ix * 0.001, y: iy * 0.001, z: iz * 0.001 };
        } catch (e) {
            return null;
        }
    }

    function safeReadFloat(base, offset, defVal) {
        try {
            if (!isReadablePtr(base)) return defVal;
            const v = base.add(offset).readFloat();
            return isFinite(v) ? v : defVal;
        } catch (e) {
            return defVal;
        }
    }

    function safeReadVec3Field(base, offset) {
        try {
            if (!isReadablePtr(base)) return null;
            const x = base.add(offset).readFloat();
            const y = base.add(offset + 4).readFloat();
            const z = base.add(offset + 8).readFloat();
            if (!isFinite(x) || !isFinite(y) || !isFinite(z)) return null;
            return { x: x, y: y, z: z };
        } catch (e) {
            return null;
        }
    }

    function vec3DistanceXZ(a, b) {
        if (!a || !b) return NaN;
        const dx = Number(a.x) - Number(b.x);
        const dz = Number(a.z) - Number(b.z);
        return Math.sqrt(dx * dx + dz * dz);
    }

    function vec3DistanceY(a, b) {
        if (!a || !b) return NaN;
        return Number(a.y) - Number(b.y);
    }

    function fmtNum(v) {
        if (!isFinite(Number(v))) return 'nan';
        return Number(v).toFixed(2);
    }

    function classifyBotState(entry, botPos, playerPos, finalTarget, gNearPos, gNextPos, pathPtr, nextId, nextPathPos, jumpTime, blockedTime, crouchEndTime) {
        const tags = [];

        if (!botPos || !playerPos) tags.push('NO_POS');

        if (botPos && playerPos) {
            const dyBP = Math.abs(Number(botPos.y) - Number(playerPos.y));
            const dxzBP = vec3DistanceXZ(botPos, playerPos);
            if (dyBP > 0.35 || dxzBP > 0.35) tags.push('BOT_PLAYER_MISMATCH');
        }

        if (finalTarget && botPos) {
            const dy = vec3DistanceY(botPos, finalTarget);
            const dxz = vec3DistanceXZ(botPos, finalTarget);
            if (dy > Number(Runtime.config.airborneThreshold || 1.8)) tags.push('HIGH_FROM_FINAL');
            if (dxz > Number(Runtime.config.driftThreshold || 2.0)) tags.push('DRIFT_XZ');
        }

        if (gNearPos && botPos) {
            const dyG = Math.abs(Number(botPos.y) - Number(gNearPos.y));
            if (dyG > 1.5) tags.push('OFF_GRAPH_Y');
        }

        if (isReadablePtr(pathPtr)) tags.push('HAS_PATH');
        if (nextId >= 0) tags.push('NEXT_ID_' + nextId);
        if (nextPathPos && finalTarget) {
            const dyNP = vec3DistanceY(nextPathPos, finalTarget);
            const dxzNP = vec3DistanceXZ(nextPathPos, finalTarget);
            if (Math.abs(dyNP) > 0.8 || dxzNP > 1.5) tags.push('NEXTPOS_OLD');
        }

        if (isFinite(jumpTime) && jumpTime > 0) tags.push('JUMP_TIME');
        if (isFinite(blockedTime) && blockedTime > 0) tags.push('BLOCKED');
        if (isFinite(crouchEndTime) && crouchEndTime > 0) tags.push('CROUCH');

        if (tags.length === 0) tags.push('OK');
        return tags.join('|');
    }

    function buildBotMonitorLine(entry, index) {
        const bot = entry.bot;
        const player = entry.player;
        const pos = readEntityPositions(bot, player);

        const gNear = safeReadPointer(bot, O.Bot_gNode_Nearset);
        const gNext = safeReadPointer(bot, O.Bot_gNode_Next);
        const gNearPos = graphNodeToVec3(gNear);
        const gNextPos = graphNodeToVec3(gNext);

        const pathPtr = safeReadPointer(bot, O.Bot_path);
        const pathLength = safeReadFloat(bot, O.Bot_pathLength, -1);
        const nextId = safeReadS32(bot, O.Bot_nextPathVectorID, -999);
        const lastStartPoint = safeReadVec3Field(bot, O.Bot_lastStartPoint);
        const nextPathPos = safeReadVec3Field(bot, O.Bot_nextPathPos);
        const dirToNext = safeReadVec3Field(bot, O.Bot_dirToNextNode);
        const nextFindPathTime = safeReadFloat(bot, O.Bot_nextFindPathTime, 0);
        const nextJumpTime = safeReadFloat(bot, O.Bot_nextJumpTime, 0);
        const blockedTime = safeReadFloat(bot, O.Bot_blockedTime, 0);
        const crouchEndTime = safeReadFloat(bot, O.Bot_crouchEndTime, 0);
        const seeker = safeReadPointer(bot, O.Bot_seeker);

        const finalTarget = entry.lastFinalTarget || null;
        const botPos = pos ? pos.bot : null;
        const playerPos = pos ? pos.player : null;

        const dyFinal = finalTarget && botPos ? vec3DistanceY(botPos, finalTarget) : NaN;
        const dxzFinal = finalTarget && botPos ? vec3DistanceXZ(botPos, finalTarget) : NaN;
        const dyGraph = gNearPos && botPos ? Number(botPos.y) - Number(gNearPos.y) : NaN;

        const state = classifyBotState(entry, botPos, playerPos, finalTarget, gNearPos, gNextPos, pathPtr, nextId, nextPathPos, nextJumpTime, blockedTime, crouchEndTime);

        return {
            index: index,
            bot: bot.toString(),
            player: player.toString(),
            state: state,
            botPos: vec3ToString(botPos),
            playerPos: vec3ToString(playerPos),
            final: vec3ToString(finalTarget),
            dyFinal: fmtNum(dyFinal),
            dxzFinal: fmtNum(dxzFinal),
            gNear: gNear.toString(),
            gNearPos: vec3ToString(gNearPos),
            dyGraph: fmtNum(dyGraph),
            gNext: gNext.toString(),
            gNextPos: vec3ToString(gNextPos),
            seeker: seeker.toString(),
            path: pathPtr.toString(),
            pathLength: fmtNum(pathLength),
            nextId: nextId,
            lastStart: vec3ToString(lastStartPoint),
            nextPathPos: vec3ToString(nextPathPos),
            dirToNext: vec3ToString(dirToNext),
            nextFindPathTime: fmtNum(nextFindPathTime),
            nextJumpTime: fmtNum(nextJumpTime),
            blockedTime: fmtNum(blockedTime),
            crouchEndTime: fmtNum(crouchEndTime),
            seq: entry.lastTeleportSeq || 0,
            regroundCount: entry.regroundCount || 0
        };
    }


    function writeVec3(buf, v) {
        buf.writeFloat(Number(v.x));
        buf.add(4).writeFloat(Number(v.y));
        buf.add(8).writeFloat(Number(v.z));
        buf.add(12).writeFloat(0);
    }

    function resetRuntime(reason) {
        Runtime.generation += 1;
        Runtime.cache.trackedBots = {};
        Runtime.cache.trackedPlayers = {};
        Runtime.cache.pendingTeleport = false;
        Runtime.cache.pendingReason = '';
        Runtime.cache.lastMonitorTs = 0;
        Runtime.cache.lastTeleportSeq = 0;
        Runtime.cache.diagSnapshots = {};
        Runtime.originals = {};
        Runtime.stats.lastResetReason = reason || 'unknown';
        logOnce('reset', 'resetRuntime: ' + Runtime.stats.lastResetReason + ', gen=' + Runtime.generation, 300);
    }

    function resolveModule() {
        const mod = Process.findModuleByName('GameAssembly.dll');
        if (!mod) throw new Error('GameAssembly.dll not found');
        Runtime.module = mod;
        Runtime.base = mod.base;
        return mod.base;
    }

    function nf(rva, ret, args) {
        return new NativeFunction(Runtime.base.add(rva), ret, args, ABI);
    }

    function findExport(name) {
        // 兼容不同 Frida 版本：
        // 旧版常见：Module.findExportByName(...)
        // 新版常见：Process.getModuleByName(...).getExportByName(...)
        // 有些环境只能 enumerateExports / ApiResolver。
        function asPtrOrNull(v) {
            try {
                if (!v) return NULL;
                const p = ptr(v);
                return p && !p.isNull() ? p : NULL;
            } catch (e) {
                return NULL;
            }
        }

        function tryCall(fn) {
            try {
                const p = fn();
                return asPtrOrNull(p);
            } catch (e) {
                return NULL;
            }
        }

        let p = NULL;

        // Frida old API
        if (typeof Module !== 'undefined' && typeof Module.findExportByName === 'function') {
            p = tryCall(function () { return Module.findExportByName('GameAssembly.dll', name); });
            if (!p.isNull()) return p;
            p = tryCall(function () { return Module.findExportByName(null, name); });
            if (!p.isNull()) return p;
        }

        if (typeof Module !== 'undefined' && typeof Module.getExportByName === 'function') {
            p = tryCall(function () { return Module.getExportByName('GameAssembly.dll', name); });
            if (!p.isNull()) return p;
            p = tryCall(function () { return Module.getExportByName(null, name); });
            if (!p.isNull()) return p;
        }

        if (typeof Module !== 'undefined' && typeof Module.getGlobalExportByName === 'function') {
            p = tryCall(function () { return Module.getGlobalExportByName(name); });
            if (!p.isNull()) return p;
        }

        if (typeof Module !== 'undefined' && typeof Module.findGlobalExportByName === 'function') {
            p = tryCall(function () { return Module.findGlobalExportByName(name); });
            if (!p.isNull()) return p;
        }

        // Frida new Module object API
        const preferredModules = ['GameAssembly.dll', 'UnityPlayer.dll'];
        for (let i = 0; i < preferredModules.length; i++) {
            const mn = preferredModules[i];
            const m = tryCall(function () {
                const mod = Process.findModuleByName(mn);
                return mod ? mod.base : NULL;
            });
            if (!m.isNull()) {
                const modObj = Process.findModuleByName(mn);
                if (modObj) {
                    if (typeof modObj.getExportByName === 'function') {
                        p = tryCall(function () { return modObj.getExportByName(name); });
                        if (!p.isNull()) return p;
                    }
                    if (typeof modObj.findExportByName === 'function') {
                        p = tryCall(function () { return modObj.findExportByName(name); });
                        if (!p.isNull()) return p;
                    }
                    if (typeof modObj.enumerateExports === 'function') {
                        try {
                            const exps = modObj.enumerateExports();
                            for (let j = 0; j < exps.length; j++) {
                                if (exps[j].name === name) return asPtrOrNull(exps[j].address);
                            }
                        } catch (e) {}
                    }
                }
            }
        }

        // Last resort: enumerate all loaded modules.
        try {
            const mods = Process.enumerateModules();
            for (let i = 0; i < mods.length; i++) {
                const modObj = mods[i];
                if (!modObj || typeof modObj.enumerateExports !== 'function') continue;
                try {
                    const exps = modObj.enumerateExports();
                    for (let j = 0; j < exps.length; j++) {
                        if (exps[j].name === name) return asPtrOrNull(exps[j].address);
                    }
                } catch (e) {}
            }
        } catch (e) {}

        // ApiResolver fallback
        try {
            const resolver = new ApiResolver('module');
            const patterns = [
                'exports:GameAssembly.dll!' + name,
                'exports:UnityPlayer.dll!' + name,
                'exports:*!' + name
            ];
            for (let i = 0; i < patterns.length; i++) {
                try {
                    const matches = resolver.enumerateMatches(patterns[i]);
                    if (matches && matches.length > 0) return asPtrOrNull(matches[0].address);
                } catch (e) {}
            }
        } catch (e) {}

        return NULL;
    }

    function initIl2CppExports() {
        const names = [
            'il2cpp_domain_get',
            'il2cpp_domain_get_assemblies',
            'il2cpp_assembly_get_image',
            'il2cpp_class_from_name',
            'il2cpp_class_get_type',
            'il2cpp_type_get_object',
            'il2cpp_object_get_class',
            'il2cpp_class_is_assignable_from',
            'il2cpp_runtime_class_init'
        ];

        const exp = {};
        for (let i = 0; i < names.length; i++) {
            exp[names[i]] = findExport(names[i]);
        }

        if (!exp.il2cpp_domain_get.isNull()) {
            Runtime.il2cpp.domain_get = new NativeFunction(exp.il2cpp_domain_get, 'pointer', [], ABI);
        }
        if (!exp.il2cpp_domain_get_assemblies.isNull()) {
            Runtime.il2cpp.domain_get_assemblies = new NativeFunction(exp.il2cpp_domain_get_assemblies, 'pointer', ['pointer', 'pointer'], ABI);
        }
        if (!exp.il2cpp_assembly_get_image.isNull()) {
            Runtime.il2cpp.assembly_get_image = new NativeFunction(exp.il2cpp_assembly_get_image, 'pointer', ['pointer'], ABI);
        }
        if (!exp.il2cpp_class_from_name.isNull()) {
            Runtime.il2cpp.class_from_name = new NativeFunction(exp.il2cpp_class_from_name, 'pointer', ['pointer', 'pointer', 'pointer'], ABI);
        }
        if (!exp.il2cpp_class_get_type.isNull()) {
            Runtime.il2cpp.class_get_type = new NativeFunction(exp.il2cpp_class_get_type, 'pointer', ['pointer'], ABI);
        }
        if (!exp.il2cpp_type_get_object.isNull()) {
            Runtime.il2cpp.type_get_object = new NativeFunction(exp.il2cpp_type_get_object, 'pointer', ['pointer'], ABI);
        }
        if (!exp.il2cpp_object_get_class.isNull()) {
            Runtime.il2cpp.object_get_class = new NativeFunction(exp.il2cpp_object_get_class, 'pointer', ['pointer'], ABI);
        }
        if (!exp.il2cpp_class_is_assignable_from.isNull()) {
            Runtime.il2cpp.class_is_assignable_from = new NativeFunction(exp.il2cpp_class_is_assignable_from, 'bool', ['pointer', 'pointer'], ABI);
        }
        if (!exp.il2cpp_runtime_class_init.isNull()) {
            Runtime.il2cpp.runtime_class_init = new NativeFunction(exp.il2cpp_runtime_class_init, 'void', ['pointer'], ABI);
        }
    }

    function initNativeFunctions() {
        Runtime.funcs.isMy = nf(R.P_isMy, 'bool', ['pointer', 'pointer']);
        Runtime.funcs.isDead = nf(R.E_isDead, 'bool', ['pointer', 'pointer']);
        Runtime.funcs.getCC = nf(R.E_getCC, 'pointer', ['pointer', 'pointer']);
        Runtime.funcs.setControllerEnabled = nf(R.C_setEn, 'void', ['pointer', 'int', 'pointer']);
        Runtime.funcs.getTransform = nf(R.Component_get_transform, 'pointer', ['pointer', 'pointer']);
        Runtime.funcs.getGameObject = nf(R.Component_get_gameObject, 'pointer', ['pointer', 'pointer']);
        Runtime.funcs.componentGetComponent = nf(R.Component_GetComponent_Type, 'pointer', ['pointer', 'pointer', 'pointer']);
        Runtime.funcs.gameObjectGetComponent = nf(R.GameObject_GetComponent_Type, 'pointer', ['pointer', 'pointer', 'pointer']);
        Runtime.funcs.setPositionInjected = nf(R.Transform_set_position_Injected, 'void', ['pointer', 'pointer', 'pointer']);
        Runtime.funcs.getPositionInjected = nf(R.Transform_get_position_Injected, 'void', ['pointer', 'pointer', 'pointer']);
        Runtime.funcs.richAiTeleport = nf(R.RichAI_Teleport, 'void', ['pointer', Vec3, 'int', 'pointer']);
        Runtime.funcs.richAiSearchPath = nf(R.RichAI_SearchPath, 'void', ['pointer', 'pointer']);
        Runtime.funcs.aiBaseCancelPath = nf(R.AIBase_CancelCurrentPathRequest, 'void', ['pointer', 'pointer']);
        Runtime.funcs.aiBaseSetPath = nf(R.AIBase_SetPath, 'void', ['pointer', 'pointer', 'pointer']);
        Runtime.funcs.aiBaseSearchPath = nf(R.AIBase_SearchPath, 'void', ['pointer', 'pointer']);
        Runtime.funcs.aiBaseTeleport = nf(R.AIBase_Teleport, 'void', ['pointer', Vec3, 'int', 'pointer']);
        Runtime.funcs.botUpdateNearestGraphNode = nf(R.Bot_UpdateNearestGraphNode, 'void', ['pointer', 'pointer']);
        Runtime.funcs.botPathSetting = nf(R.Bot_PathSetting, 'void', ['pointer', 'pointer']);
    }

    function allocUtf8(s) {
        return Memory.allocUtf8String(s || '');
    }

    function getClassFromName(namespaceName, className) {
        try {
            const api = Runtime.il2cpp;
            if (!api.domain_get || !api.domain_get_assemblies || !api.assembly_get_image || !api.class_from_name) return NULL;
            const domain = api.domain_get();
            if (!isReadablePtr(domain)) return NULL;
            const sizeBuf = Memory.alloc(Process.pointerSize);
            sizeBuf.writePointer(NULL);
            const assemblies = api.domain_get_assemblies(domain, sizeBuf);
            if (!isReadablePtr(assemblies)) return NULL;
            const count = sizeBuf.readU32();
            const nsPtr = allocUtf8(namespaceName);
            const namePtr = allocUtf8(className);
            for (let i = 0; i < count; i++) {
                const asm = assemblies.add(i * Process.pointerSize).readPointer();
                if (!isReadablePtr(asm)) continue;
                const image = api.assembly_get_image(asm);
                if (!isReadablePtr(image)) continue;
                const klass = api.class_from_name(image, nsPtr, namePtr);
                if (isReadablePtr(klass)) return klass;
            }
        } catch (e) {
            recordError('getClassFromName.' + className, e);
        }
        return NULL;
    }

    function getClassFromTypeInfoSlot(rva) {
        try {
            const slot = Runtime.base.add(rva);
            const klass = slot.readPointer();
            if (isReadablePtr(klass)) return klass;
        } catch (e) {}
        return NULL;
    }

    function systemTypeFromClass(klass) {
        try {
            const api = Runtime.il2cpp;
            if (!isReadablePtr(klass) || !api.class_get_type || !api.type_get_object) return NULL;
            try {
                if (api.runtime_class_init) api.runtime_class_init(klass);
            } catch (e) {}
            const il2cppType = api.class_get_type(klass);
            if (!isReadablePtr(il2cppType)) return NULL;
            const systemType = api.type_get_object(il2cppType);
            return isReadablePtr(systemType) ? systemType : NULL;
        } catch (e) {
            recordError('systemTypeFromClass', e);
            return NULL;
        }
    }

    function resolveType(label, namespaceName, className, typeInfoRva) {
        let klass = getClassFromName(namespaceName, className);
        if (!isReadablePtr(klass)) klass = getClassFromTypeInfoSlot(typeInfoRva);
        const systemType = systemTypeFromClass(klass);
        Runtime.types[label] = { klass: klass, type: systemType };
        logOnce('type:' + label, label + ' klass=' + klass + ' type=' + systemType, 1000);
    }

    function initTypes() {
        resolveType('RichAI', 'Pathfinding', 'RichAI', TYPEINFO_RVA.RichAI);
        resolveType('AIBase', 'Pathfinding', 'AIBase', TYPEINFO_RVA.AIBase);
        resolveType('IAstarAI', 'Pathfinding', 'IAstarAI', TYPEINFO_RVA.IAstarAI);
    }

    function isInstanceOf(obj, typeLabel) {
        try {
            const api = Runtime.il2cpp;
            const target = Runtime.types[typeLabel] && Runtime.types[typeLabel].klass;
            if (!isReadablePtr(obj) || !isReadablePtr(target) || !api.object_get_class || !api.class_is_assignable_from) return false;
            const cls = api.object_get_class(obj);
            if (!isReadablePtr(cls)) return false;
            return !!api.class_is_assignable_from(target, cls);
        } catch (e) {
            return false;
        }
    }

    function getComponentByType(componentPtr, typeLabel) {
        try {
            const typeInfo = Runtime.types[typeLabel];
            if (!typeInfo || !isReadablePtr(typeInfo.type)) return NULL;
            if (isReadablePtr(componentPtr)) {
                const c1 = Runtime.funcs.componentGetComponent(componentPtr, typeInfo.type, NULL);
                if (isReadablePtr(c1)) return c1;
                const go = Runtime.funcs.getGameObject(componentPtr, NULL);
                if (isReadablePtr(go)) {
                    const c2 = Runtime.funcs.gameObjectGetComponent(go, typeInfo.type, NULL);
                    if (isReadablePtr(c2)) return c2;
                }
            }
        } catch (e) {
            recordError('getComponentByType.' + typeLabel, e);
        }
        return NULL;
    }

    function resolveAiComponent(botPtr) {
        if (!isReadablePtr(botPtr)) return { kind: 'none', ptr: NULL, reason: 'bot_invalid' };

        if (Runtime.config.useRichAI) {
            const rich = getComponentByType(botPtr, 'RichAI');
            if (isReadablePtr(rich)) return { kind: 'richai', ptr: rich, reason: 'GetComponent(RichAI)' };
        }

        if (Runtime.config.useAIBase) {
            const base = getComponentByType(botPtr, 'AIBase');
            if (isReadablePtr(base)) {
                if (isInstanceOf(base, 'RichAI')) return { kind: 'richai', ptr: base, reason: 'GetComponent(AIBase)->RichAI' };
                return { kind: 'aibase', ptr: base, reason: 'GetComponent(AIBase)' };
            }
        }

        if (Runtime.config.useIAstarAIProbe) {
            const ai = getComponentByType(botPtr, 'IAstarAI');
            if (isReadablePtr(ai)) {
                if (isInstanceOf(ai, 'RichAI')) return { kind: 'richai', ptr: ai, reason: 'GetComponent(IAstarAI)->RichAI' };
                if (isInstanceOf(ai, 'AIBase')) return { kind: 'aibase', ptr: ai, reason: 'GetComponent(IAstarAI)->AIBase' };
                return { kind: 'iastarai_unknown', ptr: ai, reason: 'GetComponent(IAstarAI), class not AIBase/RichAI' };
            }
        }

        return { kind: 'none', ptr: NULL, reason: 'no_ai_component' };
    }

    function isValidObject(p) {
        return isReadablePtr(p);
    }

    function isHumanPlayer(playerPtr) {
        const cd = safeReadPointer(playerPtr, O.P_clientData);
        if (isReadablePtr(cd)) {
            const b = safeReadU8(cd, O.CD_isBot, 255);
            if (b === 1) return false;
            if (b === 0) return true;
        }
        const cameraMgr = safeReadPointer(playerPtr, O.P_cameraManager);
        if (isReadablePtr(cameraMgr)) return true;
        return false;
    }

    function shouldSkipPlayer(playerPtr) {
        if (!isValidObject(playerPtr)) return 'invalid';
        try { if (Runtime.funcs.isMy(playerPtr, NULL)) return 'self'; } catch (e) {}
        try { if (isHumanPlayer(playerPtr)) return 'human'; } catch (e) {}
        try { if (Runtime.funcs.isDead(playerPtr, NULL)) return 'dead'; } catch (e) {}
        return '';
    }

    function trackPlayer(playerPtr, source) {
        if (!isValidObject(playerPtr)) return false;
        const key = playerPtr.toString();
        if (!Runtime.cache.trackedPlayers[key]) {
            Runtime.cache.trackedPlayers[key] = { player: playerPtr, source: source || 'unknown', seen: 1, gen: Runtime.generation };
        } else {
            Runtime.cache.trackedPlayers[key].seen++;
        }
        Runtime.stats.playersTracked = Object.keys(Runtime.cache.trackedPlayers).length;
        return true;
    }

    function trackFromBot(botPtr) {
        try {
            if (!isValidObject(botPtr)) return;
            const key = botPtr.toString();
            const player = safeReadPointer(botPtr, O.Bot_thisPlayer);
            const pValid = isValidObject(player);
            if (!Runtime.cache.trackedBots[key]) {
                Runtime.cache.trackedBots[key] = {
                    bot: botPtr,
                    player: pValid ? player : NULL,
                    hasPlayer: pValid,
                    aiKind: '',
                    aiPtr: NULL,
                    aiReason: '',
                    seen: 1,
                    gen: Runtime.generation
                };
            } else {
                const item = Runtime.cache.trackedBots[key];
                item.seen++;
                if (pValid) {
                    item.player = player;
                    item.hasPlayer = true;
                }
            }
            if (pValid) trackPlayer(player, 'Bot.Update');
            Runtime.stats.botsTracked = Object.keys(Runtime.cache.trackedBots).length;
        } catch (e) {
            recordError('trackFromBot', e);
        }
    }

    function scanAllPlayersFromGM() {
        try {
            const gm = Runtime.cache.gm;
            if (!isReadablePtr(gm)) return 0;
            const ap = safeReadPointer(gm, O.GM_allPlayers);
            if (!isReadablePtr(ap)) return 0;
            const total = ap.add(0x0C).readU32();
            let n = 0;
            for (let i = 0; i < total && i < 64; i++) {
                const pp = ap.add(0x10 + i * 8).readPointer();
                if (trackPlayer(pp, 'allPlayers')) n++;
            }
            return n;
        } catch (e) {
            recordError('scanAllPlayersFromGM', e);
            return 0;
        }
    }

    function zeroJumpLinkStruct(botPtr) {
        // Bot.nextJumpLink 是 struct Bot_JumpLink.Link，不是对象指针。
        // 结构体总长 0x1C: endTransform/endNode/needSpeed/accuracy/direction。
        try {
            if (!isReadablePtr(botPtr)) return false;
            botPtr.add(O.Bot_nextJumpLink + 0x00).writePointer(NULL);
            botPtr.add(O.Bot_nextJumpLink + 0x04).writePointer(NULL);
            botPtr.add(O.Bot_nextJumpLink + 0x08).writeFloat(0);
            botPtr.add(O.Bot_nextJumpLink + 0x0C).writeFloat(0);
            botPtr.add(O.Bot_nextJumpLink + 0x10).writeFloat(0);
            botPtr.add(O.Bot_nextJumpLink + 0x14).writeFloat(0);
            botPtr.add(O.Bot_nextJumpLink + 0x18).writeFloat(0);
            return true;
        } catch (e) {
            Runtime.stats.skippedInvalid++;
            return false;
        }
    }

    function syncBotPathFields(botPtr, target) {
        if (!Runtime.config.syncBotPathFields || !isReadablePtr(botPtr)) return 'sync=skip';

        let w = 0;
        const zero = vec3Zero();

        // 这个项目的 Bot 没挂 RichAI/AIBase，移动状态主要在 Bot 自己：
        // seeker/path/gNode/nextPathVectorID/lastStartPoint/nextPathPos 等。
        // 注意：这里不直接改 seeker，不直接改 Destination_Listener，只清旧路径和移动缓存。
        if (safeWritePointer(botPtr, O.Bot_path, NULL)) w++;
        if (safeWriteFloat(botPtr, O.Bot_pathLength, 0)) w++;

        const nearest = safeReadPointer(botPtr, O.Bot_gNode_Nearset);
        if (isReadablePtr(nearest)) {
            if (safeWritePointer(botPtr, O.Bot_gNode_Next, nearest)) w++;
        } else {
            if (safeWritePointer(botPtr, O.Bot_gNode_Next, NULL)) w++;
        }

        if (safeWriteS32(botPtr, O.Bot_nextPathVectorID, -1)) w++;
        if (safeWriteVec3Field(botPtr, O.Bot_lastStartPoint, target)) w++;
        if (safeWriteVec3Field(botPtr, O.Bot_nextPathPos, target)) w++;
        if (safeWriteVec3Field(botPtr, O.Bot_dirToNextNode, zero)) w++;
        if (safeWriteFloat(botPtr, O.Bot_nextFindPathTime, 0)) w++;

        // 清掉跳跃/卡住/蹲伏相关状态，避免瞬移后继续执行旧 jump/crouch/block 逻辑。
        if (safeWritePointer(botPtr, O.Bot_nextJumpStartNode, NULL)) w++;
        if (zeroJumpLinkStruct(botPtr)) w++;
        if (safeWriteFloat(botPtr, O.Bot_nextJumpTime, 0)) w++;
        if (safeWriteFloat(botPtr, O.Bot_blockedTime, 0)) w++;
        if (safeWriteFloat(botPtr, O.Bot_crouchEndTime, 0)) w++;

        return 'sync=ok,w=' + w + ',nearest=' + (isReadablePtr(nearest) ? 'yes' : 'no');
    }

    function callBotRefresh(botPtr, playerPtr, rawTarget, options) {
        options = options || {};
        if (!Runtime.config.callBotRefresh || !isReadablePtr(botPtr)) {
            return { text: 'refresh=skip', finalTarget: rawTarget, graph: null };
        }

        let parts = [];
        let graphPos = null;
        let finalTarget = rawTarget;

        // 1) 按当前 Transform 刷新最近 GraphNode。
        try {
            Runtime.funcs.botUpdateNearestGraphNode(botPtr, NULL);
            parts.push('nearest=ok');
        } catch (e) {
            parts.push('nearest=err');
        }

        // 2) 从 gNode_Nearset 读取真正的导航图坐标，用于贴地。
        const nearest = safeReadPointer(botPtr, O.Bot_gNode_Nearset);
        graphPos = graphNodeToVec3(nearest);
        if (graphPos) {
            parts.push('graph=' + vec3ToString(graphPos));
            if (Runtime.config.groundToNearestNode) {
                finalTarget = {
                    x: Runtime.config.useGraphNodeXZ ? graphPos.x : rawTarget.x,
                    y: graphPos.y + (Number(Runtime.config.graphYOffset) || 0),
                    z: Runtime.config.useGraphNodeXZ ? graphPos.z : rawTarget.z
                };
                parts.push('ground=' + vec3ToString(finalTarget));
            }
        } else {
            parts.push('graph=null');
        }

        // 3) 如果目标点被贴地，重新设置 Transform 到 GraphNode 位置。
        if (!options.skipGroundSet && Runtime.config.groundToNearestNode && finalTarget && !sameVec3(finalTarget, rawTarget)) {
            try {
                const fb = fallbackTransform(botPtr, playerPtr, finalTarget);
                parts.push(fb.ok ? 'groundSet=ok' : 'groundSet=' + fb.method);
            } catch (e) {
                parts.push('groundSet=err');
            }

            try {
                Runtime.funcs.botUpdateNearestGraphNode(botPtr, NULL);
                parts.push('nearest2=ok');
            } catch (e) {
                parts.push('nearest2=err');
            }
        }

        // 4) 路径缓存只同步到最终贴地点，不再同步 rawTarget。
        try {
            parts.push(syncBotPathFields(botPtr, finalTarget));
        } catch (e) {
            parts.push('sync=err');
        }

        if (Runtime.config.pathSettingAfterTeleport) {
            try {
                Runtime.funcs.botPathSetting(botPtr, NULL);
                parts.push('pathSetting=ok');
            } catch (e) {
                parts.push('pathSetting=err');
            }
        } else {
            parts.push('pathSetting=skip');
        }

        return { text: parts.join(','), finalTarget: finalTarget, graph: graphPos };
    }

    function teleportByAi(aiInfo, target) {
        if (!Runtime.config.aiFirst) return { ok: false, method: 'ai_disabled' };
        if (!isReadablePtr(aiInfo.ptr)) return { ok: false, method: 'ai_null' };
        const v = [Number(target.x), Number(target.y), Number(target.z)];

        try {
            if (aiInfo.kind === 'richai') {
                Runtime.funcs.richAiTeleport(aiInfo.ptr, v, 1, NULL);
                if (Runtime.config.callSearchPath) {
                    try { Runtime.funcs.richAiSearchPath(aiInfo.ptr, NULL); } catch (e) {}
                }
                Runtime.stats.richAiOk++;
                Runtime.stats.aiTeleportOk++;
                return { ok: true, method: 'RichAI.Teleport(clearPath=true)' };
            }

            if (aiInfo.kind === 'aibase') {
                try { Runtime.funcs.aiBaseCancelPath(aiInfo.ptr, NULL); } catch (e) {}
                try { Runtime.funcs.aiBaseSetPath(aiInfo.ptr, NULL, NULL); } catch (e) {}
                Runtime.funcs.aiBaseTeleport(aiInfo.ptr, v, 1, NULL);
                if (Runtime.config.callSearchPath) {
                    try { Runtime.funcs.aiBaseSearchPath(aiInfo.ptr, NULL); } catch (e) {}
                }
                Runtime.stats.aiBaseOk++;
                Runtime.stats.aiTeleportOk++;
                return { ok: true, method: 'AIBase.Teleport(clearPath=true)' };
            }
        } catch (e) {
            recordError('teleportByAi.' + aiInfo.kind, e);
            return { ok: false, method: aiInfo.kind + '.err:' + (e.message || String(e)) };
        }

        return { ok: false, method: aiInfo.kind || 'none' };
    }

    function getTransformOf(componentPtr) {
        try {
            if (!isReadablePtr(componentPtr)) return NULL;
            const tr = Runtime.funcs.getTransform(componentPtr, NULL);
            return isReadablePtr(tr) ? tr : NULL;
        } catch (e) {
            return NULL;
        }
    }

    function getTransformPosition(tr) {
        try {
            if (!isReadablePtr(tr)) return null;
            const buf = Memory.alloc(16);
            Runtime.funcs.getPositionInjected(tr, buf, NULL);
            return readVec3(buf);
        } catch (e) {
            return null;
        }
    }

    function readEntityPositions(botPtr, playerPtr) {
        const botTr = getTransformOf(botPtr);
        let playerTr = getTransformOf(playerPtr);
        if (!isReadablePtr(playerTr)) playerTr = safeReadPointer(playerPtr, O.P_charContainer);
        return {
            bot: getTransformPosition(botTr),
            player: getTransformPosition(playerTr)
        };
    }

    function setTransformPosition(tr, target) {
        if (!isReadablePtr(tr)) return false;
        writeVec3(posBuf, target);
        Runtime.funcs.setPositionInjected(tr, posBuf, NULL);

        // v4 默认关闭 native cache 直写，避免高度漂移时多一个不确定因素。
        if (Runtime.config.writeNativeTransformCache) {
            try {
                const nativePtr = tr.add(0x10).readPointer();
                if (isReadablePtr(nativePtr)) {
                    nativePtr.add(0x38).writeFloat(Number(target.x));
                    nativePtr.add(0x3C).writeFloat(Number(target.y));
                    nativePtr.add(0x40).writeFloat(Number(target.z));
                }
            } catch (e) {}
        }
        return true;
    }

    function fallbackTransform(botPtr, playerPtr, target) {
        if (!Runtime.config.transformFallback) return { ok: false, method: 'fallback_disabled' };
        try {
            let cc = NULL;
            try { cc = Runtime.funcs.getCC(playerPtr, NULL); } catch (e) {}
            if (isReadablePtr(cc)) {
                try { Runtime.funcs.setControllerEnabled(cc, 0, NULL); } catch (e) {}
            }

            let ok = false;
            const botTr = getTransformOf(botPtr);
            if (setTransformPosition(botTr, target)) ok = true;

            let playerTr = getTransformOf(playerPtr);
            if (!isReadablePtr(playerTr)) playerTr = safeReadPointer(playerPtr, O.P_charContainer);
            if (setTransformPosition(playerTr, target)) ok = true;

            if (isReadablePtr(cc)) {
                try { Runtime.funcs.setControllerEnabled(cc, 1, NULL); } catch (e) {}
            }

            if (ok) {
                Runtime.stats.fallbackOk++;
                return { ok: true, method: 'TransformFallback(bot+player)' };
            }
            return { ok: false, method: 'fallback_no_transform' };
        } catch (e) {
            recordError('fallbackTransform', e);
            return { ok: false, method: 'fallback_err:' + (e.message || String(e)) };
        }
    }

    function prepareTarget(rawTarget) {
        // v1: 不主动调用 AstarPath.GetNearest，避免在未确认签名时增加崩溃点。
        // 这里先保留接口，后续验证 RichAI/AIBase Teleport 稳定后，再加入 navmesh/graph 贴点。
        return {
            x: Number(rawTarget.x),
            y: Number(rawTarget.y),
            z: Number(rawTarget.z)
        };
    }

    function teleportOneBot(entry, target, index) {
        const bot = entry.bot;
        const player = entry.player;
        const skip = shouldSkipPlayer(player);
        if (skip) {
            if (skip === 'self') Runtime.stats.skippedSelf++;
            else if (skip === 'human') Runtime.stats.skippedHuman++;
            else if (skip === 'dead') Runtime.stats.skippedDead++;
            else Runtime.stats.skippedInvalid++;
            return { ok: false, skipped: true, reason: skip };
        }

        const beforePos = readEntityPositions(bot, player);

        let aiInfo = resolveAiComponent(bot);
        entry.aiKind = aiInfo.kind;
        entry.aiPtr = aiInfo.ptr;
        entry.aiReason = aiInfo.reason;

        let aiResult = { ok: false, method: aiInfo.kind };
        if (aiInfo.kind === 'richai' || aiInfo.kind === 'aibase') {
            aiResult = teleportByAi(aiInfo, target);
            if (aiResult.ok) {
                const refresh = callBotRefresh(bot, player, target);
                const afterPos = readEntityPositions(bot, player);
                return {
                    ok: true,
                    method: aiResult.method,
                    refresh: refresh.text,
                    ai: aiInfo.kind,
                    before: beforePos,
                    after: afterPos,
                    graph: refresh.graph,
                    finalTarget: refresh.finalTarget
                };
            }
        } else {
            Runtime.stats.skippedNoAi++;
        }

        const fb = fallbackTransform(bot, player, target);
        if (fb.ok) {
            const refresh2 = callBotRefresh(bot, player, target);
            const afterPos2 = readEntityPositions(bot, player);
            return {
                ok: true,
                method: fb.method,
                refresh: refresh2.text,
                ai: aiInfo.kind,
                aiFail: aiResult.method,
                before: beforePos,
                after: afterPos2,
                graph: refresh2.graph,
                finalTarget: refresh2.finalTarget
            };
        }

        Runtime.stats.failed++;
        return { ok: false, skipped: false, reason: fb.method, ai: aiInfo.kind, aiFail: aiResult.method, before: beforePos };
    }




    function compactMonitorObject(m) {
        return {
            index: m.index,
            bot: m.bot,
            player: m.player,
            state: m.state,
            botPos: m.botPos,
            playerPos: m.playerPos,
            final: m.final,
            dyFinal: m.dyFinal,
            dxzFinal: m.dxzFinal,
            gNearPos: m.gNearPos,
            dyGraph: m.dyGraph,
            gNextPos: m.gNextPos,
            path: m.path,
            pathLength: m.pathLength,
            nextId: m.nextId,
            nextPathPos: m.nextPathPos,
            lastStart: m.lastStart,
            dirToNext: m.dirToNext,
            nextFindPathTime: m.nextFindPathTime,
            nextJumpTime: m.nextJumpTime,
            blockedTime: m.blockedTime,
            crouchEndTime: m.crouchEndTime,
            seq: m.seq
        };
    }

    function snapshotKeyForEntry(entry) {
        try { return entry && entry.bot ? entry.bot.toString() : ''; } catch (e) { return ''; }
    }

    function makeDiagnosticSnapshot(label, seq) {
        if (!Runtime.config.diagEnabled) return null;

        const keys = collectValidBotKeys();
        const maxBots = Math.max(1, Number(Runtime.config.diagMaxBots) || 64);
        const snap = {
            label: label,
            seq: seq,
            time: Date.now(),
            byBot: {},
            order: []
        };

        let high = 0;
        let drift = 0;
        let hasPath = 0;
        let mismatch = 0;

        for (let i = 0; i < keys.length && i < maxBots; i++) {
            const entry = Runtime.cache.trackedBots[keys[i]];
            if (!entry) continue;
            const m = compactMonitorObject(buildBotMonitorLine(entry, i));
            const k = snapshotKeyForEntry(entry);
            if (!k) continue;

            if (String(m.state).indexOf('HIGH_FROM_FINAL') >= 0 || String(m.state).indexOf('OFF_GRAPH_Y') >= 0) high++;
            if (String(m.state).indexOf('DRIFT_XZ') >= 0 || String(m.state).indexOf('NEXTPOS_OLD') >= 0) drift++;
            if (String(m.state).indexOf('HAS_PATH') >= 0) hasPath++;
            if (String(m.state).indexOf('BOT_PLAYER_MISMATCH') >= 0) mismatch++;

            snap.byBot[k] = m;
            snap.order.push(k);
        }

        snap.summary = {
            bots: snap.order.length,
            high: high,
            drift: drift,
            hasPath: hasPath,
            mismatch: mismatch
        };

        if (!Runtime.cache.diagSnapshots[seq]) Runtime.cache.diagSnapshots[seq] = {};
        Runtime.cache.diagSnapshots[seq][label] = snap;
        Runtime.stats.diagRuns++;

        return snap;
    }

    function fieldsChanged(a, b) {
        const changed = [];
        if (!a || !b) return changed;

        const fields = [
            'botPos', 'playerPos', 'gNearPos', 'gNextPos', 'path',
            'pathLength', 'nextId', 'nextPathPos', 'lastStart',
            'dirToNext', 'nextFindPathTime', 'nextJumpTime',
            'blockedTime', 'crouchEndTime', 'state'
        ];

        for (let i = 0; i < fields.length; i++) {
            const f = fields[i];
            if (String(a[f]) !== String(b[f])) changed.push(f + ':' + String(a[f]) + '->' + String(b[f]));
        }

        return changed;
    }

    function analyzeSnapshotDiff(seq, fromLabel, toLabel) {
        const store = Runtime.cache.diagSnapshots[seq] || {};
        const a = store[fromLabel];
        const b = store[toLabel];
        if (!a || !b) return null;

        const lines = [];
        let pathRecreated = 0;
        let pathChanged = 0;
        let nextPosChanged = 0;
        let moved = 0;
        let high = b.summary.high || 0;
        let drift = b.summary.drift || 0;
        let hasPath = b.summary.hasPath || 0;
        let mismatch = b.summary.mismatch || 0;
        let weaponLikeSyncSuspect = 0;

        const limit = Math.max(1, Number(Runtime.config.diagDetailLimit) || 64);

        for (let i = 0; i < b.order.length; i++) {
            const k = b.order[i];
            const before = a.byBot[k];
            const after = b.byBot[k];
            if (!before || !after) continue;

            const tags = [];

            if (before.path === '0x0' && after.path !== '0x0') {
                tags.push('PATH_RECREATED');
                pathRecreated++;
            } else if (before.path !== after.path) {
                tags.push('PATH_CHANGED');
                pathChanged++;
            }

            if (before.nextPathPos !== after.nextPathPos) {
                tags.push('NEXTPOS_CHANGED');
                nextPosChanged++;
            }

            if (String(after.state).indexOf('DRIFT_XZ') >= 0 || String(after.state).indexOf('HIGH_FROM_FINAL') >= 0 || String(after.state).indexOf('OFF_GRAPH_Y') >= 0) {
                tags.push('MOVED_OR_HIGH');
                moved++;
            }

            if (String(after.state).indexOf('HAS_PATH') >= 0 && String(after.state).indexOf('NEXTPOS_OLD') >= 0) {
                tags.push('AI_PATH_TAKING_OVER');
            }

            if (before.nextId !== after.nextId || before.path !== after.path || before.nextPathPos !== after.nextPathPos) {
                tags.push('PATH_STATE_MUTATED');
            }

            // 如果多个 Bot 同步出现 path/nextPathPos 变化，而 jump/block/crouch 都为 0，
            // 更像行为层/目标层更新，而不是物理跳跃/阻塞。
            if (tags.length > 0 && lines.length < limit) {
                const changed = fieldsChanged(before, after).slice(0, 8).join(';');
                lines.push(
                    '#' + after.index +
                    ' bot=' + after.bot +
                    ' tags=' + tags.join('|') +
                    ' state=' + after.state +
                    ' pos=' + before.botPos + '->' + after.botPos +
                    ' final=' + after.final +
                    ' gNear=' + after.gNearPos +
                    ' path=' + before.path + '->' + after.path +
                    ' nextId=' + before.nextId + '->' + after.nextId +
                    ' nextPath=' + before.nextPathPos + '->' + after.nextPathPos +
                    ' changed=' + changed
                );
            }
        }

        Runtime.stats.diagPathRecreated += pathRecreated;
        Runtime.stats.diagNextPosChanged += nextPosChanged;
        Runtime.stats.diagMovedFromFinal += moved;

        const summary =
            'diag seq=' + seq +
            ' ' + fromLabel + '->' + toLabel +
            ' bots=' + b.order.length +
            ' high=' + high +
            ' drift=' + drift +
            ' hasPath=' + hasPath +
            ' mismatch=' + mismatch +
            ' pathRecreated=' + pathRecreated +
            ' pathChanged=' + pathChanged +
            ' nextPosChanged=' + nextPosChanged +
            ' movedOrHigh=' + moved;

        log(summary);
        for (let j = 0; j < lines.length && j < 16; j++) log('  ' + lines[j]);

        send({
            t: 'bot_ai_teleport_diag',
            summary: summary,
            details: lines,
            seq: seq,
            from: fromLabel,
            to: toLabel,
            counts: {
                high: high,
                drift: drift,
                hasPath: hasPath,
                mismatch: mismatch,
                pathRecreated: pathRecreated,
                pathChanged: pathChanged,
                nextPosChanged: nextPosChanged,
                movedOrHigh: moved
            }
        });

        return { summary: summary, details: lines };
    }

    function scheduleDiagnosticSnapshots(seq) {
        if (!Runtime.config.diagEnabled) return;
        const delays = [200, 500, 1000, 2000, 4000];

        for (let i = 0; i < delays.length; i++) {
            (function (delay) {
                const timerId = setTimeout(function () {
                    try {
                        const label = 't+' + delay + 'ms';
                        makeDiagnosticSnapshot(label, seq);
                        analyzeSnapshotDiff(seq, 'post', label);
                    } catch (e) {
                        recordError('scheduleDiagnosticSnapshots.' + delay, e);
                    }
                }, delay);
                Runtime.timers.push(timerId);
            })(delays[i]);
        }
    }

    function runDiagnosticNow() {
        const seq = Runtime.cache.lastTeleportSeq || 0;
        const label = 'manual_' + Date.now();
        makeDiagnosticSnapshot(label, seq);
        if (Runtime.cache.diagSnapshots[seq] && Runtime.cache.diagSnapshots[seq].post) {
            return analyzeSnapshotDiff(seq, 'post', label) || getStatus();
        }
        return getStatus();
    }

    function startMonitorTimer() {
        if (!Runtime.config.monitorEnabled) return;
        for (let i = 0; i < Runtime.timers.length; i++) {
            // 不尝试识别旧 timer 类型；disable/cleanup 会统一 clear。
        }
        const interval = Math.max(500, Number(Runtime.config.monitorIntervalMs) || 1000);
        const id = setInterval(function () {
            try { monitorTick(); } catch (e) { recordError('monitorTick', e); }
        }, interval);
        Runtime.timers.push(id);
        log('monitor started interval=' + interval + 'ms');
    }

    function monitorTick() {
        if (!Runtime.enabled || !Runtime.config.monitorEnabled) return;

        const keys = collectValidBotKeys();
        const maxBots = Math.max(1, Number(Runtime.config.monitorMaxBots) || 64);
        const lines = [];
        let high = 0;
        let drift = 0;
        let hasPath = 0;
        let mismatch = 0;

        Runtime.stats.monitorTicks++;

        for (let i = 0; i < keys.length && i < maxBots; i++) {
            const entry = Runtime.cache.trackedBots[keys[i]];
            if (!entry) continue;

            const m = buildBotMonitorLine(entry, i);

            if (String(m.state).indexOf('HIGH_FROM_FINAL') >= 0 || String(m.state).indexOf('OFF_GRAPH_Y') >= 0) high++;
            if (String(m.state).indexOf('DRIFT_XZ') >= 0 || String(m.state).indexOf('NEXTPOS_OLD') >= 0) drift++;
            if (String(m.state).indexOf('HAS_PATH') >= 0) hasPath++;
            if (String(m.state).indexOf('BOT_PLAYER_MISMATCH') >= 0) mismatch++;

            lines.push(
                '#' + m.index +
                ' state=' + m.state +
                ' bot=' + m.bot +
                ' player=' + m.player +
                ' botPos=' + m.botPos +
                ' playerPos=' + m.playerPos +
                ' final=' + m.final +
                ' dyFinal=' + m.dyFinal +
                ' dxzFinal=' + m.dxzFinal +
                ' gNearPos=' + m.gNearPos +
                ' dyGraph=' + m.dyGraph +
                ' path=' + m.path +
                ' pathLen=' + m.pathLength +
                ' nextId=' + m.nextId +
                ' nextPathPos=' + m.nextPathPos +
                ' lastStart=' + m.lastStart +
                ' jump=' + m.nextJumpTime +
                ' block=' + m.blockedTime +
                ' crouch=' + m.crouchEndTime
            );
        }

        Runtime.stats.highObserved += high;
        Runtime.stats.driftObserved += drift;

        const summary = 'monitor tick=' + Runtime.stats.monitorTicks +
            ' bots=' + keys.length +
            ' high=' + high +
            ' drift=' + drift +
            ' hasPath=' + hasPath +
            ' mismatch=' + mismatch +
            ' seq=' + Runtime.cache.lastTeleportSeq;

        log(summary);
        for (let j = 0; j < lines.length; j++) log('  ' + lines[j]);
        send({ t: 'bot_ai_teleport_monitor', summary: summary, details: lines });
    }

    function monitorTickFromGameUpdate() {
        if (!Runtime.enabled || !Runtime.config.monitorEnabled) return;
        const now = Date.now();
        const interval = Math.max(500, Number(Runtime.config.monitorIntervalMs) || 1000);
        if (Runtime.cache.lastMonitorTs && (now - Runtime.cache.lastMonitorTs) < interval) return;
        Runtime.cache.lastMonitorTs = now;
        try {
            monitorTick();
        } catch (e) {
            recordError('monitorTickFromGameUpdate', e);
        }
    }


    function computeClusterTarget(base, index) {
        if (!Runtime.config.spreadCluster) return base;

        const spacing = Math.max(0.1, Number(Runtime.config.clusterSpacing) || 0.75);
        const maxRadius = Math.max(spacing, Number(Runtime.config.clusterMaxRadius) || 4.2);

        // 黄金角螺旋：不会把所有 Bot 堆在同一点，也不会形成过密同心圆。
        const angle = index * 2.399963229728653;
        const radius = Math.min(maxRadius, spacing * Math.sqrt(index + 1));

        return {
            x: Number(base.x) + Math.cos(angle) * radius,
            y: Number(base.y),
            z: Number(base.z) + Math.sin(angle) * radius
        };
    }

    function isEntryRuntimeValid(entry) {
        try {
            if (!entry) return false;
            if (!isValidObject(entry.bot)) return false;
            if (!isValidObject(entry.player)) return false;
            const botTr = getTransformOf(entry.bot);
            let playerTr = getTransformOf(entry.player);
            if (!isReadablePtr(playerTr)) playerTr = safeReadPointer(entry.player, O.P_charContainer);
            if (!isReadablePtr(botTr) || !isReadablePtr(playerTr)) return false;
            const bp = getTransformPosition(botTr);
            const pp = getTransformPosition(playerTr);
            if (!bp || !pp) return false;
            entry.hasPlayer = true;
            return true;
        } catch (e) {
            return false;
        }
    }

    function collectValidBotKeys() {
        const rawKeys = Object.keys(Runtime.cache.trackedBots);
        const keys = [];
        const seenPlayers = {};
        let purged = 0;

        for (let i = 0; i < rawKeys.length; i++) {
            const key = rawKeys[i];
            const entry = Runtime.cache.trackedBots[key];

            if (!isEntryRuntimeValid(entry)) {
                delete Runtime.cache.trackedBots[key];
                purged++;
                continue;
            }

            const pkey = entry.player.toString();
            if (seenPlayers[pkey]) {
                // 同一个 Player 出现多个 Bot 缓存时，后面的通常是旧缓存，直接丢弃。
                delete Runtime.cache.trackedBots[key];
                purged++;
                continue;
            }

            seenPlayers[pkey] = true;
            keys.push(key);
        }

        if (purged > 0) {
            Runtime.stats.invalidPurged += purged;
            Runtime.stats.botsTracked = Object.keys(Runtime.cache.trackedBots).length;
            logOnce('purge_invalid', 'purged invalid/duplicate bot cache=' + purged + ', remain=' + keys.length, 500);
        }

        return keys;
    }

    function scheduleStabilityCheck(seq) {
        if (!Runtime.config.restickAirborne) return;
        const delay = Math.max(100, Number(Runtime.config.verifyAfterMs) || 600);

        const timerId = setTimeout(function () {
            try { verifyTeleportStability(seq); } catch (e) { recordError('verifyTeleportStability', e); }
        }, delay);

        Runtime.timers.push(timerId);
    }

    function verifyTeleportStability(seq) {
        if (!Runtime.enabled) return;

        const threshold = Math.max(0.2, Number(Runtime.config.airborneThreshold) || 1.8);
        const maxReground = Math.max(0, Number(Runtime.config.maxRegroundPerBot) || 1);
        const keys = collectValidBotKeys();

        let checked = 0;
        let high = 0;
        let reground = 0;
        const lines = [];

        for (let i = 0; i < keys.length; i++) {
            const entry = Runtime.cache.trackedBots[keys[i]];
            if (!entry || entry.lastTeleportSeq !== seq || !entry.lastFinalTarget) continue;

            checked++;
            const pos = readEntityPositions(entry.bot, entry.player);
            const finalTarget = entry.lastFinalTarget;
            const by = pos && pos.bot ? Number(pos.bot.y) : NaN;
            const py = pos && pos.player ? Number(pos.player.y) : NaN;
            const tooHigh = (isFinite(by) && by > Number(finalTarget.y) + threshold) ||
                            (isFinite(py) && py > Number(finalTarget.y) + threshold);

            if (!tooHigh) continue;
            high++;

            entry.regroundCount = entry.regroundCount || 0;
            if (entry.regroundCount >= maxReground) {
                lines.push('high_no_reground bot=' + entry.bot + ' pos=' + vec3ToString(pos && pos.bot) + ' final=' + vec3ToString(finalTarget));
                continue;
            }

            try {
                const fb = fallbackTransform(entry.bot, entry.player, finalTarget);
                const refresh = callBotRefresh(entry.bot, entry.player, finalTarget, { skipGroundSet: true });
                entry.regroundCount++;
                Runtime.stats.airborneReground++;
                reground++;
                lines.push('reground bot=' + entry.bot + ' pos=' + vec3ToString(pos && pos.bot) + ' final=' + vec3ToString(finalTarget) + ' ' + fb.method + ' ' + refresh.text);
            } catch (e) {
                lines.push('reground_err bot=' + entry.bot);
            }
        }

        const summary = 'stability seq=' + seq + ' checked=' + checked + ' high=' + high + ' reground=' + reground;
        log(summary);
        for (let j = 0; j < lines.length && j < 12; j++) log('  ' + lines[j]);
        send({ t: 'bot_ai_teleport_stability', summary: summary, details: lines });
    }

    function executeTeleport(reason) {
        if (!Runtime.enabled) return { ok: false, reason: 'disabled' };
        Runtime.stats.teleportRuns++;
        Runtime.cache.pendingTeleport = false;
        Runtime.cache.pendingReason = '';
        Runtime.cache.lastTeleportSeq++;
        const teleportSeq = Runtime.cache.lastTeleportSeq;

        scanAllPlayersFromGM();
        const baseTarget = prepareTarget(Runtime.config.target);
        const keys = collectValidBotKeys();
        makeDiagnosticSnapshot('pre', teleportSeq);
        let ok = 0;
        let fail = 0;
        let skip = 0;
        const lines = [];
        let batch = Number(Runtime.config.batchSize);
        if (!isFinite(batch) || batch <= 0) batch = keys.length;
        if (Runtime.config.processAllOnRpc !== false && String(reason || '').indexOf('rpc.teleport') >= 0) {
            batch = keys.length;
        }
        batch = Math.max(1, Math.min(keys.length, batch));

        for (let i = 0; i < keys.length && i < batch; i++) {
            const entry = Runtime.cache.trackedBots[keys[i]];
            if (!entry || !entry.hasPlayer) { skip++; continue; }
            const target = computeClusterTarget(baseTarget, i);
            const r = teleportOneBot(entry, target, i);
            if (r.ok) {
                ok++;
                entry.lastTeleportSeq = teleportSeq;
                entry.lastFinalTarget = r.finalTarget || target;
                entry.lastTeleportAt = Date.now();
                entry.regroundCount = 0;
                let posText = '';
                if (Runtime.config.positionDebug) {
                    posText = ' raw=' + vec3ToString(target) +
                              ' final=' + vec3ToString(r.finalTarget) +
                              ' graph=' + vec3ToString(r.graph) +
                              ' bot ' + vec3ToString(r.before && r.before.bot) + '->' + vec3ToString(r.after && r.after.bot) +
                              ' player ' + vec3ToString(r.before && r.before.player) + '->' + vec3ToString(r.after && r.after.player);
                }
                lines.push('#' + i + ' OK ' + r.method + ' bot=' + entry.bot + ' ai=' + (r.ai || '') + ' ' + (r.refresh || '') + posText);
            } else if (r.skipped) {
                skip++;
                if (Runtime.config.debug) lines.push('#' + i + ' SKIP ' + r.reason);
            } else {
                fail++;
                lines.push('#' + i + ' FAIL bot=' + entry.bot + ' ' + (r.reason || '') + ' ai=' + (r.ai || '') + ' aiFail=' + (r.aiFail || ''));
            }
        }

        Runtime.stats.lastSummary = 'reason=' + (reason || 'manual') + ' baseTarget=' + vec3ToString(baseTarget) + ' bots=' + keys.length + ' ok=' + ok + ' fail=' + fail + ' skip=' + skip;
        log(Runtime.stats.lastSummary);
        for (let j = 0; j < lines.length && j < 12; j++) log('  ' + lines[j]);
        send({ t: 'bot_ai_teleport_done', summary: Runtime.stats.lastSummary, details: lines });

        if (ok > 0) {
            makeDiagnosticSnapshot('post', teleportSeq);
            analyzeSnapshotDiff(teleportSeq, 'pre', 'post');
            scheduleDiagnosticSnapshots(teleportSeq);
            scheduleStabilityCheck(teleportSeq);
            try { monitorTick(); } catch (e) { recordError('monitorTick.afterTeleport', e); }
        }

        return { ok: true, target: baseTarget, trackedBots: keys.length, moved: ok, failed: fail, skipped: skip, details: lines };
    }

    function installHooks() {
        if (Runtime.initialized) return true;
        resolveModule();
        initIl2CppExports();
        if (!Runtime.il2cpp.class_from_name || !Runtime.il2cpp.class_get_type || !Runtime.il2cpp.type_get_object) {
            logOnce('il2cpp_exports_missing', 'IL2CPP export lookup incomplete; AI GetComponent(Type) may fail, hooks/fallback still continue', 1500);
        }
        initNativeFunctions();
        initTypes();

        const hBot = Interceptor.attach(Runtime.base.add(R.Bot_Update), {
            onEnter: function (args) {
                Runtime.stats.hookHits++;
                Runtime.stats.botUpdateHits++;
                try {
                    trackFromBot(args[0]);
                } catch (e) {
                    recordError('Bot.Update', e);
                }
            }
        });
        Runtime.hooks.push(hBot);

        const hPlayer = Interceptor.attach(Runtime.base.add(R.P_Update), {
            onEnter: function (args) {
                Runtime.stats.playerUpdateHits++;
                Runtime.cache.lastPlayerUpdateTs = nowMs();
                try {
                    if (Runtime.enabled && Runtime.cache.pendingTeleport && Runtime.config.executeOnPlayerUpdate) {
                        executeTeleport(Runtime.cache.pendingReason || 'Player.Update');
                    }
                    // v7: 强制从游戏 Update 驱动监控，不依赖 setInterval / 按钮。
                    monitorTickFromGameUpdate();
                } catch (e) {
                    recordError('Player.Update', e);
                }
            }
        });
        Runtime.hooks.push(hPlayer);

        try {
            const hAdd = Interceptor.attach(Runtime.base.add(R.GM_AddP), {
                onEnter: function (args) {
                    if (isReadablePtr(args[0])) Runtime.cache.gm = args[0];
                }
            });
            Runtime.hooks.push(hAdd);
        } catch (e) {
            logOnce('hook.addplayer.fail', 'AddPlayer hook skipped: ' + e.message, 2000);
        }

        try {
            const hMap = Interceptor.attach(Runtime.base.add(R.MM_MapGun), {
                onEnter: function (args) {
                    if (isReadablePtr(args[0])) Runtime.cache.mm = args[0];
                }
            });
            Runtime.hooks.push(hMap);
        } catch (e) {
            logOnce('hook.mapgun.fail', 'MapGunInit hook skipped: ' + e.message, 2000);
        }

        Runtime.initialized = true;
        log('hooks installed. base=' + Runtime.base);
        return true;
    }

    function cleanupHooks() {
        for (let i = 0; i < Runtime.hooks.length; i++) {
            try {
                const h = Runtime.hooks[i];
                if (h && h.detach) h.detach();
            } catch (e) {}
        }
        Runtime.hooks = [];
        Runtime.initialized = false;
    }

    function cleanupTimers() {
        for (let i = 0; i < Runtime.timers.length; i++) {
            try { clearInterval(Runtime.timers[i]); } catch (e) {}
        }
        Runtime.timers = [];
    }

    function enableFeature() {
        installHooks();
        Runtime.enabled = true;
        Runtime.stats.errorCount = 0;
        log('enabled target=' + vec3ToString(Runtime.config.target));
        return true;
    }

    function disableFeature() {
        Runtime.enabled = false;
        cleanupTimers();
        resetRuntime('disable');
        log('disabled');
        return true;
    }

    function cleanupFeature() {
        Runtime.enabled = false;
        Runtime.stats.cleanupCount++;
        try { cleanupTimers(); } catch (e) {}
        try { cleanupHooks(); } catch (e) {}
        resetRuntime('cleanup');
        log('cleanup done');
        return true;
    }

    function setConfig(config) {
        config = config || {};
        if (config.target) {
            const t = config.target;
            Runtime.config.target = {
                x: Number(t.x),
                y: Number(t.y),
                z: Number(t.z)
            };
        }
        const keys = [
            'batchSize', 'aiFirst', 'useRichAI', 'useAIBase', 'useIAstarAIProbe',
            'callSearchPath', 'callBotRefresh', 'transformFallback',
            'groundToNearestNode', 'useGraphNodeXZ', 'graphYOffset',
            'writeNativeTransformCache', 'positionDebug', 'spreadCluster',
            'clusterSpacing', 'clusterMaxRadius', 'pathSettingAfterTeleport',
            'verifyAfterMs', 'airborneThreshold', 'restickAirborne', 'maxRegroundPerBot',
            'monitorEnabled', 'monitorIntervalMs', 'monitorMaxBots', 'monitorDetail', 'driftThreshold',
            'diagEnabled', 'diagMaxBots', 'diagDetailLimit',
            'executeOnPlayerUpdate', 'debug', 'logIntervalMs'
        ];
        for (let i = 0; i < keys.length; i++) {
            const k = keys[i];
            if (Object.prototype.hasOwnProperty.call(config, k)) Runtime.config[k] = config[k];
        }
        log('config updated target=' + vec3ToString(Runtime.config.target));
        return true;
    }

    function buildStatus() {
        return {
            feature_id: Runtime.feature_id,
            enabled: Runtime.enabled,
            initialized: Runtime.initialized,
            generation: Runtime.generation,
            target: Runtime.config.target,
            config: Runtime.config,
            tracked_bots: Object.keys(Runtime.cache.trackedBots).length,
            tracked_players: Object.keys(Runtime.cache.trackedPlayers).length,
            pending_teleport: Runtime.cache.pendingTeleport,
            hook_hits: Runtime.stats.hookHits,
            bot_update_hits: Runtime.stats.botUpdateHits,
            player_update_hits: Runtime.stats.playerUpdateHits,
            ai_teleport_ok: Runtime.stats.aiTeleportOk,
            rich_ai_ok: Runtime.stats.richAiOk,
            ai_base_ok: Runtime.stats.aiBaseOk,
            fallback_ok: Runtime.stats.fallbackOk,
            skipped_no_ai: Runtime.stats.skippedNoAi,
            failed: Runtime.stats.failed,
            invalid_purged: Runtime.stats.invalidPurged,
            airborne_reground: Runtime.stats.airborneReground,
            monitor_ticks: Runtime.stats.monitorTicks,
            high_observed: Runtime.stats.highObserved,
            drift_observed: Runtime.stats.driftObserved,
            diag_runs: Runtime.stats.diagRuns,
            diag_path_recreated: Runtime.stats.diagPathRecreated,
            diag_next_pos_changed: Runtime.stats.diagNextPosChanged,
            diag_moved_from_final: Runtime.stats.diagMovedFromFinal,
            error_count: Runtime.stats.errorCount,
            last_error: Runtime.stats.lastError,
            last_reset_reason: Runtime.stats.lastResetReason,
            last_summary: Runtime.stats.lastSummary,
            types: {
                RichAI: Runtime.types.RichAI ? { klass: Runtime.types.RichAI.klass.toString(), type: Runtime.types.RichAI.type.toString() } : null,
                AIBase: Runtime.types.AIBase ? { klass: Runtime.types.AIBase.klass.toString(), type: Runtime.types.AIBase.type.toString() } : null,
                IAstarAI: Runtime.types.IAstarAI ? { klass: Runtime.types.IAstarAI.klass.toString(), type: Runtime.types.IAstarAI.type.toString() } : null
            }
        };
    }

    function debugDump() {
        const bots = [];
        const keys = Object.keys(Runtime.cache.trackedBots);
        for (let i = 0; i < keys.length && i < 40; i++) {
            const e = Runtime.cache.trackedBots[keys[i]];
            const ai = resolveAiComponent(e.bot);
            bots.push({
                bot: e.bot.toString(),
                player: e.player ? e.player.toString() : '0x0',
                hasPlayer: !!e.hasPlayer,
                aiKind: ai.kind,
                aiPtr: ai.ptr.toString(),
                aiReason: ai.reason,
                seeker: safeReadPointer(e.bot, O.Bot_seeker).toString(),
                path: safeReadPointer(e.bot, O.Bot_path).toString(),
                gNode_Nearset: safeReadPointer(e.bot, O.Bot_gNode_Nearset).toString(),
                gNode_Next: safeReadPointer(e.bot, O.Bot_gNode_Next).toString(),
                nextPathVectorID: safeReadS32(e.bot, O.Bot_nextPathVectorID, -1)
            });
        }
        return { status: buildStatus(), bots: bots };
    }

    rpc.exports = {
        enable: function () {
            return enableFeature();
        },
        disable: function () {
            return disableFeature();
        },
        cleanup: function () {
            return cleanupFeature();
        },
        status: function () {
            return buildStatus();
        },
        setConfig: function (config) {
            return setConfig(config || {});
        },
        set_config: function (config) {
            return setConfig(config || {});
        },
        reset: function (reason) {
            resetRuntime(reason || 'manual');
            return true;
        },
        teleport: function (target) {
            if (target) setConfig({ target: target });
            Runtime.stats.teleportRequests++;
            if (!Runtime.enabled) enableFeature();
            Runtime.cache.pendingTeleport = true;
            Runtime.cache.pendingReason = 'rpc.teleport';
            log('teleport requested target=' + vec3ToString(Runtime.config.target));
            if (!Runtime.config.executeOnPlayerUpdate) {
                return executeTeleport('rpc.teleport.direct');
            }
            return { ok: true, pending: true, target: Runtime.config.target };
        },
        probe: function () {
            if (!Runtime.enabled) enableFeature();
            scanAllPlayersFromGM();
            return debugDump();
        },
        debugDump: function () {
            return debugDump();
        },
        debug_dump: function () {
            return debugDump();
        }
    };

    log('loaded. call enable(), then teleport({x:13.6,y:14.1,z:0.1})');
})();
