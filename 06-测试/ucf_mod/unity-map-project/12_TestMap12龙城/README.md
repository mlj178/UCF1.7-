# 龙城 · level12 · TestMap12

| 项 | 值 |
| --- | --- |
| 序号 / 关卡 / 场景名 | 12 / `level12` / `TestMap12` |
| 下拉框显示 | **龙城**（团队模式 · 第 4 项，**追加**，不顶替任何原图） |
| 骨架（借的场景） | `level11` 死亡擂台 DeathRing（原版一个字节没动） |
| Unity | 2020.3.30f1c1 |
| 原始资源 | `src\ForbiddenTD_Classic.GLB`（8.35 MB）+ `unity\Assets\Models\ForbiddenTD_Classic.fbx` |
| 搭建日期 | 2026-11-21 ~ 11-22（原记录：`docs\guide\新增地图_完整工作流.md`） |

## 一、做了什么

借 `level11` 的**整份外壳**，只换外观：

| 类别 | 数量 | 说明 |
| --- | --- | --- |
| 原样保留 | 52 个 MonoBehaviour + 相机 + 灯光 + 2 个出生点标记 + A* 图 + 14 个 BoxCollider | 弹力出场、寻路、观战视角全是白送的 |
| 替换 | 56 / 69 个渲染位的网格与材质；52 个 MeshCollider 的网格 | 紫禁城的几何 |
| 修改 | 56 个 Transform 归零并断开父级；16 个出生点 y：−1.85 → **3.0** | 掉图就死在这一步 |
| 新造 | `sharedassets12.assets` + `.resS` | 56 网格 + 56 材质 + 52 贴图 |

## 二、四个产物（部署包在 `run\gamepatch\12_TestMap12龙城\`）

| 文件 | 字节 | sha256（前 16） | 性质 |
| --- | --- | --- | --- |
| `UnityCrossFire_Data\level12` | 61,960 | `0975B8DCFE366E86` | 新文件 |
| `UnityCrossFire_Data\sharedassets12.assets` | 1,956,352 | `BEEBD29BD32C07D4` | 新文件 |
| `UnityCrossFire_Data\sharedassets12.assets.resS` | 2,518,856 | `8DE5A36B9232354F` | 新文件 |
| `UnityCrossFire_Data\globalgamemanagers` | 1,614,512 | `E36B6EFB79D2E427` | **改造**（原版 1,617,300 / `AFE371A188561D1C`，名册 12 → 13 条） |

**不改** `sharedassets0.assets`（70 MB）：老做法是在里面把第 3 项 `Cebu_City` 换成 `TestMap12`（19 字节），
副作用是顶掉椰岛之巅。现在改成**插件注入第 4 项**（`game_mode = 0` = `GameMode.TeamDeath`，见 dump.cs 第 235472 行），
这张图一个字节都不用动。

## 三、怎么重新构建

```powershell
# 1. Unity 打开工程（不能加 -batchmode）
#    D:\trae_project\ucf1.7-modifier\06-测试\ucf_mod\unity-map-project\12_TestMap12龙城\unity
# 2. 导出（产物 = level0 → level12 + sharedassets0.assets → sharedassets12.assets）
python tools\patch_a.py        # 改名 + 修 .resS 路径（这两步就是"两个字节补丁"）
python tools\repatch.py        # level0 里的外部依赖名
python tools\patch_final.py    # 借 level11 骨架、换网格材质、抬出生点
```

⚠️ 这几个脚本里的路径写死在 `D:\ucf_test_level12\game` 和 `D:\ucf_unity\build`（当时的临时位置），
**它们现在是"证据/存档"，不是"可一键重跑"的脚本**。要重跑，先把 `GAME` / `OUT` / `SRCB` 三个变量改成当前路径。
（下一步会加一个参数化的 `tools\build.py`，把这三个脚本收编进去。）

## 四、已知限制

- **寻路图还是死亡擂台的**（A* 图原样复制），所以人机路线是"死亡擂台的形状"；
- 出生点朝向沿用原图；
- 原版设计里团队模式只有 3 项，我们是第 4 项 —— 如果哪天游戏更新了 UI 布局，要重新验证第 4 项能不能显示出来。

## 五、踩过的坑（按出现概率）

| 现象 | 原因 | 解法 |
| --- | --- | --- |
| 表面全是彩虹噪点 | `.resS` 路径字符串没改（25 → 26 字节） | `patch_a.py` / `repatch.py` |
| 一直在掉 / 视野纯蓝 | 出生点 y 低于模型地面 | 抬 `MapManager` 里 16 个 `SpawnPoint.y` |
| 进图崩溃 | `m_Externals[2]` 或悬空 PPtr（天空盒/反射/光照探针） | `patch_final.py` 里 null external-3 |
| 下拉框看不到新图 | 名册没打通（`globalgamemanagers` 还是 12 条） | 第 13 条 |
