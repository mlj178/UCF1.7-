# 15｜多人生化 Buff 选择（Nano4T Attribute Selector）

来源：`features/15_nano4t/`（script.js + events.py + panel.py）。开发素材：`05-正式功能\15-多人生化_BUFF选择器\` 下的 `多人生化_BUBFF项目总结.md`、`多人生化模式-总结.md`、`AAAAA-nano4t_selector.py`。

---

## 核心原理

**一句话**：`Interceptor.attach`（`onLeave`）`Nano4TManager.ChooseTrait`(+0xB4C420)，把吃随机选择返回的属性指针，在返回时替换为用户指定的特性指针（`retval.replace(p)`）；阵营用 `args[1]` 判定；`OnDestroy`(+0xB44320) 检测房间销毁。

**手段归类**：改返回值（`onLeave` 替换属性指针注入），不调用任何游戏初始化函数；Python 侧 `events.py/panel.py` 通过 RPC 下发 `WANTED_GHOST/WANTED_HUMAN`，JS 侧只读全局变量即生效。

## 关键 Hook 表（GameAssembly.dll）

| RVA | 函数 | 手段 | 作用 |
|---|---|---|---|
| +0xB4C420 | `Nano4TManager.ChooseTrait`（GetAttribute） | Interceptor.attach（`onLeave`） | 对返回的属性指针做 `retval.replace(p)`，注入指定幽灵/佣兵特性 |
| +0xB467A0 | `Nano4TManager.GetInstance` | NativeFunction | 取管理器实例 |
| +0xB44320 | `Nano4TManager.OnDestroy` | Interceptor.attach | 模式销毁时置 `modeDestroyed`、下发 `destroyed` 通知 UI 禁用 |

## 修改的关键字段

| 偏移 | 字段 | 用法 |
|---|---|---|
| `inst+0xD8` | `attributeAsset` | 读，取特性资源对象 |
| `asset+0x14` | `attributes[]`（IL2CPP 数组） | 读，按 ID 取属性指针 |
| 数组 `+0x0C`/`+0x10` | len / data（32-bit） | 遍历特性池 |
| `inst+0xE0` | `attribute_Nano`（幽灵方） | 读 |
| `inst+0xE4` | `attribute_Human`（佣兵方） | 读 |
| 返回值 | `ChooseTrait` 返回的 attribute 指针 | `retval.replace(指定特性指针)` |

**特殊处理（具体到逻辑）**：
- **阵营判定**：脚本用 `!args[1].isNull()` 取本轮阵营（幽灵/佣兵）。（素材文档曾记录 isNano 参数位置踩坑，须按实际版本运行时验证。）
- **只读全局变量**：`onLeave` 直接读 `WANTED_GHOST`/`WANTED_HUMAN`，第二次 `set()` 只改全局，**无需重装 Hook**（下一回合自动生效）。
- **不调用游戏初始化函数**：不 `Init()`、不改权重，0 crash / 0 breakpoint。
- **生命周期**：`OnDestroy` 置 `modeDestroyed=true`、`READY=false` 并 `send({type:'destroyed'})`；Hook 内检查标志跳过已销毁；UI 收到后禁用按钮（Python `_set_buttons(False)`）。
- **可逆卸载**：`detach` + 清理全局。
- 与 Python 侧线程同步：Frida 回调在后台线程，UI 更新用 `self.after(0, ...)` 调度到主线程。

## 作用范围

**回合特性本身是对局共享（全局）**：`ChooseTrait` 决定本回合幽灵/佣兵**所有玩家**的特性 BUFF，注入指针后全队生效；不区分单个玩家。本功能通过改写"本回合被选中的特性"来定点指定，作用面是当前回合对局。

## 产品设计巧思

- **自动检测/自动连接**：自动识别并连接游戏进程，用户不用手点连接，省去重复操作。
- **防呆**：未进房时禁用选择按钮并提示；退出房间自动禁用、重新进房自动恢复连接——不会在无效状态误操作。
- **实时反馈**：选择即更新效果描述 + 显示"下回合生效"预测标签（按实际选择明确告知），用户能确认自己要的是否正确。
- **傻瓜式操作**：双下拉选择 + 明确当前状态/未就绪原因，几步即可完成设置。
- **后台健康检查 + 生命周期**：进程/房间状态自动维护，异常时自动兜底，无需用户干预。

## 开发历程（重点）

### 踩过的坑（问题 → 原因 → 解决）

1. **32-bit / 64-bit 布局错误 → 数组/字符串读错**
   - 问题：读特性数组长度=0 或异常大、字符串乱码。
   - 原因：游戏是 **32-bit IL2CPP**，却按 64-bit 偏移读（数组 len 在 +0x18、元素 +0x20、指针 8B）。
   - 解决：改成 32-bit 布局（len `+0x0C`、元素 `+0x10`、元素 4B/个个）。

2. **调用 `RandomItem.Init()` 触发 `breakpoint triggered`（改权重会崩）**
   - 问题：原方案用权重让目标特性必被选中，`RandomItem.Init()` 触发 Frida `breakpoint triggered`，可能崩溃。
   - 原因：直接调用游戏初始化函数触发内部断言/状态机破坏。
   - 解决：**放弃改权重，改为 `onLeave` 注入返回值指针**——不调任何初始化函数，0 crash / 0 breakpoint。

3. **`GetAttribute` 的 isNano 参数位置判断错 → 幽灵选了佣兵特性**
   - 问题：幽灵特性被写成佣兵的。
   - 原因：IL2CPP 函数签名/参数位置理解错误（32-bit：`args[0]=this`，之后是参数），曾误用 `args[1]`/`args[2]` 语义。
   - 解决：按运行时实际验证固定阵营判定写法（整合包 `!args[1].isNull()`），记录"参数位置必须实测，不同版本可能不同"。

4. **退出房间后仍可"应用"，旧指针指向已销毁内存**
   - 原因：未 Hook `OnDestroy`、未检测实例生命周期。
   - 解决：`attach OnDestroy`(+0xB44320) 置 `modeDestroyed`/`READY=false` 并 `send({type:'destroyed'})`；Hook 检查标志跳过已销毁；Python 收到后禁用应用按钮。

5. **第二次选择失效（变回随机）**
   - 原因：`set()` 只改了 JS 变量但不确定 Hook 读到的是最新值。
   - 解决：确认 `onLeave` 直接读全局 `WANTED_GHOST/WANTED_HUMAN`，一切 `set()` 更新全局即可，无需重装 Hook。

6. **CustomTkinter ComboBox 事件不触发**
   - 问题：选择后描述不更新。
   - 原因：用了 `<<ComboboxSelected>>` 虚拟事件，CustomTkinter 不支持。
   - 解决：改用 `command` 回调。

7. **线程安全：Frida 回调后台线程直接操作 GUI**
   - 问题：UI 卡顿或崩溃。
   - 解决：`self.after(0, lambda: ...)` 把 UI 操作调度到主线程。

### 方案迭代

1. **方案A（改权重）**：把目标特性权重改成 9999、其余 0，让随机必选目标。符合原生流程、看似只改数值。触发 `RandomItem.Init()` 断言/`breakpoint triggered`，且权重数组嵌套复杂易被游戏重扫覆盖 → **废弃**。
2. **方案B（注入返回值指针，最终采用）**：`ChooseTrait.onLeave` 直接 `retval.replace(指定 pointer)`。只拦返回、不调任何游戏函数、0 crash、签名稳定、可维护。**改返回值 > 改数据（权重）/ 调用函数（Init）**。

### 一开始没考虑到的点

- **32-bit IL2CPP 布局** vs 64-bit，数组/指针偏移完全不同，必须先确认位数。
- **"改数值（权重）"看似最小侵入≠最安全**：触发内部断言/断点的往往正是这类"改数据"；而"改返回值"更安全。
- **不能调用游戏初始化函数**（`Init()` 会破坏状态机）。
- **必须管理实例生命周期**（`OnDestroy`），否则退出房间后旧指针崩。
- **多次应用的 Hook 要读最新全局变量**，而不是依赖重装 Hook。
- **函数签名/参数位置要实测**（isNano 位置因版本而异）。
- **GUI 框架的虚拟事件/线程模型差异**（ComboBox 事件、UI 主线程调度）。

### 经验教训

- **优先"改返回值"而非"改数据/调用函数"**：前者侵入小、稳定、可逆。
- **改动方案变更必须明确告知并记录**（改权重→注入指针的决策要说明原因与对比）。
- **生命周期管理不可省略**：Hook `OnDestroy`、清理旧指针、禁用过期 UI 操作。
- **先确认 32/64 位与函数签名**（参数位置要实测，别假设）。
- **回调线程安全**：后台回调对 UI 操作必须调度回主线程。
- **Hook + Python 分层**：JS 只读全局变量、Python 负责选择下发与生命周期 UI，职责清晰。

## 一句话总结

`onLeave` Hook `Nano4TManager.ChooseTrait`(+0xB4C420) 用 `retval.replace(p)` 把随机特性指针替换为用户指定幽灵/佣兵特性（`args[1]` 判阵营），`OnDestroy`(+0xB44320) 管房间销毁；从"改权重（`RandomItem.Init()` 触发 breakpoint→弃）"迭代到"注入返回值指针（0 crash）"；踩坑覆盖 32/64 位布局、isNano 参数位置须实测、生命周期、二次应用读全局、GUI 事件/线程。