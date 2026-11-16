# 原始地图数据集 + 只读还原点（2026-11-16）

> **序号 / 关卡 / 中文名 / 场景名的权威表**：`ucf_mod/地图对照表.md`（手写、持久，脚本都读它）。
>
> **一句话**：`ucf_mod/maps/` 是游戏自己扫出来的原始导航数据，一张图一份、编号 + 官方中文名；
> `ucf_mod/backup/maps_original_20261116/` 是**只读还原点**（带 sha256 清单）；
> `vis/` 里堆了半个月的历史 JSON 已经全部归档，不再混在一起。

---

## 1. 11 张图：编号 ↔ 关卡 ↔ 中文名

| 序号 | 关卡 | 中文名 | 游戏里的场景名 | 数据 |
| --- | --- | --- | --- | --- |
| 01 | level1 | **运输船** | TransportShip | ✅ 786 点 / 1391 边 / 16 特征 |
| 02 | level2 | **小型工厂** | Factory | ⛔ 现有导出疑似大厅数据（见 §3） |
| 03 | level3 | **椰岛之巅** | Cebu_City | ⚠️ 2 点（白名单保留，样本极小） |
| 04 | level4 | **胜利广场** | NY_TM | ⬜ 待采集 |
| 05 | level5 | **竞技场** | Arena | ⬜ 待采集 |
| 06 | level6 | **刀锋寨** | GrimReaperKM | ⛔ 现有导出疑似大厅数据（见 §3） |
| 07 | level7 | **沙漠要塞** | DesertFort | ⬜ 待采集 |
| 08 | level8 | **生化酒店** | NanoResort | ⬜ 待采集 |
| 09 | level9 | **暴风**（隐藏图） | Nano30_Storm | ⚠️ 694 点（插件铺的点，见 §3） |
| 10 | level10 | **新寂静村** | Nano_DawnVillage | ⬜ 待采集 |
| 11 | level11 | **死亡擂台** | DeathRing | ⛔ 现有导出疑似大厅数据（见 §3） |

同一份表也在 `ucf_mod/maps/_index.json`（给程序看）和 `ucf_mod/maps/INDEX.md`（给人看），
每次跑整理脚本会自动重写。

### 中文名是从哪来的（不是猜的）

1. `UnityCrossFire_Data/sharedassets0.assets` 里有一张**选图表**，每条是「模式名 / 场景名 / 中文名」三元组，例如：

   ```
   TeamDeath   TransportShip  运输船
   Factory     Factory        小型工厂
   Special     Arena          竞技场
   DeathRing   DeathRing      死亡擂台
   Nano4_Terminator  Nano_DawnVillage  新寂静村
   ```

2. 再看每个场景文件里到底写着哪个场景名（`level1` 里能找到 `TransportShip`、`level2` 里是 `Factory`、
   `level3`=`Cebu_City`、`level4`=`NY_TM`、`level5`=`Arena`、`level6`=`GrimReaperKM`、
   `level7`=`DesertFort`、`level8`=`NanoResort`、`level10`=`Nano_DawnVillage`、`level11`=`DeathRing`）。

两边一对，就是上表。`level9` = `Nano30_Storm`，也就是插件往选图列表里插的那张「隐藏地图 暴风」。

---

## 2. 「原始」是怎么定义的

游戏的 A\* 点图是**进图时现扫**的，插件的编辑（`nav/<指纹>.txt`）是**扫描结果之上另加**的。
所以同一张图的多份导出里：

- 编辑只会**加点**（`node add`），或者把点标记成不可走（`node del`，点还在数组里）；
- 因此**节点最少的那份最早、最接近原图**；
- 导出里的 `map.fingerprint` 是**导出那一刻**算的，加过点就会变（n786 → n792 → …），
  但游戏进图算的是**套编辑之前**的指纹（始终是 n786）。

整理脚本按这个规则挑原始，并把「这份原图之上游戏还套着几条编辑」写进索引的 `edits_on_top`。
例如运输船：原始 786 点，`ucf_mod/nav/n786-57a46e3465c847cb.txt` 里有 6 条 `node add`，
所以游戏里实际是 786 + 6 = 792 点。

---

## 3. 现在有什么、缺什么

**有数据（5 张）**：运输船（完整）、暴风、小型工厂、刀锋寨、死亡擂台。

**要注意的两件事**：

1. **暴风不是游戏原图**。这张图官方没做导航（点图是空的），`09_暴风.json` 里 694 个点是**我们插件**
   `navfix` 用向下射线自动铺出来的（文件里 `map.source = "ours"`、`map.origin = "mod-generated"`）。
   拿它当「游戏原始数据」是错的，索引里已经标了「插件铺的点」。
2. **小型工厂 / 刀锋寨 / 死亡擂台只有十几个点**，那是进图时只扫到一小块（不是全图）。
   想补全：进这张图走一圈，再按 `Ctrl+E` 重新导出。

**还没有数据（6 张）**：椰岛之巅、胜利广场、竞技场、沙漠要塞、生化酒店、新寂静村。

### 怎么把缺的补齐（一次跑完）

1. 进游戏，按 `Ctrl+Shift+X` 开**采集模式**（`ucf_mod/collect.flag` 出现；该模式下插件只导出、不改图）；
2. 把缺的 6 张图各进一次（进去停 2~3 秒等点图稳定，插件会自动导出到 `ucf_mod/vis/`）；
3. 退出游戏，双击 `ucf_mod/tools/启动导航编辑器.bat` 那套里的脚本，或者直接命令行：

   ```
   cd ucf_mod/tools
   python organize_maps.py --archive
   ```

4. `ucf_mod/maps/` 会自动多出 `03_椰岛之巅.json` 这些文件，还原点也会一起重建。

> 采集模式开关是 `Ctrl+Shift+X`；如果开了却进图不导出，检查 `ucf_mod/collect.flag` 是否存在、
> 以及 `ucf_mod/ucf_mod.log` 里有没有 `auto-export: graph stable at N nodes`。

---

## 4. 只读还原点怎么用

目录（2026-11-16 生成）：

```
ucf_mod/backup/maps_original_20261116/
├── raw/               游戏 Ctrl+E 导出的原始 JSON（原文件名，逐字节复制）
├── canonical/         整理后的编号版（和 ucf_mod/maps/ 内容一致）
├── MANIFEST.json      每个文件的 sha256 / 指纹 / 节点数 / edits_on_top
└── README.txt         还原说明
```

所有文件带**只读**属性（`-r---`）。校验没被动过：

```
python -c "import hashlib,json,os;r=r'ucf_mod/backup/maps_original_20261116';m=json.load(open(r+'/MANIFEST.json',encoding='utf-8'));[print(k,d['file']) for e in m['maps'] for k in ('raw','canonical') if (d:=e.get(k))]"
```

（上面只是列出清单；要逐文件核对就自己算 sha256 和 MANIFEST 里对一下，2026-11-16 生成时 10 个文件全部一致。）

**还原步骤**：

- 只想看/对比：直接打开 `canonical/` 里的 JSON。
- 想恢复编辑器里的数据：把 `canonical/xx_中文名.json` 复制回 `ucf_mod/maps/`。
- 想让**游戏**也回到原始点图：删掉 `ucf_mod/nav/<指纹>.txt`，下次进图就不再套编辑。
  只删某一个指纹的文件才能只影响那一张图；`nav/names.json` 不受影响。
- 想改备份里的文件：先右键 → 属性 → 去掉「只读」，或者复制一份出来再改。

---

## 5. 以后新导出怎么整理

```
python tools/organize_maps.py               # 整理：编号 + 中文名 + 重建索引 + 备份
python tools/organize_maps.py --archive     # 顺带把 vis/ 清空（搬进 backup/vis_history_<时间>/）
python tools/organize_maps.py --dry         # 只看会做什么，不写任何文件
python tools/organize_maps.py --no-backup   # 不动还原点
python tools/organize_maps.py --no-geo      # 不按地形猜关卡（只认文件名和 names.json）
```

脚本判断「这次导出是哪张图」的顺序：
`nav/names.json` 里的指纹 → 文件/地图名里的 `levelN` → **按地形匹配**（拿节点的位置去比 `geo/*.npz` 的顶点，
命中率 ≥45% 且明显高于第二名才算），所以就算导出名叫 `map_n792-…` 也能认出是运输船。

---

## 6. 在编辑器里看

- 左侧「打开」按 **01…11 序号**排列，每组一个中文名 + 关卡徽标；
- 打开 `01_运输船.json` 时，顶栏会显示 `节点 792`，地图信息里的「节点/边」后面会补一句
  `（原始 786 + 清单 +6）` —— 因为游戏里这张图确实还套着 6 条编辑；
- 从 `maps/` 打开的文件是**只读参考**：编辑器保存时永远写 `ucf_mod/nav/`，不会改 `maps/`。

---

## 7. 这次清理动了什么（可追溯）

| 动作 | 位置 |
| --- | --- |
| 新建原始数据集（5 张） | `ucf_mod/maps/`（+ `_index.json` / `INDEX.md`） |
| 新建只读还原点 | `ucf_mod/backup/maps_original_20261116/`（10 个文件 + 清单） |
| 历史导出归档 | `ucf_mod/backup/vis_history_20261116_122127/`（40 个文件：23 份 JSON + 13 个 `_seen_*` 标记 + 2 个 navmesh + 旧 INDEX.md） |
| 清空 `vis/` | 只留一个 `README.txt` 说明；下次 Ctrl+E 会重新往里写 |
| 更新中文名库 | `ucf_mod/nav/names.json`（11 张图的关卡名 + 场景名别名） |
| 未改动 | `ucf_mod/nav/n786-57a46e3465c847cb.txt`（游戏写的那 6 条编辑，字节未变） |

> 所有原始 JSON 都是**搬走/复制**，没有删任何一份。要找回任何一份历史导出，去归档目录。