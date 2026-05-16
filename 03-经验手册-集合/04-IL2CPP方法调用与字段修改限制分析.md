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

#### 

#### 

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

#### 

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

### 

## 三、实例地址 vs 方法地址

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



