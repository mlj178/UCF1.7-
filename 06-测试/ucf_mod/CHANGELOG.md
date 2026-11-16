# CHANGELOG · 改动记录

> 时间倒序。本文件只做索引：记「改了什么、为什么、证据在哪」。
> 当前状态见 [STATUS.md](STATUS.md)，功能说明见 [FEATURES.md](FEATURES.md)，详细过程在 [docs/](docs/)。

---

## 2026-11-16

### 23:12 · 「A* 可走面」可视化：网页编辑器 + 游戏内 HUD（独立开关）

- 背景：22:20 的结论是「人机真正跑在 NavMeshGraph 上」。但那张面只在后台导出成
  `vis/navmesh_*.bin`，看不见；这轮把它画出来，并给一个能随时开关的入口。
- 网页（`tools/navview.html` + `tools/navserver.py`）：
  - 「显示」组新增 **可走面（A* NavMesh）** 勾选，右边直接显示 `1139 三角 / 840 顶点`；
  - 2D 俯视和 3D 都画三角网线框（绿色），没数据的图显示「无数据」；
  - 服务端新增 `/api/navmesh?level=levelN`（`?info=1` 只回 JSON）。
    解析顺序：`maps/*.json` 里记的原导出名 → 按原生顶点数对号
    `vis/navmesh_nm<顶点数>-*.bin` → 404（运输船/生化酒店/暴风本来就没有）。
  - 深链接：`?open=maps/02_小型工厂.json&notour=1&navm=0` 直接打开某张图并指定可走面开关。
- 游戏内（`src/editor.c` + `src/cfg.c`）：
  - 新开关 `navmesh_show`（控制台「查看」组，默认开），**独立于 Ctrl+V 的五层**：
    Ctrl+V 关着也能只显示可走面；
  - `Ctrl+Shift+6` 随时开关，立即重建；换图后自动重建；
  - HUD 多一行：`可走面 开  1139 三角 / 840 顶点  (A* NavMeshGraph，Ctrl+Shift+6 开关)`，
    没有 NavMeshGraph 的图写「无（这张图没有 NavMeshGraph）」；
  - 数据直接读运行时 `NavmeshBase.tiles → NavmeshTile{tris,verts}`（和 nm_dump 同一份），
    不新增采集、不碰资产；线框抬高 5 cm，避免和地形打架。
- 格式坑（已写进代码注释）：`UCFNM3` 头里第二个 int 是**索引个数**（3417 = 1139×3），
  不是三角形个数；magic 是 7 字节（含结尾 0），顶点表从偏移 99 开始。
- 截图：`screenshots/web_navmesh_l2.png`（开）、`web_navmesh_l2_off.png`（关）、
  `console_navmesh_switch.png`（控制台开关）。
- 产物：`ucf_mod.dll` **252,458 B**，部署 **23:01:21**，
  回滚点 `ucf_mod.dll.deployed_20261116_230121`（249,587 B）。
- 待验证：进图看 HUD 那行与线框。本轮自动化**点不进**房间的「开始游戏」（见 STATUS §6.7）。

### 22:20 · 11 张图的「原生可通行空间」清点（PointGraph / NavMeshGraph）
- 问题：小型工厂只有 12 个 A* 点，怀疑漏采；"点这么少人机怎么还会走"也没有定论。
- 结论：12 是游戏自己报的完整节点数（不是抽样）；这 12 个点是 6 个 `WayLink`（NodeLink）的端点，
  不是路点网。小型工厂的路面是 `Factory_NavMesh`（网格 843 顶点 → A* 去重后 840；3417 索引 / 1139 三角形）。
  人机在 navmesh 上寻路，所以照常走动、寻敌。
- 方法：直接读游戏场景 `levelN` 里 AstarData 的 base64→zip→`graphN.json`（A* 4.2.17）；
  路点数按场景里 tag 20022（WayPoint）的激活物体数；网格顶点/三角形从 `resources.assets` 的 `*_NavMesh` 读。
  新增 `tools/scan_native_nav.py`，一条命令复现整张表。
- 结果表 + 证据：`docs/地图对照表.md` §「原生可通行空间（A* 图）」。
- 顺带纠正：胜利广场、死亡擂台场景里没有 PointGraph（只有 NavMeshGraph），`待采集` 对它们是错的；
  暴风配了 PointGraph 但场景里 0 个 WayPoint、也没有 navmesh，原生可走面为 0（现在那 694 点是插件铺的）。
- 原生合计：路点 4056 个（786+2+17+8+3063+180）；navmesh 8 个网格 / 7496 个三角形。

### 21:26 · 进图卡死修复：survey 的 maxZ 初值 + 五十亿次循环
- 现象：控制台启动、进「暴风」图后游戏卡死/闪退；21:13:38 WER 记录 `AppHangB1`。
- 证据：日志最后一行 `survey: coarse hits=35 bounds x[-50.0,30.0] z[-130.0,1000000000.0]`，
  之后没有 `survey: spots`；主线程卡在细扫循环。
- 根因（`src/navfix.c`）：`survey()` 的 `maxZ` 初值写成 +1e9（应为 -1e9），粗扫更新不了它；
  细扫 `fz += 4` 到 1e9 → 约 55 亿次循环，游戏无响应。日志里的 z 上限 1e9 是初值，不是命中点。
- 改法：`maxZ` 初值 -1e9；`hit_sane()` 校验命中点（有限 / 与起点同竖线 ±0.75 m / y ±500）；
  粗扫包络限 1–700 m；细扫列数上限 50000；坏点计数与首条坐标写日志。
- 验证：21:20 运输船（786 点）与 21:23 小型工厂（12 点）均能进图，未触发 survey；
  暴风图属于 `GameMode 6 = Nano4_Terminator`，房间要先选「终结者模式」才出现在地图下拉，
  下一轮复验。
- 顺带完成 20:28 的 HUD 进图复验：运输船日志 `hud: cjk font … (probe U+4E2D)` /
  `hud: ready … (game/CJK)`，左上角中文状态面板正常，截图 `screenshots/inmap_cjk_hud.png`。
- 产物：`ucf_mod.dll` **249,587 B**，SHA256 `E24D18A3…`，部署 21:32:01；
  备份 `ucf_mod.dll.deployed_20261116_213201`（21:26 首次防卡死版）。

### 20:28 · HUD 只进图显示 + 真中文字体
- 现象：大厅/房间左上角出现 `00000000`，下面一条黄色 `|++|...`。
  两者都是 UCF HUD（`g_hud` 状态行 + `g_keys` 快捷键行）：`editor_tick` 在大厅也跑，
  HUD 被提前建出来；借到的字体没有中文字形，中文标签全被吞掉，只剩数字/标点。
- 改法（`src/editor.c`）：
  1) `hud_refresh()` 开头检查 `navfix_point_graph()`，大厅直接 return，不建 HUD。
  2) 换图后旧 Canvas 可能已销毁但指针还在 → `uobj_live()` 验活，失效则 `hud_reset()`。
  3) 新增 `find_cjk_font()`：遍历场景 UGUI Text 的字体，用
     `Font.HasCharacter('中'/'国'/'的'/'房'/'间')` 选真正带中文字形的字体；
     找到后用 gchandle 根住，找不到才退回 Arial + 英文 fallback。
  4) `g_cjk` 只在字体真含中文时为 1；`g_keys` / `g_cat` 补英文 fallback，不再出现乱码。
- 验证：
  - 20:29 启动游戏，大厅日志只到 `waiting for PointGraph`，**没有** `hud: ready`
    （19:53 旧版同一位置会建 HUD）。
  - 房间截图：左上角 `00000000` 和黄色 `|++|` 条都消失
    （`screenshots/final_lobby_crop.png`）。
  - 进图中文字体本轮未复验：自动化点「开始游戏」没触发场景切换，下一轮进图确认
    `hud: cjk font ...` 与中文状态面板。
- 产物：`ucf_mod.dll` **248,005 B**，部署 20:28:47，SHA256 `261FC846…`。
  旧版备份 `ucf_mod.dll.deployed_20261116_202847`（248,005 B，20:25 版）；更早的 `…202537`（247,973 B，20:17 首版）。

### 19:46 · 控制台：「加载暴风地图」单独成组
- 需求：控制台继续拆分功能，把加载暴风地图独立出来。
- 改动：`tools/控制台.pyw` 的 `GROUPS` 顶部新增「地图」组，只放 `hidden_map`；
  标题「加载暴风地图」，说明「把隐藏图 Nano30_Storm 插进房间下拉框；关掉后选不到暴风」。
  原有「建图 / 查看 / 手动」三组不动。C 侧 `hidden_map` 本来就是独立开关
  （`plugin.c` 的 `g_hiddenMap`），这次只是补上界面入口，不重新编译 DLL。
- 防回归：新增 `tools/test_console_switches.py` —— 解析 `src/cfg.c` 的 `g_defs[]` 与面板
  `GROUPS`，断言 feature 开关一一对应、默认值一致、`hidden_map` 独占一组。
  （「C 里有开关、面板里没入口」正是它要拦的情况。）
- 验证：`python tools\test_console_switches.py` → `OK: 9 feature switches in 4 groups;
  hidden_map separate`；`控制台.pyw` 无头冒烟通过 —— 建窗、读配置、切
  `hidden_map` 写盘（false → true）、销毁；已有 `features` 键保持原值（缺的键按默认值补上，
  这是 `persist()` 的既有行为）。
- 截图：`screenshots/console_map_group.png`（本机，未入库）。

### 19:00 · 启动通行证：直接双击 exe = 原版
- 需求：`UnityCrossFire.exe` 直接启动应是原版；从控制台启动才加载 mod。
- **为什么不改加载器**：游戏根的 `winhttp.dll` 是 51 KB 预编译代理，用 pefile 查过 ——
  92 个导出**全部**是转发到 `winhttp_orig.<名字>`，导入只有 KERNEL32 + msvcrt，
  DllMain 里用立即数拼出 `<dir>\ucf_mod\ucf_mod.dll` 再 LoadLibrary（所以字符串搜不到 "ucf_mod"）。
  它能保证的只有"一定会被游戏加载"，载不载 ucf_mod.dll 由它单方面决定，没有源码就改不动。
- **改法**：把闸门放进我们自己的 `ucf_mod.dll`。`DllMain` 第一句查环境变量
  `UCF_MOD`，不是 `1` 就 `return TRUE` —— 不起线程、不读配置、不写日志、不装钩子。
- 控制台 `launch_game()` 用 `env={"UCF_MOD":"1"}` 启动游戏，令牌只对这一次子进程有效。
- **实测 A/B（真跑游戏）**：
  - 直接双击 exe → 游戏正常运行，`ucf_mod.log` 新增 **0 行**；
  - 带令牌启动 → 完整加载，`injected into MapAsset (mode=6) -> 2 entries`（4 秒内）。
- 产物：`ucf_mod.dll` **246,387 B**，部署 18:56:46，SHA256 `5A4BB25D…`。

### 18:42 · 死代码清理 + 编译闸门
- 删掉 6 处「定义了但没人用」的代码：
  `navfix.c` 的 `rptr()` 与 `make_guard_area` 里的 `tr`/`zero`；
  `editor.c` 的 `find_img()`（整段 il2cpp 图像查找，从未被调用）、
  随之失效的 `x_image_get_name` 指针与 `RESOLVE(image_get_name)`、
  解析 `nav/*.txt` 时读进来就丢的 `k2`。
- `build.ps1` 增加 `-Werror=unused-function -Werror=unused-variable`。
  **验证过闸门有效**：注入 `static int ucf_dead_probe(void)` 后编译立即失败，
  随后还原（SHA256 与注入前一致）。
- 删完 DLL 仍是 **246,163 B，字节数不变** —— 删掉的确实从未进入产物，行为零风险。
- 产物：`ucf_mod.dll` 246,163 B，部署 18:42:55，SHA256 `EF3C1113…`。

### 18:35 · 功能开关化（cfg.c + 控制台 + 拆分建图动作）
- **发现**：`plugin.c` 的 `read_config()` 从未被调用 —— 整个 `ucf_mod.json` 是死的，
  `enabled` / `scene` / `game_mode` 一直用硬编码默认值（`Nano30_Storm` / 6）。
  日志里从来没有 `config:` 那一行就是证据。
- **新增 `src/cfg.c` / `cfg.h`**：唯一配置读取器。不引 JSON 库，线性扫 `"key"\s*:\s*true|false`。
  `cfg_dump()` 启动时把 10 个开关全打进日志（`[cfg]` 前缀），关掉哪个都看得见。
- **拆分 `build_waypoints()`**：原来「铺路点 / 补蹲守点 / 造守卫区」在同一函数体里，
  第一个不跑后两个永远不执行 —— 三个开关是假的。现拆为
  `survey()`（纯采样）+ `act_waypoints()` / `act_crouch()` / `act_guard()`，
  各自读自己的开关，互不为前提。
- **`editor.c`**：HUD / 可视化 / 自动导出 / 编辑模式全部受开关控制；
  可视化关着时 HUD 仍然每 2 s 刷新（原来 `if (!g_visOn) return` 会连 HUD 一起冻住）。
- **新增 `tools/控制台.pyw` + `启动控制台.bat`**：CustomTkinter 窗口，三组开关 + 日志尾巴 + 开始游戏。
- **`tools/build.ps1` 两个 bug**：① 加源文件后丢失 UTF-8 BOM，PowerShell 5.1 解析中文报错；
  ② 局部变量 `$deploy` 与参数 `[switch]$Deploy` 同名（PowerShell 大小写不敏感）→ 赋值失败。
- 产物：`ucf_mod.dll` **246,163 B**。旧版备份 `ucf_mod.dll.deployed_20261116_183359`。
- 复现性：同源码连续编译字节数恒定，SHA256 每次不同（gcc 写入非确定性内容）——
  **核对用字节数，不要用哈希**。
- 验证：`cfg.c` 单独编译零警告；用样例 json 跑 `cfg_dump()`，10 个开关的值与文件一致；
  `控制台.pyw` 通过无头冒烟测试（建窗 + 读配置 + 读日志 + 销毁）。

### 17:30 · 工程化重构（工程/部署分离 + 清创）
- 工程端（`src/` `tools/` `docs/` `geo/` 文档）从游戏目录搬到 `06-测试\ucf_mod`，
  游戏目录只留运行时文件。工具改用 `tools/ucf_paths.py` 解析两端路径。
- 清创：部署端 1120→40 文件（122.83→3.52 MB）；工程端 973→52 文件。
- 新增 `tools/build.ps1`（编译 + `-Deploy`）；`tools/extract_geo.py`（从弃用的 navedit 抽出）。
- `uninstall.ps1` 重写为白名单删除 —— **旧版会 `Remove-Item -Recurse` 整个 ucf_mod 目录**。
- 证据：commit `1d7480da`（B1）、`3d02c3c1`（C）。

### 16:53 · 修复「人机复活后只会直走」
- 根因：进图把 A* 点图 786→27 重建，并把被删点的 `nodeIndex` 写成 -1；
  `PathHandler.pathNodes` 只在 `AstarPath.Awake` 分配一次 → 寻路线程 `IndexOutOfRange` 永久停摆 →
  `Seeker.StartPath` 永不返回 → `Bot.Update` 只能沿旧方向 `Move()`。
- 改法：删点 = A* 软删除（清 walkable 位 + 摘边）；加点 = 复用被删槽位，运行期绝不 append；不再写 -1。
- 产物：`ucf_mod.dll` 240,960 B（MD5 98BC33FD…）。
- 数据：运输船草稿改名停用 `nav\n786-57a46e3465c847cb.txt.disabled_20261116_1655`。
- 证据：`docs/NAV_STRAIGHT_2026-11-16.md`。**复验待做**：`Player.log` 不应再出现 `Unhandled exception during pathfinding`。

### 15:50 · 原始地图数据集 + 只读还原点
- `maps/` 按 `NN_中文名` 归档 11 张图原始导航数据；`backup/maps_original_<日期>` 只读还原点。
- 证据：`docs/MAPS_ORIGINAL_2026-11-16.md`、`tools/organize_maps.py`。

### 14:40 · 网页版导航编辑器
- `tools/navserver.py` + `tools/navview.html`：俯视 + 3D 分屏，保存写 `nav/<指纹>.txt` + `nav/<名>.json`。
- 证据：`docs/NAVVIEW_2026-11-16.md`。

### 13:33 · 采集模式导不出数据 + 进图 Runtime Error
- 原因 1：`vis_export()` 只在"可视化关着"时重读数据 → 开着 Ctrl+V 导出写到上个场景残留，留下 `_seen_n0` 把真图当重复跳过。
- 原因 2：导出路径调 `vis_rebuild()`（建 Mesh + UGUI Text）撞在场景加载期 → il2cpp 托管异常穿出 C 帧 → CRT abort。
- 修法：导出固定走只读 `collect_read()`、忽略图层开关、读不到点就不写文件。
- 证据：`docs/FIX_2026-11-16_navcollect.md`。

---

## 2026-11-15

### 第八轮 · 运输船渲染修正（静态合批）
- 现象：运输船画成"一堆乱刀片"。
- 根因：没处理 Unity 静态合批 —— 一个 `Combined Mesh (root: scene)` 被 69 个 Transform 各画一遍。
- 改法：读 `Renderer.m_StaticBatchInfo` 只取自己那段子网格；合批网格顶点已是世界坐标，变换用单位矩阵。
- 结果：level1 面数 1,377,197 → 39,433（真实值）；打开背面剔除；光照照搬 RenderSettings + 场景 Light。

### 第七轮 · 导航编辑器 v0.2（贴图 + 点选检视）
- `Texture2D` 读不出：UnityPy 对这个构建少读 24 字节（`m_PlatformBlob`）→ 用 `read_typetree(check_read=False)` 绕过。
- 贴图像素在 `.resS`：按 `m_StreamData.offset/size` 读，`texture2ddecoder` 解 BC1/BC3。
- `CrossFire/Shadow` 是投影副本、`ALPHA_Blocker/collision/invisible` 是隐形阻挡体 → 默认隐藏。
- 左键点选（CPU 射线-三角形求交，1.37M 面约 60 ms）；右侧检视面板。

### 第六轮 · 自动导出修正 + 只读采集模式
- 导出触发从"navfix 重建过图之后"改到 `editor_tick → auto_export_tick()`：节点数稳定约 2 秒即导出。
- 新增 `collect.flag` 只读采集模式（当时用于规避 14:47~14:48 连崩 4 次）。

### 第五轮 · 3D 导航编辑器 v0.1（navedit）—— 已于 11-16 弃用
- PyQt5 + moderngl 离线读 `UnityCrossFire_Data`，自由相机 + 点选检视，自动叠加 `vis/` 路点。
- 抽取缓存 `geo/<场景>.npz`（几何 + 分块表 + 材质表）。**抽取器保留为 `tools/extract_geo.py`。**
- 全场景三角形数：level1 1,377,197 / level8 64,872 / level9 64,508 / level10 27,556 …

### 第五轮补充 · 进图自动导出路点
- 路点图建好后插件等 2 秒自动导出一份 JSON 到 `vis/`。

### 第四轮 · 离线导航数据编辑器 P0/P1
- 导出格式升级 v1：64 位稳定 id（坐标哈希）、地图指纹、来源、包围盒。
- `tools/navview.html`（单文件，双击即用）：滚轮缩放 / 拖动平移 / 点选 / F 适应 / G 下一个孤立点 / V1–V6 校验。
- 实测 Storm：694 节点 / 1132 边，孤立 95 个（13.7%），连通分量 139 个 —— 寻路图本身是碎的。
- 契约：`docs/NAVGRAPH_FORMAT.md`。

### 第三轮 · 文字标签默认关闭
- 开机只画线框/方块/颜色，不再显示 344 个重叠中文标签。

### 第二轮 · 导航可视化编辑器
- Ctrl+V 总开关、Ctrl+Shift+1..5 分层、Ctrl+E 导出、Ctrl+H 快捷键面板。

### 第一轮 · 退出卡死 + 幽灵守卫区
- 退出卡死：nav/注入后台线程退出时不再调 il2cpp（只 PostMessage）；`WM_DESTROY` 恢复旧窗口过程。
- 幽灵卡在复活点：运行时造 42 个守卫区。
- 导航：多层射线采样 + 出生点 170 节点 + 连线 raycast 遮挡 → 694 节点；`Bot.Update` NRE 从 1595 降到 27 且不再增长。
- 证据：`docs/CRASH_FIX_2026-11-15.md`、`docs/FIX_2026-11-15.md`、`docs/VISUALIZER_2026-11-15.md`。

### 离线编辑器首版
- `docs/NAV_EDIT_2026-11-15.md`、`docs/NAV_EDIT_2026-11-15.md`。

---

## 2026-11-14 · 初版（PoC）
- `winhttp.dll` 代理加载器 → `ucf_mod\ucf_mod.dll`（原生 C，mingw 编译，运行时挂 il2cpp）。
- 隐藏地图注入（Nano30_Storm）；A* 导航点自动补全；蹲守点自动补全；标记编辑器阶段 0+1+2。
- 修改 `level9`：禁用 Canvas1/2/3、EventSystem、SniperCrosshariBG（还原点 `backup/level9.orig`）。

---

## 跨轮次关键坑（别再踩）

1. `Scan()` 只建节点不建连接，必须再调 `PointGraph.ConnectNodes`。
2. `PathHandler.pathNodes` 只在 `AstarPath.Awake` 分配一次；运行期改节点数 → 越界炸寻路线程。
3. `CreatePrimitive` 运行期拿到 `Hidden/InternalErrorShader`，必须自己 `Shader.Find("Universal Render Pipeline/Unlit")`。
4. 相机 `cullingMask=0x1f3`，layer 2 不在其中 → 标记球放 layer 0。
5. Unity API 必须在主线程：按键走 `WndProc(WM_KEYDOWN)`，换场景走 `WM_APP+0x52`，无焦点注入走 `WM_APP+0x53`。
6. UnityPy 读 `Texture2D` 少 24 字节（`m_PlatformBlob`）→ `read_typetree(check_read=False)`。
7. 贴图像素不在 `.assets` 里，按 `m_StreamData` 去 `resources.assets.resS` 读。
8. Unity 静态合批：读 `m_StaticBatchInfo`，否则同一网格被多个 Transform 重复画。
9. **覆盖 dll 前必须关游戏**（文件被占用）。
10. 构建路径不同 → 同尺寸不同哈希（gcc 嵌入路径），比对用**字节数 + 源码时间戳**，不要用哈希跨机器对照。
