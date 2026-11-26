#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：路点菜单选点 / 预览必须以「准星」为准（2026-11-26）。

跑法：python app/tests/test_xhair_pick.py

用户原话：「连接路径，选取路点的时候，预选的时候，起始路点，终点，并不是根据屏幕
中心的准星来的，是有偏差的，我的意思是我的准星和路点之间有偏差才能选上……
我希望是以准星的位置为选择的。」

旧实现：cam_point() 沿 transform.forward 打一条射线，取第一个撞到的碰撞体当落点，
再找「落点 3 m 内最近的」可走路点。方块不在那层表面上就选不中。
现在：屏幕中心射线（Camera.ScreenPointToRay）+ 点到射线的垂直距离。

查这几件事：
  1) 屏幕中心射线真的走 ScreenPointToRay（地址 / 签名 / Mono 眼 / 退化长度兜底）；
  2) 选点判据是「到射线的垂直距离」，不再是「落点 3 m 内」，且不看落点；
  3) 选 A / 选 B / 删点 / 断边 / 贴地 / 跳点两端 全部换成新选点器；
  4) 虚线框预览和按键用同一个选点器（预览不能骗人）；
  5) 菜单文案不再写「3 m 内」；日志写清「偏了多少 / 和 forward 差多少度」；
  6) 数学样例：同样的几何下旧判据漏、新判据中；偏开 1.5 m 时新判据不误抓；
  7) 别把变量叫 near（windef.h 里是宏，gcc 会报 expected identifier）。
"""
import math
import os
import re

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
    if i < 0:
        return ""
    j = src.find(end, i + 1)
    return src[i:j] if j > i else src[i:]


def main():
    ed = read(os.path.join("src", "editor.c"))

    print("[1] 屏幕中心射线（Camera.ScreenPointToRay）")
    check("#define R_SPR_INJ     0x327AD0" in ed, "地址：ScreenPointToRay_Injected = 0x327AD0（IDA 0x10327AD0 核对过）")
    check("#define R_SCREEN_W    0x3E6820" in ed, "地址：Screen.get_width = 0x3E6820")
    check("#define R_SCREEN_H    0x3E6800" in ed, "地址：Screen.get_height = 0x3E6800")
    check("typedef struct { V3 o, d; } RAY;" in ed, "Ray 按 24 字节结构体 + out 指针（不按结构体返回值调）")
    check("typedef void (*spr_t)(P, V2*, int, RAY*, void*);" in ed, "spr_t 签名：(this, Vector2* pos, eye, Ray* ret, MethodInfo*)")
    xray = section(ed, "static int cam_xray(V3* o, V3* d) {", "\n}\n")
    check(xray.count("R_SPR_INJ") == 1, "cam_xray 调 ScreenPointToRay_Injected")
    check("R_SCREEN_W" in xray and "R_SCREEN_H" in xray, "屏幕尺寸取 Screen.get_width/height")
    check("2 /* MonoOrStereoscopicEye.Mono */" in xray, "eye = Mono(2)，不是左右眼")
    check("len > 0.5f && len < 1.5f" in xray, "方向长度校验（防 ABI/空相机拿到垃圾）")
    check("ray.d.x == ray.d.x" in xray, "NaN 兜底")
    check("cam_ray(o, d)" in xray, "取不到就退回「相机位置 + forward」，不会把菜单搞死")
    check("acos((double)dot)" in xray and "g_xrAng" in xray, "记录「屏幕中心射线 vs forward」夹角（诊断）")

    print("[2] 落点也用同一条准星射线")
    cpr = section(ed, "static int cam_point_ray(V3* out, V3* ro, V3* rd) {", "\n}\n")
    check("cam_xray(&pos, &fw)" in cpr, "cam_point_ray 走 cam_xray")
    check("R_TDIR_INJ" not in cpr and "R_GET_POS_INJ" not in cpr, "不再自己取 transform.forward")
    check("if (ro) *ro = pos;" in cpr and "if (rd) *rd = fw;" in cpr, "把准星射线带出去给选点用")
    check("static int cam_point(V3* out) { return cam_point_ray(out, 0, 0); }" in ed,
          "cam_point 变成薄包装（放置类功能行为不变）")

    print("[3] 选点判据 = 到准星射线的垂直距离")
    pick = section(ed, "static int nav_pick_ray(P g, const V3* o, const V3* d,", "\n}\n")
    check(pick != "", "nav_pick_ray 存在")
    check("t < 0.25f" in pick, "跳过相机背后 / 贴脸的点")
    # 打印走 GBK 控制台：别用 ² 之类的字符，否则自检自己会 UnicodeEncodeError
    check("v.x * v.x + v.y * v.y + v.z * v.z - t * t" in pick, "垂直距离^2 = |v|^2 - t^2（不借助落点）")
    check("sqrtf(perp)" in pick, "开方")
    check("0.45f + 0.02f * t" in pick, "容差 = 0.45 m + 2% 距离（≈ 3 个方块半径）")
    check("if (tol > 3.0f) tol = 3.0f;" in pick, "容差上限 3 m")
    check("nav_walk(nd)" in pick, "只选可走点（删掉的死点不参与）")
    check("nav_find(" not in pick, "不再退回「离落点 N 米内最近」")
    check("cam_point" not in pick, "选点本身完全不需要落点")
    check("nav_pick(" not in ed, "老的 nav_pick(hint,maxd) 包装已删除")

    print("[4] 所有选点入口都换了")
    # 2026-11-26 晚：nav_pick_menu 多了第二个参数（失败时屏幕提示的文案），
    # 这里只比对函数名 + who 前缀，别再钉死右括号。
    for fn, key in [("static void nav_sel_a(void) {", "nav_pick_menu(\"naved: A\""),
                    ("static void nav_del_here(void) {", "nav_pick_menu(\"naved: 删点\""),
                    ("static void nav_unlink_here(void) {", "nav_pick_menu(\"wpmenu: 断边\""),
                    ("static void nav_link_one(void) {", "nav_pick_menu(\"wpmenu: 连边 B\"")]:
        body = section(ed, fn, "\n}\n")
        check(key in body, fn.split("(")[0].split()[-1] + " 用 nav_pick_menu")
        check("nav_find(g, &p, 3.0f)" not in body, fn.split("(")[0].split()[-1] + " 不再用 3 m 落点判据")
    ground = section(ed, "static void nav_ground_here(void) {", "\n}\n")
    check("cam_point_ray(&q, &ro, &rd)" in ground, "贴地：仍要落点（取地面高度）")
    check("nav_pick_ray(g, &ro, &rd, &nr, &perp)" in ground, "贴地：贴哪颗点用准星射线")
    jump = section(ed, "static void wp_place(void) {", "\n}\n")
    check(jump.count("nav_pick_ray(g, &ro, &rd, 0, 0)") == 2, "跳点起点 + 落点都用准星射线")
    check("准星 3 m 内没有路点" not in ed, "旧的「准星 3 m 内没有路点」提示已删")
    check("nav_find(g, &p, 3.0f)" not in ed, "全文件不再有「落点 3 m」选点")
    check("nav_find(g, &p, 2.5f)" not in ed, "全文件不再有「落点 2.5 m」选点")
    check("nav_find(g, &g_nedA, 0.6f)" in ed, "A 的定位（按坐标找槽位）没动，那本来就该按坐标")

    print("[5] 预览 == 按键")
    ghost = section(ed, "static void ghost_tick(void) {", "static int make_jump_link_ex")
    check(ghost.count("nav_pick_ray(g, &ro, &rd, 0, 0)") == 2,
          "虚线框的「起点 / 落点」都用同一个选点器")
    check("cam_point_ray(&p, &ro, &rd)" in ghost, "ghost_tick 只算一次射线，省一次 native 调用")
    check("nav_find(g, &p, 3.0f)" not in ghost and "nav_find(g, &p, 2.5f)" not in ghost,
          "预览里没有旧的落点判据")

    print("[6] 菜单文案 / 日志")
    check("终点 B：准星压在路点方块上" in ed, "菜单不再写「对准准星 3 m 内的路点」")
    check("对准 3 m 内的路点" not in ed, "旧文案已删")
    check("准星没压住路点（最近 #%d 偏 %.2f m；屏幕中心射线和 forward 差 %.2f°）" in ed,
          "失败日志写清：最近哪颗、偏多少、和 forward 差几度")
    check("准星选中 #%d（偏 %.2f m" in ed, "成功日志也写偏了多少（下次能据此调容差）")
    check("和 forward 差 %.2f°" in ed, "开菜单就打一行诊断（不按 5 也能看出 forward 有没有偏）")
    check("（相机 '%s'）" in ed, "诊断里带上 Camera.main 的名字（万一是拿错了相机，一眼能看出来）")

    print("[7] 数学样例（同样的几何，旧判据漏 / 新判据中）")
    cam = (0.0, 10.0, 0.0)
    node = (0.0, 6.0, 8.0)          # 半空的跳点：方块画在 6 m 高，脚下地面是 0 m

    def sub(a, b):
        return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

    def dot(a, b):
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    def norm(a):
        n = math.sqrt(dot(a, a))
        return (a[0] / n, a[1] / n, a[2] / n)

    v = sub(node, cam)
    d = norm(v)
    t = dot(v, d)
    perp = math.sqrt(max(0.0, dot(v, v) - t * t))
    tol = min(0.45 + 0.02 * t, 3.0)
    # 旧判据：沿同一条射线找第一个撞到地面 y=0 的点
    s = (0.0 - cam[1]) / d[1]
    hit = (cam[0] + d[0] * s, cam[1] + d[1] * s, cam[2] + d[2] * s)
    old_d = math.sqrt(dot(sub(hit, node), sub(hit, node)))
    print("       相机%s 节点%s 落点%s: 旧判据偏 %.2f m，新判据垂直距离 %.2f m（容差 %.2f）"
          % (cam, node, tuple(round(x, 2) for x in hit), old_d, perp, tol))
    check(old_d > 3.0, "旧判据：落点离方块 %.2f m > 3 m -> 选不中（用户遇到的正是这种）" % old_d)
    check(perp <= tol, "新判据：垂直距离 %.2f m <= 容差 %.2f m -> 选中" % (perp, tol))

    # 偏开 1.5 m（20 m 外）不该误抓
    t2 = 20.0
    perp2 = 1.5
    tol2 = min(0.45 + 0.02 * t2, 3.0)
    check(perp2 > tol2, "准星偏开 1.5 m（20 m 外）容差 %.2f m -> 不选，不会一按就抓旁边的点" % tol2)
    # 手感：近处 ≈ 3~4 个方块半径（方块半边长 0.14 m），远处按 2% 放宽但屏幕上仍有可瞄像素。
    focal = 1080.0 / (2.0 * math.tan(math.radians(30.0)))     # 1080p / 60° FOV
    for dist in (3.0, 10.0, 30.0, 60.0):
        tol_d = min(0.45 + 0.02 * dist, 3.0)
        radii = tol_d / 0.14
        px = (tol_d / dist) * focal
        if dist <= 10.0:
            check(3.0 <= radii <= 4.8, "%.0f m 处容差 = %.1f 个方块半径（近处跟手）" % (dist, radii))
        check(20.0 <= px <= 200.0, "%.0f m 处屏幕上还有 %.0f px 的可瞄范围（远处方块再小也点得住）"
              % (dist, px))

    print("[8] 编译陷阱 / 文档")
    check(re.search(r"\b(?:int|float|unsigned)\s[^;\n]*\bnear\b\s*=", ed) is None,
          "没有把变量叫 near（windef.h 的宏，gcc 会报 expected identifier）")
    check(os.path.isfile(os.path.join(UCF_ROOT, "docs", "record", "准星选点_2026-11-26.md")),
          "改动记录 docs/record/准星选点_2026-11-26.md")

    print("")
    if FAIL:
        print("FAILED: %d 项" % len(FAIL))
        for f in FAIL:
            print("  - " + f)
        return 1
    print("全部通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
