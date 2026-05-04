// ============================================================
// Bot 出生点集合器 v21 — 修复 AddPlayer 签名 + 万能收集
//
// v20 致命 Bug: AddPlayer(bool isBot, Team team) 的 args[1] 
//   是 isBot (bool), 不是 Player 指针! 追踪了错误地址。
// 修正: 用 onLeave 获取 AddPlayer 返回的 Player 指针。
//
// 新增数据源:
//   ⑤ ModeBase_Nano.respawningPlayer (0xAC)
//   ⑥ ModeBase_Nano.randomPlayerList (0xB4)
//
// 新增: Singleton<GameManager>.get_instance (RVA 0x4A8170)
//   作为无法 Hook 时的后备获取方式。
// ============================================================

(function() {
    'use strict';

    function L(l, m) {
        var p = '[BotSpawn-v21] ';
        if (l === 'e') console.error(p + m);
        else if (l === 'w') console.warn(p + m);
        else console.log(p + m);
    }

    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) { L('e', 'GameAssembly.dll not found'); return; }
    var B = mod.base;

    L('i', '╔══════════════════════════════════════════════╗');
    L('i', '║  Bot 出生点集合器 v21 — 签名修正+万能收集   ║');
    L('i', '║  GameAssembly.dll @ ' + B);
    L('i', '╚══════════════════════════════════════════════╝');

    // ================================================================
    // RVA 地址表
    // ================================================================
    var R = {
        GM_AddP:    0xAF9A90,  // GameManager.AddPlayer(bool isBot, Team team) : Player
        GM_AddPs:   0xAF9DE0,  // GameManager.AddPlayers()
        GM_isNano:  0xAFDA80,  // GameManager.get_isNanoMode
        MM_MapGun:  0xAEBB70,  // MapManager.MapGunInit
        P_Update:   0xB551D0,  // Player.Update
        P_isMy:     0xB55FD0,  // Player.get_isMyPlayer
        E_isDead:   0xB400E0,  // Entity.get_isDead
        E_getCC:    0x1CF180,  // Entity.get_characterController
        C_setEn:    0xAB86B0,  // CharacterController.set_enabled
        getTrans:   0x32CF40,  // Component.get_transform
        setPosInj:  0x3F4810,  // Transform.set_position_Injected
        SingGetIns: 0x4A8170,  // Singleton<T>.get_instance (generic)
        MN4_Awake:  0xB410D0,  // Mode_Nano4.Awake - get Nano4 instance
        MN4_OnNewP: 0xB42140,  // Mode_Nano4.OnNewPlayerJoin(Player)
    };

    // ================================================================
    // 字段偏移 (dump.cs 验证)
    // ================================================================
    var O = {
        // GameManager 实例字段
        GM_entityBL_Alive:  0x14,  // List<Entity>
        GM_entityGR_Alive:  0x18,  // List<Entity>
        GM_allPlayers:      0x1C,  // Player[]
        GM_playersBL:       0x20,  // List<Player>
        GM_playersBL_Alive: 0x24,  // List<Player>
        GM_playersGR:       0x28,  // List<Player>
        GM_playersGR_Alive: 0x2C,  // List<Player>

        // MapManager 实例字段
        MM_SP_BL:      0x10,  // SpawnPoint[]
        MM_SP_GR:      0x14,  // SpawnPoint[]
        MM_SP_Netural: 0x18,  // SpawnPoint[]

        // Player (extends Entity)
        P_cameraManager:      0x48,  // PlayerCameraManager* (真人!=null, Bot==null)
        P_characterContainer: 0x58,  // Transform*
        P_clientData:         0x94,  // ClientData*
        P_playerData:         0x98,  // PlayerData*

        // Entity
        E_team: 0x20,  // Team (int)

        // ClientData  
        CD_isBot:    0x1C,  // bool
        CD_joinTeam: 0x18,  // Team (int)

        // ModeBase_Nano fields (继承自 ModeBase)
        MN_respawningPlayer:  0xAC,  // List<Player>
        MN_randomPlayerList:  0xB4,  // List<Player>

        // ModeBase fields
        MB_myPlayer: 0x6C,  // Player (本地玩家)
    };

    // ================================================================
    // 状态变量
    // ================================================================
    var gm = null;
    var mm = null;
    var modeNano = null;  // ModeBase_Nano / Mode_Nano4 实例
    var spawn = null;
    var ntp = false;
    var tn = 0;

    // AddPlayer 跟踪: 记录 AddPlayer(bool, Team) 返回的所有 Player
    var trackedPlayers = [];
    var trackedSet = {};

    // ================================================================
    // NativeFunction 绑定
    // ================================================================
    var isMyPlayer = new NativeFunction(B.add(R.P_isMy),  'bool',    ['pointer', 'pointer']);
    var isDead     = new NativeFunction(B.add(R.E_isDead), 'bool',    ['pointer', 'pointer']);
    var getCC      = new NativeFunction(B.add(R.E_getCC), 'pointer',  ['pointer', 'pointer']);
    var ccSetEn    = new NativeFunction(B.add(R.C_setEn), 'void',     ['pointer', 'int', 'pointer']);
    var getTrans   = new NativeFunction(B.add(R.getTrans), 'pointer',  ['pointer', 'pointer']);
    var setPosInj  = new NativeFunction(B.add(R.setPosInj), 'void',    ['pointer', 'pointer', 'pointer']);
    var singletonGetter = new NativeFunction(B.add(R.SingGetIns), 'pointer', ['pointer']);
    var posBuf     = Memory.alloc(16);

    L('i', '✓ NativeFunction bindings ready');

    // ================================================================
    // 辅助函数
    // ================================================================

    function rp(addr, off) {
        try { return addr.add(off).readPointer(); } catch (e) { return null; }
    }

    function readList(listPtr) {
        if (!listPtr || listPtr.isNull()) return null;
        try {
            var items = listPtr.add(0x10).readPointer();
            var size  = listPtr.add(0x18).readU32();
            if (!items || items.isNull() || size <= 0 || size > 500) return null;
            return { ptr: items, len: size };
        } catch (e) { return null; }
    }

    function readArray(arrPtr) {
        if (!arrPtr || arrPtr.isNull()) return null;
        try {
            var len = arrPtr.add(0xC).readU32();
            if (len <= 0 || len > 500) return null;
            return { ptr: arrPtr, len: len };
        } catch (e) { return null; }
    }

    function readSpawnPos(arrPtr) {
        var data = readArray(arrPtr);
        if (!data || data.len === 0) return null;
        try {
            var p = data.ptr.add(0x10);
            return {
                x: p.readFloat(),
                y: p.add(4).readFloat(),
                z: p.add(8).readFloat()
            };
        } catch (e) { return null; }
    }

    function isValidPlayerPtr(pp) {
        if (!pp || pp.isNull()) return false;
        try {
            var vt = pp.readPointer();
            return vt && !vt.isNull();
        } catch (e) { return false; }
    }

    function isRealHuman(pp) {
        try {
            var cam = rp(pp, O.P_cameraManager);
            if (cam && !cam.isNull()) return true;

            var cd = rp(pp, O.P_clientData);
            if (cd && !cd.isNull()) {
                var isBotVal = 0;
                try { isBotVal = cd.add(O.CD_isBot).readU8(); } catch (e) {}
                if (isBotVal === 0) return true;
            }
            return false;
        } catch (e) { return false; }
    }

    // ================================================================
    // ★ 核心: 从所有 6 个数据源收集 Player (自动去重)
    // ================================================================
    function collectAllPlayers() {
        var seen = {};
        var result = [];

        function add(pp) {
            if (!isValidPlayerPtr(pp)) return;
            var key = pp.toString();
            if (seen[key]) return;
            seen[key] = true;
            result.push(pp);
        }

        // ① AddPlayer Hook 跟踪表 (每个 Player 创建时记录)
        for (var i = 0; i < trackedPlayers.length; i++) {
            add(trackedPlayers[i]);
        }

        if (!gm) return result;

        // ② allPlayers 数组 (0x1C) — 固定 30 槽
        try {
            var ap = gm.add(O.GM_allPlayers).readPointer();
            var arrData = readArray(ap);
            if (arrData) {
                for (var i = 0; i < arrData.len; i++) {
                    try { add(arrData.ptr.add(0x10 + i * 8).readPointer()); } catch (e) {}
                }
            }
        } catch (e) {}

        // ③ playersBL / playersGR (List<Player>)
        try {
            var offsets = [O.GM_playersBL, O.GM_playersGR];
            for (var oi = 0; oi < offsets.length; oi++) {
                var listData = readList(gm.add(offsets[oi]).readPointer());
                if (listData) {
                    for (var i = 0; i < listData.len; i++) {
                        try { add(listData.ptr.add(0x10 + i * 8).readPointer()); } catch (e) {}
                    }
                }
            }
        } catch (e) {}

        // ④ playersBL_Alive / playersGR_Alive (List<Player>)
        try {
            var offsets = [O.GM_playersBL_Alive, O.GM_playersGR_Alive];
            for (var oi = 0; oi < offsets.length; oi++) {
                var listData = readList(gm.add(offsets[oi]).readPointer());
                if (listData) {
                    for (var i = 0; i < listData.len; i++) {
                        try { add(listData.ptr.add(0x10 + i * 8).readPointer()); } catch (e) {}
                    }
                }
            }
        } catch (e) {}

        // ⑤ ModeBase_Nano.randomPlayerList (0xB4) — ★ 新增: 所有参与玩家
        if (modeNano) {
            try {
                var listData = readList(modeNano.add(O.MN_randomPlayerList).readPointer());
                if (listData) {
                    for (var i = 0; i < listData.len; i++) {
                        try { add(listData.ptr.add(0x10 + i * 8).readPointer()); } catch (e) {}
                    }
                }
            } catch (e) {}

            // ⑥ ModeBase_Nano.respawningPlayer (0xAC) — ★ 新增: 重生中的玩家
            try {
                var listData = readList(modeNano.add(O.MN_respawningPlayer).readPointer());
                if (listData) {
                    for (var i = 0; i < listData.len; i++) {
                        try { add(listData.ptr.add(0x10 + i * 8).readPointer()); } catch (e) {}
                    }
                }
            } catch (e) {}
        }

        return result;
    }

    // ================================================================
    // 传送一个 Bot
    // ================================================================
    function teleportBot(pp) {
        try {
            var tr = getTrans(pp, ptr(0));
            var usedSub = false;
            if (!tr || tr.isNull()) {
                tr = rp(pp, O.P_characterContainer);
                usedSub = true;
            }
            if (!tr || tr.isNull()) return 'T=null';

            var cc = getCC(pp, ptr(0));
            if (cc && !cc.isNull()) ccSetEn(cc, 0, ptr(0));

            setPosInj(tr, posBuf, ptr(0));
            try {
                var np = tr.add(0x10).readPointer();
                if (np) {
                    np.add(0x38).writeFloat(spawn.x);
                    np.add(0x3C).writeFloat(spawn.y);
                    np.add(0x40).writeFloat(spawn.z);
                }
            } catch (e) {}

            if (cc && !cc.isNull()) ccSetEn(cc, 1, ptr(0));

            return usedSub ? 'OK(sub)' : 'OK';
        } catch (e) {
            return 'ERR:' + e.message;
        }
    }

    // ================================================================
    // 执行传送
    // ================================================================
    function executeTeleport() {
        tn++;
        L('i', '');
        L('i', '╔══ 传送执行 #' + tn + ' ══╗');

        if (!gm || !mm) {
            L('e', 'GameManager/MapManager 未就绪');
            L('i', '╚════════════════╝');
            return;
        }

        if (!spawn) {
            spawn = { x: 0, y: 0, z: 0 };
            L('w', '出生点为 (0,0,0)');
        }

        posBuf.writeFloat(spawn.x);
        posBuf.add(4).writeFloat(spawn.y);
        posBuf.add(8).writeFloat(spawn.z);

        L('i', '目标: (' + spawn.x.toFixed(1) + ', ' + spawn.y.toFixed(1) + ', ' + spawn.z.toFixed(1) + ')');
        L('i', '跟踪表: ' + trackedPlayers.length + ' | Nano模式: ' + (modeNano ? '✓' : '✗'));

        var allP = collectAllPlayers();
        L('i', '去重后 Player 总数: ' + allP.length);

        if (allP.length === 0) {
            L('e', '无 Player');
            L('i', '╚════════════════╝');
            return;
        }

        var selfCount = 0;
        var realCount = 0;
        var deadCount = 0;
        var botCount = 0;
        var okCount = 0;
        var failCount = 0;
        var detailLog = [];

        for (var i = 0; i < allP.length; i++) {
            var pp = allP[i];
            var label = '#' + i;

            try {
                if (isMyPlayer(pp, ptr(0))) {
                    selfCount++;
                    detailLog.push(label + ': ★ 自己');
                    continue;
                }
                if (isRealHuman(pp)) {
                    realCount++;
                    detailLog.push(label + ': 真人');
                    continue;
                }
                var dead = false;
                try { dead = isDead(pp, ptr(0)); } catch (e) {}
                if (dead) {
                    deadCount++;
                    detailLog.push(label + ': Bot(已死)');
                    continue;
                }

                botCount++;
                var result = teleportBot(pp);
                if (result === 'OK' || result === 'OK(sub)') {
                    okCount++;
                    detailLog.push(label + ': Bot → ' + result);
                } else {
                    failCount++;
                    detailLog.push(label + ': Bot → FAIL: ' + result);
                }
            } catch (e) {
                failCount++;
                detailLog.push(label + ': ★ 异常: ' + e.message);
            }
        }

        for (var j = 0; j < detailLog.length; j++) {
            L('i', '  ' + detailLog[j]);
        }

        L('i', '');
        L('i', '┌─ 统计 ────────────────────────────────┐');
        L('i', '│  总计: ' + allP.length + '  自己: ' + selfCount + '  真人: ' + realCount);
        L('i', '│  Bot已死: ' + deadCount + '  Bot存活: ' + botCount + '  成功: ' + okCount);
        if (failCount > 0) L('i', '│  失败: ' + failCount);
        L('i', '└────────────────────────────────────────┘');
        L('i', '╚════════════════╝');

        send(JSON.stringify({ t: 'done', n: tn, total: allP.length, bots: botCount, ok: okCount }));
    }

    // ================================================================
    // ★ Hook: GameManager.AddPlayer(bool isBot, Team team) → Player
    //   签名: public Player AddPlayer(bool isBot, Team team)
    //   args[0] = this (GameManager)
    //   args[1] = isBot (bool, 0/1) — 不是 Player!
    //   args[2] = team (Team enum)
    //   retVal  = Player* (在 onLeave 中获取)
    // ================================================================
    L('i', '');
    L('i', '安装 GameManager.AddPlayer Hook...');
    try {
        Interceptor.attach(B.add(R.GM_AddP), {
            onEnter: function(args) {
                if (!gm) {
                    gm = args[0];
                    L('i', '✅ GameManager: ' + gm);
                    send(JSON.stringify({ t: 'gm', addr: gm.toString() }));
                }
            },
            onLeave: function(retVal) {
                // retVal = 刚创建的 Player 对象
                var player = retVal;
                if (player && !player.isNull() && isValidPlayerPtr(player)) {
                    var key = player.toString();
                    if (!trackedSet[key]) {
                        trackedSet[key] = true;
                        trackedPlayers.push(player);
                    }
                }
            }
        });
        L('i', '✅ AddPlayer Hook OK (onLeave 捕获返回值)');
    } catch (e) {
        L('e', 'AddPlayer Hook 失败: ' + e.message);
    }

    // ================================================================
    // Hook: Mode_Nano4.OnNewPlayerJoin(Player) — 备用 Player 捕获
    // ================================================================
    try {
        Interceptor.attach(B.add(R.MN4_OnNewP), {
            onEnter: function(args) {
                var player = args[1];
                if (player && !player.isNull() && isValidPlayerPtr(player)) {
                    var key = player.toString();
                    if (!trackedSet[key]) {
                        trackedSet[key] = true;
                        trackedPlayers.push(player);
                    }
                }
            }
        });
        L('i', '✅ Mode_Nano4.OnNewPlayerJoin Hook OK');
    } catch (e) {
        L('w', 'Mode_Nano4.OnNewPlayerJoin Hook 不可用 (非 Nano 模式?)');
    }

    // ================================================================
    // Hook: Mode_Nano4.Awake — 捕获 Mode_Nano4 实例
    // ================================================================
    try {
        Interceptor.attach(B.add(R.MN4_Awake), {
            onEnter: function(args) {
                if (!modeNano) {
                    modeNano = args[0];
                    L('i', '✅ Mode_Nano4 实例: ' + modeNano);
                }
            }
        });
        L('i', '✅ Mode_Nano4.Awake Hook OK');
    } catch (e) {
        L('w', 'Mode_Nano4.Awake Hook 不可用');
    }

    // ================================================================
    // 后备: 用 Singleton.get_instance 获取 GM/MM
    // ================================================================
    setTimeout(function() {
        if (!gm) {
            L('i', '⏳ GM Hook 未触发, 尝试 Singleton.get_instance...');
            try {
                var instance = singletonGetter(ptr(0));
                if (instance && !instance.isNull()) {
                    gm = instance;
                    L('i', '✅ GM 通过 Singleton.get_instance: ' + gm);
                    send(JSON.stringify({ t: 'gm', addr: gm.toString() }));
                }
            } catch (e) {
                L('w', 'Singleton.get_instance 失败: ' + e.message);
            }
        }
    }, 5000);

    // ================================================================
    // Hook: MapManager.MapGunInit → 出生点
    // ================================================================
    L('i', '');
    L('i', '安装 MapManager.MapGunInit Hook...');
    try {
        Interceptor.attach(B.add(R.MM_MapGun), {
            onEnter: function(args) {
                if (!mm) {
                    mm = args[0];
                    L('i', '✅ MapManager: ' + mm);

                    var sGR  = readSpawnPos(mm.add(O.MM_SP_GR).readPointer());
                    var sBL  = readSpawnPos(mm.add(O.MM_SP_BL).readPointer());
                    var sNet = readSpawnPos(mm.add(O.MM_SP_Netural).readPointer());

                    if (sNet) L('i', '  SP_Netural: (' + sNet.x.toFixed(1) + ', ' + sNet.y.toFixed(1) + ', ' + sNet.z.toFixed(1) + ')');
                    if (sBL)  L('i', '  SP_BL: (' + sBL.x.toFixed(1) + ', ' + sBL.y.toFixed(1) + ', ' + sBL.z.toFixed(1) + ')');
                    if (sGR)  L('i', '  SP_GR: (' + sGR.x.toFixed(1) + ', ' + sGR.y.toFixed(1) + ', ' + sGR.z.toFixed(1) + ')');

                    spawn = sGR || sBL;
                    L('i', '  → 目标: ' + (sGR ? 'SP_GR' : sBL ? 'SP_BL' : '无'));
                    send(JSON.stringify({ t: 'mm', addr: mm.toString() }));
                }
            }
        });
        L('i', '✅ MapGunInit Hook OK');
    } catch (e) {
        L('e', 'MapGunInit Hook 失败: ' + e.message);
    }

    // ================================================================
    // Hook: Player.Update → 执行传送
    // ================================================================
    L('i', '');
    L('i', '安装 Player.Update Hook...');
    try {
        Interceptor.attach(B.add(R.P_Update), {
            onEnter: function(args) {
                if (!ntp) return;
                ntp = false;
                if (!gm || !mm) {
                    L('w', 'GM/MM 未就绪');
                    send(JSON.stringify({ t: 'err', msg: 'not ready' }));
                    return;
                }
                executeTeleport();
            }
        });
        L('i', '✅ Player.Update Hook OK');
    } catch (e) {
        L('e', 'Player.Update Hook 失败: ' + e.message);
    }

    // ================================================================
    // RPC 接口
    // ================================================================
    rpc.exports = {
        teleport: function() {
            if (!gm || !mm) {
                var msg = 'GM=' + (gm ? '✓' : '✗') + ' MM=' + (mm ? '✓' : '✗');
                L('w', '未就绪: ' + msg);
                send(JSON.stringify({ t: 'err', msg: msg }));
                return 'ERR: ' + msg;
            }
            ntp = true;
            L('i', '★ ★ ★ 收到传送指令 ★ ★ ★');
            return 'OK: 已触发';
        },

        getStatus: function() {
            return {
                gm: gm ? gm.toString() : null,
                mm: mm ? mm.toString() : null,
                modeNano: modeNano ? modeNano.toString() : null,
                spawn: spawn,
                tracked: trackedPlayers.length,
                ready: !!(gm && mm)
            };
        },

        diag: function() {
            if (!gm) { L('w', 'GM 未就绪'); return { error: 'GM not ready' }; }
            L('i', '══ 诊断 ══');
            L('i', 'GM: ' + gm + ' | MM: ' + mm + ' | Nano: ' + modeNano);
            L('i', 'TrackedPlayers: ' + trackedPlayers.length);

            var all = collectAllPlayers();
            L('i', '去重后总数: ' + all.length);

            // 各列表统计
            var fields = [
                { n: 'entityBL_Alive',  o: O.GM_entityBL_Alive,  t: 'list' },
                { n: 'entityGR_Alive',  o: O.GM_entityGR_Alive,  t: 'list' },
                { n: 'allPlayers',      o: O.GM_allPlayers,      t: 'arr' },
                { n: 'playersBL',       o: O.GM_playersBL,       t: 'list' },
                { n: 'playersBL_Alive', o: O.GM_playersBL_Alive,  t: 'list' },
                { n: 'playersGR',       o: O.GM_playersGR,       t: 'list' },
                { n: 'playersGR_Alive', o: O.GM_playersGR_Alive,  t: 'list' },
            ];

            for (var fi = 0; fi < fields.length; fi++) {
                var f = fields[fi];
                try {
                    var ptr = gm.add(f.o).readPointer();
                    var data = f.t === 'arr' ? readArray(ptr) : readList(ptr);
                    L('i', '  ' + f.n + ' (+0x' + f.o.toString(16) + '): ' + (data ? (f.t==='arr'?'len=':'size=') + data.len : '空'));
                } catch (e) {
                    L('i', '  ' + f.n + ': ERR ' + e.message);
                }
            }

            // Mode_Nano 列表
            if (modeNano) {
                try {
                    var rp = readList(modeNano.add(O.MN_respawningPlayer).readPointer());
                    L('i', '  respawningPlayer (0xAC): ' + (rp ? 'size=' + rp.len : '空'));
                } catch (e) { L('i', '  respawningPlayer: ERR'); }
                try {
                    var rl = readList(modeNano.add(O.MN_randomPlayerList).readPointer());
                    L('i', '  randomPlayerList (0xB4): ' + (rl ? 'size=' + rl.len : '空'));
                } catch (e) { L('i', '  randomPlayerList: ERR'); }
            }

            L('i', '══ 诊断结束 ══');
            return { tracked: trackedPlayers.length, totalUnique: all.length };
        }
    };

    L('i', '');
    L('i', '╔══════════════════════════════════════════╗');
    L('i', '║  v21 已就绪                              ║');
    L('i', '║                                         ║');
    L('i', '║  RPC:                                   ║');
    L('i', '║    teleport() → 传送 Bot                ║');
    L('i', '║    getStatus() → 状态                    ║');
    L('i', '║    diag() → 诊断所有列表                 ║');
    L('i', '╚══════════════════════════════════════════╝');
})();
