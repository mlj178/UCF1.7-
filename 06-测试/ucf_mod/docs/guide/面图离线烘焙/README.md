# 面图（可走面）离线烘焙 → 运行时 NavMeshGraph

> 目标：**不进游戏**把地图几何烘成可走三角网，进图时由插件挂成 A* 的 NavMeshGraph，人机就能在上面走。
> 首张图：`nano30_storm`（原生 0 点、无面）。点图方案已撤销，这里只做面。

> **2026-11-28 起，主数据源变了**：先用人走一遍图的「跟随式采样」
> （`log/ground_samples_<图>.txt`，玩家脚下的真实碰撞面），再烘面。
> 几何（`data/geo/web/<map>.bin`）只当交叉校验 —— 实测它只覆盖游戏里量出来的
> 地面的 33%，土丘、室内地板、二楼都在缺的那部分里。详见 `规范.md` §1 / §1.1。
> （原「地面扫描」功能 2026-11-28 已整体删除，见 `规范.md` §1 末尾。）

## 1. 数据链

```text
data/geo/web/<map>.bin        UCFG v1/v2（世界坐标三角网）
      | bake_navmesh.py        地面/天花板/墙分类 -> 1 m 栅格 -> 分层可走 -> 共享顶点出三角
      v
<map>.navmesh                 UCFN v2：magic + ver + jsonLen + nv + nt + json + verts(f32x3) + tris(u32x3)
      | 复制到 data/maps/<图>/navmesh_auto.bin
      v
插件 navfix_load_navmesh()    建 Mesh -> 建 NavMeshGraph -> 挂 AstarData.graphs -> Scan()
```

## 2. 命令

```powershell
python "06-测试/ucf_mod/docs/guide/面图离线烘焙/代码/bake_navmesh.py" ^
  --map nano30_storm ^
  --user "06-测试/ucf_mod/data/maps/10_Nano30_Storm飓风危城/n0-0000000000000000.txt" ^
  --cell 1.0

Copy-Item "06-测试/ucf_mod/docs/guide/面图离线烘焙/out/nano30_storm/nano30_storm.navmesh" ^
          "06-测试/ucf_mod/data/maps/10_Nano30_Storm飓风危城/navmesh_auto.bin" -Force
```

参数：`--cell` 栅格（1.0）、`--step 0.45` 台阶、`--head 1.8` 净空、`--slope 45`、`--min-tri 12` 岛过滤。

## 3. storm 第一版（2026-11-28）

| 项 | 值 |
| --- | --- |
| 可走面积 | 13,272 m2 |
| 顶点 / 三角形 | 12,874 / 23,694 |
| 岛 | 11 片，保留 8 片 |
| 文件 | 439,020 B（UCFN v2） |
| 你的 196 个路线点落在面上 | 25 个（13%） |

**13% 的原因**：现在只烘"最低一层"。把几何按层展开后，**126/196（64%）**能对上——
剩下 34% 在导出的几何里根本没有可站的面（二楼/室内可能没导进来）。这是下一步要补的。

## 4. 插件改动

| 文件 | 改动 |
| --- | --- |
| `src/navfix.c` | 新增 `navfix_load_navmesh(path)`：读 UCFN -> 建 Mesh -> 建 NavMeshGraph -> 挂图 -> Scan |
| `src/editor.c` | 新增 `nm_load_tick()`，在 `editor_tick()` 里调用；每张图只试一次（按 AstarPath 指针判断换图） |

触发条件：`<UCF_PACK_DIR>/<图>/navmesh_auto.bin` 存在。删掉这个文件就退回原样（不改代码）。

日志关键字：`nm: loaded` / `nm: Scan threw` / `nm: 挂载失败`。

## 5. 回滚

```powershell
# 插件回退到上一版
Copy-Item "06-测试/ucf_mod/run/build/ucf_mod-20261128-0943-2310aff9b.dll" "06-测试/ucf_mod/run/build/ucf_mod.dll" -Force
# 面图关闭
Remove-Item "06-测试/ucf_mod/data/maps/10_Nano30_Storm飓风危城/navmesh_auto.bin"
```

## 6. 已知风险

1. 运行时造 Mesh 调的是 il2cpp；`.ctor` 取不到就直接放弃（已加保护，不会带着空 Mesh 去 SetVertices）。
2. `Scan()` 在托管层抛异常会被捕获，图会挂上但可能是空的——日志里 `Scan threw` 就是这个。
3. 24k 三角形对 A* 是中等规模；若卡顿，先用 `--cell 1.5` 出粗版。
4. 高度对齐：面来自场景几何，若与游戏世界差一个整体偏移，人机会贴不到面，只能进图观察。

## 7. 下一步

- [ ] 多层网格（把 64% 做实）：每层单独出三角，再焊接相邻层的顶点
- [ ] 路线结合：人机目标点从你的 196 个点里挑，面负责走位（不改 A* 图结构）
- [ ] 覆盖率验收：面图顶点到你的点的最近距离分布，>2 m 的点单独列出来

## 8. 调试记录

| 日期 | 现象 | 处理 |
| --- | --- | --- |
| 2026-11-28 | 点图方案：装上 1,800 点后人机全不动 | 撤销点图，改面图 |
| 2026-11-28 | 单层网格只覆盖路线 13% | 统计分层数据：64% 可覆盖；待做多层网格 |
| 2026-11-28 | gcc -Werror=unused-variable 拦下未用变量 | 删掉该变量再编译 |
| 2026-11-28 | 运行时 `nm: class missing int=0`（System.Int32 没取到） | 遍历程序集遇空指针改为 continue；兜底按 `mscorlib.dll` 取 Int32（插件里程序集名带 .dll） |
| 2026-11-28 | 进图直接闪退（栈里是 navfix_load_navmesh -> GameAssembly） | 改成三步走 + 复用可视化那套已验证的 RVA 建 Mesh + 数组长度校验（插件注释里记过同类堆损坏事故） |
| 2026-11-28 | `Scan threw NullReferenceException at NavmeshBase.ReplaceTile` | 图对象是 object_new 出来的，没跑 ctor，`navmeshUpdateData` / `nodeRecyclingHashBuffer` 是空。改成先调 0 参 ctor（dump 里没列，按名字找不到就遍历方法表）再填字段 |
