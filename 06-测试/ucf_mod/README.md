# ucf_mod · UCF 1.7 导航/人机插件

UnityCrossFire 1.7.1（Unity + IL2CPP）的文件化插件。
形态：游戏目录的 `winhttp.dll` 代理加载器 → 加载 `ucf_mod\ucf_mod.dll`（原生 C，mingw 编译，运行时挂 il2cpp）。

> **只想玩游戏 / 只想改路点？** 不用看本文件，看游戏目录里的 `ucf_mod\README.txt`（三句话讲完）。
> 本文件是开发说明，给改代码的人看。
> **2026-11-24 目录重构**：代码进 `app/`，数据进 `data/`，产物进 `run/`，日志留在 `log/`；
> 控制台按页签拆开（一个页签一个文件）。迁移明细见 `docs/record/目录重构_2026-11-24.md`。
> **2026-11-24 身份**：控制台分「用户 / 开发者」两种身份，首次启动自己选；用户只有 2 页，开发者 10 页。
> 见 `docs/record/身份与页签_2026-11-24.md`。

---

## 一、三个目录、三个数据区，别搞混

| | 位置 | 内容 | 版本控制 |
|---|---|---|---|
| **工程端** | 本目录（`06-测试\ucf_mod`）| `app/ src/ docs/ data/ run/ log/ archive/` | ✅ 进 git（run/build、log、部分派生数据除外） |
| **部署端（运行时）** | 游戏目录 `...\UnityCrossFire1.7.1\ucf_mod\` | `ucf_mod.dll` `ucf_mod.json` `log/` `markers/` | ❌ 不进 git |

```
① 备份版（只读）   工程端 data\navdata\native    只有 navdata.py freeze 会写
② 开发版（唯一源） 工程端 data\navdata\dev       编辑器 / 插件导出 / 控制台「整理导出」「发布到成品」
③ 游戏目录         游戏目录 ucf_mod\             只放 dll + 配置 + log\ + markers（2026-11-21 起不放数据）
```

② 里 `final\` 是**成品**（多版本），`vis\` 是导出收件箱，`packs\` 是**编辑中**（可写沙盒），`archive\` 是归档。

### 三档启动（控制台底部按钮）

| 档 | 插件读哪 | 能写吗 |
|---|---|---|
| 成品 | `UCF_PACK_DIR=②` + `UCF_PACK=<版本名>` | 不能（文件带只读属性） |
| 编辑中 | `UCF_PACK=②` | 可写，游戏内存回包里 |
| 原版 | 插件待机 | — |

成品是**多版本**的（一版 = 一整套数据）；「发布到成品」默认新建一版，版本名沿用测试包名（重名 `-2`/`-3`）。
成品档**按包启动**，读 `final\<版本>\` 用的是和编辑中完全相同的加载逻辑，所以 grow / keep / 增量三种包发布过去后行为一致。

数据流：**游戏导出 → ② vis →（整理导出）→ ② 图文件夹；测试包做完 →（发布到成品）→ ② final\<包名> → 成品档**。

**日志（2026-11-23 起）**：主位置是**工程端** `log\` —— 控制台启动游戏时用环境变量 `UCF_LOG_DIR` 指过去，
所以**游戏目录里不生成日志**。`ucf_mod.log`（超过 16 MB 自动轮转成 `ucf_mod.prev.log`，只保 1 代）、`autotest.txt`（车测结果）、
`player_marks.txt`（玩家坐标记录）都在这里。历史日志在 `log\_历史\`。
没走控制台启动（手动开 / 别人机器上）时，插件依次落 `<游戏>\ucf_mod\log\` → `<游戏>\ucf_mod\`，
控制台和工作台三级都能读到。`ucf_navcmd.txt` 是控制台 ↔ 插件的命令通道，仍留在游戏目录根。

部署端路径由 `%LOCALAPPDATA%\UCFMod\deploy.json`（控制台「部署」页选游戏时写）或 `app/tools/deploy.json`（开发机）指定，
所有工具都通过 `app/core/ucf_paths.py` 解析：`DEPLOY` = 游戏目录，`PROJ` = 工程端，`DEV` = ② 开发版。

---

## 二、目录（2026-11-24 重构后，根目录 7 个文件夹）

```text
ucf_mod/
├── .ucfroot                 项目根标记：所有脚本靠它向上找 PROJ（别删）
├── .gitignore
├── README.md                本文件（入口）
├── 启动控制台.bat            唯一的用户入口（一行转发到 app\启动控制台.bat）
├── app/                     ★ 全部 Python + 网页（进 git）
│   ├── 控制台.pyw             窗口壳：启动条 / 状态 / 启动游戏 / 页签装配（~760 行）
│   ├── 启动控制台.bat
│   ├── ui/                    页签共用件（不归属任何一页）
│   │   ├── env.py             路径与环境：sys.path、三区路径常量、第三方 import（所有模块的底座）
│   │   ├── consts.py          开关表 GROUPS / DEV_ITEMS、颜色、热键速查、车测文案
│   │   ├── util.py            文件 / 时间 / 大小 / 哈希 / 配置 / 游戏进程 / 日志读取
│   │   ├── maps.py            地图对照表与图文件夹（序号_场景名中文名、map.json / navmesh.bin）
│   │   ├── stats.py           导出收件箱 / 可走面 / 目录哈希与差异
│   │   ├── packs.py           测试包 + 成品版本台账（含 PackMixin）+ 命令文件
│   │   └── kit.py             共用控件：开关卡片 / 区块标题 / 文本卡 / 图例 / 文件对话框
│   ├── tabs/                  ★ 一个页签一个文件
│   │   ├── map.py             地图
│   │   ├── vis.py             可视化
│   │   ├── export.py          导出
│   │   ├── hotkey.py          快捷键
│   │   ├── waypoint.py        人机路点（两档页 / 版本对比 / 建包 / 清空 / 发布）
│   │   ├── record/            录制
│   │   │   ├── tab.py         三态页（录前准备 / 录制中 / 复盘）
│   │   │   └── ucf_rec.py     识别算法：4 m 重采样、跳 / 落 / 岔路（纯计算）
│   │   ├── data.py            数据（三区路径与时间、部署 / 还原 / 校验）
│   │   ├── deploy/            部署
│   │   │   ├── deploy_tab.py  页签 UI + 六道闸门
│   │   │   ├── deploy_mod.py  部署引擎（搬 dll / 加载器 / 卸载）
│   │   │   └── first_run.py   首次设置向导
│   │   ├── autotest.py        车测（插件自己在进程内切图）
│   │   └── dev/               开发者选项
│   │       ├── tab.py         玩家坐标记录 + 轨迹采集卡片
│   │       └── ucf_trace.py   原始轨迹：目录 / 增量读取 / 摘要
│   ├── core/                  ★ 路径与数据台账
│   │   ├── ucf_paths.py       工程端 / 部署端 / 三区路径解析（唯一真相）+ P.tool()
│   │   ├── map_table.py       读 docs/guide/地图对照表.md（序号_场景名中文名）
│   │   └── navdata.py         三区台账：status / verify / restore / diff / freeze / pack …
│   ├── workbench/             网页端（只读）
│   │   ├── navserver.py       本地只读服务（也托管网页）
│   │   └── web/               nav-studio.html/.css/.js（七页工作台）+ navview.html（2D/3D 查看器）
│   ├── tools/                 命令行工具
│   │   ├── build.ps1          编译（产物进 run/build/，带日期与 git 短哈希）
│   │   ├── autotest.ps1       车测命令行
│   │   ├── deploy.json(.example)  开发机部署路径（本机路径，已 gitignore）
│   │   ├── geo/               extract_geo.py  geo2web.py  fetch_tex.py
│   │   ├── data/              tidy_vis.py  organize_maps.py  check_jumps.py  make_practice.py  scan_native_nav.py
│   │   └── _oneoff/           历史迁移脚本（已执行完，留档）
│   └── tests/                 ★ 静态自检（8 个）
├── src/                     C 源码：cfg.c(配置) plugin.c(加载/注入) navfix.c(A*导航) editor.c(可视化/编辑/菜单/录制) autotest.c
│   └── proxy/               winhttp 加载器源码 + 编译脚本
├── data/                    ★ 数据
│   ├── geo/                 *.npz 地形源；web/、tex/ 由脚本生成（gitignore）
│   └── navdata/             三区数据：native/（冻结只读）+ dev/（开发版）
├── run/                     ★ 产物与弹药
│   ├── payload/             部署弹药库：加载器 dll、uninstall.ps1、README.txt、level9 回滚点（唯一副本）
│   └── build/               编译产物（gitignore）
├── log/                     运行日志（gitignore；控制台注入 UCF_LOG_DIR）
├── docs/                    guide/（指南）+ record/（每轮实现记录）
└── archive/                 不参与运行的历史证据：design/ bench_watch.c README-原文
```

**改代码去哪**：页签在 `app/tabs/`（一页一个文件），共用件在 `app/ui/`，路径与环境在 `app/ui/env.py`。

**路径规则**：所有脚本靠 `.ucfroot` 向上找项目根，不靠“自己是第几层目录”。
新增脚本请照抄现有文件头那 4 行（见任一 `app/tools/data/*.py`、`app/tabs/*.py`），搬家时才不用改一堆相对路径。

### 身份 → 页签 → 文件（改哪一页就开哪个文件）

2026-11-24 起控制台按**身份**建页：身份存在 `ucf_mod.json` 的 `ui.role`（`UCF_ROLE` 环境变量优先），
首次启动弹窗选，右上角「切换身份」随时改（会重启一下）。表在 `app/ui/consts.py`：

- **用户**（`USER_PAGES`）：地图、部署 —— 平铺两页，隐藏「路点工作台」「去人机路点改」等开发入口。
- **开发者**（`TAB_GROUPS`）：10 页分 4 组（用户那两页也在里面，不用切身份）：

| 组 | 页签 | 代码 | 说明 |
|---|---|---|---|
| **插件开关** | 地图 | `app/tabs/map.py` | 房间选图列表里的隐藏图（暴风） |
| | 可视化 | `app/tabs/vis.py` | 进图读什么、画什么（逐类勾选 + 图例） |
| | 导出 | `app/tabs/export.py` | Ctrl+E 导出开关与内容、最近导出、整理收件箱 |
| | 快捷键 | `app/tabs/hotkey.py` | 游戏内热键速查 |
| **路点数据** | 人机路点 | `app/tabs/waypoint.py` + `ui/packs.py` | 编辑中 / 成品两档、节点计数、清空、版本对比、建包、发布 |
| | 录制 | `app/tabs/record/tab.py` + `ucf_rec.py` | 录前准备 / 录制中 / 复盘 |
| | 数据 | `app/tabs/data.py` | 三区路径与时间、部署 / 还原 / 校验 |
| **部署与测试** | 部署 | `app/tabs/deploy/*` | 选游戏位置、六道闸门、一键部署 / 校验 / 卸载 |
| | 车测 | `app/tabs/autotest.py` | 插件自己在进程内逐张 LoadScene |
| **开发调试** | 开发者选项 | `app/tabs/dev/*` | 玩家坐标记录、原始轨迹采集 |

窗口壳 `app/控制台.pyw` 只留：窗口骨架、分组装配、启动条件条、开始游戏、状态刷新、关窗。
分组只多一层按钮：一级 `CTkTabview`（4 组），二级是组内按钮条（2 页以上才显示，单页组直接出内容）。
**每个组记住上次停留的子页**（`ucf_mod.json` 的 `ui.sub_<组名>`）；旧版本存的平铺页签名会按 `TAB_OLD_MAP` 自动搬进新组，升级后不会跳回第一页。

---

## 三、构建与部署

```powershell
# 编译（产物进 run/build/，带日期与 git 短哈希）
.\app\tools\build.ps1

# 部署到游戏目录：用控制台「部署」页（推荐，会自动选位置 + 六道闸门）
# 命令行老路：.\app\tools\build.ps1 -Deploy   ← 读 app\tools\deploy.json
```

> `app\tools\deploy.json` 目前指向 `D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\`（另一份游戏副本），
> 而控制台的用户配置指向 `...\test-1\UnityCrossFire1.7.1\` —— **这是有意为之**，`-Deploy` 会装到前者。

部署端 `uninstall.ps1` 只移除部署物（dll / 加载器 / 还原场景），**不会删源码**。

---

## 四、控制台（`app\控制台.pyw`，双击根目录 `启动控制台.bat`）

**身份决定看到几页**（2026-11-24）——右上角身份牌，旁边「切换身份」（会重启一下）：

| 身份 | 页签 | 说明 |
|---|---|---|
| **用户** | 地图 · 部署 | 装好就能玩：隐藏开发入口，开始游戏独占一行 |
| **开发者** | 4 组 × 10 页 | 用户那两页也有，不用切身份 |

开发者身份的 4 组（一级点组、二级点页）：

| 组 | 组内页签 | 这一组在管什么 |
|---|---|---|
| **插件开关** | 地图 · 可视化 · 导出 · 快捷键 | 进游戏后插件画什么、导什么、有哪些键；改完重启生效 |
| **路点数据** | 人机路点 · 录制 · 数据 | 做路点的完整链路：选包编辑 → 录制补充 → 发布 / 还原 / 校验 |
| **部署与测试** | 部署 · 车测 | 把插件装进游戏，再让它自己逐图跑一遍验收 |
| **开发调试** | 开发者选项 | 坐标记录、原始轨迹——给离线分析用的取证入口 |

- **身份存哪**：`ucf_mod.json` 的 `ui.role`（`user` / `dev`）；`UCF_ROLE=user|dev` 环境变量优先，脚本和快捷方式用。
- **切换为什么重启**：用户身份根本不建那 8 页，动态换页签会把控件状态全丢；重启约 1 秒，并且回到该身份上次那一页。

- **数据 / 部署**：三区路径与时间、部署/还原/校验；选游戏位置 + 一键部署（取代了原来的独立部署脚本）。
- **车测**：插件自己在进程内逐张 LoadScene，不用鼠标键盘。
- **开发者选项**：玩家坐标记录、原始轨迹采集（原来的「可视化」「录制」里的两块搬来）。
- **人机路点**：启动档两页（编辑中 / 成品，页内再分标签）、六项开关、节点/边计数、清空本图；撤销/重做/保存/重读在游戏内 F2 菜单。
  成品页「版本」下拉选一版整套启动（只读）；「版本对比」表左编辑中、右成品，最后一列给结论（sha256 相同 = 同一文件）。

### 游戏内 F2 菜单要点

- 按 **F2** 打开；**长按 E 0.45 s** 备用。按 F2 前先点一下游戏画面拿焦点。
- 键位：`1-9` 直选；小键盘 `8/2` 上下、`5` 确认；`Esc` 或主键盘 `0` 返回（滚轮也可上下）；左键确认、右键返回。
  W/A/S/D、空格、Shift、Ctrl 仍交给游戏。
- **连续编辑**：类型页 / 方向页常驻，选好类型后按 5 可以一直放同一种点；连完 `A->B` 后 A 自动前进到 B；删除页也停留。
- **加点前提**：运行期不能增长 PointGraph 节点数组，只能复用「不可走」槽位。原生点全可走的图（沙漠要塞、运输船）要先建**空白底图测试包**；
  飓风危城原生 0 点，建不了空白包。
- **跳跃点**必须「一对路点 + 一条 A->B 的边」，否则 A* 永远不会把两端连着排。菜单会自动补落点路点与单向边；
  旧数据用 `python app/tools/data/check_jumps.py` 体检（同点 / 缺路点 / 无连线 / 太短）。
- **方向可视化**：A 起点 = 绿色方块 + 竖条；准星虚线框按身份上色（起点绿 / 终点红 / 非法灰）；
  单向边的箭头层只在菜单打开时显示。
- **预置虚影**：选好类型后，准星处先显示虚线框，按下去之前就能看清会不会被拒绝（灰框 = 会失败）。

配置键：`wp_menu`、`wp_autoground`（bool）、`wp_brush`（normal/jump/crouch/guard/area/tag，只在游戏内切）。

---

## 五、路点工作台（`app/workbench/`，只读）

启动：控制台点「路点工作台（查看）」，或 `python app/workbench/navserver.py --no-browser`（默认 `/web/nav-studio.html`，只监听 127.0.0.1）。

- 七页：总览 / 路点库 / 路线 / 区域 / 自动铺设 / 地图数据 / 日志。
- 顶栏数据档下拉：**① 备份版 / ② 成品 / ② 编辑中**（选编辑中时旁边选当前图的包）。切换只改“看哪一份”，不写文件。
- 3D 侧栏（右侧停靠 iframe `/navview.html`）：俯视 + 3D + 可走面 + 贴图，W/A/S/D 飞、Q/E 升降、右键转视角、F 全图、Esc 收起。
- **只读硬限制**：保存 / 部署 / 还原 / 加点全部没有；`navview.html` 的 `VIEWONLY` 固定 true；服务端所有 POST 返回 405。

### 方向约定（三处必须一致）

```text
北 = 世界 -Z（平面图 / 3D 俯视的正上方）    东 = 世界 +X
南 = 世界 +Z（下）                          西 = 世界 -X
```

约定写在 `app/workbench/web/nav-studio-app.js` 的 `DIR4/dirScreen`、`app/workbench/web/navview.html` 的同名函数、
`src/editor.c` 的 `compass_bucket` 三处，改要一起改。游戏内还有一份汉字罗盘（控制台「可视化」→「方向罗盘」，或 Ctrl+Shift+7）。

### 3D 地形与贴图

- 地形来自 `data/geo/*.npz`，`app/tools/geo/geo2web.py` 转成 `data/geo/web/<关卡>.bin`（UCFG v2：位置 + 法线 + UV + 每块贴图号）。
- 贴图由 AssetRipper 导出的 Unity 工程转（`docs/guide/地图3D资源导出/代码/scene_export2web.py`），level1~level11 全接入；
  3D 工具条「贴图」开关（默认开），关掉就是灰模。
- 重建：`python app/tools/geo/geo2web.py --force`（只重跑某张图就加关卡名）。`data/geo/web` 缺失时 navserver 会按需自动重建。
- **场景里每件道具都有两个 MeshRenderer**：`X (1)`（独立网格 + `CrossFire/Shadow` 材质，MeshCollider 用的也是这份）和
  `X`（合并网格子网格，位置对不上）。geo2web 只挑一套，运输船留 Shadow 那套——代价是只在合并网格里的小块（玻璃/灯/气罐，约 3%）会缺。
- 巨幅装饰面 `card` 默认**保留**（运输船的船体/桅杆/围栏都被标成 card，丢了好船就剩一块平板）；要老行为用 `--drop-cards`。

---

## 六、录制（控制台「录制」页）

三态：① 录前准备 → ② 录制中 → ③ 复盘。启动档固定 **编辑中**（成品档只读，不能录）。

- 采样：`src/editor.c` 的 `rec_tick()`，20 Hz 节流，记相机位置/朝向、正下方射线地面高度、空格/Ctrl。
  插件**不推断路点**，怎么走、哪里跳由玩家决定。
- 识别（`app/tabs/record/ucf_rec.py`，纯计算）：4 m 重采样（2.5 / 4 / 6 可选）；跳链 = 空格 + 离地 > 0.3 m 且水平 ≥ 1.5 m；
  落下 = 下降 ≥ 1.5 m 且落差 ≥ 2 m；2.5 m 内二次经过 = 岔路候选；蹲 > 0.8 s 只提示；单帧 > 15 m 断段。
- 落盘：原始轨迹 `data/navdata/dev/vis/rec/<图>_<包>_<时间>.jsonl`；复盘确认后只往包里**追加** `node add`/`edge add`/`jump add`，
  改前备份 `.bak-rec-<时间>`。
- 命令：控制台写 `ucf_navcmd.txt` 的 `cmd=rec` + `act=start|stop|pause|resume`；插件 0.5 s 内执行。
- 已知边界：车测时相机在天上、脚下射线打不到地面（`gy=-9999`），跳跃/落下识别要用真实对局验证。

---

## 七、自检

```powershell
python app/tests/test_console_switches.py   # cfg.c 开关表 ↔ 控制台页签分组
python app/tests/test_blank_pack.py         # grow/keep 建包链路（editor.c / navdata / navserver / navview / 控制台）
python app/tests/test_mapfolders.py         # ①② 目录布局、四个读法数字一致、迁移日志
python app/tests/test_console_packcmd.py    # 包统计 + ucf_navcmd.txt
python app/tests/test_trace.py              # 轨迹字段表 C/Python 对钉
python app/tests/test_ucf_rec.py            # 录制识别（合成轨迹）
python app/tests/test_workbench_views.py    # 工作台三档 + grow/jump/单向边
python app/tests/test_logpaths.py           # 日志三级查找 + 注入 + 轮转
python app/tests/test_layout.py             # 目录树与 README 一致（重构后新增）
python app/tests/test_roles.py              # 身份（用户/开发）↔ 页表、旧配置迁移
```

---

## 八、文档

| 文件 | 内容 |
| --- | --- |
| `docs/guide/地图对照表.md` | ★ **唯一权威表**：11 张图的 序号/关卡/中文名/场景名（手写，脚本都读它）+ 原生 A* 数据 |
| `docs/guide/地图数据标准_取用与核对.md` | 数据长什么样、谁写谁读、怎么核对 |
| `docs/guide/部署总览.md` | 部署端的组成与三档启动怎么落 |
| `docs/guide/人机与路线设计.md` | **新手先看**：人机行为优先级、路线元素、各模式需要什么 |
| `docs/guide/寻路全流程_从建图到蹲下.md` | 想懂原理：三层结构、类关系、五个阶段 |
| `docs/guide/点图与可走面_为什么每张图不一样.md` | 一张图靠点、一张图靠面，为什么 |
| `docs/guide/新增地图_完整工作流.md` | 加新地图：Blender → Unity → 字节补丁 → 修出生点 |
| `docs/guide/游戏基础信息.md` | 模式枚举 + 阵营缩写 + 出生点容器 |
| `docs/record/目录重构_2026-11-24.md` | 2026-11-24 目录重构：旧路径 → 新路径对照 |
| `docs/record/身份与页签_2026-11-24.md` | 2026-11-24 身份（用户/开发）：页表、切换、迁移、自检 |
| `docs/record/逆向速查_版本偏移与地址.md` | 引擎版本 + md5、字段偏移、函数 RVA |
| `docs/record/` | 每轮实现笔记（文件名带日期）；只作历史证据，现状看本文件 |
| `app/workbench/web/README.md` | 工作台七页的数据来源、方向约定、3D 操作 |
| `archive/README-原文_2026-11-23.md` | 上次整理前的 README 原文（逐字保留） |

---

## 九、已知问题

1. `data/navdata/dev/vis/` 里还有两份没归位的可走面（`navmesh_nm532-…`、`navmesh_nm716-…`），
   所以 `app/tests/test_mapfolders.py` 的第 2 项红 3 条。整理收件箱即可：`python app/core/navdata.py import`（可先 `--dry`）。
2. `app/tools/deploy.json` 指向另一份游戏副本（见「构建与部署」），命令行 `-Deploy` 与控制台部署页目标不同——有意保留。
3. `src/editor.c` 里还留着 5 个 `UCF_UI_*` 环境变量（2026-11-20 排查进图闪退用的调试开关），代码自述“定位完就删”；
   删之前要真机验证一次。
4. 2026-11-24 目录重构删掉了几份历史快照（`archive/probe_map_loader/`、`data/navdata/dev/archive/` 下的四个迁移快照），
   它们是 git 跟踪过的文件，需要时用 `git log -- archive/probe_map_loader` 找回。
   `run/payload/_rescue/level9.orig` **没删**：它是唯一一份没被打过补丁的场景。
