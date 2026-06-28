# AI 协作开发操作文档

## 文档作用

本文档是后续 AI 继续开发 `game_modifier` 的工作准则。

- 告诉 AI：新增功能、修复功能、重构功能时，代码应该放到哪一层。
- 约束 AI：不要把业务逻辑继续堆进 `ui/app.py`。
- 约束 AI：不要为了减少行数盲目拆分，必须围绕当前功能边界逐步解耦。
- 约束 AI：每次修改都要同步考虑日志规范、状态持久化、UI 线程安全和验收方法。

## 当前判断

还有必要继续降低耦合，但不建议一次性大拆。

当前 `app.py` 已经从最初的巨型文件拆出视图、控制器、服务、仓库和状态模块，但它仍然承担几类职责：

- 主窗口生命周期：窗口创建、关闭、折叠、日志、状态栏。
- 连接生命周期：连接游戏、后台连接、断线监听、清理资源。
- UI 状态映射：把功能状态同步到按钮、开关、提示文字。
- Nano4T 运行控制：连接、初始化、应用配置、决战回合状态。
- 功能状态持久化桥接：把界面状态转换成可保存配置。

后续应该继续拆，但优先按“正在修改的功能”顺手拆，不要单纯为了减少行数而拆。

## 文件职责边界

后续新增或修改代码时，优先按下面边界放置：

- `ui/app.py`：只保留主窗口接线、生命周期入口、页面组合，不放具体业务逻辑。
- `ui/views/`：只负责创建控件、布局、展示文案、返回控件句柄，不直接调用 Frida。
- `ui/controllers/`：负责用户操作编排，例如按钮点击、热键、事件响应、状态切换。
- `ui/state/`：负责界面层状态对象，不负责读写文件和调用游戏指令。
- `core/services/`：负责业务动作封装，例如连接游戏、功能开关、赋予武器、Nano4T 指令。
- `core/repositories/`：只负责配置文件读写、默认值、格式兼容。
- `core/adapters/`：负责外部事件适配，例如把 Frida/EventBus 事件转换成应用可理解的事件。
- `core/weapon_catalog.py` 等目录文件：负责静态数据，不要在多个 UI 文件里复制同一份数据。
- `tests/`：每次拆分职责时，至少补一个轻量回归测试，证明新模块能独立工作。

## 功能代码放置规范

新增或修改功能时，先按职责归类，不允许一股脑写进 `ui/app.py`。

- 页面布局、卡片、按钮、标签、滚动区域、视觉状态：放到 `ui/views/`。
- 用户点击、滑条变化、热键触发、按钮防抖、UI 状态编排：放到 `ui/controllers/`。
- Frida 指令封装、功能启停、导出函数调用、连接动作：放到 `core/services/`。
- JSON 配置读写、默认配置、旧配置兼容迁移：放到 `core/repositories/`。
- 运行时状态对象、功能状态快照、UI 状态到持久化状态的转换：放到 `ui/state/` 或后续独立 `core/state/`。
- Frida / EventBus 原始事件转换成应用事件：放到 `core/adapters/`。
- 武器列表、功能元数据、固定常量目录：放到 `core/weapon_catalog.py` 或独立 catalog 文件。
- JS Hook 逻辑：放到 `scripts/XX-feature.js`；如果脚本超过约 500 行，优先拆内部模块或拆公共 helper。
- Python Feature 注册类：放到 `features/feature_xx_name.py`，只负责 feature 元数据和 JS 文件绑定，不写复杂业务流程。
- 全局快捷键和武器快捷键底层注册：放到 `core/hotkey_manager.py`、`core/weapon_hotkey_manager.py`，UI 只传回调。
- 资源处理、构建辅助：放到独立 `core/*_utils.py` 或构建脚本，不和主窗口混写。

`ui/app.py` 只允许放这些内容：

- 主窗口创建和模块接线。
- 页面组合入口。
- 生命周期入口，例如启动、关闭、清理。
- 少量跨模块状态桥接。
- 临时兼容代码，但必须在 `新增内容.md` 记录后续迁移方向。

禁止放进 `ui/app.py` 的内容：

- 新功能的完整业务逻辑。
- 直接拼 Frida 指令。
- JSON 文件读写细节。
- 大段 UI 卡片构建。
- Hook、RVA、任务队列等开发细节。
- 大段 if/elif 功能分发。

## 日志规范

后续开发新功能或修改旧功能时，必须先判断日志是给玩家看的，还是给开发者排查用的。

- 用户日志：只写用户能理解、能行动的内容，例如“暂未就绪，请重新连接游戏后重试”“请先进入房间”“功能初始化失败，请稍后重试”。
- 开发日志：写 Hook、RVA、指针、weaponId、taskId、ModeBase、GM/MM、异常堆栈、扫描结果、重试次数等内部细节。
- 双通道日志：同一件事既需要提示用户，又需要保留技术细节时，用户文案必须简短，开发细节放到 `dev_detail`。

JS 脚本日志调用规则：

- 优先使用 `sendUserLog(level, module, message)` 输出纯用户提示。
- 优先使用 `sendDevLog(level, module, message, devDetail)` 输出内部调试信息。
- 优先使用 `sendBothLog(level, module, userMessage, devDetail)` 输出“用户提示 + 开发细节”。
- 不要在新代码里继续新增旧 `sendLog(...)`；旧 `sendLog` 只作为兼容入口，默认进入开发日志。
- 不要把地址、指针、Hook 名、RVA、NativeFunction、GameAssembly、任务队列细节直接显示给用户。

Python 日志路由规则：

- UI 日志只显示 `audience=user` 或 `audience=both`。
- `audience=dev` 只写入 `game_modifier/logs/game_modifier.log`。
- Frida 事件进入 Python 后要保留 `audience` 和 `dev_detail`，不要在适配层丢字段。
- 开发日志允许中英文搭配：中文方便快速阅读，英文细节方便定位模块、函数和异常。

日志验收标准：

- 正常玩家操作时，UI 日志不出现 `RVA`、指针地址、`GameAssembly`、`ModeBase`、`GM/MM`、`NativeFunction` 等内部词。
- 用户操作失败时，UI 日志必须给出下一步动作，例如重连、进房间、稍后重试。
- 开发者日志必须能反查问题原因，至少包含模块名、失败点、异常信息或关键 ID。
- 高频循环日志、Hook 回调日志、扫描日志只能进入开发日志，不能刷 UI。

## AI 修改前检查

每次让 AI 写代码前，先让 AI 执行这组判断：

1. 本次改动属于视图、状态、控制器、服务、仓库、适配器中的哪一类。
2. 是否会让 `app.py` 增加新的业务逻辑。
3. 是否存在可复用的服务、控制器、视图模块。
4. 是否需要同步更新 `新增内容.md`。
5. 是否涉及中文文案，涉及时必须确认 UTF-8 和乱码守卫测试。
6. 是否涉及日志，涉及时必须按“用户日志 / 开发日志 / 双通道日志”分类。

如果本次改动只是在 `app.py` 里追加方法，AI 必须先说明为什么不能放到现有模块或新模块。

## AI 修改后检查

每次修改完成后，至少做这些检查：

- `python -m py_compile` 检查被改动的 Python 文件。
- 与改动相关的单元测试必须运行。
- 如果改动影响通用逻辑，运行 `python -m unittest discover -s tests -p "test_*.py"`。
- 检查 `app.py` 是否新增了过多职责，尤其是按钮回调、业务指令、JSON 读写、事件处理。
- 检查中文文案是否出现乱码。
- 检查新增日志是否误把开发细节显示到 UI。
- 把更新记录写入 `新增内容.md`。

## 什么时候继续拆

遇到下面情况，应该继续拆分：

- 一个方法超过约 50 行，并且同时做 UI、状态、业务调用。
- 一个文件超过约 800 行，并且职责不止一种。
- 新增功能需要改动 `app.py`、视图、服务多个位置，说明边界还不够清晰。
- 测试必须启动完整 UI 才能验证普通业务逻辑。
- 同一份配置读写、武器数据、状态转换在多个文件重复出现。

## 什么时候不要拆

遇到下面情况，暂时不要拆：

- 只是为了减少行数，但没有更清晰的职责归属。
- 拆出来的模块只有一个很薄的转发方法，反而增加跳转成本。
- 当前功能还不稳定，边界没有想清楚。
- 拆分会迫使大量文件同时改动，但用户只要求一个小修复。

## 分阶段架构治理路线

不要一次性大拆。后续按下面阶段推进，每一阶段完成后再进入下一阶段。

### 阶段 1：统一服务层调用路径

目标：让 UI 控制器不再直接调用 `app._frida.send_toggle()` 或 `app._frida.call_export()`，统一走 `core/services/`。

改动范围：

- `ui/controllers/feature_action_controller.py`
- `ui/controllers/weapon_interaction_controller.py`
- `ui/controllers/round_skip_monitor.py`
- `ui/controllers/app_event_controller.py`
- `core/services/feature_command_service.py`
- `core/services/game_action_service.py`
- `core/services/game_connection_service.py`
- `core/services/weapon_giver_service.py`

验收测试：

- 启动程序，连接游戏，确认普通功能开关可用。
- 测试滑条类功能：快刀、滑板鞋、剑气化丝、时间加速、轻重力。
- 测试动作类功能：聚怪、回合跳过、赋予武器、复活自动装备。
- 测试断开连接后点击功能，UI 应提示未连接，不应报错。
- 搜索 `ui/controllers`，确认不再新增直接 `app._frida.send_toggle` 和 `app._frida.call_export`。

### 阶段 2：拆 Nano4T 与决战回合运行控制器

目标：把 Nano4T 初始化、当前特性读取、应用特性、房间销毁、决战回合状态从 `ui/app.py` 中移出。

建议新增：

- `ui/controllers/nano4t_runtime_controller.py`
- `ui/controllers/battle_round_controller.py`

改动范围：

- `ui/app.py`
- `ui/controllers/app_event_controller.py`
- `ui/controllers/nano4t_selection_controller.py`
- `core/services/game_action_service.py`
- `scripts/15-buff_selector.js`
- `scripts/19-battle_round.js`

验收测试：

- 未连接游戏时点击 Nano4T 连接，UI 给出明确提示。
- 连接游戏但未进多人生化时，UI 显示未就绪，不误判为已生效。
- 进入多人生化房间后，Nano4T 状态变为已就绪。
- 选择幽灵方和人类方特性后点击应用，状态显示已激活或下一回合生效。
- 退出房间后，Nano4T 状态恢复未激活，决战回合状态同步变更。
- 决战回合开关在未连接、已连接但未进模式、已进模式三种情况下状态显示正确。

### 阶段 3：收敛状态持久化双轨

目标：统一 `feature_state.json`、`desired_states.json`、Nano4T 配置、武器复活配置的读写入口，避免多个模块各写一份状态。

建议新增或强化：

- `ui/state/app_state.py`
- `core/repositories/feature_state_repository.py`
- `core/repositories/session_state_repository.py`
- `core/repositories/nano4t_config_repository.py`

改动范围：

- `ui/app.py`
- `core/game_session_manager.py`
- `ui/controllers/feature_action_controller.py`
- `ui/controllers/weapon_interaction_controller.py`
- `core/repositories/`

验收测试：

- 启动程序，修改多个开关和滑条，关闭程序再打开，状态应恢复。
- 测试快刀、滑板鞋、剑气化丝、时间加速、轻重力参数是否恢复。
- 测试决战回合开关状态是否恢复，但实际生效状态不应被误认为已生效。
- 测试复活自动装备武器是否恢复。
- 删除配置文件后启动程序，应使用默认值，不应崩溃。
- 检查 `data` 目录，确认没有多份状态互相覆盖或语义重复。

### 阶段 4：赋予武器虚拟列表 / 虚拟网格

目标：解决赋予武器页面一次性创建大量控件导致的打开慢、滚动延迟、残影问题。

建议方向：

- 优先做分页或折叠分组，风险低。
- 如果继续 CustomTkinter，可尝试 Canvas 虚拟网格，只渲染可见卡片。
- 长期迁移新 UI 技术时，再考虑完整虚拟列表组件。

改动范围：

- `ui/views/weapon_giver_view.py`
- `ui/controllers/weapon_interaction_controller.py`
- `core/weapon_catalog.py`

验收测试：

- 启动程序时间不应明显变慢。
- 首次打开“赋予武器”页不应卡住 1 到 2 秒。
- 快速上下滚动，残影和拖慢应明显减少。
- 武器赋予按钮、快捷键绑定、快捷键徽章、复活自动装备仍可用。
- 搜索、分页或折叠状态如果新增，关闭重开后行为应符合预期。

### 阶段 5：JS 脚本模块化

目标：降低大型 JS 脚本维护难度，尤其是赋予武器、时间加速、射速连狙。

优先处理：

- `scripts/16-weapon_giver.js`
- `scripts/20-unity_time_acceleration.js`
- `scripts/13-fire_rate_auto_sniper.js`

拆分方向：

- 地址常量单独集中。
- Hook 安装单独函数区。
- 运行时状态和任务队列单独区。
- 用户日志和开发日志保持当前规范。
- RPC 入出口保持兼容，避免 Python 侧大改。

验收测试：

- Frida 脚本能正常加载。
- 三个脚本对应功能可正常启用和关闭。
- 赋予武器、复活自动装备、射速联动、时间加速仍保持原行为。
- UI 日志不出现 Hook、RVA、指针、NativeFunction 等开发细节。
- 开发日志仍能看到足够排查信息。

### 阶段 6：收尾清理

目标：清理历史兼容层、无用代码、重复状态和编译产物。

检查范围：

- `__pycache__`、`.pyc` 是否进入项目目录或发布包。
- 未使用的 service、adapter、state 是否已真正接入。
- `except Exception: pass` 是否需要改为开发日志。
- `core/config.py` 是否还混杂过多静态数据。
- `ui/app.py` 是否稳定下降到约 300 到 450 行。

验收测试：

- 启动程序无异常。
- 主要功能冒烟测试通过。
- 关闭程序时无残留线程、无明显报错。
- 开发日志无新的 Python Traceback。
- 全局搜索确认没有新增旧 `sendLog(...)` 和不合理的 `app._frida` 直连。

## 给 AI 的固定提示词

后续开发前，可以把下面这段直接发给 AI：

```text
请先阅读 AI协作开发操作文档.md 和 新增内容.md。
本次修改不要把业务逻辑继续堆进 ui/app.py。
请先判断本次修改属于哪个架构治理阶段，以及是否需要顺手降低耦合。
请先判断改动属于 view / controller / service / repository / state / adapter 哪一层。
如果必须修改 app.py，只允许做接线、生命周期入口或状态桥接。
修改完成后运行相关测试，并把更新记录写入 新增内容.md。
涉及中文文案时，必须保持 UTF-8，并运行乱码守卫测试。
涉及日志时，必须区分用户日志、开发日志和双通道日志；不要新增旧 sendLog。
请在最终回复里说明：改了哪些层、如何验收、哪些风险未处理。
```

## 核心原则

代码不是拆得越碎越好，而是要让每个文件都有清楚的理由存在。

`app.py` 应该像指挥台，不应该像仓库。按钮、状态、服务、配置、事件都可以接到这里，但具体事情应该交给对应模块完成。
