#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""身份（用户 / 开发者）——谁能看到哪些页。

2026-11-24 用户要求：别人拿到这份东西，自己选当用户还是开发者。

    user  用户      只有 地图 / 部署 两页（装好就能玩）
    dev   开发者    全部 11 页（含用户那两页，不用切身份）

存哪：ucf_mod.json 的 ui.role；UCF_ROLE 环境变量优先（脚本 / 快捷方式用）。
"""

import os

import customtkinter as ctk

from ui.consts import FONT, FONT_B, FONT_S, USER_PAGES  # noqa: F401  USER_PAGES 给调用方用
from ui.util import load_cfg, save_cfg

ROLE_USER = "user"
ROLE_DEV = "dev"
ROLE_LABEL = {ROLE_USER: "用户", ROLE_DEV: "开发者"}
ROLE_ALIAS = {
    "user": ROLE_USER, "player": ROLE_USER, "用户": ROLE_USER, "玩家": ROLE_USER, "1": ROLE_USER,
    "dev": ROLE_DEV, "developer": ROLE_DEV, "开发者": ROLE_DEV, "2": ROLE_DEV,
}


def normalize_role(value):
    r"""把配置 / 环境变量 / 参数里的身份写法统一成 user / dev；认不出返回空串。"""
    return ROLE_ALIAS.get(str(value or "").strip().lower(), "")


def env_role():
    return normalize_role(os.environ.get("UCF_ROLE"))


def role_from_cfg():
    cfg = load_cfg()
    ui = cfg.get("ui") if isinstance(cfg.get("ui"), dict) else {}
    return normalize_role(ui.get("role"))


def save_role(role):
    role = normalize_role(role)
    if not role:
        return
    cfg = load_cfg()
    ui = cfg.get("ui")
    if not isinstance(ui, dict):
        ui = {}
        cfg["ui"] = ui
    ui["role"] = role
    save_cfg(cfg)


def ask_role(default=ROLE_USER):
    r"""首次启动的身份选择窗。返回 user / dev；直接关窗口按 default 走。"""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title("UCF 控制台 · 选择身份")
    root.geometry("620x356")
    root.resizable(False, False)
    root.configure(fg_color="#242424")
    try:
        root.attributes("-topmost", True)
    except Exception:            # noqa: BLE001  某些窗口管理器不认
        pass

    pick = {"value": normalize_role(default) or ROLE_USER}

    ctk.CTkLabel(root, text="这台电脑怎么用这个控制台？", font=FONT_B).pack(
        anchor="w", padx=24, pady=(22, 2))
    ctk.CTkLabel(root, text="选错了也不要紧——右上角「切换身份」随时能改（会重启一下控制台）。",
                 font=FONT_S, text_color="#9aa0a6").pack(anchor="w", padx=24, pady=(0, 14))

    wrap = ctk.CTkFrame(root, fg_color="transparent")
    wrap.pack(fill="x", padx=24)
    cards = {}

    def style(role):
        on = pick["value"] == role
        card = cards[role]
        card.configure(border_color="#2f6fdb" if on else "#3d4046",
                       fg_color="#2b3854" if on else "#2e2e2e")

    def choose(role):
        pick["value"] = role
        for r in cards:
            style(r)

    def make(role, title, lead, bullets, width):
        card = ctk.CTkFrame(wrap, width=width, height=168, corner_radius=11,
                            border_width=2, border_color="#3d4046", fg_color="#2e2e2e")
        card.pack(side="left", padx=(0, 12))
        card.pack_propagate(False)
        name = ctk.CTkLabel(card, text=title, font=("Microsoft YaHei UI", 15, "bold"), anchor="w")
        name.pack(anchor="w", padx=16, pady=(14, 2))
        desc = ctk.CTkLabel(card, text=lead, font=FONT_S, text_color="#9aa0a6",
                            anchor="w", justify="left", wraplength=width - 34)
        desc.pack(anchor="w", padx=16)
        body = ctk.CTkLabel(card, text=bullets, font=FONT_S, text_color="#b9c2cc",
                            anchor="w", justify="left", wraplength=width - 34)
        body.pack(anchor="w", padx=16, pady=(8, 0))
        for w in (card, name, desc, body):
            w.bind("<Button-1>", lambda _e, r=role: choose(r))
        cards[role] = card
        return card

    make(ROLE_USER, "用户", "装好就能玩，界面只有两页。",
         "· 地图：多加一张暴风图\n· 部署：装进游戏 / 修复 / 卸载\n· 开始游戏一键启动", 268)
    make(ROLE_DEV, "开发者", "做路点、调地图、跑车测，全部 11 页。",
         "· 可视化 / 导出 / 快捷键\n· 人机路点 / 录制 / 数据\n· 部署 / 车测 / 开发者选项", 268)
    for r in cards:
        style(r)

    foot = ctk.CTkFrame(root, fg_color="transparent")
    foot.pack(fill="x", padx=24, pady=(16, 0))
    ctk.CTkLabel(foot, text="", font=FONT_S).pack(side="left")
    ctk.CTkButton(foot, text="就用这个身份", width=132, height=34, font=FONT,
                  fg_color="#2f6fdb", hover_color="#255bb4",
                  command=root.destroy).pack(side="right")
    ctk.CTkButton(foot, text="以后再说（默认用户）", width=150, height=34, font=FONT_S,
                  fg_color="transparent", border_width=1, border_color="#4a4a4a",
                  hover_color="#2e2e2e",
                  command=lambda: (pick.update({"value": ROLE_USER}), root.destroy())
                  ).pack(side="right", padx=(0, 10))

    root.protocol("WM_DELETE_WINDOW", lambda: (pick.update({"value": normalize_role(default) or ROLE_USER}),
                                               root.destroy()))
    root.update_idletasks()
    w, h = 620, 356
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 3
    root.geometry("%dx%d+%d+%d" % (w, h, x, y))
    root.mainloop()
    return pick["value"]
