#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：守卫区工具里 1-7 只是「切换选中」，不能一按就建东西（2026-11-26 用户要求）。

跑法：python app/tests/test_menu_select.py

用户原话：「按1切换到新建守卫区，应该是切换过去，而不是直接就设立了守卫区，
应该是先选择，第一步是先选择，那个2也是的……3，4也是」。

查这几件事：
  1) 守卫区工具（sub 3）的数字键只改选中项，不调 menu_activate；
  2) 真正执行仍然走 5 / 左键 / 回车（menu_confirm -> menu_activate）；
  3) 入口 / 逃跑点 / 删除入口 / 删除逃跑点 / 整体移动（3-7）按 5 才生效；
     安全等级在「加守卫点」子页（sub 10）按 1-4 直接切；
  4) 菜单里写明「1-7 / 8/2 只切换选中」；
  5) 其它子页（添加点位 / 建立路径）的数字键行为没被误改。
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)

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

    print("[1] 数字键：sub 3 只选中")
    keys = section(ed, "int editor_menu_key(unsigned vk, int ext) {", "void editor_on_key_plain")
    check("if (g_wpMenuSub == 3 || g_wpMenuSub == 4 || g_wpMenuSub == 6) {" in keys,
          "数字键里先判断是不是「只选中」的那三页")
    pick = section(ed, "if (g_wpMenuSub) {\n      if (i < menu_sub_count()) {",
                   "} else if (i >= 0 && i < WP_MENU_N) {")
    check("menu_refresh();" in pick, "只刷新菜单（高亮变了）")
    check("menu_activate();" in pick, "其它子页分支里仍有 menu_activate（守卫区工具分支不调）")
    check("g_wpMenuSub == 3 || g_wpMenuSub == 4 || g_wpMenuSub == 6" in pick,
          "守卫区工具(3) / 撤销保存(4) / 删除连线·路点(6) 三页都只选中")
    sub3 = section(pick, "if (g_wpMenuSub == 3 ||", "} else {")
    check("menu_activate();" not in sub3, "**不**在这三页分支里调用 menu_activate")
    check("按 5 / 左键 才执行" in pick, "日志写清楚要按 5")
    check(keys.count("menu_activate();") >= 1, "其它子页仍然保留 menu_activate 的老行为")
    main_digits = section(ed, "} else if (i >= 0 && i < WP_MENU_N) {", "return 1;\n  }")
    check("if (i == 6) {" in main_digits, "主菜单第 6 项（落地/贴地）也要先选中")
    check("选中 6（落地 / 贴地）—— 按 5 / 左键 才执行" in main_digits,
          "按 6 只是选中，日志说明按 5 才执行")
    m6 = section(main_digits, "if (i == 6) {", "} else {")
    check("menu_activate();" not in m6, "按 6 不执行 nav_ground_here")

    print("[2] 执行路径没变")
    confirm = section(ed, "static void menu_confirm(void) {", "/* 菜单打开时：菜单键")
    check("menu_activate();" in confirm, "5 / 左键 / 回车 仍然走 menu_activate")
    check("if (g_wpArm)" in confirm, "连续放置（添加点位）仍然直接放")

    print("[3] 加守卫点子页：1-4 换等级，5 放点")
    act = section(ed, "if (g_wpMenuSub == 3) {                 /* 守卫区 */", "if (g_wpMenuSub == 4)")
    sub = section(ed, "static int guard_add_place(void) {", "/* 菜单确认")
    keys = section(ed, "int editor_menu_key(unsigned vk, int ext) {", "void editor_on_key_plain")
    confirm = section(ed, "static void menu_confirm(void) {", "/* 菜单打开时：菜单键")
    check("if (i == 1)" in act and "g_wpMenuSub = 10" in act, "守卫区第 2 项进入加点子页")
    check("if (i == 2)" in act and "make_entrance" in act, "入口按 5 才落盘")
    check("if (i == 3)" in act and "make_escape" in act, "逃跑点按 5 才落盘")
    check("area_at(&p)" in sub and "make_nanopos(g_mk[ai].aid, p, g_nanoSafety" in sub,
          "子页放点按准星归区、用当前安全等级")
    check("ed_step();" in sub and "mke_note_add(n0);" in sub, "放点仍进撤销栈")
    check("g_wpMenuSub == 10 && vk >= '1' && vk <= '5'" in keys, "子页数字键 1-4 直接换、5 放")
    check("g_nanoSafety = gi" in keys, "1-4 立即设置 g_nanoSafety")
    check("if (g_wpMenuSub == 10)" in confirm and "guard_add_place();" in confirm,
          "回车 / 小键盘 5 / 左键在子页也直接放点")

    print("[4] 菜单提示")
    block = section(ed, "if (g_wpMenuSub == 3 && off < (int)sizeof s - 460)", "/* 准星处那个虚线框的坐标")
    check("1-7 / 8/2 只切换选中 · 5 / 左键 / 回车 才真正执行" in block,
          "守卫区工具底部写明「先选后执行」")
    check("1-%d / 8/2 只切换选中 · 5 / 左键 / 回车 才执行" in ed,
          "撤销保存页 / 删除连线路点页也写明「先选后执行」")
    check("落地 / 贴地：按 6 只是选中，按 5 / 左键 才执行" in ed,
          "主菜单停在 6 时提示「按 6 只是选中」")

    print("[5] 选中项高亮（黄色）")
    check('#define MENU_HI_ON  "<color=#FFD24A>"' in ed, "定义高亮起始标签（金色 #FFD24A）")
    check('#define MENU_HI_OFF "</color>"' in ed, "定义高亮结束标签")
    main_loop = section(ed, "if (g_wpMenuSub == 0) {", "} else {")
    sub_loop = section(ed, "    n = menu_sub_count();", "  }\n  if (g_wpMenuSub == 4")
    check("on ? MENU_HI_ON : \"\"" in main_loop and "on ? MENU_HI_OFF : \"\"" in main_loop,
          "主菜单：选中行套上颜色标签")
    check("on ? MENU_HI_ON : \"\"" in sub_loop and "on ? MENU_HI_OFF : \"\"" in sub_loop,
          "子菜单：选中行套上颜色标签")
    check("int on = (i == g_wpMenuSel);" in main_loop, "主菜单按 g_wpMenuSel 判定选中")
    check("int on = (i == g_wpMenuSubSel);" in sub_loop, "子菜单按 g_wpMenuSubSel 判定选中")

    print("")
    if FAIL:
        print("失败 %d 项：" % len(FAIL))
        for f in FAIL:
            print("  - " + f)
        return 1
    print("全部通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
