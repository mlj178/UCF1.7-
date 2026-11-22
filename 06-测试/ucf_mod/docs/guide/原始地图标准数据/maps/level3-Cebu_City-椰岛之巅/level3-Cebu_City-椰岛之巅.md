# level3 · Cebu_City · 椰岛之巅

> 所属模式：TeamDeath 团队模式　｜　上级索引：[点位与区域标准.md](../../点位与区域标准.md)

## 0. 来源文件

```
文件：UnityCrossFire_Data\level3
大小：60,500 字节
MD5 ：7546065d5f8daf143ca72ffc16b9af02
场景：Assets/Scenes/TeamDeath/Cebu_City.unity
提取：SerializedFile v22 对象表遍历，122 个 GameObject 全量分类
```

## 1. 摘要

| 项目 | 数量 |
|---|---|
| GameObject 总数 | 122 |
| 路点（tag 20022） | 2 |
| 区域对象 | 0 |
| 标记点对象 | 10 |
| 连线 | 4 |
| └ crouch_pos | 10 |

## 2. 区域表（0 条）

| # | 名称 | 类型 | 中心X | 中心Y | 中心Z | 尺寸X | 尺寸Y | 尺寸Z | 形状 | 父级 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|
（本图无区域对象）

## 3. 标记点表（10 条）

| # | 名称 | 类型 | X | Y | Z | 父级 | 脚本 | 备注 |
|---|---|---|---|---|---|---|---|---|
| 1 | CrouchPosBL_3 | crouch_pos | -21.000 | -11.000 | -2.000 | - | Bot_CrouchPos | - |
| 2 | CrouchPosNeutral_1_2 | crouch_pos | -28.000 | -4.000 | -2.000 | - | Bot_CrouchPos | - |
| 3 | CrouchPosGR_2 | crouch_pos | 5.000 | -11.000 | 24.000 | - | Bot_CrouchPos | - |
| 4 | CrouchPosNeutral_1_1 | crouch_pos | -20.000 | -4.000 | 6.000 | - | Bot_CrouchPos | - |
| 5 | CrouchPosGR_3 | crouch_pos | -20.000 | -11.000 | 15.000 | - | Bot_CrouchPos | - |
| 6 | CrouchPosBL_2 | crouch_pos | 4.000 | -11.000 | -11.000 | - | Bot_CrouchPos | - |
| 7 | CrouchPosGR_1 | crouch_pos | 30.000 | -11.000 | 15.000 | - | Bot_CrouchPos | - |
| 8 | CrouchPosNeutral_2_1 | crouch_pos | 29.500 | -4.000 | 6.500 | - | Bot_CrouchPos | - |
| 9 | CrouchPosNeutral_2_2 | crouch_pos | 38.000 | -4.000 | 15.000 | - | Bot_CrouchPos | - |
| 10 | CrouchPosBL_1 | crouch_pos | 30.000 | -11.000 | -2.000 | - | Bot_CrouchPos | - |

## 4. 线表（4 条）

| # | 名称 | 类型 | 起点X | 起点Y | 起点Z | 终点对象 | 终点X | 终点Y | 终点Z | 父级 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1 | link | 28.000 | -3.000 | 6.500 | 2 | 22.000 | -11.000 | 6.500 | Window1 | NodeLink |
| 2 | Window2 | link | -20.000 | -4.000 | 6.500 | 1 | -22.000 | -3.000 | 6.500 | - | Bot_JumpLink/NodeLink |
| 3 | 1 | link | -22.000 | -3.000 | 6.500 | 2 | -28.000 | -11.000 | 6.500 | Window2 | NodeLink |
| 4 | Window1 | link | 30.000 | -4.000 | 6.500 | 1 | 28.000 | -3.000 | 6.500 | - | Bot_JumpLink/NodeLink |

## 5. 分组结构

```
(根)  (10 个)
```

## 6. 路点全量坐标（2 个）

路点 = 场景里 tag 等于 20022（WayPoint）的 GameObject。格式：X Y Z 名称。

```
28.000 -3.000 6.500 1
-22.000 -3.000 6.500 1
```
