// ============================================================
// 42_waypoint_probe / script.js   —— 路点体检（修改器功能）
//
// feature_id: waypoint_probe
//
// 做的事（只在功能开启时生效，关掉即恢复）：
//   1) 物理探针：按人机体积沿每条路点边扫一遍，判定 PASS/BLOCK/GAP/STEP/STEEP
//   2) 停战：把 bot 的 Player 队伍改成和本地玩家同队 + 全部无敌 + 清目标
//   3) 跟随：每个阵营挑 1 个 bot，把它的“敌人”指成本地玩家，让它自己寻路跟过来
//   4) 采样：定时记录 bot 所在节点，节点变化时记一条“走过这条边”
//
// 所有结果都通过 log 事件写进修改器日志（持久化），格式见 README。
//
// RVA 来源：IDA（GameAssembly.dll）与 06-测试/ucf_mod 里已验证的偏移
//   AstarPath_TypeInfo 0x00E2544C   Bot_TypeInfo 0x00E25F44
//   GameManager_TypeInfo 0x00E2933C
//   Physics.Raycast 0x00ABB0A0      Object.FindObjectsOfType(Type,bool) 0x004E9620
//   Component.get_transform 0x0032CF40  Transform.get_position_Injected 0x003F4280
// ============================================================
(function () {
    "use strict";

    var MODULE_NAME = "GameAssembly.dll";
    var CALL_CONV = "mscdecl";

    var RVA = {
        AstarPath_TypeInfo: 0x00E2544C,
        Bot_TypeInfo: 0x00E25F44,
        GameManager_TypeInfo: 0x00E2933C,
        Physics_Raycast: 0x00ABB0A0,
        Entity_SetTeam: 0x00B3F940,
        Bot_CheckAttackTarget: 0x00B2DD80,
        HealthData_Hurt: 0x00AE45B0,
        Object_FindObjectsOfType: 0x004E9620,
        Component_get_transform: 0x0032CF40,
        Transform_get_position_Injected: 0x003F4280,
        Player_get_isMyPlayer: 0x00B55FD0
    };

    var OFF = {
        Il2CppClass_static_fields: 0x5C,
        AstarPath_active: 0x0C,
        AstarPath_data: 0x10,
        AstarData_graphs: 0x20,
        Array_length: 0x0C,
        Array_items: 0x10,
        PointGraph_nodes: 0xE8,
        PointGraph_nodeCount: 0xEC,
        GraphNode_flags: 0x0C,
        GraphNode_position: 0x14,
        PointNode_connections: 0x20,
        Connection_stride: 12,
        Bot_thisPlayer: 0x24,
        Bot_enemyInfo: 0x28,
        BotEnemyInfo_enemy: 0x0C,
        BotEnemyInfo_isPlayer: 0x18,
        BotEnemyInfo_enemyPos: 0x1C,
        BotEnemyInfo_distance: 0x28,
        BotEnemyInfo_findTime: 0x10,
        BotEnemyInfo_lastLostTime: 0x14,
        BotEnemyInfo_nextCheckVisibleTime: 0x48,
        Bot_stopAllBot: 0x0C,
        Bot_tryFindEnemy: 0x2C,
        Bot_faceToEnemy: 0x30,
        Bot_nextCheckEnemyInViewTime: 0x38,
        Bot_nextAttackTime: 0x3C,
        Entity_isInvincible: 0x18,
        Entity_team: 0x20,
        GameManager_myPlayer: 0x00
    };

    var V = { PASS: 0, BLOCK: 1, GAP: 2, STEP: 3, DROP: 4, STEEP: 5 };
    var VNAME = ["PASS", "BLOCK", "GAP", "STEP", "DROP", "STEEP"];

    var Runtime = {
        feature_id: "waypoint_probe",
        enabled: false,
        base: null,
        config: {
            pacify: false,
            freeze: false,
            follow: false,
            walk: false,
            sample_ms: 300
        },
        native: {
            ready: false,
            classGetType: null,
            findObjects: null,
            getTransform: null,
            getPosition: null,
            raycast: null,
            isMyPlayer: null
        },
        hooks: {},
        timers: [],
        probe: { edges: [], summary: {}, ranAt: 0, fp: "" },
        botCache: [],
        botCacheAt: 0,
        nodeCache: [],
        nodeCacheG: null,
        followLast: {},
        lastNode: {},
        freezeLogged: false,
        nextPick: 0,
        savedInv: {},
        bots: 0,
        me: null,
        myTeam: null,
        noted: {},
        stats: {
            errors: 0,
            rayErrors: 0,
            lastErrorKey: "",
            lastErrorAt: 0,
            samples: 0,
            traversals: 0,
            linked0: 0,
            pacifyWrites: 0,
            followMoves: 0,
            lastError: ""
        },
        lastPos: {}
    };

    function log(level, msg) {
        try {
            console.log("[waypoint_probe][" + level + "] " + msg);
        } catch (e) {}
        try {
            send({ type: "log", level: level, module: "waypoint_probe", message: msg });
        } catch (e) {}
    }

    function setError(where, err) {
        var msg = where + ": " + (err && err.message ? err.message : String(err));
        Runtime.stats.errors = (Runtime.stats.errors || 0) + 1;
        Runtime.stats.lastError = msg;
        var now = Date.now();
        /* 同一个错误 3 秒内只写一次日志，避免 100ms 定时器把日志刷爆 */
        if (msg === Runtime.stats.lastErrorKey && (now - Runtime.stats.lastErrorAt) < 3000) return;
        Runtime.stats.lastErrorKey = msg;
        Runtime.stats.lastErrorAt = now;
        log("error", msg);
    }

    /* 只报一次的状态提示（比如“bot 类还没初始化”），不刷屏 */
    function noteOnce(key, msg) {
        if (!Runtime.noted) Runtime.noted = {};
        if (Runtime.noted[key]) return;
        Runtime.noted[key] = 1;
        log("warn", msg);
    }

    function fmt(v) {
        return (Math.round(v * 100) / 100).toFixed(2);
    }

    /* ---------------- native ---------------- */
    function buildRaycastStub(target) {
        var code = Memory.alloc(128);
        Memory.protect(code, 128, "rwx");
        var head = [
            0x55,                   // push ebp
            0x89, 0xE5,             // mov ebp, esp
            0x6A, 0x00,             // push 0            (MethodInfo*)
            0xFF, 0x75, 0x18,       // push [ebp+0x18]   mask
            0xFF, 0x75, 0x14,       // push [ebp+0x14]   maxDistance
            0xFF, 0x75, 0x10,       // push [ebp+0x10]   hit ptr
            0x8B, 0x45, 0x0C,       // mov eax,[ebp+0x0C] dir ptr
            0xFF, 0x70, 0x08,       // push [eax+8]
            0xFF, 0x70, 0x04,       // push [eax+4]
            0xFF, 0x30,             // push [eax]
            0x8B, 0x45, 0x08,       // mov eax,[ebp+0x08] origin ptr
            0xFF, 0x70, 0x08,
            0xFF, 0x70, 0x04,
            0xFF, 0x30,
            0xB8                    // mov eax, imm32（目标地址）
        ];
        var tail = [0x83, 0xC4, 0x28, 0x5D, 0xC3];   // add esp,0x28 / pop ebp / ret（10 个 dword：2×Vector3 + ptr + float + int + MethodInfo）
        code.writeByteArray(head);
        code.add(head.length).writePointer(target);
        code.add(head.length + 4).writeByteArray([0xFF, 0xD0]);   // call eax
        code.add(head.length + 6).writeByteArray(tail);
        return code;
    }

    // Frida 17 移除了 Module.getExportByName / Module.findExportByName；
    // 新 API 是 mod.getExportByName 或 Module.getGlobalExportByName。这里三种都试。
    function resolveExport(mod, name) {
        var fn = null;
        if (mod && typeof mod.getExportByName === "function") fn = mod.getExportByName;
        else if (mod && typeof mod.findExportByName === "function") fn = mod.findExportByName;
        if (fn) {
            try { var a = fn.call(mod, name); if (a) return a; } catch (e) {}
        }
        if (typeof Module.getGlobalExportByName === "function") {
            try { var b = Module.getGlobalExportByName(name); if (b) return b; } catch (e2) {}
        }
        if (typeof Module.findGlobalExportByName === "function") {
            try { var c = Module.findGlobalExportByName(name); if (c) return c; } catch (e3) {}
        }
        return null;
    }

    function initNative() {
        if (Runtime.native.ready) return true;
        var mod = Process.findModuleByName(MODULE_NAME);
        if (!mod) { Runtime.stats.lastError = "GameAssembly.dll not found"; return false; }
        if (Process.arch !== "ia32" || Process.pointerSize !== 4) {
            Runtime.stats.lastError = "not 32-bit: " + Process.arch;
            return false;
        }
        Runtime.base = mod.base;
        try {
            var getType = resolveExport(mod, "il2cpp_class_get_type");
            if (!getType) throw new Error("il2cpp_class_get_type export not found");
            Runtime.native.classGetType = new NativeFunction(getType, "pointer", ["pointer"], CALL_CONV);
            /* il2cpp 反射 API：按名字找类，比 TypeInfo 静态槽稳（对局外也有效） */
            var eDomain = resolveExport(mod, "il2cpp_domain_get");
            var eAsms = resolveExport(mod, "il2cpp_domain_get_assemblies");
            var eImage = resolveExport(mod, "il2cpp_assembly_get_image");
            var eClass = resolveExport(mod, "il2cpp_class_from_name");
            if (eDomain && eAsms && eImage && eClass) {
                Runtime.native.domainGet = new NativeFunction(eDomain, "pointer", [], CALL_CONV);
                Runtime.native.domainGetAssemblies = new NativeFunction(
                    eAsms, "pointer", ["pointer", "pointer"], CALL_CONV);
                Runtime.native.assemblyGetImage = new NativeFunction(
                    eImage, "pointer", ["pointer"], CALL_CONV);
                Runtime.native.classFromName = new NativeFunction(
                    eClass, "pointer", ["pointer", "pointer", "pointer"], CALL_CONV);
                var eTypeObj = resolveExport(mod, "il2cpp_type_get_object");
                if (eTypeObj) {
                    /* Object.FindObjectsOfType 要的是 System.Type 对象，不是 Il2CppType* */
                    Runtime.native.typeGetObject = new NativeFunction(eTypeObj, "pointer", ["pointer"], CALL_CONV);
                } else {
                    log("warn", "il2cpp_type_get_object 不可用，FindObjectsOfType 会失败");
                }
            } else {
                log("warn", "il2cpp 反射 API 不全，只能退回 TypeInfo 静态槽");
            }
            var eThreadAttach = resolveExport(mod, "il2cpp_thread_attach");
            if (eThreadAttach && Runtime.native.domainGet) {
                /* 外来线程调用托管代码前必须挂到 il2cpp 域上 */
                var fAttach = new NativeFunction(eThreadAttach, "pointer", ["pointer"], CALL_CONV);
                var dom = Runtime.native.domainGet();
                if (dom && !dom.isNull()) log("info", "thread_attach=" + fAttach(dom));
            }
            Runtime.native.findObjects = new NativeFunction(
                Runtime.base.add(RVA.Object_FindObjectsOfType), "pointer",
                ["pointer", "uint8", "pointer"], CALL_CONV);
            Runtime.native.getTransform = new NativeFunction(
                Runtime.base.add(RVA.Component_get_transform), "pointer",
                ["pointer", "pointer"], CALL_CONV);
            Runtime.native.getPosition = new NativeFunction(
                Runtime.base.add(RVA.Transform_get_position_Injected), "void",
                ["pointer", "pointer", "pointer"], CALL_CONV);
            Runtime.native.setTeam = new NativeFunction(
                Runtime.base.add(RVA.Entity_SetTeam), "void",
                ["pointer", "int", "pointer"], CALL_CONV);
            Runtime.native.isMyPlayer = new NativeFunction(
                Runtime.base.add(RVA.Player_get_isMyPlayer), "bool",
                ["pointer", "pointer"], CALL_CONV);
            var stub = buildRaycastStub(Runtime.base.add(RVA.Physics_Raycast));
            Runtime.native.raycast = new NativeFunction(stub, "uint8",
                ["pointer", "pointer", "pointer", "float", "int"], CALL_CONV);
            Runtime.native.ready = true;
            log("info", "native ready");
            return true;
        } catch (e) {
            setError("initNative", e);
            Runtime.native.ready = false;
            return false;
        }
    }

    /* 指针可用性判断：0x10000~0x7FFF0000 之外一律当成垃圾（对局外静态字段常常是脏数据） */
    function isPtr(p) {
        if (!p) return false;
        try {
            var v = parseInt(p.toString(), 16);
            return v >= 0x00010000 && v <= 0x7FFF0000;
        } catch (e) { return false; }
    }

    /* 任何一次解引用都可能 AV（Frida 会抛成 JS 异常），统一兜住 */
    function safe(fn, dflt) {
        try { return fn(); } catch (e) { return dflt; }
    }

    /* Il2CppClass 布局（il2cpp.h，32 位）：+0x08 name，+0x5C static_fields */
    function klassName(klass) {
        return safe(function () {
            var np = klass.add(0x08).readPointer();
            if (!isPtr(np)) return "";
            var s = np.readUtf8String();          /* 必须读到 \0 为止；给长度会读进相邻内存报错 */
            if (!s || s.length === 0 || s.length > 60) return "";
            if (!/^[A-Za-z_][A-Za-z0-9_`<>.,+\[\]]*$/.test(s)) return "";
            return s;
        }, "");
    }

    /* 所有程序集镜像缓存（il2cpp_domain_get_assemblies 只取一次） */
    function assemblyImages() {
        if (Runtime.images) return Runtime.images;
        var out = [];
        Runtime.images = null;
        var dom = safe(function () { return Runtime.native.domainGet(); }, null);
        if (!isPtr(dom)) return null;
        var cnt = Memory.alloc(4);
        cnt.writeU32(0);
        var arr = safe(function () { return Runtime.native.domainGetAssemblies(dom, cnt); }, null);
        if (!isPtr(arr)) return null;
        var n = cnt.readU32(), i;
        if (n > 400) n = 400;
        for (i = 0; i < n; i++) {
            var asm = safe(function () { return arr.add(i * 4).readPointer(); }, null);
            if (!isPtr(asm)) continue;
            var img = safe(function () { return Runtime.native.assemblyGetImage(asm); }, null);
            if (isPtr(img)) out.push(img);
        }
        Runtime.images = out;
        return out;
    }

    /* 按名字找 Il2CppClass*：和 TypeInfo 静态槽不同，程序集一加载就能找到，不用等对局 */
    function findClassByName(name) {
        var imgs = assemblyImages();
        if (!imgs) return null;
        var nmBuf = Memory.allocUtf8String(name);
        var namespaces = ["", "UnityEngine", "UnityEngine.AI", "Pathfinding"];
        var n, i, c;
        for (n = 0; n < namespaces.length; n++) {
            var nsBuf = Memory.allocUtf8String(namespaces[n]);
            for (i = 0; i < imgs.length; i++) {
                c = safe(function () { return Runtime.native.classFromName(imgs[i], nsBuf, nmBuf); }, null);
                if (isPtr(c) && klassName(c) === name) return c;
            }
        }
        return null;
    }

    /* 注意：这个游戏带 CodeStage Anti-Cheat Toolkit，会把我们改过的函数入口（E9 跳转）
       自动还原序号，实测 Interceptor.replace 过几分钟就被它改回去，还会让调用方跳到已释放内存上崩溃。
       所以这里**不做任何代码 patch**，全部改用纯数据写入：
         Bot.stopAllBot（静态）→ 冻结 AI；Bot.enemyInfo → 指定目标；Entity.isInvincible → 无敌。 */


    /* Entity.SetTeam 会同时维护 GameManager.entityBL_Alive / entityGR_Alive 两个列表；
       直接写 Entity.team 字段列表不会更新，人机选敌（按列表挑）看不到变化 —— 这是停战无效的根因 */
    function setEntityTeam(pl, team) {
        return safe(function () {
            if (!Runtime.native.setTeam) return false;
            Runtime.native.setTeam(pl, team | 0, ptr(0));
            return true;
        }, false);
    }

    function classPtr(name, rva) {
        if (!Runtime.classCache) Runtime.classCache = {};
        if (Runtime.classCache[name]) return Runtime.classCache[name];
        var k = findClassByName(name);
        if (!k && rva) {
            k = safe(function () {
                var p = Runtime.base.add(rva).readPointer();
                if (!isPtr(p)) return null;
                return klassName(p) === name ? p : null;
            }, null);
        }
        if (k) Runtime.classCache[name] = k;
        return k || null;
    }

    function staticFields(klass) {
        return safe(function () {
            if (!klass || klass.isNull()) return ptr(0);
            var sf = klass.add(OFF.Il2CppClass_static_fields).readPointer();
            return isPtr(sf) ? sf : ptr(0);
        }, ptr(0));
    }

    /* ---------------- 点图 ---------------- */
    function astarPath() {
        return safe(function () {
            var sf = staticFields(classPtr("AstarPath", RVA.AstarPath_TypeInfo));
            if (sf.isNull()) return null;
            var a = sf.add(OFF.AstarPath_active).readPointer();
            return isPtr(a) ? a : null;
        }, null);
    }

    function pointGraph() {
        return safe(function () {
            var a = astarPath();
            if (!a) return null;
            var data = a.add(OFF.AstarPath_data).readPointer();
            if (!isPtr(data)) return null;
            var graphs = data.add(OFF.AstarData_graphs).readPointer();
            if (!isPtr(graphs)) return null;
            var n = graphs.add(OFF.Array_length).readInt();
            if (n <= 0 || n > 64) return null;
            var best = null, bestCount = 0, i;
            for (i = 0; i < n && i < 16; i++) {
                var g = graphs.add(OFF.Array_items + i * 4).readPointer();
                if (!isPtr(g)) continue;
                var c = g.add(OFF.PointGraph_nodeCount).readInt();
                if (c > bestCount && c < 1000000) { bestCount = c; best = g; }
            }
            return best;
        }, null);
    }

    function nodeCount(g) {
        return g ? g.add(OFF.PointGraph_nodeCount).readInt() : 0;
    }

    function nodeAt(g, i) {
        return safe(function () {
            if (!isPtr(g)) return null;
            var arr = g.add(OFF.PointGraph_nodes).readPointer();
            if (!isPtr(arr)) return null;
            var p = arr.add(OFF.Array_items + i * 4).readPointer();
            return isPtr(p) ? p : null;
        }, null);
    }

    function nodePos(node) {
        return safe(function () {
            var b = node.add(OFF.GraphNode_position);
            return {
                x: b.readS32() / 1000.0,
                y: b.add(4).readS32() / 1000.0,
                z: b.add(8).readS32() / 1000.0
            };
        }, null);
    }

    function nodeWalkable(node) {
        return (node.add(OFF.GraphNode_flags).readU32() & 1) === 1;
    }

    function connCount(node) {
        var arr = node.add(OFF.PointNode_connections).readPointer();
        if (arr.isNull()) return 0;
        return arr.add(OFF.Array_length).readInt();
    }

    function connNode(node, j) {
        var arr = node.add(OFF.PointNode_connections).readPointer();
        if (arr.isNull()) return null;
        var p = arr.add(OFF.Array_items + j * OFF.Connection_stride).readPointer();
        return p.isNull() ? null : p;
    }

    function hasEdge(a, b) {
        var n = connCount(a), i;
        for (i = 0; i < n; i++) {
            if (connNode(a, i) && connNode(a, i).equals(b)) return true;
        }
        return false;
    }

    /* ---------------- 射线 ---------------- */
    var hitBuf = null, orgBuf = null, dirBuf = null;

    function ensureRayBuffers() {
        if (!hitBuf) {
            hitBuf = Memory.alloc(128);
            orgBuf = Memory.alloc(12);
            dirBuf = Memory.alloc(12);
        }
    }

    function raycast(o, d, maxDist) {
        ensureRayBuffers();
        orgBuf.writeFloat(o.x); orgBuf.add(4).writeFloat(o.y); orgBuf.add(8).writeFloat(o.z);
        dirBuf.writeFloat(d.x); dirBuf.add(4).writeFloat(d.y); dirBuf.add(8).writeFloat(d.z);
        var ok;
        try {
            ok = Runtime.native.raycast(orgBuf, dirBuf, hitBuf, maxDist, 1);
        } catch (e) {
            Runtime.stats.rayErrors = (Runtime.stats.rayErrors || 0) + 1;
            noteOnce("raycast", "Physics.Raycast 调用失败：" + (e && e.message ? e.message : String(e)));
            return null;
        }
        if (!ok) return null;
        return {
            x: hitBuf.readFloat(),
            y: hitBuf.add(4).readFloat(),
            z: hitBuf.add(8).readFloat(),
            nx: hitBuf.add(12).readFloat(),
            ny: hitBuf.add(16).readFloat(),
            nz: hitBuf.add(20).readFloat()
        };
    }

    function dist2D(a, b) {
        var dx = b.x - a.x, dz = b.z - a.z;
        return Math.sqrt(dx * dx + dz * dz);
    }

    function checkEdge(A, B) {
        var out = { v: V.PASS, gmax: 0, block: 0, gap: 0 };
        var d = dist2D(A, B);
        if (d < 0.01) return out;
        var down = { x: 0, y: -1, z: 0 };
        /* 基准偏移：节点常常悬在地面上方 */
        var h0 = raycast({ x: A.x, y: A.y + 1.6, z: A.z }, down, 8.0);
        if (!h0) { out.v = V.GAP; out.gap = 1; return out; }
        var base = h0.y - A.y;
        var ns = Math.floor(d / 0.5) + 2;
        if (ns > 16) ns = 16;
        var i, k;
        for (i = 0; i < ns; i++) {
            var t = i / (ns - 1);
            var p = { x: A.x + (B.x - A.x) * t, y: A.y + (B.y - A.y) * t, z: A.z + (B.z - A.z) * t };
            var h = raycast({ x: p.x, y: p.y + 1.6, z: p.z }, down, 8.0);
            if (!h) { out.gap = 1; continue; }
            var dh = (h.y - p.y) - base;
            if (Math.abs(dh) > out.gmax) out.gmax = Math.abs(dh);
            if (h.ny > 0 && h.ny < 0.7071 && Math.abs(dh) > 0.25) out.block = 1;
            if (i + 1 < ns) {
                var t2 = (i + 1) / (ns - 1);
                var np = { x: A.x + (B.x - A.x) * t2, y: p.y, z: A.z + (B.z - A.z) * t2 };
                var dx = np.x - p.x, dz = np.z - p.z;
                var nd = Math.sqrt(dx * dx + dz * dz);
                if (nd > 0.001) {
                    var dir = { x: dx / nd, y: 0, z: dz / nd };
                    var hs = [0.35, 1.15];
                    for (k = 0; k < 2; k++) {
                        var ro = { x: p.x, y: h.y + hs[k], z: p.z };
                        var rh = raycast(ro, dir, nd + 0.15);
                        if (rh) {
                            var dd = (rh.x - ro.x) * dir.x + (rh.z - ro.z) * dir.z;
                            if (dd < nd - 0.20) out.block = 1;
                        }
                    }
                }
            }
        }
        if (out.block) out.v = V.BLOCK;
        else if (out.gap) out.v = V.GAP;
        else if (out.gmax > 0.75) out.v = V.STEP;
        else if (out.gmax > 0.35) out.v = V.STEEP;
        return out;
    }

    /* ---------------- 探针 ---------------- */
    function runProbe() {
        if (!Runtime.enabled) {
            return { ok: false, reason: "feature_disabled" };
        }
        if (!initNative()) return { ok: false, reason: Runtime.stats.lastError || "native_not_ready" };
        var g = pointGraph();
        if (!g) return { ok: false, reason: "no_point_graph" };
        var n = nodeCount(g);
        if (n <= 0) return { ok: false, reason: "empty_graph" };

        var rayBefore = Runtime.stats.rayErrors || 0;
        raycast({ x: 0, y: 50, z: 0 }, { x: 0, y: -1, z: 0 }, 500);
        if ((Runtime.stats.rayErrors || 0) > rayBefore) {
            log("error", "PROBE|ABORT|Physics.Raycast 不可用，探针中止（否则整张图会被误判成 GAP）");
            return { ok: false, reason: "raycast_unavailable" };
        }

        var edges = [], counts = [0, 0, 0, 0, 0, 0];
        var idMap = {};
        var i, j;
        for (i = 0; i < n; i++) {
            var nd0 = nodeAt(g, i);
            if (nd0) idMap[nd0.toString()] = i;
        }
        for (i = 0; i < n; i++) {
            var a = nodeAt(g, i);
            if (!a) continue;
            var A = nodePos(a);
            if (!A) continue;
            var cn = connCount(a);
            for (j = 0; j < cn; j++) {
                var b = connNode(a, j);
                if (!b) continue;
                var bi = idMap[b.toString()];
                if (bi === undefined || bi <= i) continue;   /* 无向边只取一次 */
                var B = nodePos(b);
                if (!B) continue;
                var r;
                if (!nodeWalkable(a) || !nodeWalkable(b)) {
                    r = { v: V.BLOCK, gmax: 0, block: 1, gap: 0 };
                } else {
                    r = checkEdge(A, B);
                }
                counts[r.v] += 1;
                edges.push({ a: i, b: bi, v: VNAME[r.v], ax: A.x, ay: A.y, az: A.z, bx: B.x, by: B.y, bz: B.z,
                             d: dist2D(A, B), gmax: r.gmax, block: r.block, gap: r.gap });
            }
        }

        Runtime.probe.edges = edges;
        Runtime.probe.summary = {
            total: edges.length, pass: counts[0], block: counts[1], gap: counts[2],
            step: counts[3], drop: counts[4], steep: counts[5]
        };
        Runtime.probe.ranAt = Date.now();

        log("info", "PROBE|SUMMARY|total=" + edges.length + "|pass=" + counts[0] + "|block=" + counts[1] +
            "|gap=" + counts[2] + "|step=" + counts[3] + "|drop=" + counts[4] + "|steep=" + counts[5] +
            "|nodes=" + n);

        /* 分块写进日志：每行 20 条，够离线分析 */
        var chunk = [], ci;
        for (ci = 0; ci < edges.length; ci++) {
            var e = edges[ci];
            chunk.push([e.a, e.b, e.ax, e.ay, e.az, e.bx, e.by, e.bz, e.d, e.v, e.gmax, e.block, e.gap].join(","));
            if (chunk.length >= 20 || ci === edges.length - 1) {
                log("info", "PROBE|EDGES|" + chunk.join(";"));
                chunk = [];
            }
        }
        return { ok: true, summary: Runtime.probe.summary };
    }

    /* ---------------- bot ---------------- */
    function botClass() { return classPtr("Bot", RVA.Bot_TypeInfo); }

    /* 取 Il2CppType* 并缓存；类还没初始化时返回 null，绝不把空指针丢给 il2cpp */
    function typeOfClass(name) {
        var key = "type_" + name;
        if (Runtime.native[key]) return Runtime.native[key];
        var k = classPtr(name);
        if (!k) { noteOnce("klass_" + name, name + " 类还没加载（按名字也没找到）"); return null; }
        var t = safe(function () { return Runtime.native.classGetType(k); }, null);
        if (!t || t.isNull() || !isPtr(t)) { noteOnce("type_" + name, name + " il2cpp_class_get_type 返回无效指针"); return null; }
        Runtime.native[key] = t;
        log("info", name + " class=" + k + " type=" + t);
        return t;
    }

    /* Il2CppType* -> System.Type 托管对象（FindObjectsOfType 的参数） */
    function systemTypeOf(name) {
        var key = "stype_" + name;
        if (Runtime.native[key]) return Runtime.native[key];
        var t = typeOfClass(name);
        if (!t) return null;
        if (!Runtime.native.typeGetObject) { noteOnce("notypeobj", "il2cpp_type_get_object 不可用"); return null; }
        var o = safe(function () { return Runtime.native.typeGetObject(t); }, null);
        if (!isPtr(o)) { noteOnce("stype_" + name, name + " 转 System.Type 失败"); return null; }
        Runtime.native[key] = o;
        return o;
    }

    function findObjectsOf(name) {
        return safe(function () {
            var type = systemTypeOf(name);
            if (!type) return [];
            return readObjectArray(Runtime.native.findObjects(type, 1, ptr(0)));
        }, []);
    }

    function readObjectArray(arr) {
        var out = [];
        if (!isPtr(arr)) return out;
        var n = arr.add(OFF.Array_length).readInt();
        if (n <= 0 || n > 4096) return out;
        var i;
        for (i = 0; i < n; i++) {
            var p = arr.add(OFF.Array_items + i * 4).readPointer();
            if (isPtr(p)) out.push(p);
        }
        return out;
    }

    function allBots() {
        return findObjectsOf("Bot");
    }

    function botPlayer(b) {
        var p = b.add(OFF.Bot_thisPlayer).readPointer();
        return p.isNull() ? null : p;
    }

    function playerPos(p) {
        return safe(function () {
            if (!isPtr(p)) return null;
            var tr = Runtime.native.getTransform(p, ptr(0));
            if (!isPtr(tr)) return null;
            var buf = Memory.alloc(12);
            Runtime.native.getPosition(tr, buf, ptr(0));
            return { x: buf.readFloat(), y: buf.add(4).readFloat(), z: buf.add(8).readFloat() };
        }, null);
    }

    function myPlayer() {
        if (isPtr(Runtime.me)) return Runtime.me;
        Runtime.me = null;
        return safe(function () {
            var sf = staticFields(classPtr("GameManager", RVA.GameManager_TypeInfo));
            if (!sf.isNull()) {
                var me = sf.add(OFF.GameManager_myPlayer).readPointer();
                if (isPtr(me)) { Runtime.me = me; return me; }
            }
            /* 兜底：遍历 Player 调 isMyPlayer */
            var players = allPlayers();
            var i;
            for (i = 0; i < players.length; i++) {
                if (Runtime.native.isMyPlayer(players[i], ptr(0))) { Runtime.me = players[i]; return players[i]; }
            }
            return null;
        }, null);
    }

    function allPlayers() {
        return findObjectsOf("Player");
    }

    function remember(key, value) {
        if (Runtime.savedInv[key] === undefined) Runtime.savedInv[key] = value;
    }

    function restoreAll() {
        var k, keys = Object.keys(Runtime.savedInv);
        for (k = 0; k < keys.length; k++) {
            var rec = Runtime.savedInv[keys[k]];
            if (rec && rec.sf) {
                safe(function () { rec.sf.add(OFF.Bot_stopAllBot).writeU8(rec.stop ? 1 : 0); });
                continue;
            }
            if (!rec || !rec.p) continue;
            try {
                if (rec.inv !== undefined) rec.p.add(OFF.Entity_isInvincible).writeU8(rec.inv);
                if (rec.team !== undefined) {
                    var cur = safe(function () { return rec.p.add(OFF.Entity_team).readS32(); }, rec.team);
                    if (cur !== rec.team) setEntityTeam(rec.p, rec.team);
                    else rec.p.add(OFF.Entity_team).writeS32(rec.team);
                }
            } catch (e) {}
        }
        Runtime.savedInv = {};
        Runtime.myTeam = null;
    }

    function botStaticFields() {
        return staticFields(classPtr("Bot", RVA.Bot_TypeInfo));
    }

    /* Bot.stopAllBot（静态 +0xC）：游戏自带的“所有人机暂停”开关，24-人机暂停 功能验证过 */
    function setStopAllBot(on) {
        var sfb = botStaticFields();
        if (sfb.isNull()) { noteOnce("nobotstatic", "Bot 静态字段读不到，停不住人机"); return false; }
        if (Runtime.savedInv["__bot"] === undefined) {
            Runtime.savedInv["__bot"] = { sf: sfb, stop: sfb.add(OFF.Bot_stopAllBot).readU8() };
        }
        var cur = sfb.add(OFF.Bot_stopAllBot).readU8();
        if (on && cur === 0) { sfb.add(OFF.Bot_stopAllBot).writeU8(1); return true; }
        if (!on && cur !== 0 && Runtime.savedInv["__bot"].stop === 0) {
            sfb.add(OFF.Bot_stopAllBot).writeU8(0);
            return true;
        }
        return false;
    }

    function pacifyOnce() {
        var me = myPlayer();
        var bots = allBots();
        var i, changed = 0;
        if (!me && bots.length === 0) {
            /* 还没进对局：没有任何可操作对象，安静退出，别每 100ms 报一次错 */
            noteOnce("no_game", "当前没有玩家/人机（应该还没进入对局）");
            return;
        }
        var following = !!Runtime.config.follow;
        /* 只开停战（没开跟随）时，直接用游戏自带的全局暂停；一开跟随就得解冻，否则人机不能动 */
        if (Runtime.config.pacify && !following) {
            if (setStopAllBot(true)) log("info", "Bot.stopAllBot = true（人机全部暂停）");
        } else {
            setStopAllBot(false);
        }
        if (me && Runtime.myTeam === null) {
            Runtime.myTeam = me.add(OFF.Entity_team).readS32();
            log("info", "my_team=" + Runtime.myTeam);
        }
        var followerCount = 0;
        for (i = 0; i < bots.length; i++) {
            var b = bots[i];
            var pl = botPlayer(b);
            if (!pl) continue;
            var isFollower = following;   /* 跟随模式下目标由 followOnce 统一写，这里别再清 */
            if (isFollower) followerCount += 1;
            var k = b.toString();
            if (!Runtime.savedInv[k]) {
                Runtime.savedInv[k] = {
                    p: pl,
                    team: safe(function () { return pl.add(OFF.Entity_team).readS32(); }, 0),
                    inv: safe(function () { return pl.add(OFF.Entity_isInvincible).readU8(); }, 0)
                };
            }
            /* 默认不动阵营（改 team 会动到 BL/GR 存活列表，可能触发回合结算），
               停火靠上面 hook 掉 CheckAttackTarget + 清目标 */
            if (safe(function () { return pl.add(OFF.Entity_isInvincible).readU8(); }, 0) === 0) {
                safe(function () { pl.add(OFF.Entity_isInvincible).writeU8(1); }, null);
            }
            if (!isFollower) {
                /* 清掉 AI 的当前目标 + 把“下一次找敌人”的时间推到很久以后，它就不会再开战 */
                var info = safe(function () { return b.add(OFF.Bot_enemyInfo).readPointer(); }, null);
                if (isPtr(info)) {
                    safe(function () { info.add(OFF.BotEnemyInfo_enemy).writePointer(ptr(0)); }, null);
                }
                safe(function () { b.add(OFF.Bot_tryFindEnemy).writePointer(ptr(0)); }, null);
                safe(function () { b.add(OFF.Bot_nextCheckEnemyInViewTime).writeFloat(1.0e9); }, null);
            }
            safe(function () { b.add(OFF.Bot_faceToEnemy).writeU8(0); }, null);
            safe(function () { b.add(OFF.Bot_nextAttackTime).writeFloat(1.0e9); }, null);
        }
        if (following && followerCount === 0) {
            noteOnce("nofollower", "跟随打开了但一个跟随者都没选上（看 follow picked 那行）");
        }
        Runtime.bots = bots.length;
        if (me) {
            var mk = me.toString();
            if (!Runtime.savedInv[mk]) Runtime.savedInv[mk] = { p: me, inv: me.add(OFF.Entity_isInvincible).readU8() };
            if (me.add(OFF.Entity_isInvincible).readU8() === 0) me.add(OFF.Entity_isInvincible).writeU8(1);
        }
        if (changed) {
            Runtime.stats.pacifyWrites += changed;
            if (Runtime.stats.pacifyWrites < 40) log("info", "pacify bots=" + bots.length + " changed=" + changed);
        }
    }

    /* FindObjectsOfType 很贵，缓存 1 秒；人机列表变化不大 */
    function allBotsCached(maxAgeMs) {
        var now = Date.now();
        var age = Runtime.botCacheAt ? (now - Runtime.botCacheAt) : 1e9;
        if (Runtime.botCache.length === 0 || age >= (maxAgeMs || 1000)) {
            Runtime.botCache = allBots();
            Runtime.botCacheAt = now;
        }
        return Runtime.botCache;
    }

    /* 节点坐标不会变，缓存起来，别每次采样都重读 786 个节点 */
    function nodePositions(g) {
        var n = nodeCount(g);
        if (Runtime.nodeCacheG && Runtime.nodeCacheG.equals(g) && Runtime.nodeCache.length === n) {
            return Runtime.nodeCache;
        }
        var out = [], i;
        for (i = 0; i < n; i++) {
            var nd = nodeAt(g, i);
            out.push(nd ? nodePos(node) : null);
        }
        Runtime.nodeCacheG = g;
        Runtime.nodeCache = out;
        log("info", "node cache built: " + out.length + " nodes");
        return out;
    }

    /* ---------------- 跟随：所有人机都朝我走 ---------------- */
    function followOnce() {
        var me = myPlayer();
        if (!me) return;
        var bots = allBotsCached(1000);
        var mp = playerPos(me);
        var i;
        Runtime.followTargets = bots.length;
        for (i = 0; i < bots.length; i++) {
            var b = bots[i];
            var info = safe(function () { return b.add(OFF.Bot_enemyInfo).readPointer(); }, null);
            if (!isPtr(info)) continue;
            var dist = 3.0;
            if (mp) {
                var bp = playerPos(b);
                if (bp) {
                    var dx = mp.x - bp.x, dy = mp.y - bp.y, dz = mp.z - bp.z;
                    dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
                }
            }
            safe(function () {
                /* 目标锁死成我：这样它们不会再去寻别的敌人，也不会互相打 */
                info.add(OFF.BotEnemyInfo_enemy).writePointer(me);
                info.add(OFF.BotEnemyInfo_isPlayer).writeU8(1);
                info.add(OFF.BotEnemyInfo_findTime).writeFloat(1.0e9);
                info.add(OFF.BotEnemyInfo_lastLostTime).writeFloat(1.0e9);
                info.add(OFF.BotEnemyInfo_nextCheckVisibleTime).writeFloat(1.0e9);
                info.add(OFF.BotEnemyInfo_distance).writeFloat(dist);
                if (mp) {
                    info.add(OFF.BotEnemyInfo_enemyPos).writeFloat(mp.x);
                    info.add(OFF.BotEnemyInfo_enemyPos + 4).writeFloat(mp.y);
                    info.add(OFF.BotEnemyInfo_enemyPos + 8).writeFloat(mp.z);
                }
                b.add(OFF.Bot_tryFindEnemy).writePointer(me);
                b.add(OFF.Bot_nextCheckEnemyInViewTime).writeFloat(1.0e9);
                b.add(OFF.Bot_nextAttackTime).writeFloat(1.0e9);
                b.add(OFF.Bot_faceToEnemy).writeU8(0);
            }, null);
        }
    }

    function followLog() {
        var me = myPlayer();
        if (!me) return;
        var mp = playerPos(me);
        if (!mp) return;
        var bots = allBotsCached(1000);
        var max = bots.length < 4 ? bots.length : 4;
        var i, shown = 0;
        for (i = 0; i < bots.length && shown < max; i++) {
            var b = bots[i];
            var p = playerPos(b);
            if (!p) continue;
            var d = Math.sqrt((p.x - mp.x) * (p.x - mp.x) + (p.y - mp.y) * (p.y - mp.y) + (p.z - mp.z) * (p.z - mp.z));
            var key = b.toString();
            var last = Runtime.followLast[key];
            var moved = last ? Math.sqrt((p.x - last.x) * (p.x - last.x) + (p.z - last.z) * (p.z - last.z)) : 0;
            Runtime.followLast[key] = p;
            if (moved > 0.4) Runtime.stats.followMoves += 1;
            var info = safe(function () { return b.add(OFF.Bot_enemyInfo).readPointer(); }, null);
            var en = isPtr(info) ? safe(function () { return info.add(OFF.BotEnemyInfo_enemy).readPointer(); }, ptr(0)) : ptr(0);
            var own = (isPtr(en) && en.equals(me)) ? 1 : 0;
            log("info", "FOLLOW|i=" + shown + "|dist=" + fmt(d) + "|moved=" + fmt(moved) + "|own=" + own);
            shown += 1;
        }
        if (shown === 0) noteOnce("nofollownone", "跟随开着但一个可跟的人机都没找到");
    }

    /* ---------------- 采样（吃缓存的节点坐标，别每 tick 重读） ---------------- */
    function walkOnce() {
        var g = pointGraph();
        if (!g) return;
        var pos = nodePositions(g);
        var bots = allBotsCached(1000);
        var i, k;
        var n = pos.length;
        var budget = bots.length < 8 ? bots.length : 8;
        for (i = 0; i < budget; i++) {
            var b = bots[i];
            var key = b.toString();
            var p = playerPos(b);
            if (!p) continue;
            var lastP = Runtime.lastPos[key];
            if (lastP && Math.abs(p.x - lastP) < 0.4 && Math.abs(p.z - lastP) < 0.4) {
                continue;                     /* 没动就别算最近节点 */
            }
            Runtime.lastPos[key] = p;
            var nd = -1, best = 1e18;
            for (k = 0; k < n; k++) {
                var q = pos[k];
                if (!q) continue;
                var dx = p.x - q.x, dy = p.y - q.y, dz = p.z - q.z;
                var d = dx * dx + dy * dy + dz * dz;
                if (d < best) { best = d; nd = k; }
            }
            Runtime.stats.samples += 1;
            var prevNode = Runtime.lastNode[key];
            if (prevNode !== undefined && prevNode !== nd && prevNode >= 0 && nd >= 0) {
                var a = nodeAt(g, prevNode), bb = nodeAt(g, nd);
                var linked = (a && bb && hasEdge(a, bb)) ? 1 : 0;
                Runtime.stats.traversals += 1;
                if (!linked) Runtime.stats.linked0 += 1;
                if (!linked || (Runtime.stats.traversals % 20) === 0) {
                    log("info", "TRACE|bot=" + i + "|" + prevNode + ">" + nd + "|linked=" + linked);
                }
            }
            Runtime.lastNode[key] = nd;
        }
    }

    /* ---------------- 冻结人机行为 ---------------- */
    function freezeOnce() {
        setStopAllBot(true);
        if (!Runtime.freezeLogged) {
            Runtime.freezeLogged = true;
            log("info", "冻结人机行为：Bot.stopAllBot=true（不寻敌/不巡逻/不开火）");
        }
        if (Runtime.config.follow) {
            noteOnce("freeze_follow", "冻结和跟随同时打开时以冻结为准，人机不会走过来");
        }
    }

    /* ---------------- timers ---------------- */
    function clearTimers() {
        var i;
        for (i = 0; i < Runtime.timers.length; i++) {
            try { clearInterval(Runtime.timers[i]); } catch (e) {}
        }
        Runtime.timers = [];
    }

    function startTimers() {
        clearTimers();
        var cfg = Runtime.config;
        if (cfg.freeze) {
            Runtime.freezeLogged = false;
            Runtime.timers.push(setInterval(function () {
                try { freezeOnce(); } catch (e) { setError("freeze", e); }
            }, 300));
        } else {
            setStopAllBot(false);
        }
        if (cfg.pacify) {
            Runtime.timers.push(setInterval(function () {
                try { pacifyOnce(); } catch (e) { setError("pacify", e); }
            }, 200));
        }
        if (cfg.follow) {
            Runtime.timers.push(setInterval(function () {
                try { followOnce(); } catch (e) { setError("follow", e); }
            }, 100));
            Runtime.timers.push(setInterval(function () {
                try { followLog(); } catch (e) { setError("followLog", e); }
            }, 1000));
        }
        if (cfg.walk) {
            var ms = Math.max(300, cfg.sample_ms || 300);
            Runtime.timers.push(setInterval(function () {
                try { walkOnce(); } catch (e) { setError("walk", e); }
            }, ms));
        }
    }

    /* ---------------- rpc ---------------- */
    function apiEnable() {
        if (!initNative()) return { ok: false, reason: Runtime.stats.lastError };
        Runtime.enabled = true;
        startTimers();
        log("info", "enabled pacify=" + Runtime.config.pacify + " freeze=" + Runtime.config.freeze + " follow=" + Runtime.config.follow + " walk=" + Runtime.config.walk);
        return { ok: true };
    }

    function apiDisable() {
        Runtime.enabled = false;
        clearTimers();
        try { restoreAll(); } catch (e) { setError("restore", e); }
        Runtime.botCache = [];
        Runtime.botCacheAt = 0;
        Runtime.followLast = {};
        Runtime.lastNode = {};
        Runtime.lastPos = {};
        log("info", "disabled");
        return { ok: true };
    }

    function apiSetConfig(cfg) {
        if (!cfg) return { ok: false };
        if (cfg.pacify !== undefined) Runtime.config.pacify = !!cfg.pacify;
        if (cfg.freeze !== undefined) Runtime.config.freeze = !!cfg.freeze;
        if (cfg.follow !== undefined) Runtime.config.follow = !!cfg.follow;
        if (cfg.walk !== undefined) Runtime.config.walk = !!cfg.walk;
        if (cfg.sample_ms !== undefined) Runtime.config.sample_ms = Math.max(50, Math.min(5000, Number(cfg.sample_ms) || 200));
        if (Runtime.enabled) startTimers();
        log("info", "config pacify=" + Runtime.config.pacify + " freeze=" + Runtime.config.freeze + " follow=" + Runtime.config.follow +
            " walk=" + Runtime.config.walk + " sample_ms=" + Runtime.config.sample_ms);
        return { ok: true, config: Runtime.config };
    }

    function apiStatus() {
        return {
            ok: true,
            enabled: Runtime.enabled,
            config: Runtime.config,
            probe: Runtime.probe.summary,
            bots: Runtime.bots,
            followTargets: Runtime.followTargets || 0,
            myTeam: Runtime.myTeam,
            stats: Runtime.stats,
            edges: Runtime.probe.edges.length,
            probeRanAt: Runtime.probe.ranAt,
            errors: Runtime.stats.errors || 0,
            lastError: Runtime.stats.lastError
        };
    }

    /* ---------------- 自检 ---------------- */
    function apiSelfTest() {
        var steps = [], ok = true;
        function step(name, fn) {
            try { steps.push(name + "=" + fn()); }
            catch (e) { ok = false; steps.push(name + "=ERR(" + (e && e.message ? e.message : String(e)) + ")"); }
        }
        step("module", function () {
            var m = Process.findModuleByName(MODULE_NAME);
            return m ? (m.base + "/" + m.size) : "missing";
        });
        step("arch", function () { return Process.arch + "/" + Process.pointerSize; });
        step("native", function () { return initNative() ? "ready" : ("fail:" + Runtime.stats.lastError); });
        step("astarpath", function () { var a = astarPath(); return a ? a.toString() : "null"; });
        step("pointgraph", function () { var g = pointGraph(); return g ? (nodeCount(g) + "nodes") : "null"; });
        step("assemblies", function () { var imgs = assemblyImages(); return imgs ? (imgs.length + " images") : "unavailable"; });
        step("astar_class", function () { var k = classPtr("AstarPath", RVA.AstarPath_TypeInfo); return k ? (k + "/" + klassName(k)) : "null"; });
        step("bot_class", function () { var k = classPtr("Bot", RVA.Bot_TypeInfo); return k ? (k + "/" + klassName(k)) : "null"; });
        step("player_class", function () { var k = classPtr("Player", 0x00E2E3B4); return k ? (k + "/" + klassName(k)) : "null"; });
        step("gm_class", function () { var k = classPtr("GameManager", RVA.GameManager_TypeInfo); return k ? (k + "/" + klassName(k)) : "null"; });
        step("gm_static", function () { var sf = staticFields(classPtr("GameManager", RVA.GameManager_TypeInfo)); return sf.isNull() ? "null" : sf.toString(); });
        step("myplayer", function () { var me = myPlayer(); return me ? me.toString() : "null"; });
        step("bot_type", function () { var t = typeOfClass("Bot"); return t ? t.toString() : "null"; });
        step("bots", function () { return allBots().length; });
        step("players", function () { return allPlayers().length; });
        step("cameras", function () { return findObjectsOf("Camera").length; });
        step("stopallbot", function () {
            var sfb = botStaticFields();
            return sfb.isNull() ? "no-static-fields" : sfb.add(OFF.Bot_stopAllBot).readU8();
        });
        step("il2cpp_api", function () {
            var mod = Process.findModuleByName(MODULE_NAME);
            var eDomain = resolveExport(mod, "il2cpp_domain_get");
            var eAsms = resolveExport(mod, "il2cpp_domain_get_assemblies");
            var eImage = resolveExport(mod, "il2cpp_assembly_get_image");
            var eClass = resolveExport(mod, "il2cpp_class_from_name");
            if (!eDomain || !eAsms || !eImage || !eClass) return "missing il2cpp api exports";
            var fDomain = new NativeFunction(eDomain, "pointer", [], CALL_CONV);
            var fAsms = new NativeFunction(eAsms, "pointer", ["pointer", "pointer"], CALL_CONV);
            var fImage = new NativeFunction(eImage, "pointer", ["pointer"], CALL_CONV);
            var fClass = new NativeFunction(eClass, "pointer", ["pointer", "pointer", "pointer"], CALL_CONV);
            var dom = fDomain();
            if (!dom || dom.isNull()) return "domain=null";
            var cnt = Memory.alloc(4); cnt.writeU32(0);
            var arr = fAsms(dom, cnt);
            if (!arr || arr.isNull()) return "assemblies=null";
            var n = cnt.readU32(), i;
            if (n > 400) n = 400;
            var want = [["UnityEngine", "Object"], ["UnityEngine", "Camera"], ["", "Bot"], ["", "Player"]];
            for (i = 0; i < n; i++) {
                var asm = arr.add(i * 4).readPointer();
                if (!isPtr(asm)) continue;
                var img = safe(function () { return fImage(asm); }, null);
                if (!img || img.isNull()) continue;
                var w;
                for (w = 0; w < want.length; w++) {
                    var ns = Memory.allocUtf8String(want[w][0]);
                    var nm = Memory.allocUtf8String(want[w][1]);
                    var k = safe(function () { return fClass(img, ns, nm); }, null);
                    if (k && !k.isNull() && isPtr(k)) {
                        return want[w][1] + "->" + k + "/name=" + klassName(k);
                    }
                }
            }
            return "no known class found in " + n + " assemblies";
        });
        step("raycast", function () {
            if (!Runtime.native.ready) return "native_not_ready";
            if (!astarPath()) return "skipped(no_map)";
            var r = raycast({ x: 0, y: 50, z: 0 }, { x: 0, y: -1, z: 0 }, 200);
            return r ? ("hit y=" + fmt(r.y) + " ny=" + fmt(r.ny)) : "miss";
        });
        var line = "SELFTEST|ok=" + ok + "|" + steps.join("|");
        log(ok ? "info" : "error", line);
        return { ok: ok, line: line, steps: steps };
    }

    function apiCleanup() {
        return apiDisable();
    }

    rpc.exports = {
        enable: apiEnable,
        disable: apiDisable,
        setConfig: apiSetConfig,
        setconfig: apiSetConfig,
        runProbe: runProbe,
        runprobe: runProbe,
        selfTest: apiSelfTest,
        selftest: apiSelfTest,
        status: apiStatus,
        cleanup: apiCleanup
    };
})();
