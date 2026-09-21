"""统一 UI 设计令牌（Design Token）。

新样式统一从这里取值，不要在 widget 参数里直接写十六进制颜色或字号。
"""

FONT_FAMILY = "Microsoft YaHei UI"
FONT_MONO = "Consolas"

# --- 字阶（固定四级）---
FONT_TITLE = (FONT_FAMILY, 15, "bold")
FONT_SECTION = (FONT_FAMILY, 13, "bold")
FONT_BODY = (FONT_FAMILY, 12)
FONT_BODY_BOLD = (FONT_FAMILY, 12, "bold")
FONT_CAPTION = (FONT_FAMILY, 11)
FONT_MONO_BODY = (FONT_MONO, 11)

# --- 底色层级 ---
BG_WINDOW = "#0f1115"
BG_BAR = "#171a20"
BG_CARD = "#1e222a"
BG_INNER = "#262b34"
BG_HOVER = "#2f3540"

# --- 描边 ---
LINE = "#2e343e"
LINE_STRONG = "#3a424e"

# --- 文字层级 ---
FG_PRIMARY = "#f3f5f8"
FG_BODY = "#b8c0cc"
FG_MUTED = "#7d8694"
FG_DISABLED = "#5a626e"

# --- 强调色与语义色 ---
ACCENT = "#4c8dff"
OK = "#34d399"
WARN = "#fbbf24"
ERR = "#f87171"

# --- 几何 ---
RADIUS_CARD = 10
RADIUS_CONTROL = 8
RADIUS_PILL = 999

PAD_XS = 4
PAD_SM = 8
PAD_MD = 12
PAD_LG = 16

HEIGHT_BUTTON = 32
HEIGHT_BUTTON_ACTION = 36
WIDTH_SWITCH = 44
HEIGHT_SWITCH = 24
WIDTH_BADGE = 64
HEIGHT_BADGE = 20