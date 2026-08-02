# 32/33 功能接入整合包 2.4 设计

## 目标

将 `05-正式功能` 中的“32-亮度调节探针”和“33-玩家信息修改器”复制并适配为整合包 2.4 的普通插件功能卡片，统一放入现有“游戏参数”页（代码标识：`game_parameters_tab`）。

## 已确认的用户要求

- 两个功能都做成主窗口中的普通功能卡片。
- 两个功能都放入“游戏参数”tab。
- 迁移时先复制源功能，再按 2.4 当前插件架构适配。
- `02-开发规范` 作为参考；如与 2.4 实际代码冲突，以用户判断为准。

## 现有架构约束

2.4 通过 `features/<feature_dir>/manifest.json` 发现插件，`PluginRegistry` 加载 `feature.py`，普通 tab 由 `PluginFeaturePage` 按 manifest 的 `layout` 和 `controls` 构建。需要复杂控件的插件可以提供 `panel.py` 的 `build_card`，但仍然属于普通卡片，不创建特殊 tab。

游戏内修改通过 `FeatureCommandService -> FridaManager -> script.js` 的 RPC 链路完成；插件的本地文件功能不能误走该链路。

## 功能 32：亮度调节探针

### 用户界面

在 `game_parameters_tab` 中显示宽卡片，保留源工具的核心控件：

- 曝光 `exposure` 滑块，默认 `1.5`，范围 `-2.0..4.0`。
- 对比度 `contrast` 滑块，默认 `0`，范围 `-50..50`。
- 饱和度 `saturation` 滑块，默认 `0`，范围 `-100..100`。
- 中间调 Gamma `gamma` 滑块，默认 `0`，范围 `-1..1`。
- 亮部 Gain `gain` 滑块，默认 `0`，范围 `-1..1`。
- “应用参数”按钮：先顺序发送配置，再调用 `applybrightness`，避免 RPC busy 冲突。
- “恢复游戏初始值”按钮：调用 `resetbrightness`，恢复探针首次写入前记录的值。
- 卡片中显示连接/探针状态以及读回的 `postExposure` 等诊断信息。

### 运行时

沿用源探针的 URP `ColorAdjustments` / `LiftGammaGain` 查找和写入逻辑，复制为 2.4 插件目录中的 `script.js`，并确保导出 RPC 名称与 manifest 一致：`enable`、`disable`、`setConfig`、`setconfig`、`applybrightness`、`resetbrightness`、`status`、`cleanup`。

该功能是实验性探针，不声明“画面必然变亮”；验证报告区分参数读写成功和游戏画面实际效果。

### 持久化与生命周期

- 参数写入 2.4 现有配置管理器，对应 `user_config.json`。
- 为避免启动后未经确认自动修改画面，探针不自动恢复启用状态。
- 清理时恢复探针记录的原始参数，并遵循 2.4 的 Frida 生命周期；探针不修改相机后处理开关。

## 功能 33：玩家信息修改器

### 用户界面

在 `game_parameters_tab` 中显示宽卡片，包含：

- 当前 `PlayerData.dat` 默认路径和可选文件路径。
- 昵称、等级、VIP 等级输入框。
- “读取”按钮：读取 `[Player]`，不存在时提示保存会自动插入。
- “保存到 PlayerData.dat”按钮。
- 保存状态与简洁日志。

卡片操作不依赖游戏连接，也不注入游戏。保存直接写回 `PlayerData.dat`，不生成备份文件。

### 本地服务

从源功能复制 `player_profile_service.py`，保留并测试以下行为：

- 默认路径使用当前 Windows 用户目录，不写死用户名。
- 没有 `[Player]` 时插入到 `[Inven]` 前。
- 已有 `[Player]` 时只更新 `NickName`、`Level`、`VipLevel`。
- 昵称不能为空且不能包含换行；等级和 VIP 等级不能小于 0。
- 保存不生成备份文件。
- 文本统一按 UTF-8 读写。

### 插件动作路由

33 号使用普通卡片回调，但动作类型标为 `plugin_feature`。对 2.4 的 `ActionRouter` 做最小扩展，让插件动作方法接收 panel 传来的 payload；33 号插件自身调用本地 service，不调用 `FeatureCommandService`，从架构上隔离本地文件操作与 Frida RPC。

## 文件边界

新增：

- `全功能整合包2.4/game_modifier/features/32_brightness_probe/manifest.json`
- `全功能整合包2.4/game_modifier/features/32_brightness_probe/feature.py`
- `全功能整合包2.4/game_modifier/features/32_brightness_probe/panel.py`
- `全功能整合包2.4/game_modifier/features/32_brightness_probe/script.js`
- `全功能整合包2.4/game_modifier/features/32_brightness_probe/test_brightness_probe_static.py`
- `全功能整合包2.4/game_modifier/features/33_player_profile_editor/manifest.json`
- `全功能整合包2.4/game_modifier/features/33_player_profile_editor/feature.py`
- `全功能整合包2.4/game_modifier/features/33_player_profile_editor/panel.py`
- `全功能整合包2.4/game_modifier/features/33_player_profile_editor/player_profile_service.py`
- `全功能整合包2.4/game_modifier/features/33_player_profile_editor/test_player_profile_service.py`

修改：

- `全功能整合包2.4/game_modifier/ui/controllers/action_router.py`：允许 `plugin_feature` 动作透传 payload。
- 2.4 的功能开关与参数持久化记录：登记 32/33 的参数归属和恢复策略。
- 2.4 发布/功能说明文档：说明两个功能的使用边界和 33 号重启生效行为。

源目录中的独立 UI 文件、临时运行时 hook 和独立入口不直接放进 2.4 发布包；只迁移可复用的运行时脚本、本地 service 和必要测试。

## 错误处理

- 32 号：无游戏连接、RPC 失败、模块/RVA 不可用时，卡片显示失败状态并写入开发日志；不吞掉可诊断的错误。
- 33 号：文件不存在、编码错误、字段格式错误、权限错误和输入校验失败时，卡片显示简洁结果并记录错误；保存失败不覆盖源文件。
- 33 号修改后重启游戏生效。

## 验证标准

1. 32/33 的 manifest 可以被 2.4 `ManifestLoader` 以 UTF-8 读取，必填字段完整，tab 为 `game_parameters_tab`。
2. 2.4 的静态测试、源功能迁移测试和新增测试全部通过。
3. Python 文件通过编译检查；内嵌/独立 JavaScript 通过 Node 语法检查。
4. 33 号测试证明插入、更新、不生成备份和输入校验行为。
5. 2.4 打包配置包含新插件目录和必要资源，不包含独立工具入口、`__pycache__`、日志或测试数据。
6. 真实游戏验证仅能由运行游戏的用户确认：探针是否实际改变画面，以及切房/退出时是否符合预期。

## 设计取舍

采用“普通卡片 + 自定义 panel”的方式，而不是保留独立窗口或为本地文件功能建立新的 UI 子系统。这样能保持 2.4 的用户入口和布局一致，同时把新增架构改动限制在必要的动作 payload 透传上。
