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
| `hud_states` | 关 | 面板第一行：可视化 / 五层 / 标签的开关状态 | 不显示（控制台「状态面板」可开） |
| `hud_keys` | 关 | Ctrl+H 那四行快捷键帮助块 | 不显示（Ctrl+H 仍可临时叫出，只对本次进程） |
| `hud_log` | 开 | 面板底部：导出结果 + 最近 3 行日志 | 不显示（Ctrl+M 仍可切） |
| `vis_layer_a` | 开 | 可视化 A 层：路点 / 连线 | 不画 A 层（导出仍全量） |
| `vis_layer_b` | 开 | 可视化 B 层：人类蹲守 | 不画 B 层 |
| `vis_layer_c` | 开 | 可视化 C 层：幽灵守区 | 不画 C 层 |
| `vis_layer_d` | 开 | 可视化 D 层：出生点 / 补给箱 | 不画 D 层 |
| `vis_layer_e` | 开 | 可视化 E 层：模式 | 不画 E 层 |
| `vis_labels` | 0 | 文字标签：0 关 / 1 近距 35 m / 2 全部 | —— 三态，不是 bool |
| `visualizer` | 关 | 进图就画网格 | 不画（Ctrl+V 可开） |
| `navmesh_show` | **开** | 画 A* 可走面（NavMeshGraph 三角网线框）| 不画（Ctrl+Shift+6 可开；与 Ctrl+V 无关）|
| `vis_lists` | **开** | 可视化时读游戏组件表（守区/蹲守/出生点）| **完全不碰**这些表，只画 A* 图与可走面（进图闪退时的兜底开关）|
| `editor` | 开 | 游戏内编辑 | Ctrl+1 失效 |
| `collect_only` | 关 | 只读采集 | —— 开启后只导出、不改游戏 |
| `area_watch` | 开 | 每 0.5 s 体检游戏自己的守卫区列表（`SpareAreaList` / 各守区 `posList`），坏了立刻写 `!!! areas CORRUPT` | **完全不碰**这两张表（诊断期建议留着，实测开销 <0.1%）|
| `perf` | 关 | 每 60 s 把 `area_watch` 实测耗时打进日志 | 不打（默认关，只在回答「吃不吃性能」时开）|

> 控制台页签（2026-11-17 起）：**地图 / 查看 / 状态面板 / 手动** 四个开关页，外加「测试数据」「数据」页
> （2026-11-17 21:10 起「测试数据」从上方常驻面板改成页签）。
> 「建图」页（`auto_waypoints` / `auto_crouch` / `ghost_areas`）已从面板删除：
> C 侧键保留默认开，旧 `ucf_mod.json` 与回滚仍然有效，只是控制台不再提供入口。
> `hidden_map` 在「地图」页，标题「加载暴风地图」；**面板的开关全部在「状态面板」页**
> （2026-11-17 21:01 起：面板本身 / 面板显示什么 / 可视化五层 + 可走面 / 文字标签），
> 「查看」页只剩 `auto_export` 与 `vis_lists`。快捷键表仍在控制台页底部，
> 由 `tools/test_console_switches.py` 与 `src/editor.c` 逐行核对。

> HUD（`hud`）只在有 `PointGraph` 的地图里创建；大厅/房间不画。
> 2026-11-17 21:01 起游戏里**只留状态数字**：开关状态行（`hud_states`）与快捷键块（`hud_keys`）
> 默认关；开关都搬到控制台「状态面板」页。Ctrl+V / Ctrl+Shift+1..6 / Ctrl+Shift+L / Ctrl+M / Ctrl+H
> 热键仍可用，只改默认值（Ctrl+H 按一下仍能临时叫出快捷键块）。
> 字体遍历场景 UGUI Text，用 `Font.HasCharacter('中')` 选真正带中文字形的字体；
> 找不到才退回 Arial + 英文 fallback（2026-11-16 20:28）。
> 21:20 运输船进图复验通过：`hud: cjk font … (probe U+4E2D)`，左上角中文状态面板正常
> （`screenshots/inmap_cjk_hud.png`）。

> **启动通行证**：只有从 `tools\启动控制台.bat` 启动游戏时，才会递入环境变量 `UCF_MOD=1`。
> 直接双击 `UnityCrossFire.exe` 时插件在 `DllMain` 第一句就返回 —— 不起线程、不读配置、
> 不写日志、不装钩子，等于没装。（加载器 `winhttp.dll` 仍会被游戏加载，它只做纯转发。）

> `auto_waypoints` / `auto_crouch` / `ghost_areas` 原来写在同一个函数里，
> 关掉第一个后两个永远不会执行（假开关）。现已拆成 `survey()` + 三个独立动作。

## 一、游戏内功能

### 1. 隐藏地图注入
把 `Nano30_Storm`（隐藏地图「暴风」）作为可选地图插进房间下拉框。
配置在部署端 `ucf_mod.json`：`scene` / `label` / `game_mode`。
控制台「地图 → 加载暴风地图」可单独关；关掉后房间下拉框里没有暴风。
状态：✅ 可用。

### 2. A* 导航点自动补全
隐藏图的 `PointGraph` 是空的 → `Bot.Update` 每帧空引用 → 人机原地乱跳。
插件进图时：4 米网格多层射线采样（屋顶 + 室内）→ 建 `UCF_WayPoints` → 设为 `PointGraph.root`
→ `maxDistance=6` → `Scan()` → **`ConnectNodes()`**。
仅在该图节点数为 0 时触发。
状态：✅ 可用。

> 防卡死（2026-11-16 21:26）：`maxZ` 初值曾误写成 +1e9，细扫跑到 1e9 变成约 55 亿次循环，
> 主线程卡死（WER `AppHangB1`）。现有四重保险：初值 -1e9；`hit_sane` 验命中点
> （有限、与射线起点同竖线、y ±500）；包络 1–700 m；细扫列数上限 50000。

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
| Ctrl+H | 快捷键面板（默认不显示，按一下临时叫出） |

状态：✅ 可用。状态面板只进图显示，大厅/房间不再出现；中文由 `find_cjk_font()` 选中文字体。
2026-11-17 21:01 起开关默认值改由控制台「状态面板」页管理，游戏里面板只显示状态数字。

### 6.5 A* 可走面可视化（2026-11-16 23:12）

人机真正寻路用的是 **NavMeshGraph**（烘焙三角网），不是 PointGraph 路点（见
`docs/地图对照表.md` §「原生可通行空间」）。这一层以前只在后台导出成
`vis/navmesh_*.bin`，现在能直接看。

- 开关：cfg `navmesh_show`（控制台「查看」组，默认开）；`Ctrl+Shift+6` 随时开关、立即重建。
  **独立于 Ctrl+V 的五层**——可视化关着时也能只显示可走面。
- 画法：读运行时 `NavmeshBase.tiles`，把每个三角形的三条边画成细线（抬高 5 cm，双面可见）。
  不填面：游戏材质不透明，填面会把场景盖住。
- HUD 第四行：`可走面 开  1139 三角 / 840 顶点  (A* NavMeshGraph，Ctrl+Shift+6 开关)`；
  没有 NavMeshGraph 的图（运输船 / 生化酒店 / 暴风）写「无（这张图没有 NavMeshGraph）」。
- 批量上限：一条边 8 顶点 / 12 索引，批满（16000 顶点 / 56000 索引）就落一块网格，
  一张图最多 16 块，不会静默丢三角形。
- 状态：✅ 代码/编译/部署完成；⏳ 进图复验待做（见 STATUS §6.7）。

### 7. 只读采集模式
部署端存在 `collect.flag` 即开启（游戏内 Ctrl+Shift+X 也可切换）。
开启后插件**完全不改游戏状态**：不建路点、不建蹲守点/守卫区、不创建任何 GameObject；
导出走只读通道 `collect_read()`。屏幕上无显示，反馈全在 `ucf_mod.log`。
状态：✅ 可用（当前关闭）。

### 8. 自动导出路点
进图后路点图节点数稳定约 2 秒，自动落一份 JSON 到 `vis/`。
状态：✅ 可用。理由：路点是运行时生成的，资源文件里没有。

### 8.5 测试包（2026-11-17）

**一句话**：进游戏之前，在控制台里选「这次读正式版，还是读某个测试包，并且只对哪一张图生效」。
测试包是一份只对该图生效的路线改动，放在游戏目录 `packs\<包名>\<指纹>.txt`；正式版 `nav\` 一个字节都不动。

| 在哪 | 怎么做 |
| --- | --- |
| 控制台（启动前） | 「测试数据」页：正式版 / 测试包 + 包下拉 + 地图下拉 + 「只对这张图生效」→ 开始游戏 |
| 控制台（运行中） | **载入到游戏 / 重新应用 / 保存路线 / 清空当前图 / 回正式版**，不重启游戏（走 `ucf_navcmd.txt`） |
| 游戏内 | `Ctrl+Shift+N` 加点、`Ctrl+Shift+A` 选起点、`Ctrl+Shift+J` 连/断边、`Ctrl+Shift+D` 删点、`Ctrl+Shift+Z` 撤销，自动存盘 |
| 编辑器（顶栏） | **存为测试包**：把当前图刚保存的改动复制成一份包（弹框填包名） |
| 命令行 | `navdata.py pack list / new / diff / promote` |
| 验证通过后 | `navdata.py pack promote <包名>` → 备份旧文件后写进正式版 `nav\` |

插件侧启动时读三个环境变量（控制台递进来）：`UCF_PACK`（读哪个包）、`UCF_FP`（只对哪张图生效）、
`UCF_FPLABEL`（显示用）。不设 = 和以前完全一样读 `nav\`。
运行中控制台改写成对：插件每 0.5 s 查一次 `ucf_navcmd.txt`（seq 变了才执行），
`cmd=apply|reload|save|off`；切包前先用原生底图快照还原，再重新读文件套用，不需要重启游戏。
HUD 第 5 行固定显示来源：`数据 测试包 chain_a · 只对 暴风 生效 · 包内 0 项改动` / `当前图已跳过`。
状态：✅ 可用（2026-11-17 实机车测：pack 版与正式版各跑 level7/level10 均 PASS）。

**空白底图测试包（2026-11-17 20:52 起）**

如果不想在原生路线上测，而是**从 0 画自己的整条路线**，用「空白底图」包：

- 包文件第一行写 `blank`（表头下面），例如：
  ```
  # ucf-navedit v1 fp=n786-57a46e3465c847cb
  blank
  node add ...
  edge add ...
  ```
- 插件进图先把这张图的**所有原生节点**标不可走、摘掉连接，再套文件里的 `node add` / `edge add`；
  文件里没有的点/边就是没有，原生路线不会「漏」回来。
- 包目录里放一个 `nogen.txt`，自动铺点也关掉（否则暴风这种 0 点图会被自动填满）。
- 生成方式：
  - 控制台「测试数据 → 新建空白包」；
  - 网页编辑器保存面板「测试包 → 新建空白包」；
  - 命令行 `python navdata.py pack new blank_a --level 1 --blank`。
- 进图后直接在游戏里画（上面那组 Ctrl+Shift 热键），改动自动写 `packs\<包名>\`，正式版 `nav\` 一个字节不动。
- 控制台「测试数据」页可以运行中 **载入到游戏 / 重新应用 / 保存路线 / 清空当前图 / 回正式版**，不用重启游戏。
- 空白底图 **不能** `pack promote` 到正式版（正式版没有清空整张图的机制，会明确拒绝）。
- 边界：`blank` 只对测试包生效；正式版 `nav\` 里即使出现也会被插件忽略并写日志。
- **只清路点图（PointGraph）**：运输船 / 生化酒店 / 暴风这类「只有点图」的图才是真正完全空白；
  胜利广场 / 死亡擂台这类同时有 NavMeshGraph 可走面的图，原生可走面仍在，别拿它们做「完全空白」验证。

## 二、离线工具链

### 9. 网页导航编辑器（可选）
> 2026-11-17 21:23 起，主力流程是「控制台建空白包 → 进游戏 `Ctrl+Shift+N` 画 →
> 控制台「载入到游戏 / 重新应用」」；网页编辑器保留给批量查看 / 离线改点，
> **不再要求**进游戏前先载入包。

`tools\启动导航编辑器.bat` → 浏览器打开俯视 + 3D 分屏。
把游戏导出的原生数据（`maps\NN_中文名.json`）读进来编辑路点 / 连边 / 删点 / 移动；
保存写两份：`nav/<图指纹>.txt`（游戏插件读的编辑清单）+ `nav/<地图名>.json`（给人看的数据）。

**数据三版（2026-11-17）**：编辑器不再直接改游戏目录，改成 ①备份 → ②开发 → ③部署：

| 版 | 路径 | 谁写 |
| --- | --- | --- |
| ① 备份版（原生·只读，永不编辑） | `06-测试\ucf_mod\navdata\native` | 只在 `navdata.py freeze` 时写一次 |
| ② 开发版 | `06-测试\ucf_mod\navdata\dev` | 编辑器（默认） |
| ③ 部署版 | 游戏目录 `ucf_mod\` | `navdata.py publish` / 顶栏「部署到游戏」 |
| ④ 测试包 | 游戏目录 `ucf_mod\packs\<包名>\` | 顶栏「存为测试包」/ `navdata.py pack new`；只对该图生效 |

顶栏「还原原生」= ① → ②；四版路径/时间/是否一致看**控制台「数据」页**（= `python tools/navdata.py status`），
部署/还原/校验也在那页；每张卡的路径旁有 **打开文件夹**，直接开资源管理器到对应目录。
只改运行时点图，不碰 DLL、不碰游戏资源；清掉 ③ 里的 `nav\n<指纹>.txt` 就回到原图。

**地形下拉显示中文名（2026-11-17）**：`level1 · 运输船  0.67 MB` 这种格式，按关卡号排序，
同一张图有两份网格（`level9` / `nano30_storm`）按名字去重只留 `levelN` 那份。

**可走面图层（2026-11-16 23:12）**：「显示」组勾选 **可走面（A* NavMesh）**，
俯视 + 3D 都叠绿色三角网，勾选框右边直接写 `1139 三角 / 840 顶点`。
数据来自插件导出的 `vis/navmesh_*.bin`（UCFNM3），服务端 `/api/navmesh?level=levelN`
按「maps 里记录的原文件名 → 原生顶点数对号」解析；运输船/生化酒店/暴风没有 NavMeshGraph，显示「无数据」。
深链接参数：`?open=maps/02_小型工厂.json`、`&navm=0`（关掉可走面）、`&notour=1`（不弹新手引导）。
状态：✅ 可用（已实测截图 `screenshots/web_navmesh_l2.png` / `..._off.png`）。

### 9.5 进图车测（2026-11-17 新增，不用鼠标键盘）

```
cd 06-测试\ucf_mod\tools
powershell -ExecutionPolicy Bypass -File .\autotest.ps1 -Targets 7,10 -Settle 170
```

- 关卡号 = `levelN` 的 N（见 `docs\地图对照表.md`：7=沙漠要塞、10=新寂静村）；
- 插件里的 `src/autotest.c` 用 `SceneManager.LoadScene(index, LoadSceneMode.Single)` 逐张切图，
  每张等 `Settle` 个 tick（一 tick 250 ms），全过写 `autotest.txt` + 日志 `RESULT PASS` 并退出；
- 退出码 0=PASS，1=CRASH/FAIL/超时；崩了脚本会把 `!!! crash` 段打出来；
- 只在设了环境变量 `UCF_AUTOTEST` 时动作，正常游戏完全不受影响；
- 之所以要它：DSH 会话里抢不到游戏窗口前台（合成点击会落到别的窗口），只能从进程内部换图。
- 配套：`tools\screenshot_game.ps1`（PrintWindow 抓窗口）、`tools\rva_dis.py`（RVA→反汇编，不依赖 IDA）。

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
