# level7 · DesertFort · 沙漠要塞

> 所属模式：Nano4 终结者模式 / Nano6 生化剑客模式　｜　上级索引：[点位与区域标准.md](../../点位与区域标准.md)

## 0. 来源文件

```
文件：UnityCrossFire_Data\level7
大小：82,068 字节
MD5 ：f4dba2dc8e16245deeab9c5b56f2b483
场景：Assets/Scenes/Nano/DesertFort.unity
提取：SerializedFile v22 对象表遍历，199 个 GameObject 全量分类
```

## 1. 摘要

| 项目 | 数量 |
|---|---|
| GameObject 总数 | 199 |
| 路点（tag 20022） | 8 |
| 区域对象 | 17 |
| 标记点对象 | 56 |
| 连线 | 11 |
| └ guard_pos | 51 |
| └ fall_point | 3 |
| └ air_point | 2 |

## 2. 区域表（17 条）

| # | 名称 | 类型 | 中心X | 中心Y | 中心Z | 尺寸X | 尺寸Y | 尺寸Z | 形状 | 父级 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Cube (7) | area_box | 20.040 | 6.960 | 41.010 | 10.071 | 100.000 | 1.000 | 盒体 | AirWall | - |
| 2 | Cube (6) | area_box | 23.230 | 2.420 | -32.380 | 12.000 | 100.000 | 1.000 | 盒体 | AirWall | - |
| 3 | Cube | area_box | -56.800 | 9.610 | 5.190 | 90.000 | 100.000 | 1.000 | 盒体 | AirWall | - |
| 4 | GuardArea_Tower | guard_area | -47.720 | 20.060 | -5.310 | 9.000 | 2.000 | 9.000 | 盒体 | - | Trigger |
| 5 | Rappel1 | area_box | 10.817 | 20.800 | 15.205 | 2.500 | 2.500 | 2.500 | 盒体 | - | Trigger |
| 6 | Cube (5) | area_box | 20.070 | 6.960 | 40.830 | 14.421 | 100.000 | 1.000 | 盒体 | AirWall | - |
| 7 | GuardArea_Bridge | guard_area | -10.920 | 15.050 | -5.250 | 14.000 | 5.000 | 7.000 | 盒体 | - | Trigger |
| 8 | GuardArea_House | guard_area | -21.370 | 9.000 | 23.610 | 12.000 | 4.000 | 18.000 | 盒体 | - | Trigger |
| 9 | Cube (2) | area_box | -13.690 | 9.164 | 49.560 | 90.000 | 100.000 | 1.000 | 盒体 | AirWall | - |
| 10 | Cube (4) | area_box | 24.660 | 9.340 | -33.480 | 3.995 | 100.000 | 1.000 | 盒体 | AirWall | - |
| 11 | Cube (1) | area_box | -13.690 | 9.164 | -39.350 | 90.000 | 100.000 | 1.000 | 盒体 | AirWall | - |
| 12 | FALCustom1 | area_box | -21.252 | 9.141 | 17.785 | 1.000 | 1.500 | 1.000 | 盒体 | - | - |
| 13 | Cube (3) | area_box | 25.520 | 6.960 | 5.200 | 90.000 | 100.000 | 1.000 | 盒体 | AirWall | - |
| 14 | ClimbArea | area_box | -49.650 | 19.800 | -5.450 | 1.500 | 12.000 | 0.500 | 盒体 | - | Trigger |
| 15 | FALCustom2 | area_box | -9.104 | 14.752 | -22.366 | 1.000 | 1.500 | 1.000 | 盒体 | - | - |
| 16 | FALCustom3 | area_box | -1.248 | 14.604 | 11.857 | 2.500 | 2.000 | 2.500 | 盒体 | - | Trigger |
| 17 | Rappel2 | area_box | -44.214 | 19.640 | -1.830 | 2.500 | 2.500 | 2.500 | 盒体 | - | Trigger |

## 3. 标记点表（56 条）

| # | 名称 | 类型 | X | Y | Z | 父级 | 脚本 | 备注 |
|---|---|---|---|---|---|---|---|---|
| 1 | 3 (3) | guard_pos | -16.370 | 8.000 | 23.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 2 | 6 (2) | guard_pos | -17.920 | 15.050 | -4.250 | GuardArea_Bridge | Bot_NanoGuardPos | - |
| 3 | 1 (1) | guard_pos | -27.370 | 8.000 | 17.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 4 | 1 | guard_pos | -27.370 | 8.000 | 14.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 5 | AirPoint | air_point | -16.471 | 15.699 | -0.454 | Fall_1 | NodeLink | - |
| 6 | 4 | guard_pos | -13.920 | 15.050 | -8.250 | GuardArea_Bridge | Bot_NanoGuardPos | - |
| 7 | 3 | guard_pos | -21.870 | 8.000 | 26.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 8 | 5 | guard_pos | -15.920 | 15.050 | -8.250 | GuardArea_Bridge | Bot_NanoGuardPos | - |
| 9 | 3 | guard_pos | -11.920 | 15.050 | -6.250 | GuardArea_Bridge | Bot_NanoGuardPos | - |
| 10 | 5 (2) | guard_pos | -15.920 | 15.050 | -4.250 | GuardArea_Bridge | Bot_NanoGuardPos | - |
| 11 | Fall_1 | fall_point | -16.471 | 15.699 | -2.454 | GuardArea_Bridge | NodeLink/NodeLink | - |
| 12 | 2 (8) | guard_pos | -16.370 | 8.000 | 29.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 13 | 2 (3) | guard_pos | -24.870 | 8.000 | 23.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 14 | AirPoint (1) | air_point | -18.471 | 15.699 | -2.454 | Fall_1 | NodeLink | - |
| 15 | 3 (1) | guard_pos | -11.920 | 15.050 | -4.250 | GuardArea_Bridge | Bot_NanoGuardPos | - |
| 16 | 4 (3) | guard_pos | -13.920 | 15.050 | -2.250 | GuardArea_Bridge | Bot_NanoGuardPos | - |
| 17 | 2 (7) | guard_pos | -18.870 | 8.000 | 29.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 18 | 1 (9) | guard_pos | -18.370 | 8.000 | 32.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 19 | 1 (8) | guard_pos | -21.370 | 8.000 | 32.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 20 | 4 (1) | guard_pos | -13.920 | 15.050 | -6.250 | GuardArea_Bridge | Bot_NanoGuardPos | - |
| 21 | 3 (6) | guard_pos | -16.370 | 8.000 | 14.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 22 | 2 (1) | guard_pos | -9.920 | 15.050 | -4.250 | GuardArea_Bridge | Bot_NanoGuardPos | - |
| 23 | 1 (10) | guard_pos | -15.370 | 8.000 | 32.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 24 | 5 (3) | guard_pos | -15.920 | 15.050 | -2.250 | GuardArea_Bridge | Bot_NanoGuardPos | - |
| 25 | 3 (5) | guard_pos | -16.370 | 8.000 | 17.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 26 | 5 | guard_pos | -20.370 | 9.000 | 20.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 27 | 4 | guard_pos | -20.370 | 9.000 | 23.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 28 | 1 (5) | guard_pos | -27.370 | 8.000 | 29.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 29 | 1 | guard_pos | -7.920 | 15.050 | -6.250 | GuardArea_Bridge | Bot_NanoGuardPos | - |
| 30 | 2 (5) | guard_pos | -24.870 | 8.000 | 29.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 31 | 1 (7) | guard_pos | -24.370 | 8.000 | 32.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 32 | 3 (1) | guard_pos | -18.870 | 8.000 | 26.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 33 | 1 (6) | guard_pos | -27.370 | 8.000 | 32.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 34 | 2 (1) | guard_pos | -24.870 | 8.000 | 17.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 35 | 2 (6) | guard_pos | -21.870 | 8.000 | 29.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 36 | 4 (1) | guard_pos | -22.370 | 9.000 | 23.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 37 | 1 (1) | guard_pos | -8.110 | 15.050 | -4.250 | GuardArea_Bridge | Bot_NanoGuardPos | - |
| 38 | 4 (2) | guard_pos | -13.920 | 15.050 | -4.250 | GuardArea_Bridge | Bot_NanoGuardPos | - |
| 39 | 6 (3) | guard_pos | -17.920 | 15.050 | -2.250 | GuardArea_Bridge | Bot_NanoGuardPos | - |
| 40 | 2 | guard_pos | -24.870 | 8.000 | 14.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 41 | 1 (4) | guard_pos | -27.370 | 8.000 | 26.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 42 | 6 (1) | guard_pos | -17.920 | 15.050 | -6.250 | GuardArea_Bridge | Bot_NanoGuardPos | - |
| 43 | 5 (1) | guard_pos | -22.370 | 9.000 | 20.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 44 | FallPoint | fall_point | -23.051 | 2.449 | -2.504 | AirPoint (1) | - | - |
| 45 | FallPoint | fall_point | -16.111 | 2.449 | 2.656 | AirPoint | - | - |
| 46 | 1 (2) | guard_pos | -27.370 | 8.000 | 20.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 47 | 3 (2) | guard_pos | -16.370 | 8.000 | 26.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 48 | 2 | guard_pos | -44.950 | 20.060 | -0.880 | GuardArea_Tower | Bot_NanoGuardPos | - |
| 49 | 3 (4) | guard_pos | -16.370 | 8.000 | 20.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 50 | 1 (3) | guard_pos | -27.370 | 8.000 | 23.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 51 | 1 | guard_pos | -42.800 | 20.060 | -0.900 | GuardArea_Tower | Bot_NanoGuardPos | - |
| 52 | 6 | guard_pos | -17.920 | 15.050 | -8.250 | GuardArea_Bridge | Bot_NanoGuardPos | - |
| 53 | 2 (2) | guard_pos | -24.870 | 8.000 | 20.610 | GuardArea_House | Bot_NanoGuardPos | - |
| 54 | 5 (1) | guard_pos | -15.920 | 15.050 | -6.250 | GuardArea_Bridge | Bot_NanoGuardPos | - |
| 55 | 2 | guard_pos | -9.920 | 15.050 | -6.250 | GuardArea_Bridge | Bot_NanoGuardPos | - |
| 56 | 2 (4) | guard_pos | -24.870 | 8.000 | 26.610 | GuardArea_House | Bot_NanoGuardPos | - |

## 4. 线表（11 条）

| # | 名称 | 类型 | 起点X | 起点Y | 起点Z | 终点对象 | 终点X | 终点Y | 终点Z | 父级 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | StairLink2 | link | -50.340 | 19.572 | -8.730 | 1 (5) | -49.650 | 19.800 | -5.150 | ClimbArea | NodeLink |
| 2 | AirPoint | link | -16.471 | 15.699 | -0.454 | FallPoint | -16.111 | 2.449 | 2.656 | Fall_1 | NodeLink |
| 3 | Fall_1 | link | -16.471 | 15.699 | -2.454 | AirPoint (1) | -18.471 | 15.699 | -2.454 | GuardArea_Bridge | NodeLink/NodeLink |
| 4 | AirPoint (1) | link | -18.471 | 15.699 | -2.454 | FallPoint | -23.051 | 2.449 | -2.504 | Fall_1 | NodeLink |
| 5 | HouseJump1 | link | -25.920 | 8.700 | 34.890 | HouseJump2 | -25.920 | 8.700 | 40.890 | GuardArea_House | Bot_JumpLink/NodeLink2 |
| 6 | JumpLink | link | -43.748 | 20.462 | -1.656 | RappelEscape | -43.730 | 22.560 | -1.680 | GuardArea_Tower | Bot_JumpLink |
| 7 | RappelEscape | link | -43.730 | 22.560 | -1.680 | End | -43.730 | 12.560 | 39.720 | GuardArea_Tower | NodeLink2/PointNodeTagModifier |
| 8 | HouseJump2 | link | -25.920 | 8.700 | 40.890 | HouseJump1 | -25.920 | 8.700 | 34.890 | HouseJump1 | Bot_JumpLink |
| 9 | StairLink1 | link | -49.673 | 8.580 | -4.333 | 1 | -49.650 | 9.800 | -5.150 | ClimbArea | NodeLink |
| 10 | Jump1 | link | -55.060 | 8.110 | 13.580 | End | -55.060 | 8.110 | 17.080 | - | NodeLink/Bot_JumpLink |
| 11 | End | link | -55.060 | 8.110 | 17.080 | Jump1 | -55.060 | 8.110 | 13.580 | Jump1 | Bot_JumpLink/NodeLink |

## 5. 分组结构

```
GuardArea_House  (31 个)
GuardArea_Bridge  (19 个)
(根)  (9 个)
AirWall  (8 个)
Fall_1  (2 个)
GuardArea_Tower  (2 个)
AirPoint (1)  (1 个)
AirPoint  (1 个)
```

## 6. 路点全量坐标（8 个）

路点 = 场景里 tag 等于 20022（WayPoint）的 GameObject。格式：X Y Z 名称。

```
-49.650 15.800 -5.150 1 (3)
-16.471 15.699 -0.454 AirPoint
-49.650 13.800 -5.150 1 (2)
-18.471 15.699 -2.454 AirPoint (1)
-49.650 17.800 -5.150 1 (4)
-49.650 9.800 -5.150 1
-49.650 19.800 -5.150 1 (5)
-49.650 11.800 -5.150 1 (1)
```
