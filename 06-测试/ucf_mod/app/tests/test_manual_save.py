#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：游戏内编辑「必须手动保存」的语义（2026-11-25 用户要求）。

跑法：python app/tests/test_manual_save.py

只读，不开窗口。查这几件事：
  1) editor.c 只有一个保存入口 editor_save_all（save_file / nav_save 都只在那里调）
  2) 每次编辑只 mark dirty（editor_dirty_mk / editor_dirty_nav），不再自动落盘
  3) Ctrl+S 是唯一的保存键；Ctrl+6 / Ctrl+Shift+S 的保存已删除
  4) F2 菜单里显示「未保存 / 已保存」，保存项走 editor_save_all
  5) 退出房间 / 退出游戏 / 切包 / 重读都会丢弃未保存编辑并写日志
  6) navfix 把 Ctrl+S 派发给编辑器（菜单开着也能存）
  7) 控制台热键速查同步；录制页必须点「保存增量」才落盘
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记，本文件搬到哪都对

FAIL = []


def check(cond, what):
    if cond:
        print("  OK   " + what)
    else:
        print("  !!   " + what)
        FAIL.append(what)


def read(rel):
    with open(os.path.join(UCF_ROOT, rel), "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def section(src, start, end):
    i = src.find(start)
    j = src.find(end, i + 1)
    return src[i:j] if i >= 0 and j > i else ""


def main():
    ed = read(os.path.join("src", "editor.c"))
    nv = read(os.path.join("src", "navfix.c"))
    consts = read(os.path.join("app", "ui", "consts.py"))
    rec = read(os.path.join("app", "tabs", "record", "tab.py"))
    readme = read("README.md")

    print("[1] 唯一保存入口")
    check("void editor_save_all(void)" in ed, "editor.c 有 editor_save_all")
    check(ed.count("!save_file()") == 1 and "save_file();" not in ed,
          "save_file() 只有一处调用（editor_save_all）")
    save_body = section(ed, "void editor_save_all(void)", "static void nav_edit_load")
    check("!save_file()" in save_body, "save_file() 的调用确实在 editor_save_all 里")
    check("nav_save();" not in ed, "没有别处直接调 nav_save()")
    check("!nav_save()" in save_body, "editor_save_all 会检查 nav_save 的返回值")

    print("[2] 编辑只 mark dirty")
    check(ed.count("editor_dirty_mk();") >= 6, "markers 编辑都走 editor_dirty_mk（>=6 处）")
    check(ed.count("editor_dirty_nav();") >= 4, "点图编辑都走 editor_dirty_nav（>=4 处）")
    push = section(ed, "static void nav_push(int kind", "static void nav_push_dir")
    check("editor_dirty_nav();" in push, "nav_push 只 mark，不写盘")
    check("nav_save" not in push, "nav_push 里没有 nav_save")
    check("记录一条编辑：只改内存" in ed, "nav_push 的注释写清「只改内存」")

    print("[3] Ctrl+S 是唯一保存键")
    check("if (!shift && vk == 'S') { editor_save_all(); return; }" in ed,
          "editor_on_key_mod 里 Ctrl+S -> editor_save_all")
    check("Ctrl+6 保存已取消" in ed, "Ctrl+6 保存已删除（只提示用 Ctrl+S）")
    check("Ctrl+Shift+S 保存已取消" in ed, "Ctrl+Shift+S 保存已删除")
    check("ctrl+6 保存" not in consts.lower(), "热键速查里不再把 Ctrl+6 当保存")
    check("Ctrl+Shift+S 手动保存" not in consts, "热键速查里不再有 Ctrl+Shift+S 手动保存")

    print("[4] F2 菜单")
    check('"保存（Ctrl+S）"' in ed, "菜单项名称写成「保存（Ctrl+S）」")
    check("else if (i == 2) editor_save_all();" in ed, "菜单第 3 项走 editor_save_all")
    check("● 未保存 · Ctrl+S 保存" in ed, "菜单第一行显示未保存状态")
    check("已保存 · Ctrl+S 保存" in ed, "菜单第一行显示已保存状态")

    print("[5] 退出房间 / 切包 / 重读 = 丢弃未保存")
    scene = section(ed, "void editor_on_scene(void* astar)", "void editor_mark_dirty")
    check("退出房间，丢弃未保存的编辑" in scene, "换房间时打日志并丢弃未保存编辑")
    check("g_dirtyNav = 0;" in scene and "g_dirtyMk = 0;" in scene, "换房间时清脏标记")
    quit_body = section(ed, "void editor_on_quit(void)", "static void freecam")
    check("丢弃未保存的游戏内编辑" in quit_body, "退出游戏时打日志说明未保存编辑丢弃")
    pack = section(ed, "static int nav_cmd_set_pack", "static void nav_cmd_tick")
    check("切包 / 重新载入会丢弃未保存的游戏内编辑" in pack, "切包 / 重新载入前提醒")
    check("g_dirtyNav = 0;" in pack and "g_dirtyMk = 0;" in pack, "切包后清脏标记")
    reapply = section(ed, "static void nav_reapply(void)", "static void nav_unlink_here")
    check("重读会丢弃未保存的点图编辑" in reapply, "重读（Ctrl+Shift+R）前提醒")

    print("[6] 键盘派发（navfix）")
    key = section(nv, "if (msg == WM_KEYDOWN)", "if (msg == WM_LBUTTONDOWN")
    check("if (w == 'S' && !shift)" in key, "WM_KEYDOWN 里单独放行 Ctrl+S")
    check("editor_save_all();" in key, "navfix 调 editor_save_all")
    check("else if (!editor_menu_is_open() || shift)" in key, "Ctrl+S 不受「菜单开着」限制")

    print("[7] 录制：必须点了保存才算保存")
    check("保存增量" in rec, "复盘页按钮是「保存增量」")
    check("只预览、还没写进草稿" in rec, "复盘页明确写了「还没保存」")
    finish = section(rec, "def rec_finish(", "def rec_review_from_file(")
    review = section(rec, "def rec_review_from_file(", "def rec_fill_done(")
    check("self.rec_save(" not in finish, "结束录制不会自动保存")
    check("self.rec_save(" not in review, "复盘完成不会自动保存")

    print("[8] 文档")
    check("Ctrl+S 才写文件" in readme, "README 写清「Ctrl+S 才写文件」")
    check("不按 Ctrl+S 就退房间 = 改动全部丢弃" in consts, "控制台速查写清退房间会丢")

    print("\n" + ("FAIL" if FAIL else "OK") + ": 手动保存语义（唯一入口 / 无自动保存 / 退房间丢弃）")
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
