// ============================================================
// Bot 出生点集合器 v11 — 直写 native Transform C++ 内存
// 根因: CharacterController 覆盖 Unity 托管层的 Transform.position
// 方案: get_transform → 读原生ptr(Trans+0x10) → 直写 native 内存
//       + 写 Transform.set_position_Injected 双保险
// ============================================================

(function() {
    'use strict';

    function L(l,m){var p='[BotToSpawn] ';if(l==='e')console.error(p+m);else if(l==='w')console.warn(p+m);else console.log(p+m);}

    var m=Process.findModuleByName('GameAssembly.dll');
    if(!m){L('e','no GameAssembly');return;}
    var B=m.base;
    L('i','base='+B);

    var R={
        GM_AddP:   0xAF9A90,
        MM_MapGun: 0xAEBB70,
        P_Update:  0xB551D0,
        P_isMy:    0xB55FD0,
        E_isDead:  0xB400E0,
        getTrans:  0x32CF40, // get_transform() → works(v9)
        setPosInj: 0x3F4810, // set_position_Injected
    };
    var O={
        P_cd:  0x94,  CD_isBot:0x14,
        GM_ap: 0x1C,  MM_SPB:  0x10,
    };

    var gm=null, mm=null, ntp=false, tn=0, spawn=null;

    var isMy=  new NativeFunction(B.add(R.P_isMy), 'bool',    ['pointer','pointer']);
    var isDead=new NativeFunction(B.add(R.E_isDead),'bool',    ['pointer','pointer']);
    var gt=    new NativeFunction(B.add(R.getTrans),'pointer', ['pointer','pointer']);
    var spi=   new NativeFunction(B.add(R.setPosInj),'void',   ['pointer','pointer','pointer']);
    var bf=    Memory.alloc(16);
    var zeroBf=Memory.alloc(16);

    function rdS(p){
        if(!p||p.isNull())return null;
        if(p.add(0xC).readU32()===0)return null;
        var e=p.add(0x10);
        return {x:e.readFloat(),y:e.add(4).readFloat(),z:e.add(8).readFloat()};
    }

    // GM
    try{Interceptor.attach(B.add(R.GM_AddP),{onEnter:function(a){if(!gm){gm=a[0];send(JSON.stringify({t:'gm'}));L('i','GM@'+gm);}}});}catch(e){}
    // MM — 立即缓存 SP_BL
    try{Interceptor.attach(B.add(R.MM_MapGun),{onEnter:function(a){
        if(!mm){mm=a[0];
            try{spawn=rdS(mm.add(O.MM_SPB).readPointer());if(spawn)L('i','SP_BL:('+spawn.x.toFixed(1)+','+spawn.y.toFixed(1)+','+spawn.z.toFixed(1)+')');}catch(x){}
            send(JSON.stringify({t:'mm'}));}
    }});}catch(e){}
    // Player.Update
    try{Interceptor.attach(B.add(R.P_Update),{onEnter:function(a){
        if(!ntp)return; ntp=false;
        if(!gm)return; if(!spawn)spawn={x:0,y:0,z:0};
        tn++;
        L('i','=== #'+tn+' ===');

        bf.writeFloat(spawn.x); bf.add(4).writeFloat(spawn.y); bf.add(8).writeFloat(spawn.z);

        var ap=gm.add(O.GM_ap).readPointer();
        if(!ap||ap.isNull())return;
        var n=ap.add(0xC).readU32();

        var bot=0,dead=0,skip=0,native=0,managed=0;
        // 尝试的 native 位置偏移 (Unity 2020-2022 常见值)
        var NOFF=[0x38,0x70,0x90,0xA0];

        for(var i=0;i<n;i++){
            try{
                var pp=ap.add(0x10+i*8).readPointer();
                if(!pp||pp.isNull()){skip++;continue;}
                if(isMy(pp,ptr(0))){skip++;continue;}

                var cd=pp.add(O.P_cd).readPointer();
                if(!cd||cd.isNull()){skip++;continue;}
                if(!cd.add(O.CD_isBot).readU8()){skip++;continue;}
                if(isDead(pp,ptr(0))){dead++;continue;}

                // -- Step1: managed 层 set_position_Injected --
                var tr=gt(pp,ptr(0));
                if(tr&&!tr.isNull()){
                    spi(tr,bf,ptr(0)); managed++;
                }

                // -- Step2: native 层直写 Transform C++ 内存 --
                if(tr&&!tr.isNull()){
                    var np=tr.add(0x10).readPointer();
                    if(np&&!np.isNull()){
                        for(var k=0;k<NOFF.length;k++){
                            try{
                                np.add(NOFF[k]).writeFloat(spawn.x);
                                np.add(NOFF[k]+4).writeFloat(spawn.y);
                                np.add(NOFF[k]+8).writeFloat(spawn.z);
                                native++;
                                if(i===0)L('i','  native write @+0x'+NOFF[k].toString(16));
                                break; // 成功一个就停
                            }catch(e2){}
                        }
                    }
                }

                bot++;
            }catch(e){
                L('w','#'+i+' 异常:'+e.message);
            }
        }

        var msg='传送 '+bot+'Bot (managed='+managed+' native='+native+')';
        if(dead>0)msg+=' | '+dead+'死';
        L('i',msg);
        send(JSON.stringify({t:'done',c:bot,m:msg}));
    }});}catch(e){}

    rpc.exports={teleport:function(){
        if(!gm){send(JSON.stringify({t:'err',m:'GM未就绪'}));return;}
        ntp=true; L('i','已收到指令');
    }};

    L('i','====================');
    L('i','v11 | native Transform');
    L('i','====================');
})();
