import customtkinter as ctk

from ui.components.feature_card import FeatureCardBuilder


GRAVITY_MODE_VALUES = ("仅自己", "全部玩家")


TITLE_COLORS = {
    "knife": "#FFB347",
    "recoil": "#6A9FB5",
    "ammo": "#E5B73B",
    "ammoplus": "#D4AF37",
    "range": "#AF69EF",
    "aim": "#FF6B6B",
    "speedgun": "#FFD93D",
    "movespeed": "#5FAD56",
    "time": "#4C9F9F",
    "gravity": "#F4A261",
    "godmode": "#E74C3C",
    "skillcd": "#A855F7",
    "gather": "#E76F51",
    "isbot": "#00D4FF",
    "esp_box": "#60A5FA",
    "timescale": "#00CED1",
}


class PluginFeaturePage:
    def __init__(self, registry, callbacks):
        self.registry = registry
        self.callbacks = callbacks
        self.card_builder = FeatureCardBuilder(callbacks)

    def build_tab(self, scroll, tab_id):
        for i in range(2):
            scroll.grid_columnconfigure(i, weight=1, uniform=f"{tab_id}_col")

        handles = {}
        row = 0
        col = 0
        for feature in self.registry.by_tab(tab_id):
            manifest = feature.manifest
            layout = manifest.get("layout", {})
            colspan = int(layout.get("columnspan", 1))
            if colspan >= 2 and col == 1:
                row += 1
                col = 0

            feature_id = manifest["feature_id"]
            new_handles = self._build_feature(scroll, manifest, row, col, colspan)
            handles.update(new_handles)

            if colspan >= 2 or col == 1:
                row += 1
                col = 0
            else:
                col = 1
        return handles

    def _build_feature(self, scroll, manifest, row, col, colspan):
        feature_id = manifest["feature_id"]
        if feature_id == "gravity":
            return self._build_gravity_card(scroll, manifest, row)
        if feature_id == "gather":
            return self._build_gather_card(scroll, manifest, row, col, colspan)
        if feature_id == "roundskip":
            return self._build_skip_card(scroll, manifest, row, col, colspan)
        if feature_id == "isbot":
            return self._build_isbot_card(scroll, manifest, row, col, colspan)
        if feature_id == "esp_box":
            return self._build_esp_box_card(scroll, manifest, row, col, colspan)
        if feature_id == "timescale":
            return self._build_timescale_card(scroll, manifest, row, col, colspan)
        if feature_id == "speedgun":
            return self._build_speedgun_card(scroll, manifest, row, col, colspan)

        return self._build_standard_card(scroll, manifest, row, col, colspan)

    def _build_standard_card(self, scroll, manifest, row, col, colspan):
        feature_id = manifest["feature_id"]
        slider_control = self._first_control(manifest, "slider")
        slider_var = None
        callback = None
        slider_range = None
        if slider_control:
            slider_var = ctk.DoubleVar(value=float(slider_control.get("default", 1.0)))
            slider_range = (float(slider_control["min"]), float(slider_control["max"]))
            callback = self.callbacks["slider"].get(feature_id)

        _, switch, label = self.card_builder.make_feature_card(
            scroll,
            row,
            col,
            colspan,
            manifest,
            slider_callback=callback,
            slider_var=slider_var,
            slider_range=slider_range,
            title_color=TITLE_COLORS.get(feature_id),
        )

        handles = {self._switch_name(feature_id): switch}
        if slider_var is not None:
            handles[self._var_name(feature_id)] = slider_var
        if label is not None:
            handles[self._label_name(feature_id)] = label
        return handles

    def _build_speedgun_card(self, scroll, manifest, row, col, colspan):
        frame = ctk.CTkFrame(scroll, corner_radius=6, fg_color="#3a3a1a", border_width=1, border_color="#555555")
        frame.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)

        top = ctk.CTkFrame(frame, fg_color="transparent")
        top.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top, text=f"{manifest['icon']} {manifest['display_name']}", font=("Microsoft YaHei", 15, "bold"), text_color=TITLE_COLORS["speedgun"]).pack(side="left", padx=4)
        switch = ctk.CTkSwitch(top, text="", font=("Microsoft YaHei", 12), width=50, command=lambda: self.callbacks["toggle"]("speedgun"))
        switch.pack(side="right", padx=12)
        ctk.CTkLabel(
            frame,
            font=("Microsoft YaHei", 12),
            text="• 射速 10 倍加速\n• 连狙：半自动 → 全自动，狙击镜常开\n• 后坐力清零 + 扩散归零",
            text_color="#a0a0a0",
            wraplength=280,
            justify="left",
            anchor="w",
        ).pack(fill="x", expand=False, padx=8, pady=(2, 6))
        return {"speedgun_switch": switch}

    def _build_gravity_card(self, parent, manifest, row):
        frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555")
        frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=3, pady=3)

        top = ctk.CTkFrame(frame, fg_color="transparent")
        top.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top, text=f"{manifest['icon']} {manifest['display_name']}", font=("Microsoft YaHei", 15, "bold"), text_color=TITLE_COLORS["gravity"]).pack(side="left", padx=4)
        switch = ctk.CTkSwitch(top, text="", font=("Microsoft YaHei", 12), width=50, command=lambda: self.callbacks["toggle"]("gravity"))
        switch.pack(side="right", padx=12)

        slider_frame = ctk.CTkFrame(frame, fg_color="transparent")
        slider_frame.pack(fill="x", padx=8, pady=(4, 0))
        ctk.CTkLabel(slider_frame, text="重力:", font=("Microsoft YaHei", 11), text_color="#e0e0e0").pack(side="left", padx=(4, 2))
        gravity_var = ctk.DoubleVar(value=1.0)
        gravity_slider = ctk.CTkSlider(slider_frame, from_=0.0, to=1.0, variable=gravity_var, number_of_steps=10, command=self.callbacks["gravity"], width=100)
        gravity_slider.pack(side="left", padx=2)
        gravity_label = ctk.CTkLabel(slider_frame, text="1.0", font=("Microsoft YaHei", 11), text_color="#e0e0e0", width=28)
        gravity_label.pack(side="left", padx=(2, 6))
        ctk.CTkLabel(slider_frame, text="跳跃:", font=("Microsoft YaHei", 11), text_color="#e0e0e0").pack(side="left", padx=(4, 2))
        jump_var = ctk.DoubleVar(value=1.0)
        jump_slider = ctk.CTkSlider(slider_frame, from_=1.0, to=5.0, variable=jump_var, number_of_steps=8, command=self.callbacks["jump"], width=100)
        jump_slider.pack(side="left", padx=2)
        jump_label = ctk.CTkLabel(slider_frame, text="1.0", font=("Microsoft YaHei", 11), text_color="#e0e0e0", width=28)
        jump_label.pack(side="left", padx=2)

        mode_frame = ctk.CTkFrame(frame, fg_color="transparent")
        mode_frame.pack(fill="x", padx=8, pady=(2, 2))
        ctk.CTkLabel(mode_frame, text="生效范围:", font=("Microsoft YaHei", 11), text_color="#e0e0e0").pack(side="left", padx=(4, 4))
        mode_var = ctk.StringVar(value=GRAVITY_MODE_VALUES[0])
        mode_combo = ctk.CTkComboBox(
            mode_frame,
            values=list(GRAVITY_MODE_VALUES),
            variable=mode_var,
            font=("Microsoft YaHei", 12),
            height=30,
            width=120,
            state="readonly",
            command=self.callbacks["gravity_mode"],
        )
        mode_combo.pack(side="left", padx=4)
        ctk.CTkLabel(frame, font=("Microsoft YaHei", 15), text=manifest["desc"], text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", expand=False, padx=5, pady=5)
        return {
            "gravity_switch": switch,
            "gravity_var": gravity_var,
            "gravity_slider": gravity_slider,
            "gravity_label": gravity_label,
            "jump_var": jump_var,
            "jump_slider": jump_slider,
            "jump_label": jump_label,
            "gravity_mode_var": mode_var,
            "gravity_mode_combo": mode_combo,
        }

    def _build_gather_card(self, scroll, manifest, row, col, colspan):
        frame = ctk.CTkFrame(scroll, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555")
        frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)
        top = ctk.CTkFrame(frame, fg_color="transparent")
        top.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top, text=f"{manifest['icon']} {manifest['display_name']}", font=("Microsoft YaHei", 15, "bold"), text_color=TITLE_COLORS["gather"]).pack(side="left", padx=4)
        switch = ctk.CTkSwitch(top, text="启用追踪", font=("Microsoft YaHei", 12), width=50, command=lambda: self.callbacks["toggle"]("gather"))
        switch.pack(side="right", padx=12)
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=8, pady=(2, 2))
        button = ctk.CTkButton(btn_frame, text="📍 一键聚怪", font=("Microsoft YaHei", 14, "bold"), height=45, command=self.callbacks["gather"], fg_color="#b45309", hover_color="#92400e")
        button.pack(fill="x", padx=4, pady=4)
        ctk.CTkLabel(frame, font=("Microsoft YaHei", 15), text=manifest["desc"], text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", expand=False, padx=8, pady=(2, 6))
        return {"gather_switch": switch, "gather_btn": button}

    def _build_isbot_card(self, scroll, manifest, row, col, colspan):
        frame = ctk.CTkFrame(scroll, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555")
        frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)
        top = ctk.CTkFrame(frame, fg_color="transparent")
        top.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top, text=f"{manifest['icon']} {manifest['display_name']}", font=("Microsoft YaHei", 15, "bold"), text_color=TITLE_COLORS["isbot"]).pack(side="left", padx=4)
        switch = ctk.CTkSwitch(top, text="", font=("Microsoft YaHei", 12), width=50, command=lambda: self.callbacks["toggle"]("isbot"))
        switch.pack(side="right", padx=6)
        status = ctk.CTkLabel(frame, text="状态: 已关闭", font=("Microsoft YaHei", 11), text_color="#888888", anchor="w")
        status.pack(fill="x", padx=12, pady=(2, 0))
        placeholder = ctk.CTkFrame(frame, fg_color="transparent", height=1)
        placeholder.pack(fill="x", padx=8, pady=(0, 0))
        placeholder.pack_propagate(False)
        ctk.CTkLabel(frame, font=("Microsoft YaHei", 15), text=manifest["desc"], text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", expand=False, padx=8, pady=(0, 4))
        return {"isbot_switch": switch, "isbot_status_label": status}

    def _build_skip_card(self, scroll, manifest, row, col, colspan):
        frame = ctk.CTkFrame(scroll, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555")
        frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)
        top = ctk.CTkFrame(frame, fg_color="transparent")
        top.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top, text=f"{manifest['icon']} {manifest['display_name']}", font=("Microsoft YaHei", 15, "bold"), text_color="#e0e0e0").pack(side="left", padx=4)
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=8, pady=(2, 2))
        button = ctk.CTkButton(btn_frame, text="▶ 第一次跳过需要点击两次", font=("Microsoft YaHei", 14, "bold"), height=45, command=self.callbacks["skip_round"], fg_color="#b45309", hover_color="#92400e")
        button.pack(fill="x", padx=4, pady=4)
        ctk.CTkLabel(frame, font=("Microsoft YaHei", 15), text=manifest["desc"], text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", expand=False, padx=8, pady=(2, 6))
        return {"skip_round_btn": button}

    def _build_esp_box_card(self, scroll, manifest, row, col, colspan):
        frame = ctk.CTkFrame(scroll, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555")
        frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)
        top = ctk.CTkFrame(frame, fg_color="transparent")
        top.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top, text=f"{manifest['icon']} {manifest['display_name']}", font=("Microsoft YaHei", 15, "bold"), text_color=TITLE_COLORS["esp_box"]).pack(side="left", padx=4)
        switch = ctk.CTkSwitch(top, text="", font=("Microsoft YaHei", 12), width=50, command=lambda: self.callbacks["toggle"]("esp_box"))
        switch.pack(side="right", padx=6)
        placeholder = ctk.CTkFrame(frame, fg_color="transparent", height=20)
        placeholder.pack(fill="x", padx=8, pady=(0, 0))
        placeholder.pack_propagate(False)
        ctk.CTkLabel(frame, font=("Microsoft YaHei", 15), text=manifest["desc"], text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", expand=False, padx=8, pady=(0, 4))
        return {"esp_box_switch": switch}

    def _build_timescale_card(self, scroll, manifest, row, col, colspan):
        frame = ctk.CTkFrame(scroll, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555")
        frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)
        top = ctk.CTkFrame(frame, fg_color="transparent")
        top.pack(fill="x", padx=8, pady=(4, 0))
        ctk.CTkLabel(top, text=f"{manifest['icon']} {manifest['display_name']}", font=("Microsoft YaHei", 15, "bold"), text_color=TITLE_COLORS["timescale"]).pack(side="left", padx=4)
        switch = ctk.CTkSwitch(top, text="", font=("Microsoft YaHei", 12), width=50, command=lambda: self.callbacks["toggle"]("timescale"))
        switch.pack(side="right", padx=6)
        slider_frame = ctk.CTkFrame(frame, fg_color="transparent")
        slider_frame.pack(fill="x", padx=8, pady=(4, 0))
        var = ctk.DoubleVar(value=1.0)
        slider = ctk.CTkSlider(slider_frame, from_=0.1, to=10.0, variable=var, number_of_steps=99, command=self.callbacks["slider"]["timescale"], width=150)
        slider.pack(side="left", padx=4)
        label = ctk.CTkLabel(slider_frame, text="1.0x", font=("Microsoft YaHei", 12), text_color="#e0e0e0", width=50)
        label.pack(side="left")
        ctk.CTkLabel(frame, font=("Microsoft YaHei", 15), text=manifest["desc"], text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", expand=False, padx=8, pady=(2, 6))
        return {"timescale_switch": switch, "timescale_var": var, "timescale_slider": slider, "timescale_label": label}

    @staticmethod
    def _first_control(manifest, control_type):
        for control in manifest.get("controls", []):
            if control.get("type") == control_type:
                return control
        return None

    @staticmethod
    def _switch_name(feature_id):
        names = {"movespeed": "move_switch"}
        return names.get(feature_id, f"{feature_id}_switch")

    @staticmethod
    def _var_name(feature_id):
        names = {"knife": "knife_speed_var", "movespeed": "move_speed_var", "range": "range_var"}
        return names.get(feature_id, f"{feature_id}_var")

    @staticmethod
    def _label_name(feature_id):
        names = {"knife": "knife_speed_label", "movespeed": "move_speed_label", "range": "range_label"}
        return names.get(feature_id, f"{feature_id}_label")
