// ============================================================
// Bot 出生点集合器 v13 — Nano4T 全Bot + 印刷全部出生点 + 健壮遍历
// 突破: v12 CC.disable→move→CC.enable 生效 (14/14 Bot)
// 修复: #25/#27/#29 数组空洞导致crash → 健壮遍历
//       打印 SP_Netural/SP_BL/SP_GR 三个坐标，方便确认正确出生点
// ============================================================

(function() {
    'use strict';

    function L(l,m){var p='[BotSpawn] ';if(l==='e')console.error(p+m);else if(l==='w')console.warn(p+m);else console.log(p+m);}

    var mod=Process.findModuleByName('GameAssembly.dll');
    if(!mod){L('e','GameAssembly.dll未找到');return;}
    var B=mod.base;

    var R={
        GM_AddP:    0xAF9A90,
        MM_MapGun:  0xAEBB70,
        P_Update:   0xB551D0,
        P_isMy:     0xB55FD0,
        E_isDead:   0xB400E0,
        E_getCC:    0x1CF180,
        C_setEn:    0xAB86B0,
        getTrans:   0x32CF40,
        setPosInj:  0x3F4810,
    };

    var O={
        P_cd:   0x94,  CD_isB:0x14,  GM_ap:0x1C,
        MM_SPN: 0x18,  // SP_Netural
        MM_SPB: 0x10,  // SP_BL
        MM_SPG: 0x14,  // SP_GR
    };

    var gm=null, mm=null;
    var spawn=null;       // 选中的出生点
    var spawnN=null;      // SP_Netural[0]
    var spawnB=null;      // SP_BL[0]
    var spawnG=null;      // SP_GR[0]
    var ntp=false, tn=0;

    var isMy  =new NativeFunction(B.add(R.P_isMy),  'bool',    ['pointer','pointer']);
    var isDead=new NativeFunction(B.add(R.E_isDead),'bool',    ['pointer','pointer']);
    var getCC =new NativeFunction(B.add(R.E_getCC), 'pointer', ['pointer','pointer']);
    var ccSetE=new NativeFunction(B.add(R.C_setEn), 'void',    ['pointer','int','pointer']);
    var gt    =new NativeFunction(B.add(R.getTrans),'pointer', ['pointer','pointer']);
    var spi   =new NativeFunction(B.add(R.setPosInj),'void',  ['pointer','pointer','pointer']);

    var vb=Memory.alloc(16);

    // 读取 SpawnPoint[index]
    function rdS(p){
        if(!p||p.isNull())return null;
        try{var len=p.add(0xC).readU32();if(len===0)return null;}catch(e){return null;}
        try{var e=p.add(0x10);return {x:e.readFloat(),y:e.add(4).readFloat(),z:e.add(8).readFloat()};}catch(e2){return null;}
    }

    // 安全读 allPlayers[i]
    function safeP(arr,i){
        try{
            var p=arr.add(0x10+i*8);
            var sz=Process.pointerSize===8?8:4;
            // 用 try-read 替代读指针，避免访问违规
            return p.readPointer();
        }catch(e){return null;}
    }

    // Hook GM
    try{Interceptor.attach(B.add(R.GM_AddP),{onEnter:function(a){
        if(!gm){gm=a[0];send(JSON.stringify({t:'gm'}));L('i','GM@'+gm);}
    }});}catch(e){}

    // Hook MM — 缓存全部出生点
    try{Interceptor.attach(B.add(R.MM_MapGun),{onEnter:function(a){
        if(!mm){
            mm=a[0];
            spawnN=rdS(mm.add(O.MM_SPN).readPointer());
            spawnB=rdS(mm.add(O.MM_SPB).readPointer());
            spawnG=rdS(mm.add(O.MM_SPG).readPointer());
            L('i','--- 所有出生点 ---');
            if(spawnN)L('i','SP_Netural[0]: ('+spawnN.x.toFixed(1)+','+spawnN.y.toFixed(1)+','+spawnN.z.toFixed(1)+')');
            else L('i','SP_Netural[0]: (空)');
            if(spawnB)L('i','SP_BL[0]:     ('+spawnB.x.toFixed(1)+','+spawnB.y.toFixed(1)+','+spawnB.z.toFixed(1)+')');
            else L('i','SP_BL[0]:     (空)');
            if(spawnG)L('i','SP_GR[0]:     ('+spawnG.x.toFixed(1)+','+spawnG.y.toFixed(1)+','+spawnG.z.toFixed(1)+')');
            else L('i','SP_GR[0]:     (空)');
            // 优先选 SP_Netural, 其次 SP_BL, 最后 SP_GR
            spawn=spawnN||spawnB||spawnG;
            L('i','→ 选中出生点: '+(spawnN?'SP_Netural':spawnB?'SP_BL':'SP_GR'));
            send(JSON.stringify({t:'mm'}));
        }
    }});}catch(e){}

    // Hook Player.Update — 传送
    try{Interceptor.attach(B.add(R.P_Update),{onEnter:function(a){
        if(!ntp)return; ntp=false;
        if(!gm)return;
        if(!spawn)spawn=spawnN||spawnB||spawnG||{x:0,y:0,z:0};
        tn++;
        L('i','══════ 传送 #'+tn+' ══════');
        L('i','出生点: ('+spawn.x.toFixed(1)+','+spawn.y.toFixed(1)+','+spawn.z.toFixed(1)+')');

        vb.writeFloat(spawn.x); vb.add(4).writeFloat(spawn.y); vb.add(8).writeFloat(spawn.z);

        var ap=gm.add(O.GM_ap).readPointer();
        if(!ap||ap.isNull()){L('e','allPlayers==null');return;}
        var total=ap.add(0xC).readU32();
        L('i','数组长度='+total);

        // ---- 识别 + 传送 ----
        var botId=0, deadC=0, skipC=0, okC=0, errC=0;
        var idLog=[];

        for(var i=0;i<total;i++){
            try{
                var pp=safeP(ap,i);
                if(!pp||pp.isNull()){
                    idLog.push('#'+i+': null(跳过)');
                    skipC++; continue;
                }

                // 本地玩家
                if(isMy(pp,ptr(0))){
                    idLog.push('#'+i+': ★玩家(跳过)');
                    skipC++; continue;
                }

                // ClientData
                var cd;
                try{cd=pp.add(O.P_cd).readPointer();}catch(e){cd=null;}
                if(!cd||cd.isNull()){
                    idLog.push('#'+i+': cd=null(跳过)');
                    skipC++; continue;
                }

                var isBot;
                try{isBot=cd.add(O.CD_isB).readU8();}catch(e){isBot=0;}
                if(!isBot){
                    idLog.push('#'+i+': 真人(跳过)');
                    skipC++; continue;
                }

                // 死亡
                var dead;
                try{dead=isDead(pp,ptr(0));}catch(e){dead=true;}
                if(dead){
                    idLog.push('#'+i+': Bot(已死)');
                    deadC++; continue;
                }

                idLog.push('#'+i+': Bot ✓ 传送中');
                botId++;

                // --- CharacterController.disable → move → enable ---
                var ccOk=false, trOk=false;
                try{
                    var cc=getCC(pp,ptr(0));
                    if(cc&&!cc.isNull()){
                        ccSetE(cc,0,ptr(0));
                        ccOk=true;
                    }
                }catch(e){}

                try{
                    var tr=gt(pp,ptr(0));
                    if(tr&&!tr.isNull()){
                        spi(tr,vb,ptr(0));
                        // native直写(双保险)
                        try{
                            var np=tr.add(0x10).readPointer();
                            if(np&&!np.isNull()){
                                np.add(0x38).writeFloat(spawn.x);
                                np.add(0x3C).writeFloat(spawn.y);
                                np.add(0x40).writeFloat(spawn.z);
                            }
                        }catch(e){}
                        trOk=true;
                    }
                }catch(e){}

                if(ccOk){
                    try{ccSetE(cc,1,ptr(0));}catch(e){}
                }

                if(trOk) okC++;
                else skipC++;
            }catch(e){
                idLog.push('#'+i+': ★异常 '+e.message);
                errC++;
            }
        }

        // 打印识别
        for(var j=0;j<idLog.length;j++)L('i','  '+idLog[j]);

        var msg='传送 '+okC+'/'+botId+' Bot';
        if(deadC>0)msg+=' | 已死='+deadC;
        if(skipC>0)msg+=' | 跳过='+skipC;
        if(errC>0)msg+=' | 异常='+errC;
        L('i',msg);
        L('i','══════ 完成 ══════');
        send(JSON.stringify({t:'done',c:okC,m:msg}));
    }});}catch(e){}

    rpc.exports={teleport:function(){
        if(!gm){send(JSON.stringify({t:'err',m:'GM未就绪'}));return;}
        ntp=true; L('i','收到传送指令');
    }};

    L('i','========================================');
    L('i','v13 Nano4T | 全部出生点 | 健壮遍历');
    L('i','CC.disable→move→enable | SP_Netural优先');
    L('i','========================================');
})();
