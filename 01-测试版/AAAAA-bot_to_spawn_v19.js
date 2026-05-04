// ============================================================
// Bot 出生点集合器 v19 — 三重OR判定 + 全量日志 + Transform降级
// Bot判定: isBot==1 || (rec=1 && cam=0) || (cd=null && rec=1)
// 传送: rootT → subT(0x58) 降级
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
        C_setEn:0xAB86B0, getTrans:0x32CF40, setPosInj:0x3F4810,
    };
    var O={
        P_cd:0x94, CD_isB:0x14, GM_ap:0x1C, MM_SPG:0x14, MM_SPB:0x10,
        P_cam:0x48, P_rec:0x54, P_skill:0xB0, P_cc:0x58,
    };

    var gm=null,mm=null,sc=null,ntp=false,tn=0;
    var isM=new NativeFunction(B.add(R.P_isMy),'bool',['pointer','pointer']);
    var isD=new NativeFunction(B.add(R.E_isDead),'bool',['pointer','pointer']);
    var gCC=new NativeFunction(B.add(R.E_getCC),'pointer',['pointer','pointer']);
    var cSE=new NativeFunction(B.add(R.C_setEn),'void',['pointer','int','pointer']);
    var gt =new NativeFunction(B.add(R.getTrans),'pointer',['pointer','pointer']);
    var sp =new NativeFunction(B.add(R.setPosInj),'void',['pointer','pointer','pointer']);
    var vb=Memory.alloc(16);

    function rp(a,o){try{return a.add(o).readPointer();}catch(e){return null;}}
    function rdS(p){if(!p||p.isNull())return null;
        try{if(p.add(0xC).readU32()===0)return null;}catch(e){return null;}
        try{var e=p.add(0x10);return {x:e.readFloat(),y:e.add(4).readFloat(),z:e.add(8).readFloat()};}catch(e2){return null;}
    }

    function movePlayer(pp){
        var rootT=gt(pp,ptr(0));
        var subT =rp(pp,O.P_cc);   // characterContainer字段(0x58)
        var useT =null, tLabel='';
        if(rootT&&!rootT.isNull()){useT=rootT;tLabel='rootT';}
        else if(subT&&!subT.isNull()){useT=subT;tLabel='subT';}
        else return 'T=null';

        try{var cc=gCC(pp,ptr(0));if(cc&&!cc.isNull())cSE(cc,0,ptr(0));}catch(e){}
        sp(useT,vb,ptr(0));
        try{var np=useT.add(0x10).readPointer();if(np){np.add(0x38).writeFloat(sc.x);np.add(0x3C).writeFloat(sc.y);np.add(0x40).writeFloat(sc.z);}}catch(e){}
        try{var cc2=gCC(pp,ptr(0));if(cc2&&!cc2.isNull())cSE(cc2,1,ptr(0));}catch(e){}
        return 'OK['+tLabel+']';
    }

    // Hooks
    try{Interceptor.attach(B.add(R.GM_AddP),{onEnter:function(a){if(!gm){gm=a[0];send(JSON.stringify({t:'gm'}));}}});}catch(e){}
    try{Interceptor.attach(B.add(R.MM_MapGun),{onEnter:function(a){
        if(!mm){mm=a[0];
            var sB=rdS(mm.add(O.MM_SPB).readPointer()),sG=rdS(mm.add(O.MM_SPG).readPointer());
            sc=sG||sB;
            L('i','出生点('+sc.x.toFixed(1)+','+sc.y.toFixed(1)+','+sc.z.toFixed(1)+')');
            send(JSON.stringify({t:'mm'}));
        }
    }});}catch(e){}
    try{Interceptor.attach(B.add(R.P_Update),{onEnter:function(a){
        if(!ntp)return;ntp=false;if(!gm||!sc)return;tn++;

        vb.writeFloat(sc.x);vb.add(4).writeFloat(sc.y);vb.add(8).writeFloat(sc.z);
        var ap=gm.add(O.GM_ap).readPointer();
        if(!ap||ap.isNull()){L('e','allPlayers==null');return;}
        var total=ap.add(0xC).readU32();
        L('i','═══ #'+tn+' (共'+total+'个) ═══');

        var ok=0, deadC=0, skipC=0, failC=0;

        for(var i=0;i<total;i++){
            var pp; try{pp=ap.add(0x10+i*8).readPointer();}catch(e){pp=null;}
            if(!pp||pp.isNull()){
                L('i','  #'+i+': [null] 空槽位');
                skipC++;continue;
            }

            // --- 指纹 ---
            var cam   = rp(pp,O.P_cam),   hasC=!!(cam&&!cam.isNull());
            var rec   = rp(pp,O.P_rec),   hasR=!!(rec&&!rec.isNull());
            var sk    = rp(pp,O.P_skill), hasS=!!(sk &&!sk.isNull());
            var cd    = rp(pp,O.P_cd),    hasD=!!(cd &&!cd.isNull());
            var fp='cam='+(hasC?1:0)+' rec='+(hasR?1:0)+' sk='+(hasS?1:0)+' cd='+(hasD?1:0);

            // --- 本地玩家 ---
            if(isM(pp,ptr(0))){
                L('i','  #'+i+': [☆☆玩家] '+fp);
                skipC++;continue;
            }

            // --- 三重OR判定 ---
            var ib=0; if(hasD)try{ib=cd.add(O.CD_isB).readU8();}catch(e){}
            var tag='';
            if(ib){tag='isB=1';}                          // ① 明确标记
            else if(hasR && !hasC){tag='cam=0→Bot';}     // ② 无摄像机=必Bot
            else if(!hasD && hasR){tag='cd=null+rec=1';} // ③ 无数据但有Player指纹
            if(!tag){
                // 非Bot
                var humanTag='真人';
                if(hasC)humanTag='真人(cam=1)';
                else if(!hasR&&!hasS)humanTag='非Player(无指纹)';
                L('i','  #'+i+': ['+humanTag+'] '+fp);
                skipC++;continue;
            }

            // --- 是Bot → 检查死亡 ---
            var dead; try{dead=isD(pp,ptr(0));}catch(e){dead=false;}
            if(dead){
                L('i','  #'+i+': [Bot|'+tag+'] '+fp+' dead=1 → 跳过');
                deadC++;continue;
            }

            // --- 传送 ---
            var r=movePlayer(pp);
            if(r.startsWith('OK')){ok++;L('i','  #'+i+': [Bot|'+tag+'] '+fp+' dead=0 '+r);}
            else{failC++;L('i','  #'+i+': [Bot|'+tag+'] '+fp+' dead=0 → FAIL:'+r);}
        }

        var msg='成功='+ok;
        if(failC>0)msg+=' | 失败='+failC;
        if(deadC>0)msg+=' | 已死='+deadC;
        if(skipC>0)msg+=' | 跳过='+skipC;
        L('i',msg);L('i','═══ 完成 ═══');
        send(JSON.stringify({t:'done',c:ok,m:msg}));
    }});}catch(e){}

    rpc.exports={teleport:function(){
        if(!gm){send(JSON.stringify({t:'err',m:'GM未就绪'}));return;}
        ntp=true;
    }};
    L('i','========================================');
    L('i','v19 | 三重OR | 全量日志 | rootT→subT降级');
    L('i','Bot=isB=1|(rec=1&&cam=0)|(cd=null&&rec=1)');
    L('i','========================================');
})();
