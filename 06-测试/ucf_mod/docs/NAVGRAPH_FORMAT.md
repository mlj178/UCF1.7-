# 导航数据文件格式 v1（ucf-navgraph）

> 面向"离线导航数据编辑器 + 游戏内薄插件"这套工具链的数据契约。
> 游戏侧只负责扫描/导出和应用，编辑全部发生在桌面端；这份文件就是两者之间唯一的语言。
> 改格式必须同时改 `version`，旧版本文件必须仍能被新编辑器打开。

## 0. 文件放在哪

| 目录 | 内容 | 谁写 | 规则 |
| --- | --- | --- | --- |
| `ucf_mod\vis\` | 游戏内 `Ctrl+E` 导出的原始扫描 | 插件 | 只增不改，文件名带时间戳，用来对比"这次扫描和上次差在哪" |
| `ucf_mod\nav\` | 编辑后的权威数据 | 桌面编辑器 | 一张地图一个文件 `<map>.json`，可重复覆盖，建议进版本库 |

原始扫描不是权威数据：游戏每次进图都会重扫，节点索引会变，所以任何长期保存的编辑都必须建立在下面的"稳定 id"上。

## 1. 顶层结构

```json
{
  "format": "ucf-navgraph",
  "version": 1,
  "generated": "2026-11-15 13:20:00",
  "plugin": "ucf_mod 2026-11-15",
  "map": {
    "name": "xxx_minimap",
    "fingerprint": "n694-3f0c9ab41d2e7711",
    "source": "ours",
    "node_count": 694,
    "bbox": [[-118.4, -12.6, -121.0], [122.0, 14.2, 118.7]]
  },
  "counts": { "nodes": 694, "edges": 1138, "features": 335,
              "nano_area": 41, "nano_pos": 60, "crouch": 158,
              "guard": 0, "spawn": 85, "jump": 0, "tag": 0 },
  "nodes":    [ ],
  "edges":    [ ],
  "features": [ ],
  "lines":    { "nano_neighbor": [], "entrance_escape": [], "jump": [] }
}
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `format` | string | 固定 `ucf-navgraph`，用来拒绝别的 JSON |
| `version` | int | 契约版本，当前 1 |
| `generated` | string | 扫描时刻（本地时间） |
| `plugin` | string | 产出它的插件版本，出 bug 时先看这个 |
| `map.name` | string | 小地图贴图名（清洗成 `[A-Za-z0-9_-]`），拿不到就是空串 |
| `map.fingerprint` | string | `n<节点数>-<16 位十六进制>`，见 §3 |
| `map.source` | string | `ours` = 点由我们的 build_waypoints 生成（可改点位）；`game` = 游戏自己扫的（只可改边/标签/可走性） |
| `map.node_count` | int | 冗余字段，不解析 nodes 也能校验 |
| `map.bbox` | [[x,y,z],[x,y,z]] | 节点包围盒，防"补丁打到别的图上"的第二道保险 |
| `counts` | object | 各类计数，纯为人看 |

## 2. 节点 id：为什么不能用索引

A* 每次 Scan 之后节点顺序会重排，今天的 `#137` 明天可能是 `#402`。
所以每个节点有一个由位置算出来的 64 位 id：把坐标按 1 cm 量化，做 FNV-1a 64 位哈希。

关键细节：哈希的是打印出来的两位小数，不是原始 float。这样编辑器在任何平台上都能由坐标重算出同一个 id。

C 侧（插件）：

```c
int qcm(float v) { char b[32]; sprintf(b, "%.2f", v);          /* 先格式化 */
                   return (int)floorf((float)atof(b) * 100.0f + 0.5f); }
/* qx = qcm(x), qy = qcm(y), qz = qcm(z)，每个当作 uint32 小端写 4 个字节 */
unsigned long long h = 14695981039346656037ULL;
for each q in (seed, qx, qy, qz):
    for i in 0..3: h = (h ^ ((q >> (8*i)) & 0xFF)) * 1099511628211ULL;
```

JS 侧（编辑器，必须逐位等价）：

```js
const MASK = (1n << 64n) - 1n;
function fnvU32(h, q) {
  q = q >>> 0;                       // 与 C 的 (unsigned int) 强转等价
  for (let i = 0; i < 4; i++) h = ((h ^ BigInt((q >>> (i * 8)) & 0xff)) * 1099511628211n) & MASK;
  return h;
}
function nodeId(p, seed = 0) {
  const q = (v) => Math.floor(Number(v.toFixed(2)) * 100 + 0.5);
  let h = 14695981039346656037n;
  h = fnvU32(h, seed); h = fnvU32(h, q(p[0])); h = fnvU32(h, q(p[1])); h = fnvU32(h, q(p[2]));
  return h.toString(16).padStart(16, '0');
}
```

`seed` 的用途：节点用 0；feature 用 `kind*100 + aux`，这样"同一位置上的不同种类对象"不会撞 id。

## 3. 地图指纹

`fingerprint = "n" + node_count + "-" + hex(XOR of nodeId(p, 0) over all nodes)`

用异或而不是顺序哈希，是为了与节点顺序无关：同一次扫描换序、或扫描器实现微调，指纹都不变。
指纹变了就说明地图或扫描参数真的变了，此时应用旧补丁必须拒绝——这是防"把 A 图补丁打到 B 图"的最后一道闸。

## 4. nodes

```json
{ "id": "3f0c9ab41d2e7711", "p": [12.34, -1.28, -87.55], "tag": 0, "walk": 1, "pen": 0 }
```

| 字段 | 类型 | 来源 | 可编辑 |
| --- | --- | --- | --- |
| `id` | 16 位 hex | 位置哈希 | 只读（移动点 = 换 id） |
| `p` | [x,y,z] 米 | `GraphNode.position` × 0.001 | 仅 `source=ours` |
| `tag` | 0–31 | `flags` bit19–23 | 是 |
| `walk` | 0/1 | `flags` bit0 | 是（0 = 不可走，等价于软删除） |
| `pen` | uint | `GraphNode.penalty` | 是（越大越不想走） |

## 5. edges

`[["3f0c9ab41d2e7711","a71b0c93ff12ee04"], ...]`

无向、无重复（导出时只保留 `i < j` 的一侧）。补丁里出现的边 = 要建立的连接；`remove_edges` 里出现的 = 要断开的连接。

## 6. features

```json
{ "id": "...", "kind": "spawn", "name": "保卫者出生", "aux": 0, "p": [0,0,0] }
```

| kind | 含义 | aux |
| --- | --- | --- |
| `nano_area` | 生化幽灵守区 `Bot_NanoGuardArea` | 索引 |
| `nano_pos` | 幽灵守点 `Bot_NanoGuardPos` | `_safety` |
| `crouch` | 人类蹲守点 `Bot_CrouchPos` | 0=BL 1=GR |
| `guard` | 守卫点 `Bot_GuardPos` | 索引 |
| `guard_area` | 守卫区域 `Bot_GuardArea` | 索引 |
| `spawn` | 出生点 | 0 BL / 1 GR / 2 中立 / 3 补给箱 / 4 红箱 / 5 蓝箱 |
| `jump` | 跳跃链接 `Bot_JumpLink` | 索引 |
| `tag_region` | `PointNodeTagModifier` 标签区 | tag 值 |

## 7. lines

纯展示用的连线，编辑器不把它们当数据（由 features 推导），保留是为了让人核对入口/撤离/邻居关系对不对：

| 键 | 内容 |
| --- | --- |
| `nano_neighbor` | 守区中心 → 邻接守区中心 |
| `entrance_escape` | 守区中心 → 入口点 / 撤离点 / 可撤离邻区 |
| `jump` | 跳跃链接的起终点 |

## 8. 编辑文件（nav/<map>.json）与原始扫描的区别

编辑文件在原格式上加一个 `edits` 段，其余字段是"扫描时的快照"，用来校验：

```json
{
  "format": "ucf-navgraph", "version": 1,
  "map": { "name": "x", "fingerprint": "n694-...", "source": "game" },
  "edits": {
    "remove_edges": [["idA","idB"]],
    "add_edges":    [["idA","idB"]],
    "set_nodes":    [{ "id": "idA", "tag": 3, "walk": 0, "pen": 400 }],
    "add_nodes":    [{ "p": [1,2,3], "tag": 0, "walk": 1, "pen": 0 }],
    "remove_nodes": ["idX"],
    "features_add": [{ "kind": "crouch", "aux": 0, "p": [0,0,0] }],
    "features_remove": ["idY"]
  }
}
```

## 9. 应用规则（游戏侧）

1. 时机：必须在游戏 Scan + ConnectNodes 之后（现有 nav_tick 已经在监测节点数，复用它）。
2. 防呆：fingerprint 或 node_count 不匹配 → 拒绝应用，日志写 `apply rejected: fingerprint mismatch`，绝不猜。
3. 幂等：连续应用两次结果相同；add_edges 前先查重，remove_edges 前先查存在。
4. 原子：先算好全部目标状态再一次性改，避免中途异常留下半套补丁。
5. 可关闭：`Ctrl+Shift+P` 暂停应用（调试用），日志明确写出"已应用 N 条"。

## 10. 校验规则（编辑器必须实现）

| 编号 | 规则 | 处理 |
| --- | --- | --- |
| V1 | 节点 `walk=0` 但仍被边引用 | 警告：这些边会被忽略 |
| V2 | 孤立节点（无任何边） | 标红并列出来（幽灵卡住的直接判据） |
| V3 | 连通分量 > 1 | 列出各分量大小，标出"出生点所在分量" |
| V4 | 出生点不在最大分量内 | 危险，红色 |
| V5 | 边两端距离 > 8 m | 可疑，通常意味着穿墙或跨图 |
| V6 | 特征点悬空（附近 1.5 m 内无节点） | 警告，AI 可能到不了 |

## 11. 版本策略

- 新增字段：不升版本，老编辑器忽略未知字段即可（必须容忍未知字段）。
- 改语义 / 删字段：version +1，编辑器同时支持读旧版并提示"升级后另存"。
- plugin 与 version 不一致时照读，但状态栏提示"导出器比编辑器旧"。

## 12. 已知限制（v1）

- 没有高度图/地形几何，3D 预览只画点云（P4）。
- 没有碰撞数据，编辑器无法判断"这条边是不是穿墙"——只能靠 V5 距离启发式。
- `source=game` 时点位不可移动：位置由游戏扫描决定，我们能改的是边/标签/惩罚/可走性。
