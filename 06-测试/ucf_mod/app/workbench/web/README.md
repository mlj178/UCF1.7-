# UCF 路点工作台（只读 · 七页）

> 2026-11-18：按当时的 `design/nav-studio-launcher.html` 的七页结构重做，数据全部接真实文件（该设计稿已随 `design/` 归档）。
> 网页端仍然只读；编辑在游戏内完成。
>
> **2026-11-23：数据档改成「① 备份版 / ② 成品 / ② 编辑中」，③ 部署版不再作为数据档。**
> （2026-11-21 的「四版 → 三区」见更新记录；三区里的 ③ 已降为游戏运行目录。）
>
> **数据档**：顶栏右侧下拉 **① 备份版 / ② 成品 / ② 编辑中**；选「编辑中」时旁边出现「包」下拉：
>
> - **① 备份版** `navdata\native\` —— 原生冻结快照，只读对照，游戏不读它
> - **② 成品** `navdata\dev\final\<当前版本>\` —— 控制台「成品」档启动时读的那一版；
>   网页只看当前版，历史版本 / 版本对比在控制台成品页
> - **② 编辑中** `navdata\dev\packs\<图文件夹>\<包名>\<指纹>.txt` —— 每张图一个测试包，
>   默认最新；没有包 / 指纹失效会在下拉和提示里标出来
> - **③ 部署版**（游戏目录）—— 只是运行环境（dll / 配置 / 日志）；2026-11-21 起不放导航数据，
>   **不再作为数据档**
>
> 切换只改「看哪一份」，不写任何文件。默认档：成品有当前版看成品，否则有包看编辑中；之后记住上次。
> navview 顶栏也有同一个下拉；3D 侧栏跟着工作台的「数据档 + 包」走。

## 一、一张图一个文件夹

```
navdata\dev\
  00_公共\                 names.json  _index.json  INDEX.md  nogen.txt（原 nav\ 和 maps\ 里的公共文件）
  01_TransportShip运输船\   map.json  navmesh.bin  导出\*.json
  02_Factory小型工厂\       ...
  final\                   <版本名>\<指纹>.txt（成品，只读）+ _index.json + _current.txt
  packs\<图文件夹>\<包名>\   <指纹>.txt / manifest.json（编辑中，可写）
  vis\                     收件箱：raw\ rec\ _state\
  archive\                 历史 / 还原点
```

① 备份版同构，但没有 final / packs / vis / 导出。

## 二、入口与职责

| 入口 | 打开 | 权限 |
| --- | --- | --- |
| 控制台「路点工作台（查看）」 | `console/web/nav-studio.html`（服务地址 `/web/nav-studio.html`） | **看**：总览 / 路点库 / 路线 / 区域 / 自动铺设 / 地图数据 / 日志 |
| 左侧「3D / 可走面」或右上「3D 侧栏」 | 同页右侧的停靠栏 iframe（`console/web/navview.html?view=1&embed=1&notour=1&profile=<版本>&open=<图文件夹>/map.json`） | 3D 地形 + 可走面 + 路点/路线/区域图层；**不跳页、不盖住工作台**，换页不断开；拖左边框调宽、双击复位，`关闭 ✕` / `Esc` 收起；开关与宽度记在 localStorage |

停靠栏（2026-11-18 晚改）：侧栏「3D / 可走面」带 **开/关** 徽标；默认 480px，停靠时最右详情列让位给 2D 地图，
地图 / 版本切换后 3D 自动跟到新图。内嵌模式由 `navview.html?embed=1` 提供，只留 3D 画面。

### 3D 侧栏里怎么动（2026-11-21 加）

| 操作 | 作用 |
| --- | --- |
| 鼠标停在 3D 画面上 + **W/A/S/D** | 前后左右飞（速度跟镜头距离挂钩，拉远看全图时飞得也快） |
| **Q / E**（或 空格 / Shift+空格） | 下降 / 上升；按住 **Shift** 加速 ×3 |
| **右键拖动** | 转视角（鼠标往右拖 = 视角右转） |
| 中键拖动 / Shift+右键 | 平移 |
| 滚轮 | 推拉远近 |
| **F** | 全图；**Esc** 收起侧栏 |

鼠标悬停在 3D 上时 iframe 拿不到键盘焦点，所以按键由工作台这一页转发（`fly-hover` / `fly-key` 两条 postMessage）；
点过 3D 画面之后焦点就在 iframe 里，navview 自己处理，两条路不会重复。

### 3D 贴图（2026-11-23 加，全部地图）

3D 工具条多了 **「贴图」**（默认勾上）：地形按游戏原贴图渲染，取消勾选就是原来的灰模。

贴图直接从 **AssetRipper 导出的 Unity 工程**转，不再从原始 assets 猜：

```bash
python "docs/guide/地图3D资源导出/代码/scene_export2web.py" --scene level1 --level level1
# 批量：level2..level11 各跑一次，--scene/--level 用同一个 levelN
```

- 默认工程：`00-游戏逆向分析-相关信息/地图3D资源导出/AssetRipper工程/ExportedProject`
- 输出 `geo/web/<level>.bin`（UCFG v2，世界坐标）和 `geo/tex/<level>/*.png`
- 现在 **level1..level11 都已接入贴图**，其它图不再是灰模；旧版 v1 备份已按要求清理
- 资源库、代码、文档和完整执行记录见
  [../docs/guide/地图3D资源导出/需求与执行记录.md](../docs/guide/地图3D资源导出/需求与执行记录.md)
- 跳过的是 `CrossFire/Shadow` 影子代理、`Lit` 灯片、水面；绳网/铁栅栏按 `_AlphaClip` 镂空，不透明帆布/油布保持实体
- 没有 map.json、只有可走面的地图（04 胜利广场、07 死亡擂台）由工作台带 `&level=levelN`
  直接指定 3D 关卡，navview 不会再回退到上一张图（2026-11-23 修复）
- 原理和注意事项见根目录 [README.md](../README.md)「3D 贴图」一节。

### 方向（东南西北）

| 在哪 | 长什么样 | 开关 |
| --- | --- | --- |
| 工作台平面图（俯视图 / 路线 / 区域） | 四边中点写 **北/东/南/西**，右下角一个罗盘：四方位字 + 圈心写「你正对着哪」+ 顶上三角标「画面正上方」 | 地图左上「方向」按钮 |
| 工作台 3D 侧栏（navview 3D） | 同一个罗盘，**跟着视角转**（右侧居中） | 3D 工具条上的「方向」勾选 |
| 3D 查看器单独打开（俯视 + 3D 两栏） | 俯视图四边方位字 + 罗盘；3D 罗盘跟视角转 | 同上（两栏共用一个状态） |
| 游戏内 | 屏幕下方正中的汉字罗盘：**圈会跟着镜头转**、顶部金色三角指针、离正上方最近的方位字点亮，圈心写当前朝向 | 控制台「可视化」页「方向罗盘」；游戏内 **Ctrl+Shift+7** |

**方向约定（三处必须一致，改要一起改）**：

```text
北 = 世界 -Z（平面图 / 3D 俯视的正上方）    东 = 世界 +X（右）
南 = 世界 +Z（下）                         西 = 世界 -X（左）
```

为什么北是 -Z：平面图把世界 x 画到屏幕右、z 画到屏幕下，3D 的「俯视」按钮（yaw = 0）
屏幕上方同样是 -Z，所以「图的上方 = 北」在平面图、3D、游戏里是同一件事。
约定写在 `console/web/nav-studio-app.js` 的 `DIR4/dirScreen`、`console/web/navview.html` 的同名函数、
`src/editor.c` 的 `compass_bucket` 三处。

3D 侧栏的「方向」和工作台平面图的「方向」是 **同一个状态**：在工作台按「方向」，
iframe 用 postMessage 同步过去（不重载 3D）；在 3D 里取消勾选，平面图的按钮也跟着灭。

只读硬限制：

- 保存、部署、还原、撤销/重做、加点/连线/删点、地图命名全部没有；
- `navview.html` 的 `VIEWONLY` 固定为 true，`?edit=1` 后门失效；
- `navserver.py` 所有 POST 返回 405；
- 工作台只发 `GET /api/workbench`、`/api/raw`、`/api/txt`、`/api/profile`。

## 三、七个页面看到的真实数据

| 页面 | 数据来源 | 说明 |
| --- | --- | --- |
| 总览 | `/api/workbench` + 当前地图 | 真实点数/边数/特征点、连通块/孤立点、数据档数字（成品/编辑中/收件箱）、最近文件、按数据算的建议 |
| 路点库 | `<图文件夹>/map.json` | PointNode 可走/不可走、自动连边；出生/补给、蹲守、跳跃、守区/守点、标签区；没有的层显示 0 |
| 路线 | `lines.jump` + `routes[]` | 这个游戏没有手画路线；路线 = 点图 + 自动连边 + Bot_JumpLink；`lines.jump` 为空时不猜配对 |
| 区域 | `features` | 可用的 Bot_NanoGuardArea/Pos、旧 Bot_GuardArea/Pos、标签区；守点按最近守区中心分组，只用于看图 |
| 自动铺设 | `ucf_mod.json` + `<图>/map.json` | 三个开关、当前图会不会触发、源码里的 4 m 采样 / 4.6 m 连边 / 9 m 蹲点 / 每 11 点造守区 |
| 地图数据 | `00_公共/_index.json` + 数据档目录 + `final\` + `packs\` | 11 张图、点/边/特征、可走面、**成品条数 / 编辑中包数 / 导出份数**、数据档汇总（①/②成品/②编辑中）、成品版本、按包查看、命令行 |
| 日志 | `log\ucf_mod.log`（旧部署的根目录那份也认） | 尾部只读、按 自动铺设/导航/编辑/导出/测试包/车测/配置/数据 过滤，默认隐藏 `[at] resolve` |

## 四、文件

运行文件（改这里才会影响页面）：

| 文件 | 是什么 |
| --- | --- |
| `console/web/nav-studio.html` | 七页只读工作台骨架 |
| `console/web/nav-studio.css` | 深色控制台样式（沿用启动器视觉） |
| `console/web/nav-studio-app.js` | 取数、画布、七个页面的渲染逻辑 |
| `console/navserver.py` | 本地只读服务；静态根就是本目录（`/web/` 与 `/navview.html`），提供 `/api/workbench` 汇总接口 |
| `console/web/navview.html` | 2D 俯视 + 3D + 可走面查看器（永久只读）；`?embed=1` 供工作台停靠栏内嵌，只留 3D |

设计稿（不参与运行，已归档到 `archive/design/`）：

| 文件 | 是什么 |
| --- | --- |
| `archive/design/record-mode.html` | 控制台「录制」页的交互样稿（页已实装，只作设计存档） |
| `archive/design/README.md` | 设计稿目录说明（早期三份样稿已不在） |

## 五、数据与调试

- 工作台默认档：成品有当前版看成品，否则有包看编辑中；之后按浏览器 localStorage 记住上次。
  顶栏下拉可切三档；选「编辑中」时旁边选当前图的包。
- 切换接口是 `GET /api/profile?set=native|final|pack`，只改服务内存里读哪套数据，不写文件；
  旧 `?set=dev|deploy` 落成品、`?set=test|export` 落编辑中，并返回一句提示（不报错）。
- 成品档的「成品」列 = 成品当前版里这张图的改动条数；编辑中档的包下拉只列当前图的包，
  指纹对不上的旧包标红禁用，不会套到画布上。
- 地图 JSON 里的 `routes[]` / `zones[]` 只用于查看图层，插件不读，不影响寻路。
- 深链接：`nav-studio.html?page=zones&view=pack&map=01_TransportShip运输船/map.json&pack=01_TransportShip运输船/TransportShip_20261121_143202`
  （`map` 取 `<图文件夹>/map.json`；`pack` 是 `<图文件夹>/<包名>`）。
- 启动服务：控制台 →「路点工作台（查看）」；或 `python console/navserver.py --no-browser`。
- 数据改版后如果页面还是老的，**先把控制台的旧服务关掉重开**（浏览器强刷 Ctrl+F5），
  服务是启动那一刻读的代码。

## 更新记录

```text
2026-11-23  三区 → 数据档（①备份 / ②成品 / ②编辑中）：
            - ③ 部署版从工作台 / navview 的下拉移除（游戏运行目录只供日志 / 配置）；
            - ② 开发版拆成 成品（final 当前版）/ 编辑中（packs，按图选包）；
            - 补 grow 语义（blank/grow = 原生点全禁 + 清单重建）、jump add、edge out/in；
            - 编辑中档点数与游戏一致：151954=196 / 214511=27 / 140112=151 / 143202=111；
            - 旧 ?profile=dev|deploy|test 深链接兼容并提示；默认档按数据自动选、之后记住上次。
2026-11-21  四版 → 三区（①备份 / ②开发 / ③部署）：
            - 顶栏下拉、总览、地图数据页、版本卡片全部改成三版；
            - 一张图一个文件夹：<图文件夹>/map.json + navmesh.bin + 导出/；
            - 新增「成品（final 版本）/ 编辑中（packs）/ 收件箱（vis）」三块数字；
            - 地图表：可走面 / 成品 / 编辑中 / 状态，导出份数挂在图名下；
            - 3D 侧栏支持 WASD 飞行（含 Q/E 升降、Shift 加速，鼠标悬停即可用）。
2026-11-23  目录整理：运行文件从 workbench/ 移到 console/web/，服务从 tools/ 移到 console/；
            URL 从 /workbench/ 改成 /web/（旧的 /workbench/ 与 /studio 仍 302 过去）；
            静态根从 tools/ 收成 console/web/，源码不再能被浏览器下载。
2026-11-19  运行文件从 design/ 移到 workbench/。
2026-11-18  七页结构重做。
```
