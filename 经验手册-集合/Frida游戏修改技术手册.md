# 🔧 Frida 游戏修改技术手册

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

```bash

```

#### 3.3.2 查找目标方法

```bash

```

#### 3.3.3 查看字段偏移

```csharp

```

### 3.4 分析 script.json

```json

```

**地址转换**：
```

```

---

## 四、Frida 脚本开发

### 4.1 基础脚本结构

```javascript
// 脚本名称：no_recoil.js
// 使用方法：frida -p <PID> -l no_recoil.js

console.log("[*] 脚本启动...");

(function () {
    // 1. 查找 GameAssembly.dll
    var gameAssembly = Process.findModuleByName("GameAssembly.dll");
    
    if (!gameAssembly) {
        console.log("[-] GameAssembly.dll not found!");
        return;
    }

    // 2. 计算目标地址
    var ADDR_TARGET = gameAssembly.base.add(0xB19980);  // RVA 地址

    console.log("[*] Target @ " + ADDR_TARGET);

    // 3. Hook 目标函数
    Interceptor.replace(
        ADDR_TARGET,
        new NativeCallback(function (thisPtr, methodInfo) {
            // 自定义逻辑
            console.log("[+] Target called @ " + thisPtr);
            
            // 不执行原函数（跳过）
        }, "void", ["pointer", "pointer"])
    );

    console.log("[+] Hook successful!");
})();
```

### 4.2 Interceptor 用法对比

| 方法 | 用途 | 性能 | 适用场景 |
|------|------|------|---------|
| `Interceptor.attach` | 监听函数调用 | 中 | 调试、日志 |
| `Interceptor.replace` | 替换函数实现 | 优 | 修改行为、跳过函数 |

#### 4.2.1 Interceptor.attach（监听）

```javascript
Interceptor.attach(ADDR_TARGET, {
    onEnter: function (args) {
        // 函数进入时
        console.log("[+] Enter: " + args[0]);
    },
    onLeave: function (retval) {
        // 函数返回时
        console.log("[+] Leave: " + retval);
    }
});
```

#### 4.2.2 Interceptor.replace（替换）

```javascript
// 保存原函数
var OriginalFunc = new NativeFunction(
    ADDR_TARGET,
    "void",  // 返回类型
    ["pointer", "pointer"]  // 参数类型
);

// 替换函数
Interceptor.replace(
    ADDR_TARGET,
    new NativeCallback(function (thisPtr, methodInfo) {
        // 自定义逻辑
        
        // 可选：调用原函数
        // OriginalFunc(thisPtr, methodInfo);
        
        // 或跳过原函数（直接返回）
    }, "void", ["pointer", "pointer"])
);
```

### 4.3 内存读写

```javascript
// 读取内存
var value = ptr.add(0x68).readFloat();  // 读取 float
var intValue = ptr.add(0x10).readInt(); // 读取 int

// 写入内存
ptr.add(0x68).writeFloat(0.0);  // 写入 float
ptr.add(0x10).writeInt(9999);   // 写入 int
```

### 4.4 调用游戏函数

```javascript
// 创建 NativeFunction
var GameFunc = new NativeFunction(
    gameAssembly.base.add(0xB55FD0),  // 地址
    "bool",  // 返回类型
    ["pointer", "pointer"]  // 参数类型
);

// 调用函数
var result = GameFunc(thisPtr, ptr(0));
console.log("[+] Result: " + result);
```

### 4.5 调试技巧

```javascript
// 1. 打印指针信息
console.log("[+] Pointer: " + ptr);
console.log("[+] IsNull: " + ptr.isNull());

// 2. 检查指针可读性
function isReadablePointer(p) {
    if (!p || p.isNull()) return false;
    try {
        return Process.findRangeByAddress(p) !== null;
    } catch (e) {
        return false;
    }
}

// 3. 限制日志输出
var logCount = 0;
var logLimit = 20;

if (logCount < logLimit) {
    console.log("[Log " + (logCount+1) + "] ...");
    logCount++;
}
```

---

## 五、打包发布流程

### 5.1 创建 Python 启动器

### 5.2 创建打包脚本

### 5.3 执行打包

---

## 六、常见问题与解决方案

### 6.1 游戏崩溃

**症状**：注入后游戏秒退

### 6.2 掉帧严重

**症状**：注入后游戏帧率下降 30%+

**原因**：使用了 `Interceptor.attach` 而非 `replace`

### 6.3 换房间失效

**症状**：第一局有效，换房间后失效

**原因**：缓存的指针失效，新对象未识别

**解决方案**：

```javascript
// ✅ 使用缓存策略
```

---

## 七、最佳实践

### 7.1 脚本开发

| 实践 | 说明 |
|------|------|
| **优先使用 `replace`** | 性能优于 `attach` |
| **限制日志输出** | 避免日志刷屏影响性能 |
| **检查指针有效性** | 避免空指针崩溃 |
| **使用 RVA 地址** | 游戏更新后只需更新地址 |
| **查看 dump.cs** | 理解类结构和字段偏移 |

7.3 内存修改

| 操作 | 方法 | 注意事项 |
|------|------|---------|
| **读取 float** | `ptr.add(offset).readFloat()` | 确认偏移正确 |
| **写入 float** | `ptr.add(offset).writeFloat(value)` | 确认类型匹配 |
| **读取 int** | `ptr.add(offset).readInt()` | 注意符号 |
| **写入 int** | `ptr.add(offset).writeInt(value)` | 注意范围 |



### 8.5 常用 Frida API

```javascript
// 进程
Process.findModuleByName("GameAssembly.dll")
Process.enumerateModules()
Process.enumerateRanges('r--')

// 内存
ptr.add(offset).readFloat()
ptr.add(offset).writeFloat(value)
ptr.add(offset).readInt()
ptr.add(offset).writeInt(value)

// 拦截器
Interceptor.attach(address, { onEnter, onLeave })
Interceptor.replace(address, callback)
Interceptor.revert(address)

// NativeFunction
var func = new NativeFunction(address, returnType, argTypes)
func(arg1, arg2, ...)

// NativeCallback
var callback = new NativeCallback(function (...) { ... }, returnType, argTypes)
```

