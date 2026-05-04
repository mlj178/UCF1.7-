// ============================================================
// Bot 出生点集合器 v17 — v15传送逻辑 + v16指纹诊断 (Nano4T)
// v16失效根因: f_cc=characterContainer(0x58)是模型子节点Transform
//              spi(f_cc,spawn) 改了子节点位置，根Transform没动
// 修复: 恢复 get_transform() 拿根Transform (v14/v15 14/14成功)
//       保留指纹识别 cam/rec/skill/cd 快速分类30个条目
// ============================================================

(function() {
    'use strict';

    function L(l,m){var p='[BotSpawn] ';if(l==='e')console.error(p+m);else if(l==='w')console.warn(p+m);else console.log(p+m);}

    var mod=Process.findModuleByName('GameAssembly.dll');
    if(!mod){L('e','GameAssembly.dll未找到');return;}
    var B=mod.base;

    var R={
        GM_AddP:0xAF9A90, MM_MapGun:0xAEBB70, P_Update:0xB551D0,
        P_isMy:0xB55FD0, E_isDead:0xB400E0, E_getCC:0x1CF180,
        C_setEn:0xAB86B0, getTrans:0x32CF40, setPosInj:0x3F4810,
    };
    var O={
        P_cd:0x94, CD_isB:0x14, GM_ap:0x1C, MM_SPG:0x14,
        P_cam:0x48, P_rec:0x54, P_skill:0xB0,
    };

    var gm=null, mm=null, spawn=null, ntp=false, tn=0;

    var isMy  =new NativeFunction(B.add(R.P_isMy),  'bool',   ['pointer','pointer']);
    var isDead=new NativeFunction(B.add(R.E_isDead),'bool',   ['pointer','pointer']);
    var getCC =new NativeFunction(B.add(R.E_getCC), 'pointer',['pointer','pointer']);
    var ccSetE=new NativeFunction(B.add(R.C_setEn), 'void',   ['pointer','int','pointer']);
    var gt    =new NativeFunction(B.add(R.getTrans),'pointer',['pointer','pointer']);
    var spi   =new NativeFunction(B.add(R.setPosInj),'void',  ['pointer','pointer','pointer']);
    var vb    =Memory.alloc(16);

    function rp(a,o){try{return a.add(o).readPointer();}catch(e){return null;}}
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
            var sB=rdS(mm.add(0x10).readPointer()), sG=rdS(mm.add(O.MM_SPG).readPointer());
            spawn=sG||sB;
            L('i','出生点('+spawn.x.toFixed(1)+','+spawn.y.toFixed(1)+','+spawn.z.toFixed(1)+')');
            send(JSON.stringify({t:'mm'}));
        }
    }});}catch(e){}
    try{Interceptor.attach(B.add(R.P_Update),{onEnter:function(a){
        if(!ntp)return; ntp=false;
        if(!gm||!spawn)return;
        tn++; L('i','═══ #'+tn+' ═══');

        vb.writeFloat(spawn.x); vb.add(4).writeFloat(spawn.y); vb.add(8).writeFloat(spawn.z);

        var ap=gm.add(O.GM_ap).readPointer();
        if(!ap||ap.isNull()){L('e','allPlayers==null');return;}
        var total=ap.add(0xC).readU32();

        var bot=0, dead=0, ok=0;

        for(var i=0;i<total;i++){
            try{
                var pp=ap.add(0x10+i*8).readPointer();
                if(!pp||pp.isNull()){L('i','  #'+i+': null');continue;}

                // 指纹 (仅用于日志,不决定传送逻辑)
                var cam=rp(pp,O.P_cam), rec=rp(pp,O.P_rec), sk=rp(pp,O.P_skill), cd=rp(pp,O.P_cd);
                var fp='cam='+(cam&&!cam.isNull()?'1':'0')+' rec='+(rec&&!rec.isNull()?'1':'0')+' sk='+(sk&&!sk.isNull()?'1':'0')+' cd='+(cd&&!cd.isNull()?'1':'0');

                if(isMy(pp,ptr(0))){L('i','  #'+i+': ★玩家');continue;}

                if(!cd||cd.isNull()){
                    // 无ClientData → 靠指纹判断
                    var isPlayer = (cam&&!cam.isNull())||(rec&&!rec.isNull())||(sk&&!sk.isNull());
                    if(isPlayer){
                        // 无ClientData的Player → 当Bot处理,尝试传送
                        var dOk=false;
                        try{
                            var tr=gt(pp,ptr(0));
                            if(tr&&!tr.isNull()){
                                try{var cc=getCC(pp,ptr(0));if(cc&&!cc.isNull())ccSetE(cc,0,ptr(0));}catch(e){}
                                spi(tr,vb,ptr(0));
                                try{var np=tr.add(0x10).readPointer();if(np){np.add(0x38).writeFloat(spawn.x);np.add(0x3C).writeFloat(spawn.y);np.add(0x40).writeFloat(spawn.z);}}catch(e){}
                                try{var cc2=getCC(pp,ptr(0));if(cc2&&!cc2.isNull())ccSetE(cc2,1,ptr(0));}catch(e){}
                                dOk=true;
                            }
                        }catch(e){}
                        if(dOk){ok++; L('i','  #'+i+': Bot?(cd=null) fp='+fp+' → OK(根T)');}
                        else   {L('i','  #'+i+': Bot?(cd=null) fp='+fp+' → FAIL'); bot++;}
                    } else {
                        L('i','  #'+i+': 非Player(墓碑?) fp='+fp);
                    }
                    continue;
                }

                // 有ClientData → 正常路径
                var ib=0;
                try{ib=cd.add(O.CD_isB).readU8();}catch(e){}
                if(!ib){L('i','  #'+i+': 真人 fp='+fp);continue;}

                var d=isDead(pp,ptr(0));
                if(d){L('i','  #'+i+': Bot(已死) fp='+fp);dead++;continue;}
                bot++;

                // CC.disable → 根Transform.move → CC.enable
                var mOk=false;
                try{
                    var cc=getCC(pp,ptr(0));
                    if(cc&&!cc.isNull())ccSetE(cc,0,ptr(0));
                    var tr=gt(pp,ptr(0));
                    if(tr&&!tr.isNull()){
                        spi(tr,vb,ptr(0));
                        try{var np=tr.add(0x10).readPointer();if(np){np.add(0x38).writeFloat(spawn.x);np.add(0x3C).writeFloat(spawn.y);np.add(0x40).writeFloat(spawn.z);}}catch(e){}
                        mOk=true;
                    }
                    if(cc&&!cc.isNull())ccSetE(cc,1,ptr(0));
                }catch(e){}
                if(mOk){ok++; L('i','  #'+i+': Bot fp='+fp+' → OK');}
                else   {L('i','  #'+i+': Bot fp='+fp+' → FAIL');}
            }catch(e){
                L('i','  #'+i+': ★崩溃 '+e.message);
            }
        }

        var msg='传送: '+ok+'/'+bot+' Bot 成功';
        if(dead>0)msg+=' | 已死='+dead;
        L('i',msg); L('i','═══ 完成 ═══');
        send(JSON.stringify({t:'done',c:ok,m:msg}));
    }});}catch(e){}

    rpc.exports={teleport:function(){
        if(!gm){send(JSON.stringify({t:'err',m:'GM未就绪'}));return;}
        ntp=true;
    }};

    L('i','========================================');
    L('i','v17 Nano4T | 根Transform+指纹诊断');
    L('i','修复: characterContainer→get_transform');
    L('i','========================================');
})();
