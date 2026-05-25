(function() {
    'use strict';

    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) { send('no module'); return; }
    var base = mod.base;

    var isMyPlayer = new NativeFunction(base.add(0xB55FD0), 'bool', ['pointer']);
    var state = {
        enabled: false,
        mode: 'player_only',
        gravityScale: 1.0,
        jumpScale: 1.0,
        airJump: false,
        airMove: false
    };
    var gm = null;
    var timer = null;
    var loopCount = 0;
    var lastLogTime = 0;
    var playerState = {};

    send('OK');

    function hasGm() {
        if (!gm) return false;
        try {
            var v = gm.add(0x1C).readPointer();
            return v && !v.isNull();
        } catch(e) { return false; }
    }

    function loop() {
        if (!state.enabled) return;

        // If GM pointer is dead, try to re-capture from AddPlayer hook
        if (!hasGm()) {
            gm = null;
            playerState = {};
            return;
        }

        try {
            var ap = gm.add(0x1C).readPointer();
            if (!ap || ap.isNull()) return;
            var total = ap.add(0xC).readU32();
            if (total < 1 || total > 64) return;

            loopCount++;

            for (var i = 0; i < total; i++) {
                var pp = ap.add(0x10 + i * 8).readPointer();
                if (!pp || pp.isNull()) continue;
                if (state.mode !== 'all' && !isMyPlayer(pp)) continue;

                var key = pp.toString();

                var isGrounded = pp.add(0x70).readU8() !== 0;

                var vd = pp.add(0x90).readPointer();
                if (!vd || vd.isNull()) continue;
                var curY = vd.add(0x10).readFloat();

                var prev = playerState[key];
                var lastGrounded = prev ? prev.lastGrounded : true;

                if (lastGrounded && !isGrounded && curY > 0.1 && state.jumpScale !== 1.0) {
                    vd.add(0x10).writeFloat(curY * state.jumpScale);
                }

                if (curY < -0.1 && state.gravityScale < 1.0) {
                    vd.add(0x10).writeFloat(curY * state.gravityScale);
                }

                if (state.airMove && !isGrounded) {
                    pp.add(0x88).writeFloat(999999.0);
                }

                if (state.airJump && !isGrounded) {
                    try {
                        var playerInput = pp.add(0x9C).readPointer();
                        if (playerInput && !playerInput.isNull()) {
                            var jumpBtnState = playerInput.add(0xC).readInt();
                            if (jumpBtnState === 2) {
                                vd.add(0x10).writeFloat(10.0);
                            }
                        }
                    } catch(_) {}
                }

                playerState[key] = { lastGrounded: isGrounded };
            }

            var now = Date.now();
            if (now - lastLogTime > 4000) {
                lastLogTime = now;
                var playerPP = null;
                for (var i = 0; i < total; i++) {
                    var ppp = ap.add(0x10 + i * 8).readPointer();
                    if (ppp && !ppp.isNull() && isMyPlayer(ppp)) { playerPP = ppp; break; }
                }
                if (playerPP) {
                    var pvd = playerPP.add(0x90).readPointer();
                    if (pvd) {
                        var vy = pvd.add(0x10).readFloat();
                        var pg = playerPP.add(0x70).readU8() !== 0;
                        send('vy=' + vy.toFixed(3) + ' gnd=' + pg + ' grav=' + state.gravityScale.toFixed(2) + ' jump=' + state.jumpScale.toFixed(2) + ' airJ=' + state.airJump + ' airM=' + state.airMove);
                    }
                }
            }
        } catch(_) {}
    }

    rpc.exports = {
        installhook: function() {
            if (timer) return { ok: true };
            timer = setInterval(loop, 50);
            return { ok: true };
        },

        setconfig: function(gravityScale, jumpScale, mode, airJump, airMove) {
            state.mode = mode || 'player_only';
            state.gravityScale = gravityScale;
            state.jumpScale = jumpScale;
            state.airJump = !!airJump;
            state.airMove = !!airMove;
            if (state.gravityScale < 0) state.gravityScale = 0;
            if (state.gravityScale > 1) state.gravityScale = 1;
            if (state.jumpScale < 1.0) state.jumpScale = 1.0;
            if (state.jumpScale > 2.0) state.jumpScale = 2.0;
            state.enabled = (state.gravityScale < 1.0 || state.jumpScale !== 1.0 || state.airJump || state.airMove);
            return { ok: true };
        },

        resetall: function() {
            state.enabled = false;
            state.gravityScale = 1.0;
            state.jumpScale = 1.0;
            state.airJump = false;
            state.airMove = false;
            return { ok: true };
        },

        getstatus: function() {
            return { enabled: state.enabled, gravityScale: state.gravityScale, jumpScale: state.jumpScale, airJump: state.airJump, airMove: state.airMove, haveGM: hasGm() };
        },

        startmonitor: function() { return { ok: true }; },
        stopmonitor: function() { return { ok: true }; }
    };

    // Hook OnJumpBtnDown - force isGrounded=true when airJump enabled
    try {
        Interceptor.attach(base.add(0xB51780), {
            onEnter: function(args) {
                if (!state.airJump || !state.enabled) return;
                try {
                    var pp = args[0];
                    if (pp && !pp.isNull()) {
                        var grounded = pp.add(0x70).readU8();
                        if (!grounded) {
                            pp.add(0x70).writeU8(1);
                        }
                    }
                } catch(_) {}
            }
        });
    } catch(e) {}

    // Capture GM - always update, reset playerState on change
    try {
        Interceptor.attach(base.add(0xAF9A90), {
            onEnter: function(args) {
                var newGm = args[0];
                if (newGm && !newGm.isNull()) {
                    gm = newGm;
                    playerState = {};  // Reset state tracking for new room
                }
            }
        });
    } catch(e) {}
})();
