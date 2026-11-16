# FEATURES · 功能清单（当前）

> 只写「现在有什么、怎么用、可用状态」。改动沿革见 [CHANGELOG.md](CHANGELOG.md)，运行状态见 [STATUS.md](STATUS.md)。

## 零、开关（2026-11-16 新增）

全部开关在部署端 `ucf_mod.json` 的 `features` 里，由 `src/cfg.c` 读取，
**启动时把每一项打进日志**（`[cfg]` 前缀），关掉哪个都看得见。

界面：`tools\启动控制台.bat`（双击开窗，勾选即写盘）。

| 键 | 默认 | 作用 | 关掉之后 |
| --- | --- | --- | --- |
| `enabled` | 开 | 总开关 | 插件加载后完全不动作 |
| `hidden_map` | 开 | 注入隐藏地图 | 下拉框里没有「暴风」 |
| `auto_waypoints` | 开 | 铺路点 + 连线 | 人机原地不动 |
| `auto_crouch` | 开 | 自动补蹲守点 | 不布蹲点 |
| `ghost_areas` | 开 | 造幽灵守卫区 | 幽灵没巡逻区 |
| `auto_export` | 开 | 进图自动导出路点 | 不写 `vis\`（Ctrl+E 仍可） |
| `hud` | 开 | 进图显示状态面板 | 不显示（Ctrl+H 可叫出） |
| `visualizer` | 关 | 进图就画网格 | 不画（Ctrl+V 可开） |
| `editor` | 开 | 游戏内编辑 | Ctrl+1 失效 |
| `collect_only` | 关 | 只读采集 | —— 开启后只导出、不改游戏 |

> **启动通行证**：只有从 `tools\启动控制台.bat` 启动游戏时，才会递入环境变量 `UCF_MOD=1`。
> 直接双击 `UnityCrossFire.exe` 时插件在 `DllMain` 第一句就返回 —— 不起线程、不读配置、
> 不写日志、不装钩子，等于没装。（加载器 `winhttp.dll` 仍会被游戏加载，它只做纯转发。）

> `auto_waypoints` / `auto_crouch` / `ghost_areas` 原来写在同一个函数里，
> 关掉第一个后两个永远不会执行（假开关）。现已拆成 `survey()` + 三个独立动作。

## 一、游戏内功能

### 1. 隐藏地图注入
把 `Nano30_Storm`（隐藏地图「暴风」）作为可选地图插进房间下拉框。
配置在部署端 `ucf_mod.json`：`scene` / `label` / `game_mode`。
状态：✅ 可用。

### 2. A* 导航点自动补全
隐藏图的 `PointGraph` 是空的 → `Bot.Update` 每帧空引用 → 人机原地乱跳。
插件进图时：4 米网格多层射线采样（屋顶 + 室内）→ 建 `UCF_WayPoints` → 设为 `PointGraph.root`
→ `maxDistance=6` → `Scan()` → **`ConnectNodes()`**。
仅在该图节点数为 0 时触发。
状态：✅ 可用。

> 坑：`Scan()` 只建节点不建连接，必须再调 `PointGraph.ConnectNodes`。

### 3. 人机蹲守点
- 编辑器手工放置（见下）
- 自动补全：同一批采样点上 `AddComponent<Bot_CrouchPos>(team=BlackList)`，只在「该图除编辑器放的点外没有任何蹲守点」时触发。
状态：✅ 可用（当前运输船 11 个手工点）。

### 4. 幽灵守卫区 `Bot_NanoGuardArea` / `Bot_NanoGuardPos`
隐藏图原本 0 个守卫区，Ghost 的 NanoGuard 没有目标。插件运行时造 42 个区（每区 1~2 守点 + 邻居链接），注册进 `SpareAreaList`。
状态：⚠️ 可用但有残留（部分 bot 仍卡出生洞穴）。
启用前置：`posList` 非空、`entrancePos` 空数组、`zoomPos` ≥ 1 —— 否则注册了没点，`Bot.Update` 每帧 NRE。

### 5. 游戏内标记编辑器
| 键 | 作用 |
| --- | --- |
| Ctrl+1 | 开关编辑模式 |
| Ctrl+2 | 在准星地面放蹲守点 |
| Del | 删除准星最近的标记（射线优先，其次 12 米内落点）|
| Ctrl+0 | 显示/隐藏标记球 |
| Ctrl+8 | 切换新点阵营 BL/GR |
| Ctrl+9 | 状态写日志（含游戏静态表计数）|
| Ctrl+6 / Ctrl+7 | 保存到 `markers/markers.txt` / 从文件重载 |
| Ctrl+3 / Ctrl+4 | 幽灵守点 / 区域 —— **本版禁用** |

标记球 = 0.24 米球体，浮在落点上方 0.45 米，无碰撞、不投影（不干扰游戏射线）。
状态：✅ 可用。

> 坑：`CreatePrimitive` 运行期拿到的是 `Hidden/InternalErrorShader`（build 裁了 Standard），
> 必须自己 `Shader.Find("Universal Render Pipeline/Unlit")` 建材质。
> 相机 `cullingMask=0x1f3`，**layer 2 (Ignore Raycast) 不在其中** → 标记球放 layer 0。
> HUD 字体从游戏现有 UI Text 借 Font，所以中文能显示。

### 6. 导航可视化
| 键 | 作用 |
| --- | --- |
| Ctrl+V | 总开关（A 路点 / B 人类 / C 幽灵 / D 出生 / E 模式）|
| Ctrl+Shift+1..5 | 分层开关 |
| Ctrl+Shift+L | 文字标签：关（默认）→ 近距 35 m → 全部 |
| Ctrl+E | 导出 `vis/graph_*.json` |
| Ctrl+H | 快捷键面板 |

状态：✅ 可用。

### 7. 只读采集模式
部署端存在 `collect.flag` 即开启（游戏内 Ctrl+Shift+X 也可切换）。
开启后插件**完全不改游戏状态**：不建路点、不建蹲守点/守卫区、不创建任何 GameObject；
导出走只读通道 `collect_read()`。屏幕上无显示，反馈全在 `ucf_mod.log`。
状态：✅ 可用（当前关闭）。

### 8. 自动导出路点
进图后路点图节点数稳定约 2 秒，自动落一份 JSON 到 `vis/`。
状态：✅ 可用。理由：路点是运行时生成的，资源文件里没有。

## 二、离线工具链

### 9. 网页导航编辑器（主力）
`tools\启动导航编辑器.bat` → 浏览器打开俯视 + 3D 分屏。
编辑路点 / 连边 / 删点 / 移动；保存同时写两份：
- `nav/<图指纹>.txt` —— 游戏内插件直接读的编辑清单（进图自动套用，或 Ctrl+Shift+R 重套）
- `nav/<地图名>.json` —— 编辑后的权威数据，供下次打开继续改

只改运行时点图，不碰 DLL、不碰游戏资源；删掉 `nav/<指纹>.txt` 即恢复原图。
状态：✅ 可用。

### 10. 数据格式
`docs/NAVGRAPH_FORMAT.md`：节点 64 位稳定 id（坐标哈希）、地图指纹、来源(ours/game)、包围盒，
patch 与 full 语义，V1–V6 校验规则。

## 三、明确未做 / 已废弃

| 项 | 状态 | 说明 |
| --- | --- | --- |
| `Bot_JumpLink` 跳台 | ❌ 未做 | 必须绑定 A* 图节点对，需在 Scan 后挂 |
| `SP_RedBox`/`SP_BlueBox` 补给箱点 | ❌ 未做 | `MapManager.pointDic` 缺 SupplyBox → 偶发 NRE（不影响游玩）|
| 阵营出生点全量注册 | ❌ 未做 | 同上 |
| 桌面版 3D 编辑器 `navedit` | 🗑 已弃用 | 2026-11-16 被网页版取代；抽取器保留为 `tools/extract_geo.py` |
| 体探针 / botwalk | 🗑 已废弃 | 源码零引用，文件已清理 |
