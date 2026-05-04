// ============================================================
// Bot 出生点集合器 v12 — CC.disable→move→CC.enable (Nano4T)
// 根因: v1-v11 直接写 Transform/SetPos → CharacterController 立刻覆盖
// 修复: CC.set_enabled(false) → 移动 Transform → CC.set_enabled(true)
//       + Nano4T 模式确认 + 详细识别日志
// ============================================================

(function() {
    'use strict';

    function L(l,m){var p='[BotToSpawn] ';if(l==='e')console.error(p+m);else if(l==='w')console.warn(p+m);else console.log(p+m);}

    var m=Process.findModuleByName('GameAssembly.dll');
    if(!m){L('e','GameAssembly.dll未找到');return;}
    var B=m.base;
    L('i','base='+B);

    // ============================================================
    // RVA (全部在 GameAssembly – IL2CPP 编入单二进制)
    // ============================================================
    var R={
        GM_AddP:    0xAF9A90,  // Image 50
        MM_MapGun:  0xAEBB70,  // Image 50
        P_Update:   0xB551D0,  // Image 50
        P_isMy:     0xB55FD0,  // Image 50
        E_isDead:   0xB400E0,  // Image 50
        ModeNano4T: 0xB467A0,  // Image 50 返回 Mode_Nano4_Terminator*
        E_getCC:    0x1CF180,  // Image 0  Entity.get_characterController()
        C_setEn:    0xAB86B0,  // Image 7  Collider.set_enabled(bool)
        C_getEn:    0xAB8650,  // Image 7  Collider.get_enabled()
        getTrans:   0x32CF40,  // Image 7  Component.get_transform()
        setPosInj:  0x3F4810,  // Image 7  Transform.set_position_Injected
    };

    // 字段偏移
    var O={
        P_cd:   0x94,  // Player.clientData
        CD_isB: 0x14,  // ClientData.isBot
        GM_ap:  0x1C,  // GameManager.allPlayers
        MM_SPB: 0x10,  // MapManager.SP_BL
    };

    // ============================================================
    // 状态
    // ============================================================
    var gm=null, mm=null, spawn=null;
    var ntp=false, tn=0;
    var isNano4T=false;

    // ============================================================
    // NativeFunctions
    // ============================================================
    var isMy   =new NativeFunction(B.add(R.P_isMy),  'bool',    ['pointer','pointer']);
    var isDead =new NativeFunction(B.add(R.E_isDead),'bool',    ['pointer','pointer']);
    var getCC  =new NativeFunction(B.add(R.E_getCC), 'pointer', ['pointer','pointer']);
    var ccGetEn=new NativeFunction(B.add(R.C_getEn), 'bool',    ['pointer','pointer']);
    var ccSetEn=new NativeFunction(B.add(R.C_setEn), 'void',    ['pointer','int','pointer']);
    var gt     =new NativeFunction(B.add(R.getTrans),'pointer', ['pointer','pointer']);
    var spi    =new NativeFunction(B.add(R.setPosInj),'void',   ['pointer','pointer','pointer']);

    // 预分配缓冲区
    var vb=Memory.alloc(16); // Vector3 spawn
    var zb=Memory.alloc(16); // Vector3 zero (备用)

    function rdS(p){
        if(!p||p.isNull())return null;
        if(p.add(0xC).readU32()===0)return null;
        var e=p.add(0x10);
        return {x:e.readFloat(),y:e.add(4).readFloat(),z:e.add(8).readFloat()};
    }

    // ============================================================
    // Hook 1: GameManager.AddPlayer → 捕获 GM
    // ============================================================
    try{Interceptor.attach(B.add(R.GM_AddP),{onEnter:function(a){
        if(!gm){gm=a[0];send(JSON.stringify({t:'gm'}));L('i','GM@'+gm);}
    }});}catch(e){}

    // ============================================================
    // Hook 2: MapManager.MapGunInit → 捕获 MM + 缓存 SP_BL[0]
    // ============================================================
    try{Interceptor.attach(B.add(R.MM_MapGun),{onEnter:function(a){
        if(!mm){
            mm=a[0];
            try{spawn=rdS(mm.add(O.MM_SPB).readPointer());
                if(spawn)L('i','✓ SP_BL[0]:('+spawn.x.toFixed(1)+','+spawn.y.toFixed(1)+','+spawn.z.toFixed(1)+')');
            }catch(x){}
            send(JSON.stringify({t:'mm'}));
        }
    }});}catch(e){}

    // ============================================================
    // Hook 3: Player.Update → 主线程入口
    // ============================================================
    try{Interceptor.attach(B.add(R.P_Update),{onEnter:function(a){
        if(!ntp)return; ntp=false;
        if(!gm)return;

        // ---- 步骤0: 确认 Nano4T 模式 ----
        if(!isNano4T){
            try{
                var mode=new NativeFunction(B.add(R.ModeNano4T),'pointer',[]);
                var inst=mode();
                isNano4T=!!(inst&&!inst.isNull());
                L('i','模式检查: Nano4T='+isNano4T+' (inst='+inst+')');
            }catch(e){L('w','模式检查异常:'+e.message);isNano4T=true;}
        }

        if(!spawn)spawn={x:0,y:0,z:0};
        tn++;
        L('i','══════ 传送 #'+tn+' ══════');
        L('i','模式: Nano4T='+isNano4T);
        L('i','出生点 SP_BL[0]: ('+spawn.x.toFixed(1)+','+spawn.y.toFixed(1)+','+spawn.z.toFixed(1)+')');

        vb.writeFloat(spawn.x); vb.add(4).writeFloat(spawn.y); vb.add(8).writeFloat(spawn.z);

        // --- 读 allPlayers ---
        var ap=gm.add(O.GM_ap).readPointer();
        if(!ap||ap.isNull()){L('e','allPlayers==null');return;}
        var total=ap.add(0xC).readU32();
        L('i','allPlayers 总数: '+total);

        // ============================================================
        // 先遍历一遍，输出识别日志
        // ============================================================
        var idLog=[];
        for(var i=0;i<total;i++){
            try{
                var pp=ap.add(0x10+i*8).readPointer();
                if(!pp||pp.isNull()){idLog.push('#'+i+': null');continue;}
                var isMine=isMy(pp,ptr(0));
                if(isMine){idLog.push('#'+i+': ★ 本地玩家');continue;}
                var cd=pp.add(O.P_cd).readPointer();
                if(!cd||cd.isNull()){idLog.push('#'+i+': cd=null(可能是Player但无ClientData)');continue;}
                var bot=cd.add(O.CD_isB).readU8();
                var dead=isDead(pp,ptr(0));
                var tag='';
                if(bot&&dead)tag='Bot(已死)';
                else if(bot)tag='Bot ✓';
                else if(dead)tag='真人(已死)';
                else tag='真人';
                idLog.push('#'+i+': '+tag);
            }catch(e){idLog.push('#'+i+': 异常 '+e.message);}
        }
        for(var j=0;j<idLog.length;j++)L('i','  '+idLog[j]);

        // ============================================================
        // 传送: CC.disable → move → CC.enable
        // ============================================================
        var botC=0,deadC=0,skipC=0,okC=0,failC=0;

        for(var i=0;i<total;i++){
            try{
                var pp=ap.add(0x10+i*8).readPointer();
                if(!pp||pp.isNull()){skipC++;continue;}
                if(isMy(pp,ptr(0))){skipC++;continue;}

                var cd=pp.add(O.P_cd).readPointer();
                if(!cd||cd.isNull()){skipC++;continue;}
                if(!cd.add(O.CD_isB).readU8()){skipC++;continue;}
                if(isDead(pp,ptr(0))){deadC++;continue;}

                botC++;

                // --- 获取 CharacterController ---
                var cc=null, ccOk=false;
                try{
                    cc=getCC(pp,ptr(0));
                    if(cc&&!cc.isNull()){
                        // Step A: 禁用 CC
                        ccSetEn(cc,0,ptr(0));
                        ccOk=true;
                    }
                }catch(e){}

                // --- 移动 Transform ---
                var tr=null;
                try{tr=gt(pp,ptr(0));}catch(e){}
                if(tr&&!tr.isNull()){
                    try{spi(tr,vb,ptr(0));}catch(e){} // managed写入
                    // native 直写(双保险)
                    try{
                        var np=tr.add(0x10).readPointer();
                        if(np&&!np.isNull()){
                            np.add(0x38).writeFloat(spawn.x);
                            np.add(0x3C).writeFloat(spawn.y);
                            np.add(0x40).writeFloat(spawn.z);
                        }
                    }catch(e){}
                }

                // Step C: 重新启用 CC
                if(ccOk){
                    try{ccSetEn(cc,1,ptr(0));}catch(e){}
                }

                okC++;
            }catch(e){
                failC++;
                if(failC<=3)L('w','#'+i+' 异常:'+e.message);
            }
        }

        var msg='传送 '+okC+'/'+botC+' Bot';
        if(deadC>0)msg+=' | '+deadC+' 已死';
        if(skipC>0)msg+=' | '+skipC+' 跳过';
        L('i',msg);
        L('i','══════ 完成 ══════');
        send(JSON.stringify({t:'done',c:okC,m:msg}));
    }});}catch(e){}

    // ============================================================
    // RPC
    // ============================================================
    rpc.exports={teleport:function(){
        if(!gm){send(JSON.stringify({t:'err',m:'GM未就绪'}));return;}
        ntp=true; L('i','收到传送指令');
    }};

    L('i','========================================');
    L('i','v12 Nano4T | CC.disable→move→CC.enable');
    L('i','SP_BL[0] | 详细识别日志');
    L('i','========================================');
})();
