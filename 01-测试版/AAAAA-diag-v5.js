// ============================================================
// 诊断工具 v5: 直接检查 allPlayers 中的元素
// ============================================================

(function() {
    'use strict';

    function L(l,m){var p='[Diag5] ';if(l==='e')console.error(p+m);else if(l==='w')console.warn(p+m);else console.log(p+m);}

    var mod=Process.findModuleByName('GameAssembly.dll');
    if(!mod){L('e','GameAssembly.dll未找到');return;}
    var B=mod.base;
    L('i','=============================================================');
    L('i','诊断工具 v5: 检查 allPlayers 元素');
    L('i','=============================================================');

    var R={GM_AddP:0xAF9A90, GM_isNano:0xAFDA80};
    var O={P_cd:0x94, CD_isB:0x1C};
    var gm=null;
    var isMy=new NativeFunction(B.add(0xB55FD0),'bool',['pointer','pointer']);
    var isDead=new NativeFunction(B.add(0xB400E0),'bool',['pointer','pointer']);

    try{Interceptor.attach(B.add(R.GM_AddP),{onEnter:function(a){if(!gm){gm=a[0];L('i','✅ GM: '+gm);}}});}catch(e){}
    setTimeout(function(){
        if(!gm){
            try{
                var h=Interceptor.attach(B.add(R.GM_isNano),{onEnter:function(a){if(!gm){gm=a[0];L('i','✅ GM(备用): '+gm);h.detach();}}});
            }catch(e){}
        }
    },1500);

    function rp(a,o){try{return a.add(o).readPointer();}catch(e){return null;}}
    function inRange(p){if(!p||p.isNull())return false;var o=p.sub(B);return o.compare(0)>=0&&o.compare(mod.size)<0;}

    rpc.exports={
        check:function(){
            var waited=0;
            while(!gm&&waited<5000){Thread.sleep(0.1);waited+=100;}
            if(!gm){L('w','GM未就绪');return;}

            var allP=gm.add(0x1C).readPointer();
            L('i','');
            L('i','═══════════════════════════════════════════');
            L('i','🔍 allPlayers@'+allP);
            L('i','═══════════════════════════════════════════');

            var arrLen=allP.add(0xC).readU32();
            L('i','数组长度: '+arrLen);
            L('i','');

            for(var i=0;i<arrLen;i++){
                var ep;try{ep=allP.add(0x10+i*8).readPointer();}catch(e){ep=null;}
                if(!ep||ep.isNull()){
                    L('i','  #'+i+': null');
                    continue;
                }

                // 读取原始内存
                try{
                    var vtable=ep.readPointer();
                    var vtableOff=vtable.sub(B);
                    var inGame=inRange(vtable);

                    // 尝试读取 ClientData
                    var cdPtr=rp(ep,O.P_cd);
                    var cdValid=cdPtr&&!cdPtr.isNull()&&inRange(cdPtr);
                    var isBot='N/A';
                    if(cdValid){
                        try{isBot=cdPtr.add(O.CD_isB).readU8();}catch(e){isBot='ERR';}
                    }

                    // 尝试 isMyPlayer
                    var isSelf='N/A';
                    try{isSelf=isMy(ep,ptr(0));}catch(e){isSelf='ERR';}

                    // 尝试 isDead
                    var dead='N/A';
                    try{dead=isDead(ep,ptr(0));}catch(e){dead='ERR';}

                    L('i','  #'+i+': @'+ep+' | vtable='+vtable+' (off=0x'+vtableOff.toString(16)+', inGame='+inGame+') | CD='+(cdValid?'OK':'null')+' | isBot='+isBot+' | isMy='+isSelf+' | isDead='+dead);
                }catch(e){
                    L('i','  #'+i+': @'+ep+' | 异常: '+e.message);
                }
            }

            L('i','');
            L('i','═══════════════════════════════════════════');
            L('i','✅ 检查完成');
            L('i','═══════════════════════════════════════════');
        }
    };

    L('i','✅ 已加载, 调用 rpc.exports.check()');
})();
