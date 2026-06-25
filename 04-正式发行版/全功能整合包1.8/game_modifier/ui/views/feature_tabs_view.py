from dataclasses import dataclass

import customtkinter as ctk


GRAVITY_MODE_VALUES = ("仅自己", "全部玩家")


@dataclass
class FeatureTabsHandles:
    knife_speed_var: ctk.DoubleVar
    knife_switch: ctk.CTkSwitch
    knife_speed_label: ctk.CTkLabel
    recoil_switch: ctk.CTkSwitch
    ammo_switch: ctk.CTkSwitch
    ammoplus_switch: ctk.CTkSwitch
    range_var: ctk.DoubleVar
    range_switch: ctk.CTkSwitch
    range_label: ctk.CTkLabel
    aim_switch: ctk.CTkSwitch
    speedgun_switch: ctk.CTkSwitch
    move_speed_var: ctk.DoubleVar
    move_switch: ctk.CTkSwitch
    move_speed_label: ctk.CTkLabel
    time_switch: ctk.CTkSwitch
    gravity_switch: ctk.CTkSwitch
    gravity_var: ctk.DoubleVar
    gravity_slider: ctk.CTkSlider
    gravity_label: ctk.CTkLabel
    jump_var: ctk.DoubleVar
    jump_slider: ctk.CTkSlider
    jump_label: ctk.CTkLabel
    gravity_mode_var: ctk.StringVar
    gravity_mode_combo: ctk.CTkComboBox
    godmode_switch: ctk.CTkSwitch
    skillcd_switch: ctk.CTkSwitch
    gather_switch: ctk.CTkSwitch
    gather_btn: ctk.CTkButton
    isbot_switch: ctk.CTkSwitch
    isbot_status_label: ctk.CTkLabel
    skip_round_btn: ctk.CTkButton
    esp_box_switch: ctk.CTkSwitch
    timescale_switch: ctk.CTkSwitch
    timescale_var: ctk.DoubleVar
    timescale_slider: ctk.CTkSlider
    timescale_label: ctk.CTkLabel


class FeatureTabsView:
    def __init__(
        self,
        *,
        on_toggle_feature,
        on_knife_speed_change,
        on_move_speed_change,
        on_range_change,
        on_timescale_change,
        on_gravity_change,
        on_jump_change,
        on_gravity_mode_change,
        on_gather,
        on_skip_round,
    ):
        self._on_toggle_feature = on_toggle_feature
        self._on_knife_speed_change = on_knife_speed_change
        self._on_move_speed_change = on_move_speed_change
        self._on_range_change = on_range_change
        self._on_timescale_change = on_timescale_change
        self._on_gravity_change = on_gravity_change
        self._on_jump_change = on_jump_change
        self._on_gravity_mode_change = on_gravity_mode_change
        self._on_gather = on_gather
        self._on_skip_round = on_skip_round

    def build(self, *, weapon_scroll, player_scroll, other_scroll):
        weapon_handles = self._build_weapon_tab(weapon_scroll)
        player_handles = self._build_player_tab(player_scroll)
        other_handles = self._build_other_tab(other_scroll)
        return FeatureTabsHandles(
            knife_speed_var=weapon_handles["knife_speed_var"],
            knife_switch=weapon_handles["knife_switch"],
            knife_speed_label=weapon_handles["knife_speed_label"],
            recoil_switch=weapon_handles["recoil_switch"],
            ammo_switch=weapon_handles["ammo_switch"],
            ammoplus_switch=weapon_handles["ammoplus_switch"],
            range_var=weapon_handles["range_var"],
            range_switch=weapon_handles["range_switch"],
            range_label=weapon_handles["range_label"],
            aim_switch=weapon_handles["aim_switch"],
            speedgun_switch=weapon_handles["speedgun_switch"],
            move_speed_var=player_handles["move_speed_var"],
            move_switch=player_handles["move_switch"],
            move_speed_label=player_handles["move_speed_label"],
            time_switch=player_handles["time_switch"],
            gravity_switch=player_handles["gravity_switch"],
            gravity_var=player_handles["gravity_var"],
            gravity_slider=player_handles["gravity_slider"],
            gravity_label=player_handles["gravity_label"],
            jump_var=player_handles["jump_var"],
            jump_slider=player_handles["jump_slider"],
            jump_label=player_handles["jump_label"],
            gravity_mode_var=player_handles["gravity_mode_var"],
            gravity_mode_combo=player_handles["gravity_mode_combo"],
            godmode_switch=player_handles["godmode_switch"],
            skillcd_switch=player_handles["skillcd_switch"],
            gather_switch=other_handles["gather_switch"],
            gather_btn=other_handles["gather_btn"],
            isbot_switch=other_handles["isbot_switch"],
            isbot_status_label=other_handles["isbot_status_label"],
            skip_round_btn=other_handles["skip_round_btn"],
            esp_box_switch=other_handles["esp_box_switch"],
            timescale_switch=other_handles["timescale_switch"],
            timescale_var=other_handles["timescale_var"],
            timescale_slider=other_handles["timescale_slider"],
            timescale_label=other_handles["timescale_label"],
        )

    def _make_feature_card(
        self,
        parent,
        row,
        col,
        colspan,
        color,
        feature_id,
        icon,
        name,
        desc,
        has_slider=False,
        slider_callback=None,
        slider_var=None,
        slider_range=None,
        title_color=None,
    ):
        bg_color = "#3a3a3a"
        text_color = "#e0e0e0"
        title_text_color = title_color if title_color else text_color

        frame = ctk.CTkFrame(
            parent,
            corner_radius=6,
            fg_color=bg_color,
            border_width=1,
            border_color="#555555",
            cursor="hand2",
        )
        frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)

        top_frame = ctk.CTkFrame(frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=8, pady=(6, 0))

        ctk.CTkLabel(
            top_frame,
            text=f"{icon} {name}",
            font=("Microsoft YaHei", 15, "bold"),
            text_color=title_text_color,
        ).pack(side="left", padx=4)

        frame.bind("<Button-1>", lambda e: self._on_toggle_feature(feature_id))

        slider_label_ref = None
        if has_slider and slider_var and slider_range:
            slider = ctk.CTkSlider(
                top_frame,
                from_=slider_range[0],
                to=slider_range[1],
                variable=slider_var,
                number_of_steps=int((slider_range[1] - slider_range[0]) * 10),
                command=slider_callback,
                width=90,
            )
            slider.pack(side="left", padx=4)
            slider_label_ref = ctk.CTkLabel(
                top_frame,
                text=f"{slider_var.get()}x",
                font=("Microsoft YaHei", 11),
                text_color=text_color,
                width=35,
            )
            slider_label_ref.pack(side="left")
            slider_var.trace_add(
                "write",
                lambda *args: slider_label_ref.configure(text=f"{slider_var.get():.1f}x"),
            )

        switch = ctk.CTkSwitch(
            top_frame,
            text="",
            font=("Microsoft YaHei", 12),
            width=50,
            command=lambda: self._on_toggle_feature(feature_id),
        )
        switch.pack(side="right", padx=6)

        wrap_width = 280 * colspan
        ctk.CTkLabel(
            frame,
            font=("Microsoft YaHei", 15),
            text=desc,
            text_color="#a0a0a0",
            wraplength=wrap_width,
            justify="left",
            anchor="w",
        ).pack(fill="x", padx=8, pady=(2, 6), expand=False)

        return frame, switch, slider_label_ref

    def _build_weapon_tab(self, scroll):
        for i in range(2):
            scroll.grid_columnconfigure(i, weight=1, uniform="wcol")

        knife_speed_var = ctk.DoubleVar(value=5.0)
        _, knife_switch, knife_speed_label = self._make_feature_card(
            scroll,
            0,
            0,
            1,
            "#3a1a1a",
            "knife",
            "🔪",
            "快刀",
            "提升挥刀速度（人类 / 生化幽灵通用）",
            has_slider=True,
            slider_callback=self._on_knife_speed_change,
            slider_var=knife_speed_var,
            slider_range=(1.0, 10.0),
            title_color="#FFB347",
        )

        _, recoil_switch, _ = self._make_feature_card(
            scroll, 0, 1, 1, "#1a1a3a", "recoil", "🎯", "无后座力", "消除所有枪械后座力", title_color="#6A9FB5"
        )

        _, ammo_switch, _ = self._make_feature_card(
            scroll, 1, 0, 1, "#3a2a1a", "ammo", "🔫", "无限子弹", "子弹永不消耗", title_color="#E5B73B"
        )

        _, ammoplus_switch, _ = self._make_feature_card(
            scroll, 1, 1, 1, "#3a1a2a", "ammoplus", "⚡", "快速换弹", "换弹速度加快", title_color="#D4AF37"
        )

        range_var = ctk.DoubleVar(value=50.0)
        _, range_switch, range_label = self._make_feature_card(
            scroll,
            2,
            0,
            2,
            "#1a2a1a",
            "range",
            "⚔️",
            "剑气化丝",
            "扩大近战攻击距离（人类 / 生化幽灵通用）",
            has_slider=True,
            slider_callback=self._on_range_change,
            slider_var=range_var,
            slider_range=(1.0, 50.0),
            title_color="#AF69EF",
        )

        _, aim_switch, _ = self._make_feature_card(
            scroll, 3, 0, 1, "#2a1a3a", "aim", "🎯", "自瞄", "自动瞄准敌方玩家\n\n", title_color="#FF6B6B"
        )

        speedgun_frame = ctk.CTkFrame(scroll, corner_radius=6, fg_color="#3a3a1a", border_width=1, border_color="#555555", cursor="hand2")
        speedgun_frame.grid(row=3, column=1, sticky="nsew", padx=3, pady=3)
        speedgun_frame.bind("<Button-1>", lambda e: self._on_toggle_feature("speedgun"))

        speedgun_top = ctk.CTkFrame(speedgun_frame, fg_color="transparent")
        speedgun_top.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(speedgun_top, text="⚡ 射速变快 / 连狙", font=("Microsoft YaHei", 15, "bold"), text_color="#FFD93D").pack(side="left", padx=4)
        speedgun_switch = ctk.CTkSwitch(speedgun_top, text="", font=("Microsoft YaHei", 12), width=50, command=lambda: self._on_toggle_feature("speedgun"))
        speedgun_switch.pack(side="right", padx=12)

        ctk.CTkLabel(
            speedgun_frame,
            font=("Microsoft YaHei", 12),
            text="• 射速 10 倍加速\n• 连狙：半自动 → 全自动，狙击镜常开\n• 后坐力清零 + 扩散归零",
            text_color="#a0a0a0",
            wraplength=280,
            justify="left",
            anchor="w",
        ).pack(fill="x", expand=False, padx=8, pady=(2, 6))

        return {
            "knife_speed_var": knife_speed_var,
            "knife_switch": knife_switch,
            "knife_speed_label": knife_speed_label,
            "recoil_switch": recoil_switch,
            "ammo_switch": ammo_switch,
            "ammoplus_switch": ammoplus_switch,
            "range_var": range_var,
            "range_switch": range_switch,
            "range_label": range_label,
            "aim_switch": aim_switch,
            "speedgun_switch": speedgun_switch,
        }

    def _build_player_tab(self, scroll):
        for i in range(2):
            scroll.grid_columnconfigure(i, weight=1, uniform="pcol")

        move_speed_var = ctk.DoubleVar(value=3.0)
        _, move_switch, move_speed_label = self._make_feature_card(
            scroll,
            0,
            0,
            1,
            "#1a2a3a",
            "movespeed",
            "👟",
            "滑板鞋",
            "提升移动速度",
            has_slider=True,
            slider_callback=self._on_move_speed_change,
            slider_var=move_speed_var,
            slider_range=(1.0, 6.0),
            title_color="#5FAD56",
        )

        _, time_switch, _ = self._make_feature_card(
            scroll, 0, 1, 1, "#1a2a1a", "time", "⏰", "无限时间", "设定时间为 9:59", title_color="#4C9F9F"
        )

        gravity_handles = self._build_gravity_card(scroll, 1)

        _, godmode_switch, _ = self._make_feature_card(
            scroll, 2, 0, 1, "#3a1a1a", "godmode", "🛡️", "金刚不坏", "角色受到攻击时不会受伤", title_color="#E74C3C"
        )

        _, skillcd_switch, _ = self._make_feature_card(
            scroll, 2, 1, 1, "#3a2a3a", "skillcd", "✨", "技能无冷却", "生化模式，所有技能无冷却", title_color="#A855F7"
        )

        gravity_handles.update(
            {
                "move_speed_var": move_speed_var,
                "move_switch": move_switch,
                "move_speed_label": move_speed_label,
                "time_switch": time_switch,
                "godmode_switch": godmode_switch,
                "skillcd_switch": skillcd_switch,
            }
        )
        return gravity_handles

    def _build_gravity_card(self, parent, row):
        gravity_frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555", cursor="hand2")
        gravity_frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=3, pady=3)
        gravity_frame.bind("<Button-1>", lambda e: self._on_toggle_feature("gravity"))

        top_frame = ctk.CTkFrame(gravity_frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top_frame, text="🌌 轻重力 / 高跳", font=("Microsoft YaHei", 15, "bold"), text_color="#F4A261").pack(side="left", padx=4)
        gravity_switch = ctk.CTkSwitch(top_frame, text="", font=("Microsoft YaHei", 12), width=50, command=lambda: self._on_toggle_feature("gravity"))
        gravity_switch.pack(side="right", padx=12)

        gravity_slider_frame = ctk.CTkFrame(gravity_frame, fg_color="transparent")
        gravity_slider_frame.pack(fill="x", padx=8, pady=(4, 0))
        ctk.CTkLabel(gravity_slider_frame, text="重力:", font=("Microsoft YaHei", 11), text_color="#e0e0e0").pack(side="left", padx=(4, 2))
        gravity_var = ctk.DoubleVar(value=1.0)
        gravity_slider = ctk.CTkSlider(gravity_slider_frame, from_=0.0, to=1.0, variable=gravity_var, number_of_steps=10, command=self._on_gravity_change, width=100)
        gravity_slider.pack(side="left", padx=2)
        gravity_label = ctk.CTkLabel(gravity_slider_frame, text="1.0", font=("Microsoft YaHei", 11), text_color="#e0e0e0", width=28)
        gravity_label.pack(side="left", padx=(2, 6))
        ctk.CTkLabel(gravity_slider_frame, text="跳跃:", font=("Microsoft YaHei", 11), text_color="#e0e0e0").pack(side="left", padx=(4, 2))
        jump_var = ctk.DoubleVar(value=1.0)
        jump_slider = ctk.CTkSlider(gravity_slider_frame, from_=1.0, to=5.0, variable=jump_var, number_of_steps=8, command=self._on_jump_change, width=100)
        jump_slider.pack(side="left", padx=2)
        jump_label = ctk.CTkLabel(gravity_slider_frame, text="1.0", font=("Microsoft YaHei", 11), text_color="#e0e0e0", width=28)
        jump_label.pack(side="left", padx=2)

        gravity_mode_frame = ctk.CTkFrame(gravity_frame, fg_color="transparent")
        gravity_mode_frame.pack(fill="x", padx=8, pady=(2, 2))
        ctk.CTkLabel(gravity_mode_frame, text="生效范围:", font=("Microsoft YaHei", 11), text_color="#e0e0e0").pack(side="left", padx=(4, 4))
        gravity_mode_var = ctk.StringVar(value=GRAVITY_MODE_VALUES[0])
        gravity_mode_combo = ctk.CTkComboBox(
            gravity_mode_frame,
            values=list(GRAVITY_MODE_VALUES),
            variable=gravity_mode_var,
            font=("Microsoft YaHei", 12),
            height=30,
            width=120,
            state="readonly",
            command=self._on_gravity_mode_change,
        )
        gravity_mode_combo.pack(side="left", padx=4)
        ctk.CTkLabel(gravity_frame, font=("Microsoft YaHei", 15), text="调整重力与跳跃倍率", text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", expand=False, padx=5, pady=5)

        return {
            "gravity_switch": gravity_switch,
            "gravity_var": gravity_var,
            "gravity_slider": gravity_slider,
            "gravity_label": gravity_label,
            "jump_var": jump_var,
            "jump_slider": jump_slider,
            "jump_label": jump_label,
            "gravity_mode_var": gravity_mode_var,
            "gravity_mode_combo": gravity_mode_combo,
        }

    def _build_other_tab(self, scroll):
        for i in range(2):
            scroll.grid_columnconfigure(i, weight=1, uniform="ocol")

        gather_frame = ctk.CTkFrame(scroll, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555", cursor="hand2")
        gather_frame.grid(row=0, column=0, columnspan=1, sticky="ew", padx=3, pady=3)
        gather_frame.bind("<Button-1>", lambda e: self._on_toggle_feature("gather"))
        top_frame = ctk.CTkFrame(gather_frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top_frame, text="👾 聚怪", font=("Microsoft YaHei", 15, "bold"), text_color="#E76F51").pack(side="left", padx=4)
        gather_switch = ctk.CTkSwitch(top_frame, text="启用追踪", font=("Microsoft YaHei", 12), width=50, command=lambda: self._on_toggle_feature("gather"))
        gather_switch.pack(side="right", padx=12)
        gather_btn_frame = ctk.CTkFrame(gather_frame, fg_color="transparent")
        gather_btn_frame.pack(fill="x", padx=8, pady=(2, 2))
        gather_btn = ctk.CTkButton(gather_btn_frame, text="📍 一键聚怪", font=("Microsoft YaHei", 14, "bold"), height=45, command=self._on_gather, fg_color="#b45309", hover_color="#92400e")
        gather_btn.pack(fill="x", padx=4, pady=4)
        ctk.CTkLabel(gather_frame, font=("Microsoft YaHei", 15), text="将所有人机聚集到佣兵出生点", text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", expand=False, padx=8, pady=(2, 6))

        isbot_frame = ctk.CTkFrame(scroll, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555", cursor="hand2")
        isbot_frame.grid(row=1, column=0, sticky="ew", padx=3, pady=3)
        isbot_frame.bind("<Button-1>", lambda e: self._on_toggle_feature("isbot"))
        isbot_top = ctk.CTkFrame(isbot_frame, fg_color="transparent")
        isbot_top.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(isbot_top, text="🧠 天机傀儡", font=("Microsoft YaHei", 15, "bold"), text_color="#00D4FF").pack(side="left", padx=4)
        isbot_switch = ctk.CTkSwitch(isbot_top, text="", font=("Microsoft YaHei", 12), width=50, command=lambda: self._on_toggle_feature("isbot"))
        isbot_switch.pack(side="right", padx=6)
        isbot_status_label = ctk.CTkLabel(isbot_frame, text="状态: 已关闭", font=("Microsoft YaHei", 11), text_color="#888888", anchor="w")
        isbot_status_label.pack(fill="x", padx=12, pady=(2, 0))
        isbot_placeholder = ctk.CTkFrame(isbot_frame, fg_color="transparent", height=1)
        isbot_placeholder.pack(fill="x", padx=8, pady=(0, 0))
        isbot_placeholder.pack_propagate(False)
        ctk.CTkLabel(isbot_frame, font=("Microsoft YaHei", 15), text="玩家由人机控制", text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", expand=False, padx=8, pady=(0, 4))

        skip_frame = ctk.CTkFrame(scroll, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555")
        skip_frame.grid(row=0, column=1, columnspan=1, sticky="ew", padx=3, pady=3)
        top_skip = ctk.CTkFrame(skip_frame, fg_color="transparent")
        top_skip.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top_skip, text="⏭️ 回合跳过", font=("Microsoft YaHei", 15, "bold"), text_color="#e0e0e0").pack(side="left", padx=4)
        skip_btn_frame = ctk.CTkFrame(skip_frame, fg_color="transparent")
        skip_btn_frame.pack(fill="x", padx=8, pady=(2, 2))
        skip_round_btn = ctk.CTkButton(skip_btn_frame, text="▶ 第一次跳过需要点击两次", font=("Microsoft YaHei", 14, "bold"), height=45, command=self._on_skip_round, fg_color="#b45309", hover_color="#92400e")
        skip_round_btn.pack(fill="x", padx=4, pady=4)
        ctk.CTkLabel(skip_frame, font=("Microsoft YaHei", 15), text="结束当前回合", text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", expand=False, padx=8, pady=(2, 6))

        esp_box_frame = ctk.CTkFrame(scroll, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555", cursor="hand2")
        esp_box_frame.grid(row=1, column=1, sticky="ew", padx=3, pady=3)
        esp_box_frame.bind("<Button-1>", lambda e: self._on_toggle_feature("esp_box"))
        esp_box_top = ctk.CTkFrame(esp_box_frame, fg_color="transparent")
        esp_box_top.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(esp_box_top, text="📦 方框透视", font=("Microsoft YaHei", 15, "bold"), text_color="#60A5FA").pack(side="left", padx=4)
        esp_box_switch = ctk.CTkSwitch(esp_box_top, text="", font=("Microsoft YaHei", 12), width=50, command=lambda: self._on_toggle_feature("esp_box"))
        esp_box_switch.pack(side="right", padx=6)
        esp_box_placeholder = ctk.CTkFrame(esp_box_frame, fg_color="transparent", height=20)
        esp_box_placeholder.pack(fill="x", padx=8, pady=(0, 0))
        esp_box_placeholder.pack_propagate(False)
        ctk.CTkLabel(esp_box_frame, font=("Microsoft YaHei", 15), text="开启敌人方框显示", text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", expand=False, padx=8, pady=(0, 4))

        timescale_frame = ctk.CTkFrame(scroll, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555", cursor="hand2")
        timescale_frame.grid(row=2, column=0, columnspan=1, sticky="ew", padx=3, pady=3)
        timescale_frame.bind("<Button-1>", lambda e: self._on_toggle_feature("timescale"))
        timescale_top = ctk.CTkFrame(timescale_frame, fg_color="transparent")
        timescale_top.pack(fill="x", padx=8, pady=(4, 0))
        ctk.CTkLabel(timescale_top, text="⏩ 时间加速", font=("Microsoft YaHei", 15, "bold"), text_color="#00CED1").pack(side="left", padx=4)
        timescale_switch = ctk.CTkSwitch(timescale_top, text="", font=("Microsoft YaHei", 12), width=50, command=lambda: self._on_toggle_feature("timescale"))
        timescale_switch.pack(side="right", padx=6)
        timescale_slider_frame = ctk.CTkFrame(timescale_frame, fg_color="transparent")
        timescale_slider_frame.pack(fill="x", padx=8, pady=(4, 0))
        timescale_var = ctk.DoubleVar(value=1.0)
        timescale_slider = ctk.CTkSlider(timescale_slider_frame, from_=0.1, to=10.0, variable=timescale_var, number_of_steps=99, command=self._on_timescale_change, width=150)
        timescale_slider.pack(side="left", padx=4)
        timescale_label = ctk.CTkLabel(timescale_slider_frame, text="1.0x", font=("Microsoft YaHei", 12), text_color="#e0e0e0", width=50)
        timescale_label.pack(side="left")
        ctk.CTkLabel(timescale_frame, font=("Microsoft YaHei", 15), text="调整游戏时间倍率", text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", expand=False, padx=8, pady=(2, 6))

        return {
            "gather_switch": gather_switch,
            "gather_btn": gather_btn,
            "isbot_switch": isbot_switch,
            "isbot_status_label": isbot_status_label,
            "skip_round_btn": skip_round_btn,
            "esp_box_switch": esp_box_switch,
            "timescale_switch": timescale_switch,
            "timescale_var": timescale_var,
            "timescale_slider": timescale_slider,
            "timescale_label": timescale_label,
        }
