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

```bash
# 下载 Python 3.8+
# https://www.python.org/downloads/

# 验证安装
python --version
```

### 2.2 安装 Frida 工具

```bash
# 安装 frida-tools（包含 frida 命令行工具和 Python 绑定）
pip install frida-tools -i https://pypi.tuna.tsinghua.edu.cn/simple

# 验证安装
frida --version
python -c "import frida; print(frida.__version__)"
```

### 2.3 安装 PyInstaller

```bash
# 安装打包工具
pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple

# 验证安装
pyinstaller --version
```

### 2.4 安装 Il2CppDumper（可选，用于游戏分析）

```bash
# 下载 Il2CppDumper
# https://github.com/Perfare/Il2CppDumper/releases

# 使用方法：
# 1. 提取游戏的 GameAssembly.dll 和 global-metadata.dat
# 2. 运行 Il2CppDumper.exe
# 3. 选择 GameAssembly.dll
# 4. 选择 global-metadata.dat
# 5. 输出 dump.cs 和 script.json
```

---

## 三、游戏分析流程

### 3.1 提取游戏文件

```bash
# 游戏路径示例
游戏目录/
├── UnityCrossFire.exe          # 游戏主程序
├── UnityCrossFire_Data/
│   ├── global-metadata.dat     # IL2CPP 元数据
│   └── ...
└── GameAssembly.dll            # IL2CPP 编译后的代码
```

### 3.2 使用 Il2CppDumper 分析

```bash
# 运行 Il2CppDumper
Il2CppDumper.exe

# 选择文件：
# 1. GameAssembly.dll
# 2. global-metadata.dat

# 输出文件：
输出目录/
├── dump.cs          # 所有类的定义
├── script.json      # 方法地址映射
└── ...
```

### 3.3 分析 dump.cs

#### 3.3.1 查找目标类

```bash
# 搜索类定义
grep "class ClassName" dump.cs

# 示例：查找 Recoil 类
grep "class Recoil" dump.cs
```

#### 3.3.2 查找目标方法

```bash
# 搜索方法定义
grep "MethodName()" dump.cs

# 示例：查找 OnGunShot 方法
grep "OnGunShot()" dump.cs
```

#### 3.3.3 查看字段偏移

```csharp
// 示例：Recoil 类字段
public class Recoil : MonoBehaviour
{
    private float <addYaw>k__BackingField; // 0x68  ← 字段偏移
    private float <addPitch>k__BackingField; // 0x6C
    private float addYaw_Target; // 0x70
    private float addPitch_Target; // 0x74
}
```

### 3.4 分析 script.json

```json
{
  "ScriptMethod": [
    {
      "Address": 11635072,  // 十进制地址
      "Name": "Recoil$$OnGunShot",
      "Signature": "void Recoil__OnGunShot (Recoil_o* __this, const MethodInfo* method);"
    }
  ]
}
```

**地址转换**：
```
十进制：11635072
十六进制：0xB19980
RVA 地址：0xB19980（用于 Frida）
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

```python
# launcher.py
import frida
import sys
import os
import time
import threading

# 1. 读取 JS 脚本
def get_js_code():
    # PyInstaller 打包时，资源文件路径会变为 sys._MEIPASS
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    
    js_file = os.path.join(base_path, 'script.js')
    with open(js_file, 'r', encoding='utf-8') as f:
        return f.read()

# 2. 消息处理
def on_message(message, data):
    if message['type'] == 'send':
        print(f"[+] {message['payload']}")
    elif message['type'] == 'error':
        print(f"[-] {message['stack']}")

# 3. 主逻辑
def main():
    TARGET_PROCESS = "Game.exe"
    
    print("=" * 50)
    print("  No Recoil Launcher")
    print("=" * 50)
    
    script_code = get_js_code()
    current_session = None
    current_script = None
    
    def inject_script():
        nonlocal current_session, current_script
        
        try:
            print(f"\n[*] 查找进程：{TARGET_PROCESS}...")
            current_session = frida.attach(TARGET_PROCESS)
            print(f"[+] 附加成功：{TARGET_PROCESS}")
            
            current_script = current_session.create_script(script_code)
            current_script.on('message', on_message)
            current_script.load()
            print("[+] 注入成功！")
            
        except frida.ProcessNotFoundError:
            print(f"[-] 找不到进程 {TARGET_PROCESS}")
            return False
        except Exception as e:
            print(f"[-] 错误：{e}")
            return False
        
        return True
    
    # 注入
    while not inject_script():
        time.sleep(3)
    
    # 保持运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] 退出中...")
        if current_script:
            current_script.unload()
        if current_session:
            current_session.detach()
        print("[*] 已退出")

if __name__ == '__main__':
    main()
```

### 5.2 创建打包脚本

```batch
@echo off
chcp 65001 >nul
title Package Launcher

echo.
echo ==========================================
echo    Package Launcher
echo ==========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found.
    pause
    exit /b 1
)

echo Step 1: Checking Python... OK

echo.
echo Step 2: Checking frida-tools...
python -c "import frida" >nul 2>&1
if errorlevel 1 (
    echo Installing frida-tools...
    pip install frida-tools -i https://pypi.tuna.tsinghua.edu.cn/simple
) else (
    echo frida-tools OK
)

echo.
echo Step 3: Installing PyInstaller...
pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo Step 4: Packaging...
echo.

pyinstaller --onefile --add-data "script.js;." --hidden-import=frida.core --name "Launcher" launcher.py

echo.
echo ==========================================
if exist "dist\Launcher.exe" (
    echo SUCCESS - Packaging Complete!
    echo Output: dist\Launcher.exe
    echo ==========================================
    pause
    exit /b 0
) else (
    echo ERROR - Packaging failed
    echo ==========================================
    pause
    exit /b 1
)
```

### 5.3 执行打包

```bash
# 运行打包脚本
.\package.bat

# 输出文件
dist/
└── Launcher.exe  ← 约 50MB，包含所有依赖
```

### 5.4 打包参数说明

| 参数 | 说明 |
|------|------|
| `--onefile` | 打包为单文件 EXE |
| `--add-data "script.js;."` | 嵌入 JS 脚本（Windows 用 `;`，Linux/Mac 用 `:`） |
| `--hidden-import=frida.core` | 隐藏导入 frida 核心模块 |
| `--name "Launcher"` | 输出文件名 |

### 5.5 路径处理（关键）

```python
# PyInstaller 打包后，资源文件路径会变化
if getattr(sys, 'frozen', False):
    # 打包后：使用 sys._MEIPASS
    base_path = sys._MEIPASS
else:
    # 脚本模式：使用脚本所在目录
    base_path = os.path.dirname(__file__)

js_file = os.path.join(base_path, 'script.js')
```

---

## 六、常见问题与解决方案

### 6.1 游戏崩溃

**症状**：注入后游戏秒退

**原因**：
1. 指针类型不匹配
2. 调用了错误的函数
3. 内存访问违规

**解决方案**：
```javascript
// ❌ 错误：指针类型不匹配
var Player_get_isMyPlayer = new NativeFunction(...);
Player_get_isMyPlayer(recoilPtr, ptr(0));  // recoilPtr 是 Recoil*，不是 Player*

// ✅ 正确：使用匹配的指针类型
// 或放弃调用，直接操作内存
```

### 6.2 掉帧严重

**症状**：注入后游戏帧率下降 30%+

**原因**：使用了 `Interceptor.attach` 而非 `replace`

**解决方案**：
```javascript
// ❌ 错误：使用 attach（性能差）
Interceptor.attach(ADDR, {
    onEnter: function (args) { ... }
});

// ✅ 正确：使用 replace（性能好）
Interceptor.replace(
    ADDR,
    new NativeCallback(function (...) { ... }, "void", ["pointer", "pointer"])
);
```

### 6.3 换房间失效

**症状**：第一局有效，换房间后失效

**原因**：缓存的指针失效，新对象未识别

**解决方案**：
```javascript
// ✅ 使用缓存策略
var playerRecoilSet = {};

function isPlayerRecoil(recoilPtr) {
    var key = recoilPtr.toString();
    if (playerRecoilSet[key]) return true;
    
    var count = Object.keys(playerRecoilSet).length;
    if (count < 2) {
        playerRecoilSet[key] = true;
        return true;
    }
    
    return false;
}
```

### 6.4 打包后找不到 JS 文件

**症状**：运行 EXE 提示找不到 script.js

**原因**：路径处理错误

**解决方案**：
```python
# ✅ 正确的路径处理
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

js_file = os.path.join(base_path, 'script.js')
```

### 6.5 打包失败

**症状**：PyInstaller 报错

**常见错误**：
1. `--add-data` 参数格式错误
2. 缺少隐藏导入
3. 文件不存在

**解决方案**：
```batch
# ✅ 正确格式（Windows）
pyinstaller --onefile --add-data "script.js;." --hidden-import=frida.core --name "Launcher" launcher.py

# ✅ 正确格式（Linux/Mac）
pyinstaller --onefile --add-data "script.js:" --hidden-import=frida.core --name "Launcher" launcher.py
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

### 7.2 玩家识别

| 方法 | 适用场景 | 可靠性 |
|------|---------|--------|
| **调用游戏 API** | 指针类型匹配时 | 高 |
| **缓存前 N 个对象** | 玩家对象先创建时 | 中 |
| **特征码匹配** | 有固定特征时 | 高 |

### 7.3 内存修改

| 操作 | 方法 | 注意事项 |
|------|------|---------|
| **读取 float** | `ptr.add(offset).readFloat()` | 确认偏移正确 |
| **写入 float** | `ptr.add(offset).writeFloat(value)` | 确认类型匹配 |
| **读取 int** | `ptr.add(offset).readInt()` | 注意符号 |
| **写入 int** | `ptr.add(offset).writeInt(value)` | 注意范围 |

### 7.4 打包发布

| 实践 | 说明 |
|------|------|
| **使用 `--onefile`** | 单文件 EXE，便于分发 |
| **嵌入所有资源** | 使用 `--add-data` |
| **隐藏导入** | 使用 `--hidden-import` |
| **测试打包后文件** | 确保路径正确 |
| **提供使用说明** | 编写 README.md |

---

## 八、附录：完整命令参考

### 8.1 Frida 命令

```bash
# 列出进程
frida-ls-devices

# 附加到进程
frida -p <PID>
frida -n "ProcessName"

# 加载脚本
frida -p <PID> -l script.js

# 自动重新加载（开发用）
frida -p <PID> -l script.js --reload

# 查看模块
frida -p <PID> -e "Process.enumerateModules()"

# 查看内存范围
frida -p <PID> -e "Process.enumerateRanges('r--')"
```

### 8.2 Python 命令

```bash
# 安装 frida-tools
pip install frida-tools

# 安装 PyInstaller
pip install pyinstaller

# 查看 frida 版本
python -c "import frida; print(frida.__version__)"

# 查看 PyInstaller 版本
pyinstaller --version
```

### 8.3 PyInstaller 命令

```bash
# 基础打包
pyinstaller --onefile script.py

# 嵌入数据文件
pyinstaller --onefile --add-data "data.txt;." script.py

# 隐藏导入
pyinstaller --onefile --hidden-import=module.name script.py

# 指定图标
pyinstaller --onefile --icon=icon.ico script.py

# 指定名称
pyinstaller --onefile --name "MyApp" script.py

# 完整示例
pyinstaller --onefile --add-data "script.js;." --hidden-import=frida.core --name "Launcher" launcher.py
```

### 8.4 地址转换

```python
# 十进制转十六进制
dec = 11635072
hex_addr = hex(dec)  # 0xb19980

# 十六进制转十进制
hex_addr = 0xB19980
dec = int(hex_addr)  # 11635072
```

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

---

## 📚 参考资源

| 资源 | 链接 |
|------|------|
| **Frida 官方文档** | https://frida.re/docs/ |
| **Frida API 参考** | https://frida.re/docs/javascript-api/ |
| **Il2CppDumper** | https://github.com/Perfare/Il2CppDumper |
| **PyInstaller 文档** | https://pyinstaller.org/ |
| **Python 官方文档** | https://docs.python.org/3/ |

---

## 📝 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| V1.0 | 2026-04-23 | 初始版本，包含完整技术栈、开发流程、打包流程 |

---

**本手册为 Frida 游戏修改的完整技术参考，适用于 Unity IL2CPP 游戏的内存修改和功能开发。**
