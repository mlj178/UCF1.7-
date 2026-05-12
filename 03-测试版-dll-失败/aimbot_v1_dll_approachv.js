// ====================================================================
// UnityCrossFire.dll 自瞄模块完整实现
// 基于 IDA 逆向分析的完整算法实现
// 
// 功能模块:
//   1. 按键检测 (GetAsyncKeyState / Input.GetMouseButton)
//   2. 玩家列表获取 (GameManager.allPlayers)
//   3. 目标筛选算法 (距离、角度、队伍、可见性)
//   4. 队伍检查 (Entity.team)
//   5. 距离计算 (3D空间距离)
//   6. 可见性检测 (Physics.Linecast)
//   7. 瞄准角度计算 (atan2数学运算)
//   8. 视角设置 (Player.AddCameraRotation)
//
// RVA来源: IDA逆向分析 + Il2CppDumper
// ====================================================================
(function() {
  'use strict';

  // ================================================================
  // 日志系统
  // ================================================================
  var LOG_LEVEL = {
    DEBUG: 0,
    INFO: 1,
    WARN: 2,
    ERROR: 3
  };
  
  var currentLogLevel = LOG_LEVEL.INFO;
  var logCounts = {};
  var MAX_LOGS_PER_CATEGORY = 50;
  
  function log(level, category, message) {
    if (level < currentLogLevel) return;
    if (!logCounts[category]) logCounts[category] = 0;
    if (logCounts[category] >= MAX_LOGS_PER_CATEGORY) return;
    logCounts[category]++;
    
    var levelStr = ['DEBUG', 'INFO', 'WARN', 'ERROR'][level];
    var timestamp = new Date().toISOString().substr(11, 12);
    console.log('[' + timestamp + '][' + levelStr + '][' + category + '] ' + message);
  }

  // ================================================================
  // 获取 GameAssembly.dll 模块
  // ================================================================
  var gameAssembly = null;
  
  function getGameAssembly() {
    if (gameAssembly) return gameAssembly;
    try {
      var mod = Process.findModuleByName('GameAssembly.dll');
      if (!mod) {
        log(LOG_LEVEL.ERROR, '系统', '未找到 GameAssembly.dll');
        return null;
      }
      gameAssembly = mod;
      log(LOG_LEVEL.INFO, '系统', 'GameAssembly.dll 基址: ' + mod.base + ' 大小: ' + mod.size);
      return mod;
    } catch(e) {
      log(LOG_LEVEL.ERROR, '系统', '获取模块失败: ' + e.message);
      return null;
    }
  }

  // ================================================================
  // RVA 地址常量 (从IDA逆向分析获取)
  // ================================================================
  var RVA = {
    // GameManager 单例获取
    SingletonGet:                0x4A8170,   // Singleton<GameManager>.get_instance
    GM_Singleton_MethodInfo:     0xE1CE64,   // MethodInfo* 元数据指针
    
    // Transform 相关
    Component_get_transform:     0x32CF40,   // Transform* Component.get_transform()
    Transform_get_position:      0x3F42B0,   // void Transform.get_position(Vector3& ret)
    
    // Player/Entity 属性
    Player_get_isMyPlayer:       0xB55FD0,   // bool Player.get_isMyPlayer()
    Entity_get_isDead:           0xB400E0,   // bool Entity.get_isDead()
    Entity_get_team:             0x1E0070,   // Team Entity.get_team()
    
    // 视角控制
    Player_AddCameraRotation:    0xB4F790,   // void Player.AddCameraRotation(float x, float y)
    
    // 输入检测
    Input_GetMouseButton:        0xACFB20,   // bool Input.GetMouseButton(int button)
    Input_GetKey:                0xACF9A0,   // bool Input.GetKey(KeyCode key)
    
    // 物理检测
    Physics_Linecast:            0xAB9B80,   // bool Physics.Linecast(Vector3 start, Vector3 end, int layerMask)
    Physics_Raycast:             0xAB9A00,   // bool Physics.Raycast(Vector3 origin, Vector3 direction, RaycastHit& hit, float maxDistance, int layerMask)
    
    // Bot相关
    Bot_Update:                  0xB33370,   // void Bot.Update()
  };

  // ================================================================
  // 字段偏移量 (从IDA逆向分析获取)
  // ================================================================
  var OFFSET = {
    // GameManager 字段
    GM_allPlayers:      0x1C,   // Player[] 所有玩家数组
    GM_playersBL:       0x20,   // List<Player> 黑队列表
    GM_playersGR:       0x28,   // List<Player> 红队列表
    GM_myPlayer:        0x30,   // Player 本地玩家
    
    // Entity 字段
    E_team:             0x20,   // Team (int32) 队伍ID
    E_health:           0x24,   // int32 血量
    E_maxHealth:        0x28,   // int32 最大血量
    
    // Player 字段
    P_cameraRotation:   0x4C,   // Vector2 (x=yaw, y=pitch) 弧度
    P_recoil:           0x54,   // Recoil* 后座力对象
    P_characterContainer: 0x58, // Transform 角色容器
    P_clientData:       0x94,   // ClientData* 客户端数据
    P_position:         0x38,   // Vector3 位置 (在characterContainer中)
    
    // ClientData 字段
    CD_isBot:           0x1C,   // bool 是否是Bot
    CD_playerName:      0x20,   // string 玩家名称
    
    // IL2CPP 数组结构
    Array_length:       0x0C,   // uint32 数组长度
    Array_data:         0x10,   // T[] 数据起始位置
    
    // IL2CPP List结构
    List_items:         0x08,   // T[] _items 内部数组
    List_size:          0x0C,   // int _size 实际元素数量
    
    // 指针大小
    PTR_SIZE:           4,
  };

  // ================================================================
  // 骨骼索引定义
  // ================================================================
  var BONE_INDEX = {
    HEAD:    0,
    NECK:    3,
    CHEST:   7,
    PELVIS:  10,
    HAND_R:  6,
    HAND_L:  15,
  };
  
  // 骨骼Y轴偏移 (相对于脚底位置)
  var BONE_HEIGHT_OFFSET = {
    0:  1.65,   // HEAD 头部
    3:  1.45,   // NECK 颈部
    7:  1.05,   // CHEST 胸部
    10: 0.85,   // PELVIS 骨盆
    6:  0.75,   // HAND_R 右手
    15: 0.75,   // HAND_L 左手
  };

  // ================================================================
  // 自瞄配置
  // ================================================================
  var AIMBOT_CONFIG = {
    // 基础设置
    enabled:           true,      // 是否启用自瞄
    aimKey:            0,         // 瞄准按键: 0=鼠标左键, 1=鼠标右键, 2=鼠标中键
    aimKeyVK:          0x02,      // 虚拟键码: 0x02=鼠标右键 (VK_RBUTTON)
    
    // 目标选择
    aimBone:           BONE_INDEX.CHEST,  // 瞄准骨骼
    maxAimDistance:    200.0,     // 最大瞄准距离 (米)
    maxFOV:            90.0,      // 最大视野角度 (度)
    targetPriority:    'distance', // 目标优先级: 'distance', 'angle', 'health'
    
    // 筛选条件
    checkTeam:         true,      // 检查队伍 (排除友军)
    checkDead:         true,      // 检查死亡 (排除死亡玩家)
    checkVisibility:   false,     // 检查可见性 (射线检测)
    checkBot:          false,     // 是否瞄准Bot
    
    // 平滑设置
    smoothness:        1.0,       // 平滑度: 1.0=瞬间, 0.1=缓慢
    smoothRandom:      0.0,       // 随机平滑度变化
    
    // 高级设置
    targetLockTime:    500,       // 目标锁定时间 (毫秒)
    aimDelay:          0,         // 瞄准延迟 (毫秒)
    shootAfterAim:     false,     // 瞄准后自动射击
    
    // 调试设置
    debugMode:         true,      // 调试模式
    showESP:           false,     // 显示ESP
    logTargets:        true,      // 记录目标信息
  };

  // ================================================================
  // NativeFunction 缓存
  // ================================================================
  var nativeFunctions = {
    singletonGet:       null,
    getTransform:       null,
    getPosition:        null,
    isMyPlayer:         null,
    isDead:             null,
    getTeam:            null,
    addCameraRotation:  null,
    getMouseButton:     null,
    linecast:           null,
  };

  // ================================================================
  // 目标缓存
  // ================================================================
  var targetCache = {
    currentTarget:     null,      // 当前目标
    lockTime:          0,         // 锁定时间
    lastScanTime:      0,         // 上次扫描时间
    scanInterval:      50,        // 扫描间隔 (毫秒)
  };

  // ================================================================
  // 统计数据
  // ================================================================
  var stats = {
    totalScans:        0,
    targetsFound:      0,
    shotsFired:        0,
    startTime:         Date.now(),
  };

  // ================================================================
  // 初始化 NativeFunction
  // ================================================================
  function initNativeFunctions() {
    var mod = getGameAssembly();
    if (!mod) return false;
    
    var base = mod.base;
    var success = true;
    
    // Singleton<GameManager>.get_instance
    try {
      nativeFunctions.singletonGet = new NativeFunction(
        base.add(RVA.SingletonGet),
        'pointer',
        ['pointer']
      );
      log(LOG_LEVEL.INFO, '初始化', 'SingletonGet 初始化成功');
    } catch(e) {
      log(LOG_LEVEL.ERROR, '初始化', 'SingletonGet 失败: ' + e.message);
      success = false;
    }
    
    // Component.get_transform
    try {
      nativeFunctions.getTransform = new NativeFunction(
        base.add(RVA.Component_get_transform),
        'pointer',
        ['pointer', 'pointer']
      );
      log(LOG_LEVEL.INFO, '初始化', 'GetTransform 初始化成功');
    } catch(e) {
      log(LOG_LEVEL.ERROR, '初始化', 'GetTransform 失败: ' + e.message);
      success = false;
    }
    
    // Transform.get_position
    try {
      nativeFunctions.getPosition = new NativeFunction(
        base.add(RVA.Transform_get_position),
        'void',
        ['pointer', 'pointer', 'pointer']
      );
      log(LOG_LEVEL.INFO, '初始化', 'GetPosition 初始化成功');
    } catch(e) {
      log(LOG_LEVEL.ERROR, '初始化', 'GetPosition 失败: ' + e.message);
      success = false;
    }
    
    // Player.get_isMyPlayer
    try {
      nativeFunctions.isMyPlayer = new NativeFunction(
        base.add(RVA.Player_get_isMyPlayer),
        'bool',
        ['pointer', 'pointer']
      );
      log(LOG_LEVEL.INFO, '初始化', 'IsMyPlayer 初始化成功');
    } catch(e) {
      log(LOG_LEVEL.ERROR, '初始化', 'IsMyPlayer 失败: ' + e.message);
      success = false;
    }
    
    // Entity.get_isDead
    try {
      nativeFunctions.isDead = new NativeFunction(
        base.add(RVA.Entity_get_isDead),
        'bool',
        ['pointer', 'pointer']
      );
      log(LOG_LEVEL.INFO, '初始化', 'IsDead 初始化成功');
    } catch(e) {
      log(LOG_LEVEL.ERROR, '初始化', 'IsDead 失败: ' + e.message);
      success = false;
    }
    
    // Entity.get_team
    try {
      nativeFunctions.getTeam = new NativeFunction(
        base.add(RVA.Entity_get_team),
        'int32',
        ['pointer', 'pointer']
      );
      log(LOG_LEVEL.INFO, '初始化', 'GetTeam 初始化成功');
    } catch(e) {
      log(LOG_LEVEL.WARN, '初始化', 'GetTeam 失败: ' + e.message + ' (将使用内存读取)');
      nativeFunctions.getTeam = null;
    }
    
    // Player.AddCameraRotation
    try {
      nativeFunctions.addCameraRotation = new NativeFunction(
        base.add(RVA.Player_AddCameraRotation),
        'void',
        ['pointer', 'float', 'float', 'pointer']
      );
      log(LOG_LEVEL.INFO, '初始化', 'AddCameraRotation 初始化成功');
    } catch(e) {
      log(LOG_LEVEL.ERROR, '初始化', 'AddCameraRotation 失败: ' + e.message);
      success = false;
    }
    
    // Input.GetMouseButton
    try {
      nativeFunctions.getMouseButton = new NativeFunction(
        base.add(RVA.Input_GetMouseButton),
        'bool',
        ['int32', 'pointer']
      );
      log(LOG_LEVEL.INFO, '初始化', 'GetMouseButton 初始化成功');
    } catch(e) {
      log(LOG_LEVEL.WARN, '初始化', 'GetMouseButton 失败: ' + e.message);
      nativeFunctions.getMouseButton = null;
    }
    
    // Physics.Linecast
    try {
      nativeFunctions.linecast = new NativeFunction(
        base.add(RVA.Physics_Linecast),
        'bool',
        ['pointer', 'pointer', 'int32', 'pointer']
      );
      log(LOG_LEVEL.INFO, '初始化', 'Linecast 初始化成功');
    } catch(e) {
      log(LOG_LEVEL.WARN, '初始化', 'Linecast 失败: ' + e.message);
      nativeFunctions.linecast = null;
    }
    
    return success;
  }

  // ================================================================
  // 模块1: 按键检测
  // ================================================================
  
  /**
   * 检测自瞄按键是否按下
   * 算法:
   *   1. 优先使用 GetAsyncKeyState (Windows API)
   *   2. 备选使用 Input.GetMouseButton (Unity API)
   *   3. 支持鼠标按键和键盘按键
   * 
   * @returns {boolean} 按键是否按下
   */
  function isAimKeyPressed() {
    // 方法1: 使用 GetAsyncKeyState (更可靠)
    try {
      var user32 = Module.findBaseAddress('user32.dll');
      if (user32) {
        var getAsyncKeyState = new NativeFunction(
          Module.getExportByName('user32.dll', 'GetAsyncKeyState'),
          'int16',
          ['int32']
        );
        
        var key = AIMBOT_CONFIG.aimKeyVK;
        var state = getAsyncKeyState(key);
        
        // 检查最高位 (当前按下状态)
        if ((state & 0x8000) !== 0) {
          return true;
        }
      }
    } catch(e) {
      // 忽略错误，尝试备选方法
    }
    
    // 方法2: 使用 Unity Input.GetMouseButton
    if (nativeFunctions.getMouseButton) {
      try {
        var result = nativeFunctions.getMouseButton(AIMBOT_CONFIG.aimKey, ptr(0));
        return result === true || result === 1;
      } catch(e) {
        // 忽略错误
      }
    }
    
    return false;
  }
  
  /**
   * 获取按键名称 (用于日志)
   */
  function getKeyName() {
    var keyNames = {
      0x01: '鼠标左键',
      0x02: '鼠标右键',
      0x04: '鼠标中键',
    };
    return keyNames[AIMBOT_CONFIG.aimKeyVK] || '未知按键';
  }

  // ================================================================
  // 模块2: 获取玩家列表
  // ================================================================
  
  /**
   * 获取 GameManager 单例实例
   * 算法:
   *   1. 从 GM_Singleton_MethodInfo 地址读取 MethodInfo* 指针
   *   2. 将 MethodInfo* 传递给 SingletonGet 函数
   *   3. 返回 GameManager 实例指针
   * 
   * @returns {NativePointer} GameManager 实例指针
   */
  function getGameManager() {
    try {
      var base = getGameAssembly().base;
      
      // 读取 MethodInfo 指针
      var methodInfo = base.add(RVA.GM_Singleton_MethodInfo).readPointer();
      
      if (methodInfo.isNull()) {
        // 尝试直接调用 (某些情况下 MethodInfo 可以为空)
        methodInfo = ptr(0);
      }
      
      // 调用 Singleton<GameManager>.get_instance
      var gm = nativeFunctions.singletonGet(methodInfo);
      
      if (gm.isNull()) {
        return null;
      }
      
      return gm;
    } catch(e) {
      log(LOG_LEVEL.ERROR, 'GameManager', '获取失败: ' + e.message);
      return null;
    }
  }
  
  /**
   * 获取所有玩家列表
   * 算法:
   *   1. 从 GameManager 读取三个玩家列表:
   *      - allPlayers: Player[] 所有玩家数组
   *      - playersBL: List<Player> 黑队列表
   *      - playersGR: List<Player> 红队列表
   *   2. 合并去重 (使用指针地址作为key)
   *   3. 验证每个玩家指针的有效性
   * 
   * @param {NativePointer} gm - GameManager 实例
   * @returns {Array<NativePointer>} 玩家指针数组
   */
  function getAllPlayers(gm) {
    var playerMap = {};
    
    // 读取 allPlayers 数组
    try {
      var allPlayersPtr = gm.add(OFFSET.GM_allPlayers).readPointer();
      if (!allPlayersPtr.isNull()) {
        var allPlayers = readIL2CppArray(allPlayersPtr);
        for (var i = 0; i < allPlayers.length; i++) {
          var player = allPlayers[i];
          if (isValidPlayerPointer(player)) {
            playerMap[player.toString()] = player;
          }
        }
      }
    } catch(e) {
      log(LOG_LEVEL.WARN, '玩家列表', '读取 allPlayers 失败: ' + e.message);
    }
    
    // 读取 playersBL 列表
    try {
      var playersBLPtr = gm.add(OFFSET.GM_playersBL).readPointer();
      if (!playersBLPtr.isNull()) {
        var playersBL = readIL2CppList(playersBLPtr);
        for (var i = 0; i < playersBL.length; i++) {
          var player = playersBL[i];
          if (isValidPlayerPointer(player)) {
            playerMap[player.toString()] = player;
          }
        }
      }
    } catch(e) {
      // 忽略错误
    }
    
    // 读取 playersGR 列表
    try {
      var playersGRPtr = gm.add(OFFSET.GM_playersGR).readPointer();
      if (!playersGRPtr.isNull()) {
        var playersGR = readIL2CppList(playersGRPtr);
        for (var i = 0; i < playersGR.length; i++) {
          var player = playersGR[i];
          if (isValidPlayerPointer(player)) {
            playerMap[player.toString()] = player;
          }
        }
      }
    } catch(e) {
      // 忽略错误
    }
    
    return Object.values(playerMap);
  }
  
  /**
   * 读取 IL2CPP 数组
   */
  function readIL2CppArray(arrayPtr) {
    var result = [];
    if (!arrayPtr || arrayPtr.isNull()) return result;
    
    try {
      var length = arrayPtr.add(OFFSET.Array_length).readU32();
      for (var i = 0; i < length; i++) {
        var elemPtr = arrayPtr.add(OFFSET.Array_data + i * OFFSET.PTR_SIZE).readPointer();
        if (!elemPtr.isNull()) {
          result.push(elemPtr);
        }
      }
    } catch(e) {
      // 忽略错误
    }
    
    return result;
  }
  
  /**
   * 读取 IL2CPP List
   */
  function readIL2CppList(listPtr) {
    var result = [];
    if (!listPtr || listPtr.isNull()) return result;
    
    try {
      var itemsPtr = listPtr.add(OFFSET.List_items).readPointer();
      var size = listPtr.add(OFFSET.List_size).readS32();
      
      if (!itemsPtr.isNull() && size > 0) {
        for (var i = 0; i < size; i++) {
          var elemPtr = itemsPtr.add(OFFSET.Array_data + i * OFFSET.PTR_SIZE).readPointer();
          if (!elemPtr.isNull()) {
            result.push(elemPtr);
          }
        }
      }
    } catch(e) {
      // 忽略错误
    }
    
    return result;
  }
  
  /**
   * 验证玩家指针有效性
   */
  function isValidPlayerPointer(playerPtr) {
    if (!playerPtr || playerPtr.isNull()) return false;
    
    try {
      // 检查队伍ID是否在有效范围内 (0=无队伍, 1=黑队, 2=红队)
      var team = playerPtr.add(OFFSET.E_team).readS32();
      return team >= 0 && team <= 2;
    } catch(e) {
      return false;
    }
  }

  // ================================================================
  // 模块3: 获取本地玩家
  // ================================================================
  
  /**
   * 获取本地玩家对象
   * 算法:
   *   1. 从 GameManager.myPlayer 字段读取
   *   2. 或遍历所有玩家检查 isMyPlayer 属性
   * 
   * @param {NativePointer} gm - GameManager 实例
   * @returns {NativePointer} 本地玩家指针
   */
  function getMyPlayer(gm) {
    // 方法1: 从 GameManager.myPlayer 字段读取
    try {
      var myPlayerPtr = gm.add(OFFSET.GM_myPlayer).readPointer();
      if (!myPlayerPtr.isNull()) {
        return myPlayerPtr;
      }
    } catch(e) {
      // 忽略错误
    }
    
    // 方法2: 遍历所有玩家检查 isMyPlayer
    try {
      var allPlayers = getAllPlayers(gm);
      for (var i = 0; i < allPlayers.length; i++) {
        var player = allPlayers[i];
        if (nativeFunctions.isMyPlayer(player, ptr(0))) {
          return player;
        }
      }
    } catch(e) {
      // 忽略错误
    }
    
    return null;
  }

  // ================================================================
  // 模块4: 目标筛选算法
  // ================================================================
  
  /**
   * 选择最佳目标
   * 算法:
   *   1. 检查目标缓存是否有效
   *   2. 遍历所有玩家应用筛选条件
   *   3. 计算每个有效目标的得分
   *   4. 选择得分最低的目标
   * 
   * 筛选条件:
   *   - 排除自己
   *   - 排除死亡玩家
   *   - 排除同队玩家
   *   - 排除超出距离的玩家
   *   - 排除超出FOV的玩家
   *   - 排除被遮挡的玩家 (可选)
   * 
   * 得分计算:
   *   score = distanceWeight * distance + angleWeight * angleDiff
   * 
   * @param {NativePointer} gm - GameManager 实例
   * @param {NativePointer} myPlayer - 本地玩家
   * @returns {NativePointer} 最佳目标指针
   */
  function selectBestTarget(gm, myPlayer) {
    var now = Date.now();
    
    // 检查缓存目标是否有效
    if (targetCache.currentTarget && 
        (now - targetCache.lockTime < AIMBOT_CONFIG.targetLockTime)) {
      if (isTargetStillValid(targetCache.currentTarget, myPlayer)) {
        return targetCache.currentTarget;
      }
    }
    
    // 获取所有玩家
    var allPlayers = getAllPlayers(gm);
    if (allPlayers.length === 0) {
      return null;
    }
    
    // 获取本地玩家信息
    var myPos = getPlayerPosition(myPlayer);
    var myAngle = getPlayerCameraAngle(myPlayer);
    var myTeam = getPlayerTeam(myPlayer);
    
    if (!myPos || !myAngle) {
      return null;
    }
    
    // 筛选目标
    var validTargets = [];
    
    for (var i = 0; i < allPlayers.length; i++) {
      var player = allPlayers[i];
      
      // 筛选条件1: 排除自己
      if (player.equals(myPlayer)) {
        continue;
      }
      
      // 筛选条件2: 排除死亡玩家
      if (AIMBOT_CONFIG.checkDead) {
        try {
          var isDead = nativeFunctions.isDead(player, ptr(0));
          if (isDead) {
            continue;
          }
        } catch(e) {
          // 忽略错误
        }
      }
      
      // 筛选条件3: 排除同队玩家
      if (AIMBOT_CONFIG.checkTeam) {
        var team = getPlayerTeam(player);
        if (team === myTeam && team !== 0) {
          continue;
        }
      }
      
      // 获取目标位置
      var targetPos = getBonePosition(player, AIMBOT_CONFIG.aimBone);
      if (!targetPos) {
        continue;
      }
      
      // 筛选条件4: 距离检测
      var distance = calculateDistance3D(myPos, targetPos);
      if (distance > AIMBOT_CONFIG.maxAimDistance) {
        continue;
      }
      
      // 计算角度差
      var targetAngle = calculateAimAngle(myPos, targetPos);
      if (!targetAngle) {
        continue;
      }
      
      var angleDiff = calculateAngleDifference(myAngle, targetAngle);
      
      // 筛选条件5: FOV检测
      if (angleDiff > AIMBOT_CONFIG.maxFOV) {
        continue;
      }
      
      // 筛选条件6: 可见性检测
      if (AIMBOT_CONFIG.checkVisibility) {
        var isVisible = checkLineOfSight(myPos, targetPos);
        if (!isVisible) {
          continue;
        }
      }
      
      // 计算得分
      var score = calculateTargetScore(distance, angleDiff, player);
      
      validTargets.push({
        player: player,
        distance: distance,
        angleDiff: angleDiff,
        score: score,
      });
    }
    
    // 排序选择最佳目标
    if (validTargets.length === 0) {
      targetCache.currentTarget = null;
      return null;
    }
    
    // 按得分排序 (得分越低越好)
    validTargets.sort(function(a, b) {
      return a.score - b.score;
    });
    
    var bestTarget = validTargets[0].player;
    
    // 更新缓存
    targetCache.currentTarget = bestTarget;
    targetCache.lockTime = now;
    
    if (AIMBOT_CONFIG.logTargets) {
      log(LOG_LEVEL.INFO, '目标选择', 
          '找到目标: 距离=' + validTargets[0].distance.toFixed(1) + 'm ' +
          '角度=' + validTargets[0].angleDiff.toFixed(1) + '° ' +
          '得分=' + validTargets[0].score.toFixed(2));
    }
    
    stats.targetsFound++;
    
    return bestTarget;
  }
  
  /**
   * 检查缓存目标是否仍然有效
   */
  function isTargetStillValid(target, myPlayer) {
    if (!target || target.isNull()) return false;
    
    // 检查是否死亡
    if (AIMBOT_CONFIG.checkDead) {
      try {
        if (nativeFunctions.isDead(target, ptr(0))) {
          return false;
        }
      } catch(e) {
        return false;
      }
    }
    
    // 检查距离
    var myPos = getPlayerPosition(myPlayer);
    var targetPos = getBonePosition(target, AIMBOT_CONFIG.aimBone);
    
    if (!myPos || !targetPos) return false;
    
    var distance = calculateDistance3D(myPos, targetPos);
    if (distance > AIMBOT_CONFIG.maxAimDistance) {
      return false;
    }
    
    return true;
  }
  
  /**
   * 计算目标得分
   * 得分越低越优先
   */
  function calculateTargetScore(distance, angleDiff, player) {
    var score = 0;
    
    switch (AIMBOT_CONFIG.targetPriority) {
      case 'distance':
        // 距离优先
        score = distance;
        break;
        
      case 'angle':
        // 角度优先 (准星附近的敌人)
        score = angleDiff * 10;
        break;
        
      case 'health':
        // 血量优先 (血量少的敌人)
        var health = getPlayerHealth(player);
        score = distance + (health / 100) * 50;
        break;
        
      default:
        // 综合评分
        var distanceWeight = 1.0;
        var angleWeight = 2.0;
        score = distanceWeight * distance + angleWeight * angleDiff;
    }
    
    return score;
  }

  // ================================================================
  // 模块5: 队伍检查
  // ================================================================
  
  /**
   * 获取玩家队伍
   * 算法:
   *   1. 优先使用 Entity.get_team() 方法
   *   2. 备选直接读取内存中的队伍字段
   * 
   * @param {NativePointer} player - 玩家指针
   * @returns {number} 队伍ID (0=无队伍, 1=黑队, 2=红队)
   */
  function getPlayerTeam(player) {
    // 方法1: 使用 Entity.get_team() 方法
    if (nativeFunctions.getTeam) {
      try {
        var team = nativeFunctions.getTeam(player, ptr(0));
        return team;
      } catch(e) {
        // 忽略错误，使用备选方法
      }
    }
    
    // 方法2: 直接读取内存
    try {
      var team = player.add(OFFSET.E_team).readS32();
      return team;
    } catch(e) {
      return 0;
    }
  }
  
  /**
   * 判断是否是敌人
   */
  function isEnemy(player, myPlayer) {
    var myTeam = getPlayerTeam(myPlayer);
    var targetTeam = getPlayerTeam(player);
    
    // 0表示无队伍，所有人都可能是敌人
    if (myTeam === 0 || targetTeam === 0) {
      return true;
    }
    
    return myTeam !== targetTeam;
  }

  // ================================================================
  // 模块6: 距离计算
  // ================================================================
  
  /**
   * 计算3D空间距离
   * 算法: distance = sqrt(dx^2 + dy^2 + dz^2)
   * 
   * @param {Object} pos1 - 位置1 {x, y, z}
   * @param {Object} pos2 - 位置2 {x, y, z}
   * @returns {number} 距离 (米)
   */
  function calculateDistance3D(pos1, pos2) {
    var dx = pos2.x - pos1.x;
    var dy = pos2.y - pos1.y;
    var dz = pos2.z - pos1.z;
    
    return Math.sqrt(dx * dx + dy * dy + dz * dz);
  }
  
  /**
   * 计算2D水平距离
   */
  function calculateDistance2D(pos1, pos2) {
    var dx = pos2.x - pos1.x;
    var dz = pos2.z - pos1.z;
    
    return Math.sqrt(dx * dx + dz * dz);
  }

  // ================================================================
  // 模块7: 可见性检测
  // ================================================================
  
  /**
   * 检查视线是否被遮挡
   * 算法:
   *   1. 从玩家眼睛位置发射射线到目标位置
   *   2. 使用 Physics.Linecast 检测碰撞
   *   3. 使用 LayerMask 排除玩家层
   * 
   * LayerMask 说明:
   *   - 0xFFFFFF00: 检测8-31层 (障碍物层)
   *   - 排除0-7层 (玩家、角色层)
   * 
   * @param {Object} from - 起点 {x, y, z}
   * @param {Object} to - 终点 {x, y, z}
   * @returns {boolean} true=可见, false=被遮挡
   */
  function checkLineOfSight(from, to) {
    if (!nativeFunctions.linecast) {
      return true;  // 没有linecast函数，默认可见
    }
    
    try {
      // 眼睛高度偏移 (从眼睛位置发射射线)
      var eyeHeight = 0.25;
      
      // 构造起点 (玩家眼睛位置)
      var start = {
        x: from.x,
        y: from.y + eyeHeight,
        z: from.z
      };
      
      // 分配内存存储 Vector3
      var startBuf = Memory.alloc(12);
      startBuf.writeFloat(start.x);
      startBuf.add(4).writeFloat(start.y);
      startBuf.add(8).writeFloat(start.z);
      
      var endBuf = Memory.alloc(12);
      endBuf.writeFloat(to.x);
      endBuf.add(4).writeFloat(to.y);
      endBuf.add(8).writeFloat(to.z);
      
      // LayerMask: 排除玩家层 (0-7层)
      var layerMask = 0xFFFFFF00;
      
      // 调用 Physics.Linecast
      var hit = nativeFunctions.linecast(startBuf, endBuf, layerMask, ptr(0));
      
      // hit=true 表示有碰撞 (被遮挡)
      // hit=false 表示无碰撞 (可见)
      return !hit;
      
    } catch(e) {
      log(LOG_LEVEL.WARN, '可见性检测', 'Linecast 失败: ' + e.message);
      return true;  // 异常时默认可见
    }
  }

  // ================================================================
  // 模块8: 位置和角度获取
  // ================================================================
  
  /**
   * 获取玩家位置
   * 算法:
   *   1. 调用 Component.get_transform() 获取 Transform
   *   2. 调用 Transform.get_position() 获取位置
   *   3. 备选直接读取 characterContainer 中的位置字段
   * 
   * @param {NativePointer} player - 玩家指针
   * @returns {Object} 位置 {x, y, z} 或 null
   */
  function getPlayerPosition(player) {
    if (!player || player.isNull()) return null;
    
    // 方法1: 通过 Transform.get_position
    try {
      var transform = nativeFunctions.getTransform(player, ptr(0));
      if (transform && !transform.isNull()) {
        var posBuf = Memory.alloc(12);
        nativeFunctions.getPosition(posBuf, transform, ptr(0));
        
        var x = posBuf.readFloat();
        var y = posBuf.add(4).readFloat();
        var z = posBuf.add(8).readFloat();
        
        // 验证坐标有效性
        if (Math.abs(x) < 10000 && Math.abs(y) < 10000 && Math.abs(z) < 10000) {
          return { x: x, y: y, z: z };
        }
      }
    } catch(e) {
      // 忽略错误
    }
    
    // 方法2: 直接读取 characterContainer 中的位置
    try {
      var container = player.add(OFFSET.P_characterContainer).readPointer();
      if (container && !container.isNull()) {
        var x = container.add(OFFSET.P_position).readFloat();
        var y = container.add(OFFSET.P_position + 4).readFloat();
        var z = container.add(OFFSET.P_position + 8).readFloat();
        
        if (Math.abs(x) < 10000 && Math.abs(y) < 10000 && Math.abs(z) < 10000) {
          return { x: x, y: y, z: z };
        }
      }
    } catch(e) {
      // 忽略错误
    }
    
    return null;
  }
  
  /**
   * 获取骨骼位置
   * 算法:
   *   1. 获取玩家基础位置
   *   2. 根据骨骼索引添加高度偏移
   * 
   * @param {NativePointer} player - 玩家指针
   * @param {number} boneIndex - 骨骼索引
   * @returns {Object} 位置 {x, y, z} 或 null
   */
  function getBonePosition(player, boneIndex) {
    var pos = getPlayerPosition(player);
    if (!pos) return null;
    
    // 添加骨骼高度偏移
    var yOffset = BONE_HEIGHT_OFFSET[boneIndex];
    if (yOffset !== undefined) {
      pos.y += yOffset;
    }
    
    return pos;
  }
  
  /**
   * 获取玩家相机角度
   * 算法:
   *   直接读取 Player.cameraRotation 字段
   *   - x: yaw (偏航角) 弧度
   *   - y: pitch (俯仰角) 弧度
   * 
   * @param {NativePointer} player - 玩家指针
   * @returns {Object} 角度 {yaw, pitch} 弧度
   */
  function getPlayerCameraAngle(player) {
    if (!player || player.isNull()) return null;
    
    try {
      var yaw = player.add(OFFSET.P_cameraRotation).readFloat();
      var pitch = player.add(OFFSET.P_cameraRotation + 4).readFloat();
      
      return { yaw: yaw, pitch: pitch };
    } catch(e) {
      return null;
    }
  }
  
  /**
   * 获取玩家血量
   */
  function getPlayerHealth(player) {
    if (!player || player.isNull()) return 0;
    
    try {
      var health = player.add(OFFSET.E_health).readS32();
      return health;
    } catch(e) {
      return 0;
    }
  }

  // ================================================================
  // 模块9: 瞄准角度计算
  // ================================================================
  
  /**
   * 计算瞄准角度
   * 算法:
   *   yaw = atan2(dx, dz)          // 偏航角 (水平)
   *   pitch = atan2(dy, hDist)     // 俯仰角 (垂直)
   *   
   * 其中:
   *   dx = targetX - myX
   *   dy = targetY - myY
   *   dz = targetZ - myZ
   *   hDist = sqrt(dx^2 + dz^2)    // 水平距离
   * 
   * @param {Object} from - 起点 {x, y, z}
   * @param {Object} to - 终点 {x, y, z}
   * @returns {Object} 角度 {yaw, pitch} 弧度
   */
  function calculateAimAngle(from, to) {
    var dx = to.x - from.x;
    var dy = to.y - from.y;
    var dz = to.z - from.z;
    
    // 计算水平距离
    var hDist = Math.sqrt(dx * dx + dz * dz);
    
    if (hDist < 0.01) {
      return null;  // 距离太近，无法计算
    }
    
    // 计算偏航角
    var yaw = Math.atan2(dx, dz);
    
    // 计算俯仰角
    var pitch = Math.atan2(dy, hDist);
    
    return { yaw: yaw, pitch: pitch };
  }
  
  /**
   * 计算角度差
   * 返回角度差的绝对值 (度数)
   */
  function calculateAngleDifference(angle1, angle2) {
    var dyaw = normalizeAngle(angle2.yaw - angle1.yaw);
    var dpitch = normalizeAngle(angle2.pitch - angle1.pitch);
    
    // 转换为度数
    var dyawDeg = Math.abs(dyaw * 180 / Math.PI);
    var dpitchDeg = Math.abs(dpitch * 180 / Math.PI);
    
    // 返回总角度差
    return Math.sqrt(dyawDeg * dyawDeg + dpitchDeg * dpitchDeg);
  }
  
  /**
   * 归一化角度到 [-PI, PI] 范围
   */
  function normalizeAngle(angle) {
    while (angle > Math.PI) angle -= 2 * Math.PI;
    while (angle < -Math.PI) angle += 2 * Math.PI;
    return angle;
  }

  // ================================================================
  // 模块10: 视角设置
  // ================================================================
  
  /**
   * 应用平滑瞄准
   * 算法:
   *   smoothedAngle = currentAngle + (targetAngle - currentAngle) * smoothness
   *   
   * smoothness 参数:
   *   1.0 = 瞬间瞄准
   *   0.5 = 中等平滑
   *   0.1 = 非常平滑 (缓慢移动)
   * 
   * @param {Object} currentAngle - 当前角度 {yaw, pitch}
   * @param {Object} targetAngle - 目标角度 {yaw, pitch}
   * @param {number} smoothness - 平滑度 [0.0, 1.0]
   * @returns {Object} 平滑后的角度 {yaw, pitch}
   */
  function applySmoothing(currentAngle, targetAngle, smoothness) {
    // 添加随机平滑度变化 (更自然)
    var actualSmoothness = smoothness;
    if (AIMBOT_CONFIG.smoothRandom > 0) {
      var randomFactor = (Math.random() - 0.5) * 2 * AIMBOT_CONFIG.smoothRandom;
      actualSmoothness = smoothness * (1 + randomFactor);
      actualSmoothness = Math.max(0.01, Math.min(1.0, actualSmoothness));
    }
    
    // 计算角度差
    var dyaw = normalizeAngle(targetAngle.yaw - currentAngle.yaw);
    var dpitch = normalizeAngle(targetAngle.pitch - currentAngle.pitch);
    
    // 应用平滑
    var smoothedYaw = currentAngle.yaw + dyaw * actualSmoothness;
    var smoothedPitch = currentAngle.pitch + dpitch * actualSmoothness;
    
    return { yaw: smoothedYaw, pitch: smoothedPitch };
  }
  
  /**
   * 设置相机角度
   * 算法:
   *   1. 计算角度增量 (deltaYaw, deltaPitch)
   *   2. 调用 Player.AddCameraRotation(deltaYaw, deltaPitch)
   *   3. 重置后座力标志 (防止游戏拉回准星)
   * 
   * @param {NativePointer} player - 玩家指针
   * @param {number} deltaYaw - 偏航角增量 (弧度)
   * @param {number} deltaPitch - 俯仰角增量 (弧度)
   */
  function setCameraAngle(player, deltaYaw, deltaPitch) {
    if (!player || player.isNull()) return;
    
    try {
      // 调用 Player.AddCameraRotation
      nativeFunctions.addCameraRotation(player, deltaYaw, deltaPitch, ptr(0));
      
      // 重置后座力标志 (防止游戏拉回准星)
      resetRecoilFlags(player);
      
    } catch(e) {
      log(LOG_LEVEL.ERROR, '视角设置', 'AddCameraRotation 失败: ' + e.message);
    }
  }
  
  /**
   * 重置后座力标志
   * 算法:
   *   清除 characterContainer 中的后座力相关标志
   *   防止游戏自动拉回准星
   */
  function resetRecoilFlags(player) {
    if (!player || player.isNull()) return;
    
    try {
      var container = player.add(OFFSET.P_characterContainer).readPointer();
      if (container && !container.isNull()) {
        // 清除后座力标志 (具体偏移需要根据游戏版本调整)
        // 这里使用 characterContainer 而非 recoil 对象
        container.add(0x58).writeU8(0);
      }
    } catch(e) {
      // 忽略错误
    }
  }

  // ================================================================
  // 主循环
  // ================================================================
  
  /**
   * 自瞄主循环
   * 流程:
   *   1. 检测按键
   *   2. 获取 GameManager
   *   3. 获取本地玩家
   *   4. 选择目标
   *   5. 计算瞄准角度
   *   6. 应用平滑
   *   7. 设置视角
   */
  function aimbotLoop() {
    if (!AIMBOT_CONFIG.enabled) {
      return;
    }
    
    // 1. 检测按键
    if (!isAimKeyPressed()) {
      // 按键释放时清除缓存
      targetCache.currentTarget = null;
      return;
    }
    
    // 2. 获取 GameManager
    var gm = getGameManager();
    if (!gm) {
      return;
    }
    
    // 3. 获取本地玩家
    var myPlayer = getMyPlayer(gm);
    if (!myPlayer) {
      return;
    }
    
    // 4. 选择目标
    var target = selectBestTarget(gm, myPlayer);
    if (!target) {
      return;
    }
    
    // 5. 获取位置和角度
    var myPos = getPlayerPosition(myPlayer);
    var myAngle = getPlayerCameraAngle(myPlayer);
    var targetPos = getBonePosition(target, AIMBOT_CONFIG.aimBone);
    
    if (!myPos || !myAngle || !targetPos) {
      return;
    }
    
    // 6. 计算瞄准角度
    var targetAngle = calculateAimAngle(myPos, targetPos);
    if (!targetAngle) {
      return;
    }
    
    // 7. 应用平滑
    var smoothedAngle = applySmoothing(myAngle, targetAngle, AIMBOT_CONFIG.smoothness);
    
    // 8. 计算角度增量
    var deltaYaw = normalizeAngle(smoothedAngle.yaw - myAngle.yaw);
    var deltaPitch = normalizeAngle(smoothedAngle.pitch - myAngle.pitch);
    
    // 9. 设置视角
    setCameraAngle(myPlayer, deltaYaw, deltaPitch);
    
    // 更新统计
    stats.totalScans++;
  }

  // ================================================================
  // 自瞄控制接口
  // ================================================================
  var aimModule = (function() {
    var _enabled = false;
    var _timer = null;

    return {
      enable: function() {
        if (_enabled) {
          log(LOG_LEVEL.INFO, '自瞄', '已经启用，跳过');
          return;
        }
        log(LOG_LEVEL.INFO, '系统', '=====================================');
        log(LOG_LEVEL.INFO, '系统', 'UnityCrossFire 自瞄模块启动');
        log(LOG_LEVEL.INFO, '系统', '=====================================');
        
        if (!initNativeFunctions()) {
          log(LOG_LEVEL.ERROR, '系统', '初始化失败，无法启动自瞄');
          return;
        }
        
        log(LOG_LEVEL.INFO, '系统', 'NativeFunction 初始化成功');
        log(LOG_LEVEL.INFO, '配置', '瞄准按键: ' + getKeyName());
        log(LOG_LEVEL.INFO, '配置', '最大距离: ' + AIMBOT_CONFIG.maxAimDistance + 'm');
        log(LOG_LEVEL.INFO, '配置', '最大FOV: ' + AIMBOT_CONFIG.maxFOV + '°');
        log(LOG_LEVEL.INFO, '配置', '平滑度: ' + AIMBOT_CONFIG.smoothness);
        log(LOG_LEVEL.INFO, '配置', '可见性检测: ' + (AIMBOT_CONFIG.checkVisibility ? '开' : '关'));
        
        _enabled = true;
        _timer = setInterval(aimbotLoop, 10);
        
        log(LOG_LEVEL.INFO, '系统', '自瞄模块已启动，按 ' + getKeyName() + ' 激活');
      },

      disable: function() {
        if (!_enabled) return;
        if (_timer) {
          clearInterval(_timer);
          _timer = null;
        }
        targetCache.currentTarget = null;
        _enabled = false;
        log(LOG_LEVEL.INFO, '自瞄', '已禁用');
      },

      toggle: function() {
        if (_enabled) this.disable();
        else this.enable();
      },

      isEnabled: function() {
        return _enabled;
      },

      setConfig: function(cfg) {
        if (cfg.aimKey !== undefined) AIMBOT_CONFIG.aimKey = cfg.aimKey;
        if (cfg.aimKeyVK !== undefined) AIMBOT_CONFIG.aimKeyVK = cfg.aimKeyVK;
        if (cfg.smoothness !== undefined) AIMBOT_CONFIG.smoothness = cfg.smoothness;
        if (cfg.smoothRandom !== undefined) AIMBOT_CONFIG.smoothRandom = cfg.smoothRandom;
        if (cfg.maxAimDistance !== undefined) AIMBOT_CONFIG.maxAimDistance = cfg.maxAimDistance;
        if (cfg.maxFOV !== undefined) AIMBOT_CONFIG.maxFOV = cfg.maxFOV;
        if (cfg.checkTeam !== undefined) AIMBOT_CONFIG.checkTeam = cfg.checkTeam;
        if (cfg.checkDead !== undefined) AIMBOT_CONFIG.checkDead = cfg.checkDead;
        if (cfg.checkVisibility !== undefined) AIMBOT_CONFIG.checkVisibility = cfg.checkVisibility;
        if (cfg.checkBot !== undefined) AIMBOT_CONFIG.checkBot = cfg.checkBot;
        if (cfg.targetPriority !== undefined) AIMBOT_CONFIG.targetPriority = cfg.targetPriority;
        if (cfg.targetLockTime !== undefined) AIMBOT_CONFIG.targetLockTime = cfg.targetLockTime;
        if (cfg.aimDelay !== undefined) AIMBOT_CONFIG.aimDelay = cfg.aimDelay;
        if (cfg.shootAfterAim !== undefined) AIMBOT_CONFIG.shootAfterAim = cfg.shootAfterAim;
        if (cfg.logTargets !== undefined) AIMBOT_CONFIG.logTargets = cfg.logTargets;
        if (cfg.aimBone !== undefined) AIMBOT_CONFIG.aimBone = cfg.aimBone;
        log(LOG_LEVEL.INFO, '自瞄', '配置更新: ' + JSON.stringify(cfg));
      },

      getConfig: function() {
        return {
          enabled: _enabled,
          aimKey: AIMBOT_CONFIG.aimKey,
          aimKeyVK: AIMBOT_CONFIG.aimKeyVK,
          smoothness: AIMBOT_CONFIG.smoothness,
          smoothRandom: AIMBOT_CONFIG.smoothRandom,
          maxAimDistance: AIMBOT_CONFIG.maxAimDistance,
          maxFOV: AIMBOT_CONFIG.maxFOV,
          checkTeam: AIMBOT_CONFIG.checkTeam,
          checkDead: AIMBOT_CONFIG.checkDead,
          checkVisibility: AIMBOT_CONFIG.checkVisibility,
          checkBot: AIMBOT_CONFIG.checkBot,
          targetPriority: AIMBOT_CONFIG.targetPriority,
          targetLockTime: AIMBOT_CONFIG.targetLockTime,
          aimDelay: AIMBOT_CONFIG.aimDelay,
          shootAfterAim: AIMBOT_CONFIG.shootAfterAim,
          logTargets: AIMBOT_CONFIG.logTargets,
          aimBone: AIMBOT_CONFIG.aimBone,
          totalScans: stats.totalScans,
          targetsFound: stats.targetsFound,
        };
      },

      getTarget: function() {
        return targetCache.currentTarget;
      },
    };
  })();

  // ================================================================
  // Frida RPC 导出 — 供外部工具调用
  // ================================================================
  rpc.exports = {
    aimEnable: function() {
      aimModule.enable();
      return 'ok';
    },
    aim_enable: function() {
      aimModule.enable();
      return 'ok';
    },
    aimDisable: function() {
      aimModule.disable();
      return 'ok';
    },
    aim_disable: function() {
      aimModule.disable();
      return 'ok';
    },
    aimToggle: function() {
      aimModule.toggle();
      return aimModule.isEnabled() ? 'enabled' : 'disabled';
    },
    aim_toggle: function() {
      aimModule.toggle();
      return aimModule.isEnabled() ? 'enabled' : 'disabled';
    },
    aimStatus: function() {
      return aimModule.isEnabled() ? 'enabled' : 'disabled';
    },
    aim_status: function() {
      return aimModule.isEnabled() ? 'enabled' : 'disabled';
    },
    aimSetConfig: function(jsonStr) {
      try {
        aimModule.setConfig(JSON.parse(jsonStr));
        return 'ok';
      } catch(e) {
        return 'error: ' + e.message;
      }
    },
    aim_set_config: function(jsonStr) {
      try {
        aimModule.setConfig(JSON.parse(jsonStr));
        return 'ok';
      } catch(e) {
        return 'error: ' + e.message;
      }
    },
    aimGetStatus: function() {
      var cfg = aimModule.getConfig();
      return JSON.stringify(cfg);
    },
    aim_get_status: function() {
      var cfg = aimModule.getConfig();
      return JSON.stringify(cfg);
    },
  };

  // 自动启用
  log(LOG_LEVEL.INFO, '系统', '脚本加载完成，正在自动启用...');
  aimModule.enable();
  
})();
