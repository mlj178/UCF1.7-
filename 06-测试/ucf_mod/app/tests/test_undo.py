#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：路点菜单「撤销一步」必须真的把上一步撤回来（2026-11-26 用户报障）。

跑法：python app/tests/test_undo.py

只读，不开窗口。查这几件事：
  1) 一次用户动作 = 一个撤销步（NAVED.grp），加点+自动连边、跳点三件套整组反做；
  2) 跳点撤销要真删掉场景里的 Bot_JumpLink（mk_kill_jump），不能只从清单里摘；
  3) 删点撤销要把底图快照里的连线一起搬回来（nav_base_restore_conns）；
  4) 删掉「自己加的点」也能撤销（NPOPADD + g_drop 槽位），不会再弹到更早一步；
  5) 贴地进撤销栈（NMOVE，会话级，不落盘）；
  6) 标记 / 出生点的增删也进撤销栈（mke_*），和点图共用步号比较先后；
  7) 撤销/重做失败必须写日志说明，不能静默出栈；
  8) 菜单里能看到撤销栈状态和「上一手做了什么」；
  9) 保存时不写会话级辅助条目。
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

    print("[1] 一次动作 = 一个撤销步")
    check("int   grp;" in section(ed, "typedef struct {", "} NAVED;"),
          "NAVED 有 grp（撤销步号）")
    push = section(ed, "static void nav_push(int kind", "static void nav_push_dir")
    check("e->grp = g_edStep;" in push, "nav_push 给条目打步号")
    check("static void ed_step(void)" in ed, "有 ed_step()（动作边界）")
    for fn, why in [
        ("static void nav_add_here", "加点"),
        ("static void nav_del_here", "删点"),
        ("static void nav_unlink_here", "断边"),
        ("static void nav_link_one", "连边"),
        ("static void nav_ground_here", "贴地"),
        ("static void wp_place", "放置（含标记）"),
        ("static int delete_nearest_of", "删除标记"),
    ]:
        body = section(ed, fn, "\n}\n")
        check("ed_step();" in body, "%s 前先开新的一步（ed_step）" % why)
    undo = section(ed, "static void nav_undo(void) {", "static void nav_redo(void) {")
    check("grp = g_ned[g_nedN - 1].grp;" in undo, "撤销取栈顶步号")
    check("if (grp > 0 && e->grp != grp) break;" in undo, "撤销按步号整组出栈")
    check("if (grp <= 0) break;" in undo, "读盘的旧条目（无步号）一次只撤一条")

    print("[2] 跳点撤销真的删掉跳链")
    u1 = section(ed, "static int nav_undo_one", "static int nav_redo_one")
    check("case JADD:" in u1 and "mk_kill_jump" in u1, "JADD 撤销 -> mk_kill_jump")
    kill = section(ed, "static int mk_kill_jump", "static void nav_ed_desc")
    check("del_index_ex(i, 0);" in kill, "跳链用 del_index_ex(.., 0) 真销毁（不动清单）")
    check("jump_unsee(" in kill, "跳链销毁后把 jumpSeen 记录一起摘掉")
    check('elog("naved: undo jump: 场景里没有这条跳链' in kill, "找不到跳链时写日志，不静默")

    print("[3] 删点撤销恢复连线")
    check("nav_find_dead_at(g, &e->a)" in u1, "按整数倍地下深度找回原来的槽位")
    check("nav_base_restore_conns(g, ia)" in u1, "从底图快照恢复这一点的连线")
    check("nav_apply_edges(g);" in u1, "再用清单里剩下的边记录校正一遍")

    print("[4] 删掉自己加的点也能撤销")
    drop = section(ed, "static int nav_drop_add(const V3* p) {", "/* 删跳链")
    check("g_lastDrop.e[g_lastDrop.n++] = *e;" in drop, "nav_drop_add 抄下被摘掉的条目")
    delh = section(ed, "static void nav_del_here(void)", "/* ---- 菜单动作")
    check("nav_push(NPOPADD" in delh, "删自加点时压一条 NPOPADD")
    check("g_drop[d] = g_lastDrop;" in delh, "摘掉的条目按槽位存好")
    check("case NPOPADD:" in u1, "撤销 NPOPADD = 点放回来 + 条目补回清单")

    print("[5] 贴地进撤销栈（会话级）")
    check("#define NMOVE" in ed, "有 NMOVE 种类")
    ground = section(ed, "static void nav_ground_here(void)", "static void nav_link_one")
    check("nav_push(NMOVE" in ground, "贴地压 NMOVE（a=旧坐标 b=新坐标）")
    check("case NMOVE:" in u1, "撤销贴地 -> 写回旧坐标")
    save = section(ed, "static int nav_save(void)", "void editor_save_all")
    check("e->kind == NMOVE || e->kind == NPOPADD" in save, "保存时跳过会话级条目")
    na = section(ed, "static int nav_needs_apply", "#define NAV_CONN_MAX")
    check("e->kind == NPOPADD" in na and "e->kind == NMOVE" in na,
          "重套核对时跳过会话级条目（NMOVE 只核对位置）")

    print("[6] 标记 / 出生点也有撤销")
    check("static MKE g_mke[MKE_MAX];" in ed, "有标记撤销栈 g_mke")
    check("static void mke_note_add(int first);" in ed, "有 mke_note_add 声明")
    dlex = section(ed, "static void del_index_ex(int idx, int drop_nav)", "static void del_index(int idx)")
    check("mke_note_del(&m," in dlex, "删标记时记一笔（守卫区连带点位按同一组）")
    check("if (drop_nav)" in dlex, "撤销自己删的标记时不再重复记")
    wp = section(ed, "static void wp_place(void)", "/* ---- 测试包")
    check("mke_note_add(n0);" in wp, "放置标记后记一笔")
    spawn = section(ed, "static int spawn_add_point", "static void spawn_restore_orig")
    check("mke_note_spawn_add(" in spawn, "加出生点记一笔")
    check("mke_note_spawn_del(" in spawn, "删出生点记一笔")
    check("static void ed_undo(void)" in ed and "ed_top_mke() > ed_top_nav()" in ed,
          "撤销按步号比较点图 / 标记，永远反做最近那一步")
    check("static void ed_redo(void)" in ed, "重做同样按步号比较")

    print("[7] 入口改走统一撤销")
    menu4 = section(ed, "if (g_wpMenuSub == 4) {", "if (g_wpMenuSub == 5)")
    check("ed_undo();" in menu4 and "ed_redo();" in menu4, "菜单「撤销一步 / 恢复」-> ed_undo / ed_redo")
    check('WP_EDIT[3] = { "撤销一步", "恢复（撤销的反操作）", "保存（Ctrl+S）" };' in ed,
          "菜单第 2 项叫「恢复（撤销的反操作）」（2026-11-26 用户要求改名）")
    check('if (g_wpMenuSub == 4) return 3;' in ed, "撤销页只剩 3 项")
    check('"重读并套用"' not in ed and "static void nav_reapply" not in ed,
          "「重读并套用」整项删除（菜单里不再出现；重读改走控制台重新应用）")
    check('if (!strcmp(cmd, "undo")) { ed_undo(); return; }' in ed, "控制台 cmd=undo -> ed_undo")
    check('if (!strcmp(cmd, "redo")) { ed_redo(); return; }' in ed, "控制台 cmd=redo -> ed_redo")

    print("[8] 失败要说清楚，菜单要看得见")
    check('elog("naved: undo edge: 端点已经不在图上' in u1, "边撤销失败有日志")
    check('elog("naved: undo del: 找不到原点' in u1, "删点撤销失败有日志")
    check('wp_hint("撤销 %d 条' in ed, "撤销结果写进菜单提示")
    check("点图 %d 条 · 标记 %d 个" in ed, "菜单显示两套撤销栈的条数")
    check("最近一步：" in ed, "菜单显示最近一步是什么")
    check("nav_ed_desc(" in ed and "mke_desc(" in ed, "两套撤销都有可读描述")
    for fn in ("static int mke_undo_one", "static int mke_redo_one"):
        body = section(ed, fn, "static void mke_undo(void)")
        check("e->kind == MKE_ADD" in body and "mk_recreate(e)" in body,
              "%s 支持增 / 删两个方向" % fn.split()[-1])

    print()
    if FAIL:
        print("FAILED %d check(s):" % len(FAIL))
        for f in FAIL:
            print("  - " + f)
        raise SystemExit(1)
    print("OK: undo step grouping / jump destroy / conn restore / del-added / move / "
          "marker undo / menu feedback all present in editor.c")


if __name__ == "__main__":
    main()
