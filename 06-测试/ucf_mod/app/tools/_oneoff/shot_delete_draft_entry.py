#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""一次性：给「删除本图草稿」入口拍真实截图（不删任何数据）。

做什么：起控制台 -> 跳到「路点数据 -> 人机路点 -> 编辑中 -> 本图草稿」-> 截入口；
        再真弹一次「删除本图草稿」确认框 -> 截弹窗 -> 自动按「取消」，草稿原样留着；
        最后换一张没草稿的图，截「删除」置灰的样子。
跑法：python app/tools/_oneoff/shot_delete_draft_entry.py
产物：docs/design/删除草稿_demo/*.png
"""
import ctypes
import importlib.util
import os
import sys
import time

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)      # 物理像素：截图和窗口坐标一致
except Exception:                                       # noqa: BLE001
    pass

APP = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = os.path.dirname(APP)
OUT = os.path.join(ROOT, "docs", "design", "删除草稿_demo")
sys.path.insert(0, APP)

import customtkinter as ctk                              # noqa: E402
from PIL import ImageGrab                                # noqa: E402

from ui.maps import map_folder                           # noqa: E402
from ui.packs import pack_dir                            # noqa: E402


def load_console():
    spec = importlib.util.spec_from_file_location("ucf_console", os.path.join(APP, "控制台.pyw"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["ucf_console"] = mod
    spec.loader.exec_module(mod)
    return mod


def grab(bbox, name):
    img = ImageGrab.grab(bbox=bbox, all_screens=True)
    path = os.path.join(OUT, name)
    img.save(path)
    print("saved %s %s" % (path, img.size))
    return img


def entry_bbox(app):
    r"""本图草稿卡片：标题 + 按钮那一行 + 本图标记那一行（不含下面的长说明 / 日志）。"""
    card = app.card_pick
    row = app.btn_delete_draft.master
    x0 = max(card.winfo_rootx() - 6, app.winfo_rootx())
    y0 = max(card.winfo_rooty() - 6, app.winfo_rooty())
    x1 = min(card.winfo_rootx() + card.winfo_width() + 6,
             app.winfo_rootx() + app.winfo_width())
    y1 = max(row.winfo_rooty() + row.winfo_height(),
             app.btn_clear_markers.winfo_rooty() + app.btn_clear_markers.winfo_height()) + 14
    return (x0, y0, x1, y1)


def settle(app, times=1):
    for _ in range(times):
        app.update()
        time.sleep(0.1)


def main():
    os.makedirs(OUT, exist_ok=True)
    console = load_console()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = console.App(role="dev")
    app.attributes("-topmost", True)
    app.update()
    # 只为截图：游戏开着时不弹「还在跑」的确认；run_navdata 也是空壳，绝不会写盘
    app._guard_game = lambda title: True
    app.jump_to_pick()
    settle(app)
    if not app.draft_exists():
        for disp, (lv, _lab, fp) in app.map_disp.items():
            if os.path.isdir(pack_dir(map_folder(lv, fp))):
                app.opt_map.set(disp)
                app.on_pack_change(persist=False)
                app.jump_to_pick()
                break
    app.lift()
    settle(app, 22)                      # 等 jump_to_pick 的橙色高亮自己淡掉（1.6 s）
    print("map:", app.opt_map.get(), "draft:", app.draft_exists())

    x, y = app.winfo_rootx(), app.winfo_rooty()
    grab((x, y, x + app.winfo_width(), y + app.winfo_height()), "01_整窗_编辑中.png")
    grab(entry_bbox(app), "02_本图草稿_删除入口.png")

    # 危险确认框：真显示、真截图，然后直接销毁 Toplevel
    # （不点红色按钮 -> confirm_danger 返回 False -> 不会删任何东西）
    state = {"shot": False}

    def shoot_dialog():
        tops = [w for w in app.winfo_children() if isinstance(w, ctk.CTkToplevel)]
        if not tops:
            app.after(250, shoot_dialog)
            return
        top = tops[-1]
        top.update_idletasks()
        x0, y0 = top.winfo_rootx(), top.winfo_rooty()
        grab((x0, y0, x0 + top.winfo_width(), y0 + top.winfo_height()),
             "03_删除确认弹窗.png")
        state["shot"] = True
        try:
            top.destroy()            # 直接销毁 = 取消
        except Exception:
            pass

    # 双保险：截图脚本绝不删任何东西 ——
    #   1) 弹窗真实渲染但**固定返回 False**（不管标题栏关闭 / 默认按钮怎么落）；
    #   2) run_navdata 换成空壳，哪怕前面判成「是」也不会起 navdata.py。
    def no_navdata(args, title):
        print("[shot] 跳过写盘命令：navdata.py %s" % " ".join(args))

    real_run = app.run_navdata
    app.run_navdata = no_navdata

    app.after(900, shoot_dialog)
    try:
        app.delete_draft()           # 等弹窗被销毁后返回 False
    finally:
        app.run_navdata = real_run
    print("dialog screenshot:", state["shot"], "draft still there:", app.draft_exists())
    settle(app)

    # 再换一张没有草稿的图：同一个入口应该置灰
    for disp, (lv, _lab, fp) in app.map_disp.items():
        if not os.path.isdir(pack_dir(map_folder(lv, fp))):
            app.opt_map.set(disp)
            app.on_pack_change(persist=False)
            app.opt_map.set(app.opt_map.get())
            settle(app, 3)
            print("empty-map state:", app.opt_map.get(), "draft:", app.draft_exists(),
                  "btn:", app.btn_delete_draft.cget("state"))
            grab(entry_bbox(app), "04_无草稿_按钮置灰.png")
            break

    app.update()
    app.destroy()
    sys.stdout.flush()   # os._exit 不刷缓冲区：先冲掉再强退
    os._exit(0)          # 控制台可能留着后台线程，别让脚本卡住


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:                                    # noqa: BLE001
        import traceback
        traceback.print_exc()
        os._exit(1)
