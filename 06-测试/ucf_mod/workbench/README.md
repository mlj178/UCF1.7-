# UCF 路点工作台（只读 · 七页）

> 2026-11-18：路点工作台按 `design/nav-studio-launcher.html` 的七页结构重做，数据全部接真实文件。
> 网页端仍然只读；编辑在游戏内完成。
>
> **版本切换**：顶栏右侧下拉可以在 ①备份版 / ②开发版 / ③部署版 / ④测试版 之间切；
> 只改“看哪套 maps/nav”，不写任何文件。navview 顶栏也有同一个下拉。
>
> **2026-11-19**：运行文件从 `design/` 移到本目录 `workbench/`；`design/` 现在只放设计样稿。

## 一、入口与职责

| 入口 | 打开 | 权限 |
| --- | --- | --- |
| 控制台「路点工作台（查看）」 | `workbench/nav-studio.html` | **看**：总览 / 路点库 / 路线 / 区域 / 自动铺设 / 地图数据 / 日志 |
| 左侧「3D / 可走面」或右上「3D 侧栏」 | 同页右侧的停靠栏 iframe（`tools/navview.html?view=1&embed=1&notour=1&profile=<版本>&open=<目录>/<文件>`） | 3D 地形 + 可走面 + 路点/路线/区域图层；**不跳页、不盖住工作台**，换页不断开；拖左边框调宽、双击复位，`关闭 ✕` / `Esc` 收起；开关与宽度记在 localStorage |

停靠栏（2026-11-18 晚改）：侧栏「3D / 可走面」带 **开/关** 徽标；默认 480px，停靠时最右详情列让位给 2D 地图，
地图 / 版本切换后 3D 自动跟到新图。内嵌模式由 `navview.html?embed=1` 提供，只留 3D 画面。

只读硬限制：

- 保存、部署、还原、撤销/重做、加点/连线/删点、地图命名全部没有；
- `navview.html` 的 `VIEWONLY` 固定为 true，`?edit=1` 后门失效；
- `navserver.py` 所有 POST 返回 405；
- 工作台只发 `GET /api/workbench`、`/api/raw`、`/api/txt`、`/api/profile`。

## 二、七个页面看到的真实数据

| 页面 | 数据来源 | 说明 |
| --- | --- | --- |
| 总览 | `/api/workbench` + 当前地图 | 真实点数/边数/特征点、连通块/孤立点、四版时间、最近文件、按数据算的建议 |
| 路点库 | `maps/<图>.json` | PointNode 可走/不可走、自动连边；出生/补给、蹲守、跳跃、守区/守点、标签区；没有的层显示 0 |
| 路线 | `lines.jump` + `routes[]` | 这个游戏没有手画路线；路线 = 点图 + 自动连边 + Bot_JumpLink；`lines.jump` 为空时不猜配对 |
| 区域 | `features` | 可用的 Bot_NanoGuardArea/Pos、旧 Bot_GuardArea/Pos、标签区；守点按最近守区中心分组，只用于看图 |
| 自动铺设 | `ucf_mod.json` + `maps/*.json` | 三个开关、当前图会不会触发、源码里的 4 m 采样 / 4.6 m 连边 / 9 m 蹲点 / 每 11 点造守区 |
| 地图数据 | `_index.json` + 四版目录 | 11 张图、点/边/特征、可走面、编辑数、③部署 SHA256 比对、测试包、命令行 |
| 日志 | `ucf_mod.log` | 尾部只读、按 自动铺设/导航/编辑/导出/测试包/车测/配置/数据 过滤，默认隐藏 `[at] resolve` |

## 三、文件

运行文件（改这里才会影响页面）：

| 文件 | 是什么 |
| --- | --- |
| `workbench/nav-studio.html` | 七页只读工作台骨架 |
| `workbench/nav-studio.css` | 深色控制台样式（沿用启动器视觉） |
| `workbench/nav-studio-app.js` | 取数、画布、七个页面的渲染逻辑 |
| `tools/navserver.py` | 本地只读服务；托管 `/workbench/` 与 `/navview.html`，提供 `/api/workbench` 汇总接口 |
| `tools/navview.html` | 2D 俯视 + 3D + 可走面查看器（永久只读）；`?embed=1` 供工作台停靠栏内嵌，只留 3D |

设计稿（不参与运行，见 `design/README.md`）：

| 文件 | 是什么 |
| --- | --- |
| `design/nav-studio-launcher.html` | 最初的设计稿（已冻结，仅作对照） |
| `design/console-waypoint-tab.html` | 控制台「人机路点」页 + 游戏内 SyPB 式菜单设计稿（可交互；只演示） |
| `design/console-launch-guard.html` | 控制台启动 / 总开关页设计稿 |

## 四、数据与调试

- 工作台读 `UCF_PROFILE` 指定的那一版（默认 ② 开发版）；顶栏下拉可切到 ①/③/④。
- 切换接口是 `GET /api/profile?set=dev|native|deploy|test`，只改服务内存里读哪套 `maps/nav`，不写文件。
- 地图 JSON 里的 `routes[]` / `zones[]` 只用于查看图层，插件不读，不影响寻路。
- 深链接：`nav-studio.html?page=zones&map=09_生化酒店.json&profile=dev`
  （`map` 取 `maps/` 下的文件名；④ 测试版取 `vis/raw/...` 的相对路径）。
- 启动服务：控制台 →「路点工作台（查看）」；或 `python tools/navserver.py --no-browser`。
