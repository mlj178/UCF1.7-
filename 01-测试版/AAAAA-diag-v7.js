// ============================================================
// 诊断工具 v7: 通过 Player.Update Hook 读取 GM 字段
// 参考 v19 的成功方式
// ============================================================

(function() {
    'use strict';

    function L(l,m){var p='[Diag7] ';if(l==='e')console.error(p+m);else if(l==='w')console.warn(p+m);else console.log(p+m);}

    var mod=Process.findModuleByName('GameAssembly.dll');
    if(!mod){L('e','no GameAssembly.dll');return;}
    var B=mod.base;
    L('i','=============================================================');
    L('i','诊断工具 v7: 通过 Player.Update 读取 GM 字段');
    L('i','=============================================================');

    var R={
        GM_AddP:0xAF9A90, P_Update:0xB551D0,
    };
    var O={
        P_cd:0x94, CD_isB:0x1C, GM_ap:0x1C,
        GM_pBL:0x20, GM_pBLA:0x24, GM_pGR:0x28, GM_pGRA:0x2C,
        GM_eBL:0x14, GM_eGR:0x18,
    };

    var gm=null, fired=false;
    var isM=new NativeFunction(B.add(0xB55FD0),'bool',['pointer','pointer']);

    function rp(a,o){try{return a.add(o).readPointer();}catch(e){return null;}}
    function inRange(p){if(!p||p.isNull())return false;var o=p.sub(B);return o.compare(0)>=0&&o.compare(mod.size)<0;}

    // 读取数组
    function readArray(arrPtr){
        if(!arrPtr||arrPtr.isNull())return null;
        try{var len=arrPtr.add(0xC).readU32();if(len<=0||len>200)return null;return{ptr:arrPtr,len:len};}catch(e){return null;}
    }

    // 读取 List
    function readList(listPtr){
        if(!listPtr||listPtr.isNull())return null;
        try{
            var itemsPtr=listPtr.add(0x10).readPointer();
            var size=listPtr.add(0x18).readU32();
            if(!itemsPtr||itemsPtr.isNull()||size<=0||size>200)return null;
            return{ptr:itemsPtr,len:size};
        }catch(e){return null;}
    }

    function checkPlayer(ptr){
        if(!ptr||ptr.isNull())return{type:'null'};
        if(!inRange(ptr))return{type:'invalid'};
        try{
            var vtable=ptr.readPointer();
            if(!inRange(vtable))return{type:'bad_vt'};
            var cdPtr=rp(ptr,O.P_cd);
            var hasCD=cdPtr&&!cdPtr.isNull();
            var isBot='?';
            if(hasCD){try{isBot=cdPtr.add(O.CD_isB).readU8();}catch(e){isBot='err';}}
            else{isBot='nullCD';}
            var isSelf=false;try{isSelf=isM(ptr,ptr(0));}catch(e){}
            if(isSelf)return{type:'SELF'};
            if(isBot===1)return{type:'BOT'};
            if(isBot===0)return{type:'REAL'};
            return{type:'unk('+isBot+')'};
        }catch(e){return{type:'err'}};
    }

    function dumpField(name,off,isArray){
        var ptr=gm.add(off).readPointer();
        if(!ptr||ptr.isNull()){L('i','  '+name+' (+0x'+off.toString(16).padStart(2,'0')+'): null');return;}

        var data=isArray?readArray(ptr):readList(ptr);
        if(!data){L('i','  '+name+' (+0x'+off.toString(16).padStart(2,'0')+'): '+ptr+' (读取失败)');return;}

        var selfC=0,botC=0,realC=0,nullC=0,invC=0;
        for(var i=0;i<data.len;i++){
            var ep;try{ep=data.ptr.add(0x10+i*8).readPointer();}catch(e){ep=null;}
            var p=checkPlayer(ep);
            if(p.type==='null')nullC++;
            else if(p.type==='SELF')selfC++;
            else if(p.type==='BOT')botC++;
            else if(p.type==='REAL')realC++;
            else invC++;
        }
        L('i','  '+name+' (+0x'+off.toString(16).padStart(2,'0')+'): '+data.len+' 元素 | 自己='+selfC+' BOT='+botC+' 真人='+realC+' null='+nullC+' 无效='+invC);
    }

    // Hook Player.Update
    try{
        Interceptor.attach(B.add(R.P_Update),{
            onEnter:function(a){
                if(fired)return;
                fired=true;

                // Player.Update 的 this 指针是 Player 对象
                var playerThis=this.context.x0;
                L('i','Player.Update this='+playerThis);

                // 通过 Player 对象无法直接获取 GM，但我们可以用 AddPlayer Hook 捕获的 gm
                if(!gm){
                    L('w','gm 尚未捕获，等待 AddPlayer Hook...');
                    return;
                }

                L('i','');
                L('i','═══════════════════════════════════════════');
                L('i','🔍 GM@'+gm);
                L('i','═══════════════════════════════════════════');

                dumpField('entityBL_Alive',O.GM_eBL,false);
                dumpField('entityGR_Alive',O.GM_eGR,false);
                dumpField('allPlayers',O.GM_ap,true);
                dumpField('playersBL',O.GM_pBL,false);
                dumpField('playersBL_Alive',O.GM_pBLA,false);
                dumpField('playersGR',O.GM_pGR,false);
                dumpField('playersGR_Alive',O.GM_pGRA,false);

                L('i','');
                L('i','═══════════════════════════════════════════');
                L('i','✅ 检查完成');
                L('i','═══════════════════════════════════════════');
            }
        });
        L('i','✅ Player.Update Hook 已安装');
    }catch(e){L('e','Hook 失败: '+e.message);}

    // Hook AddPlayer 捕获 gm
    try{
        Interceptor.attach(B.add(R.GM_AddP),{
            onEnter:function(a){
                if(!gm){gm=a[0];L('i','✅ GM 捕获: '+gm);}
            }
        });
        L('i','✅ AddPlayer Hook 已安装');
    }catch(e){L('e','AddPlayer Hook 失败: '+e.message);}

    rpc.exports={
        trigger:function(){
            L('i','等待 Player.Update 触发...');
            L('i','请在游戏中移动或等待几秒');
        }
    };

    L('i','✅ 已加载, 调用 rpc.exports.trigger()');
})();
