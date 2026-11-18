# ucf_mod · UCF 1.7 导航/人机插件

UnityCrossFire 1.7.1（Unity + IL2CPP）的文件化插件。
形态：游戏目录的 `winhttp.dll` 代理加载器 → 加载 `ucf_mod\ucf_mod.dll`（原生 C，mingw 编译，运行时挂 il2cpp）。

> **只想玩游戏 / 只想改路点？** 不用看本文件，看游戏目录里的 `ucf_mod\README.txt`（三句话讲完）。
> 本文件是开发说明，给改代码的人看。

## 三个目录、四版数据，别搞混

| | 位置 | 内容 | 版本控制 |
|---|---|---|---|
| **工程端** | 本目录（`06-测试\ucf_mod`）| `src/` `tools/` `docs/` `geo/` `navdata/` | ✅ 进 git |
| **部署端** | 游戏目录 `...\UnityCrossFire1.7.1\ucf_mod\` | `ucf_mod.dll` `ucf_mod.json` `nav/` `markers/` `maps/` | ❌ 不进 git |

数据分四版（2026-11-18 起）：

| 版 | 在哪 | 谁写 |
| --- | --- | --- |
| ① 备份版（只读） | 工程端 `navdata\native` | 只有 `navdata.py freeze` |
| ② 开发版 | 工程端 `navdata\dev` | 编辑器 / 控制台「导入到开发版 ④→②」 |
| ③ 部署版 | 游戏目录 `ucf_mod\` | 只有控制台「部署到游戏 ②→③」 |
| ④ 测试版 | 工程端 `navdata\test\`（vis / packs / archive） | 插件 Ctrl+E 导出、测试包、游戏内试改 |

数据流：**游戏导出 → ④ →（导入）→ ② →（部署）→ ③**；① 随时冻结。详细规则见
[docs/三版数据与路径_2026-11-17.md](docs/三版数据与路径_2026-11-17.md)（内容已升级为四版）。

部署端路径由 `tools/deploy.json` 指定（本机路径，已 gitignore）。所有工具都通过
`tools/ucf_paths.py` 解析：`DEPLOY` = 部署端，`PROJ` = 工程端，`TEST` = ④。

## 目录

```
ucf_mod/
├── README.md            本文件（入口）
├── STATUS.md            ★ 当前生效状态（唯一权威，先看这个）
├── src/                 C 源码：cfg.c(配置) plugin.c(加载/注入) navfix.c(A*导航) editor.c(编辑器/可视化)
├── tools/
│   ├── ucf_paths.py     工程端/部署端路径解析（唯一真相）
│   ├── navserver.py     路点工作台本地只读服务
│   ├── navview.html     只读查看前端（俯视 + 3D + 可走面）
│   ├── geo2web.py       geo/*.npz → geo/web/*.bin（3D 地形）
│   ├── 控制台.pyw        开关面板（CustomTkinter，双击 启动控制台.bat）
│   ├── test_console_switches.py  cfg.c ↔ 控制台开关表一致性自检
│   ├── extract_geo.py   从游戏资源抽几何 → geo/*.npz
│   ├── navdata.py       四版管理（status / import / publish / restore / verify / freeze / pack）
│   ├── tidy_vis.py      ④ 导出归类（raw/ + navmesh/ + _state/）
│   ├── migrate_four_versions.py  一次性迁移：③ 里的导出搬进 ④
│   ├── organize_maps.py ④ 导出 → ② maps/ 归档
│   └── make_practice.py 生成空白练习图
├── docs/                各轮记录 + 地图对照表.md（★ 序号/关卡/中文名/场景名的唯一权威表）
└── geo/                 *.npz 地形源；geo/web/ 由 geo2web.py 生成（gitignore）
```

## 构建与部署

```powershell
# 编译（产物进 build/，带日期与 git 短哈希）
.\tools\build.ps1

# 部署到游戏目录（会先关游戏，再备份旧 dll 为 .deployed_<时间>）
.\tools\build.ps1 -Deploy
```

部署端 `uninstall.ps1` 只移除部署物（dll/加载器/还原场景），**不会删源码**。

## 只读查看

打开 UCF 控制台，点「路点工作台（查看）」→ 浏览器打开路点工作台（只读）：
俯视 + 3D、可走面、特征点、路线/区域、文件列表、关卡切换；网页端不提供编辑。
部署 / 建测试包仍用控制台「数据」「测试数据」页，或 `python tools/navdata.py publish|pack`。
`geo/web` 缺失时会自动用 `geo2web.py` 重建。

## 控制台「人机路点」+ 游戏内菜单（2026-11-18）

- 控制台新页签「人机路点」：选图 / ④ 测试包 / ③ 正式版、六项开关、点类型笔刷、节点/边/特征计数、撤销/重做/保存/重读/清空、最近 `[naved]` 日志。
- 游戏内按 **F2** 打开路点菜单；**长按 E 0.45 s** 备用（UCF 没有 E 交互，用户已确认）。按 F2 / 小键盘前先点一下游戏画面，让游戏窗口拿到焦点。
  菜单键位（2026-11-18 二次调整，避开游戏内的 Enter/Esc/W/S）：`1-9` 直选；小键盘 `8/2` 上下、`5` 确认、`0` 返回（滚轮也可上下）；左键确认、右键返回。
  菜单打开时只拦菜单键和会误触的武器/功能键（数字、Q/R/G/F/Tab 等）；小键盘专供菜单；W/A/S/D、空格、Shift、Ctrl 仍交给游戏，选完 A 可以走到 B 再按小键盘 5 连边；回车/Esc 只作用于菜单，不再触发游戏。鼠标左右键和滚轮也被菜单消费。
- **加点前提**：运行期不能增长 PointGraph 节点数组，只能复用「不可走」槽位。原生点全可走的图（沙漠要塞 12 点、运输船 786 点）直接加点会打 `no free slot`；先建 **空白底图测试包**（运输船 / 新寂静村，把原生点全禁用），或先删一个点。**飓风危城原生 0 点，建不了空白包**（没有可借槽位）。
- 菜单动作：添加普通/蹲守/守点/聚集区/标签区；跳跃点用 `Bot_JumpLink`（Link[] 一个元素，`OnLatePostScan` 挂 `startNode`，**本轮是 session-only，重启不保留**）；建立双向/单向路径（文件里 `edge out` / `edge in`）；删除路径/点；落地；聚集区新建/加守点；撤销/重做/保存；显示图层。
- 点/边仍写 ④ 包或 ③ `nav\<指纹>.txt`；蹲守/守区/守点/标签写 `ucf_mod\markers\markers.txt`（**目前不分图，按指纹分文件还没做**）。
- 新增配置键：`wp_menu`、`wp_autoground`（bool）、`wp_brush`（字符串 normal/jump/crouch/guard/area/tag）。
- 实测（2026-11-18 21:40）：F2 开 → 小键盘 2 两次（`sel=2`）→ 小键盘 5 进「建立路径」→ 小键盘 8 一次从 1 回绕到 3（`subsel=2`）→ 小键盘 5（`path dir=2`）；小键盘 0 先取消放置、再关菜单；主键盘 `3` 连按两次也能直选路径方向；W 仍交给游戏（选完 A 可走到 B），滚轮 / 右键 / 回车 / Esc 都被菜单消费。
- 本轮部署 DLL：`ucf_mod-20261118-2140-41f78046.dll`，SHA256 `AEF98FFF612F0F50A2D1AAAEA2072E2BB8ABB43D9E088254DC42BA982054E3B3`（已复制到游戏目录 `ucf_mod\ucf_mod.dll`）。

## 文档

| 文件 | 内容 |
| --- | --- |
| [STATUS.md](STATUS.md) | ★ 当前生效状态：DLL/开关/数据/功能可用性/已知问题 |
| [FEATURES.md](FEATURES.md) | 功能清单：怎么用、可用状态、明确未做项 |
| [CHANGELOG.md](CHANGELOG.md) | 改动记录（时间倒序）+ 跨轮次关键坑 |
| [FILE-INVENTORY.csv](FILE-INVENTORY.csv) | 2026-11-16 清理台账（1120 文件的分类与处置依据）|
| [docs/地图对照表.md](docs/地图对照表.md) | ★ **唯一权威**：11 张图的 序号/关卡/中文名/场景名（手写，脚本都读它）+ 原生 A* 数据 + 每张图挂了哪些人机组件 |
| [docs/人机与路线设计.md](docs/人机与路线设计.md) | **新手先看这篇**：人机行为的优先级、路线元素（点/线/面）、各模式与各图需要什么、能不能在启动前预设人机行为 |
| [docs/](docs/) | 各轮详细记录（历史证据，不作现状依据）|
