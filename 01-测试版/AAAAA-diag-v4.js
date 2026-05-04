// ============================================================
// 诊断工具 v4: 验证 GameManager 实例并读取 List<Entity>
// ============================================================

(function() {
    'use strict';

    function L(l,m){var p='[Diag4] ';if(l==='e')console.error(p+m);else if(l==='w')console.warn(p+m);else console.log(p+m);}

    var mod=Process.findModuleByName('GameAssembly.dll');
    if(!mod){L('e','GameAssembly.dll未找到');return;}
    var B=mod.base;
    L('i','=============================================================');
    L('i','诊断工具 v4: 验证 GameManager + 读取 List<Entity>');
    L('i','=============================================================');

    var R={GM_AddP:0xAF9A90, GM_isNano:0xAFDA80, GM_Awake:0xAFB2B0};
    var O={P_cd:0x94, CD_isB:0x1C};
    var gm=null;
    var isMy=new NativeFunction(B.add(0xB55FD0),'bool',['pointer','pointer']);
    var isDead=new NativeFunction(B.add(0xB400E0),'bool',['pointer','pointer']);

    // Hook AddPlayer 捕获 gm
    try{Interceptor.attach(B.add(R.GM_AddP),{onEnter:function(a){
        if(!gm){gm=a[0];L('i','✅ GM 捕获 (AddPlayer): '+gm);}
    }});}catch(e){}

    // 备用 Hook
    setTimeout(function(){
        if(!gm){
            try{
                var h=Interceptor.attach(B.add(R.GM_isNano),{onEnter:function(a){
                    if(!gm){gm=a[0];L('i','✅ GM 捕获 (备用): '+gm);h.detach();}
                }});
            }catch(e){}
        }
    },1500);

    function rp(a,o){try{return a.add(o).readPointer();}catch(e){return null;}}
    function inRange(p){if(!p||p.isNull())return false;var o=p.sub(B);return o.compare(0)>=0&&o.compare(mod.size)<0;}

    // 读取 IL2CPP List<T>
    // List 结构: 0x0-0xF 对象头, 0x10 _items(T[]), 0x18 _size
    // T[] 结构: 0x0-0xF 对象头, 0xC length, 0x10 第一个元素
    function readList(listPtr){
        if(!listPtr||listPtr.isNull())return null;
        try{
            var itemsPtr=listPtr.add(0x10).readPointer();
            var size=listPtr.add(0x18).readU32();
            if(!itemsPtr||itemsPtr.isNull()||size<=0||size>200)return null;
            // itemsPtr 指向 T[] 数组，元素从 0x10 开始
            return{items:itemsPtr,size:size};
        }catch(e){return null;}
    }

    // 检查是否是有效的 Entity
    function checkEntity(ptr){
        if(!ptr||ptr.isNull())return null;
        if(!inRange(ptr))return null;
        try{
            // 读取 vtable
            var vtable=ptr.readPointer();
            if(!inRange(vtable))return null;
            return{ptr:ptr,valid:true};
        }catch(e){return null;}
    }

    // 检查是否是 Player (有 ClientData)
    function checkPlayer(ptr){
        if(!ptr||ptr.isNull())return null;
        if(!inRange(ptr))return null;
        try{
            var vtable=ptr.readPointer();
            if(!inRange(vtable))return null;
            var cdPtr=rp(ptr,O.P_cd);
            if(!cdPtr||cdPtr.isNull())return{type:'nullBOT',ptr:ptr};
            var isBot=cdPtr.add(O.CD_isB).readU8();
            if(isBot>1)return null;
            var isSelf=false;try{isSelf=isMy(ptr,ptr(0));}catch(e){}
            return{type:isSelf?'SELF':(isBot===1?'BOT':'REAL'),ptr:ptr};
        }catch(e){return null;}
    }

    rpc.exports={
        verify:function(){
            var waited=0;
            while(!gm&&waited<5000){Thread.sleep(0.1);waited+=100;}
            if(!gm){L('w','GM未就绪');return;}

            L('i','');
            L('i','═══════════════════════════════════════════');
            L('i','🔍 验证 GM@'+gm);
            L('i','═══════════════════════════════════════════');

            // 验证: 读取 +0x1C (allPlayers) 看是否是 Player[]
            var allP=gm.add(0x1C).readPointer();
            L('i','');
            L('i','┌─ allPlayers (+0x1C) ─');
            L('i','│ 指针: '+allP);
            if(allP&&!allP.isNull()){
                var arrLen=allP.add(0xC).readU32();
                L('i','│ 数组长度: '+arrLen);
                if(arrLen>0&&arrLen<=100){
                    for(var i=0;i<Math.min(arrLen,5);i++){
                        var ep=allP.add(0x10+i*8).readPointer();
                        var p=checkPlayer(ep);
                        if(p){
                            L('i','│  #'+i+': '+p.type+' @'+p.ptr);
                        }else{
                            L('i','│  #'+i+': '+(ep?'无效':'null'));
                        }
                    }
                }
            }
            L('i','└─ ─');

            // 读取 +0x14 (entityBL_Alive List<Entity>)
            var eBL=gm.add(0x14).readPointer();
            L('i','');
            L('i','┌─ entityBL_Alive (+0x14) ─');
            L('i','│ 指针: '+eBL);
            if(eBL&&!eBL.isNull()){
                var list=readList(eBL);
                if(list){
                    L('i','│ List 有效: _items='+list.items+' _size='+list.size);
                    for(var i=0;i<Math.min(list.size,30);i++){
                        var ep=list.items.add(0x10+i*8).readPointer();
                        var e=checkEntity(ep);
                        if(e){
                            // 尝试作为 Player 检查
                            var p=checkPlayer(ep);
                            if(p){
                                L('i','│  #'+i+': Player('+p.type+') @'+p.ptr);
                            }else{
                                L('i','│  #'+i+': Entity @'+e.ptr);
                            }
                        }else{
                            L('i','│  #'+i+': '+(ep?'无效':'null'));
                        }
                    }
                }else{
                    L('i','│ List 无效');
                    // 尝试直接读取
                    var itemsPtr=eBL.add(0x10).readPointer();
                    var size=eBL.add(0x18).readU32();
                    L('i','│   _items='+itemsPtr+' _size='+size);
                }
            }
            L('i','└─ ─');

            // 读取 +0x18 (entityGR_Alive List<Entity>)
            var eGR=gm.add(0x18).readPointer();
            L('i','');
            L('i','┌─ entityGR_Alive (+0x18) ─');
            L('i','│ 指针: '+eGR);
            if(eGR&&!eGR.isNull()){
                var list=readList(eGR);
                if(list){
                    L('i','│ List 有效: _items='+list.items+' _size='+list.size);
                    for(var i=0;i<Math.min(list.size,30);i++){
                        var ep=list.items.add(0x10+i*8).readPointer();
                        var e=checkEntity(ep);
                        if(e){
                            var p=checkPlayer(ep);
                            if(p){
                                L('i','│  #'+i+': Player('+p.type+') @'+p.ptr);
                            }else{
                                L('i','│  #'+i+': Entity @'+e.ptr);
                            }
                        }else{
                            L('i','│  #'+i+': '+(ep?'无效':'null'));
                        }
                    }
                }else{
                    L('i','│ List 无效');
                    var itemsPtr=eGR.add(0x10).readPointer();
                    var size=eGR.add(0x18).readU32();
                    L('i','│   _items='+itemsPtr+' _size='+size);
                }
            }
            L('i','└─ ─');

            L('i','');
            L('i','═══════════════════════════════════════════');
            L('i','✅ 验证完成');
            L('i','═══════════════════════════════════════════');
        }
    };

    L('i','✅ 已加载, 调用 rpc.exports.verify()');
})();
