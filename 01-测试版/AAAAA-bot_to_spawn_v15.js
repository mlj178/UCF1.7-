// ============================================================
// Bot 出生点集合器 v15 — 深度诊断 cd=null 条目
// 问题: #16,#18,#19,#20 有 Player 指针但 ClientData 为 null
//       这些可能是未被 ClientData 初始化的 Bot 或其他类型实体
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
        P_cd:0x94, CD_isB:0x14, GM_ap:0x1C, MM_SPG:0x14,
    };

    var gm=null, mm=null, spawn=null, ntp=false, tn=0;

    var isMy  =new NativeFunction(B.add(R.P_isMy),  'bool',   ['pointer','pointer']);
    var isDead=new NativeFunction(B.add(R.E_isDead),'bool',   ['pointer','pointer']);
    var getCC =new NativeFunction(B.add(R.E_getCC), 'pointer',['pointer','pointer']);
    var ccSetE=new NativeFunction(B.add(R.C_setEn), 'void',   ['pointer','int','pointer']);
    var gt    =new NativeFunction(B.add(R.getTrans),'pointer',['pointer','pointer']);
    var spi   =new NativeFunction(B.add(R.setPosInj),'void',  ['pointer','pointer','pointer']);
    var vb    =Memory.alloc(16);

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
            L('i','SP_GR: ('+spawn.x.toFixed(1)+','+spawn.y.toFixed(1)+','+spawn.z.toFixed(1)+')');
            send(JSON.stringify({t:'mm'}));
        }
    }});}catch(e){}

    try{Interceptor.attach(B.add(R.P_Update),{onEnter:function(a){
        if(!ntp)return; ntp=false;
        if(!gm||!spawn)return;
        tn++;
        L('i','══════ #'+tn+' ══════');

        vb.writeFloat(spawn.x); vb.add(4).writeFloat(spawn.y); vb.add(8).writeFloat(spawn.z);

        var ap=gm.add(O.GM_ap).readPointer();
        if(!ap||ap.isNull()){L('e','allPlayers null');return;}
        var total=ap.add(0xC).readU32();
        L('i','数组长度='+total);

        var bot=0, dead=0, skip=0, ok=0, mystery=0, mysteryBot=0;
        var rows=[];

        for(var i=0;i<total;i++){
            try{
                var pp=ap.add(0x10+i*8).readPointer();
                if(!pp||pp.isNull()){skip++;continue;}

                if(isMy(pp,ptr(0))){rows.push('#'+i+': ★你自己');skip++;continue;}

                // --- 读 ClientData ---
                var cd, cdRaw=false;
                try{cd=pp.add(O.P_cd).readPointer();}catch(e){cd=null;}
                if(cd&&!cd.isNull()) cdRaw=true;

                if(!cdRaw){
                    // ★ 诊断: 没有 ClientData 的 Player
                    mystery++;
                    // 尝试读实体级信息
                    var teamH, hasHealth, hasAnim, hasCC, ccR;
                    try{
                        var raw0=pp.add(0x20).readU8(); // 摸一下 offset 0x20
                        try{var cc=getCC(pp,ptr(0));if(cc&&!cc.isNull())hasCC='yes';else hasCC='no';}catch(e){hasCC='e';}
                        try{var tr=gt(pp,ptr(0));if(tr&&!tr.isNull())ccR='yes';else ccR='no';}catch(e){ccR='e';}
                        rows.push('#'+i+': ⚡cd=null [CC='+hasCC+' T='+ccR+' raw0x20='+raw0+']');
                    }catch(e){
                        rows.push('#'+i+': ⚡cd=null [read失败:'+e.message+']');
                    }

                    // 尝试传送 (即使没有 ClientData, 能传就传)
                    try{
                        var tr=gt(pp,ptr(0));
                        if(tr&&!tr.isNull()){
                            try{var cc=getCC(pp,ptr(0));if(cc&&!cc.isNull())ccSetE(cc,0,ptr(0));}catch(e){}
                            spi(tr,vb,ptr(0));
                            try{
                                var np=tr.add(0x10).readPointer();
                                if(np){np.add(0x38).writeFloat(spawn.x);np.add(0x3C).writeFloat(spawn.y);np.add(0x40).writeFloat(spawn.z);}
                            }catch(e){}
                            try{var cc2=getCC(pp,ptr(0));if(cc2&&!cc2.isNull())ccSetE(cc2,1,ptr(0));}catch(e){}
                            mysteryBot++;
                        }
                    }catch(e){}
                    continue;
                }

                // --- 正常 ClientData 路径 ---
                var ib;
                try{ib=cd.add(O.CD_isB).readU8();}catch(e){ib=0;}
                if(!ib){rows.push('#'+i+': 真人');skip++;continue;}

                // isDead
                var d;
                try{d=isDead(pp,ptr(0));}catch(e){d=true;}
                if(d){rows.push('#'+i+': Bot(已死)');dead++;continue;}

                bot++;

                // --- 传送 ---
                var tc='-';
                try{var cc=getCC(pp,ptr(0));if(cc&&!cc.isNull()){ccSetE(cc,0,ptr(0));tc='ok';}}catch(e){tc='e';}

                try{var tr=gt(pp,ptr(0));if(tr&&!tr.isNull()){spi(tr,vb,ptr(0));
                    try{var np=tr.add(0x10).readPointer();if(np){np.add(0x38).writeFloat(spawn.x);np.add(0x3C).writeFloat(spawn.y);np.add(0x40).writeFloat(spawn.z);}}catch(e){}};
                    tc='√';}catch(e){tc='X';}

                if(tc!=='e'){
                    try{var cc2=getCC(pp,ptr(0));if(cc2&&!cc2.isNull())ccSetE(cc2,1,ptr(0));}catch(e){}
                }

                if(tc==='√') ok++;
                rows.push('#'+i+': Bot [CC='+tc+'] '+(tc==='√'?'OK':'FAIL'));
            }catch(e){
                rows.push('#'+i+': ★崩溃 '+e.message);
            }
        }

        for(var j=0;j<rows.length;j++)L('i','  '+rows[j]);

        var msg='Bot: '+ok+'/'+bot+' | 谜之cd=null: '+mystery+' (已传='+mysteryBot+')';
        if(dead>0)msg+=' | 已死='+dead;
        if(skip>0)msg+=' | 跳过='+skip;
        L('i',msg);
        L('i','══════ 完成 ══════');
        send(JSON.stringify({t:'done',c:ok,mb:mysteryBot,m:msg}));
    }});}catch(e){}

    rpc.exports={teleport:function(){
        if(!gm){send(JSON.stringify({t:'err',m:'GM未就绪'}));return;}
        ntp=true;
    }};

    L('i','====================');
    L('i','v15 Nano4T | cd=null诊断');
    L('i','====================');
})();
