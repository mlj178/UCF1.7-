// ============================================================
// 诊断工具 v2: 直接扫描内存中的 Entity 对象
// 思路: 通过已知的 Player 对象特征，在内存中搜索其他 Entity
// ============================================================

(function() {
    'use strict';

    function L(l,m){var p='[Diag2] ';if(l==='e')console.error(p+m);else if(l==='w')console.warn(p+m);else console.log(p+m);}

    var mod=Process.findModuleByName('GameAssembly.dll');
    if(!mod){L('e','GameAssembly.dll未找到');return;}
    var B=mod.base;
    L('i','=============================================================');
    L('i','诊断工具 v2: 直接扫描 Entity 对象');
    L('i','=============================================================');

    // ------------------ RVA ------------------
    var R={
        GM_AddP:    0xAF9A90,
        GM_isNano:  0xAFDA80,
    };

    // ------------------ 字段偏移 ------------------
    var O={
        P_cd:0x94,
        CD_isB:0x1C,  // ClientData.isBot 在 0x1C
    };

    var gm=null;

    // ------------------ NativeFunction ------------------
    var isMy  =new NativeFunction(B.add(0xB55FD0), 'bool',   ['pointer','pointer']);

    // ------------------ Hook ------------------
    try{Interceptor.attach(B.add(R.GM_AddP),{onEnter:function(a){
        if(!gm){gm=a[0];L('i','✅ GameManager 捕获: '+gm);}
    }});}catch(e){}

    setTimeout(function(){
        if(!gm){
            try{
                var h=Interceptor.attach(B.add(R.GM_isNano),{
                    onEnter:function(a){
                        if(!gm){gm=a[0];L('i','✅ GameManager 捕获 (备用): '+gm);h.detach();}
                    }
                });
            }catch(e){}
        }
    },1500);

    // ------------------ 辅助函数 ------------------
    function rp(a,o){try{return a.add(o).readPointer();}catch(e){return null;}}

    function classifyEntity(pp){
        if(!pp||pp.isNull())return'null';
        try{
            var isSelf=false;try{isSelf=isMy(pp,ptr(0));}catch(e){}
            if(isSelf)return'SELF';
            var cdPtr=rp(pp,O.P_cd);
            if(!cdPtr||cdPtr.isNull())return'nullBOT';
            var isBot=cdPtr.add(O.CD_isB).readU8();
            if(isBot===1)return'BOT';
            if(isBot===0)return'REAL';
            return'UNK('+isBot+')';
        }catch(e){return'ERR';}
    }

    // ------------------ RPC ------------------
    rpc.exports={
        scan:function(){
            var waited=0;
            while(!gm && waited<5000){Thread.sleep(0.1);waited+=100;}
            if(!gm){L('w','GameManager未就绪');return;}

            L('i','');
            L('i','═══════════════════════════════════════════');
            L('i','🔍 开始扫描 GameManager 所有指针字段');
            L('i','GM@'+gm);
            L('i','═══════════════════════════════════════════');
            L('i','');

            // 扫描 GameManager 从 0xC 到 0x60 的所有指针
            for(var off=0xC;off<=0x60;off+=4){
                try{
                    var ptr=gm.add(off).readPointer();
                    if(!ptr||ptr.isNull())continue;

                    // 检查指针是否指向有效的游戏对象
                    // 尝试读取 vtable (第一个指针)
                    try{
                        var vtable=ptr.readPointer();
                        if(!vtable||vtable.isNull())continue;

                        // 检查 vtable 是否在 GameAssembly.dll 范围内
                        var vtableOff=vtable.sub(B);
                        if(vtableOff.compare(0)<0 || vtableOff.compare(mod.size)>0)continue;

                        // 尝试作为 Player 读取 ClientData
                        var cdPtr=rp(ptr,O.P_cd);
                        if(cdPtr && !cdPtr.isNull()){
                            try{
                                var isBot=cdPtr.add(O.CD_isB).readU8();
                                if(isBot<=1){
                                    L('i','  +0x'+off.toString(16).padStart(2,'0')+': '+ptr+' → 可能是 Player/Entity (isBot='+isBot+')');
                                }
                            }catch(e){}
                        }
                    }catch(e){}
                }catch(e){}
            }

            L('i','');
            L('i','═══════════════════════════════════════════');
            L('i','✅ 扫描完成');
            L('i','═══════════════════════════════════════════');
        }
    };

    L('i','✅ 诊断工具 v2 已加载');
    L('i','使用方法: rpc.exports.scan()');
})();
