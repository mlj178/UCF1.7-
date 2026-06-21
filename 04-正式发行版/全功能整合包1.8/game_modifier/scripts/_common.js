// _common.js - Frida 公共函数库
// 所有模块共享的基础函数，由 frida_manager 在拼接脚本时首先加载

var MAX_LOGS_PER_MODULE = 10;
var moduleLogCounts = {};

function sendLog(level, module, message) {
  if (!moduleLogCounts[module]) moduleLogCounts[module] = 0;
  if (moduleLogCounts[module] >= MAX_LOGS_PER_MODULE) return;
  if (module !== '系统' && moduleLogCounts[module] === MAX_LOGS_PER_MODULE - 1) {
    moduleLogCounts[module]++;
    send({ type: 'log', level: 'info', module: module, message: message + ' (后续日志已静默)' });
    return;
  }
  moduleLogCounts[module]++;
  send({ type: 'log', level: level, module: module, message: message });
}

// 发送日志到文件（同时显示在控制台）
function sendLogFile(level, module, message) {
  send({ type: 'log_file', level: level, module: module, message: message });
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
      sendLog('error', '系统', '未找到 GameAssembly.dll');
      return null;
    }
    _gameAssemblyCache = mod;
    if (!_gameAssemblyLogged) {
      _gameAssemblyLogged = true;
      sendLog('info', '系统', 'GameAssembly.dll: base=' + mod.base + ' size=' + mod.size);
    }
    return mod;
  } catch(e) { sendLog('error', '系统', '获取模块失败: ' + e.message); return null; }
}

function readPtr(addr) {
  try { if (!addr || addr.isNull()) return null; var v = addr.readPointer(); return (v && !v.isNull()) ? v : null; } catch (e) { return null; }
}

function readI32(addr) { try { return addr ? addr.readS32() : null; } catch (e) { return null; } }
function readF32(addr) { try { return addr ? addr.readFloat() : null; } catch (e) { return null; } }
function readU8(addr) { try { return addr ? addr.readU8() : null; } catch (e) { return null; } }

// 模块注册表 - 所有模块通过 modules 对象注册
var modules = {};
