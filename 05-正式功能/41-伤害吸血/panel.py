"""伤害吸血 · 面板（整合包卡片 UI）。

单张宽卡片：
- 顶部：标题 + 总开关
- 一行：吸血比例滑块（0% ~ 100%）
- 一组：伤害来源开关（主武器 / 副武器 / 枪托重击 / 近战 / 投掷 / 特殊 / 感染）
- 一行：只吸敌人
- 底部：当前设置汇总

本文件只负责搭 UI 和把用户操作转成 callbacks，不直接碰 Frida。
"""

import customtkinter as ctk

# (config 后缀, 显示名, 说明, 主题色)
CATEGORY_ROWS = (
    ("gun_primary", "主武器", "步枪 / 狙击 / 机枪 / 冲锋枪 / 霰弹枪", "#f87171"),
    ("gun_secondary", "副武器", "手枪", "#fb923c"),
    ("gun_stock", "枪托重击", "枪械近战（枪托 / 刺刀）", "#fbbf24"),
    ("knife", "近战武器", "刀 / 英雄近战", "#a78bfa"),
    ("grenade", "投掷 / 爆炸", "手雷 / RPG / 榴弹", "#60a5fa"),
    ("special", "特殊 / 技能", "其它伤害类型", "#34d399"),
    ("infect", "感染", "生化感染（默认关）", "#94a3b8"),
)

DISABLED_COLOR = "#5a626e"


def _control(manifest, control_type=None, key=None):
    for item in manifest.get("controls", []):
        if control_type and item.get("type") != control_type:
            continue
        if key is not None and item.get("key") != key:
            continue
        return item
    return {}


def _master_control(manifest):
    for item in manifest.get("controls", []):
        if item.get("type") == "switch" and not item.get("key"):
            return item
    return {}


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    handles = manifest.get("ui_handles", {})
    config = dict(manifest.get("config") or {})
    master = _master_control(manifest)
    percent_control = _control(manifest, "slider", "lifesteal_percent")

    frame = ctk.CTkFrame(
        parent,
        corner_radius=6,
        fg_color="transparent",
        border_width=1,
        border_color="#4b5563",
    )
    frame.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)

    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))

    ctk.CTkLabel(
        top,
        text=manifest.get("display_name", ""),
        font=("Microsoft YaHei", 15, "bold"),
        text_color=manifest.get("layout", {}).get("title_color", "#ef4444"),
    ).pack(side="left", padx=4)

    switch = ctk.CTkSwitch(
        top,
        text=master.get("label", ""),
        font=("Microsoft YaHei", 12),
        width=50,
        command=lambda: callbacks["toggle"](feature_id),
    )
    switch.pack(side="right", padx=6)

    desc_lines = manifest.get("ui_text", {}).get("lines") or [manifest.get("desc", "")]
    ctk.CTkLabel(
        frame,
        text="\n".join(desc_lines),
        text_color="#a0a0a0",
        font=("Microsoft YaHei", 12),
        wraplength=520 * max(1, colspan // 2),
        justify="left",
        anchor="w",
    ).pack(fill="x", padx=10, pady=(4, 6))

    # ---------------- 吸血比例 ----------------
    percent_row = ctk.CTkFrame(frame, fg_color="transparent")
    percent_row.pack(fill="x", padx=10, pady=(2, 6))
    percent_row.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(
        percent_row,
        text=percent_control.get("label", "吸血比例"),
        font=("Microsoft YaHei", 12, "bold"),
        text_color="#ef4444",
        width=70,
        anchor="w",
    ).grid(row=0, column=0, padx=(0, 8), sticky="w")

    minimum = float(percent_control.get("min", 0))
    maximum = float(percent_control.get("max", 100))
    step = float(percent_control.get("step", 1)) or 1.0
    default_value = float(config.get("lifesteal_percent", percent_control.get("default", 10)))
    default_value = min(maximum, max(minimum, default_value))
    steps = max(1, int(round((maximum - minimum) / step)))

    percent_var = ctk.DoubleVar(value=default_value)
    percent_label = ctk.CTkLabel(
        percent_row,
        text=f"{int(round(default_value))}%",
        font=("Microsoft YaHei", 12, "bold"),
        width=52,
        anchor="e",
    )

    def on_percent_change(value):
        numeric = int(round(float(value)))
        callbacks["set_config"](feature_id, "lifesteal_percent", numeric)
        refresh_summary()

    percent_slider = ctk.CTkSlider(
        percent_row,
        from_=minimum,
        to=maximum,
        number_of_steps=steps,
        variable=percent_var,
        command=on_percent_change,
    )
    percent_slider.grid(row=0, column=1, padx=(0, 8), sticky="ew")

    def refresh_percent_label(*_args):
        percent_label.configure(text=f"{int(round(float(percent_var.get())))}%")
        refresh_summary()

    percent_var.trace_add("write", refresh_percent_label)
    percent_label.grid(row=0, column=2, sticky="e")

    # ---------------- 伤害来源 ----------------
    ctk.CTkLabel(
        frame,
        text="伤害来源（可分别开关，关闭后该来源不吸血）",
        text_color="#8f98a8",
        font=("Microsoft YaHei", 11),
        anchor="w",
    ).pack(fill="x", padx=10, pady=(2, 2))

    source_frame = ctk.CTkFrame(frame, fg_color="transparent")
    source_frame.pack(fill="x", padx=6, pady=(0, 2))
    source_frame.grid_columnconfigure(0, weight=1)
    source_frame.grid_columnconfigure(1, weight=1)

    category_vars = {}
    category_switches = {}

    def make_toggle_handler(cfg_key, var):
        def handler():
            callbacks["set_config"](feature_id, cfg_key, bool(var.get()))
            refresh_summary()
        return handler

    for index, (key, name, hint, color) in enumerate(CATEGORY_ROWS):
        cfg_key = f"src_{key}_enabled"
        enabled_control = _control(manifest, "switch", cfg_key)
        default_enabled = bool(config.get(cfg_key, enabled_control.get("default", key != "infect")))

        cell = ctk.CTkFrame(source_frame, fg_color="transparent")
        cell.grid(row=index // 2, column=index % 2, sticky="ew", padx=4, pady=1)
        cell.grid_columnconfigure(0, weight=1)

        var = ctk.BooleanVar(value=default_enabled)

        label = ctk.CTkLabel(
            cell,
            text=name,
            font=("Microsoft YaHei", 12, "bold"),
            text_color=color if default_enabled else DISABLED_COLOR,
            anchor="w",
        )
        label.grid(row=0, column=0, sticky="w")

        hint_label = ctk.CTkLabel(
            cell,
            text=hint,
            font=("Microsoft YaHei", 10),
            text_color="#7c8595" if default_enabled else DISABLED_COLOR,
            anchor="w",
        )
        hint_label.grid(row=1, column=0, sticky="w")

        toggle = ctk.CTkSwitch(
            cell,
            text="",
            width=40,
            variable=var,
            command=make_toggle_handler(cfg_key, var),
        )
        toggle.grid(row=0, column=1, rowspan=2, padx=(6, 2), sticky="e")

        def refresh_category(
            *_args,
            var=var,
            label=label,
            hint_label=hint_label,
            color=color,
        ):
            enabled = bool(var.get())
            label.configure(text_color=color if enabled else DISABLED_COLOR)
            hint_label.configure(text_color="#7c8595" if enabled else DISABLED_COLOR)
            refresh_summary()

        var.trace_add("write", refresh_category)
        category_vars[key] = var
        category_switches[key] = toggle

    # ---------------- 只吸敌人 ----------------
    enemy_row = ctk.CTkFrame(frame, fg_color="transparent")
    enemy_row.pack(fill="x", padx=10, pady=(4, 2))
    enemy_row.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        enemy_row,
        text="只吸敌人（打队友 / 自己不掉血也不吸血）",
        font=("Microsoft YaHei", 11),
        text_color="#a0a0a0",
        anchor="w",
    ).grid(row=0, column=0, sticky="w")

    enemy_var = ctk.BooleanVar(value=bool(config.get("only_enemy_victim", True)))
    enemy_switch = ctk.CTkSwitch(
        enemy_row,
        text="",
        width=40,
        variable=enemy_var,
        command=lambda: callbacks["set_config"](feature_id, "only_enemy_victim", bool(enemy_var.get())),
    )
    enemy_switch.grid(row=0, column=1, sticky="e")

    # ---------------- 汇总 ----------------
    summary = ctk.CTkLabel(
        frame,
        text="",
        font=("Microsoft YaHei", 11),
        text_color="#a0a0a0",
        anchor="w",
        justify="left",
    )
    summary.pack(fill="x", padx=10, pady=(4, 8))

    def refresh_summary():
        percent_text = f"{int(round(float(percent_var.get())))}%"
        enabled_names = [name for key, name, _hint, _color in CATEGORY_ROWS if bool(category_vars[key].get())]
        if not enabled_names:
            source_text = "无（不会吸血）"
        elif len(enabled_names) == len(CATEGORY_ROWS):
            source_text = "全部"
        else:
            source_text = "、".join(enabled_names)
        summary.configure(text=f"当前 · 吸血 {percent_text} ｜ 来源：{source_text}")

    refresh_summary()

    result = {
        handles.get("switch", "lifesteal_switch"): switch,
        handles.get("summary", "lifesteal_summary"): summary,
        handles.get("lifesteal_percent_var", "lifesteal_percent_var"): percent_var,
        handles.get("lifesteal_percent_slider", "lifesteal_percent_slider"): percent_slider,
        handles.get("lifesteal_percent_label", "lifesteal_percent_label"): percent_label,
        handles.get("only_enemy_victim_var", "lifesteal_only_enemy_victim_var"): enemy_var,
        handles.get("only_enemy_victim_switch", "lifesteal_only_enemy_victim_switch"): enemy_switch,
    }
    for key, _name, _hint, _color in CATEGORY_ROWS:
        result[handles.get(f"src_{key}_enabled_var", f"lifesteal_src_{key}_var")] = category_vars[key]
        result[handles.get(f"src_{key}_enabled_switch", f"lifesteal_src_{key}_switch")] = category_switches[key]
    return result
