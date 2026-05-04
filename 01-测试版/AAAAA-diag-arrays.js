// ============================================================
// 诊断工具: 对比 GameManager 所有实体数组
// 目的: 找出 allPlayers 中为 null 的 BOT 藏在哪个数组里
// ============================================================

(function() {
    'use strict';

    function L(l,m){var p='[Diag] ';if(l==='e')console.error(p+m);else if(l==='w')console.warn(p+m);else console.log(p+m);}

    var mod=Process.findModuleByName('GameAssembly.dll');
    if(!mod){L('e','GameAssembly.dll未找到');return;}
    var B=mod.base;
    L('i','=============================================================');
    L('i','诊断工具: GameManager 数组对比');
    L('i','GameAssembly.dll 基址: ' + B);
    L('i','=============================================================');

    // ------------------ RVA 地址表 ------------------
    var R={
        GM_AddP:    0xAF9A90,  // GameManager.AddPlayer
        GM_isNano:  0xAFDA80,  // GameManager.get_isNanoMode
    };

    // ------------------ GameManager 字段偏移 (基于 dump.cs) ------------------
    var GM={
        entityBL_Alive: 0x14,  // List<Entity>  保卫者存活实体
        entityGR_Alive: 0x18,  // List<Entity>  潜伏者存活实体
        allPlayers:     0x1C,  // Player[]      所有玩家数组
        playersBL:      0x20,  // List<Player>  保卫者玩家
        playersBL_Alive:0x24,  // List<Player>  保卫者存活玩家
        playersGR:      0x28,  // List<Player>  潜伏者玩家
        playersGR_Alive:0x2C,  // List<Player>  潜伏者存活玩家
    };

    // ------------------ 字段偏移 ------------------
    var O={
        P_cd:0x94,    // Player->ClientData*
        CD_isB:0x14,  // ClientData.isBot
    };

    // ------------------ 状态变量 ------------------
    var gm=null;

    // ------------------ NativeFunction ------------------
    var isMy  =new NativeFunction(B.add(0xB55FD0), 'bool',   ['pointer','pointer']);
    var isDead=new NativeFunction(B.add(0xB400E0),'bool',  ['pointer','pointer']);

    // ------------------ 辅助函数 ------------------
    function probe(p){try{p.readU8();return true;}catch(e){return false;}}
    function rp(a,o){var p=a.add(o);if(!probe(p))return null;try{return p.readPointer();}catch(e){return null;}}

    // 读取 IL2CPP List<T>
    function readList(listPtr){
        if(!listPtr||listPtr.isNull())return null;
        try{
            // IL2CPP List<T> 对象内存布局:
            // 0x0-0xF: 对象头
            // 0x10: _items (T[] 数组指针)
            // 0x18: _size
            // 0x1C: _version
            // 0x20: _syncRoot
            
            // 但 _items 指向的是 T[] 数组，需要再解引用
            var itemsArrayPtr=listPtr.add(0x10).readPointer();
            var size=listPtr.add(0x18).readU32();
            
            L('i','    [DEBUG] List@'+listPtr);
            L('i','      _items(0x10)='+itemsArrayPtr);
            L('i','      _size(0x18)='+size);
            
            // 如果 _items 为空但 size>0，尝试直接读取 _items 数组
            if(!itemsArrayPtr||itemsArrayPtr.isNull()){
                // 可能 _items 未初始化，但 List 本身有效
                // 尝试读取 _items 数组的内容
                L('i','      [DEBUG] _items 为空，尝试直接使用 listPtr+0x10 作为数组');
                // 在 IL2CPP 中，List 的 _items 可能直接内联在对象中
                return{items:listPtr.add(0x10),size:size,direct:true};
            }
            
            // _items 指向 T[] 数组，数组结构:
            // 0x0-0xF: 对象头
            // 0xC: length
            // 0x10: 第一个元素
            if(size>0 && size<=100){
                return{items:itemsArrayPtr,size:size,direct:false};
            }
            
            L('i','    [DEBUG] List 无效: size='+size);
            return null;
        }catch(e){
            L('i','    [DEBUG] List 读取异常: '+e.message);
            return null;
        }
    }

    // 读取 IL2CPP 数组 (Player[])
    function readArray(arrPtr){
        if(!arrPtr||arrPtr.isNull())return null;
        try{
            var size=arrPtr.add(0xC).readU32();
            if(size<=0||size>100)return null;
            return{items:arrPtr,size:size,elemOffset:0x10};
        }catch(e){return null;}
    }

    // 读取 ClientData 信息
    function readCD(pp){
        var cdPtr=rp(pp,O.P_cd);
        if(!cdPtr||cdPtr.isNull())return{cdNull:true,isBot:-1};
        try{
            return{cdNull:false,isBot:cdPtr.add(O.CD_isB).readU8()};
        }catch(e){return{cdNull:true,isBot:-1};}
    }

    // 分类实体
    function classifyEntity(pp,label){
        if(!pp||pp.isNull())return'null';
        try{
            var isSelf=false;try{isSelf=isMy(pp,ptr(0));}catch(e){}
            if(isSelf)return'SELF';
            var cd=readCD(pp);
            if(cd.cdNull)return'nullBOT';
            if(cd.isBot===1)return'BOT';
            if(cd.isBot===0)return'REAL';
            return'UNK('+cd.isBot+')';
        }catch(e){return'ERR';}
    }

    // 统计数组
    function countArray(name,data){
        if(!data){L('i','  '+name+': null');return{};}
        var stats={SELF:0,nullBOT:0,BOT:0,REAL:0,UNK:0,ERR:0,null:0,total:data.size};
        for(var i=0;i<data.size;i++){
            var elem;
            if(data.direct){
                // 直接模式: items 就是元素数组的起始位置
                elem=data.items.add(i*8);
            }else if(data.elemOffset!==undefined){
                // 数组模式: 需要跳过对象头
                elem=data.items.add(data.elemOffset+i*8);
            }else{
                // 默认: Il2CppArray 结构 (0x10 开始是元素)
                elem=data.items.add(0x10+i*8);
            }
            var pp;try{pp=elem.readPointer();}catch(e){pp=null;}
            var cls=classifyEntity(pp,name);
            if(cls==='null')stats.null++;
            else if(stats[cls]!==undefined)stats[cls]++;
            else stats.UNK++;
        }
        L('i','  '+name+': 总数='+stats.total+' | 自己='+stats.SELF+' | BOT='+stats.BOT+' | nullBOT='+stats.nullBOT+' | 真人='+stats.REAL+' | 空='+stats.null+' | 异常='+stats.ERR);
        return stats;
    }

    // ------------------ Hook: GameManager.AddPlayer ------------------
    try{Interceptor.attach(B.add(R.GM_AddP),{onEnter:function(a){
        if(!gm){gm=a[0];L('i','✅ GameManager 捕获: '+gm);}
    }});}catch(e){}

    // ------------------ 备用Hook: get_isNanoMode ------------------
    setTimeout(function(){
        if(!gm){
            try{
                var h=Interceptor.attach(B.add(R.GM_isNano),{
                    onEnter:function(a){
                        if(!gm){
                            gm=a[0];
                            L('i','✅ GameManager 捕获 (备用): '+gm);
                            h.detach();
                        }
                    }
                });
                L('i','✅ 备用Hook已安装');
            }catch(e){L('e','备用Hook失败: '+e.message);}
        }
    },1500);

    // ------------------ RPC 接口 ------------------
    rpc.exports={
        diagnose:function(){
            // 等待 GameManager 被捕获 (最多等 5 秒)
            var waited=0;
            while(!gm && waited<5000){
                Thread.sleep(0.1);
                waited+=100;
            }
            if(!gm){L('w','GameManager未就绪 (等待5秒超时)');return;}

            L('i','');
            L('i','═══════════════════════════════════════════');
            L('i','🔍 开始诊断 GameManager 所有数组');
            L('i','GameManager 实例: '+gm);
            L('i','═══════════════════════════════════════════');
            L('i','');

            // 读取所有数组 - 先打印原始内存
            L('i','┌─ GameManager 原始字段 (GM@'+gm+') ─');
            for(var off=0x10;off<=0x3C;off+=4){
                try{
                    var val=gm.add(off).readPointer();
                    L('i','│  +'+('0x'+off.toString(16).padStart(2,'0'))+': '+val);
                }catch(e){}
            }
            L('i','└─ 原始字段结束 ─');
            L('i','');

            var arrays={};

            // allPlayers (数组)
            var apPtr=rp(gm,GM.allPlayers);
            arrays['allPlayers']=readArray(apPtr);

            // entityBL_Alive (List)
            var eBLPtr=rp(gm,GM.entityBL_Alive);
            arrays['entityBL_Alive']=readList(eBLPtr);

            // entityGR_Alive (List)
            var eGRPtr=rp(gm,GM.entityGR_Alive);
            arrays['entityGR_Alive']=readList(eGRPtr);

            // playersBL (List)
            var pBLPtr=rp(gm,GM.playersBL);
            arrays['playersBL']=readList(pBLPtr);

            // playersBL_Alive (List)
            var pBLAPtr=rp(gm,GM.playersBL_Alive);
            arrays['playersBL_Alive']=readList(pBLAPtr);

            // playersGR (List)
            var pGRPtr=rp(gm,GM.playersGR);
            arrays['playersGR']=readList(pGRPtr);

            // playersGR_Alive (List)
            var pGRAPtr=rp(gm,GM.playersGR_Alive);
            arrays['playersGR_Alive']=readList(pGRAPtr);

            L('i','┌─ 数组统计 ─');
            var allStats=countArray('allPlayers',arrays['allPlayers']);
            var eBLStats=countArray('entityBL_Alive',arrays['entityBL_Alive']);
            var eGRStats=countArray('entityGR_Alive',arrays['entityGR_Alive']);
            var pBLStats=countArray('playersBL',arrays['playersBL']);
            var pBLAStats=countArray('playersBL_Alive',arrays['playersBL_Alive']);
            var pGRStats=countArray('playersGR',arrays['playersGR']);
            var pGRAStats=countArray('playersGR_Alive',arrays['playersGR_Alive']);
            L('i','└─ 统计完成 ─');
            L('i','');

            // 对比分析
            L('i','┌─ 对比分析 ─');
            var apTotal=allStats.total||0;
            var eBLTotal=eBLStats.total||0;
            var eGRTotal=eGRStats.total||0;
            var allEntityTotal=eBLTotal+eGRTotal;
            var apNull=allStats.null||0;
            var apBot=allStats.BOT||0;
            var apNullBot=allStats.nullBOT||0;

            L('i','│ allPlayers 总数: '+apTotal);
            L('i','│ entityBL_Alive + entityGR_Alive 总数: '+allEntityTotal);
            L('i','│ allPlayers 中 null 数量: '+apNull);
            L('i','│ allPlayers 中 BOT(isBot=1) 数量: '+apBot);
            L('i','│ allPlayers 中 nullBOT 数量: '+apNullBot);
            L('i','│');

            if(allEntityTotal>apTotal){
                L('i','│ ⚠️ entity 数组总数('+allEntityTotal+') > allPlayers总数('+apTotal+')');
                L('i','│ → 缺失的 '+(allEntityTotal-apTotal)+' 个实体在 entityBL_Alive / entityGR_Alive 中');
            }else{
                L('i','│ entity 数组总数('+allEntityTotal+') <= allPlayers总数('+apTotal+')');
            }

            L('i','│');
            L('i','│ 结论:');
            if(apNull>0){
                L('i','│   allPlayers 中有 '+apNull+' 个 null 槽位');
                L('i','│   这些 null 槽位对应的实体可能在 entityBL_Alive / entityGR_Alive 中');
            }
            if(apNullBot>0){
                L('i','│   allPlayers 中有 '+apNullBot+' 个 nullBOT (ClientData=null)');
            }
            L('i','└─ 分析完成 ─');
            L('i','');

            // 详细对比: 找出 entity 数组中有但 allPlayers 中没有的实体
            L('i','┌─ 实体指针对比 ─');
            var allPlayersSet={};
            if(arrays['allPlayers']){
                var ap=arrays['allPlayers'];
                for(var i=0;i<ap.size;i++){
                    var pp;try{pp=ap.items.add(0x10+i*8).readPointer();}catch(e){pp=null;}
                    if(pp&&!pp.isNull())allPlayersSet[pp.toString()]=true;
                }
            }

            var onlyInEntity=[];
            if(arrays['entityBL_Alive']){
                var el=arrays['entityBL_Alive'];
                for(var i=0;i<el.size;i++){
                    var pp;try{pp=el.items.add(0x10+i*8).readPointer();}catch(e){pp=null;}
                    if(pp&&!pp.isNull()&&!allPlayersSet[pp.toString()]){
                        onlyInEntity.push({ptr:pp.toString(),list:'entityBL_Alive',idx:i});
                    }
                }
            }
            if(arrays['entityGR_Alive']){
                var el=arrays['entityGR_Alive'];
                for(var i=0;i<el.size;i++){
                    var pp;try{pp=el.items.add(0x10+i*8).readPointer();}catch(e){pp=null;}
                    if(pp&&!pp.isNull()&&!allPlayersSet[pp.toString()]){
                        onlyInEntity.push({ptr:pp.toString(),list:'entityGR_Alive',idx:i});
                    }
                }
            }

            if(onlyInEntity.length>0){
                L('i','│ 找到 '+onlyInEntity.length+' 个实体只在 entity 数组中，不在 allPlayers 中:');
                for(var j=0;j<onlyInEntity.length;j++){
                    var e=onlyInEntity[j];
                    var pPtr=ptr(e.ptr);
                    var cls=classifyEntity(pPtr,e.list);
                    L('i','│   ['+j+'] '+e.list+'['+e.idx+'] ptr='+e.ptr+' 类型='+cls);
                }
            }else{
                L('i','│ 所有 entity 数组中的实体都在 allPlayers 中');
            }
            L('i','└─ 对比完成 ─');

            L('i','');
            L('i','═══════════════════════════════════════════');
            L('i','✅ 诊断完成');
            L('i','═══════════════════════════════════════════');

            // 额外诊断: 检查 allPlayers 中 null 槽位的原始内存
            L('i','');
            L('i','┌─ allPlayers null 槽位详细检查 ─');
            if(arrays['allPlayers']){
                var ap=arrays['allPlayers'];
                for(var i=0;i<ap.size;i++){
                    var slotPtr=ap.items.add(0x10+i*8);
                    var pp;try{pp=slotPtr.readPointer();}catch(e){pp=null;}
                    if(!pp||pp.isNull()){
                        // 读取槽位本身的内存 (可能是被释放的指针)
                        try{
                            var raw=slotPtr.readU64();
                            L('i','│  #'+i+': null (槽位原始值: 0x'+raw.toString(16)+')');
                        }catch(e){
                            L('i','│  #'+i+': null (无法读取)');
                        }
                    }
                }
            }
            L('i','└─ 检查完成 ─');
        }
    };

    L('i','');
    L('i','=============================================================');
    L('i','✅ 诊断工具已加载');
    L('i','=============================================================');
    L('i','使用方法:');
    L('i','  1. 进入游戏房间');
    L('i','  2. 调用: rpc.exports.diagnose()');
    L('i','  3. 查看日志对比结果');
    L('i','=============================================================');
})();
