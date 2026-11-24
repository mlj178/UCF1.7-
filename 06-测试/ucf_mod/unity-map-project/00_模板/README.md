# 00_模板 —— 加一张新图的脚手架

复制整个目录改名（`NN_<场景名><中文名>`），然后按下面 9 步做。**不要在原地改模板**。

## 目录

```
00_模板\
├─ README.md       本文件
├─ map.json        元数据模板（no / level / scene / label / skeleton / game_mode）
├─ src\            原始资源（GLB / 预览图）
├─ unity\          Unity 工程骨架（ProjectSettings + Packages + Editor\UcfBuild.cs + .gitignore）
└─ tools\          构建/补丁脚本放这里
```

## 9 步

| # | 动作 | 产出 |
| --- | --- | --- |
| 1 | 复制 `00_模板` → `NN_场景名中文名` | 目录 |
| 2 | 改 `map.json` | 关卡号 / 场景名 / 中文名 / 骨架 / game_mode |
| 3 | 原始资源进 `src\` | GLB / 贴图 |
| 4 | Unity 打开 `unity\`（**不能加 -batchmode**） | 场景 + 预制 |
| 5 | 构建脚本导出 | `run\gamepatch\NN_...\UnityCrossFire_Data\` |
| 6 | 字节补丁（外部依赖名 / .resS 路径 / 名册） | patch.json 里的 files[] |
| 7 | 校验：对象数、名册条数、每件文件 sha256 | 校验脚本 |
| 8 | `docs\guide\地图对照表.md` 加一行 | 三处同名成立 |
| 9 | 控制台「地图」页勾上 → 应用 → 进游戏 | 验收 |

## 三条必须遵守

1. **下拉框位置**：优先「追加」（`inject: true` + `game_mode`），不要顶替原图；
2. **名册**：`globalgamemanagers` 的场景条数必须 +1，否则"has not been added to the build settings"；
3. **出生点**：`MapManager` 里 16 个 `SpawnPoint.y` = 模型地面高度 + 2~3 米，不做就掉图。
