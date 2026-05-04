// ============================================================
// Bot 出生点集合器 v10 — 冻结AI + 传送 (Nano4T)
// 根因: v9 Trans=14 但位置没变 → Bot.UpdateAction 每帧覆盖我们的修改
// 修复: 替换 Bot.UpdateAction 为空 → AI冻结 → 传送永久生效
// ============================================================

(function() {
    'use strict';

    function L(l, m) {
        var p = '[BotToSpawn] ';
        if (l==='e') console.error(p+m);
        else if (l==='w') console.warn(p+m);
        else console.log(p+m);
    }

    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) { L('e','GameAssembly.dll not found'); return; }
    var ba = mod.base;
    L('i','base='+ba);

    // ============================================================
    // RVA (全部 Image 50)
    // ============================================================
    var R = {
        GM_AddPlayer:     0xAF9A90,
        MM_MapGunInit:    0xAEBB70,
        Player_Update:    0xB551D0,
        Bot_UpdateAction: 0xB33070,
        Player_isMy:      0xB55FD0,
        Entity_isDead:    0xB400E0,
        Player_SetPos:    0xB534C0,
    };
    var O = {
        P_clientData: 0x94,
        CD_isBot:     0x14,
        GM_allP:      0x1C,
        MM_SP_BL:     0x10,
    };

    var gm=null, mm=null, ntp=false, tpn=0;
    var spawn=null, aiFrozen=false;

    var isMy = new NativeFunction(ba.add(R.Player_isMy), 'bool', ['pointer','pointer']);
    var isDead=new NativeFunction(ba.add(R.Entity_isDead),'bool',['pointer','pointer']);
    var setPos=new NativeFunction(ba.add(R.Player_SetPos),'void',['pointer','pointer','pointer']);
    var veB  = Memory.alloc(16);

    // 读 SP_BL[0]: Vector3(x,y,z)
    function rdS(p) {
        if (!p||p.isNull()) return null;
        if (p.add(0xC).readU32()===0) return null;
        var e=p.add(0x10);
        return {x:e.readFloat(),y:e.add(4).readFloat(),z:e.add(8).readFloat()};
    }

    // Hook: GameManager
    try { Interceptor.attach(ba.add(R.GM_AddPlayer),{
        onEnter:function(a){if(!gm){gm=a[0];send(JSON.stringify({t:'gm'}));L('i','GM@'+gm);}}
    });} catch(e){}

    // Hook: MapManager — 触发时缓存出生点
    try { Interceptor.attach(ba.add(R.MM_MapGunInit),{
        onEnter:function(a){
            if(!mm){
                mm=a[0];
                try{spawn=rdS(mm.add(O.MM_SP_BL).readPointer());
                    L('i','SP_BL:('+spawn.x.toFixed(1)+','+spawn.y.toFixed(1)+','+spawn.z.toFixed(1)+')');}
                catch(x){}
                send(JSON.stringify({t:'mm'}));
            }
        }
    });} catch(e){}

    // Hook: Player.Update — 主线程入口
    try { Interceptor.attach(ba.add(R.Player_Update),{
        onEnter:function(a){
            if (!ntp) return;
            ntp=false;

            // --- 步骤1: 冻结 Bot AI ---
            if (!aiFrozen) {
                L('i','冻结Bot.UpdateAction...');
                try {
                    Interceptor.replace(ba.add(R.Bot_UpdateAction),
                        new NativeCallback(function(){},'void',['pointer','pointer']));
                    aiFrozen=true;
                    L('i','✓ Bot.UpdateAction 已替换为空');
                } catch(e) { L('e','替换失败:'+e.message); }
            }

            if (!gm) return;
            if (!spawn) spawn={x:0,y:0,z:0};

            // --- 步骤2: 传送 ---
            L('i','=== 传送 #'+(++tpn)+' ===');
            L('i','出生点:('+spawn.x.toFixed(1)+','+spawn.y.toFixed(1)+','+spawn.z.toFixed(1)+')');

            veB.writeFloat(spawn.x);
            veB.add(4).writeFloat(spawn.y);
            veB.add(8).writeFloat(spawn.z);

            var ap=gm.add(O.GM_allP).readPointer();
            if (!ap||ap.isNull()) return;
            var n=ap.add(0xC).readU32();

            var bot=0,dead=0,skip=0,crash=0;
            for (var i=0;i<n;i++) {
                if (crash>=3) break;
                try {
                    var pp=ap.add(0x10+i*8).readPointer();
                    if (!pp||pp.isNull()){skip++;continue;}
                    if (isMy(pp,ptr(0))){skip++;continue;}

                    var cd=pp.add(O.P_clientData).readPointer();
                    if (!cd||cd.isNull()){skip++;continue;}
                    if (!cd.add(O.CD_isBot).readU8()){skip++;continue;}
                    if (isDead(pp,ptr(0))){dead++;continue;}

                    setPos(pp,veB,ptr(0));
                    bot++;
                } catch(e) {
                    crash++;
                    L('w','#'+i+' 异常:'+e.message);
                }
            }

            var msg='传送 '+bot+' 个Bot | AI冻结='+aiFrozen;
            if (dead>0) msg+=' | '+dead+' 死亡';
            if (skip>0) msg+=' | '+skip+' 跳过';
            L('i',msg);
            send(JSON.stringify({t:'done',c:bot,m:msg}));
        }
    });} catch(e){}

    rpc.exports = {
        teleport: function() {
            if (!gm) { send(JSON.stringify({t:'err',m:'GM未就绪'})); return; }
            ntp=true;
            L('i','收到指令');
        }
    };

    L('i','==========================');
    L('i','v10 Nano4T | 冻结AI+传送');
    L('i','==========================');
})();
