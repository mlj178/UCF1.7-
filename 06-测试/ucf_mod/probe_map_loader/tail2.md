## 5. 冲突清单

> 规则：**本表以游戏文件为准**；现有文档/代码的说法列在右列，只报告、不修改。
> 状态：✅ 一致 / ⚠️ 冲突 / 📌 本表新增 / 🔧 本表自身修正或局限

| # | 项目 | 本表（实测） | 现有说法 | 出处 | 状态 |
|---|---|---|---|---|---|
| 1 | 运输船路点数 | **786 / 786（激活）** | 「运输船的 786 点」 | [寻路全流程_从建图到蹲下.md](../../寻路全流程_从建图到蹲下.md) §6 | ✅ 一致 |
| 2 | 刀锋寨路点 / 节点 | **0 个 WayPoint；9 个 NodeLink2 → 18 节点** | 「刀锋寨场景 0 个 WayPoint、却有 18 个节点」 | 寻路全流程 §5 | ✅ 一致 |
| 3 | 小型工厂路点 | **0 个 WayPoint；6 个 NodeLink2** | 「6 个 NodeLink2 → 点图 12 个节点」 | [人机与路线设计.md](../../人机与路线设计.md) :222 | ✅ 一致 |
| 4 | 沙漠要塞路点 | **8 个 WayPoint；2 个 NodeLink2** | 「8 个 WayPoint + 2 个 NodeLink2（4 端点）= 12」 | 人机与路线设计 :224 | ✅ 一致 |
| 5 | 生化酒店路点（总/激活） | **3,070 / 3,063** | 「3070 / 3063」 | [地图对照表.md](../../地图对照表.md) §2 | ✅ 一致 |
| 6 | 点图/面图分类 | 运输船、生化酒店纯点；胜利广场、死亡擂台纯面；飓风危城两者皆无 | 同左 | [点图与可走面_为什么每张图不一样.md](../../点图与可走面_为什么每张图不一样.md) §3 | ✅ 一致 |
| 7 | `Bot_GuardPos`/`Bot_GuardArea` 分布 | 仅 level8（25 / 2）；`Bot_GuardArea` 在 dump.cs 里是**空类** | 「只活在生化酒店(8)且是死数据」 | 地图对照表 :166；dump.cs:231641 | ✅ 一致 |
| 8 | `Bot_NanoGuardPos`/`Bot_NanoGuardArea` 分布 | 仅 level7（51/3）、level10（55/10） | 「只出现在 7 和 10」 | 地图对照表 :164 | ✅ 一致 |
| 9 | **`PointNodeTagModifier` 分布** | **仅 level7（1 个）；level10 为 0** | 「`NanoGuardPos / NanoGuardArea / PointNodeTagModifier` 只出现在 7 和 10」 | 地图对照表 :164 | ⚠️ **冲突** |
| 10 | 死亡擂台形态 | 0 路点 / 0 标记点 / 0 连线；14 个 `LockVelocityArea` 经 IDA 确认**只对 Player 生效**（`OnTriggerStay` 里 `GetComponentsInParent` 找 `Player`，@0x10AE7EB0） | 「胜利广场、死亡擂台只有可走面」 | 地图对照表 :163；dump.cs:243365 | ✅ 一致（14 个不属 AI 区域） |
| 11 | `Bot_CrouchPos` 继承关系 | **继承 `Bot_GuardPos`**，另有 `crouchDisabled`@0x20、`always`@0x21 | 「是什么：`Bot_CrouchPos`（`team`@0xC、`zoomPos[]`@0x10…）」 | 人机与路线设计 :131；dump.cs:231590 | 📌 补充（继承关系未提及） |
| 12 | 蹲守点命名两套 | `CrouchPos2_BL`（level2）与 `CrouchPosBL_2`（level3）并存 | 未提及 | - | 📌 新增 |
| 13 | 单对象多连线组件 | level10 有对象同时挂 `NodeLink` 与 `Bot_JumpLink`，指向同一端点 | 未提及 | - | 📌 新增 |
| 14 | 大厅的 22 个 area | 全是 UI（Slider 的 Fill/Sliding/Handle Area） | 未提及 | - | 📌 新增 |
| 15 | **`Bot_JumpLink.links` 是数组** | 函数 `GetLinkEndByGraphNode` 暗示一条 JumpLink 可含多个端点；本表只解出**一个**端点字段（偏移 48） | — | dump.cs:231723 | 🔧 本表局限 |
| 16 | **本表 v1.1 的错误** | v1.1 把「点位」当成路点（生化酒店只列 2 个，实际 3,070 个路点） | — | 本文件 v1.1 | 🔧 v1.2 已修正 |

**本轮扫描范围**：`游戏基础信息.md`、`人机与路线设计.md`、`点图与可走面_为什么每张图不一样.md`、`寻路全流程_从建图到蹲下.md` 全文；`地图对照表.md` §1~§4 全文；`dump.cs` 相关类定义；IDA `LockVelocityArea.OnTriggerStay`。
**仍未扫描**：`部署总览.md`、`03-经验手册/`、`game_modifier/features/` 源码、`ucf_mod` 源码。

---

## 6. 校验记录

| 校验项 | 方法 | 结果 |
|---|---|---|
| 场景名册 | `globalgamemanagers` BuildSettings 解析 | ✅ 12 条，与 12 个 levelN 一一对应 |
| 对象计数 | 对象表遍历，非字符串扫描 | ✅ 12 张图共 6,440 个 GameObject |
| 路点计数 | `GameObject.m_Tag == 20022` | ✅ 共 4,063 个；与《地图对照表》§2 的 11 个数字**逐个吻合** |
| 连线端点 | `NodeLink`(44) / `NodeLink2`(44) / `Bot_JumpLink`(48) 解出的 PPtr 必须命中本场景 Transform | ✅ 744 条全部解析 |
| 世界坐标 | 局部坐标沿父链累加 | ✅ 量级合理（≈±100 m） |
| 表格自检 | 逐图比对「声明条数」与「实际行数」 | ✅ 12 图 × 3 表全部一致 |
| 脚本归属 | 每个点位的 `m_Script` → MonoScript 类名 | ✅ 全量可解析（1,338 个 MonoScript） |
| 语义核对 | dump.cs 字段偏移 + IDA 反编译 | ✅ `LockVelocityArea` / `Bot_CrouchPos` / `Bot_GuardArea` / `Bot_JumpLink` / `Bot_NanoGuardArea` 五个类已核 |

---

## 7. 与其他文档的重叠索引

| 文档 | 可能重叠 |
|---|---|
| [地图对照表.md](../../地图对照表.md) | 地图清单、点图/面图明细、模式 ↔ 地图 —— **重叠最多**，本表 §2.4 直接引用其导出数据 |
| [人机与路线设计.md](../../人机与路线设计.md) | 路点、路线、蹲守语义 |
| [寻路全流程_从建图到蹲下.md](../../寻路全流程_从建图到蹲下.md) | A\* 建图流程、tag 20022 定义 |
| [点图与可走面_为什么每张图不一样.md](../../点图与可走面_为什么每张图不一样.md) | 点图/面图分类 |
| [游戏基础信息.md](../../游戏基础信息.md) | 模式枚举、阵营 |
| `06-测试/ucf_mod/navdata/dev/*/map.json` | 工作台导出的点位坐标（C 级交叉源） |

---

## 8. 原始文件副本

每张图的原始场景文件已复制到：

```
maps/level{N}-{英文}-{中文}/level{N}
```

用于脱离游戏安装目录复现本表。MD5 见 §1。

---