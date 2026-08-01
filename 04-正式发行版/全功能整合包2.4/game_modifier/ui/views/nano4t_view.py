from dataclasses import dataclass

import customtkinter as ctk


GRAVITY_MODE_VALUES = ("仅自己", "全部玩家")


def build_nano4t_option_values(attrs, start, stop):
    return [f"{i}: {attrs[i][0]}" for i in range(start, stop)]


def build_nano4t_selection_copy(attrs, selected_id):
    return f"{selected_id}: {attrs[selected_id][0]}", f"效果: {attrs[selected_id][1]}"


@dataclass
class Nano4tViewHandles:
    nano4t_top_frame: ctk.CTkFrame
    nano4t_status_dot: ctk.CTkLabel
    nano4t_status_label: ctk.CTkLabel
    nano4t_round_frame: ctk.CTkFrame
    nano4t_round_label: ctk.CTkLabel
    nano4t_next_label: ctk.CTkLabel
    nano4t_ghost_status_label: ctk.CTkLabel
    nano4t_ghost_var: ctk.StringVar
    nano4t_ghost_combo: ctk.CTkComboBox
    nano4t_ghost_desc: ctk.CTkLabel
    nano4t_human_status_label: ctk.CTkLabel
    nano4t_human_var: ctk.StringVar
    nano4t_human_combo: ctk.CTkComboBox
    nano4t_human_desc: ctk.CTkLabel
    nano4t_apply_btn: ctk.CTkButton
    battle_round_status_label: ctk.CTkLabel
    battle_round_switch: ctk.CTkSwitch
    inline_card_host: ctk.CTkFrame


class Nano4tView:
    def __init__(
        self,
        *,
        attrs,
        temp_ghost,
        temp_human,
        on_ghost_select,
        on_human_select,
        on_apply,
        on_toggle_battle_round,
    ):
        self._attrs = attrs
        self._temp_ghost = temp_ghost
        self._temp_human = temp_human
        self._on_ghost_select = on_ghost_select
        self._on_human_select = on_human_select
        self._on_apply = on_apply
        self._on_toggle_battle_round = on_toggle_battle_round

    def build(self, scroll):
        nano4t_card = ctk.CTkFrame(
            scroll,
            corner_radius=6,
            fg_color="#3a3a3a",
            border_width=1,
            border_color="#555555",
        )
        nano4t_card.pack(fill="x", padx=8, pady=(8, 4))

        nano4t_title_frame = ctk.CTkFrame(nano4t_card, fg_color="transparent")
        nano4t_title_frame.pack(fill="x", padx=12, pady=(8, 2))
        ctk.CTkLabel(
            nano4t_title_frame,
            text="多人生化Buff选择",
            font=("Microsoft YaHei", 15, "bold"),
            text_color="#a7f3d0",
        ).pack(side="left")

        nano4t_top_frame = ctk.CTkFrame(nano4t_card, corner_radius=6, fg_color="#2b2b2b")
        nano4t_top_frame.pack(fill="x", padx=8, pady=(4, 4))
        nano4t_top_frame.grid_columnconfigure(0, weight=0)
        nano4t_top_frame.grid_columnconfigure(1, weight=1)
        nano4t_top_frame.grid_columnconfigure(2, weight=0)
        nano4t_status_dot = ctk.CTkLabel(nano4t_top_frame, text="⚫", font=("Arial", 18))
        nano4t_status_dot.grid(row=0, column=0, padx=(12, 4), pady=6)
        nano4t_status_label = ctk.CTkLabel(nano4t_top_frame, text="等待游戏启动...", font=("Microsoft YaHei", 14))
        nano4t_status_label.grid(row=0, column=1, padx=4, pady=6, sticky="w")
        nano4t_round_frame = ctk.CTkFrame(nano4t_top_frame, corner_radius=6, fg_color="#1a2a1a")
        nano4t_round_frame.grid(row=0, column=2, padx=(4, 8), pady=6)
        nano4t_round_label = ctk.CTkLabel(
            nano4t_round_frame,
            text="当前回合: 等待进入多人生化模式...",
            font=("Microsoft YaHei", 11),
            text_color="#88aa88",
        )
        nano4t_round_label.pack(padx=8, pady=4)

        nano4t_next_label = ctk.CTkLabel(nano4t_card, text="", font=("Microsoft YaHei", 11), text_color="#aaccaa")
        nano4t_next_label.pack(anchor="w", padx=16, pady=(0, 0))

        nano4t_sel_frame = ctk.CTkFrame(nano4t_card, corner_radius=8, fg_color="transparent")
        nano4t_sel_frame.pack(fill="x", padx=8, pady=2)
        nano4t_sel_frame.grid_columnconfigure(0, weight=1, uniform="n4col")
        nano4t_sel_frame.grid_columnconfigure(1, weight=1, uniform="n4col")

        ghost_frame = ctk.CTkFrame(nano4t_sel_frame, corner_radius=6, fg_color="#3a1a1a", height=170)
        ghost_frame.grid(row=0, column=0, sticky="nsew", padx=(8, 4), pady=(6, 4))
        ghost_frame.grid_propagate(False)
        ghost_header = ctk.CTkFrame(ghost_frame, fg_color="transparent")
        ghost_header.pack(anchor="w", padx=12, pady=(6, 2))
        ctk.CTkLabel(ghost_header, text="幽灵方特性", font=("Microsoft YaHei", 14, "bold"), text_color="#ff6666").pack(side="left")
        nano4t_ghost_status_label = ctk.CTkLabel(ghost_header, text="[未激活]", font=("Microsoft YaHei", 11), text_color="#888888")
        nano4t_ghost_status_label.pack(side="left", padx=(8, 0))

        ghost_display_text, ghost_desc_text = build_nano4t_selection_copy(self._attrs, self._temp_ghost)
        nano4t_ghost_var = ctk.StringVar(value=ghost_display_text)
        nano4t_ghost_combo = ctk.CTkComboBox(
            ghost_frame,
            values=build_nano4t_option_values(self._attrs, 0, 10),
            variable=nano4t_ghost_var,
            font=("Microsoft YaHei", 13),
            dropdown_font=("Microsoft YaHei", 12),
            height=34,
            state="readonly",
            command=self._on_ghost_select,
        )
        nano4t_ghost_combo.pack(fill="x", padx=12, pady=(4, 2))
        nano4t_ghost_desc = ctk.CTkLabel(ghost_frame, text=ghost_desc_text, font=("Microsoft YaHei", 11), text_color="#cc8888")
        nano4t_ghost_desc.pack(anchor="w", padx=12, pady=(2, 6))

        human_frame = ctk.CTkFrame(nano4t_sel_frame, corner_radius=6, fg_color="#1a1a3a", height=170)
        human_frame.grid(row=0, column=1, sticky="nsew", padx=(4, 8), pady=(6, 4))
        human_frame.grid_propagate(False)
        human_header = ctk.CTkFrame(human_frame, fg_color="transparent")
        human_header.pack(anchor="w", padx=12, pady=(6, 2))
        ctk.CTkLabel(human_header, text="人类方特性", font=("Microsoft YaHei", 14, "bold"), text_color="#6688ff").pack(side="left")
        nano4t_human_status_label = ctk.CTkLabel(human_header, text="[未激活]", font=("Microsoft YaHei", 11), text_color="#888888")
        nano4t_human_status_label.pack(side="left", padx=(8, 0))

        human_display_text, human_desc_text = build_nano4t_selection_copy(self._attrs, self._temp_human)
        nano4t_human_var = ctk.StringVar(value=human_display_text)
        nano4t_human_combo = ctk.CTkComboBox(
            human_frame,
            values=build_nano4t_option_values(self._attrs, 10, 20),
            variable=nano4t_human_var,
            font=("Microsoft YaHei", 13),
            dropdown_font=("Microsoft YaHei", 12),
            height=34,
            state="readonly",
            command=self._on_human_select,
        )
        nano4t_human_combo.pack(fill="x", padx=12, pady=(4, 2))
        nano4t_human_desc = ctk.CTkLabel(human_frame, text=human_desc_text, font=("Microsoft YaHei", 11), text_color="#8888cc")
        nano4t_human_desc.pack(anchor="w", padx=12, pady=(2, 6))

        btn_frame = ctk.CTkFrame(nano4t_card, corner_radius=8, fg_color="transparent")
        btn_frame.pack(fill="x", padx=8, pady=(2, 8))
        nano4t_apply_btn = ctk.CTkButton(btn_frame, text="✅ 应用", font=("Microsoft YaHei", 14, "bold"), height=38, command=self._on_apply, fg_color="#333333", state="disabled")
        nano4t_apply_btn.pack(fill="x", padx=12, pady=8)

        battle_round_frame = ctk.CTkFrame(scroll, corner_radius=6, fg_color="#3a2a1a", border_width=1, border_color="#555555")
        battle_round_frame.pack(fill="x", padx=8, pady=(4, 8))
        battle_round_top = ctk.CTkFrame(battle_round_frame, fg_color="transparent")
        battle_round_top.pack(fill="x", padx=12, pady=(8, 4))
        ctk.CTkLabel(battle_round_top, text="决战回合", font=("Microsoft YaHei", 14, "bold"), text_color="#FFB347").pack(side="left")
        battle_round_status_label = ctk.CTkLabel(
            battle_round_top,
            text="状态: 等待进入多人生化模式...",
            font=("Microsoft YaHei", 11),
            text_color="#888888",
        )
        battle_round_status_label.pack(side="left", padx=(12, 0))
        ctk.CTkLabel(battle_round_top, text="该功能开启后下一回合生效", font=("Microsoft YaHei", 11), text_color="#a0a0a0").pack(side="left", padx=(12, 0))
        battle_round_switch = ctk.CTkSwitch(battle_round_top, text="", font=("Microsoft YaHei", 12), command=self._on_toggle_battle_round, state="normal")
        battle_round_switch.pack(side="right")
        ctk.CTkLabel(battle_round_frame, text="每局强制触发决战回合（保底局）", font=("Microsoft YaHei", 11), text_color="#a0a0a0").pack(anchor="w", padx=12, pady=(0, 2))
        ctk.CTkLabel(battle_round_frame, text="决战回合：多人生化模式倒计时进入最后 30 秒，触发希望 buff", font=("Microsoft YaHei", 11), text_color="#a0a0a0").pack(anchor="w", padx=12, pady=(0, 8))

        inline_card_host = ctk.CTkFrame(scroll, fg_color="transparent")
        inline_card_host.pack(fill="x", padx=8, pady=(4, 8))

        return Nano4tViewHandles(
            nano4t_top_frame=nano4t_top_frame,
            nano4t_status_dot=nano4t_status_dot,
            nano4t_status_label=nano4t_status_label,
            nano4t_round_frame=nano4t_round_frame,
            nano4t_round_label=nano4t_round_label,
            nano4t_next_label=nano4t_next_label,
            nano4t_ghost_status_label=nano4t_ghost_status_label,
            nano4t_ghost_var=nano4t_ghost_var,
            nano4t_ghost_combo=nano4t_ghost_combo,
            nano4t_ghost_desc=nano4t_ghost_desc,
            nano4t_human_status_label=nano4t_human_status_label,
            nano4t_human_var=nano4t_human_var,
            nano4t_human_combo=nano4t_human_combo,
            nano4t_human_desc=nano4t_human_desc,
            nano4t_apply_btn=nano4t_apply_btn,
            battle_round_status_label=battle_round_status_label,
            battle_round_switch=battle_round_switch,
            inline_card_host=inline_card_host,
        )
