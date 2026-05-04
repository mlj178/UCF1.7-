// ============================================================
// 诊断工具 v8: 详细输出 List 的 _items 和 _size
// ============================================================

(function() {
    'use strict';

    function L(l,m){var p='[Diag8] ';if(l==='e')console.error(p+m);else if(l==='w')console.warn(p+m);else console.log(p+m);}

    var mod=Process.findModuleByName('GameAssembly.dll');
    if(!mod){L('e','no GameAssembly.dll');return;}
    var B=mod.base;
    L('i','=============================================================');
    L('i','诊断工具 v8: 详细 List 内存分析');
    L('i','=============================================================');

    var R={GM_AddP:0xAF9A90, P_Update:0xB551D0};
    var O={
        P_cd:0x94, CD_isB:0x1C, GM_ap:0x1C,
        GM_pBL:0x20, GM_pBLA:0x24, GM_pGR:0x28, GM_pGRA:0x2C,
        GM_eBL:0x14, GM_eGR:0x18,
    };

    var gm=null, fired=false;
    var isM=new NativeFunction(B.add(0xB55FD0),'bool',['pointer','pointer']);

    function rp(a,o){try{return a.add(o).readPointer();}catch(e){return null;}}
    function inRange(p){if(!p||p.isNull())return false;var o=p.sub(B);return o.compare(0)>=0&&o.compare(mod.size)<0;}

    function analyzeList(name,off){
        var listPtr=gm.add(off).readPointer();
        if(!listPtr||listPtr.isNull()){
            L('i','  '+name+' (+0x'+off.toString(16).padStart(2,'0')+'): null');
            return;
        }

        L('i','  '+name+' (+0x'+off.toString(16).padStart(2,'0')+'):');
        L('i','    List对象@'+listPtr);

        // 读取 List 内部字段
        var itemsPtr;try{itemsPtr=listPtr.add(0x10).readPointer();}catch(e){itemsPtr='ERR';}
        var size;try{size=listPtr.add(0x18).readU32();}catch(e){size='ERR';}
        var version;try{version=listPtr.add(0x1C).readU32();}catch(e){version='ERR';}

        L('i','    _items(0x10)='+itemsPtr);
        L('i','    _size(0x18)='+size);
        L('i','    _version(0x1C)='+version);

        if(itemsPtr==='ERR'||size==='ERR'){
            L('i','    → 无法读取');
            return;
        }

        if(!itemsPtr||itemsPtr.isNull()||size===0){
            L('i','    → 空列表');
            return;
        }

        if(size>200){
            L('i','    → size 异常('+size+')，可能不是 List');
            return;
        }

        // 遍历元素
        var selfC=0,botC=0,realC=0,nullC=0,invC=0;
        for(var i=0;i<size&&i<30;i++){
            var ep;try{ep=itemsPtr.add(0x10+i*8).readPointer();}catch(e){ep=null;}
            if(!ep||ep.isNull()){
                nullC++;
                L('i','      #'+i+': null');
                continue;
            }
            var p=checkPlayer(ep);
            if(p.type==='null')nullC++;
            else if(p.type==='SELF')selfC++;
            else if(p.type==='BOT')botC++;
            else if(p.type==='REAL')realC++;
            else invC++;
        }
        L('i','    → 统计: 总数='+size+' | 自己='+selfC+' BOT='+botC+' 真人='+realC+' null='+nullC+' 无效='+invC);
    }

    function analyzeArray(name,off){
        var arrPtr=gm.add(off).readPointer();
        if(!arrPtr||arrPtr.isNull()){
            L('i','  '+name+' (+0x'+off.toString(16).padStart(2,'0')+'): null');
            return;
        }

        L('i','  '+name+' (+0x'+off.toString(16).padStart(2,'0')+'):');
        L('i','    数组@'+arrPtr);

        var len;try{len=arrPtr.add(0xC).readU32();}catch(e){len='ERR';}
        L('i','    length(0xC)='+len);

        if(len==='ERR'||len===0||len>200){
            L('i','    → 无效数组');
            return;
        }

        var selfC=0,botC=0,realC=0,nullC=0,invC=0;
        for(var i=0;i<len&&i<30;i++){
            var ep;try{ep=arrPtr.add(0x10+i*8).readPointer();}catch(e){ep=null;}
            if(!ep||ep.isNull()){
                nullC++;
                L('i','      #'+i+': null');
                continue;
            }
            var p=checkPlayer(ep);
            if(p.type==='null')nullC++;
            else if(p.type==='SELF')selfC++;
            else if(p.type==='BOT')botC++;
            else if(p.type==='REAL')realC++;
            else invC++;
        }
        L('i','    → 统计: 总数='+len+' | 自己='+selfC+' BOT='+botC+' 真人='+realC+' null='+nullC+' 无效='+invC);
    }

    try{
        Interceptor.attach(B.add(R.P_Update),{
            onEnter:function(a){
                if(fired)return;
                fired=true;

                if(!gm){
                    L('w','gm 尚未捕获');
                    return;
                }

                L('i','');
                L('i','═══════════════════════════════════════════');
                L('i','🔍 GM@'+gm);
                L('i','═══════════════════════════════════════════');

                analyzeList('entityBL_Alive',O.GM_eBL);
                analyzeList('entityGR_Alive',O.GM_eGR);
                analyzeArray('allPlayers',O.GM_ap);
                analyzeList('playersBL',O.GM_pBL);
                analyzeList('playersBL_Alive',O.GM_pBLA);
                analyzeList('playersGR',O.GM_pGR);
                analyzeList('playersGR_Alive',O.GM_pGRA);

                L('i','');
                L('i','═══════════════════════════════════════════');
                L('i','✅ 检查完成');
                L('i','═══════════════════════════════════════════');
            }
        });
    }catch(e){L('e','Hook 失败: '+e.message);}

    try{
        Interceptor.attach(B.add(R.GM_AddP),{
            onEnter:function(a){
                if(!gm){gm=a[0];L('i','✅ GM 捕获: '+gm);}
            }
        });
    }catch(e){}

    rpc.exports={
        trigger:function(){
            L('i','等待 Player.Update 触发...');
        }
    };

    L('i','✅ 已加载, 调用 rpc.exports.trigger()');
})();
