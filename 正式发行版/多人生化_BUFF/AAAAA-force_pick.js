// Nano4T 回合特性强制选择 (vFinal - Hook 返回值)
// frida -p PID -l force_pick.js
//
// 原理: Hook GetAttribute(bool isNano) 注入返回值
// 游戏流程: OnStartNewGameRound → GetAttribute(true) → 存 attribute_Nano
//                                     GetAttribute(false)→ 存 attribute_Human
// 我们截住 GetAttribute 的 return, 换成我们想要的那个 Nano4T_Attribute*
// 不调 Init(), 不改权重, 0 crash, 0 breakpoint

var base = null;
var ATTR_PTR = {};
var WANTED_GHOST = 9;
var WANTED_HUMAN = 19;
var callCount = 0;
var READY = false;

function rdPtr(a) { try { return a.readPointer(); } catch(e) { return ptr(0); } }
function rdS32(a) { try { return a.readS32(); } catch(e) { return 0; } }

function loadAttrs() {
    try {
        var fn = new NativeFunction(base.add(0xB467A0), 'pointer', []);
        var n4 = fn();
        if (!n4 || n4.isNull()) return false;
        var aa = rdPtr(n4.add(0xD8));
        if (aa.isNull()) return false;
        var attrs = rdPtr(aa.add(0x14));
        if (attrs.isNull()) return false;
        var len = attrs.add(0x0C).readU32();
        ATTR_PTR = {};
        for (var i = 0; i < len && i < 50; i++) {
            var a = rdPtr(attrs.add(0x10 + i*4));
            if (!a.isNull()) ATTR_PTR[rdS32(a.add(0x0C))] = a;
        }
        return Object.keys(ATTR_PTR).length > 0;
    } catch(e) { return false; }
}

var mod = Process.findModuleByName('GameAssembly.dll');
if (!mod) { send(JSON.stringify({type:'error',msg:'未检测到游戏'})); }
else {
    base = mod.base;
    var fn = new NativeFunction(base.add(0xB467A0), 'pointer', []);
    var n4 = fn();
    if (!n4 || n4.isNull()) {
        send(JSON.stringify({type:'error',msg:'未进入多人生化模式'}));
    } else if (!loadAttrs()) {
        send(JSON.stringify({type:'error',msg:'未进入多人生化模式房间'}));
    } else {
        Interceptor.attach(base.add(0xB4C420), {
            onEnter: function(args) { this._isNano = !args[1].isNull(); },
            onLeave: function(retval) {
                var id = this._isNano ? WANTED_GHOST : WANTED_HUMAN;
                var p = ATTR_PTR[id];
                if (p && !p.isNull()) { retval.replace(p); }
            }
        });
        READY = true;
        send(JSON.stringify({type:'ready', ids:Object.keys(ATTR_PTR).sort()}));
    }
}

rpc.exports = {
    set: function(g, h) {
        WANTED_GHOST = g; WANTED_HUMAN = h;
        send(JSON.stringify({type:'set', g:g, h:h}));
    },
    getcurrent: function() {
        if (!READY) return JSON.stringify({type:'current', g:-1, h:-1, ready:false});
        try {
            var fn2 = new NativeFunction(base.add(0xB467A0), 'pointer', []);
            var inst = fn2(); if (!inst||inst.isNull()) return JSON.stringify({type:'current',g:-1,h:-1,ready:true});
            var an = rdPtr(inst.add(0xE0)); var ah = rdPtr(inst.add(0xE4));
            var gid = an.isNull()?-1:rdS32(an.add(0x0C));
            var hid = ah.isNull()?-1:rdS32(ah.add(0x0C));
            return JSON.stringify({type:'current', g:gid, h:hid, ready:true});
        } catch(e) { return JSON.stringify({type:'current',g:-1,h:-1,ready:true}); }
    }
};
