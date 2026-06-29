// _common.js - Frida 公共函数库
// 所有模块共享的基础函数，由 frida_manager 在拼接脚本时首先加载

var MAX_LOGS_PER_MODULE = 10;
var moduleLogCounts = {};

function sendRoutedLog(level, module, message, audience, devDetail) {
  if (!moduleLogCounts[module]) moduleLogCounts[module] = 0;
  if (moduleLogCounts[module] >= MAX_LOGS_PER_MODULE) return;
  if (module !== '系统' && moduleLogCounts[module] === MAX_LOGS_PER_MODULE - 1) {
    moduleLogCounts[module]++;
    send({ type: 'log', level: 'info', module: module, message: message + ' (后续日志已静默)', audience: audience || 'dev', dev_detail: devDetail || '' });
    return;
  }
  moduleLogCounts[module]++;
  send({ type: 'log', level: level, module: module, message: message, audience: audience || 'dev', dev_detail: devDetail || '' });
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
  sendDevLog(level, module, message);
}

// 发送开发日志到文件，不进入用户日志窗口
function sendLogFile(level, module, message) {
  send({ type: 'log_file', level: level, module: module, message: message, audience: 'dev' });
}

function sendStatus(feature, enabled) {
  send({ type: 'status', feature: feature, enabled: enabled });
}

var _gameAssemblyCache = null;
var _gameAssemblyLogged = false;

function getGameAssembly() {
  try {
    if (_gameAssemblyCache) return _gameAssemblyCache;
    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) {
      sendDevLog('error', '系统', '未找到 GameAssembly.dll', 'GameAssembly.dll not found');
      return null;
    }
    _gameAssemblyCache = mod;
    if (!_gameAssemblyLogged) {
      _gameAssemblyLogged = true;
      sendDevLog('info', '系统', 'GameAssembly.dll: base=' + mod.base + ' size=' + mod.size, 'GameAssembly module located');
    }
    return mod;
  } catch(e) { sendDevLog('error', '系统', '获取模块失败: ' + e.message, 'getGameAssembly failed: ' + e.message); return null; }
}

function readPtr(addr) {
  try { if (!addr || addr.isNull()) return null; var v = addr.readPointer(); return (v && !v.isNull()) ? v : null; } catch (e) { return null; }
}

function readI32(addr) { try { return addr ? addr.readS32() : null; } catch (e) { return null; } }
function readF32(addr) { try { return addr ? addr.readFloat() : null; } catch (e) { return null; } }
function readU8(addr) { try { return addr ? addr.readU8() : null; } catch (e) { return null; } }

// 模块注册表 - 所有模块通过 modules 对象注册
var modules = {};
var cleanupCallbacks = [];
var cleanupRunning = false;

function registerCleanup(callback) {
  if (typeof callback !== 'function') return false;
  cleanupCallbacks.push(callback);
  return true;
}

function cleanupAll(reason) {
  if (cleanupRunning) {
    return JSON.stringify({ ok: true, skipped: true, reason: 'cleanup_already_running' });
  }

  cleanupRunning = true;
  var result = { ok: true, reason: reason || 'cleanup', modules: [], callbacks: 0, errors: [] };

  try {
    sendLogFile('info', '系统', '[CLEANUP] 开始清理: ' + result.reason);
  } catch (_) {}

  try {
    for (var name in modules) {
      if (!Object.prototype.hasOwnProperty.call(modules, name)) continue;
      var module = modules[name];
      if (!module) continue;

      try {
        if (typeof module.disable === 'function') {
          module.disable();
          result.modules.push(name + '.disable');
        } else if (typeof module.cleanup === 'function') {
          module.cleanup();
          result.modules.push(name + '.cleanup');
        } else if (typeof module.stop === 'function') {
          module.stop();
          result.modules.push(name + '.stop');
        }
      } catch (e) {
        result.ok = false;
        result.errors.push(name + ': ' + (e.message || e));
      }
    }

    for (var i = cleanupCallbacks.length - 1; i >= 0; i--) {
      try {
        cleanupCallbacks[i](result.reason);
        result.callbacks++;
      } catch (e2) {
        result.ok = false;
        result.errors.push('callback#' + i + ': ' + (e2.message || e2));
      }
    }
  } finally {
    cleanupCallbacks = [];
    cleanupRunning = false;
    try {
      sendLogFile('info', '系统', '[CLEANUP] 清理完成: modules=' + result.modules.length + ', callbacks=' + result.callbacks + ', errors=' + result.errors.length);
    } catch (_) {}
  }

  return JSON.stringify(result);
}
