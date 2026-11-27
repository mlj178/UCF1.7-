#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""「快捷键」页：游戏内热键速查 —— **2026-11-27 起已停用**。

用户要求删掉「插件开关 → 快捷键」这一页：F2 菜单里本来就有全部键位，单独一页没用。
控制台已经不再 import 这个模块、也不再挂这个页签；文件保留只是为了不在这次改动里
制造一个"删了但没提交"的半截状态，**可以整个删掉**（连同 ui/consts.py 的
HUD_KEYS / HUD_NOTES）。留着它不会影响任何功能。
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
