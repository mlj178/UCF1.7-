// weapon_giver.js - 武器赋予（主线程调度）
// 核心功能：赋予武器、复活自动装备武器
// 关键技术：Hook ModeBase.Update实现主线程调度（GiveWeapon必须在主线程执行）

modules.weapon_giver = (function() {
  var enabled = false;
  var hooks = [];

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

  function readPtr(addr) {
    try {
      if (!addr || addr.isNull()) return null;
      var v = addr.readPointer();
      return (v && !v.isNull()) ? v : null;
    } catch(e) {
      return null;
    }
  }

  function getGameManagerKlass() {
    try {
      var mod = getGameAssembly();
      if (!mod) return null;
      var typeInfoSlot = mod.base.add(RVA.GameManager_TypeInfo);
      return readPtr(typeInfoSlot);
    } catch(e) {
      sendLog('error', '武器赋予', '获取GameManager klass失败: ' + e.message);
      return null;
    }
  }

  function getGiveWeaponMethodInfo() {
    if (_giveWeaponMethodInfo) return _giveWeaponMethodInfo;

    var mod = getGameAssembly();
    if (!mod) return null;

    var klass = getGameManagerKlass();
    if (!klass) {
      sendLog('error', '武器赋予', '无法获取GameManager klass');
      return null;
    }

    try {
      var exportAddr = mod.getExportByName('il2cpp_class_get_method_from_name');
      if (!exportAddr) {
        sendLog('error', '武器赋予', '未找到il2cpp_class_get_method_from_name导出');
        return null;
      }

      var getClassMethod = new NativeFunction(exportAddr, 'pointer', ['pointer', 'pointer', 'uint32']);
      var methodName = Memory.allocUtf8String('GiveWeapon');
      var methodInfo = getClassMethod(klass, methodName, 4);

      if (methodInfo && !methodInfo.isNull()) {
        _giveWeaponMethodInfo = methodInfo;
        sendLog('success', '武器赋予', '成功获取GiveWeapon MethodInfo: ' + methodInfo);
        return methodInfo;
      }

      sendLog('error', '武器赋予', 'il2cpp_class_get_method_from_name返回null');
      return null;

    } catch(e) {
      sendLog('error', '武器赋予', '获取MethodInfo失败: ' + e.message);
      return null;
    }
  }

  function initNativeFunctions() {
    if (_initialized) return true;

    var mod = getGameAssembly();
    if (!mod) {
      sendLog('error', '武器赋予', '无法获取 GameAssembly.dll');
      return false;
    }
    var base = mod.base;

    try {
      var exportInvoke = mod.getExportByName('il2cpp_runtime_invoke');
      if (!exportInvoke) {
        sendLog('error', '武器赋予', '未找到 il2cpp_runtime_invoke');
        return false;
      }
      _il2cpp_runtime_invoke = new NativeFunction(
        exportInvoke,
        'pointer',
        ['pointer', 'pointer', 'pointer', 'pointer']
      );
      sendLog('success', '武器赋予', 'il2cpp_runtime_invoke 初始化成功');
    } catch(e) {
      sendLog('error', '武器赋予', 'il2cpp_runtime_invoke 初始化失败: ' + e.message);
      return false;
    }

    try {
      _giveWeaponFunc = new NativeFunction(
        base.add(RVA.GiveWeapon),
        'pointer',
        ['pointer', 'int', 'int', 'int', 'pointer'],
        'mscdecl'
      );
      sendLog('success', '武器赋予', 'GiveWeapon NativeFunction 初始化成功 (mscdecl)');
    } catch(e) {
      sendLog('warn', '武器赋予', 'GiveWeapon 直接调用初始化失败: ' + e.message);
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
      sendLog('error', '武器赋予', '获取玩家异常: ' + e.message);
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
      sendLog('error', '武器赋予', '主线程: 无法获取玩家实例');
      return false;
    }

    if (_giveWeaponFunc) {
      try {
        var methodInfo = getGiveWeaponMethodInfo();
        var methodArg = methodInfo ? methodInfo : ptr(0);

        var weapon = _giveWeaponFunc(myPlayer, wpnId, giveUpInt, selectInt, methodArg);

        if (weapon && !weapon.isNull()) {
          sendLog('success', '武器赋予', '赋予武器成功! weaponId=' + wpnId);
          return true;
        } else {
          sendLog('error', '武器赋予', '赋予武器返回null');
          return false;
        }
      } catch(e) {
        sendLog('error', '武器赋予', '赋予武器异常: ' + e.message);
      }
    }

    if (_il2cpp_runtime_invoke) {
      try {
        var methodInfo = getGiveWeaponMethodInfo();
        if (!methodInfo) {
          sendLog('error', '武器赋予', '主线程: 无法获取MethodInfo');
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

        var weapon = _il2cpp_runtime_invoke(methodInfo, ptr(0), params, exc);

        var excVal = exc.readPointer();
        if (!excVal.isNull()) {
          sendLog('error', '武器赋予', '主线程 IL2CPP 异常! exc=' + excVal);
          return false;
        }

        if (weapon && !weapon.isNull()) {
          sendLog('success', '武器赋予', '赋予武器成功! weaponId=' + wpnId);
          return true;
        } else {
          sendLog('error', '武器赋予', '赋予武器返回null');
          return false;
        }
      } catch(e) {
        sendLog('error', '武器赋予', '主线程 invoke 异常: ' + e.message);
        return false;
      }
    }

    sendLog('error', '武器赋予', '无可用的调用方式');
    return false;
  }

  function installMainThreadHook() {
    if (_hookInstalled) return true;

    var mod = getGameAssembly();
    if (!mod) {
      sendLog('error', '武器赋予', '无法获取 GameAssembly.dll');
      return false;
    }

    var updateAddr = mod.base.add(RVA.ModeBase_Update);

    try {
      hooks.push(Interceptor.attach(updateAddr, {
        onEnter: function(args) {
          var currentFrame = _lastCheckFrame + 1;
          _lastCheckFrame = currentFrame;

          while (_pendingTasks.length > 0) {
            var task = _pendingTasks.shift();
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
      }));

      _hookInstalled = true;
      sendLog('success', '武器赋予', 'ModeBase.Update Hook 安装成功（主线程调度）');
      return true;

    } catch(e) {
      sendLog('error', '武器赋予', 'Hook 安装失败: ' + e.message);
      return false;
    }
  }

  function checkPlayerRespawn() {
    if (!_cachedMyPlayer) return;

    var currentDead = isPlayerDead(_cachedMyPlayer);

    if (_isPlayerDead && !currentDead) {
      sendLog('success', '武器赋予', '检测到玩家复活!');
      _isPlayerDead = false;

      try {
        send({ type: 'playerRespawned' });
      } catch(e) {
        sendLog('error', '武器赋予', '发送复活事件失败: ' + e.message);
      }
    } else if (!_isPlayerDead && currentDead) {
      sendLog('info', '武器赋予', '检测到玩家死亡');
      _isPlayerDead = true;
    }
  }

  function installRespawnHook() {
    if (_respawnHookInstalled) return true;

    var mod = getGameAssembly();
    if (!mod) {
      sendLog('error', '武器赋予', '无法获取 GameAssembly.dll');
      return false;
    }

    var deathAddr = mod.base.add(RVA.Player_OnEntityDeath);

    try {
      hooks.push(Interceptor.attach(deathAddr, {
        onEnter: function(args) {
          var player = args[0];
          var myPlayer = getMyPlayer();

          if (player && myPlayer && player.equals(myPlayer)) {
            sendLog('info', '武器赋予', '检测到本地玩家死亡');
            _isPlayerDead = true;
            _cachedMyPlayer = player;
          }
        }
      }));

      _respawnHookInstalled = true;
      sendLog('success', '武器赋予', 'Player.OnEntityDeath Hook 安装成功');

      var myPlayer = getMyPlayer();
      if (myPlayer) {
        _cachedMyPlayer = myPlayer;
        _isPlayerDead = isPlayerDead(myPlayer);
      }

      return true;

    } catch (e) {
      sendLog('error', '武器赋予', 'Hook 安装失败: ' + e.message);
      return false;
    }
  }

  function installSpawnHook() {
    if (_spawnHookInstalled) return true;

    var mod = getGameAssembly();
    if (!mod) {
      sendLog('error', '武器赋予', '无法获取 GameAssembly.dll');
      return false;
    }

    var spawnAddr = mod.base.add(RVA.Player_Spawn);

    try {
      hooks.push(Interceptor.attach(spawnAddr, {
        onEnter: function(args) {
          var player = args[0];
          var myPlayer = getMyPlayer();

          if (player && myPlayer && player.equals(myPlayer)) {
            sendLog('info', '武器赋予', '检测到本地玩家复活');
            _isPlayerDead = false;
            _cachedMyPlayer = player;

            if (_waitingForRespawnWeaponId !== null) {
              sendLog('success', '武器赋予', '检测到复活，准备自动赋予武器: ' + _waitingForRespawnWeaponId);

              if (initNativeFunctions() && installMainThreadHook()) {
                var taskId = ++_taskIdCounter;
                _pendingTasks.push({
                  id: taskId,
                  wpnId: parseInt(_waitingForRespawnWeaponId) || 0,
                  giveUp: 1,
                  select: 1
                });
                sendLog('success', '武器赋予', '复活自动赋予任务已入队: taskId=' + taskId + ', weaponId=' + _waitingForRespawnWeaponId);
              } else {
                sendLog('error', '武器赋予', '复活自动赋予失败: 初始化未完成');
              }

              send({
                type: 'playerRespawnedWithWeapon',
                weaponId: _waitingForRespawnWeaponId,
                weaponName: _waitingForRespawnWeaponName
              });
            } else {
              send({ type: 'playerRespawned' });
            }
          }
        }
      }));

      _spawnHookInstalled = true;
      sendLog('success', '武器赋予', 'Player.Spawn Hook 安装成功');

      return true;

    } catch (e) {
      sendLog('error', '武器赋予', 'Hook 安装失败: ' + e.message);
      return false;
    }
  }

  function giveWeapon(weaponIndex, autoGiveUp, autoSelect) {
    try {
      var wpnId = parseInt(weaponIndex) || 0;
      var giveUpInt = (autoGiveUp === true || autoGiveUp === 1 || autoGiveUp === 'true') ? 1 : 0;
      var selectInt = (autoSelect === true || autoSelect === 1 || autoSelect === 'true') ? 1 : 0;

      if (!initNativeFunctions()) {
        sendLog('error', '武器赋予', 'NativeFunction 初始化失败');
        return false;
      }

      if (!checkGameManagerInit()) {
        sendLog('error', '武器赋予', 'GameManager 未初始化!请确保已进入游戏房间');
        return false;
      }

      if (!installMainThreadHook()) {
        sendLog('error', '武器赋予', '主线程 Hook 安装失败');
        return false;
      }

      if (!installRespawnHook()) {
        sendLog('warn', '武器赋予', '复活 Hook 安装失败，但功能可用');
      }

      if (!installSpawnHook()) {
        sendLog('warn', '武器赋予', 'Spawn Hook 安装失败，但功能可用');
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

      sendLog('info', '武器赋予', '任务已入队: taskId=' + taskId + '，等待主线程执行...');

      return 'pending:' + taskId;

    } catch(e) {
      sendLog('error', '武器赋予', '异常: ' + e.message);
      return false;
    }
  }

  return {
    enable: function() {
      if (enabled) return;
      enabled = true;
      sendLog('success', '武器赋予', '武器赋予功能已启用');
      sendStatus('weapon_giver', true);
    },
    disable: function() {
      if (!enabled) return;
      for (var i = 0; i < hooks.length; i++) {
        try { hooks[i].detach(); } catch(e) {}
      }
      hooks = [];
      enabled = false;
      sendLog('info', '武器赋予', '武器赋予功能已禁用');
      sendStatus('weapon_giver', false);
    },
    giveweapon: giveWeapon,
    getmyplayer: getMyPlayer,
    setrespawnweapon: function(weaponId, weaponName) {
      try {
        _waitingForRespawnWeaponId = weaponId;
        _waitingForRespawnWeaponName = weaponName;
        sendLog('success', '武器赋予', '设置复活自动武器: ' + weaponId + ' - ' + weaponName);
        return true;
      } catch (e) {
        sendLog('error', '武器赋予', '设置复活武器失败: ' + e.message);
        return false;
      }
    },
    clearrespawnweapon: function() {
      try {
        _waitingForRespawnWeaponId = null;
        _waitingForRespawnWeaponName = null;
        sendLog('info', '武器赋予', '清除复活自动武器');
        return true;
      } catch (e) {
        sendLog('error', '武器赋予', '清除复活武器失败: ' + e.message);
        return false;
      }
    },
    isEnabled: function() { return enabled; }
  };
})();
