// ============================================================
// 诊断工具 v3: 深度扫描 GameManager 所有字段
// 目的: 找出所有包含 Entity/Player 的数组/List
// ============================================================

(function() {
    'use strict';

    function L(l,m){var p='[Diag3] ';if(l==='e')console.error(p+m);else if(l==='w')console.warn(p+m);else console.log(p+m);}

    var mod=Process.findModuleByName('GameAssembly.dll');
    if(!mod){L('e','GameAssembly.dll未找到');return;}
    var B=mod.base;
    L('i','=============================================================');
    L('i','诊断工具 v3: 深度扫描 GameManager');
    L('i','=============================================================');

    var R={GM_AddP:0xAF9A90, GM_isNano:0xAFDA80};
    var O={P_cd:0x94, CD_isB:0x1C};
    var gm=null;
    var isMy=new NativeFunction(B.add(0xB55FD0),'bool',['pointer','pointer']);

    try{Interceptor.attach(B.add(R.GM_AddP),{onEnter:function(a){if(!gm){gm=a[0];L('i','✅ GM: '+gm);}}});}catch(e){}
    setTimeout(function(){
        if(!gm){
            try{
                var h=Interceptor.attach(B.add(R.GM_isNano),{onEnter:function(a){if(!gm){gm=a[0];L('i','✅ GM(备用): '+gm);h.detach();}}});
            }catch(e){}
        }
    },1500);

    function rp(a,o){try{return a.add(o).readPointer();}catch(e){return null;}}
    function probe(p){try{p.readU8();return true;}catch(e){return false;}}
    function inRange(p){if(!p||p.isNull())return false;var o=p.sub(B);return o.compare(0)>=0&&o.compare(mod.size)<0;}

    // 读取 IL2CPP 数组
    function readIl2cppArray(arrPtr){
        if(!arrPtr||arrPtr.isNull())return null;
        try{
            var len=arrPtr.add(0xC).readU32();
            if(len<=0||len>200)return null;
            return{ptr:arrPtr,len:len,elemOff:0x10};
        }catch(e){return null;}
    }

    // 读取 IL2CPP List<T>
    function readIl2cppList(listPtr){
        if(!listPtr||listPtr.isNull())return null;
        try{
            var itemsPtr=listPtr.add(0x10).readPointer();
            var size=listPtr.add(0x18).readU32();
            if(size<=0||size>200)return null;
            if(!itemsPtr||itemsPtr.isNull())return null;
            return{ptr:itemsPtr,len:size,elemOff:0x10};
        }catch(e){return null;}
    }

    // 检查指针是否是 Player/Entity 对象
    function checkEntity(ptr,label){
        if(!ptr||ptr.isNull())return null;
        if(!inRange(ptr))return null;
        try{
            var vtable=ptr.readPointer();
            if(!inRange(vtable))return null;
            var cdPtr=rp(ptr,O.P_cd);
            if(!cdPtr||cdPtr.isNull())return{type:'Entity(no CD)',ptr:ptr};
            var isBot=cdPtr.add(O.CD_isB).readU8();
            if(isBot>1)return null;
            var isSelf=false;try{isSelf=isMy(ptr,ptr(0));}catch(e){}
            return{type:isSelf?'SELF':(isBot===1?'BOT':'REAL'),ptr:ptr};
        }catch(e){return null;}
    }

    rpc.exports={
        deepscan:function(){
            var waited=0;
            while(!gm&&waited<5000){Thread.sleep(0.1);waited+=100;}
            if(!gm){L('w','GM未就绪');return;}

            L('i','');
            L('i','═══════════════════════════════════════════');
            L('i','🔍 深度扫描 GM@'+gm);
            L('i','═══════════════════════════════════════════');
            L('i','');

            // 重点检查 entityBL_Alive 和 entityGR_Alive
            var targets=[
                {off:0x14,name:'entityBL_Alive'},
                {off:0x18,name:'entityGR_Alive'},
                {off:0x1c,name:'allPlayers'},
            ];

            targets.forEach(function(t){
                try{
                    var ptr=gm.add(t.off).readPointer();
                    if(!ptr||ptr.isNull()){
                        L('i','');
                        L('i','┌─ '+t.name+' (+'+('0x'+t.off.toString(16).padStart(2,'0'))+') ─');
                        L('i','│ null');
                        L('i','└─ ─');
                        return;
                    }

                    // 先尝试作为数组读取
                    var arr=readIl2cppArray(ptr);
                    if(arr){
                        L('i','');
                        L('i','┌─ '+t.name+' (+'+('0x'+t.off.toString(16).padStart(2,'0'))+') ─');
                        L('i','│ 数组@'+ptr+' 长度='+arr.len);

                        var selfC=0,botC=0,realC=0,nullC=0;
                        for(var i=0;i<arr.len;i++){
                            var ep;try{ep=arr.ptr.add(arr.elemOff+i*8).readPointer();}catch(e){ep=null;}
                            if(!ep||ep.isNull()){
                                nullC++;
                                L('i','│  #'+i+': null');
                                continue;
                            }
                            var e=checkEntity(ep,'');
                            if(e){
                                if(e.type==='SELF'){selfC++;L('i','│  #'+i+': ★自己');}
                                else if(e.type==='BOT'){botC++;L('i','│  #'+i+': BOT');}
                                else if(e.type==='REAL'){realC++;L('i','│  #'+i+': 真人');}
                                else{L('i','│  #'+i+': '+e.type+' @'+e.ptr);}
                            }else{
                                L('i','│  #'+i+': 无效实体 @'+ep);
                            }
                        }
                        L('i','│ 统计: 总数='+arr.len+' | 自己='+selfC+' | BOT='+botC+' | 真人='+realC+' | null='+nullC);
                        L('i','└─ ─');
                        return;
                    }

                    // 尝试作为 List 读取 (List 的 _items 在 0x10, _size 在 0x18)
                    var itemsPtr;try{itemsPtr=ptr.add(0x10).readPointer();}catch(e){itemsPtr=null;}
                    var size;try{size=ptr.add(0x18).readU32();}catch(e){size=0;}
                    L('i','');
                    L('i','┌─ '+t.name+' (+'+('0x'+t.off.toString(16).padStart(2,'0'))+') ─');
                    L('i','│ List@'+ptr);
                    L('i','│   _items(0x10)='+itemsPtr);
                    L('i','│   _size(0x18)='+size);

                    if(!itemsPtr||itemsPtr.isNull()||size<=0||size>200){
                        L('i','│   List 无效');
                        L('i','└─ ─');
                        return;
                    }

                    var selfC=0,botC=0,realC=0,nullC=0;
                    for(var i=0;i<size;i++){
                        var ep;try{ep=itemsPtr.add(0x10+i*8).readPointer();}catch(e){ep=null;}
                        if(!ep||ep.isNull()){
                            nullC++;
                            L('i','│  #'+i+': null');
                            continue;
                        }
                        var e=checkEntity(ep,'');
                        if(e){
                            if(e.type==='SELF'){selfC++;L('i','│  #'+i+': ★自己');}
                            else if(e.type==='BOT'){botC++;L('i','│  #'+i+': BOT');}
                            else if(e.type==='REAL'){realC++;L('i','│  #'+i+': 真人');}
                            else{L('i','│  #'+i+': '+e.type+' @'+e.ptr);}
                        }else{
                            L('i','│  #'+i+': 无效实体 @'+ep);
                        }
                    }
                    L('i','│ 统计: 总数='+size+' | 自己='+selfC+' | BOT='+botC+' | 真人='+realC+' | null='+nullC);
                    L('i','└─ ─');
                }catch(e){
                    L('e','┌─ '+t.name+' 异常: '+e.message);
                    L('e','└─ ─');
                }
            });

            L('i','');
            L('i','═══════════════════════════════════════════');
            L('i','✅ 扫描完成');
            L('i','═══════════════════════════════════════════');
        }
    };

    L('i','✅ 已加载, 调用 rpc.exports.deepscan()');
})();
