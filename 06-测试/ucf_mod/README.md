# ucf_mod · UCF 1.7 导航/人机插件

UnityCrossFire 1.7.1（Unity + IL2CPP）的文件化插件。
形态：游戏目录的 `winhttp.dll` 代理加载器 → 加载 `ucf_mod\ucf_mod.dll`（原生 C，mingw 编译，运行时挂 il2cpp）。

> **只想玩游戏 / 只想改路点？** 不用看本文件，看游戏目录里的 `ucf_mod\README.txt`（三句话讲完）。
> 本文件是开发说明，给改代码的人看。

---

## 一、三个目录、三个数据区，别搞混

| | 位置 | 内容 | 版本控制 |
|---|---|---|---|
| **工程端** | 本目录（`06-测试\ucf_mod`）| `src/ core/ console/ tools/ tests/ docs/ geo/ navdata/` | ✅ 进 git |
| **部署端（运行时）** | 游戏目录 `...\UnityCrossFire1.7.1\ucf_mod\` | `ucf_mod.dll` `ucf_mod.json` `log/` `markers/` | ❌ 不进 git |

```
① 备份版（只读）   工程端 navdata\native      只有 navdata.py freeze 会写
② 开发版（唯一源） 工程端 navdata\dev         编辑器 / 插件导出 / 控制台「整理导出」「发布到成品」
③ 游戏目录         游戏目录 ucf_mod\          只放 dll + 配置 + log\ + markers（2026-11-21 起不放数据）
```

② 里 `final\` 是**成品**（多版本），`vis\` 是导出收件箱，`packs\` 是**编辑中**（可写沙盒），`archive\` 是归档。

### 三档启动（控制台底部按钮）

| 档 | 插件读哪 | 能写吗 |
|---|---|---|
| 成品 | `UCF_PACK_DIR=②\final` + `UCF_PACK=<版本名>` | 不能（文件带只读属性） |
| 编辑中 | `UCF_PACK=②\packs\<图>\<包>` | 可写，游戏内存回包里 |
| 原版 | 插件待机 | — |

成品是**多版本**的（一版 = 一整套数据）；「发布到成品」默认新建一版，版本名沿用测试包名（重名 `-2`/`-3`）。
成品档**按包启动**，读 `final\<版本>\` 用的是和编辑中完全相同的加载逻辑，所以 grow / keep / 增量三种包发布过去后行为一致。

数据流：**游戏导出 → ② vis →（整理导出）→ ② maps；测试包做完 →（发布到成品）→ ② final\<包名> → 成品档**。

**日志（2026-11-23 起）**：主位置是**工程端** `log\` —— 控制台启动游戏时用环境变量 `UCF_LOG_DIR` 指过去，
所以**游戏目录里不生成日志**。`ucf_mod.log`（超过 16 MB 自动轮转成 `ucf_mod.prev.log`，只保 1 代）、`autotest.txt`（车测结果）、
`player_marks.txt`（玩家坐标记录）都在这里；历史日志在 `log\_历史\`。
没走控制台启动（手动开 / 别人机器上）时，插件依次落 `<游戏>\ucf_mod\log\` → `<游戏>\ucf_mod\`，
控制台和工作台三级都能读到。`ucf_navcmd.txt` 是控制台 ↔ 插件的命令通道，仍留在游戏目录根。

部署端路径由 `%LOCALAPPDATA%\UCFMod\deploy.json`（控制台「部署」页选游戏时写）或 `tools/deploy.json`（开发机）指定，
所有工具都通过 `core/ucf_paths.py` 解析：`DEPLOY` = 游戏目录，`PROJ` = 工程端，`DEV` = ② 开发版。

---

## 二、目录

```text
ucf_mod/
├── .ucfroot                 项目根标记：ucf_paths 靠它向上找 PROJ（别删）
├── README.md                本文件（入口）
├── src/                     C 源码：cfg.c(配置) plugin.c(加载/注入) navfix.c(A*导航) editor.c(可视化/编辑/菜单/录制)
│   └── proxy/               winhttp 加载器源码 + 编译脚本
├── console/                 ★ 控制台（桌面 GUI）和它拉起的一切
│   ├── 控制台.pyw            开关面板 + 14 个页签（CustomTkinter，双击 启动控制台.bat）
│   ├── 启动控制台.bat
│   ├── navserver.py          本地只读服务（也托管网页），由控制台「路点工作台」启动
│   ├── deploy_tab.py «部署»页   deploy_mod.py 部署引擎   first_run.py 首次设置向导
│   ├── ucf_rec.py            录制轨迹：解析 / 重采样 / 跳跃·落下·岔路识别（纯计算）
│   ├── ucf_trace.py          原始轨迹采集：目录 / 增量读取 / 摘要
│   └── web/                  ★ 网页端（只读），静态根就是它
│       ├── nav-studio.html/.css/nav-studio-app.js    七页工作台
│       ├── navview.html                              2D 俯视 + 3D + 可走面查看器（?embed=1 供停靠栏）
│       └── README.md                                 工作台说明（方向约定、七页数据源、只读限制）
├── core/                    ★ 共享底座（谁都能 import）
│   ├── ucf_paths.py          工程端/部署端/三区路径解析（唯一真相）+ P.tool() 脚本解析
│   ├── map_table.py          读 docs/guide/地图对照表.md（序号_场景名中文名）
│   └── navdata.py            三区台账：status / verify / restore / diff / freeze / pack / final …（库 + CLI）
├── tools/                   ★ 命令行工具（人手动跑）
│   ├── build.ps1             编译（产物进 build/，带日期与 git 短哈希）
│   ├── deploy.json(.example) 开发机部署路径（本机路径，已 gitignore）
│   ├── geo/                  extract_geo.py(资源→npz)  geo2web.py(npz→geo/web)  fetch_tex.py(贴图)
│   ├── data/                 tidy_vis.py  organize_maps.py  check_jumps.py  make_practice.py  scan_native_nav.py
│   └── _oneoff/              migrate_four_versions.py  migrate_map_folders.py（已执行完的历史迁移）
├── tests/                   ★ 静态自检 / 离线自检（7 个，见下）
├── docs/                    guide/（指南）+ record/（每轮实现记录）+ img/
├── geo/                     *.npz 地形源；geo/web、geo/tex 由脚本生成（gitignore）
├── navdata/                 三区数据（native / dev）
├── payload/                 部署弹药库：加载器 dll、uninstall.ps1、README.txt、level9 回滚点（唯一副本）
├── build/                   编译产物（gitignore；bench_watch.c 已挪到 archive/）
└── archive/                 不参与运行的历史证据：probe_map_loader/ design/ bench_watch.c README-原文
```

**路径规则**：所有脚本靠 `.ucfroot` 向上找项目根，不靠"自己是第几层目录"。
新增脚本请照抄现有文件头那 4 行（见任一 `tools/data/*.py`），搬家时才不用改一堆相对路径。

---

## 三、构建与部署

```powershell
# 编译（产物进 build/，带日期与 git 短哈希）
.\tools\build.ps1

# 部署到游戏目录：用控制台「部署」页（推荐，会自动选位置 + 六道闸门）
# 命令行老路：.\tools\build.ps1 -Deploy   ← 读 tools\deploy.json
```

> `tools\deploy.json` 目前指向 `D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\`（另一份游戏副本），
> 而控制台的用户配置指向 `...\test-1\UnityCrossFire1.7.1\` —— **这是有意为之**，`-Deploy` 会装到前者。

部署端 `uninstall.ps1` 只移除部署物（dll / 加载器 / 还原场景），**不会删源码**。

---

## 四、控制台（`console/控制台.pyw`）

页签：**地图 · 可视化 · 导出 · 快捷键 · 人机路点 · 录制 · 数据 · 部署 · 车测 · 开发者选项**。

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
  旧数据用 `python tools/data/check_jumps.py` 体检（同点 / 缺路点 / 无连线 / 太短）。
- **方向可视化**：A 起点 = 绿色方块 + 竖条；准星虚线框按身份上色（起点绿 / 终点红 / 非法灰）；
  单向边的箭头层只在菜单打开时显示。
- **预置虚影**：选好类型后，准星处先显示虚线框，按下去之前就能看清会不会被拒绝（灰框 = 会失败）。

配置键：`wp_menu`、`wp_autoground`（bool）、`wp_brush`（normal/jump/crouch/guard/area/tag，只在游戏内切）。

---

## 五、路点工作台（`console/web/`，只读）

启动：控制台点「路点工作台（查看）」，或 `python console/navserver.py --no-browser`（默认 `/web/nav-studio.html`，只监听 127.0.0.1）。

- 七页：总览 / 路点库 / 路线 / 区域 / 自动铺设 / 地图数据 / 日志。
- 顶栏数据档下拉：**① 备份版 / ② 成品 / ② 编辑中**（选编辑中时旁边选当前图的包）。切换只改"看哪一份"，不写文件。
- 3D 侧栏（右侧停靠 iframe `/navview.html`）：俯视 + 3D + 可走面 + 贴图，W/A/S/D 飞、Q/E 升降、右键转视角、F 全图、Esc 收起。
- **只读硬限制**：保存 / 部署 / 还原 / 加点全部没有；`navview.html` 的 `VIEWONLY` 固定 true；服务端所有 POST 返回 405。

### 方向约定（三处必须一致）

```text
北 = 世界 -Z（平面图 / 3D 俯视的正上方）    东 = 世界 +X
南 = 世界 +Z（下）                          西 = 世界 -X
```

约定写在 `console/web/nav-studio-app.js` 的 `DIR4/dirScreen`、`console/web/navview.html` 的同名函数、
`src/editor.c` 的 `compass_bucket` 三处，改要一起改。游戏内还有一份汉字罗盘（控制台「可视化」→「方向罗盘」，或 Ctrl+Shift+7）。

### 3D 地形与贴图

- 地形来自 `geo/*.npz`，`tools/geo/geo2web.py` 转成 `geo/web/<关卡>.bin`（UCFG v2：位置 + 法线 + UV + 每块贴图号）。
- 贴图由 AssetRipper 导出的 Unity 工程转（`docs/guide/地图3D资源导出/代码/scene_export2web.py`），level1~level11 全接入；
  3D 工具条「贴图」开关（默认开），关掉就是灰模。
- 重建：`python tools/geo/geo2web.py --force`（只重跑某张图就加关卡名）。`geo/web` 缺失时 navserver 会按需自动重建。
- **场景里每件道具都有两个 MeshRenderer**：`X (1)`（独立网格 + `CrossFire/Shadow` 材质，MeshCollider 用的也是这份）和
  `X`（合并网格子网格，位置对不上）。geo2web 只挑一套，运输船留 Shadow 那套——代价是只在合并网格里的小块（玻璃/灯/气罐，约 3%）会缺。
- 巨幅装饰面 `card` 默认**保留**（运输船的船体/桅杆/围栏都被标成 card，丢了好船就剩一块平板）；要老行为用 `--drop-cards`。

---

## 六、录制（控制台「录制」页）

三态：① 录前准备 → ② 录制中 → ③ 复盘。启动档固定 **编辑中**（成品档只读，不能录）。

- 采样：`src/editor.c` 的 `rec_tick()`，20 Hz 节流，记相机位置/朝向、正下方射线地面高度、空格/Ctrl。
  插件**不推断路点**，怎么走、哪里跳由玩家决定。
- 识别（`console/ucf_rec.py`，纯计算）：4 m 重采样（2.5 / 4 / 6 可选）；跳链 = 空格 + 离地 > 0.3 m 且水平 ≥ 1.5 m；
  落下 = 下降 ≥ 1.5 m 且落差 ≥ 2 m；2.5 m 内二次经过 = 岔路候选；蹲 > 0.8 s 只提示；单帧 > 15 m 断段。
- 落盘：原始轨迹 `navdata/dev/vis/rec/<图>_<包>_<时间>.jsonl`；复盘确认后只往包里**追加** `node add`/`edge add`/`jump add`，
  改前备份 `.bak-rec-<时间>`。
- 命令：控制台写 `ucf_navcmd.txt` 的 `cmd=rec` + `act=start|stop|pause|resume`；插件 0.5 s 内执行。
- 已知边界：车测时相机在天上、脚下射线打不到地面（`gy=-9999`），跳跃/落下识别要用真实对局验证。

---

## 七、自检

```powershell
python tests/test_console_switches.py   # cfg.c 开关表 ↔ 控制台页签分组
python tests/test_blank_pack.py        # grow/keep 建包链路（editor.c / navdata / navserver / navview / 控制台）
python tests/test_mapfolders.py        # ①② 目录布局、四个读法数字一致、迁移日志
python tests/test_console_packcmd.py   # 包统计 + ucf_navcmd.txt
python tests/test_trace.py             # 轨迹字段表 C/Python 对钉
python tests/test_ucf_rec.py           # 录制识别（合成轨迹）
python tests/test_workbench_views.py   # 工作台三档 + grow/jump/单向边
```

---

## 八、文档

| 文件 | 内容 |
| --- | --- |
| [docs/guide/地图对照表.md](docs/guide/地图对照表.md) | ★ **唯一权威表**：11 张图的 序号/关卡/中文名/场景名（手写，脚本都读它）+ 原生 A* 数据 |
| [docs/guide/地图数据标准_取用与核对.md](docs/guide/地图数据标准_取用与核对.md) | 数据长什么样、谁写谁读、怎么核对 |
| [docs/guide/部署总览.md](docs/guide/部署总览.md) | 部署端的组成与三档启动怎么落 |
| [docs/guide/人机与路线设计.md](docs/guide/人机与路线设计.md) | **新手先看**：人机行为优先级、路线元素、各模式需要什么 |
| [docs/guide/寻路全流程_从建图到蹲下.md](docs/guide/寻路全流程_从建图到蹲下.md) | 想懂原理：三层结构、类关系、五个阶段 |
| [docs/guide/点图与可走面_为什么每张图不一样.md](docs/guide/点图与可走面_为什么每张图不一样.md) | 一张图靠点、一张图靠面，为什么 |
| [docs/guide/新增地图_完整工作流.md](docs/guide/新增地图_完整工作流.md) | 加新地图：Blender → Unity → 字节补丁 → 修出生点 |
| [docs/guide/游戏基础信息.md](docs/guide/游戏基础信息.md) | 模式枚举 + 阵营缩写 + 出生点容器 |
| [docs/record/逆向速查_版本偏移与地址.md](docs/record/逆向速查_版本偏移与地址.md) | 引擎版本 + md5、字段偏移、函数 RVA |
| [docs/record/](docs/record/) | 每轮实现笔记（文件名带日期）；只作历史证据，现状看本文件 |
| [console/web/README.md](console/web/README.md) | 工作台七页的数据来源、方向约定、3D 操作 |
| [archive/README-原文_2026-11-23.md](archive/README-原文_2026-11-23.md) | 本次整理前的 README 原文（逐字保留） |

---

## 九、已知问题

1. `navdata/dev/vis/` 里还有两份没归位的可走面（`navmesh_nm532-…`、`navmesh_nm716-…`），
   所以 `tests/test_mapfolders.py` 的第 2 项红 3 条。整理收件箱即可：`python core/navdata.py import`（可先 `--dry`）。
2. `tools/deploy.json` 指向另一份游戏副本（见「构建与部署」），命令行 `-Deploy` 与控制台部署页目标不同——有意保留。
3. `src/editor.c` 里还留着 5 个 `UCF_UI_*` 环境变量（2026-11-20 排查进图闪退用的调试开关），代码自述"定位完就删"；
   删之前要真机验证一次。
