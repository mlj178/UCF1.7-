#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：路点菜单「守卫区工具」里的新建守卫区 / 加守卫点要有落点预览（2026-11-26）。

跑法：python app/tests/test_guard_preview.py

用户原话：这两项没有预设，希望先画个虚线框，告诉人「如果你选的话会落在这个位置」。
只读、不开窗口。查这几件事：
  1) 预览只由「守卫区工具」的选中行触发（第 1/2 项），不靠 g_wpArm；
  2) 预览用的笔刷 = 真会创建的东西（第 1 项守卫区 4、第 2 项守卫点 3），
     颜色也走同一套调色板（守卫点绿、守卫区蓝）；
  3) 预览只画框，不创建、不进撤销栈（ghost_tick 里没有 make_* / mke_note_add）；
  4) 预览位置和创建位置一致：+0.05 抬高；守卫区 3 m 立方体按 BoxCollider 中心摆；
  5) 按 5 的行为不变（还是立刻建），没有偷偷改成「先选中再放置」；
  6) 菜单里写清这一项会建什么、挂到哪个区；准星打不到地面时也说明；
  7) 挪到「入口 / 逃跑点」或关菜单，虚线框要收起来。
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记

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

    print("[1] 预览的触发条件")
    guard = section(ed, "static int wp_guard_preview(void) {", "\n}\n")
    check("g_wpMenuSub == 3" in guard, "只看「守卫区工具」这一页（sub 3）")
    check("(g_wpMenuSubSel == 0 || g_wpMenuSubSel == 1)" in guard,
          "只预览前两项（新建守卫区 / 加守卫点）")
    tick = section(ed, "static void ghost_tick(void) {", "static int make_jump_link_ex")
    check("!wp_guard_preview()" in tick, "ghost_tick 的开关里带上预览条件")
    check("!g_wpMenuOpen" in tick, "菜单关掉就不画")
    # 2026-11-26：采集模式（collect_only）删了，预览只看菜单/笔刷状态
    check("g_collectOnly" not in tick, "采集模式已删除，预览不再看它")

    print("[2] 预览画的就是真会建的东西")
    check("brush = preview ? (g_wpMenuSubSel == 0 ? 4 : 3)" in tick,
          "第 1 项 = 守卫区(4)，第 2 项 = 守卫点(3)")
    slot = section(ed, "static int ghost_slot(int brush) {", "static int ghost_mesh_key")
    check("case 3: return 2;" in slot, "守卫点预览 = 槽位 2（绿，和实体的 Bot_NanoGuardPos 同色）")
    check("case 4: return 3;" in slot, "守卫区预览 = 槽位 3（蓝，和 Bot_NanoGuardArea 同色）")
    size = section(ed, "static float ghost_size(int brush) {", "/* 预置框用什么颜色槽")
    check("case 3: return 0.66f;" in size, "守卫点框 0.66 m（标记半径 0.32）")
    check("case 4: return 3.00f;" in size, "守卫区框 3.00 m（游戏里就是 3 m BoxCollider）")

    print("[3] 预览不创建、不进撤销栈")
    for bad in ("make_area(", "make_nanopos(", "mke_note_add(", "editor_dirty_mk("):
        check(bad not in tick, "ghost_tick 里不调用 " + bad)
    act = section(ed, "if (g_wpMenuSub == 3) {                 /* 守卫区 */", "if (g_wpMenuSub == 4)")
    check("make_area(30, p);" in act, "按 5 仍然立刻建守卫区（行为没变）")
    check("make_nanopos(" in act, "按 5 仍然立刻建守卫点")
    check("g_wpArm" not in act, "没有偷偷改成「先选中再放置」（不碰 g_wpArm）")
    check("mke_note_add(n0);" in act, "创建仍进撤销栈（预览不进）")

    print("[4] 预览位置 = 创建位置")
    check("if (preview) p.y += 0.05f;" in tick, "预览也 +0.05（和创建时的落点修正一致）")
    check("p.y += 0.05f;" in act, "menu_activate 里创建前同样 +0.05")
    check("if (preview && brush == 4) q.y -= ghost_size(4) * 0.5f;" in tick,
          "守卫区按 BoxCollider 中心摆框（3 m 立方体上下各 1.5 m）")
    area = section(ed, "static int make_area_aid(int scale10", "static int make_area(int scale10")
    check("R_SET_SCALE" in area and "offset" not in area.lower() and "m_Center" not in area,
          "make_area_aid 只改 scale、不改碰撞体 offset（所以预览按中心摆才对）")

    print("[5] 菜单文字")
    title = section(ed, "static void menu_sub_title(char* out, int cap) {", "static int menu_sub_count")
    check("守卫区工具（虚线框 = 预置落点）" in title, "标题直接写清楚虚线框是预置落点")
    block = section(ed, "if (g_wpMenuSub == 3 && off < (int)sizeof s - 460)", "/* 准星处那个虚线框的坐标")
    check("3.0 m 见方" in block, "第 1 项说明守卫区尺寸")
    check("BoxCollider 中心在准星落点" in block, "第 1 项说明中心落在准星")
    check("蓝色框" in block, "第 1 项说明颜色")
    check("准星在守卫区 #%d（aid=%d）里：按 5 就挂进这个区" in block,
          "第 2 项说明会挂进准星所在的那个区")
    check("准星不在任何守卫区里" in block, "不在任何区里时说明会新建一个区")
    check("area_at" in block, "用的是按落点归区（area_at），不是「当前区」")
    check("入口 / 逃跑点还没接" in block, "第 3/4 项说明还没接（别让人等虚线）")
    check("准星没打到地面" in block, "打不到地面时说明虚线为何不显示")
    check("g_wpMenuSubSel <= 1 && !g_ghostPvOk" in block,
          "只有前两项才提示「没打到地面」（第 3/4 项本来就没框）")
    tip = section(ed, "int prev = (g_ghostPrev && wp_guard_preview());", "/* 上一手到底做了什么")
    check("仅预览 · 按 5 创建" in tip, "坐标行标注「仅预览 · 按 5 创建」")
    check("g_ghostPrev ?" not in tip, "坐标行用现算的 prev，不用上一帧的 g_ghostPrev")

    print("[6] 状态复位 / 切走就收起")
    reset = section(ed, "static void ghost_reset(void) {", "static void ghost_hide(void) {")
    hide = section(ed, "static void ghost_hide(void) {", "/* 每帧（主线程）")
    check(reset.count("g_ghostPrev = 0;") == 1, "换图 ghost_reset 清掉预览标记")
    check(hide.count("g_ghostPrev = 0;") == 1, "ghost_hide 清掉预览标记")
    check("g_ghostPrev = preview;" in tick, "ghost_tick 每帧写回预览标记")
    check(ed.count("g_ghostPrev = 0;") == 2, "只有这两处清零（没有第三处乱清）")

    print("[7] 日志")
    check("选中项在准星处画虚线预置框" in ed, "进「守卫区工具」时写一行日志（便于对日志核验）")
    check("#define MT_AREA    3" in ed, "菜单文字用的 MT_AREA 就是 g_mk 里的 3（和创建路径一致）")

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
