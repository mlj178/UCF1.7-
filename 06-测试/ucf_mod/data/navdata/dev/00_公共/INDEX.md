# 原始地图数据集（自动生成，勿手改）

生成时间：2026-11-17 11:14:53

序号 / 关卡 / 中文名 / 场景名的**权威表**在 docs/guide/地图对照表.md（手写、持久）；
本文件只是按那张表整理出来的结果，每次跑脚本都会重写。

| 序号 | 关卡 | 中文名 | 场景名 | 节点 | 边 | 特征 | 文件 | 状态 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | level1 | **运输船** | TransportShip | 786 | 1391 | 16 | 01_TransportShip运输船/map.json | 有数据 |  |
| 02 | level2 | **小型工厂** | Factory | 12 | 6 | 35 | 02_Factory小型工厂/map.json | 有数据 | 样本很小（可能只扫到局部，或这张图的点图本来就只做 node link 端点） |
| 03 | level3 | **椰岛之巅** | Cebu_City | 2 | - | 43 | 03_Cebu_City椰岛之巅/map.json | 有数据 | 样本很小（可能只扫到局部，或这张图的点图本来就只做 node link 端点） |
| 04 | level4 | **胜利广场** | NY_TM | - | - | - | - | 待采集 |  |
| 05 | level5 | **竞技场** | Arena | 17 | 24 | 48 | 05_Arena竞技场/map.json | 有数据 | 样本很小（可能只扫到局部，或这张图的点图本来就只做 node link 端点） |
| 06 | level6 | **刀锋寨** | GrimReaperKM | 18 | 9 | 34 | 06_GrimReaperKM刀锋寨/map.json | 有数据 | 样本很小（可能只扫到局部，或这张图的点图本来就只做 node link 端点） |
| 07 | level11 | **死亡擂台** | DeathRing | - | - | - | - | 待采集 |  |
| 08 | level7 | **沙漠要塞** | DesertFort | 12 | 7 | 46 | 08_DesertFort沙漠要塞/map.json | 有数据 | 样本很小（可能只扫到局部，或这张图的点图本来就只做 node link 端点） |
| 09 | level8 | **生化酒店** | NanoResort | 3063 | 5584 | 118 | 09_NanoResort生化酒店/map.json | 有数据 |  |
| 10 | level9 | **暴风** | Nano30_Storm | - | - | - | - | 待采集 | 隐藏地图，插件注入选图列表 |
| 11 | level10 | **新寂静村** | Nano_DawnVillage | 180 | 98 | 105 | 11_Nano_DawnVillage新寂静村/map.json | 有数据 |  |

## 说明

- **原始**：游戏进图时自己 Scan 出来的 A* 点图。同一张图有多份导出时取**节点最少**的那份，
  因为插件编辑只会往原图上加点，最少的那份最接近原图。
- 文件里的 map.fingerprint 就是游戏套编辑之前算的指纹，也是 nav/<指纹>.txt 用的那个。
- edits_on_top：这份原图之上，游戏现在还套着几条编辑。
- 想让游戏回到原图：删掉 ucf_mod/nav/<指纹>.txt，下次进图就是干净的原始点图。
- 只读还原点：ucf_mod/backup/maps_original_<日期>/（含 sha256 清单）。
- 早先标成「疑似大厅数据」、还没进数据集的导出在 ucf_mod/backup/review_20261116/；
  其中小型工厂那 12 点已证实是 node link 端点（真数据），已经收进数据集。
- 序号/关卡/中文名/场景名以 ucf_mod/docs/guide/地图对照表.md 为准，本文件不定义名字。
