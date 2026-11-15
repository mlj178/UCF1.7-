UCF 文件化插件（PoC）

这是新增文件，不属于原版游戏。卸载：删除 winhttp.dll / winhttp_orig.dll / ucf_mod 整个目录
（或运行 ucf_mod\uninstall.ps1，会先还原 level9 再清理）

文件说明：
  winhttp.dll      加载器（UnityPlayer 加载它，再由它加载 ucf_mod\ucf_mod.dll）
  winhttp_orig.dll 系统 winhttp 副本，供加载器转发
  ucf_mod\         插件本体、配置、日志、源码

配置：ucf_mod\ucf_mod.json
  scene / label / game_mode   隐藏地图注入（Nano30_Storm）

功能 1：隐藏地图注入
  把 Nano30_Storm 作为一张可选地图插进房间下拉框。

功能 2：自动补 A* 导航点（2026-11-14 已验证）
  隐藏图点图为空 → Bot.Update 每帧空引用 → 人机原地乱跳。插件进图时自动：
  4 米网格射线采样 → 建 UCF_WayPoints → 设为 PointGraph.root → maxDistance 改 6
  → Scan() → ConnectNodes()（★Scan 只建节点不建连线）。
  实测：826 节点 / 抽样 300 中 284 有连接 / 1366 条连接。

功能 3：人机标记编辑器（Ctrl+数字）  2026-11-15 阶段 0+1+2 已验证
  Ctrl+1   开/关编辑模式
  Ctrl+2   在准星地面放蹲守点（Bot_CrouchPos）
  Ctrl+Del 删除准星瞄准的那个标记（射线优先，其次准星落点 12 米内）
  Ctrl+5   撤销最后一个
  Ctrl+6   保存到 ucf_mod\markers\markers.txt
  Ctrl+7   重新从文件加载（丢弃未保存的）
  Ctrl+8   切换新蹲守点阵营 BL/GR
  Ctrl+9   状态写日志（含游戏静态表计数）
  Ctrl+0   显示/隐藏所有标记球
  Ctrl+3 / Ctrl+4 放置幽灵守点 / 区域 —— 本版禁用（见下"仍未解决"）

  标记颜色：蹲守点=红  幽灵点=绿  区域=蓝  跳跃=黄（后两种随功能解禁生效）
  左上角 HUD 常驻显示：编辑模式 / 阵营 / 可视化 / 标记数量 / 快捷键提示
  标记球 = 0.24 米球体，浮在落点上方 0.45 米，不投影、无碰撞（不干扰游戏射线）

功能 4：自动补蹲守点（2026-11-14，2026-11-15 修正共存）
  同一批采样点上 AddComponent<Bot_CrouchPos>（team=BlackList），Awake 自动注册。
  只在"除本编辑器放的点之外该图没有任何蹲守点"时触发。
  实测：existing=11 (editor-made=11) → created=147 registered=158。

踩过的坑（都已修，别再踩）：
  * CreatePrimitive 运行期拿到的是 Hidden/InternalErrorShader（build 把 Standard 裁了），
    必须自己 Shader.Find("Universal Render Pipeline/Unlit") 建材质；
  * 相机 cullingMask 实测 0x1f3，**layer 2(Ignore Raycast) 不在其中**，
    阶段 1 标记球"创建成功但看不见"就是这个原因 → 现在放 layer 0；
  * HUD 字体从游戏现有 UI Text 借（Font 对象），所以中文能显示；
    Resources.GetBuiltinResource(Arial.ttf) 只作兜底（无中文）。
  * Unity API 必须在主线程：按键走 WndProc(WM_KEYDOWN)，换场景走 WM_APP+0x52，
    WM_APP+0x53 = 无焦点注入按键（自动化测试用，wParam=虚拟键码）。

仍未解决的（内容层）：
  * 幽灵守卫区 Bot_NanoGuardArea / Bot_NanoGuardPos：Awake 先读 posList，
    AddComponent 出来的对象该字段为 null → 注册了但没点 → Bot.Update 每帧 NRE。
    要先造 posList(List<Bot_NanoGuardPos>)、entrancePos 空数组、zoomPos≥1 才能启用。
  * 跳跃链接 Bot_JumpLink：必须绑定 A* 图节点对，需在 Scan 后挂。
  * 补给箱点 / 阵营出生点：MapManager.pointDic（BL/GR/SupplyBox/RedBox/BlueBox），
    隐藏图缺 SupplyBox → 偶发 GetSupplyBoxPoint 空引用（不影响游玩）。

日志：ucf_mod\ucf_mod.log（[nav] 导航 / [edit] 编辑器）
标记文件：ucf_mod\markers\markers.txt（纯文本可手改，一行一个点）
源码备份：ucf_mod\src\*.c ；二进制备份：ucf_mod\src\ucf_mod.<日期>.bin

2026-11-15 修复（完整记录见 FIX_2026-11-15.md）
  * 退出卡死：nav/注入后台线程退出时不再调 il2cpp（只 PostMessage），
    WM_DESTROY 恢复旧窗口过程；实测退出 0.5~1.1 s，日志有 [nav]/[edit] quit 行。
  * 幽灵卡在复活点：隐藏图原本 0 个 Bot_NanoGuardArea/Pos，Ghost 的
    NanoGuard 没有目标。插件运行时造 42 个守卫区（每区 1~2 守点 + 邻居链接），
    SpareAreaList 42；实测 29 个 Bot 中 19 个 60 s 位移 >15 m。
  * 导航：多层射线采样（屋顶+室内）+ 出生点 170 个节点 + 连线 raycast 遮挡，
    最终 694 节点；Bot.Update NRE 从 1595 条降到 27 条且不再增长。
  * 仍未解决：Bot_JumpLink、SP_RedBox/SP_BlueBox（补给箱 NRE）、
    7/29 个 Bot 仍留在出生洞穴。

2026-11-15 第二轮：导航可视化编辑器（完整记录见 VISUALIZER_2026-11-15.md）
  Ctrl+V            可视化总开关（A 路点 / B 人类 / C 幽灵 / D 出生 / E 模式）
  Ctrl+Shift+1..5   分层开关              Ctrl+Shift+L 标签：关/近距/全部
  Ctrl+E            导出 vis/graph_*.json Ctrl+H      快捷键面板
  Delete            删除准星最近的手工标记（不再需要 Ctrl）
  截图：screenshots/vis_hud_hotkeys.png、screenshots/vis_ingame_layers.png
2026-11-15 第三轮：文字标签默认关闭
  开机只画线框/方块/颜色，屏幕上不再有浮动中文标签（之前“全部显示”时 344 个标签重叠）。
  Ctrl+Shift+L 仍可开回：关（默认）→ 近距 35 m → 全部。
  顶部状态栏与 Ctrl+H 快捷键面板保留。

2026-11-15 第四轮：离线导航数据编辑器（P0/P1 已完成）
  * 导出格式升级 v1：节点带 64 位稳定 id（坐标哈希）、地图指纹、来源(ours/game)、包围盒。
    契约见 NAVGRAPH_FORMAT.md（字段表 / id 算法 / patch 与 full 语义 / V1-V6 校验规则）。
  * 目录约定：vis\ 只放原始扫描（只增不改），nav\ 放编辑后的权威数据（一图一文件）。
  * 新增 tools\navview.html（单文件，双击即用，无需安装）：
      滚轮缩放 / 拖动平移 / 单击看节点与邻居 / F 适应视图 / G 下一个孤立点
      图层开关、孤立节点标红、连通分量统计、V1-V6 校验、特征点定位
  * 用 Storm 的实测扫描跑出来的结果：694 节点 / 1132 边，孤立 95 个(13.7%)，
    连通分量 139 个，最大分量仅 250 个节点——寻路图本身是碎的，这是幽灵卡住的直接解释。

2026-11-15 第五轮：3D 导航编辑器 v0.1（离线读图 + 自由相机）
---------------------------------------------------------------
新增 tools/navedit/：独立桌面程序（PyQt5 + moderngl），不用开游戏。
  * 选一次 UnityCrossFire_Data 目录 -> 列出 level0..level11
  * 选中 level9（生化幽灵·风暴）即可在 3D 里飞行查看地形
  * 自动叠加 vis/ 下最新导出的路点与连线
  * 右键转视角 / WASD 移动 / QE 升降 / F 聚焦 / Tab 俯视
实测：资源索引 0.34 秒；Storm 几何 113 块 / 64,508 三角形 / 1 秒提取，
      缓存后 0.01 秒；渲染 60+ FPS（Intel UHD，读回 QImage 方式）。
全场景提取结果（三角形数）：
  level1 1,377,197 | level2 18,569 | level3 15,810 | level4 22,054
  level5 4,609 | level6 21,901 | level7 33,790 | level8 64,872
  level9 64,508 | level10 27,556 | level11 23,253 | level0 无网格(主菜单)
用法见 tools/navedit/README.md。

2026-11-15 第五轮补充：进图自动导出路点
---------------------------------------------------------------
* navfix 建好路点图后，插件会自动等 2 秒再导出一份 JSON（不用按 Ctrl+E）。
* 文件落在 vis/<地图名>_<时间戳>.json，一张图进一次就有一份。
* 关闭自动导出：editor_set_auto_export(0)（暂无热键）。
* 为什么只能进游戏导：路点是运行时生成的，资源文件里没有；
  离线用网格重算对不上（实测 Storm 重算出 5412 点/覆盖全场，游戏只有 694 点/只覆盖竞技场）。

2026-11-15 第六轮：自动导出修正 + 只读采集模式（v0.2）
---------------------------------------------------------------
【问题】第五轮补充的自动导出实际上一次都没触发：
  vis\ 里从头到尾只有 11:53 那一份 Storm 的 graph_20261115_115359.json。
  原因：导出条件写成了「navfix 自己重建过图之后」才导出（editor_mark_dirty 只在
  build_waypoints 末尾调用），而 build_waypoints 只在 nodeCount==0 时才跑。
  14:44~14:48 那批地图游戏自己就建了图（日志里一次 scan done 都没有），
  所以永远走不到导出那一步。

【改法】导出触发改到 navfix 每 tick 的统一入口：
  editor_tick -> auto_export_tick()：只要当前场景的路点图有节点、且节点数稳定
  约 2 秒，就落一份 JSON，不管这图是游戏建的还是我们建的。
  同时日志补一行 auto-export: graph stable at N nodes。

【新增】只读采集模式（collect-only）
  * 开关：ucf_mod\collect.flag 存在 = 开；游戏里 Ctrl+Shift+X 也可切换（并写/删该文件）。
  * 开启后插件完全不改游戏状态：
      - 不建路点（不调 Scan / ConnectNodes）
      - 不建蹲守点、不建幽灵守区、不 purge 守区
      - 不创建 HUD/文字/网格等任何 GameObject（导出走 collect_read()，只读不建）
  * 屏幕上不会有任何显示，反馈全在 ucf_mod.log：
      mode: COLLECT-ONLY 只读采集
      auto-export: graph stable at N nodes, writing JSON
      vis: exported nodes=... edges=... features=... map='...' -> ...\vis\xxx.json
      hb: collect-only map='...' nodes=N     （每 5 秒一行心跳，崩溃时可定位到地图）
  * 小地图没名字时文件名用指纹：map_n<节点数>-<哈希>_<时间戳>.json，避免互相覆盖。

【为什么加这个模式】14:47~14:48 连崩 4 次（事件日志：GameAssembly.dll +0x1290B1 /
  +0x1290C1 访问冲突，另一次 unknown 模块 offset 0 即跳空指针）。11:25~11:46 也有
  11 次 UnityPlayer.dll +0x0076019D 同点崩溃——那时还没有自动导出，说明闪退不是
  本次改动引入的。采集模式把「进图会动的代码」压到最少，尽量规避这类崩溃。

【已验证】DLL 218,180 B / MD5 F10CDBDEB4E6F237C2FCD2CC972735B8，字符串自检通过；
  旧版备份 ucf_mod.dll.bak_214836。

2026-11-15 第七轮：导航编辑器 v0.2 —— 贴图 + 点选检视
-----------------------------------------------------------
【目标】编辑器之前只有灰白几何，分不清「这是什么」。这一轮把地图贴图、材质、
       物体名都接进来看，并支持左键点选查看。

【能读到的资产（实测）】
  Texture2D 3557   Material 1640   Mesh 1421   Shader 121   全游戏
  level9(Storm) 113 块 / 110 材质 / 110 贴图；level8 157 块 / 82 贴图。

【关键坑 1】Texture2D 读不出来
  UnityPy 1.25.4 对这个构建的 Texture2D typetree 少了 24 字节（m_PlatformBlob），
  正常 read() 全部抛：ValueError: Expected to read 164 bytes, but only read 140。
  3557 张贴图一张都拿不到。
  绕过：ObjectReader.read_typetree(check_read=False)，字段能完整拿到
  （m_Name / m_Width / m_Height / m_TextureFormat / m_StreamData）。

【关键坑 2】贴图在 .resS 里
  DXT1/DXT5 的像素不在 .assets 内，按 m_StreamData.offset/size 去
  resources.assets.resS 读，再用 texture2ddecoder.decode_bc1/bc3 解。
  512x512 一张约 1.4 ms。

【坑 3】Shadow 材质是阴影专用副本
  level8 有 75 块网格用 CrossFire/Shadow 材质，是同一批模型的投影副本，
  当普通几何画出来就是一层层灰白板子。默认隐藏（菜单「显示阴影体」可开）。

【坑 4】ALPHA_Blocker / collision / invisible
  这类是看不见的阻挡体，名字里带 blocker/collision/invisible，默认隐藏。
  Storm 那块 ALPHA_Blocker（1817 面）之前就是挡在视野中间的黑墙。

【坑 5】透明贴图变实心
  DXT5/BC3 的树、栏杆、铁丝网带 alpha，不做 alpha 裁剪就是一块块实心片。
  按 0.35 阈值 discard；水面（CrossFire/Water）走 0.55 半透明。

【新增功能】
  * 几何缓存升到 v4：顶点 + 法线 + UV + 索引 + 分块表（每块名字/材质/贴图/范围）。
  * 贴图落盘：ucf_mod\geo\tex\<场景>\<贴图名>.png（首次提取时解码，之后直接用）。
  * 视口按块绘制，每块绑自己的贴图；T 键开关贴图，关掉回到顶点色。
  * 左键点选：CPU 射线-三角形求交，1.37M 面的 level1 也只要约 60 ms。
  * 右侧「检视」面板：对象名 / 网格名 / 材质 / 着色器 / 贴图缩略图 / 面数 /
    点击坐标 / 距离 / 最近路点（编号 + 距离）。
  * 菜单「视图」新增：显示贴图、显示阴影体、显示网格。

【实测数据（全部 11 张图已提取并缓存）】
  场景    三角形     分块  带贴图  用时
  level1  1,377,197   137    71    4.6s
  level2     18,569    97    85    0.7s
  level3     15,810    79    70    0.6s
  level4     22,054    97    92    0.7s
  level5      4,609    47    47    0.3s
  level6     21,901    44    39    0.6s
  level7     33,790    72    68    0.6s
  level8     64,872   157    82    1.0s
  level9     64,508   112   109    0.9s
  level10    27,556   108   107    0.9s
  level11    23,253    66    65    0.6s
  渲染 65~110 FPS（Intel UHD，1280x720~1600x950）。

【新发现，下一轮处理】
  level1 的主网格是静态合批（GameObject 名 "Combined Mesh (root: scene)"），
  一个 19673 面的合并网格横跨全图；点选只能定位到"合批块"，不能定位到单个道具。
  要精确到道具，得按材质/顶点范围再切分，或改用未合批之前的原始网格。

【未做】粒子系统 555 个、贴花、天空盒、动画物体（只取静态网格）。
