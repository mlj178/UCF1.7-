# STATUS · 当前生效状态

> **唯一权威**的"现在是什么"。每次构建 / 部署 / 改运行时数据后更新本文件。
> 最后更新：2026-11-16 23:12

## 1. 跑的是哪个 DLL

| 项 | 值 |
| --- | --- |
| 部署位置 | 游戏目录 `ucf_mod\ucf_mod.dll` |
| 大小 | **252,458 B**（23:01 可走面版；249,587 B 是 21:32 防卡死版）|
| SHA256 | `2598518F7FA784D3…` |
| 部署时间 | 2026-11-16 23:01:21 |
| 源码 | `src/cfg.c` + `plugin.c` + `navfix.c` + `editor.c`（+ 可走面线框 `navmesh_show` / Ctrl+Shift+6）|
| 回滚点 | `ucf_mod\ucf_mod.dll.deployed_20261116_230121`（249,587 B 防卡死版，回到它可去掉可走面）|
| 中间版本 | `…184234` / `…184255` / `…185646`（同一天几次构建，可忽略）|
| 构建方式 | `tools\build.ps1 -Deploy` → `build/build.json` 记录来源 |

> **可复现性说明**：同一份源码连续编译，字节数恒定（当前 249,587 B）但 SHA256 每次不同。
> gcc 会往产物里写非确定性内容，所以**核对用字节数 + build.json，不要用哈希比对**。

## 2. 配置：ucf_mod.json（2026-11-16 起真的会被读）

> ⚠️ 2026-11-16 之前，`plugin.c` 里的 `read_config()` **从未被调用**，
> 整个 `ucf_mod.json` 是死的：`enabled` / `scene` / `game_mode` 全都没生效，
> 实际一直用硬编码默认值（`Nano30_Storm` / `game_mode=6`）。
> 现在由 `src/cfg.c` 统一读取，并且**启动时把每一项打进日志**（`[cfg]` 前缀）。

| 开关 | 默认 | 关掉之后 |
| --- | --- | --- |
| `enabled` | 开 | **总开关**：插件加载后完全不动作 |
| `hidden_map` | 开 | 房间地图列表里没有「暴风」 |
| `auto_waypoints` | 开 | 没路点的图不铺路点（人机会原地不动） |
| `auto_crouch` | 开 | 不自动补蹲守点 |
| `ghost_areas` | 开 | 不造幽灵守卫区 |
| `auto_export` | 开 | 不自动导出 `vis\*.json`（Ctrl+E 仍可） |
| `hud` | 开 | 进图不显示状态面板（Ctrl+H 可叫出） |
| `visualizer` | **关** | 进图画不出导航网格（Ctrl+V 可开） |
| `navmesh_show` | **开** | 不画 A* 可走面（NavMeshGraph 三角网）；Ctrl+Shift+6 可随时开关，与 Ctrl+V 互不影响 |
| `editor` | 开 | 关掉后 Ctrl+1 无法进编辑模式 |
| `collect_only` | 关 | —— 见下 |

界面：`tools\启动控制台.bat`（CustomTkinter 窗口，勾选即写盘）。面板分
**地图 / 建图 / 查看 / 手动** 四组；「加载暴风地图」（`hidden_map`）从 2026-11-16 19:46
起单独占「地图」组（此前面板里没有它的入口，只能手改 json）。

## 2.5 启动通行证（2026-11-16 19:00 起）

**直接双击 `UnityCrossFire.exe` = 原版游戏；从「UCF 控制台」点开始游戏 = 加载 mod。**

机制：加载器 `winhttp.dll`（游戏根的代理 DLL）总会把 `ucf_mod\ucf_mod.dll` 载入进程，
所以"载不载"控制不了。控制的是**载进去之后干不干活**：

```c
/* plugin.c DllMain 第一句 */
DWORD n = GetEnvironmentVariableA("UCF_MOD", gate, sizeof(gate));
if (n == 0 || gate[0] != '1') return TRUE;   /* 原版模式：到此为止 */
```

控制台启动游戏时把它放进子进程环境（`UCF_MOD=1`），所以只有从控制台起才有这枚令牌。
没有令牌：不起线程、不读配置、不写日志、不装窗口钩子。

**实测 A/B**（就是这台机器上做的）：

| 场景 | 结果 |
| --- | --- |
| 直接双击 exe，跑 22 秒 | 游戏正常运行，`ucf_mod.log` **新增 0 行** |
| 带 `UCF_MOD=1` 启动 | 完整加载，4 秒内出现 `injected into MapAsset (mode=6)` |

> 为什么不改加载器：`winhttp.dll` 是 51 KB 的预编译代理（92 个导出全是转发到 `winhttp_orig`），
> 没有源码。改它风险高、收益小 —— 反正它一定会被加载，能做的只是"纯转发"。

## 3. 三个"建图动作"已经拆开

2026-11-16 之前 `build_waypoints()` 把「铺路点 / 补蹲守点 / 造守卫区」写在一个函数体里，
第一个不跑后两个永远不会执行 —— 三个开关是假的。现在拆成：

```
survey()          只做射线采样，填 g_all[]，不创建任何对象
act_waypoints()   建 UCF_WayPoints + Scan + ConnectNodes
act_crouch()      补 Bot_CrouchPos（图里已有则跳过）
act_guard()       造 Bot_NanoGuardArea（图里已有则跳过）
run_setup()       按开关各跑各的，日志里各打一行
```

## 4. 其它运行时开关（文件形式，仍然有效）

| 开关 | 文件 | 当前 |
| --- | --- | --- |
| 只读采集 | `collect.flag` | 关（不存在）；等价于 `features.collect_only` |
| 禁止自动铺路点 | `nav\nogen.txt` | 关（不存在） |

## 5. 运行时数据（部署端）

| 文件 | 作用 | 状态 |
| --- | --- | --- |
| `markers\markers.txt` | 11 个蹲守点 | **生效** |
| `nav\n0-0000000000000000.txt` | 练习场编辑清单 | **生效** |
| `nav\n786-57a46e3465c847cb.txt.disabled_20261116_1655` | 运输船编辑草稿 | **已停用** |
| `nav\names.json` | 地图中文名注册表 | 生效 |
| `maps\*.json` | 11 张图原始导航数据 | 参考数据（游戏不读）|
| `vis\*.json` | 自动导出产物 | 输出 |

## 6. 功能状态

| 功能 | 状态 | 证据 |
| --- | --- | --- |
| 隐藏地图注入（Nano30_Storm）| ✅ | 房间下拉可选；日志 `injected into MapAsset` |
| 自动铺 A* 路点 + 连线 | ✅ | 0 点图 → 786 点 / 1391 边 |
| 自动补蹲守点 | ✅ | 图内蹲守点为 0 时触发 |
| 幽灵守卫区 | ⚠️ 可造但有残留 | 仍有 bot 卡在出生洞穴 |
| 导航可视化（Ctrl+V）| ✅ | 分层 + 标签 |
| 可走面可视化（网页）| ✅ 已实测 | 小型工厂 1139 三角 / 840 顶点；2D 俯视 + 3D 都是绿色三角网；开关对比截图 `screenshots/web_navmesh_l2.png` / `..._off.png` |
| 可走面可视化（游戏内）| ⏳ 已实现待进图复验 | 独立开关 `navmesh_show` + Ctrl+Shift+6 + HUD 一行计数；进图日志应出现 `vis: navmesh wire tris=...`（见 §6.7）|
| 游戏内标记编辑 | ✅ | `loaded 11 markers` |
| 自动导出路点 JSON | ✅ | 17:05 导出 132 KB |
| 网页导航编辑器 | ✅ | 俯视 + 3D，保存写 `nav/<fp>.txt` |
| 控制台开关面板 | 🆕 待验证 | `tools\启动控制台.bat` |
| HUD 只进图 + 中文字体 | ✅ 已验证 | 20:29 大厅无 HUD；21:20 运输船进图 `hud: cjk font … (probe U+4E2D)`、`hud: ready … (game/CJK)`，截图 `screenshots/inmap_cjk_hud.png` |
| 进图采样不卡死 | ✅ 已修 / ⏳ 暴风待复验 | `survey` 的 `maxZ` 初值修正 + 命中点/包络/列数三重保险；21:13 AppHang 的根因见 §6.6 |
| Bot_JumpLink 跳台 | ❌ 未做 | |
| SP_RedBox / SP_BlueBox | ❌ 未做 | HUD 里 `缺:` 那行就是它 |

## 6.5 HUD 修复：只进图显示 + 真中文字体（20:28）

**现象**：大厅/房间左上角有 `00000000`，下面一条黄色 `|++|...`。
两者都是 UCF HUD：`g_hud` 的状态行（8 个计数）和 `g_keys` 的快捷键行；
HUD 在大厅就被 `editor_tick` 建出来，而且借到的字体没有中文字形，
中文标签全被吞掉，只剩数字/标点。

**改法**（`src/editor.c`）：

1. `hud_refresh()` 开头先查 `navfix_point_graph()`：大厅没有 PointGraph 直接 return，
   不建 HUD、不刷文字。
2. 换图后旧 Canvas 可能已被场景销毁但 `g_hud` 指针还在 → 先用 `uobj_live()` 验活，
   失效则 `hud_reset()` 重建，避免对已销毁 UGUI Text 调 SetText 崩溃。
3. 新增 `find_cjk_font()`：遍历场景所有 UGUI Text 的字体，用
   `Font.HasCharacter('中'/'国'/'的'/'房'/'间')` 选真正带中文字形的字体；
   找到后用 gchandle 根住。找不到才退回 Arial，并自动改用英文 fallback。
4. `g_cjk` 现在只在字体真的含中文时为 1；`g_keys` / `g_cat` 都补了英文 fallback。

**验证**：

- 20:29 启动游戏（`UCF_MOD=1`），大厅日志只到 `waiting for PointGraph`，
  **没有** `hud: ready`（旧版 19:53 同一位置会建 HUD）。
- 房间截图：左上角 `00000000` 和黄色 `|++|` 条都消失（`screenshots/final_lobby_crop.png`）。
- 21:20 进「运输船」复验通过：日志出现 `hud: cjk font 23d82138 from Text #0 (probe U+4E2D)`
  与 `hud: ready font=23d82138 (game/CJK)`；游戏内左上角是中文状态面板（`screenshots/inmap_cjk_hud.png`）。

## 6.6 进图卡死修复：survey 的 maxZ 初值（21:26）

**现象**：从控制台启动、进「暴风」图后游戏卡死/闪退。Windows 事件日志
21:13:38 记录 `AppHangB1`（进程 UnityCrossFire.exe）。

**证据**：`ucf_mod.log` 最后一行停在

```
21:13:15 [nav] survey: coarse hits=35 bounds x[-50.0,30.0] z[-130.0,1000000000.0]
```

之后再也没有 `survey: spots=...`，主线程停住。

**根因**（`src/navfix.c`）：

1. `survey()` 里 `float minX = 1e9f, maxX = -1e9f, minZ = 1e9f, maxZ = 1e9f;`
   —— `maxZ` 的初值写成了 **+1e9**，应为 `-1e9`。粗扫更新 `maxZ` 的条件是
   `hit.z > maxZ`，正常地图永远不成立，所以 `maxZ` 一直是 1e9。
2. 细扫 `for (fz = minZ-4; fz <= maxZ+4; fz += 4)` 于是从 -134 跑到 +1e9，
   约 `(1e9/4) × 列数 ≈ 五十多亿次`，主线程永远出不来。
   日志里的 z 上限 1000000000 就是初值，不是命中点。

**改法**：

1. `maxZ` 初值改为 `-1e9f`（真正的修复）。
2. 新增 `hit_sane()`：命中点必须有限、与射线起点同竖线（±0.75 m）、y 在 ±500 内；
   坏点直接丢弃。
3. 粗扫后校验包络：宽/高必须 ≥1 m 且 ≤700 m，否则本次采样放弃（下个 tick 重试）。
4. 细扫加列数上限 50000，超限直接放弃；日志新增 `survey: dropped N bogus hits`
   与第一条坏点的坐标。

**验证**：

- 21:20「运输船」、21:23「小型工厂」均能进图，HUD/自动导出正常；中文字体已确认（见 §6.5）。
  这两张图的路点图本来就有节点（786 / 12），`run_setup` 不会触发，所以没走到 survey。
- 暴风图本轮未复验：自动化房间里 `比赛类型` 是「团队模式」，地图下拉只有
  运输船/小型工厂/椰岛之巅。暴风属于 `GameMode 6 = Nano4_Terminator`（终结者模式），
  要在「比赛类型」里选终结者模式，mode 6 的 MapAsset（已注入 2 条）才会成为当前地图列表。
- 复验时日志应出现 `survey: coarse hits=...` 且 z 范围正常（不会再出现 1000000000），
  随后 `survey: spots=...`；若命中点异常会出现 `survey: dropped N bogus hits`。

**产物**：`ucf_mod.dll` **249,587 B**，SHA256 `E24D18A3…`，部署 21:32:01；
回滚点 `ucf_mod.dll.deployed_20261116_213201`（21:26 首次防卡死版）。

## 6.7 可走面可视化 + 进图自动化受限（23:12）

**做了什么**：把 A* NavMeshGraph 的三角形**画出来**，并且开关可见、可复盘。

- 游戏内（`src/editor.c`）：`nm_walk()` 直接读运行时 `NavmeshBase.tiles`（和导出同一个结构），
  按三角形边生成线框网格（`flush_mesh_to` 单独一批对象，不占 Ctrl+V 五层的 80 个名额）；
  独立开关 `navmesh_show`（cfg.c + 控制台「查看」组，默认开），`Ctrl+Shift+6` 随时开关并立即重建；
  换图后 `vis_scene_reset` 把对象链表清空、下一帧重建。HUD 多一行计数：
  `可走面 开  1139 三角 / 840 顶点  (A* NavMeshGraph，Ctrl+Shift+6 开关)`。
- 网页（`tools/navview.html` + `navserver.py`）：「显示」组新增勾选 + 计数，
  2D/3D 都画绿色三角网；`/api/navmesh?level=` 按「maps 里记的原文件名 → 原生顶点数对号」解析。

**格式坑**：`UCFNM3` 头 = 7 字节 magic（含结尾 0）+ nv + **索引数** + ntile + flags +
矩阵 + 平移；第二个 int 是索引数（3417 = 1139×3），不是三角形数。顶点表从 99 开始。

**验证**：
- 网页：小型工厂开/关两张截图，计数 1139/840 与 22:20 的原生清点一致；
  `/api/navmesh?level=level2|level3|level5` 都能取到，`level1`（运输船，无 NavMeshGraph）返回 404。
- 游戏内：**未完成**。本轮自动化点不进房间的「开始游戏」（见下），所以 HUD/线框还没有进图截图。

**进图自动化受限**（记下来免得下次再撞）：
- 现象：`SetCursorPos` + `mouse_event`/`SendInput` 对 UnityCrossFire 窗口无效
  （连标题栏双击都不放大），同一套注入对资源管理器/浏览器有效；`SendKeys` 键盘也无效。
  窗口前台切换成功（`GetForegroundWindow` 已是游戏），但游戏不响应合成输入。
- 判断：本轮 agent 的进程与游戏窗口不在同一个可交互输入桌面/窗口站，注入的事件到不了 Unity 的消息队列。
- 影响：进图复验需要**人手点一次「开始游戏」**（游戏现存于房间界面，选好 运输船/团队模式）。
- 复验时看三处：HUD 第四行「可走面 …」；地图上的绿色三角网；日志 `vis: navmesh wire tris=… verts=… meshes=N`。
  按 `Ctrl+Shift+6` 应看到线框立即消失/出现，日志出现 `navmesh OFF/ON`。

## 7. 死代码清理 + 编译闸门（18:42）

删掉 6 处「定义了但没人用」的代码，并给 gcc 加了闸门，防止同类问题再悄悄进来。

| 位置 | 删了什么 | 为什么要删 |
| --- | --- | --- |
| `plugin.c` | `read_config()`（上一轮已删）| 从没被调用，是 `ucf_mod.json` 变死的元凶 |
| `navfix.c` | `rptr()` | 一行取值辅助，早已被直接强制转换取代 |
| `navfix.c` | `make_guard_area` 的 `tr` / `zero` | 从没用过的局部变量 |
| `editor.c` | `find_img()` | 整段 il2cpp image 查找，**从头到尾没被调用** |
| `editor.c` | `x_image_get_name` 指针 + `RESOLVE(image_get_name)` | 仅被 `find_img` 使用，随之死亡 |
| `editor.c` | 解析 `nav/*.txt` 时的 `k2` | 读进来就丢，格式里没有第二个 key |

**闸门**：`build.ps1` 现在带 `-Werror=unused-function -Werror=unused-variable`。
验证过——往 `cfg.c` 塞一个 `static int ucf_dead_probe(void)`，编译直接失败：

```
cfg.c:126:12: error: 'ucf_dead_probe' defined but not used [-Werror=unused-function]
```

> 删完后 DLL 字节数 **仍然 246,163 B，一个字节没变** —— 说明删掉的东西从来没进过产物，
> 是真的死代码，行为零风险。

## 8. 已知未解决

1. 部分 bot 卡在出生洞穴。
2. `Bot_JumpLink`、补给箱/出生点全量注册未实现。
3. 隐藏图缺 `MapManager.pointDic` 的 SupplyBox → 偶发空引用（不影响游玩）。
4. 日志中文偶发乱码（GBK/UTF-8 混写）。

## 9. 下一步

- [ ] **验证本次改动**：进一次图，确认 `ucf_mod.log` 开头出现 `[cfg] ======== ucf_mod.json loaded` 与 10 行开关。
- [ ] 逐个关开关试：关 `auto_crouch` 后日志应出现 `[cfg] auto_crouch = off, skip crouch points`。
- [ ] 复验「复活后只会直走」修复。
- [ ] 复验通过后，把 `n786-…disabled_20261116_1655` 改回原名重新套用。
- [x] 进图复验 HUD：21:20 运输船通过（中文面板 + `hud: cjk font`）。
- [ ] 进暴风图复验 survey：比赛类型选「终结者模式」→ 地图选「隐藏地图 暴风」→ 开始；
      确认不再卡死，日志出现正常的 `survey: coarse ...` / `survey: spots=...`。
