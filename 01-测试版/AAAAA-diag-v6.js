// ============================================================
// 诊断工具 v6: 检查所有 Player 相关的 List
// ============================================================

(function() {
    'use strict';

    function L(l,m){var p='[Diag6] ';if(l==='e')console.error(p+m);else if(l==='w')console.warn(p+m);else console.log(p+m);}

    var mod=Process.findModuleByName('GameAssembly.dll');
    if(!mod){L('e','GameAssembly.dll未找到');return;}
    var B=mod.base;
    L('i','=============================================================');
    L('i','诊断工具 v6: 检查所有 Player List');
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

    // 读取 IL2CPP 数组 T[]
    function readArray(arrPtr){
        if(!arrPtr||arrPtr.isNull())return null;
        try{
            var len=arrPtr.add(0xC).readU32();
            if(len<=0||len>200)return null;
            return{ptr:arrPtr,len:len};
        }catch(e){return null;}
    }

    // 读取 IL2CPP List<T>
    function readList(listPtr){
        if(!listPtr||listPtr.isNull())return null;
        try{
            var itemsPtr=listPtr.add(0x10).readPointer();
            var size=listPtr.add(0x18).readU32();
            if(!itemsPtr||itemsPtr.isNull()||size<=0||size>200)return null;
            return{ptr:itemsPtr,len:size};
        }catch(e){return null;}
    }

    // 检查 Player
    function checkPlayer(ptr){
        if(!ptr||ptr.isNull())return{type:'null',ptr:null};
        if(!inRange(ptr))return{type:'invalid',ptr:ptr};
        try{
            var vtable=ptr.readPointer();
            if(!inRange(vtable))return{type:'bad_vtable',ptr:ptr};
            var cdPtr=rp(ptr,O.P_cd);
            var cdValid=cdPtr&&!cdPtr.isNull()&&inRange(cdPtr);
            var isBot='?';
            if(cdValid){
                try{isBot=cdPtr.add(O.CD_isB).readU8();}catch(e){isBot='err';}
            }else{
                isBot='nullCD';
            }
            var isSelf='?';
            try{isSelf=isMy(ptr,ptr(0));}catch(e){isSelf='err';}
            return{type:isSelf===true?'SELF':(isBot===1?'BOT':(isBot===0?'REAL':('unk('+isBot+')'))),ptr:ptr,cdValid:cdValid};
        }catch(e){return{type:'err:'+e.message,ptr:ptr};}
    }

    // 读取并显示一个数组/List
    function dumpField(name,off,isArray){
        var ptr=gm.add(off).readPointer();
        L('i','');
        L('i','┌─ '+name+' (+0x'+off.toString(16).padStart(2,'0')+') ─');
        L('i','│ 指针: '+ptr);

        if(!ptr||ptr.isNull()){
            L('i','│ null');
            L('i','└─ ─');
            return;
        }

        var data=null;
        if(isArray){
            data=readArray(ptr);
            if(data)L('i','│ 数组 长度='+data.len);
        }else{
            data=readList(ptr);
            if(data)L('i','│ List size='+data.len);
        }

        if(!data){
            L('i','│ 读取失败');
            L('i','└─ ─');
            return;
        }

        var selfC=0,botC=0,realC=0,nullC=0,invC=0;
        for(var i=0;i<data.len;i++){
            var ep;try{ep=data.ptr.add(0x10+i*8).readPointer();}catch(e){ep=null;}
            var p=checkPlayer(ep);
            if(p.type==='null'){nullC++;L('i','│  #'+i+': null');}
            else if(p.type==='SELF'){selfC++;L('i','│  #'+i+': ★自己');}
            else if(p.type==='BOT'){botC++;L('i','│  #'+i+': BOT');}
            else if(p.type==='REAL'){realC++;L('i','│  #'+i+': 真人');}
            else{invC++;L('i','│  #'+i+': '+p.type+' @'+(p.ptr?p.ptr:'null'));}
        }
        L('i','│ 统计: 总数='+data.len+' | 自己='+selfC+' | BOT='+botC+' | 真人='+realC+' | null='+nullC+' | 无效='+invC);
        L('i','└─ ─');
    }

    rpc.exports={
        dump:function(){
            var waited=0;
            while(!gm&&waited<5000){Thread.sleep(0.1);waited+=100;}
            if(!gm){L('w','GM未就绪');return;}

            L('i','');
            L('i','═══════════════════════════════════════════');
            L('i','🔍 GM@'+gm);
            L('i','═══════════════════════════════════════════');

            // dump.cs 中的字段:
            // public Player[] allPlayers; // 0x1C
            // public List<Player> playersBL; // 0x20
            // public List<Player> playersBL_Alive; // 0x24
            // public List<Player> playersGR; // 0x28
            // public List<Player> playersGR_Alive; // 0x2C

            dumpField('allPlayers',0x1C,true);
            dumpField('playersBL',0x20,false);
            dumpField('playersBL_Alive',0x24,false);
            dumpField('playersGR',0x28,false);
            dumpField('playersGR_Alive',0x2C,false);

            L('i','');
            L('i','═══════════════════════════════════════════');
            L('i','✅ 检查完成');
            L('i','═══════════════════════════════════════════');
        }
    };

    L('i','✅ 已加载, 调用 rpc.exports.dump()');
})();
