#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：蹲守点的「朝向」（2026-11-27；2026-11-28 守卫点去掉方向）。

跑法：python app/tests/test_direction.py

用户原话：路点菜单里的蹲守点、守卫点有方向，可是游戏里只显示一个球，看不出来；
先讨论方案（选定：方案 C = 射线 + 近点度数文本；默认只显示准星对着的那一个点）。
只读、不开窗口。查这几件事：
  1) 方向真的写进游戏：zoomPos@0x10 写一个「点位 + 朝向*10 m」的世界目标点；
     原生数据核实是世界目标点（UnityPy 解场景，7~53 m），不是单位向量；
  2) 放置时朝向 = 相机朝向（蹲守点 / 守卫点两条创建路径都要传）；
  3) markers.txt 老格式照读，新格式第 5/6 列是朝向（度，0=北 90=东）；
  4) 撤销 / 重做重建点位时朝向要一起回来；
  5) 显示：只画准星正对着的那一个点；读不到方向画虚线、菜单写「未知」，不默认 0°；
  6) 朝向工具页：设为相机朝向 / 顺逆 15° / 清空 / 显示样式；←/→ 直接转（Shift 1°）；
  7) 原生点位不能改（改不了就不给假象）。
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
    if i < 0:
        return ""
    j = src.find(end, i + 1)
    return src[i:j] if j > i else src[i:]


def main():
    ed = read(os.path.join("src", "editor.c"))

    print("[1] 方向写进游戏（zoomPos）")
    wz = section(ed, "static int write_zoom(P comp, const V3* p, float yaw) {", "static int read_zoom(")
    check("(char*)comp + 0x10" in wz, "写 Bot_GuardPos / Bot_NanoGuardPos 的 zoomPos 字段（0x10）")
    check("DIR_RANGE" in wz, "写的是「点位 + 朝向 * DIR_RANGE」的世界目标点")
    check("t.y = p->y;" in wz, "目标点和点位同高：只表达水平朝向，不带俯仰")
    rz = section(ed, "static int read_zoom(P comp, const V3* p, float* out, int cap) {", "static int make_crouch(")
    check("yaw_of_dir" in rz, "读原生 zoomPos：世界点 -> 点位指向它的角度")
    check("fabsf(y - out[0]) < 2.0f" in rz, "重复方向去重（Init 会把入口点并进来，常见重复）")

    print("[2] 放置时朝向 = 相机朝向")
    check("static float cam_dir_yaw(void)" in ed, "有相机朝向（0=北 90=东，和罗盘同一套）")
    check("make_crouch(V3 p, float yaw)" in ed, "make_crouch 收朝向")
    check("make_nanopos(int aid, V3 p, int safety, float yaw)" in ed, "make_nanopos 收朝向")
    crouch = section(ed, "static int make_crouch(V3 p, float yaw) {", "static P vec3_arr_new")
    check("write_zoom(comp, &p, yaw)" in crouch, "蹲守点创建时就写 zoomPos（以前是 null，朝向未定义）")
    nano = section(ed, "static int make_nanopos(int aid, V3 p, int safety, float yaw) {", "static int area_at(")
    check("(void)yaw;" in nano, "守卫点不再使用 yaw（2026-11-28 用户要求去掉方向）")
    check("vec3_arr_new(0, 0)" in nano, "守卫点自己的 zoomPos 留空")
    check("make_entrance(aid, c)" in nano, "没有入口时自动补区中心入口（保证 zoomPos 非空）")
    check("(0,0,1)" not in nano or "固定值" in nano, "不再写死 (0,0,1)/(1,0,0) 占位方向")
    place = section(ed, "static void wp_place(void) {", "static void pack_stat(void)")
    check("cam_dir_yaw()" in place, "按 5 放置蹲守点时仍用相机朝向")
    sub = section(ed, "static int guard_add_place(void) {", "/* 菜单确认")
    check("make_nanopos(g_mk[ai].aid, p, g_nanoSafety, YAW_NONE)" in sub,
          "加守卫点子页放点用当前安全等级、不带方向")

    print("[3] markers.txt 兼容")
    save = section(ed, "static int save_file(void) {", "static void reset_markers(void)")
    check('"crouch %d %.3f %.3f %.3f %.1f' in save, "crouch 行可带第 5 列朝向")
    check('"nanopos %d %.3f %.3f %.3f %d' in save, "nanopos 行不再写第 6 列朝向")
    check('"crouch %d %.3f %.3f %.3f %.1f' in save, "crouch 行仍带朝向")
    load = section(ed, "static int load_file(void) {", "/* ================= 出生点编辑")
    check('"crouch %d %f %f %f %f"' in load, "读 crouch 第 5 列")
    check('"nanopos %d %f %f %f %d"' in load, "读 nanopos 5 列（老第 6 列忽略）")
    check("make_nanopos(a, p, b, YAW_NONE)" in load, "读档建守卫点时不再传朝向")
    check(">= 4" in load and ">= 5" in load, "列数不够（老文件）不会误判失败")

    print("[4] 撤销 / 重做带朝向")
    note = section(ed, "static void mke_note_add(int first) {", "static void mke_note_del(")
    check("e.yaw = mk->yaw;" in note, "记撤销时存下朝向")
    rec = section(ed, "static int mk_recreate(const MKE* e) {", "static void mke_desc(")
    check("make_crouch(e->p, e->yaw)" in rec, "撤销重建蹲守点带朝向")
    check("make_nanopos(e->aid, e->p, e->prm, YAW_NONE)" in rec, "撤销重建守卫点不再带朝向")

    print("[5] 显示：只画准星对着的那一个")
    pick = section(ed, "static int dir_pick(int* src", "/* 方向层网格")
    check("g_mk[i].type != MT_CROUCH" in pick, "只看蹲守点（守卫点已去掉方向）")
    check("perp <= 0.9f" in pick, "按准星射线选点（垂直距离 <= 0.9 m）")
    check("g_vf[i].kind != K_CROUCH" in pick, "自己建的点优先，其次读游戏里的蹲守点")
    tick = section(ed, "static void dir_tick(void) {", "static void overlay_init")
    check("dir_pick(&src, &idx, &p, yaw, &n, &unknown)" in tick, "每 tick 只挑一个点")
    check("dir_hide(); return;" in tick, "没对准就收起（不糊屏）")
    check("!g_wpMenuOpen" in tick, "只在 F2 菜单开着时显示（关菜单 = 画面干净，和单向边箭头同口径）")
    build = section(ed, "static void dir_build_mesh(void) {", "static unsigned dir_sig(void) {")
    check("g_dirUnknown" in build and "0.35f" in build, "读不到方向画虚线小圈")
    check("DIR_RAY_LEN" in build or "DIR_RAY_LEN" in tick, "射线样式（用户选的方案 A 打底）")
    check("DIR_FAN_R" in build, "扇形样式（朝向工具里可切）")
    check("朝向未知" in tick, "浮字写明「未知」，不默认 0°")
    lbl = section(ed, "static void dir_label_build(P canvasTr) {", "/* 弹一条提示")
    check("UCF_HUD_DirText" in lbl, "准星下方一行度数文本（方案 C）")
    check("dir_tick();" in ed, "主循环里调用 dir_tick")

    print("[6] 朝向工具页")
    menu = section(ed, "static const char* WP_MENU[] = {", "#define WP_MENU_N")
    check("朝向工具" in menu, "主菜单有「朝向工具」")
    wd = section(ed, "static const char* WP_DIR[WP_DIR_N] = {", "static const char* WP_DEL[2]")
    check("设为相机朝向" in wd, "设为相机朝向")
    check("顺时针" in wd and "逆时针" in wd, "顺 / 逆 15°")
    check("清空方向" in wd, "清空方向（回到未知）")
    check("射线 / 扇形 / 关" in wd, "显示样式：射线 / 扇形 / 关")
    keys = section(ed, "int editor_menu_key(unsigned vk, int ext) {", "int editor_menu_is_open(void)")
    check("vk == VK_LEFT || vk == VK_RIGHT" in keys, "← / → 直接转")
    check("VK_SHIFT" in keys, "Shift 精调 1°")
    apply_ = section(ed, "static int dir_apply(float yaw, const char* why) {", "static int dir_rotate(")
    check("只能改自己放的" in apply_ or "原生点位，朝向改不了" in apply_, "原生点位不给假象（明确拒绝）")
    check("write_zoom(m->comp, &m->p, m->yaw)" in apply_, "改完立刻写回游戏")
    check("editor_dirty_mk()" in apply_, "改朝向算未保存（Ctrl+S 才落盘）")
    check("YAW_NONE" in apply_, "清空 = 回到未知（游戏侧留兜底，不写空数组）")

    print("[7] 放置预览带朝向")
    gt = section(ed, "static void ghost_dir_arrow_tick(V3 p, float yaw) {", "/* 换图 / 退出时把预览全部丢掉")
    check("dir_of_yaw(yaw, &d)" in gt, "预览箭头按同一套朝向摆")
    gk = section(ed, "static void ghost_tick(void) {", "static int make_jump_link_ex")
    check("brush == 2 && ok" in gk, "只有蹲守点预览画朝向（守卫点已去掉方向）")
    check("ghost_dir_arrow_hide();" in gk, "其它情况收起")

    print()
    if FAIL:
        print("失败 %d 项：" % len(FAIL))
        for f in FAIL:
            print("  - " + f)
        raise SystemExit(1)
    print("全部通过")


if __name__ == "__main__":
    main()
