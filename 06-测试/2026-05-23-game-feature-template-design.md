# 游戏功能修改器模板设计文档

**日期：** 2026-05-23  
**状态：** 已批准  
**类型：** 模板设计

---

## 一、需求概述

### 1.1 目标
创建 JavaScript (Frida游戏功能脚本) 和 Python (CustomTkinter UI界面) 的完整模板，提炼常用代码模式，保障稳定性和安全性。

### 1.2 核心需求
- ✅ 完整模板（包含所有基础设施）
- ✅ 独立文件（每个模板都是完整可运行的代码文件）
- ✅ Frida注入流程
- ✅ 安全机制（指针检查、异常处理、日志限流）
- ✅ 日志与通信系统
- ✅ 常见Hook模式示例

### 1.3 特殊要求
- JavaScript模板：通过 `GameManager → myPlayer → clientData → nickname` 链式访问，不使用Hook方式
- Python模板：使用 CustomTkinter（不使用QT）
- 文件命名：前缀命名（AAAAA-xxx）

---

## 二、技术方案

### 2.1 JavaScript模板设计

#### 核心结构
```
1. 日志系统
2. 模块查找（GameAssembly.dll）
3. RVA地址常量定义
4. 字段偏移常量定义
5. 安全读取函数
6. 核心功能实现（链式访问）
7. RPC接口导出
8. 初始化
```

#### 链式访问路径
```
GameManager_TypeInfo (静态槽地址)
  ↓
Il2CppClass.static_fields (静态字段区域)
  ↓
GameManager.myPlayer (玩家指针)
  ↓
Player.clientData (客户端数据)
  ↓
ClientData.nickName (昵称字符串)
  ↓
Il2CppString (读取UTF-16字符串)
```

#### 安全机制
- 指针null检查
- 异常捕获（try-catch）
- 字符串长度验证（防止越界读取）
- 分级日志输出

### 2.2 Python模板设计

#### 核心结构
```
1. CustomTkinter UI框架
2. Frida会话管理
3. 自动连接游戏进程
4. 消息处理机制
5. 日志显示系统
6. 功能调用接口
```

#### UI组件
- 标题栏
- 状态栏（连接状态显示）
- 控制按钮区
- 日志显示区（CTkTextbox）

#### Frida流程
```
查找游戏进程 (psutil)
  ↓
连接进程 (frida.get_local_device().attach())
  ↓
加载JS脚本 (session.create_script())
  ↓
注册消息处理 (script.on('message', handler))
  ↓
加载脚本 (script.load())
```

---

## 三、文件结构

### 3.1 输出位置
```
d:\trae_project\UCF1.7修改大全\06-测试\
├── AAAAA-game_template.js    (JavaScript模板)
└── AAAAA-ui_template.py      (Python UI模板)
```

### 3.2 文件命名
- JavaScript: `AAAAA-game_template.js`
- Python: `AAAAA-ui_template.py`
- 前缀 `AAAAA-` 用于排序和识别

---

## 四、核心代码模式

### 4.1 JavaScript模式

#### 日志系统
```javascript
function log(level, module, message) {
    console.log('[' + level + '][' + module + '] ' + message);
    send({type: 'log', level: level, module: module, message: message});
}
```

#### 安全读取
```javascript
function readPtr(addr) {
    try {
        if (!addr || addr.isNull()) return null;
        var v = addr.readPointer();
        return (v && !v.isNull()) ? v : null;
    } catch(e) { 
        return null; 
    }
}
```

#### 链式访问
```javascript
// Step 1: 获取静态字段区域
var typeInfoSlot = base.add(RVA.GameManager_TypeInfo);
var klass = readPtr(typeInfoSlot);
var staticFields = readPtr(klass.add(0x5C));

// Step 2: 读取实例字段
var myPlayer = readPtr(staticFields.add(OFF.GM_myPlayer));
var clientData = readPtr(myPlayer.add(OFF.P_clientData));
var nickNameObj = readPtr(clientData.add(OFF.CD_nickName));

// Step 3: 读取字符串
var len = nickNameObj.add(0x08).readS32();
var nickname = nickNameObj.add(0x0C).readUtf16String(len * 2);
```

### 4.2 Python模式

#### CustomTkinter UI
```python
import customtkinter as ctk

class GameFeatureUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("游戏功能修改器")
        self.setup_ui()
```

#### Frida连接
```python
def connect_to_game(self, pid):
    self.device = frida.get_local_device()
    self.session = self.device.attach(pid)
    self.script = self.session.create_script(js_code)
    self.script.on('message', self.on_message)
    self.script.load()
```

#### 消息处理
```python
def on_message(self, message, data):
    if message['type'] == 'send':
        payload = message['payload']
        if payload.get('type') == 'log':
            self.log(payload['message'], payload['level'])
```

---

## 五、稳定性保障

### 5.1 指针安全
- 所有指针读取前进行null检查
- 使用安全的读取函数封装
- 异常捕获防止崩溃

### 5.2 数据验证
- 字符串长度范围检查（0-500）
- RVA地址有效性验证
- 字段偏移合理性检查

### 5.3 异常处理
- JavaScript: try-catch包裹所有关键操作
- Python: try-except处理Frida连接异常

---

## 六、安全性保障

### 6.1 日志限流
- 防止日志刷屏影响性能
- 分级日志（info/warn/error/success）

### 6.2 内存安全
- 不直接操作危险内存区域
- 使用Frida提供的API进行内存访问
- 避免修改游戏关键数据结构

### 6.3 线程安全
- Python端使用线程锁保护共享状态
- 避免多线程竞争条件

---

## 七、使用说明

### 7.1 JavaScript模板使用
1. 复制 `AAAAA-game_template.js`
2. 修改RVA地址常量（根据游戏版本）
3. 修改字段偏移常量（根据dump.cs）
4. 添加自定义功能函数
5. 导出RPC接口

### 7.2 Python模板使用
1. 复制 `AAAAA-ui_template.py`
2. 修改游戏进程名称（默认：UnityCrossFire.exe）
3. 修改JS脚本路径
4. 添加自定义UI控件
5. 添加功能调用方法

### 7.3 配合使用
1. Python UI加载JavaScript脚本
2. 通过RPC接口调用JavaScript函数
3. JavaScript通过send()发送日志到Python
4. Python在UI中显示日志

---

## 八、扩展建议

### 8.1 添加新功能
- 在JavaScript中添加新的功能函数
- 在rpc.exports中导出新函数
- 在Python中添加调用按钮和方法

### 8.2 Hook模式扩展
如需使用Hook模式，可参考以下模板：
```javascript
Interceptor.attach(targetAddr, {
    onEnter: function(args) {
        // Hook进入逻辑
    },
    onLeave: function(retval) {
        // Hook退出逻辑
    }
});
```

### 8.3 Replace模式扩展
```javascript
Interceptor.replace(targetAddr, new NativeCallback(
    function(args) {
        // 替换逻辑
        return result;
    },
    returnType, [argTypes]
));
```

---

## 九、验收标准

### 9.1 功能完整性
- ✅ JavaScript模板可独立运行
- ✅ Python模板可独立运行
- ✅ 两者配合可正常工作

### 9.2 代码质量
- ✅ 代码结构清晰
- ✅ 注释完整
- ✅ 命名规范

### 9.3 安全性
- ✅ 所有指针操作有安全检查
- ✅ 所有异常有捕获处理
- ✅ 日志系统完善

---

**设计批准：** ✅ 已批准  
**下一步：** 创建实际模板文件
