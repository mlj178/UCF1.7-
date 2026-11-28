#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：路点菜单每个动作都要给屏幕反馈（2026-11-26 用户要求）。

跑法：python app/tests/test_add_point.py

用户原话：
> 你只给普通路点做了提示，其他的都没做，应该都要做，路径，路点，守卫区，点，都要做上，给用户反馈。

查这几件事：
  1) 加点仍然禁止（不偷偷切 keep / AddNode），拒绝时红字提示；
  2) toast 两种语义：成功绿（短）/ 禁止红（长）——「提示下一步」的黄字按用户要求已删；
  3) **每一个菜单动作**都有 toast：普通路点、跳点、蹲守点、守卫区、守卫点、出生点、
     连边 / 断边、删点 / 删标记 / 删区域 / 删出生点、贴地、撤销 / 重做、保存；
  4) 失败分支和成功分支都要有（不能只弹失败）；
  5) toast 居中 / 亮色 / 3 s 内消失 / 换图重建 / 连按去重。
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

    print("[1] 加分仍然禁止（不偷偷新建）")
    check("static int nav_add_fresh" not in ed, "没有 keep/AddNode 自动兜底")
    live = section(ed, "static int nav_add_live(P g, const V3* p)", "static int nav_apply_core")
    check("idx = nav_add_node(g, p);" in live, "先借空槽位")
    check("if (idx >= 0) return idx;" in live, "借到就返回")
    check("g_nedKeep = 1" not in live, "借不到时不再改 keep 标记")

    print("[2] toast 两种语义（黄字「提示下一步」已按用户要求删掉）")
    check("COL_TOAST_OK  = { 0.35f, 0.95f, 0.45f" in ed, "成功 = 亮绿")
    check("COL_TOAST    = { 1.00f, 0.23f, 0.16f" in ed, "禁止 = 亮红")
    check("COL_TOAST_SH  = { 0.00f, 0.00f, 0.00f" in ed, "黑色影子")
    check("#define TOAST_MS_OK  1600" in ed and "#define TOAST_MS_ERR 3000" in ed,
          "成功短一点、禁止停久一点")
    check("toast_info" not in ed and "COL_TOAST_INF" not in ed and "TOAST_MS_INF" not in ed,
          "没有黄色「提示下一步」那一套了")
    for fn, args in (("toast_ok", "COL_TOAST_OK, TOAST_MS_OK"),
                     ("toast_bad", "&COL_TOAST, TOAST_MS_ERR")):
        body = section(ed, "static void %s(const char* fmt, ...) {" % fn, "}")
        check(args in body, "%s 用对颜色/时长" % fn)
    for gone, label in (("已选 A #%d (%.1f", "「已选 A，对准下一个点」"),
                        ("当前类型：%s —— 小键盘5 放置", "「当前类型」"),
                        ("连线方向：%s —— 准星对准起点", "「连线方向」"),
                        ("起跳点已锁定 #%d：对准落点", "「起跳点已锁定」")):
        check(gone not in ed, "不再弹%s" % label)

    print("[3] 每个菜单动作都有反馈")
    def n_toasts(fn_start, fn_end, need, label):
        body = section(ed, fn_start, fn_end)
        cnt = body.count("toast_ok(") + body.count("toast_bad(") + body.count("toast_info(")
        check(cnt >= need, "%s：%d 处提示（>=%d）" % (label, cnt, need))
        return body

    body = n_toasts("static void nav_add_here(void)", "static void nav_del_here", 3, "普通路点")
    check("toast_ok(" in body, "普通路点：成功也提示")
    body = n_toasts("static void wp_place(void)", "/* ---- 测试包", 14, "放置（跳点/蹲守/守卫区/标签/出生点）")
    for kw, label in (("跳点已建", "跳点成功"), ("蹲守点已放", "蹲守点"),
                      ("守卫区已建", "守卫区"), ("守卫点已加到守卫区", "守卫点"),
                      ("标签区已建", "标签区"), ("出生点 BL 已加", "出生点 BL"),
                      ("出生点 GR 已加", "出生点 GR"),
                      ("出生点 中立 已加", "出生点 中立")):
        check(kw in body, "放置反馈包含「%s」" % label)

    body = n_toasts("static void nav_link_one(void)", "static void make_tag", 4, "连边 / 选 A")
    check("已连边" in body, "连边成功提示")
    body = n_toasts("static void nav_unlink_here(void)", "static void nav_ground_here", 2, "断边")
    check("已断开" in body, "断边成功提示")
    body = n_toasts("static void nav_del_here(void)", "/* 2026-11-26 用户要求：菜单里的", 2, "删路点")
    check("已删路点" in body, "删路点成功提示")
    body = n_toasts("static void nav_ground_here(void)", "static void nav_link_one", 4, "贴地")
    check("已贴地" in body, "贴地成功提示")
    body = n_toasts("static int delete_nearest_of(int want) {", "static int delete_nearest(void)", 4, "删点位/删区域")
    check("已删%s" in body, "删标记成功提示")
    body = n_toasts("static int editor_spawn_delete(int team) {", "static void spawn_restore_orig", 5, "删出生点")
    check("已删出生点" in body, "删出生点成功提示")
    body = n_toasts("static void nav_undo(void)", "static void nav_redo(void)", 2, "撤销（点图）")
    check("已撤销" in body, "撤销成功提示")
    body = n_toasts("static void nav_redo(void)", "static void ed_undo(void)", 2, "重做（点图）")
    check("已重做" in body, "重做成功提示")
    body = n_toasts("static void mke_undo(void)", "static void mke_redo(void)", 2, "撤销（标记）")
    check("已撤销" in body, "标记撤销提示")
    body = n_toasts("static void mke_redo(void)", "static void ed_undo(void)", 2, "重做（标记）")
    check("已重做" in body, "标记重做提示")
    body = n_toasts("void editor_save_all(void) {", "static void nav_edit_load", 4, "保存")
    check("已保存" in body, "保存成功提示")
    body = n_toasts("static void menu_activate(void) {", "static void menu_confirm(void) {", 1, "菜单（守卫区工具）")
    check("入口 / 逃跑点还没接线" not in body and "入口 / 逃跑点还没接线" not in ed,
          "旧的「入口 / 逃跑点还没接线」占位已删除（2026-11-28 已接线）")
    body = n_toasts("static void menu_confirm(void) {", "static int menu_sys_key", 1, "确认键（删除页未选类型）")
    check("先选删除类型" in body, "删除页没选类型也有提示")

    print("[3b] 出生点三个数组都能改（2026-11-27：个人竞技全员走 Neutral）")
    check("#define SPAWN_TEAMS 3" in ed, "SPAWN_TEAMS = 3")
    check("SPAWN_OFF[SPAWN_TEAMS] = { 0x10, 0x14, 0x18 }" in ed,
          "字段偏移 0x10/0x14/0x18（SP_BL / SP_GR / SP_Netural）")
    check('x_class_get_field_from_name(g_mmCls, "SPID_Netural")' in ed,
          "取到 SPID_Netural 静态计数器")
    eff = section(ed, "static int spawn_effective(int team", "static int spawn_count(int team)")
    loop_add = eff.find("for (i = 0; i < g_spawnAddN[team] && n < cap")
    loop_orig = eff.find("for (j = 0; j < g_spawnOrigN[team] && n < cap")
    check(loop_add >= 0 and loop_orig >= 0 and loop_add < loop_orig,
          "新增点排在原生点前面（否则要轮完一遍原生点才轮到，看起来像没用）")
    check("static void spawn_clear_ids(void)" in ed and "spawn_clear_ids();" in ed,
          "写回后清 SPID_*（下一次取点 = 第 1 个新增点）")
    check("if (!g_inited || g_sceneAge < 1) return;" in ed,
          "进图第 1 个心跳就套出生点（抢在死亡重生 2 s 之前）")
    check("MT_SPAWN_NT" in ed and "editor_spawn_delete(2)" in ed, "中立出生点也能删")

    print("[3c] 出生点高度 = 游戏原生高度（2026-11-27：以前 +0.05 太低，重生穿地板）")
    gap = section(ed, "static float spawn_height_gap(void)", "static void spawn_fix_heights_all(void)")
    check("g_spawnOrig[team][i].p" in gap and "ground_below(" in gap,
          "从本图原生出生点反推「地面 + 高度」")
    check("g_spawnGap > 0.02f && g_spawnGap < 3.0f" in gap, "离谱值有兜底")
    fix = section(ed, "static void spawn_fix_height(V3* p)", "static void spawn_fix_heights_all(void)")
    check("want = g.y + gap;" in fix, "新增点抬到地面 + 原生高度")
    addp = section(ed, "static int spawn_add_point(int team, V3 p, float yaw)", "static int editor_spawn_delete(int team)")
    check("spawn_fix_height(&p);" in addp, "加点时先对齐高度再存")
    apply_body = section(ed, "static int spawn_apply(void)", "static void spawn_tick(void)")
    check("spawn_fix_heights_all();" in apply_body, "进图后把旧文件的低点一起改正")
    ghost = section(ed, "static void ghost_tick(void)", "static void wp_place(void) {")
    check("ground_below(p, 1.0f, 40.0f, &g)" in ghost and "MT_SPAWN" in ghost,
          "预览框也按原生高度摆（别骗人）")

    print("[3d] 开局抢跑：人机第一次出生也用改过的点（2026-11-27）")
    early = section(ed, "static void spawn_early_tick(void)", "void editor_spawn_tick(void)")
    check("mm != g_spawnEarlyMm" in early, "按 MapManager 实例变化触发（不等 navfix 场景通知）")
    check("spawn_early_load()" in early and "spawn_apply();" in early,
          "只读 spawn 行 + 立刻写回数组")
    check("if (!ready) return;" in early, "Awake 还没拆数组时不动")
    check("void editor_spawn_tick(void)" in ed, "对外提供高频入口")
    nv = read(os.path.join("src", "navfix.c"))
    check("editor_spawn_tick();" in nv, "hi-res WM_TIMER（≈15 ms）里调用")
    check(ed.count("spawn_early_tick();") >= 2, "4 Hz 的 editor_tick 也调（兜底）")
    check("spawn_parse_line(line)" in ed, "markers 的 spawn 解析只有一份（load_file 与抢跑共用）")

    print("[3f] 取点钩子：整函数替换 MapManager.GetSpawnPoint（2026-11-27 第四轮）")
    check("#define R_GET_SPAWN 0xAEB6E0" in ed, "目标 RVA 0xAEB6E0")
    hook = section(ed, "static int spawn_hook_install(void)", "/* Ctrl+7")
    check("0x55 && p[1] == 0x8B && p[2] == 0xEC" in hook,
          "打补丁前校验函数开头（版本不对就不动）")
    check("p[0] = 0xE9" in hook and "VirtualProtect" in hook and "FlushInstructionCache" in hook,
          "入口 5 字节 E9 + 改页保护 + 刷指令缓存")
    getbody = section(ed, "static void* __cdecl spawn_hook_get", "/* 打补丁")
    check("return ret;" in getbody, "把 sret 缓冲区指针放在 EAX 返回（调用方 [eax] 取结果）")
    check("hook_sync();" in getbody and "hook_points(" in getbody, "先对齐本图数据再取点")
    sync = section(ed, "static void hook_sync(void)", "/* 取 team 的生效点")
    check("mm == g_hookMm" in sync and "spawn_early_load();" in sync,
          "MapManager 换实例就丢旧图数据、重读本图 markers")
    check("g_hookId[team] = 0;" in section(ed, "static int hook_points(int team", "static void* __cdecl spawn_hook_get"),
          "数组被游戏重建时轮转一起归零")
    check("void spawn_preload(void)" in ed and "spawn_preload();" in ed,
          "启动时预读 markers 的 spawn 行（第一波出生比任何 tick 早）")
    check('cfg_bool("spawn_hook", 1)' in ed, "有 spawn_hook 开关（出事可整体关掉）")
    init = section(ed, "static int ed_init(void)", "elog(\"init: exports ok")
    check("spawn_hook_install();" in ed, "安装点存在")
    check(init == "" or "spawn_hook_install();" not in init, "不在 ed_init 前段装（g_ga 未就绪）")
    check(ed.count("spawn_hook_install();") >= 2, "ed_init 末尾 + 早 tick 兜底重试都在调")
    check("if (!g_hookOn) spawn_hook_install();" in ed, "早 tick 每拍兜底重试（装上前不会静默）")


    print("[4] toast 的样子")
    tb = section(ed, "static void toast_build(P canvasTr)", "/* 弹一条提示")
    check(tb.count("0.5f, 0.5f, 0.5f, 0.5f") >= 2, "两个 Text 锚在屏幕中心")
    check("TOAST_Y" in tb, "Y 上移，不压准星")
    check("R_TEXT_ALIGN))(g_toast, 4, 0)" in tb, "正文居中（MiddleCenter）")
    check("R_SETACTIVE))(g_toastGo, 0, 0)" in tb, "默认隐藏")
    tv = section(ed, "static void toast_v(const COL* col", "/* 两种语义")
    check("overlay_reset();" in tv and "overlay_refresh();" in tv, "换图后对象没了会重建")
    check("now - lastMs < 500" in tv, "同一条消息连按不重复闪")
    check("R_GRAPHIC_COL))(g_toast, *col, 0)" in tv, "每次按语义换颜色")
    tick = section(ed, "static void toast_tick(void)", "/* ---- marker store")
    check("R_SETACTIVE))(g_toastGo, 0, 0)" in tick, "到点隐藏")
    check("toast_tick();" in ed, "主 tick 里驱动 toast_tick")

    print()
    if FAIL:
        print("FAILED %d check(s):" % len(FAIL))
        for f in FAIL:
            print("  - " + f)
        raise SystemExit(1)
    print("OK: every waypoint-menu action reports success (green) or refusal (red) on screen")


if __name__ == "__main__":
    main()
