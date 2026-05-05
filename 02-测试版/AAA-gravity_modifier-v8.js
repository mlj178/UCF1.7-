(function() {
    'use strict';

    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) { send('no module'); return; }
    var base = mod.base;

    var isMyPlayer = new NativeFunction(base.add(0xB55FD0), 'bool', ['pointer']);
    var state = { enabled: false, mode: 'player_only', scale: 1.0 };
    var gm = null;
    var timer = null;

    send('OK');

    function loop() {
        if (!state.enabled || !gm) return;
        try {
            var ap = gm.add(0x1C).readPointer();
            if (!ap || ap.isNull()) return;
            var total = ap.add(0xC).readU32();
            // Safety: total must be reasonable (max 64 players)
            if (total < 1 || total > 64) return;
            for (var i = 0; i < total; i++) {
                var pp = ap.add(0x10 + i * 8).readPointer();
                if (!pp || pp.isNull()) continue;
                if (state.mode !== 'all' && !isMyPlayer(pp)) continue;
                var vd = pp.add(0x90).readPointer();
                if (!vd || vd.isNull()) continue;
                var curY = vd.add(0x10).readFloat();
                if (curY < -0.1) vd.add(0x10).writeFloat(curY * state.scale);
            }
        } catch(_) {}
    }

    rpc.exports = {
        installhook: function() {
            if (timer) return { ok: true };
            timer = setInterval(loop, 50);
            return { ok: true };
        },
        setgravity: function(value, mode) {
            state.mode = mode || 'player_only';
            if (value <= 0) {
                state.scale = value / -20.0;
                if (state.scale < 0) state.scale = 0;
                if (state.scale > 1) state.scale = 1;
            } else state.scale = 1.0;
            state.enabled = (state.scale < 1.0);
            return { ok: true, scale: state.scale };
        },
        resetgravity: function() { state.enabled = false; state.scale = 1.0; return { ok: true }; },
        getgravity: function() { return { current: state.scale * -20.0, original: -20.0, scale: state.scale, enabled: state.enabled }; },
        startmonitor: function() { return { ok: true }; },
        stopmonitor: function() { return { ok: true }; },
        getstatus: function() { return { enabled: state.enabled, scale: state.scale, haveGM: !!gm }; }
    };

    try {
        Interceptor.attach(base.add(0xAF9A90), {
            onEnter: function(args) { if (!gm) gm = args[0]; }
        });
    } catch(e) {}
})();
