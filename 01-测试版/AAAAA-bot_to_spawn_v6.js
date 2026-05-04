// ============================================================
// Bot 出生点集合器 v6 — 直接写 Transform.position 物理坐标
// 修复: Player.SetPos 只改逻辑spawn位置，不动物理坐标
//       改用 Transform.set_position (UnityEngine.CoreModule.dll)
//       Player.characterContainer 字段偏移 0x58 直接拿 Transform*
// ============================================================

(function() {
    'use strict';

    function sendLog(level, msg) {
        var prefix = '[BotToSpawn] ';
        if (level === 'error') console.error(prefix + msg);
        else if (level === 'warn') console.warn(prefix + msg);
        else console.log(prefix + msg);
    }

    var gMod = Process.findModuleByName('GameAssembly.dll');
    if (!gMod) { sendLog('error', 'GameAssembly.dll 未找到'); return; }
    var gBase = gMod.base;
    sendLog('info', 'GameAssembly base = ' + gBase);

    var uMod = Process.findModuleByName('UnityEngine.CoreModule.dll');
    if (!uMod) { sendLog('error', 'UnityEngine.CoreModule.dll 未找到'); return; }
    var uBase = uMod.base;
    sendLog('info', 'CoreModule base = ' + uBase);

    // ============================================================
    // RVA
    // ============================================================
    var RVA = {
        // GameAssembly.dll (Assembly-CSharp)
        GM_AddPlayer:     0xAF9A90,
        MM_NewGameRound:  0xAEBCB0,
        Player_Update:    0xB551D0,
        Player_isMyPlayer: 0xB55FD0,
        Entity_isDead:    0xB400E0,
    };

    var CORE_RVA = {
        // UnityEngine.CoreModule.dll
        Transform_set_position: 0x3F4840,
    };

    var O = {
        Player_characterContainer: 0x58,  // dump.cs: Transform characterContainer @ offset 0x58
        Player_clientData:         0x94,
        ClientData_isBot:          0x14,
        GM_allPlayers:             0x1C,
        MM_SP_BL:                  0x10,
    };

    var gmInstance = null;
    var mmInstance = null;
    var pendingTeleport = false;
    var teleportCount = 0;

    // ============================================================
    // NativeFunctions
    // ============================================================
    var isMyPlayerFn = new NativeFunction(gBase.add(RVA.Player_isMyPlayer), 'bool', ['pointer', 'pointer']);
    var getIsDeadFn  = new NativeFunction(gBase.add(RVA.Entity_isDead),     'bool', ['pointer', 'pointer']);

    // Transform.set_position(Vector3) — CoreModule
    var setTransformPos = new NativeFunction(uBase.add(CORE_RVA.Transform_set_position), 'void', ['pointer', 'pointer', 'pointer']);

    var vecBuf = Memory.alloc(16);

    // ============================================================
    // 缓存第一份有效出生点，避免 SP_BL 数组过期
    // ============================================================
    var cachedSpawn = null;

    function readFirstSpawnPoint(spArrPtr) {
        if (!spArrPtr || spArrPtr.isNull()) return null;
        var len = spArrPtr.add(0xC).readU32();
        if (len === 0) return null;
        var elem = spArrPtr.add(0x10);
        return { x: elem.readFloat(), y: elem.add(4).readFloat(), z: elem.add(8).readFloat() };
    }

    // ============================================================
    // Hook 1: GameManager.AddPlayer
    // ============================================================
    try {
        Interceptor.attach(gBase.add(RVA.GM_AddPlayer), {
            onEnter: function(args) {
                if (!gmInstance) {
                    gmInstance = args[0];
                    send(JSON.stringify({type:'gm_ready'}));
                    sendLog('info', '✓ GameManager @ ' + gmInstance);
                }
            }
        });
    } catch(e) { sendLog('error', 'Hook AddPlayer: ' + e.message); }

    // ============================================================
    // Hook 2: MapManager.NewGameRoundStart
    // ============================================================
    try {
        Interceptor.attach(gBase.add(RVA.MM_NewGameRound), {
            onEnter: function(args) {
                if (!mmInstance) {
                    mmInstance = args[0];
                    send(JSON.stringify({type:'mm_ready'}));
                    sendLog('info', '✓ MapManager @ ' + mmInstance);
                }
            }
        });
    } catch(e) { sendLog('error', 'Hook NewGameRound: ' + e.message); }

    // ============================================================
    // Hook 3: Player.Update — 主线程入口
    // ============================================================
    try {
        Interceptor.attach(gBase.add(RVA.Player_Update), {
            onEnter: function(args) {
                if (!pendingTeleport) return;
                pendingTeleport = false;
                executeTeleport();
            }
        });
    } catch(e) { sendLog('error', 'Hook Player.Update: ' + e.message); }

    // ============================================================
    // executeTeleport
    // ============================================================
    function executeTeleport() {
        teleportCount++;

        if (!gmInstance) {
            send(JSON.stringify({type:'error', msg:'GameManager 未就绪'}));
            return;
        }

        // --- 读取出生点 (首次有效 → 缓存，之后不再重读) ---
        if (!cachedSpawn) {
            if (mmInstance) {
                try {
                    var spArr = mmInstance.add(O.MM_SP_BL).readPointer();
                    cachedSpawn = readFirstSpawnPoint(spArr);
                } catch(e) {}
            }
            if (!cachedSpawn) {
                cachedSpawn = { x: 0, y: 0, z: 0 };
            }
        }
        sendLog('info', '出生点(缓存): (' +
            cachedSpawn.x.toFixed(1) + ', ' +
            cachedSpawn.y.toFixed(1) + ', ' +
            cachedSpawn.z.toFixed(1) + ')');

        vecBuf.writeFloat(cachedSpawn.x);
        vecBuf.add(4).writeFloat(cachedSpawn.y);
        vecBuf.add(8).writeFloat(cachedSpawn.z);

        // --- 遍历传送 ---
        var allArr = gmInstance.add(O.GM_allPlayers).readPointer();
        if (!allArr || allArr.isNull()) {
            send(JSON.stringify({type:'error', msg:'allPlayers 为 null'}));
            return;
        }
        var total = allArr.add(0xC).readU32();
        sendLog('info', '共 ' + total + ' 个Player');

        var botCount = 0, deadCount = 0, skipCount = 0;

        for (var i = 0; i < total; i++) {
            try {
                var pp = allArr.add(0x10 + i * 8).readPointer();
                if (!pp || pp.isNull()) { skipCount++; continue; }
                if (isMyPlayerFn(pp, ptr(0))) { skipCount++; continue; }

                var cd = pp.add(O.Player_clientData).readPointer();
                if (!cd || cd.isNull()) { skipCount++; continue; }
                if (!cd.add(O.ClientData_isBot).readU8()) { skipCount++; continue; }
                if (getIsDeadFn(pp, ptr(0))) { deadCount++; continue; }

                // ★ 直接读 characterContainer (Transform*) @ offset 0x58
                var tr = pp.add(O.Player_characterContainer).readPointer();
                if (!tr || tr.isNull()) {
                    sendLog('warn', 'Player#' + i + ' Transform 为 null');
                    skipCount++; continue;
                }

                // ★ 调用 Transform.set_position(tr, &pos, method)
                setTransformPos(tr, vecBuf, ptr(0));
                botCount++;
            } catch(e) {
                sendLog('warn', 'Player#' + i + ' 异常: ' + e.message);
                break;
            }
        }

        var msg = '传送 ' + botCount + ' 个Bot (Transform)';
        if (deadCount > 0) msg += ' | ' + deadCount + ' 已死亡';
        if (skipCount > 0) msg += ' | ' + skipCount + ' 跳过';
        sendLog('info', msg);
        send(JSON.stringify({type:'done', count:botCount, msg:msg}));
    }

    rpc.exports = {
        teleportBots: function() {
            if (!gmInstance) {
                send(JSON.stringify({type:'error', msg:'GameManager 未就绪'}));
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
    sendLog('info', 'Bot出生点集合器 v6 已加载');
    sendLog('info', 'Transform.set_position | 物理坐标');
    sendLog('info', '===============================');
})();
