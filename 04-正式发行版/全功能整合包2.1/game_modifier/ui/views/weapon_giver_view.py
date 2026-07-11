from dataclasses import dataclass

import customtkinter as ctk

from core.weapon_catalog import TYPE_COLORS, WEAPON_LIST


WEAPON_GIVER_TITLE = "🔨 赋予武器"
RESPAWN_WEAPON_TEXT = "复活自动装备武器"
CURRENT_WEAPON_TEXT = "当前武器: 无"
GIVE_BUTTON_TEXT = "赋予"
HERO_TYPE_NAME = "英雄"
HOTKEY_BUTTON_TEXT = "⌨"
WEAPON_COLUMNS = 3
ROW_BUILD_BATCH_SIZE = 2


@dataclass
class WeaponGiverViewHandles:
    respawn_weapon_var: ctk.BooleanVar
    respawn_weapon_check: ctk.CTkCheckBox
    current_weapon_label: ctk.CTkLabel


class WeaponGiverView:
    def __init__(
        self,
        *,
        respawn_enabled,
        on_respawn_toggle,
        on_give_weapon,
        on_bind_hotkey,
        create_hotkey_badge,
        weapon_top_frames,
        weapon_hotkey_badges,
    ):
        self._weapons = WEAPON_LIST
        self._type_colors = TYPE_COLORS
        self._respawn_enabled = respawn_enabled
        self._on_respawn_toggle = on_respawn_toggle
        self._on_give_weapon = on_give_weapon
        self._on_bind_hotkey = on_bind_hotkey
        self._create_hotkey_badge = create_hotkey_badge
        self._weapon_top_frames = weapon_top_frames
        self._weapon_hotkey_badges = weapon_hotkey_badges

    def build(self, scroll):
        weapon_giver_frame = ctk.CTkFrame(scroll, corner_radius=8, fg_color="#2b2b2b")
        weapon_giver_frame.pack(fill="x", padx=8, pady=(8, 4))

        top_frame = ctk.CTkFrame(weapon_giver_frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(
            top_frame,
            text=WEAPON_GIVER_TITLE,
            font=("Microsoft YaHei", 16, "bold"),
            text_color="#FF6B6B",
        ).pack(side="left", padx=4)

        tools_frame = ctk.CTkFrame(weapon_giver_frame, fg_color="transparent")
        tools_frame.pack(fill="x", padx=8, pady=(4, 4))

        respawn_weapon_var = ctk.BooleanVar(value=self._respawn_enabled)
        respawn_weapon_check = ctk.CTkCheckBox(
            tools_frame,
            text=RESPAWN_WEAPON_TEXT,
            font=("Microsoft YaHei", 11),
            variable=respawn_weapon_var,
            command=lambda: self._on_respawn_toggle(respawn_weapon_var.get()),
        )
        respawn_weapon_check.pack(side="left", padx=4)

        current_weapon_label = ctk.CTkLabel(
            tools_frame,
            text=CURRENT_WEAPON_TEXT,
            font=("Microsoft YaHei", 11),
            text_color="#2ecc71",
        )
        current_weapon_label.pack(side="left", padx=8)

        self._build_weapon_list(weapon_giver_frame)

        return WeaponGiverViewHandles(
            respawn_weapon_var=respawn_weapon_var,
            respawn_weapon_check=respawn_weapon_check,
            current_weapon_label=current_weapon_label,
        )

    def _build_weapon_list(self, parent):
        self._batched_grid = BatchedWeaponGrid(
            weapons=self._weapons,
            type_colors=self._type_colors,
            on_give_weapon=self._on_give_weapon,
            on_bind_hotkey=self._on_bind_hotkey,
            create_hotkey_badge=self._create_hotkey_badge,
            weapon_top_frames=self._weapon_top_frames,
            weapon_hotkey_badges=self._weapon_hotkey_badges,
        )
        parent._batched_weapon_grid = self._batched_grid
        self._batched_grid.build(parent)


class BatchedWeaponGrid:
    def __init__(
        self,
        *,
        weapons,
        type_colors,
        on_give_weapon,
        on_bind_hotkey,
        create_hotkey_badge,
        weapon_top_frames,
        weapon_hotkey_badges,
    ):
        self._weapons = weapons
        self._type_colors = type_colors
        self._on_give_weapon = on_give_weapon
        self._on_bind_hotkey = on_bind_hotkey
        self._create_hotkey_badge = create_hotkey_badge
        self._weapon_top_frames = weapon_top_frames
        self._weapon_hotkey_badges = weapon_hotkey_badges
        self._rows = []
        self._host = None

    def build(self, parent):
        self._host = ctk.CTkFrame(parent, fg_color="transparent")
        self._host.pack(fill="x", padx=4, pady=(4, 8))
        self._rows = self._build_static_sections(self._host)
        self._host.after_idle(lambda: self._render_batch(0))

    def _build_static_sections(self, parent):
        weapons_by_type = {}
        for weapon in self._weapons:
            _, _, _, weapon_type = weapon
            weapons_by_type.setdefault(weapon_type, []).append(weapon)

        type_counts = [(weapon_type, len(weapons)) for weapon_type, weapons in weapons_by_type.items()]
        type_counts.sort(key=lambda item: item[1], reverse=True)

        rows = []
        for weapon_type, _ in type_counts:
            weapons = weapons_by_type[weapon_type]
            if not weapons:
                continue

            type_section = ctk.CTkFrame(
                parent,
                fg_color=self._type_colors.get(weapon_type, "#2b2b2b"),
                corner_radius=6,
            )
            type_section.pack(fill="x", padx=4, pady=(6, 3))

            ctk.CTkLabel(
                type_section,
                text=f"{weapon_type} ({len(weapons)})",
                font=("Microsoft YaHei", 12, "bold"),
                text_color="#ecf0f1",
                anchor="w",
            ).pack(fill="x", padx=10, pady=(6, 3))

            cards_frame = ctk.CTkFrame(type_section, fg_color="transparent")
            cards_frame.pack(fill="x", padx=6, pady=(0, 6))
            for col in range(WEAPON_COLUMNS):
                cards_frame.grid_columnconfigure(col, weight=1, uniform="weapon_col")

            for index in range(0, len(weapons), WEAPON_COLUMNS):
                rows.append({
                    "parent": cards_frame,
                    "row": index // WEAPON_COLUMNS,
                    "weapons": weapons[index:index + WEAPON_COLUMNS],
                })
        return rows

    def _render_batch(self, start_index):
        if self._host is None or not self._host.winfo_exists():
            return

        end_index = min(len(self._rows), start_index + ROW_BUILD_BATCH_SIZE)
        for row in self._rows[start_index:end_index]:
            self._create_weapon_row(row)

        if end_index < len(self._rows):
            self._host.after(1, lambda: self._render_batch(end_index))

    def _create_weapon_row(self, row):
        row_frame = ctk.CTkFrame(row["parent"], fg_color="transparent")
        row_frame.grid(row=row["row"], column=0, columnspan=WEAPON_COLUMNS, sticky="ew")
        for col in range(WEAPON_COLUMNS):
            row_frame.grid_columnconfigure(col, weight=1, uniform="weapon_col")
        for col, weapon in enumerate(row["weapons"]):
            self._create_weapon_card(row_frame, weapon, col)

    def _create_weapon_card(self, row_frame, weapon, col):
        weapon_id, _, cn_name, weapon_kind = weapon
        is_hero = weapon_kind == HERO_TYPE_NAME
        card = ctk.CTkFrame(
            row_frame,
            fg_color="#1a1a2e" if not is_hero else "#2c3e50",
            corner_radius=4,
        )
        card.grid(row=0, column=col, padx=3, pady=3, sticky="nsew")

        top_frame = ctk.CTkFrame(card, fg_color="transparent")
        top_frame.pack(fill="x", padx=3, pady=(3, 0))
        self._weapon_top_frames[weapon_id] = top_frame

        ctk.CTkLabel(
            top_frame,
            text=cn_name,
            font=("Microsoft YaHei", 10, "bold"),
            text_color="#ecf0f1",
            anchor="w",
        ).pack(side="left", padx=3, fill="x", expand=True)

        hotkey_badge = self._create_hotkey_badge(top_frame, weapon_id, cn_name)
        if hotkey_badge:
            hotkey_badge.pack(side="right", padx=3)
            self._weapon_hotkey_badges[weapon_id] = hotkey_badge

        actions_frame = ctk.CTkFrame(card, fg_color="transparent")
        actions_frame.pack(padx=3, pady=(1, 3))
        ctk.CTkButton(
            actions_frame,
            text=GIVE_BUTTON_TEXT,
            width=50,
            height=20,
            font=("Microsoft YaHei", 9),
            command=lambda wid=weapon_id, name=cn_name: self._on_give_weapon(wid, name),
            fg_color="#3498db" if not is_hero else "#e74c3c",
            hover_color="#2980b9" if not is_hero else "#c0392b",
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            actions_frame,
            text=HOTKEY_BUTTON_TEXT,
            width=20,
            height=20,
            font=("Microsoft YaHei", 9),
            command=lambda wid=weapon_id, name=cn_name: self._on_bind_hotkey(wid, name),
            fg_color="#9b59b6",
            hover_color="#8e44ad",
        ).pack(side="left", padx=2)
