# IL2CPP 静态字段获取操作手册（UCF 1.7 / 32 位）

> 适用：Frida 附加 `GameAssembly.dll`，本游戏为 **32 位 IL2CPP**。  
> 示例：`GameManager.myPlayer`  
> 参考脚本：`get_static_fields_fixed.js`（已修正）

---

## 一、以前为什么读不到？

### 错误做法（旧版 `get_all_instances.js`）

```text
klass地址 = GameAssembly基址 + 0xE2933C   ← 把「TypeInfo 槽」当成了 klass 本体
static_fields = klass地址 + 0x5C 读 4 字节
```

### 实际内存布局

```text
地址 (基址+0xE2933C)  存的是「指针」→ 指向真正的 Il2CppClass
                      不是 Il2CppClass 结构体本身
```

在 `0xE2933C + 0x5C` 读到的是 **相邻全局数据**，不是 `static_fields`。

### 正确链路（三层指针）

```text
TypeInfo槽 ─readPointer()→ Il2CppClass* (klass)
klass      ─+0x5C readPointer()→ static_fields 内存块
static_fields ─+字段偏移→ 具体静态字段值
```

旧脚本少了解引用第一层，所以地址和数值都不对。

---

## 二、通用方法（任意类的静态字段）

### 步骤 0：准备 dump 文件

| 文件 | 路径 | 用途 |
|------|------|------|
| `dump.cs` | `01-游戏逆向分析-相关信息/Il2CppDumper/dump.cs` | 查类名、**静态字段偏移** |
| `script.json` | 同上目录 `script.json` | 查 `类名_TypeInfo` 的 **RVA** |
| `il2cpp.h` | 同上目录（注释结构） | 查 `Il2CppClass` 布局（本游戏 32 位 `static_fields` 在 klass **+0x5C**） |

游戏更新后需重新跑 Il2CppDumper，**所有 RVA 会变**。

---

### 步骤 1：在 dump.cs 找目标类与字段偏移

搜索：`public class 你的类名`

**只抄 `public static` / `private static` 行的偏移**（实例字段偏移无效）。

示例（`dump.cs` 约 242579 行）：

```csharp
public class GameManager : Singleton<GameManager>
{
    public static Player myPlayer;        // 0x0  ← 静态字段偏移
    public static GameMode gameMode;      // 0x4
    public static WeaponLimited weaponLimited; // 0x8
    ...
    public GameObject playerPrefab;       // 0xC  ← 实例字段，不能从 static_fields 读
}
```

记下：`myPlayer` 偏移 = **0x00**，类型 = `Player*`（指针，4 字节）。

---

### 步骤 2：在 script.json 找 TypeInfo 的 RVA

搜索：`"Name": "GameManager_TypeInfo"`

```json
{
  "Address": 14848828,
  "Name": "GameManager_TypeInfo",
  "Signature": "GameManager_c*"
}
```

`14848828` = `0x0E2933C` → 这是 **TypeInfo 槽在 DLL 内的偏移（RVA）**，不是 klass 本体地址。

规律：类名 + `_TypeInfo`，如 `Player_TypeInfo`、`ModeBase_TypeInfo`。

---

### 步骤 3：Frida 中计算运行时地址

```javascript
var base = Process.findModuleByName("GameAssembly.dll").base;
var TYPEINFO_RVA = 0x0E2933C;   // 来自 script.json

var typeInfoSlot = base.add(TYPEINFO_RVA);  // TypeInfo 槽地址
var klass = typeInfoSlot.readPointer();     // ★ 第一次解引用
```

验证 klass 是否有效：在 IDA 或脚本里读 `klass+0x08` 的字符串，应为类名 `"GameManager"`。

---

### 步骤 4：确保类已初始化（有 static_fields 块）

部分类要先跑静态构造函数（`.cctor`），`static_fields` 才分配。

```javascript
// klass + 0x64 进入 Il2CppClass_2
var cctor_finished = klass.add(0x64 + 0x10).readU32();
var bitflags2 = klass.add(0x64 + 0x57).readU8();
if ((bitflags2 & 4) !== 0 && cctor_finished === 0) {
    var init = new NativeFunction(base.add(0x108970), 'void', ['pointer']);
    init(klass);  // ★ 传入 klass，不是 typeInfoSlot
}
```

`0x108970`：`il2cpp_runtime_class_init` 的 RVA（可用 IDA 搜符号确认）。

---

### 步骤 5：读 static_fields 指针

```javascript
var staticFields = klass.add(0x5C).readPointer();  // ★ 32 位 IL2CPP 固定偏移
```

`staticFields` = 该类所有静态字段所在的 **连续内存块首地址**。

---

### 步骤 6：按 dump 偏移读字段值

| 字段类型 | Frida 读法 |
|----------|------------|
| 指针（`Player*`、`string` 等） | `staticFields.add(偏移).readPointer()` |
| `int` / `enum` | `readS32()` |
| `bool` | `readU8()` |
| `float` | `readFloat()` |

```javascript
var myPlayer = staticFields.add(0x00).readPointer();  // Player 对象地址
```

---

### 步骤 7：区分「静态字段」和「单例对象」

| 目标 | 路径 | 得到 |
|------|------|------|
| 静态字段 `myPlayer` | `TypeInfo → klass → static_fields + 0x0` | **Player*** |
| 单例 `GameManager.instance` | `MethodInfo@0xE1CE64` + 函数 `0x4A8170` | **GameManager***（MonoBehaviour 组件） |

读 `allPlayers` 等要用 **GameManager 实例**；判断本地玩家用 **myPlayer**。

---

## 三、实例：GameManager.myPlayer 完整数据链

### 数据来源一览

| 数据 | 文件 | 值 |
|------|------|-----|
| 类名 | dump.cs | `GameManager` |
| 字段 | dump.cs | `public static Player myPlayer; // 0x0` |
| TypeInfo RVA | script.json | `0x0E2933C` |
| klass 上 static_fields 偏移 | il2cpp.h / IDA | `+0x5C`（32 位） |
| class_init | IDA | `0x108970` |

### 运行时计算公式

假设 `GameAssembly.dll` 基址 = `B`：

```text
① TypeInfo槽地址     = B + 0x0E2933C
② klass               = [①]                    （readPointer）
③ static_fields块     = [② + 0x5C]           （readPointer）
④ myPlayer (Player*)  = [③ + 0x00]           （readPointer）
```

**myPlayer 字段的「值」** = ④（一个 Player 对象指针）。  
若要读昵称等，再对 ④ 加 `ClientData` 等**实例字段**偏移（仍在 dump.cs 里查，但属于 Player 类）。

### 最小 Frida 片段

```javascript
var B = Process.findModuleByName("GameAssembly.dll").base;
var klass = B.add(0x0E2933C).readPointer();
var sf = klass.add(0x5C).readPointer();
var myPlayer = sf.readPointer();  // offset 0x0
console.log("myPlayer = " + myPlayer);
```

### 何时为 null？

- 在大厅、加载界面：正常，尚未赋值  
- 必须在**对局内**、本地玩家已生成后再读  

---

## 四、换其他类怎么做？

把下面三项替换即可，流程不变：

1. `dump.cs` → `类名` + `static 字段偏移`  
2. `script.json` → `类名_TypeInfo` 的 `Address`（转十六进制 RVA）  
3. Frida → `klass = base.add(RVA).readPointer()` → `sf = klass.add(0x5C).readPointer()` → `sf.add(字段偏移)`

**不要**对 `base.add(RVA)` 直接加 `0x5C`。

---

## 五、自检清单

- [ ] `klass+0x08` 读出的字符串是否为目标类名？  
- [ ] `static_fields` 非 0？  
- [ ] 字段在 dump 里是否标了 `static`？  
- [ ] 指针字段是否用 `readPointer()`？  
- [ ] 是否在对局内测试？  
- [ ] 游戏版本更新后是否重新 dump？

---

## 六、本目录相关文件

| 文件 | 作用 |
|------|------|
| `get_static_fields_fixed.js` | 完整流程 + class_init + 读多个静态字段 + 单例对比 |
| `get_all_instances.js` | 诊断：验证 klass、扫偏移（已改为先解引用） |
| 本手册 | 原理与通用步骤 |
