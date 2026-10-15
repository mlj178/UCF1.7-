"""开火直伤/弹体追踪 —— 2.7 功能卡片。

卡片结构（从上到下）：
    标题 + 总开关
    说明文字
    4 个子开关：常规枪械射线接管 / 射线接管总开关 / 榴弹手雷RPG 追踪 / 特殊技能弹 追踪

C 路线边界（2026-10-16 起）：
    本功能**不注入伤害、不处理死亡与复活**。常规枪械只把这一发的射线方向掰到目标身上，
    命中判定 / 伤害 / 死亡广播 / 复活调度全部由游戏原版完成；爆炸类 / 技能弹只做弹体追踪。
    旧版的自定义伤害 + 死亡兜底（death_fix_*）已移除，
    备份见 04-正式发行版/_备份_40_direct_damage_注入版_2.7/。
    联动提示行（A 方案）：提示追踪弹体是否会被墙挡住，可一键开启「子弹穿墙/弹体穿墙」

为什么不用默认卡片（PluginFeaturePage._build_default_card）：
    默认卡片只渲染"第一个 slider"加一个总开关，而本功能需要 4 个
    action=setConfig 的子开关，所以这里自己画卡片。

子开关句柄为什么要包一层 _SyncedSwitchVar：
    框架的 App._sync_plugin_controls_from_config 对"带 key 的 switch 控件"会调用
    handle.set(bool(config[key]))，而原生 CTkSwitch 只有 select()/deselect()、没有 set()。
    包一层提供 set(bool)/get()，同时把用户点击转到 callbacks["set_config"]。
句柄名必须和 manifest.ui_handles 里的 <key>_var 一致（框架按这个名字 getattr）。
"""

import customtkinter as ctk

WALL_FEATURE_ID = "29_bullet_wall_penetration"
WALL_CARD_TITLE = "子弹穿墙/弹体穿墙"
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
    """返回 (提示文案, 颜色类型, 是否显示「一键开启」按钮)。"""
    if tracking:
        if wall_on:
            return "✓ 已联动：追踪弹体可穿墙命中墙后目标。", "ok", False
        return (
            "⚠ 追踪弹体目前会被墙体阻挡（撞墙即爆）。建议同时开启「子弹穿墙/弹体穿墙」。",
            "warn",
            True,
        )
    return "追踪关闭时两者无联动；开启追踪后，与「子弹穿墙/弹体穿墙」同时开启即可穿墙。", "idle", False


def _bind_link_hint(hint, button, callbacks, resolve):
    """固定间隔刷新提示行；返回可立即刷新一次的 refresh（供开关点击时调用）。

    状态变化来自本卡各开关或另一张卡片，每轮都重新解析，不依赖事件。
    """
    shown = {"button": None, "state": None}

    def refresh():
        tracking, wall_on = resolve()
        text, kind, show_button = _link_hint(tracking, wall_on)
        hint.configure(text=text, text_color=HINT_COLORS[kind])
        if show_button != shown["button"]:
            shown["button"] = show_button
            if show_button:
                button.pack(side="right", padx=(6, 0))
            else:
                button.pack_forget()
        if show_button:
            state = "normal" if callbacks["is_connected"]() else "disabled"
            if state != shown["state"]:
                shown["state"] = state
                button.configure(state=state)

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


class _SyncedSwitchVar:
    """把 CTkSwitch 适配成框架可用的句柄：提供 set(bool) / get()。"""

    def __init__(self, switch, initial, on_change):
        self._switch = switch
        self._value = bool(initial)
        self._on_change = on_change
        self._syncing = False

    def get(self):
        return self._value

    def set(self, value):
        """框架同步配置时调用：只改显示状态，不再回写 config（避免来回抖动）。"""
        self._syncing = True
        try:
            self._value = bool(value)
            if self._value:
                self._switch.select()
            else:
                self._switch.deselect()
        finally:
            self._syncing = False

    def on_click(self):
        """用户点击子开关：翻转自己的镜像值并回写 config。"""
        if self._syncing:
            return
        self._value = not self._value
        self._on_change(self._value)


def _config_switches(manifest):
    """取所有 action=setConfig 的 switch 控件（即"带 key 的子开关"）。"""
    return [
        control
        for control in manifest.get("controls", [])
        if control.get("type") == "switch" and control.get("key")
    ]


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    handles = manifest.get("ui_handles", {})
    config = manifest.get("config") or {}

    frame = ctk.CTkFrame(
        parent,
        corner_radius=6,
        fg_color="transparent",
        border_width=1,
        border_color="#4b5563",
    )
    frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)

    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))

    ctk.CTkLabel(
        top,
        text=manifest.get("display_name", ""),
        font=("Microsoft YaHei", 15, "bold"),
        text_color=manifest.get("layout", {}).get("title_color", "#e0e0e0"),
    ).pack(side="left", padx=4)

    # 总开关：走框架的 toggle（enable/disable 整功能）
    switch = ctk.CTkSwitch(
        top,
        text="",
        font=("Microsoft YaHei", 12),
        width=50,
        command=lambda: callbacks["toggle"](feature_id),
    )
    switch.pack(side="right", padx=6)

    ctk.CTkLabel(
        frame,
        text=manifest.get("desc", ""),
        text_color="#a0a0a0",
        font=("Microsoft YaHei", 12),
        wraplength=280 * colspan,
        justify="left",
        anchor="w",
    ).pack(fill="x", padx=10, pady=(4, 6))

    result = {handles.get("switch", feature_id + "_switch"): switch}
    # 提示行在子开关之后创建，这里先用占位函数把刷新接到子开关点击上
    refresh_ref = {"fn": lambda: None}

    for control in _config_switches(manifest):
        key = control["key"]

        row_frame = ctk.CTkFrame(frame, fg_color="transparent")
        row_frame.pack(fill="x", padx=12, pady=2)

        ctk.CTkLabel(
            row_frame,
            text=control.get("label", key),
            font=("Microsoft YaHei", 12),
            text_color="#e0e0e0",
        ).pack(side="left")

        sub = ctk.CTkSwitch(
            row_frame,
            text="",
            font=("Microsoft YaHei", 11),
            width=44,
            height=20,
        )
        sub.pack(side="right")

        # 初始状态以 manifest.config 为准（JS 端的内置默认值与它保持一致）
        initial = bool(config.get(key, control.get("default", False)))
        if initial:
            sub.select()
        else:
            sub.deselect()

        holder = _SyncedSwitchVar(
            sub,
            initial,
            lambda value, fid=feature_id, cfg_key=key: (
                callbacks["set_config"](fid, cfg_key, value),
                refresh_ref["fn"](),
            ),
        )
        sub.configure(command=holder.on_click)
        result[handles.get(key + "_var", feature_id + "_" + key + "_var")] = holder

    # A 方案联动提示：追踪已开启而「子弹穿墙/弹体穿墙」关闭时提醒，并可一键开启穿墙
    hint_row = ctk.CTkFrame(frame, fg_color="transparent")
    hint_row.pack(fill="x", padx=10, pady=(2, 8))
    hint = ctk.CTkLabel(
        hint_row,
        text="",
        font=("Microsoft YaHei", 11),
        text_color=HINT_COLORS["idle"],
        wraplength=280 * colspan,
        justify="left",
        anchor="w",
    )
    hint.pack(side="left", fill="x", expand=True)
    open_button = ctk.CTkButton(
        hint_row,
        text="一键开启穿墙",
        font=("Microsoft YaHei", 11),
        width=118,
        height=24,
        fg_color="#b45309",
        hover_color="#92400e",
        command=lambda: callbacks["toggle"](WALL_FEATURE_ID),
    )

    def resolve():
        """每轮重新解析两张卡片的开关状态：另一张卡片可能还没构建出来。"""
        wall_switch = _find_card_switch(parent, WALL_CARD_TITLE)
        wall_on = _visible_enabled(wall_switch, callbacks, WALL_FEATURE_ID)
        own_on = _visible_enabled(switch, callbacks, feature_id)
        config = callbacks["get_config"](feature_id) or {}
        return _tracking_from(config, own_on), wall_on

    refresh_hint = _bind_link_hint(hint, open_button, callbacks, resolve)
    refresh_ref["fn"] = refresh_hint
    switch.configure(command=lambda: (callbacks["toggle"](feature_id), refresh_hint()))

    return result