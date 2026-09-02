// Local helpers for this feature only.
var modules = {};
var __localMaxLogsPerModule = 10;
var __localModuleLogCounts = {};

function sendRoutedLog(level, module, message, audience, devDetail) {
  try {
    if (!__localModuleLogCounts[module]) __localModuleLogCounts[module] = 0;
    if (__localModuleLogCounts[module] >= __localMaxLogsPerModule) return;
    if (module !== '??' && __localModuleLogCounts[module] === __localMaxLogsPerModule - 1) {
      __localModuleLogCounts[module]++;
      send({ type: 'log', level: 'info', module: module, message: message + ' (???????)', audience: audience || 'dev', dev_detail: devDetail || '' });
      return;
    }
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
  sendDevLog(level, module, message);
}

function sendLogFile(level, module, message) {
  try { send({ type: 'log_file', level: level, module: module, message: message, audience: 'dev' }); } catch (_) {}
}

function sendStatus(feature, enabled) {
  try { send({ type: 'status', feature: feature, enabled: enabled }); } catch (_) {}
}

var __localGameAssemblyCache = null;
var __localGameAssemblyLogged = false;

function getGameAssembly() {
  try {
    if (__localGameAssemblyCache) return __localGameAssemblyCache;
    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) {
      sendDevLog('error', '??', '??? GameAssembly.dll', 'GameAssembly.dll not found');
      return null;
    }
    __localGameAssemblyCache = mod;
    if (!__localGameAssemblyLogged) {
      __localGameAssemblyLogged = true;
      sendDevLog('info', '??', 'GameAssembly.dll: base=' + mod.base + ' size=' + mod.size, 'GameAssembly module located');
    }
    return mod;
  } catch (e) {
    sendDevLog('error', '??', '??????: ' + e.message, 'getGameAssembly failed: ' + e.message);
    return null;
  }
}

function readPtr(addr) {
  try { if (!addr || addr.isNull()) return null; var v = addr.readPointer(); return (v && !v.isNull()) ? v : null; } catch (_) { return null; }
}

function readI32(addr) { try { return addr ? addr.readS32() : null; } catch (_) { return null; } }
function readF32(addr) { try { return addr ? addr.readFloat() : null; } catch (_) { return null; } }
function readU8(addr) { try { return addr ? addr.readU8() : null; } catch (_) { return null; } }

var __localCleanupCallbacks = [];
function registerCleanup(callback) {
  if (typeof callback !== 'function') return false;
  __localCleanupCallbacks.push(callback);
  return true;
}

// speed_gun.js - 射速变快 + 连狙 — 终极武器修改
// 10个Hook点：动画加速10x + 清除射击间隔 + 半自动→全自动 + 狙击镜不关闭 + RPG特殊处理 + 后坐力清零 + 扩散归零

modules.speedgun = (function() {
  // ===== 配置与运行状态 =====
  var enabled = false;
  var hooks = [];
  var isMyWeaponFn = null;
  var getCharAnim = null;
  var setAnimSpeed = null;
  var rpgAnimSpeedFn = null;
  var grenadeAnimSpeedFn = null;
  var classGetNameFn = null;
  var componentGetTransformFn = null;
  var transformGetForwardFn = null;
  var brainGetOutputCameraFn = null;
  var scopeCameraTransform = null;
  var scopeRayDirectionBuffer = null;
  var scopeRayCorrectionLastLogAt = 0;
  var scopeRayCorrectionLastWarnAt = 0;
  var isPlayerShooting = false;
  var pendingAcquiredWeapons = [];
  var acquiredWeaponRetryFrames = 3;
  var RVA = {
    ModeBase_Update: 0xAF6A00
  };

  // ===== 指针与类型工具 =====
  function safeReadPointer(basePtr, offset) {
    try {
      if (!basePtr || basePtr.isNull()) return null;
      var value = basePtr.add(offset).readPointer();
      return (value && !value.isNull()) ? value : null;
    } catch(e) {
      return null;
    }
  }

  function getObjectClassName(object) {
    try {
      if (!classGetNameFn || !object || object.isNull()) return null;
      var klass = object.readPointer();
      if (!klass || klass.isNull()) return null;
      var name = classGetNameFn(klass);
      return (name && !name.isNull()) ? name.readUtf8String() : null;
    } catch(e) {
      return null;
    }
  }

  // ===== 武器数据写入 =====
  function applyGunDataSpeed(weapon, requireGrenadeGun) {
    try {
      var data = safeReadPointer(weapon, 0x68);
      var gunData = safeReadPointer(weapon, 0xEC);
      if (!data || !gunData || !gunData.equals(data)) return false;
      if (requireGrenadeGun === true && getObjectClassName(data) !== 'WD_GrenadeGun') return false;

      gunData.add(0xD0).writeFloat(10.0);
      weapon.add(0xF0).writeU8(0);
      weapon.add(0x108).writeS32(0);
      weapon.add(0x110).writeFloat(0.0);
      return true;
    } catch(e) {
      return false;
    }
  }

  function applyRpgDataSpeed(weapon) {
    try {
      var data = safeReadPointer(weapon, 0x68);
      var rpgData = safeReadPointer(weapon, 0xF0);
      if (!data || !rpgData || !rpgData.equals(data)) return false;

      rpgData.add(0xEC).writeFloat(30.0);
      rpgData.add(0xF0).writeFloat(30.0);
      weapon.add(0xF8).writeS32(1);
      return true;
    } catch(e) {
      return false;
    }
  }

  // 只处理 GiveWeapon 明确返回的新武器；数据对象就绪后写入一次，不扫描武器列表。
  function applyAcquiredWeaponSpeed(weapon, weaponId) {
    if (!enabled || !weapon || weapon.isNull()) { sendDevLog('warn', '射速', 'applyAcquired: 前置检查失败 enabled=' + enabled, 'SpeedGun applyAcquired precheck failed'); return false; }
    if (!isMyWeaponFn || !getCharAnim || !setAnimSpeed) { sendDevLog('warn', '射速', 'applyAcquired: NativeFunction未初始化', 'SpeedGun NativeFunction not initialized'); return false; }

    try {
      weapon.readU8();
      if (!isMyWeaponFn(weapon, ptr(0))) { sendDevLog('warn', '射速', 'applyAcquired: isMyWeapon=false weaponId=' + weaponId, 'SpeedGun skipped non-local weapon'); return false; }

      var data = safeReadPointer(weapon, 0x68);
      if (!data) { sendDevLog('warn', '射速', 'applyAcquired: data=null weaponId=' + weaponId, 'SpeedGun weapon data pointer is null'); return false; }

      var gunApplied = applyGunDataSpeed(weapon, false);
      var rpgApplied = applyRpgDataSpeed(weapon);
      var applied = gunApplied || rpgApplied;

      if (!applied) { sendDevLog('warn', '射速', 'applyAcquired: 数据写入失败 gun=' + gunApplied + ' rpg=' + rpgApplied + ' weaponId=' + weaponId, 'SpeedGun weapon data write failed'); return false; }

      var anim = getCharAnim(weapon, ptr(0));
      var animValid = anim && !anim.isNull();
      if (animValid) {
        // TEMP TPS jitter test: disable direct 10x visual animation speed.
        // setAnimSpeed(anim, 10.0, ptr(0));
      }
      sendDevLog('info', '射速', 'applyAcquired: 数据写入成功 gun=' + gunApplied + ' rpg=' + rpgApplied + ' anim=' + animValid + ' weaponId=' + weaponId);

      // RPG/AT4/Nano AT4 只写 WD_RPG 自身倍率字段，避免公共动画倍率影响第三人称模型。
      if (rpgApplied) {
        sendDevLog('info', '射速', 'applyAcquired: RPG/AT4已写入专属动画倍率 weaponId=' + weaponId);
      } else if (gunApplied && grenadeAnimSpeedFn &&
                 getObjectClassName(data) === 'WD_GrenadeGun') {
        grenadeAnimSpeedFn(weapon, ptr(0));
        sendDevLog('info', '射速', 'applyAcquired: 已调用grenadeAnimSpeedFn weaponId=' + weaponId);
      }
      return true;
    } catch(e) {
      sendDevLog('error', '射速', 'applyAcquired: 异常 weaponId=' + weaponId + ' ' + e.message, 'SpeedGun applyAcquired exception');
      return false;
    }
  }

  function clearAcquiredWeaponTasks() {
    pendingAcquiredWeapons = [];
  }

  // ===== 赋予武器后的延迟应用队列 =====
  function notifyWeaponAcquired(weapon, weaponId) {
    if (!enabled || !weapon || weapon.isNull()) return;

    // 只保留最后一次 GiveWeapon 返回值；双次赋予可能使第一次的对象立即失效。
    pendingAcquiredWeapons = [{
      weapon: weapon,
      weaponId: weaponId,
      delayFrames: 1,
      framesLeft: acquiredWeaponRetryFrames
    }];
    sendDevLog('info', '射速', 'notifyWeaponAcquired: weaponId=' + weaponId + ' delayFrames=1 retryFrames=' + acquiredWeaponRetryFrames);
  }

  function processPendingWeaponSpeed() {
    if (!enabled || pendingAcquiredWeapons.length === 0) return;

    var remaining = [];
    for (var i = 0; i < pendingAcquiredWeapons.length; i++) {
      var task = pendingAcquiredWeapons[i];
      if (!task || !task.weapon || task.weapon.isNull()) {
        sendDevLog('warn', '射速', 'processPending: 任务武器指针无效，已跳过');
        continue;
      }

      if (task.delayFrames > 0) {
        task.delayFrames -= 1;
        remaining.push(task);
        continue;
      }

      if (applyAcquiredWeaponSpeed(task.weapon, task.weaponId)) {
        sendDevLog('info', '射速', 'processPending: 成功应用 weaponId=' + task.weaponId);
        continue;
      }

      task.framesLeft -= 1;
      if (task.framesLeft > 0) remaining.push(task);
    }
    pendingAcquiredWeapons = remaining;
  }

  function installPendingWeaponUpdateHook(base) {
    try {
      hooks.push(Interceptor.attach(base.add(RVA.ModeBase_Update), {
        onEnter: function(args) {
          try {
            processPendingWeaponSpeed();
          } catch(e) {
            sendDevLog('warn', '射速', '处理新武器射速队列失败: ' + e.message);
          }
        }
      }));
      sendDevLog('info', '射速', 'ModeBase.Update 新武器射速队列 Hook 已安装');
    } catch(e) {
      sendDevLog('warn', '射速', 'ModeBase.Update 新武器射速队列 Hook失败: ' + e.message);
    }
  }

  // ===== ScopeSettleProbe（只读开镜稳定探测） =====
  // 该探测不写入候选字段；它仅在本地枪械第一次开火时，对可能承载开镜收束状态的
  // 武器、武器数据和 Recoil 对象做短时间序列采样，以便用实测结果确定后续修改目标。
  var scopeSettleProbeRunId = 0;
  var scopeSettleProbeLastStartAt = 0;
  var scopeSettleProbeLastRecoil = null;
  var pendingScopeSettleWeapon = null;
  var scopeSettleProbeIntervalsMs = [0, 150, 350, 750, 1200, 1800, 2200];

  function scopeSettleProbeFinite(value) {
    return typeof value === 'number' && isFinite(value) && Math.abs(value) < 1000000.0;
  }

  function collectScopeSettleFloatBlock(target, label) {
    var values = {};
    if (!target || target.isNull()) return values;
    for (var offset = 0x10; offset <= 0x240; offset += 4) {
      try {
        var value = target.add(offset).readFloat();
        if (scopeSettleProbeFinite(value)) values[label + '+0x' + offset.toString(16)] = value;
      } catch (_) {}
    }
    return values;
  }

  function discoverScopeSettleObjects(weapon) {
    var objects = [];
    var seen = {};
    for (var offset = 0x10; offset <= 0x240; offset += Process.pointerSize) {
      var candidate = safeReadPointer(weapon, offset);
      if (!candidate) continue;
      var address = candidate.toString();
      if (seen[address]) continue;
      seen[address] = true;
      var className = getObjectClassName(candidate) || 'unknown';
      objects.push({
        pointer: candidate,
        label: 'scopeObject+0x' + offset.toString(16) + ':' + className
      });
    }
    return objects;
  }

  function collectScopeSettleSnapshot(weapon, recoil) {
    var snapshot = {};
    var data = safeReadPointer(weapon, 0x68);
    var gunData = safeReadPointer(weapon, 0xEC);
    var groups = [
      { pointer: weapon, label: 'weapon' },
      { pointer: data, label: 'weaponData' },
      { pointer: gunData && data && gunData.equals(data) ? gunData : null, label: 'gunData' },
      { pointer: recoil, label: 'recoil' }
    ];
    var controllers = discoverScopeSettleObjects(weapon);
    for (var controllerIndex = 0; controllerIndex < controllers.length; controllerIndex++) groups.push(controllers[controllerIndex]);
    for (var i = 0; i < groups.length; i++) {
      var values = collectScopeSettleFloatBlock(groups[i].pointer, groups[i].label);
      for (var key in values) snapshot[key] = values[key];
    }
    return snapshot;
  }

  function reportScopeSettleProbe(run) {
    var paths = {};
    for (var i = 0; i < run.samples.length; i++) {
      var sample = run.samples[i];
      for (var key in sample.values) {
        if (!paths[key]) paths[key] = [];
        paths[key].push({ atMs: sample.atMs, value: sample.values[key] });
      }
    }

    var candidates = [];
    for (var path in paths) {
      var values = paths[path];
      if (values.length < 5) continue;
      var first = values[0].value;
      var last = values[values.length - 1].value;
      var maxAbs = 0.0;
      var descending = 0;
      for (var j = 0; j < values.length; j++) {
        maxAbs = Math.max(maxAbs, Math.abs(values[j].value));
        if (j > 0 && Math.abs(values[j].value) <= Math.abs(values[j - 1].value)) descending++;
      }
      if (maxAbs < 0.001 || descending < 4) continue;
      if (Math.abs(last) > Math.abs(first) * 0.35) continue;
      candidates.push({ path: path, first: first, last: last, descending: descending, values: values });
    }
    candidates.sort(function(a, b) { return Math.abs(b.first - b.last) - Math.abs(a.first - a.last); });
    candidates = candidates.slice(0, 24);

    sendLogFile('info', '射速', 'ScopeSettleProbe run=' + run.id + ' samples=' + run.samples.length + ' candidates=' + candidates.length);
    for (var k = 0; k < candidates.length; k++) {
      var candidate = candidates[k];
      var series = candidate.values.map(function(item) { return item.atMs + 'ms:' + item.value.toFixed(5); }).join(',');
      sendLogFile('info', '射速', 'ScopeSettleProbe candidate ' + candidate.path + ' first=' + candidate.first.toFixed(5) + ' last=' + candidate.last.toFixed(5) + ' series=[' + series + ']');
    }
    if (candidates.length === 0) {
      sendLogFile('warn', '射速', 'ScopeSettleProbe 未在当前对象范围发现归零型字段；请保留本次日志，下一轮将扩大到开镜控制器。');
    }
    sendDevLog('info', '射速', '开镜稳定探测完成：样本 ' + run.samples.length + '，候选字段 ' + candidates.length + ' 个');
  }

  function scheduleScopeSettleProbe(weapon, source, recoil) {
    var now = Date.now();
    if (!weapon || weapon.isNull() || (now - scopeSettleProbeLastStartAt) < 3000) return;
    scopeSettleProbeLastStartAt = now;
    var frozenRecoil = recoil && !recoil.isNull() ? recoil : null;
    var run = { id: ++scopeSettleProbeRunId, startedAt: now, samples: [] };
    sendDevLog('info', '射速', '开镜稳定探测已开始 source=' + (source || 'shoot_fallback') + '：请本次开镜后保持不动约 3 秒');
    scopeSettleProbeIntervalsMs.forEach(function(delayMs) {
      setTimeout(function() {
        try {
          if (!enabled) return;
          run.samples.push({
            atMs: delayMs,
            values: collectScopeSettleSnapshot(weapon, frozenRecoil)
          });
          if (delayMs === scopeSettleProbeIntervalsMs[scopeSettleProbeIntervalsMs.length - 1]) reportScopeSettleProbe(run);
        } catch(e) {
          sendLogFile('warn', '射速', 'ScopeSettleProbe sample failed at ' + delayMs + 'ms: ' + e.message);
        }
      }, delayMs);
    });
  }

  function readScopeRayDirection(retBuffer) {
    try {
      if (!retBuffer || retBuffer.isNull()) return null;
      var direction = {};
      direction.x = retBuffer.add(0x0C).readFloat();
      direction.y = retBuffer.add(0x10).readFloat();
      direction.z = retBuffer.add(0x14).readFloat();
      var length = Math.sqrt(direction.x * direction.x + direction.y * direction.y + direction.z * direction.z);
      if (!scopeSettleProbeFinite(length) || length < 0.00001) return null;
      direction.x /= length;
      direction.y /= length;
      direction.z /= length;
      return direction;
    } catch (_) {
      return null;
    }
  }

  function installScopeSettleZoomMethodHooks(mod) {
    try {
      var domainGetAddr = mod.findExportByName('il2cpp_domain_get');
      var assembliesGetAddr = mod.findExportByName('il2cpp_domain_get_assemblies');
      var assemblyGetImageAddr = mod.findExportByName('il2cpp_assembly_get_image');
      var imageClassCountAddr = mod.findExportByName('il2cpp_image_get_class_count');
      var imageGetClassAddr = mod.findExportByName('il2cpp_image_get_class');
      var classGetMethodsAddr = mod.findExportByName('il2cpp_class_get_methods');
      var methodGetNameAddr = mod.findExportByName('il2cpp_method_get_name');
      var methodGetPointerAddr = mod.findExportByName('il2cpp_method_get_pointer');
      if (!domainGetAddr || !assembliesGetAddr || !assemblyGetImageAddr || !imageClassCountAddr || !imageGetClassAddr || !classGetMethodsAddr || !methodGetNameAddr || !methodGetPointerAddr) {
        sendLogFile('warn', '射速', 'ScopeSettleProbe zoom_method 枚举不可用：缺少 IL2CPP 导出');
        return;
      }

      var il2cpp_domain_get = new NativeFunction(domainGetAddr, 'pointer', []);
      var il2cpp_domain_get_assemblies = new NativeFunction(assembliesGetAddr, 'pointer', ['pointer', 'pointer']);
      var il2cpp_assembly_get_image = new NativeFunction(assemblyGetImageAddr, 'pointer', ['pointer']);
      var il2cpp_image_get_class_count = new NativeFunction(imageClassCountAddr, 'uint32', ['pointer']);
      var il2cpp_image_get_class = new NativeFunction(imageGetClassAddr, 'pointer', ['pointer', 'uint32']);
      var il2cpp_class_get_methods = new NativeFunction(classGetMethodsAddr, 'pointer', ['pointer', 'pointer']);
      var il2cpp_method_get_name = new NativeFunction(methodGetNameAddr, 'pointer', ['pointer']);
      var il2cpp_method_get_pointer = new NativeFunction(methodGetPointerAddr, 'pointer', ['pointer']);
      var assemblyCountPtr = Memory.alloc(4);
      assemblyCountPtr.writeU32(0);
      var assemblies = il2cpp_domain_get_assemblies(il2cpp_domain_get(), assemblyCountPtr);
      var assemblyCount = assemblyCountPtr.readU32();
      var installed = 0;

      for (var assemblyIndex = 0; assemblyIndex < assemblyCount; assemblyIndex++) {
        var image = il2cpp_assembly_get_image(assemblies.add(assemblyIndex * Process.pointerSize).readPointer());
        var classCount = il2cpp_image_get_class_count(image);
        for (var classIndex = 0; classIndex < classCount; classIndex++) {
          var klass = il2cpp_image_get_class(image, classIndex);
          if (!klass || klass.isNull() || !classGetNameFn) continue;
          var classNamePtr = classGetNameFn(klass);
          var className = classNamePtr && !classNamePtr.isNull() ? classNamePtr.readUtf8String() : '';
          if (className !== 'WPN_Gun') continue;

          var iterator = Memory.alloc(Process.pointerSize);
          iterator.writePointer(ptr(0));
          while (true) {
            var method = il2cpp_class_get_methods(klass, iterator);
            if (!method || method.isNull()) break;
            var methodNamePtr = il2cpp_method_get_name(method);
            var methodName = methodNamePtr && !methodNamePtr.isNull() ? methodNamePtr.readUtf8String() : '';
            if (!/zoom/i.test(methodName) || /closezoom/i.test(methodName)) continue;
            var methodPointer = il2cpp_method_get_pointer(method);
            if (!methodPointer || methodPointer.isNull()) continue;
            (function(name, address) {
              hooks.push(Interceptor.attach(address, {
                onEnter: function(args) {
                  try {
                    if (args[0] && !args[0].isNull() && isMyWeaponFn(args[0], ptr(0))) {
                      scheduleScopeSettleProbe(args[0], 'zoom_method:' + name);
                    }
                  } catch (_) {}
                }
              }));
            })(methodName, methodPointer);
            installed++;
            sendLogFile('info', '射速', 'ScopeSettleProbe zoom_method hook installed: WPN_Gun.' + methodName + ' @ ' + methodPointer);
          }
        }
      }
      sendDevLog('info', '射速', 'ScopeSettleProbe 已安装开镜方法 Hook：' + installed + ' 个');
    } catch(e) {
      sendLogFile('warn', '射速', 'ScopeSettleProbe zoom_method 枚举失败: ' + e.message);
    }
  }

  // ===== 开镜即时稳定修正 =====
  // 开镜收束最终体现在 Recoil.GetShootRay 输出的方向上。这里不再猜测中间
  // 计时字段，而是在本地玩家开火的最后一步将方向同步为当前镜头前向量。
  function cacheScopeCamera(brain) {
    try {
      if (!brain || brain.isNull() || !brainGetOutputCameraFn || !componentGetTransformFn) return false;
      var camera = brainGetOutputCameraFn(brain, ptr(0));
      if (!camera || camera.isNull()) return false;
      var transform = componentGetTransformFn(camera, ptr(0));
      if (!transform || transform.isNull()) return false;
      scopeCameraTransform = transform;
      return true;
    } catch (_) {
      return false;
    }
  }

  function readScopeCameraForward() {
    try {
      if (!scopeCameraTransform || scopeCameraTransform.isNull() || !transformGetForwardFn || !scopeRayDirectionBuffer) return null;
      transformGetForwardFn(scopeRayDirectionBuffer, scopeCameraTransform, ptr(0));
      var x = scopeRayDirectionBuffer.readFloat();
      var y = scopeRayDirectionBuffer.add(4).readFloat();
      var z = scopeRayDirectionBuffer.add(8).readFloat();
      var length = Math.sqrt(x * x + y * y + z * z);
      if (!scopeSettleProbeFinite(length) || length < 0.00001) return null;
      return { x: x / length, y: y / length, z: z / length };
    } catch (_) {
      return null;
    }
  }

  function writeScopeRayDirection(retBuffer, direction) {
    try {
      if (!retBuffer || retBuffer.isNull() || !direction) return false;
      retBuffer.add(0x0C).writeFloat(direction.x);
      retBuffer.add(0x10).writeFloat(direction.y);
      retBuffer.add(0x14).writeFloat(direction.z);
      return true;
    } catch (_) {
      return false;
    }
  }

  function applyInstantScopeStability(retBuffer) {
    var forward = readScopeCameraForward();
    var now = Date.now();
    if (!forward) {
      if ((now - scopeRayCorrectionLastWarnAt) >= 3000) {
        scopeRayCorrectionLastWarnAt = now;
        sendLogFile('warn', '射速', 'ScopeSettleCorrection skipped: camera_forward_unavailable');
      }
      return false;
    }
    var applied = writeScopeRayDirection(retBuffer, forward);
    if (applied && (now - scopeRayCorrectionLastLogAt) >= 3000) {
      scopeRayCorrectionLastLogAt = now;
      sendLogFile('info', '射速', 'ScopeSettleCorrection applied: final ray aligned to camera forward');
    }
    return applied;
  }

  // ===== NativeFunction 初始化与状态清理 =====
  function resetNativeFunctions() {
    isMyWeaponFn = null;
    getCharAnim = null;
    setAnimSpeed = null;
    rpgAnimSpeedFn = null;
    grenadeAnimSpeedFn = null;
    classGetNameFn = null;
    componentGetTransformFn = null;
    transformGetForwardFn = null;
    brainGetOutputCameraFn = null;
    scopeCameraTransform = null;
    scopeRayDirectionBuffer = null;
  }

  function initNativeFunctions(base) {
    isMyWeaponFn = new NativeFunction(base.add(0xB6E1D0), "bool", ["pointer", "pointer"]);
    getCharAnim = new NativeFunction(base.add(0xB35310), "pointer", ["pointer", "pointer"]);
    setAnimSpeed = new NativeFunction(base.add(0xAA8C30), "void", ["pointer", "float", "pointer"]);
    rpgAnimSpeedFn = new NativeFunction(base.add(0xB66CA0), "void", ["pointer", "pointer"]);
    grenadeAnimSpeedFn = new NativeFunction(base.add(0xB5F7A0), "void", ["pointer", "pointer"]);
    componentGetTransformFn = new NativeFunction(base.add(0x32CF40), "pointer", ["pointer", "pointer"]);
    transformGetForwardFn = new NativeFunction(base.add(0x3F3F20), "void", ["pointer", "pointer", "pointer"]);
    brainGetOutputCameraFn = new NativeFunction(base.add(0x82CDB0), "pointer", ["pointer", "pointer"]);
    scopeRayDirectionBuffer = Memory.alloc(12);
  }

  function initClassNameFunction(mod) {
    try {
      var classGetNameAddr = mod.findExportByName('il2cpp_class_get_name');
      classGetNameFn = classGetNameAddr
        ? new NativeFunction(classGetNameAddr, "pointer", ["pointer"])
        : null;
    } catch(e) {
      classGetNameFn = null;
    }
  }

  function detachHooks() {
    for (var i = 0; i < hooks.length; i++) {
      try { hooks[i].detach(); } catch(e) {}
    }
    hooks = [];
  }

  function resetRuntimeState() {
    isPlayerShooting = false;
    pendingScopeSettleWeapon = null;
    scopeSettleProbeLastRecoil = null;
    scopeRayCorrectionLastLogAt = 0;
    scopeRayCorrectionLastWarnAt = 0;
    clearAcquiredWeaponTasks();
  }

  // ===== Hook 安装 =====
  function enableFeature() {
      if (enabled) return;
      var mod = getGameAssembly();
      if (!mod) { sendBothLog('error', '射速', '射速连狙暂未就绪，请重新连接游戏后重试', 'SpeedGun GameAssembly.dll not found'); return; }
      var base = mod.base;

      try {
        initNativeFunctions(base);
      } catch(e) {
        resetNativeFunctions();
        sendBothLog('error', '射速', '射速连狙初始化失败，请稍后重试', 'SpeedGun NativeFunction init failed: ' + e.message);
        return;
      }

      initClassNameFunction(mod);
      installPendingWeaponUpdateHook(base);
      installScopeSettleZoomMethodHooks(mod);

      // 1) WPN_Gun.AnimSpeedSetting — 枪械(背包)动画加速（改进：onEnter立即设置）
      try {
        hooks.push(Interceptor.attach(base.add(0xB60B00), {
          onEnter: function(args) {
            this.self = args[0];
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                var anim = getCharAnim(this.self, ptr(0));
                if (!anim.isNull()) {
                  // TEMP TPS jitter test: disable direct 10x visual animation speed.
                  // setAnimSpeed(anim, 10.0, ptr(0));
                }
              }
            } catch(e) {}
          },
          onLeave: function(retVal) {
            if (!this.self) return;
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                var anim = getCharAnim(this.self, ptr(0));
                if (!anim.isNull()) {
                  // TEMP TPS jitter test: disable direct 10x visual animation speed.
                  // setAnimSpeed(anim, 10.0, ptr(0));
                }
              }
            } catch(e) {}
          }
        }));
      } catch(e) { sendDevLog('warn', '射速', 'WPN_Gun.AnimSpeedSetting Hook失败: ' + e.message); }

      // 1.5) WPN_RPG.AnimSpeedSetting — RPG/AT4 动画加速（改进：onEnter立即设置）
      try {
        hooks.push(Interceptor.attach(base.add(0xB66CA0), {
          onEnter: function(args) {
            this.self = args[0];
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                var anim = getCharAnim(this.self, ptr(0));
                if (!anim.isNull()) {
                  // TEMP TPS jitter test: disable direct 10x visual animation speed.
                  // setAnimSpeed(anim, 10.0, ptr(0));
                }
              }
            } catch(e) {}
          },
          onLeave: function(retVal) {
            if (!this.self) return;
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                var anim = getCharAnim(this.self, ptr(0));
                if (!anim.isNull()) {
                  // TEMP TPS jitter test: disable direct 10x visual animation speed.
                  // setAnimSpeed(anim, 10.0, ptr(0));
                }
              }
            } catch(e) {}
          }
        }));
      } catch(e) { sendDevLog('warn', '射速', 'WPN_RPG.AnimSpeedSetting Hook失败: ' + e.message); }

      // 1.6) WPN_GrenadeGun.AnimSpeedSetting — 榴弹枪动画加速
      try {
        hooks.push(Interceptor.attach(base.add(0xB5F7A0), {
          onEnter: function(args) {
            this.self = args[0];
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                var realData = this.self.add(0xEC).readPointer();
                if (!realData.isNull()) {
                  realData.add(0xD0).writeFloat(10.0);
                }
              }
            } catch(e) {}
          },
          onLeave: function(retVal) {
            if (!this.self) return;
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                var anim = getCharAnim(this.self, ptr(0));
                if (!anim.isNull()) {
                  // TEMP TPS jitter test: disable direct 10x visual animation speed.
                  // setAnimSpeed(anim, 10.0, ptr(0));
                }
              }
            } catch(e) {}
          }
        }));
      } catch(e) { sendDevLog('warn', '射速', 'WPN_GrenadeGun.AnimSpeedSetting Hook失败: ' + e.message); }

      // 1.7) 在原游戏 Deploy 调用 AnimSpeedSetting/AnimatorInit 前写入特殊武器倍率。
      // 不保存武器指针，不在 onLeave 访问对象，避免旧版长生命周期任务的失效指针风险。
      try {
        hooks.push(Interceptor.attach(base.add(0xB67030), {
          onEnter: function(args) {
            this.self = args[0];
            try {
              if (this.self && !this.self.isNull() && isMyWeaponFn(this.self, ptr(0))) {
                applyRpgDataSpeed(this.self);
              }
            } catch(e) {}
          },
          onLeave: function(retVal) {
            if (!this.self) return;
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                sendDevLog('info', '射速', 'WPN_RPG.Deploy onLeave → notifyWeaponAcquired(3494)');
                notifyWeaponAcquired(this.self, 3494);
              }
            } catch(e) {}
          }
        }));
      } catch(e) { sendDevLog('warn', '射速', 'WPN_RPG.Deploy Hook失败: ' + e.message); }

      // 1.8) 'WPN_RPG.Fire' — RPG/AT4/Nano AT4 开火当帧补写专属动画倍率。
      try {
        hooks.push(Interceptor.attach(base.add(0xB670A0), {
          onEnter: function(args) {
            this.self = args[0];
            try {
              if (this.self && !this.self.isNull() && isMyWeaponFn(this.self, ptr(0))) {
                applyRpgDataSpeed(this.self);
              }
            } catch(e) {}
          }
        }));
      } catch(e) { sendDevLog('warn', '射速', 'RPG Fire Hook失败: ' + e.message); }

      try {
        hooks.push(Interceptor.attach(base.add(0xB61E60), {
          onEnter: function(args) {
            this.self = args[0];
            try {
              if (this.self && !this.self.isNull() && isMyWeaponFn(this.self, ptr(0))) {
                applyGunDataSpeed(this.self, true);
              }
            } catch(e) {}
          },
          onLeave: function(retVal) {
            if (!this.self) return;
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                sendDevLog('info', '射速', 'WPN_GrenadeGun.Deploy onLeave → notifyWeaponAcquired(2978)');
                notifyWeaponAcquired(this.self, 2978);
              }
            } catch(e) {}
          }
        }));
      } catch(e) { sendDevLog('warn', '射速', 'WPN_GrenadeGun.Deploy Hook失败: ' + e.message); }

      // 2) GunShoot — 清除射击间隔 + 半自动 => 全自动（改进：onEnter立即修改）
      try {
        hooks.push(Interceptor.attach(base.add(0xB624C0), {
          onEnter: function(args) {
            this.self = args[0];
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                isPlayerShooting = true;
                pendingScopeSettleWeapon = this.self;
                scopeSettleProbeLastRecoil = null;
                this.self.add(0xF0).writeU8(0);
                this.self.add(0x110).writeFloat(0.0);
                this.self.add(0x108).writeS32(0);
                var anim = getCharAnim(this.self, ptr(0));
                if (!anim.isNull()) {
                  // TEMP TPS jitter test: disable direct 10x visual animation speed.
                  // setAnimSpeed(anim, 10.0, ptr(0));
                }
                var realData = this.self.add(0xEC).readPointer();
                if (!realData.isNull()) {
                  realData.add(0x1BC).writeU8(0);
                }
              }
            } catch(e) {}
          },
          onLeave: function(retVal) {
            if (!this.self) return;
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                this.self.add(0x110).writeFloat(0.0);
                this.self.add(0x108).writeS32(0);
              }
            } catch(e) {}
            if (pendingScopeSettleWeapon && pendingScopeSettleWeapon.equals(this.self)) {
              scheduleScopeSettleProbe(this.self, 'shoot_fallback', scopeSettleProbeLastRecoil);
              pendingScopeSettleWeapon = null;
            }
            isPlayerShooting = false;
          }
        }));
      } catch(e) { sendDevLog('warn', '射速', 'GunShoot Hook失败: ' + e.message); }

      // 2.05) Brain.PushStateToUnityCamera — 缓存正在输出的本地镜头，用作最终弹道方向。
      try {
        hooks.push(Interceptor.attach(base.add(0x82B750), {
          onEnter: function(args) { this.brain = args[0]; },
          onLeave: function() { cacheScopeCamera(this.brain); }
        }));
      } catch(e) { sendDevLog('warn', '射速', '镜头方向缓存 Hook失败: ' + e.message); }

      // 2.1) Recoil.GetShootRay — 只保存本地本次射击的 Recoil 指针，供 ScopeSettleProbe 读取。
      try {
        hooks.push(Interceptor.attach(base.add(0xB195C0), {
          onEnter: function(args) {
            try {
              this.retBuffer = args[0];
              this.localShot = isPlayerShooting;
              if (isPlayerShooting && args[1] && !args[1].isNull()) {
                scopeSettleProbeLastRecoil = args[1];
                if (pendingScopeSettleWeapon) {
                  scheduleScopeSettleProbe(pendingScopeSettleWeapon, 'shoot_ray', args[1]);
                  pendingScopeSettleWeapon = null;
                }
              }
            } catch (_) {}
          },
          onLeave: function() {
            if (!this.localShot) return;
            var originalDirection = readScopeRayDirection(this.retBuffer);
            var corrected = applyInstantScopeStability(this.retBuffer);
            var direction = readScopeRayDirection(this.retBuffer);
            if (!direction) return;
            sendLogFile('info', '射速', 'ScopeSettleProbe final_ray corrected=' + corrected + ' original=' + (originalDirection ? originalDirection.x.toFixed(6) + ',' + originalDirection.y.toFixed(6) + ',' + originalDirection.z.toFixed(6) : 'unavailable') + ' final=' + direction.x.toFixed(6) + ',' + direction.y.toFixed(6) + ',' + direction.z.toFixed(6));
          }
        }));
      } catch(e) { sendDevLog('warn', '射速', 'Recoil.GetShootRay ScopeSettleProbe Hook失败: ' + e.message); }

      // 2.5) WPN_Gun.get_isSemiGun — 半自动→全自动
      try {
        hooks.push(Interceptor.attach(base.add(0xB63AD0), {
          onLeave: function(retVal) { retVal.replace(0); }
        }));
      } catch(e) { sendDevLog('warn', '射速', 'get_isSemiGun Hook失败: ' + e.message); }

      // 2.6) WPN_Gun.CloseZoom — 狙击镜不关闭（新增：连狙功能）
      try {
        hooks.push(Interceptor.attach(base.add(0xB60F00), {
          onEnter: function(args) {
            this.self = args[0];
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                args[1] = ptr(0);
              }
            } catch(e) {}
          }
        }));
      } catch(e) { sendDevLog('warn', '射速', 'CloseZoom Hook失败: ' + e.message); }

      // 2.7) Player.TryPickUpWeapon — 捡武器时立即设置动画速度（新增：补给箱处理）
      try {
        hooks.push(Interceptor.attach(base.add(0xB53F50), {
          onEnter: function(args) {
            this.wpn = args[1];
          },
          onLeave: function(retVal) {
            if (!this.wpn) return;
            if ((retVal.toUInt32() & 0xFF) === 0) return;
            try {
              if (isMyWeaponFn(this.wpn, ptr(0))) {
                var anim = getCharAnim(this.wpn, ptr(0));
                if (!anim.isNull()) {
                  // TEMP TPS jitter test: disable direct 10x visual animation speed.
                  // setAnimSpeed(anim, 10.0, ptr(0));
                }
                var data = this.wpn.add(0x68).readPointer();
                if (!data.isNull()) {
                  var wpnClass = data.add(0x10).readU32();
                  if (wpnClass === 5) {
                    var realData = this.wpn.add(0xEC).readPointer();
                    if (!realData.isNull()) {
                      realData.add(0xD0).writeFloat(10.0);
                    }
                  }
                  if (wpnClass === 1 || wpnClass === 2) {
                    var realData = this.wpn.add(0xEC).readPointer();
                    if (!realData.isNull()) {
                      realData.add(0x1BC).writeU8(0);
                    }
                  }
                }
              }
            } catch(e) {}
          }
        }));
      } catch(e) { sendDevLog('warn', '射速', 'TryPickUpWeapon Hook失败: ' + e.message); }

      // 3) WPN_Gun.OnGenerateFromOwner — 补给箱枪械创建时加速
      try {
        hooks.push(Interceptor.attach(base.add(0xB62900), {
          onEnter: function(args) { this.self = args[0]; },
          onLeave: function(retVal) {
            if (!this.self) return;
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                var anim = getCharAnim(this.self, ptr(0));
                if (!anim.isNull()) {
                  // TEMP TPS jitter test: disable direct 10x visual animation speed.
                  // setAnimSpeed(anim, 10.0, ptr(0));
                }
              }
            } catch(e) {}
          }
        }));
      } catch(e) { sendDevLog('warn', '射速', 'OnGenerateFromOwner Hook失败: ' + e.message); }

      // 4) WPN_RPG.OnGenerateFromOwner — 补给箱RPG/AT4创建时加速
      try {
        hooks.push(Interceptor.attach(base.add(0xB67740), {
          onEnter: function(args) { this.self = args[0]; },
          onLeave: function(retVal) {
            if (!this.self) return;
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                var anim = getCharAnim(this.self, ptr(0));
                if (!anim.isNull()) {
                  // TEMP TPS jitter test: disable direct 10x visual animation speed.
                  // setAnimSpeed(anim, 10.0, ptr(0));
                }
                var realData = this.self.add(0xF0).readPointer();
                if (!realData.isNull()) {
                  realData.add(0xF0).writeFloat(30.0);
                  realData.add(0xEC).writeFloat(30.0);
                }
              }
            } catch(e) {}
          }
        }));
      } catch(e) { sendDevLog('warn', '射速', 'RPG OnGenerateFromOwner Hook失败: ' + e.message); }

      // 5) WPN_RPG.OnFireBtnPressed — RPG/AT4 半自动绕过
      try {
        hooks.push(Interceptor.attach(base.add(0xB67700), {
          onEnter: function(args) { this.self = args[0]; },
          onLeave: function(retVal) {
            if (!this.self) return;
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                this.self.add(0xF8).writeS32(1);
                var realData = this.self.add(0xF0).readPointer();
                if (!realData.isNull()) {
                  realData.add(0xF0).writeFloat(30.0);
                  realData.add(0xEC).writeFloat(30.0);
                }
              }
            } catch(e) {}
          }
        }));
      } catch(e) { sendDevLog('warn', '射速', 'RPG OnFireBtnPressed Hook失败: ' + e.message); }

      // 6) Recoil.OnGunShot — 清零后坐力
      try {
        hooks.push(Interceptor.attach(base.add(0xB19980), {
          onEnter: function(args) { this.self = args[0]; },
          onLeave: function(retVal) {
            if (!isPlayerShooting || !this.self) return;
            this.self.add(0x68).writeFloat(0.0);
            this.self.add(0x6C).writeFloat(0.0);
            this.self.add(0x70).writeFloat(0.0);
            this.self.add(0x74).writeFloat(0.0);
            this.self.add(0xA8).writeS32(0);
          }
        }));
      } catch(e) { sendDevLog('warn', '射速', 'Recoil.OnGunShot Hook失败: ' + e.message); }

      // 7) Recoil.GetCurrentPerturb — 强制 0 扩散
      try {
        hooks.push(Interceptor.attach(base.add(0xB19420), {
          onLeave: function(retVal) { retVal.replace(0.0); }
        }));
      } catch(e) { sendDevLog('warn', '射速', 'Recoil.GetCurrentPerturb Hook失败: ' + e.message); }

      enabled = true;
      sendDevLog('success', '射速', '射速变快已启用');
      sendStatus('speedgun', true);
  }

  // ===== 功能开关与 RPC 边界 =====
  function disableFeature() {
      if (!enabled) return;
      detachHooks();
      resetRuntimeState();
      resetNativeFunctions();
      enabled = false;
      sendDevLog('info', '射速', '射速变快已禁用');
      sendStatus('speedgun', false);
  }

  // 由武器赋予模块的 ModeBase.Update 在主线程下一帧处理。
  function clearRoomState() {
    resetRuntimeState();
  }

  function isEnabled() {
    return enabled;
  }

  return {
    enable: enableFeature,
    disable: disableFeature,
    clearRoomState: clearRoomState,
    notifyWeaponAcquired: notifyWeaponAcquired,
    processPendingWeaponSpeed: processPendingWeaponSpeed,
    isEnabled: isEnabled
  };
})();


// Plugin RPC wrapper. Hook internals above are copied unchanged from the legacy script.
var __pluginFeatureId = "speedgun";
var __pluginModuleName = "speedgun";
var __pluginEnabled = false;
var __pluginConfig = {};

function __pluginModule() {
  return modules[__pluginModuleName];
}

function __pluginApplyConfig(config) {
  if (config) {
    for (var key in config) {
      if (Object.prototype.hasOwnProperty.call(config, key)) __pluginConfig[key] = config[key];
    }
  }
  var module = __pluginModule();
  if (!module) return { ok: false, reason: 'module_not_loaded', config: __pluginConfig };

  return { ok: true, config: __pluginConfig };
}

function __pluginEnable(config) {
  if (config) __pluginApplyConfig(config);
  var module = __pluginModule();
  if (!module || typeof module.enable !== 'function') return { ok: false, reason: 'enable_missing' };
  var result = module.enable();
  __pluginEnabled = true;
  return result || { ok: true, enabled: true };
}

function __pluginDisable() {
  var module = __pluginModule();
  if (module && typeof module.disable === 'function') module.disable();
  __pluginEnabled = false;
  return { ok: true, enabled: false };
}

function __pluginStatus() {
  var module = __pluginModule();
  var stats = {};
  try {
    if (module && typeof module.getstatus === 'function') stats = module.getstatus();
    else if (module && typeof module.getStatus === 'function') stats = module.getStatus();
  } catch (_) {}
  return { enabled: __pluginEnabled, config: __pluginConfig, stats: stats };
}

function __pluginNotifyWeaponAcquired(payload) {
  payload = payload || {};
  var module = __pluginModule();
  if (!module || typeof module.notifyWeaponAcquired !== 'function') {
    return { ok: false, reason: 'notify_missing' };
  }
  if (!__pluginEnabled) {
    return { ok: false, reason: 'disabled' };
  }
  if (!payload.weaponPtr) {
    return { ok: false, reason: 'missing_weapon_ptr' };
  }
  var weapon = ptr(payload.weaponPtr);
  module.notifyWeaponAcquired(weapon, payload.weaponId || 0);
  return { ok: true, queued: true };
}

function __pluginCleanup(payload) {
  __pluginDisable();
  return { ok: true, reason: payload && payload.reason ? payload.reason : 'cleanup' };
}

rpc.exports = {
  enable: __pluginEnable,
  disable: __pluginDisable,
  setConfig: __pluginApplyConfig,
  status: __pluginStatus,
  notifyWeaponAcquired: __pluginNotifyWeaponAcquired,
  cleanup: __pluginCleanup
};

rpc.exports.notifyweaponacquired = rpc.exports.notifyWeaponAcquired;

