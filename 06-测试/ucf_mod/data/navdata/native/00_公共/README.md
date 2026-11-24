# ① 备份版 · UCF 原生导航数据（只读，永不编辑）

冻结时间：2026-11-17 12:13:28　来源：`D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\ucf_mod`

> 这里只能**只读**：文件带只读属性，`tools/navdata.py` 只往里读、从不往里写。
> 想编辑请改 **② 开发版** `navdata/dev/`；改坏了跑 `python tools/navdata.py restore` 一键还原。

## 收进来的（原生）

一张图一个文件夹（`<序号>_<场景><中文名>\`），里面是 `map.json` + `navmesh.bin`；
不属于任何一张图的（对照表 / 清单 / 说明）都放在 `00_公共\`。

| 文件夹 | 点图 | 关卡 | 中文名 | 节点 | 边 | 指纹 |
| --- | --- | --- | --- | --- | --- | --- |
| 01_TransportShip运输船 | map.json | level1 | 运输船 | 786 | 1391 | n786-57a46e3465c847cb |
| 02_Factory小型工厂 | map.json | level2 | 小型工厂 | 12 | 6 | n12-0e2829fa03c469e3 |
| 03_Cebu_City椰岛之巅 | map.json | level3 | 椰岛之巅 | 2 | 0 | n2-24a647eff15d6ca4 |
| 05_Arena竞技场 | map.json | level5 | 竞技场 | 17 | 24 | n17-f352f68820fae99c |
| 06_GrimReaperKM刀锋寨 | map.json | level6 | 刀锋寨 | 18 | 9 | n18-1976c65d7f7ef2db |
| 08_DesertFort沙漠要塞 | map.json | level7 | 沙漠要塞 | 12 | 7 | n12-17a93cfb246913e1 |
| 09_NanoResort生化酒店 | map.json | level8 | 生化酒店 | 3063 | 5584 | n3063-b04b59b2593bfae4 |
| 10_Nano30_Storm飓风危城 | map.json | level9 | 飓风危城 | 0 | 0 | — |
| 11_Nano_DawnVillage新寂静村 | map.json | level10 | 新寂静村 | 180 | 98 | n180-03b43b7ee737fcdc |

可走面（NavMeshGraph 导出，游戏自己烘焙的网格）：8 张图 ——

- `02_Factory小型工厂/navmesh.bin`　原文件 `navmesh_nm840-40749e0342e84cbd.bin`
- `03_Cebu_City椰岛之巅/navmesh.bin`　原文件 `navmesh_nm532-e33d6b4d26b6983e.bin`
- `04_NY_TM胜利广场/navmesh.bin`　原文件 `navmesh_nm716-497a1a862c4146d9.bin`
- `05_Arena竞技场/navmesh.bin`　原文件 `navmesh_nm683-5a28f3e9cb95f718.bin`
- `06_GrimReaperKM刀锋寨/navmesh.bin`　原文件 `navmesh_nm559-c8d6b4433ee4e22c.bin`
- `07_DeathRing死亡擂台/navmesh.bin`　原文件 `navmesh_nm60-41b97d9f6a766e59.bin`
- `08_DesertFort沙漠要塞/navmesh.bin`　原文件 `navmesh_nm919-1d6104d863c754be.bin`
- `11_Nano_DawnVillage新寂静村/navmesh.bin`　原文件 `navmesh_nm944-a99b40ea454de4a0.bin`

## 怎么用

```
cd tools
python navdata.py status      # 三区在哪、多少文件
python navdata.py verify      # 校验这一版没被动过
python navdata.py restore     # 开发版 <- 这里（还原）
```

清单：`SHA256SUMS.txt`（18 个文件），机器可读信息：`.frozen.json`。
