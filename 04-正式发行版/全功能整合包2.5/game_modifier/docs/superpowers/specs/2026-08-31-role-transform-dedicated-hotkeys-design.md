# 角色变身专用快捷键与监听清理设计

## 目标

修复普通快捷键重新应用后旧监听未注销、导致同一按键触发新旧功能的问题；同时将角色变身的四个动作从 Ctrl+1～Ctrl+5 的可选项改为固定的专用快捷键。

## 固定映射

| 快捷键 | 动作 |
| --- | --- |
| Ctrl+Q | 本地玩家：选择英雄（`local_hero`） |
| Ctrl+W | 本地玩家：选择超级终结者（`local_terminator`） |
| Ctrl+E | 所有 Bot：随机英雄（`bot_hero`） |
| Ctrl+R | 所有 Bot：随机超级终结者（`bot_terminator`） |

以上四键在设置页显示为固定绑定，不属于普通功能下拉框；Ctrl+1～Ctrl+5 只保留普通功能与“未绑定”。

## 监听生命周期

`keyboard.add_hotkey` 返回的是注销函数，必须用 `keyboard.remove_hotkey(handle)` 移除。快捷键重新应用和应用关闭时，热键管理器必须对每个已保存 handle 调用此方法，再清空 handle 列表。这样重新绑定后，系统中只存在最新一轮监听。

## 配置兼容

读取旧 `hotkeys.json` 时，如果 Ctrl+1～Ctrl+5 任一槽位保存的是 `role_transform` 的动作对象，加载时将其丢弃并保存为未绑定；普通字符串功能绑定继续保留。新的角色变身专用快捷键不写入可编辑的普通绑定配置。

## 不变项

- F1、F2、Alt+1、Alt+2 的定点瞬移专用快捷键不变。
- Ctrl+Z、Ctrl+X、Ctrl+C 的武器快捷键不变。
- 角色变身插件、RPC、面板按钮与 Frida 脚本不变。

## 验证

- 使用 mock 验证每次重新应用和关闭时，所有旧 handle 都经 `keyboard.remove_hotkey` 注销。
- 验证 Ctrl+Q/W/E/R 分别分派正确的 `role_transform / trigger / payload.action`。
- 验证 Ctrl+1～Ctrl+5 的候选项不再包含角色变身动作，旧配置中的该类动作会被清除。
- 运行现有定点瞬移、角色变身与新增快捷键回归测试。
