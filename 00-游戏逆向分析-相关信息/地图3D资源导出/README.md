# 地图 3D 资源导出

> 2026-11-23 · 路点工作台 3D 贴图数据  
> 说明文档：`../../06-测试/ucf_mod/docs/guide/地图3D资源导出/需求与执行记录.md`

这个目录集中存放路点工作台 3D 用到的**原始导出工程**和**最终产出**，供后续复用、对比和重新生成。

## 目录

| 目录 | 内容 |
| --- | --- |
| `AssetRipper工程\ExportedProject` | AssetRipper 导出的工程文件（场景 YAML、合并网格、单体网格、材质、贴图；约 1.33 GB）。`ProjectVersion` 为 2020.3.30f1c1，仅作记录；本流程**不需要 Unity 编辑器** |
| `AssetRipper工程\AuxiliaryFiles` | AssetRipper 辅助文件（`path_id_map.json` + 游戏程序集） |
| `工作台数据\web\level1..level11.bin` | 最终 UCFG v2 地形数据（工作台副本） |
| `工作台数据\tex\level1..level11\` | 最终贴图 PNG（工作台副本） |
| `截图\` | 全地图拼图、单图截图、近景、工作台 3D 实测 |

工作台实际读取的是：

```text
06-测试\ucf_mod\geo\web\level1..level11.bin
06-测试\ucf_mod\geo\tex\level1..level11\
```

本目录的 `工作台数据` 是**供别人复用的副本**；如果要让工作台使用，把 `工作台数据\web` 和 `工作台数据\tex` 覆盖到上面的 `geo` 目录即可。

## 代码

转换器只有一份，放在 guide 里：

```text
06-测试\ucf_mod\docs\guide\地图3D资源导出\代码\scene_export2web.py
```

用法：

```powershell
python "D:\trae_project\ucf1.7-modifier\06-测试\ucf_mod\docs\guide\地图3D资源导出\代码\scene_export2web.py" --scene level1 --level level1
```

默认工程目录就是本目录下的 `AssetRipper工程\ExportedProject`；可用 `--project` 覆盖。

## 覆盖范围

- 地图：level1 运输船、level2 小型工厂、level3 椰岛之巅、level4 胜利广场、level5 竞技场、level6 刀锋寨、level7 沙漠要塞、level8 生化酒店、level9 飓风危城、level10 新寂静村、level11 死亡擂台。
- 每张图都有：bin、贴图、工作台实测截图。
- 跳过：`CrossFire/Shadow` 影子代理、`Lit` 灯片、水面、level7 的 3 个 `Leg` 网格。
- `nano30_storm` 没有对应场景，不在本次范围。

## 重新生成

```powershell
# 单张
python "...\代码\scene_export2web.py" --scene level4 --level level4

# 批量
foreach ($n in 2..11) {
  python "...\代码\scene_export2web.py" --scene "level$n" --level "level$n"
}
```

产出会写到 `06-测试\ucf_mod\geo\web` 和 `geo\tex`；如需同步到本资源库，把这两个目录里的 `level*` 复制到 `工作台数据` 即可。
