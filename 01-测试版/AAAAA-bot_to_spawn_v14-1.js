// ============================================================
// Bot 出生点集合器 v14-1 — null BOT 支持 + 简化传送
// 优化: ClientData=null 的 BOT 也能传送
// BOT判定: 排除自己 + 排除真人(isBot==0) → 其余全部当BOT
// 传送: 直接 get_transform → set_position_Injected
// 不需要 CC.disable/enable
// ============================================================

(function() {
    'use strict';

    function L(l,m){var p='[BotSpawn-v14-1] ';if(l==='e')console.error(p+m);else if(l==='w')console.warn(p+m);else console.log(p+m);}

    var mod=Process.findModuleByName('GameAssembly.dll');
    if(!mod){L('e','GameAssembly.dll未找到');return;}
    var B=mod.base;
    L('i','=============================================================');
    L('i','Bot出生点集合器 v14-1 已加载');
    L('i','GameAssembly.dll 基址: ' + B);
    L('i','=============================================================');

    // ------------------ RVA 地址表 ------------------
    var R={
        GM_AddP:    0xAF9A90,  // GameManager.AddPlayer - 主Hook
        GM_AddPs:   0xAF9DE0,  // GameManager.AddPlayers - 备用Hook1
        GM_isNano:  0xAFDA80,  // GameManager.get_isNanoMode - 备用Hook2(每帧调用)
        MM_MapGun:  0xAEBB70,  // MapManager.MapGunInit - 捕获MapManager+出生点
        P_Update:   0xB551D0,  // Player.Update - 执行入口
        P_isMy:     0xB55FD0,  // Player.get_isMyPlayer - 判断是否自己
        E_isDead:   0xB400E0,  // Entity.get_isDead - 判断是否死亡
        getTrans:   0x32CF40,  // Component.get_transform - 获取Transform
        setPosInj:  0x3F4810,  // Transform.set_position_Injected - 设置位置
    };

    // ------------------ 字段偏移 ------------------
    var O={
        P_cd:0x94,    // Player->ClientData*
        CD_isB:0x14,  // ClientData.isBot (1=BOT, 0=真人)
        GM_ap:0x1C,   // GameManager.allPlayers (Player[]*)
        MM_SPG:0x14,  // MapManager.SP_GR (潜伏者出生点)
        MM_SPB:0x10,  // MapManager.SP_BL (保卫者出生点)
        MM_SPN:0x18,  // MapManager.SP_Netural (中立出生点)
    };

    // ------------------ 状态变量 ------------------
    var gm=null, mm=null, spawn=null, ntp=false, tn=0;

    // ------------------ NativeFunction ------------------
    var isMy  =new NativeFunction(B.add(R.P_isMy), 'bool',   ['pointer','pointer']);
    var isDead=new NativeFunction(B.add(R.E_isDead),'bool',  ['pointer','pointer']);
    var gt    =new NativeFunction(B.add(R.getTrans),'pointer',['pointer','pointer']);
    var spi   =new NativeFunction(B.add(R.setPosInj),'void', ['pointer','pointer','pointer']);
    var vb    =Memory.alloc(16);

    L('i','✓ NativeFunction: Player.get_isMyPlayer');
    L('i','✓ NativeFunction: Entity.get_isDead');
    L('i','✓ NativeFunction: Component.get_transform');
    L('i','✓ NativeFunction: Transform.set_position_Injected');

    // ------------------ 辅助函数: 读取出生点 ------------------
    function rdS(p){
        if(!p||p.isNull())return null;
        try{if(p.add(0xC).readU32()===0)return null;}catch(e){return null;}
        try{var e=p.add(0x10);return {x:e.readFloat(),y:e.add(4).readFloat(),z:e.add(8).readFloat()};}catch(e2){return null;}
    }

    // ------------------ Hook: GameManager.AddPlayer ------------------
    L('i','━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    L('i','安装 GameManager.AddPlayer Hook');
    L('i','  RVA: ' + ptr(R.GM_AddP));
    L('i','━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

    try{Interceptor.attach(B.add(R.GM_AddP),{onEnter:function(a){
        if(!gm){
            gm=a[0];
            L('i','✅ GameManager 捕获 (AddPlayer) - 实例: ' + gm);
            send(JSON.stringify({t:'gm',addr:gm.toString(),method:'AddPlayer'}));
        }
    }});}catch(e){L('e','GameManager.AddPlayer Hook 失败: '+e.message);}

    // ------------------ 备用Hook1: GameManager.AddPlayers ------------------
    var gmBackup1Installed=false;
    setTimeout(function(){
        if(!gm && !gmBackup1Installed){
            L('i','⏳ AddPlayer未触发，安装备用Hook1 (AddPlayers)...');
            try{
                Interceptor.attach(B.add(R.GM_AddPs),{onEnter:function(a){
                    if(!gm){
                        gm=a[0];
                        L('i','✅ GameManager 捕获 (备用AddPlayers) - 实例: ' + gm);
                        send(JSON.stringify({t:'gm',addr:gm.toString(),method:'AddPlayers'}));
                    }
                }});
                gmBackup1Installed=true;
                L('i','✅ 备用Hook1已安装');
            }catch(e){L('e','备用Hook1安装失败: '+e.message);}
        }
    },1000);

    // ------------------ 备用Hook2: GameManager.get_isNanoMode (高频调用，捕获后立即解除) ------------------
    var gmBackup2Installed=false;
    var gmBackup2Hook=null;
    setTimeout(function(){
        if(!gm && !gmBackup2Installed){
            L('i','⏳ 前两个Hook都未捕获，安装备用Hook2 (get_isNanoMode - 每帧调用)...');
            try{
                gmBackup2Hook=Interceptor.attach(B.add(R.GM_isNano),{
                    onEnter:function(a){
                        if(!gm){
                            gm=a[0];
                            L('i','✅ GameManager 捕获 (备用get_isNanoMode) - 实例: ' + gm);
                            send(JSON.stringify({t:'gm',addr:gm.toString(),method:'get_isNanoMode'}));
                            // 捕获后立即解除Hook，不影响性能
                            if(gmBackup2Hook){gmBackup2Hook.detach();gmBackup2Hook=null;}
                            L('i','   备用Hook2已解除');
                        }
                    }
                });
                gmBackup2Installed=true;
                L('i','✅ 备用Hook2已安装 (get_isNanoMode)，等待捕获...');
            }catch(e){L('e','备用Hook2安装失败: '+e.message);}
        }
    },2000);

    // ------------------ Hook: MapManager.MapGunInit ------------------
    L('i','━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    L('i','安装 MapManager.MapGunInit Hook');
    L('i','  RVA: ' + ptr(R.MM_MapGun));
    L('i','━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

    try{Interceptor.attach(B.add(R.MM_MapGun),{onEnter:function(a){
        if(!mm){
            mm=a[0];
            L('i','✅ MapManager 捕获 - 实例: ' + mm);

            // 读取全部出生点
            var sN=rdS(mm.add(O.MM_SPN).readPointer());
            var sB=rdS(mm.add(O.MM_SPB).readPointer());
            var sG=rdS(mm.add(O.MM_SPG).readPointer());

            L('i','   ┌─ 出生点列表 ─');
            if(sN)L('i','   │ SP_Netural: ('+sN.x.toFixed(1)+','+sN.y.toFixed(1)+','+sN.z.toFixed(1)+')');
            else   L('i','   │ SP_Netural: (空)');
            if(sB)L('i','   │ SP_BL(保卫者): ('+sB.x.toFixed(1)+','+sB.y.toFixed(1)+','+sB.z.toFixed(1)+')');
            else   L('i','   │ SP_BL(保卫者): (空)');
            if(sG)L('i','   │ SP_GR(潜伏者): ('+sG.x.toFixed(1)+','+sG.y.toFixed(1)+','+sG.z.toFixed(1)+')');
            else   L('i','   │ SP_GR(潜伏者): (空)');
            L('i','   └─ 读取完成 ─');

            // 佣兵出生点 = SP_GR(潜伏者) 优先，其次 SP_BL(保卫者)
            spawn = sG || sB;
            L('i','   → 选中目标: '+(sG?'SP_GR(潜伏者)':sB?'SP_BL(保卫者)':'无'));
            send(JSON.stringify({t:'mm',addr:mm.toString()}));
        }
    }});}catch(e){L('e','MapManager.MapGunInit Hook 失败: '+e.message);}

    // ------------------ Hook: Player.Update (执行传送) ------------------
    L('i','━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    L('i','安装 Player.Update Hook (执行入口)');
    L('i','  RVA: ' + ptr(R.P_Update));
    L('i','━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

    try{Interceptor.attach(B.add(R.P_Update),{onEnter:function(a){
        if(!ntp)return;
        ntp=false;

        if(!gm||!mm){
            L('w','GameManager/MapManager 未就绪，忽略传送请求');
            send(JSON.stringify({t:'err',msg:'实例未就绪'}));
            return;
        }
        if(!spawn){
            spawn={x:0,y:0,z:0};
            L('w','出生点为空，使用默认坐标 (0,0,0)');
        }

        tn++;
        L('i','═══════════════════════════════════════');
        L('i','🚀 传送执行 #'+tn);
        L('i','📍 目标出生点: ('+spawn.x.toFixed(1)+','+spawn.y.toFixed(1)+','+spawn.z.toFixed(1)+')');
        L('i','═══════════════════════════════════════');

        // 写入目标坐标到缓冲区
        vb.writeFloat(spawn.x);
        vb.add(4).writeFloat(spawn.y);
        vb.add(8).writeFloat(spawn.z);

        // 读取 allPlayers 数组
        var ap;
        try{ap=gm.add(O.GM_ap).readPointer();}catch(e){L('e','读取allPlayers失败: '+e.message);return;}
        if(!ap||ap.isNull()){L('e','allPlayers==null');return;}
        var total=ap.add(0xC).readU32();
        L('i','📋 allPlayers 数组长度: ' + total);
        L('i','');

        // ============================================================
        // 全面输出 allPlayers 数组信息 (精简版，避免卡死)
        // ============================================================
        var summaryLines=[];
        var nullBotCount=0, isBotCount=0, realCount=0, selfCount=0, deadCount=0;

        for(var i=0;i<total;i++){
            try{
                var pp;
                try{pp=ap.add(0x10+i*8).readPointer();}catch(e){pp=null;}
                if(!pp||pp.isNull()){continue;}

                var isSelf=false;
                try{isSelf=isMy(pp,ptr(0));}catch(e){}

                var cd;
                try{cd=pp.add(O.P_cd).readPointer();}catch(e){cd=null;}

                var isBotVal=-1;
                if(cd&&!cd.isNull()){
                    try{isBotVal=cd.add(O.CD_isB).readU8();}catch(e){}
                }

                var dead=false;
                try{dead=isDead(pp,ptr(0));}catch(e){}

                var typeStr='';
                if(isSelf){typeStr='SELF';selfCount++;}
                else if(!cd||cd.isNull()){typeStr='nullBOT';nullBotCount++;}
                else if(isBotVal===1){typeStr='BOT';isBotCount++;}
                else if(isBotVal===0){typeStr='REAL';realCount++;}
                else{typeStr='UNK';}

                if(dead)deadCount++;

                summaryLines.push('['+i+']'+typeStr+(dead?'[死]':''));
            }catch(e){}
        }

        L('i','📊 allPlayers统计: 总数='+total+' | 自己='+selfCount+' | BOT(isBot)='+isBotCount+' | nullBOT='+nullBotCount+' | 真人='+realCount+' | 死亡='+deadCount);
        L('i','📋 详情: '+summaryLines.join(' '));
        L('i','');

        var botCount=0, deadSkip=0, realSkip=0, selfSkip=0, okCount=0, failCount=0;
        var rows=[];

        for(var i=0;i<total;i++){
            try{
                // 安全读取 Player 指针
                var pp;
                try{pp=ap.add(0x10+i*8).readPointer();}catch(e){pp=null;}
                if(!pp||pp.isNull()){rows.push('['+i+'] null → skip');realSkip++;continue;}

                // 1. 跳过自己
                if(isMy(pp,ptr(0))){
                    rows.push('['+i+'] ⭐自己 → skip');
                    selfSkip++;
                    continue;
                }

                // 2. 读取 ClientData
                var cd;
                try{cd=pp.add(O.P_cd).readPointer();}catch(e){cd=null;}

                // 3. BOT 判定逻辑 (核心优化)
                var isBot=false;
                var botType='';

                if(!cd||cd.isNull()){
                    // ClientData 为 null → BOT (未初始化 ClientData 的 BOT)
                    isBot=true;
                    botType='null BOT';
                } else {
                    // ClientData 存在，读取 isBot 字段
                    var b;
                    try{b=cd.add(O.CD_isB).readU8();}catch(e){b=0;}

                    if(b===1){
                        isBot=true;
                        botType='isBot=1';
                    } else {
                        // isBot==0 → 真人玩家，跳过
                        rows.push('['+i+'] 👤真人(isBot=0) → skip');
                        realSkip++;
                        continue;
                    }
                }

                // 4. 死亡检查 (对所有 BOT 执行)
                var d;
                try{d=isDead(pp,ptr(0));}catch(e){d=true;}
                if(d){
                    rows.push('['+i+'] 🤖['+botType+'] 已死 → skip');
                    deadSkip++;
                    continue;
                }

                botCount++;

                // 5. 传送 BOT (无论 ClientData 是否存在)
                var trT='-';

                // Step1: get_transform
                try{
                    var tr=gt(pp,ptr(0));
                    if(tr&&!tr.isNull()){
                        // Step2: set_position_Injected
                        try{
                            spi(tr,vb,ptr(0));
                            trT='√';
                        }catch(e2){trT='setErr:'+e2.message;}
                    } else {trT='tr=null';}
                }catch(e){trT='getErr:'+e.message;}

                if(trT==='√'){
                    okCount++;
                    rows.push('['+i+'] 🤖['+botType+'] ✅ OK');
                } else {
                    failCount++;
                    rows.push('['+i+'] 🤖['+botType+'] ❌ '+trT);
                }

            }catch(e){
                rows.push('['+i+'] ★异常: '+e.message);
                failCount++;
            }
        }

        // 印刷所有结果
        L('i','┌─ 传送详情 ─');
        for(var j=0;j<rows.length;j++)L('i','│ '+rows[j]);
        L('i','└─ 详情结束 ─');
        L('i','');

        var msg='📊 传送结果: 成功='+okCount+'/'+botCount+' Bot';
        if(deadSkip>0)msg+=' | 死亡跳过='+deadSkip;
        if(realSkip>0)msg+=' | 真人跳过='+realSkip;
        if(selfSkip>0)msg+=' | 自己跳过='+selfSkip;
        if(failCount>0)msg+=' | 失败='+failCount;

        L('i',msg);
        L('i','═══════════════════════════════════════');
        send(JSON.stringify({t:'done',ok:okCount,bot:botCount,dead:deadSkip,skip:realSkip+selfSkip,fail:failCount,msg:msg}));
    }});}catch(e){L('e','Player.Update Hook 失败: '+e.message);}

    // ------------------ RPC 接口 ------------------
    rpc.exports={
        teleport:function(){
            if(!gm){
                L('w','GameManager 尚未就绪，请先进入房间');
                send(JSON.stringify({t:'err',msg:'GM未就绪'}));
                return;
            }
            if(!mm){
                L('w','MapManager 尚未就绪，请等待地图加载');
                send(JSON.stringify({t:'err',msg:'地图未加载'}));
                return;
            }
            ntp=true;
            L('i','📡 传送指令已接收，将在下一帧执行...');
        },
        getStatus:function(){
            return JSON.stringify({
                gm:gm!==null,
                mm:mm!==null,
                spawn:spawn?{x:spawn.x,y:spawn.y,z:spawn.z}:null
            });
        }
    };

    L('i','');
    L('i','=============================================================');
    L('i','✅ v14-1 加载完成');
    L('i','=============================================================');
    L('i','📋 功能说明:');
    L('i','   1. 识别所有BOT (包括 ClientData=null 的 null BOT)');
    L('i','   2. 跳过真人玩家和自己');
    L('i','   3. 跳过死亡的 BOT');
    L('i','   4. 传送到佣兵出生点 (SP_GR 优先)');
    L('i','   5. 不需要 CC.disable/enable');
    L('i','');
    L('i','🎮 使用方法:');
    L('i','   1. 进入多人生化模式房间');
    L('i','   2. 等待地图加载完成');
    L('i','   3. 点击 "传送BOT" 按钮');
    L('i','   4. 查看日志确认传送结果');
    L('i','=============================================================');
})();
