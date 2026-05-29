// ============================================================
// weapon-hero-giver-fixed-v2.js - 武器赋予脚本（修复版v6）
//
// 修复历史:
//   v2: 使用有效的 MethodInfo 指针
//   v3: 改用直接原生调用，但缺少 cdecl 声明导致崩溃
//   v4: 修复 ABI 名称 cdecl->mscdecl，但仍然 access violation 0x8
//   v5: 根因修复 - GiveWeapon 必须在游戏主线程执行
//       原因: GiveWeapon 内部调用 Unity API（Instantiate/GetComponent）
//       这些 API 只能在主线程调用，Frida RPC 运行在独立线程
//       方案: Hook ModeBase$$Update（主线程每帧调用），通过任务队列
//       将 GiveWeapon 调度到主线程执行
//   v6: 添加复活自动恢复武器功能
//
// IDA确认的函数签名:
//   Weapon_o *__cdecl GameManager__GiveWeapon(
//       Player_o *player, int32_t weaponIndex,
//       bool autoGiveUp, bool autoSelect,
//       const MethodInfo *method)
//   void __cdecl ModeBase__Update(
//       ModeBase_o *__this, const MethodInfo *method)
// ============================================================

(function() {
  'use strict';

  var MAX_LOGS_PER_MODULE = 100;
  var moduleLogCounts = {};

  function log(level, module, message) {
    if (!moduleLogCounts[module]) moduleLogCounts[module] = 0;
    if (moduleLogCounts[module] >= MAX_LOGS_PER_MODULE) return;
    moduleLogCounts[module]++;
    var fullMsg = '[' + module + '] ' + message;
    console.log('[' + level + '] ' + fullMsg);
    try {
      send({ type: 'log', level: level, module: module, message: message });
    } catch(e) {}
  }

  var _gameAssembly = null;

  function getGameAssembly() {
    if (_gameAssembly) return _gameAssembly;
    try {
      var mod = Process.findModuleByName('GameAssembly.dll');
      if (!mod) {
        log('error', '系统', '未找到 GameAssembly.dll');
        return null;
      }
      _gameAssembly = mod;
      log('success', '系统', 'GameAssembly.dll 基址: ' + mod.base);
      return mod;
    } catch(e) {
      log('error', '系统', '获取模块失败: ' + e.message);
      return null;
    }
  }

  var RVA = {
    GameManager_TypeInfo: 0x0E2933C,
    ModeBase_TypeInfo: 0x0E2CC54,
    GiveWeapon: 0xAFB390,
    GetWpnName: 0xAFB1F0,
    ModeBase_Update: 0xAF6A00,
    Player_OnEntityDeath: 0xB51210,
    Player_Spawn: 0xB53760,
    Entity_get_isDead: 0xB400E0,
    Player_get_isMyPlayer: 0xB55FD0,
};

  var OFF = {
    Klass_staticFields: 0x5C,
    GM_myPlayer: 0x00,
  };

  function readPtr(addr) {
    try {
      if (!addr || addr.isNull()) return null;
      var v = addr.readPointer();
      return (v && !v.isNull()) ? v : null;
    } catch(e) {
      return null;
    }
  }

  var _giveWeaponFunc = null;
  var _il2cpp_runtime_invoke = null;
  var _giveWeaponMethodInfo = null;
  var _initialized = false;
  var _hookInstalled = false;
  var _respawnHookInstalled = false;
  var _spawnHookInstalled = false;

  var _pendingTasks = [];
  var _taskResults = {};
  var _taskIdCounter = 0;

  var _isPlayerDead = false;
  var _lastCheckFrame = 0;
  var _cachedMyPlayer = null;
  var _checkAliveInterval = 30;
  var _waitingForRespawnWeaponId = null;
  var _waitingForRespawnWeaponName = null;

  function getGameManagerKlass() {
    try {
      var mod = getGameAssembly();
      if (!mod) return null;
      var typeInfoSlot = mod.base.add(RVA.GameManager_TypeInfo);
      return readPtr(typeInfoSlot);
    } catch(e) {
      log('error', 'MethodInfo', '获取GameManager klass失败: ' + e.message);
      return null;
    }
  }

  function getGiveWeaponMethodInfo() {
    if (_giveWeaponMethodInfo) return _giveWeaponMethodInfo;

    var mod = getGameAssembly();
    if (!mod) return null;

    var klass = getGameManagerKlass();
    if (!klass) {
      log('error', 'MethodInfo', '无法获取GameManager klass');
      return null;
    }

    try {
      var exportAddr = mod.getExportByName('il2cpp_class_get_method_from_name');
      if (!exportAddr) {
        log('error', 'MethodInfo', '未找到il2cpp_class_get_method_from_name导出');
        return null;
      }

      var getClassMethod = new NativeFunction(exportAddr, 'pointer', ['pointer', 'pointer', 'uint32']);
      var methodName = Memory.allocUtf8String('GiveWeapon');
      var methodInfo = getClassMethod(klass, methodName, 4);

      if (methodInfo && !methodInfo.isNull()) {
        _giveWeaponMethodInfo = methodInfo;
        log('success', 'MethodInfo', '成功获取GiveWeapon MethodInfo: ' + methodInfo);
        return methodInfo;
      }

      log('error', 'MethodInfo', 'il2cpp_class_get_method_from_name返回null');
      return null;

    } catch(e) {
      log('error', 'MethodInfo', '获取MethodInfo失败: ' + e.message);
      return null;
    }
  }

  function initNativeFunctions() {
    if (_initialized) return true;

    var mod = getGameAssembly();
    if (!mod) {
      log('error', 'Init', '无法获取 GameAssembly.dll');
      return false;
    }
    var base = mod.base;

    try {
      var exportInvoke = mod.getExportByName('il2cpp_runtime_invoke');
      if (!exportInvoke) {
        log('error', 'Init', '未找到 il2cpp_runtime_invoke');
        return false;
      }
      _il2cpp_runtime_invoke = new NativeFunction(
        exportInvoke,
        'pointer',
        ['pointer', 'pointer', 'pointer', 'pointer']
      );
      log('success', 'Init', 'il2cpp_runtime_invoke 初始化成功');
    } catch(e) {
      log('error', 'Init', 'il2cpp_runtime_invoke 初始化失败: ' + e.message);
      return false;
    }

    try {
      _giveWeaponFunc = new NativeFunction(
        base.add(RVA.GiveWeapon),
        'pointer',
        ['pointer', 'int', 'int', 'int', 'pointer'],
        'mscdecl'
      );
      log('success', 'Init', 'GiveWeapon NativeFunction 初始化成功 (mscdecl)');
    } catch(e) {
      log('warn', 'Init', 'GiveWeapon 直接调用初始化失败: ' + e.message);
      _giveWeaponFunc = null;
    }

    _initialized = true;
    return true;
  }

  function getMyPlayer() {
    try {
      var mod = getGameAssembly();
      if (!mod) return null;
      var base = mod.base;

      var typeInfoSlot = base.add(RVA.GameManager_TypeInfo);
      var klass = readPtr(typeInfoSlot);
      if (!klass) return null;

      var staticFields = readPtr(klass.add(OFF.Klass_staticFields));
      if (!staticFields) return null;

      var myPlayer = readPtr(staticFields.add(OFF.GM_myPlayer));
      if (!myPlayer) return null;

      return myPlayer;

    } catch(e) {
      log('error', 'Player', '异常: ' + e.message);
      return null;
    }
  }

  function checkGameManagerInit() {
    try {
      var mod = getGameAssembly();
      if (!mod) return false;

      var typeInfoSlot = mod.base.add(RVA.GameManager_TypeInfo);
      var klass = readPtr(typeInfoSlot);
      if (!klass) return false;

      var staticFields = readPtr(klass.add(OFF.Klass_staticFields));
      if (!staticFields) return false;

      return true;

    } catch(e) {
      return false;
    }
  }

  function isPlayerDead(player) {
    try {
      var mod = getGameAssembly();
      if (!mod) return false;

      var funcAddr = mod.base.add(RVA.Entity_get_isDead);
      var isDeadFunc = new NativeFunction(funcAddr, 'int', ['pointer', 'pointer'], 'mscdecl');
      var result = isDeadFunc(player, ptr(0));
      return result !== 0;
    } catch(e) {
      return false;
    }
  }

  function isMyPlayer(player) {
    try {
      var mod = getGameAssembly();
      if (!mod) return false;

      var funcAddr = mod.base.add(RVA.Player_get_isMyPlayer);
      var isMyPlayerFunc = new NativeFunction(funcAddr, 'int', ['pointer', 'pointer'], 'mscdecl');
      var result = isMyPlayerFunc(player, ptr(0));
      return result !== 0;
    } catch(e) {
      return false;
    }
  }

  function executeGiveWeaponOnMainThread(wpnId, giveUpInt, selectInt) {
    var myPlayer = getMyPlayer();
    if (!myPlayer) {
      log('error', 'Weapon', '主线程: 无法获取玩家实例');
      return false;
    }
    log('success', 'Weapon', '主线程: 获取玩家实例: ' + myPlayer);

    if (_giveWeaponFunc) {
      try {
        var methodInfo = getGiveWeaponMethodInfo();
        var methodArg = methodInfo ? methodInfo : ptr(0);

        log('info', 'Weapon', '主线程: 直接调用 GiveWeapon(player=' + myPlayer + ', wpnId=' + wpnId + ', giveUp=' + giveUpInt + ', select=' + selectInt + ', method=' + methodArg + ')');

        var weapon = _giveWeaponFunc(myPlayer, wpnId, giveUpInt, selectInt, methodArg);

        if (weapon && !weapon.isNull()) {
          log('success', 'Weapon', '主线程直接调用成功! weapon=' + weapon);
          return true;
        } else {
          log('error', 'Weapon', '主线程直接调用返回null');
          return false;
        }
      } catch(e) {
        log('error', 'Weapon', '主线程直接调用异常: ' + e.message);
      }
    }

    if (_il2cpp_runtime_invoke) {
      try {
        var methodInfo = getGiveWeaponMethodInfo();
        if (!methodInfo) {
          log('error', 'Weapon', '主线程: 无法获取MethodInfo');
          return false;
        }

        var playerBuf = Memory.alloc(Process.pointerSize);
        playerBuf.writePointer(myPlayer);

        var wpnIdBuf = Memory.alloc(4);
        wpnIdBuf.writeS32(wpnId);

        var giveUpBuf = Memory.alloc(4);
        giveUpBuf.writeU8(giveUpInt);

        var selectBuf = Memory.alloc(4);
        selectBuf.writeU8(selectInt);

        var params = Memory.alloc(Process.pointerSize * 4);
        params.writePointer(playerBuf);
        params.add(Process.pointerSize).writePointer(wpnIdBuf);
        params.add(Process.pointerSize * 2).writePointer(giveUpBuf);
        params.add(Process.pointerSize * 3).writePointer(selectBuf);

        var exc = Memory.alloc(Process.pointerSize);
        exc.writePointer(ptr(0));

        log('info', 'Weapon', '主线程: il2cpp_runtime_invoke 调用中...');

        var weapon = _il2cpp_runtime_invoke(methodInfo, ptr(0), params, exc);

        var excVal = exc.readPointer();
        if (!excVal.isNull()) {
          log('error', 'Weapon', '主线程 IL2CPP 异常! exc=' + excVal);
          return false;
        }

        if (weapon && !weapon.isNull()) {
          log('success', 'Weapon', '主线程 invoke 成功! weapon=' + weapon);
          return true;
        } else {
          log('error', 'Weapon', '主线程 invoke 返回null');
          return false;
        }
      } catch(e) {
        log('error', 'Weapon', '主线程 invoke 异常: ' + e.message);
        return false;
      }
    }

    log('error', 'Weapon', '无可用的调用方式');
    return false;
  }

  function installMainThreadHook() {
    if (_hookInstalled) return true;

    var mod = getGameAssembly();
    if (!mod) {
      log('error', 'Hook', '无法获取 GameAssembly.dll');
      return false;
    }

    var updateAddr = mod.base.add(RVA.ModeBase_Update);

    try {
      Interceptor.attach(updateAddr, {
        onEnter: function(args) {
          var currentFrame = _lastCheckFrame + 1;
          _lastCheckFrame = currentFrame;

          while (_pendingTasks.length > 0) {
            var task = _pendingTasks.shift();
            log('info', 'Hook', '主线程拾取任务: taskId=' + task.id + ', wpnId=' + task.wpnId);

            var result = executeGiveWeaponOnMainThread(task.wpnId, task.giveUp, task.select);
            _taskResults[task.id] = result;

            send({
              type: 'giveWeaponResult',
              taskId: task.id,
              success: result
            });
          }

          if (_cachedMyPlayer && currentFrame % _checkAliveInterval === 0) {
            checkPlayerRespawn();
          }
        }
      });

      _hookInstalled = true;
      log('success', 'Hook', 'ModeBase$$Update Hook 安装成功（主线程调度）');
      return true;

    } catch(e) {
      log('error', 'Hook', 'Hook 安装失败: ' + e.message);
      return false;
    }
  }

  function checkPlayerRespawn() {
    if (!_cachedMyPlayer) return;

    var currentDead = isPlayerDead(_cachedMyPlayer);

    if (_isPlayerDead && !currentDead) {
      log('success', 'Respawn', '检测到玩家复活!');
      _isPlayerDead = false;

      try {
        send({ type: 'playerRespawned' });
      } catch(e) {
        log('error', 'Respawn', '发送复活事件失败: ' + e.message);
      }
    } else if (!_isPlayerDead && currentDead) {
      log('info', 'Respawn', '检测到玩家死亡');
      _isPlayerDead = true;
    }
  }

  function installRespawnHook() {
    if (_respawnHookInstalled) return true;

    var mod = getGameAssembly();
    if (!mod) {
      log('error', 'RespawnHook', '无法获取 GameAssembly.dll');
      return false;
    }

    var deathAddr = mod.base.add(RVA.Player_OnEntityDeath);

    try {
      Interceptor.attach(deathAddr, {
        onEnter: function(args) {
          var player = args[0];
          var myPlayer = getMyPlayer();

          if (player && myPlayer && player.equals(myPlayer)) {
            log('info', 'RespawnHook', '检测到本地玩家死亡');
            _isPlayerDead = true;
            _cachedMyPlayer = player;
          }
        }
      });

      _respawnHookInstalled = true;
      log('success', 'RespawnHook', 'Player_OnEntityDeath Hook 安装成功');

      var myPlayer = getMyPlayer();
      if (myPlayer) {
        _cachedMyPlayer = myPlayer;
        _isPlayerDead = isPlayerDead(myPlayer);
        log('info', 'RespawnHook', '初始玩家状态: ' + (_isPlayerDead ? '死亡' : '存活'));
      }

      return true;

    } catch (e) {
      log('error', 'RespawnHook', 'Hook 安装失败: ' + e.message);
      return false;
    }
  }

  function installSpawnHook() {
    if (_spawnHookInstalled) return true;

    var mod = getGameAssembly();
    if (!mod) {
      log('error', 'SpawnHook', '无法获取 GameAssembly.dll');
      return false;
    }

    var spawnAddr = mod.base.add(RVA.Player_Spawn);

    try {
      Interceptor.attach(spawnAddr, {
        onEnter: function(args) {
          var player = args[0];
          var myPlayer = getMyPlayer();

          if (player && myPlayer && player.equals(myPlayer)) {
            log('info', 'SpawnHook', '检测到本地玩家复活 (Player.Spawn)');
            _isPlayerDead = false;
            _cachedMyPlayer = player;

            if (_waitingForRespawnWeaponId !== null) {
              log('success', 'SpawnHook', '检测到复活，准备自动赋予武器: ' + _waitingForRespawnWeaponId);
              var weaponId = _waitingForRespawnWeaponId;
              var weaponName = _waitingForRespawnWeaponName;
              _waitingForRespawnWeaponId = null;
              _waitingForRespawnWeaponName = null;

              send({
                type: 'playerRespawnedWithWeapon',
                weaponId: weaponId,
                weaponName: weaponName
              });
            } else {
              send({ type: 'playerRespawned' });
            }
          }
        }
      });

      _spawnHookInstalled = true;
      log('success', 'SpawnHook', 'Player.Spawn Hook 安装成功');

      return true;

    } catch (e) {
      log('error', 'SpawnHook', 'Hook 安装失败: ' + e.message);
      return false;
    }
  }

  function giveWeapon(weaponIndex, autoGiveUp, autoSelect) {
    try {
      log('info', 'Weapon', '开始赋予武器（主线程调度）');

      var wpnId = parseInt(weaponIndex) || 0;
      var giveUpInt = (autoGiveUp === true || autoGiveUp === 1 || autoGiveUp === 'true') ? 1 : 0;
      var selectInt = (autoSelect === true || autoSelect === 1 || autoSelect === 'true') ? 1 : 0;

      log('info', 'Weapon', '参数: weaponIndex=' + wpnId + ', autoGiveUp=' + giveUpInt + ', autoSelect=' + selectInt);

      if (!initNativeFunctions()) {
        log('error', 'Weapon', 'NativeFunction 初始化失败');
        return false;
      }

      if (!checkGameManagerInit()) {
        log('error', 'Weapon', 'GameManager 未初始化!请确保已进入游戏房间');
        return false;
      }

      if (!installMainThreadHook()) {
        log('error', 'Weapon', '主线程 Hook 安装失败');
        return false;
      }

      if (!installRespawnHook()) {
        log('warn', 'Weapon', '复活 Hook 安装失败，但功能可用');
      }

      if (!installSpawnHook()) {
        log('warn', 'Weapon', 'Spawn Hook 安装失败，但功能可用');
      }

      var myPlayer = getMyPlayer();
      if (myPlayer) {
        _cachedMyPlayer = myPlayer;
        _isPlayerDead = isPlayerDead(myPlayer);
      }

      var taskId = ++_taskIdCounter;
      _pendingTasks.push({
        id: taskId,
        wpnId: wpnId,
        giveUp: giveUpInt,
        select: selectInt
      });

      log('info', 'Weapon', '任务已入队: taskId=' + taskId + '，等待主线程执行...');

      return 'pending:' + taskId;

    } catch(e) {
      log('error', 'Weapon', '异常: ' + e.message);
      return false;
    }
  }

  function getWeaponName(weaponIndex) {
    return null;
  }

  rpc.exports = {
    giveweapon: giveWeapon,
    getmyplayer: getMyPlayer,
    getweaponname: getWeaponName,
    setrespawnweapon: function(weaponId, weaponName) {
      try {
        _waitingForRespawnWeaponId = weaponId;
        _waitingForRespawnWeaponName = weaponName;
        log('success', 'Weapon', '设置复活自动武器: ' + weaponId + ' - ' + weaponName);
        return true;
      } catch (e) {
        log('error', 'Weapon', '设置复活武器失败: ' + e.message);
        return false;
      }
    },
    clearrespawnweapon: function() {
      try {
        _waitingForRespawnWeaponId = null;
        _waitingForRespawnWeaponName = null;
        log('info', 'Weapon', '清除复活自动武器');
        return true;
      } catch (e) {
        log('error', 'Weapon', '清除复活武器失败: ' + e.message);
        return false;
      }
    },
  };

  log('success', '系统', '武器赋予脚本已加载（修复版v6：支持复活检测）');
  log('info', '系统', '游戏进程: UnityCrossFire.exe');
  log('info', '系统', '');
  log('warn', '系统', 'v5修复说明:');
  log('warn', '系统', '  1. 根因: GiveWeapon内部调用Unity API（Instantiate/GetComponent）');
  log('warn', '系统', '     这些API只能在游戏主线程调用');
  log('warn', '系统', '  2. Frida RPC运行在独立线程，直接调用会触发access violation');
  log('warn', '系统', '  3. 方案: Hook ModeBase$$Update（主线程每帧执行）');
  log('warn', '系统', '     RPC请求入队 -> 主线程Update回调拾取并执行GiveWeapon');
  log('warn', '系统', '  4. 结果通过send()消息返回给Python端');
  log('info', '系统', '');
  log('info', '系统', 'v6新增: 复活自动恢复武器功能');
  log('info', '系统', '  1. Hook Player_OnEntityDeath检测玩家死亡');
  log('info', '系统', '  2. 每30帧检查玩家是否复活');
  log('info', '系统', '  3. 检测到复活后发送playerRespawned事件给Python端');

})();
