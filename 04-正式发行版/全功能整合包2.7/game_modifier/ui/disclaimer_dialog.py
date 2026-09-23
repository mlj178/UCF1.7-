# -*- coding: utf-8 -*-
"""首次启动免责声明弹窗

首次运行主程序时弹出一次，用户点击「我已知晓并继续」后，在数据目录写入已读标记，
之后不再弹出；点击「不同意，退出」或直接关闭窗口则退出主程序。

数据目录见 core/config.DATA_DIR（打包后为 %LOCALAPPDATA%\\UCFModifier）。
声明正文与「设置 - 免责声明」页保持一致。
"""

import json
import os

import customtkinter as ctk

from core.config import DATA_DIR

ACK_FILE = os.path.join(DATA_DIR, "disclaimer_ack.json")

_DIALOG_TEXT = (
    "1.本工具为免费开源的第三方非官方修改器，仅供个人学习与单机娱乐使用。\n"
    "2.使用可能导致游戏崩溃；请勿用于破坏他人游戏体验或任何违反当地法律法规的行为。\n"
    "3.本程序按「现状」提供，不提供任何担保，作者不承担因使用产生的责任。\n"
    "4.点击「我已知晓并继续」即视为你已阅读并同意完整条款（设置 - 免责声明）。"
)


def is_acknowledged():
    try:
        with open(ACK_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return False
    return isinstance(data, dict) and bool(data.get("acknowledged"))


def mark_acknowledged():
    """写入已读标记；写失败不阻断使用，仅导致下次启动再次弹出。"""
    try:
        with open(ACK_FILE, "w", encoding="utf-8") as f:
            json.dump({"acknowledged": True}, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


class DisclaimerDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("免责声明")
        self.geometry("430x320")
        self.resizable(False, False)
        self.attributes('-topmost', True)
        self.transient(parent)
        self.grab_set()

        self._parent = parent

        ctk.CTkLabel(self, text="使用前请阅读",
                     font=("Microsoft YaHei", 15, "bold"),
                     text_color="#ffcc00").pack(pady=(18, 8))

        ctk.CTkLabel(self, text=_DIALOG_TEXT,
                     font=("Microsoft YaHei", 12),
                     justify="left", anchor="w", wraplength=380).pack(
            fill="x", padx=20, pady=(0, 18))

        action = ctk.CTkFrame(self, fg_color="transparent")
        action.pack(pady=(0, 16))
        ctk.CTkButton(action, text="我已知晓并继续", font=("Microsoft YaHei", 12),
                      width=140, command=self._on_accept).pack(side="left", padx=6)
        ctk.CTkButton(action, text="不同意，退出", font=("Microsoft YaHei", 12),
                      width=120, fg_color="#7a2a2a", hover_color="#9a3a3a",
                      command=self._on_decline).pack(side="left", padx=6)

        # 点右上角关闭等同「不同意」
        self.protocol("WM_DELETE_WINDOW", self._on_decline)

    def _on_accept(self):
        mark_acknowledged()
        self.destroy()

    def _on_decline(self):
        self.destroy()
        close = getattr(self._parent, "_on_close", None)
        if callable(close):
            close()
        else:
            self._parent.destroy()


def show_if_needed(parent):
    """首次运行时弹出声明弹窗；已读则返回 None。"""
    if is_acknowledged():
        return None
    return DisclaimerDialog(parent)