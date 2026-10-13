"""开火直伤/弹体追踪 —— 2.7 功能卡片。

卡片结构（从上到下）：
    标题 + 总开关
    说明文字
    3 个子开关：常规枪械直伤 / 榴弹手雷RPG 追踪 / 特殊技能弹 追踪

为什么不用默认卡片（PluginFeaturePage._build_default_card）：
    默认卡片只渲染"第一个 slider"加一个总开关，而本功能需要 3 个
    action=setConfig 的子开关，所以这里自己画卡片。

子开关句柄为什么要包一层 _SyncedSwitchVar：
    框架的 App._sync_plugin_controls_from_config 对"带 key 的 switch 控件"会调用
    handle.set(bool(config[key]))，而原生 CTkSwitch 只有 select()/deselect()、没有 set()。
    包一层提供 set(bool)/get()，同时把用户点击转到 callbacks["set_config"]。
句柄名必须和 manifest.ui_handles 里的 <key>_var 一致（框架按这个名字 getattr）。
"""

import customtkinter as ctk


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
            lambda value, fid=feature_id, cfg_key=key: callbacks["set_config"](
                fid, cfg_key, value
            ),
        )
        sub.configure(command=holder.on_click)
        result[handles.get(key + "_var", feature_id + "_" + key + "_var")] = holder

    return result