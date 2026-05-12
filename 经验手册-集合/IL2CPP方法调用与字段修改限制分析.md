# IL2CPP 方法调用与字段修改限制分析

> 基于 CE 修改器 .NET Info 和 Frida 逆向实践，整理 IL2CPP 游戏中**哪些方法能/不能直接调用**、**哪些字段能/不能直接修改**，以及各自的底层原因。

---

## 一、方法调用：能调用 vs 不能调用

### 1.1 能直接调用的方法

#### 特征：只读 + 无副作用 + 无外部依赖

| 特征 | 说明 |
|------|------|
| 纯读取 | 方法内部只读字段值，不写入任何字段 |
| 简单计算 | 只做比较/运算，返回 bool/int/float 等基本类型 |
| 无事件回调 | 不触发 `Action`、`SubscribeableProperty` 的 listener |
| 不依赖 Unity API | 不调用 `GetComponent`、`Transform`、`GameObject` 等 |
| 不触发 GC 分配 | 不 `new` 对象，不产生字符串拼接等堆分配 |
| 不使用 MethodInfo* | IL2CPP 隐藏的第二个参数 `MethodInfo*` 传 `null` 无影响 |
| 线程无关 | 任何线程调用结果一致，不关心调用上下文 |

#### 典型示例

```csharp
// HealthData.get_isDead() — RVA: 0xAE4830
// 内部逻辑：return currentHealth == 0;
// ✅ 只读 + 比较 + 返回bool，零副作用

// HealthData.get_isMaxHP() — RVA: 0xAE48B0
// 内部逻辑：return currentHealth >= maxHealth;
// ✅ 只读 + 比较 + 返回bool，零副作用

// HealthData.get_rate() — RVA: 0xAE4950
// 内部逻辑：return currentHealth / maxHealth;
// ✅ 只读 + 除法 + 返回float，零副作用
```

#### CE 中调用方式

```
1. 在 .NET Info 中找到方法
2. 直接双击/Invoke，传入实例指针
3. 即可获取返回值
```

---

### 1.2 不能直接调用的方法

#### 共有特征：有写入 / 有副作用 / 有依赖链

| 特征 | 说明 |
|------|------|
| 写入字段 | 方法内部修改了实例字段，打破只读安全区 |
| 写入加密字段 | 修改 `ObscuredInt`/`ObscuredFloat` 等反作弊类型 |
| 触发事件回调 | 调用 `Action`/`listener`/`SubscribeableProperty.set_value` |
| 依赖 Unity 主线程 | 内部访问 Unity API（UI、Transform、GameObject 等） |
| 触发网络同步 | 修改后通知服务端，可能被反作弊检测 |
| 触发 GC 分配 | `new` 对象、字符串操作，可能引发 GC 冲突 |
| 使用 MethodInfo* | 方法内部读取了 MethodInfo 参数，传 null 会崩溃 |

---

### 1.3 不能调用的方法分类详解

#### 类型 A：写入加密字段（Obscured 系列）

**代表方法**：`HealthData.ClearTempHealth()` — RVA: 0xAE4400

```csharp
public void ClearTempHealth() {
    tempHealth = 0;  // ObscuredInt 赋值，触发加密写入
}
```

**ObscuredInt 内存布局**：

```
偏移    字段               类型      说明
0x00    currentCryptoKey   int       当前加密密钥
0x04    hiddenValue        int       加密后的真实值（XOR结果）
0x08    inited             bool      是否已初始化
0x0C    fakeValue          int       伪值（欺骗CE扫描）
0x10    fakeValueActive    bool      伪值是否激活
```

**为什么不能直接调用**：

1. 写入 `hiddenValue` 时需要与 `currentCryptoKey` 做 XOR 运算
2. 必须同步更新 `fakeValue` 和 `fakeValueActive`
3. 如果游戏线程同时在读取，加密状态损坏 → 崩溃
4. `ObscuredInt` 的隐式赋值运算符内部会调用 `ApplyNewCryptoKey()`，更换密钥

**同类型方法**：

| 方法 | RVA | 写入的加密字段 |
|------|-----|---------------|
| `HealthData.ClearTempHealth()` | 0xAE4400 | tempHealth (ObscuredInt) |
| `HealthData.AddTempHealth(int)` | 0xAE4360 | tempHealth (ObscuredInt) |
| `HealthData.Hurt(int)` | 0xAE45B0 | currentHealth (ObscuredInt) |
| `HealthData.Heal(int)` | 0xAE44F0 | currentHealth (ObscuredInt) |
| `HealthData.Heal()` | 0xAE44D0 | currentHealth (ObscuredInt) |
| `HealthData.SetHealthMax(int, bool)` | 0xAE4720 | currentHealth + maxHealth |
| `HealthData.AddHealthMax(int, bool)` | 0xAE4260 | maxHealth + currentHealth |

---

#### 类型 B：触发 SubscribeableProperty 事件链

**代表方法**：`Entity.set_team(Team)` — RVA: 0x1E00C0

```csharp
// PlayerData 中的 SubscribeableProperty<int> kill — 偏移 0x4C
public class SubscribeableProperty<T1> {
    private T1 value;                    // 0x0  实际值
    private Action<T1, T1> listener;     // 0x0  变更回调（旧值, 新值）
}
```

**为什么不能直接调用**：

1. `set_value` 内部会调用 `listener?.Invoke(oldValue, newValue)`
2. listener 可能指向 UI 更新代码（非主线程访问 Unity → 崩溃）
3. listener 可能触发网络同步（服务端校验不通过 → 回弹/封号）
4. 链式反应：一个 set 可能触发多个 listener，不可控

**涉及 SubscribeableProperty 的字段**：

| 类 | 字段 | 类型 | 偏移 |
|----|------|------|------|
| PlayerData | kill | SubscribeableProperty\<int\> | 0x4C |
| PlayerData | death | SubscribeableProperty\<int\> | 0x50 |
| PlayerData | survival | SubscribeableProperty\<int\> | 0x54 |
| PlayerData | score | SubscribeableProperty\<int\> | 0x58 |
| PlayerData | aceSign | SubscribeableProperty\<AceSign\> | 0x5C |
| PlayerData | nanoRole | SubscribeableProperty\<NanoRole\> | 0x60 |
| Nano4T_Data | humanLayer | SubscribeableProperty\<int\> | 0x8 |
| Nano4T_Data | nanoLayer | SubscribeableProperty\<int\> | 0xC |
| Nano4T_Data | pickUpBoxCount | SubscribeableProperty\<int\> | 0x10 |

---

#### 类型 C：触发 PropertyModifier 委托链

**代表方法**：任何修改 `Modifier_` 字段的方法

```csharp
// PlayerWeapons.Modifier_ReloadSpeed — 偏移 0x3C
// PlayerWeapons.Modifier_KnifeRange — 偏移 0x40
// PlayerWeapons.Modifier_KnifeSpeed — 偏移 0x44
// Player.Modifier_MoveSpeedRatio — 偏移 0x8C

public class PropertyModifier {
    public PlayerRefFloat modifier;  // 0x8  委托，指向计算逻辑
}

public sealed class PlayerRefFloat : MulticastDelegate {
    public virtual void Invoke(Player player, ref float value);
}
```

**为什么不能直接调用**：

1. `PropertyModifier` 内部持有 `PlayerRefFloat` 委托
2. 委托是 `MulticastDelegate`，可能指向多个回调方法
3. 修改值时委托链被触发，回调中可能访问 Unity API
4. 委托目标方法可能校验参数合法性，非法值导致异常

---

#### 类型 D：依赖 Unity 主线程的方法

**代表方法**：涉及 UI 更新、动画、物理、渲染的方法

| 操作 | 线程要求 | 崩溃原因 |
|------|---------|---------|
| 修改 Transform 位置 | 主线程 | Unity 内部检查 `currentThread == mainThread` |
| 访问 GameObject | 主线程 | GameObject 非主线程操作抛异常 |
| 修改 Animator | 主线程 | 动画系统内部有线程检查 |
| UI 更新 | 主线程 | Canvas/Text/Image 非主线程操作崩溃 |
| Instantiate/Destroy | 主线程 | 对象生命周期管理线程不安全 |
| 协程相关 | 主线程 | Coroutine 只能在主线程启动/停止 |

---

#### 类型 E：涉及网络同步的方法

**代表方法**：修改血量、位置、武器状态等

| 修改内容 | 服务端校验 | 后果 |
|---------|-----------|------|
| 血量 (HealthData) | ✅ 服务端校验 | 回弹/无效/封号 |
| 位置 (Transform) | ✅ 服务端校验 | 回弹/拉回 |
| 武器切换 | ✅ 服务端校验 | 切换失败 |
| 弹药数量 | ✅ 服务端校验 | 无限弹药可能被检测 |
| 射速 | ⚠️ 部分校验 | 可能触发异常数据上报 |

---

### 1.4 方法调用安全等级总表

| 安全等级 | 条件 | 示例 | CE直接调用 |
|---------|------|------|-----------|
| 🟢 安全 | 只读 + 简单返回 | `get_isDead()`, `get_isMaxHP()`, `get_rate()` | ✅ 可以 |
| 🟡 有风险 | 只读但访问复杂对象 | `get_nickName()`, `get_level()` | ⚠️ 可能成功 |
| 🟠 危险 | 写入普通字段 | `set_team()`, `set_isInvincible()` | ❌ 可能崩溃 |
| 🔴 极危险 | 写入加密字段 + 事件链 | `ClearTempHealth()`, `Hurt()`, `Heal()` | ❌ 大概率崩溃 |
| ⛔ 禁止 | 网络同步 + 反作弊 | 涉及服务端校验的修改方法 | ❌ 崩溃+封号 |

---

## 二、字段修改：能修改 vs 不能修改

### 2.1 能直接修改的字段

#### 特征：普通类型 + 无回调 + 无服务端校验

| 特征 | 说明 |
|------|------|
| 普通值类型 | `int`、`float`、`bool` 等非加密类型 |
| 无 setter 回调 | 属性只有 `get`，没有 `set`，或 `set` 不触发 listener |
| 本地生效 | 修改后本地立即生效，不依赖服务端确认 |
| 无联动逻辑 | 修改此字段不会触发其他字段的级联更新 |

#### 典型示例

| 类 | 字段 | 偏移 | 类型 | 说明 |
|----|------|------|------|------|
| Entity | baseMoveSpeed | 0x0C | float | 基础移动速度 |
| Entity | speedPenalty | 0x10 | float | 速度惩罚 |
| Entity | damageRate | 0x14 | float | 伤害倍率 |
| Entity | isInvincible | 0x18 | bool | 无敌状态 |
| WeaponData_Gun | shotsPerMinute | 0xCC | float | 射速 |
| WeaponData_Gun | fireAnimMultiplier | 0xD0 | float | 射击动画倍率 |
| WeaponData_Gun | reloadAnimRatio | 0xD4 | float | 换弹动画比率 |
| WeaponData_Gun | clip | 0xB8 | int | 弹匣容量 |
| WeaponData_Gun | ammo | 0xBC | int | 备弹数量 |

---

### 2.2 不能直接修改的字段

---

#### 类型 A：Obscured 加密字段（写入后被校验覆盖）

**特征**：字段类型为 `ObscuredInt`、`ObscuredFloat`、`ObscuredBool`

**ObscuredInt 内部结构**：

```
偏移    字段               类型      说明
0x00    currentCryptoKey   int       加密密钥（静态+实例各一份）
0x04    hiddenValue        int       加密值 = 真实值 XOR currentCryptoKey
0x08    inited             bool      初始化标记
0x0C    fakeValue          int       伪值（CE扫描到的是这个）
0x10    fakeValueActive    bool      伪值是否激活
```

**为什么不能直接修改**：

1. **直接写 hiddenValue**：下次读取时 `InternalDecrypt()` 用 `currentCryptoKey` 解密，得到的是 XOR 后的乱码值
2. **同时写 hiddenValue + currentCryptoKey**：`fakeValue` 不一致，`fakeValueActive` 检测到不匹配可能触发反作弊
3. **游戏线程持续读写**：你写的同时游戏也在读，加密状态瞬间损坏
4. **ObscuredInt 的 setter 会换密钥**：每次赋值都调用 `ApplyNewCryptoKey()` 生成新密钥，外部写入无法同步

**正确修改方式**：

```javascript
// 方式1：Hook 加密类型的隐式转换运算符
// ObscuredInt.op_Implicit(ObscuredInt) → int（读取时）
// ObscuredInt.op_Implicit(int) → ObscuredInt（写入时）

// 方式2：Hook 使用该字段的方法，在方法返回前修改返回值
// 例如 Hook get_currentHealth() 返回你想要的值

// 方式3：直接修改 hiddenValue，但要同步计算 XOR
var key = healthData.add(0x30).readS32();          // currentCryptoKey
var desiredValue = 999;
var encrypted = desiredValue ^ key;                 // XOR 加密
healthData.add(0x30 + 0x04).writeS32(encrypted);   // hiddenValue
healthData.add(0x30 + 0x0C).writeS32(desiredValue); // fakeValue
```

**涉及的加密字段**：

| 类 | 字段 | 偏移 | 加密类型 |
|----|------|------|---------|
| HealthData | currentHealth | 0x08 | ObscuredInt |
| HealthData | maxHealth | 0x1C | ObscuredInt |
| HealthData | tempHealth | 0x30 | ObscuredInt |

---

#### 类型 B：只读属性（无 setter，配置文件写死）

**特征**：dump.cs 中属性声明为 `{ get; }`，没有 `{ set; }`

**典型示例**：

```csharp
// Player 中的只读属性（来自 ClientData 配置）
public string nickName { get; }      // 昵称，登录时从服务端获取
public int level { get; }            // 等级，服务端数据
public int vipLevel { get; }         // VIP等级，服务端数据
```

**为什么不能修改**：

1. **无 setter 方法**：C# 编译器不为 `{ get; }` 生成 `set_` 方法
2. **后备字段是 private**：`[CompilerGenerated] private T <nickName>k__BackingField`，外部无法直接访问
3. **数据来源是服务端**：昵称、等级等在登录时从服务端下发，本地改了也无效
4. **即使改了后备字段**：下次服务端推送数据时会被覆盖回原值

**只读属性一览**：

| 类 | 属性 | 类型 | 数据来源 |
|----|------|------|---------|
| Player | nickName | string | 服务端/配置 |
| Player | level | int | 服务端 |
| Player | vipLevel | int | 服务端 |
| Entity | isDead | bool | 由 currentHealth 计算 |
| Entity | isBlackList | bool | 由 team 字段计算 |
| Entity | isGlobalRisk | bool | 由 team 字段计算 |
| HealthData | rate | float | 由 currentHealth/maxHealth 计算 |
| HealthData | isDead | bool | 由 currentHealth == 0 计算 |
| HealthData | isMaxHP | bool | 由 currentHealth >= maxHealth 计算 |

---

#### 类型 C：SubscribeableProperty 包装字段（写入触发事件链）

**特征**：字段类型为 `SubscribeableProperty<T>`

**SubscribeableProperty 内部结构**：

```
偏移    字段               类型                    说明
0x00    <value>k__BackingField  T1                 实际值
0x04    listener           Action<T1, T1>         变更回调（旧值→新值）
```

**为什么不能直接修改**：

1. 直接写 `value` 字段 → `listener` 不会被调用 → UI 不更新 → 状态不一致
2. 调用 `set_value()` → `listener` 被调用 → 可能触发 Unity API → 非主线程崩溃
3. `listener` 可能包含网络同步逻辑 → 服务端校验失败 → 回弹

**涉及的字段**：

| 类 | 字段 | 泛型参数 | 偏移 |
|----|------|---------|------|
| PlayerData | kill | int | 0x4C |
| PlayerData | death | int | 0x50 |
| PlayerData | survival | int | 0x54 |
| PlayerData | score | int | 0x58 |
| PlayerData | aceSign | AceSign | 0x5C |
| PlayerData | nanoRole | NanoRole | 0x60 |
| Nano4T_Data | humanLayer | int | 0x8 |
| Nano4T_Data | nanoLayer | int | 0xC |
| Nano4T_Data | pickUpBoxCount | int | 0x10 |

---

#### 类型 D：PropertyModifier 委托字段（修改被委托计算覆盖）

**特征**：字段类型为 `PropertyModifier`，值由委托动态计算

```csharp
public class PropertyModifier {
    public PlayerRefFloat modifier;  // 0x8  委托
    public float Get(Player player) {
        // 调用委托获取最终值
    }
}
```

**为什么不能直接修改**：

1. `PropertyModifier` 本身不存储值，它存储的是**计算委托**
2. 每次读取都通过 `Get(player)` 调用委托重新计算
3. 你无法"写入"一个委托计算的结果，下次读取时又被重新计算覆盖
4. 要修改效果，必须 Hook `Get()` 方法的返回值

**涉及的 PropertyModifier 字段**：

| 类 | 字段 | 偏移 | 效果 |
|----|------|------|------|
| Player | Modifier_MoveSpeedRatio | 0x8C | 移动速度倍率 |
| PlayerWeapons | Modifier_ReloadSpeed | 0x3C | 换弹速度 |
| PlayerWeapons | Modifier_KnifeRange | 0x40 | 刀攻击范围 |
| PlayerWeapons | Modifier_KnifeSpeed | 0x44 | 刀攻击速度 |

---

#### 类型 E：服务端权威字段（本地修改无效/被回弹）

**特征**：关键游戏状态由服务端校验，本地修改后会被服务端纠正

| 字段类型 | 服务端校验 | 修改后果 |
|---------|-----------|---------|
| 血量 | ✅ 强校验 | 修改后立即回弹，可能封号 |
| 位置 | ✅ 强校验 | 修改后拉回原位 |
| 金币/货币 | ✅ 强校验 | 仅本地显示变化，实际不变 |
| 等级/VIP | ✅ 强校验 | 仅本地显示变化，实际不变 |
| 弹药 | ⚠️ 部分校验 | 部分模式有效，部分无效 |
| 射速 | ⚠️ 弱校验 | 通常本地生效，但异常数据可能被上报 |

---

#### 类型 F：string 引用字段（直接写入导致内存损坏）

**特征**：字段类型为 `string`（IL2CPP 中的 `System.String`）

**IL2CPP String 内存布局**：

```
偏移    字段               类型      说明
0x00    Il2CppObject header  ptr      类元数据指针
0x08:   length              int      字符串长度（负4偏移读取）
0x0C:   chars[0]            char     UTF-16 字符数据起始
```

**为什么不能直接修改**：

1. `string` 在 C# 中是不可变的，修改长度字段可能导致 GC 异常
2. 写入比原字符串更长的内容 → 越界写入 → 内存损坏
3. 写入比原字符串更短的内容 → 长度字段不匹配 → 读取时崩溃
4. IL2CPP 的字符串可能被 intern（字符串池化），修改一个会影响所有引用

---

### 2.3 字段修改安全等级总表

| 安全等级 | 字段类型 | 修改方式 | 示例 |
|---------|---------|---------|------|
| 🟢 安全 | 普通 int/float/bool | 直接写内存 | baseMoveSpeed, shotsPerMinute |
| 🟡 需技巧 | ObscuredInt/Float | XOR 加密后写入 | currentHealth, maxHealth |
| 🟠 有风险 | SubscribeableProperty | Hook getter 返回值 | kill, death, score |
| 🔴 基本无效 | 只读属性（服务端数据） | 无法修改 | nickName, level, vipLevel |
| 🔴 基本无效 | PropertyModifier | Hook Get() 返回值 | Modifier_ReloadSpeed |
| ⛔ 禁止 | string 引用 | 不可直接改 | nickName, orignalCharacterName |
| ⛔ 禁止 | 服务端权威数据 | 修改即回弹 | 血量(网络模式), 位置, 货币 |

---

## 三、实例地址 vs 方法地址：为什么拿到实例不能直接调方法

### 3.1 核心概念

在 IL2CPP 中，**对象实例**和**方法代码**是完全分离的：

```
对象实例（堆内存）              方法代码（GameAssembly.dll）
┌────────────────────┐         ┌──────────────────────────┐
│ Il2CppObject header│──→ 类元数据  │ get_isDead() @ 0xAE4830 │
│ currentHealth      │         │ get_isMaxHP() @ 0xAE48B0 │
│ maxHealth          │         │ ClearTempHealth() @ 0xAE4400│
│ tempHealth         │         │ Hurt() @ 0xAE45B0        │
│ invinsibleEndTime  │         └──────────────────────────┘
└────────────────────┘
  ↑ 你拿到的 0x352984B0       ↑ 需要从 dump.cs 查 RVA
  只有数据，没有方法指针
```

### 3.2 关键区别

| 操作 | 需要什么 | 从实例地址能获取吗 |
|------|---------|-----------------|
| 读字段 | 实例地址 + 偏移 | ✅ 可以 |
| 写字段 | 实例地址 + 偏移 | ✅ 可以（但可能被覆盖） |
| 调方法 | 实例地址 + **方法 RVA** | ❌ 实例中不存储方法地址 |

### 3.3 IL2CPP 方法调用约定

每个 IL2CPP 方法的原生签名：

```c
// C# 中的: public void ClearTempHealth()
// IL2CPP 编译后:
void HealthData_ClearTempHealth(HealthData* this, MethodInfo* method);
```

- 第1个参数：`this` 指针（实例地址）
- 第2个参数：`MethodInfo*`（IL2CPP 元数据，通常传 NULL 即可）

### 3.4 Frida 中正确调用方法的方式

```javascript
var base = Process.findModuleByName("GameAssembly.dll").base;

// 1. 通过 RVA 找到方法地址
var RVA_CLEAR_TEMP_HEALTH = 0xAE4400;
var clearTempHealth = new NativeFunction(
    base.add(RVA_CLEAR_TEMP_HEALTH),
    'void',
    ['pointer', 'pointer']  // (this, MethodInfo*)
);

// 2. 传入实例地址调用
var healthDataPtr = inst.healthData;  // 你拿到的 0x352984B0
clearTempHealth(healthDataPtr, ptr(0));
```

### 3.5 线程安全要求

| 调用场景 | 线程 | 安全性 |
|---------|------|--------|
| `Interceptor.replace` 回调 | 游戏主线程 | ✅ 安全 |
| `Interceptor.attach` onEnter/onLeave | 游戏主线程 | ✅ 安全 |
| `setTimeout` / `rpc` 回调 | Frida 线程 | ❌ 可能崩溃 |
| CE .NET Info 调用 | CE 线程 | ⚠️ 只读方法安全 |

---

## 四、快速判断指南

### 4.1 方法能否直接调用 — 判断流程

```
方法是否只读字段？
├── 否 → ❌ 不能直接调用（有写入风险）
│   ├── 写入 ObscuredInt/Float？ → 🔴 加密字段写入，极危险
│   ├── 写入普通字段？ → 🟠 可能触发事件链
│   └── 触发网络同步？ → ⛔ 封号风险
│
└── 是 → 方法是否依赖 Unity API？
    ├── 是 → ❌ 非主线程调用崩溃
    └── 否 → ✅ 可以安全调用
```

### 4.2 字段能否直接修改 — 判断流程

```
字段类型是什么？
├── ObscuredInt/Float/Bool → 🟡 需要 XOR 加密写入
├── SubscribeableProperty<T> → 🟠 需 Hook getter，不能直接写
├── PropertyModifier → 🔴 需 Hook Get()，不能直接写
├── string → 🔴 不能直接写（不可变+可能越界）
├── 普通 int/float/bool
│   ├── 属性有 set？ → 🟢 可以修改
│   └── 属性只有 get？ → 🔴 只读，改了也被覆盖
└── 服务端权威数据 → ⛔ 修改无效或封号
```

---

## 五、不能直接调用/修改时的替代策略

> **核心原则**：能不直接调方法，就不直接调。让游戏自己调，你只改触发条件。

当方法不能直接调用、字段不能直接修改时，可以采用以下策略实现相同效果：

---

### 5.1 策略一：Hook 上游调用者

**原理**：找到调用目标方法的上游方法，在上游方法的执行流程中让游戏自己调用目标方法。

**适用场景**：
- 目标方法会被游戏正常调用，但调用时机/条件不满足
- 需要在特定时机触发目标方法

**示例**：触发 `ClearTempHealth()`

```
游戏逻辑
    ↓
OnRoundStart / OnRespawn / OnBuffExpire（上游方法）
    ↓
HealthData.ClearTempHealth()  ← 目标方法
```

```javascript
// Hook 上游方法，在游戏线程中安全触发
var RVA_ON_RESPAWN = 0xXXXXXX;
Interceptor.attach(base.add(RVA_ON_RESPAWN), {
    onEnter: function(args) {
        // 在 OnRespawn 执行前，确保条件满足
        // 游戏会自动调用 ClearTempHealth
        sendLog('info', 'OnRespawn 触发，游戏将自动调用 ClearTempHealth');
    }
});
```

**优点**：
- ✅ 在游戏线程执行，线程安全
- ✅ 所有前置条件、参数校验由游戏完成
- ✅ 不破坏游戏逻辑
- ✅ 完整的事件链正常触发

**缺点**：
- ❌ 需要找到正确的上游方法
- ❌ 无法精确控制调用时机

---

### 5.2 策略二：修改触发条件

**原理**：修改方法调用的判断条件，让游戏"认为"条件已满足，从而自动调用目标方法。

**适用场景**：
- 目标方法有条件判断（if/switch）
- 可以找到条件判断方法或字段

**示例 A**：修改 Buff 过期时间触发 `ClearTempHealth`

```javascript
// 如果 tempHealth 是由某个 Buff 提供的
// 把 Buff 的 endTime 改成"已过期"，游戏检测后自动清除

var buffPtr = ...;  // Buff 实例地址
var buffEndTime = buffPtr.add(0x10);  // 假设 endTime 在 0x10
var currentTime = getGameTime();       // 获取游戏当前时间

buffEndTime.writeFloat(currentTime - 1);  // 设为"已过期"

// 下一帧游戏检测到 Buff 过期 → 自动调用 ClearTempHealth
```

**示例 B**：Hook 条件判断方法

```javascript
// 假设有个 ShouldClearTempHealth() 方法返回 bool
var RVA_SHOULD_CLEAR = 0xXXXXXX;
Interceptor.replace(base.add(RVA_SHOULD_CLEAR), new NativeCallback(function(self) {
    return 1;  // 强制返回 true，游戏就会调用 ClearTempHealth
}, 'bool', ['pointer']));
```

**优点**：
- ✅ 游戏自己调用，线程安全
- ✅ 逻辑完整，事件链正常
- ✅ 不易被检测

**缺点**：
- ❌ 需要分析条件判断逻辑
- ❌ 可能影响其他依赖该条件的逻辑

---

### 5.3 策略三：Hook 方法本身修改行为

**原理**：目标方法会被正常调用，但效果不是你想要的。Hook 它，改变其行为或返回值。

**适用场景**：
- 方法会被调用，但需要修改其效果
- 需要监控方法调用

**示例 A**：Hook `ClearTempHealth` 监控调用

```javascript
var RVA_CLEAR_TEMP_HEALTH = 0xAE4400;
Interceptor.attach(base.add(RVA_CLEAR_TEMP_HEALTH), {
    onEnter: function(args) {
        sendLog('info', 'ClearTempHealth 被调用，实例: ' + args[0]);
    },
    onLeave: function(retval) {
        // 方法执行完后，可以把值改回来
        // 或者做其他操作
    }
});
```

**示例 B**：Hook `get_currentHealth` 返回虚假值

```javascript
// 不修改 actual health，只修改读取时的返回值
var RVA_GET_CURRENT_HEALTH = 0xXXXXXX;
Interceptor.replace(base.add(RVA_GET_CURRENT_HEALTH), new NativeCallback(function(self, methodInfo) {
    return 999;  // 永远返回 999 血量
}, 'int', ['pointer', 'pointer']));
```

**优点**：
- ✅ 不修改实际数据，只改读取结果
- ✅ 不会被服务端校验发现（实际值没变）
- ✅ 可以监控所有调用

**缺点**：
- ❌ 只影响读取，不影响游戏内部逻辑使用的真实值
- ❌ 如果游戏内部也用这个方法，可能产生副作用

---

### 5.4 策略四：模拟调用链

**原理**：找到目标方法调用的完整前置条件，按顺序模拟/满足这些条件。

**适用场景**：
- 目标方法需要多个前置条件
- 可以逐个满足这些条件

**示例**：触发 `ClearTempHealth`

```javascript
// ClearTempHealth 可能需要这些前置条件：
// 1. tempHealth > 0
// 2. 某个状态标记为 true
// 3. 游戏处于正确阶段

// Step 1: Hook 检查方法，让它返回"需要清除"
var RVA_CHECK_TEMP = 0xXXXXXX;
Interceptor.replace(base.add(RVA_CHECK_TEMP), new NativeCallback(function(self) {
    return 1;  // 返回 true
}, 'bool', ['pointer']));

// Step 2: 游戏下一帧自动调用 ClearTempHealth
```

**优点**：
- ✅ 完整模拟游戏逻辑
- ✅ 线程安全

**缺点**：
- ❌ 需要深入分析调用链
- ❌ 实现复杂

---

### 5.5 策略五：Interceptor.replace 完全替换

**原理**：用 `Interceptor.replace` 完全替换目标方法的实现，在游戏线程中安全执行自定义逻辑。

**适用场景**：
- 需要完全控制方法行为
- 方法内部逻辑可以重写

**示例**：替换 `get_KnifeRange` 实现无限刀距

```javascript
var RVA_GET_KNIFE_RANGE = 0xB170A0;
var origGetKnifeRange = new NativeFunction(base.add(RVA_GET_KNIFE_RANGE), 'float', ['pointer', 'pointer']);

Interceptor.replace(base.add(RVA_GET_KNIFE_RANGE), new NativeCallback(function(self, methodInfo) {
    // 在游戏线程中安全调用其他方法
    var isMyPlayer = origIsMyPlayer(self, ptr(0));
    if (isMyPlayer) {
        return 999.0;  // 本地玩家返回超大范围
    }
    return origGetKnifeRange(self, methodInfo);  // 其他玩家正常返回
}, 'float', ['pointer', 'pointer']));
```

**优点**：
- ✅ 在游戏线程执行，线程安全
- ✅ 可以调用其他 NativeFunction
- ✅ 完全控制方法行为

**缺点**：
- ❌ 需要了解原方法逻辑
- ❌ 可能影响其他依赖该方法的地方

---

### 5.6 策略六：修改方法参数

**原理**：Hook 方法入口，修改传入参数，让方法按你想要的方式执行。

**适用场景**：
- 方法参数影响结果
- 可以预测参数含义

**示例**：修改 `Hurt(int damage)` 的伤害值

```javascript
var RVA_HURT = 0xAE45B0;
Interceptor.attach(base.add(RVA_HURT), {
    onEnter: function(args) {
        // args[0] = this (HealthData*)
        // args[1] = MethodInfo*
        // args[2] = damage (int)
        
        var originalDamage = args[2].toInt32();
        sendLog('info', 'Hurt 被调用，原始伤害: ' + originalDamage);
        
        // 修改伤害为 0（无敌效果）
        args[2] = ptr(0);
    }
});
```

**优点**：
- ✅ 不改变方法逻辑，只改输入
- ✅ 简单直接

**缺点**：
- ❌ 需要知道参数含义
- ❌ 可能被后续逻辑覆盖

---

### 5.7 策略七：绕过方法，直接操作字段

**原理**：如果方法只是修改某个字段，直接操作该字段，绕过方法调用。

**适用场景**：
- 方法只是简单的字段赋值
- 字段可以被直接修改

**示例 A**：绕过 `ClearTempHealth`，直接清零 `tempHealth`

```javascript
// ClearTempHealth() 内部就是 tempHealth = 0
// 直接操作 ObscuredInt 字段

var healthDataPtr = inst.healthData;
var tempHealthPtr = healthDataPtr.add(0x30);  // tempHealth 偏移

// 读取加密密钥
var key = tempHealthPtr.readS32();  // currentCryptoKey

// 计算加密值（0 XOR key = key）
var encryptedZero = 0 ^ key;

// 写入加密后的值
tempHealthPtr.add(0x04).writeS32(encryptedZero);  // hiddenValue
tempHealthPtr.add(0x0C).writeS32(0);              // fakeValue
```

**示例 B**：绕过 `set_team`，直接修改 `team` 字段

```javascript
// set_team(Team) 有 listener，直接写字段绕过
var playerPtr = inst.player;
playerPtr.add(0x20).writeS32(1);  // 直接改为保卫者
// 注意：UI 不会更新，因为没触发 listener
```

**优点**：
- ✅ 不触发事件链/回调
- ✅ 简单直接

**缺点**：
- ❌ 可能导致状态不一致（UI 不更新）
- ❌ 加密字段需要正确处理 XOR

---

### 5.8 策略八：利用游戏内置机制

**原理**：利用游戏已有的调试功能、作弊码、开发者模式等。

**适用场景**：
- 游戏有内置调试功能
- 有可利用的游戏机制

**常见利用点**：

| 机制 | 说明 | 示例 |
|------|------|------|
| 控制台命令 | 开发者留下的调试命令 | `god`, `noclip` |
| 配置文件 | 游戏配置可修改 | `.ini`, `.json`, `.xml` |
| 开发者模式 | 隐藏的开发选项 | `isDebugMode`, `cheatsEnabled` |
| 测试地图 | 特殊测试场景 | 无限弹药、无敌等 |
| 单机模式 | 离线模式无服务端校验 | 本地修改生效 |

**优点**：
- ✅ 游戏原生支持，最安全
- ✅ 不需要逆向

**缺点**：
- ❌ 不是所有游戏都有
- ❌ 可能被版本更新移除

---

### 5.9 策略九：输入/UI 模拟

**原理**：模拟玩家输入或 UI 操作，让游戏按正常流程执行。

**适用场景**：
- 目标功能可以通过 UI 触发
- 可以模拟输入事件

**示例**：模拟按键触发武器切换

```javascript
// 与其调用 SwitchWeapon()，不如模拟按键
// 游戏会正常处理按键事件，包括所有校验和回调

// 方式1：修改输入状态字段
var playerInput = inst.playerInput;
playerInput.add(0x08).writeS32(1);  // 模拟按键按下

// 方式2：Hook 输入处理方法
var RVA_ON_KEY_PRESS = 0xXXXXXX;
Interceptor.attach(base.add(RVA_ON_KEY_PRESS), {
    onEnter: function(args) {
        // 在按键处理时注入自定义逻辑
    }
});
```

**优点**：
- ✅ 完全模拟正常游戏流程
- ✅ 所有校验、回调正常触发
- ✅ 最难被检测

**缺点**：
- ❌ 需要了解输入系统
- ❌ 可能受 UI 状态限制

---

### 5.10 策略对比总结

| 策略 | 线程安全 | 实现难度 | 隐蔽性 | 适用场景 |
|------|---------|---------|--------|---------|
| Hook 上游调用者 | ✅ | 中 | 高 | 方法会被正常调用 |
| 修改触发条件 | ✅ | 中 | 高 | 有条件判断的方法 |
| Hook 方法本身 | ✅ | 低 | 中 | 需要监控/修改行为 |
| 模拟调用链 | ✅ | 高 | 高 | 复杂前置条件 |
| Interceptor.replace | ✅ | 中 | 中 | 需要完全控制方法 |
| 修改方法参数 | ✅ | 低 | 中 | 参数影响结果 |
| 直接操作字段 | ⚠️ | 低 | 低 | 简单字段赋值 |
| 利用内置机制 | ✅ | 低 | 最高 | 有调试功能 |
| 输入/UI 模拟 | ✅ | 中 | 最高 | 可通过 UI 触发 |

---

### 5.11 实际案例对照表

| 目标 | ❌ 错误做法 | ✅ 推荐策略 |
|------|-----------|-----------|
| 清除临时血量 | 直接调 `ClearTempHealth()` | 修改 Buff 过期时间，让游戏自己调 |
| 恢复血量 | 直接调 `Heal()` | Hook `get_currentHealth` 返回值 |
| 切换武器 | 直接调 `SwitchWeapon()` | 修改 `curSlot` 或模拟按键 |
| 触发无敌 | 直接调 `SetInvincible()` | 修改 `isInvincible` + `invinsibleEndTime` |
| 修改射速 | — | 直接修改 `shotsPerMinute` 字段 |
| 增加刀范围 | — | Hook `get_KnifeRange` 返回值 |
| 修改击杀数 | 直接写 `kill` 字段 | Hook `get_kill` 返回值（避免触发 listener） |
| 修改移动速度 | 直接写 `baseMoveSpeed` | 直接写字段即可（普通 float） |

---

## 六、本项目中各类字段/方法的安全等级速查

### 6.1 Entity 类

| 偏移 | 字段 | 类型 | 读取 | 写入 | 说明 |
|------|------|------|------|------|------|
| 0x0C | baseMoveSpeed | float | 🟢 | 🟢 | 直接读写 |
| 0x10 | speedPenalty | float | 🟢 | 🟢 | 直接读写 |
| 0x14 | damageRate | float | 🟢 | 🟢 | 直接读写 |
| 0x18 | isInvincible | bool | 🟢 | 🟡 | 写入可能触发状态检查 |
| 0x1C | healthData | HealthData* | 🟢 | — | 指针，不要修改 |
| 0x20 | team | int | 🟢 | 🟠 | set_team 有 listener |
| 0x34 | buffs | List* | 🟢 | — | 指针，不要修改 |

### 6.2 HealthData 类

| 偏移 | 字段 | 类型 | 读取 | 写入 | 说明 |
|------|------|------|------|------|------|
| 0x08 | currentHealth | ObscuredInt | 🟡 需解密 | 🟡 需加密写 | XOR 运算 |
| 0x1C | maxHealth | ObscuredInt | 🟡 需解密 | 🟡 需加密写 | XOR 运算 |
| 0x30 | tempHealth | ObscuredInt | 🟡 需解密 | 🟡 需加密写 | XOR 运算 |
| 0x44 | invinsibleEndTime | float | 🟢 | 🟢 | 直接读写 |

### 6.3 ClientData 类

| 偏移 | 字段 | 类型 | 读取 | 写入 | 说明 |
|------|------|------|------|------|------|
| 0x08 | defaultWpnBagID | int | 🟢 | 🟠 | 可能影响武器逻辑 |
| 0x10 | nickName | string | 🟢 | 🔴 | 只读属性+不可变字符串 |
| 0x14 | level | int | 🟢 | 🔴 | 只读属性，服务端数据 |
| 0x18 | joinTeam | int | 🟢 | 🔴 | 服务端权威 |
| 0x1C | isBot | bool | 🟢 | 🔴 | 服务端设定 |
| 0x20 | vipLevel | int | 🟢 | 🔴 | 只读属性，服务端数据 |
| 0x24 | character | int | 🟢 | 🔴 | 服务端数据 |

### 6.4 PlayerData 类

| 偏移 | 字段 | 类型 | 读取 | 写入 | 说明 |
|------|------|------|------|------|------|
| 0x14 | playerID | int | 🟢 | 🔴 | 服务端分配 |
| 0x18 | orignalCharacterName | string | 🟢 | 🔴 | 不可变字符串 |
| 0x4C | kill | SubscribeableProperty\<int\> | 🟠 需调get | 🔴 | 有listener |
| 0x50 | death | SubscribeableProperty\<int\> | 🟠 需调get | 🔴 | 有listener |
| 0x58 | score | SubscribeableProperty\<int\> | 🟠 需调get | 🔴 | 有listener |

### 6.5 PlayerWeapons 类

| 偏移 | 字段 | 类型 | 读取 | 写入 | 说明 |
|------|------|------|------|------|------|
| 0x10 | curSlot | int | 🟢 | 🟠 | 切换武器可能触发动画 |
| 0x18 | inUse | Weapon* | 🟢 | — | 指针，不要修改 |
| 0x3C | Modifier_ReloadSpeed | PropertyModifier | 🟠 需调Get() | 🔴 | 委托计算 |
| 0x40 | Modifier_KnifeRange | PropertyModifier | 🟠 需调Get() | 🔴 | 委托计算 |
| 0x44 | Modifier_KnifeSpeed | PropertyModifier | 🟠 需调Get() | 🔴 | 委托计算 |

### 6.6 WeaponData_Gun 类

| 偏移 | 字段 | 类型 | 读取 | 写入 | 说明 |
|------|------|------|------|------|------|
| 0xB8 | clip | int | 🟢 | 🟢 | 弹匣容量 |
| 0xBC | ammo | int | 🟢 | 🟢 | 备弹 |
| 0xCC | shotsPerMinute | float | 🟢 | 🟢 | 射速 |
| 0xD0 | fireAnimMultiplier | float | 🟢 | 🟢 | 射击动画倍率 |
| 0xD4 | reloadAnimRatio | float | 🟢 | 🟢 | 换弹动画比率 |
