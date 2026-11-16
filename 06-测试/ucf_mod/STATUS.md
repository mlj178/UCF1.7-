# STATUS · 当前生效状态

> **唯一权威**的"现在是什么"。每次构建 / 部署 / 改运行时数据后更新本文件。
> 最后更新：2026-11-16 19:00

## 1. 跑的是哪个 DLL

| 项 | 值 |
| --- | --- |
| 部署位置 | 游戏目录 `ucf_mod\ucf_mod.dll` |
| 大小 | **246163 B**（上一版 240,960 B）|
| SHA256 | `5A4BB25D074F2CEE…` |
| 部署时间 | 2026-11-16 18:56:46 |
| 源码 | `src/cfg.c`（新）+ `plugin.c` + `navfix.c` + `editor.c` |
| 回滚点 | `ucf_mod\ucf_mod.dll.deployed_20261116_183359`（**改动前**的 240,960 B 版本）|
| 中间版本 | `…184234` / `…184255` / `…185646`（同一天几次构建，可忽略）|
| 构建方式 | `tools\build.ps1 -Deploy` → `build/build.json` 记录来源 |

> **可复现性说明**：同一份源码连续编译，字节数恒定（246,163 B）但 SHA256 每次不同。
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
| `editor` | 开 | 关掉后 Ctrl+1 无法进编辑模式 |
| `collect_only` | 关 | —— 见下 |

界面：`tools\启动控制台.bat`（CustomTkinter 窗口，勾选即写盘）。

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
| 游戏内标记编辑 | ✅ | `loaded 11 markers` |
| 自动导出路点 JSON | ✅ | 17:05 导出 132 KB |
| 网页导航编辑器 | ✅ | 俯视 + 3D，保存写 `nav/<fp>.txt` |
| 控制台开关面板 | 🆕 待验证 | `tools\启动控制台.bat` |
| Bot_JumpLink 跳台 | ❌ 未做 | |
| SP_RedBox / SP_BlueBox | ❌ 未做 | HUD 里 `缺:` 那行就是它 |

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
