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



## 三、阶段二：游戏分析

### 3.1 在 dump.cs 中搜索目标

```
搜索关键词：
1. 类名包含 {关键词} 的类      

2. 方法名包含 {关键词} 的方法

3. 字段名包含 {关键词} 的字段

4. 列出找到的类、方法、字段的 RVA 地址

   
3. 找到关键字段的偏移（offset）
4. 找到操作这些字段的方法
```

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
## 四、阶段三：脚本开发

### 4.1 选择 Frida 修改方式

hook 还是修改字段内存数值



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

### 5.7 状态轮询机制

### 5.8 清理机制

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

**获取资源文件路径（支持打包后）：**

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

### 	日志发送是否过于频繁

​	

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

---

## 七、阶段六：打包发布

### 7.1 JS 转 Python

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

