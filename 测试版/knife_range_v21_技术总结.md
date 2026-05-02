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

## 二、闪退原因分析（通过日志逐一排除）

### 闪退 1：v12 — args[0] 写坏武器对象

**现象**：挥刀 ~8 次后 "Process terminated"

**根因**：

```javascript
// v12 错误写法
onEnter:  this.retbuf = args[0];   // 以为是 retbuf
onLeave:  this.retbuf.add(0x4).writeFloat(...);  // 写到武器对象内部
```

Frida 在某些版本会剥离 IL2CPP 32-bit struct return 的隐藏 retbuf 参数，导致 `args[0]` 实际是 `WPN_Knife*`（this 指针）。向 `this + 0x4` 反复写入浮点数，逐步损坏武器对象内部字段，积累到 ~8 次后对象崩溃。

**修复**：用 `retval`（Frida 保证指向返回结构体）替代 `args[0]`。

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

**修复**：v19 改用 replace + 纯指针比较，但在第一次 onLeave 中仍有一次 `isMyPlayerFn` 调用（用于捕获 myPlayer），导致 10 次后仍崩。

**最终修复**（v21）：将 `isMyPlayer` 调用完全移出 attach 的回调，放到 replace 的 NativeCallback 中（游戏线程安全）。attach 的 onLeave 只做 `owner.equals(myPlayer)` 纯指针比较。

### 闪退 4：v12/v14/v15/v18/v19 — 双 Hook 竞态

**现象**：所有带基类 Hook（`Weapon.GetKnifeAttackData` 0xB79008）的版本都闪退

**根因**（v20 验证）：

```
[近战] retval=0xceea10  ← 同一个缓冲区
[近战] retval区域: base=0xcd4000 size=180224 prot=rw-
```

WPN_Knife 和 Weapon 两个 Hook 的 `onLeave` 共用同一个 retval 缓冲区（0xceea10）。两个 Hook 同时在该内存上读写 → 竞态条件 → 内存损坏 → 闪退。

**v20 验证**：去掉基类 Hook，只保留 WPN_Knife Hook，零崩溃。

**修复**：只保留一个主 Hook（0xB63EC0），去掉基类兜底 Hook。

---

## 三、闪退原因汇总

| 版本 | 崩溃点 | 根因 | 修复 |
|------|--------|------|------|
| v12 | ~8刀后 | `args[0]` 写坏了 WPN_Knife 对象 | 用 `retval` |
| v14 | 初始化期间 | onEnter 调 `isMyWeapon`，武器未就绪 | 不在 onEnter 调 NativeFunction |
| v17 | 无效果 | `Interceptor.replace` 签名不匹配，函数未被调用 | 回到 `attach` |
| v18 | ~12刀后 | onLeave 中调 `isMyPlayer`，跨线程 | 移到 replace 中 |
| v19 | ~10刀后 | onLeave 中一次 `isMyPlayer` 调用 + 双 Hook 竞态 | replace捕获 + 单Hook |
| v20 | 零崩溃 | ✅ 单Hook + 纯指针比较 | — |

---

## 四、全模式应用方法

### Hook 目标

| 函数 | RVA | 说明 |
|------|-----|------|
| `WPN_Knife.GetKnifeAttackData` | 0xB63EC0 | 所有近战武器的攻击数据获取入口 |
| `PlayerWeapons.get_KnifeSpeed` | 0xB170A0 | 每次挥刀必调，用于安全捕获 myPlayer |

### 为什么全模式生效

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
