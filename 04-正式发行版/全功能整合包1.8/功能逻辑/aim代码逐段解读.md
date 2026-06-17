# aim.js 自瞄代码逐段解读

> 从穿越火线玩家的角度，用游戏语言解释每一部分代码的作用。

---

## 1. 模块外壳和状态变量（第1-6行）

```javascript
modules.aim = (function() {
  var enabled = false;      // 自瞄开关（false=关，true=开）
  var myPlayer = null;      // "我"这个角色在游戏内存里的地址
  var targetEnemy = null;   // 当前锁定的敌人（旧版遗留，实际没用到）
  var timer = null;         // 旧版定时器（已废弃）
  var roomHooks = [];       // 监听游戏事件的"耳朵"，比如新一局开始时重置状态
  var frameCount = 0;       // 执行次数计数器
```

**作用**：把整个自瞄功能包成一个独立模块，防止和其他功能互相干扰。

| 变量 | 游戏含义 |
|---|---|
| `enabled` | 自瞄开关，开/关 |
| `myPlayer` | "我"这个角色在游戏内存里的位置 |
| `targetEnemy` | 当前锁定的敌人（旧版遗留，实际没用） |
| `timer` | 旧版定时器（已废弃） |
| `roomHooks` | 监听游戏事件的"耳朵"，比如新一局开始时重置状态 |
| `frameCount` | 执行次数计数器 |

---

## 2. 自瞄参数配置（第8-18行）

```javascript
var CONFIG = {
  aimKey:          0,        // 自瞄触发键（0=鼠标左键，1=右键，2=中键）
                            // 0=左键这个映射是Unity引擎的硬编码规范，不是游戏定义的
  aimBone:         7,        // 瞄准敌人身体哪个部位（7%5=2，对应胸部）
    
                            // 0=头部(+1.65m), 1=脖子(+1.45m), 2=胸部(+1.05m), 3=腰部(+0.85m), 4=腿部(+0.75m)
    
                            // 这些Y偏移不是游戏定义的，是开发者根据playerHeight=2.6m估算的（见下方依据）
    
                            // aimBone: 7 本身就是开发者自己写的，完全可以直接写 aimBone: 2 ，效果一模一样
    
  smoothness:      1.0,      // 自瞄平滑度（1.0=瞬间锁死，0.5=慢慢转过去更像真人，越小越"自然"）
  maxAimDistance:  200.0,    // 自瞄最大距离（200米，超过这个距离的敌人不瞄）
  maxAngleFOV:     30.0,     // 自瞄视野范围（30度=准星30度内的敌人才锁，不会转头180度锁背后）
  visibilityCheck: false,    // 是否检测隔墙（false=穿墙也能锁，true=只锁你能直接看到的敌人）
  autoAim:         false,    // 自动瞄准（false=按住左键才自瞄，true=全程自动锁不用按键）
  debugLog:        true,     // 调试日志（玩家看不到，开发者调试用）
};
```

| 参数 | 游戏含义 |
|---|---|
| `aimKey: 0` | 按住鼠标左键才自瞄（0=左键，1=右键，2=中键） |
| `aimBone: 7` | 瞄准敌人身体哪个部位。7%5=2，对应胸部（0=头、1=脖子、2=胸、3=腰、4=腿）。这些Y偏移是开发者估算的，不是游戏定义的 |
| `smoothness: 1.0` | 准星移动的平滑度。1.0=瞬间锁死，0.5=慢慢转过去，更像真人 |
| `maxAimDistance: 200` | 最远锁定距离，超过200米的敌人不瞄 |
| `maxAngleFOV: 30` | 视野范围限制，只有准星30度以内的敌人才会锁定，不会转头180度去锁背后的人 |
| `visibilityCheck: false` | 是否检查隔墙。关=隔墙也能锁，开=只锁你能看见的敌人 |
| `autoAim: false` | 关=要按住左键才自瞄，开=不用按键自动锁定 |
| `debugLog: true` | 是否输出调试日志 |

---

## 3. 原生函数指针声明（第20-30行）

```javascript
var singletonGetter = null;   // 游戏总管理器（GameManager）
var compGetTransform = null;  // 角色的位置标记，拿到它才能知道角色站在地图哪个位置
var transformGetPos = null;   // 角色的精确坐标（x/y/z），读取角色在地图上的前后、左右、高低
var isMyPlayerFn = null;      // 判断"这个角色是不是我正在操控的"，从所有人里找出自己
var isDeadFn = null;          // 判断"这个角色是不是已经死了"，跳过地上的尸体不瞄
var getTeamFn = null;         // 查看队伍（0=潜伏者，1=保卫者，2=中立），区分敌我
var addCamRotFn = null;       // 转动角色视角的函数（声明了但实际没用到，改用直接写内存）
var getMouseBtnFn = null;     // 检测鼠标按键有没有按住，判断你有没有按左键
var linecastFn = null;        // 从你到敌人画条线检测有没有墙挡着，判断能不能直接看到敌人
```

**作用**：声明9个"接线头"，后面会把它们连到游戏内部的真实函数上。

| 变量 | 连到游戏的什么 |
|---|---|
| `singletonGetter` | 游戏总管理器（GameManager） |
| `compGetTransform` | 角色的位置标记 |
| `transformGetPos` | 角色的精确坐标 |
| `isMyPlayerFn` | 判断"是不是我" |
| `isDeadFn` | 判断"是不是死了" |
| `getTeamFn` | 查看队伍 |
| `addCamRotFn` | 转动视角（声明了但没用） |
| `getMouseBtnFn` | 检测鼠标按键 |
| `linecastFn` | 检测有没有墙挡着 |

---

## 4. 双定时器变量和缓存（第32-38行）

```javascript
var aimTimer = null;       // 瞄准定时器，每16ms执行一次（控制准星移动，约62.5fps）
var scanTimer = null;      // 扫描定时器，每30ms执行一次（找最近的敌人，约33fps）
var debugTimer = null;     // 调试定时器（未使用）
var cachedTarget = null;   // 缓存的当前目标，扫描器找到敌人后存这里，交给瞄准器处理
var scanYawDeg = 0;        // 扫描时你面朝的水平方向（左右看的角度）
var scanPitchDeg = 0;      // 扫描时你面朝的垂直方向（抬头看天/低头看地的角度）
```

**作用**：自瞄用两个定时器分工合作。

| 变量 | 游戏含义 |
|---|---|
| `aimTimer` | 瞄准定时器，每16ms执行一次（控制准星移动） |
| `scanTimer` | 扫描定时器，每30ms执行一次（找最近的敌人） |
| `debugTimer` | 调试定时器（未使用） |
| `cachedTarget` | 缓存的当前目标，扫描器找到后传给瞄准器 |
| `scanYawDeg` | 扫描时你面朝的水平方向 |
| `scanPitchDeg` | 扫描时你面朝的垂直方向（抬头/低头） |

---

## 5. RVA地址表（第40-51行）

```javascript
var RVA_AIM = {
  SingletonGet:                    0x4A8170,  // 获取游戏总管理器的函数入口（IL2CPP泛型共享，所有Singleton<T>共用一个函数体）
  GM_Singleton_MethodInfo:         0xE1CE64,  // GameManager的类型信息，告诉函数你要的是GameManager而不是别的单例
  Component_get_transform:         0x32CF40,  // 获取角色位置标记的函数入口
  Transform_get_position:          0x3F42B0,  // 读取角色精确坐标的函数入口
    
    //结合IDA伪代码+游戏逻辑，用大白话拆分：
1. **compGetTransform（0x32CF40）**
输入：玩家/角色对象
输出：角色身上**位置组件**的内存地址
作用：先找到角色身上负责记录位置的“容器”，只拿地址，**不读具体坐标**。

2. **transformGetPos（0x3F42B0）**
输入：上面拿到的位置组件地址
输出：把组件里的 **X/Y/Z 三维坐标** 读出来存到缓存
作用：打开这个“容器”，取出实际位置数据。

---
### 一句话流程（游戏里）
想知道敌人在哪 → 先用`compGetTransform`找到他的位置容器 → 再用`transformGetPos`读出坐标。
**顺序不能反，少一步都拿不到位置**。

  Player_get_isMyPlayer:           0xB55FD0,  // 判断"这个角色是不是我"的函数入口
  Entity_get_isDead:               0xB400E0,  // 判断"这个角色是不是死了"的函数入口
  Entity_get_team:                 0x1E0070,  // 查看角色队伍的函数入口（0=潜伏者，1=保卫者，2=中立）
  Player_AddCameraRotation:        0xB4F790,  // 转动角色视角的函数入口（声明了但没调用，改用直接写内存）
  Input_GetMouseButton:            0xACFB20,  // 检测鼠标按键状态的函数入口
  Physics_Linecast:                0xAB9B80,  // 从A到B画线检测有没有墙的函数入口
};
```

**作用**：这是游戏内部函数的"门牌号"。每个地址对应GameAssembly.dll里的一个功能入口，修改器通过这些地址找到并调用游戏内部函数。

## 6. 偏移量表（第53-66行）

```javascript
var OFF_AIM = {
  GM_allPlayers:      0x1C,  // 游戏管理器里的"所有玩家名单"，就像记分板上显示的所有人
  GM_playersBL:       0x20,  // 蓝队（潜伏者）玩家名单
  GM_playersGR:       0x28,  // 红队（保卫者）玩家名单
  E_team:             0x20,  // 角色身上的队伍标记（0=潜伏者，1=保卫者，2=中立），IDA验证Entity$$get_team读取[this+0x20]
  P_cameraRotation:   0x4C,  // 你角色的视线方向，存了两个float：左右看的角度+抬头低头的角度
  P_recoil:           0x54,  // 后坐力数据，开枪时枪口往上跳、往旁边飘的量，清零后枪口纹丝不动
  P_characterContainer: 0x58, // 人物模型容器，你在游戏里看到的那个3D人物，备用读坐标用
  Arr_len:            0x0C,  // 数组里有多少个人（IL2CPP标准布局，Array.length）
  Arr_data:           0x10,  // 数组里第1个人的位置（IL2CPP标准布局，Array数据起始）
  List_items:         0x08,  // 列表内部用的数组（IL2CPP标准布局，List._items）
  List_size:          0x0C,  // 列表里当前有几个人（IL2CPP标准布局，List._size）
  ptrSize:            4,     // 32位游戏，每个内存地址占4字节（64位游戏是8字节）
};
```

**作用**：游戏对象在内存里的"字段偏移"，就像表格里每一列的位置。知道偏移就能直接从内存中读取对应数据。

---

## 7. getGM() — 获取游戏总管理器（第68-78行）

```javascript
function getGM() {
  try {
    var base = getGameAssembly().base;                                    // 拿到游戏核心模块的起始地址
    var mi = base.add(RVA_AIM.GM_Singleton_MethodInfo).readPointer();    // 从内存中读取GameManager的类型信息
    if (mi.isNull()) {                                                    // 类型信息为空？
      return singletonGetter(ptr(0));                                     // 传null试试（兜底）
    }
    var gm = singletonGetter(mi);                                         // 把类型信息传给单例获取函数，拿到GameManager
    if (gm.isNull()) return null;                                         // 拿不到就返回空
    return gm;                                                            // 返回游戏总管理器
  } catch(e) { return null; }                                            // 出错就返回空
}
```

**作用**：拿到游戏的"总管理器"。就像进入房间后先找到裁判，裁判手里有所有玩家名单。自瞄的一切操作都从拿到总管理器开始。

流程：从内存中读取类型信息 → 传给单例获取函数 → 拿到GameManager对象。

---

## 8. initNativeFunctions() — 连接游戏内部函数（第80-97行）

```javascript
function initNativeFunctions() {
  var mod = getGameAssembly();                                           // 获取游戏核心模块
  if (!mod) return false;                                                // 找不到就失败
  var base = mod.base;                                                   // 模块起始地址

  // 核心函数——失败则整个自瞄无法启动
  try { singletonGetter = new NativeFunction(base.add(RVA_AIM.SingletonGet), 'pointer', ['pointer']); } catch(e) { return false; }              // 连接：获取游戏总管理器
  try { compGetTransform = new NativeFunction(base.add(RVA_AIM.Component_get_transform), 'pointer', ['pointer', 'pointer']); } catch(e) { return false; }  // 连接：获取角色位置标记
  try { transformGetPos = new NativeFunction(base.add(RVA_AIM.Transform_get_position), 'void', ['pointer', 'pointer', 'pointer']); } catch(e) { return false; } // 连接：读取角色精确坐标
  try { isMyPlayerFn = new NativeFunction(base.add(RVA_AIM.Player_get_isMyPlayer), 'bool', ['pointer', 'pointer']); } catch(e) { return false; }           // 连接：判断"是不是我"
  try { isDeadFn = new NativeFunction(base.add(RVA_AIM.Entity_get_isDead), 'bool', ['pointer', 'pointer']); } catch(e) { return false; }                   // 连接：判断"是不是死了"
  try { addCamRotFn = new NativeFunction(base.add(RVA_AIM.Player_AddCameraRotation), 'void', ['pointer', 'float', 'float', 'pointer']); } catch(e) { return false; } // 连接：转动视角（声明了但没调用）

  // 非核心函数——失败只是缺少该功能，自瞄仍可运行
  try { getTeamFn = new NativeFunction(base.add(RVA_AIM.Entity_get_team), 'int32', ['pointer', 'pointer']); } catch(e) { getTeamFn = null; }               // 连接：查看队伍（失败=无法区分敌我，改用直接读内存）
  try { getMouseBtnFn = new NativeFunction(base.add(RVA_AIM.Input_GetMouseButton), 'bool', ['int32', 'pointer']); } catch(e) { getMouseBtnFn = null; }     // 连接：检测鼠标按键（失败=无法检测按键，自瞄不触发）
  try { linecastFn = new NativeFunction(base.add(RVA_AIM.Physics_Linecast), 'bool', ['pointer', 'pointer', 'int32', 'pointer']); } catch(e) { linecastFn = null; } // 连接：检测有没有墙（失败=默认敌人都能看见）

  return true;                                                           // 全部连接成功
}
```

**作用**：把9个"接线头"连到游戏内部的真实函数上。就像给修改器装上9根线，每根线连到游戏的一个功能。

错误处理策略：
- **核心功能**（获取管理器、读坐标、判断自己、判断死亡、转动视角）失败 → 整个自瞄无法启动
- **非核心功能**（查看队伍、检测鼠标、检测隔墙）失败 → 只是缺少该功能，自瞄仍可运行。比如没有隔墙检测就默认敌人都能看见

---

## 9. isValidPlayer() — 验证是不是有效玩家（第99-106行）

```javascript
function isValidPlayer(pp) {
  if (!pp || pp.isNull()) return false;                                  // 地址为空？不是玩家
  try {
    var team = pp.add(OFF_AIM.E_team).readS32();                         // 读取角色身上的队伍标记（偏移0x20）
    return (team === 0 || team === 1 || team === 2);                     // 0=潜伏者，1=保卫者，2=中立，是这三个之一就是有效玩家
  } catch(e) { return false; }                                          // 读不到就不是玩家
}
```

**作用**：检查一个内存地址是不是真的指向一个玩家角色。方法很简单——读取队伍标记，如果是0（潜伏者）、1（保卫者）或2（中立）就是有效玩家，其他值说明这个地址指向的不是玩家。

它被 getAllPlayers() 循环调用，每读到一个玩家地址就调一次，逐个验证。所有player都要验证，不是只验证"我"一个人。

isValidPlayer() 在 getAllPlayers() 里被调用，遍历3个名单（GM_allPlayers、GM_playersBL、GM_playersGR）时， 每一个读到的玩家地址都会过一遍验证 ：

它的作用是 过滤垃圾数据 ——内存里有些地址可能指向已销毁的对象或无效数据，队伍值不是0/1/2的就是假玩家，直接跳过。房间里的所有人（包括你自己、队友、敌人）都要过这个检查。

区分"是不是我"是后面 isMyPlayerFn() 干的事，不是 isValidPlayer() 的职责。

---

## 10. readList() — 读取玩家列表（第108-120行）

```javascript
function readList(listPtr) {
  var result = [];                                                       // 存放读到的玩家地址
  if (!listPtr || listPtr.isNull()) return result;                       // 列表为空？返回空数组
  try {
    var items = listPtr.add(OFF_AIM.List_items).readPointer();           // 拿到列表内部的数组（偏移0x08）
    if (!items || items.isNull()) return result;                         // 内部数组为空？返回空
    var count = listPtr.add(OFF_AIM.List_size).readS32();                // 列表里当前有几个人（偏移0x0C）
    for (var i = 0; i < count; i++) {                                    // 从第1个读到最后1个
      var elem = items.add(OFF_AIM.Arr_data + i * OFF_AIM.ptrSize).readPointer();  // 逐个读取每个人的地址
      if (elem && !elem.isNull()) result.push(elem);                     // 地址有效就记下来
    }
  } catch(e) {}
  return result;                                                         // 返回所有玩家的地址列表
}
```

**作用**：读取的是 蓝队名单和红队名单，从第一行读到最后一行，把每个人的地址记下来。

---

## 11. readArray() — 读取玩家数组（第122-134行）

```javascript
function readArray(arrPtr) {
  var result = [];                                                       // 存放读到的玩家地址
  if (!arrPtr || arrPtr.isNull()) return result;                         // 数组为空？返回空数组
  try {
    var len = arrPtr.add(OFF_AIM.Arr_len).readU32();                     // 数组里有多少个人（偏移0x0C）
    for (var i = 0; i < len; i++) {                                      // 从第1个读到最后1个
      var elem = arrPtr.add(OFF_AIM.Arr_data + i * OFF_AIM.ptrSize).readPointer();  // 逐个读取每个人的地址
      if (elem && !elem.isNull()) result.push(elem);                     // 地址有效就记下来
    }
  } catch(e) {}
  return result;                                                         // 返回所有玩家的地址列表
}
```

**作用**：读取的是 所有玩家名单 ，

---

## 12. getAllPlayers() — 获取房间所有玩家（第136-154行）

```javascript
function getAllPlayers(gm) {
  var map = {};                                                          // 用Map去重，同一个人只记一次
  var arr = readArray(gm.add(OFF_AIM.GM_allPlayers).readPointer());     // 从"所有玩家名单"读取（偏移0x1C）
  for (var i = 0; i < arr.length; i++) {
    if (isValidPlayer(arr[i])) map[arr[i].toString()] = arr[i];         // 有效玩家就加入Map
  }
  var bl = readList(gm.add(OFF_AIM.GM_playersBL).readPointer());        // 从"蓝队（潜伏者）名单"读取（偏移0x20）
  for (var i = 0; i < bl.length; i++) {
    if (isValidPlayer(bl[i])) map[bl[i].toString()] = bl[i];            // 有效玩家就加入Map
  }
  var gr = readList(gm.add(OFF_AIM.GM_playersGR).readPointer());        // 从"红队（保卫者）名单"读取（偏移0x28）
  for (var i = 0; i < gr.length; i++) {
    if (isValidPlayer(gr[i])) map[gr[i].toString()] = gr[i];            // 有效玩家就加入Map
  }
  return Object.values(map);                                             // 返回去重后的所有玩家
}
```

**作用**：从3个名单里收集所有玩家，并且去重。3个名单是：

- **所有玩家名单**（allPlayers）——房间里所有人
- **蓝队名单**（playersBL）——潜伏者
- **红队名单**（playersGR）——保卫者

同一个人可能同时出现在"所有玩家"和"队伍名单"里，所以用Map去重，确保每个人只出现一次。

---

## 13. getPlayerPos() — 获取玩家在地图上的位置（第156-184行）

```javascript
function getPlayerPos(player) {
  if (!player || player.isNull()) return null;                           // 角色地址无效？返回空
  try {
    // 方法1：通过游戏引擎正规方式——先拿位置标记，再读坐标
    var transform = compGetTransform(player, ptr(0));                    // 获取角色的位置标记
    if (transform && !transform.isNull()) {
      var posBuf = Memory.alloc(12);                                     // 分配12字节缓冲区存坐标（3个float，每个4字节）
      transformGetPos(posBuf, transform, ptr(0));                        // 读取坐标到缓冲区
      var x = posBuf.readFloat();                                        // 左右位置
      var y = posBuf.add(4).readFloat();                                 // 高低位置
      var z = posBuf.add(8).readFloat();                                 // 前后位置
      if (Math.abs(x) < 5000 && Math.abs(y) < 5000 && Math.abs(z) < 5000) {  // 坐标合理性检查，防止读到垃圾数据
        return { x: x, y: y, z: z };
      }
    }
    // 方法2：备用——直接从3D人物模型上读坐标
    var container = player.add(OFF_AIM.P_characterContainer).readPointer();  // 获取人物模型容器（偏移0x58）
    if (container && !container.isNull()) {
      var x = container.add(0x38).readFloat();                           // 模型上的左右位置
      var y = container.add(0x3C).readFloat();                           // 模型上的高低位置
      var z = container.add(0x40).readFloat();                           // 模型上的前后位置
      if (Math.abs(x) < 5000 && Math.abs(y) < 5000 && Math.abs(z) < 5000) {  // 坐标合理性检查
        return { x: x, y: y, z: z };
      }
    }
  } catch(e) {}
  return null;                                                           // 两种方法都失败，返回空
}
```

**作用**：获取一个角色在地图上的精确位置（前后、左右、高低）。用两种方法：

1. **首选**：通过游戏引擎的正规方式——先拿角色的位置标记，再读坐标。就像问游戏引擎"这个人站在哪"
2. **备用**：直接从角色的3D模型上读坐标。如果正规方式失败就用这个

最后检查坐标是否合理（绝对值<5000），防止读到垃圾数据。



方案 1
逻辑遵循 Unity 标准，后续扩展功能（射线检测、朝向计算、骨骼定位）都能无缝衔接，代码易调试、易复用。

调用游戏原生函数，执行逻辑和正常游戏行为一致，**隐蔽性更强**

方案 2
偏移值零散，没有统一规范，后续新增功能需要不断追加硬编码偏移，代码臃肿，出问题难以排查。

内存直接读取，速度略快，但**硬偏移读取属于典型内存篡改特征**

---

## 14. getBonePos() — 获取瞄准部位的位置（第186-192行）

```javascript
function getBonePos(player, boneIndex) {
  var pos = getPlayerPos(player);                                        // 先拿到角色的脚底位置
  if (!pos) return null;                                                 // 拿不到位置就返回空
  var yOffsets = [1.65, 1.45, 1.05, 0.85, 0.75];                        // 5个身体部位的高度偏移（米）：头部/脖子/胸部/腰部/腿部
  // dump.cs里没有这个数组，游戏用真正的骨骼Transform（spine/spine1/neck），不是Y偏移
 // 这是开发者根据playerHeight=2.6m估算的（见下方IDA依据）
  var yOff = yOffsets[boneIndex % yOffsets.length] || 1.05;              // boneIndex%5取对应偏移，aimBone=7时7%5=2=胸部(+1.05m)
                                                                        // %5是防呆机制，防止boneIndex越界崩溃
  pos.y += yOff;                                                         // 在脚底位置上加上高度偏移
  return pos;                                                            // 返回估算的身体部位位置
}
```

**作用**：估算敌人某个身体部位的位置。不是真的读取骨骼系统，而是在脚底位置上加上固定高度偏移：

| boneIndex % 5 | 偏移量 | 对应部位 | 游戏里的感觉 |
|---|---|---|---|
| 0 | +1.65米 | 头部 | 爆头线 |
| 1 | +1.45米 | 脖子 | 脖子位置 |
| 2 | +1.05米 | 胸部 | **aimBone=7落在这里**（7%5=2） |
| 3 | +0.85米 | 腰部 | 腰腹位置 |
| 4 | +0.75米 | 腿部 | 大腿位置 |

> 注意：这是估算，蹲下或趴下时高度不准。



Unity 角色默认**坐标锚点在脚底**： 

1. 游戏内置 `footPos`（脚底坐标）(public class Player : Entity )，底层逻辑就是 `compGetTransform + transformGetPos`，和代码里 `getPlayerPos` 读取逻辑完全一致。
2.  2. 角色碰撞体从脚底向上延伸，总高度2.6米，因此头部位置比脚底高出 **1.65~1.75米**，代码里的 `yOffsets` 就是按这个高度做的偏移补偿，用来精准锁头。





### yOffsets的IDA依据

`yOffsets` 的5个数字不是从游戏代码中提取的，是开发者根据游戏定义的角色高度估算的。依据来自IDA反汇编 `Player$$.cctor`（Player类的静态构造函数，游戏启动时自动执行，初始化类的静态字段）：

| 字段 | 静态偏移 | 十六进制值 | 实际值 | 含义 |
|---|---|---|---|---|
| `defaultMoveSpeed` | +0x0 | 0x410AAAA4 | 8.67 | 默认移动速度 |
| **`playerHeight`** | **+0x4** | **0x40266666** | **2.6** | **角色碰撞体总高度（米）** |
| `crouchSubHeight` | +0x8 | 0x3F4CCCCD | 0.8 | 蹲下减少的高度（蹲下后高1.8米） |
| `mapCmrHeight` | +0xC | 0x3F70A3D7 | 0.94 | 小地图相机高度 |
| `mapCmrCrouchSubHeight` | +0x10 | 0x3F051EB8 | 0.52 | 小地图蹲下减少高度 |
| `playerGravity.y` | +0x18 | 0xC1F00000 | -30 | 重力加速度 |

> **`Player$$.cctor`是什么？** 它是Player类的静态构造函数（class constructor），游戏加载Player类时自动执行一次，用来初始化 `static readonly` 字段。上面的数值就保存在这个函数的机器码里（硬编码在IL2CPP编译后的GameAssembly.dll中），不是从配置文件读取的。

> **yOffsets怎么来的？** 游戏定义角色总高2.6米，开发者按人体比例估算：头部约1.65m（2.6m的63%）、胸部约1.05m（2.6m的40%）等。游戏本身没有定义这些部位高度——游戏用 `CharacterModel.hitboxes`（Transform数组）和 `spine/spine1/neck` 骨骼做精确受击判定，aim.js选择了简化方案用固定偏移估算。

---

## 15. checkVisibility() — 检测敌人是否被墙挡住（第194-205行）

```javascript
function checkVisibility(from, to) {
  if (!linecastFn) return true;                                          // 没有检测函数？默认能看到（不阻挡）
  try {
    var buf1 = Memory.alloc(12);                                         // 分配12字节存起点坐标（你的位置）
    buf1.writeFloat(from.x); buf1.add(4).writeFloat(from.y); buf1.add(8).writeFloat(from.z);
    var buf2 = Memory.alloc(12);                                         // 分配12字节存终点坐标（敌人的位置）
    buf2.writeFloat(to.x); buf2.add(4).writeFloat(to.y); buf2.add(8).writeFloat(to.z);
    return !linecastFn(buf1, buf2, -1, ptr(0));                          // 画线检测，-1=检测所有类型的障碍物，有墙=true，取反=看不到
  } catch(e) { return true; }                                           // 出错默认能看到
}
```

**作用**：从你到敌人之间画一条线，检测中间有没有墙。就像现实中你隔着墙看不到对面的人。layerMask=-1表示检测所有类型的障碍物。

如果检测函数不可用，默认返回"能看到"（不阻挡）。

---

## 16. targetScanner() — 目标扫描器（第207-271行）⭐核心

```javascript
function targetScanner() {
  if (!enabled) return;                                                  // 自瞄关了就不执行
  var gm = getGM();                                                      // 拿到游戏总管理器
  if (!gm || gm.isNull()) return;                                        // 拿不到就退出

  // 第一步：找到"我"是谁
  if (!myPlayer || myPlayer.isNull()) {                                  // 还没找到自己？
    var all = getAllPlayers(gm);                                          // 获取所有玩家
    for (var i = 0; i < all.length; i++) {
      try { if (isMyPlayerFn(all[i], ptr(0))) { myPlayer = all[i]; break; } } catch(e) {}  // 逐个问"是不是我"，找到了就记住
    }
    if (!myPlayer) { cachedTarget = null; return; }                      // 找不到自己？清空目标，退出
  }

  // 第二步：检查自己的状态
  try { if (!isMyPlayerFn(myPlayer, ptr(0))) { myPlayer = null; cachedTarget = null; return; } } catch(e) { myPlayer = null; cachedTarget = null; return; }  // 我不再是我了？（断线/切换）重置
  try { if (isDeadFn(myPlayer, ptr(0))) return; } catch(e) { return; }  // 我死了？不执行自瞄

  // 第三步：读取当前视角
  var myPos = getBonePos(myPlayer, CONFIG.aimBone);                      // 获取我的位置（瞄准部位）
  if (!myPos) return;                                                    // 拿不到位置就退出

  scanYawDeg = myPlayer.add(OFF_AIM.P_cameraRotation).readFloat();       // 读取我面朝的水平方向（偏移0x4C）
  scanPitchDeg = myPlayer.add(OFF_AIM.P_cameraRotation + 4).readFloat(); // 读取我面朝的垂直方向（偏移0x50）

  // 第四步：遍历所有玩家，筛选敌人
  var allPlayers = getAllPlayers(gm);                                     // 获取所有玩家
  var myTeam = 0;                                                         // 我的队伍
  try {
    if (getTeamFn) myTeam = getTeamFn(myPlayer, ptr(0));                 // 通过函数查看我的队伍
    else myTeam = myPlayer.add(OFF_AIM.E_team).readS32();                // 函数不可用就直接读内存（偏移0x20）
  } catch(e) {}

  var best = null;                                                        // 最优目标
  var bestAngleDeg = 999999;                                              // 最小角度差（初始设很大）

  for (var i = 0; i < allPlayers.length; i++) {                          // 遍历每个玩家
    var p = allPlayers[i];
    try {
      if (p.equals(myPlayer)) continue;                                  // 是我自己？跳过
      if (isDeadFn(p, ptr(0))) continue;                                 // 已经死了？跳过，不瞄尸体
      var team = getTeamFn ? getTeamFn(p, ptr(0)) : p.add(OFF_AIM.E_team).readS32();  // 查看对方队伍
      var isEnemy = (myTeam === 2) || (team === 2) || (myTeam !== team); // 敌我判断：中立看谁都是敌人，非中立不同队就是敌人
      if (!isEnemy) continue;                                            // 是队友？跳过

      var targetPos = getBonePos(p, CONFIG.aimBone);                     // 获取敌人的位置
      if (!targetPos) continue;                                          // 拿不到位置？跳过

      if (CONFIG.visibilityCheck) {                                      // 开启了隔墙检测？
        if (!checkVisibility(myPos, targetPos)) continue;                // 被墙挡住了？跳过
      }

      // 第五步：计算角度和距离
      var dx = targetPos.x - myPos.x;                                    // 敌人相对我的左右距离
      var dy = targetPos.y - myPos.y;                                    // 敌人相对我的高低距离
      var dz = targetPos.z - myPos.z;                                    // 敌人相对我的前后距离
      var dist = Math.sqrt(dx*dx + dy*dy + dz*dz);                      // 三维直线距离
      if (dist > CONFIG.maxAimDistance) continue;                        // 超过200米？太远了，跳过

      var targetYawDeg = Math.atan2(dx, dz) * 180.0 / Math.PI;          // 敌人的水平角度（左右）
      var targetPitchDeg = Math.atan2(dy, Math.sqrt(dx*dx + dz*dz)) * 180.0 / Math.PI;  // 敌人的垂直角度（上下）

      var yawDiff = targetYawDeg - scanYawDeg;                           // 和我当前视角的水平差
      var pitchDiff = targetPitchDeg - scanPitchDeg;                     // 和我当前视角的垂直差
      if (yawDiff > 180) yawDiff -= 360;                                 // 处理角度环绕（-180到180）
      if (yawDiff < -180) yawDiff += 360;
      if (pitchDiff > 180) pitchDiff -= 360;
      if (pitchDiff < -180) pitchDiff += 360;
      var angleDeg = Math.sqrt(yawDiff*yawDiff + pitchDiff*pitchDiff);   // 综合角度距离（偏离准星多少度）

      if (angleDeg > CONFIG.maxAngleFOV) continue;                       // 超过30度FOV？不在视野内，跳过

      // 第六步：选择最优目标
      if (angleDeg < bestAngleDeg) {                                      // 角度更小=离准星更近
        bestAngleDeg = angleDeg;
        best = { player: p, pos: targetPos, targetYawDeg: targetYawDeg, targetPitchDeg: targetPitchDeg, angleDeg: angleDeg, dist: dist };  // 记录最优目标
      }
    } catch(e) {}
  }

  cachedTarget = best;                                                    // 把找到的最优目标存入缓存，交给瞄准器
}
```

**作用**：每30ms执行一次，负责"找敌人"。完整流程：

1. 拿到游戏总管理器 → 失败就退出
2. 找到"我"是谁 → 遍历所有玩家，逐个问"是不是我"
3. 检查自己的状态 → 死了就不执行，断线就重置
4. 读取当前视角 → 我面朝哪个方向
5. 遍历所有玩家，筛选敌人 → 跳过自己、死人、队友、太远的、不在视野内的
6. 选择最优目标 → 离准星角度最小的敌人，存入cachedTarget

---

## 17. writeAimbot() — 执行瞄准（第273-313行）⭐核心

```javascript
function writeAimbot() {
  if (!enabled || !myPlayer || !cachedTarget) return;                    // 自瞄关了/没找到自己/没目标？退出

  try {
    // 第一步：读取当前视角
    var curYawDeg = myPlayer.add(OFF_AIM.P_cameraRotation).readFloat();       // 我当前面朝的水平方向（偏移0x4C）
    var curPitchDeg = myPlayer.add(OFF_AIM.P_cameraRotation + 4).readFloat(); // 我当前面朝的垂直方向（偏移0x50）

    // 第二步：检测玩家是否手动转头（防止自瞄和玩家操作打架）
    var userYawDelta = curYawDeg - scanYawDeg;                           // 当前视角和上次扫描时的水平差
    var userPitchDelta = curPitchDeg - scanPitchDeg;                     // 当前视角和上次扫描时的垂直差
    if (userYawDelta > 180) userYawDelta -= 360;                         // 处理角度环绕
    if (userYawDelta < -180) userYawDelta += 360;
    if (userPitchDelta > 180) userPitchDelta -= 360;
    if (userPitchDelta < -180) userPitchDelta += 360;
    var userAngleDelta = Math.sqrt(userYawDelta*userYawDelta + userPitchDelta*userPitchDelta);  // 玩家手动转了多少度

    if (userAngleDelta > CONFIG.maxAngleFOV * 0.5) {                     // 转了超过FOV的一半（15度）？
      cachedTarget = null;                                                // 说明玩家自己在转头，放弃锁定
      return;
    }

    // 第三步：计算最终瞄准方向
    var targetYawDeg = cachedTarget.targetYawDeg;                         // 目标的水平角度
    var targetPitchDeg = cachedTarget.targetPitchDeg;                     // 目标的垂直角度

    var finalYawDeg = targetYawDeg;                                       // 默认直接锁到目标
    var finalPitchDeg = targetPitchDeg;
    if (CONFIG.smoothness < 1.0 && CONFIG.smoothness > 0.0) {            // 开启平滑插值？
      var yawDiff = targetYawDeg - curYawDeg;                             // 目标和当前的水平差
      var pitchDiff = targetPitchDeg - curPitchDeg;                       // 目标和当前的垂直差
      if (yawDiff > 180) yawDiff -= 360;                                  // 处理角度环绕
      if (yawDiff < -180) yawDiff += 360;
      if (pitchDiff > 180) pitchDiff -= 360;
      if (pitchDiff < -180) pitchDiff += 360;
      finalYawDeg = curYawDeg + yawDiff * CONFIG.smoothness;              // 只移动差值的一部分，慢慢转过去
      finalPitchDeg = curPitchDeg + pitchDiff * CONFIG.smoothness;        // smoothness=0.5时每次只转差距的一半
    }

    // 第四步：直接写入视角（不是通过游戏的"正规转头"函数，而是直接改内存）
    myPlayer.add(OFF_AIM.P_cameraRotation).writeFloat(finalYawDeg);           // 写入水平方向（偏移0x4C）
    myPlayer.add(OFF_AIM.P_cameraRotation + 4).writeFloat(finalPitchDeg);     // 写入垂直方向（偏移0x50）

    // 第五步：后坐力清零（开枪时枪口不会往上跳、不会往旁边飘）
    var recoil = myPlayer.add(OFF_AIM.P_recoil).readPointer();           // 读取后坐力对象（偏移0x54）
    if (recoil && !recoil.isNull()) {
      recoil.add(0x10).writeU32(0);                                      // 清零后坐力字段1
      recoil.add(0x24).writeU32(0);                                      // 清零后坐力字段2
      recoil.add(0x40).writeU32(0);                                      // 清零后坐力字段3
      recoil.add(0x54).writeU32(0);                                      // 清零后坐力字段4
    }

    frameCount++;                                                         // 执行次数+1
  } catch(e) {}
}
```

**作用**：每16ms执行一次，负责"移动准星"。完整流程：

1. 读取当前视角 → 我现在面朝哪
2. 检测玩家是否手动转头 → 转了超过15度就放弃锁定，让玩家自己控制
3. 平滑插值 → smoothness<1时慢慢转过去，1.0时瞬间锁死
4. 直接写入视角 → 绕过游戏的"正规转头"函数，直接改内存
5. 后坐力清零 → 枪口不跳不飘，配合自瞄锁住敌人后开枪纹丝不动

---

## 18. aimLoop() — 瞄准主循环（第315-330行）

```javascript
function aimLoop() {
  if (!enabled) return;                                                  // 自瞄关了？不执行

  if (!CONFIG.autoAim) {                                                 // 不是自动模式？
    if (!getMouseBtnFn) return;                                          // 没有鼠标检测函数？不执行
    try {
      var btnDown = getMouseBtnFn(CONFIG.aimKey, ptr(0));                // 检测鼠标左键有没有按住
      if (!btnDown) return;                                              // 没按住？不执行（松开左键就停止自瞄）
    } catch(e) { return; }
  }

  if (!myPlayer) return;                                                 // 没找到自己？不执行
  if (!cachedTarget) return;                                             // 没找到目标？不执行

  writeAimbot();                                                         // 全部通过，执行瞄准
}
```

**作用**：每16ms触发一次，是瞄准的"启动器"。

流程：
1. 自瞄关了？→ 不执行
2. 不是自动模式？→ 检查鼠标左键有没有按住，没按就不执行
3. 没找到自己？→ 不执行
4. 没找到目标？→ 不执行
5. 全部通过 → 调用writeAimbot()移动准星

---

## 19. installRoomHooks() — 监听游戏事件（第332-345行）

```javascript
function installRoomHooks(base) {
  var addrs = [0xAF9A90, 0xAEE370, 0xAF5B30];                           // 3个游戏事件的地址
  for (var i = 0; i < addrs.length; i++) {
    try {
      var h = Interceptor.attach(base.add(addrs[i]), {                   // 在游戏函数上装"监听器"
        onEnter: function() {                                            // 游戏函数被调用时触发
          myPlayer = null;                                               // 重置"我"（地址可能变了）
          targetEnemy = null;                                            // 重置目标
          frameCount = 0;                                                // 重置计数器
        }
      });
      roomHooks.push(h);                                                 // 记录监听器，关闭时要拔掉
    } catch(e) {}
  }
}
```

**作用**：在3个游戏事件上装"监听器"，当这些事件发生时自动重置自瞄状态。

| 事件 | 游戏场景 | 触发时做什么 |
|---|---|---|
| `GameManager$$AddPlayer` (0xAF9A90) | 有新玩家加入房间 | 重置"我"和目标，重新查找 |
| `ModeBase$$Awake` (0xAEE370) | 游戏模式初始化（进入新地图） | 重置所有状态 |
| `ModeBase$$OnStartNewGameRound` (0xAF5B30) | 新回合开始（比如爆破模式换边） | 重置所有状态 |

为什么要重置？因为换局/换边后，"我"的内存地址可能变了，旧的数据已经无效。

---

## 20. enable() — 启用自瞄（第347-362行）

```javascript
enable: function() {
  if (enabled) return;                                                   // 已经开了？不重复启动
  var mod = getGameAssembly();                                           // 获取游戏核心模块
  if (!mod) { sendLog('error', '自瞄', '无 GameAssembly.dll'); return; }  // 找不到就报错
  if (!initNativeFunctions()) { sendLog('error', '自瞄', 'NativeFunction 初始化失败'); return; }  // 连接游戏函数失败就报错
  installRoomHooks(mod.base);                                            // 安装3个游戏事件监听器
  aimTimer = setInterval(aimLoop, 16);                                   // 启动瞄准定时器（每16ms移动准星）
  scanTimer = setInterval(targetScanner, 30);                            // 启动扫描定时器（每30ms找敌人）
  enabled = true;                                                        // 标记为已启用
  sendLog('success', '自瞄', '已启用');                                   // 发送成功通知
  sendStatus('aim', true);                                               // 更新状态
}
```

**作用**：启动自瞄的完整流程：
1. 已经开了？→ 不重复启动
2. 找到游戏核心模块？→ 找不到就报错
3. 连接9个游戏内部函数？→ 失败就报错
4. 安装3个游戏事件监听器
5. 启动**扫描定时器**（30ms一次，找敌人）
6. 启动**瞄准定时器**（16ms一次，移准星）
7. 标记为已启用，发送通知

---

## 21. disable() — 关闭自瞄（第363-378行）

```javascript
disable: function() {
  if (!enabled) return;                                                  // 已经关了？不重复关闭
  if (aimTimer) { clearInterval(aimTimer); aimTimer = null; }            // 停掉瞄准定时器
  if (scanTimer) { clearInterval(scanTimer); scanTimer = null; }         // 停掉扫描定时器
  if (debugTimer) { clearInterval(debugTimer); debugTimer = null; }      // 停掉调试定时器
  for (var i = 0; i < roomHooks.length; i++) { try { roomHooks[i].detach(); } catch(e) {} }  // 拔掉3个游戏事件监听器
  roomHooks = [];                                                        // 清空监听器列表
  myPlayer = null;                                                       // 清空"我"
  targetEnemy = null;                                                    // 清空目标
  enabled = false;                                                       // 标记为已禁用
  sendLog('info', '自瞄', '已禁用');                                      // 发送通知
  sendStatus('aim', false);                                              // 更新状态
}
```

**作用**：关闭自瞄，清理一切：
1. 停掉所有定时器
2. 拔掉3个游戏事件监听器
3. 清空所有状态
4. 标记为已禁用，发送通知

---

## 22. isEnabled() — 查询状态（第379行）

```javascript
isEnabled: function() { return enabled; }                                // 返回自瞄是否开启
```

**作用**：外部查询自瞄是否开启。

---

## 23. setConfig() — 修改参数（第380-386行）

```javascript
setConfig: function(cfg) {
  if (cfg.smoothness !== undefined) CONFIG.smoothness = cfg.smoothness;           // 修改平滑度（不用重启，运行时生效）
  if (cfg.maxAimDistance !== undefined) CONFIG.maxAimDistance = cfg.maxAimDistance; // 修改最远锁定距离
  if (cfg.maxAngleFOV !== undefined) CONFIG.maxAngleFOV = cfg.maxAngleFOV;       // 修改FOV角度
  if (cfg.visibilityCheck !== undefined) CONFIG.visibilityCheck = cfg.visibilityCheck; // 开关隔墙检测
  if (cfg.autoAim !== undefined) CONFIG.autoAim = cfg.autoAim;                   // 开关自动瞄准
}
```

**作用**：运行时修改自瞄参数，不用重启。可以调整：平滑度、最远距离、FOV角度、隔墙检测、自动瞄准。

---

## 24. getConfig() — 读取当前参数（第387-390行）

```javascript
getConfig: function() {
  return { smoothness: CONFIG.smoothness, maxAngleFOV: CONFIG.maxAngleFOV, maxAimDistance: CONFIG.maxAimDistance, autoAim: CONFIG.autoAim, visibilityCheck: CONFIG.visibilityCheck };  // 返回当前配置
}
```

**作用**：外部读取当前自瞄参数配置。

