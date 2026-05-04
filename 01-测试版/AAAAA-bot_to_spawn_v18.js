// ============================================================
// Bot 出生点集合器 v18 — 多重身份判定 + Transform降级
// v17发现: #20-#24 cam=0但rec=1 sk=1 cd=1 → isBot=0假象
//   FPS游戏中真人必有cameraManager → cam=0必是Bot
// 新增: cd=null条目 → characterContainer(0x58)降级传送
// ============================================================

(function() {
    'use strict';
    function L(l,m){var p='[BotSpawn] ';if(l==='e')console.error(p+m);else if(l==='w')console.warn(p+m);else console.log(p+m);}

    var mod=Process.findModuleByName('GameAssembly.dll');
    if(!mod){L('e','no GameAssembly.dll');return;}
    var B=mod.base, R={
        GM_AddP:0xAF9A90, MM_MapGun:0xAEBB70, P_Update:0xB551D0,
        P_isMy:0xB55FD0, E_isDead:0xB400E0, E_getCC:0x1CF180,
        C_setEn:0xAB86B0, getTrans:0x32CF40, setPosInj:0x3F4810,
    }, O={
        P_cd:0x94, CD_isB:0x14, GM_ap:0x1C, MM_SPG:0x14,
        P_cam:0x48, P_rec:0x54, P_skill:0xB0, P_cc:0x58,
    };

    var gm=null,mm=null,sc=null,ntp=false,tn=0;
    var isM=new NativeFunction(B.add(R.P_isMy),'bool',['pointer','pointer']);
    var isD=new NativeFunction(B.add(R.E_isDead),'bool',['pointer','pointer']);
    var gCC=new NativeFunction(B.add(R.E_getCC),'pointer',['pointer','pointer']);
    var cSE=new NativeFunction(B.add(R.C_setEn),'void',['pointer','int','pointer']);
    var gt=new NativeFunction(B.add(R.getTrans),'pointer',['pointer','pointer']);
    var sp=new NativeFunction(B.add(R.setPosInj),'void',['pointer','pointer','pointer']);
    var vb=Memory.alloc(16);

    function rp(a,o){try{return a.add(o).readPointer();}catch(e){return null;}}
    function rdS(p){if(!p||p.isNull())return null;
        try{if(p.add(0xC).readU32()===0)return null;}catch(e){return null;}
        try{var e=p.add(0x10);return {x:e.readFloat(),y:e.add(4).readFloat(),z:e.add(8).readFloat()};}catch(e2){return null;}
    }

    // 核心: 移动一个Player到spawn (拿根Transform或降级拿子节点)
    function movePlayer(pp, label){
        try{
            // Step1: 拿Transform (root first, fallback to characterContainer)
            var tr=gt(pp,ptr(0));         // 根Transform
            var fallback=false;
            if(!tr||tr.isNull()){
                tr=rp(pp,O.P_cc);          // 降级: characterContainer(子节点)
                fallback=true;
            }
            if(!tr||tr.isNull()) return 'T=null';

            // Step2: CC.disable
            try{var cc=gCC(pp,ptr(0));if(cc&&!cc.isNull())cSE(cc,0,ptr(0));}catch(e){}

            // Step3: 写Transform.position
            sp(tr,vb,ptr(0));
            try{var np=tr.add(0x10).readPointer();if(np){np.add(0x38).writeFloat(sc.x);np.add(0x3C).writeFloat(sc.y);np.add(0x40).writeFloat(sc.z);}}catch(e){}

            // Step4: CC.enable
            try{var cc2=gCC(pp,ptr(0));if(cc2&&!cc2.isNull())cSE(cc2,1,ptr(0));}catch(e){}

            return fallback?'OK(sub)':'OK';
        }catch(e){return 'crash:'+e.message;}
    }

    // Hooks
    try{Interceptor.attach(B.add(R.GM_AddP),{onEnter:function(a){if(!gm){gm=a[0];send(JSON.stringify({t:'gm'}));}}});}catch(e){}
    try{Interceptor.attach(B.add(R.MM_MapGun),{onEnter:function(a){
        if(!mm){mm=a[0];var sB=rdS(mm.add(0x10).readPointer()),sG=rdS(mm.add(O.MM_SPG).readPointer());sc=sG||sB;
            L('i','出生点('+sc.x.toFixed(1)+','+sc.y.toFixed(1)+','+sc.z.toFixed(1)+')');send(JSON.stringify({t:'mm'}));}
    }});}catch(e){}
    try{Interceptor.attach(B.add(R.P_Update),{onEnter:function(a){
        if(!ntp)return;ntp=false;if(!gm||!sc)return;tn++;

        vb.writeFloat(sc.x);vb.add(4).writeFloat(sc.y);vb.add(8).writeFloat(sc.z);
        var ap=gm.add(O.GM_ap).readPointer();
        if(!ap||ap.isNull()){L('e','ap==null');return;}
        var total=ap.add(0xC).readU32();
        L('i','═══ #'+tn+' (共'+total+'条目) ═══');

        var okA=0, okB=0, okC=0, deadC=0, skipC=0;

        for(var i=0;i<total;i++){
            try{
                var pp=ap.add(0x10+i*8).readPointer();
                if(!pp||pp.isNull()){skipC++;continue;}
                if(isM(pp,ptr(0))){L('i','  #'+i+': ☆玩家');skipC++;continue;}

                var cam=rp(pp,O.P_cam), rec=rp(pp,O.P_rec), sk=rp(pp,O.P_skill), cd=rp(pp,O.P_cd);
                var fp='cam='+(cam&&!cam.isNull()?'1':'0')+' rec='+(rec&&!rec.isNull()?'1':'0')+' sk='+(sk&&!sk.isNull()?'1':'0')+' cd='+(cd&&!cd.isNull()?'1':'0');
                var hasCam=!!(cam&&!cam.isNull()),
                    hasRec=!!(rec&&!rec.isNull()),
                    hasSk =!!(sk &&!sk.isNull()),
                    hasCd =!!(cd &&!cd.isNull());

                // ─── 身份判定 ───
                var isBot=false, reason='';

                if(hasCd){
                    var ib=0;try{ib=cd.add(O.CD_isB).readU8();}catch(e){}
                    if(ib){isBot=true;reason='isBot=1';}           // A类: ClientData确认的Bot
                    else if(!hasCam && hasRec && hasSk){isBot=true;reason='cam=0→必Bot';}  // B类: 无摄像机的"真人"假象
                    else if(!hasCam){isBot=true;reason='cam=0→必Bot';}                     // C类: 无摄像机
                    else {reason='真人(cam=1)';}                                            // D类: 有摄像机→真人
                } else {
                    // 无ClientData → 靠Player指纹
                    if(hasRec||hasSk){isBot=true;reason='cd=null但有Player指纹';}
                    else {reason='非Player';}
                }

                var label='#'+i+': ';
                if(!isBot){L('i','  '+label+reason+' fp='+fp);skipC++;continue;}

                // ─── 死亡检查 ───
                var dead;
                try{dead=isD(pp,ptr(0));}catch(e){dead=false;}
                if(dead){L('i','  '+label+'Bot('+reason+')(已死) fp='+fp);deadC++;continue;}

                // ─── 传送 ───
                var r=movePlayer(pp,label);
                if(r==='OK'){okA++;L('i','  '+label+'Bot('+reason+')→OK fp='+fp);}
                else if(r==='OK(sub)'){okB++;L('i','  '+label+'Bot('+reason+')→OK(sub) fp='+fp);}
                else{L('i','  '+label+'Bot('+reason+')→'+r+' fp='+fp);okC++;}
            }catch(e){
                L('i','  #'+i+': ★崩溃 '+e.message);
            }
        }

        var msg='成功='+(okA+okB)+' (根T='+okA+' 子T='+okB+')';
        if(deadC>0)msg+=' | 已死='+deadC;
        if(skipC>0)msg+=' | 跳过='+skipC;
        if(okC>0)msg+=' | 失败='+okC;
        L('i',msg);L('i','═══ 完成 ═══');
        send(JSON.stringify({t:'done',c:okA+okB,m:msg}));
    }});}catch(e){}

    rpc.exports={teleport:function(){
        if(!gm){send(JSON.stringify({t:'err',m:'GM未就绪'}));return;}
        ntp=true;
    }};
    L('i','====================');
    L('i','v18 | 多重身份判定');
    L('i','cam=0→必Bot | T降级');
    L('i','====================');
})();
