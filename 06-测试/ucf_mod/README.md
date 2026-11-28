# ucf_mod · UCF 1.7 导航/人机插件

UnityCrossFire 1.7.1（Unity + IL2CPP）的文件化插件。
形态：游戏目录的 `winhttp.dll` 代理加载器 → 读 `UCF_MOD_DLL`，直接加载**工程端** `run\build\ucf_mod.dll`（原生 C，mingw 编译，运行时挂 il2cpp）。

> **只想玩游戏 / 只想改路点？** 不用看本文件，看 `run\payload\ucf_mod\README.txt`（用户说明；游戏目录不再放它）。
> 本文件是开发说明，给改代码的人看。
> **2026-11-25 直读**：游戏目录不再有 `ucf_mod\`；插件/配置/日志/标记全在工程端，一键部署只铺加载器 + 本体补丁。
> **2026-11-24 目录重构**：代码进 `app/`，数据进 `data/`，产物进 `run/`，日志留在 `log/`；
> 控制台按页签拆开（一个页签一个文件）。迁移明细见 `docs/record/目录重构_2026-11-24.md`。
> **2026-11-24 身份**：控制台分「用户 / 开发者」两种身份，首次启动自己选；用户只有 2 页，开发者 9 页。
> 见 `docs/record/身份与页签_2026-11-24.md`。

---

## 一、三个目录、三个数据区，别搞混

| | 位置 | 内容 | 版本控制 |
|---|---|---|---|
| **工程端** | 本目录（`06-测试\ucf_mod`）| `app/ src/ docs/ data/ run/ log/ archive/` | ✅ 进 git（run/build、log、部分派生数据除外） |
| **部署端（运行时）** | 游戏目录 `...\UnityCrossFire1.7.1\` | 只有 `winhttp.dll` `winhttp_orig.dll` + 本体补丁 | ❌ 不进 git |

```
① 冻结副本（只读） 工程端 data\maps\<图>\native     只有 navdata.py freeze 会写
② 开发数据（唯一源）工程端 data\maps\<图>\          编辑器 / 插件导出 / 控制台「整理导出」「发布到成品」
③ 游戏目录         游戏目录（不再有 ucf_mod\）       只放加载器 + 本体补丁（2026-11-25 起）
运行时状态          工程端 run\runtime\              ucf_mod.json / ucf_navcmd.txt / deploy 清单
```

**一张图一个文件夹**（2026-11-27 起，见 §二）：点图 `map.json`、可走面 `navmesh.bin`、草稿 `<指纹>.txt`、
编辑标记 `markers.txt`、成品 `final\<指纹>.txt`、冻结副本 `native\` 全在同一张图的文件夹里。
`_inbox\` 是导出收件箱，`_archive\` 是回收站（都挂在 `data\maps\` 下，不属于任何一张图）。

### 三档启动（控制台底部按钮）

| 档 | 插件读哪 | 能写吗 |
|---|---|---|
| 成品 | `UCF_PACK_DIR=data\maps` + `UCF_NAV_SEARCH=1` + `UCF_NAV_SUB=final`（按当前图指纹找 `<图>\final\<指纹>.txt`） | 不能（文件带只读属性） |
| 编辑中 | `UCF_PACK_DIR=data\maps` + `UCF_PACK=<地图文件夹>`（读 `<图>\<指纹>.txt`） | 可写，游戏内存回草稿 |
| 原版 | 插件待机 | — |

成品是**一张图一份**（没有版本号）：发布 = 覆盖 `<图>\final\<指纹>.txt`，覆盖前旧成品自动进 `_archive\final_prev\`（每图最近 5 份）。
成品档和编辑中走完全相同的加载逻辑，所以 grow / keep / 增量发布过去后行为一致；草稿就在 `<图>\` 根下，一张图只有一个。
成品档不设 `UCF_PACK`（没有"唯一一张图"），插件按场景指纹去各图文件夹里找 —— 一次启动照样能玩全部图。

数据流：**游戏导出 → _inbox →（整理导出）→ `<图>\map.json`；草稿做完 →（发布这张图）→ `<图>\final\<指纹>.txt` → 成品档**。

**日志（2026-11-23 起，2026-11-27 全部集中）**：唯一位置是**工程端** `log\` —— 控制台启动游戏时用环境变量
`UCF_LOG_DIR` 指过去，所以**游戏目录里不生成日志**。现在一处的文件：

| 文件 | 谁写的 | 说明 |
| --- | --- | --- |
| `ucf_mod.log` / `ucf_mod.prev.log` | C 插件 | 主日志；超过 16 MB 轮转，只保 1 代 |
| `ucf_mod.prev_HHMMSS.log` | 车测脚本 | 开跑前备份上一份，方便对比 |
| `autotest.txt` | C 插件 | 车测结果（每张图 OK + 最后 RESULT） |
| `player_marks.txt` | C 插件 | 玩家坐标记录（追加） |
| `navdata.log` / `navdata.prev.log` | `navdata.py` | 命令行 stdout 抄本；超过 16 MB 轮转 |
| `publish.log` | `navdata.py` | 成品发布流水（TSV：时间 / 指纹 / 标签 / 点数 / sha / 备注） |

历史日志在 `log\_历史\`。没走控制台启动时，插件落 `%LOCALAPPDATA%\UCFMod\log` 或 `%TEMP%\ucf_mod\log`，
不会写游戏目录；加载器载入失败只写 `%TEMP%\ucf_mod_proxy.log`（那时工程端路径还不可信，故意留在 %TEMP%）。
`ucf_navcmd.txt` 是控制台 ↔ 插件的命令通道，现在在 `run\runtime\`；`ucf_mod.json` 也在那里。

部署端路径由 `%LOCALAPPDATA%\UCFMod\deploy.json`（控制台「部署」页选游戏时写）或 `app/tools/deploy.json`（开发机）指定，
所有工具都通过 `app/core/ucf_paths.py` 解析：`DEPLOY` = `<游戏>\ucf_mod`（只用于反推游戏目录，目录可以不建）、
`RUNTIME` = 工程端 `run\runtime`，`PROJ` = 工程端，`DEV` = ② 开发版。

---

## 二、目录（2026-11-24 重构后，根目录 8 个文件夹）

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
│   │   ├── packs.py           草稿 / 成品 + 命令文件（含 PackMixin）
│   │   ├── overview.py        地图总览数据层：11 张图的备份 / 草稿 / 成品 / 游戏加载
│   │   └── kit.py             共用控件：开关卡片 / 区块标题 / 文本卡 / 图例 / 文件对话框
│   ├── tabs/                  ★ 一个页签一个文件
│   │   ├── map.py             地图
│   │   ├── vis.py             可视化
│   │   ├── overview.py        地图总览（矩阵 / 卡片 / 看板三视图）
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
│   │       ├── tab.py         玩家坐标记录 + 轨迹采集卡片（采集对象 / 档位 / 报告）
│   │       └── ucf_trace.py   原始轨迹：目录 / 增量读取 / 摘要（解析在 core/ucf_sample.py）
│   ├── core/                  ★ 路径与数据台账
│   │   ├── ucf_paths.py       工程端 / 部署端 / 三区路径解析（唯一真相）+ P.tool()
│   │   ├── ucf_sample.py      ★ 采样文件读取（ucf-trace/1·2·3）：录制和采集共用一份解析
│   │   ├── map_table.py       读 docs/guide/07-地图对照表.md（序号_场景名中文名）
│   │   └── navdata.py         数据台账：status / verify / restore / diff / freeze / pack …
│   ├── workbench/             网页端（只读）
│   │   ├── navserver.py       本地只读服务（也托管网页）
│   │   └── web/               nav-studio.html/.css/.js（七页工作台）+ navview.html（2D/3D 查看器）
│   ├── tools/                 命令行工具
│   │   ├── build.ps1          编译（产物进 run/build/，带日期与 git 短哈希）
│   │   ├── autotest.ps1       车测命令行
│   │   ├── deploy.json(.example)  开发机部署路径（本机路径，已 gitignore）
│   │   ├── ledger.py          ★ 资产台账：run/gamepatch ⇄ 各游戏副本对账（只读，scan / verify）
│   │   ├── geo/               extract_geo.py  geo2web.py  fetch_tex.py
│   │   ├── data/              tidy_vis.py  organize_maps.py  check_jumps.py  make_practice.py  scan_native_nav.py
│   │   └── _oneoff/           历史迁移脚本（已执行完，留档）
│   └── tests/                 ★ 静态自检（12 个）
├── src/                     C 源码：cfg.c(配置) plugin.c(加载/注入) navfix.c(A*导航) editor.c(可视化/编辑/菜单/录制) autotest.c
│   └── proxy/               winhttp 加载器源码 + 编译脚本
├── data/                    ★ 数据
│   ├── geo/                 *.npz 地形源；web/、tex/ 由脚本生成（gitignore）
│   └── maps/                ★ 一图一夹（2026-11-27）：同上 11 张图，每张一个文件夹
│       ├── 00_公共/          names.json / _index.json / INDEX.md / SHA256SUMS.txt / .frozen.json
│       ├── 01_TransportShip运输船/      map.json  navmesh.bin  <指纹>.txt  markers.txt
│       │                              native\（冻结只读）  final\<指纹>.txt（成品）
│       ├── …（02 / 03 / 05 / 06 / 08 / 09 / 10 / 11）
│       ├── 04_NY_TM胜利广场/  07_DeathRing死亡擂台/  原生没有点图，只有 navmesh.bin
│       ├── _inbox/          可走面导出 / 录制轨迹（派生，可重建）
│       └── _archive/        删草稿 / 清标记 / 发布前快照 / 迁移日志
├── unity-map-project/       ★ 地图工程（生产侧：进 git，不进分发包）
│   ├── README.md            命名规则 / 加图 9 步 / 三处同名
│   ├── 00_模板/             脚手架：ProjectSettings + Packages + UcfBuild.cs + map.json
│   └── 12_TestMap12龙城/    龙城：src/（GLB）+ unity/（工程）+ tools/（构建/补丁脚本）
├── run/                     ★ 产物与弹药
│   ├── runtime/             运行时状态：ucf_mod.json / ucf_navcmd.txt / deploy 清单（gitignore）
│   ├── deploy_backup/       一键部署覆盖前备份（gitignore；卸载还原用）
│   ├── payload/             部署弹药库：加载器 dll、loader_history.json、README.txt、level9 回滚点
│   ├── gamepatch/           ★ 游戏本体补丁包：一张图一个目录 + patch.json + orig/（原版哈希 → 补丁后哈希）
│   ├── ledger/              资产台账运行态：drift.json + 快照（gitignore）
│   └── build/               编译产物（gitignore）
├── log/                     运行日志唯一目录（gitignore；控制台注入 UCF_LOG_DIR）
│                            ucf_mod.log / autotest.txt / player_marks.txt /
│                            navdata.log / publish.log
├── docs/                    guide/（指南）+ record/（每轮实现记录）
└── archive/                 不参与运行的历史证据：design/ bench_watch.c README-原文
```

**改代码去哪**：页签在 `app/tabs/`（一页一个文件），共用件在 `app/ui/`，路径与环境在 `app/ui/env.py`。

**改游戏本体去哪**：**不许直接改游戏目录**。补丁包进 `run/gamepatch/<序号_场景名中文名>/`（`patch.json` 写清原版哈希 → 补丁后哈希），
地图工程与构建脚本进 `unity-map-project/<同名>/`；改完跑 `python app/tools/ledger.py scan` 对账，
它会列出"哪份副本装了、哪份没装、有没有只存在于游戏目录的改动"。

**路径规则**：所有脚本靠 `.ucfroot` 向上找项目根，不靠“自己是第几层目录”。
新增脚本请照抄现有文件头那 4 行（见任一 `app/tools/data/*.py`、`app/tabs/*.py`），搬家时才不用改一堆相对路径。

### 身份 → 页签 → 文件（改哪一页就开哪个文件）

2026-11-24 起控制台按**身份**建页：身份存在 `ucf_mod.json` 的 `ui.role`（`UCF_ROLE` 环境变量优先），
首次启动弹窗选，右上角「切换身份」随时改（会重启一下）。表在 `app/ui/consts.py`：

- **用户**（`USER_PAGES`）：地图、部署 —— 平铺两页，隐藏「路点工作台」「去人机路点改」等开发入口。
- **开发者**（`TAB_GROUPS`）：9 页分 4 组（用户那两页也在里面，不用切身份）：

| 组 | 页签 | 代码 | 说明 |
|---|---|---|---|
| **插件开关** | 地图 | `app/tabs/map.py` | 房间选图列表里的隐藏图（暴风） |
| | 可视化 | `app/tabs/vis.py` | 进图读什么、画什么（逐类勾选 + 图例） |
| **路点数据** | 地图总览 | `app/tabs/overview.py` + `ui/overview.py` | 11 张图一张一行：备份① / 编辑中 / 成品 / 游戏加载；矩阵 / 卡片 / 看板三视图 |
| | 人机路点 | `app/tabs/waypoint.py` + `ui/packs.py` | 编辑中 / 成品两档、本图草稿（含删除）、发布、草稿↔成品对比 |
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
# 编译（产物进 run\build\，带日期与 git 短哈希）
.\app\tools\build.ps1

# 可选：同步到 run\payload\ucf_mod\ucf_mod.dll（不写游戏目录）
.\app\tools\build.ps1 -Payload

# 一键部署：只铺游戏目录必须有的文件（加载器 + 启用的本体补丁）
python app\tabs\deploy\deploy_mod.py --game-exe "D:\...\UnityCrossFire.exe"
# 也可以：控制台「部署」页 → 一键部署

# 连未启用的地图补丁一起铺（例如龙城）
python app\tabs\deploy\deploy_mod.py --game-exe "..." --all-packs

# 校验 / 卸载
python app\tabs\deploy\deploy_mod.py --game-exe "..." --verify
python app\tabs\deploy\deploy_mod.py --game-exe "..." --uninstall
```

**部署语义（2026-11-25 起）**：
- 不再往游戏目录写 `ucf_mod\`（没有 dll / 配置 / README / uninstall / manifest）；
- 游戏目录只放：`winhttp.dll`、`winhttp_orig.dll`、`run\gamepatch` 里登记的本体补丁；
- 覆盖前备份、部署清单都在工程端 `run\deploy_backup` / `run\runtime\deploy`；
- `patch.json` 的 `orig` 哈希对不上就拒绝，绝不盲打；卸载按清单 + 包内 `orig/` 还原。
- 插件本体/配置/日志/标记/地图数据全在工程端；控制台启动时用 `UCF_MOD_DLL` / `UCF_MOD_DIR` 指过去。

---

## 四、控制台（`app\控制台.pyw`，双击根目录 `启动控制台.bat`）

**身份决定看到几页**（2026-11-24）——右上角身份牌，旁边「切换身份」（会重启一下）：

| 身份 | 页签 | 说明 |
|---|---|---|
| **用户** | 地图 · 部署 | 装好就能玩：隐藏开发入口，开始游戏独占一行 |
| **开发者** | 4 组 × 9 页 | 用户那两页也有，不用切身份 |

开发者身份的 4 组（一级点组、二级点页）：

| 组 | 组内页签 | 这一组在管什么 |
|---|---|---|
| **插件开关** | 地图 · 可视化 | 进游戏后插件画什么、有哪些开关；改完重启生效 |
| **路点数据** | 地图总览 · 人机路点 · 录制 · 数据 | 先看 11 张图的状态，再做路点：选图编辑 → 录制补充 → 发布 / 还原 / 校验 |
| **部署与测试** | 部署 · 车测 | 把插件装进游戏，再让它自己逐图跑一遍验收 |
| **开发调试** | 开发者选项 | 坐标记录、原始轨迹——给离线分析用的取证入口 |

- **身份存哪**：`ucf_mod.json` 的 `ui.role`（`user` / `dev`）；`UCF_ROLE=user|dev` 环境变量优先，脚本和快捷方式用。
- **切换为什么重启**：用户身份根本不建那 8 页，动态换页签会把控件状态全丢；重启约 1 秒，并且回到该身份上次那一页。

- **数据 / 部署**：三区路径与时间、部署/还原/校验；选游戏位置 + 一键部署（取代了原来的独立部署脚本）。
- **车测**：插件自己在进程内逐张 LoadScene，不用鼠标键盘。
- **开发者选项**：玩家坐标记录、原始轨迹采集（原来的「可视化」「录制」里的两块搬来）。
  采集对象可选 玩家 / 人机 / 全部（人机 10 Hz）；**选择记在 `ucf_mod.json` 的 `trace.who`，
  下次打开控制台恢复上次那个**，卡片上会写「上次的采集对象：…」。采集中 / 停止后分开报
  「玩家 N 样本 · 人机 M 条」；日志里 header 的 `who` 和人机行的 `"k":"b"` 区分谁是谁。
  这一页**只采不分析**：要报告就命令行跑
  `python app\tools\data\jump_stats.py <日志或目录>`（录制日志同一套格式，也能直接喂）。
  边界见 docs/record/采集与录制_边界_2026-11-27.md、docs/record/采集对象记忆_2026-11-27.md。
- **地图总览**：只读总览，矩阵 / 卡片 / 看板共用同一套筛选和状态；顶部显示全局插件部署、当前启动档、草稿/成品/快照数量。
  「部署 / 游戏加载」按当前启动档算，不是把地图复制进游戏目录；每行展开有草稿/成品/快照路径和跳转。
- **人机路点**：启动档两页（编辑中 / 成品）+ 一个共用地图选择；编辑中只有「本图草稿」（一张图一个），成品只有「已发布」（一张图一份）。
  发布 = 覆盖 `<图>\final\<指纹>.txt`；成品页「草稿 ↔ 成品」表按图给结论（sha256 相同 = 同一文件）。
  编辑中卡片三个动作：打开草稿目录 / 重置本图草稿（只清点边，草稿还在）/ **删除本图草稿**（只把草稿三件
  `manifest.json` / `<指纹>.txt` / `nogen.txt` 挪到 `_archive\pack_trash\`，
  这张图回到「还没有草稿」；**点图 `map.json` / 可走面 / `markers.txt` / `native\` / 成品都原地不动**，
  要撤发布走成品页）。一图一夹以后草稿和图数据在同一个目录里，整份搬会把地图一起搬走（2026-11-27 踩过）。
  **草稿 ≠ 编辑标记**：守卫区 / 守卫点 / 蹲守点 / 标签 / 出生点 存在 `<图>\markers.txt`；
  删草稿的弹窗里「同时清空本图标记」默认勾上（取消勾选就只删草稿），同一行也显示「本图标记：N」
  并可单独「清空本图标记」（都挪到 `_archive\markers_trash\`）。
  **纯面图**（胜利广场 / 死亡擂台）也列进地图下拉、带「· 纯面图」后缀：场景里的 A* 只有 NavMeshGraph、
  没有 PointGraph（`app/tools/data/scan_native_nav.py` 实读场景可证）。点「开始编辑这张图」建空白草稿后，
  插件进图会**现场补一张 0 节点的 PointGraph**（`src/navfix.c` 的 `navfix_add_point_graph`），grow 时再把这张图的
  可走面（NavMeshGraph）摘掉 —— 人机改走你画的点，和飓风危城一样。限制：只能停在「编辑中」
  （飓风危城 / 胜利广场 / 死亡擂台 三张 0 点图指纹都是 `n0-…`，成品档按指纹找文件会撞车），发布按钮是灰的。

### 游戏内 F2 菜单要点

- **手动保存（2026-11-25，唯一保存方式）**：游戏内所有编辑（路点 / 连线 / 跳链 / 蹲守点 / 守卫区 / 标签 / 出生点）
  只改内存和当前场景，**按 Ctrl+S 才写文件**（F2 菜单「撤销 / 保存」→「保存（Ctrl+S）」是同一个入口，
  菜单第一行常驻「● 未保存 / 已保存」）。没按 Ctrl+S 就退房间 = 改动全部丢弃，
  `ucf_mod.log` 会写一行「退出房间，丢弃未保存的编辑」。旧的快捷键保存入口（Ctrl+6 / Ctrl+Shift+S 等）已全部删除。
- 按 **F2** 打开；**长按 E 0.45 s** 备用。按 F2 前先点一下游戏画面拿焦点。
- 键位：`1-9` 直选；小键盘 `8/2` 上下、`5` 确认；`Esc` 或主键盘 `0` 返回（滚轮也可上下）；左键确认、右键返回。
  W/A/S/D、空格、Shift、Ctrl 仍交给游戏。
- **热键（2026-11-26 精简）**：游戏里只剩 F2 菜单、`Ctrl+S` 保存、`Ctrl+V` 可视化总开关、`Delete` 删准星最近标记。
  原来的 `Ctrl+0`~`Ctrl+9`（编辑模式那一套）、`Ctrl+Shift+A/N/J/D/Z/R`、`Ctrl+Shift+6/+7`、
  `Ctrl+E`（手动导出 JSON）、`Ctrl+Shift+X`（只读采集）全部下线 —— 前两组做的事 F2 菜单里都有，
  后两个功能连代码一起删了（导出页、export_* 开关、collect.flag 都不在了）。
- **可视化实时下发**：控制台「插件开关 → 可视化」的勾选会在游戏运行时写一条 `ucf_navcmd.txt`（`cmd=vis`），
  插件 0.5 s 内应用，**不用重进图、不用重开游戏**。
- **连续编辑**：类型页 / 方向页常驻，选好类型后按 5 可以一直放同一种点；连完 `A->B` 后 A 自动前进到 B；删除页也停留。
- **加点前提**：运行期不能增长 PointGraph 节点数组，只能复用「不可走」槽位。原生点全可走的图（沙漠要塞、运输船）要先建**空白底图草稿**；
  飓风危城原生 0 点，建不了空白包。
- **跳跃点**必须「一对路点 + 一条 A->B 的边」，否则 A* 永远不会把两端连着排。菜单会自动补落点路点与单向边；
  旧数据用 `python app/tools/data/check_jumps.py` 体检（同点 / 缺路点 / 无连线 / 太短）。
- **方向可视化**：A 起点 = 绿色方块 + 竖条；准星虚线框按身份上色（起点绿 / 终点红 / 非法灰）；
  单向边的箭头层只在菜单打开时显示。
- **蹲守点的朝向**（2026-11-27；2026-11-28 守卫点不再单独设方向）：球看不出朝向，准星对着蹲守点时，
  地上画**射线 + 箭头**（多方向最多 3 条），准星下方一行「朝向 东北 42°」；读不到方向的画虚线写「未知」。
  放置时朝向 = **相机朝向**；放完在 `F2 → 9 朝向工具` 里改：设为相机朝向 / 顺逆 15° / 清空 / 显示样式。
  **守卫点没有自己的方向**：张望方向来自守卫区入口（`3 守卫区工具 → 3 加入口`）；
  没有入口时插件自动补一个区中心入口，防止 `zoomPos` 为空。原生守卫点只读、不能改。
- **加守卫点子页 / 只建点，不连带建区**（2026-11-27；2026-11-28 子页）：
  `3 守卫区工具 → 2 加守卫点` 先确认准星在**已有守卫区**的 3 m 框里，再进入加点子页；
  子页按 **1~4 选安全等级、5 放一个、Esc 返回**，放完仍留子页可连续放。
  区外虚线框变灰、只提示「这里没有守卫区：先按 1 建区」，不建对象、不进撤销栈。
  以前会顺手在同一坐标再建一个区（一次点击两个物体），看着像「加点却多出来一个区」。
  详见 `docs/record/守卫点只建点_2026-11-27.md`。
- **守卫区入口 / 逃跑点**（2026-11-28）：`3 守卫区工具 → 3 加入口 / 4 加逃跑点` 已接线，
  `5 删除入口 / 6 删除逃跑点` 删准星 **0.6 m 内**的那一个（对不准就拒绝，不猜；只删插件自己加的）。
  入口**不是进区的门**，只是守卫点站定后的张望方向（游戏并进 zoomPos），人机仍靠 A\* 进区；
  逃跑点是被压时的随机撤退落点。两者都进 `markers.txt`，可删除 / 撤销；
  逃跑区 / 邻居区引用仍由原生场景配，插件新建区是空的。
  可视化页对应三个勾选：**入口点（黄球）/ 逃跑点（白球）/ 入口连线（粉色）**，对应 `vis_entry` / `vis_escape` / `vis_eline`，游戏运行时实时生效。
- **加守卫点子页 / 安全等级**（2026-11-28）：`3 守卫区工具 → 2 加守卫点` 进入子页：
  **1~4 直接切 0~3，5 放一个，Esc 返回**；放完仍留子页可连续放，等级保持到改选/退出。
  第 5 项会动态显示“放一个守卫点（安全等级 N）”；只影响之后新建的点，默认值存 `markers.txt` 的 `# nano_safety`。
  越大越靠里；被压时游戏只换 **严格更高** 的点，全 3 等于区内不换位。
  F2 菜单开着、朝向显示开着时，准星指向守卫点，屏幕中间显示「守卫点 · 安全等级 N」。
- **整体移动守卫区**（2026-11-28）：`3 守卫区工具 → 7 整体移动守卫区`，**两步确认**：
  准星照着区的 3 m 框按 5 选中（菜单显示守卫点 / 入口 / 逃跑点数量），走到新位置再按 5 确认；
  `0 / Esc` 取消。区本体（BoxCollider）、区下所有守卫点、入口、逃跑点、`entrancePos` /
  `escapePos` 数组一起平移，相对布局 / `safety` / `aid` 都不变；一步撤销，`Ctrl+S` 才落盘。
  只动插件自己建的区；原生区保持只读（和原生守卫点不能改方向同一条边界）。
- **预置虚影**：选好类型后，准星处先显示虚线框，按下去之前就能看清会不会被拒绝（灰框 = 会失败）。
- **出生点编辑**（2026-11-25；2026-11-27 加中立）：`1 添加点位 → 4/5/6 = 出生点 BL/GR/中立`，
  准星落点 + 当前朝向；`5 删除点位 → 5/6/7` 删三种出生点（至少保留 1 个）；原来的「删除标记」拆成
  `5 删除点位` 和 `6 删除区域`（守卫区）。改的是 `MapManager.SP_BL/SP_GR/SP_Netural` 运行时数组，
  不写原图；新增/删除先记在内存，Ctrl+S 才写 `markers\<图>\markers.txt`（`spawn` / `spawndel`，队号 0/1/2），
  保存后每次进图自动重套。
  **第一次出生**：写数组抢不过"地图加载那一帧"，事后挪玩家又会闪退，最终改成
  **整函数替换 `MapManager.GetSpawnPoint`**（入口 5 字节 `E9`，2026-11-27）：
  初始化时预读 markers 的 `spawn / spawndel`，钩子里按队返回"新增优先 + 原生去删除"的点，
  第一波和复活都走它；不碰 Player/Transform。`ucf_mod.json: "spawn_hook": false` 可一键关）。
  **高度**：新增点不是「地面 + 5 cm」，而是从本图原生出生点反推「地面 + 原生高度」
  （`spawn_height_gap`），历史存的低点在进图后自动回填 —— 以前重生会穿地板/掉进虚空。
  为什么要有中立：`GameManager.AddPlayer` 按 `GameMode` 定队 —— 团队/特殊战用 `ClientData.joinTeam`（BL/GR），
  **个人竞技（DeathMatch）全员 Neutral**，生化（Nano3/4/6、终结者）全员 GlobalRisk。所以只改 BL/GR 时，
  个人竞技里"加了出生点没人出生"（游戏只读 `SP_Netural`）。详见 `docs/record/出生点三阵营_2026-11-27.md`。

配置键：`wp_menu`、`wp_autoground`（bool）、`wp_brush`（normal/jump/crouch/guard/area/tag/spawn_bl/spawn_gr，只在游戏内切）。

---

## 五、路点工作台（`app/workbench/`，只读）

启动：控制台点「路点工作台（查看）」，或 `python app/workbench/navserver.py --no-browser`（默认 `/web/nav-studio.html`，只监听 127.0.0.1）。

- 七页：总览 / 路点库 / 路线 / 区域 / 自动铺设 / 地图数据 / 日志。
- 顶栏数据档下拉：**① 备份版 / ② 成品 / ② 编辑中**。编辑中一张图只有一个草稿，不再有“选包”下拉；切换只改“看哪一份”，不写文件。
- 3D 侧栏（右侧停靠 iframe `/navview.html`）：俯视 + 3D + 可走面 + 贴图，W/A/S/D 飞、Q/E 升降、右键转视角、F 全图、Esc 收起。
- **只读硬限制**：保存 / 部署 / 还原 / 加点全部没有；`navview.html` 的 `VIEWONLY` 固定 true；服务端所有 POST 返回 405。

### 方向约定（三处必须一致）

```text
北 = 世界 -Z（平面图 / 3D 俯视的正上方）    东 = 世界 +X
南 = 世界 +Z（下）                          西 = 世界 -X
```

约定写在 `app/workbench/web/nav-studio-app.js` 的 `DIR4/dirScreen`、`app/workbench/web/navview.html` 的同名函数、
`src/editor.c` 的 `compass_bucket` 三处，改要一起改。游戏内还有一份汉字罗盘（控制台「可视化」→「方向罗盘」勾选，运行中实时生效）。

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

- 采样（`src/editor.c` 的采样会话，和「原始轨迹采集」共用 `ss_tick()`）：玩家 30 Hz，
  记**脚底坐标** / 是否在地面 / 竖直速度 / 空格·Ctrl；落地那一帧插件直接写一行 `ev=jump`。
  「采集对象」可选 玩家 / 人机 / 全部（人机 10 Hz，用来看人机实际怎么走）。插件**不推断路点**，怎么走、哪里跳由玩家决定。
  录制页也把两边分开报：采集中 / 复盘显示「玩家 N 样本 · 人机 M 台 / K 条」；
  人机样本只写日志、**不进路点**（只选人机时没有玩家样本，不生成草稿，界面会说明）。
- 识别（`app/tabs/record/ucf_rec.py`，纯计算）：按形状放点（DP ε=10 cm，最大段长 1.5 / 2.5 / 4 / 6 m 可选）；
  跳链只保留下限 **3D ≥ 1.5 m**（2026-11-27 取消上限：能不能跳进游戏看，不再按长度拦）；
  主动起跳（v0 ≥ 9 且滞空 ≥ 0.3 s）落点低也按「跨缺口」，不记「跳下」；
  但净下落 ≥ 3 m 的按「跳下」处理（只写单向边，不建跳链 —— 免得人机去跳 13 m）；
  落下写单向边（落差 < 2 m 也建，只在 issues 里提一句）；2.5 m 内二次经过 = 岔路候选；
  静止 2 s 只提示；单帧 > 15 m 的那条边不建。
  `jump add` 第 10~12 列是蹲：`ct0 ct1 ctb`（空中开始 / 结束蹲的秒数，-1 = 没蹲；老文件没有这三列）。
- 落盘：原始轨迹 `data/maps/_inbox/rec/<图>_<包>_<时间>.jsonl`（同一套 `ucf-trace/3`，header 带图 / 包 / who；
  人机行带 `"k":"b"`，玩家行不带 k）；
  复盘确认后只往草稿里**追加** `node add`/`edge add`/`jump add`，改前备份 `.bak-rec-<时间>`。
- **必须点「保存增量」才算保存**（2026-11-25）：录制过程只写原始 jsonl，不进草稿；
  结束录制只到复盘页，不点保存就什么也不写；点保存后才追加 + 通知插件重新载入。
- 命令：控制台写 `ucf_navcmd.txt` 的 `cmd=rec` + `act=start|stop|pause|resume`（带 `out=` / `hz=` / `who=`）；插件 0.5 s 内执行。
- **一个写入者**（2026-11-27）：录制和采集同时只跑一个，开另一个会先把这一个收尾（录制照样能复盘保存）。
- 录制日志就是可分析的原始轨迹：`python app\tools\data\jump_stats.py <那份 jsonl>` 能直接出报告，不用重录。
- 已知边界：玩家对象抓不到时退回相机估算（header 写 `src=camera`，绝对高度有常数偏差）。

---

## 七、自检

```powershell
python app/tests/test_console_switches.py   # cfg.c 开关表 ↔ 控制台页签分组
python app/tests/test_blank_pack.py         # grow/keep 建包链路（editor.c / navdata / navserver / navview / 控制台）
python app/tests/test_mapfolders.py         # 一图一夹：native 冻结副本 / 草稿 / 成品 / 四个读法数字一致
python app/tests/test_navsearch_c.py       # 成品档按指纹找图的 C 实现（从 editor.c 抽函数编译跑）
python app/tests/test_console_packcmd.py    # 包统计 + ucf_navcmd.txt
python app/tests/test_trace.py              # 轨迹字段表 C/Python 对钉
python app/tests/test_ucf_rec.py            # 录制识别（合成轨迹）
python app/tests/test_sampling_shared.py    # 录制 / 采集共用一套格式 + 解析（2026-11-27）
python app/tests/test_workbench_views.py    # 工作台三档 + grow/jump/单向边
python app/tests/test_manual_save.py        # 手动保存：唯一入口 / 无自动保存 / 退房间丢弃
python app/tests/test_logpaths.py           # 日志三级查找 + 注入 + 轮转
python app/tests/test_layout.py             # 目录树与 README 一致（重构后新增）
python app/tests/test_guide_docs.py         # guide 文档改名后：代码常量 / 对照表 / 编号 / 链接四处对上（2026-11-28）
python app/tests/test_roles.py              # 身份（用户/开发）↔ 页表、旧配置迁移
python app/tests/test_console_timers.py     # 控制台定时链只有一条：折叠停 / 展开续 / 关窗摘
python app/tests/test_guard_entry_escape.py # 守卫区入口 / 逃跑点：菜单接线 / 数组 / 落盘 / 撤销
python app/tests/test_guard_zone_ops.py    # 删除入口 / 删除逃跑点 / 整体移动守卫区（菜单 / 数组 / 撤销）
```

---

## 八、文档

| 文件 | 内容 |
| --- | --- |
| `docs/guide/07-地图对照表.md` | ★ **唯一权威表**：11 张图的 序号/关卡/中文名/场景名（手写，脚本都读它）+ 原生 A* 数据 |
| `docs/guide/03-地图数据标准_取用与核对.md` | 数据长什么样、谁写谁读、怎么核对 |
| `docs/guide/06-部署总览.md` | 直读模式 + 一键部署（加载器 / 本体补丁 / 备份 / 卸载） |
| `docs/guide/09-人机与路线设计.md` | **新手先看**：人机行为优先级、路线元素、各模式需要什么 |
| `docs/guide/08-寻路全流程_从建图到蹲下.md` | 想懂原理：三层结构、类关系、五个阶段 |
| `docs/guide/04-点图与可走面_为什么每张图不一样.md` | 一张图靠点、一张图靠面，为什么 |
| `docs/guide/02-新增地图_完整工作流.md` | 加新地图：Blender → Unity → 字节补丁 → 修出生点 |
| `docs/guide/01-游戏基础信息.md` | 模式枚举 + 阵营缩写 + 出生点容器 |
| `docs/record/一图一夹_2026-11-27.md` | ★ 2026-11-27 一图一夹：navdata 四处并进 data/maps，成品进 <图>/final |
| `docs/record/目录重构_2026-11-24.md` | 2026-11-24 目录重构：旧路径 → 新路径对照 |
| `docs/record/身份与页签_2026-11-24.md` | 2026-11-24 身份（用户/开发）：页表、切换、迁移、自检 |
| `docs/record/游戏目录清理_2026-11-25.md` | 2026-11-25 清游戏目录 + 直读 + 一键部署改造记录 |
| `docs/record/出生点编辑与删除拆分_2026-11-25.md` | 2026-11-25 出生点 BL/GR 增删 + 删除点位/删除区域拆分 |
| `docs/record/出生点三阵营_2026-11-27.md` | **为什么"加了出生点没人出生"**：模式↔数组映射、人机重生路径、三阵营编辑 + 新增点优先 |
| `docs/record/守卫区入口逃跑点_2026-11-28.md` | 守卫区工具 3/4 接线：入口只影响张望方向、逃跑点随机撤退、markers 格式 |
| `docs/record/守卫区删除与整体移动_2026-11-28.md` | 守卫区工具 5/6/7：严格准星删入口/逃跑点、整区两步移动 + 撤销 |
| `docs/record/采集对象记忆_2026-11-27.md` | 原始轨迹采集的「采集对象」记住上次选择：trace.who / 恢复 / 验证 |
| `docs/record/录制_人机区分_2026-11-27.md` | 录制页也分玩家 / 人机：解析、实时/复盘计数、只采人机的行为 |
| `docs/record/蹲跳与主动起跳_2026-11-27.md` | **蹲跳为什么录不进去**：主动起跳判据、小落差单向边、ct 落盘、跳链上限取消 |
| `docs/record/手动保存_2026-11-25.md` | 2026-11-25 游戏内编辑必须手动保存（Ctrl+S 唯一入口，退房间丢弃未保存） |
| `docs/record/逆向速查_版本偏移与地址.md` | 引擎版本 + md5、字段偏移、函数 RVA |
| `docs/record/` | 每轮实现笔记（文件名带日期）；只作历史证据，现状看本文件 |
| `app/workbench/web/README.md` | 工作台七页的数据来源、方向约定、3D 操作 |
| `archive/README-原文_2026-11-23.md` | 上次整理前的 README 原文（逐字保留） |

---

## 九、已知问题

1. `data/maps/_inbox/` 里还有几份没归位的可走面（`navmesh_nm*.bin` 6 个）；
   归位用 `python app/core/navdata.py import`（可先 `--dry`）。
2. ① 冻结副本的 SHA256 清单与磁盘内容对不上（9 个 map.json + 8 个 navmesh.bin 全部被标记"被改过"）。
   这是**搬动之前就有**的：清单是 2026-11-17 冻结时写的，之后 native 目录被重写过一次但没重算清单。
   `navdata.py verify` 因此一直是红的；要不要重新冻结（`freeze --force`，从游戏目录重建）由作者定。
2. `app/tools/deploy.json` 只用于开发机兜底找游戏；控制台「部署」页和 `deploy_mod.py` 以用户配置/命令行
   `--game-exe` 为准，不再用 `build.ps1 -Deploy` 往游戏目录拷 dll。
3. 运行时配置 `run\runtime\ucf_mod.json` 和部署清单 `run\runtime\deploy\` 是机器相关文件，已 gitignore；
   换机器/重装工程端时，第一次启动会从旧部署端 `ucf_mod.json` 自动搬一次（如果还在），否则用默认值。
3. `src/editor.c` 里还留着 5 个 `UCF_UI_*` 环境变量（2026-11-20 排查进图闪退用的调试开关），代码自述“定位完就删”；
   删之前要真机验证一次。
4. 2026-11-24 目录重构删掉了几份历史快照（`archive/probe_map_loader/`、`data/navdata/dev/archive/` 下的四个迁移快照），
   它们是 git 跟踪过的文件，需要时用 `git log -- archive/probe_map_loader` 找回。
   `run/payload/_rescue/level9.orig` **没删**：它是唯一一份没被打过补丁的场景。
