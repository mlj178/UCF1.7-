"""子弹穿墙/弹体穿墙 —— 2.7 功能卡片。

本卡只有总开关（manifest card_type=simple），这里在默认卡片下方补一行
「联动提示」，把"现在到底会不会穿墙"直接写清楚：

    开关开启  -> 子弹穿墙 + 本地玩家投射物（火箭筒 / 榴弹 / 手雷 / 技能弹）穿墙，
                 与「开火直伤/弹体追踪」开不开无关（弹体穿墙是本功能自己的 Hook）。
    追踪开着但本功能关 -> 追踪弹体撞墙即爆（原版行为）。
    都没开        -> 提示同时开启的效果。

提示状态以"用户看到的开关"为准（开关可见状态与框架启用状态同时成立才算开启）：
未连接游戏时框架会拒绝改启用状态，若只看框架状态，开关已经被点灭了提示却还停在绿色。
提示只用于显示，不参与任何穿墙判定。
"""

import customtkinter as ctk

DD_FEATURE_ID = "direct_damage"
DD_CARD_TITLE = "开火直伤/弹体追踪"
HINT_REFRESH_MS = 500
HINT_COLORS = {"ok": "#4ade80", "warn": "#fbbf24", "idle": "#94a3b8"}


def _iter_descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from _iter_descendants(child)


def _find_card_switch(parent, title):
    """在同一 tab 的滚动容器里，按卡片标题找到该卡片的总开关。"""
    target = "".join(str(title).split())
    try:
        for card in parent.winfo_children():
            labeled = [
                widget
                for widget in _iter_descendants(card)
                if isinstance(widget, ctk.CTkLabel)
                and "".join(str(widget.cget("text")).split()) == target
            ]
            if not labeled:
                continue
            for scope in (labeled[0].master, card):
                for widget in _iter_descendants(scope):
                    if isinstance(widget, ctk.CTkSwitch):
                        return widget
    except Exception:
        return None
    return None


def _visible_enabled(switch, callbacks, feature_id):
    """开关可见状态与框架启用状态同时成立才算开启；取不到部件时退回框架状态。"""
    enabled = bool(callbacks["is_enabled"](feature_id))
    try:
        if switch is not None and switch.winfo_exists():
            return enabled and bool(switch.get())
    except Exception:
        pass
    return enabled


def _tracking_from(config, enabled):
    """追踪弹体是否真的会发射：功能启用 + 追踪相关配置打开。"""
    if not enabled:
        return False
    if not bool(config.get("enable_homing", True)):
        return False
    return bool(
        config.get("enable_explosives", True)
        or config.get("enable_skill_projectiles", True)
    )


def _link_hint(tracking, wall_on):
    """返回 (提示文案, 颜色类型)。"""
    if wall_on:
        return "✓ 已开启：子弹与本地投射物（火箭筒 / 榴弹 / 手雷 / 技能弹）都能穿墙。", "ok"
    if tracking:
        return "⚠ 「开火直伤/弹体追踪」已开启追踪，本功能关闭 → 追踪弹体撞墙即爆。", "warn"
    return "开启后子弹可穿墙；本地投射物（火箭筒 / 榴弹 / 手雷 / 技能弹）也一起穿墙。", "idle"


def _bind_link_hint(hint, parent, switch, callbacks, feature_id):
    """固定间隔刷新提示；返回可立即刷新一次的 refresh（供开关点击时调用）。"""
    def resolve():
        dd_switch = _find_card_switch(parent, DD_CARD_TITLE)
        wall_on = _visible_enabled(switch, callbacks, feature_id)
        dd_on = _visible_enabled(dd_switch, callbacks, DD_FEATURE_ID)
        config = callbacks["get_config"](DD_FEATURE_ID) or {}
        return _tracking_from(config, dd_on), wall_on

    def refresh():
        tracking, wall_on = resolve()
        text, kind = _link_hint(tracking, wall_on)
        hint.configure(text=text, text_color=HINT_COLORS[kind])

    def tick():
        try:
            if not hint.winfo_exists():
                return
            refresh()
        except Exception:
            pass
        try:
            hint.after(HINT_REFRESH_MS, tick)
        except Exception:
            return

    refresh()
    hint.after(HINT_REFRESH_MS, tick)
    return refresh


def build_card(scroll, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]

    frame, switch, label = card_builder.make_feature_card(scroll, row, col, colspan, manifest)

    hint = ctk.CTkLabel(
        frame,
        text="",
        font=("Microsoft YaHei", 11),
        text_color=HINT_COLORS["idle"],
        wraplength=280 * colspan,
        justify="left",
        anchor="w",
    )
    hint.pack(fill="x", padx=10, pady=(0, 6))

    refresh = _bind_link_hint(hint, scroll, switch, callbacks, feature_id)
    switch.configure(command=lambda: (callbacks["toggle"](feature_id), refresh()))

    return {
        manifest.get("ui_handles", {}).get("switch", f"{feature_id}_switch"): switch,
        f"{feature_id}_label": label,
    }
