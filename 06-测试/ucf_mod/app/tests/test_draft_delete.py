#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：「删除本图草稿」只删草稿，不删这张图（2026-11-25 建，2026-11-27 补）。

一条入口串三处，缺一处就断：
    navdata.py   pack rm + PACK_TRASH（草稿三件挪 archive\pack_trash\，--hard 才真删）
    ui/packs.py  delete_draft()：游戏守卫 -> 确认弹窗 -> run_navdata(["pack", "rm", ...])
    tabs/waypoint.py  本图草稿卡片右侧的红色按钮；有草稿才亮、没草稿置灰

和「重置本图草稿」的区别必须一直在：重置 = 清空内容（草稿还在），删除 = 回到「还没有草稿」。

**2026-11-27 事故**：一图一夹以后草稿和图数据在同一个文件夹里，pack rm 还在「整份目录挪走」，
运输船的 map.json 跟着进了回收站 —— 控制台地图下拉里这张图直接消失（用户问「地图怎么没了」）。
所以这个自检除了读源码，还会在临时目录里真跑一遍：删完草稿，map.json / 可走面 / 标记 / 成品必须一件不少。

跑法：python app/tests/test_draft_delete.py
"""
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
while not os.path.isfile(os.path.join(ROOT, ".ucfroot")) and os.path.dirname(ROOT) != ROOT:
    ROOT = os.path.dirname(ROOT)


def read(*parts):
    with open(os.path.join(ROOT, *parts), "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def static_checks():
    nav = read("app", "core", "navdata.py")
    packs = read("app", "ui", "packs.py")
    way = read("app", "tabs", "waypoint.py")
    kit = read("app", "ui", "kit.py")

    # ---- navdata：pack rm 只搬草稿 ----
    assert "PACK_TRASH" in nav and "pack_trash" in nav, "navdata.py 缺删草稿的回收目录"
    assert "def pack_draft_files" in nav, "navdata.py 缺「哪些文件算草稿」"
    draft = nav[nav.index("def pack_draft_files"):nav.index("def is_map_folder")]
    for fn in ("manifest.json", "nogen.txt"):
        assert fn in draft, "pack_draft_files 漏了 %s" % fn
    assert "map.json" not in draft.split('"""')[-1], \
        "草稿清单里混进了 map.json（它是图数据，删草稿不许动它）"
    assert "def is_map_folder" in nav, "navdata.py 缺「这是不是图文件夹」的判断"
    assert "def pack_store_remove" in nav, "navdata.py 缺 pack_store_remove"
    assert "def cmd_pack_rm" in nav, "navdata.py 缺 cmd_pack_rm"
    assert '"rm", help=' in nav, "navdata.py 没注册 pack rm 子命令"
    assert "--hard" in nav, "navdata.py pack rm 丢了 --hard"
    rm = nav[nav.index("def pack_store_remove"):nav.index("def cmd_pack_rm")]
    assert "pack_draft_files(pdir)" in rm, "pack rm 不再按草稿清单搬文件"
    assert "is_map_folder(pdir)" in rm, "pack rm 不再区分「图文件夹」和「老布局的包目录」"
    assert "for p in draft:" in rm, "pack rm 没有逐个搬草稿文件"
    assert rm.count("shutil.move(") >= 1 and "shutil.move(pdir, dst)" in rm, \
        "老布局（没有点图的包目录）还得整份挪，这条兼容不能丢"
    assert "_pack_trash_dst" in rm, "pack rm 没走回收站目录的公共函数"
    # 成品不能被误删：rm 只处理 packs\<图>\
    assert "final_store_remove" not in nav[nav.index("def cmd_pack_rm"):nav.index("def cmd_final_rm")], \
        "pack rm 里混进了删成品的调用（成品该走 final rm）"

    # ---- packs.py：按钮背后那一步 ----
    assert "def delete_draft" in packs, "packs.py 缺 delete_draft"
    body = packs[packs.index("def delete_draft"):packs.index("def default_pack_name")]
    assert 'run_navdata(["pack", "rm", folder], "删除本图草稿")' in body, \
        "delete_draft 不再调 navdata.py pack rm"
    assert "_guard_game(" in body, "delete_draft 没问「游戏开着」"
    assert "confirm_danger(" in body, "delete_draft 没走危险确认框"
    assert "messagebox.askyesno" not in body, \
        "删草稿又用回 askyesno（Windows 上关窗会返回「是」）"
    assert "成品里已发布的那份不动" in body, "确认弹窗没说清成品不动"
    assert "pack_trash" in body, "确认弹窗没说清草稿挪到 archive\\pack_trash\\"
    assert "原地不动" in body, "确认弹窗没写「图数据原地不动」（2026-11-27 就是这么丢的 map.json）"
    assert "checkbox_text=" in body, "删草稿没给「同时清空本图标记」的勾选"
    assert "self.clear_markers(ask=False)" in body, "勾选了却没清标记"
    assert "checkbox_checked=True" in body, "「同时清空标记」默认不勾（用户要的是删干净）"
    assert "草稿没删" in body, "标记没清掉时不该继续删草稿"

    # ---- 危险确认框本身：× / Esc 必须是「否」 ----
    assert "def confirm_danger" in kit, "kit.py 缺 confirm_danger"
    dlg = kit[kit.index("def confirm_danger"):]
    assert 'protocol("WM_DELETE_WINDOW", lambda: close(False))' in dlg, \
        "危险确认框的标题栏 × 没绑成「取消」"
    assert 'bind("<Escape>", lambda _e: close(False))' in dlg, "危险确认框 Esc 没绑成「取消」"
    assert "btn_cancel.focus_set()" in dlg, "危险确认框默认焦点不在「取消」"
    assert "checkbox_text" in dlg and "out[\"checked\"]" in dlg, \
        "confirm_danger 不支持「顺带清标记」勾选框"

    # ---- waypoint.py：入口长什么样 ----
    assert "self.btn_delete_draft" in way, "waypoint.py 缺「删除本图草稿」按钮"
    assert 'text="删除本图草稿"' in way, "按钮文案不是「删除本图草稿」"
    assert 'fg_color="#8a1c1c"' in way, "删除按钮不是危险色"
    assert 'self.btn_delete_draft.pack(side="right")' in way, "删除按钮没放在右侧危险区"
    assert "只把草稿三件" in way, "卡片说明没写「删除只搬草稿三件」（图数据不动）"
    for state in ('configure(state="normal", fg_color="#8a1c1c")',
                  'configure(state="disabled", fg_color="#3a3f47")'):
        assert state in way, "按钮状态没跟着草稿有无变：%s" % state
    # 重置还在，两个动作不能混
    assert "重置本图草稿" in way and "clear_pack_map" in way, "「重置本图草稿」被删了？"
    assert "「重置本图草稿」只清内容" in way, "卡片里没解释重置 / 删除的区别"


def _write(path, text=""):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def functional_check():
    r"""在临时目录里真跑 pack rm：草稿挪走，map.json / 可走面 / 标记 / 成品一件不少。"""
    tmp = tempfile.mkdtemp(prefix="ucf_packrm_")
    root = os.path.join(tmp, "maps")
    trash = os.path.join(tmp, "pack_trash")
    folder_name = "01_TransportShip运输船"
    fp = "n786-57a46e3465c847cb"
    folder = os.path.join(root, folder_name)
    try:
        # 一张「完整的图」：点图 + 可走面 + 标记 + 冻结副本 + 成品 + 草稿三件 + 草稿备份
        _write(os.path.join(folder, "map.json"), '{"map": {"level": "level1"}}')
        _write(os.path.join(folder, "navmesh.bin"), "nm")
        _write(os.path.join(folder, "markers.txt"), "spawn 0 1 2 3 4\n")
        _write(os.path.join(folder, "native", "map.json"), '{"map": {"level": "level1"}}')
        _write(os.path.join(folder, "final", fp + ".txt"), "# final\n")
        _write(os.path.join(folder, "manifest.json"), '{"fp": "%s"}' % fp)
        _write(os.path.join(folder, fp + ".txt"), "# ucf-navedit v1 fp=%s\ngrow\n" % fp)
        _write(os.path.join(folder, "nogen.txt"), "")
        _write(os.path.join(folder, fp + ".txt.bak-rec-20261125-093759"), "# bak\n")

        os.environ["UCF_PACK_DIR"] = root
        os.environ["UCF_PACK_TRASH"] = trash
        core = os.path.join(ROOT, "app", "core")
        if core not in sys.path:
            sys.path.insert(0, core)
        import navdata as nd                                    # noqa: E402
        assert os.path.abspath(nd.packs_root()) == os.path.abspath(root), \
            "自检没指到临时目录（UCF_PACK_DIR 没生效），不往下跑"
        assert nd.pack_ids() == [folder_name], "临时图文件夹没被认成「有草稿的图」"

        pdir, where, node, edge = nd.pack_store_remove(folder_name)
        assert os.path.abspath(pdir) == os.path.abspath(folder), "删的不是这张图的目录：%s" % pdir
        # 1) 草稿三件 + 备份进了回收站
        moved = sorted(os.listdir(where))
        for fn in ("manifest.json", "nogen.txt", fp + ".txt",
                   fp + ".txt.bak-rec-20261125-093759"):
            assert fn in moved, "草稿文件没进回收站：%s（回收站里：%s）" % (fn, moved)
        # 2) 图文件夹里草稿没了，图数据一件不少
        for fn in ("map.json", "navmesh.bin", "markers.txt",
                   os.path.join("native", "map.json"), os.path.join("final", fp + ".txt")):
            assert os.path.isfile(os.path.join(folder, fn)), "删草稿把图数据也删了：%s" % fn
        for fn in ("manifest.json", "nogen.txt", fp + ".txt"):
            assert not os.path.isfile(os.path.join(folder, fn)), "草稿文件还留在图文件夹里：%s" % fn
        # 3) 这张图「还没有草稿」，但仍然是一张能选的图
        assert nd.pack_ids() == [], "删完草稿还把这张图算成「有草稿」"
        assert nd.is_map_folder(folder), "删完草稿这张图就不算图文件夹了（下拉会消失）"

        # 4) 再删一次：这张图已经没有草稿了，要明确报错而不是乱搬
        try:
            nd.pack_store_remove(folder_name)
        except SystemExit:
            pass
        else:
            raise AssertionError("没有草稿时 pack rm 居然成功了（应该报「这张图还没有草稿」）")
        assert os.path.isfile(os.path.join(folder, "map.json")), "报错那一次把 map.json 弄丢了"

        # 5) --hard：只真删草稿，图还在
        _write(os.path.join(folder, "manifest.json"), '{"fp": "%s"}' % fp)
        _write(os.path.join(folder, fp + ".txt"), "grow\n")
        nd.pack_store_remove(folder_name, hard=True)
        assert not os.path.isfile(os.path.join(folder, fp + ".txt")), "--hard 没删草稿"
        assert os.path.isfile(os.path.join(folder, "map.json")), "--hard 把图数据一起删了"
        assert os.path.isdir(folder), "--hard 把整个图文件夹删了"

        # 6) 老布局（packs\<图>\<包>\，里面没有点图）：还是整份挪，不能留在原地
        legacy = os.path.join(root, "09_Legacy", "old_pack")
        _write(os.path.join(legacy, "manifest.json"), '{"fp": "%s"}' % fp)
        _write(os.path.join(legacy, fp + ".txt"), "grow\n")
        _pdir, _where, _n, _e = nd.pack_store_remove("09_Legacy/old_pack")
        assert not os.path.isdir(legacy), "老布局的包目录没被整份挪走"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    static_checks()
    functional_check()
    print("OK: 删除本图草稿只搬草稿三件（图数据 / 成品不动）；有 / 无草稿两态；--hard 只删草稿")
    return 0


if __name__ == "__main__":
    sys.exit(main())
