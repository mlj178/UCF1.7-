// gravity.js - 轻重力/高跳 (Gravity + Jump Modifier)
// 通过定时器遍历玩家列表，修改 velocity.y 实现重力缩放和高跳

modules.gravity = (function() {
  var enabled = false;
  var isMyPlayer = null;
  var state = { enabled: false, mode: 'player_only', gravityScale: 1.0, jumpScale: 1.0, airJump: false, airMove: false };
  var gm = null, timer = null, gmHook = null, jumpHook = null, singletonGetter = null;
  var loopCount = 0, lastLogTime = 0, playerState = {};
  var roomShuttingDown = true;
  var lifecycleHooks = [];

  function beginRoomShutdown() {
    roomShuttingDown = true;
    gm = null;
    playerState = {};
  }

  function hasGm() { if (roomShuttingDown || !gm) return false; try { var v = gm.add(0x1C).readPointer(); return v && !v.isNull(); } catch(e) { return false; } }

  function tryGetGM() {
    if (roomShuttingDown || gm) return;
    try { var methodInfo = getGameAssembly().base.add(0xE1CE64).readPointer(); var temp = singletonGetter(methodInfo); if (temp && !temp.isNull()) { gm = temp; playerState = {}; } } catch(e) {}
  }

  function loop() {
    if (!state.enabled) return;
    if (roomShuttingDown) return;
    if (!hasGm()) { tryGetGM(); if (!hasGm()) { gm = null; playerState = {}; return; } }
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
        var prev = playerState[key]; var lastGrounded = prev ? prev.lastGrounded : true;
        if (lastGrounded && !isGrounded && curY > 0.1 && state.jumpScale !== 1.0) vd.add(0x10).writeFloat(curY * state.jumpScale);
        if (curY < -0.1 && state.gravityScale < 1.0) vd.add(0x10).writeFloat(curY * state.gravityScale);
        if (state.airMove && !isGrounded) pp.add(0x88).writeFloat(999999.0);
        if (state.airJump && !isGrounded) {
          try {
            var playerInput = pp.add(0x9C).readPointer();
            if (playerInput && !playerInput.isNull()) {
              var jumpBtnState = playerInput.add(0xC).readInt();
              if (jumpBtnState === 2) vd.add(0x10).writeFloat(5.0 * state.jumpScale);
            }
          } catch(_) {}
        }
        playerState[key] = { lastGrounded: isGrounded };
      }
      var now = Date.now();
      if (now - lastLogTime > 4000) {
        lastLogTime = now;
        for (var i = 0; i < total; i++) { var ppp = ap.add(0x10 + i * 8).readPointer(); if (ppp && !ppp.isNull() && isMyPlayer(ppp)) { var pvd = ppp.add(0x90).readPointer(); if (pvd) { var vy = pvd.add(0x10).readFloat(); var pg = ppp.add(0x70).readU8() !== 0; sendLog('info', '轻重力', 'vy=' + vy.toFixed(3) + ' gnd=' + pg + ' grav=' + state.gravityScale.toFixed(2) + ' jump=' + state.jumpScale.toFixed(2)); } break; } }
      }
    } catch(_) {}
  }

  return {
    enable: function() {
      if (enabled) return;
      var mod = getGameAssembly();
      if (!mod) {
        sendBothLog('error', '轻重力', '轻重力暂未就绪，请重新连接游戏后重试', 'Gravity GameAssembly.dll not found');
        return;
      }
      var base = mod.base;
      isMyPlayer = new NativeFunction(base.add(0xB55FD0), 'bool', ['pointer']);
      singletonGetter = new NativeFunction(base.add(0x4A8170), 'pointer', ['pointer']);
      try { gmHook = Interceptor.attach(base.add(0xAF9A90), { onEnter: function(args) { var newGm = args[0]; if (newGm && !newGm.isNull()) { roomShuttingDown = false; gm = newGm; playerState = {}; } } }); } catch(e) {}
      try { jumpHook = Interceptor.attach(base.add(0xB51780), { onEnter: function(args) { if (roomShuttingDown || !state.airJump || !state.enabled) return; try { var pp = args[0]; if (pp && !pp.isNull()) { var grounded = pp.add(0x70).readU8(); if (!grounded) pp.add(0x70).writeU8(1); } } catch(_) {} } }); } catch(e) {}
      try { lifecycleHooks.push(Interceptor.attach(base.add(0xAF6A00), { onEnter: function() { roomShuttingDown = false; } })); } catch(e) {}
      try { lifecycleHooks.push(Interceptor.attach(base.add(0xAEE850), { onEnter: beginRoomShutdown })); } catch(e) {}
      try { lifecycleHooks.push(Interceptor.attach(base.add(0xAFB6F0), { onEnter: beginRoomShutdown })); } catch(e) {}
      timer = setInterval(loop, 50);
      state.enabled = true; state.airJump = true; state.airMove = true; enabled = true;
      sendLog('success', '轻重力', '已启用 (重力=' + state.gravityScale.toFixed(1) + ', 跳跃=' + state.jumpScale.toFixed(1) + ', 模式=' + state.mode + ')');
      sendStatus('gravity', true);
    },
    disable: function() {
      if (!enabled) return;
      if (timer) { clearInterval(timer); timer = null; }
      if (gmHook) { try { gmHook.detach(); } catch(e) {} gmHook = null; }
      if (jumpHook) { try { jumpHook.detach(); } catch(e) {} jumpHook = null; }
      for (var i = 0; i < lifecycleHooks.length; i++) { try { lifecycleHooks[i].detach(); } catch(e) {} }
      lifecycleHooks = [];
      state.enabled = false; roomShuttingDown = true; gm = null; playerState = {}; enabled = false;
      sendLog('info', '轻重力', '已禁用');
      sendStatus('gravity', false);
    },
    setconfig: function(g, j, m) {
      state.mode = m || 'player_only'; state.gravityScale = g; state.jumpScale = j;
      if (state.gravityScale < 0) state.gravityScale = 0; if (state.gravityScale > 1) state.gravityScale = 1;
      if (state.jumpScale < 1.0) state.jumpScale = 1.0; if (state.jumpScale > 5.0) state.jumpScale = 5.0;
      if (enabled) { state.enabled = (state.gravityScale < 1.0 || state.jumpScale !== 1.0 || state.airJump || state.airMove); } else { state.enabled = false; }
      sendLog('info', '轻重力', '配置已更新: 重力=' + state.gravityScale.toFixed(1) + ', 跳跃=' + state.jumpScale.toFixed(1) + ', 模式=' + state.mode);
      return { ok: true };
    },
    resetall: function() {
      state.enabled = false; state.gravityScale = 1.0; state.jumpScale = 1.0; state.airJump = false; state.airMove = false;
      if (timer) { clearInterval(timer); timer = null; }
      if (gmHook) { try { gmHook.detach(); } catch(e) {} gmHook = null; }
      if (jumpHook) { try { jumpHook.detach(); } catch(e) {} jumpHook = null; }
      for (var i = 0; i < lifecycleHooks.length; i++) { try { lifecycleHooks[i].detach(); } catch(e) {} }
      lifecycleHooks = [];
      roomShuttingDown = true; gm = null; playerState = {}; enabled = false;
      sendLog('info', '轻重力', '已重置'); sendStatus('gravity', false); return { ok: true };
    },
    getstatus: function() { return { enabled: state.enabled, gravityScale: state.gravityScale, jumpScale: state.jumpScale, airJump: state.airJump, airMove: state.airMove, haveGM: hasGm() }; }
  };
})();
