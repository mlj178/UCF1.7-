// ============================================================
// Bot 出生点集合器 v16 — 全场身份大检验 (Nano4T)
// 诊断: #16 CC=yes T=e → 有CC但Transform崩,可能是Player但状态异常
//       #18-20 CC=no → 不是Player(可能是TombStone/墓碑)
// 方法: 对所有30条目做多字段指纹识别确认身份
// ============================================================

(function() {
    'use strict';

    function L(l,m){var p='[BotSpawn] ';if(l==='e')console.error(p+m);else if(l==='w')console.warn(p+m);else console.log(p+m);}

    var mod=Process.findModuleByName('GameAssembly.dll');
    if(!mod){L('e','no GameAssembly.dll');return;}
    var B=mod.base;

    var R={
        GM_AddP:0xAF9A90, MM_MapGun:0xAEBB70, P_Update:0xB551D0,
        P_isMy:0xB55FD0, E_isDead:0xB400E0, E_getCC:0x1CF180,
        C_setEn:0xAB86B0, setPosInj:0x3F4810,
    };

    var O={
        P_cd:0x94, CD_isB:0x14, GM_ap:0x1C, MM_SPG:0x14,
        // Player 专属字段 (用于身份识别)
        P_cam:0x48,       // cameraManager → 有=Player
        P_rec:0x54,       // recoil → 有=Player
        P_charCont:0x58,  // characterContainer (Transform*) → 直接读
        P_skills:0xB0,    // skills → 有=Player
    };

    var gm=null, mm=null, spawn=null, ntp=false, tn=0;

    var isMy  =new NativeFunction(B.add(R.P_isMy),  'bool',   ['pointer','pointer']);
    var isDead=new NativeFunction(B.add(R.E_isDead),'bool',   ['pointer','pointer']);
    var getCC =new NativeFunction(B.add(R.E_getCC), 'pointer',['pointer','pointer']);
    var ccSetE=new NativeFunction(B.add(R.C_setEn), 'void',   ['pointer','int','pointer']);
    var spi   =new NativeFunction(B.add(R.setPosInj),'void',  ['pointer','pointer','pointer']);
    var vb    =Memory.alloc(16);

    // 安全读指针字段
    function rp(addr,off){
        try{return addr.add(off).readPointer();}catch(e){return null;}
    }
    // 安全读 bool
    function rb(addr,off){
        try{return addr.add(off).readU8();}catch(e){return -1;}
    }

    function rdS(p){
        if(!p||p.isNull())return null;
        try{if(p.add(0xC).readU32()===0)return null;}catch(e){return null;}
        try{var e=p.add(0x10);return {x:e.readFloat(),y:e.add(4).readFloat(),z:e.add(8).readFloat()};}catch(e2){return null;}
    }

    try{Interceptor.attach(B.add(R.GM_AddP),{onEnter:function(a){
        if(!gm){gm=a[0];send(JSON.stringify({t:'gm'}));}
    }});}catch(e){}

    try{Interceptor.attach(B.add(R.MM_MapGun),{onEnter:function(a){
        if(!mm){
            mm=a[0];
            var sB=rdS(mm.add(0x10).readPointer());
            var sG=rdS(mm.add(O.MM_SPG).readPointer());
            spawn=sG||sB;
            L('i','SP_GR = ('+spawn.x.toFixed(1)+','+spawn.y.toFixed(1)+','+spawn.z.toFixed(1)+')');
            send(JSON.stringify({t:'mm'}));
        }
    }});}catch(e){}

    try{Interceptor.attach(B.add(R.P_Update),{onEnter:function(a){
        if(!ntp)return; ntp=false;
        if(!gm||!spawn)return;
        tn++;
        L('i','══════ 身份检验 #'+tn+' ══════');

        vb.writeFloat(spawn.x); vb.add(4).writeFloat(spawn.y); vb.add(8).writeFloat(spawn.z);

        var ap=gm.add(O.GM_ap).readPointer();
        if(!ap||ap.isNull()){L('e','allPlayers null');return;}
        var total=ap.add(0xC).readU32();
        L('i','allPlayers 长度='+total);

        var botOK=0, botFail=0, deadC=0;

        for(var i=0;i<total;i++){
            try{
                var pp=ap.add(0x10+i*8).readPointer();
                if(!pp||pp.isNull()){
                    L('i','  #'+i+': ═ null (槽位空)');
                    continue;
                }

                // ---- 指纹识别 ----
                // 读取 Player 专有字段作为指纹
                var f_cd    = rp(pp,O.P_cd);        // ClientData*
                var f_cam   = rp(pp,O.P_cam);       // cameraManager*
                var f_rec   = rp(pp,O.P_rec);       // recoil*
                var f_skill = rp(pp,O.P_skills);    // skills*
                var f_cc    = rp(pp,O.P_charCont);  // characterContainer(Transform*,字段直读)

                // 分类
                var isSelf=false;
                try{isSelf=isMy(pp,ptr(0));}catch(e){}

                var hasCam = !!(f_cam && !f_cam.isNull());
                var hasRec = !!(f_rec && !f_rec.isNull());
                var hasSkill = !!(f_skill && !f_skill.isNull());
                var hasCd = !!(f_cd && !f_cd.isNull());
                var hasCCt = !!(f_cc && !f_cc.isNull());
                var isBot = false;
                if(hasCd){
                    try{isBot=!!f_cd.add(O.CD_isB).readU8();}catch(e){}
                }

                // 构建指纹串
                var fp='cam='+(hasCam?'1':'0')+' rec='+(hasRec?'1':'0')+' skill='+(hasSkill?'1':'0')+' cd='+(hasCd?'1':'0')+' cc='+(hasCCt?'1':'0');

                if(isSelf){
                    L('i','  #'+i+': ★★ 本地玩家 ('+fp+')');
                    continue;
                }

                if(hasCam||hasRec||hasSkill){
                    // 确认是 Player
                    if(hasCd&&isBot){
                        // Bot 有 ClientData
                        var d=false;
                        try{d=isDead(pp,ptr(0));}catch(e){d=true;}
                        if(d){L('i','  #'+i+': Bot ('+fp+') [已死亡]');deadC++;continue;}

                        // 传送
                        var ok=false;
                        try{
                            var cc=getCC(pp,ptr(0));
                            if(cc&&!cc.isNull())try{ccSetE(cc,0,ptr(0));}catch(e){}
                            if(hasCCt){
                                spi(f_cc,vb,ptr(0));
                                try{var np=f_cc.add(0x10).readPointer();if(np){np.add(0x38).writeFloat(spawn.x);np.add(0x3C).writeFloat(spawn.y);np.add(0x40).writeFloat(spawn.z);}}catch(e){}
                                ok=true;
                            }
                            if(cc&&!cc.isNull())try{ccSetE(cc,1,ptr(0));}catch(e){}
                        }catch(e){}
                        if(ok){botOK++;L('i','  #'+i+': Bot✓ ('+fp+') → OK');}
                        else  {botFail++;L('i','  #'+i+': Bot ('+fp+') → FAIL(无Transform)');}
                    } else if(hasCd&&!isBot){
                        L('i','  #'+i+': 真人 ('+fp+')');
                    } else {
                        // Player无ClientData, 但有cameraManager → 可能是未初始化的玩家
                        L('i','  #'+i+': Player? ('+fp+') [无ClientData,疑似Bot]');
                        // 尝试传送
                        if(hasCCt){
                            try{var cc=getCC(pp,ptr(0));if(cc&&!cc.isNull())ccSetE(cc,0,ptr(0));}catch(e){}
                            try{spi(f_cc,vb,ptr(0));var np=f_cc.add(0x10).readPointer();if(np){np.add(0x38).writeFloat(spawn.x);np.add(0x3C).writeFloat(spawn.y);np.add(0x40).writeFloat(spawn.z);}}catch(e){}
                            try{var cc2=getCC(pp,ptr(0));if(cc2&&!cc2.isNull())ccSetE(cc2,1,ptr(0));}catch(e){}
                            botOK++;L('i','    ↳ 已传送！');
                        } else {botFail++;L('i','    ↳ 无Transform,跳过');}
                    }
                } else {
                    // 不是 Player (无cameraManager,无recoil,无skills)
                    // 可能是 TombStone 或已销毁对象
                    if(!hasCCt){
                        L('i','  #'+i+': 非Player ('+fp+') [可能是TombStone/墓碑]');
                    } else {
                        L('i','  #'+i+': ?未知 ('+fp+') [无Player指纹但有Transform]');
                    }
                }
            }catch(e){
                L('i','  #'+i+': ★崩溃 '+e.message);
            }
        }

        var msg='传送: '+botOK+' 成功 | 失败='+botFail+' | 已死='+deadC;
        L('i',msg);
        L('i','══════ 完成 ══════');
        send(JSON.stringify({t:'done',c:botOK,m:msg}));
    }});}catch(e){}

    rpc.exports={teleport:function(){
        if(!gm){send(JSON.stringify({t:'err',m:'GM未就绪'}));return;}
        ntp=true;
    }};

    L('i','============================================');
    L('i','v16 Nano4T | 全场身份指纹检测');
    L('i','cam/rec/skill=Player指纹 | cc=Transform字段');
    L('i','============================================');
})();
