# 面图（可走面）离线烘焙 → 运行时

> 目标：把"游戏里人真正能站的地面"变成可走三角网 + 点图，进图后由插件加载，
> 人机按它走。首张图：`nano30_storm`（原生 0 点、无面）。

**2026-11-28 定版**：主数据源只有一个是可信的 —— **玩家脚下的碰撞地面**
（控制台「开发者选项 → 跟随式可通行性采样」，人走一圈）。其余数据源全部降级为交叉校验，
失败的方案见第 5 节。详细规范与实测数据在 [`规范.md`](规范.md)。

## 1. 数据链（现役，唯一链路）

```text
控制台「跟随式采样」 → 人走一圈
      v
log/ground_samples_<地图>.txt      每行 x z y（1 m 格，玩家脚下打到的碰撞面）
      | 代码/sweep2navmesh.py      逐格出面（每格自己一个高度，不插值）
      v
<map>.navmesh                      UCFN v2：magic + ver + jsonLen + nv + nt + json + verts + tris
      | 复制到 data/maps/<图>/navmesh.bin
      v
插件 nm_load_tick()                读 UCFN → 建 Mesh → 建 NavMeshGraph（**只显示**，不参与寻路）
      |
      | 代码/mesh2points.py        面 → 3 m 间距铺点 → 同层连边 → 与手摆点桥接
      v
data/maps/<图>/<fp>.txt            grow 包：node add / edge add / jump add（跳链原样照抄）
      v
插件 nav_apply_grow()              进图后建点 → 人机重绑 → **人机按它走**
```

要点：**面图负责显示和"地面真值"，人机实际走的是面图铺出来的点图**。
（A* 的 NavMeshGraph 直接接管寻路那条路还没打通，见 §6。）

## 2. 命令

```powershell
# ① 采样数据 → 面
python "06-测试/ucf_mod/docs/guide/面图离线烘焙/代码/sweep2navmesh.py" ^
  --sweep "06-测试/ucf_mod/log/ground_samples_10_Nano30_Storm飓风危城.txt" ^
  --out   "06-测试/ucf_mod/docs/guide/面图离线烘焙/out/storm_follow_v2.navmesh" ^
  --map nano30_storm

# ② 面 → 点图（--user 填你手摆的路线包，跳链会原样带上）
python "06-测试/ucf_mod/docs/guide/面图离线烘焙/代码/mesh2points.py" ^
  --navmesh "06-测试/ucf_mod/docs/guide/面图离线烘焙/out/storm_follow_v2.navmesh" ^
  --user "06-测试/ucf_mod/data/maps/10_Nano30_Storm飓风危城/n0-0000000000000000.txt.bak-route196" ^
  --gap 3.0 --dist 3.4 --bridge 3.0 --bridge-dy 1.8 ^
  --fp n0-0000000000000000 ^
  --out "06-测试/ucf_mod/docs/guide/面图离线烘焙/out/storm_pack.txt"

# ③ 装（先备份）
Copy-Item <新面> "06-测试/ucf_mod/data/maps/10_Nano30_Storm飓风危城/navmesh.bin" -Force
Copy-Item <新包> "06-测试/ucf_mod/data/maps/10_Nano30_Storm飓风危城/n0-0000000000000000.txt" -Force
```

`sweep2navmesh.py` 会自动认格子边长（`--cell` > 文件头 `cell=` > 从数据推），
跟随采样是 1.00 m；`--max-rise` 默认 `1.2 × 格子`（≈50°），别用老默认 0.9（会砍掉 31° 以上的坡）。

## 3. storm 现状（2026-11-28）

| 项 | 值 |
| --- | --- |
| 采样 | 6,238 格 / 5,639 m²，8 邻域最大块 99.9%，y −0.28 ~ 15.42 |
| 面图 `navmesh.bin` | 6,400 顶点 / 11,026 三角 / 204 KB |
| 点图 `n0-….txt` | 768 点 / 2,000 边行 / 21 跳（用户手工编辑后） |
| 待装 v5 | 737 点（删 31 孤立点）+ 补 8 桥 → 主块 95%、孤立点 0（见 `规范.md` §10.5） |

## 4. 插件改动

| 文件 | 改动 |
| --- | --- |
| `src/editor.c` | `nm_load_tick()`：读 `<图>/navmesh.bin`（兼容老名 `navmesh_auto.bin`）→ 建 Mesh → 建 NavMeshGraph（detached，只显示） |
| `src/editor.c` | `gf_*`：跟随式采样（每 250 ms、半径 8 m、1 m 格、脚 +1.2 m 向下 6 m）+ 游戏内可视化 |
| `src/editor.c` | `nav_apply_grow()` + `bot_rebind_after_apply()`：点图应用后人机重绑（否则路径引用变野指针） |
| `app/tabs/dev/tab.py` | 「开发者选项」页新增跟随采样卡片（开始/停止/计数/打开 log） |

## 5. 历史方案（**全部废弃，代码与产物已删除**）

| 方案 | 为什么废 |
| --- | --- |
| 导出视觉几何 → Recast/Unity 烘面 | 只覆盖游戏自扫地面的 **33%**，48 岛；几何不是碰撞面（Unity 工程 `unity-navmesh/` 已删） |
| AssetBundle 加载面图 | 游戏里崩在 `LoadFromFile`（`navmesh_bundle` 与 C 分支已删） |
| 从天上扫整图（`ground_sweep/ground_low`） | 4 m 以上室内地板、土丘侧面打不到；仅留作交叉校验 |
| 运行期 append 节点 / 8 个点图变体（`*_grow.txt`） | 超过进图节点数 → `PathHandler` 越界 → 寻路线程死 |
| `PointGraph.Scan()` | 把图清成 0 节点，NRE 6,104 |

## 6. 已知限制

1. **面图不参与寻路**：现在只负责显示 + 当点图的地基。让 A* 的 NavMeshGraph 直接接管寻路还没验证通。
2. **点图会碎**：手工删点容易删到割点（实测 80 个点把 714 的主块切成 379+166 两块）；
   改完建议跑一次连通性检查（`规范.md` §10.4）。
3. **同一 x,z 只记一层**：高度表本质如此，屋顶正下方已采过的街面会挡住屋顶采样。
4. **屋顶/高层要自己走上去**：玩家没站过的层采不到，只能补走或补跳链。

## 7. 回滚

```powershell
# 面图关掉
Remove-Item "06-测试/ucf_mod/data/maps/10_Nano30_Storm飓风危城/navmesh.bin"
# 点图退回备份
Copy-Item "…\n0-0000000000000000.txt.bak-route196" "…\n0-0000000000000000.txt" -Force
```
