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
    ModeBase_ExitGame: 0xAEE850,
    GameManager_GameRoundEnd: 0xAFAA40,
    GameManager_OnDestroy: 0xAFB6F0,
    Player_OnEntityDeath: 0xB51210,
    Player_OnDestroy: 0xB511C0,
    Player_Spawn: 0xB53760,
    Entity_get_isDead: 0xB400E0,
    Player_get_isMyPlayer: 0xB55FD0,
  };

  var OFF = {
    Klass_staticFields: 0x5C,
    GM_myPlayer: 0x00,
  };

  var _giveWeaponFunc = null;
  var _isDeadFunc = null;
  var _isMyPlayerFunc = null;
  var _initialized = false;
  var _hookInstalled = false;
  var _respawnHookInstalled = false;
  var _spawnHookInstalled = false;

  var _pendingTasks = [];
  var _taskIdCounter = 0;
  var _taskTtlMs = 5000;

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
  var _roomShuttingDown = false;
  var _exitingModeBaseInstance = null;
  var _specialDoubleGiveWeaponIds = {
    2978: true,
    3494: true
  };
  var _firstRoomSpecialGiveDoneByWeaponId = {};

  function isSpecialDoubleGiveWeapon(wpnId) {
    return _specialDoubleGiveWeaponIds[wpnId] === true;
  }

  function resetFirstRoomSpecialGiveState() {
    _firstRoomSpecialGiveDoneByWeaponId = {};
  }

  function resetRoomState(reason, shuttingDown, exitingInstance) {
    _roomShuttingDown = shuttingDown === true;
    _exitingModeBaseInstance = _roomShuttingDown && exitingInstance ? exitingInstance : null;
    _modeBaseInstance = null;
    _pendingTasks = [];
    _cachedMyPlayer = null;
    _isPlayerDead = false;
    _lastCheckFrame = 0;
    _lastModeUpdateTime = 0;
    _modeSwitchGraceUntil = Date.now() + _modeSwitchGraceMs;
    if (_roomShuttingDown) {
      resetFirstRoomSpecialGiveState();
    }
    try {
      if (modules.speedgun && modules.speedgun.clearRoomState) {
        modules.speedgun.clearRoomState(_roomShuttingDown, _exitingModeBaseInstance);
      }
    } catch(e) {}
    if (reason) {
      sendLog('info', '武器赋予', reason);
    }
  }

  function isRoomActive() {
    var now = Date.now();
    if (_roomShuttingDown) return false;
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

  function rollbackHooks(startIndex) {
    while (hooks.length > startIndex) {
      var hook = hooks.pop();
      try { hook.detach(); } catch(e) {}
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

  function initNativeFunctions() {
    if (_initialized) return true;

    var mod = getGameAssembly();
    if (!mod) {
      sendLog('error', '武器赋予', '无法获取 GameAssembly.dll');
      return false;
    }
    var base = mod.base;

    try {
      _giveWeaponFunc = new NativeFunction(
        base.add(RVA.GiveWeapon),
        'pointer',
        ['pointer', 'int', 'int', 'int', 'pointer'],
        'mscdecl'
      );
      _isDeadFunc = new NativeFunction(
        base.add(RVA.Entity_get_isDead),
        'int',
        ['pointer', 'pointer'],
        'mscdecl'
      );
      _isMyPlayerFunc = new NativeFunction(
        base.add(RVA.Player_get_isMyPlayer),
        'int',
        ['pointer', 'pointer'],
        'mscdecl'
      );
      sendLog('success', '武器赋予', 'GiveWeapon NativeFunction 初始化成功 (mscdecl)');
    } catch(e) {
      sendLog('error', '武器赋予', 'GiveWeapon 直接调用初始化失败: ' + e.message);
      _giveWeaponFunc = null;
      _isDeadFunc = null;
      _isMyPlayerFunc = null;
      return false;
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
      if (!_isDeadFunc || !player || player.isNull()) return true;
      var result = _isDeadFunc(player, ptr(0));
      return result !== 0;
    } catch(e) {
      return true;
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

      // IDA: Player.wpns 位于 +0xA0，GiveWeapon 内部会立即访问它。
      var playerWeapons = readPtr(player.add(0xA0));
      if (!playerWeapons) {
        return false;
      }

      if (!isMyPlayer(player)) {
        return false;
      }
      
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
      if (!_isMyPlayerFunc || !player || player.isNull()) return false;
      var result = _isMyPlayerFunc(player, ptr(0));
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

    if (!_giveWeaponFunc) {
      sendLog('error', '武器赋予', 'GiveWeapon函数未初始化');
      return false;
    }

    try {
      // 与 HUD_Cheat / HUD_ChatBox 的游戏内部调用完全一致：
      // GiveWeapon(player, weaponId, false, autoSelect, NULL)
      var weapon = _giveWeaponFunc(myPlayer, wpnId, 0, selectInt, ptr(0));
      if (!weapon || weapon.isNull()) {
        sendLog('error', '武器赋予', 'GiveWeapon返回null，weaponId=' + wpnId);
        return false;
      }

      notifySpeedgunWeaponAcquired(weapon);
      sendLog('success', '武器赋予', '赋予武器成功! weaponId=' + wpnId);
      return true;
    } catch(e) {
      _giveWeaponFunc = null;
      _isDeadFunc = null;
      _isMyPlayerFunc = null;
      _initialized = false;
      sendLog('error', '武器赋予', 'GiveWeapon直接调用异常: ' + e.message);
      return false;
    }
  }

  function handleModeBaseUpdate(instance) {
    if (!instance || instance.isNull()) return false;

    var now = Date.now();
    if (_roomShuttingDown) {
      if (_exitingModeBaseInstance && instance.equals(_exitingModeBaseInstance)) {
        return false;
      }
      _roomShuttingDown = false;
      _exitingModeBaseInstance = null;
      _modeSwitchGraceUntil = now + _modeSwitchGraceMs;
    }

    if (!_modeBaseInstance) {
      _modeBaseInstance = instance;
      _lastCheckFrame = 0;
      _modeSwitchGraceUntil = now + _modeSwitchGraceMs;
      sendLog('info', '武器赋予', '检测到ModeBase实例: ' + instance);
    } else if (!instance.equals(_modeBaseInstance)) {
      _modeBaseInstance = instance;
      resetFirstRoomSpecialGiveState();
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
    var hookStartIndex = hooks.length;

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
                  send({
                    type: 'giveWeaponResult',
                    taskId: task.id,
                    success: false
                  });
                  sendLog('warn', '武器赋予', '赋予任务已过期，已丢弃: taskId=' + task.id);
                } else {
                  var result = executeGiveWeaponOnMainThread(task.wpnId, task.giveUp, task.select);

                  send({
                    type: 'giveWeaponResult',
                    taskId: task.id,
                    success: result
                  });
                }
              } catch(e) {
                sendLog('error', '武器赋予', '执行赋予任务异常: ' + e.message);
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

      // 回合结束只清理缓存，不进入退出状态。
      hooks.push(Interceptor.attach(mod.base.add(RVA.GameManager_GameRoundEnd), {
        onEnter: function() {
          resetRoomState('检测到回合结束，已清空赋予任务和玩家缓存', false, null);
        }
      }));

      // 退出房间开始时立即封锁全部旧指针和新任务。
      hooks.push(Interceptor.attach(mod.base.add(RVA.ModeBase_ExitGame), {
        onEnter: function(args) {
          resetRoomState('检测到退出房间，已停止武器赋予', true, args[0]);
        }
      }));

      // 场景销毁的最终保险。
      hooks.push(Interceptor.attach(mod.base.add(RVA.GameManager_OnDestroy), {
        onEnter: function() {
          resetRoomState('检测到游戏场景销毁，已清理武器状态', true, _modeBaseInstance);
        }
      }));

      _hookInstalled = true;
      sendLog('success', '武器赋予', '主线程调度及退出清理 Hook 安装成功');
      return true;

    } catch(e) {
      rollbackHooks(hookStartIndex);
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
    var hookStartIndex = hooks.length;

    try {
      hooks.push(Interceptor.attach(deathAddr, {
        onEnter: function(args) {
          try {
            if (_roomShuttingDown || !isRoomActive()) return;
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

      hooks.push(Interceptor.attach(mod.base.add(RVA.Player_OnDestroy), {
        onEnter: function(args) {
          try {
            var player = args[0];
            if (_cachedMyPlayer && player && player.equals(_cachedMyPlayer)) {
              _pendingTasks = [];
              _cachedMyPlayer = null;
              _isPlayerDead = false;
              try {
                if (modules.speedgun && modules.speedgun.clearRoomState) {
                  modules.speedgun.clearRoomState(_roomShuttingDown, _exitingModeBaseInstance);
                }
              } catch(e) {}
            }
          } catch(e) {
            _cachedMyPlayer = null;
            _pendingTasks = [];
          }
        }
      }));

      _respawnHookInstalled = true;
      sendLog('success', '武器赋予', 'Player.OnEntityDeath Hook 安装成功');

      var myPlayer = isRoomActive() ? getMyPlayer() : null;
      if (myPlayer && isPlayerValid(myPlayer)) {
        _cachedMyPlayer = myPlayer;
        _isPlayerDead = isPlayerDead(myPlayer);
      }

      return true;

    } catch (e) {
      rollbackHooks(hookStartIndex);
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
    var hookStartIndex = hooks.length;

    try {
      hooks.push(Interceptor.attach(spawnAddr, {
        onEnter: function(args) {
          this.player = args[0];
        },
        onLeave: function() {
          try {
            if (_roomShuttingDown || !isRoomActive()) return;
            var player = this.player;
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
      rollbackHooks(hookStartIndex);
      sendLog('error', '武器赋予', 'Hook 安装失败: ' + e.message);
      return false;
    }
  }

  function giveWeapon(weaponIndex, autoGiveUp, autoSelect) {
    try {
      if (_roomShuttingDown) {
        sendLog('warn', '武器赋予', '正在退出房间，已忽略赋予请求');
        return false;
      }

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

      var repeatCount = 1;
      if (isSpecialDoubleGiveWeapon(wpnId) && !_firstRoomSpecialGiveDoneByWeaponId[wpnId]) {
        repeatCount = 2;
        _firstRoomSpecialGiveDoneByWeaponId[wpnId] = true;
      }

      var firstTaskId = null;
      for (var i = 0; i < repeatCount; i++) {
        var taskId = ++_taskIdCounter;
        if (firstTaskId === null) firstTaskId = taskId;
        _pendingTasks.push({
          id: taskId,
          wpnId: wpnId,
          giveUp: giveUpInt,
          select: selectInt,
          expiresAt: Date.now() + _taskTtlMs
        });
      }

      if (repeatCount > 1) {
        sendLog('info', '武器赋予', '首次进入房间特殊武器，已入队2次赋予任务: weaponId=' + wpnId + ', firstTaskId=' + firstTaskId);
      } else {
        sendLog('info', '武器赋予', '任务已入队: taskId=' + firstTaskId + '，等待主线程执行...');
      }

      return 'pending:' + firstTaskId;

    } catch(e) {
      sendLog('error', '武器赋予', '异常: ' + e.message);
      return false;
    }
  }

  return {
    enable: function() {
      if (enabled) return;
      resetRoomState(null, false, null);
      enabled = true;
      sendLog('success', '武器赋予', '武器赋予功能已启用');
      sendStatus('weapon_giver', true);
    },
    disable: function() {
      for (var i = 0; i < hooks.length; i++) {
        try { hooks[i].detach(); } catch(e) {}
      }
      hooks = [];
      _hookInstalled = false;
      _respawnHookInstalled = false;
      _spawnHookInstalled = false;
      resetRoomState(null, true, _modeBaseInstance);
      _giveWeaponFunc = null;
      _isDeadFunc = null;
      _isMyPlayerFunc = null;
      _initialized = false;
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
