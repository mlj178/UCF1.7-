# ucf_mod · UCF 1.7 导航/人机插件

UnityCrossFire 1.7.1（Unity + IL2CPP）的文件化插件。
形态：游戏目录的 `winhttp.dll` 代理加载器 → 加载 `ucf_mod\ucf_mod.dll`（原生 C，mingw 编译，运行时挂 il2cpp）。

## 两个目录，别搞混

| | 位置 | 内容 | 版本控制 |
|---|---|---|---|
| **工程端** | 本目录（`06-测试\ucf_mod`）| `src/` `tools/` `docs/` `geo/` 文档 | ✅ 进 git |
| **部署端** | 游戏目录 `...\UnityCrossFire1.7.1\ucf_mod\` | `ucf_mod.dll\ `ucf_mod.json` `nav/` `markers/` `maps/` `vis/` | ❌ 不进 git |

部署端路径由 `tools/deploy.json` 指定（本机路径，已 gitignore）。所有工具都通过
`tools/ucf_paths.py` 解析：`DEPLOY` = 部署端，`PROJ` = 工程端。

**数据留在部署端**：`nav/` `markers/` `maps/` `vis/` 只在游戏目录，工具直接读写那边，工程端不留副本
（避免两份数据分叉——这正是 2026-11-16 之前"黑盒"的成因之一）。

## 目录

```
ucf_mod/
├── README.md            本文件（入口）
├── STATUS.md            ★ 当前生效状态（唯一权威，先看这个）
├── src/                 C 源码：plugin.c(加载/配置) navfix.c(A*导航) editor.c(编辑器/可视化/离线编辑)
├── tools/
│   ├── ucf_paths.py     工程端/部署端路径解析（唯一真相）
│   ├── navserver.py     网页导航编辑器后端
│   ├── navview.html     网页导航编辑器前端（俯视 + 3D）
│   ├── geo2web.py       geo/*.npz → geo/web/*.bin（3D 地形）
│   ├── extract_geo.py   从游戏资源抽几何 → geo/*.npz
│   ├── organize_maps.py vis/ 导出 → maps/ 归档
│   ├── make_practice.py 生成空白练习图
│   └── 启动导航编辑器.bat
├── docs/                各轮记录（历史证据，不作现状依据）
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

## 编辑器

双击 `tools\启动导航编辑器.bat` → 浏览器打开俯视 + 3D 分屏编辑：
编辑路点/连边/删点/移动，保存写部署端 `nav\<指纹>.txt`（游戏内插件直接读）。
`geo/web` 缺失时会自动用 `geo2web.py` 重建。

## 文档

| 文件 | 内容 |
| --- | --- |
| [STATUS.md](STATUS.md) | ★ 当前生效状态：DLL/开关/数据/功能可用性/已知问题 |
| [FEATURES.md](FEATURES.md) | 功能清单：怎么用、可用状态、明确未做项 |
| [CHANGELOG.md](CHANGELOG.md) | 改动记录（时间倒序）+ 跨轮次关键坑 |
| [FILE-INVENTORY.csv](FILE-INVENTORY.csv) | 2026-11-16 清理台账（1120 文件的分类与处置依据）|
| [docs/](docs/) | 各轮详细记录（历史证据，不作现状依据）|
