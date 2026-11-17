# CHANGELOG · 改动记录

> 时间倒序。本文件只做索引：记「改了什么、为什么、证据在哪」。
> 当前状态见 [STATUS.md](STATUS.md)，功能说明见 [FEATURES.md](FEATURES.md)，详细过程在 [docs/](docs/)。

---

## 2026-11-17

### 21:35 · 数据页每张卡加「打开文件夹」

**为什么**：用户要求「数据这里，给路径做一个按钮，可以快捷打开文件夹路径」。

**做法（2 处）**

| 文件 | 改动 |
| --- | --- |
| `tools/控制台.pyw` | 数据页四张卡（①备份 / ②开发 / ③部署 / ④测试包）的路径行右侧加 **打开文件夹** 按钮（88×22，深灰）；新增 `open_folder(path)`：存在 → `os.startfile` 并在状态栏写「已打开：…」，不存在 → 「目录不存在：…」（不自动建目录）；路径 `wraplength` 610 → 500 给按钮让位 |
| `tools/test_console_switches.py` | 静态断言「打开文件夹」按钮与 `open_folder` 存在 |

**边界**：只动控制台；`src\*.c` / 部署端 DLL 未动。测试数据页原有的「打开目录」（会顺手建空目录）保持原样。

**验证**

- 实例化 + 临时 `os.startfile` 打桩：4 张卡都带「打开文件夹」；`open_folder(①)` → `已打开：…`；
  `open_folder(不存在的路径)` → `目录不存在：…`
- 截图 `screenshots/console_tabs_data.png`

### 21:23 · 控制台内完成「应用 / 载入」，路线改到游戏里画

**为什么**：用户嫌「网页编辑器 → 载入运输船 → 应用到游戏 → 测试包填包名 → 载入包」太绕，要求
「暂时不要动导航编辑器，进游戏内部编辑地图；应用、载入这些内容做到控制台里」。

**做法（4 处）**

| 文件 | 改动 |
| --- | --- |
| `src/editor.c` | 新增控制台命令通道 `ucf_navcmd.txt`（`seq / cmd / pack / fp`，seq 用 64 位）：主线程 tick 每 0.5 s 查一次，seq 变了才执行 `apply / reload / save / off`；首次套用前拍原生底图快照（可走位 + 坐标 + 连接，连接按 nodeIndex 存），切包/回正式版先还原再套新文件；`nav_reapply`（Ctrl+Shift+R）改成「还原底图 → 重读文件 → 套用」；空白底图激活时可视化不再画不可走的原生点 |
| `tools/控制台.pyw` | 「测试数据」页新增 **载入到游戏 / 重新应用 / 保存路线 / 清空当前图 / 回正式版** 五个按钮 + 当前包摘要（空白底图 · 几点几边 · 最后写入时间）；按钮写 `<部署端>\ucf_navcmd.txt`；「新建空白包」在游戏运行中会自动发送 apply；底部「打开导航编辑器」改成「导航编辑器（可选）」 |
| `tools/test_console_packcmd.py` | 新增：包摘要（blank/加点/加边/删点/删边）、manifest.fp 优先、命令文件原子替换 + seq 单调 + 四行格式 |
| 文档 | `docs/人机与路线设计.md` §5.3.1、`FEATURES.md` §8.5、`STATUS.md` §2.4 改成「进游戏里画 + 控制台按钮」流程 |

**机制**：控制台原子写 `ucf_navcmd.txt`，插件 `pack_init()` 启动时只记 seq 不执行旧命令；
运行中 `nav_cmd_tick()` 看到新 seq 才动作。切包前 `nav_base_restore()` 用快照把
PointGraph 还原成进图原生状态，再读 `packs\<包>\<fp>.txt` 套用；连接全部按 nodeIndex
还原，场景重建后不会把旧 PointNode 写进新图。

**边界**：网页编辑器代码（navview.html / navserver.py / navdata.py）没改；正式版 `nav\` 仍然拒绝 `blank`；
空白包不能 `pack promote`；`blank` 只清 PointGraph，胜利广场/死亡擂台的 NavMeshGraph 可走面仍在。

**验证**

- gcc 编译 **287,371 B**，产物 `build/ucf_mod-20261117-2123-6f8cbca3.dll`；**21:23:28 已 -Deploy**，
  旧 DLL 备份 `ucf_mod.dll.deployed_20261117_212328`（286,859 B，21:19 运行中命令首版）
- `python tools/test_console_packcmd.py` → `OK: pack summary + ucf_navcmd.txt`
- `python tools/test_blank_pack.py` → OK（空白链仍在）
- `python tools/test_console_switches.py` → `OK: 17 feature switches in 4 tabs …`
- 真实控制台实例化：6 个页签、`lbl_pack` 摘要、`opt_pack` 值 `['blank_a','chain_a']`，切「测试数据」无异常；
  截图 `screenshots/console_pack_controls.png`
- **车测 level1（运输船）PASS**：360 tick，日志 `naved: blank base: disabled 786 native nodes`、
  `naved: applied 786/0 edits … [blank base]`；运行中依次发 `reload` → `base restored (786 nodes)` → 再套 blank；
  `off` → `pack -> (official nav)`；`apply` → 再套 blank；`=== RESULT PASS target=1 ===`
- **游戏内加点验证**：WM_APP+0x53 注入 Ctrl+Shift+N → `naved: node added idx=0`，
  pack 文件写出 `blank + node add -0.000 -16.590 0.399`；临时包用后已删
- 说明：第一次用 `UCF_AT_EXIT=0` 启动时，autotest 在解析阶段崩过一次（栈全在 `autotest.c`，
  与导航改动无直接栈帧）；改用 `UCF_AT_EXIT=1` 重跑通过，未复现

### 21:10 · 「测试数据」从常驻面板改成页签

**为什么**：用户要求「测试数据你放到下面的页内标签切换」——它原来常驻在页签上方，占掉约 250 px，
把下面的开关页挤得只剩一小条，必须滚动。

**做法（2 处）**

| 文件 | 改动 |
| --- | --- |
| `tools/控制台.pyw` | `build_pack_panel()`（`self` 上常驻的卡）→ `build_pack_tab(tab)`（页内滚动区 + 卡片）；页签顺序 **地图 / 查看 / 状态面板 / 手动 / 测试数据 / 数据**；顶部说明改成「测试包模式、四版数据……切到『测试数据』『数据』页」；切到「测试数据」页自动刷新包列表（`on_tab`） |
| `tools/test_console_switches.py` | 新增静态断言：`self.tabview.add("测试数据")` 必须存在、旧 `build_pack_panel` 必须消失、「测试数据」页在「数据」页之前 |

**边界**：只动控制台布局；`src\*.c` / 部署端 DLL 一个字节没改（仍跑 21:01 那版 281,732 B）；
测试包选择、env（`UCF_PACK` / `UCF_FP`）、新建空白包的语义都不变。

**验证**

- `python tools/test_console_switches.py` → 通过（17 个开关 / 4 个开关页；测试数据页断言通过）
- 实例化真实窗口：页签顺序 `地图 / 查看 / 状态面板 / 手动 / 测试数据 / 数据`（6 个）；
  `opt_pack` / `opt_map` / `seg_mode` 都在，切到「测试数据」页调 `on_tab` 无异常
- 页签可视高度 **285 → 553 px**（同一窗口），「状态面板」页一屏能同时看到面板 + 可视化两组开关
- 截图 `screenshots/console_tabs_pack.png` / `screenshots/console_tabs_status.png`

### 21:01 · 面板开关搬进控制台，游戏里只留状态数字

**为什么**：用户澄清「我的意思是把面板的一些开关给迁移到控制台里。不在游戏里面展示。」
20:45 那版只是把面板内容抄成静态示意，开关仍只能在游戏里按热键，状态也还画在屏幕上。

**做法（4 处）**

| 文件 | 改动 |
| --- | --- |
| `src/cfg.c` | 新增 9 个开关：`hud_states`（第一行开关状态，默认关）、`hud_keys`（快捷键块，默认关）、`hud_log`（导出 / 最近日志行，默认开）、`vis_layer_a..e`（五层，默认开）、`vis_labels`（0 关 / 1 近距 35 m / 2 全部，默认 0）；`cfg_dump` 对 `vis_labels` 按整数打印 |
| `src/editor.c` | `editor_start()` 读这 9 个键（`g_lay` 由五个 bool 拼、`g_lblMode` 夹在 0..2）；`hud_refresh()` 第一行只在 `hud_states` 打开时才画，快捷键块只在 `hud_keys` 打开时才画（否则空串）；Ctrl+V / Ctrl+Shift+1..6 / Ctrl+Shift+L / Ctrl+M / Ctrl+H 热键全部保留，只改默认值 |
| `tools/控制台.pyw` | 「状态面板」页改成控制页：**面板**（hud / hud_states / hud_keys / hud_log）+ **可视化**（visualizer + A–F 六层）+ **文字标签**三态 + 键位表；「查看」页只剩 `auto_export` / `vis_lists`；`persist()` 把 `vis_labels` 写成 int（不是 bool） |
| `tools/test_console_switches.py` | 17 个开关 / 4 个页签的断言；`vis_labels` 进 `CUSTOM` 白名单并核对默认值；新增 `LAYER_KEYS` / `vis_labels` 必须在「状态面板」页 |

**边界**：热键语义不变（只改默认显隐）；`hud=off` 时游戏里不留任何提示，控制台是唯一入口；
这些键仍是「写 `ucf_mod.json` → 下次启动生效」，不是运行中即时生效。

**验证**

- `python tools/test_console_switches.py` → `OK: 17 feature switches in 4 tabs (地图/查看/状态面板/手动); 3 build-map switches retired; HUD keys 4/4 match editor.c`
- gcc 编译 **281,732 B**，产物 `build/ucf_mod-20261117-2101-6f8cbca3.dll`（含 20:52 空白底图改动）；
  **21:01:04 已 `-Deploy`**，旧 DLL 备份 `ucf_mod.dll.deployed_20261117_210104`（280,677 B，空白底图版）
- 车测 `autotest.ps1 -Targets 7,10 -Settle 60` → **PASS**（21:01:14 → 21:02:00，level7 / level10 各 60 tick）；
  日志：`[cfg] hud_states = off (default)` … `[cfg] vis_labels = 0 (default)`；
  `editor ready: hud=1 states=0 keys=0 log=1 visualizer=1 layers=0x1F labels=0 …`
- 控制台实例化 + 临时 `ucf_mod.json`：`vis_layer_c` / `hud_states` / `visualizer` 勾掉、标签切「全部」
  → 落盘 `false / false / true / 2`；`hud` / `editor` 原样保留，`seg_labels` 读回「近距 35 m」

### 20:52 · 测试包支持「空白底图」：原生点全禁用，从 0 画自己的路线

**为什么**：测试包原来是「正式底图 + 增量改动」，空包 = 什么都不改，所以进图仍然走游戏原生路线。
用户要的是**完全空白**：原生点一个都不留，测试包里的点/边就是唯一路线，自己画完再验证。

**做法（6 处）**

| 文件 | 改动 |
| --- | --- |
| `src/editor.c` | 识别测试包文件里的 `blank`：进图先把该图**所有原生节点**标不可走、摘掉连接，再套 `node add` / `edge add`（`nav_revive_slot` 复用原生槽位，不增长 nodes 数组）；`nav_save` 保留 `blank`；`nav_needs_apply` 在 blank 下核对「可走点必须全是 add、add 点/边都还在」，图被重扫会自动重套；`blank` 只对测试包生效，正式版 nav 里写了也会被忽略；顺手修了游戏内编辑器「删自己加的点」会留下 add+del、重进图又活过来的问题（`nav_drop_add`） |
| `tools/控制台.pyw` | 「测试数据」新增 **新建空白包**：按当前选中的图建 `packs\<包名>\<指纹>.txt`（`blank`）+ `nogen.txt` + `manifest.json`，并自动切到测试包模式 |
| `tools/navserver.py` | 新增 `GET /api/pack-txt`、`POST /api/pack-save`（只写 packs，备份旧文件，维护 manifest / nogen）；`validate_txt` 识别 `blank`，正式版 `/api/save` 明确拒绝 blank |
| `tools/navview.html` | 保存面板新增「测试包 / 载入包 / 新建空白包」；进入测试包后空白底图 = 0 点 0 边起步，保存写回 pack；目标指纹在包模式下锁定；状态栏/校验卡显示「空白底图」 |
| `tools/navdata.py` | `pack new <名> --level N --blank` 生成空白包（含 nogen.txt）；`pack list` 标「空白底图」；`pack promote` 拒绝把 blank 包升正式版 |
| `docs\人机与路线设计.md` / `FEATURES.md` | 补「空白底图」的五步工作流和边界 |

**边界**：空白底图只允许测试包；正式版 `nav\` 仍是增量改动，不会清空整张图。
包目录里的 `nogen.txt` 会让 `editor_nogen()` 跳过自动铺点（暴风这种 0 点图也不会被自动填满）。

**验证**

- `gcc` 全量编译通过（280,677 B，产物 `build/ucf_mod-20261117-2056-6f8cbca3.dll`；**20:56 已 `-Deploy`**，旧 DLL 备份 `ucf_mod.dll.deployed_20261117_205622`）
- 网页编辑器（headless Chrome + 本地服务）实跑：载入运输船 786 点 → 新建空白包 → 模型 0 点 0 边 → 加 2 点 1 边 → 保存 → 包文件为 `# ucf-navedit v1 fp=…` + `blank` + 2 个 node add + 1 个 edge add；重载后仍是 2 点 1 边、`origNodes=0`
- `/api/pack-save` / `/api/pack-txt` / 正式版拒绝 blank / 非法行拒绝：临时服务端测试全部通过
- 控制台实例化真实窗口：选中运输船 → 新建空白包 → 生成 `blank` 文件 + nogen + manifest，页签切到测试包
- `python tools/test_console_switches.py` 仍通过；新增 `tools/test_blank_pack.py` 静态核对
  editor.c / navdata.py / navserver.py / navview.html / 控制台.pyw 五处链路 → **OK**
- JS `node --check` 通过

**下一步**：从控制台「新建空白包」建包 → 编辑器画路线 → 开始游戏。DLL 已部署；以后要再换 DLL 只能 `tools\build.ps1 -Deploy`（会先关游戏）。

### 20:45 · 控制台新增「状态面板」页：HUD 从「查看」独立出来

**为什么**：用户要求「控制台状态面板，专门独立出来一个 tab」。`hud` 原来混在「查看」的四个开关里，
而它自带一屏内容（4 行状态 + 第 5 行数据来源 + Ctrl+M 日志行）和一整块 Ctrl+H 快捷键，值得单独一页。

**做法（2 处）**

| 文件 | 改动 |
| --- | --- |
| `tools/控制台.pyw` | `GROUPS`：`hud` 移出「查看」，新增「状态面板」页（页签顺序 地图 / 查看 / 状态面板 / 手动，`数据` 仍在最后）；开关卡片抽成 `switch_card()` 复用；新页 `build_hud_tab()` 附两块只读示意 `HUD_PREVIEW`（面板长什么样）与 `HUD_KEYS`（Ctrl+H 快捷键原文），底部四条说明（只进图创建 / 关掉后 Ctrl+H 能叫回 / 第 5 行是数据来源 / Ctrl+M 与只读采集）；文本框用 `wrap="word"`，快捷键不会断在词中间 |
| `tools/test_console_switches.py` | `TABS` 改为 地图/查看/状态面板/手动；断言 `hud` 必须属于「状态面板」；`HUD_KEYS` 逐行与 `src/editor.c` 做子串比对（C 侧改了键位、控制台忘了同步 → 直接报错） |

**边界**：只动控制台与自检，`src\*.c` 和部署端 `ucf_mod.dll` 一个字节没改；`hud` 语义不变
（cfg 键、默认开、进图才创建、Ctrl+H 叫回）。

**验证**

- `python tools/test_console_switches.py` → `OK: 8 feature switches in 4 tabs (地图/查看/状态面板/手动); 3 build-map switches retired; HUD keys 4/4 match editor.c`
- 实例化真实窗口（临时脚本放 `%TEMP%`，跑完即删）：5 个页签顺序正确、逐个切换无异常；
  两块文本框内容与常量逐字一致；`hud` 勾掉 / 勾回各写一次**临时** `ucf_mod.json`，`enabled` / `editor` 原样保留
- 截图 `screenshots/console_tabs_status.png`

> **21:01 更新**：这一版的静态示意已被「状态面板」真正的开关页取代（见上一条）。

### 19:13 · 控制台改页签：删「建图」页，地图 / 查看 / 手动 三页切换

**为什么**：控制台原来是一条长滚动列表，四组开关堆在一起；「建图」那页的三项
（自动铺路点 / 自动补蹲守点 / 幽灵守卫区）不再从面板改，留着只会误点。

**做法（2 处）**

| 文件 | 改动 |
| --- | --- |
| `tools/控制台.pyw` | `GROUPS` 删掉「建图」三项；剩余三组改成 `CTkTabview` 三个页签（地图 / 查看 / 手动），每页内部仍可滚动；窗口高度按 DPI 折算（125% 下原 900 会把底部按钮顶到任务栏外），按钮/日志改为从底边占位 |
| `tools/test_console_switches.py` | `RETIRED` 显式豁免三个建图键（C 侧默认仍为开）；断言页签顺序为 地图/查看/手动、`hidden_map` 留在「地图」页、三个键不许再冒回面板 |

**边界**：只动控制台，`src/cfg.c` / `navfix.c` 与部署端 `ucf_mod.dll` 一个字节没改；
旧 `ucf_mod.json` 里的三个键仍然生效（默认开），只是面板不再提供开关。

**验证**：`python tools/test_console_switches.py` → `OK: 8 feature switches in 3 tabs
(地图/查看/手动); 3 build-map switches retired`；实开窗口截图三页正常，底部按钮可见。

### 19:55 · 四版信息搬进控制台；三个 navdata .bat 删除

**为什么**：用户要求"各个版本的更新日期+时间、位置等信息放到 UCF 控制台里，文档不需要了；
部署到游戏 / 还原原生 / 三版状态三个 bat 并进控制台，把 bat 删掉"。

**做法**

| 位置 | 改动 |
| --- | --- |
| `tools/控制台.pyw` | 新增第四页「数据」：①备份 / ②开发 / ③部署 / ④测试包 四张卡（绝对路径、最近写入时间、图数 / 编辑文件+条数 / 可走面 / 体积 / 文件数）；一行一致性结论（只比 `maps\*.json` 与 `nav\*.txt`，索引与 names.json 不算）；四个按钮 **部署到游戏 ②→③** / **还原原生 ①→②**（先弹确认）/ **校验备份版** / **刷新**，切页签自动刷新 |
| 同上（线程模型） | `navdata.py` 在后台线程跑（`PYTHONIOENCODING=utf-8`、`CREATE_NO_WINDOW`），结果进 `queue.Queue`，主线程 `after(150)` 轮询再写控件——工作线程不碰 Tk（否则报 `main thread is not in main loop`） |
| `tools/部署到游戏.bat`、`还原原生.bat`、`三版状态.bat` | **删除**（3 个文件）；功能 = 上面三个按钮 + 四张卡 |
| `docs/数据四版_时间与路径_2026-11-17.md` | **删除**（19:05 建的 270 行文档，内容以卡片形式进了控制台） |
| 文档同步 | `三版数据与路径_2026-11-17.md` §3 的 bat 表格改成"控制台「数据」页 → 等价命令"；FEATURES 8.4 / STATUS §5 的 `三版状态.bat` 改成控制台；README / 人机与路线设计 去掉刚加的文档链接 |

**证据**（`tools/_smoke_console.py` 实例化真实窗口后读控件文本，跑完即删）

    ① | 2026-11-17 12:13:28 | 9 图 · 编辑 0 个文件/0 条 · 8 可走面 · 1.3 MB，共 18 个文件
    ② | 2026-11-17 11:14:53 | 9 图 · 编辑 0 个文件/0 条 · 8 可走面 · 1.3 MB，共 20 个文件
    ③ | 2026-11-17 18:52:13 | 9 图 · 编辑 0 个文件/0 条 · 8 可走面 · 1.8 MB，共 37 个文件
    ④ | 2026-11-17 18:39:16 | 1 个包：chain_a（0 条）
    一致性（只比 maps\*.json 与 nav\*.txt，索引与 names.json 不算）：①=② · ②=③
    点「校验备份版」→ OK 备份版校验：通过（18 个文件）／只读属性：是

**边界**：只动工具与文档，`src\*.c` 与部署端 `ucf_mod.dll` 一个字节没改；`启动控制台.bat`
与 `启动导航编辑器.bat` 保留。CLI 用法不变：`python navdata.py status|publish|restore|verify|diff`。

**顺带**：STATUS 里 ① 的冻结时间仍是实测的 **12:13**（`.frozen.json` 的 `frozen_at`），不是 bat 时代写的 11:15。

### 18:41 · 测试包：进图前选「正式版 / 测试包 + 只对哪张图生效」

**为什么**：要"启动前在控制台选这次加载哪张图的人机路线"，且**不能污染正式版数据**；
人机行为本身改不了（进图才 new），但"读哪套路线数据"完全可以提前定。

**做法（4 处）**

| 文件 | 改动 |
| --- | --- |
| `src/editor.c` | `pack_init()` 读 `UCF_PACK` / `UCF_FP` / `UCF_FPLABEL`；`g_navDir` 取代两处硬编码的 `%s\nav`；`nav_edit_tick` 指纹不符就整包跳过（`pack: skip`）；HUD 加第 5 行「数据 正式版/测试包 …」；换图时清 `g_packSkip` 让每张图各记一行；`editor_nogen()` 也认包目录 |
| `tools/控制台.pyw` | 新增「测试数据」面板：正式版/测试包 + 包下拉 + 地图下拉 + 「只对这张图生效」；启动时塞 env；选择存进 `ucf_mod.json` 的 `pack` 段（插件不读，只是面板记忆）；窗口 720×900 |
| `tools/navdata.py` | `pack list / new / diff / promote`（`promote` 先备份旧文件再写正式版；`level4/11` 只有可走面，明确提示"测试包没意义"） |
| `tools/navserver.py` + `navview.html` | 编辑器顶栏 **存为测试包** → `POST /api/pack-new` → `packs\<包名>\<指纹>.txt` + `manifest.json` |

**实机车测（无人值守，`UCF_AUTOTEST=7,10`）**

| 跑法 | 日志 | 结果 |
| --- | --- | --- |
| `UCF_PACK=chain_a UCF_FP=n0-0000000000000000` | `pack: chain_a dir=…\packs\chain_a target=n0-…` → 两次 `pack: skip chain_a (want n0-…, current n12-…/n180-…)` | **PASS** |
| 不设 `UCF_PACK`（正式版） | `pack: (none / official nav) dir=…\nav` → `naved: no edit file for n12-…/n180-…` | **PASS** |

**边界**：不设这两个变量时，行为与上一版完全一致（正式版路径、编辑清单、HUD 其余 4 行都没变）。
包名只收 ASCII：插件用 ANSI 的 `CreateDirectoryA/fopen`，中文路径没验证过。

### 13:40 · 看门狗开销实测：一个槽位 13.5 µs → 1.4 µs，频率减半，且可关

**为什么动它**：13:33 用户实机（沙漠要塞，`areas: n=3 cap=4`）问「看门狗会不会拖慢游戏」。

**实测**（`build/bench_watch.c`，同款 gcc -O2，本机）：

| 项 | 实测 |
| --- | --- |
| `VirtualQuery`（`safe_rd` 每读一次都调） | **391 ns** |
| 旧实现 `obj_klass_ok` 校一个槽位（读槽位 + 扫类名 17 字节 = 21 次 VirtualQuery） | **13.5 µs** |
| 新实现（类指针命中速查表后只剩 2 次读） | **1.37 µs**（≈10×） |

**改动**（`src/editor.c`）

1. `obj_klass_ok` 加 8 项类指针速查表 `g_clsMemo`：同一个列表里的槽位几乎总是同一个类，
   只有第一次遇到新类才逐字节扫类名。`Il2CppClass` 生命周期等于进程，缓存不会失效。
2. 体检从「每 tick」改成「**每 2 tick**（0.5 s）一次」—— 代码注释本来就写着 2 tick，实际没实现。
3. 新开关 `area_watch`（默认 true）：设 false 则完全不碰这张表。
4. 新调试开关 `perf`（默认 false）：打开后每 60 s 打一行
   `perf: area_watch avg=..us max=..us (~..% of one core)`，用实测数据回答性能问题。

**实机旁证**（用户 13:33:24 启动、沙漠要塞）：tick 计数 60/120/180/240/300 分别落在
13:33:41/56/13:34:11/26/41 —— **正好 4.00 tick/s，无停顿**；`areas: n=3 → n=2 → n=3`
是游戏自己加/摘守区，**没有一条 `!!! areas CORRUPT`**。

### 13:10 · 闪退真因（已修）：`purge_guard_areas()` 把游戏的 `Bot_NanoGuardArea.SpareAreaList` 数组写花了

**这是 10:22 以来全部 6 次闪退（沙漠要塞 / 新寂静村）的共同真因，已在本机复现并修掉。**

**怎么定位的**

1. 12:39 的崩溃栈（crash.dmp 解出来）不是存活判定，而是人机 AI：
   `Bot.Update → BotAction.NanoGuard.Update → Bot_NanoGuardArea.GetPos → SpareAreaList.Remove(this) → List.IndexOf → ObjectEqualityComparer.IndexOf`，
   在 **某个数组槽位** 上做虚调用时崩（槽位值 `0xacf898f8`，没映射）。
2. 12:51 加了「守卫区列表看门狗」（每 tick 抄一遍 SpareAreaList 的槽位指纹）——
   **车测（进程内 LoadScene，没人机）就能复现**：`n=3 cap=4`，槽位 `[0]=5050f0d8 [1]=027c027c`，
   第三个是合法 `Bot_NanoGuardArea`（用 il2cpp 的 `type_get_name` 解出来）。
3. 用 `List<T>` 的字段偏移核对（`_items=+0x8 _size=+0xc _version=+0x10`，和猜的一致）+ 二分：
   - 只读采集（collect-only，插件不动手）→ 列表干净；
   - 强制 GC（`gc_probe`）→ 列表干净；
   - 交互模式（会跑 purge）→ 列表花；
4. 在 purge 前后各打一次快照，**一次锁定**：

```
dbg[purge-before] [0]=027954d8 ok=1  [1]=027950f0 ok=1  [2]=02795050 ok=1
dbg[purge-after]  [0]=5050f0d8 ok=0  [1]=02790279 ok=0  [2]=02795050 ok=1   ← 被写花
```

**根因**（`src/navfix.c` `purge_guard_areas`）：压缩循环原来这么写

```c
P o = *(P*)((char*)items + 0x10 + i*4);
if (n_live(o)) *(P*)((char*)items + 0x10 + w++) = o;   /* ← 这一行 */
```

在 `-O2` 下，「读槽位 → 判活 → 写回同一下标」被压成半宽度（16 位错位）写入：
`0x027954d8` 变成 `0x5050f0d8`、`0x027950f0` 变成 `0x02790279` —— 高 16 位来自堆基址、低 16 位串位。
数组里于是留下两个**不是对象**的野值，而 `_size` 仍是 3。

**为什么只有这两张图崩**：只有沙漠要塞(level7)/新寂静村(level10) 进图时 `SpareAreaList` 里有内容
（幽灵守区；level7 是 3 个，level10 是 10 个）。列表被写花后：

- 进图 0–1 s Unity 自动 `UnloadUnusedAssets` 的存活判定走查这个数组 → 0x1290b1 崩（10:22/10:23/10:35/11:32/11:33 五次）；
- 对局里人机 `Bot_NanoGuardArea.GetPos` 走 `SpareAreaList.Remove` → `IndexOf` 对野值做 `Equals` → 崩（12:39 那次）。

原版没这个函数，所以原版不崩；车测没人机，只有第一个症状，所以之前一直以为「车测复现不了」。

**改法**（`src/navfix.c`）：显式 4 字节读、**只在 `w != i` 时才 4 字节搬**，绝不原地写：

```c
unsigned tmp = 0;
memcpy(&tmp, (char*)items + 0x10 + i*4, 4);
o = (P)tmp;
if (!o) continue;
if (n_live(o)) { if (w != i) memcpy((char*)items + 0x10 + w*4, &tmp, 4); w++; }
else dead++;
```

**验证（本机，13:05–13:07）**

- 修前：level7 `purge-before` 3 个全合法 → `purge-after` 花 2 个；level10 `n=10` 同样花；
- 修后：level7 `[0..2]` **逐字节一致**、level10 `n=10 cap=16` 一致；
- 正常配置（hud/visualizer/navmesh 全开）车测 `7,10,5,2` 全 PASS，日志里没有任何 `areas CORRUPT`。

**顺手修的**：`hud_refresh` 里 `sprintf(miss, "   缺:%s", g_miss)`（`miss[200]` / `g_miss` 最多 255 字节）
会踩栈 → 改 320 字节 + `snprintf`。

**新增诊断（留着）**：`areas:` 看门狗（每 tick 校验 SpareAreaList + 每个守区的 posList，发现非对象槽位立刻打
`!!! areas CORRUPT` + 槽位/类名/最近日志）；`flush_mesh_to`/`inject_one` 增加「数组长度必须等于请求长度」的闸；
`list layout` 启动时打印 List<T> 字段偏移；`gc_probe` 调试开关。

### 12:27 · 闪退真因再定位：不是 GC 写屏障，是 Unity 的「资产存活判定」（Resources.UnloadUnusedAssets）

**10:33 那条结论（GameAssembly+0x1290b1 = il2cpp GC 写屏障）是错的。** 本次用 PE 导出表 +
反汇编逐条核对：

| 名字 | 真实 RVA | 说明 |
| --- | --- | --- |
| `il2cpp_gc_wbarrier_set_field` | 0x1084e0 → **0x14cd80** | 真正的写屏障 |
| `il2cpp_unity_liveness_calculation_from_root` | 0x109340 → **0x12cdb0** | 崩溃帧 #4（0x12d0f1）就在这个函数里 |
| `il2cpp_unity_liveness_calculation_from_statics` | 0x109350 → 0x12ce10 | 同上 |
| 0x1290a0 / 0x1290b1 / 0x1290c1 | 内部函数 | 存活判定走查：`test $1,klass` → `mov (%ebx),%eax` 读 obj->klass |

调用链（5 次闪退的 EBP 链完全一致）：

```
UnityPlayer+0x601ad1 → il2cpp_unity_liveness_calculation_*（0x12ce00）
  → 0x144217 → 0x14458a → 0x1441dc（逐槽位走查一个「引用数组」）
  → 0x1290a0（把槽位值当对象，读它的 klass）→ 崩
```

- 崩溃时 `esi` = 数组长度（两次分别 16 / 4），`edi-0x10` = 数组对象，`ebx` = 被当成对象的坏值。
  坏值有时是**数据**（0x70007500 = UTF-16 "pu"、0x35cd35cd），有时是**已释放的托管对象**
  （0x08cc35c4，klass=0）→ 这个「引用数组」里混进了非对象数据 / 已回收对象。
- 触发时机：进图后 ~0–1 s，即 Unity 换图后自动跑的那次 `Resources.UnloadUnusedAssets`。
- 只在 **沙漠要塞(level7) / 新寂静村(level10)**：这两张是**仅有的两张走 `Mode_Nano6` /
  `Mode_Nano4_Terminator` 专用模式类的图**（生化酒店是普通 `Mode_Nano4`，其余是
  TeamDeath/DeathMatch/Special）。模式对象只在「房间里点开始游戏」之后才建立 —— 所以
  车测（进程内直接 `SceneManager.LoadScene`）永远复现不出来（12:24 又验证了一次：
  interactive + 主动调 UnloadUnusedAssets + settle 60，level7/10 仍 PASS）。

**新增崩溃探针（VEH，src/editor.c）**：崩的瞬间把走查到的那个数组点名 ——

```
!!! walk-obj(ebx) ... klass=... '类型名'
!!! walk-array(edi-0x10) ... len=N klass=... 'Xxx[]' elem='Yyy'
!!!   raw 前 8 个 dword
!!!   [i] ... klass=... '类型名'      ← 前 8 个槽位逐个点名
!!! walk-owner(ebp+0xc) / arg0 / arg1 / arg2
```

**下一步**：从控制台启动 → 进新寂静村或沙漠要塞 → 崩了把 `ucf_mod\ucf_mod.log` 里
`!!! walk-` 段发回来，数组类名 + 槽位内容就能直接指出谁往引用数组里写了非对象数据。

### 12:15 · 对照表补齐 NavMeshGraph（可走面）明细 · 三版一致性口径修正

你问的「可走面是什么」= **NavMeshGraph**（美术烘焙的三角网），不是路点图。本轮把
`docs\地图对照表.md` 从 155 行重写成 242 行，两张图**分开列全**：

- 新增 §0 名词表：PointGraph（tag 20022 的点网）vs NavMeshGraph（可走面三角网），各自存成什么、谁在用；
- §1 收录总表：11 关卡 × ① 备份 / ② 开发 / ③ 部署，路点（点/边）+ 可走面（`nmXXX` · 三角形）各一列；
- §2 PointGraph 明细 11 行：图名、searchTag、maxDistance、mask、场景 WayPoint（总/激活）、导出点/边、
  特征数、导出时间、指纹；
- §3 NavMeshGraph 明细 8 行：网格名、网格顶点、A* 顶点、三角形、索引数、缩放/偏移/旋转、
  bin 文件名与字节数，外加 `UCFNM3` 二进制格式说明；
- 合计与解释：8 个网格 / 7,496 三角形 / 22,488 索引 / 5,253 A* 顶点 / bin 共 396,720 字节。
数字是 12:05 重跑 `python tools\scan_native_nav.py --json` 得到的，和 11:15 那批一致。

**口径修正**：原来写「三版逐字节完全一致」不严谨。地图 JSON 确实逐字节相同，但 navmesh bin 的
**文件名/指纹**相同、字节可能不同——每进一次图 A* 重写 bin 时三角形索引顺序会轮转：

- 11:35 手动进竞技场 → `navmesh_nm683` 与备份差 230 字节（索引区 0xCCC1–0xDCD1）；
- 12:09 车测进死亡擂台 → `navmesh_nm60` 又轮转一次。
两次都用 ① 备份的副本覆盖回来（`restored navmesh_nm60…` / `nm683…`），三版现在又是同一份字节。
文档里已改成「文件名/指纹一致，字节可能轮转，以 ① 备份为准」。

顺带修了 `docs\三版数据与路径_2026-11-17.md` 里过期的「可走面 ×7」→ ×8（补 `nm944`）。

### 11:15 · 沙漠要塞 + 新寂静村 收进开发版，重新冻结原生备份（三版已齐）

车测（§6.10）顺带把这两张图的**原生**数据采齐了，本轮把它们正式并进三版：

**步骤与结果**

1. `nav/names.json` 登记两个新指纹（`organize_maps` 靠它认图；n12 只有 12 点，
   低于地形匹配的 20 点门槛，不登记会被丢进「认不出关卡」）：
   `n12-17a93cfb246913e1 → level7 沙漠要塞`、`n180-03b43b7ee737fcdc → level10 新寂静村`。
2. `vis/` 里两份新导出被整理成 `dev\maps\08_沙漠要塞.json`（12 点 / 7 边 / 46 特征）与
   `dev\maps\11_新寂静村.json`（180 点 / 98 边 / 105 特征）；可走面 `navmesh_nm944` 补进 `dev\vis`
   （`nm919` 早就有了，与本次新 dump **SHA256 完全一致**，说明之前那张 919 是真数据）。
   其他 8 张图按「同图取节点最少那份」重新落盘，指纹不变。
3. `navdata.py publish` → ③ 部署版（写入 12 个文件）。
4. `navdata.py freeze --force` → ① 原生备份重建：**18 个文件**（maps 9 / nav 1 / vis 8），
   只读，`verify` 通过，清单 SHA256 `be7ef5e263714d4e…`。
5. 三版逐字节比对：9 个地图 JSON、8 份可走面 **全部一致**。
   （插曲：核验 level11 有没有原生 PointGraph 时又进了一次死亡擂台，插件照例把
   `navmesh_nm60` 重写了一份——4923 字节里只有最后 9 字节不同，是同一个三角形三个顶点的
   索引顺序，几何完全一样。已用开发版的副本覆盖回来，保证三版同一份字节。）

**为什么 level4 / level11 还是没有地图文件**

不是没采，是**原生就没有 PointGraph**：

- 静态：`python tools/scan_native_nav.py` → 这两张「原生 A* 图」只写 `NavMeshGraph`，路点列是 `—`；
- 运行时：车测进图后日志 `[nav] diag: graphs=1`，只有 `NavMeshGraph`（胜利广场 716 顶点、死亡擂台 60 顶点），
  `waiting for PointGraph` 一直到离开 —— 连图对象都不存在，永远导不出 0 点以外的内容。

它们的可走面已在三版里（`navmesh_nm716` / `navmesh_nm60`），所以「原生可通行空间」这块是齐的。

**三版收录矩阵**（`tools\navdata.py status` / 自检脚本结果）

| 关卡 | 中文名 | 备份 | 开发 | 部署 | 可走面 |
| --- | --- | --- | --- | --- | --- |
| level1 | 运输船 | 786 点 / 1391 边 | 同 | 同 | 原生没有 |
| level2 | 小型工厂 | 12 / 6 | 同 | 同 | nm840 |
| level3 | 椰岛之巅 | 2 / 0 | 同 | 同 | nm532 |
| level4 | 胜利广场 | —（无 PointGraph） | — | — | nm716 |
| level5 | 竞技场 | 17 / 24 | 同 | 同 | nm683 |
| level6 | 刀锋寨 | 18 / 9 | 同 | 同 | nm559 |
| level11 | 死亡擂台 | —（无 PointGraph） | — | — | nm60 |
| level7 | 沙漠要塞 | 12 / 7 | 同 | 同 | nm919 |
| level8 | 生化酒店 | 3063 / 5584 | 同 | 同 | 原生没有 |
| level9 | 暴风 | 空档 stub（原生 0 点） | 同 | 同 | 原生没有 |
| level10 | 新寂静村 | 180 / 98 | 同 | 同 | nm944 |

- 备份 9 maps / 8 bins = 开发 9 / 8 = 部署 9 / 8，`navdata.py diff` 只剩 `INDEX.md`/`_index.json` 这类自动生成文件的差异。
- 编辑器（`/api/maps`，profile=dev）现在返回 11 行：8 行「有数据」+ 暴风空档 + level4/level11 标「待采集」（这个词对这两张图是误导，见上）。


### 11:00 · 第三次修复：真因是「导出的时机」，不是 GC —— 沙漠要塞 + 新寂静村 车测通过

**这次是真正定位到根因，而且是我自己跑测试跑出来的，不是推断。**

先解决「我测不了」这个前提问题：
新增 @@src/autotest.c@@（开关 @@UCF_AUTOTEST=7,10@@），在游戏进程里直接调
@@SceneManager.LoadScene(buildIndex, LoadSceneMode.Single)@@ 换图，每张图等 N 个 tick，
全部通过就写 @@autotest.txt@@ + 日志 @@RESULT PASS@@ 然后退出；崩了就没有 PASS。
跑法：@@powershell tools\autotest.ps1 -Targets 7,10 -Settle 170@@（进程用 WMI 拉起，
不受会话作业回收影响）。附带产物：@@tools/rva_dis.py@@（RVA→反汇编，不依赖 IDA）、
@@tools/screenshot_game.ps1@@（抓游戏窗口）。

**崩溃现场（第一次拿到我们自己的帧）**

- 编译加 @@-fno-omit-frame-pointer@@、VEH 只把「可执行节里的地址」当返回地址、
  并打印寄存器 —— 之前三次闪退日志里一个 ucf_mod 帧都没有，就是因为 @@-O2@@ 把 EBP 优化掉了。
- 这次栈是完整的：
  @@NavProc → editor_tick+0x9de → vis_export+0xa9 → read_nano+0xb3 → comp_pos+0x46
    → GameAssembly.dll+0x32cf63（Component.get_transform） → UnityPlayer.dll+0x755e86@@
- 寄存器 @@ebx=esi=edi=0x43ef6323@@、@@eax=ef673022@@ —— 都是 **float 的位模式**（0x43ef6323 ≈ 478.77）。
  也就是说 @@SpareAreaList[0]@@ 读出来的「组件」是一个浮点数，我们把它当 Component 传给了 Unity。

**真因**

@@auto_export_tick@@ 只等「路点数量稳定 ~2 s」就导出，进图约 2 s 就触发 @@vis_export@@；
而游戏自己的静态组件表（@@SpareAreaList@@ / @@SpareList_BL/GR@@ / @@MapManager@@）此时还是
上一张图正在销毁的东西。09:55 那次的 @@VIS_SCENE_WAIT=90@@ 只保护了 @@vis_rebuild@@，
**没保护导出路径** —— 10:22/10:35 的 GameAssembly 崩溃也是这条路径的下游（读坏对象 → GC 侧炸）。

**改法**

1. @@auto_export_tick@@ 与 @@vis_export@@ 都要求 @@g_sceneAge >= VIS_SCENE_WAIT(90)@@（约 22 s）；
2. @@collect_read()@@ 在场景稳定前只读「路点 + 可走面」（这两个来自 A* 图，换图后是新对象），
   组件表整段跳过；
3. 新增 @@obj_is(o, cls)@@，列表元素先校验 klass 再当组件用（@@read_nano@@ / @@read_crouch@@），
   @@read_spawns@@ 读数组前 @@mem_ok@@；
4. GC 根重做：10:33 那版用 @@object[2048]@@，但 @@System.Object@@ 找不到
   （mscorlib 在程序集数组未初始化尾巴之后），日志刷 @@roots: no System.Object class@@，
   **一个都没钉住**；现在改成**一个对象一个 @@il2cpp_gchandle_new@@**，换场景 @@roots_clear()@@ 归还句柄；
5. VEH 过滤 @@0x406D1388@@（改线程名）/@@0xE06D7363@@（C++ 异常）噪声，栈扫描 128→512 格。

**车测结果**（同一套测试，修复前后对比）

| | 修复前 10:57 版 | 修复后 11:00 版 |
| --- | --- | --- |
| level7 沙漠要塞 | 过 | 过 |
| level10 新寂静村 | **崩在 auto-export** | 过，@n180-03b43b7ee737fcdc@ 导出成功（180 点 / 98 边 / 105 特征） |
| 再进一轮 7→10 | — | 过（@@RESULT PASS targets=2@@，11:02:07） |
| 复测 7,10,7,10 | — | 过 |

- DLL **265,870 B** / SHA256 @@327D22899E6E0A56…@@ / 11:08:09 部署
  （11:00:28 那版 265,870 B 同样 PASS，只差一个 autotest 文案 bug；
  再往前的 @@…110028@@ / @@…105737@@（265,297 B）是车测抓崩的两版，可回滚对照）。
- **最终验收**：11:08:21 起 @@tools\autotest.ps1 -Targets 7,10 -Settle 170@@ → 11:10:01 @@RESULT PASS@@，
  两张图各跑满 170 tick（约 42 s），自动导出都在进图后约 24 s 正常完成。

### 10:33 · 第二次闪退：定位到 il2cpp 的 GC 写屏障 + 加崩溃现场记录

- 10:22:29 / 10:23:04 又崩了两次（新寂静村），但和 09:33 那次不同：
  事件日志显示 `GameAssembly.dll+0x1290b1`（不是 UnityPlayer），崩溃线程栈上**一个 ucf_mod 帧都没有**。
- 反汇编 `0x1290a0` 处的函数（从 dump 的异常地址反推）确认：这是 il2cpp 的
  **GC 写屏障**（读 `*(obj)` → `klass+0xBA` 标志位 → 写 remembered set → `orl $1,(obj)`）。
  也就是说：游戏托管代码在给「一个已经被回收的对象」写字段时崩了
  —— 典型的「托管包装对象只被 C 静态变量引用，GC 看不见、于是回收掉」。
- 改法：
  1. 新增 `roots_setup()/root_put()`：建一个 `object[2048]` 用 gchandle 钉住，
     把 HUD/标签/可视化网格对象/材质都塞进去（材质原本已有 gchandle，其余没有）；
  2. 新增 **VEH 崩溃记录**（`AddVectoredExceptionHandler`）：崩溃瞬间把
     异常码/地址、读或写的地址、栈上所有落在 GameAssembly/UnityPlayer/ucf_mod 的返回地址、
     EBP 链、以及**最近 24 条日志**写进 `ucf_mod.log`（前缀 `!!!`）；
  3. 交互模式每 60 tick 一行心跳 `hb: interactive tick=.. age=.. nodes=..`。
- DLL **256,217 B**，10:33:25 部署。

### 09:55 · 修「进沙漠要塞必闪退」+ 收进 3 张新采集地图

**崩溃证据（不是猜的）**

- 日志里两个会话都在同一位置截断：@@vis: navmesh wire tris=1259 verts=919 meshes=2@@ → 进程消失；
- 事件日志：@@UnityCrossFire.exe@@ / @@UnityPlayer.dll+0x755e86@@ / @@0xc0000005@@，两次同一偏移；
- Unity 崩溃报告：@@%TEMP%@@ 下 @@Alexander_GaGa/穿越火线/Crashes/Crash_2026-11-17_013402735/crash.dmp@@
  （另一份 @@_013339588@@）。解析 dump 后，崩溃线程栈上有 **30 个 ucf_mod 返回地址**，还原出来是：
  @@NavProc -> editor_tick+0x65f -> vis_rebuild+0x17e -> read_crouch/read_nano -> comp_pos+0x27 -> call *%ecx@@
  —— @@comp_pos+0x27@@ 正好是 @@call *%ecx@@（il2cpp 取 Transform 位置）的下一条指令，
  所以是「拿一个不是 Transform 的指针向 Unity 要坐标」，崩在 UnityPlayer 里。

**改法（三层）**

1. @@VIS_SCENE_WAIT=90@@：刚进图的 90 帧不读游戏自己的组件表（@@SpareAreaList@@ /
   @@SpareList_BL/GR@@ / @@MapManager@@ 出生点）——换图瞬间它们还挂着上一张图正在销毁的组件；
   可走面线框不受影响（@@nm_tick@@ 里照画）。
2. @@comp_pos@@ 加三道闸：@@mem_ok(comp)@@ → Transform 必须 @@uobj_live@@ → **类对象必须等于已知
   Transform 的 klass**（@@hud_init@@ 时从 HUD 文本的 Transform 学到），不是就 @@g_badTr++@@ 跳过。
3. 新开关 @@vis_lists@@（@@ucf_mod.json@@，默认 true）：关掉后**完全不碰**游戏组件表，
   只画 A* 路点图和可走面 —— 万一还有图崩，先翻这个开关，再回传日志。

DLL：**253,077 B**，SHA256 @@1489CBC917BBA2B5...@@，09:47:38 部署（旧 DLL 已备份）。

**同时收进这次采集（都是游戏自己 Scan / 烘焙的原生数据）**

- @@05_竞技场@@ 17 点 / 24 边（+ navmesh 683）
- @@06_刀锋寨@@ 18 点 / 9 边（+ navmesh 559）
- @@09_生化酒店@@ 3063 点 / 5584 边
- navmesh 新增 @@nm716@@（胜利广场）/ @@nm60@@（死亡擂台）/ @@nm919@@（沙漠要塞）→ 现在 7/8 张图有可走面
- 备份版重新冻结：**15 个文件**（6 张图 + 暴风空档 + 7 个可走面），@@verify@@ 通过、只读

**顺手修的三个坑**

- @@navserver@@ 的后台「自动归档」线程默认关了（它会在后台跑 @@organize_maps@@，把 0 点的暴风空档
  当「可疑」搬进 @@_suspect/@@）；要归档请手动跑 @@python tools/organize_maps.py --archive@@。
- 编辑器「打开」列表按指纹去重：同一张图的 @@vis/@@ 原始导出不再和 @@maps/@@ 里的重复出现。
- @@organize_maps@@ 不再搬 @@origin=native-empty@@ 的空档文件。

### 09:25 · 修 .bat 双击没反应（LF→CRLF）+ 回执 / 日志

- 根因：上一轮生成 / 打补丁时用 Python 文本模式读，CRLF 被归一成 LF，写回是 **LF 换行**；
  cmd.exe 对 LF 批处理的续行、`goto :label`、括号块都会解析错 → 双击一闪而过 / 直接不执行。
  `启动导航编辑器.bat` 也被这轮补 `UCF_PROFILE=dev` 时改成了 LF，等于我把能用的文件弄坏了。
- 修法：4 个 bat 全部重新生成，**GBK + CRLF**，并且：
  - 开头 `chcp 936`，`title` 带用途；先打印 `navdata.py status` 让人看到当前三版；
  - 结束一律 `[成功] …` / `[失败] 退出码 N（原因见上）+ 日志路径`，然后 `pause` 停住窗口；
  - `-y` 跳过 y/N 确认、`-q` 不暂停（给自动化/测试用）；
  - `navdata.py` 输出改为跟随控制台编码（cp936 下中文正常），并把每次输出抄一份到
    `navdata\_logs\navdata.log`。
- 实测（我自己跑过）：
  `三版状态.bat -q` → 退出码 0，status + verify 都打印「OK 备份版校验：通过（12 个文件）」；
  `部署到游戏.bat -y -q` → 退出码 0，publish 写入 7 个文件；
  `还原原生.bat -y -q` → 退出码 0，restore 写入 5 个、删掉 2 个；
  `启动导航编辑器.bat --no-browser -q` → 起在 127.0.0.1:8765，`/api/maps` 正常（snapshots=4 / geo=11）。
  截图：`screenshots\bat_status_console.png`。
- 顺带说明 maps 不全：`vis\` 里只有 NavMeshGraph 的 `.bin`（没有路点/边），
  所以两者不是互补；`maps\` 缺的 7 张是**从没进过图**（插件只在进图时导出）。

### 08:50 · 导航数据只留原生 + 三版分离（备份 / 开发 / 部署）+ 地形下拉显示中文名

- 背景：编辑器「打开」列表混着 `g_`、`练习场（空白）`、两个 `暴风`、26 条练习场编辑指令
  —— 都不是 UCF 原版的东西；地形下拉只写 `level2 0.62 MB`，对不上地图；
  也没有「原生只读 / 开发 / 部署」分层，编辑会直接影响游戏。
- 只留原生（判据 `map.source == game`）：
  - 留 运输船 786/1391、小型工厂 12/6 + navmesh 840、椰岛之巅 2/0 + navmesh 532、7 份 `vis\navmesh_nm*.bin`；
  - 删 `maps\00_练习场.json`、`maps\10_暴风.json`（694 点，插件自动铺）、`nav\g_.json`、
    `nav\暴风.json`、`nav\练习场（空白）.json`、`nav\n0-0000000000000000.txt`、
    `nav\n786-57a46e3465c847cb.txt.disabled_*`；
  - 暴风（level9）原生 0 路点、无 NavMeshGraph → 写成空档说明文件 `10_暴风.json`。
- 新增 `tools/navdata.py`（status / verify / restore / publish / diff / freeze）；
  三版路径写进 `docs/三版数据与路径_2026-11-17.md`：
  - ① `06-测试\ucf_mod\navdata\native`（只读 + SHA256，永不编辑）
  - ② `06-测试\ucf_mod\navdata\dev`（编辑器默认）
  - ③ `D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\ucf_mod`（游戏读）
- `tools/ucf_paths.py`：`UCF_PROFILE`（dev/native/deploy）、`NATIVE/DEV/DATA/DATAVIS/READONLY`；
  `VIS` 固定为部署版 `vis\`（插件导出仍是唯一输入，自动归档不受影响）。
- `tools/navserver.py`：`/api/maps` 带 `profile`；只读档写入返回 403；
  新增 `POST /api/publish`、`/api/restore-native`；`/api/geo` 带中文名、按关卡号排序、
  同图多份网格按名字去重（`level9` 与 `nano30_storm` 只留前者）。
- `tools/navview.html`：地形下拉 `level2 · 小型工厂 0.62 MB`；顶栏「版本」徽标 +
  「部署到游戏」「还原原生」两个按钮；新手引导改在运输船练手；说明面板加「数据三版」表格。
- 启动器：新增 `部署到游戏.bat` / `还原原生.bat` / `三版状态.bat`（GBK），
  编辑器 bat 显式 `set UCF_PROFILE=dev`。
- 截图：`screenshots/web_native_only.png`（只剩 4 条原生图 + 开发版徽标）、
  `screenshots/web_level_names.png`（下拉 11 张图全带中文名）。
- 回滚：`navdata\_before_cleanup_20261117.zip`（旧 maps/ nav/ vis/ 全部 21 个文件）。

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
