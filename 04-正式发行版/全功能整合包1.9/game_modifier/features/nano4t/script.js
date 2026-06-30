// Local helpers for this special feature only.
var modules = {};
var __localMaxLogsPerModule = 80;
var __localModuleLogCounts = {};
var __localGameAssemblyCache = null;
var __localGameAssemblyLogged = false;
var __localCleanupCallbacks = [];

function sendRoutedLog(level, module, message, audience, devDetail) {
  try {
    if (!__localModuleLogCounts[module]) __localModuleLogCounts[module] = 0;
    if (__localModuleLogCounts[module] >= __localMaxLogsPerModule) return;
    __localModuleLogCounts[module]++;
    send({ type: 'log', level: level, module: module, message: message, audience: audience || 'dev', dev_detail: devDetail || '' });
  } catch (_) {}
}

function sendUserLog(level, module, message) {
  sendRoutedLog(level, module, message, 'user', '');
}

function sendDevLog(level, module, message, devDetail) {
  sendRoutedLog(level, module, message, 'dev', devDetail || '');
}

function sendBothLog(level, module, message, devDetail) {
  sendRoutedLog(level, module, message, 'both', devDetail || '');
}

function sendLog(level, module, message) {
  sendDevLog(level, module, message, '');
}

function sendLogFile(level, module, message) {
  try { send({ type: 'log_file', level: level, module: module, message: message, audience: 'dev', dev_detail: '' }); } catch (_) {}
}

function sendStatus(feature, enabled) {
  try { send({ type: 'status', feature: feature, enabled: enabled }); } catch (_) {}
}

function getGameAssembly() {
  try {
    if (__localGameAssemblyCache) return __localGameAssemblyCache;
    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) {
      sendDevLog('error', '系统', '未找到 GameAssembly.dll', 'GameAssembly.dll not found');
      return null;
    }
    __localGameAssemblyCache = mod;
    if (!__localGameAssemblyLogged) {
      __localGameAssemblyLogged = true;
      sendDevLog('info', '系统', 'GameAssembly.dll: base=' + mod.base + ' size=' + mod.size, 'GameAssembly module located');
    }
    return mod;
  } catch (e) {
    sendDevLog('error', '系统', '获取 GameAssembly 失败: ' + (e.message || e), 'getGameAssembly failed');
    return null;
  }
}

function registerCleanup(callback) {
  if (typeof callback !== 'function') return false;
  __localCleanupCallbacks.push(callback);
  return true;
}

function cleanupAll(reason) {
  var errors = [];
  for (var i = __localCleanupCallbacks.length - 1; i >= 0; i--) {
    try { __localCleanupCallbacks[i](reason || 'cleanup'); } catch (e) { errors.push(e.message || String(e)); }
  }
  __localCleanupCallbacks = [];
  return { ok: errors.length === 0, errors: errors, reason: reason || 'cleanup' };
}

function parseJsonResult(value, fallback) {
  if (typeof value !== 'string') return value === undefined ? (fallback || { ok: true }) : value;
  try { return JSON.parse(value); } catch (_) { return fallback || { ok: true, result: value }; }
}


// nano4t.js - 多人生化特性选择器 (Nano4T)
// Hook ChooseTrait 替换返回的属性指针 + Hook OnDestroy 检测模式销毁

modules.nano4t = (function() {
  // ===== 配置与运行状态 =====
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

  // ===== 指针读取与实例获取 =====
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

  // ===== 特性列表加载 =====
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

  // ===== Hook 安装与清理 =====
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
        sendDevLog('info', 'Nano4T', '多人生化模式实例已销毁', 'Nano4T OnDestroy triggered');
        send(JSON.stringify({ type: 'nano4t_destroyed' }));
      }
    }));
  }

  // ===== 主线程任务执行 =====
  function performInit() {
    try {
      sendDevLog('info', 'Nano4T', '开始初始化多人生化特性系统', 'Nano4T performInit start');
      clearHooks();
      NANO4T_READY = false;
      NANO4T_MODE_DESTROYED = false;
      NANO4T_ATTR_PTR = {};
      var n4 = getNanoInstance();
      if (!n4) {
        sendDevLog('warn', 'Nano4T', '未进入多人生化模式', 'Nano4T getInstance returned null');
        send(JSON.stringify({ type: 'nano4t_error', msg: '未进入多人生化模式' }));
      } else if (!loadAttrs()) {
        sendDevLog('warn', 'Nano4T', '未进入多人生化模式房间', 'Nano4T loadAttrs failed');
        send(JSON.stringify({ type: 'nano4t_error', msg: '未进入多人生化模式房间' }));
      } else {
        installHooks();
        NANO4T_READY = true;
        sendDevLog('success', 'Nano4T', '多人生化特性系统已就绪', 'Nano4T ready, attrCount=' + Object.keys(NANO4T_ATTR_PTR).length);
        send(JSON.stringify({ type: 'nano4t_ready', ids: Object.keys(NANO4T_ATTR_PTR).sort() }));
      }
    } catch(e) {
      sendDevLog('error', 'Nano4T', '初始化异常: ' + (e.message || e), 'Nano4T performInit exception');
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

  function queueMainThreadRequest(requestName, failLogLevel, failLogTitle, failLogDev, failMessage) {
    _pendingRequests[requestName] = true;
    if (ensureMainThreadHook()) {
      return JSON.stringify({ ok: true, queued: true });
    }

    _pendingRequests[requestName] = false;
    if (failLogTitle) {
      sendDevLog(failLogLevel || 'warn', 'Nano4T', failLogTitle, failLogDev);
    }
    if (failMessage) {
      send(JSON.stringify({ type: 'nano4t_error', msg: failMessage }));
    }
    return JSON.stringify({ ok: false });
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

  // ===== 主线程调度 Hook =====
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

  // ===== 功能开关与 RPC 边界 =====
  function initFeature() {
      var result = queueMainThreadRequest(
        'init',
        'error',
        '无法安装主线程调度 Hook',
        'Nano4T ensureMainThreadHook failed during init',
        '未检测到游戏进程'
      );
      if (result !== JSON.stringify({ ok: true, queued: true })) return result;
      sendDevLog('info', 'Nano4T', '初始化任务已排队', 'Nano4T init queued on ModeBase.Update');
      return JSON.stringify({ ok: true, queued: true });
  }

  function enableFeature() {
      initFeature();
  }

  function setWantedTraits(g, h) {
      NANO4T_WANTED_GHOST = g;
      NANO4T_WANTED_HUMAN = h;
      NANO4T_ACTIVE = true;  // 设置时激活
      sendDevLog('info', 'Nano4T', '已设置目标特性 g=' + g + ', h=' + h, 'Nano4T wanted traits updated');
      send(JSON.stringify({ type: 'nano4t_set', g: g, h: h }));
  }

  function getCurrentTraits() {
      return queueMainThreadRequest(
        'current',
        'warn',
        '读取当前特性失败：无法安装主线程调度 Hook',
        'Nano4T getCurrent ensureMainThreadHook failed',
        null
      );
  }

  function healthCheck() {
      return queueMainThreadRequest(
        'health',
        'warn',
        '健康检查失败：无法安装主线程调度 Hook',
        'Nano4T healthCheck ensureMainThreadHook failed',
        null
      );
  }

  function onModeRound() {
      if (!NANO4T_READY || NANO4T_MODE_DESTROYED) {
        return initFeature();
      }
      return getCurrentTraits();
  }

  function destroyFeature() {
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

  function disableFeature() {
      destroyFeature();
  }

  return {
    enable: enableFeature,
    disable: disableFeature,
    init: initFeature,
    set: setWantedTraits,
    getCurrent: getCurrentTraits,
    healthCheck: healthCheck,
    onModeRound: onModeRound,
    destroy: destroyFeature
  };
})();


function __nano4tModule() {
  return modules.nano4t;
}

rpc.exports = {
  enable: function(config) {
    return rpc.exports.nano4tInit(config || {});
  },
  disable: function() {
    var module = __nano4tModule();
    if (module && typeof module.destroy === 'function') module.destroy();
    return { ok: true, enabled: false };
  },
  setConfig: function(config) {
    return { ok: true, config: config || {} };
  },
  status: function() {
    return { ok: true, feature: 'nano4t' };
  },
  cleanup: function(payload) {
    var module = __nano4tModule();
    if (module && typeof module.destroy === 'function') module.destroy();
    return { ok: true, reason: payload && payload.reason ? payload.reason : 'cleanup' };
  },
  nano4tInit: function(payload) {
    var module = __nano4tModule();
    if (!module || typeof module.init !== 'function') return { ok: false, msg: '多人生化模块未加载' };
    return parseJsonResult(module.init(), { ok: true });
  },
  nano4tSet: function(payload) {
    var module = __nano4tModule();
    if (!module || typeof module.set !== 'function') return { ok: false, msg: '多人生化模块未加载' };
    payload = payload || {};
    var g = parseInt(payload.g, 10);
    var h = parseInt(payload.h, 10);
    module.set(g, h);
    return { ok: true, g: g, h: h };
  },
  nano4tGetCurrent: function(payload) {
    var module = __nano4tModule();
    if (!module || typeof module.getCurrent !== 'function') return { type: 'nano4t_current', g: -1, h: -1, ok: false };
    return parseJsonResult(module.getCurrent(), { ok: true });
  },
  nano4tHealthCheck: function(payload) {
    var module = __nano4tModule();
    if (!module || typeof module.healthCheck !== 'function') return { type: 'nano4t_dead' };
    return parseJsonResult(module.healthCheck(), { ok: true });
  }
};


