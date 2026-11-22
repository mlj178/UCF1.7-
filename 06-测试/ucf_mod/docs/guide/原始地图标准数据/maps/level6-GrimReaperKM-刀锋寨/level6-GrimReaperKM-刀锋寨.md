# level6 · GrimReaperKM · 刀锋寨

> 所属模式：Special 特殊战　｜　上级索引：[点位与区域标准.md](../../点位与区域标准.md)

## 0. 来源文件

```
文件：UnityCrossFire_Data\level6
大小：50,364 字节
MD5 ：b764d94d64e848d87e3f5a1ba34c3b55
场景：Assets/Scenes/Special/GrimReaperKM.unity
提取：SerializedFile v22 对象表遍历，113 个 GameObject 全量分类
```

## 1. 摘要

| 项目 | 数量 |
|---|---|
| GameObject 总数 | 113 |
| 路点（tag 20022） | 0 |
| 区域对象 | 0 |
| 标记点对象 | 6 |
| 连线 | 36 |
| └ fall_point | 6 |

## 2. 区域表（0 条）

| # | 名称 | 类型 | 中心X | 中心Y | 中心Z | 尺寸X | 尺寸Y | 尺寸Z | 形状 | 父级 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|
（本图无区域对象）

## 3. 标记点表（6 条）

| # | 名称 | 类型 | X | Y | Z | 父级 | 脚本 | 备注 |
|---|---|---|---|---|---|---|---|---|
| 1 | Fall3 | fall_point | 3.630 | -9.980 | -15.590 | - | NodeLink2 | - |
| 2 | GR_Fall3 | fall_point | 0.890 | -10.010 | 18.950 | - | NodeLink2 | - |
| 3 | GR_Fall1 | fall_point | 0.890 | -9.730 | 25.130 | - | NodeLink2 | - |
| 4 | Fall1 | fall_point | 3.630 | -9.730 | -22.520 | - | NodeLink2 | - |
| 5 | GR_Fall2 | fall_point | 0.890 | -9.870 | 22.020 | - | NodeLink2 | - |
| 6 | Fall2 | fall_point | 3.630 | -10.110 | -19.140 | - | NodeLink2 | - |

## 4. 线表（36 条）

| # | 名称 | 类型 | 起点X | 起点Y | 起点Z | 终点对象 | 终点X | 终点Y | 终点Z | 父级 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Fall3 | link | 3.630 | -9.980 | -15.590 | End | 2.260 | -13.370 | -15.590 | - | NodeLink2 |
| 2 | End | link | 4.074 | -13.768 | 21.660 | GR_OneJump3 | 5.274 | -13.028 | 21.660 | GR_OneJump3 | Bot_JumpLink |
| 3 | JumpLink1 | link | 4.570 | -12.100 | -1.450 | End | -0.850 | -12.100 | -1.450 | - | Bot_JumpLink/NodeLink2 |
| 4 | GR_OneJump7 | link | 5.274 | -13.028 | 5.660 | End | 4.074 | -13.768 | 5.660 | - | NodeLink |
| 5 | End | link | -2.360 | -13.768 | -20.110 | GR_OneJump7 (1) | -1.160 | -13.028 | -20.110 | GR_OneJump7 (1) | Bot_JumpLink |
| 6 | GR_OneJump7 (1) | link | -1.160 | -13.028 | -20.110 | End | -2.360 | -13.768 | -20.110 | - | NodeLink |
| 7 | End | link | 4.074 | -13.768 | 13.660 | GR_OneJump5 | 5.274 | -13.028 | 13.660 | GR_OneJump5 | Bot_JumpLink |
| 8 | GR_Fall3 | link | 0.890 | -10.010 | 18.950 | End | -0.480 | -13.400 | 18.950 | - | NodeLink2 |
| 9 | GR_OneJump3 | link | 5.274 | -13.028 | 21.660 | End | 4.074 | -13.768 | 21.660 | - | NodeLink |
| 10 | End | link | 4.074 | -13.768 | 5.660 | GR_OneJump7 | 5.274 | -13.028 | 5.660 | GR_OneJump7 | Bot_JumpLink |
| 11 | GR_Fall1 | link | 0.890 | -9.730 | 25.130 | End | -0.480 | -13.120 | 25.130 | - | NodeLink2 |
| 12 | GR_OneJump4 | link | 5.274 | -13.028 | 17.660 | End | 4.074 | -13.768 | 17.660 | - | NodeLink |
| 13 | End | link | 7.576 | -13.800 | 21.819 | GR_OneJump1 | 8.776 | -13.060 | 21.819 | GR_OneJump1 | Bot_JumpLink |
| 14 | End | link | -0.850 | -12.100 | -1.450 | JumpLink1 | 4.570 | -12.100 | -1.450 | JumpLink1 | Bot_JumpLink |
| 15 | JumpLink3 | link | 4.570 | -12.640 | 8.260 | End | -0.850 | -11.780 | 8.260 | - | Bot_JumpLink/NodeLink2 |
| 16 | Fall1 | link | 3.630 | -9.730 | -22.520 | End | 2.260 | -13.120 | -22.520 | - | NodeLink2 |
| 17 | End | link | 4.074 | -13.768 | 17.660 | GR_OneJump4 | 5.274 | -13.028 | 17.660 | GR_OneJump4 | Bot_JumpLink |
| 18 | GR_OneJump6 (1) | link | -1.160 | -13.028 | -16.110 | End | -2.360 | -13.768 | -16.110 | - | NodeLink |
| 19 | End | link | -0.850 | -12.020 | 3.430 | JumpLink2 | 4.570 | -12.020 | 3.430 | JumpLink2 | Bot_JumpLink |
| 20 | GR_OneJump6 | link | 5.274 | -13.028 | 9.660 | End | 4.074 | -13.768 | 9.660 | - | NodeLink |
| 21 | GR_OneJump1 | link | 8.776 | -13.060 | 21.819 | End | 7.576 | -13.800 | 21.819 | - | NodeLink |
| 22 | GR_OneJump2 | link | 6.728 | -12.872 | 23.175 | End | 5.528 | -13.612 | 23.175 | - | NodeLink |
| 23 | JumpLink2 | link | 4.570 | -12.020 | 3.430 | End | -0.850 | -12.020 | 3.430 | - | Bot_JumpLink/NodeLink2 |
| 24 | GR_OneJump3 (1) | link | -1.160 | -13.028 | -4.110 | End | -2.360 | -13.768 | -4.110 | - | NodeLink |
| 25 | GR_Fall2 | link | 0.890 | -9.870 | 22.020 | End | -0.480 | -13.260 | 22.020 | - | NodeLink2 |
| 26 | End | link | -2.360 | -13.768 | -4.110 | GR_OneJump3 (1) | -1.160 | -13.028 | -4.110 | GR_OneJump3 (1) | Bot_JumpLink |
| 27 | End | link | 4.074 | -13.768 | 9.660 | GR_OneJump6 | 5.274 | -13.028 | 9.660 | GR_OneJump6 | Bot_JumpLink |
| 28 | End | link | 5.528 | -13.612 | 23.175 | GR_OneJump2 | 6.728 | -12.872 | 23.175 | GR_OneJump2 | Bot_JumpLink |
| 29 | GR_OneJump5 | link | 5.274 | -13.028 | 13.660 | End | 4.074 | -13.768 | 13.660 | - | NodeLink |
| 30 | End | link | -2.360 | -13.768 | -16.110 | GR_OneJump6 (1) | -1.160 | -13.028 | -16.110 | GR_OneJump6 (1) | Bot_JumpLink |
| 31 | GR_OneJump4 (1) | link | -1.160 | -13.028 | -8.110 | End | -2.360 | -13.768 | -8.110 | - | NodeLink |
| 32 | GR_OneJump5 (1) | link | -1.160 | -13.028 | -12.110 | End | -2.360 | -13.768 | -12.110 | - | NodeLink |
| 33 | End | link | -2.360 | -13.768 | -12.110 | GR_OneJump5 (1) | -1.160 | -13.028 | -12.110 | GR_OneJump5 (1) | Bot_JumpLink |
| 34 | End | link | -2.360 | -13.768 | -8.110 | GR_OneJump4 (1) | -1.160 | -13.028 | -8.110 | GR_OneJump4 (1) | Bot_JumpLink |
| 35 | End | link | -0.850 | -11.780 | 8.260 | JumpLink3 | 4.570 | -12.640 | 8.260 | JumpLink3 | Bot_JumpLink |
| 36 | Fall2 | link | 3.630 | -10.110 | -19.140 | End | 2.260 | -13.500 | -19.140 | - | NodeLink2 |

## 5. 分组结构

```
(根)  (6 个)
```

## 6. 路点全量坐标（0 个）

路点 = 场景里 tag 等于 20022（WayPoint）的 GameObject。格式：X Y Z 名称。

```
```
