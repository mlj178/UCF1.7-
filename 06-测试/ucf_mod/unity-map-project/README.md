# 地图工程（unity-map-project）

> **这是什么**：我们自己做的新地图的「原料 + Unity 工程 + 补丁脚本」。
> **不放哪**：不放分发包。用户拿到的是 `run\payload` + `run\gamepatch`，跟这里无关。
> **为什么要在这里**：这些文件是「让龙城重做一遍」的唯一依据。以前它们在 `D:\ucf_unity` 根目录里，
> 不在 git 里，删了就永久没了。2026-11-24 起统一挪进来。

## 一、三处同名

同一张图在三个地方用**同一个文件夹名**（序号 + 场景名 + 中文名）：

| 位置 | 放什么 | 进 git | 进分发包 |
| --- | --- | --- | --- |
| `unity-map-project\12_TestMap12龙城\` | 原料 / Unity 工程 / 补丁脚本 | ✅ | ❌ |
| `run\gamepatch\12_TestMap12龙城\` | 部署用补丁包（成品文件 + patch.json） | ✅ | ✅ |
| `data\navdata\dev\12_TestMap12龙城\` | 点图 / navmesh / 成品路线 | ✅ | ❌（数据从工程端读） |

名字由 `app\core\map_table.py` 从 `docs\guide\07-地图对照表.md` 第一张表生成 —— **表里没这张图，三处名字就对不上**。

## 二、一张图的目录约定

```
12_TestMap12龙城\
├─ README.md        地图档案：来源、骨架、改了什么、哈希、踩坑
├─ map.json         机器读的元数据（关卡 / 场景名 / 中文名 / 模式 / 骨架 / 注入方式）
├─ src\             原料：GLB 原始资源、预览图、glb_info.json
├─ unity\           Unity 工程（只提交 Assets / ProjectSettings / Packages）
│  └─ .gitignore    排除 Library / Temp / Logs / UserSettings / obj
└─ tools\           构建与补丁脚本（这是"源码"，不许只留在别处）
```

## 三、加一张新图（9 步）

1. 复制 `00_模板\` → `NN_<场景名><中文名>\`；
2. 改 `map.json`：`no / level / scene / label / skeleton / game_mode`；
3. 原始资源（GLB/FBX/贴图）丢 `src\`；
4. Unity 2020.3.30f1c1 打开工程，Scene 建好（**不能加 -batchmode**，见《新增地图_完整工作流》§3.2）；
5. 跑 `tools\` 里的构建脚本 → 产物进 `run\gamepatch\NN_...\UnityCrossFire_Data\`；
6. 跑字节补丁脚本（外部依赖名 / .resS 路径），把补丁结果写进 `patch.json`；
7. `tools\verify.py`（或手算哈希）核对：对象数、名册条数、每件文件的 sha256；
8. `docs\guide\07-地图对照表.md` 第一张表加一行（序号 = 显示顺序，不是关卡号）；
9. 控制台「插件开关 → 地图」自动多一行（读 `map.json`），勾上 → 应用 → 进游戏验证。

## 四、注意

- `.gitignore` 里有一条 `/maps/`（旧部署端遗留，锚定 ucf_mod 根目录），**别在根目录建 `maps\`**，会被静默忽略 —— 所以这里叫 `unity-map-project`。
- `Library\` 有 140 MB+，永远不要复制进来；Unity 打开工程会自己重建。
- 工程里的 `.meta` 文件必须一起提交，否则路径 GUID 变了，场景会丢引用。
