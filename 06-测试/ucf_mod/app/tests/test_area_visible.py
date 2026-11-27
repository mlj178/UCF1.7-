#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：新建守卫区必须「看得见」，且绿框的含义不能被悄悄改掉（2026-11-26）。

跑法：python app/tests/test_area_visible.py

用户问题（原话）：「添加守卫区，并不会立即显示绿色的方框，一个会立即显示，一个不会。
另外就是守卫区显示绿色方框，是不是必须里面有守卫点才会显示呢？」

结论已写进 docs/record/守卫区绿框与待激活_2026-11-26.md。这个脚本只查代码别走样：
  1) 绿框来自 read_nano 读游戏的 SpareAreaList（不是我们的标记表）；
  2) 守卫区建完**故意不激活**，第一个守卫点挂上才激活（激活 = 进 SpareAreaList）；
  3) 未激活的守卫区由我们自己补画金色线框（同尺寸、只画不进导出），立刻有反馈；
  4) 菜单把「金色线框 → 绿框」和「点离区中心多远」写出来；
  5) elog 有 printf 格式检查，且 vis 汇总行不再有错位的 guard=%d。
"""
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
    j = src.find(end, i + 1)
    return src[i:j] if i >= 0 and j > i else ""


def main():
    ed = read(os.path.join("src", "editor.c"))

    print("[1] 绿框的来源")
    nano = section(ed, "static void read_nano(void) {", "static void read_crouch")
    check('static_obj(g_areaCls, "SpareAreaList")' in nano,
          "守卫区是从游戏的 SpareAreaList 读的（不是从我们的 markers 表）")
    check('vf_add(p, K_NAREA, i, "守卫区");' in nano, "读到的区进 K_NAREA（绿框）")
    vis = section(ed, "static void vis_draw(void) {", "static void vis_show(int on)")
    check("draw_vf(K_NAREA, 2, 1, 2.4f, 1.7f, 2.4f);" in vis,
          "绿框尺寸 2.4/1.7/2.4（半尺寸）")

    print("[2] 激活时机：必须有一个守卫点")
    area = section(ed, "static int make_area_aid(int scale10", "static int make_area(int scale10")
    check("g_areaLive[aid] = 0;" in area, "新建区标记为「未激活」")
    check("((set_active_t)RVA(R_SETACTIVE))(go, 0, 0);" in area, "新建区 GameObject 先不激活")
    check("等第一个守卫点再激活" in area, "代码里写明「等第一个守卫点再激活」")
    # 2026-11-27：make_nanopos 多了一个朝向参数（蹲守点 / 守卫点写 zoomPos 用）
    npos = section(ed, "static int make_nanopos(int aid, V3 p, int safety, float yaw) {", "/* delete marker at idx")
    check("g_areaLive[aid] = 1;" in npos, "挂上第一个守卫点时把区标成已激活")
    check("((set_active_t)RVA(R_SETACTIVE))(areaGo, 1, 0);" in npos, "挂上第一个守卫点时激活区")
    check("area_register(areaComp);" in npos, "激活后兜底登记 SpareAreaList")

    print("[3] 未激活的区也要看得见（金色线框，且不吃进图后的推迟）")
    pend = section(ed, "static void pend_draw_set(int k, const V3* pos", "static void vis_show(int on)")
    check(pend != "", "有 pend_area_tick()（自己的那套，不走 vis_rebuild）")
    check("g_mk[i].type != MT_AREA" in pend, "只挑守卫区标记")
    check("g_areaLive[aid]" in pend, "已激活的跳过（绿框已经由 read_nano 画）")
    check("pend_draw_set(0, posP, np, 14, hp);" in pend, "未激活 -> 槽位 14（金色）")
    check("pend_draw_set(1, posL, nl, 2, hl);" in pend,
          "已挂点但可视化还没重建 -> 槽位 2（绿），避免「点了框就没了」")
    check("P mat = mat_for(slot);" in pend, "两套框共用同一个画框函数")
    check("bs_wbox(pos[i], hh, 0.05f);" in pend, "画的是线框（和绿框同一种画法）")
    check("hh.x = 2.4f; hh.y = 1.7f; hh.z = 2.4f;" in pend, "尺寸和绿框一致")
    check("g_nanoSeen[j] == g_mk[i].comp" in pend, "已经在 SpareAreaList 里的区让位给可视化层（不叠加）")
    check("vf_add" not in pend, "不塞进 g_vf（导出 JSON 里的守卫区仍然只认真列表）")
    check("g_sceneAge" not in pend, "不受 VIS_SCENE_WAIT 限制（进图头 22 s 也能看）")
    # 2026-11-26：采集模式（collect_only）整块删了，这里只剩总开关 + 守卫区图层
    check("!g_visOn || !g_visNano" in pend, "跟着总开关 / 守卫区图层")
    tick = section(ed, "void editor_tick(void)", "/* 练习场开关")
    check("pend_area_tick();" in tick, "editor_tick 每 tick 调一次")
    check("vis_area_pend" not in vis, "vis_draw 里不再重复画（避免两份金色框）")
    reset = section(ed, "static void vis_scene_reset(void) {", "static void vis_toggle(void)")
    check("g_pendGo[pi] = g_pendMesh[pi] = g_pendMf[pi] = g_pendMr[pi] = 0;" in reset,
          "换图时丢掉旧的线框对象指针")
    check("g_nanoSeenN = 0;" in reset, "换图时清掉上一张图的 SpareAreaList 快照")

    print("[4] 菜单把状态写清楚")
    check("金色线框" in ed, "菜单写明新建后是金色线框")
    check("金色线框 → 绿框" in ed, "菜单写明挂点后变绿框")
    check("static int area_at(const V3* p)" in ed, "有 area_at()：按落点归区")
    check("if (dx > 1.6f || dy > 1.6f || dz > 1.6f) continue;" in ed,
          "只认 3 m 框内（半宽 1.5 + 0.1 容差）")
    act2 = section(ed, "if (g_wpMenuSub == 3) {                 /* 守卫区 */", "if (g_wpMenuSub == 4)")
    check("area_at(&p)" in act2, "菜单里「加守卫点」按落点找区")
    place = section(ed, "    case 3: {", "    case 4:")
    check("area_at(&p)" in place, "笔刷放守卫点也按落点找区")
    check("当前没有守卫区" not in ed, "不再按「当前区」挂点（旧规则已删）")

    print("[5] 日志不再错位")
    check("__attribute__((format(printf, 1, 2)))" in ed, "elog 有 printf 格式检查")
    check("crouch=%d guard=%d" not in ed, "vis 汇总行里没有残留的 guard=%d")
    i0 = ed.find('elog("vis: nodes=%d')
    i1 = ed.find(");", i0)
    line = ed[i0:i1] if i0 >= 0 and i1 > i0 else ""
    fmt = line.split('"', 1)[1].rsplit('"', 1)[0] if '"' in line else ""
    args = line.rsplit('"', 1)[1] if '"' in line else ""
    nspec = len(re.findall(r"%[ds]", fmt))
    nargs = len([a for a in args.split(",") if a.strip()])
    check(nspec > 0 and nspec == nargs,
          "vis 汇总行：格式符 %d 个 / 参数 %d 个（必须相等）" % (nspec, nargs))

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
