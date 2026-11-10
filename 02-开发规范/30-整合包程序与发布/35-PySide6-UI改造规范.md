# PySide6 UI 改造规范

本文档是**未来 UI 层的唯一实现依据**。当前（2.8 开发中）不执行，只作规范冻结；等整合包 2.8 的功能开发收尾、宣布进入 UI 阶段后，按本文档 §10 的步骤执行。

写作风格对齐 31-程序与UI设计规范.md：口语化、能落地、以代码可对照为准。

## 0. 决策与边界

### 0.1 已定结论

| 项目 | 结论 | 理由 |
|---|---|---|
| UI 框架 | **PySide6（Qt 6，LGPLv3）** | 原生控件、DirectWrite 渲染、无浏览器内核依赖；许可证允许闭源分发 |
| 目标系统 | Windows 10 x64 / Windows 11 x64 | 不做跨平台；Frida + IL2CPP 偏移 + Win32 命名管道本身不可移植 |
| 不采用 | React / Electron / Tauri / pywebview | 多一层协议 + 状态所有权重写 + WebView2 依赖；本 UI 只有 6 种控件、约 6 300 行，用不上 Web 组件生态 |
| 不改动 | core/（11 909 行）、features/*/script.js（32 395 行）、Universal-ImGui-Hook.dll、data/*.json 格式 | UI 只是消费者，换实现不能动业务 |
| 打包形态 | 仍为 PyInstaller onedir + Inno Setup | 见 32-打包发布须知.md、34-安装器打包规范-onedir+InnoSetup.md |

### 0.2 本规范解决的问题（对应三个已确认诉求）

| 诉求 | 现状（2.8 实测） | 本规范的解法 |
|---|---|---|
| 三套主题（黑/白/绿）可切换 | 303 处硬编码颜色散在 42 个文件、219 处硬编码字体元组、402 处内联 fg_color=/text_color=；CTk 主题只有约 20 个颜色键，管不到卡片 | §3 三层令牌 + QSS 模板，切换主题 = 换一份 JSON 并 setStyleSheet |
| 卡片圆角 / 阴影 / hover 动效 | CTk 无阴影、无过渡动效，圆角只能整体设 | §4 自绘 CardFrame + 属性动画 + 阴影缓存 |
| 卡片自适应 | 36 处硬编码 columnspan；125% DPI 下靠 text_fit.py 手工测宽兜底 | §5 响应式列数 + setWordWrap + Qt 原生 Per-Monitor DPI |

### 0.3 与 31 文档的分工（避免两套事实）

- **31 文档仍是权威**：窗口分区、状态栏语义、tab 归属、功能清单、卡片交互规则（如「卡片不做整卡点击」）一律以 31 为准。
- **本文档只负责**：视觉令牌、主题文件、控件实现方式、自适应与性能规则、迁移步骤。
- 两者冲突时：**交互语义听 31，实现细节听本文档**。

---

## 1. 概念绑定表

中文给人和 AI 看，英文 ID 给代码用，全部小写下划线。

| 英文 ID | 中文名 | 说明 |
|---|---|---|
| ui_theme_tokens | 主题令牌表 | 一层扁平 dict，键见 §3.3，值全是字符串 |
| theme_pack | 主题包 | 一份覆盖令牌的 JSON，如 themes/green.json |
| semantic_role | 语义角色 | 如 text_primary、accent，不允许按「颜色名」定义令牌 |
| card_frame | 卡片容器 | 自绘圆角/边框/阴影的 QFrame 子类，对应旧 feature_card |
| card_hover_motion | 卡片悬停动效 | 0→1 的 hover 属性动画，驱动底色渐变与阴影 |
| card_elevation | 卡片层级 | 0 = 平面，1 = 悬停浮起；对应阴影强度档位 |
| responsive_columns | 响应式列数 | 按可用宽度算出的网格列数，替代硬编码 columnspan |
| ui_bridge | UI 桥 | QObject + Signal，把 EventBus 的跨线程事件投递到主线程 |
| declarative_renderer | 声明式渲染器 | 读 manifest 的 controls 自动生成卡片 |
| card_context | 卡片上下文 | 渲染器传给 panel.py 的只读对象，含 manifest、回调、令牌 |
| virtual_list | 虚拟列表 | QListView + Model + Delegate，只渲染可见项 |
| token_literal | 令牌字面量 | 代码里直接写死颜色/字号（禁止项） |

旧概念对照：feature_card → card_frame；grid_columnconfigure / columnspan → responsive_columns；text_fit.py → 删除（Qt 原生折行）。

---

## 2. 三条硬原则

1. **零令牌字面量**：ui/ 与 features/*/panel.py 里不允许出现颜色、字号、圆角、间距的字面量。令牌只允许定义在 ui/theme/ 下。
2. **声明式优先**：普通功能卡一律由 declarative_renderer 从 manifest 生成；panel.py 只在特殊卡片和特殊页里出现，且不允许自己创建顶层卡片。
3. **跨线程只走信号**：任何 Frida 回调、worker 线程、atexit 清理都不能直接碰 widget；一律 ui_bridge.emit(...)，由 Qt 队列投递到主线程。

---

## 3. 令牌体系

### 3.1 三层结构

~~~text
primitive（原始值：具体色值/毫秒/像素）
    └─ semantic（语义角色：text_primary、accent、status_danger）
            └─ component（组件尺寸：radius_card、spacing_m、motion_base）
~~~

**代码只允许引用 semantic 与 component 两层**。primitive 只在主题 JSON 内部出现，任何 widget 代码都不许直接写 #3B82F6。

### 3.2 目录与文件

~~~text
ui/theme/
    tokens.base.json      # 三套主题共用：尺寸/字体/动效/圆角（不含颜色）
    themes/black.json     # 深色主题（默认）
    themes/green.json     # 绿色主题
    themes/white.json     # 浅色主题
    theme_manager.py      # 加载、合并、生成 QSS、热切换
    qss/base.qss.tpl      # QSS 模板，占位符用 $token 形式
    icons/                # SVG 图标（禁止 PNG 缩放）
~~~

themes/*.json 必须 UTF-8 无 BOM（见 91-编码与文件规范.md）。JSON 只用双引号，不写注释。

### 3.3 语义令牌清单（颜色）

| 键 | 用途 |
|---|---|
| bg_app | 主窗口背景 |
| bg_surface | 分页面板、设置窗口内容区 |
| bg_card | 卡片底色（平面态） |
| bg_card_hover | 卡片悬停底色 |
| bg_input | 输入框、下拉框、滑块槽 |
| bg_statusbar | 顶部状态栏 |
| border_default | 卡片、输入框默认描边 |
| border_strong | 分隔线、悬停时的高对比描边 |
| border_focus | 键盘焦点环 |
| text_primary | 标题、主要数值 |
| text_secondary | 说明文字 |
| text_disabled | 禁用态文字 |
| text_on_accent | 强调色上的文字 |
| accent | 开启态、主按钮、滑块填充 |
| accent_hover / accent_pressed | 强调色的悬停/按下 |
| accent_subtle | 强调色的淡化底（选中行、标签底） |
| status_success / status_warning / status_danger / status_info / status_idle | 状态圆点与提示条五态，延续 31 文档「绿=已连接、黄=等待、红=断开、灰=空闲」 |
| shadow_rgb / shadow_alpha | 阴影颜色与不透明度（浅色主题必须更淡） |
| overlay_scrim | 免责声明弹窗遮罩 |

### 3.4 组件令牌清单（尺寸/字体/动效，三主题共用）

**令牌值自带单位**（如 "8px"、"11pt"），模板里直接写 $radius_card，不需要花括号拼接单位。

自绘代码里需要的是数字，统一用 ui/theme/units.py 的 px() / pt() 转换：px("8px") → 8，pt("11pt") → 11。**禁止在业务代码里手写 int(x[:-2])**，避免单位格式一变就崩。

| 键 | 值 | 说明 |
|---|---|---|
| radius_card | 8px | 卡片圆角（逻辑像素） |
| radius_control | 6px | 输入框、按钮、下拉框 |
| radius_pill | 999px | 开关、标签药丸 |
| border_width | 1px | 描边宽度 |
| spacing_xs / spacing_s / spacing_m / spacing_l / spacing_xl | 4px / 8px / 12px / 16px / 24px | 内边距与间距 |
| card_padding | 12px | 卡片内边距 |
| card_min_width | 240px | 卡片最小宽度，低于此值触发降列 |
| font_family | "Microsoft YaHei UI" | 统一字体，不再出现 ("Microsoft YaHei", 15) 元组 |
| font_size_xs / sm / base / lg / xl | 9pt / 10pt / 11pt / 13pt / 15pt | 单位 pt（不是 px，见 §5.4） |
| motion_fast / motion_base / motion_slow | 120ms / 180ms / 240ms | 动效时长 |
| easing_standard | OutCubic | 动效缓动 |

### 3.5 三套主题调色板

**theme_black（深色，默认）**

| 键 | 值 | 键 | 值 |
|---|---|---|---|
| bg_app | #0D0F13 | border_default | #262B34 |
| bg_surface | #14171D | border_strong | #3A4250 |
| bg_card | #191D24 | border_focus | #3B82F6 |
| bg_card_hover | #1F242D | text_primary | #E8EBF0 |
| bg_input | #11141A | text_secondary | #98A2B3 |
| bg_statusbar | #12151A | text_disabled | #5B6472 |
| accent | #3B82F6 | text_on_accent | #FFFFFF |
| accent_hover | #60A5FA | status_success | #22C55E |
| accent_pressed | #2563EB | status_warning | #F59E0B |
| accent_subtle | #14243D | status_danger | #EF4444 |
| shadow_rgb | 0,0,0 | status_info | #38BDF8 |
| shadow_alpha | 0.55 | status_idle | #6B7280 |

**theme_white（浅色）**

| 键 | 值 | 键 | 值 |
|---|---|---|---|
| bg_app | #F4F6F8 | border_default | #E2E6EC |
| bg_surface | #FFFFFF | border_strong | #C7D0DB |
| bg_card | #FFFFFF | border_focus | #2563EB |
| bg_card_hover | #F2F6FC | text_primary | #1A1F29 |
| bg_input | #FFFFFF | text_secondary | #5B6472 |
| bg_statusbar | #ECEFF3 | text_disabled | #A3ACB9 |
| accent | #2563EB | text_on_accent | #FFFFFF |
| accent_hover | #1D4ED8 | status_success | #16A34A |
| accent_pressed | #1E40AF | status_warning | #D97706 |
| accent_subtle | #E8F0FE | status_danger | #DC2626 |
| shadow_rgb | 15,23,42 | status_info | #0284C7 |
| shadow_alpha | 0.12 | status_idle | #94A3B8 |

**theme_green（绿色）**

| 键 | 值 | 键 | 值 |
|---|---|---|---|
| bg_app | #0A120E | border_default | #24352B |
| bg_surface | #101A15 | border_strong | #34503D |
| bg_card | #16211B | border_focus | #22C55E |
| bg_card_hover | #1C2A22 | text_primary | #E6F0EA |
| bg_input | #0D1611 | text_secondary | #94A89C |
| bg_statusbar | #0E1712 | text_disabled | #5C6E63 |
| accent | #22C55E | text_on_accent | #04140A |
| accent_hover | #4ADE80 | status_success | #22C55E |
| accent_pressed | #16A34A | status_warning | #EAB308 |
| accent_subtle | #12281B | status_danger | #F87171 |
| shadow_rgb | 0,0,0 | status_info | #38BDF8 |
| shadow_alpha | 0.55 | status_idle | #6B7F72 |

> theme_green 的 text_on_accent 用深色 #04140A：因为 #22C55E 上放白字对比度只有约 2.9:1，放深色字约 7.8:1。

### 3.6 对比度红线

- 正文与说明文字对底色：**≥ 4.5:1**
- 图标、描边、控件边界对底色：**≥ 3:1**
- 新增或修改主题后必须跑 tools/check_theme_contrast.py（§11.3），不达标不许合入。

### 3.7 QSS 生成与热切换

QSS 里全是花括号，**不能用 str.format**（会把 border-radius 的花括号当占位符吃掉）。统一用 string.Template + $token 占位符：

~~~python
from string import Template

def build_qss(template_text: str, tokens: dict) -> str:
    # safe_substitute 遇到未知占位符会原样保留，不会抛异常
    return Template(template_text).safe_substitute(tokens)
~~~

模板片段示例（ui/theme/qss/base.qss.tpl）：

~~~css
QWidget#Shell            { background: $bg_app; }
QWidget#StatusBar        { background: $bg_statusbar; }
QLabel#StatusText        { color: $text_primary; font-size: $font_size_base; }
QLabel[role="hint"]      { color: $text_secondary; }
QPushButton              { background: $bg_input; color: $text_primary;
                           border: $border_width solid $border_default;
                           border-radius: $radius_control; padding: 4px 10px; }
QPushButton:hover        { border-color: $border_strong; }
QPushButton[state="on"]  { background: $accent; color: $text_on_accent; }
QSlider::groove:horizontal   { background: $bg_input; height: 4px; border-radius: 2px; }
QSlider::sub-page:horizontal { background: $accent; border-radius: 2px; }
QSlider::handle:horizontal   { background: $text_primary; width: 12px; margin: -4px 0;
                               border-radius: 6px; }
~~~

切换主题只有三步，**不重建任何控件**：

~~~python
theme_manager.apply("green")   # 1) 合并 base + themes/green.json
                               # 2) build_qss()
                               # 3) QApplication.instance().setStyleSheet(qss)
~~~

规则：

- setStyleSheet **只允许在 QApplication 上调一次**（全局），禁止对单个 widget 调 setStyleSheet——每个控件一份样式表会重复解析并触发全量重算。
- 主题切换后不重启程序；切换耗时要求 ≤ 150ms（§8）。
- 动态状态用 QSS 属性选择器，只在状态变化时对**单个控件**做 repolish：

~~~python
w.setProperty("state", "on")
w.style().unpolish(w)
w.style().polish(w)
~~~

### 3.8 禁止事项

| 禁止 | 原因 | 检查方式 |
|---|---|---|
| 代码里出现 #RRGGBB 字面量 | 主题失效 | §11.3 正则扫描（ui/theme/ 除外） |
| 出现 ("Microsoft YaHei" 字体元组 | 字号散落 | 同上 |
| widget.setStyleSheet(...) | 样式重算风暴 | 同上 |
| 依赖 Qt 默认调色板（不写颜色就用系统色） | 三主题下会串色 | 人工评审 |
| 用 PNG 图标 | 高 DPI 模糊 | 只允许 SVG |

---

## 4. 卡片规范（圆角 / 阴影 / hover 动效）

### 4.1 卡片的样式归属

**卡片底色、描边、圆角、阴影由 CardFrame.paintEvent 自绘；QSS 只负责卡片内部的文字与子控件。**

原因：QSS 的 border-radius 不会裁剪子控件，卡片里嵌入下拉框/滑块时四角会露出方框；自绘 QPainterPath 可同时解决圆角、hover 渐变、阴影缓存三件事，且只走一次绘制。

### 4.2 结构

~~~text
card_frame (CardFrame)
├─ 左上：图标 + 标题（QLabel，可 elide）
├─ 右上：switch / button（QAbstractButton）
├─ 中部：说明文字（QLabel，setWordWrap(True)）
└─ 底部：slider + 数值（可选，QLabel 实时显示）
~~~

尺寸与间距全部取自 spacing_*、card_padding、radius_card，不允许写死像素。

### 4.3 阴影策略（性能红线）

QGraphicsDropShadowEffect 每个实例都会走一次离屏渲染。**40 张功能卡 + 61 张武器卡 = 101 个阴影 effect 会直接拖垮滚动**。规定：

1. **平面态不挂阴影**，只靠 1px border_default 区分边界；
2. **悬停态才出现阴影**，且阴影用「按尺寸缓存的 QPixmap」绘制，不创建 effect：

~~~python
def _shadow_pixmap(self, w: int, h: int, r: int) -> QPixmap:
    key = (w, h, r)
    pix = self._shadow_cache.get(key)
    if pix is None:
        # 用 QPainter 画九宫格模糊边，缓存复用
        pix = _render_shadow(w, h, r, self._t["shadow_rgb"], float(self._t["shadow_alpha"]))
        self._shadow_cache[key] = pix
    return pix
~~~

3. 缓存上限 32 项，超出按 LRU 丢弃；窗口尺寸变化时清空缓存。

**明确禁止**：QGraphicsDropShadowEffect 挂在卡片上；QGraphicsBlurEffect 挂在任何滚动区域内的控件上。

### 4.4 五态定义

| 状态 | 底色 | 描边 | 阴影 | 触发 |
|---|---|---|---|---|
| normal | bg_card | border_default | 无 | 默认 |
| hover | bg_card_hover | border_strong | elevation=1 | 鼠标进入，180ms |
| focus | bg_card | border_focus（2px） | 无 | 键盘 Tab 进入 |
| disabled | bg_card | border_default | 无 | 未连接游戏等不可用场景 |
| error | bg_card | status_danger | 无 | 脚本加载失败、RPC 报错 |

**开启态不换卡片底色**（延续 31 文档「卡片保持紧凑、不做整卡点击」），只用 switch 的 accent 与标题前的状态点表示。

### 4.5 动效参数

| 动效 | 时长 | 缓动 | 属性 |
|---|---|---|---|
| 卡片 hover 底色渐变 | motion_base（180ms） | OutCubic | hover: 0.0 → 1.0 |
| 开关滑块位移 | motion_fast（120ms） | OutCubic | offset |
| 折叠/展开窗口 | motion_slow（240ms） | OutCubic | 窗口几何（唯一允许动几何的地方） |
| Tab 切换内容淡入 | motion_fast | OutCubic | windowOpacity（仅内容容器） |

**禁止**对布局几何做动画（每帧触发重排，滚动区里必然掉帧）。

### 4.6 hover 实现骨架

~~~python
from PySide6.QtCore import Property, QPropertyAnimation, QEasingCurve

class CardFrame(QFrame):
    def __init__(self, tokens, parent=None):
        super().__init__(parent)
        self._t = tokens          # 主题令牌（含单位字符串，绘制前用 px() 转换）
        self._hover = 0.0
        self._shadow_cache = {}
        self._anim = QPropertyAnimation(self, b"hover", self)
        self._anim.setDuration(tokens["motion_base"])
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    # QPropertyAnimation 只能驱动 Qt 认识的属性，必须用 Property 暴露
    def get_hover(self) -> float:
        return self._hover

    def set_hover(self, value: float) -> None:
        self._hover = value
        self.update()

    hover = Property(float, get_hover, set_hover)

    def enterEvent(self, event):
        self._anim.stop(); self._anim.setEndValue(1.0); self._anim.start()

    def leaveEvent(self, event):
        self._anim.stop(); self._anim.setEndValue(0.0); self._anim.start()
~~~

> 注意：Property 必须来自 PySide6.QtCore；用 Python 的 @property 不行，QPropertyAnimation 认不到。

### 4.7 圆角与描边绘制

~~~python
def paintEvent(self, event):
    p = QPainter(self)
    p.setRenderHint(QPainter.Antialiasing, True)
    r = px(self._t["radius_card"])
    path = QPainterPath()
    path.addRoundedRect(self.rect().adjusted(0, 0, -1, -1), r, r)
    p.fillPath(path, self._mix(self._t["bg_card"], self._t["bg_card_hover"], self._hover))
    p.setPen(QPen(QColor(self._border_color()), px(self._t["border_width"])))
    p.drawPath(path)
~~~

矩形要 adjusted(0, 0, -1, -1)，否则 1px 描边会被右/下边界裁掉一半。

---

## 5. 自适应规范

### 5.1 响应式列数

窗口默认 610x700、最小 610x400（31 文档 §1 不变）。列数按**滚动区可用宽度**算，不再硬编码 columnspan：

| 可用宽度 | 列数 | 卡片形态 |
|---|---|---|
| 小于 520px | 1 | 整行卡（标题+开关同行，说明折行） |
| 520 ~ 759px | 2 | 半行卡（当前默认） |
| 760 ~ 1023px | 3 | 等宽三列 |
| 1024px 以上 | 4 | 等宽四列 |

特殊卡（card_type = wide / special_page）固定占满整行，不参与列数计算。

### 5.2 重排规则

~~~python
def on_viewport_resized(self, width: int) -> None:
    cols = self._columns_for(width)
    if cols == self._cols:
        return
    self._cols = cols
    self._relayout(cols)          # 只改 grid 位置，不重建控件
~~~

- resize 事件必须 **50ms 去抖**，否则拖动窗口时每帧重排。
- _relayout 只调用 removeWidget + addWidget，**不销毁控件**，避免重建开关导致状态丢失。

### 5.3 文字规则

| 元素 | 规则 |
|---|---|
| 卡片标题 | 单行，QFontMetrics.elidedText(..., Qt.ElideRight)，悬停显示完整 tooltip |
| 说明文字 | setWordWrap(True)，高度随 heightForWidth 自然撑开 |
| 数值标签 | 固定宽度 + 右对齐，避免数字跳动导致整行抖动 |
| 长列表项 | 虚拟列表内统一 elide，不做多行 |

**text_fit.py 在 Qt 版里删除**：QLabel.setWordWrap 与布局的 heightForWidth 在 125%/150% 缩放下行为正确，不需要手工测宽。

### 5.4 DPI 与字体

- 启动时设置 QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)。
- 字号统一用 **pt**（QSS 里 font-size: 11pt），Qt 会按系统 DPI 换算；**不要用 px 写字号**。
- 所有图标用 SVG；QIcon 会自动按 devicePixelRatio 取合适尺寸。
- 枚举特殊字符（对勾/叉/感叹号/警告）在 Qt 里依赖 Segoe UI Emoji 回退，**不保证三主题下颜色一致**；迁移时统一换成 ui/theme/icons/*.svg。

### 5.5 窗口行为（不改，只验证）

| 行为 | 要求 | 实现 |
|---|---|---|
| 置顶 | 始终在游戏之上 | Qt.WindowStaysOnTopHint |
| 透明度 | 0.92 | setWindowOpacity(0.92) |
| 折叠 | 400x62，位置不变 | 保存/恢复 geometry()，不改 move() |
| 可调整大小 | 是 | 保留系统边框，**不自绘标题栏** |

> 无边框自绘标题栏需要额外处理拖拽、八向缩放、多显示器、DPI 切换四件事；除非明确要求，**Step 1 不做**。

---

## 6. 声明式渲染契约

### 6.1 manifest controls → 控件映射

| type | 控件 | 说明 |
|---|---|---|
| switch | ToggleSwitch（自绘 QAbstractButton） | QSS 无法把 QCheckBox 画成现代开关，必须自绘 |
| slider | QSlider + QSS | setSingleStep 对应原 number_of_steps |
| button | QPushButton | action 字段决定下发哪个 RPC |
| select / combo | QComboBox + QSS | 下拉项样式需 QStyledItemDelegate |
| label / status | QLabel | 只读展示 |
| local_file | QPushButton + QFileDialog | 选文件类 |

渲染器签名：

~~~python
class DeclarativeRenderer:
    def build_card(self, ctx: CardContext) -> dict[str, QWidget]:
        """按 manifest 生成卡片，返回 {handle_name: widget}。"""
~~~

### 6.2 card_type

| layout.card_type | 行为 |
|---|---|
| simple | 按 §5.1 列数自动占 1 列 |
| wide | 占满整行 |
| special_inline | 占满整行，由 panel.py 补充内容，卡片外壳仍由渲染器创建 |
| special_page | 独立整页（白名单见 6.4），不走卡片网格 |

### 6.3 panel.py 降级规则

保留同名文件与 build_card 入口，但**职责收窄**：

1. 只允许往 ctx.body（渲染器给的容器）里加子控件，**禁止创建顶层卡片**、禁止设置卡片底色/边框；
2. 返回的 handle 字典键名沿用 manifest.ui_handles，保证 ui/controllers/*_router.py 不改；
3. 颜色/字体一律从 ctx.tokens 取；
4. 新签名（兼容期两套并存）：

~~~python
def build_card(ctx: CardContext) -> dict[str, QWidget]:
    ...
~~~

旧签名 build_card(scroll, manifest, row, col, colspan, callbacks, card_builder) 在 Step 2 期间保留，Step 3 结束后删除。

### 6.4 特殊页白名单

只有以下 4 个功能允许走 special_page（整页自绘），**新增特殊页必须在本文档登记**：

| 功能 | 目录 | 现有实现 |
|---|---|---|
| 多人生化特性 | features/15_nano4t | ui/views/nano4t_view.py（176 行） |
| 赋予武器 | features/16_weapon_giver | ui/views/weapon_giver_view.py（219 行） |
| 手雷模式 | features/26_grenade_mode | features/26_grenade_mode/panel.py（432 行） |
| 游戏模式切换 | features/27_game_mode_override | 卡片内嵌特殊控件 |

### 6.5 新增的 manifest 可选字段

~~~json
{
  "ui": {
    "icon": "ammo",
    "min_width": 240,
    "columns": 1,
    "tags": ["武器", "常用"]
  }
}
~~~

全部可选，缺省走渲染器默认值；**不改变现有字段语义**，2.8 的 manifest 可以原样加载。

### 6.6 设置窗口的页签（不属于功能特殊页）

设置窗口是独立 QDialog，用 QTabWidget，页签顺序与内容以 31 文档与 33 文档为准：

| 页签 | 内容来源 | 迁移注意 |
|---|---|---|
| 快捷键 | 现 settings_window.py | 快捷键表格改为 QTableView + 虚拟滚动 |
| 关于 | 现 settings_window.py | 版本号仍取 ui/window_contract.py 的 APP_VERSION |
| 免费声明 / 免责声明 | 现 settings_window.py | 长文本用 QTextBrowser，链接用 setOpenExternalLinks(True) |
| 红色主题 | 33-设置页红色主题Tab设计.md | 图片轮播 + 文本翻页，图片走 Qt 资源，禁止在滚动区放 QWebEngineView |

这些页签**都吃同一套令牌**，不允许单独写死颜色；红色主题页的「红」属于内容展示，不作为主题色，切换黑/白/绿时不跟随。

---

## 7. 线程与事件

### 7.1 ui_bridge

~~~python
from PySide6.QtCore import QObject, Signal

class UiBridge(QObject):
    event = Signal(str, object)   # (event_type, payload_dict)
~~~

- EventBus.subscribe 的回调里只做一件事：bridge.event.emit(event_type, payload)。
- 该信号在主线程 connect，Qt 自动用 QueuedConnection 跨线程投递，**天然线程安全**。
- **删除** app._safe_after、_pending_ui_callbacks、_ui_drain_heartbeat（当前三处共约 60 行，见 ui/app.py 第 242-287 行）。

### 7.2 事件映射（保持 4 类 + 插件事件不变）

| EventBus 事件 | 信号 payload | UI 反应 |
|---|---|---|
| log_message | {level, module, message, audience} | 追加日志行（环形缓冲，上限 500 行） |
| connection_status | {status, pid} | 状态圆点/文字/PID，触发 restore_features() |
| feature_status_changed | {feature, enabled} | 更新对应 switch 状态 |
| plugin_event | {feature, event, payload} | 走 PluginEventRouter 同款逻辑 |
| game_connected / game_not_found / game_disconnected | {pid?} | 卡片 enabled 态切换 |

### 7.3 主线程红线

| 禁止 | 替代 |
|---|---|
| worker 线程里创建/修改 widget | bridge.event.emit(...) |
| 主线程里 frida.attach()、读大文件、time.sleep | 丢给现有 _run_in_background |
| 在 paintEvent 里做 IO/分配大对象 | 预计算并缓存 |
| 单次事件处理超过 16ms | 拆批或异步 |

---

## 8. 性能预算

| 指标 | 预算 | 测量点 |
|---|---|---|
| 冷启动到主窗口可交互 | **≤ 800ms** | main() 入口到 show() 后首个 paintEvent |
| 切换 Tab | ≤ 120ms | QStackedWidget.setCurrentIndex 前后 |
| 切换主题 | ≤ 150ms | setStyleSheet 前后 |
| 滚动帧率 | ≥ 55fps（61 张武器卡、1080p、125% DPI） | QElapsedTimer 统计相邻 paint 间隔 |
| 常驻内存 | ≤ 150MB | 任务管理器 / psutil |
| 单次事件处理 | ≤ 16ms | 埋点日志 |

### 8.1 虚拟列表

- 列表项 **超过 200** 时必须用 QListView + QAbstractListModel + QStyledItemDelegate。
- 61 张武器卡**建议**直接走虚拟列表：现在 CTk 版要 ROW_BUILD_BATCH_SIZE = 2 分 21 个 tick 才能画完（ui/views/weapon_giver_view.py 第 186 行），Qt 版一次成型且只画可见行。
- Delegate 内禁止创建子 widget（用 painter.drawText / drawPixmap）。

### 8.2 懒加载

- tab 内容默认 lazy_build = true：首次切到该 tab 才构建；当前 2.8 只有 3 个 manifest 开了懒加载。
- 卡片创建上限：单次事件循环内 **≤ 30 张**，超出的用 QTimer.singleShot(0, next_batch) 续建（保留 2.8 的教训，阈值从 6 提高到 30）。

### 8.3 明确禁止

| 禁止 | 后果 |
|---|---|
| 每张卡挂 QGraphicsDropShadowEffect | 滚动掉到 20fps 以下 |
| 对单个控件 setStyleSheet | 样式重算，切主题时卡死 |
| resize 中同步重建控件 | 拖动窗口卡顿 |
| 每个事件都 create widget | 内存与句柄泄漏 |
| 在滚动区里放 QWebEngineView | 无必要且极慢 |

### 8.4 埋点

统一用 core/log_manager.py 的 log_to_file("debug", "UI", ...) 输出耗时，**只在 debug 级别**，发布版默认关闭。格式固定：

~~~text
[PERF] tab_switch ms=37 tab=weapon_tab
[PERF] theme_apply ms=92 theme=green
[PERF] startup ms=612
~~~

---

## 9. 目录结构（目标形态）

~~~text
ui/
    app.py                  # QApplication 启动、窗口壳、生命周期（对应旧 App）
    shell/
        shell_window.py     # 主窗口（status_bar + tab + log）
        status_bar.py
        collapsed_view.py
    theme/
        theme_manager.py
        tokens.base.json
        themes/{black,green,white}.json
        qss/base.qss.tpl
        icons/*.svg
    widgets/
        card_frame.py       # 自绘圆角/阴影/hover
        toggle_switch.py    # 自绘开关
        labeled_slider.py
        elided_label.py
    render/
        declarative_renderer.py
        card_builder.py
        responsive_grid.py
    pages/
        weapon_giver_page.py
        nano4t_page.py
        grenade_page.py
    dialogs/
        settings_dialog.py
        disclaimer_dialog.py
    bridge/
        ui_bridge.py
        event_mapper.py
~~~

旧的 ui/views/、ui/controllers/、ui/components/ 在 Step 3 结束后删除；controllers 里的路由逻辑先整体搬进 ui/bridge/event_mapper.py，**不要边迁边改逻辑**。

---

## 10. 执行步骤

> 触发条件：用户宣布 2.8 功能开发完成、进入 UI 阶段。**在此之前一行代码都不动。**

### Step 0 · 令牌化原型（3 天，保留 CTk，可回退）

| 事项 | 产出 |
|---|---|
| 抽 ui/theme/tokens.base.json + 三份 theme JSON | 三套调色板 |
| 写 theme_manager.apply(name)，在 CTk 上做最小验证（set_default_color_theme + 逐控件注入颜色） | 主题能在 CTk 上切换（不完美，仅验证令牌表） |
| 把 303 处颜色按 §3.3 分组映射成表 | 附录 B 的收敛清单 |
| 验收 | ① 切主题 < 100ms ② 125% DPI 无裁字 ③ 颜色字面量从 303 降到三份 JSON |

**Step 0 的意义**：如果三套主题在 CTk 上已经够用、卡顿可忍，可以只做 Step 0 就收工，省下 3 周。这是唯一允许「提前结束」的检查点。

### Step 1 · 换壳（1 周）

| 事项 | 文件 |
|---|---|
| QApplication + ShellWindow + StatusBar + 折叠逻辑 | ui/app.py → ui/shell/ |
| UiBridge + 事件映射，删 _safe_after 三件套 | ui/bridge/ |
| Tab 容器（QTabBar + QStackedWidget） | ui/shell/ |
| 设置窗口、免责声明弹窗 | ui/dialogs/ |
| 验收 | 启动 ≤ 800ms、切 Tab ≤ 120ms、连接/断开状态与日志与 2.8 一致 |

### Step 2 · 声明式渲染 + 面板迁移（1.5 周）

| 批次 | 内容 | 数量 |
|---|---|---|
| 2.1 | CardFrame + ToggleSwitch + DeclarativeRenderer + ResponsiveGrid | 4 个组件 |
| 2.2 | 16 个通用面板（≤1.5KB，共 260 行）→ 直接删文件，改走 manifest | 16 |
| 2.3 | 22 个自定义面板（共 3 081 行）→ 按控件映射表机械翻译 | 22 |
| 2.4 | 4 个特殊页（§6.4）单独迁，武器页改虚拟列表 | 4 |
| 验收 | 40 个功能开关/滑块/按钮全部可用；无一个 token_literal；武器页 61 卡滚动 ≥ 55fps |

### Step 3 · 主题收尾 + 打包（3 天）

| 事项 | 说明 |
|---|---|
| 三套主题联调 | 黑/白/绿 × 40 卡 × 4 特殊页，逐页截图留档 |
| 删除 CTk 依赖 | requirements-build.txt 去掉 customtkinter，加 PySide6 并锁定精确版本 |
| 打包调整 | game_modifier_onedir.spec 增加 PySide6 数据收集；excludes 排除 QtNetwork/QtQml/QtQuick/QtWebEngine* 控制体积 |
| 安装器 | packaging/installer.iss 不变，但要核对 platforms/qwindows.dll 是否随包（缺了会报 could not load the Qt platform plugin windows） |
| 许可证 | 关于页/免责声明补一句「本程序使用 Qt for Python (PySide6)，遵循 LGPLv3」 |
| 验收 | Win10 + Win11 双机、100%/125%/150% 三档 DPI、三套主题各跑一遍冒烟 |

### 10.5 回退策略

- UI 重构在**独立分支**进行，main 保留 2.8 CTk 版本。
- Step 1/2 期间加环境变量开关 UCF_UI=ctk|qt，两套入口并存，出问题当天可切回。
- Step 3 完成后删除开关与 CTk 代码。

---

## 11. 编码与检查规范

### 11.1 编码

- 所有 .py / .json / .qss.tpl 为 **UTF-8 无 BOM**（91-编码与文件规范.md）。
- JSON 用双引号，不写注释；QSS 模板允许注释。
- 文件命名 snake_case.py；类名 PascalCase；令牌键 snake_case。

### 11.2 命名

- 新增控件类必须放在 ui/widgets/，不得在 render/ 里定义。
- 渲染器、桥、主题管理器单例化方式与 core 保持一致（get_instance()），避免两套风格。

### 11.3 静态检查脚本

tools/check_ui_tokens.py：三个正则 + 三个退出码，提交前必跑。

| 规则 | 正则 | 允许范围 |
|---|---|---|
| 禁止颜色字面量 | #[0-9a-fA-F]{6} | 仅 ui/theme/ |
| 禁止字体元组 | \(\s*["']Microsoft YaHei | 无 |
| 禁止控件级样式表 | \.setStyleSheet\( | 仅 ui/theme/theme_manager.py |

~~~text
python tools/check_ui_tokens.py
退出码 0 = 通过；1 = 命中禁止项（打印 文件:行）；2 = 脚本自身异常
~~~

另需 tools/check_theme_contrast.py：读三份主题 JSON，校验 §3.6 的对比度，输出不达标组合。

### 11.4 提交前检查清单

1. check_ui_tokens.py 退出码 0
2. check_theme_contrast.py 无告警
3. 三套主题各截一张同页对比图
4. 125% DPI 下无文字裁切
5. 改动涉及列表的，附一帧耗时日志

---

## 12. 验收清单（DoD）

- [ ] 三套主题可运行时切换，无需重启，≤ 150ms
- [ ] 切换后无串色：卡片、文字、描边、状态圆点、滑块、下拉框全部跟随
- [ ] 代码中颜色/字体/圆角字面量为 0（check_ui_tokens.py 通过）
- [ ] 卡片有圆角、悬停有底色渐变 + 阴影、键盘焦点有环
- [ ] 100% / 125% / 150% DPI 下文字不裁切、图标不模糊
- [ ] 窗口宽度 610→1200 拖动时列数平滑变化，不重建控件、不丢状态
- [ ] 武器页 61 张卡滚动 ≥ 55fps
- [ ] 启动 ≤ 800ms、切 Tab ≤ 120ms
- [ ] 连接/断开/重连、功能开关恢复、日志、声明弹窗行为与 2.8 一致
- [ ] Win10 与 Win11 各跑一遍安装+启动+主要功能冒烟
- [ ] requirements-build.txt 已去 customtkinter、加 PySide6 并锁定精确版本

---

## 附录 A · CTk → Qt 控件映射

| 旧（CustomTkinter） | 新（PySide6） | 备注 |
|---|---|---|
| ctk.CTk | QMainWindow | 保留系统边框 |
| ctk.CTkToplevel | QDialog | 设置窗口、免责声明 |
| ctk.CTkFrame | CardFrame（QFrame 子类） | 圆角/阴影自绘 |
| ctk.CTkScrollableFrame | QScrollArea + QWidget | 内容超 200 项改虚拟列表 |
| ctk.CTkTabview | QTabBar + QStackedWidget | 自绘 tab 便于主题化 |
| ctk.CTkSwitch | ToggleSwitch（自绘） | QSS 画不出开关滑块 |
| ctk.CTkSlider | QSlider + QSS | 槽/圆点需自定义 |
| ctk.CTkButton | QPushButton | 全 QSS |
| ctk.CTkOptionMenu / CTkComboBox | QComboBox | 下拉项需 QStyledItemDelegate |
| ctk.CTkLabel | QLabel | setWordWrap / elide |
| ctk.CTkEntry | QLineEdit | |
| ctk.CTkProgressBar | QProgressBar | |
| ctk.CTkCheckBox | QCheckBox | |
| ctk.CTkImage | QPixmap + QLabel / QIcon | 优先 SVG |
| font=("Microsoft YaHei", 15, "bold") | QSS font-family/font-size/font-weight | 字号用 pt |

## 附录 B · 303 处颜色的收敛流程

1. **全量导出**：用正则 #RRGGBB 扫描 ui/ 与 features/，输出 文件:行:值 清单。
2. **去重归一**：按色值分组，统计每个值出现次数（预计收敛到 20~26 个语义角色）。
3. **语义归类**：每个色值必须能落到 §3.3 的某个键；落不下的先记「待定」，不许新造键。
4. **替换**：改取 ctx.tokens["key"] / tokens["key"]；卡片内部优先走 paintEvent。
5. **归零验证**：check_ui_tokens.py 退出码 0。
6. **逐主题目检**：三套主题 × 8 个 tab 截图对比，重点看对比度与状态色。

典型映射参考（以 2.8 现码为例）：

| 现状 | 语义角色 |
|---|---|
| border_color="#4b5563"（卡片描边） | border_default |
| text_color="#e0e0e0" / "#ecf0f1"（标题） | text_primary |
| #98a2b3 一类说明文字 | text_secondary |
| 状态圆点绿/黄/红 | status_success / status_warning / status_danger |

## 附录 C · tokens.base.json 示例

~~~json
{
  "radius_card": "8px",
  "radius_control": "6px",
  "radius_pill": "999px",
  "border_width": "1px",
  "spacing_xs": "4px",
  "spacing_s": "8px",
  "spacing_m": "12px",
  "spacing_l": "16px",
  "spacing_xl": "24px",
  "card_padding": "12px",
  "card_min_width": "240px",
  "font_family": "Microsoft YaHei UI",
  "font_size_xs": "9pt",
  "font_size_sm": "10pt",
  "font_size_base": "11pt",
  "font_size_lg": "13pt",
  "font_size_xl": "15pt",
  "motion_fast": 120,
  "motion_base": 180,
  "motion_slow": 240,
  "easing_standard": "OutCubic"
}
~~~

themes/green.json 只需要覆盖颜色键，缺的键从 base 与 black 继承（加载顺序：tokens.base.json → themes/black.json → themes/name.json）。

单位约定：长度令牌写成 "8px"，字号写成 "11pt"，时长写成纯数字（毫秒）。QSS 模板直接吃字符串；Python 自绘代码用 ui/theme/units.py 的 px()/pt() 转换。

## 附录 D · 风险清单

| 风险 | 影响 | 对策 |
|---|---|---|
| ToggleSwitch / 自绘控件工作量被低估 | Step 2 超期 | Step 2.1 先做这 4 个组件并单独验收，再批量迁面板 |
| 切主题触发全量 repolish，卡一下 | 体验差 | 只调 QApplication.setStyleSheet 一次；实测超 150ms 时改为「先隐藏内容区→切→显示」 |
| PyInstaller 漏收 Qt 插件 | 启动即崩（platform plugin） | spec 里显式校验 platforms/qwindows.dll 存在，打包脚本加断言 |
| 包体增加 60~80MB | 安装包变大 | excludes 排除 QtNetwork/QtQml/QtQuick/QtWebEngine/QtMultimedia，实测后再调 |
| 无边框需求临时加入 | Step 1 变 2 周 | 明确本期不做；要做得单独立项 |
| PySide6 版本升级破坏 QSS | 样式错乱 | 锁定精确版本写入 requirements-build.txt，升级前跑三主题截图对比 |

---

## 更新记录

~~~text
更新日期：2026-11-10
更新说明：新建。冻结 UI 重构路线为 PySide6：三层令牌 + 三套主题（黑/白/绿）+ 自绘卡片（圆角/阴影/hover 动效）+ 响应式列数 + 声明式渲染 + 信号式跨线程桥；明确当前不执行，待 2.8 功能开发收尾后按 §10 四步落地。含 303 处颜色收敛流程、CTk→Qt 控件映射、性能预算与 DoD。
~~~
