# level10 · Nano_DawnVillage · 新寂静村

> 所属模式：Nano4_Terminator 多人终结者模式　｜　上级索引：[点位与区域标准.md](../../点位与区域标准.md)

## 0. 来源文件

```
文件：UnityCrossFire_Data\level10
大小：197,932 字节
MD5 ：d555d653e5536998cb7e10c093af52a9
场景：Assets/Scenes/Nano30/Nano_DawnVillage.unity
提取：SerializedFile v22 对象表遍历，619 个 GameObject 全量分类
```

## 1. 摘要

| 项目 | 数量 |
|---|---|
| GameObject 总数 | 619 |
| 路点（tag 20022） | 180 |
| 区域对象 | 20 |
| 标记点对象 | 325 |
| 连线 | 258 |
| └ fall_point | 180 |
| └ air_point | 90 |
| └ guard_pos | 55 |

## 2. 区域表（20 条）

| # | 名称 | 类型 | 中心X | 中心Y | 中心Z | 尺寸X | 尺寸Y | 尺寸Z | 形状 | 父级 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Area4 | area_generic | 34.000 | 15.000 | 0.000 | - | - | - | 标记点 | - | - |
| 2 | GuardArea4_2 | guard_area | 9.340 | 23.810 | -39.700 | 7.000 | 10.000 | 10.000 | 盒体 | - | Trigger |
| 3 | Area3 | area_generic | 1.500 | 15.500 | -7.500 | - | - | - | 标记点 | - | - |
| 4 | Area7 | area_generic | -35.000 | 10.500 | 16.000 | - | - | - | 标记点 | - | - |
| 5 | GuardArea1_4 | guard_area | 32.150 | 13.700 | -13.860 | 7.000 | 2.000 | 7.000 | 盒体 | - | Trigger |
| 6 | JumpArea3 | area_generic | 7.620 | 10.000 | 22.620 | - | - | - | 标记点 | - | - |
| 7 | GuardArea3 | guard_area | -10.780 | 17.580 | -7.180 | 23.000 | 3.000 | 7.000 | 盒体 | - | Trigger |
| 8 | Area5 | area_generic | 20.000 | 10.000 | -20.000 | - | - | - | 标记点 | - | - |
| 9 | Area1 | area_generic | -9.000 | 15.000 | 37.000 | - | - | - | 标记点 | - | - |
| 10 | ClimbArea | area_box | -0.810 | 14.250 | 34.500 | 3.000 | 10.000 | 0.750 | 盒体 | - | Trigger |
| 11 | GuardArea4_1 | guard_area | 9.340 | 20.400 | -28.740 | 7.000 | 3.000 | 10.000 | 盒体 | - | Trigger |
| 12 | GuardArea2_1 | guard_area | -10.190 | 14.290 | 37.080 | 15.000 | 2.000 | 4.000 | 盒体 | - | Trigger |
| 13 | GuardArea2_2 | guard_area | -20.010 | 14.970 | 33.990 | 4.000 | 3.000 | 10.000 | 盒体 | - | Trigger |
| 14 | GuardArea1_2 | guard_area | 33.650 | 13.700 | 7.330 | 3.000 | 2.000 | 10.000 | 盒体 | - | Trigger |
| 15 | JumpArea2 | area_generic | 25.000 | 10.000 | 19.000 | - | - | - | 标记点 | - | - |
| 16 | GuardArea1_3 | guard_area | 33.650 | 13.700 | -3.750 | 3.000 | 2.000 | 10.000 | 盒体 | - | Trigger |
| 17 | Area8 | area_generic | -50.000 | 4.000 | 3.000 | - | - | - | 标记点 | - | - |
| 18 | Block | area_box | 27.290 | 8.550 | 17.540 | 1.000 | 8.000 | 7.000 | 盒体 | JumpArea2 | - |
| 19 | GuardArea2_3 | guard_area | -18.700 | 21.590 | 23.690 | 7.000 | 3.000 | 6.000 | 盒体 | - | Trigger |
| 20 | GuardArea1_1 | guard_area | 31.340 | 13.700 | 17.900 | 9.000 | 2.000 | 9.000 | 盒体 | - | Trigger |

## 3. 标记点表（325 条）

| # | 名称 | 类型 | X | Y | Z | 父级 | 脚本 | 备注 |
|---|---|---|---|---|---|---|---|---|
| 1 | FallPoint | fall_point | 6.660 | 6.000 | 26.970 | AirPoint | - | - |
| 2 | Fall_7 | fall_point | -11.030 | 15.000 | 35.210 | Area1 | NodeLink | - |
| 3 | FallPoint | fall_point | 32.960 | 6.000 | -1.080 | AirPoint | - | - |
| 4 | AirPoint | air_point | -1.390 | 20.390 | -43.890 | Fall_9 (7) | NodeLink | - |
| 5 | AirPoint | air_point | 12.500 | 14.000 | 13.360 | Fall_2 | NodeLink | - |
| 6 | Fall_3 | fall_point | -2.370 | 15.000 | 38.950 | Area1 | NodeLink | - |
| 7 | Fall_6 | fall_point | 32.960 | 14.000 | -8.840 | Area4 | NodeLink | - |
| 8 | 1 (5) | guard_pos | -21.470 | 21.090 | 21.880 | GuardArea2_3 | Bot_NanoGuardPos | - |
| 9 | FallPoint | fall_point | -27.940 | 3.500 | 20.200 | AirPoint | - | - |
| 10 | AirPoint | air_point | -3.390 | 20.390 | -43.890 | Fall_9 (8) | NodeLink | - |
| 11 | FallPoint | fall_point | -19.990 | 2.650 | 27.930 | AirPoint | - | - |
| 12 | 1 (1) | guard_pos | 28.090 | 13.700 | 17.140 | GuardArea1_1 | Bot_NanoGuardPos | - |
| 13 | 1 (1) | guard_pos | 34.310 | 13.700 | -14.290 | GuardArea1_4 | Bot_NanoGuardPos | - |
| 14 | FallPoint | fall_point | 30.550 | 6.000 | 18.080 | AirPoint | - | - |
| 15 | 1 | guard_pos | 28.090 | 13.700 | 14.140 | GuardArea1_1 | Bot_NanoGuardPos | - |
| 16 | FallPoint | fall_point | 21.500 | 5.500 | -11.120 | AirPoint | - | - |
| 17 | 1 (5) | guard_pos | -10.430 | 14.290 | 38.290 | GuardArea2_1 | Bot_NanoGuardPos | - |
| 18 | Fall_9 (8) | fall_point | -3.390 | 20.390 | -45.640 | Area6 | NodeLink | - |
| 19 | 1 (6) | guard_pos | -21.980 | 21.090 | 24.840 | GuardArea2_3 | Bot_NanoGuardPos | - |
| 20 | Fall_9 (11) | fall_point | -9.390 | 20.390 | -45.640 | Area6 | NodeLink | - |
| 21 | Fall_2 | fall_point | 12.500 | 14.000 | 11.360 | HouseTop | NodeLink | - |
| 22 | FallPoint | fall_point | 21.500 | 5.500 | -13.970 | AirPoint | - | - |
| 23 | FallPoint | fall_point | 32.960 | 6.000 | -4.840 | AirPoint | - | - |
| 24 | Fall_8 | fall_point | -15.490 | 15.000 | 35.210 | Area1 | NodeLink | - |
| 25 | Fall_15 | fall_point | 10.050 | 13.000 | 6.690 | HouseTop | NodeLink | - |
| 26 | Fall_3 | fall_point | 11.750 | 13.500 | -20.480 | Area6 | NodeLink | - |
| 27 | FallPoint | fall_point | -11.030 | 7.000 | 38.210 | AirPoint | - | - |
| 28 | Fall_2 | fall_point | -34.960 | 10.500 | 1.120 | Area7 | NodeLink | - |
| 29 | AirPoint | air_point | -15.490 | 15.000 | 36.210 | Fall_8 | NodeLink | - |
| 30 | Fall_1 | fall_point | 4.250 | 13.500 | -21.110 | Area6 | NodeLink | - |
| 31 | Fall_14 | fall_point | -19.500 | 21.000 | 21.980 | Area1 | NodeLink | - |
| 32 | FallPoint | fall_point | -5.640 | 7.000 | 41.950 | AirPoint | - | - |
| 33 | Fall_7 | fall_point | -25.000 | 7.500 | 19.190 | Area7 | NodeLink | - |
| 34 | AirPoint | air_point | 13.830 | 20.390 | -38.750 | Fall_7 | NodeLink | - |
| 35 | FallPoint | fall_point | -27.870 | 3.500 | 22.560 | AirPoint | - | - |
| 36 | 1 (3) | guard_pos | 34.550 | 13.700 | -7.220 | GuardArea1_3 | Bot_NanoGuardPos | - |
| 37 | FallPoint | fall_point | 10.610 | 5.390 | -42.890 | AirPoint | - | - |
| 38 | Fall_4 | fall_point | 32.960 | 14.000 | -1.120 | Area4 | NodeLink | - |
| 39 | FallPoint | fall_point | 0.610 | 5.390 | -42.890 | AirPoint | - | - |
| 40 | AirPoint | air_point | 11.750 | 13.500 | -18.730 | Fall_3 | NodeLink | - |
| 41 | Fall_2 | fall_point | 8.250 | 13.500 | -21.110 | Area6 | NodeLink | - |
| 42 | AirPoint | air_point | -25.000 | 7.500 | 20.940 | Fall_7 | NodeLink | - |
| 43 | AirPoint | air_point | -27.870 | 7.500 | 20.310 | Fall_10 | NodeLink | - |
| 44 | FallPoint | fall_point | -25.440 | 3.500 | 14.510 | AirPoint | - | - |
| 45 | FallPoint | fall_point | 32.960 | 6.000 | 11.040 | AirPoint | - | - |
| 46 | AirPoint | air_point | -1.860 | 17.500 | -7.830 | Fall_1 | NodeLink | - |
| 47 | FallPoint | fall_point | 2.920 | 6.000 | 11.310 | AirPoint (1) | - | - |
| 48 | Fall_1 | fall_point | -35.000 | 7.500 | -4.880 | Area7 | NodeLink | - |
| 49 | AirPoint | air_point | 12.610 | 20.390 | -43.890 | Fall_9 | NodeLink | - |
| 50 | AirPoint | air_point | -5.390 | 20.390 | -43.890 | Fall_9 (9) | NodeLink | - |
| 51 | 1 (1) | guard_pos | -16.470 | 21.090 | 23.420 | GuardArea2_3 | Bot_NanoGuardPos | - |
| 52 | FallPoint | fall_point | 5.970 | 6.000 | 30.850 | AirPoint | - | - |
| 53 | Fall_9 | fall_point | -27.440 | 7.500 | 19.490 | Area7 | NodeLink | - |
| 54 | AirPoint | air_point | 15.330 | 13.000 | -5.760 | Fall_11 | NodeLink | - |
| 55 | Fall | fall_point | -27.930 | 7.500 | 18.710 | 2 | Bot_JumpLink | - |
| 56 | FallPoint | fall_point | -3.390 | 5.390 | -42.890 | AirPoint | - | - |
| 57 | AirPoint | air_point | -27.940 | 7.500 | 12.800 | Fall_12 | NodeLink | - |
| 58 | Fall_9 (7) | fall_point | -1.390 | 20.390 | -45.640 | Area6 | NodeLink | - |
| 59 | AirPoint | air_point | 32.960 | 14.000 | 0.630 | Fall_4 | NodeLink | - |
| 60 | 1 | guard_pos | 33.650 | 13.700 | -0.250 | GuardArea1_3 | Bot_NanoGuardPos | - |
| 61 | AirPoint | air_point | 5.970 | 11.000 | 27.850 | Fall_1 | NodeLink | - |
| 62 | FallPoint | fall_point | 21.500 | 5.500 | -16.560 | AirPoint | - | - |
| 63 | AirPoint | air_point | 18.500 | 14.000 | 13.360 | Fall_4 | NodeLink | - |
| 64 | 1 (10) | guard_pos | -17.360 | 14.290 | 35.370 | GuardArea2_1 | Bot_NanoGuardPos | - |
| 65 | FallPoint | fall_point | -16.740 | 2.650 | 27.930 | AirPoint | - | - |
| 66 | FallPoint | fall_point | -9.390 | 5.390 | -42.890 | AirPoint | - | - |
| 67 | 1 (6) | guard_pos | -12.100 | 14.290 | 35.230 | GuardArea2_1 | Bot_NanoGuardPos | - |
| 68 | FallPoint | fall_point | -25.000 | 3.500 | 18.140 | AirPoint | - | - |
| 69 | FallPoint | fall_point | -35.000 | 3.500 | -0.880 | AirPoint | - | - |
| 70 | 1 | guard_pos | -16.040 | 21.090 | 25.530 | GuardArea2_3 | Bot_NanoGuardPos | - |
| 71 | FallPoint | fall_point | 18.860 | 6.000 | 10.470 | AirPoint | - | - |
| 72 | FallPoint | fall_point | 21.500 | 5.500 | -19.700 | AirPoint | - | - |
| 73 | Fall_5 | fall_point | 0.380 | 15.000 | 37.100 | Area1 | NodeLink | - |
| 74 | Fall_11 | fall_point | -22.260 | 15.000 | 32.810 | Area1 | NodeLink | - |
| 75 | AirPoint | air_point | 18.500 | 14.000 | -1.640 | Fall_9 | NodeLink | - |
| 76 | Fall_4 | fall_point | 0.380 | 15.000 | 38.950 | Area1 | NodeLink | - |
| 77 | AirPoint | air_point | 6.610 | 20.390 | -43.890 | Fall_9 (3) | NodeLink | - |
| 78 | 1 (3) | guard_pos | -19.100 | 21.090 | 24.840 | GuardArea2_3 | Bot_NanoGuardPos | - |
| 79 | 1 (7) | guard_pos | -13.300 | 14.290 | 38.500 | GuardArea2_1 | Bot_NanoGuardPos | - |
| 80 | FallPoint | fall_point | -9.000 | 7.000 | 41.950 | AirPoint | - | - |
| 81 | AirPoint | air_point | 10.050 | 13.000 | 8.440 | Fall_15 | NodeLink | - |
| 82 | FallPoint | fall_point | -25.000 | 3.500 | 23.190 | AirPoint | - | - |
| 83 | 1 | guard_pos | -19.130 | 14.470 | 37.950 | GuardArea2_2 | Bot_NanoGuardPos | - |
| 84 | Fall | fall_point | -27.930 | 7.500 | 10.710 | 1 | Bot_JumpLink | - |
| 85 | 1 (2) | guard_pos | 32.650 | 13.700 | 6.120 | GuardArea1_2 | Bot_NanoGuardPos | - |
| 86 | Fall_1 | fall_point | 21.500 | 11.000 | -23.700 | Area5 | NodeLink | - |
| 87 | AirPoint (1) | air_point | 7.500 | 14.000 | 11.360 | Fall_1 | NodeLink | - |
| 88 | AirPoint | air_point | 9.750 | 20.000 | -22.730 | Fall_4 | NodeLink | - |
| 89 | 3 | guard_pos | -6.440 | 17.580 | -10.240 | GuardArea3 | Bot_NanoGuardPos | - |
| 90 | AirPoint | air_point | 18.500 | 14.000 | 1.360 | Fall_8 | NodeLink | - |
| 91 | FallPoint | fall_point | 18.860 | 6.000 | 1.470 | AirPoint | - | - |
| 92 | Fall_8 | fall_point | -25.260 | 7.500 | 19.420 | Area7 | NodeLink | - |
| 93 | AirPoint | air_point | 32.960 | 14.000 | -7.090 | Fall_6 | NodeLink | - |
| 94 | AirPoint | air_point | 32.960 | 14.000 | -10.870 | Fall_7 | NodeLink | - |
| 95 | FallPoint | fall_point | 18.860 | 6.000 | 4.470 | AirPoint | - | - |
| 96 | Fall_6 | fall_point | -9.880 | 20.390 | -25.170 | Area6 | NodeLink | - |
| 97 | Fall_5 | fall_point | 7.350 | 20.000 | -24.480 | Area6 | NodeLink | - |
| 98 | AirPoint | air_point | -21.350 | 21.000 | 23.810 | Fall_13 | NodeLink | - |
| 99 | AirPoint | air_point | 10.050 | 13.000 | -5.760 | Fall_12 | NodeLink | - |
| 100 | FallPoint | fall_point | -25.260 | 3.500 | 23.420 | AirPoint | - | - |
| 101 | Fall_2 | fall_point | 21.500 | 11.000 | -20.560 | Area5 | NodeLink | - |
| 102 | FallPoint | fall_point | 6.610 | 5.390 | -42.890 | AirPoint | - | - |
| 103 | FallPoint | fall_point | 18.860 | 6.000 | -1.530 | AirPoint | - | - |
| 104 | Fall_4 | fall_point | 21.500 | 11.000 | -15.120 | Area5 | NodeLink | - |
| 105 | FallPoint | fall_point | 18.860 | 6.000 | 7.470 | AirPoint | - | - |
| 106 | FallPoint | fall_point | 18.860 | 6.000 | 16.470 | AirPoint | - | - |
| 107 | 1 (2) | guard_pos | -5.810 | 14.290 | 35.980 | GuardArea2_1 | Bot_NanoGuardPos | - |
| 108 | 1 (2) | guard_pos | -15.990 | 21.090 | 21.370 | GuardArea2_3 | Bot_NanoGuardPos | - |
| 109 | AirPoint | air_point | 7.350 | 20.000 | -22.730 | Fall_5 | NodeLink | - |
| 110 | AirPoint | air_point | -9.000 | 15.000 | 39.950 | Fall_1 | NodeLink | - |
| 111 | AirPoint | air_point | -21.480 | 17.500 | -5.350 | Fall_3 | NodeLink | - |
| 112 | 1 (2) | guard_pos | 32.650 | 13.700 | -4.960 | GuardArea1_3 | Bot_NanoGuardPos | - |
| 113 | FallPoint | fall_point | 8.250 | 5.500 | -17.110 | AirPoint | - | - |
| 114 | AirPoint | air_point | -6.080 | 17.500 | -7.830 | Fall_2 | NodeLink | - |
| 115 | AirPoint | air_point | 13.790 | 20.390 | -42.750 | Fall_8 | NodeLink | - |
| 116 | FallPoint | fall_point | 17.890 | 5.500 | -20.670 | AirPoint | - | - |
| 117 | 1 (2) | guard_pos | -21.920 | 14.470 | 37.050 | GuardArea2_2 | Bot_NanoGuardPos | - |
| 118 | 1 (3) | guard_pos | -22.030 | 14.470 | 34.610 | GuardArea2_2 | Bot_NanoGuardPos | - |
| 119 | AirPoint | air_point | -19.500 | 21.000 | 22.980 | Fall_14 | NodeLink | - |
| 120 | Fall_14 | fall_point | -25.440 | 7.500 | 10.510 | Area7 | NodeLink | - |
| 121 | AirPoint | air_point | -27.940 | 7.500 | 17.950 | Fall_11 | NodeLink | - |
| 122 | AirPoint | air_point | 0.380 | 15.000 | 39.950 | Fall_4 | NodeLink | - |
| 123 | AirPoint (1) | air_point | 20.500 | 14.000 | 11.360 | Fall_4 | NodeLink | - |
| 124 | Fall_10 | fall_point | -27.870 | 7.500 | 18.560 | Area7 | NodeLink | - |
| 125 | Fall_6 | fall_point | 18.500 | 14.000 | 5.360 | HouseTop | NodeLink | - |
| 126 | FallPoint | fall_point | -21.840 | 2.650 | 30.760 | AirPoint | - | - |
| 127 | Fall_5 | fall_point | 32.960 | 14.000 | -5.080 | Area4 | NodeLink | - |
| 128 | FallPoint | fall_point | 10.050 | 5.000 | -3.510 | AirPoint | - | - |
| 129 | 1 (1) | guard_pos | 34.360 | 13.700 | -2.960 | GuardArea1_3 | Bot_NanoGuardPos | - |
| 130 | Fall_9 | fall_point | -18.370 | 15.000 | 32.030 | Area1 | NodeLink | - |
| 131 | Fall_2 | fall_point | 32.960 | 14.000 | 7.040 | Area4 | NodeLink | - |
| 132 | 1 (1) | guard_pos | -3.950 | 14.290 | 38.830 | GuardArea2_1 | Bot_NanoGuardPos | - |
| 133 | AirPoint | air_point | 9.500 | 14.000 | 13.360 | Fall_1 | NodeLink/Bot_JumpLink | - |
| 134 | 1 | guard_pos | 33.610 | 13.700 | -10.950 | GuardArea1_4 | Bot_NanoGuardPos | - |
| 135 | AirPoint | air_point | 18.500 | 14.000 | 10.360 | Fall_5 | NodeLink | - |
| 136 | 1 (4) | guard_pos | -18.380 | 14.470 | 32.910 | GuardArea2_2 | Bot_NanoGuardPos | - |
| 137 | AirPoint | air_point | -22.260 | 15.000 | 37.810 | Fall_10 | NodeLink | - |
| 138 | FallPoint | fall_point | 15.330 | 5.000 | -3.510 | AirPoint | - | - |
| 139 | FallPoint | fall_point | 10.050 | 5.000 | 2.480 | AirPoint | - | - |
| 140 | AirPoint | air_point | 8.250 | 13.500 | -19.360 | Fall_2 | NodeLink | - |
| 141 | Fall_8 | fall_point | 13.790 | 20.390 | -44.500 | Area6 | NodeLink | - |
| 142 | FallPoint | fall_point | 17.890 | 6.461 | -12.030 | AirPoint | - | - |
| 143 | AirPoint | air_point | 10.050 | 13.000 | 0.230 | Fall_13 | NodeLink | - |
| 144 | Fall_10 | fall_point | -22.260 | 15.000 | 36.810 | Area1 | NodeLink | - |
| 145 | AirPoint | air_point | -27.440 | 7.500 | 21.240 | Fall_9 | NodeLink | - |
| 146 | AirPoint | air_point | -25.000 | 7.500 | 15.890 | Fall_5 | NodeLink | - |
| 147 | 1 (4) | guard_pos | 31.090 | 13.700 | 17.140 | GuardArea1_1 | Bot_NanoGuardPos | - |
| 148 | Fall_1 | fall_point | 5.970 | 11.000 | 25.850 | CarTop | NodeLink | - |
| 149 | Fall_6 | fall_point | 17.890 | 11.000 | -24.670 | Area5 | NodeLink | - |
| 150 | Fall_5 | fall_point | 6.660 | 11.000 | 21.970 | CarTop | NodeLink | - |
| 151 | 1 | guard_pos | 33.650 | 13.700 | 10.830 | GuardArea1_2 | Bot_NanoGuardPos | - |
| 152 | Fall_4 | fall_point | -25.000 | 7.500 | 11.550 | Area7 | NodeLink | - |
| 153 | Fall_6 | fall_point | -6.280 | 15.000 | 35.210 | Area1 | NodeLink | - |
| 154 | Fall_3 | fall_point | -34.960 | 10.500 | 5.120 | Area7 | NodeLink | - |
| 155 | Fall_5 | fall_point | 20.750 | 11.000 | -14.510 | Area5 | NodeLink | - |
| 156 | Fall_11 | fall_point | 15.330 | 13.000 | -7.510 | HouseTop | NodeLink | - |
| 157 | AirPoint | air_point | -18.370 | 15.000 | 33.030 | Fall_9 | NodeLink | - |
| 158 | 4 | guard_pos | -8.620 | 17.580 | -9.640 | GuardArea3 | Bot_NanoGuardPos | - |
| 159 | Fall_9 | fall_point | 12.610 | 20.390 | -45.640 | Area6 | NodeLink | - |
| 160 | FallPoint | fall_point | 2.610 | 5.390 | -42.890 | AirPoint | - | - |
| 161 | 1 | guard_pos | 12.430 | 20.060 | -44.040 | GuardArea4_2 | Bot_NanoGuardPos | - |
| 162 | AirPoint | air_point | 18.500 | 14.000 | 7.360 | Fall_6 | NodeLink | - |
| 163 | FallPoint | fall_point | 8.670 | 6.000 | 28.430 | AirPoint | - | - |
| 164 | Fall_1 | fall_point | -1.860 | 17.500 | -9.580 | Area3 | NodeLink | - |
| 165 | 1 (1) | guard_pos | 34.360 | 13.700 | 8.120 | GuardArea1_2 | Bot_NanoGuardPos | - |
| 166 | FallPoint | fall_point | -6.280 | 7.000 | 38.210 | AirPoint | - | - |
| 167 | Fall_9 (2) | fall_point | 8.610 | 20.390 | -45.640 | Area6 | NodeLink | - |
| 168 | AirPoint | air_point | -34.960 | 10.500 | 2.870 | Fall_2 | NodeLink | - |
| 169 | FallPoint | fall_point | 12.610 | 5.390 | -42.890 | AirPoint | - | - |
| 170 | Fall_7 | fall_point | 13.830 | 20.390 | -40.500 | Area6 | NodeLink | - |
| 171 | AirPoint | air_point | 8.610 | 20.390 | -43.890 | Fall_9 (2) | NodeLink | - |
| 172 | FallPoint | fall_point | -27.940 | 3.500 | 15.050 | AirPoint | - | - |
| 173 | AirPoint | air_point | -9.880 | 20.390 | -23.420 | Fall_6 | NodeLink | - |
| 174 | Fall_14 | fall_point | 10.050 | 13.000 | 3.060 | HouseTop | NodeLink | - |
| 175 | Fall_6 | fall_point | -25.000 | 7.500 | 16.830 | Area7 | NodeLink | - |
| 176 | Fall_10 | fall_point | 18.500 | 14.000 | -6.640 | HouseTop | NodeLink | - |
| 177 | Fall_4 | fall_point | 18.500 | 14.000 | 11.360 | HouseTop | NodeLink/NodeLink | - |
| 178 | FallPoint | fall_point | -7.390 | 5.390 | -42.890 | AirPoint | - | - |
| 179 | 1 (4) | guard_pos | -9.210 | 14.290 | 35.550 | GuardArea2_1 | Bot_NanoGuardPos | - |
| 180 | AirPoint | air_point | -21.350 | 21.000 | 25.810 | Fall_12 | NodeLink | - |
| 181 | AirPoint | air_point | 21.500 | 11.000 | -16.220 | Fall_3 | NodeLink | - |
| 182 | Fall_7 | fall_point | 32.960 | 14.000 | -12.620 | Area4 | NodeLink | - |
| 183 | Fall_8 | fall_point | 18.500 | 14.000 | -0.640 | HouseTop | NodeLink | - |
| 184 | 1 (2) | guard_pos | 32.870 | 13.700 | -16.580 | GuardArea1_4 | Bot_NanoGuardPos | - |
| 185 | 1 (7) | guard_pos | 34.090 | 13.700 | 17.140 | GuardArea1_1 | Bot_NanoGuardPos | - |
| 186 | Fall_2 | fall_point | -5.640 | 15.000 | 38.950 | Area1 | NodeLink | - |
| 187 | FallPoint | fall_point | 11.750 | 5.500 | -16.480 | AirPoint | - | - |
| 188 | 1 (3) | guard_pos | -7.350 | 14.290 | 38.520 | GuardArea2_1 | Bot_NanoGuardPos | - |
| 189 | 1 (8) | guard_pos | -14.990 | 14.290 | 35.560 | GuardArea2_1 | Bot_NanoGuardPos | - |
| 190 | AirPoint | air_point | 17.890 | 11.000 | -22.920 | Fall_6 | NodeLink | - |
| 191 | 1 | guard_pos | -0.980 | 17.580 | -10.030 | GuardArea3 | Bot_NanoGuardPos | - |
| 192 | Fall_3 | fall_point | 15.500 | 14.000 | 11.360 | HouseTop | NodeLink | - |
| 193 | 1 (5) | guard_pos | 31.090 | 13.700 | 20.140 | GuardArea1_1 | Bot_NanoGuardPos | - |
| 194 | AirPoint | air_point | 20.750 | 11.000 | -12.760 | Fall_5 | NodeLink | - |
| 195 | FallPoint | fall_point | -22.260 | 3.000 | 39.810 | AirPoint | - | - |
| 196 | FallPoint | fall_point | -1.390 | 5.390 | -42.890 | AirPoint | - | - |
| 197 | FallPoint | fall_point | -21.480 | 2.500 | -3.100 | AirPoint | - | - |
| 198 | FallPoint | fall_point | -18.370 | 7.000 | 35.030 | AirPoint | - | - |
| 199 | Fall_3 | fall_point | -21.480 | 17.500 | -7.100 | Area3 | NodeLink | - |
| 200 | Fall_13 | fall_point | -27.940 | 7.500 | 10.520 | Area7 | NodeLink | - |
| 201 | Fall_7 | fall_point | 18.500 | 14.000 | 2.360 | HouseTop | NodeLink | - |
| 202 | FallPoint | fall_point | 8.540 | 6.000 | 25.320 | AirPoint | - | - |
| 203 | Fall_9 (1) | fall_point | 10.610 | 20.390 | -45.640 | Area6 | NodeLink | - |
| 204 | FallPoint | fall_point | 9.860 | 6.000 | 16.470 | AirPoint | - | - |
| 205 | FallPoint | fall_point | -27.940 | 3.500 | 14.520 | AirPoint | - | - |
| 206 | AirPoint | air_point | -11.030 | 15.000 | 36.210 | Fall_7 | NodeLink | - |
| 207 | AirPoint | air_point | -35.000 | 7.500 | -3.130 | Fall_1 | NodeLink | - |
| 208 | Fall_2 | fall_point | -6.080 | 17.500 | -9.580 | Area3 | NodeLink | - |
| 209 | FallPoint | fall_point | -21.840 | 2.650 | 28.760 | AirPoint | - | - |
| 210 | FallPoint | fall_point | 8.610 | 5.390 | -42.890 | AirPoint | - | - |
| 211 | Fall_3 | fall_point | 21.500 | 11.000 | -17.970 | Area5 | NodeLink | - |
| 212 | FallPoint | fall_point | 10.050 | 5.000 | 10.690 | AirPoint | - | - |
| 213 | FallPoint | fall_point | 0.380 | 7.000 | 41.950 | AirPoint | - | - |
| 214 | Fall_4 | fall_point | 9.750 | 20.000 | -24.480 | Area6 | NodeLink | - |
| 215 | AirPoint | air_point | -22.260 | 15.000 | 33.810 | Fall_11 | NodeLink | - |
| 216 | AirPoint | air_point | -16.250 | 21.000 | 22.980 | Fall_15 | NodeLink | - |
| 217 | 1 (8) | guard_pos | 34.090 | 13.700 | 20.140 | GuardArea1_1 | Bot_NanoGuardPos | - |
| 218 | 1 (9) | guard_pos | -16.610 | 14.290 | 37.980 | GuardArea2_1 | Bot_NanoGuardPos | - |
| 219 | Fall_8 | fall_point | 30.800 | 14.000 | -16.260 | Area4 | NodeLink | - |
| 220 | Fall_5 | fall_point | 18.500 | 14.000 | 8.360 | HouseTop | NodeLink | - |
| 221 | AirPoint | air_point | -9.390 | 20.390 | -43.890 | Fall_9 (11) | NodeLink | - |
| 222 | FallPoint | fall_point | 9.750 | 12.000 | -20.480 | AirPoint | - | - |
| 223 | FallPoint | fall_point | -1.860 | 5.500 | -5.580 | AirPoint | - | - |
| 224 | FallPoint | fall_point | 7.350 | 12.000 | -20.480 | AirPoint | - | - |
| 225 | Fall_2 | fall_point | 8.670 | 11.000 | 23.430 | CarTop | NodeLink | - |
| 226 | FallPoint | fall_point | 4.610 | 5.390 | -42.890 | AirPoint | - | - |
| 227 | FallPoint | fall_point | 0.380 | 7.000 | 40.100 | AirPoint | - | - |
| 228 | AirPoint | air_point | 18.500 | 14.000 | -4.640 | Fall_10 | NodeLink | - |
| 229 | AirPoint | air_point | 21.500 | 11.000 | -21.950 | Fall_1 | NodeLink | - |
| 230 | 1 (3) | guard_pos | 34.550 | 13.700 | 3.860 | GuardArea1_2 | Bot_NanoGuardPos | - |
| 231 | FallPoint | fall_point | 32.960 | 6.000 | 6.760 | AirPoint | - | - |
| 232 | AirPoint | air_point | 8.670 | 11.000 | 25.430 | Fall_2 | NodeLink | - |
| 233 | FallPoint | fall_point | 15.860 | 6.000 | 16.470 | AirPoint | - | - |
| 234 | AirPoint | air_point | -27.940 | 7.500 | 12.270 | Fall_13 | NodeLink | - |
| 235 | FallPoint | fall_point | -34.960 | 3.500 | 9.120 | AirPoint | - | - |
| 236 | FallPoint | fall_point | 32.960 | 6.000 | -8.620 | AirPoint | - | - |
| 237 | 1 (5) | guard_pos | -21.780 | 14.470 | 31.430 | GuardArea2_2 | Bot_NanoGuardPos | - |
| 238 | Fall_7 | fall_point | 17.890 | 11.961 | -16.030 | Area5 | NodeLink | - |
| 239 | FallPoint | fall_point | 13.830 | 5.390 | -33.610 | AirPoint | - | - |
| 240 | AirPoint | air_point | 17.890 | 11.961 | -14.280 | Fall_7 | NodeLink | - |
| 241 | AirPoint | air_point | 4.250 | 13.500 | -19.360 | Fall_1 | NodeLink | - |
| 242 | AirPoint | air_point | 21.500 | 11.000 | -18.810 | Fall_2 | NodeLink | - |
| 243 | FallPoint | fall_point | -9.880 | 4.390 | -18.280 | AirPoint | - | - |
| 244 | AirPoint | air_point | 2.610 | 20.390 | -43.890 | Fall_9 (5) | NodeLink | - |
| 245 | AirPoint | air_point | 10.050 | 13.000 | 4.810 | Fall_14 | NodeLink | - |
| 246 | AirPoint | air_point | 8.540 | 11.000 | 22.320 | Fall_4 | NodeLink | - |
| 247 | AirPoint | air_point | -25.000 | 7.500 | 13.300 | Fall_4 | NodeLink | - |
| 248 | AirPoint | air_point | 32.960 | 14.000 | 8.790 | Fall_2 | NodeLink | - |
| 249 | FallPoint | fall_point | 18.860 | 6.000 | 13.470 | AirPoint | - | - |
| 250 | FallPoint | fall_point | -5.390 | 5.390 | -42.890 | AirPoint | - | - |
| 251 | FallPoint | fall_point | -10.466 | 5.390 | -41.630 | AirPoint | - | - |
| 252 | AirPoint | air_point | -25.260 | 7.500 | 21.170 | Fall_8 | NodeLink | - |
| 253 | FallPoint | fall_point | 13.790 | 5.390 | -37.610 | AirPoint | - | - |
| 254 | AirPoint | air_point | -6.280 | 15.000 | 36.210 | Fall_6 | NodeLink | - |
| 255 | Fall_9 (12) | fall_point | -10.466 | 20.390 | -44.380 | Area6 | NodeLink | - |
| 256 | Fall_9 (5) | fall_point | 2.610 | 20.390 | -45.640 | Area6 | NodeLink | - |
| 257 | AirPoint | air_point | 32.960 | 14.000 | -3.330 | Fall_5 | NodeLink | - |
| 258 | 1 | guard_pos | 8.500 | 20.400 | -23.970 | GuardArea4_1 | Bot_NanoGuardPos | - |
| 259 | FallPoint | fall_point | 10.050 | 5.000 | 7.060 | AirPoint | - | - |
| 260 | Fall_11 | fall_point | -27.940 | 7.500 | 16.200 | Area7 | NodeLink | - |
| 261 | Fall_13 | fall_point | -21.350 | 21.000 | 22.810 | Area1 | NodeLink | - |
| 262 | AirPoint | air_point | 11.220 | 11.000 | 23.420 | Fall_3 | NodeLink | - |
| 263 | Fall_9 (3) | fall_point | 6.610 | 20.390 | -45.640 | Area6 | NodeLink | - |
| 264 | AirPoint | air_point | 6.660 | 11.000 | 23.970 | Fall_5 | NodeLink | - |
| 265 | AirPoint | air_point | 18.500 | 14.000 | 4.360 | Fall_7 | NodeLink | - |
| 266 | 5 (1) | guard_pos | -21.652 | 17.580 | -8.687 | GuardArea3 | Bot_NanoGuardPos | - |
| 267 | Fall_9 (6) | fall_point | 0.610 | 20.390 | -45.640 | Area6 | NodeLink | - |
| 268 | 1 (1) | guard_pos | 12.430 | 20.400 | -24.250 | GuardArea4_1 | Bot_NanoGuardPos | - |
| 269 | 1 (3) | guard_pos | 31.090 | 13.700 | 14.140 | GuardArea1_1 | Bot_NanoGuardPos | - |
| 270 | AirPoint | air_point | -2.370 | 15.000 | 39.950 | Fall_3 | NodeLink | - |
| 271 | 1 | guard_pos | -3.465 | 14.290 | 35.331 | GuardArea2_1 | Bot_NanoGuardPos | - |
| 272 | AirPoint | air_point | 4.610 | 20.390 | -43.890 | Fall_9 (4) | NodeLink | - |
| 273 | Fall_1 | fall_point | 30.550 | 14.000 | 14.080 | Area4 | NodeLink | - |
| 274 | Fall_9 | fall_point | 18.500 | 14.000 | -3.640 | HouseTop | NodeLink | - |
| 275 | Fall_15 | fall_point | -16.250 | 21.000 | 21.980 | Area1 | NodeLink | - |
| 276 | Fall_12 | fall_point | -27.940 | 7.500 | 11.050 | Area7 | NodeLink | - |
| 277 | AirPoint | air_point | -7.390 | 20.390 | -43.890 | Fall_9 (10) | NodeLink | - |
| 278 | AirPoint | air_point | 10.610 | 20.390 | -43.890 | Fall_9 (1) | NodeLink | - |
| 279 | AirPoint | air_point | -34.960 | 10.500 | 6.870 | Fall_3 | NodeLink | - |
| 280 | Fall_3 | fall_point | 32.960 | 14.000 | 2.760 | Area4 | NodeLink | - |
| 281 | Fall_3 | fall_point | 11.220 | 11.000 | 21.420 | CarTop | NodeLink | - |
| 282 | Fall_4 | fall_point | 8.540 | 11.000 | 20.320 | CarTop | NodeLink | - |
| 283 | AirPoint | air_point | 0.610 | 20.390 | -43.890 | Fall_9 (6) | NodeLink | - |
| 284 | FallPoint | fall_point | 25.080 | 6.000 | 11.310 | AirPoint (1) | - | - |
| 285 | AirPoint | air_point | 32.960 | 14.000 | 4.510 | Fall_3 | NodeLink | - |
| 286 | Fall_12 | fall_point | 10.050 | 13.000 | -7.510 | HouseTop | NodeLink | - |
| 287 | FallPoint | fall_point | 30.800 | 6.000 | -12.510 | AirPoint | - | - |
| 288 | 1 (2) | guard_pos | 28.090 | 13.700 | 20.140 | GuardArea1_1 | Bot_NanoGuardPos | - |
| 289 | AirPoint | air_point | -25.440 | 7.500 | 12.260 | Fall_14 | NodeLink | - |
| 290 | FallPoint | fall_point | 12.860 | 6.000 | 16.470 | AirPoint | - | - |
| 291 | 1 (6) | guard_pos | 34.090 | 13.700 | 14.140 | GuardArea1_1 | Bot_NanoGuardPos | - |
| 292 | Fall_12 | fall_point | -21.350 | 21.000 | 24.810 | Area1 | NodeLink | - |
| 293 | FallPoint | fall_point | -34.960 | 3.500 | 5.120 | AirPoint | - | - |
| 294 | AirPoint | air_point | -5.640 | 15.000 | 39.950 | Fall_2 | NodeLink | - |
| 295 | 2 | guard_pos | -4.010 | 17.580 | -9.160 | GuardArea3 | Bot_NanoGuardPos | - |
| 296 | Fall_9 (9) | fall_point | -5.390 | 20.390 | -45.640 | Area6 | NodeLink | - |
| 297 | AirPoint | air_point | 0.380 | 15.000 | 38.100 | Fall_5 | NodeLink | - |
| 298 | 1 (3) | guard_pos | 29.910 | 13.700 | -16.330 | GuardArea1_4 | Bot_NanoGuardPos | - |
| 299 | FallPoint | fall_point | -6.080 | 5.500 | -5.580 | AirPoint | - | - |
| 300 | AirPoint | air_point | 30.800 | 14.000 | -14.760 | Fall_8 | NodeLink | - |
| 301 | FallPoint | fall_point | -2.370 | 7.000 | 41.950 | AirPoint | - | - |
| 302 | Fall_5 | fall_point | -25.000 | 7.500 | 14.140 | Area7 | NodeLink | - |
| 303 | Fall_13 | fall_point | 10.050 | 13.000 | -1.520 | HouseTop | NodeLink | - |
| 304 | FallPoint | fall_point | -25.000 | 3.500 | 15.550 | AirPoint | - | - |
| 305 | FallPoint | fall_point | -22.260 | 3.000 | 37.310 | AirPoint | - | - |
| 306 | Fall_9 (10) | fall_point | -7.390 | 20.390 | -45.640 | Area6 | NodeLink | - |
| 307 | FallPoint | fall_point | -15.490 | 7.000 | 38.210 | AirPoint | - | - |
| 308 | FallPoint | fall_point | 4.250 | 5.500 | -17.110 | AirPoint | - | - |
| 309 | FallPoint | fall_point | 20.750 | 5.500 | -10.510 | AirPoint | - | - |
| 310 | FallPoint | fall_point | 32.960 | 6.000 | 2.880 | AirPoint | - | - |
| 311 | FallPoint | fall_point | -27.440 | 3.500 | 23.490 | AirPoint | - | - |
| 312 | Fall_1 | fall_point | -9.000 | 15.000 | 38.950 | Area1 | NodeLink | - |
| 313 | FallPoint | fall_point | -25.000 | 3.500 | 20.830 | AirPoint | - | - |
| 314 | 1 (4) | guard_pos | -19.050 | 21.090 | 22.290 | GuardArea2_3 | Bot_NanoGuardPos | - |
| 315 | Fall_9 (4) | fall_point | 4.610 | 20.390 | -45.640 | Area6 | NodeLink | - |
| 316 | AirPoint | air_point | 21.500 | 11.000 | -13.370 | Fall_4 | NodeLink | - |
| 317 | AirPoint | air_point | 30.550 | 14.000 | 15.830 | Fall_1 | NodeLink | - |
| 318 | FallPoint | fall_point | 11.220 | 6.000 | 26.420 | AirPoint | - | - |
| 319 | AirPoint | air_point | 15.500 | 14.000 | 13.360 | Fall_3 | NodeLink | - |
| 320 | 1 (1) | guard_pos | -20.050 | 14.470 | 35.440 | GuardArea2_2 | Bot_NanoGuardPos | - |
| 321 | AirPoint | air_point | -10.466 | 20.390 | -42.630 | Fall_9 (12) | NodeLink | - |
| 322 | Fall_1 | fall_point | 9.500 | 14.000 | 11.360 | HouseTop | NodeLink/NodeLink | - |
| 323 | 5 | guard_pos | -21.250 | 17.580 | -5.690 | GuardArea3 | Bot_NanoGuardPos | - |
| 324 | 1 (1) | guard_pos | -1.820 | 17.580 | -6.270 | GuardArea3 | Bot_NanoGuardPos | - |
| 325 | AirPoint | air_point | -25.000 | 7.500 | 18.580 | Fall_6 | NodeLink | - |

## 4. 线表（258 条）

| # | 名称 | 类型 | 起点X | 起点Y | 起点Z | 终点对象 | 终点X | 终点Y | 终点Z | 父级 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Fall_7 | link | -11.030 | 15.000 | 35.210 | AirPoint | -11.030 | 15.000 | 36.210 | Area1 | NodeLink |
| 2 | AirPoint | link | -1.390 | 20.390 | -43.890 | FallPoint | -1.390 | 5.390 | -42.890 | Fall_9 (7) | NodeLink |
| 3 | AirPoint | link | 12.500 | 14.000 | 13.360 | FallPoint | 12.860 | 6.000 | 16.470 | Fall_2 | NodeLink |
| 4 | Fall_3 | link | -2.370 | 15.000 | 38.950 | AirPoint | -2.370 | 15.000 | 39.950 | Area1 | NodeLink |
| 5 | 1 (2) | link | -3.750 | 11.300 | -21.910 | 1 (3) | -6.380 | 12.890 | -21.910 | Area6 | NodeLink |
| 6 | Fall_6 | link | 32.960 | 14.000 | -8.840 | AirPoint | 32.960 | 14.000 | -7.090 | Area4 | NodeLink |
| 7 | G2 | link | -48.850 | 2.913 | 2.261 | 1 | -47.250 | 4.913 | 2.261 | 1 | Bot_JumpLink/NodeLink |
| 8 | AirPoint | link | -3.390 | 20.390 | -43.890 | FallPoint | -3.390 | 5.390 | -42.890 | Fall_9 (8) | NodeLink |
| 9 | 1 (1) | link | 25.700 | 8.500 | 16.250 | 1 (2) | 25.700 | 10.500 | 18.500 | JumpArea2 | Bot_JumpLink/NodeLink |
| 10 | 2 (3) | link | 18.000 | 13.000 | -9.200 | 2 (2) | 18.000 | 12.000 | -13.000 | Area5 | Bot_JumpLink |
| 11 | Ground3 | link | 22.680 | 6.880 | -5.150 | 1 | 20.030 | 8.520 | -5.070 | JumpArea1 | Bot_JumpLink/NodeLink |
| 12 | Fall_9 (8) | link | -3.390 | 20.390 | -45.640 | AirPoint | -3.390 | 20.390 | -43.890 | Area6 | NodeLink |
| 13 | 2 | link | 5.250 | 18.500 | -23.400 | 3 | 5.250 | 20.500 | -24.550 | Area6 | Bot_JumpLink/NodeLink |
| 14 | Fall_9 (11) | link | -9.390 | 20.390 | -45.640 | AirPoint | -9.390 | 20.390 | -43.890 | Area6 | NodeLink |
| 15 | 1 (2) | link | 20.750 | 11.000 | -25.000 | 1 (1) | 21.600 | 11.000 | -27.000 | Area5 | NodeLink |
| 16 | Ground1 | link | 23.490 | 6.750 | 14.710 | 1 (1) | 25.700 | 8.500 | 16.250 | JumpArea2 | Bot_JumpLink/NodeLink/NodeLink |
| 17 | Fall_2 | link | 12.500 | 14.000 | 11.360 | AirPoint | 12.500 | 14.000 | 13.360 | HouseTop | NodeLink |
| 18 | Fall_8 | link | -15.490 | 15.000 | 35.210 | AirPoint | -15.490 | 15.000 | 36.210 | Area1 | NodeLink |
| 19 | Fall_15 | link | 10.050 | 13.000 | 6.690 | AirPoint | 10.050 | 13.000 | 8.440 | HouseTop | NodeLink |
| 20 | Fall_3 | link | 11.750 | 13.500 | -20.480 | AirPoint | 11.750 | 13.500 | -18.730 | Area6 | NodeLink |
| 21 | Ground3 | link | 6.270 | 6.000 | 33.100 | 1 (1) | 6.620 | 8.000 | 31.120 | JumpArea3 | Bot_JumpLink/NodeLink |
| 22 | Fall_2 | link | -34.960 | 10.500 | 1.120 | AirPoint | -34.960 | 10.500 | 2.870 | Area7 | NodeLink |
| 23 | AirPoint | link | -15.490 | 15.000 | 36.210 | FallPoint | -15.490 | 7.000 | 38.210 | Fall_8 | NodeLink |
| 24 | Fall_1 | link | 4.250 | 13.500 | -21.110 | AirPoint | 4.250 | 13.500 | -19.360 | Area6 | NodeLink |
| 25 | Fall_14 | link | -19.500 | 21.000 | 21.980 | AirPoint | -19.500 | 21.000 | 22.980 | Area1 | NodeLink |
| 26 | 2 (2) | link | 18.000 | 12.000 | -13.000 | 2 (3) | 18.000 | 13.000 | -9.200 | Area5 | Bot_JumpLink/NodeLink |
| 27 | Fall_7 | link | -25.000 | 7.500 | 19.190 | AirPoint | -25.000 | 7.500 | 20.940 | Area7 | NodeLink |
| 28 | AirPoint | link | 13.830 | 20.390 | -38.750 | FallPoint | 13.830 | 5.390 | -33.610 | Fall_7 | NodeLink |
| 29 | Fall_4 | link | 32.960 | 14.000 | -1.120 | AirPoint | 32.960 | 14.000 | 0.630 | Area4 | NodeLink |
| 30 | 2 (1) | link | 18.000 | 12.000 | -16.010 | 2 (2) | 18.000 | 12.000 | -13.000 | Area5 | NodeLink |
| 31 | AirPoint | link | 11.750 | 13.500 | -18.730 | FallPoint | 11.750 | 5.500 | -16.480 | Fall_3 | NodeLink |
| 32 | Fall_2 | link | 8.250 | 13.500 | -21.110 | AirPoint | 8.250 | 13.500 | -19.360 | Area6 | NodeLink |
| 33 | AirPoint | link | -25.000 | 7.500 | 20.940 | FallPoint | -25.000 | 3.500 | 23.190 | Fall_7 | NodeLink |
| 34 | AirPoint | link | -27.870 | 7.500 | 20.310 | FallPoint | -27.870 | 3.500 | 22.560 | Fall_10 | NodeLink |
| 35 | 1 (2) | link | 25.700 | 10.500 | 18.500 | 1 (3) | 25.700 | 12.000 | 20.750 | JumpArea2 | Bot_JumpLink/NodeLink |
| 36 | AirPoint | link | -1.860 | 17.500 | -7.830 | FallPoint | -1.860 | 5.500 | -5.580 | Fall_1 | NodeLink |
| 37 | Ground1 | link | 11.120 | 6.000 | 31.120 | 1 | 9.120 | 8.000 | 31.120 | JumpArea3 | Bot_JumpLink/NodeLink |
| 38 | Bottm | link | -0.340 | 6.250 | 35.750 | GameObject | 0.450 | 6.250 | 37.420 | ClimbArea | NodeLink |
| 39 | Fall_1 | link | -35.000 | 7.500 | -4.880 | AirPoint | -35.000 | 7.500 | -3.130 | Area7 | NodeLink |
| 40 | AirPoint | link | 12.610 | 20.390 | -43.890 | FallPoint | 12.610 | 5.390 | -42.890 | Fall_9 | NodeLink |
| 41 | Ground4 | link | 22.000 | 6.500 | 22.600 | 2 | 24.270 | 7.800 | 22.520 | JumpArea2 | Bot_JumpLink/NodeLink |
| 42 | 3 | link | 1.500 | 15.500 | -9.000 | 4 | -0.500 | 17.500 | -8.000 | Area3 | NodeLink/Bot_JumpLink/NodeLink |
| 43 | AirPoint | link | -5.390 | 20.390 | -43.890 | FallPoint | -5.390 | 5.390 | -42.890 | Fall_9 (9) | NodeLink |
| 44 | Fall_9 | link | -27.440 | 7.500 | 19.490 | AirPoint | -27.440 | 7.500 | 21.240 | Area7 | NodeLink |
| 45 | AirPoint | link | 15.330 | 13.000 | -5.760 | FallPoint | 15.330 | 5.000 | -3.510 | Fall_11 | NodeLink |
| 46 | Fall | link | -27.930 | 7.500 | 18.710 | 2 | -33.430 | 10.500 | 18.710 | 2 | Bot_JumpLink |
| 47 | AirPoint | link | -27.940 | 7.500 | 12.800 | FallPoint | -27.940 | 3.500 | 15.050 | Fall_12 | NodeLink |
| 48 | 1 | link | 11.720 | 13.728 | -5.540 | 2 | 9.265 | 13.728 | -6.730 | Jump | NodeLink |
| 49 | Fall_9 (7) | link | -1.390 | 20.390 | -45.640 | AirPoint | -1.390 | 20.390 | -43.890 | Area6 | NodeLink |
| 50 | AirPoint | link | 32.960 | 14.000 | 0.630 | FallPoint | 32.960 | 6.000 | 2.880 | Fall_4 | NodeLink |
| 51 | AirPoint | link | 5.970 | 11.000 | 27.850 | FallPoint | 5.970 | 6.000 | 30.850 | Fall_1 | NodeLink |
| 52 | AirPoint | link | 18.500 | 14.000 | 13.360 | FallPoint | 18.860 | 6.000 | 16.470 | Fall_4 | NodeLink |
| 53 | 1 | link | 1.500 | 13.650 | -3.900 | 2 | 1.500 | 15.500 | -6.000 | Area3 | Bot_JumpLink/NodeLink |
| 54 | 1 (9) | link | -0.750 | 16.500 | -23.400 | 2 | 5.250 | 18.500 | -23.400 | Area6 | Bot_JumpLink/NodeLink/NodeLink |
| 55 | 3 | link | -26.000 | 7.500 | 13.990 | Box | -27.500 | 9.500 | 13.990 | Box | Bot_JumpLink |
| 56 | Fall_5 | link | 0.380 | 15.000 | 37.100 | AirPoint | 0.380 | 15.000 | 38.100 | Area1 | NodeLink |
| 57 | G2 | link | -54.390 | 2.913 | 13.329 | 2 | -52.790 | 4.913 | 13.329 | 2 | Bot_JumpLink/NodeLink |
| 58 | Fall_11 | link | -22.260 | 15.000 | 32.810 | AirPoint | -22.260 | 15.000 | 33.810 | Area1 | NodeLink |
| 59 | AirPoint | link | 18.500 | 14.000 | -1.640 | FallPoint | 18.860 | 6.000 | 1.470 | Fall_9 | NodeLink |
| 60 | Fall_4 | link | 0.380 | 15.000 | 38.950 | AirPoint | 0.380 | 15.000 | 39.950 | Area1 | NodeLink |
| 61 | Area6 | link | 0.250 | 6.000 | -19.000 | 1 | 0.250 | 8.500 | -21.000 | - | Bot_JumpLink/NodeLink |
| 62 | 1 (2) | link | -19.160 | 17.370 | 27.650 | 1 (3) | -16.380 | 19.190 | 27.650 | Area1 | Bot_JumpLink/NodeLink |
| 63 | AirPoint | link | 6.610 | 20.390 | -43.890 | FallPoint | 6.610 | 5.390 | -42.890 | Fall_9 (3) | NodeLink |
| 64 | 1 | link | 18.750 | 11.000 | -20.430 | 2 | 18.000 | 12.000 | -18.010 | 2 | Bot_JumpLink/NodeLink |
| 65 | 6 | link | -48.690 | 10.500 | 16.540 | 5 | -46.000 | 10.500 | 16.000 | Hide | NodeLink |
| 66 | AirPoint | link | 10.050 | 13.000 | 8.440 | FallPoint | 10.050 | 5.000 | 10.690 | Fall_15 | NodeLink |
| 67 | Fall | link | -27.930 | 7.500 | 10.710 | 1 | -33.430 | 10.500 | 10.710 | 1 | Bot_JumpLink |
| 68 | Fall_1 | link | 21.500 | 11.000 | -23.700 | AirPoint | 21.500 | 11.000 | -21.950 | Area5 | NodeLink |
| 69 | AirPoint (1) | link | 7.500 | 14.000 | 11.360 | FallPoint | 2.920 | 6.000 | 11.310 | Fall_1 | NodeLink |
| 70 | AirPoint | link | 9.750 | 20.000 | -22.730 | FallPoint | 9.750 | 12.000 | -20.480 | Fall_4 | NodeLink |
| 71 | Hide | link | -36.500 | 10.500 | 17.000 | 1 | -38.000 | 10.500 | 16.000 | - | NodeLink |
| 72 | AirPoint | link | 18.500 | 14.000 | 1.360 | FallPoint | 18.860 | 6.000 | 4.470 | Fall_8 | NodeLink |
| 73 | 5 | link | 6.610 | 20.500 | -38.500 | 5 | 6.610 | 20.500 | -40.500 | Area6 | NodeLink |
| 74 | Fall_8 | link | -25.260 | 7.500 | 19.420 | AirPoint | -25.260 | 7.500 | 21.170 | Area7 | NodeLink |
| 75 | AirPoint | link | 32.960 | 14.000 | -7.090 | FallPoint | 32.960 | 6.000 | -4.840 | Fall_6 | NodeLink |
| 76 | AirPoint | link | 32.960 | 14.000 | -10.870 | FallPoint | 32.960 | 6.000 | -8.620 | Fall_7 | NodeLink |
| 77 | Fall_6 | link | -9.880 | 20.390 | -25.170 | AirPoint | -9.880 | 20.390 | -23.420 | Area6 | NodeLink |
| 78 | Fall_5 | link | 7.350 | 20.000 | -24.480 | AirPoint | 7.350 | 20.000 | -22.730 | Area6 | NodeLink |
| 79 | AirPoint | link | -21.350 | 21.000 | 23.810 | FallPoint | -21.840 | 2.650 | 28.760 | Fall_13 | NodeLink |
| 80 | AirPoint | link | 10.050 | 13.000 | -5.760 | FallPoint | 10.050 | 5.000 | -3.510 | Fall_12 | NodeLink |
| 81 | Fall_2 | link | 21.500 | 11.000 | -20.560 | AirPoint | 21.500 | 11.000 | -18.810 | Area5 | NodeLink |
| 82 | 1 (3) | link | -16.380 | 19.190 | 27.650 | 1 (4) | -16.380 | 21.170 | 25.420 | Area1 | Bot_JumpLink/NodeLink |
| 83 | Fall_4 | link | 21.500 | 11.000 | -15.120 | AirPoint | 21.500 | 11.000 | -13.370 | Area5 | NodeLink |
| 84 | 2 | link | 9.620 | 12.022 | 17.790 | JumpLink1 | 9.740 | 13.680 | 15.580 | JumpLink1 | Bot_JumpLink/NodeLink |
| 85 | AirPoint | link | 7.350 | 20.000 | -22.730 | FallPoint | 7.350 | 12.000 | -20.480 | Fall_5 | NodeLink |
| 86 | AirPoint | link | -9.000 | 15.000 | 39.950 | FallPoint | -9.000 | 7.000 | 41.950 | Fall_1 | NodeLink |
| 87 | AirPoint | link | -21.480 | 17.500 | -5.350 | FallPoint | -21.480 | 2.500 | -3.100 | Fall_3 | NodeLink |
| 88 | Ground2 | link | 9.440 | 6.000 | 33.090 | 1 | 9.120 | 8.000 | 31.120 | JumpArea3 | Bot_JumpLink/NodeLink |
| 89 | JumpArea1 | link | 20.030 | 8.520 | -2.070 | 1 | 20.030 | 8.520 | -5.070 | - | NodeLink |
| 90 | AirPoint | link | -6.080 | 17.500 | -7.830 | FallPoint | -6.080 | 5.500 | -5.580 | Fall_2 | NodeLink |
| 91 | AirPoint | link | 13.790 | 20.390 | -42.750 | FallPoint | 13.790 | 5.390 | -37.610 | Fall_8 | NodeLink |
| 92 | 2 (1) | link | 6.620 | 10.000 | 28.870 | 3 (1) | 6.620 | 12.000 | 27.620 | JumpArea3 | Bot_JumpLink/NodeLink |
| 93 | AirPoint | link | -19.500 | 21.000 | 22.980 | FallPoint | -19.990 | 2.650 | 27.930 | Fall_14 | NodeLink |
| 94 | Fall_14 | link | -25.440 | 7.500 | 10.510 | AirPoint | -25.440 | 7.500 | 12.260 | Area7 | NodeLink |
| 95 | AirPoint | link | -27.940 | 7.500 | 17.950 | FallPoint | -27.940 | 3.500 | 20.200 | Fall_11 | NodeLink |
| 96 | AirPoint | link | 0.380 | 15.000 | 39.950 | FallPoint | 0.380 | 7.000 | 41.950 | Fall_4 | NodeLink |
| 97 | AirPoint (1) | link | 20.500 | 14.000 | 11.360 | FallPoint | 25.080 | 6.000 | 11.310 | Fall_4 | NodeLink |
| 98 | Fall_10 | link | -27.870 | 7.500 | 18.560 | AirPoint | -27.870 | 7.500 | 20.310 | Area7 | NodeLink |
| 99 | Box | link | -27.500 | 9.500 | 13.990 | 3 | -26.000 | 7.500 | 13.990 | Area7 | NodeLink/NodeLink/NodeLink |
| 100 | Fall_6 | link | 18.500 | 14.000 | 5.360 | AirPoint | 18.500 | 14.000 | 7.360 | HouseTop | NodeLink |
| 101 | Ground5 | link | 3.200 | 6.000 | 29.580 | 4 | 4.320 | 8.300 | 27.120 | JumpArea3 | Bot_JumpLink/NodeLink |
| 102 | Fall_5 | link | 32.960 | 14.000 | -5.080 | AirPoint | 32.960 | 14.000 | -3.330 | Area4 | NodeLink |
| 103 | Fall_9 | link | -18.370 | 15.000 | 32.030 | AirPoint | -18.370 | 15.000 | 33.030 | Area1 | NodeLink |
| 104 | Fall_2 | link | 32.960 | 14.000 | 7.040 | AirPoint | 32.960 | 14.000 | 8.790 | Area4 | NodeLink |
| 105 | AirPoint | link | 9.500 | 14.000 | 13.360 | FallPoint | 9.860 | 6.000 | 16.470 | Fall_1 | NodeLink/Bot_JumpLink |
| 106 | 4 | link | 4.320 | 8.300 | 27.120 | 4 (1) | 4.320 | 10.040 | 24.830 | JumpArea3 | Bot_JumpLink/NodeLink |
| 107 | AirPoint | link | 18.500 | 14.000 | 10.360 | FallPoint | 18.860 | 6.000 | 13.470 | Fall_5 | NodeLink |
| 108 | AirPoint | link | -22.260 | 15.000 | 37.810 | FallPoint | -22.260 | 3.000 | 39.810 | Fall_10 | NodeLink |
| 109 | 1 (2) (2) | link | 23.240 | 10.500 | 20.765 | 1 (3) | 25.700 | 12.000 | 20.750 | JumpArea2 | Bot_JumpLink/NodeLink/NodeLink/NodeLink |
| 110 | AirPoint | link | 8.250 | 13.500 | -19.360 | FallPoint | 8.250 | 5.500 | -17.110 | Fall_2 | NodeLink |
| 111 | 1 (4) | link | -8.750 | 14.500 | -22.500 | 1 (5) | -8.750 | 16.500 | -23.400 | Area6 | Bot_JumpLink/NodeLink |
| 112 | Fall_8 | link | 13.790 | 20.390 | -44.500 | AirPoint | 13.790 | 20.390 | -42.750 | Area6 | NodeLink |
| 113 | AirPoint | link | 10.050 | 13.000 | 0.230 | FallPoint | 10.050 | 5.000 | 2.480 | Fall_13 | NodeLink |
| 114 | Fall_10 | link | -22.260 | 15.000 | 36.810 | AirPoint | -22.260 | 15.000 | 37.810 | Area1 | NodeLink |
| 115 | AirPoint | link | -27.440 | 7.500 | 21.240 | FallPoint | -27.440 | 3.500 | 23.490 | Fall_9 | NodeLink |
| 116 | 1 | link | 18.750 | 8.000 | -27.000 | 1 (1) | 21.600 | 11.000 | -27.000 | Area5 | Bot_JumpLink/NodeLink |
| 117 | 4 | link | 3.250 | 13.500 | -23.400 | 1 (1) | -1.750 | 10.000 | -21.910 | Area6 | NodeLink |
| 118 | AirPoint | link | -25.000 | 7.500 | 15.890 | FallPoint | -25.000 | 3.500 | 18.140 | Fall_5 | NodeLink |
| 119 | 1 (1) | link | -1.750 | 10.000 | -21.910 | 1 (2) | -3.750 | 11.300 | -21.910 | Area6 | NodeLink |
| 120 | Fall_1 | link | 5.970 | 11.000 | 25.850 | AirPoint | 5.970 | 11.000 | 27.850 | CarTop | NodeLink |
| 121 | Fall_6 | link | 17.890 | 11.000 | -24.670 | AirPoint | 17.890 | 11.000 | -22.920 | Area5 | NodeLink |
| 122 | 1 | link | -33.430 | 10.500 | 10.710 | Fall | -27.930 | 7.500 | 10.710 | Area7 | NodeLink |
| 123 | Fall_5 | link | 6.660 | 11.000 | 21.970 | AirPoint | 6.660 | 11.000 | 23.970 | CarTop | NodeLink |
| 124 | Fall_4 | link | -25.000 | 7.500 | 11.550 | AirPoint | -25.000 | 7.500 | 13.300 | Area7 | NodeLink |
| 125 | Fall_6 | link | -6.280 | 15.000 | 35.210 | AirPoint | -6.280 | 15.000 | 36.210 | Area1 | NodeLink |
| 126 | Fall_3 | link | -34.960 | 10.500 | 5.120 | AirPoint | -34.960 | 10.500 | 6.870 | Area7 | NodeLink |
| 127 | Fall_5 | link | 20.750 | 11.000 | -14.510 | AirPoint | 20.750 | 11.000 | -12.760 | Area5 | NodeLink |
| 128 | Fall_11 | link | 15.330 | 13.000 | -7.510 | AirPoint | 15.330 | 13.000 | -5.760 | HouseTop | NodeLink |
| 129 | 1 (1) | link | 6.620 | 8.000 | 31.120 | 2 (1) | 6.620 | 10.000 | 28.870 | JumpArea3 | Bot_JumpLink/NodeLink |
| 130 | AirPoint | link | -18.370 | 15.000 | 33.030 | FallPoint | -18.370 | 7.000 | 35.030 | Fall_9 | NodeLink |
| 131 | Ground3 | link | 23.830 | 6.500 | 24.860 | 2 | 24.270 | 7.800 | 22.520 | JumpArea2 | Bot_JumpLink/NodeLink |
| 132 | 1 | link | 9.120 | 8.000 | 31.120 | 2 | 9.120 | 10.000 | 28.870 | JumpArea3 | Bot_JumpLink/NodeLink/NodeLink |
| 133 | Fall_9 | link | 12.610 | 20.390 | -45.640 | AirPoint | 12.610 | 20.390 | -43.890 | Area6 | NodeLink |
| 134 | AirPoint | link | 18.500 | 14.000 | 7.360 | FallPoint | 18.860 | 6.000 | 10.470 | Fall_6 | NodeLink |
| 135 | Fall_1 | link | -1.860 | 17.500 | -9.580 | AirPoint | -1.860 | 17.500 | -7.830 | Area3 | NodeLink |
| 136 | Fall_9 (2) | link | 8.610 | 20.390 | -45.640 | AirPoint | 8.610 | 20.390 | -43.890 | Area6 | NodeLink |
| 137 | AirPoint | link | -34.960 | 10.500 | 2.870 | FallPoint | -34.960 | 3.500 | 5.120 | Fall_2 | NodeLink |
| 138 | Fall_7 | link | 13.830 | 20.390 | -40.500 | AirPoint | 13.830 | 20.390 | -38.750 | Area6 | NodeLink |
| 139 | AirPoint | link | 8.610 | 20.390 | -43.890 | FallPoint | 8.610 | 5.390 | -42.890 | Fall_9 (2) | NodeLink |
| 140 | 1 (3) | link | -6.380 | 12.890 | -21.910 | 1 (4) | -8.750 | 14.500 | -22.500 | Area6 | NodeLink/Bot_JumpLink |
| 141 | JumpLink | link | 17.860 | 11.000 | -21.720 | Other | 11.860 | 13.000 | -21.720 | Area5 | Bot_JumpLink |
| 142 | AirPoint | link | -9.880 | 20.390 | -23.420 | FallPoint | -9.880 | 4.390 | -18.280 | Fall_6 | NodeLink |
| 143 | Fall_14 | link | 10.050 | 13.000 | 3.060 | AirPoint | 10.050 | 13.000 | 4.810 | HouseTop | NodeLink |
| 144 | Fall_6 | link | -25.000 | 7.500 | 16.830 | AirPoint | -25.000 | 7.500 | 18.580 | Area7 | NodeLink |
| 145 | Other | link | 11.860 | 13.000 | -21.720 | JumpLink | 17.860 | 11.000 | -21.720 | JumpLink | NodeLink |
| 146 | Fall_10 | link | 18.500 | 14.000 | -6.640 | AirPoint | 18.500 | 14.000 | -4.640 | HouseTop | NodeLink |
| 147 | Fall_4 | link | 18.500 | 14.000 | 11.360 | AirPoint (1) | 20.500 | 14.000 | 11.360 | HouseTop | NodeLink/NodeLink |
| 148 | 2 | link | 1.500 | 15.500 | -6.000 | 4 | -0.500 | 17.500 | -8.000 | Area3 | NodeLink/Bot_JumpLink |
| 149 | AirPoint | link | -21.350 | 21.000 | 25.810 | FallPoint | -21.840 | 2.650 | 30.760 | Fall_12 | NodeLink |
| 150 | 0 | link | 1.500 | 13.070 | -1.530 | 1 | 1.500 | 13.650 | -3.900 | Area3 | NodeLink |
| 151 | AirPoint | link | 21.500 | 11.000 | -16.220 | FallPoint | 21.500 | 5.500 | -13.970 | Fall_3 | NodeLink |
| 152 | Fall_7 | link | 32.960 | 14.000 | -12.620 | AirPoint | 32.960 | 14.000 | -10.870 | Area4 | NodeLink |
| 153 | Fall_8 | link | 18.500 | 14.000 | -0.640 | AirPoint | 18.500 | 14.000 | 1.360 | HouseTop | NodeLink |
| 154 | 4 (1) | link | 4.320 | 10.040 | 24.830 | 4 (2) | 5.740 | 11.390 | 25.570 | JumpArea3 | Bot_JumpLink/NodeLink |
| 155 | GameObject | link | 9.140 | 12.022 | 20.440 | 2 | 9.620 | 12.022 | 17.790 | JumpLink1 | NodeLink |
| 156 | Fall_2 | link | -5.640 | 15.000 | 38.950 | AirPoint | -5.640 | 15.000 | 39.950 | Area1 | NodeLink |
| 157 | G1 | link | -49.540 | 2.913 | 13.329 | 2 | -52.790 | 4.913 | 13.329 | 2 | Bot_JumpLink/NodeLink |
| 158 | AirPoint | link | 17.890 | 11.000 | -22.920 | FallPoint | 17.890 | 5.500 | -20.670 | Fall_6 | NodeLink |
| 159 | Fall_3 | link | 15.500 | 14.000 | 11.360 | AirPoint | 15.500 | 14.000 | 13.360 | HouseTop | NodeLink |
| 160 | AirPoint | link | 20.750 | 11.000 | -12.760 | FallPoint | 20.750 | 5.500 | -10.510 | Fall_5 | NodeLink |
| 161 | Top | link | 0.884 | 14.250 | 32.608 | 2 (5) | -1.810 | 15.250 | 33.500 | ClimbArea | NodeLink/NodeLink |
| 162 | Fall_3 | link | -21.480 | 17.500 | -7.100 | AirPoint | -21.480 | 17.500 | -5.350 | Area3 | NodeLink |
| 163 | Fall_13 | link | -27.940 | 7.500 | 10.520 | AirPoint | -27.940 | 7.500 | 12.270 | Area7 | NodeLink |
| 164 | Fall_7 | link | 18.500 | 14.000 | 2.360 | AirPoint | 18.500 | 14.000 | 4.360 | HouseTop | NodeLink |
| 165 | Fall_9 (1) | link | 10.610 | 20.390 | -45.640 | AirPoint | 10.610 | 20.390 | -43.890 | Area6 | NodeLink |
| 166 | AirPoint | link | -11.030 | 15.000 | 36.210 | FallPoint | -11.030 | 7.000 | 38.210 | Fall_7 | NodeLink |
| 167 | Ground | link | 16.750 | 5.500 | -27.000 | 1 | 18.750 | 8.000 | -27.000 | Area5 | Bot_JumpLink/NodeLink |
| 168 | AirPoint | link | -35.000 | 7.500 | -3.130 | FallPoint | -35.000 | 3.500 | -0.880 | Fall_1 | NodeLink |
| 169 | Fall_2 | link | -6.080 | 17.500 | -9.580 | AirPoint | -6.080 | 17.500 | -7.830 | Area3 | NodeLink |
| 170 | Fall_3 | link | 21.500 | 11.000 | -17.970 | AirPoint | 21.500 | 11.000 | -16.220 | Area5 | NodeLink |
| 171 | 2 | link | 19.590 | 10.850 | -7.330 | 3 | 18.264 | 12.756 | -7.330 | JumpArea1 | Bot_JumpLink/NodeLink |
| 172 | Fall_4 | link | 9.750 | 20.000 | -24.480 | AirPoint | 9.750 | 20.000 | -22.730 | Area6 | NodeLink |
| 173 | AirPoint | link | -22.260 | 15.000 | 33.810 | FallPoint | -22.260 | 3.000 | 37.310 | Fall_11 | NodeLink |
| 174 | AirPoint | link | -16.250 | 21.000 | 22.980 | FallPoint | -16.740 | 2.650 | 27.930 | Fall_15 | NodeLink |
| 175 | Ground4 | link | 4.390 | 6.000 | 31.930 | 1 (1) | 6.620 | 8.000 | 31.120 | JumpArea3 | Bot_JumpLink/NodeLink |
| 176 | 2 | link | 20.390 | 11.000 | -17.850 | 2 | 18.000 | 12.000 | -18.010 | 2 | Bot_JumpLink/NodeLink |
| 177 | Fall_8 | link | 30.800 | 14.000 | -16.260 | AirPoint | 30.800 | 14.000 | -14.760 | Area4 | NodeLink |
| 178 | Fall_5 | link | 18.500 | 14.000 | 8.360 | AirPoint | 18.500 | 14.000 | 10.360 | HouseTop | NodeLink |
| 179 | AirPoint | link | -9.390 | 20.390 | -43.890 | FallPoint | -9.390 | 5.390 | -42.890 | Fall_9 (11) | NodeLink |
| 180 | Ground2 | link | 25.100 | 6.750 | 12.180 | 1 | 25.700 | 6.750 | 14.250 | JumpArea2 | NodeLink |
| 181 | Fall_2 | link | 8.670 | 11.000 | 23.430 | AirPoint | 8.670 | 11.000 | 25.430 | CarTop | NodeLink |
| 182 | AirPoint | link | 18.500 | 14.000 | -4.640 | FallPoint | 18.860 | 6.000 | -1.530 | Fall_10 | NodeLink |
| 183 | AirPoint | link | 21.500 | 11.000 | -21.950 | FallPoint | 21.500 | 5.500 | -19.700 | Fall_1 | NodeLink |
| 184 | 6 | link | 3.500 | 15.500 | -9.000 | 3 | 1.500 | 15.500 | -9.000 | Area3 | Bot_JumpLink |
| 185 | AirPoint | link | 8.670 | 11.000 | 25.430 | FallPoint | 8.670 | 6.000 | 28.430 | Fall_2 | NodeLink |
| 186 | AirPoint | link | -27.940 | 7.500 | 12.270 | FallPoint | -27.940 | 3.500 | 14.520 | Fall_13 | NodeLink |
| 187 | Ground2 | link | 22.680 | 6.880 | -2.150 | JumpArea1 | 20.030 | 8.520 | -2.070 | JumpArea1 | Bot_JumpLink/NodeLink |
| 188 | 2 | link | 9.120 | 10.000 | 28.870 | 3 | 9.120 | 12.000 | 27.620 | JumpArea3 | Bot_JumpLink/NodeLink/NodeLink |
| 189 | Fall_7 | link | 17.890 | 11.961 | -16.030 | AirPoint | 17.890 | 11.961 | -14.280 | Area5 | NodeLink |
| 190 | AirPoint | link | 17.890 | 11.961 | -14.280 | FallPoint | 17.890 | 6.461 | -12.030 | Fall_7 | NodeLink |
| 191 | AirPoint | link | 4.250 | 13.500 | -19.360 | FallPoint | 4.250 | 5.500 | -17.110 | Fall_1 | NodeLink |
| 192 | AirPoint | link | 21.500 | 11.000 | -18.810 | FallPoint | 21.500 | 5.500 | -16.560 | Fall_2 | NodeLink |
| 193 | AirPoint | link | 2.610 | 20.390 | -43.890 | FallPoint | 2.610 | 5.390 | -42.890 | Fall_9 (5) | NodeLink |
| 194 | 3 (0) | link | 7.250 | 20.500 | -25.000 | 3 | 5.250 | 20.500 | -24.550 | Area6 | NodeLink |
| 195 | AirPoint | link | 10.050 | 13.000 | 4.810 | FallPoint | 10.050 | 5.000 | 7.060 | Fall_14 | NodeLink |
| 196 | AirPoint | link | 8.540 | 11.000 | 22.320 | FallPoint | 8.540 | 6.000 | 25.320 | Fall_4 | NodeLink |
| 197 | G1 | link | -44.000 | 2.913 | 2.261 | 1 | -47.250 | 4.913 | 2.261 | 1 | Bot_JumpLink/NodeLink |
| 198 | AirPoint | link | -25.000 | 7.500 | 13.300 | FallPoint | -25.000 | 3.500 | 15.550 | Fall_4 | NodeLink |
| 199 | AirPoint | link | 32.960 | 14.000 | 8.790 | FallPoint | 32.960 | 6.000 | 11.040 | Fall_2 | NodeLink |
| 200 | AirPoint | link | -25.260 | 7.500 | 21.170 | FallPoint | -25.260 | 3.500 | 23.420 | Fall_8 | NodeLink |
| 201 | AirPoint | link | -6.280 | 15.000 | 36.210 | FallPoint | -6.280 | 7.000 | 38.210 | Fall_6 | NodeLink |
| 202 | Fall_9 (12) | link | -10.466 | 20.390 | -44.380 | AirPoint | -10.466 | 20.390 | -42.630 | Area6 | NodeLink |
| 203 | Fall_9 (5) | link | 2.610 | 20.390 | -45.640 | AirPoint | 2.610 | 20.390 | -43.890 | Area6 | NodeLink |
| 204 | AirPoint | link | 32.960 | 14.000 | -3.330 | FallPoint | 32.960 | 6.000 | -1.080 | Fall_5 | NodeLink |
| 205 | Fall_11 | link | -27.940 | 7.500 | 16.200 | AirPoint | -27.940 | 7.500 | 17.950 | Area7 | NodeLink |
| 206 | Fall_13 | link | -21.350 | 21.000 | 22.810 | AirPoint | -21.350 | 21.000 | 23.810 | Area1 | NodeLink |
| 207 | 5 | link | 3.500 | 15.500 | -6.000 | 6 | 3.500 | 15.500 | -9.000 | Area3 | NodeLink/Bot_JumpLink |
| 208 | AirPoint | link | 11.220 | 11.000 | 23.420 | FallPoint | 11.220 | 6.000 | 26.420 | Fall_3 | NodeLink |
| 209 | 2 | link | -33.430 | 10.500 | 18.710 | Fall | -27.930 | 7.500 | 18.710 | Area7 | NodeLink |
| 210 | 1 | link | 20.030 | 8.520 | -5.070 | 2 | 19.590 | 10.850 | -7.330 | JumpArea1 | Bot_JumpLink/NodeLink |
| 211 | 1 | link | 9.840 | 12.884 | 11.230 | JumpLink1 | 9.740 | 13.680 | 15.580 | JumpLink1 | Bot_JumpLink/NodeLink |
| 212 | Fall_9 (3) | link | 6.610 | 20.390 | -45.640 | AirPoint | 6.610 | 20.390 | -43.890 | Area6 | NodeLink |
| 213 | AirPoint | link | 6.660 | 11.000 | 23.970 | FallPoint | 6.660 | 6.000 | 26.970 | Fall_5 | NodeLink |
| 214 | AirPoint | link | 18.500 | 14.000 | 4.360 | FallPoint | 18.860 | 6.000 | 7.470 | Fall_7 | NodeLink |
| 215 | Fall_9 (6) | link | 0.610 | 20.390 | -45.640 | AirPoint | 0.610 | 20.390 | -43.890 | Area6 | NodeLink |
| 216 | AirPoint | link | -2.370 | 15.000 | 39.950 | FallPoint | -2.370 | 7.000 | 41.950 | Fall_3 | NodeLink |
| 217 | AirPoint | link | 4.610 | 20.390 | -43.890 | FallPoint | 4.610 | 5.390 | -42.890 | Fall_9 (4) | NodeLink |
| 218 | Fall_1 | link | 30.550 | 14.000 | 14.080 | AirPoint | 30.550 | 14.000 | 15.830 | Area4 | NodeLink |
| 219 | Fall_9 | link | 18.500 | 14.000 | -3.640 | AirPoint | 18.500 | 14.000 | -1.640 | HouseTop | NodeLink |
| 220 | Fall_15 | link | -16.250 | 21.000 | 21.980 | AirPoint | -16.250 | 21.000 | 22.980 | Area1 | NodeLink |
| 221 | Fall_12 | link | -27.940 | 7.500 | 11.050 | AirPoint | -27.940 | 7.500 | 12.800 | Area7 | NodeLink |
| 222 | AirPoint | link | -7.390 | 20.390 | -43.890 | FallPoint | -7.390 | 5.390 | -42.890 | Fall_9 (10) | NodeLink |
| 223 | AirPoint | link | 10.610 | 20.390 | -43.890 | FallPoint | 10.610 | 5.390 | -42.890 | Fall_9 (1) | NodeLink |
| 224 | AirPoint | link | -34.960 | 10.500 | 6.870 | FallPoint | -34.960 | 3.500 | 9.120 | Fall_3 | NodeLink |
| 225 | Fall_3 | link | 32.960 | 14.000 | 2.760 | AirPoint | 32.960 | 14.000 | 4.510 | Area4 | NodeLink |
| 226 | Fall_3 | link | 11.220 | 11.000 | 21.420 | AirPoint | 11.220 | 11.000 | 23.420 | CarTop | NodeLink |
| 227 | Fall_4 | link | 8.540 | 11.000 | 20.320 | AirPoint | 8.540 | 11.000 | 22.320 | CarTop | NodeLink |
| 228 | AirPoint | link | 0.610 | 20.390 | -43.890 | FallPoint | 0.610 | 5.390 | -42.890 | Fall_9 (6) | NodeLink |
| 229 | 5 (16) | link | 11.510 | 20.500 | -38.140 | 5 (15) | 12.610 | 20.500 | -40.500 | 5 | NodeLink |
| 230 | 1 (3) | link | 25.700 | 12.000 | 20.750 | 1 (4) | 28.450 | 13.820 | 20.959 | JumpArea2 | Bot_JumpLink/NodeLink |
| 231 | AirPoint | link | 32.960 | 14.000 | 4.510 | FallPoint | 32.960 | 6.000 | 6.760 | Fall_3 | NodeLink |
| 232 | Fall_12 | link | 10.050 | 13.000 | -7.510 | AirPoint | 10.050 | 13.000 | -5.760 | HouseTop | NodeLink |
| 233 | 1 (1) | link | -19.160 | 15.480 | 29.800 | 1 (2) | -19.160 | 17.370 | 27.650 | Area1 | Bot_JumpLink/NodeLink |
| 234 | AirPoint | link | -25.440 | 7.500 | 12.260 | FallPoint | -25.440 | 3.500 | 14.510 | Fall_14 | NodeLink |
| 235 | Fall_12 | link | -21.350 | 21.000 | 24.810 | AirPoint | -21.350 | 21.000 | 25.810 | Area1 | NodeLink |
| 236 | AirPoint | link | -5.640 | 15.000 | 39.950 | FallPoint | -5.640 | 7.000 | 41.950 | Fall_2 | NodeLink |
| 237 | Jump | link | 7.790 | 13.830 | -6.730 | 5 | 3.500 | 15.500 | -6.000 | Area3 | Bot_JumpLink/NodeLink |
| 238 | 2 (4) | link | 18.000 | 13.000 | -8.000 | 2 (3) | 18.000 | 13.000 | -9.200 | Area5 | NodeLink |
| 239 | Fall_9 (9) | link | -5.390 | 20.390 | -45.640 | AirPoint | -5.390 | 20.390 | -43.890 | Area6 | NodeLink |
| 240 | 1 | link | 25.700 | 6.750 | 14.250 | 1 (1) | 25.700 | 8.500 | 16.250 | JumpArea2 | Bot_JumpLink/NodeLink |
| 241 | AirPoint | link | 0.380 | 15.000 | 38.100 | FallPoint | 0.380 | 7.000 | 40.100 | Fall_5 | NodeLink |
| 242 | Ground1 | link | 20.030 | 6.880 | 1.090 | JumpArea1 | 20.030 | 8.520 | -2.070 | JumpArea1 | Bot_JumpLink/NodeLink |
| 243 | AirPoint | link | 30.800 | 14.000 | -14.760 | FallPoint | 30.800 | 6.000 | -12.510 | Fall_8 | NodeLink |
| 244 | Fall_5 | link | -25.000 | 7.500 | 14.140 | AirPoint | -25.000 | 7.500 | 15.890 | Area7 | NodeLink |
| 245 | Fall_13 | link | 10.050 | 13.000 | -1.520 | AirPoint | 10.050 | 13.000 | 0.230 | HouseTop | NodeLink |
| 246 | Fall_9 (10) | link | -7.390 | 20.390 | -45.640 | AirPoint | -7.390 | 20.390 | -43.890 | Area6 | NodeLink |
| 247 | 1 | link | 0.250 | 8.500 | -21.000 | 1 (1) | -1.750 | 10.000 | -21.910 | Area6 | NodeLink |
| 248 | Fall_1 | link | -9.000 | 15.000 | 38.950 | AirPoint | -9.000 | 15.000 | 39.950 | Area1 | NodeLink |
| 249 | 1 | link | -27.500 | 7.500 | 11.990 | Box | -27.500 | 9.500 | 13.990 | Box | Bot_JumpLink |
| 250 | Fall_9 (4) | link | 4.610 | 20.390 | -45.640 | AirPoint | 4.610 | 20.390 | -43.890 | Area6 | NodeLink |
| 251 | AirPoint | link | 21.500 | 11.000 | -13.370 | FallPoint | 21.500 | 5.500 | -11.120 | Fall_4 | NodeLink |
| 252 | AirPoint | link | 30.550 | 14.000 | 15.830 | FallPoint | 30.550 | 6.000 | 18.080 | Fall_1 | NodeLink |
| 253 | 1 | link | -19.320 | 14.580 | 31.790 | 1 (1) | -19.160 | 15.480 | 29.800 | Area1 | Bot_JumpLink/NodeLink |
| 254 | AirPoint | link | 15.500 | 14.000 | 13.360 | FallPoint | 15.860 | 6.000 | 16.470 | Fall_3 | NodeLink |
| 255 | AirPoint | link | -10.466 | 20.390 | -42.630 | FallPoint | -10.466 | 5.390 | -41.630 | Fall_9 (12) | NodeLink |
| 256 | Fall_1 | link | 9.500 | 14.000 | 11.360 | AirPoint (1) | 7.500 | 14.000 | 11.360 | HouseTop | NodeLink/NodeLink |
| 257 | AirPoint | link | -25.000 | 7.500 | 18.580 | FallPoint | -25.000 | 3.500 | 20.830 | Fall_6 | NodeLink |
| 258 | 2 | link | -27.500 | 7.500 | 15.990 | Box | -27.500 | 9.500 | 13.990 | Box | Bot_JumpLink |

## 5. 分组结构

```
AirPoint  (88 个)
Area6  (21 个)
(根)  (19 个)
Area1  (15 个)
HouseTop  (15 个)
Area7  (14 个)
GuardArea2_1  (11 个)
GuardArea1_1  (9 个)
Fall_1  (9 个)
Fall_2  (8 个)
Area4  (8 个)
Fall_3  (8 个)
```

## 6. 路点全量坐标（180 个）

路点 = 场景里 tag 等于 20022（WayPoint）的 GameObject。格式：X Y Z 名称。

```
6.610 20.500 -40.500 5
-1.390 20.390 -43.890 AirPoint
12.500 14.000 13.360 AirPoint
-3.750 11.300 -21.910 1 (2)
-1.810 11.250 34.750 2 (2)
0.440 9.250 34.750 1 (1)
-3.390 20.390 -43.890 AirPoint
-1.810 14.500 34.500 2 (4)
25.700 8.500 16.250 1 (1)
18.000 13.000 -9.200 2 (3)
5.250 18.500 -23.400 2
-15.490 15.000 36.210 AirPoint
-6.750 16.500 -23.400 1 (6)
0.440 13.250 34.750 1 (3)
18.000 12.000 -13.000 2 (2)
1.250 20.500 -25.000 3 (2)
13.830 20.390 -38.750 AirPoint
-44.000 10.500 16.000 4
18.000 12.000 -16.010 2 (1)
11.750 13.500 -18.730 AirPoint
-25.000 7.500 20.940 AirPoint
-27.870 7.500 20.310 AirPoint
25.700 10.500 18.500 1 (2)
-1.860 17.500 -7.830 AirPoint
-0.340 6.250 35.750 Bottm
12.610 20.390 -43.890 AirPoint
1.500 15.500 -9.000 3
0.610 20.500 -44.500 5 (5)
-5.390 20.390 -43.890 AirPoint
15.330 13.000 -5.760 AirPoint
-27.940 7.500 12.800 AirPoint
-9.390 20.500 -44.500 5 (10)
-52.790 4.913 13.329 2
32.960 14.000 0.630 AirPoint
5.970 11.000 27.850 AirPoint
18.500 14.000 13.360 AirPoint
0.440 11.250 34.750 1 (2)
9.265 13.728 -6.730 2
1.500 13.650 -3.900 1
-0.750 16.500 -23.400 1 (9)
6.610 20.500 -42.500 5 (1)
18.500 14.000 -1.640 AirPoint
-19.160 17.370 27.650 1 (2)
6.610 20.390 -43.890 AirPoint
24.270 7.800 22.520 2
10.050 13.000 8.440 AirPoint
4.610 20.500 -44.500 5 (3)
7.500 14.000 11.360 AirPoint (1)
-38.000 10.500 16.000 1
9.750 20.000 -22.730 AirPoint
18.500 14.000 1.360 AirPoint
-46.000 10.500 16.000 5
32.960 14.000 -7.090 AirPoint
32.960 14.000 -10.870 AirPoint
-21.350 21.000 23.810 AirPoint
10.050 13.000 -5.760 AirPoint
-40.000 10.500 16.000 2
18.000 12.000 -18.010 2
-16.380 19.190 27.650 1 (3)
-4.750 20.500 -25.000 3 (5)
9.620 12.022 17.790 2
7.350 20.000 -22.730 AirPoint
-9.000 15.000 39.950 AirPoint
-21.480 17.500 -5.350 AirPoint
5.250 20.500 -24.550 3
-1.810 7.250 34.750 2
20.030 8.520 -2.070 JumpArea1
12.610 20.500 -42.500 5 (14)
-6.080 17.500 -7.830 AirPoint
13.790 20.390 -42.750 AirPoint
6.620 10.000 28.870 2 (1)
10.610 20.500 -44.500 5 (12)
6.610 20.500 -44.500 5 (2)
-19.500 21.000 22.980 AirPoint
-27.940 7.500 17.950 AirPoint
-1.810 13.250 34.750 2 (3)
0.380 15.000 39.950 AirPoint
20.500 14.000 11.360 AirPoint (1)
-27.500 9.500 13.990 Box
-6.750 20.500 -25.000 3 (6)
9.500 14.000 13.360 AirPoint
4.320 8.300 27.120 4
18.500 14.000 10.360 AirPoint
8.610 20.500 -44.500 5 (11)
-22.260 15.000 37.810 AirPoint
23.240 10.500 20.765 1 (2) (2)
8.250 13.500 -19.360 AirPoint
-8.750 14.500 -22.500 1 (4)
10.050 13.000 0.230 AirPoint
-1.810 15.250 33.500 2 (5)
-27.440 7.500 21.240 AirPoint
18.750 8.000 -27.000 1
9.740 13.680 15.580 JumpLink1
-25.000 7.500 15.890 AirPoint
-1.750 10.000 -21.910 1 (1)
0.440 14.500 34.500 1 (4)
6.620 8.000 31.120 1 (1)
-18.370 15.000 33.030 AirPoint
9.120 8.000 31.120 1
18.500 14.000 7.360 AirPoint
-8.750 20.500 -25.000 3 (7)
-34.960 10.500 2.870 AirPoint
8.610 20.390 -43.890 AirPoint
-6.380 12.890 -21.910 1 (3)
-2.750 20.500 -25.000 3 (4)
-9.880 20.390 -23.420 AirPoint
-5.390 20.500 -44.500 5 (8)
1.500 15.500 -6.000 2
-21.350 21.000 25.810 AirPoint
21.500 11.000 -16.220 AirPoint
4.320 10.040 24.830 4 (1)
17.890 11.000 -22.920 AirPoint
20.750 11.000 -12.760 AirPoint
-11.030 15.000 36.210 AirPoint
-35.000 7.500 -3.130 AirPoint
-3.390 20.500 -44.500 5 (7)
12.610 20.500 -44.500 5 (13)
19.590 10.850 -7.330 2
-22.260 15.000 33.810 AirPoint
-16.250 21.000 22.980 AirPoint
-7.390 20.500 -44.500 5 (9)
-9.390 20.390 -43.890 AirPoint
18.500 14.000 -4.640 AirPoint
21.500 11.000 -21.950 AirPoint
3.500 15.500 -9.000 6
8.670 11.000 25.430 AirPoint
-27.940 7.500 12.270 AirPoint
9.120 10.000 28.870 2
17.890 11.961 -14.280 AirPoint
4.250 13.500 -19.360 AirPoint
21.600 11.000 -27.000 1 (1)
21.500 11.000 -18.810 AirPoint
2.610 20.390 -43.890 AirPoint
10.050 13.000 4.810 AirPoint
8.540 11.000 22.320 AirPoint
-25.000 7.500 13.300 AirPoint
32.960 14.000 8.790 AirPoint
-2.750 16.500 -23.400 1 (8)
-25.260 7.500 21.170 AirPoint
-6.280 15.000 36.210 AirPoint
32.960 14.000 -3.330 AirPoint
3.500 15.500 -6.000 5
11.220 11.000 23.420 AirPoint
20.030 8.520 -5.070 1
0.440 7.250 34.750 1
0.440 15.250 33.500 1 (5)
6.660 11.000 23.970 AirPoint
18.500 14.000 4.360 AirPoint
2.610 20.500 -44.500 5 (4)
-1.810 9.250 34.750 2 (1)
-2.370 15.000 39.950 AirPoint
4.610 20.390 -43.890 AirPoint
-7.390 20.390 -43.890 AirPoint
10.610 20.390 -43.890 AirPoint
-34.960 10.500 6.870 AirPoint
-42.000 10.500 16.000 3
0.610 20.390 -43.890 AirPoint
25.700 12.000 20.750 1 (3)
32.960 14.000 4.510 AirPoint
-19.160 15.480 29.800 1 (1)
-25.440 7.500 12.260 AirPoint
-0.750 20.500 -25.000 3 (3)
-5.640 15.000 39.950 AirPoint
7.790 13.830 -6.730 Jump
25.700 6.750 14.250 1
0.380 15.000 38.100 AirPoint
23.650 10.500 18.500 1 (2) (1)
30.800 14.000 -14.760 AirPoint
0.250 8.500 -21.000 1
12.610 20.500 -40.500 5 (15)
-47.250 4.913 2.261 1
-4.750 16.500 -23.400 1 (7)
3.250 20.500 -25.000 3 (1)
21.500 11.000 -13.370 AirPoint
30.550 14.000 15.830 AirPoint
15.500 14.000 13.360 AirPoint
-10.466 20.390 -42.630 AirPoint
-8.750 16.500 -23.400 1 (5)
-1.390 20.500 -44.500 5 (6)
-25.000 7.500 18.580 AirPoint
```
