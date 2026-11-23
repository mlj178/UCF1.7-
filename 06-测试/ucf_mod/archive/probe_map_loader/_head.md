# UCF 1.7 原版地图 · 点位 / 区域 / 连线 标准表

> **版本**：v1.2（2026-11-22 按四篇文档全文校对：路点口径、三层模型、导航形态、冲突清单）　**生成**：2026-11-22
> **数据源**：原版 `UnityCrossFire1.7.1`（未修改任何文件）
> **性质**：本文件是 UCF 1.7 点位体系的标准数据源。人可读，程序可直接解析。

---

## 0. 怎么读这份文档

### 0.1 面向人

1. 先看 **§3 模式 × 地图矩阵**，确定要查哪张图
2. 到 **§4** 找对应模式，按 `levelN · 英文名 · 中文名` 定位
3. 每张图固定四块：**来源 → 摘要 → 区域表 → 点表 → 线表 → 分组**
4. 坐标全部是**世界坐标**，单位米，3 位小数

### 0.2 面向机器（数据契约）

本文件是唯一数据源，**不附带任何 json**。解析规则：

| 规则 | 说明 |
|---|---|
| 图锚点 | `#### level{N} · {英文} · {中文}`，N 为 0~11 |
| 表识别 | 每个 `**××表**（N 条）` 后紧跟一张管道表 |
| 表结构 | 第 1 行表头，第 2 行 `|---|` 分隔 |
| 列序 | 固定，**按列序取值，不要按列名**（列名可能微调） |
| 空值 | `-` |
| 数值 | 定点十进制 3 位小数 |
| 分隔 | 单元格内不含 `\|` |

### 0.3 列定义

**区域表（12 列）**

```
# | 名称 | 类型 | 中心X | 中心Y | 中心Z | 尺寸X | 尺寸Y | 尺寸Z | 形状 | 父级 | 备注
```

- `形状`：`盒体` = 有 BoxCollider，尺寸为 collider size；`标记点` = 仅 Transform，无碰撞体

**标记点表（9 列）**

```
# | 名称 | 类型 | X | Y | Z | 父级 | 脚本 | 备注
```

**线表（12 列）**

```
# | 名称 | 类型 | 起点X | 起点Y | 起点Z | 终点对象 | 终点X | 终点Y | 终点Z | 父级 | 备注
```

---

## 1. 数据来源总表

全部数据来自：

```
D:\BaiduNetdiskDownload\原始\UnityCrossFire1.7.1\UnityCrossFire1.7.1\UnityCrossFire_Data\
```

| level | 场景文件 | 字节数 | MD5 | 场景资源路径 |
|---|---|---|---|---|
| 0 | level0 | 209,276 | `3597612b9a732b7f1a7f4277ca80cbfe` | `Assets/Scenes/GameStart.unity` |
| 1 | level1 | 354,420 | `88a70fb22af57ddce6293f89aa692832` | `Assets/Scenes/TeamDeath/TransportShip.unity` |
| 2 | level2 | 76,876 | `fba06f8bb8e39244dd45d73033441444` | `Assets/Scenes/TeamDeath/Factory.unity` |
| 3 | level3 | 60,500 | `7546065d5f8daf143ca72ffc16b9af02` | `Assets/Scenes/TeamDeath/Cebu_City.unity` |
| 4 | level4 | 63,532 | `e94602dd66d0672fc82475864b15075f` | `Assets/Scenes/BlastingMode/NY_TM.unity` |
| 5 | level5 | 47,772 | `7148afffde84d8325ca9daa03c875ffc` | `Assets/Scenes/Special/Arena.unity` |
| 6 | level6 | 50,364 | `b764d94d64e848d87e3f5a1ba34c3b55` | `Assets/Scenes/Special/GrimReaperKM.unity` |
| 7 | level7 | 82,068 | `f4dba2dc8e16245deeab9c5b56f2b483` | `Assets/Scenes/Nano/DesertFort.unity` |
| 8 | level8 | 741,516 | `82471539c82ac7fd85ab610c0d16cdef` | `Assets/Scenes/Nano/NanoResort.unity` |
| 9 | level9 | 192,140 | `89c56148f205eb630730dcf58ba4fa20` | `Assets/Scenes/Nano30/Nano30_Storm.unity` |
| 10 | level10 | 197,932 | `d555d653e5536998cb7e10c093af52a9` | `Assets/Scenes/Nano30/Nano_DawnVillage.unity` |
| 11 | level11 | 61,980 | `b7f8c56b28ac80b3e5b8ee5cbfa855e5` | `Assets/Scenes/Special/DeathRing.unity` |

**场景名册**：`globalgamemanagers`（1,617,300 字节），`BuildSettings` 对象 path_id = 11，12 条路径。

**提取方法（可复现）**

1. 解析 SerializedFile v22 对象表，按真实对象计数（非字符串扫描）
2. 读 `GameObject.m_Name` 与 `Transform.m_LocalPosition`，沿父链累加得世界坐标
3. 每个 `MonoBehaviour` 的 `m_Script` PPtr → `globalgamemanagers.assets` 的 `MonoScript` 表 → 类名
4. 连线端点：`NodeLink` 字段 `end`（对象内偏移 **44**）、`Bot_JumpLink` 偏移 **48**；解出的 PPtr 必须命中本场景 Transform 表，否则丢弃
5. 区域尺寸：`BoxCollider.m_Center` / `m_Size` / `m_IsTrigger`

---

## 2. 术语与分类

### 2.1 三层模型

口径与 [寻路全流程_从建图到蹲下.md](../寻路全流程_从建图到蹲下.md) §1 一致：**可走性层**只回答"能走到哪"，**目的层**只提供坐标，两层互不知道对方存在。

| 层 | 内容 | 由谁决定 |
|---|---|---|
| 可走性层 | `PointGraph` 节点（场景里 `tag == 20022` 的物体）／`NavMeshGraph` 三角面 | A\* Pathfinding 插件 |
| 连线层 | `NodeLink`（只加边）／`NodeLink2`（加 2 个端点 + 边）／`Bot_JumpLink`（只登记跳跃，不加点） | 插件 + 关卡 |
| 目的层 | `Bot_CrouchPos`／`Bot_GuardPos`／`Bot_NanoGuardPos`／`Bot_GuardArea`／`Bot_NanoGuardArea` | 游戏行为层 |

### 2.2 本文件的口径

| 术语 | 定义 | 数据在哪 |
|---|---|---|
| **路点** | `GameObject.tag == 20022（WayPoint）` | 附录 §9（全量坐标） |
| **标记点** | 挂目的层组件的对象（蹲点/守点/坠点/空点） | §4 每图「点表」 |
| **区域** | 盒体（有 `BoxCollider`）或按命名判定的区域对象 | §4 每图「区域表」 |
| **连线** | 挂 `NodeLink`／`NodeLink2`／`Bot_JumpLink` 的对象 | §4 每图「线表」 |

> **为什么分开**：路点决定"能走"，标记点决定"想去哪"。混在一张表里会把 3,070 个点图节点和 2 个蹲点并列，既难读也容易被误当成同一种东西。

### 2.3 类型枚举

| 类型 | 所属层 | 判定规则 | 语义出处 |
|---|---|---|---|
| `waypoint` | 可走性 | `tag == 20022` | 寻路全流程 §3 阶段 A |
| `link` | 连线 | 脚本 `NodeLink` / `NodeLink2` / `Bot_JumpLink` | 人机与路线设计 §3.2 |
| `crouch_pos` | 目的 | 脚本 `Bot_CrouchPos`，名称 `CrouchPos*` | 人机与路线设计 §3.1 |
| `guard_pos` | 目的 | 脚本 `Bot_GuardPos` / `Bot_NanoGuardPos` | 人机与路线设计 §3.2 |
| `guard_area` | 目的 | 脚本 `Bot_GuardArea` / `Bot_NanoGuardArea`，名称 `GuardArea*` | 人机与路线设计 §3.2 |
| `area_faction` | 区域 | 名称 ∈ {BL_Area, GR_Area, Neutral_Area, BL_SpawnArea, GR_SpawnArea} | 游戏基础信息 §2 |
| `area_lock` | 区域 | 脚本 `LockVelocityArea`（**只对玩家生效的速度锁区**，非 AI 导航） | dump.cs:243365 + IDA `OnTriggerStay` 0x10AE7EB0 |
| `fall_point` / `air_point` | 目的 | 名称 `FallPoint`/`Fall_N`/`GR_Fall`、`AirPoint*` | 本表实测（文档未定义） |
| `area_generic` / `area_box` | 区域 | 名称含 Area，或有 BoxCollider | 本表实测 |

### 2.3.1 关键脚本的字段与行为（来自 dump.cs + IDA）

| 脚本 | 关键字段 | 行为 | 出处 |
|---|---|---|---|
| `Bot_CrouchPos` | `crouchDisabled`@0x20、`always`@0x21；**继承 `Bot_GuardPos`** | 静态 `SpareList_BL/SpareList_GR`，`GetRandomPos(Team)` 按阵营取点 | dump.cs:231590 |
| `Bot_GuardArea` | **无字段** | **空类**，只有构造函数 | dump.cs:231641 |
| `Bot_NanoGuardArea` | `entrancePos[]`@0xC、`posList`@0x10、`neighborAreas[]`@0x14、`escapeAreas[]`@0x18、`escapePos[]`@0x1C | `OnTriggerEnter/Exit` 通知区内人机；`GetPos`/`RecyclePos`/`GetRandomEscapePos`/`GetSaferPos` | dump.cs:231780 |
| `Bot_JumpLink` | 静态 `linkDic`；`startNode`@0x20、`links[]`@0x24 | `OnLatePostScan` 把 Link 登记进 `linkDic`；**不加节点，只给已有节点挂跳跃记录** | dump.cs:231723 |
| `LockVelocityArea` | `speed`@0xC、`lockTime`@0x10、`saveVelY`@0x14 | `OnTriggerStay` 里 `GetComponentsInParent` 找 **`Player`** → **只影响玩家，不影响人机** | dump.cs:243365 / IDA 0x10AE7EB0 |

### 2.4 每张图的导航形态

「路点（总/激活）」是本表实测（`tag == 20022`，激活 = `m_IsActive`）；「导出节点/边」「NavMesh」来自 [地图对照表.md](../地图对照表.md) §1~§3（游戏运行时 Scan 后落盘，本表无法从场景文件直接读出）。

| level | 地图 | 形态 | 路点（总/激活） | 导出节点/边 | NavMesh 网格 · 三角形 | 数据来源 |
|---|---|---|---|---|---|---|
| 1 | 运输船 | 纯点图 | 786 / 786 | 786 / 1391 | 无 | 实测 + 对照表 |
| 8 | 生化酒店 | 纯点图 | 3,070 / 3,063 | 3,063 / 5,584 | 无 | 实测 + 对照表 |
| 4 | 胜利广场 | 纯面图 | 0 / 0 | 无 PointGraph | `NY_TM_NavMesh` · 976 | 实测 + 对照表 |
| 11 | 死亡擂台 | 纯面图 | 0 / 0 | 无 PointGraph | `DeathRing_NavMesh` · 94 | 实测 + 对照表 |
| 9 | 飓风危城 | 两者都没有 | 0 / 0 | 0 / 0（空档） | 无 | 实测 + 对照表 |
| 2 | 小型工厂 | 面图 + 端点图 | 0 / 0 | 12 / 6 | `Factory_NavMesh` · 1139 | 实测 + 对照表 |
| 3 | 椰岛之巅 | 两者都有 | 2 / 2 | 2 / 0 | `CebuCity_Navmesh` · 725 | 实测 + 对照表 |
| 5 | 竞技场 | 两者都有 | 17 / 17 | 17 / 24 | `Arena_NavMesh` · 1221 | 实测 + 对照表 |
| 6 | 刀锋寨 | 两者都有 | 0 / 0 | 18 / 9 | `GrimReaperKM_NavMesh` · 846 | 实测 + 对照表 |
| 7 | 沙漠要塞 | 两者都有 | 8 / 8 | 12 / 7 | `DesertFort_Navmesh` · 1259 | 实测 + 对照表 |
| 10 | 新寂静村 | 两者都有 | 180 / 180 | 180 / 98 | `Nano_DawnVillage_NavMesh` · 1236 | 实测 + 对照表 |

> **交叉核对结果**：11 张图的「路点总数」与《地图对照表》§2 的「场景 WayPoint（总）」**全部一致**；
> 生化酒店的 3,070 总 / 3,063 激活也精确吻合（本表实测 7 个未激活对象）。

