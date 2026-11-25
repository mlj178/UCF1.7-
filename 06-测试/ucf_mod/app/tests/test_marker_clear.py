#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""静态自检：本图编辑标记（守卫区 / 守卫点 / 蹲守点 / 标签 / 出生点）（2026-11-25）。

用户反馈「草稿里删干净了，守卫区还在」——原因：标记存在 markers\<图>\markers.txt，
不在草稿 txt 里，删草稿不会带走。界面要看得见（本图标记：守卫区 9），要能给出口（清空本图标记）。

链路：ui/packs.py（读/算/清，清 = 挪到 archive\markers_trash）
      tabs/waypoint.py（本图草稿卡片那行 + 按钮 + 两态）
      删草稿确认框要提醒「标记不随草稿删」。
只读源码；不碰真实 markers。

跑法：python app/tests/test_marker_clear.py
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
    packs = read("app", "ui", "packs.py")
    way = read("app", "tabs", "waypoint.py")
    env = read("app", "ui", "env.py")

    # ---- 数据侧：标记是单独一份文件 ----
    assert "MARKER_LABELS" in packs and "守卫区" in packs and "蹲守点" in packs, \
        "packs.py 缺标记中文名表"
    assert "from ui.env import" in packs and "MARKERS" in packs, "packs.py 没从 ui.env 拿 MARKERS"
    assert "MARKERS = P.MARKERS" in env, "ui/env.py 丢了 MARKERS"
    body = packs[packs.index("def marker_path"):packs.index("def resolve_pack_id")]
    assert "markers.txt" in body and "MARKERS" in body, "marker_path 不再指向 markers\\<图>\\markers.txt"
    assert "def marker_counts" in body and 'kind == "spawndel"' in body, \
        "marker_counts 不再按行统计（spawndel 也要算出生点改动）"
    assert "def marker_summary" in body, "packs.py 缺 marker_summary"
    assert "def clear_markers" in body, "packs.py 缺 clear_markers"
    assert "shutil.move(p, os.path.join(dst_dir, \"markers.txt\"))" in body, \
        "clear_markers 不是整份挪走"
    assert "markers_trash" in body, "clear_markers 没落到 archive\\markers_trash\\"
    assert "os.remove(p)" not in body and "shutil.rmtree" not in body, \
        "clear_markers 在真删（应该是挪到 archive）"
    assert "confirm_danger(" in body and "_guard_game(" in body, \
        "清空标记没走危险确认框 / 没问游戏开着"

    # ---- 界面侧：一行数字 + 一个按钮 + 两态 ----
    assert "self.lbl_markers" in way, "waypoint.py 缺「本图标记」那行"
    assert "self.btn_clear_markers" in way, "waypoint.py 缺「清空本图标记」按钮"
    assert 'text="清空本图标记"' in way, "按钮文案不是「清空本图标记」"
    assert "command=self.clear_markers" in way, "按钮没接到 clear_markers"
    assert "本图标记：%s" in way, "卡片没写「本图标记：N」"
    assert "不在草稿" in way and "默认连它们一起清" in way, \
        "卡片没写「删草稿默认连标记一起清」（用户就是这么误会的）"
    assert 'configure(state="disabled", fg_color="#3a3f47")' in way, \
        "没有标记时按钮应置灰"
    # 删草稿确认框要提醒标记还在
    delb = packs[packs.index("def delete_draft"):packs.index("def default_pack_name")]
    assert "marker_summary" in delb and "不在草稿里" in delb, \
        "删草稿的确认框没解释「标记在 markers\\，不在草稿里」"
    assert "同时清空本图标记" in delb, "删草稿没提供「连标记一起清」的勾选"
    # 说明文字要解释两种文件
    assert "markers.txt" in way and "不在草稿 txt 里" in way, "卡片说明没写标记文件位置"

    print("OK: 本图标记（守卫区/守卫点/蹲守点/标签/出生点）可见 + 可清空（挪 archive\\markers_trash）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
