
(function() {
    'use strict';

    function L(l, m) {
        var p = '[BotSpawn-v20] ';
        if (l === 'e') console.error(p + m);
        else if (l === 'w') console.warn(p + m);
        else console.log(p + m);
    }

    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) { L('e', 'GameAssembly.dll not found'); return; }
    var B = mod.base;


    // ================================================================
    // RVA 地址表 (已验证可用)
    // ================================================================
    var R = {
        GM_AddP:    0xAF9A90,  // GameManager.AddPlayer(Player)
        GM_AddPs:   0xAF9DE0,  // GameManager.AddPlayers (备用)
        GM_isNano:  0xAFDA80,  // GameManager.get_isNanoMode
        MM_MapGun:  0xAEBB70,  // MapManager.MapGunInit
        P_Update:   0xB551D0,  // Player.Update
        P_isMy:     0xB55FD0,  // Player.get_isMyPlayer
        E_isDead:   0xB400E0,  // Entity.get_isDead
        E_getCC:    0x1CF180,  // Entity.get_characterController
        C_setEn:    0xAB86B0,  // CharacterController.set_enabled
        getTrans:   0x32CF40,  // Component.get_transform
        setPosInj:  0x3F4810,  // Transform.set_position_Injected
    };

    // ================================================================
    // 字段偏移 (来自 dump.cs 验证)
    // ================================================================
    var O = {
        // GameManager (单例实例)
        GM_entityBL_Alive:  0x14,  // List<Entity>
        GM_entityGR_Alive:  0x18,  // List<Entity>
        GM_allPlayers:      0x1C,  // Player[]
        GM_playersBL:       0x20,  // List<Player>
        GM_playersBL_Alive: 0x24,  // List<Player>
        GM_playersGR:       0x28,  // List<Player>
        GM_playersGR_Alive: 0x2C,  // List<Player>

        // MapManager (单例实例)
        MM_SP_BL:      0x10,  // SpawnPoint[]
        MM_SP_GR:      0x14,  // SpawnPoint[]
        MM_SP_Netural: 0x18,  // SpawnPoint[]

        // Player (extends Entity)
        P_cameraManager:     0x48,  // PlayerCameraManager* (真人!=null, Bot==null)
        P_characterContainer: 0x58,  // Transform* (子节点, 降级用)
        P_clientData:        0x94,  // ClientData*

        // Entity
        E_team: 0x20,  // Team (int)

        // ClientData
        CD_isBot:    0x1C,  // bool
        CD_joinTeam: 0x18,  // Team (int)
    };

    // ================================================================
    // 状态变量
    // ================================================================
    var gm = null;           // GameManager 实例
    var mm = null;           // MapManager 实例
    var spawn = null;        // 目标出生点 {x,y,z}
    var ntp = false;         // 触发传送标志
    var tn = 0;              // 传送执行计数
    var gmReady = false;
    var mmReady = false;

    // ★ AddPlayer 跟踪表: 记录所有加入过的 Player
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
    var posBuf     = Memory.alloc(16);

    L('i', '✓ NativeFunction bindings ready');

    // ================================================================
    // 辅助函数
    // ================================================================

    // 安全读指针
    function rp(addr, off) {
        try { return addr.add(off).readPointer(); } catch (e) { return null; }
    }

    // 读 IL2CPP List<T>
    function readList(listPtr) {
        if (!listPtr || listPtr.isNull()) return null;
        try {
            var items = listPtr.add(0x10).readPointer();
            var size  = listPtr.add(0x18).readU32();
            if (!items || items.isNull() || size <= 0 || size > 500) return null;
            return { ptr: items, len: size };
        } catch (e) { return null; }
    }

    // 读 IL2CPP T[]
    function readArray(arrPtr) {
        if (!arrPtr || arrPtr.isNull()) return null;
        try {
            var len = arrPtr.add(0xC).readU32();
            if (len <= 0 || len > 500) return null;
            return { ptr: arrPtr, len: len };
        } catch (e) { return null; }
    }

    // 读 SpawnPoint[0] 位置
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

    // 安全的 Player 验证
    function isValidPlayerPtr(pp) {
        if (!pp || pp.isNull()) return false;
        try {
            var vt = pp.readPointer();
            return vt && !vt.isNull();
        } catch (e) { return false; }
    }

    // 判断是否为真人 (有 cameraManager = 真人)
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

    // 判断是否为 Bot (非自己 + 非真人)
    function isBotPlayer(pp) {
        if (!isValidPlayerPtr(pp)) return false;
        try {
            if (isMyPlayer(pp, ptr(0))) return false;
            if (isRealHuman(pp)) return false;
            return true;
        } catch (e) { return false; }
    }

    // ================================================================
    // ★ 核心: 从所有数据源收集 Player
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

        // ① 从 AddPlayer Hook 跟踪表
        for (var i = 0; i < trackedPlayers.length; i++) {
            add(trackedPlayers[i]);
        }

        if (!gm) return result;

        // ② allPlayers 数组 (0x1C)
        try {
            var ap = gm.add(O.GM_allPlayers).readPointer();
            var arrData = readArray(ap);
            if (arrData) {
                for (var i = 0; i < arrData.len; i++) {
                    try {
                        var pp = arrData.ptr.add(0x10 + i * 8).readPointer();
                        add(pp);
                    } catch (e) {}
                }
            }
        } catch (e) {}

        // ③ playersBL + playersGR (List<Player>)
        try {
            var listOffsets = [O.GM_playersBL, O.GM_playersGR];
            for (var oi = 0; oi < listOffsets.length; oi++) {
                var listPtr = gm.add(listOffsets[oi]).readPointer();
                var listData = readList(listPtr);
                if (listData) {
                    for (var i = 0; i < listData.len; i++) {
                        try {
                            var pp = listData.ptr.add(0x10 + i * 8).readPointer();
                            add(pp);
                        } catch (e) {}
                    }
                }
            }
        } catch (e) {}

        // ④ playersBL_Alive + playersGR_Alive (List<Player>)
        try {
            var aliveOffsets = [O.GM_playersBL_Alive, O.GM_playersGR_Alive];
            for (var oi = 0; oi < aliveOffsets.length; oi++) {
                var listPtr = gm.add(aliveOffsets[oi]).readPointer();
                var listData = readList(listPtr);
                if (listData) {
                    for (var i = 0; i < listData.len; i++) {
                        try {
                            var pp = listData.ptr.add(0x10 + i * 8).readPointer();
                            add(pp);
                        } catch (e) {}
                    }
                }
            }
        } catch (e) {}

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
    // 执行传送 (由 Player.Update Hook 触发)
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
            L('w', '出生点为空，使用 (0,0,0)');
        }

        posBuf.writeFloat(spawn.x);
        posBuf.add(4).writeFloat(spawn.y);
        posBuf.add(8).writeFloat(spawn.z);

        L('i', '目标出生点: (' + spawn.x.toFixed(1) + ', ' + spawn.y.toFixed(1) + ', ' + spawn.z.toFixed(1) + ')');
        L('i', 'AddPlayer 跟踪总数: ' + trackedPlayers.length);

        // ─── 收集所有 Player ───
        var allP = collectAllPlayers();
        L('i', '去重后 Player 总数: ' + allP.length);

        if (allP.length === 0) {
            L('e', '未找到任何 Player');
            L('i', '╚════════════════╝');
            return;
        }

        // ─── 分类统计 ───
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
                // 跳过自己
                if (isMyPlayer(pp, ptr(0))) {
                    selfCount++;
                    detailLog.push(label + ': ★ 自己');
                    continue;
                }

                // 跳过真人
                if (isRealHuman(pp)) {
                    realCount++;
                    detailLog.push(label + ': 真人');
                    continue;
                }

                // 跳过死亡
                var dead = false;
                try { dead = isDead(pp, ptr(0)); } catch (e) { dead = false; }
                if (dead) {
                    deadCount++;
                    detailLog.push(label + ': Bot(已死)');
                    continue;
                }

                // ← 是活着的 Bot → 传送
                botCount++;
                var teamVal = '(?)';
                try {
                    var cd = rp(pp, O.P_clientData);
                    if (cd && !cd.isNull()) teamVal = cd.add(O.CD_joinTeam).readU8();
                } catch (e) {}

                var result = teleportBot(pp);
                if (result === 'OK' || result === 'OK(sub)') {
                    okCount++;
                    detailLog.push(label + ': Bot[team=' + teamVal + '] → ' + result);
                } else {
                    failCount++;
                    detailLog.push(label + ': Bot[team=' + teamVal + '] → FAIL: ' + result);
                }
            } catch (e) {
                failCount++;
                detailLog.push(label + ': ★ 异常: ' + e.message);
            }
        }

        // ─── 输出结果 ───
        for (var j = 0; j < detailLog.length; j++) {
            L('i', '  ' + detailLog[j]);
        }

        L('i', '');
        L('i', '┌─ 统计 ──────────────────────────┐');
        L('i', '│  Player 总数: ' + allP.length);
        L('i', '│  自己: ' + selfCount);
        L('i', '│  真人: ' + realCount);
        L('i', '│  Bot(已死): ' + deadCount);
        L('i', '│  Bot(存活): ' + botCount);
        L('i', '│  传送成功: ' + okCount);
        if (failCount > 0) L('i', '│  传送失败: ' + failCount);
        L('i', '└──────────────────────────────────┘');
        L('i', '╚════════════════╝');

        send(JSON.stringify({
            t: 'done',
            n: tn,
            total: allP.length,
            bots: botCount,
            ok: okCount,
            fail: failCount,
            dead: deadCount
        }));
    }

    // ================================================================
    // Hook: GameManager.AddPlayer
    // ================================================================
    L('i', '');
    L('i', '安装 GameManager.AddPlayer Hook...');
    try {
        Interceptor.attach(B.add(R.GM_AddP), {
            onEnter: function(args) {
                if (!gm) {
                    gm = args[0];
                    gmReady = true;
                    L('i', '✅ GameManager 实例: ' + gm);
                    send(JSON.stringify({ t: 'gm', addr: gm.toString() }));
                }
                var player = args[1];
                if (player && !player.isNull()) {
                    var key = player.toString();
                    if (!trackedSet[key]) {
                        trackedSet[key] = true;
                        trackedPlayers.push(player);
                    }
                }
            }
        });
        L('i', '✅ AddPlayer Hook OK');
    } catch (e) {
        L('e', 'AddPlayer Hook 失败: ' + e.message);
    }

    // ================================================================
    // 备用 Hook: AddPlayers (延时安装)
    // ================================================================
    var backupHook1 = null;
    setTimeout(function() {
        if (!gm) {
            L('i', '⏳ AddPlayer 未触发, 安装备用 AddPlayers Hook...');
            try {
                backupHook1 = Interceptor.attach(B.add(R.GM_AddPs), {
                    onEnter: function(args) {
                        if (!gm) {
                            gm = args[0];
                            gmReady = true;
                            L('i', '✅ GameManager (备用AddPlayers): ' + gm);
                            send(JSON.stringify({ t: 'gm', addr: gm.toString() }));
                        }
                    }
                });
                L('i', '✅ 备用 AddPlayers Hook OK');
            } catch (e) { L('e', '备用 Hook 失败: ' + e.message); }
        }
    }, 1000);

    // ================================================================
    // 备用 Hook: get_isNanoMode (高频, 捕获后立即解除)
    // ================================================================
    var backupHook2 = null;
    setTimeout(function() {
        if (!gm && !backupHook2) {
            L('i', '⏳ 安装备用 get_isNanoMode Hook...');
            try {
                backupHook2 = Interceptor.attach(B.add(R.GM_isNano), {
                    onEnter: function(args) {
                        if (!gm) {
                            gm = args[0];
                            gmReady = true;
                            L('i', '✅ GameManager (备用isNanoMode): ' + gm);
                            send(JSON.stringify({ t: 'gm', addr: gm.toString() }));
                            if (backupHook2) { backupHook2.detach(); backupHook2 = null; }
                        }
                    }
                });
                L('i', '✅ 备用 get_isNanoMode Hook OK (自动解除)');
            } catch (e) { L('e', '备用 Hook2 失败: ' + e.message); }
        }
    }, 2000);

    // ================================================================
    // Hook: MapManager.MapGunInit → 读取出生点
    // ================================================================
    L('i', '');
    L('i', '安装 MapManager.MapGunInit Hook...');
    try {
        Interceptor.attach(B.add(R.MM_MapGun), {
            onEnter: function(args) {
                if (!mm) {
                    mm = args[0];
                    mmReady = true;
                    L('i', '✅ MapManager 实例: ' + mm);

                    var sGR = readSpawnPos(mm.add(O.MM_SP_GR).readPointer());
                    var sBL = readSpawnPos(mm.add(O.MM_SP_BL).readPointer());
                    var sNet = readSpawnPos(mm.add(O.MM_SP_Netural).readPointer());

                    L('i', '  出生点:');
                    if (sNet) L('i', '    SP_Netural: (' + sNet.x.toFixed(1) + ', ' + sNet.y.toFixed(1) + ', ' + sNet.z.toFixed(1) + ')');
                    else     L('i', '    SP_Netural: (空)');
                    if (sBL)  L('i', '    SP_BL:      (' + sBL.x.toFixed(1) + ', ' + sBL.y.toFixed(1) + ', ' + sBL.z.toFixed(1) + ')');
                    else     L('i', '    SP_BL:      (空)');
                    if (sGR)  L('i', '    SP_GR:      (' + sGR.x.toFixed(1) + ', ' + sGR.y.toFixed(1) + ', ' + sGR.z.toFixed(1) + ')');
                    else     L('i', '    SP_GR:      (空)');

                    spawn = sGR || sBL;
                    L('i', '  → 选中: ' + (sGR ? 'SP_GR(潜伏者=佣兵)' : sBL ? 'SP_BL(保卫者)' : '无可用出生点'));
                    send(JSON.stringify({ t: 'mm', addr: mm.toString() }));
                }
            }
        });
        L('i', '✅ MapGunInit Hook OK');
    } catch (e) {
        L('e', 'MapGunInit Hook 失败: ' + e.message);
    }

    // ================================================================
    // Hook: Player.Update → 执行传送入口
    // ================================================================
    L('i', '');
    L('i', '安装 Player.Update Hook...');
    try {
        Interceptor.attach(B.add(R.P_Update), {
            onEnter: function(args) {
                if (!ntp) return;
                ntp = false;

                if (!gm || !mm) {
                    L('w', 'GM/MM 未就绪, 忽略传送请求');
                    send(JSON.stringify({ t: 'err', msg: 'GM/MM not ready' }));
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
        // 触发传送
        teleport: function() {
            if (!gm || !mm) {
                var msg = '就绪状态: GM=' + (gm ? '✓' : '✗') + ' MM=' + (mm ? '✓' : '✗');
                L('w', '实例未就绪: ' + msg);
                send(JSON.stringify({ t: 'err', msg: msg }));
                return 'ERR: ' + msg;
            }
            ntp = true;
            L('i', '');
            L('i', '★ ★ ★ 收到传送指令 ★ ★ ★');
            return 'OK: 已触发, 等待下一帧 Player.Update';
        },

        // 查看状态
        getStatus: function() {
            var info = {
                gm: gm ? gm.toString() : null,
                mm: mm ? mm.toString() : null,
                spawn: spawn,
                tracked: trackedPlayers.length,
                ready: !!(gm && mm)
            };
            L('i', 'Status: GM=' + (gm ? '✓' : '✗') + ' MM=' + (mm ? '✓' : '✗') + ' Tracked=' + trackedPlayers.length);
            return info;
        },

        // 查看诊断信息
        diag: function() {
            if (!gm) { L('w', 'GM 未就绪'); return { error: 'GM not ready' }; }

            var result = {};

            try {
                // allPlayers
                var ap = gm.add(O.GM_allPlayers).readPointer();
                var arrData = readArray(ap);
                result.allPlayers = arrData ? { len: arrData.len } : null;
                L('i', 'allPlayers: ' + (arrData ? arrData.len : 'null'));
            } catch (e) { result.allPlayers = { err: e.message }; }

            // List 字段
            var listFields = [
                { name: 'entityBL_Alive', off: O.GM_entityBL_Alive },
                { name: 'entityGR_Alive', off: O.GM_entityGR_Alive },
                { name: 'playersBL', off: O.GM_playersBL },
                { name: 'playersBL_Alive', off: O.GM_playersBL_Alive },
                { name: 'playersGR', off: O.GM_playersGR },
                { name: 'playersGR_Alive', off: O.GM_playersGR_Alive },
            ];

            for (var fi = 0; fi < listFields.length; fi++) {
                try {
                    var f = listFields[fi];
                    var lp = gm.add(f.off).readPointer();
                    var ld = readList(lp);
                    result[f.name] = ld ? { size: ld.len } : null;
                    L('i', f.name + ' (+0x' + f.off.toString(16) + '): ' + (ld ? 'size=' + ld.len : 'null/empty'));
                } catch (e) {
                    result[listFields[fi].name] = { err: e.message };
                }
            }

            L('i', 'TrackedPlayers: ' + trackedPlayers.length);
            var all = collectAllPlayers();
            L('i', 'After dedup total: ' + all.length);

            result.trackedPlayers = trackedPlayers.length;
            result.totalUnique = all.length;
            return result;
        }
    };

    L('i', '');
    L('i', '╔══════════════════════════════════════════════╗');
    L('i', '║  v20 已就绪                                  ║');
    L('i', '║                                            ║');
    L('i', '║  RPC 接口:                                  ║');
    L('i', '║    rpc.exports.teleport()  → 传送所有Bot    ║');
    L('i', '║    rpc.exports.getStatus() → 查看状态       ║');
    L('i', '║    rpc.exports.diag()      → 诊断GM列表     ║');
    L('i', '╚══════════════════════════════════════════════╝');
})();
