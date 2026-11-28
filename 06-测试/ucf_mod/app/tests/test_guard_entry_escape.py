#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""守卫区入口 / 逃跑点（2026-11-28）

菜单「3 守卫区工具 → 3 加入口 / 4 加逃跑点」以前是空的：按 5 只写日志。
现在：
  * 入口 -> area.entrancePos（Vector3[]），游戏 Init 时并进每个守卫点的 zoomPos，
    只影响站定后的张望方向，不决定从哪进区；
  * 逃跑点 -> area.escapePos（Vector3[]），被压且没有更安全的守卫点时随机取一个跑。
  * 两者都要写进 markers.txt：entrance <aid> x y z / escape <aid> x y z；
    删除时从数组里摘掉；撤销/重做能重建。

跑法：python app\tests\test_guard_entry_escape.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)

for _p in (HERE, os.path.join(UCF_ROOT, "app"), os.path.join(UCF_ROOT, "src")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

FAIL = []


def check(ok, msg):
    if ok:
        print("  OK  " + msg)
    else:
        FAIL.append(msg)
        print("  !!  " + msg)


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def section(src, begin, end):
    i = src.find(begin)
    if i < 0:
        return ""
    j = src.find(end, i + len(begin))
    return src[i:] if j < 0 else src[i:j]


def main():
    ed = read(os.path.join(UCF_ROOT, "src", "editor.c"))
    print("[1] 类型 / 数组扩容")
    check("#define MT_ENTRY   9" in ed and "#define MT_ESCAPE  10" in ed,
          "MT_ENTRY / MT_ESCAPE 类型已定义")
    push = section(ed, "static int vec3_arr_push(P comp, int off, const V3* p) {",
                   "static int vec3_arr_remove(")
    check("vec3_arr_new(buf, n + 1)" in push and "*(P*)((char*)comp + off) = na;" in push,
          "vec3_arr_push 重建数组（保留旧元素 + 新点）")
    rem = section(ed, "static int vec3_arr_remove(P comp, int off, const V3* p) {",
                  "static int list_count(")
    check("if (n == 1)" in rem and "vec3_arr_new(0, 0)" in rem,
          "vec3_arr_remove 删最后一个点后留空数组（不写 null）")

    print("[2] 创建函数")
    ent = section(ed, "static int make_entrance(int aid, V3 p) {", "static int make_escape(")
    esc = section(ed, "static int make_escape(int aid, V3 p) {", "/* 准星落点落在哪个守卫区")
    check("vec3_arr_push(areaComp, 0x0C, &p)" in ent, "make_entrance 写 entrancePos@0x0C")
    check("add_mk(MT_ENTRY" in ent, "入口也进 g_mk（可视化/删除/撤销）")
    check("refresh_area_guard_dirs(parent)" in ent, "加入口后刷新已有守卫点的 zoomPos")
    check("vec3_arr_push(areaComp, 0x1C, &p)" in esc, "make_escape 写 escapePos@0x1C")
    check("add_mk(MT_ESCAPE" in esc, "逃跑点也进 g_mk")
    ref = section(ed, "static void refresh_area_guard_dirs(int parent) {", "static int make_entrance(")
    check("R_POS_INIT" in ref and "vec3_arr_new(0, 0)" in ref,
          "刷新 = 清空守卫点自己的方向 + Init 重新并入 entrancePos（无入口才兜底正北）")

    print("[3] 菜单已接线")
    act = section(ed, "if (g_wpMenuSub == 3) {                 /* 守卫区 */",
                  "if (g_wpMenuSub == 4)")
    check("make_entrance(g_mk[ai].aid, p);" in act, "菜单 3 加入口")
    check("make_escape(g_mk[ai].aid, p);" in act, "菜单 4 加逃跑点")
    check("entrance/escape not wired" not in act, "旧的「还没接」占位已删除")
    check("entry / 逃跑" not in ed and "入口 / 逃跑点还没接" not in ed,
          "提示里不再说 3/4 没接")
    check("WP_AREAS" in ed and "加入口（站定后朝这看）" in ed and "加逃跑点（被压时跑这）" in ed,
          "菜单项名字直接说明作用")
    sub = section(ed, "static int guard_add_place(void) {", "/* 菜单确认")
    keys = section(ed, "int editor_menu_key(unsigned vk, int ext) {", "void editor_on_key_plain")
    check("if (i == 1)" in act and "g_wpMenuSub = 10" in act,
          "守卫区第 2 项进入加守卫点子页")
    check("WP_GADD" in ed and "安全等级 0" in ed and "放一个守卫点" in ed,
          "子页 1-4 选安全等级、5 放点")
    check('"放一个守卫点（安全等级 %d）"' in ed, "第 5 项动态显示当前等级")
    check("g_wpMenuSub == 10 && vk >= '1' && vk <= '5'" in keys and "g_nanoSafety = gi" in keys,
          "子页数字键 1-4 直接切换等级")
    check("make_nanopos(g_mk[ai].aid, p, g_nanoSafety, YAW_NONE)" in sub,
          "放点时用当前选的安全等级")
    check("static int guard_pick" in ed and "g_vf[besti].aux" in ed,
          "准星指守卫点时能读到自己/原生点的 safety")
    check("守卫点 · 安全等级 %d" in ed, "准星指向守卫点显示安全等级")
    tick = section(ed, "static void dir_tick(void) {", "static void vis_show")
    check("guard_pick(&gs, &gi, &gp, &gsafety)" in tick, "没有蹲守点时回落到守卫点 safety 显示")

    print("[4] 落盘 / 读档")
    save = section(ed, "static int save_file(void) {", "static void reset_markers(void)")
    check('"entrance %d %.3f %.3f %.3f' in save, "markers.txt 写 entrance 行")
    check('"escape %d %.3f %.3f %.3f' in save, "markers.txt 写 escape 行")
    check("entrance=%d escape=%d" in save, "header 计数带 entrance / escape")
    check('"# nano_safety %d' in save, "markers.txt 存新建守卫点默认安全等级")
    load = section(ed, "static int load_file(void) {", "static int spawn_parse_line")
    check('sscanf(line, "entrance %d %f %f %f"' in load, "读 entrance 行")
    check('sscanf(line, "escape %d %f %f %f"' in load, "读 escape 行")
    check('sscanf(line, "# nano_safety %d"' in load, "读默认安全等级")

    print("[5] 删除 / 撤销")
    mr = section(ed, "static void marker_unregister(MK* m) {", "static void del_index_ex")
    check("m->type == MT_ENTRY || m->type == MT_ESCAPE" in mr, "删除入口/逃跑点有分支")
    check("vec3_arr_remove(area, off, &m->p)" in mr, "删除时从区数组摘掉（不只删球）")
    rec = section(ed, "static int mk_recreate(const MKE* e) {", "static void mke_desc")
    check("case MT_ENTRY:" in rec and "make_entrance(e->aid, e->p)" in rec,
          "撤销/重做能重建入口")
    check("case MT_ESCAPE:" in rec and "make_escape(e->aid, e->p)" in rec,
          "撤销/重做能重建逃跑点")
    check("守卫区入口" in ed and "守卫区逃跑点" in ed, "撤销/删除日志有中文名")

    print("[6] 可视化 tab 接线")
    consts = read(os.path.join(UCF_ROOT, "app", "ui", "consts.py"))
    cfg = read(os.path.join(UCF_ROOT, "src", "cfg.c"))
    for key in ("vis_entry", "vis_escape", "vis_eline"):
        check(('"' + key + '"') in consts, "可视化页有 " + key + " 勾选")
        check(('"' + key + '"') in cfg, "cfg.c 有 " + key + " 默认值")
    check('"vis_entry": "entry"' in consts and '"vis_escape": "escape"' in consts
          and '"vis_eline": "eline"' in consts,
          "LIVE_VIS_KEYS 下发 entry / escape / eline")
    for field in ("entry=%d", "escape=%d", "eline=%d"):
        check(field in ed, "navcmd 解析 " + field)
    mk = section(ed, "static void mk_vis_apply(void) {", "static int add_mk(")
    check("MT_ENTRY" in mk and "g_visEntry" in mk, "入口黄球受 vis_entry 控制")
    check("MT_ESCAPE" in mk and "g_visEscape" in mk, "逃跑点白球受 vis_escape 控制")
    draw = section(ed, "static void vis_draw(void) {", "static int  g_visDirty")
    check("g_visELine && g_eN" in draw, "粉色入口连线受 vis_eline 控制")
    readn = section(ed, "static void read_nano(void) {", "/* 守卫区自己的线框")
    check("g_visELine" in readn, "只开连线时也会读 entrancePos")

    print("")
    if FAIL:
        print("失败 %d 项：" % len(FAIL))
        for f in FAIL:
            print("  - " + f)
        return 1
    print("OK: 守卫区入口 / 逃跑点 菜单 / 数组 / 落盘 / 删除 / 撤销 全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
