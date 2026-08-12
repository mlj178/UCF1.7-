# 角色变身接入整合包 2.5 设计

## 目标与边界

将 `05-正式功能/34-角色变身/` 的角色变身能力接入 `全功能整合包2.5/game_modifier`。功能在“多人生化”页显示为独立内嵌卡片，提供四个一次性动作：本地玩家选择英雄、本地玩家选择超级终结者、所有存活 Bot 随机变为英雄、所有存活 Bot 随机变为超级终结者。

本次不修改 `15_nano4t` 的 Buff 选择页面、强制决战回合逻辑及任何中心文件。现有未提交改动也不纳入本功能。

## 方案比较与选择

1. **采用：多人生化页内嵌卡片。** 与 `17_skillcd` 相同，声明 `ui.mode = special_inline_card`，由现有插件页构建器追加到特殊页的 `inline_card_host`。功能边界独立，且不侵入 Buff 页面。
2. **未采用：普通“其他”页卡片。** 接入简单，但玩法归类不准确。
3. **未采用：直接修改多人生化特殊主页面。** 可以自由布局，但会把角色变身与 Buff/决战回合代码耦合，不符合插件隔离原则。

## 插件结构

新建 `features/34_role_transform/`：

- `script.js`：先完整复制单功能 JS，再做整合包所需的最小 RPC/lifecycle 兼容。
- `manifest.json`：声明功能 ID、四个按钮、RPC、一次性动作生命周期、来源和内嵌卡片位置。
- `feature.py`：继承 `PluginFeatureBase`，不自行连接 Frida。
- `panel.py`：绘制四按钮卡片，仅通过 `callbacks["action"]` 触发动作。
- `events.py`：保留功能级事件入口；无事件需求时不处理。
- `test_role_transform_integration.py`：验证目录、manifest、UI 回调、JS 契约和禁止修改中心架构的静态约束。

独立测试 UI `AAAAA-role_transform_ui.py` 不直接作为正式版运行代码。它只作为 Python UI 行为参考，其四按钮文案和动作映射迁移到 `panel.py`。

## UI 与动作流

卡片位于“多人生化”页，使用 `special_inline_card`，排序在现有技能无冷却卡片之后。卡片不提供持久开关，只提供四个按钮：

- 本地玩家：选择英雄 → `trigger("local_hero")`
- 本地玩家：选择超级终结者 → `trigger("local_terminator")`
- 所有 Bot：随机英雄 → `trigger("bot_hero")`
- 所有 Bot：随机超级终结者 → `trigger("bot_terminator")`

按钮通过通用 action callback 进入整合包 RPC 路由。脚本的 `trigger` 仅排队，下一次 `ModeBase.Update` 在游戏主线程消费动作。已有 pending 动作时拒绝新动作，避免覆盖或累积。

## 生命周期与持久化

该功能是一次性按钮动作：

- 不写入 `feature_state.json`，不自动恢复，不在启动或重连后重放按钮动作。
- 无用户参数，不写入 `user_config.json`。
- 脚本仍需在执行按钮动作前处于 enabled/initialized 状态；正式版 action 路由负责按插件既有机制加载并调用。
- `cleanup` 和 `disable` 清空 pending、卸载 Hook 并重置运行态，允许重复调用。
- 不使用 room-ready 自动重放。用户必须进入有效的多人生化房间后手动点击；无有效模式或玩家对象时，本次动作失败并丢弃。

开发规范中的“功能开关与参数持久化记录”将补充角色变身条目，明确四个按钮均不持久化。

## 错误处理

UI 在未连接游戏时沿用通用 action 路由的连接校验和日志提示。JS 对无效动作、功能未就绪、当前模式无效、本地玩家或 Bot 对象不可用、已有 pending 动作等情况返回结构化状态并记录错误，不缓存跨房间对象，不延迟到未来房间执行。

## 验证

自动检查包括：

- `node --check` 验证 `script.js` 语法。
- Python 编译检查 `feature.py`、`panel.py` 和 `events.py`。
- 单元/静态测试验证四个动作映射、`special_inline_card`、`nano4t_tab`、一次性不恢复生命周期、通用 callbacks、标准 RPC、主线程 pending 动作链及关键原生调用。
- 插件发现/manifest 加载测试，确认不需要改中心文件即可加载。
- Git 差异检查，确认未改 Buff 选择、强制决战回合和用户已有改动。

游戏内验收需确认四个按钮在“多人生化”页显示并分别执行正确路径；重复点击、死亡重生、切房、断线重连和退出清理时不重放旧动作、不使用旧指针且不崩溃。
