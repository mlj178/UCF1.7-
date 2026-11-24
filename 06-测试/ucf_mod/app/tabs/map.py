#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""「地图」页：房间选图列表里的隐藏图。

2026-11-24 目录重构：从 app/控制台.pyw 拆出，方法体原样搬，只换文件位置。
"""


import customtkinter as ctk

from ui.consts import FONT_S


class MapTab:
    def build_group_tab(self, tab, hint, items):
        r"""页内再套一层滚动区：窗口压矮时开关仍然够得着。"""
        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(body, text=hint, font=FONT_S, text_color="#9aa0a6",
                     anchor="w", justify="left", wraplength=620).pack(
            fill="x", padx=12, pady=(8, 2))
        for key, label, desc, default in items:
            self.switch_card(body, key, label, desc, default)
