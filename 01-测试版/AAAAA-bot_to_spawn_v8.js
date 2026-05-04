// ============================================================
// Bot 出生点集合器 v8 — GameAssembly + SP_Netural
// 修复: Transform.set_position 在 IL2CPP 中属于 GameAssembly.dll
//       所有 dump.cs RVA 都相对 GameAssembly，不是 UnityPlayer
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
    var base = gMod.base;
    sendLog('info', 'GameAssembly base = ' + base);

    var RVA = {
        GM_AddPlayer:         0xAF9A90,
        MM_NewGameRound:      0xAEBCB0,
        Player_Update:        0xB551D0,
        Player_isMyPlayer:    0xB55FD0,
        Entity_isDead:        0xB400E0,
        Transform_setPos:     0x3F4840,  // Image 7 → 也在 GameAssembly 内
    };

    var O = {
        Player_characterContainer: 0x58,
        Player_clientData:         0x94,
        ClientData_isBot:          0x14,
        GM_allPlayers:             0x1C,
        MM_SP_Netural:             0x18,  // SP_Netural
    };

    var gmInstance = null;
    var mmInstance = null;
    var pendingTeleport = false;
    var teleportCount = 0;

    var isMyPlayerFn    = new NativeFunction(base.add(RVA.Player_isMyPlayer), 'bool', ['pointer', 'pointer']);
    var getIsDeadFn     = new NativeFunction(base.add(RVA.Entity_isDead),     'bool', ['pointer', 'pointer']);
    var setTransformPos = new NativeFunction(base.add(RVA.Transform_setPos),  'void', ['pointer', 'pointer', 'pointer']);

    var vecBuf     = Memory.alloc(16);
    var cachedSpawn = null;

    function readSpawn(spArrPtr) {
        if (!spArrPtr || spArrPtr.isNull()) return null;
        var len = spArrPtr.add(0xC).readU32();
        if (len === 0) return null;
        var e = spArrPtr.add(0x10);
        return { x: e.readFloat(), y: e.add(4).readFloat(), z: e.add(8).readFloat() };
    }

    try {
        Interceptor.attach(base.add(RVA.GM_AddPlayer), {
            onEnter: function(args) {
                if (!gmInstance) { gmInstance = args[0]; send(JSON.stringify({type:'gm_ready'})); sendLog('info', '✓ GM @ ' + gmInstance); }
            }
        });
    } catch(e) { sendLog('error', 'Hook AddPlayer: ' + e.message); }

    try {
        Interceptor.attach(base.add(RVA.MM_NewGameRound), {
            onEnter: function(args) {
                if (!mmInstance) { mmInstance = args[0]; send(JSON.stringify({type:'mm_ready'})); sendLog('info', '✓ MM @ ' + mmInstance); }
            }
        });
    } catch(e) { sendLog('error', 'Hook NewGameRound: ' + e.message); }

    try {
        Interceptor.attach(base.add(RVA.Player_Update), {
            onEnter: function(args) {
                if (!pendingTeleport) return;
                pendingTeleport = false;
                doTeleport();
            }
        });
    } catch(e) { sendLog('error', 'Hook Player.Update: ' + e.message); }

    function doTeleport() {
        teleportCount++;
        sendLog('info', '=== 传送 #' + teleportCount + ' ===');

        if (!gmInstance) { send(JSON.stringify({type:'error',msg:'GM未就绪'})); return; }

        if (!cachedSpawn) {
            if (mmInstance) {
                try { cachedSpawn = readSpawn(mmInstance.add(O.MM_SP_Netural).readPointer()); } catch(e) {}
            }
            if (!cachedSpawn) cachedSpawn = { x:0, y:0, z:0 };
        }
        sendLog('info', 'SP_Netural: (' + cachedSpawn.x.toFixed(1) + ', ' + cachedSpawn.y.toFixed(1) + ', ' + cachedSpawn.z.toFixed(1) + ')');

        vecBuf.writeFloat(cachedSpawn.x);
        vecBuf.add(4).writeFloat(cachedSpawn.y);
        vecBuf.add(8).writeFloat(cachedSpawn.z);

        var allArr = gmInstance.add(O.GM_allPlayers).readPointer();
        if (!allArr || allArr.isNull()) { send(JSON.stringify({type:'error',msg:'allPlayers null'})); return; }
        var total = allArr.add(0xC).readU32();

        var bot = 0, dead = 0, skip = 0;
        for (var i = 0; i < total; i++) {
            try {
                var pp = allArr.add(0x10 + i * 8).readPointer();
                if (!pp || pp.isNull()) { skip++; continue; }
                if (isMyPlayerFn(pp, ptr(0))) { skip++; continue; }

                var cd = pp.add(O.Player_clientData).readPointer();
                if (!cd || cd.isNull()) { skip++; continue; }
                if (!cd.add(O.ClientData_isBot).readU8()) { skip++; continue; }
                if (getIsDeadFn(pp, ptr(0))) { dead++; continue; }

                // Player.characterContainer @ 0x58 → Transform*
                var tr = pp.add(O.Player_characterContainer).readPointer();
                if (!tr || tr.isNull()) { skip++; continue; }

                setTransformPos(tr, vecBuf, ptr(0));
                bot++;
            } catch(e) {
                sendLog('warn', '#' + i + ' 异常: ' + e.message);
                break;
            }
        }

        var msg = '传送 ' + bot + ' 个Bot';
        if (dead>0) msg += ' | ' + dead + ' 已死亡';
        if (skip>0) msg += ' | ' + skip + ' 跳过';
        sendLog('info', msg);
        send(JSON.stringify({type:'done', count:bot, msg:msg}));
    }

    rpc.exports = {
        teleportBots: function() {
            if (!gmInstance) { send(JSON.stringify({type:'error',msg:'GM未就绪'})); return; }
            pendingTeleport = true;
            sendLog('info', '收到传送指令');
        }
    };

    sendLog('info', '===============================');
    sendLog('info', 'Bot出生点集合器 v8 已加载');
    sendLog('info', 'SP_Netural | Transform(GameAssembly)');
    sendLog('info', '===============================');
})();
