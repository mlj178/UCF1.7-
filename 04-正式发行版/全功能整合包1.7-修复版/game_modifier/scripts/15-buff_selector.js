// nano4t.js - 多人生化特性选择器 (Nano4T)
// Hook ChooseTrait 替换返回的属性指针 + Hook OnDestroy 检测模式销毁

modules.nano4t = (function() {
  var RVA = {
    ModeBase_Update: 0xAF6A00,
    GetInstance: 0xB467A0,
    ChooseTrait: 0xB4C420,
    OnDestroy: 0xB44320
  };
  var nano4tBase = null;
  var getInstanceFn = null;
  var NANO4T_ATTR_PTR = {};
  var NANO4T_WANTED_GHOST = -1;  // -1表示未选择
  var NANO4T_WANTED_HUMAN = -1;  // -1表示未选择
  var NANO4T_ACTIVE = false;     // 激活开关
  var NANO4T_READY = false;
  var NANO4T_MODE_DESTROYED = false;
  var hookHandles = [];
  var schedulerHook = null;
  var _pendingRequests = { init: false, health: false, current: false };

  function rdPtr(a) { try { return a.readPointer(); } catch(e) { return ptr(0); } }
  function rdS32(a) { try { return a.readS32(); } catch(e) { return 0; } }

  function getNanoInstance() {
    if (!getInstanceFn) return null;
    try {
      var instance = getInstanceFn();
      return instance && !instance.isNull() ? instance : null;
    } catch(e) {
      return null;
    }
  }

  function loadAttrs() {
    try {
      var n4 = getNanoInstance();
      if (!n4) return false;
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
    hookHandles.push(Interceptor.attach(nano4tBase.add(RVA.ChooseTrait), {
      onEnter: function(args) {
        this._isNano = !args[1].isNull();
      },
      onLeave: function(retval) {
        if (NANO4T_MODE_DESTROYED) return;
        if (!NANO4T_ACTIVE) return;  // 未激活，透传
        
        var id = this._isNano ? NANO4T_WANTED_GHOST : NANO4T_WANTED_HUMAN;
        if (id < 0) return;  // 未选择，透传
        
        var p = NANO4T_ATTR_PTR[id];
        if (p && !p.isNull()) {
          try { retval.replace(p); } catch(e) {}
        }
      }
    }));
    hookHandles.push(Interceptor.attach(nano4tBase.add(RVA.OnDestroy), {
      onEnter: function(args) {
        NANO4T_MODE_DESTROYED = true;
        NANO4T_READY = false;
        NANO4T_ACTIVE = false;  // 重置激活状态
        send(JSON.stringify({ type: 'nano4t_destroyed' }));
      }
    }));
  }

  function performInit() {
    try {
      clearHooks();
      NANO4T_READY = false;
      NANO4T_MODE_DESTROYED = false;
      NANO4T_ATTR_PTR = {};
      var n4 = getNanoInstance();
      if (!n4) {
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
  }

  function performGetCurrent() {
    var result;
    if (!NANO4T_READY || NANO4T_MODE_DESTROYED) {
      result = JSON.stringify({ type: 'nano4t_current', g: -1, h: -1, ok: false });
      send(result);
      return;
    }
    try {
      var inst = getNanoInstance();
      if (!inst) {
        result = JSON.stringify({ type: 'nano4t_current', g: -1, h: -1, ok: true });
        send(result);
        return;
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
    } catch(e) {
      result = JSON.stringify({ type: 'nano4t_current', g: -1, h: -1, ok: true });
      send(result);
    }
  }

  function performHealthCheck() {
    var result;
    if (NANO4T_MODE_DESTROYED) {
      send(JSON.stringify({ type: 'nano4t_dead' }));
      return;
    }
    try {
      var inst = getNanoInstance();
      if (!inst || rdPtr(inst.add(0xD8)).isNull()) {
        NANO4T_MODE_DESTROYED = true;
        NANO4T_READY = false;
        result = JSON.stringify({ type: 'nano4t_dead' });
      } else {
        result = JSON.stringify({ type: 'nano4t_alive' });
      }
      send(result);
    } catch(e) {
      NANO4T_MODE_DESTROYED = true;
      NANO4T_READY = false;
      send(JSON.stringify({ type: 'nano4t_dead' }));
    }
  }

  function processPendingRequests() {
    if (_pendingRequests.init) {
      _pendingRequests.init = false;
      performInit();
    }
    if (_pendingRequests.health) {
      _pendingRequests.health = false;
      performHealthCheck();
    }
    if (_pendingRequests.current) {
      _pendingRequests.current = false;
      performGetCurrent();
    }

    // 主线程任务已处理完，立即解除Update Hook，避免每帧空跑。
    if (schedulerHook) {
      try { schedulerHook.detach(); } catch(e) {}
      schedulerHook = null;
    }
  }

  function ensureMainThreadHook() {
    if (schedulerHook) return true;
    var mod = getGameAssembly();
    if (!mod) return false;
    nano4tBase = mod.base;
    try {
      getInstanceFn = new NativeFunction(nano4tBase.add(RVA.GetInstance), 'pointer', []);
      schedulerHook = Interceptor.attach(nano4tBase.add(RVA.ModeBase_Update), {
        onEnter: function() {
          processPendingRequests();
        }
      });
      return true;
    } catch(e) {
      schedulerHook = null;
      getInstanceFn = null;
      return false;
    }
  }

  return {
    enable: function() {
      this.init();
    },
    disable: function() {
      this.destroy();
    },
    init: function() {
      _pendingRequests.init = true;
      if (!ensureMainThreadHook()) {
        _pendingRequests.init = false;
        send(JSON.stringify({ type: 'nano4t_error', msg: '未检测到游戏进程' }));
        return JSON.stringify({ ok: false });
      }
      return JSON.stringify({ ok: true, queued: true });
    },
    set: function(g, h) {
      NANO4T_WANTED_GHOST = g;
      NANO4T_WANTED_HUMAN = h;
      NANO4T_ACTIVE = true;  // 设置时激活
      send(JSON.stringify({ type: 'nano4t_set', g: g, h: h }));
    },
    getCurrent: function() {
      _pendingRequests.current = true;
      if (!ensureMainThreadHook()) {
        _pendingRequests.current = false;
        return JSON.stringify({ ok: false });
      }
      return JSON.stringify({ ok: true, queued: true });
    },
    healthCheck: function() {
      _pendingRequests.health = true;
      if (!ensureMainThreadHook()) {
        _pendingRequests.health = false;
        return JSON.stringify({ ok: false });
      }
      return JSON.stringify({ ok: true, queued: true });
    },
    onModeRound: function() {
      if (!NANO4T_READY || NANO4T_MODE_DESTROYED) {
        return this.init();
      }
      return this.getCurrent();
    },
    destroy: function() {
      clearHooks();
      NANO4T_READY = false;
      NANO4T_MODE_DESTROYED = false;
      NANO4T_ACTIVE = false;  // 重置激活状态
      NANO4T_ATTR_PTR = {};
      _pendingRequests = { init: false, health: false, current: false };
      if (schedulerHook) {
        try { schedulerHook.detach(); } catch(e) {}
        schedulerHook = null;
      }
    }
  };
})();
