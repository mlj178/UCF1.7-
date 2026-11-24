#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""「快捷键」页：游戏内热键速查。

2026-11-24 目录重构：从 app/控制台.pyw 拆出，方法体原样搬，只换文件位置。
"""


import customtkinter as ctk

from ui.consts import FONT_S, HUD_KEYS, HUD_NOTES


class HotkeyTab:
    def build_hotkey_tab(self, tab, hint):
        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(body, text=hint, font=FONT_S, text_color="#9aa0a6",
                     anchor="w", justify="left", wraplength=620).pack(
            fill="x", padx=12, pady=(8, 2))
        self.text_card(body, "游戏内热键", HUD_KEYS, 330)
        ctk.CTkLabel(body, text=HUD_NOTES, font=FONT_S, text_color="#9aa0a6",
                     anchor="w", justify="left", wraplength=620).pack(
            fill="x", padx=14, pady=(10, 12))
