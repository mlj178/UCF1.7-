"""伤害吸血 · 面板（整合包卡片 UI）。

单张宽卡片：
- 顶部：标题 + 总开关
- 一行：吸血比例滑块（0% ~ 100%）
- 一行：「伤害来源」摘要 + 展开/收起（六个来源开关默认收起）
- 一行：只吸敌人
- 底部：当前设置汇总

为什么把来源开关收起：
- 实测（2026-11-14 13:38 日志）大多数对局只用刀 / 手雷 / 技能，来源开关长期不碰，
  但全摆出来会把这张卡撑到 330px，把人物属性页挤长一屏。
- 但**不能删**：「特殊 / 技能」目前兜住了未映射的伤害（枪托等），
  关掉它就会出现「刀能吸、枪托不吸」，需要给用户留入口。
- 「感染」例外：Entity.OnEntityHurt 对 type==4 直接 return，永远走不到 HealthData.Hurt，
  这个开关拖了也不会生效，所以从 UI 下线（配置键 src_infect_enabled 保留，默认 false）。

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
)

# 只保留配置键、不再出控件的分类（见文件头说明）
HIDDEN_CATEGORY_KEYS = ("infect",)

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

    # ---------------- 伤害来源（默认收起） ----------------
    advanced_header = ctk.CTkFrame(frame, fg_color="transparent")
    advanced_header.pack(fill="x", padx=10, pady=(2, 0))
    advanced_header.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        advanced_header,
        text="伤害来源",
        text_color="#8f98a8",
        font=("Microsoft YaHei", 11, "bold"),
        anchor="w",
    ).grid(row=0, column=0, sticky="w")

    source_hint = ctk.CTkLabel(
        advanced_header,
        text="",
        text_color="#6b7280",
        font=("Microsoft YaHei", 10),
        anchor="w",
        justify="left",
    )
    source_hint.grid(row=1, column=0, sticky="w")

    advanced_button = ctk.CTkButton(
        advanced_header,
        text="展开 ▾",
        width=78,
        height=22,
        font=("Microsoft YaHei", 11),
        fg_color="transparent",
        hover_color="#374151",
        text_color="#9ca3af",
        border_width=1,
        border_color="#4b5563",
        command=lambda: toggle_advanced(),
    )
    advanced_button.grid(row=0, column=1, rowspan=2, sticky="e")

    # 容器默认不 pack：收起状态只留上面那一行摘要 + 展开按钮
    source_frame = ctk.CTkFrame(frame, fg_color="transparent")
    source_frame.grid_columnconfigure(0, weight=1)
    source_frame.grid_columnconfigure(1, weight=1)

    advanced_open = {"value": False}

    def set_advanced(open_flag):
        advanced_open["value"] = bool(open_flag)
        if advanced_open["value"]:
            # before=enemy_row：展开的开关贴在「伤害来源」下面，而不是被排到卡片末尾
            source_frame.pack(fill="x", padx=6, pady=(2, 2), before=enemy_row)
            advanced_button.configure(text="收起 ▴")
        else:
            source_frame.pack_forget()
            advanced_button.configure(text="展开 ▾")
        refresh_source_hint()

    def toggle_advanced():
        set_advanced(not advanced_open["value"])

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
        default_enabled = bool(config.get(cfg_key, enabled_control.get("default", True)))

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

    def refresh_source_hint():
        off = [name for key, name, _hint, _color in CATEGORY_ROWS if not bool(category_vars[key].get())]
        if not off:
            source_hint.configure(text="全部开启 · 点右侧可单独关闭某类来源")
        else:
            source_hint.configure(text="已关闭：" + "、".join(off))

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
        refresh_source_hint()

    refresh_summary()
    # 默认收起：卡片只占 比例 / 来源摘要 / 只吸敌人 三行
    set_advanced(False)

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
    # 折叠区的控件（不入 manifest.ui_handles，仅供离线构建测试 / 排障用）
    result[handles.get("advanced_toggle", "lifesteal_advanced_toggle")] = advanced_button
    result[handles.get("advanced_frame", "lifesteal_advanced_frame")] = source_frame
    result[handles.get("source_hint", "lifesteal_source_hint")] = source_hint
    return result
