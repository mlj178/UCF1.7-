# 近战距离修改器 技术总结

## 一、玩家识别方法

### 核心路径

```
WPN_Knife + 0x30 → owner (Player*)
                      ↓
              isMyPlayer(owner)
                      ↓
                 true = 本地玩家
```

### 偏移量定位过程

通过 v18 的日志扫描脚本（扫描 WPN_Knife 对象上所有指针字段，逐一调 `isMyPlayer` 验证），确认 `owner` 位于 **`WPN_Knife + 0x30`**：

```
[近战]   +8  → 0x44294530
[近战]   +10 → 0x23c5f270
[近战]   +30 → 0x351fc450 ★ isMyPlayer=true   ← 正确偏移
[近战]   +48 → 0x227e9c20
```

### 安全调用方案

`isMyPlayer` 是 `NativeFunction`（RVA 0xB55FD0），直接在 `Interceptor.attach` 的 `onLeave` 中调用会导致跨线程崩溃。解决方案分两步：

**Step 1**：用 `Interceptor.replace` 劫持 `get_KnifeSpeed`（0xB170A0），NativeCallback 在游戏线程运行，安全调用 `isMyPlayer`，捕获 `myPlayer` 指针一次：

```javascript
Interceptor.replace(getKnifeSpeedAddr, new NativeCallback(function(self) {
    var result = origGetKnifeSpeed(self);
    if (!myPlayerFound) {
        var owner = self.add(0x8).readPointer();
        if (owner && isMyPlayerFn(owner)) {
            myPlayer = owner;
            myPlayerFound = true;
        }
    }
    return result;
}, 'float', ['pointer']));
```

**Step 2**：`Interceptor.attach` 的 `onLeave` 中纯指针比较，零 NativeFunction 调用：

```javascript
onLeave: function(retval) {
    if (!myPlayerFound) return;
    if (!this.owner.equals(myPlayer)) return;
    // 修改 range
}
```

---



### 闪退 2：v14 — 初始化期间调 NativeFunction

**现象**：未进房间就 "Process terminated"，日志只打到 "isMyWeapon @ ..." 和 "房间切换，重置缓存"

**根因**：

```javascript
// v14 错误写法
onEnter: function(args) {
    var wpn = args[1];
    this.isMine = isPlayerWeapon(wpn);  // 调了 isMyWeapon(wpnPtr, ptr(0))
}
```

游戏初始化期间 `GetKnifeAttackData` 也被触发（预加载/缓存），此时武器对象未完全初始化，`owner` 字段是野指针。`isMyWeapon` 访问无效内存 → 立即崩溃。

**修复**：不在 attach 的 onEnter 中调用任何 NativeFunction。

### 闪退 3：v18/v19 — onLeave 中调 NativeFunction

**现象**：v18 调了 `isMyPlayer(some_pointer)` → 挥刀 ~12 次后崩溃

**根因**：`Interceptor.attach` 的 `onLeave` 运行在 Frida 线程，调用 NativeFunction 会跨线程执行游戏代码，产生竞态条件。v18 每刀都在 `onLeave` 中调 `isMyPlayerFn(candidate)`，12 次后触发内存访问冲突。



## 四、全模式应用方法

### 为什么 v8 不是全模式生效

v8 有**两个致命问题**导致部分模式无效：

**问题1：Hook 点不对**

| | v8 | v12+/v21 |
|------|-----|-----|
| Hook 函数 | `WPN_Knife.PlayKnifeAttackAnim` (0xB642B0) | `WPN_Knife.GetKnifeAttackData` (0xB63EC0) |
| 函数类型 | **动画函数** | **数据函数** |

`PlayKnifeAttackAnim` 是播放攻击动画的函数。轻击（Combo1/2）走这条路，但**重击（Bigshot）走 `OnSpecialBtnDown`**（0xB64240），不经过 `PlayKnifeAttackAnim`。某些游戏模式（如生化模式、挑战模式）的攻击判定链路可能直接取数据做伤害计算，跳过动画函数。

`GetKnifeAttackData` 是底层数据获取函数——**只要游戏需要知道攻击距离，就必然调它**，无论什么模式、什么攻击类型。

**问题2：写入目标不同**

```
v8 写入路径:
  WPN_Knife + 0x68 → WeaponData_Knife* (ScriptableObject, 全局共享资产)
                   + 0xC0 → array[] → range

v12+/v21 写入路径:
  GetKnifeAttackData(retval) → retval+0x4 = range (调用者栈上临时缓冲区)
```

v8 写入 `WeaponData_Knife` 这个 **ScriptableObject**。不同游戏模式可能从不同的 AssetBundle 加载不同的 `WeaponData_Knife` 实例。如果某个模式加载的武器数据不在 v8 遇到的那个资产实例上，range 就不会被修改。

v21 写入每次 `GetKnifeAttackData` 返回的**临时缓冲区**——函数被调一次就改一次，不依赖任何静态资产实例。

### Hook 目标

| 函数 | RVA | 说明 |
|------|-----|------|
| `WPN_Knife.GetKnifeAttackData` | 0xB63EC0 | 所有近战武器的攻击数据获取入口 |
| `PlayerWeapons.get_KnifeSpeed` | 0xB170A0 | 每次挥刀必调，用于安全捕获 myPlayer |

### 为什么 v21 全模式生效

`WPN_Knife.GetKnifeAttackData` 是所有近战武器（刀、斧、铲等）获取攻击数据的统一底层函数。无论团队模式、生化模式、个人竞技、挑战模式，只要玩家挥刀，游戏必然调此函数获取 `KnifeAttackData` 结构体。

修改点在 `retval + 0x4`（range 字段），不涉及任何模式特定的配置或 ScriptableObject，因此全模式通用。

### 房间切换处理

Hook 以下三个函数检测房间切换并重置 `myPlayer`：

| 函数 | RVA | 说明 |
|------|-----|------|
| `GameRoundEnd` | 0xAFAA40 | 回合结束 |
| `OnStartRound` | 0xAF5B30 | 回合开始 |
| `NanoStart` | 0xAF15D0 | 纳新开始 |

### 完整数据流

```
玩家挥刀
    ↓
WPN_Knife.GetKnifeAttackData(attackIndex)
    ↓
onEnter: 读 self + 0x30 = owner 指针
    ↓
游戏函数执行 → 从 WeaponData 取值填入 retval
    ↓
onLeave: owner == myPlayer ?
    ├─ 是 → retval+0x4.writeFloat(orig × 50)
    └─ 否 → 跳过（Bot）
    ↓
KnifeAttackData 返回给调用者 → 攻击判定使用修改后的 range
```











# 近战距离修改器 v22 脚本分析

## 1. 概述

`knife_range_v22.js` 用于修改本地玩家的近战攻击范围（刀距）。  
脚本采用 **Hook 获取攻击数据** 的方式，在游戏读取近战攻击属性（伤害、范围、角度）时，拦截并放大 `range` 值，从而达到超远刀距的效果。

版本 v22 的特殊点在于：  
- 将原有的 `Interceptor.replace` 改为 `Interceptor.attach`，以便与同时使用 `replace` 的 **快刀脚本（speed_knife_v16）** 兼容共存。  
- 通过监听 `get_KnifeSpeed` 的调用捕获本地玩家的 `Player` 指针，而非自行遍历查找。

---

## 2. 关键内存地址

### 2.1 函数 RVA

| 函数                           | RVA      | 说明                                         |
| ------------------------------ | -------- | -------------------------------------------- |
| `Player.get_isMyPlayer`        | 0xB55FD0 | 判断 Player 是否为本地玩家                   |
| `PlayerWeapons.get_KnifeSpeed` | 0xB170A0 | 获取刀速，用于捕获 `myPlayer`                |
| `WPN_Knife.GetKnifeAttackData` | 0xB63EC0 | 获取指定刀攻击类型的数据（伤害、范围、角度） |

### 2.2 数据字段偏移

| 偏移   | 所属                     | 描述                                                 |
| ------ | ------------------------ | ---------------------------------------------------- |
| `0x8`  | `PlayerWeapons` 实例     | 指向所属 Player 的指针                               |
| `0x30` | `WPN_Knife` 实例（推测） | 指向所属 Player 的指针（脚本中 `this.owner` 的来源） |
| `+0x0` | `KnifeAttackData` 返回值 | 伤害（damage）                                       |
| `+0x4` | `KnifeAttackData` 返回值 | 范围（range）                                        |
| `+0x8` | `KnifeAttackData` 返回值 | 角度（angle）                                        |

> `KnifeAttackData` 结构是游戏用于描述每一次刀击属性的数据块，由 `GetKnifeAttackData` 返回其指针。

---

## 3. 模块逻辑详解

### 3.1 环境初始化

```javascript
var mod = Process.findModuleByName('GameAssembly.dll');
var base = mod.base;
var isMyPlayerFn = new NativeFunction(base.add(0xB55FD0), 'bool', ['pointer']);
var myPlayer = null;
var myPlayerFound = false;
```

- 获取 GameAssembly 基址，并实例化 `isMyPlayer` 判官函数。  
- 全局变量 `myPlayer` 用于存储本地玩家的地址，`myPlayerFound` 控制只捕获一次。

### 3.2 捕获本地玩家指针

```javascript
Interceptor.attach(base.add(0xB170A0), { // get_KnifeSpeed
    onLeave: function(retval) {
        if (myPlayerFound) return;
        var owner = this._self.add(0x8).readPointer();
        if (owner && !owner.isNull() && isMyPlayerFn(owner)) {
            myPlayer = owner;
            myPlayerFound = true;
        }
    }
});
```

- `get_KnifeSpeed` 函数签名为 `float get_KnifeSpeed(void* self)`，其中 `self` 是 `PlayerWeapons` 实例。  
- 从 `self + 0x8` 得到 `PlayerWeapons` 的持有者 Player 指针。  
- 通过 `isMyPlayer` 判断后，将 `myPlayer` 设置为本地玩家地址。  
- 采用 `attach` 而非 `replace`，避免与快刀脚本共存时发生冲突（两个脚本不能同时 `replace` 同一个函数）。

### 3.3 Hook `GetKnifeAttackData` 并修改范围

```javascript
Interceptor.attach(base.add(0xB63EC0), { // WPN_Knife.GetKnifeAttackData
    onEnter: function(args) {
        this.wpnSelf = args[1];   // WPN_Knife 实例
        this.attackIdx = args[2].toInt32(); // 攻击类型索引
        this.owner = args[1].add(0x30).readPointer(); // 所属 Player
    },
    onLeave: function(retval) {
        // 读取原始数据
        var dmg = retval.add(0x0).readFloat();
        var orig = retval.add(0x4).readFloat();
        var ang = retval.add(0x8).readFloat();
        
        // 校验 owner 是否为 myPlayer
        var isOwnerMine = myPlayerFound &&
            this.owner && !this.owner.isNull() &&
            this.owner.equals(myPlayer);
        if (!isOwnerMine) return; // 非本地玩家，跳过修改
        
        // 合法性检查
        if (!(orig > 0.3 && orig < 500)) return;
        
        // 修改范围 = 原范围 × 倍数
        retval.add(0x4).writeFloat(orig * KNIFE_RANGE_MULTIPLIER);
    }
});
```

**关键流程**：

1. **onEnter** 记录武器实例和所属 Player。
2. **onLeave** 中，从 `retval` 指向的结构体读取原始攻击数据。
3. 通过对比 `owner` 与 `myPlayer` 确保只修改本地玩家。
4. 对原始范围进行倍数放大（默认 50 倍），写回原地址。
5. 使用 `attach` 而非 `replace`，原函数仍然正常返回，脚本只是在函数返回后劫持数据。

### 3.4 房间切换重置

```javascript
var cleanupAddrs = [0xAFAA40, 0xAF5B30, 0xAF15D0];
for (var i = 0; i < cleanupAddrs.length; i++) {
    Interceptor.attach(base.add(cleanupAddrs[i]), {
        onEnter: function() {
            myPlayer = null;
            myPlayerFound = false;
            callCount = 0;
            rangeLogCount = 0;
        }
    });
}
```

- 在几个可能触发“房间/回合结束”的函数上挂接，重置全局状态，确保新游戏能重新捕获本地玩家。

---

## 4. 与其他脚本的兼容

以往的版本可能直接 `replace` 了 `get_KnifeSpeed` 或 `GetKnifeAttackData`，但如果快刀脚本（v16）已经 `replace` 了 `get_KnifeSpeed`，两个 `replace` 就会冲突。  
v22 改为 **全部使用 attach**，`get_KnifeSpeed` 只用于观察，不修改其返回值；`GetKnifeAttackData` 也只是在返回值上做手脚，不影响原函数执行。这样就能与使用 `replace` 的快刀脚本同时注入而不会崩溃。

---

## 5. 总结

| 条目     | 说明                                                         |
| -------- | ------------------------------------------------------------ |
| 目标     | 修改本地玩家的刀距，实现超远攻击                             |
| 原理     | Hook `GetKnifeAttackData`，在其返回值中放大 `range` 字段     |
| 关键函数 | `PlayerWeapons.get_KnifeSpeed`（用于取 myPlayer）、`WPN_Knife.GetKnifeAttackData` |
| 关键偏移 | `PlayerWeapons + 0x8` → Player；`KnifeAttackData + 0x4` → range |
| 特色     | 完全使用 `Interceptor.attach`，可与其他 `replace` 脚本共存   |
| 生命周期 | 监听回合结束函数，重置 myPlayer，确保新回合正常生效          |

