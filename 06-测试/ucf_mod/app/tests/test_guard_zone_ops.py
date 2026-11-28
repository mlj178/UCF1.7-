#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：守卫区工具的 删除入口 / 删除逃跑点 / 整体移动守卫区（2026-11-28）

用户原话：
  「删除入口，逃跑点，整体移动守卫区，包含里面的守卫点，入口，逃跑点。
    这三个，在路点菜单中有所缺失，我希望可以补上。」

已确认的三个决策：
  * 第二步 = 删除逃跑点（和删除入口并列）；
  * 整体移动 = 两步确认（第一次 5 选中原区，第二次 5 在新位置确认）；
  * 删除入口 / 逃跑点 = 严格准星（0.6 m 内才删，否则拒绝），不做 12 m 兜底；
  * 三项只放在「3 守卫区工具」页，不往「5 删除点位」页重复开入口。

查这几件事：
  1) 菜单 7 项，名字写清作用；
  2) 删除走严格准星 + 真正从 entrancePos / escapePos 摘掉 + 可撤销；
  3) 整体移动 = 区 + 区下守卫点 / 入口 / 逃跑点一起平移，数组和 zoomPos 跟着走；
  4) 移动进撤销栈（MKE_MOVE），撤销回旧中心、恢复回新中心；
  5) 预览 / 状态复位 / 取消路径齐全，不会误移；
  6) markers.txt 格式不变（不新增行类型）。

跑法：python app\tests\test_guard_zone_ops.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)

FAIL = []


def check(ok, msg):
    if ok:
        print("  OK  " + msg)
    else:
        FAIL.append(msg)
        print("  !!  " + msg)


def read(rel):
    with open(os.path.join(UCF_ROOT, rel), "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def section(src, begin, end):
    i = src.find(begin)
    if i < 0:
        return ""
    j = src.find(end, i + len(begin))
    return src[i:] if j < 0 else src[i:j]


def main():
    ed = read(os.path.join("src", "editor.c"))

    print("[1] 菜单：守卫区工具 7 项")
    check("static const char* WP_AREAS[7]" in ed, "WP_AREAS 扩到 7 项")
    for label in ("删除入口（准星对准 · 可撤销）",
                  "删除逃跑点（准星对准 · 可撤销）",
                  "整体移动守卫区（连带守卫点/入口/逃跑点）"):
        check(label in ed, "菜单项：" + label)
    check("if (g_wpMenuSub == 3) return 7;" in ed, "menu_sub_count：sub 3 返回 7")
    check("(i >= 0 && i < 7) ? WP_AREAS[i]" in ed, "menu_sub_label：第 7 项有名字")
    block = section(ed, "if (g_wpMenuSub == 3 && off < (int)sizeof s - 460)",
                    "/* 准星处那个虚线框的坐标")
    check("1-7 / 8/2 只切换选中" in block, "底部写「1-7 只切换选中」")
    check("删除入口" in block and "删除逃跑点" in block and "整体移动守卫区" in block,
          "说明块覆盖三项")
    check("0.6 m 内按 5 / Delete 删除" in block, "删除入口/逃跑点写明严格准星 0.6 m")
    check('"entrancePos" : "escapePos"' in block,
          "说明删除的是区里的两个数组")
    check("第 1 次 5" in block and "第 2 次 5" in block, "整体移动写明两步确认")
    check("入口 / 逃跑点数组一起挪" in block, "整体移动写明数组一起挪")
    check("mt_count(want)" in block, "删除页显示图里现有数量")

    print("[2] 严格准星删除")
    strict = section(ed, "static int delete_marker_strict(int want) {",
                     "static void make_tag(V3 p, int tag, float radius);")
    check("bestPerp <= 0.6f" in strict, "射线 0.6 m 内才认")
    check("bestHit <= 6.25f" in strict, "落点 2.5 m 内（2.5^2）兜底")
    check("del_index(target);" in strict, "真删：走 del_index（连带数组摘除 / 撤销记录）")
    check("editor_dirty_mk();" in strict, "删除算未保存（Ctrl+S 才落盘）")
    check("toast_bad" in strict, "选不中走拒绝提示")
    act = section(ed, "if (g_wpMenuSub == 3) {                 /* 守卫区 */",
                  "if (g_wpMenuSub == 4)")
    check("delete_marker_strict((i == 4) ? MT_ENTRY : MT_ESCAPE)" in act,
          "菜单第 5 / 6 项：删入口 / 删逃跑点")
    keys = section(ed, "int editor_menu_key(unsigned vk, int ext) {", "void editor_on_key_plain")
    check("g_wpMenuSubSel == 4 || g_wpMenuSubSel == 5" in keys
          and "delete_marker_strict" in keys,
          "停在这两项时 Delete 也走严格准星")
    mr = section(ed, "static void marker_unregister(MK* m) {", "static void del_index_ex")
    check("m->type == MT_ENTRY || m->type == MT_ESCAPE" in mr
          and "vec3_arr_remove(area, off, &m->p)" in mr,
          "删除仍从区数组摘除（不是只删球）")

    print("[3] 整体移动：区 + 子项 + 数组")
    mv = section(ed, "static int area_move_whole(int ai, const V3* to) {",
                 "static int make_entrance(int aid, V3 p) {")
    check("g_mk[i].parent != ai" in mv, "遍历区下的守卫点 / 入口 / 逃跑点")
    check("R_SET_POS))(get_tr(areaGo)" in mv, "先移区 transform（BoxCollider 跟着走）")
    check(mv.find("R_SET_POS))(get_tr(areaGo)") < mv.find("g_mk[i].parent != ai"),
          "顺序：先区、后子物体（否则子节点会被二次位移）")
    check("R_SET_POS))(get_tr(g_mk[i].go)" in mv, "子物体世界坐标同步")
    check("mk_vis_move(&g_mk[i])" in mv and "mk_vis_move(&g_mk[ai])" in mv,
          "入口 / 逃跑点的球是根对象，单独挪")
    check("vec3_arr_shift(areaComp, 0x0C" in mv, "entrancePos 一起平移")
    check("vec3_arr_shift(areaComp, 0x1C" in mv, "escapePos 一起平移")
    check("refresh_area_guard_dirs(ai)" in mv, "入口挪完重刷守卫点 zoomPos")
    check("fabsf(d.x) < 0.001f" in mv, "原地不动时跳过（不产生空动作）")
    shift = section(ed, "static int vec3_arr_shift(P comp, int off, const V3* d) {", "static int list_count(")
    check("v[i].x += d->x;" in shift and "return n;" in shift, "数组逐元素平移")

    print("[4] 两步确认 / 状态复位")
    check("g_areaMoveAid < 0" in act, "第一次 5：选中准星下的区")
    check("area_marker_of_aid(g_areaMoveAid)" in act, "第二次 5：按 aid 找回区（下标会左移）")
    check("mke_note_area_move(ai, &old, &p)" in act, "移动进撤销栈")
    check("g_areaMoveAid = -1;" in act, "确认/取消后清状态")
    check("toast_ok(\"已选守卫区 aid=%d" in act, "选中后有反馈")
    back = section(ed, "static void menu_back(void) {", "static void menu_move(int delta)")
    check("g_areaMoveAid >= 0" in back and "已取消：守卫区没有移动" in back,
          "0 / Esc 先取消待移动")
    mov = section(ed, "static void menu_move(int delta) {", "static int brush_from_name")
    check("g_areaMoveAid >= 0 && g_wpMenuSubSel != 6" in mov, "8/2 切走就取消待移动")
    check("g_areaMoveAid >= 0 && i != 6" in keys, "数字键切走就取消待移动")
    check("待移动的区不跨次保留" in ed, "menu_open 复位")
    reset = section(ed, "static void reset_markers(void) {", "static int spawn_parse_line")
    check("g_areaMoveAid = -1;" in reset, "换图复位")

    print("[5] 预览")
    prev = section(ed, "static int wp_guard_preview(void) {", "\n}")
    check("g_wpMenuSubSel == 6" in prev, "第 7 项也画虚线框")
    tick = section(ed, "static void ghost_tick(void) {", "static int make_jump_link_ex")
    check("if (preview && g_wpMenuSub == 3 && g_wpMenuSubSel == 6) brush = 4;" in tick,
          "移动预览用守卫区 3 m 蓝框")
    check("按 5 确认移动" in ed and "按 5 选中这个区" in ed, "坐标行写明是选中 / 确认")

    print("[6] 撤销 / 重做")
    check("#define MKE_MOVE 3" in ed, "新增 MKE_MOVE")
    note = section(ed, "static void mke_note_area_move(int ai, const V3* oldp, const V3* newp) {",
                   "/* 出生点队号")
    check("e.kind = MKE_MOVE;" in note and "e.p = *oldp;" in note and "e.b = *newp;" in note,
          "记录旧中心 p / 新中心 b（按 aid 定位）")
    und = section(ed, "static int mke_undo_one(const MKE* e) {", "static int mke_redo_one(const MKE* e) {")
    check("if (e->kind == MKE_MOVE)" in und and "area_move_whole(ai, &e->p)" in und,
          "撤销：移回旧中心 p")
    red = section(ed, "static int mke_redo_one(const MKE* e) {", "/* 撤销/重做一组标记动作")
    check("if (e->kind == MKE_MOVE)" in red and "area_move_whole(ai, &e->b)" in red,
          "恢复：移回新中心 b")
    check("移动 守卫区 (%.1f %.1f %.1f) ->" in ed, "撤销栈文字写「移动 守卫区 old -> new」")

    print("[7] 落盘格式不变")
    save = section(ed, "static int save_file(void) {", "static void reset_markers(void)")
    check("entrance %d %.3f %.3f %.3f" in save and "escape %d %.3f %.3f %.3f" in save,
          "仍只写 entrance / escape / area / nanopos")
    check('fprintf(f, "move' not in save and '"areamove"' not in save,
          "不新增 move 行（移动只改坐标，不新增记录）")
    load = section(ed, "static int load_file(void) {", "static int spawn_parse_line")
    check("sscanf(line, \"entrance %d %f %f %f\"" in load
          and "sscanf(line, \"escape %d %f %f %f\"" in load,
          "读档仍是 entrance / escape 两行")

    print("")
    if FAIL:
        print("失败 %d 项：" % len(FAIL))
        for f in FAIL:
            print("  - " + f)
        return 1
    print("OK: 删除入口 / 删除逃跑点 / 整体移动守卫区 全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
