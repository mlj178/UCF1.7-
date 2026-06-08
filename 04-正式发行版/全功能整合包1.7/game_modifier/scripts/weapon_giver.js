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
  var _taskTtlMs = 1500;

  var _isPlayerDead = false;
  var _lastCheckFrame = 0;
  var _cachedMyPlayer = null;
  var _checkAliveInterval = 30;
  var _waitingForRespawnWeaponId = null;
  var _waitingForRespawnWeaponName = null;
  var _modeBaseInstance = null;  // 当前ModeBase实例（用于检测模式切换）
  var _lastModeUpdateTime = 0;
  var _modeSwitchGraceUntil = 0;
  var _roomActiveWindowMs = 1200;
  var _modeSwitchGraceMs = 800;

  function resetRoomState(reason) {
    _modeBaseInstance = null;
    _pendingTasks = [];
    _taskResults = {};
    _cachedMyPlayer = null;
    _isPlayerDead = false;
    _lastCheckFrame = 0;
    _lastModeUpdateTime = 0;
    _modeSwitchGraceUntil = Date.now() + _modeSwitchGraceMs;
    if (reason) {
      sendLog('info', '武器赋予', reason);
    }
  }

  function isRoomActive() {
    var now = Date.now();
    if (!_modeBaseInstance) return false;
    if (now < _modeSwitchGraceUntil) return false;
    return _lastModeUpdateTime > 0 && (now - _lastModeUpdateTime) <= _roomActiveWindowMs;
  }

  function notifySpeedgunWeaponAcquired(weapon) {
    try {
      if (!weapon || weapon.isNull()) return;
      if (!modules.speedgun || !modules.speedgun.notifyWeaponAcquired) return;
      modules.speedgun.notifyWeaponAcquired(weapon);
    } catch(e) {
      sendLog('warn', '武器赋予', '联动射速失败: ' + e.message);
    }
  }

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

  function isPlayerValid(player) {
    /**检查玩家实例是否有效
     * 1. 地址不为null且在合理范围内
     * 2. 地址可读
     * 3. 玩家未死亡
     */
    try {
      // 检查地址是否有效
      if (!player || player.isNull()) {
        return false;
      }
      
      // 检查地址是否在合理范围内（避免访问无效内存）
      if (player.compare(ptr(0x10000)) < 0) {
        return false;
      }
      
      // 尝试读取地址（检查是否可读）
      player.readU8();
      
      // 检查玩家是否已死亡
      if (isPlayerDead(player)) {
        return false;
      }
      
      return true;
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
    if (!isRoomActive()) {
      sendLog('warn', '武器赋予', '当前不在稳定房间内，已忽略赋予任务');
      return false;
    }

    var myPlayer = getMyPlayer();
    if (!myPlayer) {
      sendLog('error', '武器赋予', '主线程: 无法获取玩家实例');
      return false;
    }
    
    // 检查玩家实例有效性
    if (!isPlayerValid(myPlayer)) {
      sendLog('error', '武器赋予', '主线程: 玩家实例无效（可能已死亡或地址无效）');
      return false;
    }

    if (_giveWeaponFunc) {
      try {
        var methodInfo = getGiveWeaponMethodInfo();
        var methodArg = methodInfo ? methodInfo : ptr(0);

        // GiveWeapon调用保护
        var weapon = null;
        var directCallFailed = false;
        try {
          weapon = _giveWeaponFunc(myPlayer, wpnId, giveUpInt, selectInt, methodArg);
        } catch(callError) {
          directCallFailed = true;
          _giveWeaponFunc = null;
          sendLog('warn', '武器赋予', 'GiveWeapon直接调用异常，改用il2cpp_runtime_invoke: ' + callError.message);
        }

        if (weapon && !weapon.isNull()) {
          notifySpeedgunWeaponAcquired(weapon);
          sendLog('success', '武器赋予', '赋予武器成功! weaponId=' + wpnId);
          return true;
        } else if (!directCallFailed) {
          sendLog('warn', '武器赋予', 'GiveWeapon直接调用返回null，改用il2cpp_runtime_invoke');
        }
      } catch(e) {
        _giveWeaponFunc = null;
        sendLog('warn', '武器赋予', 'GiveWeapon直接调用外层异常，改用il2cpp_runtime_invoke: ' + e.message);
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
          notifySpeedgunWeaponAcquired(weapon);
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

  function handleModeBaseUpdate(instance) {
    if (!instance || instance.isNull()) return false;

    var now = Date.now();
    if (!_modeBaseInstance) {
      _modeBaseInstance = instance;
      _lastCheckFrame = 0;
      _modeSwitchGraceUntil = now + _modeSwitchGraceMs;
      sendLog('info', '武器赋予', '检测到ModeBase实例: ' + instance);
    } else if (!instance.equals(_modeBaseInstance)) {
      _modeBaseInstance = instance;
      _pendingTasks = [];
      _cachedMyPlayer = null;
      _isPlayerDead = false;
      _lastCheckFrame = 0;
      _modeSwitchGraceUntil = now + _modeSwitchGraceMs;
      sendLog('info', '武器赋予', '检测到新ModeBase实例，已清理旧任务和旧玩家缓存: ' + instance);
    }

    _lastModeUpdateTime = now;
    return now >= _modeSwitchGraceUntil;
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
      // Hook ModeBase.Update（主线程调度）
      hooks.push(Interceptor.attach(updateAddr, {
        onEnter: function(args) {
          try {
            var instance = args[0];
            var roomStable = handleModeBaseUpdate(instance);
            
            var currentFrame = _lastCheckFrame + 1;
            _lastCheckFrame = currentFrame;

            // 限制每帧最多处理1个任务，避免阻塞游戏主线程
            if (roomStable && _pendingTasks.length > 0) {
              var task = _pendingTasks.shift();
              try {
                if (task.expiresAt && Date.now() > task.expiresAt) {
                  _taskResults[task.id] = false;
                  send({
                    type: 'giveWeaponResult',
                    taskId: task.id,
                    success: false
                  });
                  sendLog('warn', '武器赋予', '赋予任务已过期，已丢弃: taskId=' + task.id);
                } else {
                  var result = executeGiveWeaponOnMainThread(task.wpnId, task.giveUp, task.select);
                  _taskResults[task.id] = result;

                  send({
                    type: 'giveWeaponResult',
                    taskId: task.id,
                    success: result
                  });
                }
              } catch(e) {
                sendLog('error', '武器赋予', '执行赋予任务异常: ' + e.message);
                _taskResults[task.id] = false;
                send({
                  type: 'giveWeaponResult',
                  taskId: task.id,
                  success: false
                });
              }
            }

            if (roomStable && _cachedMyPlayer && currentFrame % _checkAliveInterval === 0) {
              try {
                checkPlayerRespawn();
              } catch(e) {
                sendLog('error', '武器赋予', '检查玩家复活异常: ' + e.message);
              }
            }
          } catch(e) {
            sendLog('error', '武器赋予', 'ModeBase.Update Hook 异常: ' + e.message);
          }
        }
      }));

      // Hook模式切换函数（清空ModeBase实例和任务队列）
      var modeChangeAddr1 = mod.base.add(0xAFAA40);
      hooks.push(Interceptor.attach(modeChangeAddr1, {
        onEnter: function() {
          resetRoomState('检测到模式切换，已清空任务队列和玩家缓存');
        }
      }));

      _hookInstalled = true;
      sendLog('success', '武器赋予', 'ModeBase.Update Hook 安装成功（主线程调度 + 模式切换检测）');
      return true;

    } catch(e) {
      sendLog('error', '武器赋予', 'Hook 安装失败: ' + e.message);
      return false;
    }
  }

  function checkPlayerRespawn() {
    if (!isRoomActive()) return;
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
          try {
            var player = args[0];
            var myPlayer = getMyPlayer();

            if (player && myPlayer && player.equals(myPlayer)) {
              sendLog('info', '武器赋予', '检测到本地玩家死亡');
              _isPlayerDead = true;
              _cachedMyPlayer = player;
            }
          } catch(e) {
            sendLog('error', '武器赋予', 'OnEntityDeath Hook 异常: ' + e.message);
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
          try {
            var player = args[0];
            var myPlayer = getMyPlayer();

            if (player && myPlayer && player.equals(myPlayer)) {
              sendLog('info', '武器赋予', '检测到本地玩家复活');
              _isPlayerDead = false;
              _cachedMyPlayer = player;

              if (_waitingForRespawnWeaponId !== null) {
                sendLog('success', '武器赋予', '检测到复活，准备自动赋予武器: ' + _waitingForRespawnWeaponId);

                try {
                  if (initNativeFunctions() && installMainThreadHook()) {
                    var taskId = ++_taskIdCounter;
                    _pendingTasks.push({
                      id: taskId,
                      wpnId: parseInt(_waitingForRespawnWeaponId) || 0,
                      giveUp: 1,
                      select: 1,
                      expiresAt: Date.now() + _taskTtlMs
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
                } catch(e) {
                  sendLog('error', '武器赋予', '复活自动赋予异常: ' + e.message);
                }
              } else {
                send({ type: 'playerRespawned' });
              }
            }
          } catch(e) {
            sendLog('error', '武器赋予', 'Spawn Hook 异常: ' + e.message);
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

      var taskId = ++_taskIdCounter;
      _pendingTasks.push({
        id: taskId,
        wpnId: wpnId,
        giveUp: giveUpInt,
        select: selectInt,
        expiresAt: Date.now() + _taskTtlMs
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
      _hookInstalled = false;
      _respawnHookInstalled = false;
      _spawnHookInstalled = false;
      resetRoomState(null);
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
