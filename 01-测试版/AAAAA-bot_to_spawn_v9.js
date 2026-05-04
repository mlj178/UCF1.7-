// ============================================================
// Bot 出生点集合器 v9 — Nano4+Terminator 专版
// 修复: SP_BL[0] 出生点 + get_transform 主Transform + set_position_Injected
//       characterContainer(子节点) → get_transform(本体的Transform)
//       set_position → set_position_Injected(0x3F4810) 直通native
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
    if (!mod) { sendLog('error', 'GameAssembly.dll 未找到'); return; }
    var base = mod.base;
    sendLog('info', 'base=' + base);

    var RVA = {
        GM_AddPlayer:         0xAF9A90,
        MM_MapGunInit:        0xAEBB70,  // ★ Nano4T 专有
        Player_Update:        0xB551D0,
        Player_isMyPlayer:    0xB55FD0,
        Entity_isDead:        0xB400E0,
        Component_getTrans:   0x32CF40,  // get_transform()
        Transform_setPosInj:  0x3F4810,  // ★ set_position_Injected
        Player_SetPos:        0xB534C0,  // 备选
    };

    var O = {
        Player_clientData:    0x94,
        ClientData_isBot:     0x14,
        GM_allPlayers:        0x1C,
        MM_SP_BL:             0x10,      // ★ SP_BL[0]
    };

    var gmInstance = null;
    var mmInstance = null;
    var pendingTeleport = false;
    var teleportCount = 0;

    var isMyPlayerFn  = new NativeFunction(base.add(RVA.Player_isMyPlayer), 'bool',    ['pointer', 'pointer']);
    var getIsDeadFn   = new NativeFunction(base.add(RVA.Entity_isDead),     'bool',    ['pointer', 'pointer']);
    var getTransform  = new NativeFunction(base.add(RVA.Component_getTrans),'pointer', ['pointer', 'pointer']);
    var setPosInj     = new NativeFunction(base.add(RVA.Transform_setPosInj),'void',   ['pointer', 'pointer', 'pointer']);
    var playerSetPos  = new NativeFunction(base.add(RVA.Player_SetPos),    'void',    ['pointer', 'pointer', 'pointer']);

    var vecBuf = Memory.alloc(16);
    var cachedSpawn = null;

    function readSpawn(arrPtr) {
        if (!arrPtr || arrPtr.isNull()) return null;
        if (arrPtr.add(0xC).readU32() === 0) return null;
        var e = arrPtr.add(0x10);
        return { x:e.readFloat(), y:e.add(4).readFloat(), z:e.add(8).readFloat() };
    }

    // Hook 1: GameManager.AddPlayer
    try {
        Interceptor.attach(base.add(RVA.GM_AddPlayer), {
            onEnter: function(args) {
                if (!gmInstance) { gmInstance=args[0]; send(JSON.stringify({type:'gm_ready'})); }
            }
        });
    } catch(e) { sendLog('error','AddPlayer: '+e.message); }

    // Hook 2: MapManager.MapGunInit (Nano4T 专有)
    try {
        Interceptor.attach(base.add(RVA.MM_MapGunInit), {
            onEnter: function(args) {
                if (!mmInstance) {
                    mmInstance=args[0];
                    // 趁早缓存出生点
                    try {
                        var sp = mmInstance.add(O.MM_SP_BL).readPointer();
                        cachedSpawn = readSpawn(sp);
                        sendLog('info','SP_BL缓存: ('+cachedSpawn.x.toFixed(1)+','+cachedSpawn.y.toFixed(1)+','+cachedSpawn.z.toFixed(1)+')');
                    } catch(e2) {}
                    send(JSON.stringify({type:'mm_ready'}));
                }
            }
        });
    } catch(e) { sendLog('error','MapGunInit: '+e.message); }

    // Hook 3: Player.Update
    try {
        Interceptor.attach(base.add(RVA.Player_Update), {
            onEnter: function(args) {
                if (!pendingTeleport) return;
                pendingTeleport = false;
                doTeleport();
            }
        });
    } catch(e) { sendLog('error','Player.Update: '+e.message); }

    function doTeleport() {
        teleportCount++;
        sendLog('info', '=== #' + teleportCount + ' ===');

        if (!gmInstance) { return; }

        if (!cachedSpawn) cachedSpawn = { x:0,y:0,z:0 };
        sendLog('info','出生点: ('+cachedSpawn.x.toFixed(1)+','+cachedSpawn.y.toFixed(1)+','+cachedSpawn.z.toFixed(1)+')');

        vecBuf.writeFloat(cachedSpawn.x);
        vecBuf.add(4).writeFloat(cachedSpawn.y);
        vecBuf.add(8).writeFloat(cachedSpawn.z);

        var allArr = gmInstance.add(O.GM_allPlayers).readPointer();
        if (!allArr || allArr.isNull()) return;
        var total = allArr.add(0xC).readU32();

        var bot=0, dead=0, skip=0, trans=0, setpos=0;

        for (var i = 0; i < total; i++) {
            try {
                var pp = allArr.add(0x10 + i*8).readPointer();
                if (!pp || pp.isNull()) { skip++; continue; }
                if (isMyPlayerFn(pp, ptr(0))) { skip++; continue; }

                var cd = pp.add(O.Player_clientData).readPointer();
                if (!cd || cd.isNull()) { skip++; continue; }
                if (!cd.add(O.ClientData_isBot).readU8()) { skip++; continue; }
                if (getIsDeadFn(pp, ptr(0))) { dead++; continue; }

                // --- 方案A: 本体的 Transform ---
                var moved = false;
                try {
                    var tr = getTransform(pp, ptr(0));
                    if (tr && !tr.isNull()) {
                        setPosInj(tr, vecBuf, ptr(0));
                        trans++; moved = true;
                    }
                } catch(e) {}

                // --- 方案B: characterContainer (子节点) ---
                if (!moved) {
                    try {
                        var cc = pp.add(0x58).readPointer();
                        if (cc && !cc.isNull()) {
                            setPosInj(cc, vecBuf, ptr(0));
                            trans++; moved = true;
                        }
                    } catch(e) {}
                }

                // --- 方案C: Player.SetPos 兜底 ---
                if (!moved) {
                    try {
                        playerSetPos(pp, vecBuf, ptr(0));
                        setpos++; moved = true;
                    } catch(e) {}
                }

                if (moved) bot++;
                else skip++;
            } catch(e) {
                sendLog('warn','#'+i+' 异常:'+e.message);
                break;
            }
        }

        var msg = '传送 '+bot+' 个Bot (Trans='+trans+' SetPos='+setpos+')';
        if (dead>0) msg += ' | '+dead+' 死亡';
        if (skip>0) msg += ' | '+skip+' 跳过';
        sendLog('info', msg);
        send(JSON.stringify({type:'done',count:bot,msg:msg}));
    }

    rpc.exports = {
        teleportBots: function() {
            if (!gmInstance) { send(JSON.stringify({type:'error',msg:'GM未就绪'})); return; }
            pendingTeleport = true;
            sendLog('info','收到指令');
        }
    };

    sendLog('info','===============================');
    sendLog('info','Bot出生点集合器 v9 已加载 (Nano4T)');
    sendLog('info','SP_BL | get_transform | set_position_Injected');
    sendLog('info','===============================');
})();
