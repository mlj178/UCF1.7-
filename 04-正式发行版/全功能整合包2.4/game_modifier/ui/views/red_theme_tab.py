# -*- coding: utf-8 -*-
"""红色主题 Tab

实现见《02-开发规范/30-整合包程序与发布/33-设置页红色主题Tab设计.md》。
两个区块（图片轮播 / 文字展示）共用一套控制条交互：
「‹ + X / N + ›」同一行，到头置灰，默认不循环。

资源根目录：RESOURCE_DIR/红色图片|红色文案
- 图片：<序号>.jpg，按文件名数字升序
- 文字：text.txt，按空行分段，按段落顺序展示

资源不齐时区块降级为占位提示，不阻断其他区块。
"""

import os
import re
import json

import customtkinter as ctk

from core.config import RESOURCE_DIR


# ---------- 模块级常量 ----------

# 图片等比缩放容器尺寸（设置窗口 500 宽，留 padding 后约 430）
_IMAGE_CONTAINER_W = 430
# 图片缩放目标高度（为下方描述区预留约 60px）
_IMAGE_CONTAINER_H = 240
# 文档 §5.1：图片区内容区固定高度（图片 240 + 描述约 60 = 300）
_IMAGE_CONTENT_H = 300
# 文字展示区内容区固定高度：容纳最长语录（约 60 字 2-3 行 + 出处行），
# 短语录下方留少量空白；极少数超长语录启用内部滚动，不撑高容器
_TEXT_CONTENT_H = 130

# 红色主题配色（文档 §5.5 占位，后续补充具体色值）
_BLOCK_BG = "#2a1a1a"        # 区块背景：暗红
_TEXT_RED = "#CC0000"        # 文字主色（文档 §5.4 指定）
_TEXT_LIGHT = "#FFAAAA"      # 浅红文字（标题）
_TEXT_DIM = "#888888"        # 置灰/占位文字
_BTN_BG = "#8B0000"          # 按钮常态：深红
_BTN_HOVER = "#CC0000"       # 按钮悬停：正红


# ---------- 资源加载 ----------

def _numeric_key(filename):
    """从文件名提取首个数字用于排序；无数字的排最后。

    避免「10.jpg」排在「2.jpg」前面（字符串排序的坑）。
    """
    match = re.search(r'\d+', filename)
    if match:
        return (0, int(match.group()))
    return (1, filename)


def _load_image_metadata():
    """加载 红色图片 目录下的图片元数据。

    优先读取 红色图片/images.json（人工维护 title/description/order）。
    JSON 不存在或损坏时，回退到扫描目录按文件名数字升序。

    返回 list[dict]，每项含：
        path:         图片绝对路径
        filename:     文件名
        title:        标题（可为空）
        description:  描述（可为空）
    """
    folder = os.path.join(RESOURCE_DIR, "红色图片")
    if not os.path.isdir(folder):
        return []

    json_path = os.path.join(folder, "images.json")
    if os.path.isfile(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            items = data.get("images", []) if isinstance(data, dict) else []
            result = []
            for item in items:
                if not isinstance(item, dict):
                    continue
                fname = item.get("filename", "")
                if not fname:
                    continue
                fpath = os.path.join(folder, fname)
                if not os.path.isfile(fpath):
                    # JSON 里登记了但文件缺失，跳过
                    continue
                result.append({
                    "path": fpath,
                    "filename": fname,
                    "title": str(item.get("title", "") or ""),
                    "description": str(item.get("description", "") or ""),
                    "_order": item.get("order", 0),
                })
            # 按 order 升序，order 相同或缺失时按 filename 数字
            result.sort(key=lambda m: (m["_order"], _numeric_key(m["filename"])))
            return result
        except (json.JSONDecodeError, OSError):
            # JSON 损坏则回退到目录扫描
            pass

    # 回退：扫描目录
    files = [f for f in os.listdir(folder)
             if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    files.sort(key=_numeric_key)
    return [{
        "path": os.path.join(folder, f),
        "filename": f,
        "title": "",
        "description": "",
        "_order": 0,
    } for f in files]


def _load_quotes():
    """加载 红色文案/mao_zedong_quotes.json，展平为语录列表。

    按 categories 顺序遍历，每个 category 内按 quotes 数组顺序，
    返回 list[dict]，每项含：
        content:  语录正文
        source:   出处（可为空）
        date:     时间（可为空）
    """
    file_path = os.path.join(RESOURCE_DIR, "红色文案", "mao_zedong_quotes.json")
    if not os.path.isfile(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(data, dict):
        return []
    result = []
    for category in data.get("categories", []):
        if not isinstance(category, dict):
            continue
        for quote in category.get("quotes", []):
            if not isinstance(quote, dict):
                continue
            content = str(quote.get("content", "") or "").strip()
            if not content:
                continue
            result.append({
                "content": content,
                "source": str(quote.get("source", "") or "").strip(),
                "date": str(quote.get("date", "") or "").strip(),
            })
    return result


# ---------- 通用区块基类 ----------

class _RedMediaBlock(ctk.CTkFrame):
    """红色主题通用区块：标题 + 内容区 + 控制条（‹ + X / N + ›）。

    子类实现 _render_content() 渲染当前索引对应的内容。
    """

    def __init__(self, master, total_count, title, content_height=None):
        super().__init__(master, fg_color=_BLOCK_BG, corner_radius=6)
        self._total = max(1, total_count)
        self._index = 0

        # 区块标题（title 为空则不显示，不占空间）
        if title:
            ctk.CTkLabel(
                self, text=title,
                font=("Microsoft YaHei", 13, "bold"),
                text_color=_TEXT_LIGHT,
            ).pack(pady=(8, 4))

        # 内容容器（子类在 _render_content 中填充）
        # 文档 §5：容器固定高度，内容适配容器，切换时不抖动
        self._content_frame = ctk.CTkFrame(self, fg_color="transparent")
        if content_height is not None:
            # 固定高度，锁死容器，内容在内部居中/滚动
            self._content_frame.configure(height=content_height)
            self._content_frame.pack_propagate(False)  # 禁止子控件撑高容器
        self._content_frame.pack(fill="both", expand=True, padx=8, pady=4)

        # 控制条：‹ + position_label + › 同一行
        # 三个元素紧贴成一组、整体居中（按钮贴近位置标签，仅保留小间距），
        # 不分散在内容区两侧
        nav = ctk.CTkFrame(self, fg_color="transparent")
        nav.pack(fill="x", padx=8, pady=(0, 8))

        center = ctk.CTkFrame(nav, fg_color="transparent")
        center.pack(expand=True)

        self._prev_btn = ctk.CTkButton(
            center, text="‹", width=40,
            fg_color=_BTN_BG, hover_color=_BTN_HOVER,
            command=self._on_prev,
        )
        self._prev_btn.pack(side="left", padx=(0, 6))

        self._pos_label = ctk.CTkLabel(
            center, text="1 / 1",
            font=("Microsoft YaHei", 12),
            text_color=_TEXT_LIGHT,
        )
        self._pos_label.pack(side="left", padx=6)

        self._next_btn = ctk.CTkButton(
            center, text="›", width=40,
            fg_color=_BTN_BG, hover_color=_BTN_HOVER,
            command=self._on_next,
        )
        self._next_btn.pack(side="left", padx=(6, 0))

        # 首次渲染（此时子类 _render_content 已可用）
        self._render_content()
        self._update_nav()

    # ---- 子类重写 ----

    def _render_content(self):
        """按 self._index 在 self._content_frame 内渲染内容。"""
        raise NotImplementedError

    # ---- 控制条逻辑 ----

    def _update_nav(self):
        # 文档 §4：位置标签格式「X / N」，数字和斜杠之间各有一个空格
        self._pos_label.configure(text=f"{self._index + 1} / {self._total}")
        # 到第一个左按钮置灰，到最后一个右按钮置灰
        self._prev_btn.configure(state="normal" if self._index > 0 else "disabled")
        self._next_btn.configure(
            state="normal" if self._index < self._total - 1 else "disabled"
        )

    def _on_prev(self):
        if self._index > 0:
            self._index -= 1
            self._render_content()
            self._update_nav()

    def _on_next(self):
        if self._index < self._total - 1:
            self._index += 1
            self._render_content()
            self._update_nav()


# ---------- 两个具体区块 ----------

class _ImageCarousel(_RedMediaBlock):
    """图片轮播区：等比缩放 + 居中，不裁剪不变形。

    在图片下方展示 title / description（来自 images.json，可为空）。
    """

    def __init__(self, master, image_meta):
        # image_meta: list[dict]，含 path/title/description
        self._image_meta = image_meta
        self._ctk_image = None  # 持有引用防 GC
        # 不显示区块标题（按需求去掉「图片轮播」字样）
        super().__init__(master, len(image_meta), "",
                         content_height=_IMAGE_CONTENT_H)

    def _render_content(self):
        for w in self._content_frame.winfo_children():
            w.destroy()
        meta = self._image_meta[self._index]
        path = meta["path"]
        title = meta.get("title", "")
        description = meta.get("description", "")

        try:
            from PIL import Image
            img = Image.open(path)
            # 等比缩放到容器尺寸内（不裁剪、不变形）
            img.thumbnail((_IMAGE_CONTAINER_W, _IMAGE_CONTAINER_H), Image.LANCZOS)
            self._ctk_image = ctk.CTkImage(
                light_image=img, dark_image=img, size=img.size
            )
            label = ctk.CTkLabel(self._content_frame, image=self._ctk_image, text="")
            label.pack(expand=True)
        except Exception as e:
            ctk.CTkLabel(
                self._content_frame, text=f"图片加载失败: {e}",
                font=("Microsoft YaHei", 11), text_color=_TEXT_RED,
            ).pack(expand=True)

        # 图片下方展示标题与描述（任一非空才显示，居中）
        if title or description:
            desc_frame = ctk.CTkFrame(self._content_frame, fg_color="transparent")
            desc_frame.pack(fill="x", pady=(4, 0))
            if title:
                ctk.CTkLabel(
                    desc_frame, text=title,
                    font=("Microsoft YaHei", 12, "bold"), text_color=_TEXT_LIGHT,
                    wraplength=410, justify="center", anchor="center",
                ).pack(fill="x")
            if description:
                ctk.CTkLabel(
                    desc_frame, text=description,
                    font=("Microsoft YaHei", 11), text_color=_TEXT_LIGHT,
                    wraplength=410, justify="center", anchor="center",
                ).pack(fill="x")


class _TextViewer(_RedMediaBlock):
    """文字展示区：展示毛泽东语录，正文 #CC0000，出处用浅色小字。

    文档 §5.2：内容区固定 180px，超长语录用 CTkTextbox 内部滚动，不撑高容器。
    """

    def __init__(self, master, quotes):
        # quotes: list[dict]，含 content/source/date
        self._quotes = quotes
        super().__init__(master, len(quotes), "",
                         content_height=_TEXT_CONTENT_H)

    def _render_content(self):
        for w in self._content_frame.winfo_children():
            w.destroy()
        quote = self._quotes[self._index]
        content = quote.get("content", "")
        source = quote.get("source", "")
        date = quote.get("date", "")

        # 用 CTkTextbox 实现：固定高度内部滚动，超长语录不截断也不撑高容器
        # 注意：fg_color 不能用 "transparent"（CTkTextbox 透明背景会导致内容不渲染），
        #       用区块背景色融入
        textbox = ctk.CTkTextbox(
            self._content_frame,
            font=("Microsoft YaHei", 16),
            text_color=_TEXT_RED,
            fg_color=_BLOCK_BG,
            wrap="word",
            activate_scrollbars=True,
        )
        textbox.pack(expand=True, fill="both", padx=4, pady=(4, 2))

        # 写入正文
        textbox.insert("1.0", content)
        # 出处与时间（拼接，非空才追加到末尾）
        meta_parts = [p for p in (source, date) if p]
        if meta_parts:
            # 记录正文末尾位置，用 index 精确定位出处行起止（比手算行号稳健）
            meta_start = textbox.index("end-1c")
            meta_text = "\n—— " + "　".join(meta_parts)
            textbox.insert("end", meta_text)
            textbox.tag_add("meta", meta_start, "end-1c")
            # CTkTextbox.tag_config 禁止 font 选项（会抛 AttributeError，导致整个
            # 文字展示区初始化失败、内容不显示），改用底层 tkinter.Text.tag_configure
            # 同时设置出处行的字号与浅红颜色
            inner_text = getattr(textbox, "_textbox", textbox)
            inner_text.tag_configure(
                "meta",
                font=("Microsoft YaHei", 10),
                foreground=_TEXT_LIGHT,
            )
        textbox.configure(state="disabled")  # 只读


class _PlaceholderBlock(ctk.CTkFrame):
    """资源未就绪时的占位区块（分阶段上线用）。"""

    def __init__(self, master, title, hint):
        super().__init__(master, fg_color=_BLOCK_BG, corner_radius=6)
        ctk.CTkLabel(
            self, text=title,
            font=("Microsoft YaHei", 13, "bold"), text_color=_TEXT_LIGHT,
        ).pack(pady=(8, 4))
        ctk.CTkLabel(
            self, text=hint,
            font=("Microsoft YaHei", 11), text_color=_TEXT_DIM,
        ).pack(pady=(0, 8))


# ---------- 对外入口 ----------

def build_red_theme_tab(tab_frame):
    """在 settings_window 的「红色主题」tab 内构建两个区块。

    按文档 §2 从上到下竖向排列：图片轮播 → 文字展示。
    资源不齐的区块降级为占位提示，不影响其他区块。
    """
    scrollable = ctk.CTkScrollableFrame(tab_frame, fg_color="transparent")
    scrollable.pack(fill="both", expand=True)

    # 1. 图片轮播区
    image_meta = _load_image_metadata()
    if image_meta:
        _ImageCarousel(scrollable, image_meta).pack(fill="x", padx=8, pady=8)
    else:
        _PlaceholderBlock(
            scrollable, "图片轮播", "红色图片资源待补充"
        ).pack(fill="x", padx=8, pady=8)

    # 2. 文字展示区
    quotes = _load_quotes()
    if quotes:
        _TextViewer(scrollable, quotes).pack(fill="x", padx=8, pady=8)
    else:
        _PlaceholderBlock(
            scrollable, "文字展示", "红色文案资源待补充"
        ).pack(fill="x", padx=8, pady=8)
