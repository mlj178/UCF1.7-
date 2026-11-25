#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""静态自检：「删除本图草稿」入口（2026-11-25）。

一条入口串三处，缺一处就断：
    navdata.py   pack rm + PACK_TRASH（默认整份挪 archive\pack_trash\，--hard 才真删）
    ui/packs.py  delete_draft()：游戏守卫 -> 确认弹窗 -> run_navdata(["pack", "rm", ...])
    tabs/waypoint.py  本图草稿卡片右侧的红色按钮；有草稿才亮、没草稿置灰

和「重置本图草稿」的区别必须一直在：重置 = 清空内容（草稿还在），删除 = 整份挪走。
只读源码，不需要游戏 / 窗口 / 数据。

跑法：python app/tests/test_draft_delete.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
while not os.path.isfile(os.path.join(ROOT, ".ucfroot")) and os.path.dirname(ROOT) != ROOT:
    ROOT = os.path.dirname(ROOT)


def read(*parts):
    with open(os.path.join(ROOT, *parts), "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def main():
    nav = read("app", "core", "navdata.py")
    packs = read("app", "ui", "packs.py")
    way = read("app", "tabs", "waypoint.py")
    kit = read("app", "ui", "kit.py")

    # ---- navdata：pack rm ----
    assert "PACK_TRASH" in nav and "pack_trash" in nav, "navdata.py 缺删草稿的回收目录"
    assert "def pack_store_remove" in nav, "navdata.py 缺 pack_store_remove"
    assert "def cmd_pack_rm" in nav, "navdata.py 缺 cmd_pack_rm"
    assert '"rm", help=' in nav, "navdata.py 没注册 pack rm 子命令"
    assert "--hard" in nav, "navdata.py pack rm 丢了 --hard"
    assert "shutil.move(pdir, dst)" in nav, "pack rm 不再整份挪目录（改成逐个删文件？）"
    assert "final_delete_dir(pdir)" in nav, "pack rm 的 --hard 不再真删目录"
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
    assert "pack_trash" in body, "确认弹窗没说清整份挪到 archive\\pack_trash\\"
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
    assert "整份挪到 archive" in way, "卡片说明没写草稿整份挪走（成品不动）"
    for state in ('configure(state="normal", fg_color="#8a1c1c")',
                  'configure(state="disabled", fg_color="#3a3f47")'):
        assert state in way, "按钮状态没跟着草稿有无变：%s" % state
    # 重置还在，两个动作不能混
    assert "重置本图草稿" in way and "clear_pack_map" in way, "「重置本图草稿」被删了？"
    assert "「重置本图草稿」只清内容" in way, "卡片里没解释重置 / 删除的区别"

    print("OK: 删除本图草稿入口（pack rm -> archive\\pack_trash\\，成品不动；有/无草稿两态）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
