// ============================================================
// Bot 出生点集合器 v14 — SP_GR + 逐Bot传送详情
// 坐标: SP_GR[0] = (13.6,14.1,0.1)
// 每个 Bot 输出: CC状态 / Transform状态 / 是否写入成功
// ============================================================

(function() {
    'use strict';

    function L(l,m){var p='[BotSpawn] ';if(l==='e')console.error(p+m);else if(l==='w')console.warn(p+m);else console.log(p+m);}

    var mod=Process.findModuleByName('GameAssembly.dll');
    if(!mod){L('e','GameAssembly.dll未找到');return;}
    var B=mod.base;

    var R={
        GM_AddP:   0xAF9A90,  MM_MapGun: 0xAEBB70,  P_Update: 0xB551D0,
        P_isMy:    0xB55FD0,  E_isDead:  0xB400E0,  E_getCC:  0x1CF180,
        C_setEn:   0xAB86B0,  getTrans:  0x32CF40,  setPosInj: 0x3F4810,
    };

    var O={
        P_cd:0x94, CD_isB:0x14, GM_ap:0x1C,
        MM_SPG:0x14, MM_SPB:0x10, MM_SPN:0x18,
    };

    var gm=null, mm=null, spawn=null, ntp=false, tn=0;

    var isMy  =new NativeFunction(B.add(R.P_isMy), 'bool',   ['pointer','pointer']);
    var isDead=new NativeFunction(B.add(R.E_isDead),'bool',  ['pointer','pointer']);
    var getCC =new NativeFunction(B.add(R.E_getCC),'pointer',['pointer','pointer']);
    var ccSetE=new NativeFunction(B.add(R.C_setEn),'void',   ['pointer','int','pointer']);
    var gt    =new NativeFunction(B.add(R.getTrans),'pointer',['pointer','pointer']);
    var spi   =new NativeFunction(B.add(R.setPosInj),'void', ['pointer','pointer','pointer']);
    var vb    =Memory.alloc(16);

    function rdS(p){
        if(!p||p.isNull())return null;
        try{if(p.add(0xC).readU32()===0)return null;}catch(e){return null;}
        try{var e=p.add(0x10);return {x:e.readFloat(),y:e.add(4).readFloat(),z:e.add(8).readFloat()};}catch(e2){return null;}
    }

    // Hook GM
    try{Interceptor.attach(B.add(R.GM_AddP),{onEnter:function(a){
        if(!gm){gm=a[0];send(JSON.stringify({t:'gm'}));L('i','GM@'+gm);}
    }});}catch(e){}

    // Hook MM — 印刷全部出生点, 选 SP_GR
    try{Interceptor.attach(B.add(R.MM_MapGun),{onEnter:function(a){
        if(!mm){
            mm=a[0];
            var sN=rdS(mm.add(O.MM_SPN).readPointer());
            var sB=rdS(mm.add(O.MM_SPB).readPointer());
            var sG=rdS(mm.add(O.MM_SPG).readPointer());
            L('i','--- 全部出生点 ---');
            if(sN)L('i','SP_Netural: ('+sN.x.toFixed(1)+','+sN.y.toFixed(1)+','+sN.z.toFixed(1)+')');
            else   L('i','SP_Netural: (空)');
            if(sB)L('i','SP_BL:      ('+sB.x.toFixed(1)+','+sB.y.toFixed(1)+','+sB.z.toFixed(1)+')');
            else   L('i','SP_BL:      (空)');
            if(sG)L('i','SP_GR:      ('+sG.x.toFixed(1)+','+sG.y.toFixed(1)+','+sG.z.toFixed(1)+')');
            else   L('i','SP_GR:      (空)');

            // ★ 用户指定优先 SP_GR, 其次 SP_BL, 最后兜底
            spawn = sG || sB;
            L('i','→ 选中: '+(sG?'SP_GR':sB?'SP_BL':'无'));
            send(JSON.stringify({t:'mm'}));
        }
    }});}catch(e){}

    // Hook Player.Update
    try{Interceptor.attach(B.add(R.P_Update),{onEnter:function(a){
        if(!ntp)return; ntp=false;
        if(!gm)return;
        if(!spawn)spawn={x:0,y:0,z:0};
        tn++;
        L('i','══════ 传送 #'+tn+' ══════');
        L('i','出生点: ('+spawn.x.toFixed(1)+','+spawn.y.toFixed(1)+','+spawn.z.toFixed(1)+')');

        vb.writeFloat(spawn.x); vb.add(4).writeFloat(spawn.y); vb.add(8).writeFloat(spawn.z);

        var ap;
        try{ap=gm.add(O.GM_ap).readPointer();}catch(e){L('e','读取allPlayers失败');return;}
        if(!ap||ap.isNull()){L('e','allPlayers==null');return;}
        var total=ap.add(0xC).readU32();

        var bot=0, dead=0, skip=0, ok=0;
        var rows=[];

        for(var i=0;i<total;i++){
            try{
                // 安全读 Player*
                var pp;
                try{pp=ap.add(0x10+i*8).readPointer();}catch(e){pp=null;}
                if(!pp||pp.isNull()){rows.push('#'+i+': null → skip');skip++;continue;}

                // 玩家自己
                if(isMy(pp,ptr(0))){rows.push('#'+i+': ★玩家 → skip');skip++;continue;}

                // ClientData
                var cd;
                try{cd=pp.add(O.P_cd).readPointer();}catch(e){cd=null;}
                if(!cd||cd.isNull()){rows.push('#'+i+': cd=null → skip');skip++;continue;}

                // isBot
                var b;
                try{b=cd.add(O.CD_isB).readU8();}catch(e){b=0;}
                if(!b){rows.push('#'+i+': 真人 → skip');skip++;continue;}

                // isDead
                var d;
                try{d=isDead(pp,ptr(0));}catch(e){d=true;}
                if(d){rows.push('#'+i+': Bot已死');dead++;continue;}

                bot++;

                // --- 传送三步 ---
                var ccT='-', trT='-', nativeT='-';

                // Step1: CC.disable
                try{
                    var cc=getCC(pp,ptr(0));
                    if(cc&&!cc.isNull()){
                        ccSetE(cc,0,ptr(0));
                        ccT='off';
                    } else {ccT='null';}
                }catch(e){ccT='crash';}

                // Step2: move Transform
                try{
                    var tr=gt(pp,ptr(0));
                    if(tr&&!tr.isNull()){
                        spi(tr,vb,ptr(0));
                        trT='√';
                        // native直写
                        try{
                            var np=tr.add(0x10).readPointer();
                            if(np&&!np.isNull()){
                                np.add(0x38).writeFloat(spawn.x);
                                np.add(0x3C).writeFloat(spawn.y);
                                np.add(0x40).writeFloat(spawn.z);
                                nativeT='√';
                            }
                        }catch(e){}
                    } else {trT='null';}
                }catch(e){trT='crash';}

                // Step3: CC.enable
                if(ccT==='off'){
                    try{
                        var cc2=getCC(pp,ptr(0));
                        if(cc2&&!cc2.isNull()){ccSetE(cc2,1,ptr(0));ccT='ok';}
                    }catch(e){ccT='e-en';}
                }

                if(trT==='√') ok++;
                rows.push('#'+i+': Bot [CC='+ccT+' T='+trT+' N='+nativeT+'] '+(trT==='√'?'OK':'FAIL'));
            }catch(e){
                rows.push('#'+i+': ★异常 '+e.message);
            }
        }

        // 印刷所有结果
        for(var j=0;j<rows.length;j++)L('i','  '+rows[j]);

        var msg='传送: '+ok+'/'+bot+' Bot 成功';
        if(dead>0)msg+=' | 已死='+dead;
        if(skip>0)msg+=' | 跳过='+skip;
        L('i',msg);
        L('i','══════ 完成 ══════');
        send(JSON.stringify({t:'done',c:ok,m:msg}));
    }});}catch(e){}

    rpc.exports={teleport:function(){
        if(!gm){send(JSON.stringify({t:'err',m:'GM未就绪'}));return;}
        ntp=true; L('i','收到指令');
    }};

    L('i','========================================');
    L('i','v14 Nano4T | SP_GR | 逐Bot详情');
    L('i','CC.disable→move→enable');
    L('i','========================================');
})();
