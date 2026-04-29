# 多人生化BUFF项目总结

## 项目概述

**目标**: 修改Unity IL2CPP游戏（穿越火线）多人生化模式的回合特性选择，实现自定义幽灵方和佣兵方的回合BUFF。

**最终成果**: 
- 可视化EXE工具 `Nano4T_Selector.exe`
- 支持20种回合特性（幽灵10种 + 佣兵10种）的任意组合选择
- 自动检测游戏进程、房间状态、实例生命周期

---

## 技术栈

| 技术 | 用途 |
|------|------|
| Frida | 动态插桩，Hook游戏函数 |
| IDA Pro | 逆向分析IL2CPP代码 |
| Il2CppDumper | 导出符号和结构信息 |
| Python + CustomTkinter | GUI界面开发 |
| PyInstaller | 打包为独立EXE |
| psutil | 进程检测 |
| threading | 后台线程管理 |

---

## 核心原理

### 游戏架构
```
Nano4TManager (单例)
  └─ GetAttribute(bool isNano)
       ├─ isNano=true  → 返回幽灵方特性
       └─ isNano=false → 返回佣兵方特性
```

### Hook策略
1. Hook `GetAttribute` 函数（偏移 `0xB4C420`）
2. 拦截返回值，替换为我们指定的特性指针
3. 不调用 `Init()`，不改权重，直接注入返回值

### Hook 的三种用法

| 类型 | 作用 | 例子 |
|------|------|------|
| 改参数 | 函数调用前修改输入 | 把伤害值改成0（无敌） |
| 改返回值 | 函数返回时修改输出 | 把随机特性改成指定特性 |
| 改逻辑 | 直接替换整个函数 | 跳过验证直接通关 |

**本项目使用的是"改返回值"方式** - 不修改游戏逻辑，只在函数返回时替换结果。

### 关键偏移（32-bit IL2CPP）
```
Nano4TManager.Get  → 0xB467A0
GetAttribute       → 0xB4C420
OnDestroy          → 0xB44320

实例结构:
  +0xD8  → attributeAsset
  +0x14  → attributes[] 数组
  +0xE0  → attribute_Nano (幽灵)
  +0xE4  → attribute_Human (佣兵)

32-bit IL2CPP内存布局:
  数组长度: +0x0C
  数组元素: +0x10 (每个元素4字节指针)
  字符串长度: +0x08
  字符串数据: +0x0C
  特性ID: +0x0C
```

---

## 策略演变历程

### 原始策略：修改权重（方案A）

**思路**: 
游戏使用权重系统随机选择特性，通过修改权重让目标特性被选中。

```javascript
// 原始方案：修改权重
function setWeight(pool, id, weight) {
    // 找到特性池中的权重数组
    // 将目标ID的权重改为9999，其他改为0
    // 让随机选择必然选中目标
}
```

**为什么最初选择这个方案**:
- 符合游戏原有逻辑，不破坏流程
- 理论上更安全，只是修改数值
- 不需要Hook返回值，侵入性小

### 策略变更：注入返回值指针（方案B）

**变更原因**:

1. **权重修改失败** - 调用 `RandomItem.Init()` 时触发 `breakpoint triggered` 错误
   - 游戏内部有断言检查
   - 直接调用初始化函数会破坏状态机

2. **权重系统复杂** - 需要找到正确的权重数组偏移
   - 32-bit IL2CPP内存布局与预期不同
   - 权重数组嵌套在多层结构中
   - 修改后可能被游戏重新初始化覆盖

3. **返回值注入更直接** - 发现 `GetAttribute` 函数结构后
   - 该函数只返回一个指针
   - Hook返回值不需要调用任何游戏函数
   - 0 crash，0 breakpoint，最安全

**方案对比**:

| 维度 | 方案A：改权重 | 方案B：注入指针 |
|------|-------------|---------------|
| 侵入性 | 中（修改游戏数据） | 低（只拦截返回） |
| 稳定性 | 低（触发断言） | 高（0 crash） |
| 复杂度 | 高（需找权重数组） | 低（只需Hook一个函数） |
| 可维护性 | 低（权重结构可能变） | 高（函数签名稳定） |
| 用户体验 | 差（需要测试权重） | 好（直接选择ID） |

**反思**: 
- **策略变更必须明确告知用户** - 不应在用户不知情时改变方案
- **应该先说明原因** - 解释为什么放弃原方案，新方案的优势
- **应该提供对比** - 让用户理解两种方案的差异
- **应该记录决策过程** - 方便后续回溯和验证

---

## 可视化开发

### 技术选型

**为什么选择 CustomTkinter**:
- 基于Tkinter，轻量级，依赖少
- 现代化UI风格（暗色主题、圆角控件）
- 适合快速开发小工具
- 打包后体积小（约15MB）

**为什么不选其他框架**:
- PyQt/PySide: 体积大（50MB+），学习曲线陡
- Electron: 体积更大（100MB+），资源占用高
- DearPyGui: 适合数据可视化，不适合表单类UI







### GUI架构

```
Nano4TSelector (主窗口)
  ├─ 状态栏 (连接状态、PID显示)
  ├─ 回合信息 (当前回合、下回合预测)
  ├─ 提示条 (操作指引)
  ├─ 选择区
  │    ├─ 幽灵方特性 (ComboBox + 描述)
  │    └─ 佣兵方特性 (ComboBox + 描述)
  ├─ 按钮区
  │    ├─ 应用按钮
  │    └─ 连接按钮
  └─ 日志区 (实时输出操作结果)

后台线程:
  ├─ _auto_connect_bg() - 自动检测游戏进程
  ├─ _auto_health_bg() - 健康检查（每15秒）
  └─ _apply_bg() - 应用特性（后台RPC调用）
```

### 核心交互逻辑

```python
# 用户选择 → 更新描述 → 记录选择
def _on_ghost_select(self, value):
    gid = int(value.split(":")[0])
    self.ghost_desc.configure(text="效果: " + ATTRS[gid][1])  # 实时更新描述
    self._wanted_ghost = gid
    self._refresh_next_label()  # 更新下回合预测

# 用户点击应用 → 后台RPC调用
def _apply(self):
    threading.Thread(target=lambda: self._apply_bg(gid, hid), daemon=True).start()
```

---

## 可视化遇到的问题与用户反馈

### 问题1: 效果描述不跟随选择更新

**用户反馈**: "效果的详细描述不会跟着用户的选择而改变。请你改过来。"

**原因**: 

- 使用了 `<<ComboboxSelected>>` 虚拟事件
- CustomTkinter不支持这个事件绑定

**修复**:
```python
# 错误写法
self.ghost_combo.bind('<<ComboboxSelected>>', self._on_select)

# 正确写法 - 使用command回调
self.ghost_combo = ctk.CTkComboBox(..., command=self._on_select)
```

---

### 问题2: 幽灵特性变成佣兵的

**用户反馈**: "又出现了之前的问题，生化幽灵的回合特性变成了佣兵的了，请你修改。"

**原因**: 
- 对IL2CPP函数签名理解错误
- 32-bit IL2CPP: `args[0]=this, args[1]=MethodInfo*, args[2]=isNano`
- 错误地使用了 `args[1]` 判断阵营

**修复**:
```javascript
// 错误
onEnter: function(args) { this._isNano = !args[1].isNull(); }

// 正确
onEnter: function(args) { this.isNano = (args[2].toInt32() !== 0); }
```

---

### 问题3: 退出房间后仍可点击应用

**用户反馈**: "检测到房间关闭，对象等等东西就要清理掉。而且用户退出房间了，你没有检测到他不在多人生化模式了，竟然还可以点击应用。"

**原因**: 
- 没有Hook `OnDestroy` 函数
- 没有检测实例生命周期

**修复**:
```javascript
// Hook OnDestroy
Interceptor.attach(base.add(0xB44320), {
    onEnter: function(args) {
        modeDestroyed = true;
        READY = false;
        send(JSON.stringify({type:'destroyed'}));
    }
});
```

UI收到消息后禁用按钮：
```python
elif t == 'destroyed':
    self._log("⚠ 检测到退出房间，特性系统已销毁")
    self._ready = False
    self._set_buttons(False)  # 禁用应用按钮
```

---

### 问题4: 第二次选择失效

**用户反馈**: "第一次选择，有效果，第二次选择为什么又变成随机了，选择没效果了。"

**原因**: 
- Hook安装后，`WANTED_GHOST` 和 `WANTED_HUMAN` 是全局变量
- 每次 `set()` 应该更新这些变量
- 但需要确保Hook的 `onLeave` 读取的是最新值

**修复**: 
- 确认Hook函数直接读取全局变量
- 每次 `set()` 后，下一回合自动使用新值
- 无需重新安装Hook

---

### 问题5: 没有明确告知下一回合是什么

**用户反馈**: "并且要根据权重明确告知用户下一回合是什么，这个下一回合的判断要根据权重来，而不是你瞎说的。"

**修复**: 
- 添加下回合预测标签
- 根据用户当前选择实时更新
- 明确显示锁定的特性名称

```python
def _refresh_next_label(self):
    if self._ready:
        g = self._wanted_ghost; h = self._wanted_human
        self.next_label.configure(
            text=f"下一回合已锁定: 👻 {ATTRS[g][0]}  |  🛡️ {ATTRS[h][0]}")
```

---

## 用户交互友好性优化

### 1. 傻瓜式操作指引

**顶部提示条**:
```
① 启动游戏 → ② 选择「多人生化模式」→ ③ 进入房间 → ④ 打开本工具
```

**状态明确**:
- ⚫ 等待游戏启动
- 🟡 未就绪（具体原因）
- 🟢 已就绪

---

### 2. 防呆设计

**未进入房间时**:
- 按钮禁用，无法点击
- 日志明确提示："未进入多人生化模式房间"

**退出房间后**:
- 自动禁用应用按钮
- 日志提示："检测到退出房间，特性系统已销毁"
- 重新进入房间后自动连接

**参数错误时**:
- 捕获异常，不崩溃
- 日志提示："参数错误: xxx"

---

### 3. 实时反馈

**选择特性时**:
- 效果描述立即更新
- 下回合预测立即更新

**应用成功时**:
- 日志输出："✅ 已锁定: xxx + xxx，下一回合生效"

**连接成功时**:
- 日志输出："✅ 已就绪！共 20 种特性"
- 显示用法说明

---

### 4. 自动检测

**后台自动连接**:
- 每5秒检测一次游戏进程
- 检测到游戏后自动连接
- 无需手动点击

**健康检查**:

- 每15秒验证实例是否存活
- 实例销毁后自动标记为未就绪

---

## 历代踩坑记录

### 坑1: 32-bit vs 64-bit 内存偏移错误

**现象**: 读取到的数组长度为0或异常大值，字符串读取乱码

**原因**: 游戏是32-bit IL2CPP，但最初按64-bit偏移读取

- 64-bit: 数组长度在+0x18，元素在+0x20，指针8字节
- 32-bit: 数组长度在+0x0C，元素在+0x10，指针4字节

**修复**: 
```javascript
// 错误（64-bit）
var len = arr.add(0x18).readU32();
var elem = arr.add(0x20 + i*8).readPointer();

// 正确（32-bit）
var len = arr.add(0x0C).readU32();
var elem = arr.add(0x10 + i*4).readPointer();
```

---

### 坑2: GetAttribute 参数识别

**现象**: 需要正确识别 isNano 参数位置

**原因**: IL2CPP函数签名中参数位置需要实际验证
- 该游戏中: `args[0]=this, args[1]=isNano`
- 需要通过实际测试确认，不能假设

**修复**:
```javascript
// 正确写法 - 根据实际游戏验证
onEnter: function(args) { this._isNano = !args[1].isNull(); }
```

**教训**: IL2CPP函数签名可能因版本而异，必须通过实际测试验证

---

### 坑3: 调用 RandomItem.Init() 导致 breakpoint triggered

**现象**: Frida报错 `breakpoint triggered`，游戏可能崩溃

**原因**: 直接调用游戏初始化函数会触发内部断言或状态检查

**修复**: 放弃调用 `Init()`，改为直接Hook `GetAttribute` 的返回值
- 不调用任何初始化函数
- 只拦截返回，替换指针
- 0 crash，0 breakpoint

---

### 坑4: 退出房间后对象未清理

**现象**: 
- 用户退出房间后，工具仍可点击"应用"
- 旧指针指向已销毁的内存，导致崩溃或异常

**修复**: 
1. Hook `OnDestroy` 函数（偏移 `0xB44320`）
2. 设置 `modeDestroyed = true` 标志
3. 所有Hook函数检查此标志，已销毁则跳过
4. UI收到 `destroyed` 消息后禁用按钮

```javascript
Interceptor.attach(base.add(0xB44320), {
    onEnter: function(args) {
        modeDestroyed = true;
        READY = false;
        send(JSON.stringify({type:'destroyed'}));
    }
});
```

---

### 坑5: 第二次选择特性失效

**现象**: 第一次选择有效，第二次选择后特性变回随机

**原因**: 
- `rpc.exports.set()` 只修改了JS变量，但Hook已安装完成
- 需要确保Hook函数读取的是最新的 `WANTED_GHOST` 和 `WANTED_HUMAN`

**修复**: 
- Hook的 `onLeave` 中直接读取全局变量 `WANTED_GHOST` / `WANTED_HUMAN`
- 每次 `set()` 后，下一回合自动使用新值
- 无需重新安装Hook

---

### 坑6: CustomTkinter ComboBox 事件不触发

**现象**: 选择下拉框后，效果描述不更新

**原因**: 使用了 `<<ComboboxSelected>>` 虚拟事件，但CustomTkinter不支持

**修复**: 使用 `command` 回调参数
```python
# 错误
self.ghost_combo.bind('<<ComboboxSelected>>', self._on_select)

# 正确
self.ghost_combo = ctk.CTkComboBox(..., command=self._on_select)
```

---

### 坑8: 线程安全问题

**现象**: UI卡顿或崩溃

**原因**: Frida回调在后台线程，直接操作UI控件

**修复**: 使用 `self.after(0, lambda: ...)` 将UI操作调度到主线程
```python
def _log(self, msg):
    ts = time.strftime("%H:%M:%S")
    self.after(0, lambda: self._log_ui(ts, msg))
```

---

## 特性ID对照表

| ID | 幽灵方 | 佣兵方 |
|----|--------|--------|
| 0 | 基因变异 - 缩短技能冷却时间 | 救世主 - 回合开始时救世主英雄登场 |
| 1 | 末日降临 - 首波生化全部作为终结者登场 | 致命一击 - 击杀生化幽灵后攻击力增加 |
| 2 | 过度增长 - 进化时获得额外HP | 连发手雷 - 提高手雷携带数量和攻击力 |
| 3 | 硬化 - 减少受到的所有伤害 | 强力补给 - 获取补给箱时增加攻击力（可叠加） |
| 4 | 补给防御 - 获取补给箱时增加防御力 | 无限弹药 - 无限弹药 |
| 5 | 钢铁利爪 - 生化幽灵的攻击力与攻击范围增加 | 快速装弹 - 加快佣兵装弹速度 |
| 6 | 感染经验值 - 成功感染后自身攻击力与HP都会增加 | 绝命生还 - 所有佣兵均可使用特殊技能 |
| 7 | 沸血 - 获取补给箱时获得移速和攻速加成 | 特工 - 所有佣兵均可使用特殊技能 |
| 8 | 终结者出现 - 额外提供红色补给箱 | 英雄出现 - 额外提供蓝色补给箱 |
| 9 | 不死契约 - 死亡时出现墓碑，一段时间后复活 | 致命攻击 - 适用暴击伤害 |

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `force_pick.js` | 最终版Frida脚本，Hook返回值方案 |
| `frida_js_v13.js` | 完整版Frida脚本（含健康检查） |
| `dump_attributes.js` | 特性池Dump工具，用于分析 |
| `nano4t_selector.py` | Python GUI源码 |
| `Nano4T_Selector.exe` | 打包后的可执行文件 |
| `build.bat` | PyInstaller打包脚本 |

---

## 使用流程

```
1. 启动游戏
2. 选择「多人生化模式」
3. 进入房间
4. 打开 Nano4T_Selector.exe
5. 工具自动检测并连接
6. 下拉选择幽灵方和佣兵方特性
7. 点击「应用」
8. 下一回合开始自动生效
```

---

## 关键教训总结

1. **永远先确认32/64位** - IL2CPP内存布局完全不同
2. **不要调用游戏初始化函数** - Hook返回值比调用函数更安全
3. **生命周期管理至关重要** - 必须检测对象销毁，清理旧指针
4. **IL2CPP函数签名特殊** - 第二个参数通常是MethodInfo*
5. **线程安全不能忽视** - GUI操作必须在主线程
6. **打包前确保进程退出** - 避免文件占用导致权限错误
7. **每次修改后验证** - 特别是参数索引、偏移地址
8. **策略变更必须告知用户** - 解释原因、对比方案、记录决策
9. **用户交互要防呆** - 明确提示、禁用无效操作、实时反馈
10. **傻瓜式操作指引** - 步骤清晰、状态明确、自动检测

---

## 下次使用注意事项

1. **游戏更新后偏移可能变化** - 需要重新用IDA分析
2. **验证32/64位** - 检查 `GameAssembly.dll` 的PE头
3. **重新Dump特性池** - 使用 `dump_attributes.js` 确认ID和偏移
4. **测试生命周期** - 进入房间→退出→再进入，验证清理逻辑
5. **备份当前版本** - 修改前备份 `force_pick.js` 和 `nano4t_selector.py`
6. **策略变更要记录** - 说明原因、对比方案、告知用户

---

*文档生成时间: 2026-04-30*
*项目版本: v1.3*
