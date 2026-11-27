#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：守卫点只是"设立点"，区外按 5 不再连带新建守卫区（2026-11-27）。

跑法：python app/tests/test_guard_no_auto_area.py

用户原话：「一次点击在同一个坐标生成了『区 + 点』两个对象 —— 这个是不对的，
修复一下。守卫点只是设立点。」

以前「3 守卫区工具 → 2 加守卫点」在准星不落任何 3 m 区框里时会先 make_area 再
make_nanopos，一次点击在同一坐标冒出两个物体（日志 11:02:53：area #11 + nanopos #13
同坐标 -60.41 -16.59 -7.66），看着就像「加点却多出来一个区」。

只读、不开窗口，查这几件事：
  1) 两条交互路径（笔刷 3 / 菜单 sub3 第 2 项）在区外**早退**，且早退在 ed_step 之前
     —— 不建、不进撤销栈、不点亮「未保存」；
  2) 早退之后没有残留的「先建区再挂点」代码（okArea / make_area + make_nanopos 连招）；
  3) 建区那条路径（第 1 项 / 笔刷 4）照旧；
  4) 预览框在区外变灰（slot 13），和按下去会被拒绝一致；
  5) 菜单文字改成「先按 1 建区，再回来加点」；
  6) make_area / make_nanopos 的调用点数量没多也没少（防止别处又偷偷连带建区）。
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
    wp = section(ed, "static void wp_place(void) {", "/* ---- 测试包")
    case3 = section(wp, "    case 3: {", "    case 4:")
    act = section(ed, "if (g_wpMenuSub == 3) {                 /* 守卫区 */",
                  "if (g_wpMenuSub == 4)")
    tick = section(ed, "static void ghost_tick(void) {", "static int make_jump_link_ex")
    block = section(ed, "if (g_wpMenuSub == 3 && off < (int)sizeof s - 460)",
                    "/* 准星处那个虚线框的坐标")

    print("[0] 段落定位（找不到段落 = 后面的检查全是假的）")
    check(len(wp) > 1000, "找到 wp_place()")
    check("case 3" in case3 and "case 4" not in case3.split("case 3")[0], "切出笔刷 3 那一段")
    check(len(act) > 500, "找到菜单 sub 3 段")
    check(len(tick) > 1000, "找到 ghost_tick()")
    check(len(block) > 200, "找到守卫区工具的菜单说明块")

    print("[1] 区外早退：两次交互都不建东西")
    check("g_wpBrush == 3 && area_at(&p) < 0" in wp,
          "笔刷放守卫点：区外先判 area_at，早退")
    check("if (i == 1 && area_at(&p) < 0)" in act,
          "菜单「2 加守卫点」：区外先判 area_at，早退")
    check(wp.find("g_wpBrush == 3 && area_at(&p) < 0") < wp.find("ed_step()"),
          "笔刷这条早退在 ed_step() 之前（不留空撤销步）")
    check(act.find("if (i == 1 && area_at(&p) < 0)") < act.find("ed_step();"),
          "菜单这条早退在 ed_step() 之前（不留空撤销步）")
    check("editor_dirty_mk" not in wp[:wp.find("ed_step()")],
          "笔刷早退路径不点亮「未保存」")
    check("editor_dirty_mk" not in act[:act.find("ed_step();")],
          "菜单早退路径不点亮「未保存」")

    print("[2] 没有「区 + 点」连招的残留")
    check("make_area" not in case3, "笔刷 3 段里不再调用 make_area")
    check("make_area" not in act.split("else if (i == 1)")[-1].split("} else {")[0],
          "菜单第 2 项分支里不再调用 make_area")
    check("okArea" not in ed, "旧的 okArea（建区失败也接着挂点）已删除")
    check("make_area(30, p); if (g_curArea" not in ed, "旧的「建区 + 立刻挂点」写法已删除")
    check("准星不在任何守卫区：已新建守卫区" not in ed, "旧的 toast 文案已删除")
    check("已新建守卫区 + 一个守卫点" not in ed, "旧的「区 + 点」toast 已删除")

    print("[3] 两条路径的提示一致")
    msg = "这里没有守卫区：先按 1 建区，再在区里加点"
    check(ed.count(msg) == 2, "笔刷 / 菜单都用同一句提示（%d 处）" % ed.count(msg))
    check("不建守卫点；先「1 新建守卫区」" in ed, "日志里写清「不建点，要先建区」")

    print("[4] 建区那条路径照旧")
    check("if (i == 0) { make_area(30, p); }" in act, "菜单「1 新建守卫区」仍然立刻建区")
    check(ed.count("make_area(30, p)") == 2, "只有两处建 3 m 区：菜单第 1 项 + 笔刷 4")
    check("case 4:\n      if (make_area(30, p)) toast_ok" in ed, "笔刷 4（守卫区）仍然立刻建区")

    print("[5] 预览跟着变灰")
    check("if (ok && brush == 3 && area_at(&p) < 0) ok = 0;" in tick,
          "区外守卫点的预览框判为「按下去会被拒绝」")
    check("if (!ok) slot = 13;" in tick, "被拒绝时用灰色槽位")
    check("make_area(" not in tick and "make_nanopos(" not in tick,
          "预览仍然不创建任何东西")

    print("[6] 菜单文字")
    check("按 5 不会建点（守卫点只挂在区里）" in block,
          "第 2 项写明区外按 5 不会建点")
    check("先按 1 建区，再回来加点" in block, "第 2 项写明该怎么办")
    check("按 5 会在该点新建一个区" not in ed, "旧的「会新建一个区」说明已删除")

    print("[7] 调用点数量（防止别处又偷偷连带建区）")
    check(ed.count("make_nanopos(") == 5,
          "make_nanopos：1 处定义 + 读档 / 撤销 / 笔刷 / 菜单 4 处调用（实际 %d）" % ed.count("make_nanopos("))
    check(ed.count("make_area_aid(") == 4,
          "make_area_aid：定义 + make_area + 读档 + 撤销（实际 %d）" % ed.count("make_area_aid("))
    check(ed.count("area_at(") >= 5, "area_at 仍被菜单 / 笔刷 / 预览共用")

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
