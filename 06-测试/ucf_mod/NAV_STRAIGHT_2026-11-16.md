# 2026-11-16 · 人机「复活后只会直直走」根因与修复（运输船）

## 0. 一句话

不是人机 AI 坏了，是插件在进图时把 A* 点图从 786 点重建成了 27 点：换数组 + 把被删点的
`nodeIndex` 写成 -1。A* 的 `PathHandler.pathNodes` 只在 `AstarPath.Awake` 分配一次，
于是寻路线程抛 `IndexOutOfRangeException` 并永久停摆 —— 之后所有 `Seeker.StartPath`
永不返回，`Bot.OnPathComplete` 不再触发，`Bot.Update` 第一行的 `Move()` 只能沿用旧方向走。

## 1. 现象

- 运输船，人机第一次出生：左右走位 / 避障 / 寻敌，正常。
- 死一次复活后：只会朝前直直走，不绕障、不追人、不开枪。

## 2. 取证（同一秒）

`ucf_mod\ucf_mod.log`（16:25:03）：
```
[nav] diag:  [0] PointGraph  +E8=43b37000 +EC=786
[edit] naved: graph rebuilt 27 nodes (kept 0, added 27, base 786)
[edit] naved: applied 843/843 edits on n786-57a46e3465c847cb (nodes 786 -> 27)
```
`Player.log`（16:25:03，与上面同一秒）：
```
IndexOutOfRangeException: Index was outside the bounds of the array.
  at Pathfinding.PointNode.Open (Pathfinding.Path path, Pathfinding.PathNode pathNode, Pathfinding.PathHandler handler)
  at Pathfinding.ABPath.CalculateStep (System.Int64 targetTick)
  at Pathfinding.PathProcessor.CalculatePathsThreaded (Pathfinding.PathHandler pathHandler)
Unhandled exception during pathfinding. Terminating.
Error : This part should never be reached.
```
上一轮 16:13 的 `Player-prev.log` 一模一样 → 可复现，不是偶发。

## 3. 机制（为什么一炸就只会直着走）

1. `PathHandler.GetPathNode(int nodeIndex)`（0x105E6790）只做 `nodeIndex >= nodes->max_length`
   的越界检查；被删点写成 `-1`（`*(int*)(nd+0x08) = -1`）后，任何还指着它的引用
   （`Bot.gNode_Nearset +0x88`、`Bot.path +0x80`）一被 `Open` 就是 0xFFFFFFFF → 抛异常。
2. `PathHandler.pathNodes` 只在 `AstarPath.Awake → InitializePathProcessor`（0x104477A0）
   按当时的节点数分配一次；`Scan()` 不重建它。所以数组换掉/变大后，新 `nodeIndex` 也会越界
   （15:50 那次 `nodes 786 -> 807` 是同一类炸点）。
3. 寻路线程死掉后 `PathProcessor` 不再取队列：`Seeker.StartPath` 的 Path 永远停在 Pending，
   `Bot.OnPathComplete` 不触发 → `bot.path` / `pathLength` / `nextPathPos +0xA0` /
   `dirToNextNode +0xAC` 全停在最后一帧的值 → `Bot.Update` 第一条 `Bot.Move()` 每帧只是沿
   同一个方向 `Player.SetMoveState` → 「直直走」。
4. 第一次出生看着正常：那些 path 是改图之前算出来的；一死一复活要重新寻路，就再也拿不到。

## 4. 修法（src/editor.c）

- **删点 = A* 软删除**：只清 walkable 位 + 摘掉活点里指向它的边；`nodes` 数组与 `nodeIndex`
  全程不动。`GetNearest` 用 `NNConstraint.Default`（constrainWalkability=1），会跳过不可走点。
- **加点 = 复用被删掉的槽位**（`nav_revive_slot` / `nav_add_node` 重写）：运行期绝不 append；
  没有空槽就拒绝并写日志（要真正扩图请走 `build_waypoints` 的 Scan 建图流程）。
- **不再写 `nodeIndex = -1`**：即使还有野指针指过来，也只是走到一个死点，不会越界。
- `nav_apply_core` 的日志改成：
  `naved: applied in place: %d disabled, %d revived, %d adds skipped (graph stays %d nodes)`

## 5. 数据侧

运输船那份「删掉游戏原本 786 点、只留 27 点」的草稿已改名停用，游戏自己的 786 点图恢复：

```
ucf_mod\nav\n786-57a46e3465c847cb.txt.disabled_20261116_1655
```

要重新套用这份草稿：把文件名改回 `n786-57a46e3465c847cb.txt` 即可（新版 DLL 下不会再炸线程）。

## 6. 产物与回滚

| 东西 | 值 |
| --- | --- |
| 新 DLL | `ucf_mod.dll` 240960 字节（2026-11-16 16:53 构建，MD5 98BC33FD…） |
| DLL 回滚 | `ucf_mod.dll.bak_20261116_1655`（原 241998 字节） |
| 源码回滚 | `src\editor.c.bak_20261116_pre_navfix`（120058 字节，与修改前一致） |
| 修改前被替换的整段源码 | `C:\Users\17242\AppData\Local\Temp\ucf_verify\old_block.txt` |

## 7. 复验步骤

1. 启动游戏 → 进运输船。
2. `ucf_mod\ucf_mod.log` 应出现 `naved: no edit file for n786-…`（草稿停用）或
   `naved: applied in place: …`（草稿改回来时）。
3. `Player.log` 里 **不应** 再出现 `Unhandled exception during pathfinding`。
4. 观察人机：死一次复活后仍应绕障/寻敌（不是直走）。

## 8. 顺带记录

- 重启能「恢复一会儿」的原因：换图会新建 `AstarPath` → `Awake` 重新分配 handler；
  只要插件再次套用那份草稿就会再炸一次。
- 本次未改动：`build_waypoints`（0 点图走 `NavGraph.Scan` 的建图流程）与守卫区/蹲守点逻辑。
