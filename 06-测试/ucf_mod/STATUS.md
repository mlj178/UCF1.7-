# STATUS · 当前生效状态

> **唯一权威**的"现在是什么"。每次构建 / 部署 / 改运行时数据后更新本文件。
> 最后更新：2026-11-16 17:30

## 1. 跑的是哪个 DLL

| 项 | 值 |
| --- | --- |
| 部署位置 | 游戏目录 `ucf_mod\ucf_mod.dll` |
| 大小 | **240,960 B** |
| SHA256 | `BB2E91026AA3466B…` |
| 构建时间 | 2026-11-16 16:53:15 |
| 源码 | `src/plugin.c` + `navfix.c` + `editor.c`（editor.c 16:52）|
| 源码↔产物一致性 | ✅ 已验证：用当前源码重建得到 240,960 B，字节数一致 |
| 回滚点 | 历史 DLL 已于 2026-11-16 清理 —— 回滚方式改为「用对应版本源码重建」|

## 2. 开关

| 开关 | 文件 | 当前 |
| --- | --- | --- |
| 隐藏地图注入 | `ucf_mod.json`（`scene=Nano30_Storm`, `enabled=true`）| **开** |
| 只读采集模式 | `collect.flag` | 关（文件不存在）|
| 禁止自动铺路点 | `nav\nogen.txt` | 关（文件不存在）|

## 3. 运行时数据（部署端）

| 文件 | 作用 | 状态 |
| --- | --- | --- |
| `markers\markers.txt` | 11 个蹲守点（crouch=11）| **生效** |
| `nav\n0-0000000000000000.txt` | 练习场编辑清单 | **生效** |
| `nav\n786-57a46e3465c847cb.txt.disabled_20261116_1655` | 运输船编辑（786→27 点）| **已停用**（会炸 A* 寻路线程；新版 DLL 下可改回原名重试）|
| `nav\names.json` | 地图中文名注册表 | 生效 |
| `maps\*.json` + `_index.json` | 11 张图原始导航数据 | 参考数据（游戏不读）|
| `vis\*.json` / `navmesh_*.bin` | 采集导出 | 输出产物 |

## 4. 功能状态

| 功能 | 状态 | 证据 / 备注 |
| --- | --- | --- |
| 隐藏地图注入（Nano30_Storm）| ✅ 可用 | 房间下拉可选 |
| 自动补 A* 导航点（0 点图）| ✅ 可用 | 网格射线采样 → Scan → ConnectNodes |
| 人机标记编辑器（Ctrl+1..9,0）| ✅ 可用 | 日志 `loaded 11 markers` |
| 自动补蹲守点 Bot_CrouchPos | ✅ 可用 | 仅在该图无蹲守点时触发 |
| 幽灵守卫区 Bot_NanoGuardArea | ⚠️ 可用有残留 | 11-15 造 42 区；仍有 bot 卡在出生洞穴 |
| 导航可视化（Ctrl+V，分层/标签）| ✅ 可用 | 日志 `vis ON layers=0x1F` |
| 进图自动导出路点（JSON）| ✅ 可用 | 17:05 导出 132 KB |
| 离线编辑 → 游戏内套用（`nav/*.txt`）| ⚠️ 修完待验 | 运输船草稿已停用；新版走 A* 软删除 |
| 「复活后只会直走」bug | ✅ 已修 / **复验待做** | 根因：重建点图 + nodeIndex=-1 炸寻路线程 |
| Bot_JumpLink 跳台 | ❌ 未做 | 需绑定 A* 图节点对 |
| 补给箱点 SP_RedBox/SP_BlueBox | ❌ 未做 | 隐藏图缺 SupplyBox → 偶发 NRE |
| 网页导航编辑器（navview + navserver）| ✅ 可用 | 俯视 + 3D，保存写 `nav/<fp>.txt` |
| 桌面版 3D 编辑器（navedit）| 🗑 已弃用 | 2026-11-16 被网页版取代；抽取器保留为 `tools/extract_geo.py` |
| 体探针 / botwalk（probe_cmd.ini）| 🗑 已废弃 | 源码零引用，文件已清理 |

## 5. 已知未解决

1. 部分 bot 仍卡在出生洞穴（11-15 记录 7/29）。
2. `Bot_JumpLink`、补给箱/出生点全量注册未实现。
3. 隐藏图缺 `MapManager.pointDic` 的 SupplyBox → 偶发空引用（不影响游玩）。
4. 日志中文偶发乱码（GBK/UTF-8 混写）。

## 6. 下一步

- [ ] 复验 16:53 的「只走直线」修复：进运输船，`Player.log` 不应再出现 `Unhandled exception during pathfinding`。
- [ ] 复验通过后，把运输船编辑草稿改回 `n786-57a46e3465c847cb.txt` 重新套用。
