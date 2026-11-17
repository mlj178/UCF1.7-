# STATUS · 当前生效状态

> **唯一权威**的"现在是什么"。每次构建 / 部署 / 改运行时数据后更新本文件。
> 最后更新：2026-11-17 21:35

## 1. 跑的是哪个 DLL

| 项 | 值 |
| --- | --- |
| 部署位置 | 游戏目录 `ucf_mod\ucf_mod.dll` |
| 大小 | **287,371 B**（2026-11-17 21:23 **控制台运行中命令版**：空白底图 + `ucf_navcmd.txt` 运行中切包/重读/保存/回正式版 + 空白底图不画原生点；seq 用 64 位）|
| SHA256 | `BE9947D8A57D56AB…`（同源重编哈希会变，核对用字节数）|
| 部署时间 | 2026-11-17 21:23:28（`build.ps1 -Deploy`，替换前自动备份）|
| 车测结论 | **PASS**：level1（运输船）360 tick；`blank base: disabled 786`；运行中 `reload` → `base restored` → 再套 blank；`off` → 回 `nav\`；`apply` → 再套 blank。游戏内注入 Ctrl+Shift+N 成功：`node added idx=0`，pack 文件写出 `blank + node add`，无崩溃 |
| 源码 | `src/cfg.c` / `plugin.c` / `navfix.c` / `editor.c` / `autotest.c`（车测入口，仅 `UCF_AUTOTEST` 时动作）|
| 回滚点 | `ucf_mod\ucf_mod.dll.deployed_20261117_212328`（286,859 B，21:19 运行中命令首版）/ `…_211917`（281,732 B，21:01 面板开关版）/ `…_210104`（280,677 B，20:56 空白底图版）/ `…_205622`（278,140 B，18:41 测试包版）/ `…184149`（278,140 B，第一版）/ `…183957`（265,870 B，11:00 修复版）/ `…110028`（265,297 B，车测抓崩版）/ `…094738`（252,458 B 可走面版）|
| 中间版本 | `…2053`（280,677 B，未部署的中间构建）/ `…184234` / `…184255` / `…185646`（同一天几次构建，可忽略）|
| 构建方式 | `tools\build.ps1 -Deploy` → `build/build.json` 记录来源 |

> **可复现性说明**：同一份源码连续编译，字节数恒定（当前 287,371 B）但 SHA256 每次不同。
> gcc 会往产物里写非确定性内容，所以**核对用字节数 + build.json，不要用哈希比对**。

> **2026-11-17 21:23 控制台运行中命令版已部署**：产物 `build\ucf_mod-20261117-2123-6f8cbca3.dll`，**287,371 B**；
> 旧 DLL 备份 `ucf_mod.dll.deployed_20261117_212328`（286,859 B，21:19 运行中命令首版）。
> 车测用 level1 运输船：空白底图 786 点全禁用，reload/off/apply 三条命令都执行成功；
> 游戏内注入 Ctrl+Shift+N 加点成功并写回 pack 文件。
> 部署方式 `tools\build.ps1 -Deploy`（会先关游戏）。
> 控制台「数据」页的「部署到游戏」只推 nav 数据，**不换 DLL**；三个旧 .bat 已在 20:45 删除。

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
| `hud` | 开 | 进图不显示状态面板（Ctrl+H 可叫出；控制台在「状态面板」页） |
| `hud_states` | 关 | 不显示面板第一行（可视化/五层/标签状态）；控制台「状态面板」可开 |
| `hud_keys` | 关 | 不显示 Ctrl+H 快捷键块；按 Ctrl+H 仍可临时叫出（只对本次进程） |
| `hud_log` | 开 | 不显示导出结果 / 最近 3 行日志；Ctrl+M 仍可切 |
| `vis_layer_a` | 开 | 不画 A 层（路点/连线）；导出仍全量 |
| `vis_layer_b` | 开 | 不画 B 层（人类蹲守） |
| `vis_layer_c` | 开 | 不画 C 层（幽灵守区） |
| `vis_layer_d` | 开 | 不画 D 层（出生点/补给箱） |
| `vis_layer_e` | 开 | 不画 E 层（模式） |
| `vis_labels` | 0 | —— 三态：0 关 / 1 近距 35 m / 2 全部 |
| `visualizer` | **关** | 进图画不出导航网格（Ctrl+V 可开） |
| `navmesh_show` | **开** | 不画 A* 可走面（NavMeshGraph 三角网）；Ctrl+Shift+6 可随时开关，与 Ctrl+V 互不影响 |
| `editor` | 开 | 关掉后 Ctrl+1 无法进编辑模式 |
| `collect_only` | 关 | —— 见下 |

界面：`tools\启动控制台.bat`（CustomTkinter 窗口，勾选即写盘）。页签 **地图 / 查看 / 状态面板 / 手动 /
测试数据 / 数据**（2026-11-17 21:10 起「测试数据」从上方常驻面板改成页签，页签可视高度 285 → 553 px）；
「建图」页连同三个自动建图开关已从面板删除，C 侧键保留默认开（旧配置/回滚仍有效）。
「加载暴风地图」（`hidden_map`）在「地图」页，从 2026-11-16 19:46 起一直单独成组；
「测试数据」页 = 正式版 / 测试包 + 只对哪张图生效 + 新建空白包 + 运行中「载入到游戏 / 重新应用 /
保存路线 / 清空当前图 / 回正式版」五个按钮 + 当前包摘要（空白底图 · 几点几边 · 最后写入时间）。

**「状态面板」页 = 面板开关总入口**（2026-11-17 21:01 起）：面板本身（`hud`）、游戏里面板显示什么
（`hud_states` / `hud_keys` / `hud_log`）、可视化（`visualizer` + A–F 五层 + `navmesh_show`）、
文字标签（`vis_labels` 三态）全在这一页；游戏里那块字只留状态数字，开关状态行与快捷键块默认不显示。
「查看」页只剩 `auto_export` / `vis_lists`。页底保留 Ctrl+H 键位表（游戏里默认看不到，文案由
`tools/test_console_switches.py` 与 `src/editor.c` 对拍）。

## 2.4 测试包：UCF_PACK / UCF_FP（2026-11-17 18:41 起）

路线数据不再只有「部署版」一套：控制台「测试数据」页可以选 **正式版 / 测试包 + 只对哪张图生效**，
两个值以环境变量递给游戏进程，插件启动时读（`editor.c` 的 `pack_init()`）。

| 变量 | 默认 | 说明 |
| --- | --- | --- |
| `UCF_PACK` | 空 | 空 = 读 `ucf_mod\nav\<指纹>.txt`（一直是正式版）；有值 = 读 `ucf_mod\packs\<包名>\<指纹>.txt` |
| `UCF_FP` | 空 | 空 = 不限图；有值 = **只有当前场景指纹等于它才套用**，别的图整包跳过（日志一行 `pack: skip`） |
| `UCF_FPLABEL` | 空 | 只用于 HUD / 日志显示（图的中文名） |

包名只收 ASCII（`[A-Za-z0-9_-]`，≤48）：插件用 ANSI 的 `CreateDirectoryA/fopen`，中文路径没验证过。

**包从哪来**

1. 编辑器画完 → 点顶栏 **存为测试包**（写 `packs\<包名>\）`，或
2. 命令行：`python navdata.py pack new chain_a --level 9`（从开发版复制该图的改动）
3. 验证满意后 `python navdata.py pack promote chain_a`（备份旧文件 → 写进正式版 `nav\`）

HUD 第 5 行固定显示数据来源：`数据 正式版（nav）` / `数据 测试包 chain_a · 只对 暴风 生效 · 包内 0 项改动` /
`… 当前图已跳过`。**出问题先看这一行。**

**空白底图（2026-11-17 20:52 起）**：包文件表头下面写一行 `blank`，插件进图先把该图**所有原生点**
标不可走、摘连接，再套包里的 `node add` / `edge add`；包目录里的 `nogen.txt` 同时关掉自动铺点。
生成：控制台「测试数据 → 新建空白包」/ 编辑器保存面板「新建空白包」/ `navdata.py pack new ... --blank`。
编辑：**进游戏里直接画**（Ctrl+Shift+N 加点 / A 选起点 / J 连断边 / D 删点 / Z 撤销），
每次改动自动写回 packs；网页编辑器只是可选工具。`blank` 包不能 promote 到正式版
（`navdata.py pack promote` 会明确拒绝，避免把正式版清空）。

**运行中命令：`ucf_navcmd.txt`（2026-11-17 21:15 起）**：控制台「测试数据」页的五个按钮不再要求重启游戏。
控制台原子写 `<插件目录>\ucf_navcmd.txt`（`seq / cmd / pack / fp` 四行），插件在主线程 tick 里每
0.5 s 查一次，seq 变了才执行：

| cmd | 控制台按钮 | 插件动作 |
| --- | --- | --- |
| `apply` | 载入到游戏 | 还原原生底图 → 切到 pack → 重读 `packs\<包>\<fp>.txt` → 套用（`blank` 照样生效） |
| `reload` | 重新应用 | 同上，强制重读文件（外部改过 txt 时用） |
| `save` | 保存路线 | 把内存里的编辑清单立即写回当前 pack 文件 |
| `off` | 回正式版 | 还原原生底图 → 改读 `nav\` → 套用正式版编辑 |

切包/回正式版前会先用**原生底图快照**还原：第一次套用前记录每个节点的可走位、坐标和连接
（连接按 nodeIndex 存，不存指针），所以场景重建后也不会把旧 PointNode 写进新图。
旧命令不会在新进程里重放：`pack_init()` 只记下当前 seq，不执行。

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

## 5. 运行时数据（三版，2026-11-17 起）

| 数据 | 路径 | 作用 | 状态 |
| --- | --- | --- | --- |
| ① 原生备份（只读） | 工程端 `navdata\native` | UCF 原版数据 + SHA256 清单 | **冻结 2026-11-17 12:13**，9 个地图文件（8 张有数据 + 暴风空档）/ 8 份可走面 |
| ② 开发版 | 工程端 `navdata\dev` | 编辑器默认读写 | 生效（= ①） |
| ③ 部署版 | `D:\…\UnityCrossFire1.7.1\ucf_mod` | 游戏插件读 | 生效（= ②） |
| ④ 测试包 | ③ 里 `packs\<包名>` | 控制台选「测试包」时插件改读这里，只对一张图 | 1 个（`chain_a`=暴风演示，0 条改动） |
| 编辑清单 | ③ 里 `nav\n<指纹>.txt` | 进图自动套用 | **无**（原生不带编辑） |
| 名字注册表 | ③ 里 `nav\names.json` | 地图中文名 | 生效 |
| 原始数据 | ③ 里 `maps\*.json` | 9 份（786 / 12 / 2 / 17 / 18 / 12 / 3063 / 180 点 + 暴风 0 点空档） | 参考（游戏不读） |
| 可走面 | ③ 里 `vis\navmesh_nm*.bin` | 8 份（60 / 532 / 559 / 683 / 716 / 840 / 919 / 944） | 输出 |
| 蹲守点 | ③ 里 `markers\markers.txt` | 11 个蹲守点 | **生效** |

> 三版怎么用、路径细节：`docs/三版数据与路径_2026-11-17.md`；四版的路径 / 最近写入时间 / 两两是否一致，
> 直接看**控制台「数据」页**（同一个 `python tools/navdata.py status`），部署/还原/校验也在那页点按钮；
> 四张卡的路径旁有 **打开文件夹**（2026-11-17 21:35 起），不用自己去资源管理器里翻。

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
| 控制台开关面板 | ✅ | 6 页：地图 / 查看 / 状态面板 / 手动 / 测试数据 / 数据；「状态面板」页 21:01 起接管面板全部开关（17 个开关 / 4 页，含五层与标签三态），游戏里只留状态数字；「测试数据」21:10 改成页签；「数据」页四张卡 21:35 起带「打开文件夹」；截图 `screenshots/console_tabs_status.png` / `console_tabs_pack.png` / `console_tabs_data.png` |
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

> **2026-11-17 21:01 起**：面板默认只留状态数字 —— 第一行开关状态（`hud_states`）与快捷键块
> （`hud_keys`）默认不显示，开关全部搬到控制台「状态面板」页（见 §2）；Ctrl+H 仍可临时叫出快捷键块。

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

## 6.8 数据只留原生 + 三版分离（2026-11-17 08:50）

**做了什么**

1. 把「我们造的」从数据里彻底拿掉（判据 `map.source == game`）：
   练习沙盒 `00_练习场.json`、暴风那 694 个插件自动铺点、`nav\g_.json` /
   `nav\暴风.json` / `nav\练习场（空白）.json` 三份带编辑的草稿、练习场 26 条编辑清单。
2. 暴风（level9）原生 0 路点、无 NavMeshGraph → 留一个空档说明文件，写清「为什么是 0」。
3. 新增 `tools/navdata.py` + 三个 bat：`freeze / verify / restore / publish / diff / status`。
4. 编辑器：地形下拉带中文名（`level2 · 小型工厂 0.62 MB`）、顶栏「版本」徽标、
   「部署到游戏」「还原原生」按钮；只读档下保存按钮禁用、服务端 403。

**三版路径**

| | 路径 |
| --- | --- |
| ① 备份版（只读，永不编辑） | `D:\trae_project\ucf1.7-modifier\06-测试\ucf_mod\navdata\native` |
| ② 开发版（可编辑） | `D:\trae_project\ucf1.7-modifier\06-测试\ucf_mod\navdata\dev` |
| ③ 部署版（游戏读） | `D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\ucf_mod` |

**证据**

- `python tools/navdata.py status`：① 12 个文件（maps 4 / nav 1 / vis 7）、只读；② 同；③ 21→15 个文件；
- `python tools/navdata.py verify`：`OK 备份版校验：通过（12 个文件）/ 只读属性：是`；
- `/api/maps` 返回 `profile.cn=开发版`、`snapshots=4`（运输船/小型工厂/椰岛之巅/暴风）、`edits=0`；
- 截图 `screenshots/web_native_only.png`、`screenshots/web_level_names.png`；
- 回滚点 `navdata\_before_cleanup_20261117.zip`（旧 21 个文件）。

## 6.9 进图闪退（沙漠要塞）· 2026-11-17 09:47

**现象**：采集完前几张图后进「沙漠要塞」（level7）必闪退；11-17 09:33:40 / 09:34:03 两次。
两次日志都停在 `vis: navmesh wire tris=1259 verts=919 meshes=2`，之后没有任何一行。

**证据**

- 事件日志：Faulting module `UnityPlayer.dll`，offset **0x755e86**，异常码 **0xc0000005**，两次相同；
- Unity 崩溃报告（`%TEMP%\Alexander_GaGa\穿越火线\Crashes\Crash_2026-11-17_01*`）里有 crash.dmp；
  自写解析器读模块表 + 异常流 + 崩溃线程栈，栈上有 30 个 ucf_mod 返回地址，还原为
  `NavProc -> editor_tick+0x65f -> vis_rebuild+0x17e -> read_crouch/read_nano -> comp_pos+0x27 -> call *%ecx`
  （`call *%ecx` 是调 il2cpp 取 Transform 位置的那条指令）。

**根因**：进图瞬间 `vis_rebuild` 立刻读游戏自己的静态组件表（`SpareAreaList` / `SpareList_BL/GR` / `MapManager`），
这些表在换图时还指着上一张图正在销毁的组件 → `comp_pos` 拿到的「Transform」是野指针 → 崩在 UnityPlayer。

**修法**

1. `VIS_SCENE_WAIT=90`：进图前 90 帧不读这些表（可走面线框仍然立刻画）；
2. `comp_pos`：`mem_ok` + `uobj_live` + **klass 必须等于已知 Transform 类**（否则 `g_badTr++` 跳过）；
3. 新开关 `vis_lists`（默认 true）：关掉后完全不碰游戏组件表，只画 A* 图与可走面。

**验证状态**：DLL 已部署 09:47:38；下次进沙漠要塞看日志应出现 `vis: nodes=... badtr=N` 且不再截断。
若仍崩：`ucf_mod.json` 里 `visualizer:false` 或 `vis_lists:false` 后复现一次并回传 `ucf_mod.log` 与 crash.dmp。

## 6.10 进图闪退的真因（导出时机）· 2026-11-17 11:00

**这次是车测跑出来的，不是推断**：`tools\autotest.ps1 -Targets 7,10` 让插件在游戏进程里
直接 `SceneManager.LoadScene(index, Single)` 切图（不需要鼠标键盘），每图等 N tick。
同一套测试：10:57 版在 level10 必崩，11:00 版 `7,10,7,10` 四趟全 PASS。

**崩溃现场（第一次抓到我们自己的帧）**

- 给 gcc 加 `-fno-omit-frame-pointer`；VEH 只把**可执行节**里的地址当返回地址；打印寄存器。
- 栈：`NavProc → editor_tick+0x9de → vis_export+0xa9 → read_nano+0xb3 → comp_pos+0x46
  → GameAssembly+0x32cf63(Component.get_transform) → UnityPlayer+0x755e86`。
- 寄存器 `ebx=esi=edi=0x43ef6323`＝float 478.77 —— `SpareAreaList[0]` 读出来的是浮点数。

**根因**：`auto_export_tick` 只等「路点数稳定 ~2 s」就导出，**没等场景稳定**。
进图 2 s 内游戏自己的静态组件表还是上一张图正在销毁的对象 → 导出路径撞上 → 崩。
09:55 的 `VIS_SCENE_WAIT` 只保护了 `vis_rebuild`，漏了导出。

**修法**（4 处）

| 改什么 | 在哪 |
| --- | --- |
| 导出必须 `g_sceneAge >= VIS_SCENE_WAIT(90)` | `auto_export_tick` / `vis_export` |
| 稳定前只读路点+可走面，组件表整段跳过 | `collect_read()` |
| 列表元素先校验 klass 再当组件用 | 新 `obj_is()` → `read_nano` / `read_crouch`；`read_spawns` 加 `mem_ok` |
| GC 根改成「一对象一句柄」+ 换场景归还 | `root_put` / `roots_clear`（10:33 那版 `System.Object` 找不到，等于没钉住）|

**顺带**：车测期间把两张图的**原生**数据都采到了（以前缺）——
沙漠要塞 `n12-17a93cfb246913e1`（12 点，navmesh 919）、新寂静村 `n180-03b43b7ee737fcdc`（180 点 / 98 边 / 105 特征，navmesh 944），
文件在部署端 `ucf_mod\vis\`。

## 6.11 闪退没修完：0x1290b1 这一类还在（2026-11-17 12:15）

11:00 修掉的是 `UnityPlayer+0x755e86` 那一类（导出撞上还没稳定的组件表）。
**`GameAssembly.dll+0x1290b1` 这一类没修掉**：它是 GC 标记阶段读到坏对象，
和 11-15 的 `docs\CRASH_FIX_2026-11-15.md` 同源（托管字段里留着已被回收的数组/对象）。

**证据**（Windows 事件日志 + 我们的 VEH 日志，都是真崩溃，不是误报）

| 时间 | 模块 + 偏移 | 说明 |
| --- | --- | --- |
| 10:22:30 / 10:23:05 / 10:35:00 | `GameAssembly.dll+0x1290b1/c1` | 修导出时机之前那三次 |
| 10:58:12 | `UnityPlayer.dll+0x755e86` | 导出时机那类，11:00 已修 |
| **11:32:49 / 11:33:08** | `GameAssembly.dll+0x1290b1` | **修完之后还在崩**（手动开局：新寂静村 / 沙漠要塞） |

现场：日志最后一行是 `[edit] naved: no edit file for …`，同一 tick 就崩；
栈上**一个 ucf_mod 帧都没有**，`ebx` 就是那个坏对象（`0xd890e098` / `0xef007898`），
`edx=0x54f` 两次完全相同。第三次会话（11:33:26–11:37:06）连进 4 张图、正常退出
（`msg=0x10`），所以不是必现。日志原件：`docs\crash_20261117_1132-1137_ucf_mod.log`。

**自动车测复现不出来**：12:07–12:10 跑 `autotest.ps1 -Targets 10,7,10,7,4,11,5,6`
（进程内 `LoadScene` 直接切图，每图 80 tick），8 次进图全 PASS。
差别在**开局路径**：手动是「大厅 → 开始比赛」，车测是「直接 LoadScene」——复现得走正常开局。

**下一步（还没做）**：在手动开局路径上复现 + 打开 WER LocalDumps 抓 minidump；
按 11-15 那份的结论，重点查“新分配的托管数组/对象在写进托管字段前没有 GC 根”的位置
（`make_guard_area` / `link_guard_areas` 的邻居数组、`build_waypoints` 的节点数组、`vis` 的 mesh）。

## 6.11 闪退真因再定位：Unity 资产存活判定（12:27）

> 10:33 那条「GC 写屏障」结论**是错的**，别再按它排查。

- 崩溃位置：`il2cpp_unity_liveness_calculation_from_root/statics`（导出 0x109340/0x109350 →
  0x12cdb0/0x12ce10）内部的 0x1290a0 —— Unity 换图后自动执行
  `Resources.UnloadUnusedAssets` 时的「托管对象存活判定」走查。真正的 GC 写屏障在
  GameAssembly+0x14cd80（`il2cpp_gc_wbarrier_set_field` 0x1084e0 跳过去）。
- 崩法：走查一个**引用数组**时（`esi`=长度、`edi-0x10`=数组），某个槽位不是对象
  （数据像 0x70007500 "pu" / 0x35cd35cd，或已释放对象的 0x08cc35c4 klass=0），
  被当成对象读 klass → 0xC0000005。
- 只有沙漠要塞(level7)/新寂静村(level10)：这两张是**仅有的两张走 `Mode_Nano6` /
  `Mode_Nano4_Terminator` 专用模式类的图**；模式对象只在房间里点「开始游戏」之后才建立，
  所以车测（进程内 LoadScene）复现不了（12:24 又验证一次：interactive + 主动
  `UnloadUnusedAssets` + settle 60 → level7/10 仍 PASS）。
- 已部署带探针的 DLL **269,717 B**（12:27 编译；`!!! walk-array` 段会直接写出数组类名、
  长度、前 8 个槽位及其类名）。下一步等一次真机闪退的日志。

## 6.12 闪退真因（已修）：purge_guard_areas 写花 SpareAreaList（13:10）

> **10:22 以来全部 6 次「沙漠要塞 / 新寂静村」闪退的共同真因。**

- 触发点：`src/navfix.c` `purge_guard_areas()` 的压缩循环
  `*(P*)((char*)items + 0x10 + w++) = o;` 在 `-O2` 下变成半宽度（16 位错位）写：
  `0x027954d8 → 0x5050f0d8`、`0x027950f0 → 0x02790279`，`_size` 不变 → 数组里留下 2 个野值。
- 证据（本机车测即可复现，插件自己打快照）：
  ```
  dbg[purge-before] [0]=027954d8 ok=1 [1]=027950f0 ok=1 [2]=02795050 ok=1
  dbg[purge-after]  [0]=5050f0d8 ok=0 [1]=02790279 ok=0 [2]=02795050 ok=1
  ```
- 两个症状：① 进图 0–1 s Unity `UnloadUnusedAssets` 存活判定走查该数组 → GameAssembly+0x1290b1 崩
  （10:22/10:23/10:35/11:32/11:33）；② 对局里 `Bot_NanoGuardArea.GetPos → SpareAreaList.Remove → IndexOf`
  对野值做 `Equals` → GameAssembly+0x3c97a 崩（12:39）。
- 只有 level7/level10 崩：只有这两张图进图时 `SpareAreaList` 非空（3 / 10 个幽灵守区）。
- 修法：显式 4 字节读；**只在 w != i 时**才 memcpy 搬；绝不原地写。
- 验证：修后 level7 槽位逐字节一致、level10 `n=10 cap=16` 一致；正常配置车测 `7,10,5,2` 全 PASS，
  日志无 `areas CORRUPT`。
- 同时修：`hud_refresh` 的 `sprintf(miss,...)` 栈溢出（200 → 320 + `snprintf`）。
- 新增常驻诊断：`areas:` 看门狗（SpareAreaList + 每个守区的 posList，坏槽位立刻 `!!! areas CORRUPT`）、
  mesh/inject 数组长度闸、`list layout` 打印、`gc_probe` 调试开关。

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
5. **进图闪退仍偶发**：`GameAssembly.dll+0x1290b1`（GC 标记读到坏对象），
   11:32/11:33 手动开局崩了两次，车测不复现 —— 详见 §6.11。
6. **同时开两个游戏实例会闪退**（2026-11-17 18:50 实测）：同一条日志里 18:50:07 / 18:50:09
   各出现一次完整 `[cfg] loaded`（两个进程），两个都崩在 `GameAssembly.dll+0x12fa26`（读 `0x9506e590` 越界）。
   随后**单实例**重跑 level7 三次（18:42 测试包版 / 18:42 正式版 / 18:52）**全部 PASS**。
   控制台已用 `game_running()` 禁用「开始游戏」，**外部脚本和手动启动不要并发**。

## 9. 下一步

- [ ] **先修 §6.11 的闪退**：`GameAssembly.dll+0x1290b1` 这一类没修掉，手动开局仍会崩；
      下一步是「手动开局复现 + WER LocalDumps 抓 dump + 复查未生根的托管字段」。
- [x] 测试包实机车测：`UCF_PACK=chain_a UCF_FP=n0-…` 跑 level7/10 两次 `pack: skip` → PASS；
      不设变量（正式版）→ 两次 `pack: (none / official nav)` → PASS（2026-11-17 18:42 / 18:52）。
- [ ] **验证本次改动**：进一次图，确认 `ucf_mod.log` 开头出现 `[cfg] ======== ucf_mod.json loaded` 与 10 行开关。
- [ ] 逐个关开关试：关 `auto_crouch` 后日志应出现 `[cfg] auto_crouch = off, skip crouch points`。
- [ ] 复验「复活后只会直走」修复。
- [ ] 复验通过后，把 `n786-…disabled_20261116_1655` 改回原名重新套用。
- [x] 进图复验 HUD：21:20 运输船通过（中文面板 + `hud: cjk font`）。
- [ ] 进暴风图复验 survey：比赛类型选「终结者模式」→ 地图选「隐藏地图 暴风」→ 开始；
      确认不再卡死，日志出现正常的 `survey: coarse ...` / `survey: spots=...`。
