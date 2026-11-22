# 三张候选地图 · 资产清单与缺口对比

> **类型：查 + 评估**——回答"这三张图里有什么、能不能加进 UCF、还缺什么"。
> **给谁看**：手里有现成地图资源，想判断哪张值得做、要补多少东西的人。
> **不回答什么**：具体怎么装 Unity、怎么一步步做出 level12（见 [新增地图_完整工作流.md](新增地图_完整工作流.md)）；路点/寻路怎么改（见 [人机与路线设计.md](人机与路线设计.md)）。
> **数据来源**：全部来自**直接解析文件字节**（glTF 头、Unity 序列化文件、GoldSrc BSP 头），不是估的。复现方式见第 9 节。

---

## 0. 结论速览

| 候选 | 位置 | 能直接用吗 | 处理后能用吗 | 主要缺口 | 工作量 |
| --- | --- | --- | --- | --- | --- |
| **A. ForbiddenTD_Classic.GLB** | D:\BaiduNetdiskDownload\ | ❌ | ✅ **已经做出来了** | 碰撞、光照、出生点、寻路 | 低（已完成） |
| **B. DC 挑战版（神秘营地）** | C:\Users\17242\Downloads\DC穿越火线挑战版本\ | ❌ | ✅ 能，但剥得多 | 脚本、NPC、版本升级 | 中 |
| **C. 赛车之城（CS 1.6）** | C:\Users\17242\Downloads\新建文件夹\赛车之城\ | ❌ | ⚠️ 勉强能 | 22 张贴图丢失、光照、比例 | 高 |

**一句话**：A 最省事且已跑通；B 资产最完整、最像 CF；C 是另一个引擎的东西，做得出但性价比最低。

---

## 1. 基准：UCF 一张地图到底由什么组成

看候选之前必须先建立基准，否则"缺什么"无从谈起。
**这一节的数据取自全部 12 个 `levelN`，不是抽样。**

### 1.1 三个文件负责三件事

| 文件 | 实测大小（运输船） | 装什么 |
| --- | --- | --- |
| UnityCrossFire_Data\level1 | 354 KB | **场景**：物体摆放、渲染器、碰撞体、灯光、管理器脚本实例 |
| UnityCrossFire_Data\sharedassets1.assets | 2.04 MB | **本图配套**：材质、角色、装备、各类 Collider |
| UnityCrossFire_Data\resources.assets | 93.09 MB | **全游戏共享池**：1,203 个 Mesh、1,792 张贴图、1,152 个材质 |

> ⚠️ 一个反直觉的事实：**UCF 的地图网格并不在 sharedassetsN 里**。
> 实测 `sharedassets1.assets` 里 Mesh = 0、Texture2D = 0，只有 83 个 Material；
> `sharedassets2` ~ `sharedassets11` 更极端，只有 **2~27 个对象**（基本是空的）。
> 地图的 Mesh 和贴图全在 **resources.assets 这个共享池**里，靠 PPtr 引用。

### 1.2 全 12 张地图实测矩阵（对象计数）

| 类型 | 大厅 | 运输船 | 小型工厂 | 椰岛之巅 | 胜利广场 | 竞技场 | 刀锋寨 | 沙漠要塞 | 生化酒店 | 飓风危城 | 新寂静村 | 死亡擂台 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 对象总数 | 1474 | 2313 | 615 | 529 | 565 | 410 | 442 | 753 | 7695 | 1671 | 1992 | 478 |
| GameObject | 351 | 953 | 142 | 122 | 120 | 99 | 113 | 199 | 3332 | 383 | 619 | 107 |
| MeshFilter | 0 | 138 | 99 | 85 | 100 | 50 | 51 | 76 | 161 | 113 | 111 | 69 |
| MeshRenderer | 0 | 138 | 99 | 85 | 100 | 50 | 51 | 76 | 161 | 113 | 111 | 69 |
| MeshCollider | 0 | 69 | 82 | 66 | 91 | 35 | 41 | 60 | 80 | 113 | 101 | 52 |
| BoxCollider | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 20 | 52 | 0 | 12 | 14 |
| MonoBehaviour | 472 | 49 | 42 | 43 | 27 | 71 | 66 | 106 | 556 | 349 | 412 | 52 |
| Light | 1 | 3 | 1 | 1 | 1 | 1 | 1 | 12 | 1 | 1 | 1 | 1 |
| Camera | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| ParticleSystem | 0 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 7 | 0 | 0 | 1 |
| RectTransform | 348 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 251 | 0 | 0 |
| Canvas | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 |
| Mesh（内嵌） | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### 1.3 从矩阵里能读出的四条事实

| # | 事实 | 证据 |
| --- | --- | --- |
| 1 | **全 12 张共有的原生类型只有 9 类** | GameObject、Transform、Camera、AudioListener、RenderSettings、Light、LightmapSettings、NavMeshSettings、MonoBehaviour |
| 2 | **11/12 张有几何**，唯一例外是 `level0` 大厅 | 大厅 MeshFilter / MeshRenderer = 0，是纯 UI 场景 |
| 3 | **每张图都是 1 个 Camera + 1 个 Light 起步** | Camera 全为 1；Light 多为 1，运输船 3 个、沙漠要塞 12 个 |
| 4 | **场景内嵌 Mesh 只在 `level1` 出现 1 个** | 说明网格全部走外部共享池，场景本身不存几何数据 |

> 📌 **修正之前的说法**：早前记录说"level10 是纯路点场景、没有网格"——**错了**。
> 实测 level10（新寂静村）有 111 组 MeshFilter/MeshRenderer、101 个 MeshCollider、619 个 GameObject。
> 它是 11 张战斗图里对象数第二多的（1,992），仅次于生化酒店（7,695）。

### 1.4 每张战斗地图固定的 26 个"骨架对象"（18 个脚本）

把每张图里的 MonoBehaviour 按"脚本 pathID"分组后发现一个非常整齐的规律：

**`level1` ~ `level11` 这 11 张图，每张都恰好有 18 个脚本、26 个实例；`level0` 大厅一个都没有。**

| pathID | 类名 | 来自哪个程序集 | 每图实例数 |
| --- | --- | --- | ---: |
| 705 | **AstarPath** | AstarPathfindingProject.dll | 1 |
| 1034 | **GameManager** | Assembly-CSharp.dll | 1 |
| 1210 | **MapManager** | Assembly-CSharp.dll | 1 |
| 680 | **CameraManager** | Assembly-CSharp.dll | 1 |
| 937 | **SoundManager** | Assembly-CSharp.dll | 1 |
| 1065 | **EffectManager** | Assembly-CSharp.dll | 1 |
| 1329 | **AssetManager** | Assembly-CSharp.dll | 1 |
| 307 | **PlayerController** | Assembly-CSharp.dll | 1 |
| 308 | CinemachineFreeLook | Cinemachine.dll | 1 |
| 682 | CinemachineBrain | Cinemachine.dll | 1 |
| 85 | CinemachineImpulseListener | Cinemachine.dll | 1 |
| 1276 | CinemachineCollider | Cinemachine.dll | 1 |
| 1343 | CinemachineComposer | Cinemachine.dll | 3 |
| 420 | CinemachineVirtualCamera | Cinemachine.dll | 3 |
| 972 | CinemachinePipeline | Cinemachine.dll | 3 |
| 852 | CinemachineOrbitalTransposer | Cinemachine.dll | 3 |
| 952 | UniversalAdditionalCameraData | Unity.RenderPipelines.Universal.Runtime.dll | 1 |
| 182 | Volume | Unity.RenderPipelines.Core.Runtime.dll | 1 |

**这意味着什么**：

- 这 26 个对象就是一张地图的"骨架"——相机系统、光照管理、声音、特效、资源加载、寻路容器
- 它们的脚本全部编译在 `Assembly-CSharp.dll` / 第三方 DLL 里，**外部 Unity 工程造不出来**
- 所以做新地图的正确做法是**复制一个原版场景当骨架**，只替换里面的几何，而不是从零建场景
- 剩下的 MonoBehaviour 才是地图特有的（运输船 23 个、小型工厂 16 个、生化酒店 530 个……）

### 1.5 UCF 用的是 URP 渲染管线（重要）

从 `resources.assets` 里的 Shader 和上面 18 个脚本能确认：

| 证据 | 说明 |
| --- | --- |
| `UniversalAdditionalCameraData` / `Volume` 脚本 | 这是 **Universal Render Pipeline（URP）** 的标志性组件 |
| Shader 参数是 `_BaseMap` / `_BaseColor` / `_WorkflowMode` | URP/Lit 的字段名（Built-in 叫 `_MainTex` / `_Color`） |
| 另有 `_MainTex` + `Sprite Texture` 的 Shader | URP/Sprites/Default |

**结论**：给新地图做材质时，**必须用 URP 的 Shader（URP/Lit、URP/Sprites/Default 等）**。
用 Built-in 的 `Standard` 会显示成粉色或直接不可见。

### 1.6 一张 UCF 地图的八件套（更新版）

| # | 要素 | 术语 | 覆盖面（12 张图里） |
| --- | --- | --- | --- |
| 1 | 静态几何 | MeshFilter + MeshRenderer | 11/12（大厅除外） |
| 2 | 碰撞 | MeshCollider（地形）+ BoxCollider | MeshCollider 11/12；BoxCollider 7/12 |
| 3 | 材质贴图 | Material + Shader + Texture2D | 全部，存放在 resources.assets 共享池 |
| 4 | 光照 | LightmapSettings + 烘焙贴图 Lightmaps / LightmapsInd | 12/12 |
| 5 | 天空/雾 | RenderSettings | 12/12 |
| 6 | 出生点 | pointDic（MonoBehaviour 里存坐标 + 朝向） | 全部战斗图 |
| 7 | 寻路 | **A-star Pathfinding Project**（AstarPath 脚本） | 11/12 |
| 8 | 骨架 | 18 个管理脚本 / 26 个实例（见 1.4） | 11/12 |


---

## 2. 候选 A：ForbiddenTD_Classic.GLB

### 2.1 位置

| 内容 | 路径 |
| --- | --- |
| 原始文件 | D:\BaiduNetdiskDownload\ForbiddenTD_Classic.GLB（7.97 MB） |
| 已转好的 FBX | D:\ucf_unity\UcfMap\Assets\Models\ForbiddenTD_Classic.fbx（3.03 MB） |
| 已导出的贴图 | D:\ucf_unity\UcfMap\Assets\Textures\（52 张 PNG） |
| 合并材质 | D:\ucf_unity\UcfMap\Assets\Merged\（112 个 .asset） |
| 场景 | D:\ucf_unity\UcfMap\Assets\Scenes\TestMap12.unity（0.15 MB） |

### 2.2 格式

**glTF 2.0 二进制（.glb）**，导出器 RezExplorer.DatGlbExporter。

- .rez 是 **LithTech 引擎**的资源包格式（《无人永生》《Tron 2.0》《F.E.A.R.》用过）。
- 材质名 forbidden、MexicoD1~D3、kairouan_wood_1、colombian_bunsu 与《穿越火线》系列资源命名一致。
- 具体对应哪张官方图：**未确认**。既有文档记的是"紫禁城塔防图"，但材质命名更像 CF 系资源，以文件事实为准。

### 2.3 里面有什么（实测）

| 项目 | 数值 |
| --- | --- |
| 网格数 | 562 个（每网格 1 个图元） |
| 节点数 | 609 个（Section_0037 … 纯编号命名） |
| 材质 | 55 个 |
| 贴图 | 52 张 PNG，合计 **3.94 MB**（全部内嵌） |
| 顶点总数 | **38,030** |
| 三角面总数 | **19,444** |
| 包围盒尺寸 | 161.5 × 50.6 × 165.8（模型单位） |
| 顶点属性 | POSITION / NORMAL / COLOR_0 / TANGENT / TEXCOORD_0 / TEXCOORD_1 |
| 动画 | 0 |
| 光照贴图 | **0** |

**顶点属性术语**：

| 属性 | 干什么的 | 缺了会怎样 |
| --- | --- | --- |
| POSITION | 顶点坐标 | 什么都渲染不出来 |
| NORMAL | 法线，决定受光方向 | 整个模型一片死黑或死白 |
| TANGENT | 切线，法线贴图要用 | 法线贴图失效，表面细节消失 |
| TEXCOORD_0 | 第一套 UV，贴图坐标 | 贴图错乱 |
| TEXCOORD_1 | 第二套 UV，常用于光照贴图 | 光烘焙不了（要做光照的话需要） |
| COLOR_0 | 顶点色 | 部分材质会失去染色 |

**结论：几何完整度极高**——38k 顶点、19k 面，连着色器要用的切线都有。

### 2.4 对照 UCF 八件套

| # | 要素 | GLB 有吗 | 说明 |
| --- | --- | --- | --- |
| 1 | 静态几何 | ✅ | 562 个网格，转成 FBX 后完整 |
| 2 | 碰撞 | ❌ | 一个 Collider 都没有，必须在 Unity 里挂 MeshCollider |
| 3 | 材质贴图 | ⚠️ | 贴图有，但材质是 LithTech 的；**UCF 用 URP 管线**（见 1.5），必须重做成 URP/Lit |
| 4 | 光照 | ❌ | 没有 lightmap、没有灯、没有 LightProbe |
| 5 | 天空/雾 | ❌ | 没有 RenderSettings |
| 6 | 出生点 | ❌ | 0 |
| 7 | 寻路图 | ❌ | 0 |
| 8 | 管理器 | ❌ | 0 |

### 2.5 现状

**这张已经做出来了，并且验证过**（见 [新增地图_完整工作流.md](新增地图_完整工作流.md)）：
团队模式第 3 项「测试地图」，能进、能站、能走、HUD 正常。

---

## 3. 候选 B：DC 穿越火线挑战版本

### 3.1 位置

| 内容 | 路径 |
| --- | --- |
| 游戏根 | C:\Users\17242\Downloads\DC穿越火线挑战版本\DC穿越火线挑战版本\ |
| 数据目录 | 同上 \DC穿越火线挑战版本_Data\ |
| 神秘营地场景 | _Data\level2（1.37 MB） |
| 本图配套资产 | _Data\sharedassets2.assets 68.16 MB + sharedassets2.assets.resS 53.74 MB + sharedassets2.resource 4.82 MB |
| 额外资料 | 根目录 无敌挂\、背包修改方法\（与本任务无关） |

### 3.2 格式

| 项 | 值 |
| --- | --- |
| 引擎 | **Unity 5.3.7f1** |
| 脚本后端 | **Mono**（Managed\Assembly-CSharp.dll 200 KB） |
| 序列化版本 | v15（UCF 是 v22） |
| 场景数 | 4 |

场景表（从 globalgamemanagers 里直接读出来的）：

| 索引 | 场景路径 | 实际是什么 |
| --- | --- | --- |
| level0 | Assets/Scene/Login.unity | 登录界面 |
| level1 | Assets/Scene/Web_House_Scene.unity | 武器库/商城 |
| level2 | Assets/Scene/ShenMiYingDi/ShenMiYingDi.unity | **神秘营地（真正的战斗地图）** |
| level3 | Assets/Scene/JuRenChengFeiXu/tz_End.unity | **结算界面（不是地图）** |

> ⚠️ **重要更正**：之前把 tz_End 当成"巨人城废墟地图"是错的。
> 实测 level3 只有 **40 个对象**（Canvas + Animator + Camera），是打完后的结算画面。
> **DC 挑战版实际只有 1 张可玩地图：神秘营地。**

### 3.3 神秘营地（level2）里面有什么

场景本体（10,501 个对象）：

| 类型 | 数量 | 是什么 |
| --- | --- | --- |
| GameObject / Transform | 4,612 / 4,457 | 物体与层级 |
| **SkinnedMeshRenderer** | **374** | **带骨骼的动画角色**——挑战模式的怪物/NPC，不是地图 |
| MonoBehaviour | 292 | DC 自己的脚本（出生点、刷怪、关卡逻辑） |
| RectTransform / CanvasRenderer | 155 / 143 | UI |
| MeshFilter / MeshRenderer | 105 / 102 | **静态地图几何（真正要的部分）** |
| Animation / Animator | 72 / 26 | 动画 |
| ParticleSystem | 39 | 特效 |
| MeshCollider | 27 | 地形碰撞 |
| BoxCollider | 4 | 盒子碰撞 |
| ReflectionProbe | 6 | 反射探针 |
| Camera | 5 | 摄像机 |
| Light | 1 | 平行光 |
| RenderSettings / LightmapSettings / NavMeshSettings | 各 1 | 渲染/光照/寻路设置 |

配套资产（sharedassets2，3,434 个对象）：

| 类型 | 数量 |
| --- | --- |
| Texture2D | **516** |
| AnimationClip | 296 |
| Sprite | 254 |
| **Mesh** | **226** |
| Material | 187 |
| AudioClip | 149 |
| Shader | 12 |
| **NavMeshData** | **1**（Unity 烘焙的寻路网格） |

光照：有烘焙贴图，命名 Lightmap-0_comp_light / Lightmap-0_comp_dir（最多到 Lightmap-3）。

### 3.4 对照 UCF 八件套

| # | 要素 | DC 有吗 | 说明 |
| --- | --- | --- | --- |
| 1 | 静态几何 | ✅ | 105 组 MeshFilter/MeshRenderer + 226 个 Mesh |
| 2 | 碰撞 | ✅ | 27 MeshCollider + 4 BoxCollider（要重新挂，因为对象会被剥） |
| 3 | 材质贴图 | ✅ | 516 张贴图、187 个材质，**完整度最高** |
| 4 | 光照 | ✅ | 有烘焙 lightmap（但 Unity 5.3 格式，升级后可能失效） |
| 5 | 天空/雾 | ✅ | 有 RenderSettings |
| 6 | 出生点 | ⚠️ | 有，但存在 DC 的脚本里，UCF 不认 |
| 7 | 寻路 | ⚠️ | 是 **Unity NavMesh**（NavMeshData），UCF 用的是 A-star，两套不通用 |
| 8 | 管理器 | ❌ | 292 个 MonoBehaviour 全是 DC 的，必须全部剥掉 |
| 9 | 渲染管线 | ❌ | DC 用 Unity 5.3 的 **Built-in** 管线，UCF 是 **URP**，材质不通用，要全部重建 |

### 3.5 要剥掉什么

| 要剥的 | 数量 | 原因 |
| --- | --- | --- |
| SkinnedMeshRenderer | 374 | 挑战模式的怪物模型，进 UCF 只会挡路 |
| DC 的 MonoBehaviour | 292 | 脚本编译在 DC 的 Assembly-CSharp.dll 里，UCF 没有 |
| UI（Canvas / RectTransform） | 约 300 | 游戏自己的界面 |
| Animator / Animation | 98 | 角色动画，用不上 |

**剥完剩下的大概就是：105 组几何 + 226 个网格 + 516 张贴图 + 27 个碰撞体。**

---

## 4. 候选 C：赛车之城（CS 1.6 地图）

### 4.1 位置

| 内容 | 路径 |
| --- | --- |
| 地图文件 | C:\Users\17242\Downloads\新建文件夹\赛车之城\cstrike\maps\#XL_racecity.bsp（4,882 KB） |
| 寻路文件 | 同目录 #XL_racecity.nav（469 KB） |
| 资源清单 | 同目录 #XL_racecity.res（0 KB，空） |
| 模型 | cstrike\models\racecity\sobol.mdl（675 KB）、Sul-DC_Viper-red.mdl（260 KB） |
| 同批还有 | 新建文件夹\夜幕山庄\（另一张 CS 图 NH_NANO4MANSION.bsp 5,158 KB） |

### 4.2 格式

**GoldSrc BSP v30** —— 《半条命 1》/《反恐精英 1.6》的地图格式。

和 Unity **没有任何关系**：不是场景、没有 GameObject、没有材质系统、没有 PBR。

### 4.3 里面有什么（实测）

| 数据块 | 大小 | 是什么 |
| --- | --- | --- |
| ENTITIES | 8,778 B | 实体列表（85 个） |
| PLANES | 66,140 B | 切割平面 |
| TEXTURES | **2,371,316 B** | 86 张纹理 |
| VERTICES | 138,456 B | 11,538 个顶点 |
| VISIBILITY | 317,208 B | 可见性预计算（PVS） |
| NODES | 86,256 B | BSP 树 |
| TEXINFO | 106,440 B | 每个面的贴图映射 |
| FACES | 167,160 B | 8,358 个面 |
| LIGHTING | **1,340,817 B** | **烘焙光照（lightmap）** |
| CLIPNODES | 71,280 B | 8,910 个碰撞节点 |
| MODELS | 1,408 B | 22 个 brush 模型 |

**几何规模**：11,538 顶点 / 8,358 面 / 22 个 brush 模型。
**尺寸**：3,960 × 3,864 × 1,312（GoldSrc 单位，1 单位约等于 1 英寸，约 100 m × 98 m × 33 m）。

**实体构成（85 个）**：

| 实体 | 数量 | 作用 |
| --- | --- | --- |
| info_player_start | 20 | 出生点 |
| info_player_deathmatch | 19 | 死亡竞赛出生点 |
| func_wall | 12 | 可移动墙体 |
| cycler_sprite | 8 | 循环动画精灵 |
| light | 7 | 点光源 |
| func_illusionary | 5 | 无碰撞装饰 |
| trigger_camera | 3 | 过场镜头 |
| info_target | 3 | 目标点 |
| worldspawn | 2 | 世界本体 |
| func_buyzone | 2 | 购买区 |
| light_environment | 1 | 环境光/太阳 |

### 4.4 缺什么 —— 这张问题最多

| 问题 | 严重度 | 说明 |
| --- | --- | --- |
| **22 张贴图不在文件里** | 🔴 高 | 86 张里只有 64 张内嵌像素，另外 22 张指向外部 .wad 文件，这个包里没有 |
| 光照带不过来 | 🔴 高 | 1.28 MB 的 lightmap 是 GoldSrc 格式，Unity 完全不认，必须重新烘 |
| 没有 Collider 对象 | 🟡 中 | 只有 CLIPNODES（碰撞用 BSP 树），要转成 MeshCollider |
| 坐标系不同 | 🟡 中 | GoldSrc 是 Z 轴向上，Unity 是 Y 轴向上，要旋转 + 缩放 |
| 比例不同 | 🟡 中 | 1 单位 = 1 英寸，UCF 的比例要实测对齐 |
| brush 转 mesh 有损 | 🟡 中 | 实体切割出来的墙面转网格会出现接缝、破面、法线翻转 |
| 材质系统不存在 | 🟡 中 | GoldSrc 只有"漫反射贴图 + lightmap"，没有金属度/粗糙度 |
| 没有出生点给 UCF 用 | 🟢 低 | 有 20+ 个 info_player_*，但那是 CS 的格式，UCF 要重新放 |
| 没有 URP 材质 | 🟡 中 | GoldSrc 没有材质概念，进 Unity 要全部新建 URP/Lit 材质 |

### 4.5 结论

**技术上能做完，但它是三张里唯一"要跨引擎"的。**
做完的效果：没有烘焙光照、22 张贴图缺失（或需要另找 WAD）、几何有接缝。

---

## 5. 三张对比总表

| 要素 | UCF 原版 | A. GLB | B. DC 神秘营地 | C. 赛车之城 |
| --- | --- | --- | --- | --- |
| 引擎 | Unity 2020.3 IL2CPP | 中立格式（glTF） | Unity 5.3 Mono | GoldSrc |
| 静态几何 | ✅ 138 组 | ✅ 562 网格 | ✅ 105 组 | ⚠️ brush 转出来有损 |
| 网格总数 | 共享池 1,203 | 562 | 226 | 22 个 brush |
| 顶点数 | — | 38,030 | 未统计（含角色） | 11,538 |
| 面数 | — | 19,444 | — | 8,358 |
| 贴图 | 共享池 1,792 | 52（3.94 MB） | 516 | 86（**缺 22**） |
| 材质 | 共享池 1,152 | 55 | 187 | 无（只有贴图+光照） |
| 碰撞体 | ✅ MeshCollider | ❌ 要自己挂 | ✅ 27 个 | ⚠️ 需从 clipnodes 转 |
| 烘焙光照 | ✅ | ❌ | ✅（5.3 格式） | ✅（GoldSrc 格式，用不了） |
| 天空/雾 | ✅ | ❌ | ✅ | ✅ |
| 出生点 | ✅ pointDic | ❌ | ⚠️ DC 脚本里的 | ⚠️ CS 实体的 |
| 寻路 | A* 图数据 | ❌ | ⚠️ Unity NavMesh（不通用） | ❌ |
| 管理器对象 | ✅ 18 个 | ❌ | ❌ | ❌ |
| 场景对象总数 | 2,313 | — | 10,501（含 374 个角色） | — |
| **能否直接用** | — | ❌ | ❌ | ❌ |
| **处理难度** | — | ⭐ | ⭐⭐ | ⭐⭐⭐⭐ |

---

## 6. 拿不到的东西 + 用什么工具拿

| 缺的东西 | 在哪张图 | 怎么拿 |
| --- | --- | --- |
| **22 张 WAD 贴图** | 赛车之城 | 需要 CS 1.6 / 半条命的 .wad 文件（cstrike.wad、halflife.wad、cs_dust.wad 等）。工具：**Wally**（WAD 编辑器）、**GCFScape**（从 Steam 的 .gcf/.vpk 里取） |
| **lightmap 贴图** | DC | **AssetStudio** → 选 Texture2D → 导出 PNG/EXR（已装在 D:\BaiduNetdiskDownload\AssetStudio.net472.v0.16.47） |
| **DC 的几何/材质** | DC | **AssetRipper**（D:\BaiduNetdiskDownload\AssetRipper_win_x64）→ 导出整个 Unity 工程，再用 Unity 2020.3 打开升级 |
| **BSP 转网格** | 赛车之城 | **BSPSource**（BSP 转 VMF）、**bsp2obj**、或 Blender 的 BSP 插件；VMF 可用 **Jackhammer** / CS 版 Hammer 打开 |
| **.mdl 模型转格式** | 赛车之城 | **Crowbar**（Source 引擎的 mdl）、**MilkShape 3D**（GoldSrc 的 mdl） |
| **GLB 转 FBX** | GLB | **Blender**（已装：D:\Program Files\Blender Foundation\Blender 5.3） |
| **UCF 自己的 Shader** | 全部 | 从游戏里导出（AssetStudio 打开 resources.assets 找 7 个 Shader），或在 Unity 里用近似材质 |

---

## 7. 术语表

| 术语 | 大白话 |
| --- | --- |
| **Mesh** | 网格。一堆三角形拼出来的"壳"，决定形状 |
| **Material / Shader** | 材质 / 着色器。前者是"用什么颜色贴哪张图"，后者是"怎么算光照" |
| **Texture2D** | 纹理贴图，就是贴上去的那张图 |
| **UV / TEXCOORD** | 贴图坐标。把平面图"包"到立体模型上的对应关系 |
| **Normal（法线）** | 每个点朝哪边。决定这个面受光多亮 |
| **Tangent（切线）** | 配合法线贴图用的方向向量 |
| **MeshCollider** | 网格碰撞体。让角色"站在"这个形状上、走不穿 |
| **BoxCollider / CapsuleCollider** | 盒子/胶囊碰撞体。用简单形状近似，比网格碰撞快 |
| **Lightmap（光照贴图）** | 提前算好的阴影和亮度，烘在一张贴图上。运行时不用实时算光，省性能 |
| **LightProbe（光照探针）** | 场景里撒的采样点，让动态物体也能接收到烘焙光 |
| **LightmapSettings / RenderSettings** | Unity 场景里存"光照设置/天空盒雾效"的对象 |
| **NavMesh / NavMeshData** | Unity 官方的寻路网格（烘焙出来的可行走区域） |
| **A-star 寻路** (A*) | 另一种寻路方案，UCF 用的是这个，和 NavMesh 不通用 |
| **PPtr** | Unity 文件里的"指针"。(文件ID, 对象ID) 指向另一个对象 |
| **SerializedFile** | Unity 的资源文件格式。版本号不同（v15 / v22）互不兼容 |
| **IL2CPP / Mono** | Unity 的两种脚本后端。IL2CPP 编译成 C++（UCF），Mono 是 .NET 程序集（DC） |
| **BSP** | 《半条命》/CS 的地图格式，用"实体切割平面"生成几何，和网格建模是两套思路 |
| **brush** | CS 地图里的"方块"，地图是由一个个 brush 拼出来的 |
| **WAD** | 《半条命》的资源包（贴图/音效），BSP 只存贴图名，像素在 WAD 里 |
| **lightmap（GoldSrc）** | CS 的烘焙光照，存在 BSP 的 LIGHTING 数据块里，格式完全私有 |
| **clipnodes** | CS 的碰撞数据结构（BSP 树），不是网格碰撞体 |
| **glTF / GLB** | 新一代 3D 交换格式，文本（.gltf）+ 二进制（.glb）。自带几何、材质、贴图、动画 |
| **FBX** | Autodesk 的 3D 交换格式，Unity 原生支持 |

---

## 8. 处理路线与工作量

### A. GLB（已完成）

    glb → Blender 转 FBX → Unity 2020.3 导入
        → 合并同材质网格（Merged/112 个 .asset）
        → 借原版场景当骨架，替换几何
        → Build → level12 + sharedassets12
        → 注册表加一项「测试地图」

**状态：已验证可用**（能进、能站、能走）。

### B. DC 神秘营地（未做）

    AssetRipper 导入 DC 根目录 → 导出 Unity 工程
        → Unity 2020.3 打开（自动升级 5.3→2020.3）
        → 删掉 292 个 MonoBehaviour + 374 个 SkinnedMeshRenderer + UI
        → 检查材质/Shader 是否丢失，重挂
        → 同上：借场景骨架 + 替换几何

**预计**：2–3 天。**风险**：5.3 的材料升级到 2020.3 可能大面积丢失，需要重挂。

### C. 赛车之城（不建议做）

    BSP → BSPSource 转 VMF → Hammer 检查
        → 导出 OBJ（或 Blender 插件）
        → 补齐 22 张 WAD 贴图
        → Blender 里缩放 1/39.37、Z-up 转 Y-up、修接缝
        → Unity 重挂材质、重新烘焙光照

**预计**：一周起，**效果最差**（无光照、贴图缺失、几何有破洞）。

---

## 9. 附录：这些数字是怎么来的

| 数据 | 用什么读的 | 怎么读 |
| --- | --- | --- |
| GLB 统计 | Node.js 直接解析 glTF JSON + accessor | 读 12 字节头 → JSON chunk → 累加各 primitive 的 POSITION.count 与 indices.count/3 |
| DC / UCF 对象统计 | **UnityPy 1.25.4**（Python） | UnityPy.load(path) → 遍历 sf.objects 按 oi.type.name 计数 |
| DC 场景表 | 直接扫 globalgamemanagers 字节 | 正则匹配 6 个字符以上的 *.unity 字符串 |
| BSP 统计 | Node.js 直接解析 BSP 头 | 15 个数据块的 offset/length，再按结构体逐个解 |
| 地图注册表 | UnityPy 定位对象 + 裸字节解析 | 见 [新增地图_完整工作流.md](新增地图_完整工作流.md) |

### 9.1 全类型 × 全地图计数表

| 类型 | 大厅 | 运输船 | 小型工厂 | 椰岛之巅 | 胜利广场 | 竞技场 | 刀锋寨 | 沙漠要塞 | 生化酒店 | 飓风危城 | 新寂静村 | 死亡擂台 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Animator | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| AudioListener | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| AudioSource | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 1 | 0 |
| BoxCollider | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 20 | 52 | 0 | 12 | 14 |
| Camera | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Canvas | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 |
| CanvasRenderer | 289 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 205 | 0 | 0 |
| CapsuleCollider | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| Cubemap | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| GameObject | 351 | 953 | 142 | 122 | 120 | 99 | 113 | 199 | 3332 | 383 | 619 | 107 |
| Light | 1 | 3 | 1 | 1 | 1 | 1 | 1 | 12 | 1 | 1 | 1 | 1 |
| LightmapSettings | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Mesh | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MeshCollider | 0 | 69 | 82 | 66 | 91 | 35 | 41 | 60 | 80 | 113 | 101 | 52 |
| MeshFilter | 0 | 138 | 99 | 85 | 100 | 50 | 51 | 76 | 161 | 113 | 111 | 69 |
| MeshRenderer | 0 | 138 | 99 | 85 | 100 | 50 | 51 | 76 | 161 | 113 | 111 | 69 |
| MonoBehaviour | 472 | 49 | 42 | 43 | 27 | 71 | 66 | 106 | 556 | 349 | 412 | 52 |
| NavMeshSettings | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| ParticleSystem | 0 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 7 | 0 | 0 | 1 |
| ParticleSystemRenderer | 0 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 7 | 0 | 0 | 1 |
| RectTransform | 348 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 251 | 0 | 0 |
| RenderSettings | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Transform | 3 | 953 | 142 | 122 | 120 | 99 | 113 | 199 | 3332 | 132 | 619 | 107 |

### 9.2 配套文件体量（sharedassetsN）

| 文件 | 对象数 | Mesh | Texture2D | Material |
| --- | ---: | ---: | ---: | ---: |
| sharedassets0.assets | 25117 | 204 | 1679 | 387 |
| sharedassets1.assets | 11171 | 0 | 0 | 83 |
| sharedassets2.assets | 7 | 0 | 0 | 3 |
| sharedassets3.assets | 4 | 0 | 0 | 1 |
| sharedassets4.assets | 4 | 0 | 0 | 1 |
| sharedassets5.assets | 2 | 0 | 0 | 1 |
| sharedassets6.assets | 3 | 0 | 0 | 0 |
| sharedassets7.assets | 27 | 0 | 0 | 1 |
| sharedassets8.assets | 7 | 0 | 0 | 4 |
| sharedassets9.assets | 5 | 0 | 1 | 1 |
| sharedassets10.assets | 4 | 0 | 0 | 1 |
| sharedassets11.assets | 4 | 0 | 0 | 1 |
| resources.assets | 27139 | 1203 | 1792 | 1152 |

### 9.3 复现脚本

复现脚本放在 06-测试\ucf_mod\probe_map_loader\：

    probe_all_maps.py   全 12 张图 + 全 12 个 sharedassets 的类型统计
    probe_scripts.py    按脚本 pathID 分组，找固定骨架
    probe_monoscript.py 把 pathID 解析成类名
    probe_hist.py       DC / UCF 对比
    probe_ext.py        外部引用表

