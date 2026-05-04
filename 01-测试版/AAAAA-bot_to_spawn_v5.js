// ============================================================
// Bot 出生点集合器 v5 — 全模式支持 + 修复传送崩溃
// 修复: MapGunInit(仅生化) → NewGameRoundStart(全模式) 捕获 mmInstance
//       gm_ready 即可启用按钮（GameManager 全模式都有）
// ============================================================

(function() {
    'use strict';

    function sendLog(level, msg) {
        var prefix = '[BotToSpawn] ';
        if (level === 'error') console.error(prefix + msg);
        else if (level === 'warn') console.warn(prefix + msg);
        else console.log(prefix + msg);
    }

    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) {
        sendLog('error', 'GameAssembly.dll 未找到');
        return;
    }
    var base = mod.base;

    var RVA = {
        GameManager_AddPlayer:      0xAF9A90,  // Image 50 ✓
        MapManager_NewGameRound:    0xAEBCB0,  // Image 50 ✓ 全模式触发
        Player_Update:              0xB551D0,  // Image 50 ✓
        Player_get_isMyPlayer:      0xB55FD0,  // Image 50 ✓
        Entity_get_isDead:          0xB400E0,  // Image 50 ✓
        Player_SetPos:              0xB534C0,  // Image 50 ✓
    };

    var O = {
        Player_clientData:     0x94,
        ClientData_isBot:      0x14,
        GameManager_allPlayers: 0x1C,
        MapManager_SP_BL:      0x10,
    };

    var gmInstance = null;
    var mmInstance = null;
    var pendingTeleport = false;
    var teleportCount = 0;

    var isMyPlayerFn = new NativeFunction(base.add(RVA.Player_get_isMyPlayer), 'bool', ['pointer', 'pointer']);
    var getIsDeadFn  = new NativeFunction(base.add(RVA.Entity_get_isDead), 'bool', ['pointer', 'pointer']);
    var setPosFn     = new NativeFunction(base.add(RVA.Player_SetPos), 'void', ['pointer', 'pointer', 'pointer']);

    var vecBuf = Memory.alloc(16);

    function readFirstSpawnPoint(spArrPtr) {
        if (!spArrPtr || spArrPtr.isNull()) return null;
        var len = spArrPtr.add(0xC).readU32();
        if (len === 0) return null;
        var elem = spArrPtr.add(0x10);
        return { x: elem.readFloat(), y: elem.add(4).readFloat(), z: elem.add(8).readFloat() };
    }

    // ============================================================
    // Hook 1: GameManager.AddPlayer — 捕获 gmInstance
    // ============================================================
    try {
        Interceptor.attach(base.add(RVA.GameManager_AddPlayer), {
            onEnter: function(args) {
                if (!gmInstance) {
                    gmInstance = args[0];
                    send(JSON.stringify({type:'gm_ready'}));
                    sendLog('info', '✓ GameManager @ ' + gmInstance);
                }
            }
        });
        sendLog('info', 'Hook AddPlayer OK');
    } catch(e) { sendLog('error', 'Hook AddPlayer失败: ' + e.message); }

    // ============================================================
    // Hook 2: MapManager.NewGameRoundStart — 全模式捕获 mmInstance
    // ============================================================
    try {
        Interceptor.attach(base.add(RVA.MapManager_NewGameRound), {
            onEnter: function(args) {
                if (!mmInstance) {
                    mmInstance = args[0];
                    send(JSON.stringify({type:'mm_ready'}));
                    sendLog('info', '✓ MapManager @ ' + mmInstance + ' (NewGameRoundStart)');
                }
            }
        });
        sendLog('info', 'Hook NewGameRoundStart OK');
    } catch(e) { sendLog('error', 'Hook NewGameRoundStart失败: ' + e.message); }

    // ============================================================
    // Hook 3: Player.Update — 主线程入口
    // ============================================================
    try {
        Interceptor.attach(base.add(RVA.Player_Update), {
            onEnter: function(args) {
                if (!pendingTeleport) return;
                pendingTeleport = false;
                sendLog('info', '=== 收到传送信号 ===');
                executeTeleport();
                sendLog('info', '=== 执行完毕 ===');
            }
        });
        sendLog('info', 'Hook Player.Update OK');
    } catch(e) { sendLog('error', 'Hook Player.Update失败: ' + e.message); }

    // ============================================================
    // executeTeleport
    // ============================================================
    function executeTeleport() {
        teleportCount++;

        if (!gmInstance) {
            send(JSON.stringify({type:'error', msg:'GameManager未就绪'}));
            return;
        }

        // --- allPlayers ---
        var allPlayersPtr = gmInstance.add(O.GameManager_allPlayers).readPointer();
        if (!allPlayersPtr || allPlayersPtr.isNull()) {
            send(JSON.stringify({type:'error', msg:'allPlayers为null'}));
            return;
        }
        var totalPlayers = allPlayersPtr.add(0xC).readU32();
        sendLog('info', '总Player数: ' + totalPlayers);

        // --- 出生点 ---
        var spawnPoint = null;
        if (mmInstance) {
            try {
                var spBLArr = mmInstance.add(O.MapManager_SP_BL).readPointer();
                spawnPoint = readFirstSpawnPoint(spBLArr);
            } catch(e) {}
        }
        if (!spawnPoint) {
            // mmInstance 未就绪 → 从 myPlayer 推测出生点
            sendLog('info', 'MapManager未就绪，使用(0,0,0)兜底');
            spawnPoint = { x: 0, y: 0, z: 0 };
        }
        sendLog('info', '出生点: (' + spawnPoint.x.toFixed(1) + ', ' + spawnPoint.y.toFixed(1) + ', ' + spawnPoint.z.toFixed(1) + ')');

        vecBuf.writeFloat(spawnPoint.x);
        vecBuf.add(4).writeFloat(spawnPoint.y);
        vecBuf.add(8).writeFloat(spawnPoint.z);

        // --- 遍历传送 ---
        var botCount = 0, deadCount = 0, skipCount = 0;

        for (var i = 0; i < totalPlayers; i++) {
            try {
                var pp = allPlayersPtr.add(0x10 + i * 8).readPointer();
                if (!pp || pp.isNull()) { skipCount++; continue; }

                if (isMyPlayerFn(pp, ptr(0))) { skipCount++; continue; }

                var cd = pp.add(O.Player_clientData).readPointer();
                if (!cd || cd.isNull()) { skipCount++; continue; }

                if (!cd.add(O.ClientData_isBot).readU8()) { skipCount++; continue; }

                if (getIsDeadFn(pp, ptr(0))) { deadCount++; continue; }

                setPosFn(pp, vecBuf, ptr(0));
                botCount++;
            } catch(e) {
                sendLog('warn', 'Player#' + i + ' 异常: ' + e.message);
                break;
            }
        }

        var msg = '传送 ' + botCount + ' 个Bot';
        if (deadCount > 0) msg += ' | ' + deadCount + ' 已死亡跳过';
        if (skipCount > 0) msg += ' | ' + skipCount + ' 跳过';
        sendLog('info', msg);
        send(JSON.stringify({type:'done', count:botCount, msg:msg}));
    }

    rpc.exports = {
        teleportBots: function() {
            if (!gmInstance) {
                send(JSON.stringify({type:'error', msg:'GameManager未就绪，请进入房间'}));
                return;
            }
            pendingTeleport = true;
            sendLog('info', '收到传送指令');
        },
        getStatus: function() {
            return JSON.stringify({
                gmReady: gmInstance !== null,
                mmReady: mmInstance !== null,
                teleportCount: teleportCount
            });
        }
    };

    sendLog('info', '===============================');
    sendLog('info', 'Bot出生点集合器 v5 已加载');
    sendLog('info', '全模式通用 | NewGameRoundStart');
    sendLog('info', '===============================');
})();
