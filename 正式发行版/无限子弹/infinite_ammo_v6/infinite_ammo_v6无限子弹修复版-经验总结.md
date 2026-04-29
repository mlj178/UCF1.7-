# 无限子弹修复版 — 经验总结

> 从 V1 到 V6，6 个版本迭代中踩过的所有坑，用大白话讲清楚。

---

## 目录

1. [核心教训总览](#核心教训总览)
2. [坑1：ObscuredInt 加密弹药 —— 为什么写 9999 会卡死](#坑1obscuredint-加密弹药--为什么写-9999-会卡死)
3. [坑2：房间切换闪退 —— 旧对象没清理](#坑2房间切换闪退--旧对象没清理)
4. [坑3：掉帧卡顿 —— Hook 太频繁](#坑3掉帧卡顿--hook-太频繁)
5. [坑4：玩家识别 —— 不要管 Bot 的枪](#坑4玩家识别--不要管-bot-的枪)
6. [坑5：触发时机 —— 热路径不能有慢操作](#坑5触发时机--热路径不能有慢操作)
7. [坑6：武器数量限制 —— 为什么第5把枪无效](#坑6武器数量限制--为什么第5把枪无效)
8. [最终方案（V6）完整架构](#最终方案v6完整架构)
9. [Hook 函数地址速查表](#hook-函数地址速查表)

---

## 核心教训总览

| 教训 | 一句话总结 |
|------|-----------|
| **不要乱写内存值** | 弹药是加密的，写 `9999` 触发反作弊 → 卡死 |
| **切房间要清空记录** | 旧对象被回收，指针变悬垂 → 闪退 |
| **Hook 不要太频繁** | per-frame hook = 掉帧；只 Hook 关键函数 |
| **只处理玩家对象** | Bot 有 16 个，每个都处理 = 卡死；用 `isMyWeapon` 过滤 |
| **热路径零慢操作** | 开火是热路径，不能放 `Process.findRangeByAddress` |
| **不要设数量上限** | 武器实例会被反复创建，上限导致新枪无效 |

---

## 坑1：ObscuredInt 加密弹药 —— 为什么写 9999 会卡死

### 问题的本质

这个游戏的弹药值不是存成普通整数，而是用了一个叫 `ObscuredInt` 的加密结构体：

```
普通存储:    弹药 = 30           （直接写一个数字）
ObscuredInt: 弹药 = encrypt(30)   （写入的是加密后的数字）
```

**结构体内存布局（从 C# dump 还原）：**
```
offset 0x00: currentCryptoKey   ← 加密密钥（随机数）
offset 0x04: hiddenValue        ← 加密后的真实弹药值
offset 0x08: inited             ← 是否已初始化
offset 0x0C: fakeValue          ← 伪装值（给内存扫描器看的假值）
offset 0x10: fakeValueActive    ← 伪装值是否激活
```

### 踩坑过程

**V1/V2/V3/V4 的做法（❌ 错误）：**
```javascript
// 直接写 9999 到 fakeValue 偏移
ammoPtr.add(0x20).writeInt(9999);
```

**后果：**
- 游戏读到 `fakeValue` 是 9999，但 `hiddenValue` 里的真实加密值在被扣减
- 游戏内部校验 `fakeValue` 和 `hiddenValue` 不匹配 → 触发反作弊 → 画面卡死
- 症状：**射了十几发子弹后突然卡死**

### V5/V6 的解决方案（✅ 正确）

```javascript
// 第一次见到这把枪：把加密后的值原样记录下来
var cv = ammoPtr.add(0x0C).readInt();  // 读 fakeValue 的当前加密值
var av = ammoPtr.add(0x20).readInt();

// 之后每次锁：原样写回
ammoPtr.add(0x0C).writeInt(cv);  // 不写 9999，写原始加密值
ammoPtr.add(0x20).writeInt(av);
```

**原理：** 游戏扣弹药时修改的是 `hiddenValue`（加密值），但 `fakeValue` 是同步更新的。我们锁定 `fakeValue` 后，游戏在扣减 `hiddenValue` 后会把 `fakeValue` 同步回来 → 我们每次写回的原始值等于告诉游戏"弹药没变"。因为写的是加密值而不是裸数字，不触发校验。

**大白话：** 就像超市的防盗磁扣——你不能直接把它砸了（写 9999），你要用正确的消磁器（原始加密值）才能让游戏以为弹药一直没少。

---

## 坑2：房间切换闪退 —— 旧对象没清理

### 问题的本质

游戏用对象池管理武器实例：

```
房间 A：创建 Weapon_1 @ 地址 0x12345600（你的主武器）
↓ 你切房间
房间 A 被销毁：Weapon_1 @ 0x12345600 → 内存被回收（free）
房间 B 创建：Weapon_1 @ 0x12345600 → 可能被其他对象复用
```

如果你的脚本还记着 `0x12345600` 这个地址，定时器还在往里写数据——**写到了已释放的内存**。

### 后果
- 最好的情况：写入被释放的内存 → Access Violation → 游戏闪退
- 最坏的情况：地址被其他对象复用了 → 写坏了其他对象 → 游戏状态损坏 → 晚几秒才闪退（更难排查）

### V5/V6 的解决方案

**Hook 三个函数，在房间切换的瞬间清空所有记录：**

```javascript
// 函数1: GameManager.GameRoundEnd
//   → 任何模式的回合结束都会调
// 函数2: ModeBase.OnStartNewGameRound
//   → 普通模式（团队/个人）新回合
// 函数3: ModeBase_Nano.OnStartNewGameRound
//   → 生化模式新回合

function clearAll() {
    wpnData = {};    // 清空玩家武器记录
    notMine = {};    // 清空 Bot 黑名单
}

Interceptor.attach(GameRoundEnd, { onEnter: clearAll });
Interceptor.attach(OnStartNewGameRound, { onEnter: clearAll });
Interceptor.attach(NanoOnStartNewGameRound, { onEnter: clearAll });
```

**防止闪退的完整保险链：**
```
① GameRoundEnd 触发 → 清空 wpnData（主保险）
② OnStartNewGameRound 触发 → 清空 wpnData（双重保险）
③ 定时器写入失败 → 自动从 wpnData 删除该条目（兜底保险）
```

---

## 坑3：掉帧卡顿 —— Hook 太频繁

### 每帧 Hook 是帧率杀手

**V6（我的第一个优化尝试）的 Hook 列表：**
```
set_addYaw       ← property setter（任何后座力赋值都触发）
set_addPitch      ← property setter（同上）
OnGunShot         ← 开枪时触发（每秒 3-5 次，OK）
UpdateAddYaw      ← 每帧调用！每个实体每帧都调！
UpdateAddPitch    ← 每帧调用！每个实体每帧都调！
```

**数学：**
```
16 个 Bot × 60 FPS = 960 次/秒 调用 UpdateAddYaw
每次调用 = Process.findRangeByAddress + 4 × writeFloat
960 次/秒 × 5 个操作 = 4800 个操作/秒 → 帧率从 60 掉到 10
```

### V7 的修复：只 Hook 触发频率低的函数

```
OnGunShot → 每秒 3-5 次（只有你开枪才触发）
GameRoundEnd → 每次切房间触发一次
OnStartNewGameRound → 同上
```

**判断一个函数是否适合 Hook 的经验法则：**

| 函数类型 | 触发频率 | 适合 Hook？ |
|---------|---------|------------|
| per-frame（Update/每帧调用） | 60次/秒 × 实体数 | ❌ 绝对不能 |
| 开火/换弹事件 | 3-5次/秒 | ✅ 可以 |
| 回合事件 | 每几分钟一次 | ✅ 完美 |
| 定时器 | 可控 | ✅ 但要降频 |

---

## 坑4：玩家识别 —— 不要管 Bot 的枪

### 不识别玩家的灾难

**V1-V4 的做法：** 不管是谁的枪，只要是枪就锁定弹药。

**实际数量：**
```
你的枪：1-2 把（主武器 + 副武器）
Bot 的枪：16 个 Bot × 每人 1-2 把 = 16-32 把
```

**后果：** 你的定时器在给 30+ 把枪写弹药 → 每秒几十次内存写入 → 卡死。

### V5 的解决方案：调用游戏自己的方法

```javascript
// 使用游戏 C# 层的 Weapon.get_isMyWeapon 方法
var isMyWeapon = new NativeFunction(
    base.add(0xB6E1D0),  // Weapon$$get_isMyWeapon
    "bool", ["pointer", "pointer"]
);

// 判断逻辑（C# 侧）：
// Weapon → owner（继承自 Model 的 owner 属性）
// → 比较 owner == GameManager.myPlayer
// → 返回 true/false
```

**武器继承链（从 C# dump）：**
```
Weapon → CFAnimator → Model → RecyclableObject → MonoBehaviour
                          ↑
                    owner: Player  ← 从这取出 owner 和 myPlayer 比较
```

### V6 的进一步优化：黑名单缓存

```javascript
var notMine = {};  // { 指针字符串 → true }

// 第一次见到这个指针 → 调 isMyWeapon 判断
if (checkIsMyWeapon(wpn)) {
    wpnData[key] = ...;  // 玩家武器 → 加入白名单
} else {
    notMine[key] = true; // Bot 武器 → 加入黑名单
}

// 下次再见到：
if (wpnData[key]) return;   // 已知玩家 → 跳过（定时器会锁）
if (notMine[key]) return;   // 已知 Bot → 直接跳过
```

**效果：**
- Bot 第一次开火 → 调 `isMyWeapon`（慢操作，约 1 微秒）
- Bot 第二次开火 → 查 `notMine` 字典（纯 JS 字符串查找，约 0.05 微秒）
- 从第二次开始，快 20 倍

---

## 坑5：触发时机 —— 热路径不能有慢操作

### 什么是"热路径"？

就是**被调用次数非常多的代码路径**。

```
冷路径：OnStartNewGameRound → 每分钟 1 次（放什么都行）
热路径：fire hook → 每秒 30-60 次（只能放快操作）
```

### 慢操作排行榜

| 操作 | 耗时 | 说明 |
|------|------|------|
| `ptr.toString()` | ~0.02 μs | JS 字符串操作，极快 ✅ |
| `obj[key]` 字典查找 | ~0.05 μs | JS 引擎优化很好 ✅ |
| `Process.findRangeByAddress()` | ~5-50 μs | **系统调用，很慢** ❌ |
| `NativeFunction` 调用 | ~1-5 μs | 跨进程调用，中等 ⚠️ |
| `readPointer()` + `writeInt()` | ~1-3 μs | 内存访问，中等 ⚠️ |
| `console.log()` | ~100-500 μs | **I/O 操作，超慢** ❌ |

### V6 的热路径设计

```javascript
// fire hook 每秒被调用 40+ 次（含 Bot 开火）

onEnter: function(args) {
    var k = wpn.toString();     // 0.02μs ← 快
    if (wpnData[k]) return;     // 0.05μs ← 快（命中率最高）
    if (notMine[k]) return;     // 0.05μs ← 快（命中率第二高）

    // 下面的慢操作只在"首次见到这个指针"时才执行一次
    if (!readable(wpn)) return;          // 5μs ← 慢，但只执行一次
    if (checkIsMyWeapon(wpn)) { ... }    // 3μs ← 慢，但只执行一次
}
```

**关键设计原则：**
> 把慢操作推到"首次执行"路径，后续都是快操作。

---

## 坑6：武器数量限制 —— 为什么第5把枪无效

### V5 的 Bug

```javascript
var MAX_WPN = 4;

// fire hook 里：
if (Object.keys(wpnData).length >= MAX_WPN) return;  // ← 这行是问题
```

**为什么 V5「只有前几把枪有效果」：**

```
你的第一把枪：AK47 @ 0xAAAA → wpnData["0xAAAA"] = ...  长度=1  ✅
拾取第二把：  AWP @ 0xBBBB  → wpnData["0xBBBB"] = ...  长度=2  ✅
死亡复活：    新 AK47 @ 0xCCCC → wpnData 还存着 0xAAAA（旧地址已失效）
             → wpnData["0xCCCC"] = ... 长度=3
切枪再切回来：新 AK47 @ 0xDDDD → wpnData["0xDDDD"] = ... 长度=4
捡地上的枪：  新步枪 @ 0xEEEE → 长度=4 >= MAX_WPN → return！❌ 无效！
```

**游戏频繁创建新武器实例的原因：**
- 切枪 = 旧实例被回收，新实例被创建
- 死亡复活 = 旧实例被回收，新实例被创建
- 捡地上的枪 = 新实例
- 生化模式变身 = 新实例

### V6 的修复

```javascript
// 移除 MAX_WPN 限制
// 依赖定时器自动清理失效引用（写入失败 → delete）
// 依赖 GameRoundEnd 在切房间时清空
```

**为什么现在不怕数量爆炸：**
```
① 切房间 → 全部清空（回到 0）
② 同一房间内 → 最多 2 把活跃武器 + 可能 1-2 个残留（定时器会清理）
③ 最坏情况 4-5 条记录 → 完全不是问题
```

---

## 最终方案（V6）完整架构

```
┌────────────────────────────────────────────────────┐
│                    无限子弹 V6                       │
├────────────────────────────────────────────────────┤
│                                                    │
│  ┌──────────────┐   ┌──────────────┐              │
│  │ 4个 fire hook │   │ 3个 room hook │              │
│  │ (发现新武器)  │   │ (切房间清理)  │              │
│  └──────┬───────┘   └──────┬───────┘              │
│         │                  │                       │
│         ▼                  ▼                       │
│  ┌─────────────────────────────────┐              │
│  │           状态存储                │              │
│  │  wpnData: { key→{ptr,cv,av} }   │ ← 玩家武器   │
│  │  notMine: { key→true }          │ ← Bot 黑名单  │
│  └─────────────┬───────────────────┘              │
│                │                                    │
│                ▼                                    │
│  ┌─────────────────────────────────┐              │
│  │      定时器 (每 2000ms)          │              │
│  │  遍历 wpnData → 写回加密弹药值   │              │
│  │  写入失败 → 自动删除引用         │              │
│  └─────────────────────────────────┘              │
│                                                    │
│  性能:      每秒 < 5 次 Frida 操作（零卡顿）       │
│  防闪退:    GameRoundEnd → 清空引用                 │
│  玩家识别:  黑名单缓存 + isMyWeapon                 │
└────────────────────────────────────────────────────┘
```

---

## Hook 函数地址速查表

| 函数 | RVA（十六进制） | 用途 |
|------|----------------|------|
| `Weapon$$get_isMyWeapon` | `0xB6E1D0` | 判断武器是否属于玩家 |
| `GameManager$$GameRoundEnd` | `0xAFAA40` | 任何模式回合结束 |
| `ModeBase$$OnStartNewGameRound` | `0xAF5B30` | 普通模式新回合 |
| `ModeBase_Nano$$OnStartNewGameRound` | `0xAF15D0` | 生化模式新回合 |
| 开火函数1 | `0xB67AF0` | 玩家开火 |
| 开火函数2 | `0xB62730` | 玩家开火 |
| 开火函数3 | `0xB621F0` | 玩家开火（NoCheck） |
| 开火函数4 | `0xAEA6B0` | 武器初始化/开火 |

### 字段偏移速查

| 偏移 | 字段 | 说明 |
|------|------|------|
| `Weapon + 0x68` | `data` | 指向 WeaponData 的指针 |
| `Weapon + 0xF4` | → `ammoData` | 指向 WPN_Gun.AmmoData 的指针 |
| `AmmoData + 0x0C` | `clip.fakeValue` | 弹夹伪装值 |
| `AmmoData + 0x20` | `ammo.fakeValue` | 备弹伪装值 |

---

## 版本演变对比

| 版本 | 玩家识别 | 定时器频率 | 切房间清理 | 弹药写入 | 效果 |
|------|---------|-----------|-----------|---------|------|
| V1 | ❌ 所有武器 | 50ms | ❌ | 9999 | 10发卡死 |
| V2 | ❌ 所有武器 | 500ms | ⚠️ 仅清理失效 | 9999 | 十几发卡死 |
| V3 | ❌ 所有武器 | 150ms | ⚠️ 仅清理失效 | 原始值 | 卡到动不了 |
| V4 | ❌ 所有武器 | 250ms | ⚠️ 仅清理失效 | 9999 | 掉帧严重 |
| V5 | ✅ isMyWeapon | 500ms | ✅ GameRoundEnd | 原始值 | 略微掉帧 |
| **V6** | **✅ 黑名单缓存** | **2000ms** | **✅ 三重清理** | **原始值** | **零卡顿** |

---

> **核心心法：写越少代码，做越少操作，游戏越流畅。**
> 
> 不要因为"感觉应该做"就加一堆保护——每多加一个 `Process.findRangeByAddress`，帧率就少一点。
> 把验证放到"变化时"（切房间、新武器），而不是"高频时"（开火、每帧）。
