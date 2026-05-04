// ============================================================
// Bot 出生点集合器 v1 — 多人生化模式
// 功能: 点击按钮一次性将所有Bot(人机)传送到各自队伍的出生点
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
    // RVA 地址表 (dump.cs 验证)
    // ============================================================
    var RVA = {
        GameManager_AddPlayer:  0xAF9A90,  // 捕获 GameManager 实例
        MapManager_MapGunInit:  0xAEBB70,  // 捕获 MapManager 实例
        Player_Update:          0xB551D0,  // 游戏线程入口 (每帧调用)
        Player_get_isMyPlayer:  0xB55FD0,  // 判断是否本地玩家
        Entity_get_isDead:      0xB400E0,  // 判断是否死亡
        Entity_get_team:        0x1E0070,  // 获取队伍 (BL=0, GR=1)
        Player_SetPos:          0xB534C0,  // 设置位置
    };

    // ============================================================
    // 字段偏移 (14-AI清洗_终版 验证)
    // ============================================================
    var Player_clientData     = 0x94;  // Player → ClientData*
    var ClientData_isBot      = 0x14;  // ClientData.isBot (bool)
    var GameManager_allPlayers = 0x1C;  // Player[] allPlayers
    var MapManager_SP_BL      = 0x10;  // SpawnPoint[] SP_BL
    var MapManager_SP_GR      = 0x14;  // SpawnPoint[] SP_GR

    // ============================================================
    // 状态变量
    // ============================================================
    var gmInstance = null;     // GameManager 实例指针
    var mmInstance = null;     // MapManager 实例指针
    var pendingTeleport = false;
    var teleportCount = 0;

    // ============================================================
    // NativeFunctions (只需创建一次)
    // ============================================================
    var isMyPlayerFn = new NativeFunction(base.add(RVA.Player_get_isMyPlayer), 'bool', ['pointer']);
    var getIsDeadFn  = new NativeFunction(base.add(RVA.Entity_get_isDead), 'bool', ['pointer']);
    var getTeamFn    = new NativeFunction(base.add(RVA.Entity_get_team), 'int', ['pointer']);
    // SetPos: Vector3(12字节) 在 x64 IL2CPP 中通过指针传递
    var setPosFn     = new NativeFunction(base.add(RVA.Player_SetPos), 'void', ['pointer', 'pointer']);

    // ============================================================
    // 辅助函数: 读取 IL2CPP 数组元素
    // ============================================================
    function readArrayElement(arrPtr, index, elemSize) {
        return arrPtr.add(0x10 + index * elemSize).readPointer();
    }

    // ============================================================
    // 辅助函数: 读取 SpawnPoint 数组的第一个出生点坐标
    // SpawnPoint: Vector3 position(0x0,12字节) + float rotaion(0xC)
    // IL2CPP数组: [0x00]=Klass* [0x08]=Monitor* [0x0C]=len [0x10]=elem0
    // ============================================================
    function readFirstSpawnPoint(spArrPtr) {
        if (!spArrPtr || spArrPtr.isNull()) return null;
        var len = spArrPtr.add(0xC).readU32();
        if (len === 0) return null;
        var elem = spArrPtr.add(0x10); // 第一个 SpawnPoint
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
    //        (确保所有操作在主线程执行，避免跨线程崩溃)
    // ============================================================
    try {
        Interceptor.attach(base.add(RVA.Player_Update), {
            onEnter: function(args) {
                if (!pendingTeleport) return;
                pendingTeleport = false; // 防止重复执行
                executeTeleport();
            }
        });
        sendLog('info', 'Player.Update hook 已安装 @ ' + ptr(base.add(RVA.Player_Update)));
    } catch(e) {
        sendLog('warn', 'Player.Update hook 失败: ' + e.message);
    }

    // ============================================================
    // 核心: 执行传送 (运行在游戏主线程中)
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

        // --- 读取两队出生点 (MapManager.SP_BL[0] / SP_GR[0]) ---
        var spBLArr, spGRArr;
        try {
            spBLArr = mmInstance.add(MapManager_SP_BL).readPointer();
            spGRArr = mmInstance.add(MapManager_SP_GR).readPointer();
        } catch(e) {
            send(JSON.stringify({type:'error', msg:'读取出生点数组失败'}));
            return;
        }

        var spawnBL = readFirstSpawnPoint(spBLArr);
        var spawnGR = readFirstSpawnPoint(spGRArr);

        if (!spawnBL && !spawnGR) {
            send(JSON.stringify({type:'error', msg:'出生点为null，地图可能未加载完整'}));
            return;
        }

        // 如果某方出生点为空，用另一方代替
        if (!spawnBL) spawnBL = spawnGR;
        if (!spawnGR) spawnGR = spawnBL;

        sendLog('info', 'BL出生点: (' + spawnBL.x.toFixed(1) + ', ' + spawnBL.y.toFixed(1) + ', ' + spawnBL.z.toFixed(1) + ')');
        sendLog('info', 'GR出生点: (' + spawnGR.x.toFixed(1) + ', ' + spawnGR.y.toFixed(1) + ', ' + spawnGR.z.toFixed(1) + ')');

        // --- 遍历所有 Player，筛选 Bot 并传送 ---
        var botCount = 0;
        var deadCount = 0;
        var skipCount = 0;
        var vecBuf = Memory.alloc(12); // 复用 Vector3 缓冲区

        for (var i = 0; i < totalPlayers; i++) {
            try {
                var playerPtr = allPlayersPtr.add(0x10 + i * 8).readPointer();
                if (!playerPtr || playerPtr.isNull()) {
                    skipCount++;
                    continue;
                }

                // 跳过自己（本地玩家）
                if (isMyPlayerFn(playerPtr)) {
                    skipCount++;
                    continue;
                }

                // 检查是否人机
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

                // 跳过已死亡的 Bot
                if (getIsDeadFn(playerPtr)) {
                    deadCount++;
                    continue;
                }

                // 获取队伍 → 选择对应出生点
                var team = getTeamFn(playerPtr);
                var sp = (team === 1) ? spawnGR : spawnBL;

                // 写入 Vector3 到缓冲区并调用 SetPos
                vecBuf.writeFloat(sp.x);
                vecBuf.add(4).writeFloat(sp.y);
                vecBuf.add(8).writeFloat(sp.z);
                setPosFn(playerPtr, vecBuf);

                botCount++;
            } catch(e) {
                sendLog('warn', 'Player#' + i + ' 处理异常: ' + e.message);
            }
        }

        // --- 输出结果 ---
        var msg = '传送完成: ' + botCount + ' 个Bot → 出生点';
        if (deadCount > 0) msg += ' | ' + deadCount + ' 个已死亡(跳过)';
        if (skipCount > 0) msg += ' | ' + skipCount + ' 个跳过';
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
                sendLog('warn', 'teleportBots 被调用但 GameManager 未就绪');
                return;
            }
            if (!mmInstance) {
                send(JSON.stringify({type:'error', msg:'请等待地图加载完成'}));
                sendLog('warn', 'teleportBots 被调用但 MapManager 未就绪');
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
    sendLog('info', 'Bot出生点集合器 v1 已加载');
    sendLog('info', '等待进入多人生化模式房间...');
    sendLog('info', '就绪后调用 rpc.exports.teleportBots() 触发传送');
    sendLog('info', '========================================');
})();
