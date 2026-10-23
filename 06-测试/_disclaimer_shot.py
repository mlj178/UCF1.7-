# -*- coding: utf-8 -*-
"""离屏验证：免责声明弹窗 5 秒读秒门禁 + 截图证据。仅用于测试，不随包发布。"""
import ctypes
import sys
import time
import json
from pathlib import Path

PKG = r"D:\trae_project\ucf1.7-modifier\04-正式发行版\全功能整合包2.7\game_modifier"
OUT = Path(r"D:\trae_project\ucf1.7-modifier\06-测试")
sys.path.insert(0, PKG)
os_ok = True

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

import customtkinter as ctk
from PIL import Image, ImageGrab
import ui.disclaimer_dialog as dd

calls = []
dd.mark_acknowledged = lambda: calls.append("ack")

root = ctk.CTk()
root.geometry("360x200+60+60")
root.title("主程序（占位）")
root.update()

dlg = dd.DisclaimerDialog(root)
dlg.deiconify()
dlg.lift()
dlg.attributes("-topmost", True)


def pump(seconds):
    end = time.time() + seconds
    while time.time() < end:
        root.update()
        time.sleep(0.02)


def shot(name):
    root.update()
    x, y = dlg.winfo_rootx(), dlg.winfo_rooty()
    w, h = dlg.winfo_width(), dlg.winfo_height()
    # 预留边距，避免窗口边框/阴影导致左侧被裁掉
    img = ImageGrab.grab(bbox=(x - 14, y - 34, x + w + 14, y + h + 14))
    img.save(OUT / name)
    return img


result = {}

pump(1.2)
result["t1.2_state"] = dlg._accept_button.cget("state")
result["t1.2_text"] = dlg._accept_button.cget("text")
img_locked = shot("免责声明-读秒中.png")

# 读秒未结束时强行触发接受，应当被拒绝（弹窗仍在、未写标记）
dlg._on_accept()
root.update()
result["blocked_still_open"] = bool(dlg.winfo_exists())
result["blocked_no_ack"] = (calls == [])

pump(5.0)  # 累计约 6.2s
result["t6.2_state"] = dlg._accept_button.cget("state")
result["t6.2_text"] = dlg._accept_button.cget("text")
img_ready = shot("免责声明-可点击.png")

# 解锁后点击应当写标记并关闭
dlg._on_accept()
pump(0.3)
result["after_accept_ack_calls"] = len(calls)
result["after_accept_closed"] = not bool(root.winfo_exists() and dlg.winfo_exists())

# 拼一张对照图
w = img_locked.width + img_ready.width + 30
h = max(img_locked.height, img_ready.height) + 40
canvas = Image.new("RGB", (w, h), (24, 24, 24))
canvas.paste(img_locked, (10, 30))
canvas.paste(img_ready, (img_locked.width + 20, 30))
canvas.save(OUT / "免责声明-阅读倒计时.png")

try:
    root.destroy()
except Exception:
    pass

print(json.dumps(result, ensure_ascii=False, indent=2))
