// ============================================================
// Bot 出生点集合器 v4 — 修复 SetPos 参数顺序 + 全模式 + 详细日志
// v3 定位问题: SetPos 的 Vector3* 和 MethodInfo* 参数顺序颠倒导致空指针崩溃
// 全模式: 不限制模式，任何有 GameManager + MapManager 的模式都能用
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
    sendLog('info', 'GameAssembly base = ' + base);

    var RVA = {
        GameManager_AddPlayer: 0xAF9A90,
        MapManager_MapGunInit: 0xAEBB70,
        Player_Update:         0xB551D0,
        Player_get_isMyPlayer: 0xB55FD0,
        Entity_get_isDead:     0xB400E0,
        Player_SetPos:         0xB534C0,
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

    // ============================================================
    // NativeFunctions — IL2CPP x64 标准签名:
    // 返回值 (__this, 其他参数..., MethodInfo*)
    // 所有函数都加 MethodInfo 参数，避免寄存器垃圾值
    // ============================================================
    sendLog('info', '创建 NativeFunction: isMyPlayer');
    var isMyPlayerFn = new NativeFunction(
        base.add(RVA.Player_get_isMyPlayer),
        'bool', ['pointer', 'pointer']
    );

    sendLog('info', '创建 NativeFunction: isDead');
    var getIsDeadFn = new NativeFunction(
        base.add(RVA.Entity_get_isDead),
        'bool', ['pointer', 'pointer']
    );

    // SetPos(Vector3 pos) → IL2CPP: void __SetPos(__this, Vector3* pos, MethodInfo* method)
    // Vector3(12B > 8B) → MSVC x64 按指针传递
    sendLog('info', '创建 NativeFunction: SetPos');
    var setPosFn = new NativeFunction(
        base.add(RVA.Player_SetPos),
        'void', ['pointer', 'pointer', 'pointer']
    );

    // 预分配 Vector3 缓冲区（16字节防对齐问题）
    var vecBuf = Memory.alloc(16);

    // ============================================================
    // 读取 SpawnPoint[0] 坐标
    // IL2CPP 数组: [0x00]Klass*(8) [0x08]Monitor*(8) [0x0C]length(4) [0x10]elem0
    // SpawnPoint: position(Vector3: x,y,z = 12B) + rotaion(float = 4B)
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
    // Hook: GameManager.AddPlayer(bool isBot, Team team)
    // ============================================================
    try {
        Interceptor.attach(base.add(RVA.GameManager_AddPlayer), {
            onEnter: function(args) {
                if (!gmInstance) {
                    gmInstance = args[0];
                    send(JSON.stringify({type:'gm_ready'}));
                    sendLog('info', '✓ GameManager 已捕获 @ ' + gmInstance);
                }
            }
        });
        sendLog('info', 'Hook AddPlayer @ ' + ptr(base.add(RVA.GameManager_AddPlayer)));
    } catch(e) {
        sendLog('error', 'Hook AddPlayer 失败: ' + e.message);
    }

    // ============================================================
    // Hook: MapManager.MapGunInit()
    // ============================================================
    try {
        Interceptor.attach(base.add(RVA.MapManager_MapGunInit), {
            onEnter: function(args) {
                if (!mmInstance) {
                    mmInstance = args[0];
                    send(JSON.stringify({type:'mm_ready'}));
                    sendLog('info', '✓ MapManager 已捕获 @ ' + mmInstance);
                }
            }
        });
        sendLog('info', 'Hook MapGunInit @ ' + ptr(base.add(RVA.MapManager_MapGunInit)));
    } catch(e) {
        sendLog('error', 'Hook MapGunInit 失败: ' + e.message);
    }

    // ============================================================
    // Hook: Player.Update() — 作为主线程入口执行传送
    // ============================================================
    try {
        Interceptor.attach(base.add(RVA.Player_Update), {
            onEnter: function(args) {
                if (!pendingTeleport) return;
                pendingTeleport = false;
                sendLog('info', '=== 收到传送信号，开始执行 ===');
                executeTeleport();
                sendLog('info', '=== 传送执行完毕 ===');
            }
        });
        sendLog('info', 'Hook Player.Update @ ' + ptr(base.add(RVA.Player_Update)));
    } catch(e) {
        sendLog('error', 'Hook Player.Update 失败: ' + e.message);
    }

    // ============================================================
    // executeTeleport — 带详细日志
    // ============================================================
    function executeTeleport() {
        teleportCount++;

        sendLog('info', '[1] 检查实例...');
        if (!gmInstance) { send(JSON.stringify({type:'error',msg:'GM未就绪'})); return; }
        if (!mmInstance) { send(JSON.stringify({type:'error',msg:'MM未就绪'})); return; }

        // --- allPlayers 数组 ---
        sendLog('info', '[2] gmInstance = ' + gmInstance);
        sendLog('info', '[3] 读 gmInstance+' + hex(O.GameManager_allPlayers) + '...');

        var allPlayersPtr;
        try {
            allPlayersPtr = gmInstance.add(O.GameManager_allPlayers).readPointer();
            sendLog('info', '[4] allPlayers 数组指针 = ' + allPlayersPtr);
        } catch(e) {
            sendLog('error', '[E4] 读 allPlayers 失败: ' + e.message);
            send(JSON.stringify({type:'error',msg:'读allPlayers失败'}));
            return;
        }

        if (!allPlayersPtr || allPlayersPtr.isNull()) {
            sendLog('error', '[E5] allPlayers 为 null');
            send(JSON.stringify({type:'error',msg:'allPlayers为null'}));
            return;
        }

        // 读数组长度
        var totalPlayers;
        try {
            totalPlayers = allPlayersPtr.add(0xC).readU32();
            sendLog('info', '[6] totalPlayers = ' + totalPlayers);
        } catch(e) {
            sendLog('error', '[E6] 读数组长度失败: ' + e.message);
            return;
        }

        // --- 出生点 ---
        sendLog('info', '[7] 读 mmInstance+' + hex(O.MapManager_SP_BL) + '...');
        var spBLArr;
        try {
            spBLArr = mmInstance.add(O.MapManager_SP_BL).readPointer();
            sendLog('info', '[8] SP_BL 指针 = ' + spBLArr);
        } catch(e) {
            sendLog('error', '[E8] 读SP_BL失败: ' + e.message);
            return;
        }

        sendLog('info', '[9] 解析 SP_BL[0]...');
        var spawnPoint = readFirstSpawnPoint(spBLArr);
        if (!spawnPoint) {
            sendLog('error', '[E9] 出生点为null');
            return;
        }
        sendLog('info', '[10] 出生点: (' +
            spawnPoint.x.toFixed(1) + ', ' +
            spawnPoint.y.toFixed(1) + ', ' +
            spawnPoint.z.toFixed(1) + ')');

        // --- 写 vecBuf ---
        sendLog('info', '[11] 写入 vecBuf...');
        vecBuf.writeFloat(spawnPoint.x);
        vecBuf.add(4).writeFloat(spawnPoint.y);
        vecBuf.add(8).writeFloat(spawnPoint.z);
        sendLog('info', '[12] vecBuf 验证: ' +
            vecBuf.readFloat() + ', ' +
            vecBuf.add(4).readFloat() + ', ' +
            vecBuf.add(8).readFloat());

        // --- 遍历 Player ---
        sendLog('info', '[13] 开始遍历 ' + totalPlayers + ' 个 Player');
        var botCount = 0;
        var deadCount = 0;
        var skipCount = 0;
        var doneCount = 0;

        for (var i = 0; i < totalPlayers; i++) {
            sendLog('info', '  [Loop ' + i + '] 读指针 @ ' +
                hex(allPlayersPtr.add(0x10 + i * 8)));

            var playerPtr;
            try {
                playerPtr = allPlayersPtr.add(0x10 + i * 8).readPointer();
            } catch(e) {
                sendLog('error', '  [Loop ' + i + '] 读指针崩溃: ' + e.message);
                break;
            }

            if (!playerPtr || playerPtr.isNull()) {
                sendLog('info', '  [Loop ' + i + '] 指针为 null，跳过');
                skipCount++;
                continue;
            }
            sendLog('info', '  [Loop ' + i + '] playerPtr = ' + playerPtr);

            // isMyPlayer
            sendLog('info', '  [Loop ' + i + '] 调用 isMyPlayer...');
            var isMine = false;
            try {
                isMine = isMyPlayerFn(playerPtr, ptr(0));
                sendLog('info', '  [Loop ' + i + '] isMyPlayer = ' + isMine);
            } catch(e) {
                sendLog('error', '  [Loop ' + i + '] isMyPlayer 崩溃: ' + e.message);
                break;
            }
            if (isMine) { skipCount++; continue; }

            // clientData
            sendLog('info', '  [Loop ' + i + '] 读 clientData @ ' +
                hex(playerPtr.add(O.Player_clientData)));
            var cdPtr;
            try {
                cdPtr = playerPtr.add(O.Player_clientData).readPointer();
                sendLog('info', '  [Loop ' + i + '] clientData = ' + cdPtr);
            } catch(e) {
                sendLog('error', '  [Loop ' + i + '] 读 clientData 崩溃: ' + e.message);
                break;
            }

            if (!cdPtr || cdPtr.isNull()) { skipCount++; continue; }

            sendLog('info', '  [Loop ' + i + '] 读 isBot @ ' +
                hex(cdPtr.add(O.ClientData_isBot)));
            var isBot;
            try {
                isBot = cdPtr.add(O.ClientData_isBot).readU8();
                sendLog('info', '  [Loop ' + i + '] isBot = ' + isBot);
            } catch(e) {
                sendLog('error', '  [Loop ' + i + '] 读 isBot 崩溃: ' + e.message);
                break;
            }
            if (!isBot) { skipCount++; continue; }

            // isDead
            sendLog('info', '  [Loop ' + i + '] 调用 isDead...');
            var isDead = false;
            try {
                isDead = getIsDeadFn(playerPtr, ptr(0));
                sendLog('info', '  [Loop ' + i + '] isDead = ' + isDead);
            } catch(e) {
                sendLog('error', '  [Loop ' + i + '] isDead 崩溃: ' + e.message);
                break;
            }
            if (isDead) { deadCount++; continue; }

            // *** ★ SetPos — 正确参数顺序 ***
            sendLog('info', '  [Loop ' + i + '] 调用 SetPos...');
            try {
                setPosFn(playerPtr, vecBuf, ptr(0));
                sendLog('info', '  [Loop ' + i + '] ★ SetPos√');
                botCount++;
                doneCount++;
                // 只传送 3 个测试，避免重复导致闪退难以分析
                if (doneCount >= 3) {
                    sendLog('info', '  [限制] 已传3个，测试完成');
                    break;
                }
            } catch(e) {
                sendLog('error', '  [Loop ' + i + '] ★ SetPos 崩溃: ' + e.message);
                break;
            }
        }

        var msg = '测试完成: 传了 ' + doneCount + ' 个 | Bot=' + botCount +
                  ' Dead=' + deadCount + ' Skip=' + skipCount;
        sendLog('info', msg);
    }

    function hex(ptr) {
        return '0x' + ptr.toString(16);
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
            sendLog('info', '收到传送指令，等待 Player.Update 触发...');
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
    sendLog('info', 'Bot出生点集合器 v4 已加载');
    sendLog('info', '全模式通用 | 修复 SetPos 参数顺序');
    sendLog('info', '===============================');
})();
