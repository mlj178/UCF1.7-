import customtkinter as ctk


class FeatureCardBuilder:
    def __init__(self, callbacks):
        self.callbacks = callbacks

    def make_feature_card(
        self,
        parent,
        row,
        col,
        colspan,
        manifest,
        *,
        slider_callback=None,
        slider_var=None,
        slider_range=None,
        title_color=None,
        switch_text="",
    ):
        feature_id = manifest["feature_id"]
        bg_color = "#3a3a3a"
        text_color = "#e0e0e0"

        frame = ctk.CTkFrame(
            parent,
            corner_radius=6,
            fg_color=bg_color,
            border_width=1,
            border_color="#555555",
        )
        frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)

        top_frame = ctk.CTkFrame(frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=8, pady=(6, 0))

        title_name_label = ctk.CTkLabel(
            top_frame,
            text=manifest.get("display_name", ""),
            font=("Microsoft YaHei", 15, "bold"),
            text_color=title_color or text_color,
        )
        title_name_label.pack(side="left", padx=(4, 4))

        slider_label_ref = None
        if slider_callback and slider_var and slider_range:
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
            text=switch_text,
            font=("Microsoft YaHei", 12),
            width=50,
            command=lambda: self.callbacks["toggle"](feature_id),
        )
        switch.pack(side="right", padx=6)

        ctk.CTkLabel(
            frame,
            font=("Microsoft YaHei", 15),
            text=manifest.get("desc", ""),
            text_color="#a0a0a0",
            wraplength=280 * colspan,
            justify="left",
            anchor="w",
        ).pack(fill="x", padx=8, pady=(2, 6), expand=False)

        return frame, switch, slider_label_ref
