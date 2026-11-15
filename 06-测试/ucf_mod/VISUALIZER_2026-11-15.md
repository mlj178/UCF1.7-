# 导航可视化编辑器（2026-11-15 第二轮）

目标：把 A–E 五层导航数据在游戏里**画出来**，能分层开关、带中文名+坐标标签、能导出。
全部代码在 `src/editor.c`（可视化模块）+ `src/navfix.c`（导出接口 / 快捷键路由）。

## 1. 快捷键

| 键 | 作用 |
| --- | --- |
| **Ctrl+V** | 可视化总开关（第一次开会现场读图并建网格，约 0.2 s） |
| **Ctrl+Shift+1** | A 层：路点 / 连接边 / 跳跃链 / 标签区 |
| **Ctrl+Shift+2** | B 层：蹲守点 / 守卫点 / 守卫区域 |
| **Ctrl+Shift+3** | C 层：幽灵守区 / 幽灵守点 / 入口·撤离·邻区连线 |
| **Ctrl+Shift+4** | D 层：六类出生点 |
| **Ctrl+Shift+5** | E 层：模式信息（目前只在左上角状态栏） |
| **Ctrl+Shift+L** | 文字标签：关闭（默认）→ 近距(35 m) → 全部 |
| **Ctrl+E** | 导出 `vis/<地图名>_<日期时间>.json`（格式见 `NAVGRAPH_FORMAT.md`） |
| **Ctrl+H** | 显示/隐藏底部快捷键面板 |
| **Delete** | 删除准星最近的手工标记（不再需要 Ctrl） |
| Ctrl+1 / 2 / 4 / 5 / 6 / 7 / 8 / 9 / 0 | 原有编辑功能（编辑模式 / 蹲守点 / 幽灵守区 / 撤销 / 保存 / 重载 / 阵营 / 状态 / 标记显示） |

> 编辑模式未打开时，Ctrl+V / Ctrl+E / Ctrl+H / Delete 仍然可用。

## 2. 画面里画了什么

| 层 | 元素 | 颜色 | 形状 |
| --- | --- | --- | --- |
| A | A* 路点（tag=0） | 淡蓝白 | 14 cm 实心方块 |
| A | 带 tag 的路点 | 橙 | 同上 |
| A | 不可走路点 | 红 | 同上 |
| A | 连接边（PointNode.connections） | 深蓝 | 5 cm 双面线 |
| A | Bot_JumpLink | 黄 | 10 cm 线段 |
| A | PointNodeTagModifier 点 | 橙 | 0.9 m 线框盒 |
| B | 蹲守点（SpareList_BL/GR） | 红 | 方块 |
| B | 守卫点（Bot_GuardPos） | 橙 | 方块 |
| B | 守卫区域（Bot_GuardArea） | 紫 | 1.8 m 线框 |
| C | 幽灵守区（SpareAreaList） | 绿 | 2.4 m 线框 |
| C | 幽灵守点（posList） | 青 | 方块 |
| C | 入口 / 撤离点 / 邻区 | 粉 / 白 | 连线 |
| D | 保卫者出生 / 幽灵出生 / 中立点 / 补给箱 / 红箱 / 蓝箱 | 蓝 / 红 / 灰 / 金 / 粉 / 青 | 0.9 m 竖条 |

标签格式：`中文名#序号` 换行 `x,y,z`（幽灵守点多一行 `safe=N`）。
标签用 UGUI Text 挂在屏幕空间 Canvas（sortingOrder 31000）上，每 250 ms 跟随一次世界坐标，
只有进入视野（z>0 且在屏幕内）才显示。

## 3. 数据来源（都是从运行中的游戏直接读，不是我们自己的扫描表）

| 数据 | 位置 |
| --- | --- |
| 路点数组 | `PointGraph.nodes` +0xE8 / `nodeCount` +0xEC |
| 节点坐标 / tag / 可走 / 代价 | `GraphNode`: position Int3 +0x14、flags +0xC（tag=bit19..23）、penalty +0x10 |
| 连接边 | `PointNode.connections` +0x20（`{GraphNode*, uint cost, byte}`，步长 12） |
| 跳跃链 | `Bot_JumpLink.links` +0x24（步长 28，endTransform 在 +0） |
| 标签区 | `PointNodeTagModifier.points` +0x20 / `pathTag` +0x24 |
| 幽灵守区 | 静态 `Bot_NanoGuardArea.SpareAreaList`；entrancePos +0xC、posList +0x10、neighborAreas +0x14、escapeAreas +0x18、escapePos +0x1C |
| 幽灵守点 | `Bot_NanoGuardPos`：area +0xC、zoomPos +0x10、safety +0x1C |
| 蹲守点 | `Bot_CrouchPos.SpareList_BL`(+0) / `SpareList_GR`(+4) |
| 出生点 | `MapManager`：SP_BL +0x10、SP_GR +0x14、SP_Netural +0x18、SP_SupplyBox +0x1C、SP_RedBox +0x20、SP_BlueBox +0x24（每项 16 字节 {Vector3; float}） |

渲染方式：每个「层+颜色」合成**一个 Mesh**（MeshFilter + MeshRenderer），
顶点在 C 里拼好一次性上传，双面三角形；实测 10 个 Mesh、约 2 万顶点、
一次建好后每帧 0 额外 CPU（只有标签在动）。

## 4. 导出

`Ctrl+E` 写 `ucf_mod/vis/<地图名>_YYYYMMDD_HHMMSS.json`。
**格式定义已独立成 `NAVGRAPH_FORMAT.md`（v1）**，下面是结构速览：

```json
{
  "format": "ucf-navgraph", "version": 1,
  "map": {"name":"...","fingerprint":"n694-...","source":"ours|game",
          "node_count":694,"bbox":[[x,y,z],[x,y,z]]},
  "counts": {"nodes":694,"edges":1138,"nano_area":41,"nano_pos":60,"crouch":158,"guard":0,"spawn":85},
  "nodes":  [{"id":"3f0c9ab4...","p":[x,y,z],"tag":0,"walk":1,"pen":0}, ...],
  "edges":  [["idA","idB"], ...],
  "features":[{"id":"...","kind":"nano_area","name":"幽灵守区","aux":16,"p":[x,y,z]}, ...],
  "lines": {"nano_neighbor":[...],"entrance_escape":[...],"jump":[...]}
}
```

kind 用字符串（`nano_area` / `nano_pos` / `crouch` / `guard` / `guard_area` / `spawn` / `jump` / `tag_region`）；
节点不再用索引，而是**由坐标算出的 64 位 id**，这样重新扫描后编辑仍然对得上。详见 `NAVGRAPH_FORMAT.md`。

## 5. 这轮踩到并修掉的坑（都是真机崩溃，逐条验证过）

1. **il2cpp 进程内 assembly 数组尾部未初始化**：`il2cpp_domain_get_assemblies` 返回 n=51，但 47 之后是空/垃圾指针，
   对垃圾指针调 `il2cpp_assembly_get_image` 直接崩在 GameAssembly。
   → 所有 `find_image/find_class` 循环改为遇到空指针就 `break`。
2. **System.Int32 在 corelib 里，扫描扫不到**（被上面的 break 挡住）。
   → 改用 `il2cpp_domain_assembly_open("mscorlib.dll")` 定向取 Image 再 `class_from_name`。
3. **材质原型被 `Resources.UnloadUnusedAssets` 回收**：缓存的原型 Material 没有任何引用，
   地图加载完后被卸载，`new Material(proto)` 崩在 UnityPlayer。
   → 材质改成每次 `Shader.Find("Universal Render Pipeline/Unlit")` 现建，并对建好的材质加 `il2cpp_gchandle_new` 根保护。
4. **Component 当 GameObject 用**：给 Text 组件调 `GameObject.get_transform`，出图后 1 帧崩。
   → 统一用 `Component.get_transform`（0x32CF40）。
5. **WorldToScreenPoint 的 `_Injected` 变体签名不对**（返回乱数 x=-35280）。
   → 改用返回值版本 `Camera.WorldToScreenPoint(Vector3)`（0x327F70），坐标正常。
6. 编辑器初始化原本在**切图时**才第一次跑，会撞上场景加载期；改成主线程第一个 tick 预热。
7. **可视化只画出过半数的边（2026-11-15 17:40 发现）**：bs_line() 里
   if (|d.y| < 0.9*len) u = (0, -d.z, d.y) 在 d.y==0 且 d.z==0（水平、沿 X 的边）时得到零向量，
   ul < 1e-6 直接 return，这些边被静默丢弃。实测运输船图 786 点 / 1391 边，其中纯 X 边 669 条，
   **只画出 1391-669=722 条**；日志 vis_edges items=1391 verts=5776 正好 = 722*8，
   而节点 786*24=18864 完全正确 —— 所以画面上路点成了「一排排平行横线」，看不到十字网格。
   → ul 退化时回退到另一组基 u = (-d.z, 0, d.x)；顺带修好了 bs_wbox 线框盒缺边的问题。
   **注意：数据（导出 JSON）一直是对的，坏的只是画线。**

## 6. 还没补上的数据（可视化里能直接看到它们空着）

| 数据 | 现状 | 在可视化里的表现 |
| --- | --- | --- |
| Bot_JumpLink | 0 | A 层没有黄色跳链，跨沟区域仍然断开 |
| Bot_GuardPos | 0 | B 层只有蹲守点，没有守卫点 |
| SP_Netural / SP_RedBox / SP_BlueBox | null | D 层显示 `缺:中立点 红箱 蓝箱` |
| PointNodeTagModifier | 0 | A 层没有标签区 |

## 7. 实机证据

- `[edit] vis: nodes=694 edges=1138 labels=344 (area=41 pos=60 crouch=158 guard=0 spawn=85 jump=0 tag=0)`
- `[edit] vis ON (layers=0x1F labels=344)`；切换图层：`vis layers=0x1E (toggled 0x1)` → `nodes=0 edges=0`
- `[edit] vis: exported 694 nodes, 1132 edges, 335 features -> ...\vis\graph_20261115_115359.json`（Node 校验 JSON 通过）
- 截图：`screenshots/vis_hud_hotkeys.png`（HUD+快捷键面板）、`screenshots/vis_ingame_layers.png`（游戏内五层叠加）
