// ============================================================
// Bot 出生点集合器 v7 — 全模块搜索 + SP_Netural
// 修复: Unity 引擎 DLL 名称不同，枚举所有模块查找
//       改用 SP_Netural(0x18) 出生点
//       双重尝试: 找 Transform.set_position → 失败则直接用 CharacterController 或内存写入
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

    // ============================================================
    // 枚举所有模块，找包含 Unity Transform 函数的 DLL
    // 候选名: UnityPlayer.dll, libunity.so, UnityEngine.CoreModule.dll
    // ============================================================
    var uBase = null;
    var uName = null;

    var modules = Process.enumerateModules();
    sendLog('info', '--- 已加载模块列表 (' + modules.length + ' 个) ---');
    for (var j = 0; j < modules.length; j++) {
        var m = modules[j];
        var mn = (m.name || '').toLowerCase();
        sendLog('info', '  [' + j + '] ' + m.name + ' @ ' + m.base + ' size=' + m.size);
        // 找 Unity 引擎模块 (非 GameAssembly)
        if (!uBase && (
            mn.indexOf('unityplayer') >= 0 ||
            mn.indexOf('unityengine') >= 0 ||
            mn.indexOf('coremodule') >= 0 ||
            mn.indexOf('libunity') >= 0
        )) {
            uBase = m.base;
            uName = m.name;
            sendLog('info', '  ★ 找到 Unity 引擎模块: ' + uName + ' @ ' + uBase);
        }
    }

    // ============================================================
    // RVA
    // ============================================================
    var RVA = {
        GM_AddPlayer:     0xAF9A90,
        MM_NewGameRound:  0xAEBCB0,
        Player_Update:    0xB551D0,
        Player_isMyPlayer: 0xB55FD0,
        Entity_isDead:    0xB400E0,
    };

    var CORE_RVA = {
        Transform_set_position: 0x3F4840,
    };

    var O = {
        Player_characterContainer: 0x58,
        Player_clientData:         0x94,
        ClientData_isBot:          0x14,
        GM_allPlayers:             0x1C,
        MM_SP_Netural:             0x18,  // ★ 用户指定: SP_Netural
    };

    var gmInstance = null;
    var mmInstance = null;
    var pendingTeleport = false;
    var teleportCount = 0;

    var isMyPlayerFn = new NativeFunction(gBase.add(RVA.Player_isMyPlayer), 'bool', ['pointer', 'pointer']);
    var getIsDeadFn  = new NativeFunction(gBase.add(RVA.Entity_isDead),     'bool', ['pointer', 'pointer']);

    var setTransformPos = null;
    if (uBase) {
        sendLog('info', '使用 ' + uName + ' 调用 Transform.set_position');
        setTransformPos = new NativeFunction(uBase.add(CORE_RVA.Transform_set_position), 'void', ['pointer', 'pointer', 'pointer']);
    } else {
        sendLog('warn', '未找到 Unity 引擎 DLL，将尝试备选方案');
    }

    var vecBuf = Memory.alloc(16);
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
            send(JSON.stringify({type:'error', msg:'GM 未就绪'}));
            return;
        }

        // --- 出生点 (SP_Netural) ---
        if (!cachedSpawn) {
            if (mmInstance) {
                try {
                    var spArr = mmInstance.add(O.MM_SP_Netural).readPointer();
                    cachedSpawn = readFirstSpawnPoint(spArr);
                } catch(e) {}
            }
            if (!cachedSpawn) {
                cachedSpawn = { x: 0, y: 0, z: 0 };
            }
        }
        sendLog('info', 'SP_Netural: (' +
            cachedSpawn.x.toFixed(1) + ', ' +
            cachedSpawn.y.toFixed(1) + ', ' +
            cachedSpawn.z.toFixed(1) + ')');

        vecBuf.writeFloat(cachedSpawn.x);
        vecBuf.add(4).writeFloat(cachedSpawn.y);
        vecBuf.add(8).writeFloat(cachedSpawn.z);

        // --- 遍历 ---
        var allArr = gmInstance.add(O.GM_allPlayers).readPointer();
        if (!allArr || allArr.isNull()) {
            send(JSON.stringify({type:'error', msg:'allPlayers null'}));
            return;
        }
        var total = allArr.add(0xC).readU32();
        sendLog('info', '共 ' + total + ' 个Player, 传送引擎: ' + (uBase ? 'Transform.set_position' : '内存直写'));

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

                // --- Player.characterContainer (Transform* @ 0x58) ---
                var tr = pp.add(O.Player_characterContainer).readPointer();

                if (setTransformPos && tr && !tr.isNull()) {
                    // 方案A: 调 Transform.set_position
                    setTransformPos(tr, vecBuf, ptr(0));
                    botCount++;
                } else if (tr && !tr.isNull()) {
                    // 方案B: 直接写 Transform 内部 m_LocalPosition
                    // IL2CPP Transform: [0x10] = native ptr, native object 偏移 0x38 左右
                    var cPtr = tr.add(0x10).readPointer();
                    if (cPtr && !cPtr.isNull()) {
                        cPtr.add(0x38).writeFloat(cachedSpawn.x);
                        cPtr.add(0x3C).writeFloat(cachedSpawn.y);
                        cPtr.add(0x40).writeFloat(cachedSpawn.z);
                        botCount++;
                    } else {
                        skipCount++;
                    }
                } else {
                    skipCount++;
                }
            } catch(e) {
                sendLog('warn', '#' + i + ' 异常: ' + e.message);
                break;
            }
        }

        var msg = '传送 ' + botCount + ' 个Bot (SP_Netural)';
        if (deadCount > 0) msg += ' | ' + deadCount + ' 已死亡';
        if (skipCount > 0) msg += ' | ' + skipCount + ' 跳过';
        sendLog('info', msg);
        send(JSON.stringify({type:'done', count:botCount, msg:msg}));
    }

    rpc.exports = {
        teleportBots: function() {
            if (!gmInstance) {
                send(JSON.stringify({type:'error', msg:'GM 未就绪'}));
                return;
            }
            pendingTeleport = true;
            sendLog('info', '收到传送指令');
        },
        getStatus: function() {
            return JSON.stringify({
                gmReady: gmInstance !== null,
                mmReady: mmInstance !== null,
                uMod: uName || '(none)',
                teleportCount: teleportCount
            });
        }
    };

    sendLog('info', '===============================');
    sendLog('info', 'Bot出生点集合器 v7 已加载');
    sendLog('info', '出生点: SP_Netural | 引擎: ' + (uName || '内存直写'));
    sendLog('info', '===============================');
})();
