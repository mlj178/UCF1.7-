# 2026-11-16 采集崩溃 + 导不出数据 —— 定位与修复

## 1. 两个现象

| # | 现象 | 后果 |
| --- | --- | --- |
| A | 补采了几张图，但 `ucf_mod/vis/` 里只有几个 12/18/2 点的老图，真正的**大图（3063 点 / 5584 边）没有落盘** | 白跑一趟，数据丢了 |
| B | 采集中弹出 `Microsoft Visual C++ Runtime Library — Runtime Error!` | 游戏直接退出 |

## 2. 证据链（`ucf_mod/ucf_mod.log`，2026-11-16 12:51~12:54）

```
12:51:34  vis ON (layers=0x1F labels=34)          <- 可视化开着
12:52:14  vis layers=0x1E (toggled 0x1)          <- A 层被关掉（Ctrl+Shift+1）
12:52:16  collect-only ON
12:52:22  vis layers=0x1F (toggled 0x1)          <- A 层又打开
12:52:38  collect-only OFF
          -> 这一轮写出的 map_n0-...json：nodes=0 / edges=0 / features=0（假的）
12:53:53  [nav] diag: PointGraph +E8=2192e000 +EC=3063   <- 真正的大图，3063 个点
12:53:54  auto-export: graph stable at 3063 nodes, writing JSON
12:53:54  vis: fp=n0-0000000000000000 already collected, skip duplicate   <- 被当成重复，跳过
12:54:10  naved: no edit file for n12-17a93cfb246913e1
12:54:10  Windows Application Error: UnityCrossFire.exe, 异常代码 e06d7363, 模块 KERNELBASE.dll
```

`e06d7363` = MSVC 的 C++ 异常魔数（`0xE06D7363`）。它不是普通的访问违例，而是
**一个 C++/托管异常没有被任何人捕获，最后走到 CRT 的 abort**，所以弹的是那个 "requested the Runtime to terminate" 框。

## 3. 根因

### A. 导出的数据是上一个场景的残留（丢数据的直接原因）

`editor.c` 里 `vis_export()` 开头原来是：

```c
if (!g_visOn) {                        /* 可视化关着才重读 */
  if (g_collectOnly) collect_read();
  else { vis_rebuild(); vis_show(0); }
}
... sprintf(fp, "n%d-%016llx", g_vnN, xr);   /* 用的是内存里剩下的 g_vn */
```

于是只要**可视化是开着的**（Ctrl+V 开过一次就一直开着），导出就完全不重读数据：
进图时 `vis_scene_reset()` 刚把 `g_vnN` 清 0 → 写出 `n0-0000000000000000` 的"0 点"文件，
并且顺手写了 `vis\_seen_n0-...` 标记。下一张图（3063 点）算出的指纹也是 `n0-...`（同样读不到），
于是命中标记、按"已采集过"跳过 —— 真数据就这么没了。

同一段代码还有个隐患：`read_nav()` 开头有 `if (!(g_lay & LAY_A)) return;`，
也就是说 A 层关着的时候（12:52:14 那一下）导出同样会少掉全部路点。

### B. 自动导出会在进图瞬间建 UGUI（崩溃的原因）

`vis_rebuild()` 除了读数据，还会建 Mesh、材质、**UGUI Text 标签**。
`auto_export_tick()` 是在 `editor_tick()` 最前面调用的，图一稳定就导出 —— 正好落在场景加载/资源卸载期间。
历史上几次崩溃都出现在这个窗口：il2cpp 的托管异常从游戏代码一路穿过我们这层没有异常处理的 C 帧，
没人接住 → CRT abort → 就是那张 `Runtime Error` 对话框。

## 4. 改了什么（`ucf_mod/src/editor.c`，已重新编译进 `ucf_mod.dll`）

| # | 改动 | 作用 |
| --- | --- | --- |
| 1 | 新增 `g_exporting`；`read_nav/read_nano/read_crouch/read_guardareas/read_spawns/read_jump/read_tags` 改成 `(!(g_lay & LAY_X) && !g_exporting)` | 导出时**忽略图层开关**，五层全读，不会因为关了某层就少导 |
| 2 | `vis_export()` 开头固定走 `g_exporting=1; collect_read(); g_exporting=0;` | 每次导出都重新读一遍，**不再用上一个场景的残留**；也不再建 Mesh/Text |
| 3 | `if (g_vnN <= 0) { elog("export skipped: read 0 nodes ..."); return; }` | 读不到点就**不写空文件、不写 `_seen` 标记**，不会再出现 n0 假文件把真数据顶掉 |
| 4 | `nav_apply_all()`：`if (ok) nav_refresh(g);`（原来无条件调） | 没改动就不调 `RebuildNodeLookup()`（il2cpp 方法调用，能省则省）；`nav_reapply()` 里重复的那次也去掉了 |
| 5 | `nm_auto_tick()` 成功后不再 `hud_refresh()` | 刚进图就 set UGUI 文本是崩溃高发点，HUD 下一 tick 自己会刷 |

编译（和原来一样的参数）：

```powershell
& 'D:/Program Files/mingw32/bin/gcc.exe' -O2 -shared -o ucf_mod_new.dll plugin.c navfix.c editor.c -luser32 -lgdi32 -static-libgcc
```

部署情况：

| 项 | 值 |
| --- | --- |
| 新 `ucf_mod.dll` | 236600 字节，2026-11-16 13:09 |
| sha256 | `79BE5817B45B390730DE1E235755385C5D2FDC3401E24A1E782AC65117CE0461` |
| 修复前备份 | `ucf_mod.dll.bak_20261116_pre_fix`（235577 字节，20:19 那版） |
| 回滚 | 关掉游戏 → 把 `ucf_mod.dll.bak_20261116_pre_fix` 复制回 `ucf_mod.dll` |

## 5. 事故说明：源码被我截断又找回

定位过程中我用"整文件读→改→整文件写"的方式改 `editor.c`，读取时只读了前 2000 行，写回把文件截成了 51 KB。
**已完整恢复**：`%LOCALAPPDATA%\Temp\ucf_verify\build_noprobe\editor.c` 里放着同样 107500 字节的构建副本，
比对前 1448 行与截断文件完全一致（差异只有我自己加的那几行补丁），已回填 `ucf_mod\src\editor.c`。

唯一无法找回的：20:19 那版 DLL 比这份源码多两条**纯日志**（`hb: collect-only ...` 心跳、`vis: spawn groups` 统计），
它们对应的源码行没留在任何副本里。重编后的 DLL 不再打印这两行，**功能不受影响**。

> 教训：改大文件只用"按位置替换"（edit），不要整读整写。

## 6. 现在怎么把缺的图补齐

1. **重启游戏**（新 DLL 才会加载；进图后在 `ucf_mod.log` 里能看到 `plugin` 版本行）。
2. **关掉可视化**：如果 HUD 上 `Ctrl+V` 是开的，按一下关掉（新版已经不受它影响，但少一层风险总是好的）。
3. `Ctrl+Shift+X` 开采集模式（会写 `ucf_mod\collect.flag`）。
4. 把缺的图各进一次，停 2~3 秒（看日志出现 `auto-export: graph stable at N nodes` 就成）。
5. 退出游戏，跑：

```
cd ucf_mod\tools
python organize_maps.py --archive
```

6. 检查 `ucf_mod\maps\INDEX.md`：对应行从 `待采集` 变成节点数就算成功。

**怎么判断这次导出是真的**：打开 `ucf_mod\vis\map_<指纹>_<时间>.json`，看 `map.node_count` ——
0 就是假的（新版不会再写出这种文件）；另外日志里如果出现 `vis: export skipped: read 0 nodes`，
说明那一刻点图确实没读到（通常是真的在切场景），等图稳定再导出即可。

上次丢掉的是一张 **3063 点 / 5584 边、navmesh 683 顶点**的图（指纹 `n3063-b04b59b2593bfae4`）；
它的 navmesh 还在 `ucf_mod\vis\navmesh_nm683-5a28f3e9cb95f718.bin`，但点图需要重新进图采一次。

---

## 追加（2026-11-16 13:35）：从游戏文件里直接读路点，以及几个新查出来的事实

### 1. 路点其实是场景里的 GameObject
每张图的 A* 设置（场景文件里嵌的一段 base64 zip）写明：PointGraph，searchTag = "WayPoint"。
也就是说 **节点 = 场景里 tag 为 WayPoint 的物体**（tag id 20022），位置就是它的 world position。
用 UnityPy 读场景文件（level1..level11）能直接数出来：

| 关卡 | 场景里的 WayPoint 物体 | 游戏内指纹 | 场景算出的指纹 | 结论 |
| --- | --- | --- | --- | --- |
| level1 运输船 | 786 | n786-57a46e3465c847cb | n786-57a46e3465c847cb | **完全一致** |
| level3 椰岛之巅 | 2 | n2-24a647eff15d6ca4 | n2-24a647eff15d6ca4 | **完全一致** |
| level5 竞技场 | 17 | n17-f352f68820fae99c | n17-5ffbdd39970c91fb | 点数同、坐标不同 |
| level8 生化酒店 | 3063（另有 7 个未激活） | n3063-b04b59b2593bfae4 | n3063-504ea5aa2f063f55 | 点数同、坐标不同 |
| level10 新寂静村 | 180 | n180-03b43b7ee737fcdc | n180-70d2db6271baba8d | 点数同、坐标不同 |
| level7 沙漠要塞 | 8 | 未记录 | n8-8633238e84711804 | 待游戏确认 |
| level2/4/6/9/11 | 0 | — | n0 | 场景里本来就没有 WayPoint |

结论：
* 运输船、椰岛之巅可以**完全离线**还原（指纹逐位一致，不用进游戏）。
* 竞技场/生化酒店/新寂静村：点数一致但坐标不一致 —— 进图后游戏自己挪过这些点，只能进图采。
* **胜利广场（level4）场景里根本没有 PointGraph**（只有 NavMeshGraph），永远不会采到路点；「待采集」这个状态对它是错的。
* level11 死亡擂台同样只有 NavMeshGraph。

### 2. 02/06/11 的老数据很可能是大厅残留
level2、level6 场景里的 PointGraph 是 maxDistance: 0 / mask: 0（连不出任何边），
但它们的导出却有 6 / 9 条边；level11 场景里连 PointGraph 都没有，导出却有 24 条边。
=> 这三份「12/18/17 点」的样本不是地图数据，是菜单/大厅场景采到的。用之前先复核。

### 3. 自动化改动
* 插件 HUD 现在直接显示最近 3 条日志 + 最近一次导出结果（Ctrl+M 开关）。
* navserver.py 新增 /api/log?n=200，并且后台线程盯着 vis/：一有新导出、静止 6 秒后**自动跑 organize_maps.py --archive**，不用再手动执行。
* organize_maps.py：新增 KEEP_FP，像椰岛之巅这种只有 2 个点的小图不再被 MIN_NODES=8 丢掉。
