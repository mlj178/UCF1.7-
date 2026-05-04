// ============================================================
// Bot 出生点集合器 v2 — 多人生化模式
// 修复: v1 中 Entity.get_team() RVA(0x1E0070) 指向 mscorlib.dll 导致闪退
// 改动: 不再区分队伍，所有 Bot 统一传送到 SP_BL[0]
//       SetPos 调用约定修正为 IL2CPP 标准 3 参数
// 用法: 加载脚本 → 进入多人生化模式房间 → 调用 rpc.exports.teleportBots()
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
        sendLog('error', 'GameAssembly.dll 未找到，请确认游戏已启动');
        return;
    }
    var base = mod.base;

    // ============================================================
    // RVA 地址表 (dump.cs 验证，全部在 Assembly-CSharp Image 50 内)
    // ============================================================
    var RVA = {
        GameManager_AddPlayer:   0xAF9A90,  // VA=0x10AF9A90 ✓ Image 50
        MapManager_MapGunInit:   0xAEBB70,  // VA=0x10AEBB70 ✓ Image 50
        Player_Update:           0xB551D0,  // VA=0x10B551D0 ✓ Image 50
        Player_get_isMyPlayer:   0xB55FD0,  // VA=0x10B55FD0 ✓ Image 50
        Entity_get_isDead:       0xB400E0,  // VA=0x10B400E0 ✓ Image 50
        Player_SetPos:           0xB534C0,  // VA=0x10B534C0 ✓ Image 50
    };

    // ============================================================
    // 字段偏移 (14-AI清洗_终版 验证)
    // ============================================================
    var Player_clientData      = 0x94;  // Player → ClientData*
    var ClientData_isBot       = 0x14;  // ClientData.isBot (bool)
    var GameManager_allPlayers = 0x1C;  // Player[] allPlayers
    var MapManager_SP_BL       = 0x10;  // SpawnPoint[] SP_BL (所有Bot统一送到此处)

    // ============================================================
    // 状态变量
    // ============================================================
    var gmInstance = null;
    var mmInstance = null;
    var pendingTeleport = false;
    var teleportCount = 0;

    // ============================================================
    // NativeFunctions
    // 参照 knife_range_v22 / no_recoil_v4 的创建模式
    // ============================================================
    var isMyPlayerFn = new NativeFunction(base.add(RVA.Player_get_isMyPlayer), 'bool', ['pointer']);
    var getIsDeadFn  = new NativeFunction(base.add(RVA.Entity_get_isDead),   'bool', ['pointer']);

    // SetPos: IL2CPP x64 标准签名 = void Player__SetPos(Player_o* __this, MethodInfo* method, Vector3* pos)
    // Vector3(12字节 > 8) → x64 IL2CPP 中结构体按指针传递
    var setPosFn = new NativeFunction(base.add(RVA.Player_SetPos), 'void', ['pointer', 'pointer', 'pointer']);

    // 预分配 Vector3 缓冲区，避免在 Interceptor 回调内反复 alloc
    var vecBuf = Memory.alloc(12);

    // ============================================================
    // 辅助函数: 读取 SpawnPoint 数组的第一个出生点坐标
    // SpawnPoint: Vector3 position(0x0,12字节) + float rotaion(0xC)
    // IL2CPP数组: [0x00]=Klass* [0x08]=Monitor* [0x0C]=len [0x10]=第一个元素
    // ============================================================
    function readFirstSpawnPoint(spArrPtr) {
        if (!spArrPtr || spArrPtr.isNull()) return null;
        var len = spArrPtr.add(0xC).readU32();
        if (len === 0) return null;
        var elem = spArrPtr.add(0x10);
        return {
            x: elem.readFloat(),
            y: elem.add(4).readFloat(),
            z: elem.add(8).readFloat()
        };
    }

    // ============================================================
    // 步骤1: 捕获 GameManager 实例 (Hook AddPlayer)
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
        sendLog('info', 'AddPlayer hook 已安装 @ ' + ptr(base.add(RVA.GameManager_AddPlayer)));
    } catch(e) {
        sendLog('warn', 'AddPlayer hook 失败: ' + e.message);
    }

    // ============================================================
    // 步骤2: 捕获 MapManager 实例 (Hook MapGunInit)
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
        sendLog('info', 'MapGunInit hook 已安装 @ ' + ptr(base.add(RVA.MapManager_MapGunInit)));
    } catch(e) {
        sendLog('warn', 'MapGunInit hook 失败: ' + e.message);
    }

    // ============================================================
    // 步骤3: 使用 Player.Update 作为游戏线程入口执行传送
    // ============================================================
    try {
        Interceptor.attach(base.add(RVA.Player_Update), {
            onEnter: function(args) {
                if (!pendingTeleport) return;
                pendingTeleport = false;
                executeTeleport();
            }
        });
        sendLog('info', 'Player.Update hook 已安装 @ ' + ptr(base.add(RVA.Player_Update)));
    } catch(e) {
        sendLog('warn', 'Player.Update hook 失败: ' + e.message);
    }

    // ============================================================
    // 核心: 执行传送 (运行在 Player.Update onEnter 中，游戏主线程)
    // ============================================================
    function executeTeleport() {
        teleportCount++;

        if (!gmInstance) {
            send(JSON.stringify({type:'error', msg:'GameManager未就绪，请先进入游戏房间'}));
            sendLog('warn', 'GameManager 未就绪');
            return;
        }
        if (!mmInstance) {
            send(JSON.stringify({type:'error', msg:'MapManager未就绪，请等待地图加载'}));
            sendLog('warn', 'MapManager 未就绪');
            return;
        }

        // --- 读取 allPlayers 数组 ---
        var allPlayersPtr;
        try {
            allPlayersPtr = gmInstance.add(GameManager_allPlayers).readPointer();
        } catch(e) {
            send(JSON.stringify({type:'error', msg:'读取allPlayers失败: ' + e.message}));
            return;
        }
        if (!allPlayersPtr || allPlayersPtr.isNull()) {
            send(JSON.stringify({type:'error', msg:'allPlayers 为空'}));
            return;
        }
        var totalPlayers = allPlayersPtr.add(0xC).readU32();
        sendLog('info', '--- 传送 #' + teleportCount + ' 开始 (共' + totalPlayers + '个Player) ---');

        // --- 读取出生点 SP_BL[0] (所有Bot统一送到这个坐标) ---
        var spBLArr;
        try {
            spBLArr = mmInstance.add(MapManager_SP_BL).readPointer();
        } catch(e) {
            send(JSON.stringify({type:'error', msg:'读取SP_BL数组失败: ' + e.message}));
            return;
        }
        var spawnPoint = readFirstSpawnPoint(spBLArr);
        if (!spawnPoint) {
            send(JSON.stringify({type:'error', msg:'SP_BL 出生点为null，地图可能未加载完整'}));
            return;
        }

        sendLog('info', '出生点: (' +
            spawnPoint.x.toFixed(1) + ', ' +
            spawnPoint.y.toFixed(1) + ', ' +
            spawnPoint.z.toFixed(1) + ')');

        // --- 写入出生点坐标到预分配缓冲区 ---
        vecBuf.writeFloat(spawnPoint.x);
        vecBuf.add(4).writeFloat(spawnPoint.y);
        vecBuf.add(8).writeFloat(spawnPoint.z);

        // --- 遍历所有 Player，筛选 Bot 并传送 ---
        var botCount = 0;
        var deadCount = 0;
        var skipCount = 0;

        for (var i = 0; i < totalPlayers; i++) {
            try {
                var playerPtr = allPlayersPtr.add(0x10 + i * 8).readPointer();
                if (!playerPtr || playerPtr.isNull()) {
                    skipCount++;
                    continue;
                }

                if (isMyPlayerFn(playerPtr)) {
                    skipCount++;
                    continue;
                }

                var clientDataPtr = playerPtr.add(Player_clientData).readPointer();
                if (!clientDataPtr || clientDataPtr.isNull()) {
                    skipCount++;
                    continue;
                }
                var isBot = clientDataPtr.add(ClientData_isBot).readU8();
                if (!isBot) {
                    skipCount++;
                    continue;
                }

                if (getIsDeadFn(playerPtr)) {
                    deadCount++;
                    continue;
                }

                // SetPos(playerPtr, MethodInfo=null, Vector3* vecBuf)
                setPosFn(playerPtr, ptr(0), vecBuf);
                botCount++;
            } catch(e) {
                sendLog('warn', 'Player#' + i + ' 异常: ' + e.message);
            }
        }

        var msg = '传送 ' + botCount + ' 个Bot → SP_BL[0]';
        if (deadCount > 0) msg += ' | ' + deadCount + ' 已死亡跳过';
        if (skipCount > 0) msg += ' | ' + skipCount + ' 跳过';
        sendLog('info', msg);
        send(JSON.stringify({
            type: 'done',
            count: botCount,
            dead: deadCount,
            total: totalPlayers,
            msg: msg
        }));
    }

    // ============================================================
    // RPC 导出: 供 Python 按钮调用
    // ============================================================
    rpc.exports = {
        teleportBots: function() {
            if (!gmInstance) {
                send(JSON.stringify({type:'error', msg:'请先进入多人生化模式房间'}));
                sendLog('warn', 'teleportBots: GameManager 未就绪');
                return;
            }
            if (!mmInstance) {
                send(JSON.stringify({type:'error', msg:'请等待地图加载完成'}));
                sendLog('warn', 'teleportBots: MapManager 未就绪');
                return;
            }
            pendingTeleport = true;
            sendLog('info', '已收到传送指令，等待下一帧执行...');
        },

        getStatus: function() {
            return JSON.stringify({
                gmReady: gmInstance !== null,
                mmReady: mmInstance !== null,
                teleportCount: teleportCount
            });
        }
    };

    sendLog('info', '========================================');
    sendLog('info', 'Bot出生点集合器 v2 已加载');
    sendLog('info', '等待进入多人生化模式房间...');
    sendLog('info', '就绪后调用 rpc.exports.teleportBots() 触发传送');
    sendLog('info', '========================================');
})();
