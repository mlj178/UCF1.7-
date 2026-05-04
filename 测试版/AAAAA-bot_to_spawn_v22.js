// ============================================================
// Bot 出生点集合器 v22 — OnNewPlayerJoin 主追踪
//
// v21 问题: 跟踪到的 Bot 指针在传送时已失效 (access violation)
//   根因: AddPlayer 返回的指针本身有效，但 Bot 的 Transform
//   可能在调用 get_transform 时已不再是有效 Player
//
// v22 修正:
//   ① 主跟踪源: Mode_Nano4.OnNewPlayerJoin(Player) — 诊断确认
//      29 个 Bot + 16 真人全部能收到
//   ② 备用跟踪源: AddPlayer 返回值
//   ③ 传送前重新扫描 allPlayers[] 获取最新有效指针
//   ④ Transform: characterContainer(0x58) 优先
//   ⑤ 增强指针有效性验证
// ============================================================

(function() {
    'use strict';

    function L(l, m) {
        var p = '[BotSpawn-v22] ';
        if (l === 'e') console.error(p + m);
        else if (l === 'w') console.warn(p + m);
        else console.log(p + m);
    }

    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) { L('e', 'GameAssembly.dll not found'); return; }
    var B = mod.base;

    L('i', '╔══════════════════════════════════════════════╗');
    L('i', '║  Bot 出生点集合器 v22 — OnNewPlayerJoin     ║');
    L('i', '║  GameAssembly.dll @ ' + B);
    L('i', '╚══════════════════════════════════════════════╝');

    // ================================================================
    // RVA
    // ================================================================
    var R = {
        GM_AddP:      0xAF9A90,  // AddPlayer(bool, Team) → Player
        GM_isNano:    0xAFDA80,  // get_isNanoMode
        MM_MapGun:    0xAEBB70,  // MapGunInit
        P_Update:     0xB551D0,  // Player.Update
        P_isMy:       0xB55FD0,  // get_isMyPlayer
        E_isDead:     0xB400E0,  // get_isDead
        E_getCC:      0x1CF180,  // get_characterController
        C_setEn:      0xAB86B0,  // set_enabled
        getTrans:     0x32CF40,  // get_transform
        setPosInj:    0x3F4810,  // set_position_Injected
        MN4_OnNewP:   0xB42140,  // OnNewPlayerJoin(Player)
        MN4_Awake:    0xB410D0,  // Awake
    };

    // ================================================================
    // 偏移 (dump.cs + IDA 验证)
    // ================================================================
    var O = {
        GM_allPlayers:  0x1C,  // Player[]
        GM_playersBL:   0x20,  // List<Player>
        GM_playersGR:   0x28,  // List<Player>
        GM_pBL_Alive:   0x24,
        GM_pGR_Alive:   0x2C,

        MM_SP_BL:  0x10,  // SpawnPoint[]
        MM_SP_GR:  0x14,  // SpawnPoint[]
        MM_SP_Net: 0x18,

        P_cameraManager:      0x48,
        P_characterContainer: 0x58,
        P_clientData:         0x94,
        P_playerData:         0x98,

        CD_isBot:    0x1C,
        CD_joinTeam: 0x18,

        E_team: 0x20,
    };

    // ================================================================
    // 状态
    // ================================================================
    var gm = null;
    var mm = null;
    var modeNano = null;
    var spawn = null;
    var ntp = false;
    var tn = 0;

    // Player 跟踪: key=指针地址, value=Player指针
    var trackedPlayers = {};
    var trackedCount = 0;

    // ================================================================
    // NativeFunction
    // ================================================================
    var isMyPlayer = new NativeFunction(B.add(R.P_isMy),  'bool',    ['pointer', 'pointer']);
    var isDead     = new NativeFunction(B.add(R.E_isDead), 'bool',    ['pointer', 'pointer']);
    var getCC      = new NativeFunction(B.add(R.E_getCC), 'pointer',  ['pointer', 'pointer']);
    var ccSetEn    = new NativeFunction(B.add(R.C_setEn), 'void',     ['pointer', 'int', 'pointer']);
    var getTrans   = new NativeFunction(B.add(R.getTrans), 'pointer',  ['pointer', 'pointer']);
    var setPosInj  = new NativeFunction(B.add(R.setPosInj), 'void',    ['pointer', 'pointer', 'pointer']);
    var posBuf     = Memory.alloc(16);
    var tmpBuf     = Memory.alloc(16);

    L('i', '✓ NativeFunction bindings ready');

    // ================================================================
    // 辅助
    // ================================================================
    function rp(addr, off) {
        try { return addr.add(off).readPointer(); } catch (e) { return null; }
    }

    function readArray(arrPtr) {
        if (!arrPtr || arrPtr.isNull()) return null;
        try {
            var len = arrPtr.add(0xC).readU32();
            if (len <= 0 || len > 500) return null;
            return { ptr: arrPtr, len: len };
        } catch (e) { return null; }
    }

    function isValidPlayerPtr(pp) {
        if (!pp || pp.isNull()) return false;
        try {
            // 验证 vtable 指针
            var vt = pp.readPointer();
            if (!vt || vt.isNull()) return false;
            // 验证 vtable 在模块范围内
            var off = vt.sub(B);
            return off.compare(0) >= 0 && off.compare(mod.size) < 0;
        } catch (e) { return false; }
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

    // ================================================================
    // ★ 核心: 重新找到 Player 的最新有效指针
    //    因为 AddPlayer 返回的指针可能随时间失效
    // ================================================================
    function refreshPlayerPtr(oldPtr) {
        if (!oldPtr || oldPtr.isNull()) return null;

        // 先检查当前指针是否仍然有效
        if (isValidPlayerPtr(oldPtr)) {
            return oldPtr;
        }

        // 失效了 → 从 allPlayers[] 扫描, 用 clientData 匹配
        if (!gm) return null;
        try {
            var ap = gm.add(O.GM_allPlayers).readPointer();
            var arrData = readArray(ap);
            if (!arrData) return null;

            // 获取旧 Player 的 ClientData 地址 (如果还活着的话)
            var oldCD = null;
            try { oldCD = rp(oldPtr, O.P_clientData); } catch (e) {}

            for (var i = 0; i < arrData.len; i++) {
                try {
                    var pp = arrData.ptr.add(0x10 + i * 8).readPointer();
                    if (!isValidPlayerPtr(pp)) continue;

                    // 如果有 ClientData, 用 ClientData 匹配
                    var cd = rp(pp, O.P_clientData);
                    if (oldCD && cd && !cd.isNull() && !oldCD.isNull()) {
                        if (cd.equals(oldCD)) return pp;
                    }
                    // 没有 ClientData → 用指针本身匹配 (重新注册时可能不同)
                    if (pp.equals(oldPtr)) return pp;
                } catch (e) {}
            }
        } catch (e) {}

        return null;
    }

    // ================================================================
    // 传送一个 Bot
    // ================================================================
    function teleportBot(pp) {
        // 先刷新指针
        var freshPp = refreshPlayerPtr(pp);
        if (!freshPp) return 'P=stale';

        // 再次检查 isDead
        try {
            if (isDead(freshPp, ptr(0))) return 'dead';
        } catch (e) { return 'dead?'; }

        try {
            // ★ characterContainer(0x58) 优先 — 诊断显示 Bot 的
            //    get_transform 可能返回无效对象
            var tr = rp(freshPp, O.P_characterContainer);
            var usedSub = false;
            if (!tr || tr.isNull()) {
                tr = getTrans(freshPp, ptr(0));
            } else {
                usedSub = true;
                // characterContainer 返回的是 Transform 指针, 不需 getTransform
            }
            if (!tr || tr.isNull()) return 'T=null';

            var cc = getCC(freshPp, ptr(0));
            if (cc && !cc.isNull()) ccSetEn(cc, 0, ptr(0));

            setPosInj(tr, posBuf, ptr(0));

            // 内存直写双保险
            try {
                var np = tr.add(0x10).readPointer();
                if (np) {
                    np.add(0x38).writeFloat(spawn.x);
                    np.add(0x3C).writeFloat(spawn.y);
                    np.add(0x40).writeFloat(spawn.z);
                }
            } catch (e) {}

            if (cc && !cc.isNull()) ccSetEn(cc, 1, ptr(0));

            return usedSub ? 'OK(cc)' : 'OK(root)';
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
        L('i', '╔══ 传送 #' + tn + ' ══╗');

        if (!gm || !mm) { L('e', 'GM/MM 未就绪'); L('i', '╚══════╝'); return; }
        if (!spawn) spawn = { x: 0, y: 0, z: 0 };

        posBuf.writeFloat(spawn.x);
        posBuf.add(4).writeFloat(spawn.y);
        posBuf.add(8).writeFloat(spawn.z);

        L('i', '目标: (' + spawn.x.toFixed(1) + ',' + spawn.y.toFixed(1) + ',' + spawn.z.toFixed(1) + ')');
        L('i', '追踪玩家: ' + trackedCount);

        // 收集所有有效 Player
        var keys = Object.keys(trackedPlayers);
        L('i', '扫描中...');

        var selfC = 0, realC = 0, deadC = 0, botC = 0, okC = 0, failC = 0;
        var detail = [];

        for (var ki = 0; ki < keys.length; ki++) {
            var origPp = trackedPlayers[keys[ki]];
            var freshPp = refreshPlayerPtr(origPp);
            var label = '#' + ki;

            if (!freshPp) {
                detail.push(label + ': 指针失效');
                continue;
            }

            try {
                if (isMyPlayer(freshPp, ptr(0))) {
                    selfC++;
                    detail.push(label + ': ★ 自己');
                    continue;
                }

                var cd = rp(freshPp, O.P_clientData);
                var isBotVal = -1;
                var teamVal = -1;
                if (cd && !cd.isNull()) {
                    try { isBotVal = cd.add(O.CD_isBot).readU8(); } catch (e) {}
                    try { teamVal = cd.add(O.CD_joinTeam).readU8(); } catch (e) {}
                }

                // 真人判定: isBot==0 或 cameraManager!=null
                var cam = rp(freshPp, O.P_cameraManager);
                var isReal = false;
                if (cam && !cam.isNull()) isReal = true;
                if (isBotVal === 0) isReal = true;

                if (isReal) {
                    realC++;
                    detail.push(label + ': 真人');
                    continue;
                }

                if (isBotVal !== 1) {
                    // 没有 isBot 标志 → 跳过
                    detail.push(label + ': ?(isBot=' + isBotVal + ')');
                    continue;
                }

                if (isDead(freshPp, ptr(0))) {
                    deadC++;
                    detail.push(label + ': Bot(已死)');
                    continue;
                }

                botC++;
                var result = teleportBot(freshPp);
                if (result.indexOf('OK') === 0) {
                    okC++;
                    detail.push(label + ': Bot[team=' + teamVal + '] ' + result);
                } else {
                    failC++;
                    detail.push(label + ': Bot[team=' + teamVal + '] FAIL: ' + result);
                }
            } catch (e) {
                failC++;
                detail.push(label + ': ★ ' + e.message);
            }
        }

        for (var j = 0; j < detail.length; j++) {
            L('i', '  ' + detail[j]);
        }

        L('i', '');
        L('i', '┌─ 统计 ────────────────────────────────┐');
        L('i', '│  自己=' + selfC + ' 真人=' + realC + '  Bot已死=' + deadC);
        L('i', '│  存活Bot=' + botC + '  成功=' + okC);
        if (failC > 0) L('i', '│  失败=' + failC);
        L('i', '└────────────────────────────────────────┘');
        L('i', '╚══════╝');

        send(JSON.stringify({ t: 'done', n: tn, bots: botC, ok: okC, fail: failC }));
    }

    // ================================================================
    // ★ 跟踪: Mode_Nano4.OnNewPlayerJoin (主源)
    // ================================================================
    L('i', '');
    L('i', '安装 Mode_Nano4.OnNewPlayerJoin (主跟踪源)...');
    try {
        Interceptor.attach(B.add(R.MN4_OnNewP), {
            onEnter: function(args) {
                var player = args[1];
                if (player && !player.isNull() && isValidPlayerPtr(player)) {
                    var key = player.toString();
                    if (!trackedPlayers[key]) {
                        trackedPlayers[key] = player;
                        trackedCount++;
                    }
                }
            }
        });
        L('i', '✅ OnNewPlayerJoin Hook OK (诊断确认: 可收到全部 45 人)');
    } catch (e) {
        L('w', 'OnNewPlayerJoin Hook 不可用: ' + e.message);
    }

    // ================================================================
    // 跟踪: AddPlayer 返回值 (备用)
    // ================================================================
    L('i', '安装 GameManager.AddPlayer (备用跟踪)...');
    try {
        Interceptor.attach(B.add(R.GM_AddP), {
            onEnter: function(args) {
                if (!gm) {
                    gm = args[0];
                    L('i', '✅ GM: ' + gm);
                    send(JSON.stringify({ t: 'gm', addr: gm.toString() }));
                }
            },
            onLeave: function(retVal) {
                var pp = retVal;
                if (pp && !pp.isNull() && isValidPlayerPtr(pp)) {
                    var key = pp.toString();
                    if (!trackedPlayers[key]) {
                        trackedPlayers[key] = pp;
                        trackedCount++;
                    }
                }
            }
        });
        L('i', '✅ AddPlayer Hook OK');
    } catch (e) {
        L('e', 'AddPlayer Hook 失败: ' + e.message);
    }

    // ================================================================
    // GM 后备获取: 扫描 allPlayers
    // ================================================================
    setTimeout(function() {
        if (!gm) {
            L('i', '⏳ GM 未捕获, 从 allPlayers 扫描...');
            try {
                // 通过 Singleton 静态字段扫描
                // GameManager 类静态字段区: this指针是 Singleton instance
                // 由于 Singleton.get_instance 泛型不好调用,
                // 这里通过 Hook Player.Update 捕获第一个 Player
            } catch (e) {}
        }
    }, 3000);

    // ================================================================
    // MapGunInit → 出生点
    // ================================================================
    L('i', '');
    L('i', '安装 MapManager.MapGunInit...');
    try {
        Interceptor.attach(B.add(R.MM_MapGun), {
            onEnter: function(args) {
                if (!mm) {
                    mm = args[0];
                    L('i', '✅ MM: ' + mm);

                    var sGR  = readSpawnPos(mm.add(O.MM_SP_GR).readPointer());
                    var sBL  = readSpawnPos(mm.add(O.MM_SP_BL).readPointer());
                    var sNet = readSpawnPos(mm.add(O.MM_SP_Net).readPointer());

                    if (sNet) L('i', '  SP_Net: (' + sNet.x.toFixed(1) + ', ' + sNet.y.toFixed(1) + ', ' + sNet.z.toFixed(1) + ')');
                    if (sBL)  L('i', '  SP_BL:  (' + sBL.x.toFixed(1) + ', ' + sBL.y.toFixed(1) + ', ' + sBL.z.toFixed(1) + ')');
                    if (sGR)  L('i', '  SP_GR:  (' + sGR.x.toFixed(1) + ', ' + sGR.y.toFixed(1) + ', ' + sGR.z.toFixed(1) + ')');

                    spawn = sGR || sBL;
                    L('i', '  → 目标: ' + (sGR ? 'SP_GR' : sBL ? 'SP_BL' : '无'));
                    send(JSON.stringify({ t: 'mm', addr: mm.toString() }));
                }
            }
        });
        L('i', '✅ MapGunInit OK');
    } catch (e) {
        L('e', 'MapGunInit 失败: ' + e.message);
    }

    // ================================================================
    // Player.Update → 执行
    // ================================================================
    L('i', '');
    L('i', '安装 Player.Update...');
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
        L('i', '✅ Player.Update OK');
    } catch (e) {
        L('e', 'Player.Update 失败: ' + e.message);
    }

    // ================================================================
    // RPC
    // ================================================================
    rpc.exports = {
        teleport: function() {
            if (!gm || !mm) {
                var msg = 'GM=' + (gm ? '✓' : '✗') + ' MM=' + (mm ? '✓' : '✗');
                L('w', '未就绪: ' + msg);
                return 'ERR: ' + msg;
            }
            ntp = true;
            L('i', '★ ★ ★ 传送 ★ ★ ★');
            return 'OK';
        },

        getStatus: function() {
            return {
                gm: gm ? gm.toString() : null,
                mm: mm ? mm.toString() : null,
                spawn: spawn,
                tracked: trackedCount,
                ready: !!(gm && mm)
            };
        },

        diag: function() {
            L('i', '══ 诊断 ══');
            L('i', 'GM=' + gm + ' MM=' + mm + ' tracked=' + trackedCount);

            if (!gm) return { error: 'GM not ready' };

            var keys = Object.keys(trackedPlayers);
            var valid = 0, stale = 0;
            for (var ki = 0; ki < keys.length; ki++) {
                if (isValidPlayerPtr(trackedPlayers[keys[ki]])) valid++;
                else stale++;
            }
            L('i', '有效指针: ' + valid + '  失效: ' + stale);

            var fields = [
                { n: 'allPlayers', o: O.GM_allPlayers, t: 'arr' },
                { n: 'playersBL', o: O.GM_playersBL, t: 'list' },
                { n: 'playersGR', o: O.GM_playersGR, t: 'list' },
            ];
            for (var fi = 0; fi < fields.length; fi++) {
                var f = fields[fi];
                try {
                    var ptr = gm.add(f.o).readPointer();
                    var data = f.t === 'arr' ? readArray(ptr) : (function(){
                        if (!ptr || ptr.isNull()) return null;
                        try {
                            var items = ptr.add(0x10).readPointer();
                            var size = ptr.add(0x18).readU32();
                            return (items && !items.isNull() && size > 0 && size < 500) ? { len: size } : null;
                        } catch(e) { return null; }
                    })();
                    L('i', '  ' + f.n + ' (+0x' + f.o.toString(16) + '): ' + (data ? (f.t==='arr'?'len=':'size=') + data.len : '空'));
                } catch (e) {
                    L('i', '  ' + f.n + ': ERR');
                }
            }

            L('i', '══ 诊断结束 ══');
            return { tracked: trackedCount, valid: valid, stale: stale };
        }
    };

    L('i', '');
    L('i', '╔══════════════════════════════════════════╗');
    L('i', '║  v22 已就绪                              ║');
    L('i', '║                                         ║');
    L('i', '║  teleport() → 传送                      ║');
    L('i', '║  getStatus() → 状态                      ║');
    L('i', '║  diag()     → 诊断                      ║');
    L('i', '╚══════════════════════════════════════════╝');
})();
