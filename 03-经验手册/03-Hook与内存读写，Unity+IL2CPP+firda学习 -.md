# 🔧Unity+IL2CPP 游戏修改技术手册

> **版本**: V1.0  
> **创建日期**: 2026-04-23  
> **适用范围**: Unity IL2CPP 游戏修改  
> **核心工具**: Frida + Python + PyInstaller

---

## 📋 目录

1. [技术栈概述](#一技术栈概述)
2. [环境准备](#二环境准备)
3. [游戏分析流程](#三游戏分析流程)
4. [Frida 脚本开发](#四frida-脚本开发)
5. [打包发布流程](#五打包发布流程)
6. [常见问题与解决方案](#六常见问题与解决方案)
7. [最佳实践](#七最佳实践)
8. [附录：完整命令参考](#八附录完整命令参考)

---

## 一、技术栈概述

### 1.1 核心工具

| 工具 | 用途 | 版本要求 |
|------|------|---------|
| **Frida** | 动态插桩框架 | 16.0+ |
| **frida-tools** | Python 绑定 | 12.0+ |
| **PyInstaller** | Python 打包为 EXE | 6.0+ |
| **Il2CppDumper** | Unity IL2CPP 反编译 | 最新版 |
| **Python** | 脚本语言 | 3.8+ |

### 1.2 工作流程

```
游戏分析 → 脚本开发 → 本地测试 → 打包发布 → 用户使用
    ↓           ↓          ↓          ↓          ↓
Il2CppDumper  JS 脚本   frida -p   PyInstaller   EXE 文件
   ↓           ↓          ↓          ↓          ↓
dump.cs     调试日志   附加进程   打包依赖   一键运行
script.json  效果验证   日志输出   单文件    无需环境
```

1.2.1 解构流程

dump.cs（理解结构） → script.json（获取地址） → Frida 脚本（Hook 实现）



### 1.3 技术优势

| 优势 | 说明 |
|------|------|
| **无需修改游戏文件** | 纯内存修改，不触碰游戏文件 |
| **热插拔** | 随时注入/卸载，无需重启游戏 |
| **跨版本兼容** | 基于 RVA 地址，游戏更新后只需更新地址 |
| **高性能** | `Interceptor.replace` 零性能影响 |
| **易于分发** | 打包为单文件 EXE，用户无需安装任何依赖 |

---

## 二、环境准备

### 2.1 安装 Python

### 2.2 安装 Frida 工具

### 2.3 安装 PyInstaller

### 2.4 安装 Il2CppDumper（可选，用于游戏分析）

---

## 三、游戏分析流程

### 3.1 提取游戏文件

### 3.2 使用 Il2CppDumper 分析

### 3.3 分析 dump.cs

#### 3.3.1 查找目标类

#### 3.3.2 查找目标方法

#### 3.3.3 查看字段偏移

### 3.4 分析 script.json



# ️ 通俗易懂串讲：磁盘、内存 + RVA / VA / 文件偏移 / 字段偏移 完整关系

> **核心目标**：先铺垫两个核心载体（磁盘、内存），再把所有地址概念串死，结合 `dump.cs`、`script.json`、CE、IL2CPP 逆向场景来讲。

------

## 一、先搞懂：磁盘 和 内存 本质区别

### 1. 磁盘（硬盘）

- **存的是静态文件**：`GameAssembly.dll` / `libil2cpp.so` 安静躺在电脑硬盘里，**没运行、不占用内存条**，只是一堆二进制原始数据。

- 特点

  - 永久保存，关机还在。
  - **CPU 不直接读磁盘**。
  - IDA看的是硬盘dll

### 2. 内存（内存条）

- **游戏双击启动后**：操作系统**把磁盘里的 DLL 文件，整个映射加载进进程虚拟内存**。

- **状态**：这时代码、函数、玩家数据、Buff 逻辑全都跑进内存条里，**CPU 只读取、运行内存里的数据**。

- 特点

  - 临时运行，关闭游戏就消失。
- CE、Frida 看的**全是内存里的东西**，不看磁盘。

------

## 二、四个核心地址概念 逐个大白话解释

### 1. 文件偏移 FileOffset（只属于磁盘）

- **定义**：只针对**硬盘里的 DLL 文件**。从文件开头算起，往后第多少字节，就是文件偏移。
- **作用**：定位**磁盘静态文件**里某段代码、某个函数的位置，和游戏运行、内存无关。

### 2. RVA 相对虚拟地址（磁盘 → 内存的桥梁）

- **全称**：Relative Virtual Address
- **参照物**：**DLL 模块加载到内存后的起始地址（模块基址 Base）**
- **含义**：**内存中，当前位置 距离 模块基址 有多少字节偏移**。

> **实战注意**：你 `dump.cs` 里的 `RVA: 0xA0470`、`script.json` 里的 `"Address": 11785072` **本质全是 RVA**。这是 Il2CppDumper 从磁盘 DLL 解析出来、预先算好的**相对偏移**，不管游戏开多少次、DLL 基址变不变，RVA 永远固定。

### 3. VA 虚拟地址（只属于运行内存）

- **全称**：Virtual Address
- **定义**：就是**进程内存里的绝对真实地址**。
- **场景**：CE 按 Ctrl+G 跳转、IDA 看的地址、调试器断点地址，全是 VA。

> **示例**：你 dump.cs 里 `VA: 0x100A0470`，假设模块基址是 `0x10000000`，则 `0x10000000 + 0xA0470 = 0x100A0470` 完全对上。

### 4. 0x98 这种字段偏移（结构体内部偏移）

- **场景**：你代码里 `private PlayerData <playerData>k__BackingField; // 0x98`
- **定义**：这个 **0x98 = 类/结构体内部成员偏移**。
- 关键点

  - 和磁盘无关、和 DLL 基址无关、和 RVA 无关。
- 是 **PlayerData 这个结构体，从实例起始地址开始，往后数 0x98 字节，就是这个成员变量**。

------

## 三、磁盘 → 内存 → RVA → VA → 字段偏移 完整链路

1. **磁盘阶段**
   硬盘里 `GameAssembly.dll` 有固定文件偏移，Il2CppDumper 解析它，算出每个函数、字段的 **RVA**，写入 `dump.cs` 和 `script.json`。
   - `script.json` 的 `Address` = 函数的 **RVA**
2. **加载进内存阶段**
   游戏启动 → 系统把 DLL 映射到内存，分配一个**模块基址 Base**。
3. 
4. **找游戏数值（血量/伤害/倍率）**
   先找到 **玩家结构体实例的 VA** → 再加 **字段偏移 0x98** → 得到最终数值内存地址 → **CE 直接搜、改数值**。

------

## 四、回答你两个关键疑问

### 1. script.json 里的 Address 有什么用？

```json
"Address": 11785072
```

- **本质**：这就是**函数的 RVA**，固定不变。

- 作用

  1. **IDA/Ghidra 导入符号**：自动定位函数位置。
  2. **Frida Hook**：`Base + Address` 拿到 VA 直接挂钩子。
  3. **CE 跳转内存**：看汇编、下断点，看 Buff 构造函数执行逻辑。
  
- ** 误区**：**不能直接拿来 CE 搜游戏数值**，它是代码地址，不是数值地址。

### 2. CE 能不能搜到游戏数值？

- **RVA、Address、VA**：只能定位函数代码，搜不到血量、倍率这类数值。
- **0x98 字段偏移**：本身也不是地址，必须 **实例 VA + 0x98** 算出最终地址，**这个最终地址可以在 CE 里直接改、锁定数值**。
- **普通数值**：血量、金币这类简单数值，直接 CE 模糊搜索/精确搜索就行，不用管 RVA。

------

## 五、通俗比喻（一秒记牢）

把 `GameAssembly.dll` 当成**一本书**：

| 概念              | 比喻                                 | 解释                                 |
| ----------------- | ------------------------------------ | ------------------------------------ |
| **磁盘**          | 放在书架上的书                       | 静态不动                             |
| **内存**          | 把书摊在桌子上读                     | 运行中                               |
| **模块基址 Base** | 桌子的左上角原点                     | 参考点                               |
| **RVA**           | 从桌子左上角，向右翻多少页           | 相对位置，永远不变                   |
| **VA**            | 整个房间里这本书某行字的**绝对坐标** | 真实位置                             |
| **0x98 字段偏移** | 某一页里，某段文字的第几个字         | 和桌子、书架都无关，只和书页排版有关 |

------

## 六、一句话总结区别

1. **磁盘**：静态文件，存原始二进制。
2. **内存**：运行时加载进来，CPU 只跑内存。
3. **RVA**：相对模块基址的偏移，磁盘解析得出，永久固定。
4. **VA**：内存绝对地址 = 基址 + RVA，CE/调试器用。
5. **0x98**：结构体内部字段偏移，用来算玩家数据、Buff 数值的真实地址。





### IDA 静态分析中的基址 0x10000000 和 CE/Frida 中的模块基址 Base 有什么区别？

#### 模式 1：IDA 静态分析（你 100% 在用这个）

- **操作**：直接双击打开磁盘里的 GameAssembly.dll（游戏没运行都能打开）。
- **数据源**：硬盘上的静态文件。
- 显示的地址：
  - 显示 **RVA**（和你的 `dump.cs`/`script.json` 完全一致）。
  - 显示的 **VA** 是假的、默认计算的（IDA 给 DLL 预设了一个固定基址 `0x10000000`，算出来的虚拟地址）。
  - **不是游戏运行时的真实内存地址**。

#### 一句话总结（必记）

- **磁盘 DLL**：IDA 静态分析用 → 拿 RVA、字段偏移
- **运行内存**：CE/Frida 用 → 拿 真实 VA，改游戏数值

#### 你在 CE / Frida 中用的 模块基址 Base

- = 游戏运行时，GameAssembly.dll 在内存里的真实加载地址
- = 这是唯一有效、能用来计算真实内存地址的基址

#### IDA 里的 0x10000000

- = 只是 磁盘 DLL 文件里写死的默认预设基址
- = 假的、静态的、游戏运行时根本不会用这个地址
- = 仅给 IDA 静态看代码用，不能用于 CE/Frida

#### 两个「模块基址」的本质区别（秒懂）

**1. IDA 静态基址：0x10000000（磁盘文件自带，假的）**

- **来源**：GameAssembly.dll 硬盘文件本身
- **作用**：让 IDA 能显示出整齐的地址，方便你看代码逻辑

**2. 运行时基址 Base（内存真实地址，真的）**

- **来源**：游戏启动后，Windows/Linux 系统随机分配
- **载体**：就是加载到内存的 GameAssembly.dll
- **特点**：每次开游戏都会变，这才是你真正要用的基址

#### 实战举例（对应你的代码）

**你 dump.cs：**

```plaintext
RVA: 0xA0470
VA: 0x100A0470 （= 0x10000000 + 0xA0470，IDA假VA）
```

**游戏运行时真实计算：**
假设系统给 GameAssembly.dll 分配的真实运行基址是：
`0x7FF6A0000000`

→ 这个地址，才是 CE 按 Ctrl+G 能跳转到的真实内存地址。

---

## 四、Frida 脚本开发

### 4.1 基础脚本结构

```javascript
这是一份基于 Frida 的 JavaScript 脚本，主要用于 Hook（挂钩） 游戏进程中的特定函数。



// 脚本名称：no_recoil.js
// 使用方法：frida -p  -l no_recoil.js
// 解释：-p 指定进程ID，-l 加载脚本文件

console.log("[*] 脚本启动...");

// 立即执行函数表达式 (IIFE)，防止污染全局变量作用域
(function () {
    // 1. 查找 GameAssembly.dll 模块
    // 这一步对应我们之前讲的：获取“运行时基址 Base”
    var gameAssembly = Process.findModuleByName("GameAssembly.dll");
    
    // 检查模块是否找到，防止游戏没启动或名字不对导致报错
    if (!gameAssembly) {
        console.log("[-] GameAssembly.dll not found!");
        return;
    }

    // 2. 计算目标地址 (核心步骤)
    // 这里演示了之前讲的公式：VA = Base + RVA
    // gameAssembly.base  -> 运行时真实的模块基址 (Base)
    // 0xB19980         -> 你从 dump.cs 或 IDA 拿到的相对偏移 (RVA)
    // .add()           -> Frida 的方法，用于地址相加，自动处理十六进制运算
    var ADDR_TARGET = gameAssembly.base.add(0xB19980);  // 最终得到真实的内存绝对地址 (VA)

    // 打印计算出的真实地址，方便你在 CE 或 IDA 中核对
    console.log("[*] Target @ " + ADDR_TARGET);

    // 3. Hook 目标函数
    // Interceptor.replace 是最强力的拦截方式，它会把原函数完全替换掉
    Interceptor.replace(
        ADDR_TARGET, // 传入刚才计算出的真实地址
        new NativeCallback(function (thisPtr, methodInfo) {  
           //  new NativeCallback(...) —— “造一个假身”
            //  游戏原本雇佣了一个叫“老员工”（原函数）的人来干活。你用 NativeCallback 造了一个叫“新员工”（你的脚本）的人，并伪造了证件，混进去把“老员工”顶替了。
            // --- 这里是新函数的逻辑 ---
            
            // 自定义逻辑：当游戏调用这个函数时，Frida 会打印这行日志
            // thisPtr 通常指代“this”指针（对象实例），methodInfo 是方法信息
            console.log("[+] Target called @ " + thisPtr);
            
            // 【关键点】：这里没有调用原函数
            // 原函数的功能（比如增加后座力、扣血、检测作弊）被直接“吃掉”了，不再执行
            // 这就是实现“无后座力”或“功能屏蔽”的原理
            // 如果想执行原函数，通常需要保存原指针并调用，但这里是 replace 模式，默认就是替换
        }, 
        "void",       // 返回值类型：void (无返回值)
        ["pointer", "pointer"]) // 参数类型：两个指针 (thisPtr, methodInfo)
    );

    console.log("[+] Hook successful!");
})();



Interceptor.replace
    作用：暴力替换。
    效果：游戏原本想执行 函数A（比如计算子弹乱飞），结果 CPU 跳转过去发现代码被你换成了 函数B（只打印一行日志，什么都不做）。
    结果：原功能失效（例如：子弹不再乱飞，变成了无后座力）。

⚠️ 注意事项
参数匹配：new NativeCallback 里的 ["pointer", "pointer"] 必须和原函数的参数一致。如果原函数参数不对，Hook 可能会导致游戏崩溃。
返回值：如果原函数有返回值（比如 bool 或 int），你这里写 void 可能会导致游戏逻辑错误。通常如果是“屏蔽功能”，返回值最好设为 true 或 0（视具体逻辑而定）。
```

## Frida 核心：Hook 技术（最重要）

Hook = **拦截函数执行，修改参数 / 返回值 / 逻辑**

分 **2 种 Hook 方式**（你的场景全覆盖）

### 1. Native 层 Hook（通用，对接 script.json Address）

针对：`script.json` 里的函数 RVA 地址

### 2. IL2CPP 专属 Hook（高级，对接 dump.cs 类 / 方法）

针对：`dump.cs` 里的**类名、方法名**（不用记 RVA，最方便）



Native和IL2CPP的区别

| 维度     | Native 层 Hook (你的代码)                                    | IL2CPP 专属 Hook (frida-il2cpp-bridge)                       |
| -------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 操作方式 | 直接修改内存地址上的机器码。                                 | 通过类名和方法名找到函数再修改。                             |
| 代码特征 | 硬编码 `0xAF6930` 这样的数字，使用 `Interceptor.attach`。    | 使用 `Il2Cpp.domain.assembly(...).class(...)`。              |
| 优点     | 性能极高，通用性强（任何 C++/游戏都能用），体积小（不需要加载额外的 bridge 库）。 | 开发简单，不用算偏移，直接用 C# 的类名/方法名，可读性强（一眼看出是 Hook 哪个函数）。 |
| 缺点     | 维护困难（游戏一更新，`0xAF6930` 地址就变了，脚本就废了），参数难猜（需要懂汇编看参数在哪个寄存器）。 | 性能稍低（有 JS 到 C# 的转换开销），依赖库（必须安装 `frida-il2cpp-bridge`），体积大。 |
| 适用场景 | 游戏外挂/破解（追求稳定和性能）、底层驱动开发、游戏版本固定时。 | Unity 逆向学习、快速原型开发、游戏版本经常变动时。           |





## Frida 字段操作（对接 dump.cs 私有字段 / 偏移 0x98）

这是你最关心的：**读 / 写 玩家数据、血量、伤害、Buff 等字段**

分 **实例字段** 和 **静态字段**



| 维度     | 实例字段 (Instance)        | 静态字段 (Static)    |
| -------- | -------------------------- | -------------------- |
| 归属     | 属于“个体” (对象)          | 属于“集体” (类/程序) |
| 比喻     | 每个人的身份证信息         | 国家的法律/公告牌    |
| 依赖     | 必须先有对象 (Instance)    | 不需要对象，直接访问 |
| 内存     | 每个对象都有自己的一份副本 | 全程只有一份副本     |
| 你的代码 | `playerInstance.add(0x98)` | `类.field("金币")`   |
| 适用场景 | 修改自己的血量、子弹、速度 | 修改全服的时间       |



------

### 📜 Frida 内存读写实战手册

**目标**：用代码实现 CE 的修改功能，支持所有数据类型
**核心逻辑**：`基址` + `偏移` = `最终数据地址`

#### 1. 核心 API 速查表

在 Frida 中，所有的内存操作都基于 `NativePointer` 对象。

| 操作类型   | 代码示例                    | 对应 CE 操作            | 适用场景                 |
| ---------- | --------------------------- | ----------------------- | ------------------------ |
| **读整数** | `addr.readInt()`            | 查看数值 (4 Bytes)      | ID、子弹数、整型开关     |
| **写整数** | `addr.writeInt(999)`        | 修改数值 (4 Bytes)      | 锁定整型数值             |
| **读浮点** | `addr.readFloat()`          | 查看数值 (Float)        | 血量、伤害、倍率、速度   |
| **写浮点** | `addr.writeFloat(999.0)`    | 修改数值 (Float)        | 锁定浮点数值             |
| **读指针** | `addr.readPointer()`        | 查看指针/指针 (Pointer) | 遍历链表、对象引用       |
| **写指针** | `addr.writePointer(ptr(0))` | 修改指针指向            | 篡改对象归属、注入假数据 |

#### 2. 实战：修改玩家血量 (对应 0x98 偏移)

假设你在 CE 中找到了 `Player` 对象的基址，且血量位于该对象的 `+0x98` 偏移处。



#### 3. 进阶技巧：多级指针 (Pointer Chain)

如果在 CE 中，血量的路径是 `GameAssembly.dll` + `Offset1` -> `Player` -> `Health` (Offset2)，代码如下：



------

### 🧐 为什么会有多级指针（多级页表）？

在操作系统中，CPU 访问内存时，必须把 **虚拟地址 (VA)** 翻译成 **物理地址 (PA)**。这个翻译过程靠的就是 **页表**。

> **核心概念**：页表本质上就是一个巨大的数组（指针数组）。

#### 1. 32位系统的“甜蜜点”（一级指针够用）

#### 2. 64位系统的“灾难”（必须用多级指针）



# Interceptor.attach vs replace：修改返回值代码对比

## 方法一：使用 `Interceptor.attach`（在 `onLeave` 中修改返回值）

```javascript
const base = Module.findBaseAddress("GameAssembly.dll");
const addrIsCooldown = base.add(0x123456);

Interceptor.attach(addrIsCooldown, {
    onLeave: function(retval) {
        // 原始函数已经执行完毕，retval 指向返回值
        // 无论原函数返回什么，强制改为 false (0)
        retval.replace(ptr(0));
        console.log("IsCooldown 返回值已被 attach 修改为 false");
    }
});
```

**特点：**

- ✅ **原函数仍然执行**，可能产生副作用（如更新内部状态）。
- ✅ **只能修改返回值**，无法修改参数（因为 getter 无参数）。
- ✅ **开销较小**，适合高频调用。

**执行流程：**
`调用方 → 原始 IsCooldown 执行 → 返回原始值 → onLeave 修改返回值 → 调用方收到 false`

------

## 方法二：使用 `Interceptor.replace`（完全替换函数）

### 2.1 不调用原函数，直接返回 false

```javascript
const base = Module.findBaseAddress("GameAssembly.dll");
const addrIsCooldown = base.add(0x123456);

Interceptor.replace(addrIsCooldown, new NativeCallback(function(skillPtr) {
    // 完全不执行原始函数，直接返回 false
    console.log("IsCooldown 被 replace 替换，直接返回 false");
    return false;
}, 'bool', ['pointer']));
```

**特点：**

- ❌ **原始函数不执行**，完全被跳过。
- ✅ **可以任意修改参数**（虽然本例没有）。
- ✅ **可以任意决定返回值**。
- ⚠️ **开销较大**（需要 JS ↔ Native 转换）。

### 2.2 调用原函数，但修改返回值

```javascript
const base = Module.findBaseAddress("GameAssembly.dll");
const addrIsCooldown = base.add(0x123456);
const origIsCooldown = new NativeFunction(addrIsCooldown, 'bool', ['pointer']);

Interceptor.replace(addrIsCooldown, new NativeCallback(function(skillPtr) {
    var original = origIsCooldown(skillPtr);
    // 如果原函数返回 true，改为 false；否则保持不变
    var result = original ? false : original;
    console.log(`原返回值=${original}, 修改后=${result}`);
    return result;
}, 'bool', ['pointer']));
```

**特点：**

- ✅ **原始函数仍会执行**（因为手动调用了 `origIsCooldown`）。
- ✅ **可以修改返回值**。
- ⚠️ **开销更大**（两次 Native → JS → Native 来回）。

------

## 对比总结（含代码行为）

| 特性               | `attach` (`onLeave`)                | `replace` (不调原函数) | `replace` (调原函数)           |
| ------------------ | ----------------------------------- | ---------------------- | ------------------------------ |
| **修改返回值**     | ✅ `retval.replace(ptr(0))`          | ✅ `return false`       | ✅ `return modified`            |
| **修改参数**       | ❌ (getter 无参，但即使有参也只能读) | ✅ 可在回调中直接改     | ✅ 可在回调中改后再调原函数     |
| **原函数是否执行** | ✅ 总是执行                          | ❌ 不执行               | ✅ 手动调用后执行               |
| **典型用途**       | 轻量修改返回值、监控                | 完全替换逻辑、绕过检查 | 需要原函数副作用但又想改返回值 |
| **性能开销**       | 低                                  | 中                     | 高                             |
| **对调用方透明性** | 透明（原函数仍运行）                | 完全透明（原函数消失） | 半透明（原函数仍运行但被包裹） |



#### Interceptor.replace 的更多用法

`Interceptor.replace` 的核心是**完全接管**一个函数的执行权。这意味着你不仅可以“屏蔽”功能，还可以“创造”功能。

------

#### 1. 完全自定义返回值 (逻辑欺骗)

这是最常用的进阶用法。你可以根据传入的参数，动态地返回不同的值，从而欺骗游戏的逻辑判断。

- **场景**：绕过VIP检查、修改金币数量、改变物品等级。
- **示例**：假设一个函数 `checkIsVIP()` 返回 `true` 或 `false`。

------

#### 2. 链接并调用原始函数 (功能增强)

你并不是非要完全抛弃原函数。你可以先调用原函数，获取它的结果，修改后再返回。这相当于给原函数打了“补丁”。

- **场景**：获取一个计算结果，然后对其进行加倍或修改。
- **关键**：在替换前，先用 `NativeFunction` 保存原始函数的指针。

这是 Frida 逆向中非常爽的一个环节——**“主动调用”**。

------

### 六、Frida 方法调用（主动调用游戏函数）

> **核心概念**：不仅能 Hook 函数，还能**主动调用**游戏里的任何函数。

#### 1. 核心代码示例

假设我们要主动调用 `PlayerData` 类中的 `AddHp` 方法，给自己增加 999 点血量。

#### 2. 两种方式对比（Native vs IL2CPP）

虽然你之前的代码多用 Native 层，但在“主动调用”这个功能上，**IL2CPP 专属方式**通常更简单直观。

| 维度         | **IL2CPP 专属方式 (推荐)**      | **Native 层方式 (硬核)**                             |
| ------------ | ------------------------------- | ---------------------------------------------------- |
| **代码风格** | `method.invoke(instance, 参数)` | `new NativeFunction(地址, 返回值, [参数类型])(参数)` |
| **难度**     | **低** (像写普通 JS 函数)       | **高** (需要手动定义参数类型，如 'int', 'pointer')   |
| **可读性**   | 高 (一眼看出是 `AddHp`)         | 低 (只能看到内存地址和十六进制数据)                  |
| **适用场景** | 只要知道类名和方法名            | 函数被混淆、或者不是标准 IL2CPP 函数时               |

#### 4. 注意事项

- **参数匹配**：调用时必须传对参数。如果函数需要 `(int amount, boolean isFull)`，你只传一个数字会报错或崩溃。
- **实例存在**：调用非静态方法时，必须确保 `playerInstance`（调用者）是有效的。如果游戏还没开始，实例为空，调用会失败。
- **返回值**：`invoke` 可能会有返回值（比如 `true` 表示加血成功），记得接收处理。





### 1. 无限弹匣 + 快速换弹 (Module 6)

**你的代码逻辑 (`game_modifier_v1.3.py`):**

```javascript
// 1. 替换 get_isInfinityAmmo
Interceptor.replace(getIsInfinityAmmoAddr, new NativeCallback(function(self) {
    return 1; // 强行返回 true
}, 'int', ['pointer']));

// 2. 替换 get_ReloadSpeed
Interceptor.replace(getReloadSpeedAddr, new NativeCallback(function(self) {
    return 2.0; // 强行返回 2.0
}, 'float', ['pointer']));
```

- **发生了什么？**
  游戏内部有一个逻辑：“如果 `get_isInfinityAmmo()` 返回 `true`，我就显示无限子弹”。
- 
- 另一个逻辑是：“把 `get_ReloadSpeed()` 的返回值拿来当换弹速度”。
  你的代码**并没有**去调用“解锁弹匣”的函数，也没有调用“加速换弹”的函数。你只是**欺骗**了游戏，让这两个**查询函数**永远返回你想要的数值（`true` 和 `2.0`）

### 2. 滑板鞋 (Module 5)

**你的代码逻辑 (`game_modifier_v1.3.py`):**

```javascript
Interceptor.replace(hookAddr, new NativeCallback(function(self, player) {
    var result = originalFn(self, player); // 先让游戏算出原本的速度
    // ... (判断是否是玩家)
    return currentSpeed; // 强行返回你设定的速度（如 3.0）
}, 'float', ['pointer', 'pointer']));
```

- **发生了什么？**
  游戏在每一帧都会去问：“这个玩家现在的速度是多少？”（通过 `PropertyModifier.Get`）。
  你的代码**并没有**调用“加速术”这个法术，而是**拦截**了游戏的询问，直接告诉它：“他的速度是 3.0”。

------

### 💡 什么是真正的“主动调用”？

真正的“主动调用”是指：**不需要游戏先问你，你自己主动去触发一个动作。**

如果这两个功能是用“主动调用”实现的，代码应该是这样的（伪代码）：

#### 场景 A：真正的“主动调用”无限子弹

你不需要修改 `get_isInfinityAmmo`，而是直接调用：

```javascript
// 假设找到了 Player 的 UnlockInfiniteAmmo() 方法
Player.UnlockInfiniteAmmo.invoke(playerInstance); 
// 这才是真正的“主动开启”一个功能
```

### 📌 总结

| 功能                      | 你的实现方式                         | 本质                                  |
| ------------------------- | ------------------------------------ | ------------------------------------- |
| **无限弹匣/快速换弹**     | **Hook & Return** (拦截并篡改返回值) | **被动欺骗** (游戏问你时撒谎)         |
| **滑板鞋**                | **Hook & Return** (拦截并篡改返回值) | **被动欺骗** (游戏问你时撒谎)         |
| **主动调用 (你之前问的)** | **Method.Invoke** (直接执行函数)     | **主动出击** (不等游戏问，直接改数据) |



### 8.5 常用 Frida API

```javascript


// NativeFunction
var func = new NativeFunction(address, returnType, argTypes)
func(arg1, arg2, ...)

// NativeCallback
var callback = new NativeCallback(function (...) { ... }, returnType, argTypes)
```

| 特性     | NativeFunction                         | NativeCallback                                    |
| -------- | -------------------------------------- | ------------------------------------------------- |
| 数据流向 | JS 发起调用                            | Native 发起调用                                   |
| 本质     | 它是 JS 里的一个函数对象               | 它是 Native 内存里的一个指针                      |
| 谁在运行 | JS 引擎在跑，但去执行了内存里的机器码  | 机器码在跑，但跳转到了 JS 引擎去执行逻辑          |
| 常见用途 | 主动调用游戏函数、系统 API             | 替换函数实现、Hook 回调、伪造返回值               |
| 你的代码 | 你之前的脚本里用得少（除非主动调函数） | 你一直在用！ (`Interceptor.replace` 的第二个参数) |

NativeFunction 就像 “遥控器”。
你（JS）手里拿着遥控器，按下按钮，电视（Native）就开始工作。是你控制它。
NativeCallback 就像 “接线员”。
你（JS）坐在电话机旁，把自己的号码留给客户（Native）。客户有事了（函数被调用），就会打电话给你，让你处理。是它控制你。













