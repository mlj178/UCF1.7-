# 游戏模式切换增加个人竞技设计

## 背景

整合包 2.5 的“游戏模式切换”目前提供团队竞技、刀战、生化系列、狙击战和手枪战，但没有个人竞技。该功能分别在界面选项、功能清单和 Frida 运行脚本中维护模式列表，因此需要让三层同时支持同一个模式键。

现有资料和代码已经确认游戏模式枚举如下：

```text
TeamDeath = 0
DeathMatch = 1
Special = 2
Nano3 = 3
Nano4 = 4
Nano6 = 5
Nano4_Terminator = 6
```

运行脚本现有的个人竞技地图兼容逻辑也使用 `gameMode === 1`，与该枚举相互印证。

## 目标

在整合包 2.5 的“游戏模式切换”下拉框中加入“个人竞技”。用户选择并启用后，在创建游戏房间的既有拦截流程中，将下一局切换为游戏原生 DeathMatch 模式。

## 非目标

- 不新增模式切换入口或重新设计界面。
- 不修改其他整合包版本。
- 不新增或更换底层 RVA、Hook 或 IL2CPP 偏移。
- 不自定义个人竞技击杀数、时间、复活时间或武器限制选项。
- 不重构现有生化、刀战、狙击战和手枪战兼容逻辑。

## 方案选择

采用“完整接入原生模式资源”方案：

```javascript
death_match: {
  label: '个人竞技',
  gameMode: 1,
  weaponLimited: 0
}
```

不采用仅增加界面选项的方案，因为运行脚本会把它判定为未知模式。也不采用新建个人竞技专用 Hook 和规则实现的方案，因为游戏已经提供 DeathMatch MapAsset 和 Mode Prefab，额外底层逻辑会增加地址兼容风险。

## 数据流

1. `panel.py` 将“个人竞技”映射为内部键 `death_match`。
2. 用户选中后，现有配置回调保存 `mode_key=death_match`。
3. `manifest.json` 声明该键和显示名称，使配置定义与界面一致。
4. `script.js` 从 `MODES` 读取 `gameMode=1`。
5. 房间开始流程中的现有 `MapAsset_ApplyGameSetting` Hook 调用 `applySelectedMode()`。
6. `findTargetMapAsset()` 在房间地图资源中查找 `gameMode=1` 的原生 DeathMatch MapAsset。
7. 现有写入逻辑更新 `GameManager.gameMode`、`weaponLimited` 和 `gameModePrefab`，并进行回读校验。
8. 现有 `MapManager_GetSpawnPoint` Hook 在 Neutral 出生点缺失时借用可用的 BL/GR 出生点，满足个人竞技玩家使用 Neutral 阵营的需求。

个人竞技沿用当前非 Nano 模式的通用分数/时间规则同步路径。此次不增加专用规则读取：当前目标是恢复原生个人竞技模式选项，具体局内规则继续来自已有房间设置流程和通用 ModeBase 字段。

## 文件改动

- `features/27_game_mode_override/panel.py`
  - 在 `MODE_OPTIONS` 中加入 `"个人竞技": "death_match"`。
- `features/27_game_mode_override/manifest.json`
  - 在 select 的 `values` 和 `display_values` 中加入 `death_match`。
- `features/27_game_mode_override/script.js`
  - 在 `MODES` 中加入 DeathMatch 定义。
- `features/27_game_mode_override/test_deathmatch_mode_option.py`
  - 新增静态一致性测试，验证三层均声明个人竞技，并确认脚本使用 `gameMode: 1`、无武器限制。

## 错误处理

继续沿用现有保护：

- 找不到 DeathMatch MapAsset 时返回“找不到目标模式 MapAsset: 个人竞技”，不进行空指针写入。
- 原生 Prefab 为空时停止应用并记录错误。
- GameManager 静态字段未初始化时停止应用。
- 写入后模式、武器限制或 Prefab 回读不一致时报告失败。
- 未知或损坏的配置键继续由现有 `MODES` 校验拒绝。

## 测试与验证

### 自动验证

1. 先添加专项测试并运行，确认它因个人竞技尚未声明而失败。
2. 完成三层最小改动后再次运行，确认专项测试通过。
3. 运行该功能目录及项目现有 Python 测试。
4. 使用 Node.js 对 `script.js` 执行语法检查。
5. 校验 `manifest.json` 可解析且模式键没有重复。

### 游戏内验证

1. 启动整合包 2.5，连接游戏。
2. 在“游戏模式切换”中选择“个人竞技”并开启。
3. 创建包含 Bot 的房间并开始游戏。
4. 确认日志显示下一局已替换为个人竞技，且没有 MapAsset、Prefab 或回读校验错误。
5. 确认计分板采用个人排名、玩家均互为敌人、死亡后可正常复活。
6. 分别从团队竞技地图和生化地图尝试切换，确认 Neutral 出生点兼容路径没有导致无法出生。

## 风险与边界

- 静态测试可以证明配置链路、枚举值和脚本语法正确，但不能替代真实游戏进程中的资源存在性验证。
- 如果个别地图的 `mapDatas` 不包含 DeathMatch MapAsset，现有逻辑会安全失败并记录明确错误；本次不伪造 Prefab。
- 若实测发现 DeathMatch 需要不同于当前通用路径的局内规则参数，应根据运行日志和游戏反编译资料另开专用改动，不在本次最小接入中猜测字段。

## 验收标准

1. 整合包 2.5 的模式下拉框显示“个人竞技”。
2. 界面、manifest 和运行脚本统一使用 `death_match`。
3. 个人竞技准确映射为 `gameMode=1`、`weaponLimited=0`。
4. 现有模式选项、默认值和切换行为不变。
5. 专项测试、相关回归测试、JSON 解析和 JavaScript 语法检查全部通过。
6. 游戏内能够创建个人竞技房间并正常生成、计分、复活；若地图不支持，功能提供清晰错误而不崩溃。
