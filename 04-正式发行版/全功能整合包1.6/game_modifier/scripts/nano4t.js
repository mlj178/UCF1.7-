// nano4t.js - 多人生化特性选择器 (Nano4T)
// Hook ChooseTrait 替换返回的属性指针 + Hook OnDestroy 检测模式销毁

modules.nano4t = (function() {
  var nano4tBase = null;
  var NANO4T_ATTR_PTR = {};
  var NANO4T_WANTED_GHOST = 9;
  var NANO4T_WANTED_HUMAN = 19;
  var NANO4T_READY = false;
  var NANO4T_MODE_DESTROYED = false;
  var hookHandles = [];

  function rdPtr(a) { try { return a.readPointer(); } catch(e) { return ptr(0); } }
  function rdS32(a) { try { return a.readS32(); } catch(e) { return 0; } }

  function loadAttrs() {
    try {
      var fn = new NativeFunction(nano4tBase.add(0xB467A0), 'pointer', []);
      var n4 = fn();
      if (!n4 || n4.isNull()) return false;
      var aa = rdPtr(n4.add(0xD8));
      if (aa.isNull()) return false;
      var attrs = rdPtr(aa.add(0x14));
      if (attrs.isNull()) return false;
      var len = attrs.add(0x0C).readU32();
      NANO4T_ATTR_PTR = {};
      for (var i = 0; i < len && i < 50; i++) {
        var a = rdPtr(attrs.add(0x10 + i*4));
        if (!a.isNull()) NANO4T_ATTR_PTR[rdS32(a.add(0x0C))] = a;
      }
      return Object.keys(NANO4T_ATTR_PTR).length > 0;
    } catch(e) { return false; }
  }

  function clearHooks() {
    for (var i = 0; i < hookHandles.length; i++) {
      try { hookHandles[i].detach(); } catch(e) {}
    }
    hookHandles = [];
  }

  function installHooks() {
    clearHooks();
    hookHandles.push(Interceptor.attach(nano4tBase.add(0xB4C420), {
      onEnter: function(args) {
        this._isNano = !args[1].isNull();
      },
      onLeave: function(retval) {
        if (NANO4T_MODE_DESTROYED) return;
        var id = this._isNano ? NANO4T_WANTED_GHOST : NANO4T_WANTED_HUMAN;
        var p = NANO4T_ATTR_PTR[id];
        if (p && !p.isNull()) {
          try { retval.replace(p); } catch(e) {}
        }
      }
    }));
    hookHandles.push(Interceptor.attach(nano4tBase.add(0xB44320), {
      onEnter: function(args) {
        NANO4T_MODE_DESTROYED = true;
        NANO4T_READY = false;
        send(JSON.stringify({ type: 'nano4t_destroyed' }));
      }
    }));
  }

  return {
    enable: function() {
      this.init();
    },
    disable: function() {
      this.destroy();
    },
    init: function() {
      try {
        clearHooks();
        NANO4T_READY = false;
        NANO4T_MODE_DESTROYED = false;
        NANO4T_ATTR_PTR = {};
        var mod = getGameAssembly();
        if (!mod) {
          send(JSON.stringify({ type: 'nano4t_error', msg: '未检测到游戏进程' }));
          return;
        }
        nano4tBase = mod.base;
        var fn = new NativeFunction(nano4tBase.add(0xB467A0), 'pointer', []);
        var n4 = fn();
        if (!n4 || n4.isNull()) {
          send(JSON.stringify({ type: 'nano4t_error', msg: '未进入多人生化模式' }));
        } else if (!loadAttrs()) {
          send(JSON.stringify({ type: 'nano4t_error', msg: '未进入多人生化模式房间' }));
        } else {
          installHooks();
          NANO4T_READY = true;
          send(JSON.stringify({ type: 'nano4t_ready', ids: Object.keys(NANO4T_ATTR_PTR).sort() }));
        }
      } catch(e) {
        send(JSON.stringify({ type: 'nano4t_error', msg: '初始化异常: ' + (e.message || e) }));
      }
    },
    set: function(g, h) {
      NANO4T_WANTED_GHOST = g;
      NANO4T_WANTED_HUMAN = h;
      send(JSON.stringify({ type: 'nano4t_set', g: g, h: h }));
    },
    getCurrent: function() {
      var result;
      if (!NANO4T_READY || NANO4T_MODE_DESTROYED) {
        result = JSON.stringify({ type: 'nano4t_current', g: -1, h: -1, ok: false });
        send(result);
        return result;
      }
      try {
        var fn2 = new NativeFunction(nano4tBase.add(0xB467A0), 'pointer', []);
        var inst = fn2();
        if (!inst || inst.isNull()) {
          result = JSON.stringify({ type: 'nano4t_current', g: -1, h: -1, ok: true });
          send(result);
          return result;
        }
        var an = rdPtr(inst.add(0xE0));
        var ah = rdPtr(inst.add(0xE4));
        result = JSON.stringify({
          type: 'nano4t_current',
          g: an.isNull() ? -1 : rdS32(an.add(0x0C)),
          h: ah.isNull() ? -1 : rdS32(ah.add(0x0C)),
          ok: true
        });
        send(result);
        return result;
      } catch(e) {
        result = JSON.stringify({ type: 'nano4t_current', g: -1, h: -1, ok: true });
        send(result);
        return result;
      }
    },
    healthCheck: function() {
      var result;
      if (NANO4T_MODE_DESTROYED) {
        result = JSON.stringify({ type: 'nano4t_dead' });
        send(result);
        return result;
      }
      try {
        var fn2 = new NativeFunction(nano4tBase.add(0xB467A0), 'pointer', []);
        var inst = fn2();
        if (!inst || inst.isNull()) {
          NANO4T_MODE_DESTROYED = true;
          NANO4T_READY = false;
          result = JSON.stringify({ type: 'nano4t_dead' });
          send(result);
          return result;
        }
        var aa = rdPtr(inst.add(0xD8));
        if (aa.isNull()) {
          NANO4T_MODE_DESTROYED = true;
          NANO4T_READY = false;
          result = JSON.stringify({ type: 'nano4t_dead' });
          send(result);
          return result;
        }
        result = JSON.stringify({ type: 'nano4t_alive' });
        send(result);
        return result;
      } catch(e) {
        NANO4T_MODE_DESTROYED = true;
        NANO4T_READY = false;
        result = JSON.stringify({ type: 'nano4t_dead' });
        send(result);
        return result;
      }
    },
    destroy: function() {
      clearHooks();
      NANO4T_READY = false;
      NANO4T_MODE_DESTROYED = false;
      NANO4T_ATTR_PTR = {};
      nano4tBase = null;
    }
  };
})();
