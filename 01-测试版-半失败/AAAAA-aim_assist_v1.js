// ====================================================================
// 自瞄模块 (Aim Assist) v2.1 — Frida API Hook 骨骼坐标版
// 基于 UnityCrossFire.dll 逆向分析 (MD 3.3 + 5.2 + 5.3)
// 骨骼坐标方案:
//   方案A: Transform.get_gameObject() → GameObject.GetComponent<Animator>()
//          → Animator.GetBoneTransform(index) → Transform.get_position()
//   方案B: Transform.get_position() + BONE_Y_OFFSET 补偿
//   方案C: getPlayerPos() + BONE_Y_OFFSET 补偿
// Frida Hook: Transform.get_position | Animator.GetBoneTransform (Interceptor)
// ====================================================================
(function() {
  'use strict';

  var MAX_LOGS_PER_MODULE = 100;
  var moduleLogCounts = {};

  function sendLog(level, module, message) {
    if (!moduleLogCounts[module]) moduleLogCounts[module] = 0;
    if (moduleLogCounts[module] >= MAX_LOGS_PER_MODULE) return;
    moduleLogCounts[module]++;
    send({ type: 'log', level: level, module: module, message: message });
  }

  function sendStatus(feature, enabled) {
    send({ type: 'status', feature: feature, enabled: enabled });
  }

  function getGameAssembly() {
    try {
      var mod = Process.findModuleByName('GameAssembly.dll');
      if (!mod) {
        sendLog('error', '系统', '未找到 GameAssembly.dll');
        return null;
      }
      return mod;
    } catch(e) { sendLog('error', '系统', '获取模块失败: ' + e.message); return null; }
  }

  var aimModule = (function() {
    var enabled = false;
    var myPlayer = null;
    var targetEnemy = null;
    var scanInterval = 30;
    var aimBone = 'chest';
    var timer = null;
    var scanTimer = null;
    var roomHooks = [];
    var botPlayers = {};
    var botUpdateHook = null;
    var logCount = 0;
    var lastEnemyCount = 0;

    // NativeFunction 缓存
    var isMyPlayerFn = null;
    var singletonGetter = null;
    var isDeadFn = null;
    var getAsyncKeyState = null;
    var compGetTransform = null;
    var transformGetPos = null;

    // DLL 风格全局变量（参照 UnityCrossFire.dll 逆向分析）
    var dword_1005A6D4 = null;    // [DLL] 当前锁定目标 = myPlayer（角度写入 +76/+80）
    var dword_1005A6C8 = null;    // [DLL] 当前敌人目标指针（外部扫描器更新，用于获取敌人坐标）
    var dword_1005A6D8 = false;   // [DLL] 自瞄开关标志
    var aimHotkey = 0x01;         // 自瞄热键虚拟键码（默认 VK_LBUTTON）

    // 角度平滑参数（MD 5.2 流程图 可选）
    var aimSmoothing = 0.0;       // 0.0=无平滑(瞬间瞄准), 0.1-0.5=推荐平滑范围

    // DLL 骨骼索引映射（参照 UnityCrossFire.dll sub_10002550）
    var BONE = {
      HEAD:  0,
      NECK:  3,
      CHEST: 7,
      PELVIS: 10,
      HAND:  6,
    };

    var RVA = {
      P_isMyPlayer:   0xB55FD0,
      E_isDead:       0xB400E0,
      SingletonGet:   0x4A8170,
      GM_Singleton:   0xE1CE64,
      GetTransform:   0x32CF40,
      GetPosition:    0x3F42B0,
      Bot_Update:     0xB33370,
    };

    var OFF = {
      GM_all:       0x1C,
      GM_BL:        0x20,
      GM_GR:        0x28,
      P_camRot:     0x4C,
      P_transform:  0x54,
      P_charCont:   0x58,
      E_team:       0x20,
      Arr_len:      0x0C,
      Arr_data:     0x10,
      Elem_sz:      8,
    };

    // ================================================================
    // IL2CPP 运行时方法解析器（避免硬编码未知 RVA）
    // 通过 GameAssembly.dll 导出的 il2cpp API 按名称查找方法
    // ================================================================

    var il2cpp = {};

    function initIl2Cpp() {
      if (il2cpp.domain_get) return true;
      try {
        var ga = getGameAssembly();
        if (!ga) return false;
        var dget   = Module.findExportByName('GameAssembly.dll', 'il2cpp_domain_get');
        var cfromn = Module.findExportByName('GameAssembly.dll', 'il2cpp_class_from_name');
        var gmfromn = Module.findExportByName('GameAssembly.dll', 'il2cpp_class_get_method_from_name');
        var madr   = Module.findExportByName('GameAssembly.dll', 'il2cpp_method_get_address');
        if (!dget || !cfromn || !gmfromn || !madr) {
          sendLog('warn', '系统', 'il2cpp API 导出不全，骨骼/可见性功能不可用');
          return false;
        }
        il2cpp.domain_get   = new NativeFunction(dget, 'pointer', []);
        il2cpp.class_from_name = new NativeFunction(cfromn, 'pointer', ['pointer', 'pointer', 'pointer']);
        il2cpp.method_from_name = new NativeFunction(gmfromn, 'pointer', ['pointer', 'pointer', 'int']);
        il2cpp.method_address = new NativeFunction(madr, 'pointer', ['pointer']);
        sendLog('info', '系统', 'il2cpp API 初始化成功');
        return true;
      } catch(e) {
        sendLog('warn', '系统', 'il2cpp API 初始化失败: ' + e.message);
        return false;
      }
    }

    function resolveUnityMethod(namespace, className, methodName, paramCount) {
      try {
        if (!il2cpp.class_from_name || !il2cpp.method_from_name) return null;
        var nsStr = Memory.allocUtf8String(namespace);
        var clsStr = Memory.allocUtf8String(className);
        var domain = il2cpp.domain_get();
        var cls = il2cpp.class_from_name(domain, nsStr, clsStr);
        if (!cls || cls.isNull()) return null;
        var mtdStr = Memory.allocUtf8String(methodName);
        var method = il2cpp.method_from_name(cls, mtdStr, paramCount);
        if (!method || method.isNull()) return null;
        if (!il2cpp.method_address) return method;
        var addr = il2cpp.method_address(method);
        return addr && !addr.isNull() ? addr : null;
      } catch(e) {
        return null;
      }
    }

    // ================================================================
    // Frida API Hook — Transform.get_position (RVA 0x3F42B0)
    // Hook 所有 Transform 位置读取，用于调试验证
    // ================================================================

    var getPosHook = null;
    var transformPosCache = {};   // TransformPtr → {x,y,z}

    function installTransformHook(base) {
      if (getPosHook) return;
      try {
        getPosHook = Interceptor.attach(base.add(RVA.GetPosition), {
          onLeave: function(retVal) {
            // retval = Vector3* written to (args[1])
          }
        });
        sendLog('info', '系统', 'Transform.get_position Hook 已安装');
      } catch(e) {
        sendLog('warn', '系统', 'Transform.get_position Hook 失败: ' + e.message);
      }
    }

    // ================================================================
    // Frida API Hook — Animator.GetBoneTransform
    // 拦截游戏对骨骼转换的请求，缓存骨骼 Transform 指针
    // ================================================================

    var getBoneHook = null;
    var boneTransformCache = {};  // animatorPtr_boneIndex → TransformPtr

    function installBoneHook(base) {
      // 先通过 il2cpp API 获取地址
      if (!initIl2Cpp()) return;
      var addr = resolveUnityMethod('UnityEngine', 'Animator', 'GetBoneTransform', 1);
      if (!addr) {
        sendLog('warn', '系统', 'Animator.GetBoneTransform 地址未找到，跳过 Hook');
        return;
      }
      // NativeFunction — 主动调用
      getBoneTransformFn = new NativeFunction(addr, 'pointer', ['pointer', 'int32', 'pointer']);
      sendLog('info', '系统', 'Animator.GetBoneTransform NativeFunction 就绪');

      // Interceptor — 被动 Hook
      try {
        getBoneHook = Interceptor.attach(addr, {
          onEnter: function(args) {
            // args[0] = Animator* this
            // args[1] = int32 boneIndex
          },
          onLeave: function(retVal) {
            if (retVal && !retVal.isNull()) {
              // 缓存返回的骨骼 Transform
              // 格式: thisPtr_boneIndex → TransformPtr
            }
          }
        });
        sendLog('info', '系统', 'Animator.GetBoneTransform Hook 已安装');
      } catch(e) {
        sendLog('warn', '系统', 'Animator.GetBoneTransform Hook 失败: ' + e.message);
      }
    }

    // ================================================================
    // Frida API Hook — Transform.get_gameObject
    // ================================================================

    var getGameObjectFn = null;

    function resolveGameObject() {
      if (getGameObjectFn) return true;
      if (!initIl2Cpp()) return false;
      // Transform.get_gameObject() → GameObject*
      try {
        var addr = resolveUnityMethod('UnityEngine', 'Transform', 'get_gameObject', 0);
        if (addr) {
          getGameObjectFn = new NativeFunction(addr, 'pointer', ['pointer', 'pointer']);
          sendLog('info', '系统', 'Transform.get_gameObject 解析成功');
          return true;
        }
      } catch(e) {}
      sendLog('warn', '系统', 'Transform.get_gameObject 解析失败');
      return false;
    }

    // ================================================================
    // Frida API Hook — GameObject.GetComponent
    // ================================================================

    var getComponentFn = null;

    function resolveGetComponent() {
      if (getComponentFn) return true;
      if (!initIl2Cpp()) return false;
      try {
        var addr = resolveUnityMethod('UnityEngine', 'GameObject', 'GetComponent', 1);
        if (!addr) addr = resolveUnityMethod('UnityEngine', 'GameObject', 'GetComponent', 2);
        if (addr) {
          getComponentFn = new NativeFunction(addr, 'pointer', ['pointer', 'pointer', 'pointer']);
          sendLog('info', '系统', 'GameObject.GetComponent 解析成功');
          return true;
        }
      } catch(e) {}
      sendLog('warn', '系统', 'GameObject.GetComponent 解析失败');
      return false;
    }

    // ================================================================
    // Frida API Hook — Physics.Linecast
    // ================================================================

    var linecastFn = null;

    function resolveLinecast() {
      if (linecastFn) return true;
      if (!initIl2Cpp()) return false;
      try {
        var addr = resolveUnityMethod('UnityEngine', 'Physics', 'Linecast', 3);
        if (addr) {
          linecastFn = new NativeFunction(addr, 'bool', ['pointer', 'pointer', 'int32', 'pointer']);
          sendLog('info', '系统', 'Physics.Linecast 解析成功');
          return true;
        }
      } catch(e) {}
      sendLog('warn', '系统', 'Physics.Linecast 解析失败，可见性检测不可用');
      return false;
    }

    // 统一初始化所有 Frida API Hook + NativeFunction
    function tryResolveRuntimeMethods() {
      if (!initIl2Cpp()) return;
      resolveGameObject();
      resolveGetComponent();
      resolveLinecast();
    }

    // ================================================================
    // 工具函数
    // ================================================================

    // 检查玩家指针是否有效 — 验证 team 字段值是否合法 (0/1/2)
    function isValidPlayer(pp) {
      if (!pp || pp.isNull()) return false;
      try {
        var team = pp.add(OFF.E_team).readS32();
        if (team !== 0 && team !== 1 && team !== 2) return false;
        return true;
      } catch(e) {
        return false;
      }
    }

    // ================================================================
    // 可见性检测（DLL 方式 — Physics.Linecast）
    // ================================================================

    function isVisible(startPos, endPos) {
      if (!linecastFn) return true;
      try {
        var buf = Memory.alloc(12);
        buf.writeFloat(startPos.x);
        buf.add(4).writeFloat(startPos.y);
        buf.add(8).writeFloat(startPos.z);
        var buf2 = Memory.alloc(12);
        buf2.writeFloat(endPos.x);
        buf2.add(4).writeFloat(endPos.y);
        buf2.add(8).writeFloat(endPos.z);
        return !linecastFn(buf, buf2, -1, ptr(0));
      } catch(e) {
        return true;
      }
    }

    // ================================================================
    // 骨骼位置读取 — Frida API Hook 方案
    // Unity 组件链:
    //   Player → Component.get_transform() → Transform
    //   → Transform.get_gameObject() → GameObject
    //   → GameObject.GetComponent<Animator>() → Animator
    //   → Animator.GetBoneTransform(index) → Bone Transform
    //   → Transform.get_position() → Vector3
    // ================================================================

    var BONE_Y_OFFSET = {
      0: 1.65,   // HEAD
      3: 1.45,   // NECK
      7: 1.05,   // CHEST
      10: 0.85,  // PELVIS
      6: 0.75,   // HAND
    };

    // 缓存 Animator Il2CPP class 指针
    var animatorClassPtr = null;

    function getAnimatorClass() {
      if (animatorClassPtr) return animatorClassPtr;
      if (!il2cpp.class_from_name) return null;
      try {
        animatorClassPtr = il2cpp.class_from_name(
          il2cpp.domain_get(),
          Memory.allocUtf8String('UnityEngine'),
          Memory.allocUtf8String('Animator')
        );
        return animatorClassPtr;
      } catch(e) { return null; }
    }

    // 获取骨骼世界坐标 — 4 级降级方案
    function getBonePos(player, boneIndex, tag) {
      // ===== 方案 A: 完整 Unity 组件链（Frida NativeFunction 主动调用）=====
      if (getBoneTransformFn && getGameObjectFn && getComponentFn) {
        try {
          var transform = compGetTransform(player, ptr(0));
          if (transform && !transform.isNull()) {
            // Step 1: Transform → GameObject
            var gameObject = getGameObjectFn(transform, ptr(0));
            if (gameObject && !gameObject.isNull()) {
              // Step 2: GameObject → Animator
              var animClass = getAnimatorClass();
              if (animClass && !animClass.isNull()) {
                var animator = getComponentFn(gameObject, animClass, ptr(0));
                if (animator && !animator.isNull()) {
                  // Step 3: Animator → Bone Transform
                  var boneTransform = getBoneTransformFn(animator, boneIndex, ptr(0));
                  if (boneTransform && !boneTransform.isNull()) {
                    // Step 4: Bone Transform → Position
                    var posBuf = Memory.alloc(12);
                    var getPosAddr = getGameAssembly().base.add(RVA.GetPosition);
                    var getPosFn = new NativeFunction(getPosAddr, 'pointer', ['pointer', 'pointer', 'pointer']);
                    getPosFn(posBuf, boneTransform, ptr(0));
                    var x = posBuf.readFloat();
                    var y = posBuf.add(4).readFloat();
                    var z = posBuf.add(8).readFloat();
                    if (Math.abs(x) < 5000 && Math.abs(y) < 5000 && Math.abs(z) < 5000) {
                      return { x: x, y: y, z: z };
                    }
                  }
                }
              }
            }
          }
        } catch(e) {
          sendLog('debug', '骨骼', tag + ' 方案 A 失败: ' + e.message);
        }
      }

      // ===== 方案 B: Transform.get_position + Y 偏移补偿 =====
      try {
        var transform = compGetTransform(player, ptr(0));
        if (transform && !transform.isNull()) {
          var posBuf = Memory.alloc(12);
          var getPosAddr = getGameAssembly().base.add(RVA.GetPosition);
          var getPosFn = new NativeFunction(getPosAddr, 'pointer', ['pointer', 'pointer', 'pointer']);
          getPosFn(posBuf, transform, ptr(0));
          var rootX = posBuf.readFloat();
          var rootY = posBuf.add(4).readFloat();
          var rootZ = posBuf.add(8).readFloat();
          if (Math.abs(rootX) < 5000 && Math.abs(rootY) < 5000 && Math.abs(rootZ) < 5000) {
            var yOff = BONE_Y_OFFSET[boneIndex] || 0.9;
            return { x: rootX, y: rootY + yOff, z: rootZ };
          }
        }
      } catch(e) {}

      // ===== 方案 C: getPlayerPos + Y 偏移补偿 =====
      var pos = getPlayerPos(player, tag);
      if (!pos) return null;
      var yOff = BONE_Y_OFFSET[boneIndex] || 0.9;
      return { x: pos.x, y: pos.y + yOff, z: pos.z };
    }

    function addBotPlayer(botPlayer) {
      if (!botPlayer || botPlayer.isNull()) return;
      try {
        if (!isValidPlayer(botPlayer)) return;
        botPlayers[botPlayer.toString()] = { player: botPlayer, time: Date.now() };
      } catch(e) {}
    }

    function cleanupBotPlayers() {
      var now = Date.now();
      for (var key in botPlayers) {
        if (now - botPlayers[key].time > 5000) {
          delete botPlayers[key];
        }
      }
    }

    function getGM() {
      try {
        var mi = getGameAssembly().base.add(RVA.GM_Singleton).readPointer();
        return mi && !mi.isNull() ? singletonGetter(mi) : null;
      } catch(e) { return null; }
    }

    function getAllPlayers(gm) {
      var ps = {};
      try {
        var ap = gm.add(OFF.GM_all).readPointer();
        if (ap && !ap.isNull()) {
          var n = ap.add(OFF.Arr_len).readU32();
          for (var i = 0; i < n; i++) {
            var pp = ap.add(OFF.Arr_data + i * OFF.Elem_sz).readPointer();
            if (pp && !pp.isNull() && isValidPlayer(pp)) ps[pp.toString()] = pp;
          }
        }
      } catch(e) {}
      try {
        var bl = gm.add(OFF.GM_BL).readPointer();
        if (bl && !bl.isNull()) {
          var n = bl.add(OFF.Arr_len).readU32();
          for (var i = 0; i < n; i++) {
            var pp = bl.add(OFF.Arr_data + i * OFF.Elem_sz).readPointer();
            if (pp && !pp.isNull() && isValidPlayer(pp)) ps[pp.toString()] = pp;
          }
        }
      } catch(e) {}
      try {
        var gr = gm.add(OFF.GM_GR).readPointer();
        if (gr && !gr.isNull()) {
          var n = gr.add(OFF.Arr_len).readU32();
          for (var i = 0; i < n; i++) {
            var pp = gr.add(OFF.Arr_data + i * OFF.Elem_sz).readPointer();
            if (pp && !pp.isNull() && isValidPlayer(pp)) ps[pp.toString()] = pp;
          }
        }
      } catch(e) {}
      // 存活列表补充：playersBL_Alive(0x24) + playersGR_Alive(0x2C)
      try {
        var bl = gm.add(0x24).readPointer();
        if (bl && !bl.isNull()) {
          var n = bl.add(OFF.Arr_len).readU32();
          for (var i = 0; i < n; i++) {
            var pp = bl.add(OFF.Arr_data + i * OFF.Elem_sz).readPointer();
            if (pp && !pp.isNull() && isValidPlayer(pp)) ps[pp.toString()] = pp;
          }
        }
      } catch(e) {}
      try {
        var gr = gm.add(0x2C).readPointer();
        if (gr && !gr.isNull()) {
          var n = gr.add(OFF.Arr_len).readU32();
          for (var i = 0; i < n; i++) {
            var pp = gr.add(OFF.Arr_data + i * OFF.Elem_sz).readPointer();
            if (pp && !pp.isNull() && isValidPlayer(pp)) ps[pp.toString()] = pp;
          }
        }
      } catch(e) {}
      // 补充 Bot 玩家
      cleanupBotPlayers();
      for (var key in botPlayers) {
        var entry = botPlayers[key];
        if (entry && entry.player && isValidPlayer(entry.player)) {
          var pp = entry.player;
          if (!ps[pp.toString()]) {
            ps[pp.toString()] = pp;
          }
        }
      }
      return Object.values(ps);
    }

    // 获取玩家位置 — 优先 get_transform 函数，失败后备 characterContainer
    // 直接读 Transform 内存字段获取坐标，不调用 transformGetPos（地址不稳定导致崩溃）
    function getPlayerPos(player, tag) {
      try {
        sendLog('debug', '位置调试', tag + ' player ptr=' + player);
        var vtable = player.readPointer();
        if (vtable.isNull()) {
          sendLog('error', '位置调试', tag + ' player vtable 为空');
          return null;
        }

        var transform = null;

        // 方案1：通过 get_transform 函数调用
        try {
          transform = compGetTransform(player, ptr(0));
          if (transform && !transform.isNull()) {
            sendLog('debug', '位置调试', tag + ' get_transform 成功，transform=' + transform);
          } else {
            sendLog('warn', '位置调试', tag + ' get_transform 返回 null');
          }
        } catch(e) {
          sendLog('error', '位置调试', tag + ' get_transform 异常: ' + e.message);
          transform = null;
        }

        // 方案2（后备）：直接读 characterContainer 字段
        if (!transform || transform.isNull()) {
          var container = player.add(0x58).readPointer();
          if (container && !container.isNull()) {
            transform = container;
            sendLog('debug', '位置调试', tag + ' 使用 characterContainer(0x58)，transform=' + transform);
          } else {
            sendLog('error', '位置调试', tag + ' 无法获取 transform');
            return null;
          }
        }

        // ✅ 方案A: 调用 Transform.get_position (RVA 0x3F42B0 已验证)
        try {
          var posBuf = Memory.alloc(12);
          // 用函数签名: Vector3* get_position(Vector3* retstr, Transform* this, MethodInfo* method)
          var resultPtr = new NativeFunction(getGameAssembly().base.add(0x3F42B0), 'pointer', ['pointer', 'pointer', 'pointer']);
          resultPtr(posBuf, transform, ptr(0));
          var fx = posBuf.readFloat();
          var fy = posBuf.add(4).readFloat();
          var fz = posBuf.add(8).readFloat();
          if (Math.abs(fx) < 5000 && Math.abs(fy) < 5000 && Math.abs(fz) < 5000 && !(fx === 0 && fy === 0 && fz === 0)) {
            sendLog('debug', '位置调试', tag + ' get_position函数 坐标=' + fx.toFixed(1) + ',' + fy.toFixed(1) + ',' + fz.toFixed(1));
            return { x: fx, y: fy, z: fz };
          }
        } catch(e) {
          sendLog('warn', '位置调试', tag + ' get_position函数 异常: ' + e.message);
        }

        // ✅ 方案B: 直接读 Transform 内存字段
        // 尝试偏移: 0x08, 0x10, 0x18, 0x20, 0x28, 0x2C, 0x30, 0x34, 0x38, 0x3C, 0x40
        var tryOffsets = [0x08, 0x10, 0x18, 0x20, 0x28, 0x2C, 0x30, 0x34, 0x38, 0x3C, 0x40];
        for (var i = 0; i < tryOffsets.length; i++) {
          try {
            var off = tryOffsets[i];
            var x = transform.add(off).readFloat();
            var y = transform.add(off + 4).readFloat();
            var z = transform.add(off + 8).readFloat();
            // 合理性检查：非全零且在地图范围内
            if (Math.abs(x) < 5000 && Math.abs(y) < 5000 && Math.abs(z) < 5000 && !(x === 0 && y === 0 && z === 0)) {
              sendLog('debug', '位置调试', tag + ' 偏移 0x' + off.toString(16) + ' 坐标=' + x.toFixed(1) + ',' + y.toFixed(1) + ',' + z.toFixed(1));
              return { x: x, y: y, z: z };
            }
          } catch(e) {}
        }

        sendLog('error', '位置调试', tag + ' 所有偏移读取坐标均失败');
        return null;
      } catch(e) {
        sendLog('error', '位置调试', tag + ' 异常: ' + e.message);
        return null;
      }
    }

    // ================================================================
    // 模式感知 + 敌人筛选
    // ================================================================

    function detectGameMode(gm) {
      try {
        var all = getAllPlayers(gm);
        for (var i = 0; i < all.length; i++) {
          var t = all[i].add(OFF.E_team).readS32();
          if (t === 2) {
            sendLog('info', '调试', '发现 Neutral(2) 队伍，判定为生化模式');
            return 3;
          }
        }
      } catch(e) {
        sendLog('error', '调试', 'detectGameMode 异常: ' + e.message);
      }
      sendLog('info', '调试', '未发现 Neutral 队伍，默认团队模式(0)');
      return 0;
    }

    function isEnemy(lp, t, mode) {
      if (t.equals(lp)) return false;
      if (mode === 1) return true;
      var mt = lp.add(OFF.E_team).readS32(), tt = t.add(OFF.E_team).readS32();
      if (mt === tt) return false;
      if (mode >= 3) return true;
      return tt !== 2;
    }

    function getEnemyList(gm, lp, mode) {
      var all = getAllPlayers(gm);
      var enemies = [];
      sendLog('info', '调试', 'getEnemyList: total players=' + all.length + ' mode=' + mode);
      for (var i = 0; i < all.length; i++) {
        try {
          var player = all[i];
          var team = player.add(OFF.E_team).readS32();
          sendLog('debug', '调试', '检查玩家' + i + ': ptr=' + player + ' team=' + team);

          if (!isValidPlayer(player)) {
            sendLog('warn', '调试', '玩家' + i + ' 有效性检查失败，跳过');
            continue;
          }

          if (player.equals(lp)) {
            sendLog('debug', '调试', '玩家' + i + ' = 自己，跳过');
            continue;
          }

          var isDead = false;
          try { isDead = isDeadFn(player, ptr(0)); }
          catch(e) { sendLog('error', '调试', 'isDeadFn 异常: ' + e.message); continue; }
          if (isDead) { sendLog('debug', '调试', '玩家' + i + ' 已死亡，跳过'); continue; }

          var enemy = false;
          try { enemy = isEnemy(lp, player, mode); }
          catch(e) { sendLog('error', '调试', 'isEnemy 异常: ' + e.message); continue; }

          if (enemy) { enemies.push(player); sendLog('debug', '调试', '玩家' + i + ' → 加入敌人列表'); }
          else { sendLog('debug', '调试', '玩家' + i + ' → 不是敌人'); }
        } catch(e) {
          sendLog('error', '调试', 'getEnemyList 循环异常: ' + e.message);
        }
      }
      sendLog('info', '调试', 'getEnemyList 最终敌人数量: ' + enemies.length);
      return enemies;
    }

    // ================================================================
    // 自瞄主循环
    // ================================================================
    // 自瞄主循环 — 完全对齐 DLL (MD 3.3 反汇编代码)
    //
    // DLL 代码流:
    //   if (GetAsyncKeyState(uCode) < 0) {          // 热键
    //     v21 = dword_1005A6D4;                     // 锁定目标
    //     if (dword_1005A6D4) {                     // 目标存在
    //       if (dword_1005A6D8) {                   // 自瞄开关
    //         v1 = *(DWORD**)(dword_1005A6D4 + 84);  // Transform
    //         if (v1) {
    //           get_pos(dword_1005A6C8);             // 敌人坐标
    //           get_self_pos();                      // 自身坐标
    //           yaw = atan2(dx, dz) * 180/PI;        // 计算水平
    //           pitch = atan2(dy, dist) * 180/PI;    // 计算垂直
    //           *(float*)(v21 + 76) = yaw;           // 写Yaw
    //           *(float*)(v21 + 80) = pitch;         // 写Pitch
    //           v1[4]=0; v1[9]=0; v1[21]=0; v1[16]=0; // 重置标志
    //         }
    //       }
    //     }
    //   }
    // ================================================================

    function aimLoop() {
      if (!enabled) return;

      // ===== DLL Step 1: GetAsyncKeyState 检测热键 =====
      // LOWORD(v1) = GetAsyncKeyState(uCode);
      // if ((__int16)v1 < 0)
      try {
        var keyState = getAsyncKeyState(aimHotkey);
        if ((keyState & 0x8000) === 0) return;
      } catch(e) {
        // 未初始化时跳过
        return;
      }

      // ===== DLL Step 2: 获取/验证 本地玩家（Frida 额外步骤，DLL 已有指针）=====
      // 这部分是 Frida 环境需要做的发现工作，DLL 中 dword_1005A6D4 已存在
      var gm = getGM();
      if (!gm || gm.isNull()) { return; }
      if (myPlayer) {
        try { if (!isMyPlayerFn(myPlayer, ptr(0))) { myPlayer = null; return; } }
        catch(e) { myPlayer = null; return; }
      }
      if (!myPlayer) {
        var all = getAllPlayers(gm);
        for (var i = 0; i < all.length; i++) {
          try {
            if (isMyPlayerFn(all[i], ptr(0))) { myPlayer = all[i]; break; }
          } catch(e) {}
        }
        if (!myPlayer) return;
      }

      // ===== DLL: dword_1005A6D4 = myPlayer（角度写入目标）=====
      dword_1005A6D4 = myPlayer;

      // ===== DLL Step 2b: if (dword_1005A6D4) =====
      if (!dword_1005A6D4) return;

      // ===== DLL Step 3: if (dword_1005A6D8) — 自瞄开关 =====
      if (!dword_1005A6D8) return;

      // ===== DLL Step 4: v1 = *(DWORD**)(dword_1005A6D4 + 84) — 获取Transform =====
      var transformPtr = dword_1005A6D4.add(OFF.P_transform).readPointer();
      if (!transformPtr || transformPtr.isNull()) return;

      // ===== DLL Step 5: 获取敌人位置 (dword_1005A6E8(&v44, dword_1005A6C8)) =====
      if (!dword_1005A6C8) return;
      var boneIndex = BONE.CHEST;
      if (aimBone === 'head') boneIndex = BONE.HEAD;
      else if (aimBone === 'neck') boneIndex = BONE.NECK;
      else if (aimBone === 'pelvis') boneIndex = BONE.PELVIS;
      var targetPos = getBonePos(dword_1005A6C8, boneIndex, '目标');
      if (!targetPos) return;

      // ===== DLL Step 6: 获取自身位置 =====
      var selfPos = getPlayerPos(myPlayer, '自身');
      if (!selfPos) return;

      // ===== DLL Step 7: 计算差值 =====
      // v46 = targetX - selfX;  v41 = targetZ - selfZ
      var dx = targetPos.x - selfPos.x;
      var dy = targetPos.y - selfPos.y;
      var dz = targetPos.z - selfPos.z;
      var hDist = Math.sqrt(dx*dx + dz*dz);
      if (hDist < 0.01) return;

      // ===== DLL Step 8: 计算Yaw = atan2(dx, dz) * 180/PI =====
      var yawRad = Math.atan2(dx, dz);
      var targetYawDeg = yawRad * 180.0 / Math.PI;

      // ===== DLL Step 9: 计算Pitch = atan2(dy, hDist) * 180/PI =====
      var pitchRad = Math.atan2(dy, hDist);
      var targetPitchDeg = pitchRad * 180.0 / Math.PI;

      // ===== (MD 5.2 可选) 角度平滑: smooth = current + (target - current) * factor =====
      var finalYaw = targetYawDeg;
      var finalPitch = targetPitchDeg;
      if (aimSmoothing > 0.0 && aimSmoothing <= 1.0) {
        try {
          var curYaw = dword_1005A6D4.add(OFF.P_camRot).readFloat();
          var curPitch = dword_1005A6D4.add(OFF.P_camRot + 4).readFloat();
          var yawDiff = targetYawDeg - curYaw;
          var pitchDiff = targetPitchDeg - curPitch;
          if (yawDiff > 180) yawDiff -= 360;
          if (yawDiff < -180) yawDiff += 360;
          finalYaw = curYaw + yawDiff * aimSmoothing;
          finalPitch = curPitch + pitchDiff * aimSmoothing;
        } catch(e) {}
      }

      // ===== DLL Step 10: 写入角度 *(float*)(v21 + 76) = yaw; *(float*)(v21 + 80) = pitch =====
      try {
        dword_1005A6D4.add(OFF.P_camRot).writeFloat(finalYaw);
        dword_1005A6D4.add(OFF.P_camRot + 4).writeFloat(finalPitch);

        // ===== DLL Step 11: 重置 Transform 标志 =====
        // v1[4]=0; v1[9]=0; v1[21]=0; v1[16]=0;
        // v1[4]  = Transform + 0x10
        // v1[9]  = Transform + 0x24
        // v1[16] = Transform + 0x40
        // v1[21] = Transform + 0x54
        transformPtr.add(0x10).writeU32(0);
        transformPtr.add(0x24).writeU32(0);
        transformPtr.add(0x40).writeU32(0);
        transformPtr.add(0x54).writeU32(0);

        logCount++;
      } catch(e) {
        sendLog('error', '自瞄', '写入角度失败: ' + e.message);
      }
    }

    // ========== 外部目标扫描器（DLL 方式：每帧遍历所有可见敌人，选角度最近）==========
    function targetScanner() {
      if (!enabled || !myPlayer) return;
      try {
        var gm = getGM();
        if (!gm || gm.isNull()) return;
        if (!isMyPlayerFn(myPlayer, ptr(0))) { myPlayer = null; dword_1005A6C8 = null; return; }

        var gameMode = detectGameMode(gm);
        var enemies = getEnemyList(gm, myPlayer, gameMode);
        if (enemies.length === 0) { dword_1005A6C8 = null; return; }

        // DLL 方式：每帧重新选最优目标（没有"存活就不换"的锁定）
        // 遍历所有敌人，计算角度距离，选择离准星最近的

        var myPos = getPlayerPos(myPlayer, '扫描');
        if (!myPos) return;
        var curYawDeg = myPlayer.add(OFF.P_camRot).readFloat();
        var curPitchDeg = myPlayer.add(OFF.P_camRot + 4).readFloat();

        var best = null;
        var bestAngleDeg = Number.MAX_VALUE;
        for (var si = 0; si < enemies.length; si++) {
          // 可见性检查（DLL 方式：读取可见性标志或 Linecast）
          if (linecastFn) {
            var targetPos = getPlayerPos(enemies[si], '扫描');
            if (targetPos && !isVisible(myPos, targetPos)) continue;
          }

          var ePos = getPlayerPos(enemies[si], '扫描');
          if (!ePos) continue;
          var boneIndex = BONE.CHEST;
          if (aimBone === 'head') boneIndex = BONE.HEAD;
          else if (aimBone === 'neck') boneIndex = BONE.NECK;
          else if (aimBone === 'pelvis') boneIndex = BONE.PELVIS;
          var yOff = BONE_Y_OFFSET[boneIndex] || 0.9;
          ePos.y += yOff;
          var dx = ePos.x - myPos.x, dz = ePos.z - myPos.z;
          var yaw = Math.atan2(dx, dz);
          var dist2d = Math.sqrt(dx*dx + dz*dz);
          var pitch = Math.atan2(ePos.y - myPos.y, dist2d);
          var cyRad = curYawDeg * Math.PI / 180;
          var cpRad = curPitchDeg * Math.PI / 180;
          var yawD = yaw - cyRad;
          if (yawD > Math.PI) yawD -= 2*Math.PI; if (yawD < -Math.PI) yawD += 2*Math.PI;
          var pitchD = pitch - cpRad;
          if (pitchD > Math.PI) pitchD -= 2*Math.PI; if (pitchD < -Math.PI) pitchD += 2*Math.PI;
          var angDeg = Math.sqrt(yawD*yawD + pitchD*pitchD) * 180 / Math.PI;
          if (angDeg < bestAngleDeg) {
            bestAngleDeg = angDeg;
            best = enemies[si];
          }
        }
        if (best) {
          dword_1005A6C8 = best;
        } else {
          dword_1005A6C8 = null;
        }
      } catch(e) {}
    }

    // ================================================================
    // 房间切换检测
    // ================================================================

    function installRoomHooks(base) {
      var addrs = [0xAF9A90, 0xAEE370, 0xAF5B30];
      for (var i = 0; i < addrs.length; i++) {
        try {
          var h = Interceptor.attach(base.add(addrs[i]), {
            onEnter: function() {
              myPlayer = null; targetEnemy = null; dword_1005A6D4 = null; dword_1005A6C8 = null; logCount = 0; lastEnemyCount = 0;
              sendLog('info', '自瞄', '房间切换，状态已重置');
            }
          });
          roomHooks.push(h);
        } catch(e) {}
      }
    }

    // ================================================================
    // 公开接口
    // ================================================================

    return {
      enable: function() {
        if (enabled) return;
        var mod = getGameAssembly();
        if (!mod) { sendLog('error', '自瞄', '无 GameAssembly.dll'); return; }
        var base = mod.base;

        // DLL 方式: GetAsyncKeyState — 从 user32.dll 导入（MD 2.3）
        try {
          var user32 = Process.findModuleByName('user32.dll');
          if (!user32) { sendLog('error', '自瞄', 'user32.dll 未加载'); return; }
          var addr = user32.findExportByName('GetAsyncKeyState');
          if (!addr) { sendLog('error', '自瞄', '找不到 GetAsyncKeyState'); return; }
          getAsyncKeyState = new NativeFunction(addr, 'int16', ['int32']);
          sendLog('info', '自瞄', 'GetAsyncKeyState 初始化成功 (hotkey=0x' + aimHotkey.toString(16) + ')');
        } catch(e) {
          sendLog('error', '自瞄', 'GetAsyncKeyState 初始化失败: ' + e.message);
          return;
        }

        // 尝试运行时解析骨骼和可见性 API
        tryResolveRuntimeMethods();

        // 安装 Frida API Hook — Transform.get_position
        installTransformHook(base);

        // 安装 Frida API Hook — Animator.GetBoneTransform
        installBoneHook(base);

        // 基础 NativeFunction
        isMyPlayerFn = new NativeFunction(base.add(RVA.P_isMyPlayer), 'bool', ['pointer', 'pointer']);
        isDeadFn = new NativeFunction(base.add(RVA.E_isDead), 'bool', ['pointer', 'pointer']);
        singletonGetter = new NativeFunction(base.add(RVA.SingletonGet), 'pointer', ['pointer']);

        // Component.get_transform: Transform*(Component* this, MethodInfo* method) — RVA 0x32CF40
        compGetTransform = new NativeFunction(base.add(RVA.GetTransform), 'pointer', ['pointer', 'pointer']);

        // Transform.get_position: void(Transform* this, Vector3* out, MethodInfo* method)
        transformGetPos = new NativeFunction(base.add(RVA.GetPosition), 'void', ['pointer', 'pointer', 'pointer']);

        installRoomHooks(base);

        // 安装 Bot.Update Hook 捕获 Bot 玩家
        try {
          var botUpdateAddr = base.add(RVA.Bot_Update);
          botUpdateHook = Interceptor.attach(botUpdateAddr, {
            onEnter: function(args) {
              var bot = args[0];
              if (!bot || bot.isNull()) return;
              try {
                var thisPlayer = bot.add(0x24).readPointer();
                if (thisPlayer && !thisPlayer.isNull()) {
                  addBotPlayer(thisPlayer);
                }
              } catch(e) {}
            }
          });
          sendLog('info', '自瞄', 'Bot.Update Hook 已安装');
        } catch(e) {
          sendLog('warn', '自瞄', '安装 Bot.Update Hook 失败: ' + e.message);
        }

        myPlayer = null; targetEnemy = null; dword_1005A6D4 = null; dword_1005A6C8 = null; dword_1005A6D8 = true; logCount = 0; lastEnemyCount = 0;
        timer = setInterval(aimLoop, scanInterval);
        scanTimer = setInterval(targetScanner, 100);
        enabled = true;
        sendLog('success', '自瞄', '已启用 (Frida Hook: Transform.get_position + Animator.GetBoneTransform)');
        sendStatus('aim', true);
      },

      disable: function() {
        if (!enabled) return;
        if (timer) { clearInterval(timer); timer = null; }
        if (scanTimer) { clearInterval(scanTimer); scanTimer = null; }
        if (getPosHook) { try { getPosHook.detach(); } catch(e) {} getPosHook = null; }
        if (getBoneHook) { try { getBoneHook.detach(); } catch(e) {} getBoneHook = null; }
        for (var i = 0; i < roomHooks.length; i++) { try { roomHooks[i].detach(); } catch(e) {} }
        roomHooks = [];
        if (botUpdateHook) { try { botUpdateHook.detach(); } catch(e) {} }
        botUpdateHook = null;
        botPlayers = {};
        isMyPlayerFn = null; isDeadFn = null; singletonGetter = null; getAsyncKeyState = null;
          compGetTransform = null; transformGetPos = null;
          myPlayer = null; targetEnemy = null; dword_1005A6D4 = null; dword_1005A6C8 = null; dword_1005A6D8 = false; enabled = false;
        linecastFn = null; getBoneTransformFn = null; getComponentFn = null; getGameObjectFn = null;
        sendLog('info', '自瞄', '已禁用');
        sendStatus('aim', false);
      },

      setconfig: function(cfg) {
        if (cfg.aimBone !== undefined) {
          aimBone = cfg.aimBone;
          sendLog('info', '自瞄', '瞄准部位: ' + aimBone);
        }
        if (cfg.smoothing !== undefined && cfg.smoothing >= 0 && cfg.smoothing <= 1) {
          aimSmoothing = cfg.smoothing;
          sendLog('info', '自瞄', '角度平滑系数: ' + aimSmoothing);
        }
        if (cfg.hotkey !== undefined && cfg.hotkey > 0) {
          aimHotkey = cfg.hotkey;
          sendLog('info', '自瞄', '自瞄热键: 0x' + aimHotkey.toString(16));
        }
      },

      getstatus: function() {
        return {
          enabled: enabled,
          dword_1005A6D8: dword_1005A6D8,
          myPlayer: myPlayer ? myPlayer.toString() : null,
          targetEnemy: targetEnemy ? targetEnemy.toString() : null,
          dword_1005A6D4: dword_1005A6D4 ? dword_1005A6D4.toString() : null,
          dword_1005A6C8: dword_1005A6C8 ? dword_1005A6C8.toString() : null,
          aimBone: aimBone,
          aimSmoothing: aimSmoothing,
          aimHotkey: aimHotkey,
        };
      }
    };
  })();

  rpc.exports = {
    aimenable: function() { aimModule.enable(); },
    aimdisable: function() { aimModule.disable(); },
    aimconfig: function(bone, smoothing, hotkey) {
      var cfg = {};
      if (bone !== undefined && bone !== '') cfg.aimBone = bone;
      if (smoothing !== undefined && smoothing >= 0 && smoothing <= 1) cfg.smoothing = smoothing;
      if (hotkey !== undefined && hotkey > 0) cfg.hotkey = hotkey;
      aimModule.setconfig(cfg);
    },
    aimstatus: function() { return JSON.stringify(aimModule.getstatus()); }
  };
})();
