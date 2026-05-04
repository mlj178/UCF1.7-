// ============================================================
// Bot 出生点集合器 v3 — DEBUG 版（逐行日志定位崩溃点）
// v2 问题：成功读取出生点后，在循环中闪退，需定位具体哪行崩溃
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
    sendLog('info', 'GameAssembly.dll base = ' + base);

    var RVA = {
        GameManager_AddPlayer:   0xAF9A90,
        MapManager_MapGunInit:   0xAEBB70,
        Player_Update:           0xB551D0,
        Player_get_isMyPlayer:   0xB55FD0,
        Entity_get_isDead:       0xB400E0,
        Player_SetPos:           0xB534C0,
    };

    var Player_clientData      = 0x94;
    var ClientData_isBot       = 0x14;
    var GameManager_allPlayers = 0x1C;
    var MapManager_SP_BL       = 0x10;

    var gmInstance = null;
    var mmInstance = null;
    var pendingTeleport = false;
    var teleportCount = 0;

    // ============================================================
    // NativeFunctions — 修正：IL2CPP 方法都有 MethodInfo* 参数
    // ============================================================
    var isMyPlayerFn = new NativeFunction(base.add(RVA.Player_get_isMyPlayer), 'bool', ['pointer', 'pointer']);
    var getIsDeadFn  = new NativeFunction(base.add(RVA.Entity_get_isDead),   'bool', ['pointer', 'pointer']);
    var setPosFn     = new NativeFunction(base.add(RVA.Player_SetPos),        'void', ['pointer', 'pointer', 'pointer']);

    var vecBuf = Memory.alloc(16); // 16字节避免对齐问题

    // ============================================================
    // 读取 SpawnPoint[0]
    // ============================================================
    function readFirstSpawnPoint(spArrPtr) {
        if (!spArrPtr || spArrPtr.isNull()) return null;
        var len = spArrPtr.add(0xC).readU32();
        sendLog('info', 'SP_BL 数组长度 = ' + len);
        if (len === 0) return null;
        var elem = spArrPtr.add(0x10);
        return {
            x: elem.readFloat(),
            y: elem.add(4).readFloat(),
            z: elem.add(8).readFloat()
        };
    }

    // ============================================================
    // Hook: 捕获 GameManager
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
        sendLog('info', 'Hook AddPlayer @ ' + ptr(base.add(RVA.GameManager_AddPlayer)));
    } catch(e) {
        sendLog('error', 'AddPlayer hook 失败: ' + e.message);
    }

    // ============================================================
    // Hook: 捕获 MapManager
    // ============================================================
    try {
        Interceptor.attach(base.add(RVA.MapManager_MapGunInit), {
            onEnter: function(args) {
                if (!mmInstance) {
                    mmInstance = args[0];
                    send(JSON.stringify({type:'mm_ready'}));
                    sendLog('info', '✓ MapManager @ ' + mmInstance);
                }
            }
        });
        sendLog('info', 'Hook MapGunInit @ ' + ptr(base.add(RVA.MapManager_MapGunInit)));
    } catch(e) {
        sendLog('error', 'MapGunInit hook 失败: ' + e.message);
    }

    // ============================================================
    // Hook: Player.Update 作为主线程入口
    // ============================================================
    try {
        Interceptor.attach(base.add(RVA.Player_Update), {
            onEnter: function(args) {
                if (!pendingTeleport) return;
                pendingTeleport = false;
                sendLog('info', '=== executeTeleport 开始 (Player.Update 触发) ===');
                executeTeleport();
                sendLog('info', '=== executeTeleport 结束 ===');
            }
        });
        sendLog('info', 'Hook Player.Update @ ' + ptr(base.add(RVA.Player_Update)));
    } catch(e) {
        sendLog('error', 'Player.Update hook 失败: ' + e.message);
    }

    // ============================================================
    // 核心 — 逐行日志版
    // ============================================================
    function executeTeleport() {
        teleportCount++;

        sendLog('info', '[1] 检查 gmInstance...');
        if (!gmInstance) {
            send(JSON.stringify({type:'error', msg:'GameManager 未就绪'}));
            return;
        }
        sendLog('info', '[2] gmInstance = ' + gmInstance);

        sendLog('info', '[3] 检查 mmInstance...');
        if (!mmInstance) {
            send(JSON.stringify({type:'error', msg:'MapManager 未就绪'}));
            return;
        }
        sendLog('info', '[4] mmInstance = ' + mmInstance);

        // --- 读 allPlayers ---
        sendLog('info', '[5] 读取 allPlayers...');
        var allPlayersPtr;
        try {
            allPlayersPtr = gmInstance.add(GameManager_allPlayers).readPointer();
            sendLog('info', '[6] allPlayers 指针 = ' + allPlayersPtr);
        } catch(e) {
            sendLog('error', '[6a] 读 allPlayers 指针失败: ' + e.message);
            send(JSON.stringify({type:'error', msg:'读allPlayers失败: ' + e.message}));
            return;
        }

        if (!allPlayersPtr || allPlayersPtr.isNull()) {
            sendLog('error', '[7] allPlayers 为 null');
            send(JSON.stringify({type:'error', msg:'allPlayers 为 null'}));
            return;
        }

        // IL2CPP 对象头: [0x00] klass(8B) [0x08] monitor(8B) [0x0C] length(4B)
        try {
            var klass = allPlayersPtr.add(0x0).readPointer();
            var monitor = allPlayersPtr.add(0x8).readPointer();
            var totalPlayers = allPlayersPtr.add(0xC).readU32();
            sendLog('info', '[8] klass=' + klass + ' monitor=' + monitor + ' length=' + totalPlayers);
        } catch(e) {
            sendLog('error', '[8a] 读数组头失败: ' + e.message);
            send(JSON.stringify({type:'error', msg:'读数组头失败'}));
            return;
        }

        // --- 读出生点 ---
        sendLog('info', '[9] 读取 SP_BL...');
        var spBLArr;
        try {
            spBLArr = mmInstance.add(MapManager_SP_BL).readPointer();
            sendLog('info', '[10] SP_BL 数组指针 = ' + spBLArr);
        } catch(e) {
            sendLog('error', '[10a] 读 SP_BL 失败: ' + e.message);
            send(JSON.stringify({type:'error', msg:'读SP_BL失败'}));
            return;
        }

        var spawnPoint = readFirstSpawnPoint(spBLArr);
        if (!spawnPoint) {
            sendLog('error', '[11] 出生点读取失败');
            send(JSON.stringify({type:'error', msg:'出生点读取失败'}));
            return;
        }
        sendLog('info', '[11] 出生点: (' + spawnPoint.x.toFixed(1) + ', ' + spawnPoint.y.toFixed(1) + ', ' + spawnPoint.z.toFixed(1) + ')');

        // --- 写 vecBuf ---
        sendLog('info', '[12] 写入 vecBuf 缓冲区...');
        try {
            vecBuf.writeFloat(spawnPoint.x);
            vecBuf.add(4).writeFloat(spawnPoint.y);
            vecBuf.add(8).writeFloat(spawnPoint.z);
            sendLog('info', '[12] vecBuf 写入完成');
        } catch(e) {
            sendLog('error', '[12a] vecBuf 写入失败: ' + e.message);
            return;
        }

        // --- 验证 vecBuf 能读回 ---
        sendLog('info', '[13] 验证 vecBuf: ' +
            vecBuf.readFloat().toFixed(1) + ', ' +
            vecBuf.add(4).readFloat().toFixed(1) + ', ' +
            vecBuf.add(8).readFloat().toFixed(1));

        // ============================================================
        // 逐个 Player 调试 — v3 先只处理第 1 个
        // ============================================================
        sendLog('info', '[14] === 开始逐个 Player 调试 ===');

        // ---- Player 0 ----
        var i = 0;
        sendLog('info', '[15] Player#' + i + ' 读取指针...');
        var playerPtr = null;
        try {
            playerPtr = allPlayersPtr.add(0x10 + i * 8).readPointer();
            sendLog('info', '[16] Player#' + i + ' 指针 = ' + playerPtr);
        } catch(e) {
            sendLog('error', '[16a] 读 Player#' + i + ' 指针失败: ' + e.message);
        }

        if (playerPtr && !playerPtr.isNull()) {
            sendLog('info', '[17] 调用 isMyPlayer...');
            try {
                var isMine = isMyPlayerFn(playerPtr, ptr(0));
                sendLog('info', '[18] isMyPlayer = ' + isMine);
            } catch(e) {
                sendLog('error', '[18a] isMyPlayer 崩溃: ' + e.message);
            }

            if (isMine) {
                sendLog('info', '[19] 是自己，跳过');
            } else {
                sendLog('info', '[19] 不是自己，继续');

                sendLog('info', '[20] 读取 clientData...');
                try {
                    var cdPtr = playerPtr.add(Player_clientData).readPointer();
                    sendLog('info', '[21] clientData = ' + cdPtr);
                    if (cdPtr && !cdPtr.isNull()) {
                        var botVal = cdPtr.add(ClientData_isBot).readU8();
                        sendLog('info', '[22] isBot = ' + botVal);
                    } else {
                        sendLog('info', '[21a] clientData 为 null');
                    }
                } catch(e) {
                    sendLog('error', '[20a] clientData 读取出错: ' + e.message);
                }

                sendLog('info', '[23] 调用 isDead...');
                try {
                    var dead = getIsDeadFn(playerPtr, ptr(0));
                    sendLog('info', '[24] isDead = ' + dead);
                } catch(e) {
                    sendLog('error', '[24a] isDead 崩溃: ' + e.message);
                }

                sendLog('info', '[25] 调用 SetPos...');
                try {
                    setPosFn(playerPtr, vecBuf, ptr(0));
                    sendLog('info', '[26] ★ SetPos 调用成功！');
                } catch(e) {
                    sendLog('error', '[26a] SetPos 崩溃: ' + e.message);
                }
            }
        }

        // ---- Player 1（看看第二个能否读到）----
        i = 1;
        sendLog('info', '[30] Player#' + i + ' 读取指针...');
        try {
            playerPtr = allPlayersPtr.add(0x10 + i * 8).readPointer();
            sendLog('info', '[31] Player#' + i + ' 指针 = ' + playerPtr);
        } catch(e) {
            sendLog('error', '[31a] 读 Player#' + i + ' 失败: ' + e.message);
        }
        // 只验证读取，不再调用 SetPos

        // ---- Player 2 ----
        i = 2;
        sendLog('info', '[32] Player#' + i + ' 读取指针...');
        try {
            playerPtr = allPlayersPtr.add(0x10 + i * 8).readPointer();
            sendLog('info', '[33] Player#' + i + ' 指针 = ' + playerPtr);
        } catch(e) {
            sendLog('error', '[33a] 读 Player#' + i + ' 失败: ' + e.message);
        }

        sendLog('info', '===== DEBUG 结束 =====');
    }

    // ============================================================
    // RPC
    // ============================================================
    rpc.exports = {
        teleportBots: function() {
            if (!gmInstance) {
                send(JSON.stringify({type:'error', msg:'GameManager 未就绪'}));
                return;
            }
            if (!mmInstance) {
                send(JSON.stringify({type:'error', msg:'MapManager 未就绪'}));
                return;
            }
            pendingTeleport = true;
            sendLog('info', '已收到传送指令，等待下一帧...');
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
    sendLog('info', 'Bot出生点集合器 v3 DEBUG 版');
    sendLog('info', '等待进入多人生化模式房间...');
    sendLog('info', '===============================');
})();
