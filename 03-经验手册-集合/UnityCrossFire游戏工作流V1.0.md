# UnityCrossFire 游戏修改工作流 V1.0

> **适用游戏**: UnityCrossFire（穿越火线高清版）  
> **技术栈**: Unity + IL2CPP + Frida + Il2CppDumper + IDA Pro + MCP  
> **更新日期**: 2026-05-08  
> **作者**: 个人开发使用

---

## 目录

1. [工作流总览](#一工作流总览)
2. [阶段一：需求分析](#二阶段一需求分析)
3. [阶段二：游戏分析](#三阶段二游戏分析)
4. [阶段三：脚本开发](#四阶段三脚本开发)
5. [阶段四：Python 可视化界面开发](#五阶段四python-可视化界面开发)
6. [阶段五：测试验证](#六阶段五测试验证)
7. [阶段六：打包发布](#七阶段六打包发布)
8. [阶段七：版本管理](#八阶段七版本管理)
9. [常见问题与解决方案](#九常见问题与解决方案)
10. [附录：核心原则](#十附录核心原则)

---

## 一、工作流总览

```
需求分析 → 游戏分析 → 脚本开发 → Python UI开发 → 测试验证 → 打包发布 → 版本管理
    ↓          ↓          ↓          ↓              ↓          ↓          ↓
明确目标   dump.cs    Frida脚本   CustomTkinter  全模式测试   Python+EXE   Git管理
IDA反编译  找类方法   日志调试   可视化界面     区分玩家Bot  整合包更新   dev/main
```

### 核心工具分工

| 工具 | 给我什么 | 什么时候用 |
|------|---------|-----------|
| **dump.cs** | 类名、字段偏移、方法签名 | 找类和字段结构 |
| **script.json** | 方法 RVA 地址 | 找函数地址 |
| **IDA Pro MCP** | 方法的真实代码逻辑 | 看函数内部在干什么 |
| **Frida** | 动态插桩、内存修改 | 实现修改功能 |
| **CustomTkinter** | Python 可视化界面 | 替代命令行，一键操作 |
| **Python+PyInstaller** | 打包成EXE | 分发给用户 |

---

## 二、阶段一：需求分析

### 2.1 明确功能目标

用大白话写下你要做什么：

```
我要实现 {功能描述}
例如：扩大刀具攻击范围。

### 2.2 需求拆解

将大目标拆分为具体步骤：

```
目标：扩大刀具攻击范围

步骤1：找到刀具攻击范围的字段/方法
步骤2：区分玩家和人机的攻击范围
步骤3：只修改玩家的攻击范围
步骤4：应用到所有模式
步骤5：切换房间不崩溃
```

### 2.3 确认技术要求

必须满足以下要求：

- [ ] 全模式适配（团队、爆破、个人、生化等）
- [ ] 区分玩家和Bot（只对自己生效）
- [ ] 主武器、副武器、所有背包武器都生效
- [ ] 切换房间/重新进房间不崩溃
- [ ] 遵守游戏逻辑，不破坏游戏流程
- [ ] 32位游戏，注意指针和内存操作
- [ ] 线程安全，不影响游戏性能

### 2.4 参考已有成功代码

- 查看（正式发行版）文件夹里面的（game_modifier_v1.3.py）的功能，这些功能已经验证可用的代码
- 后续对话都要记住参考这些代码

---

## 三、阶段二：游戏分析

### 3.1 在 dump.cs 中搜索目标

```
搜索关键词：
1. 类名包含 {关键词} 的类
2. 方法名包含 {关键词} 的方法
3. 字段名包含 {关键词} 的字段
4. 列出找到的类、方法、字段的 RVA 地址
```

### 3.2 分析类继承关系

```
找到目标类后：
1. 看这个类继承自谁
2. 画出继承链
3. 找到关键字段的偏移（offset）
4. 找到操作这些字段的方法
```
先不要生成代码，执行代码，先告诉我思路。

生成内容放在01-测试版文件夹，创建md格式文件。

检查内容，然后再补充完善md文档。




### 3.3 使用 IDA Pro MCP 反编译

**这是最关键的一步！从"猜代码逻辑"变成"读代码逻辑"**

```
操作步骤：
1. 在 script.json 中找到方法的 RVA 地址
2. 用 IDA MCP 反编译该地址
3. 查看函数的真实流程
4. 确认字段偏移是否正确
5. 找到隐藏的约束条件
6. 看清调用关系
```

**IDA 反编译能做到的 5 件事：**

| 能力 | 具体操作 | 实例 |
|------|---------|------|
| 看函数的真实流程 | `decompile_function(地址)` | 发现 GetAttribute 里先 Parse 再匹配 |
| 确认字段偏移是否正确 | 反编译里看到 `a1 + 216` = 0xD8 | 确认 attributeAsset 在 0xD8 |
| 找到隐藏的约束条件 | 代码里 `if (人数 < 8)` | 以前根本不知道有这个限制 |
| 看清调用关系 | `get_callees(地址)` | 看到 OnStartNewGameRound 调了哪些子函数 |
| 验证推测是否正确 | 把之前猜的逻辑跟反编译对比 | 推测被 100% 证实 |


---

## 四、阶段三：脚本开发

### 4.1 选择 Frida 修改方式

| 场景 | 用什么 | 示例 |
|------|--------|------|
| 只看看函数何时被调、传了什么参数 | `Interceptor.attach` | 调试追踪 |
| 阻止原函数，换成自己的逻辑 | `Interceptor.replace` | 无后座力、无限时间 |
| 主动调游戏函数 | `NativeFunction` | 英雄变身、加 Buff |

### 4.2 每次修改前三问

1. 我要拦截什么函数？ → 决定 attach 还是 replace
2. 原函数还要不要执行？ → 要=attach，不要=replace
3. 这个函数每帧都调用吗？ → 是的话 attach 可能掉帧，replace 不会

### 4.3 脚本开发规范

```javascript
// 标准脚本结构
(function () {
    // 1. 查找 GameAssembly.dll
    var gameAssembly = Process.findModuleByName("GameAssembly.dll");
    if (!gameAssembly) {
        console.log("[-] GameAssembly.dll not found!");
        return;
    }

    // 2. 计算目标地址
    var ADDR_TARGET = gameAssembly.base.add(0xXXXXXX);

    // 3. 玩家识别（必须）
    // 使用 isMyWeapon / isMyPlayer 或缓存策略

    // 4. Hook 目标函数
    Interceptor.replace(
        ADDR_TARGET,
        new NativeCallback(function (thisPtr, methodInfo) {
            // 自定义逻辑
            // 不执行原函数（如果需要）
        }, "void", ["pointer", "pointer"])
    );

    // 5. 清理机制（切换房间不崩溃）
    // Hook OnDestroy 清空缓存
})();
```

### 4.4 关键地址速查

| 方法 | RVA | 用途 |
|------|-----|------|
| `Weapon.get_isMyWeapon` | `0xB6E1D0` | 是不是我的枪 |
| `Player.get_isMyPlayer` | `0xB55FD0` | 是不是我本人 |
| `Entity.AddBuff` | `0xB3FA40` | 加 Buff |
| `Entity.SetDamageRate` | `0xB3F730` | 增伤/减伤 |
| `ModeBase.UpdateTimeUI` | `0xAF6930` | 刷新时间（全模式） |

### 4.5 开发注意事项

- **优先使用 `Interceptor.replace`**：性能优于 `attach`
- **限制日志输出**：避免日志刷屏影响性能
- **检查指针有效性**：避免空指针崩溃
- **使用 RVA 地址**：游戏更新后只需更新地址
- **不要自己转换单位**：使用 `int_convert` 工具
- **尽可能避免在 Hook 里调用复杂函数**：优先直接读字段

---

## 五、阶段四：Python 可视化界面开发

### 5.1 为什么需要 Python UI 界面

- **命令行启动很麻烦**：每次都要输入 `frida -p <PID> -l script.js`
- **可视化更方便**：一键连接、一键操作、实时状态显示
- **用户体验更好**：傻瓜式操作，避免错误操作
- **日志实时显示**：方便调试和问题排查

### 5.2 Python UI 标准架构

**核心依赖：**

```
customtkinter  # UI 框架
frida-tools    # Frida Python 绑定
psutil         # 进程查找（可选）
```

**标准 UI 结构：**

```python
import customtkinter as ctk
import frida
import threading
import time
import json
import os
from datetime import datetime

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

JS_FILE = os.path.join(os.path.dirname(__file__), "功能脚本.js")

class 功能App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("功能名称 v1.0")
        self.geometry("550x650")
        
        self.session = None
        self.script = None
        self.is_connected = False
        
        self.setup_ui()
        self.after(800, self._auto_connect_thread)
    
    def setup_ui(self):
        # 1. 标题栏
        # 2. 状态栏（连接状态、PID）
        # 3. 信息面板（实时数据）
        # 4. 操作按钮
        # 5. 日志区域
    
    def _auto_connect_thread(self):
        threading.Thread(target=self.connect_to_game, daemon=True).start()
    
    def connect_to_game(self):
        # 1. 查找游戏进程
        # 2. 附加 Frida
        # 3. 加载 JS 脚本
        # 4. 安装 Hook
    
    def on_message(self, message, data):
        # 处理 JS 发来的消息
    
    def on_closing(self):
        # 清理资源
        if self.script:
            try: self.script.unload()
            except: pass
        if self.session:
            try: self.session.detach()
            except: pass
        self.destroy()

if __name__ == "__main__":
    app = 功能App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
```

### 5.3 UI 界面标准组件

**1. 状态栏（必须）**

```python
# 显示连接状态、游戏进程名、PID
status_frame = ctk.CTkFrame(self, corner_radius=8, fg_color="#1a1a2e")
self.status_dot = ctk.CTkLabel(status_frame, text="⚫", font=ctk.CTkFont(size=18))
self.status_label = ctk.CTkLabel(status_frame, text="等待游戏启动...", font=ctk.CTkFont(size=14))
self.pid_label = ctk.CTkLabel(status_frame, text="", font=ctk.CTkFont(size=11), text_color="#888")
```

**2. 信息面板（可选）**

```python
# 显示实时数据（回合数、剩余时间、已跳过次数等）
info_frame = ctk.CTkFrame(self, corner_radius=8, fg_color="#16213e")
self.round_label = ctk.CTkLabel(info_frame, text="--", font=ctk.CTkFont(size=13, weight="bold"))
self.time_label = ctk.CTkLabel(info_frame, text="--:--", font=ctk.CTkFont(size=13, weight="bold"))
```

**3. 操作按钮（必须）**

```python
# 主操作按钮
self.action_btn = ctk.CTkButton(
    self, text="▶ 执行功能",
    font=ctk.CTkFont(size=18, weight="bold"),
    fg_color="#2ecc71", hover_color="#27ae60",
    height=52, corner_radius=10,
    command=self.on_action,
    state="disabled"  # 未连接时禁用
)

# 辅助按钮（可选）
self.refresh_btn = ctk.CTkButton(self, text="🔄 刷新状态", command=self.refresh)
self.diag_btn = ctk.CTkButton(self, text="🔍 诊断", command=self.diag)
```

**4. 日志区域（必须）**

```python
# 实时显示日志
self.log_text = ctk.CTkTextbox(
    self, font=ctk.CTkFont(size=11, family="Consolas"),
    fg_color="#0a0a0a", text_color="#e0e0e0", corner_radius=6
)

# 日志方法
def _safe_log(self, msg):
    self.after(0, self._do_log, msg)

def _do_log(self, msg):
    t = datetime.now().strftime("%H:%M:%S")
    entry = "[" + t + "] " + msg + "\n"
    self.log_text.configure(state="normal")
    self.log_text.insert("end", entry)
    self.log_text.see("end")
    self.log_text.configure(state="disabled")
```

### 5.4 进程查找方法

**方法 1：Frida 枚举进程**

```python
def connect_to_game(self):
    self.device = frida.get_local_device()
    target_process = None
    for proc in self.device.enumerate_processes():
        pname = proc.name.lower()
        if "unity" in pname or "crossfire" in pname:
            target_process = proc
            break
    
    if not target_process:
        self._safe_log("未找到游戏进程")
        return
    
    self.session = self.device.attach(target_process.pid)
```

**方法 2：psutil 查找进程**

```python
import psutil

def _find_pid(self):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            name = (proc.info['name'] or '').lower()
            if 'unitycrossfire' in name:
                return proc.info['pid']
        except Exception:
            pass
    return None
```

### 5.5 JS 与 Python 交互

**JS 端导出函数：**

```javascript
// 在 JS 脚本末尾添加
rpc.exports = {
    install: function() {
        // 安装 Hook
        return { ok: true };
    },
    getstatus: function() {
        // 返回状态
        return { ok: true, count: skipCount };
    },
    skipround: function() {
        // 执行功能
        return { ok: true, reason: "" };
    }
};
```

**Python 端调用：**

```python
# 同步调用
result = self.script.exports_sync.install()
result = self.script.exports_sync.getstatus()
result = self.script.exports_sync.skipround()

# 处理结果
if result.get("ok"):
    self._safe_log("成功")
else:
    self._safe_log("失败: " + result.get("error", ""))
```

**JS 发送消息到 Python：**

```javascript
// JS 端发送
send({
    type: "round_skipped",
    from: oldValue,
    count: skipCount
});

// Python 端接收
def on_message(self, message, data):
    if message["type"] == "send":
        payload = message["payload"]
        if isinstance(payload, dict):
            msg_type = payload.get("type", "")
            if msg_type == "round_skipped":
                self._safe_log("跳过成功")
```

### 5.6 自动连接机制

```python
def _auto_connect_thread(self):
    """后台线程自动检测游戏进程"""
    threading.Thread(target=self.connect_to_game, daemon=True).start()

def connect_to_game(self):
    """循环检测游戏进程"""
    while not self.is_connected:
        pid = self._find_pid()
        if pid:
            self._log(f"检测到游戏进程 PID={pid}")
            self._connect_to_pid(pid)
            break
        time.sleep(3)

def _connect_to_pid(self, pid):
    """连接到指定进程"""
    try:
        self.session = frida.attach(pid)
        with open(JS_FILE, "r", encoding="utf-8") as f:
            js_code = f.read()
        self.script = self.session.create_script(js_code)
        self.script.on("message", self.on_message)
        self.script.load()
        self.is_connected = True
        self._safe_log("✓ 已连接")
    except Exception as e:
        self._safe_log("连接失败: " + str(e))
```

### 5.7 状态轮询机制

```python
def _start_status_polling(self):
    """启动状态轮询"""
    self._polling = True
    threading.Thread(target=self._poll_loop, daemon=True).start()

def _poll_loop(self):
    """轮询循环"""
    while self._polling and self.is_connected and self.script:
        try:
            status = self.script.exports_sync.getstatus()
            if status.get("ok"):
                # 更新 UI
                self._update_info_display()
        except Exception:
            pass
        time.sleep(0.5)

def _update_info_display(self):
    """更新 UI 显示"""
    self.after(0, self._do_update_info)

def _do_update_info(self):
    """在主线程更新 UI"""
    self.round_label.configure(text=str(current_round))
    self.time_label.configure(text=rest_time)
```

### 5.8 清理机制

```python
def on_closing(self):
    """窗口关闭时清理资源"""
    self._stop_status_polling()
    if self.script:
        try: self.script.unload()
        except: pass
    if self.session:
        try: self.session.detach()
        except: pass
    self.destroy()

# 注册关闭事件
app.protocol("WM_DELETE_WINDOW", app.on_closing)
```

### 5.9 PyInstaller 打包要求

```
打包要求：
1. 包含所有依赖，嵌入到EXE中
2. 检查文件大小大概在50MB左右
3. 避免缺少运行环境的问题
4. 测试EXE是否能正常运行
5. JS 文件需要一起打包（使用 --add-data）
```

**打包脚本示例：**

```batch
pyinstaller --onefile ^
    --add-data "功能脚本.js;." ^
    --hidden-import=frida.core ^
    --hidden-import=customtkinter ^
    --name "功能名称" launcher.py
```

**获取资源文件路径（支持打包后）：**

```python
def get_resource_path(relative_path):
    """获取资源文件路径，支持 PyInstaller 打包"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

JS_PATH = get_resource_path("功能脚本.js")
```

### 5.10 参考示例

- `正式功能\10-跳过回合\AAAAA-skip_round_ui.py` - 回合跳过器 UI
- `正式功能\09-跳高+失重\AAAAA-gravity_modifier_ui-v2.py` - 重力修改器 UI
- `正式功能\08-聚怪\AAAAA-bot_to_spawn_v24.py` - Bot 集合器 UI

---

## 六、阶段五：测试验证

### 6.1 测试清单

每次开发完功能，必须测试以下项目：

- [ ] **全模式适用**：团队、爆破、个人、生化等所有模式
- [ ] **区分玩家和人机**：只对自己生效，不影响Bot
- [ ] **主武器、副武器、捡来的武器**：所有武器都生效
- [ ] **切换房间、重新进房间**：不崩溃，功能继续生效
- [ ] **多试验几把枪**：因为有时只有前面几个生效
- [ ] **刀的速度和距离同时开启**：检查是否冲突
- [ ] **性能测试**：不掉帧，不卡顿

### 6.2 日志分析

```
测试时注意观察日志：
1. 确认模式是否正确识别
2. 确认玩家和Bot是否正确区分
3. 确认功能是否生效
4. 确认是否有异常报错
```

### 6.3 验证执行到位

```
重要：AI执行步骤后，需要检测他到底干了什么

1. 检测执行到没到位
2. 有时AI会偷偷改你已经写好的数据、写好的逻辑
3. 把js和py和集合包py发给DeepSeek去对比
4. 检查代码逻辑和数据有没有被修改
```

### 6.4 测试问题记录

遇到问题时记录：

```
问题描述：
当前版本：
测试模式：
日志信息：
已尝试的解决方案：
```

---

## 七、阶段六：打包发布

### 7.1 JS 转 Python

```
步骤：
1. 将功能js转为功能py
2. 注意：转换时可能会悄悄改代码逻辑和数值
3. 必须对比js和py的逻辑是否一致
4. 测试py文件是否正常工作
```

### 7.2 整合到 game_modifier.py

```
步骤：
1. 参考现有的 game_modifier.py
2. 在基础上新增功能，保留原有功能
3. 在选项后面放上文字解释
4. 注意：整合时也可能会修改代码逻辑
5. 用DeepSeek检查game_modifier_v1, v2之间的区别
```

### 7.3 PyInstaller 打包

```
打包要求：
1. 包含所有依赖，嵌入到EXE中
2. 检查文件大小大概在50MB左右
3. 避免缺少运行环境的问题
4. 测试EXE是否能正常运行
```

---

## 八、阶段七：版本管理

### 8.1 分支策略

```
main          ← 稳定版本（可发布的版本）
  └─ dev      ← 开发分支（日常开发用）
```

**只需要 2 个分支！**

### 8.2 日常操作流程

```
早上开始工作：
  1. git pull origin dev          ← 拉取最新代码

工作中：
  2. 修改代码
  3. git add .
  4. git commit -m "描述改动"      ← 每次有意义的改动都提交

中午/下午/下班前：
  5. git push origin dev          ← 推送到码云备份

发布新版本时：
  6. git checkout main
  7. git merge dev
  8. git tag -a v1.2 -m "版本说明"
  9. git push origin main --tags
  10. git checkout dev            ← 回到开发分支
```

### 8.3 提交频率

| 操作 | 频率 | 分支 |
|------|------|------|
| commit | 每次有意义的改动 | dev |
| push | 每天 2-3 次 | dev |
| merge 到 main | 发布新版本时 | main |
| 打标签 | 发布新版本时 | main |

### 8.4 测试版管理

```
dev 分支
  ├─ 测试版/无限时间/
  ├─ 测试版/快刀/
  └─ 正式发行版/
```

- 所有测试功能都放在 `测试版/` 文件夹下
- 功能稳定后，移动到 `正式发行版/`
- 不需要为每个小功能创建分支
- 通过 `AAAAA-` 前缀识别真正可运行的脚本

---

## 九、常见问题与解决方案

### 9.1 Hook 没效果

| 原因 | 解决 |
|------|------|
| 地址不对/函数没被调 | console.log 确认；查 RVA |
| 换模式失效 | hook 了特定模式的类，用基类方法 |
| 主武器有效副武器无效 | 只处理了主武器，用 Weapon 基类 + isMyWeapon |

### 9.2 游戏崩溃

| 原因 | 解决 |
|------|------|
| 指针类型错误 | 确认指针类型匹配 |
| 换房间闪退 | Hook OnDestroy 清空缓存 |
| NativeFunction 调用约定不明确 | 用 IDA 确认函数签名 |

### 9.3 性能问题

| 原因 | 解决 |
|------|------|
| FPS 掉帧 | 使用 Interceptor.replace 而非 attach |
| 日志刷屏 | 限制日志输出数量 |
| 慢操作在热路径 | 慢操作移出热路径 |

### 9.4 识别问题

| 原因 | 解决 |
|------|------|
| bot 也有效果 | 没过滤 isMyWeapon，每个入口都加判断 |
| 只能找到部分Bot | 使用双路径追踪（allPlayers + Bot.Update） |
| allPlayers 有 null | null 是未注册的Bot，用 Bot.Update 补全 |

### 9.5 AI 协作问题

| 问题 | 解决 |
|------|------|
| AI 多轮对话后思路混乱 | 导出对话让 DeepSeek 分析现状 |
| 创建新文件导致上下文混乱 | 减少创建新文件，在原有文件上修改 |
| JS 转 PY 时代码被修改 | 对比 JS 和 PY 的逻辑是否一致 |
| 整合包修改了原有逻辑 | 用 DeepSeek 检查版本间的区别 |

### 9.6 Python UI 问题

| 问题 | 解决 |
|------|------|
| 界面卡死无响应 | 使用 threading 后台线程，避免阻塞主线程 |
| 日志不显示 | 使用 `self.after(0, lambda: ...)` 在主线程更新 UI |
| 找不到游戏进程 | 检查进程名是否正确，使用 psutil 辅助查找 |
| JS 文件找不到 | 使用 `get_resource_path()` 获取正确路径 |
| 打包后缺少依赖 | 使用 `--hidden-import` 添加所有依赖 |
| 打包后体积太大 | 检查是否包含了不必要的库 |
| 关闭界面后游戏崩溃 | 在 `on_closing()` 中正确清理 Frida 资源 |

---

## 十、附录：核心原则

### 10.1 修改游戏的正确顺序

```
第1步：搞清楚你要改什么（大白话写下来）
  ↓
第2步：在 dump.cs 里找到负责这个功能的类
  ↓
第3步：看这个类继承自谁 → 画继承链
  ↓
第4步：找到关键字段的偏移（offset）
  ↓
第5步：在 dump.cs 里找到操作这些字段的方法
  ↓
第6步：在 script.json 里找到方法的 RVA 地址
  ↓
第7步：用 IDA MCP 反编译方法，看真实代码逻辑 ⭐
  ↓
第8步：决定用 Hook / Attach / Replace / NativeFunction
  ↓
第9步：写 Frida 脚本
  ↓
第10步：开发 Python UI 界面
  ↓
第11步：测试 → 修 bug → 再测试
```

### 10.2 必须做到的 9 点

1. **全模式适配**：优先找基类方法
2. **主副武器都生效**：不缓存指针，每次动态判断
3. **区分玩家和Bot**：使用 isMyWeapon / isMyPlayer
4. **退出房间不崩溃**：Hook OnDestroy 清空缓存
5. **遵守游戏逻辑**：按照游戏逻辑修改
6. **32位游戏**：注意指针和内存操作
7. **线程安全**：不影响游戏性能
8. **用户友好**：傻瓜式操作，避免错误操作
9. **Python UI 界面**：替代命令行，一键操作，实时状态显示

### 9.3 Frida 三个核心概念

| Frida 概念 | 现实比喻 | 一句话 |
|-----------|---------|--------|
| **Interceptor.attach** | 快递员送快递时门口放监控 | 监听函数，不改行为 |
| **Interceptor.replace** | 把快递员换成你 | 完全替换函数 |
| **NativeFunction** | 主动打电话叫快递员 | 主动调函数 |

### 9.4 关键教训

1. **指针类型必须匹配**：Recoil* ≠ Weapon* ≠ Player*
2. **优先使用 replace 而非 attach**：性能差异巨大
3. **简单策略往往最有效**：缓存前 2 个对象比复杂 API 调用更可靠
4. **查看游戏源码**：dump.cs 是理解游戏逻辑的关键
5. **测试所有模式**：不同模式可能有不同的对象创建顺序
6. **IDA 反编译是关键**：从猜代码逻辑变成读代码逻辑
7. **减少文件创建**：避免上下文混乱和逻辑混乱
8. **验证 AI 执行结果**：检测执行到没到位

---

> **最后的话**：你现在有了完整的武器库——**dump.cs（查结构）+ script.json（查地址）+ Frida（改内存）+ IDA MCP（看逻辑）**。改任何功能就按这个流水线走，不会再瞎猜。

> **记住**：dump.cs 只告诉你有这个方法，**IDA 才告诉你这个方法在干什么**。
