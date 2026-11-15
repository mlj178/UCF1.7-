# UCF 导航数据编辑器（navedit）

离线读取 `UnityCrossFire_Data` 里的地图资源，在 3D 里飞行查看贴图地形与路点，
左键点模型可以直接看到它是「什么东西」（名字 / 材质 / 贴图）。

## 运行

双击 `启动编辑器.bat`（或 `python run.py`）。
依赖：Python 3.12 / PyQt5 / moderngl / numpy / UnityPy / Pillow / texture2ddecoder。

## 用法

1. 菜单「文件 → 选择游戏目录」，选到 `UnityCrossFire_Data`（会自动记住）。
2. 左边点 `level9`（= 生化幽灵·风暴）→「打开选中地图」。
3. 首屏会自动站到路点最密集的位置，面朝地图内部。
4. 自动加载 `ucf_mod/vis` 或 `ucf_mod/nav` 里和这张图对得上的路点 JSON。
5. **左键点一下任何模型**，右侧「检视」会显示它的对象名、网格名、材质、着色器、
   贴图缩略图、三角形数、点击位置、离得最近的路点。

## 操作

| 操作 | 键 |
| --- | --- |
| 转视角 | 按住右键拖动 |
| 前后左右 | W A S D |
| 降 / 升 | Q / E |
| 加速 | Shift |
| 推拉 | 滚轮 |
| 平移 | 中键拖动 |
| 点选模型 | 左键单击 |
| 聚焦路点整体 | F |
| 俯视 | Tab |
| 地形 / 贴图 / 阴影体 / 路点 / 连线 / 网格 | M / T / — / G / R / — |

菜单「视图」里可以勾选「显示贴图」「显示阴影体」（阴影体和 ALPHA_Blocker 默认隐藏，
它们不是看得见的模型，打开只会挡视线）。

## 贴图是怎么来的

- 网格顶点带 UV，直接从 Unity 的 OBJ 导出里解析出来（`vt`），平铺坐标原样使用（REPEAT）。
- 贴图按材质读 `_BaseMap`/`_MainTex`，DXT1/DXT5 用 `texture2ddecoder` 解，落盘成 PNG 缓存。
- **坑**：这个 Unity 构建的 `Texture2D` 结构比 UnityPy 自带 typetree 少 24 字节，
  正常读会抛 `Expected to read 164 bytes, but only read 140`，
  必须走 `read_typetree(check_read=False)` 才拿得到宽高/格式/流偏移。
- 带 alpha 的贴图（DXT5/BC3）按 0.35 阈值做 alpha 裁剪，树叶、栏杆才不会是实心方块。

## 缓存

| 路径 | 内容 |
| --- | --- |
| `ucf_mod/geo/<场景>.npz` | 顶点/法线/UV/索引 + 分块表和材质表（JSON） |
| `ucf_mod/geo/tex/<场景>/*.png` | 解出来的贴图 |

缓存带版本号（当前 4），版本对不上会自动重新提取。删掉整个 `geo` 目录也能重来。

## 架构

| 文件 | 职责 |
| --- | --- |
| `assets.py` | UnityPy 索引资源目录、遍历 Transform 层级、导出网格（含 UV）、读材质与贴图、缓存 |
| `navdata.py` | 解析旧版 `graph_*.json` 与 v1 `navgraph` |
| `viewport.py` | 独立 moderngl 上下文渲染到 FBO，读回成 QImage 显示；分块绘制 + 贴图 + 射线拾取 |
| `app.py` | 主窗口、地图列表、检视面板、菜单 |

## 已知限制

- 地图是封闭场景（有顶/外壳），俯视图会被天花板盖住，要用自由相机钻进室内看。
- 光照是自己近似的一套（方向光 + 环境光），所以不会有游戏里的 AO、描边、后处理。
- 粒子、贴花、天空盒、动画物体都没有；只取静态网格。
- 目前只读：还不能编辑路点（下一步）。
- 大图首次提取 2~5 秒（level1 更大），之后走缓存。
