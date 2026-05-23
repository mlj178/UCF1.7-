import customtkinter as ctk
import frida
import threading
import time
import json
import os

from core.config import FEATURES_INFO, NANO4T_ATTRS, DATA_DIR
from core.event_bus import EventBus
from core.frida_manager import FridaManager
from core.feature_registry import FeatureRegistry
from core.sound_manager import SoundManager
from core.hotkey_manager import HotkeyManager

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("游戏修改器控制台 - 全功能整合包 v1.6")
        self.geometry("610x700+10+10")
        self.resizable(True, True)
        self.minsize(610, 400)
        self.attributes('-topmost', True)
        self.attributes('-alpha', 0.92)

        self._event_bus = EventBus.get_instance()
        self._frida = FridaManager.get_instance()
        self._registry = FeatureRegistry.get_instance()
        self._sound = SoundManager.get_instance()
        self._hotkey = HotkeyManager.get_instance()

        self._connecting = False
        self._ready = False
        self._lock = threading.Lock()
        self._stop = False
        self._collapsed = False
        self._saved_geometry = "700x750+10+10"
        self._pid = None
        self._skip_count = 0
        self._gravity_debounce_timer = None
        self._monitoring = True

        self._features = {fid: False for fid in FEATURES_INFO}
        self._knife_speed = 5.0
        self._movespeed = 3.0
        self._range_mult = 50.0
        self._gravity = 1.0
        self._jump = 1.0
        self._gravity_mode = 'player_only'

        self._nano4t_ready = False
        _nano4t_cfg = self._load_nano4t_selector()
        self._nano4t_wanted_ghost = _nano4t_cfg.get('ghost', 9)
        self._nano4t_wanted_human = _nano4t_cfg.get('human', 19)
        self._nano4t_current_ghost = -1
        self._nano4t_current_human = -1
        self._nano4t_log_errors = False

        self.settings_window = None

        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()
        self._hotkey.set_app(self)
        self._hotkey.setup_hotkeys(self._on_hotkey_toggle, silent=True)
        self._setup_tk_hotkeys()
        self._setup_events()
        self._log("游戏修改器控制台 v1.6 — 全功能整合包 (模块化架构)")
        self._log("正在检测游戏进程...")

        threading.Thread(target=self._auto_connect_bg, daemon=True).start()
        threading.Thread(target=self._monitor_connection, daemon=True).start()
        threading.Thread(target=self._nano4t_auto_health_bg, daemon=True).start()

    def _build_ui(self):
        self._build_status_bar()
        self._build_hint_bar()
        self._build_tab_view()
        self._build_connect_button()
        self._build_log_panel()

    def _build_status_bar(self):
        self.status_frame = ctk.CTkFrame(self, corner_radius=8, fg_color="#2b2b2b")
        self.status_frame.pack(fill="x", padx=12, pady=(12, 6))
        self.status_dot = ctk.CTkLabel(self.status_frame, text="⚫", font=("Arial", 18))
        self.status_dot.pack(side="left", padx=(12, 4))
        self.status_label = ctk.CTkLabel(self.status_frame, text="等待游戏启动...",
                                          font=("Microsoft YaHei", 14))
        self.status_label.pack(side="left", padx=4)

        self.settings_btn = ctk.CTkButton(self.status_frame, text="⚙ 设置", width=70, height=28,
                                           font=("Microsoft YaHei", 11), command=self._show_settings,
                                           fg_color="#3a3a3a", hover_color="#555555")
        self.settings_btn.pack(side="right", padx=(4, 8))

        self.collapse_btn = ctk.CTkButton(self.status_frame, text="▼ 折叠界面", width=100, height=28,
                                            font=("Microsoft YaHei", 12), command=self._toggle_collapse,
                                            fg_color="#3a3a3a", hover_color="#555555")
        self.collapse_btn.pack(side="right", padx=(4, 8))
        self.pid_label = ctk.CTkLabel(self.status_frame, text="", font=("Microsoft YaHei", 11),
                                       text_color="#888")
        self.pid_label.pack(side="right", padx=12)

    def _build_hint_bar(self):
        self.hint_frame = ctk.CTkFrame(self, corner_radius=6, fg_color="#2a2a00")
        self.hint_frame.pack(fill="x", padx=12, pady=(2, 8))
        self.hint_label = ctk.CTkLabel(self.hint_frame,
                                        text="① 启动游戏 → ② 进入任意模式 → ③ 打开本工具 → ④ 开启功能开关",
                                        font=("Microsoft YaHei", 11), text_color="#ffcc00", wraplength=760)
        self.hint_label.pack(padx=8, pady=4)

    def _build_tab_view(self):
        self.tab_view = ctk.CTkTabview(self, corner_radius=8)
        self.tab_view.pack(fill="both", padx=12, pady=4, expand=True)
        tab_weapon = self.tab_view.add("武器")
        tab_player = self.tab_view.add("人物属性")
        tab_other = self.tab_view.add("其他")
        tab_nano4t = self.tab_view.add("多人生化Buff选择")

        tab_weapon_scroll = ctk.CTkScrollableFrame(tab_weapon, corner_radius=0, fg_color="transparent")
        tab_weapon_scroll.pack(fill="both", expand=True, padx=2, pady=2)
        tab_player_scroll = ctk.CTkScrollableFrame(tab_player, corner_radius=0, fg_color="transparent")
        tab_player_scroll.pack(fill="both", expand=True, padx=2, pady=2)
        tab_other_scroll = ctk.CTkScrollableFrame(tab_other, corner_radius=0, fg_color="transparent")
        tab_other_scroll.pack(fill="both", expand=True, padx=2, pady=2)
        tab_nano4t_scroll = ctk.CTkScrollableFrame(tab_nano4t, corner_radius=0, fg_color="transparent")
        tab_nano4t_scroll.pack(fill="both", expand=True, padx=2, pady=2)

        self._build_weapon_tab(tab_weapon_scroll)
        self._build_player_tab(tab_player_scroll)
        self._build_other_tab(tab_other_scroll)
        self._build_nano4t_tab(tab_nano4t_scroll)

    def _make_feature_card(self, parent, row, col, colspan, color, feature_id, icon, name, desc,
                           has_slider=False, slider_callback=None, slider_var=None, slider_range=None,
                           title_color=None):
        bg_color = "#3a3a3a"
        text_color = "#e0e0e0"
        title_text_color = title_color if title_color else text_color

        f = ctk.CTkFrame(parent, corner_radius=6, fg_color=bg_color, border_width=1,
                          border_color="#555555", cursor="hand2")
        f.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)

        top_frame = ctk.CTkFrame(f, fg_color="transparent")
        top_frame.pack(fill="x", padx=8, pady=(6, 0))

        ctk.CTkLabel(top_frame, text=f"{icon} {name}", font=("Microsoft YaHei", 15, "bold"),
                     text_color=title_text_color).pack(side="left", padx=4)

        f.bind("<Button-1>", lambda e: self._toggle_feature(feature_id))

        slider_label_ref = None
        if has_slider and slider_var and slider_range:
            slider = ctk.CTkSlider(top_frame, from_=slider_range[0], to=slider_range[1],
                                    variable=slider_var,
                                    number_of_steps=int((slider_range[1] - slider_range[0]) * 10),
                                    command=slider_callback, width=90)
            slider.pack(side="left", padx=4)
            slider_label_ref = ctk.CTkLabel(top_frame, text=f"{slider_var.get()}x",
                                             font=("Microsoft YaHei", 11), text_color=text_color,
                                             width=35)
            slider_label_ref.pack(side="left")
            slider_var.trace_add("write",
                                  lambda *args: slider_label_ref.configure(
                                      text=f"{slider_var.get():.1f}x"))

        switch = ctk.CTkSwitch(top_frame, text="", font=("Microsoft YaHei", 12),
                                width=50, command=lambda: self._toggle_feature(feature_id))
        switch.pack(side="right", padx=6)

        wrap_width = 280 * colspan
        ctk.CTkLabel(f, font=("Microsoft YaHei", 15), text=desc, text_color="#a0a0a0",
                     wraplength=wrap_width, justify="left", anchor="w").pack(fill="x", padx=8,
                                                                               pady=(2, 6),
                                                                               expand=False)

        return f, switch, slider_label_ref

    def _build_weapon_tab(self, scroll):
        for i in range(2):
            scroll.grid_columnconfigure(i, weight=1, uniform="wcol")

        self.knife_speed_var = ctk.DoubleVar(value=5.0)
        _, self.knife_switch, self.knife_speed_label = self._make_feature_card(
            scroll, 0, 0, 1, "#3a1a1a", 'knife', '🔪', '快刀',
            '提升挥刀速度（人类+生化幽灵通用）', has_slider=True,
            slider_callback=self._on_knife_speed_change, slider_var=self.knife_speed_var,
            slider_range=(1.0, 10.0), title_color="#FFB347")

        _, self.recoil_switch, _ = self._make_feature_card(
            scroll, 0, 1, 1, "#1a1a3a", 'recoil', '🎯', '无后座力',
            '消除所有枪械后座力', title_color="#6A9FB5")

        _, self.ammo_switch, _ = self._make_feature_card(
            scroll, 1, 0, 1, "#3a2a1a", 'ammo', '🔫', '无限子弹',
            '子弹永不消耗', title_color="#E5B73B")

        _, self.ammoplus_switch, _ = self._make_feature_card(
            scroll, 1, 1, 1, "#3a1a2a", 'ammoplus', '⚡', '快速换弹',
            '换弹速度加快', title_color="#D4AF37")

        self.range_var = ctk.DoubleVar(value=50.0)
        _, self.range_switch, self.range_label = self._make_feature_card(
            scroll, 2, 0, 2, "#1a2a1a", 'range', '⚔️', '剑气化丝',
            '扩大近战攻击距离（人类+生化幽灵通用）', has_slider=True,
            slider_callback=self._on_range_change, slider_var=self.range_var,
            slider_range=(1.0, 50.0), title_color="#AF69EF")

        _, self.aim_switch, _ = self._make_feature_card(
            scroll, 3, 0, 1, "#2a1a3a", 'aim', '🎯', '自瞄',
            '自动瞄准敌方玩家', title_color="#FF6B6B")

        _, self.speedgun_switch, _ = self._make_feature_card(
            scroll, 3, 1, 1, "#3a3a1a", 'speedgun', '⚡', '射速变快',
            '大幅提升枪械射速', title_color="#FFD93D")

    def _build_player_tab(self, scroll):
        for i in range(2):
            scroll.grid_columnconfigure(i, weight=1, uniform="pcol")

        self.move_speed_var = ctk.DoubleVar(value=3.0)
        _, self.move_switch, self.move_speed_label = self._make_feature_card(
            scroll, 0, 0, 1, "#1a2a3a", 'movespeed', '👟', '滑板鞋',
            '提升移动速度', has_slider=True,
            slider_callback=self._on_move_speed_change, slider_var=self.move_speed_var,
            slider_range=(1.0, 6.0), title_color="#5FAD56")

        _, self.time_switch, _ = self._make_feature_card(
            scroll, 0, 1, 1, "#1a2a1a", 'time', '⏰', '无限时间',
            '设定时间为99:59', title_color="#4C9F9F")

        self._build_gravity_card(scroll, 1)

        _, self.godmode_switch, _ = self._make_feature_card(
            scroll, 2, 0, 2, "#3a1a1a", 'godmode', '🛡️', '金刚不坏',
            '角色受到攻击时不会受伤', title_color="#E74C3C")

        _, self.skillcd_switch, _ = self._make_feature_card(
            scroll, 3, 0, 1, "#3a2a3a", 'skillcd', '✨', '技能无冷却',
            '生化模式，所有技能无冷却', title_color="#A855F7")

    def _build_gravity_card(self, parent, row):
        gravity_frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="#3a3a3a",
                                      border_width=1, border_color="#555555", cursor="hand2")
        gravity_frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=3, pady=3)
        gravity_frame.bind("<Button-1>", lambda e: self._toggle_feature('gravity'))

        top9 = ctk.CTkFrame(gravity_frame, fg_color="transparent")
        top9.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top9, text="🌌 轻重力/高跳", font=("Microsoft YaHei", 15, "bold"),
                     text_color="#F4A261").pack(side="left", padx=4)
        self.gravity_switch = ctk.CTkSwitch(top9, text="", font=("Microsoft YaHei", 12),
                                             width=50, command=lambda: self._toggle_feature('gravity'))
        self.gravity_switch.pack(side="right", padx=12)

        gravity_slider_frame = ctk.CTkFrame(gravity_frame, fg_color="transparent")
        gravity_slider_frame.pack(fill="x", padx=8, pady=(4, 0))
        ctk.CTkLabel(gravity_slider_frame, text="重力:", font=("Microsoft YaHei", 11),
                     text_color="#e0e0e0").pack(side="left", padx=(4, 2))
        self.gravity_var = ctk.DoubleVar(value=1.0)
        self.gravity_slider = ctk.CTkSlider(gravity_slider_frame, from_=0.0, to=1.0,
                                              variable=self.gravity_var, number_of_steps=10,
                                              command=self._on_gravity_change, width=100)
        self.gravity_slider.pack(side="left", padx=2)
        self.gravity_label = ctk.CTkLabel(gravity_slider_frame, text="1.0",
                                           font=("Microsoft YaHei", 11), text_color="#e0e0e0",
                                           width=28)
        self.gravity_label.pack(side="left", padx=(2, 6))
        ctk.CTkLabel(gravity_slider_frame, text="跳跃:", font=("Microsoft YaHei", 11),
                     text_color="#e0e0e0").pack(side="left", padx=(4, 2))
        self.jump_var = ctk.DoubleVar(value=1.0)
        self.jump_slider = ctk.CTkSlider(gravity_slider_frame, from_=1.0, to=5.0,
                                           variable=self.jump_var, number_of_steps=8,
                                           command=self._on_jump_change, width=100)
        self.jump_slider.pack(side="left", padx=2)
        self.jump_label = ctk.CTkLabel(gravity_slider_frame, text="1.0",
                                        font=("Microsoft YaHei", 11), text_color="#e0e0e0",
                                        width=28)
        self.jump_label.pack(side="left", padx=2)

        gravity_mode_frame = ctk.CTkFrame(gravity_frame, fg_color="transparent")
        gravity_mode_frame.pack(fill="x", padx=8, pady=(2, 2))
        ctk.CTkLabel(gravity_mode_frame, text="生效范围:", font=("Microsoft YaHei", 11),
                     text_color="#e0e0e0").pack(side="left", padx=(4, 4))
        self.gravity_mode_var = ctk.StringVar(value="仅自己")
        self.gravity_mode_combo = ctk.CTkComboBox(gravity_mode_frame,
                                                    values=["仅自己", "全部玩家"],
                                                    variable=self.gravity_mode_var,
                                                    font=("Microsoft YaHei", 12),
                                                    height=30, width=120, state="readonly",
                                                    command=self._on_gravity_mode_change)
        self.gravity_mode_combo.pack(side="left", padx=4)
        ctk.CTkLabel(gravity_frame, font=("Microsoft YaHei", 15), text="调整重力与跳跃倍率",
                     text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(
            fill="x", expand=False, padx=5, pady=5)

    def _build_other_tab(self, scroll):
        for i in range(2):
            scroll.grid_columnconfigure(i, weight=1, uniform="ocol")

        gather_frame = ctk.CTkFrame(scroll, corner_radius=6, fg_color="#3a3a3a",
                                     border_width=1, border_color="#555555", cursor="hand2")
        gather_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=3, pady=3)
        gather_frame.bind("<Button-1>", lambda e: self._toggle_feature('gather'))

        top8 = ctk.CTkFrame(gather_frame, fg_color="transparent")
        top8.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top8, text="👾 聚怪", font=("Microsoft YaHei", 15, "bold"),
                     text_color="#E76F51").pack(side="left", padx=4)
        self.gather_switch = ctk.CTkSwitch(top8, text="启用追踪", font=("Microsoft YaHei", 12),
                                            width=50, command=lambda: self._toggle_feature('gather'))
        self.gather_switch.pack(side="right", padx=12)

        gather_btn_frame = ctk.CTkFrame(gather_frame, fg_color="transparent")
        gather_btn_frame.pack(fill="x", padx=8, pady=(2, 2))
        self.gather_btn = ctk.CTkButton(gather_btn_frame, text="📍 一键聚怪",
                                          font=("Microsoft YaHei", 14, "bold"),
                                          height=45, command=self._gather,
                                          fg_color="#b45309", hover_color="#92400e")
        self.gather_btn.pack(fill="x", padx=4, pady=4)
        ctk.CTkLabel(gather_frame, font=("Microsoft YaHei", 15),
                     text="将所有人机聚集。一般用于多人生化模式",
                     text_color="#a0a0a0", wraplength=560, justify="left", anchor="w").pack(
            fill="x", expand=False, padx=5, pady=5)

        _, self.isbot_switch, _ = self._make_feature_card(
            scroll, 1, 0, 2, "#1a3a3a", 'isbot', '🧠', '天机傀儡',
            '玩家由人机控制，化身机器傀儡（开启后，重新进入房间才能生效）',
            title_color="#00D4FF")

        skip_frame = ctk.CTkFrame(scroll, corner_radius=6, fg_color="#3a3a3a",
                                   border_width=1, border_color="#555555")
        skip_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=3, pady=3)
        top10 = ctk.CTkFrame(skip_frame, fg_color="transparent")
        top10.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top10, text="⏭️ 回合跳过", font=("Microsoft YaHei", 15, "bold"),
                     text_color="#e0e0e0").pack(side="left", padx=4)
        self.skip_count_label = ctk.CTkLabel(top10, text="已跳过: 0 回合",
                                              font=("Microsoft YaHei", 11), text_color="#a0a0a0")
        self.skip_count_label.pack(side="right", padx=12)

        skip_btn_frame = ctk.CTkFrame(skip_frame, fg_color="transparent")
        skip_btn_frame.pack(fill="x", padx=8, pady=(2, 2))
        self.skip_round_btn = ctk.CTkButton(skip_btn_frame, text="▶ 第一次跳过需要点击两次",
                                              font=("Microsoft YaHei", 14, "bold"),
                                              height=45, command=self._skip_round,
                                              fg_color="#b45309", hover_color="#92400e")
        self.skip_round_btn.pack(fill="x", padx=4, pady=4)
        ctk.CTkLabel(skip_frame, font=("Microsoft YaHei", 15), text="结束当前回合（需要等待几秒）",
                     text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(
            fill="x", expand=False, padx=5, pady=5)

    def _build_nano4t_tab(self, scroll):
        self.nano4t_top_frame = ctk.CTkFrame(scroll, corner_radius=8, fg_color="#2b2b2b")
        self.nano4t_top_frame.pack(fill="x", padx=8, pady=(8, 4))
        self.nano4t_top_frame.grid_columnconfigure(0, weight=0)
        self.nano4t_top_frame.grid_columnconfigure(1, weight=1)
        self.nano4t_top_frame.grid_columnconfigure(2, weight=0)
        self.nano4t_status_dot = ctk.CTkLabel(self.nano4t_top_frame, text="⚫", font=("Arial", 18))
        self.nano4t_status_dot.grid(row=0, column=0, padx=(12, 4), pady=6)
        self.nano4t_status_label = ctk.CTkLabel(self.nano4t_top_frame, text="等待游戏启动...",
                                                  font=("Microsoft YaHei", 14))
        self.nano4t_status_label.grid(row=0, column=1, padx=4, pady=6, sticky="w")
        self.nano4t_round_frame = ctk.CTkFrame(self.nano4t_top_frame, corner_radius=6,
                                                 fg_color="#1a2a1a")
        self.nano4t_round_frame.grid(row=0, column=2, padx=(4, 8), pady=6)
        self.nano4t_round_label = ctk.CTkLabel(self.nano4t_round_frame,
                                                 text="当前回合: 等待进入多人生化模式...",
                                                 font=("Microsoft YaHei", 11), text_color="#88aa88")
        self.nano4t_round_label.pack(padx=8, pady=4)

        self.nano4t_next_label = ctk.CTkLabel(scroll, text="",
                                                font=("Microsoft YaHei", 11), text_color="#aaccaa")
        self.nano4t_next_label.pack(anchor="w", padx=16, pady=(0, 0))

        nano4t_sel_frame = ctk.CTkFrame(scroll, corner_radius=8)
        nano4t_sel_frame.pack(fill="x", padx=8, pady=2)
        nano4t_sel_frame.grid_columnconfigure(0, weight=1, uniform="n4col")
        nano4t_sel_frame.grid_columnconfigure(1, weight=1, uniform="n4col")

        nano4t_ghost_frame = ctk.CTkFrame(nano4t_sel_frame, corner_radius=6, fg_color="#3a1a1a",
                                            height=170)
        nano4t_ghost_frame.grid(row=0, column=0, sticky="nsew", padx=(8, 4), pady=(6, 4))
        nano4t_ghost_frame.grid_propagate(False)
        ctk.CTkLabel(nano4t_ghost_frame, text="👻 幽灵方特性",
                     font=("Microsoft YaHei", 14, "bold"), text_color="#ff6666").pack(
            anchor="w", padx=12, pady=(6, 2))
        self.nano4t_ghost_var = ctk.StringVar(
            value=f"{self._nano4t_wanted_ghost}: {NANO4T_ATTRS[self._nano4t_wanted_ghost][0]}")
        self.nano4t_ghost_combo = ctk.CTkComboBox(
            nano4t_ghost_frame,
            values=[f"{i}: {NANO4T_ATTRS[i][0]}" for i in range(10)],
            variable=self.nano4t_ghost_var, font=("Microsoft YaHei", 13),
            dropdown_font=("Microsoft YaHei", 12), height=34, state="readonly",
            command=self._nano4t_on_ghost_select)
        self.nano4t_ghost_combo.pack(fill="x", padx=12, pady=(4, 2))
        self.nano4t_ghost_desc = ctk.CTkLabel(
            nano4t_ghost_frame,
            text="效果: " + NANO4T_ATTRS[self._nano4t_wanted_ghost][1],
            font=("Microsoft YaHei", 11), text_color="#cc8888")
        self.nano4t_ghost_desc.pack(anchor="w", padx=12, pady=(2, 6))

        nano4t_human_frame = ctk.CTkFrame(nano4t_sel_frame, corner_radius=6, fg_color="#1a1a3a",
                                            height=170)
        nano4t_human_frame.grid(row=0, column=1, sticky="nsew", padx=(4, 8), pady=(6, 4))
        nano4t_human_frame.grid_propagate(False)
        ctk.CTkLabel(nano4t_human_frame, text="🛡️ 人类方特性",
                     font=("Microsoft YaHei", 14, "bold"), text_color="#6688ff").pack(
            anchor="w", padx=12, pady=(6, 2))
        self.nano4t_human_var = ctk.StringVar(
            value=f"{self._nano4t_wanted_human}: {NANO4T_ATTRS[self._nano4t_wanted_human][0]}")
        self.nano4t_human_combo = ctk.CTkComboBox(
            nano4t_human_frame,
            values=[f"{i}: {NANO4T_ATTRS[i][0]}" for i in range(10, 20)],
            variable=self.nano4t_human_var, font=("Microsoft YaHei", 13),
            dropdown_font=("Microsoft YaHei", 12), height=34, state="readonly",
            command=self._nano4t_on_human_select)
        self.nano4t_human_combo.pack(fill="x", padx=12, pady=(4, 2))
        self.nano4t_human_desc = ctk.CTkLabel(
            nano4t_human_frame,
            text="效果: " + NANO4T_ATTRS[self._nano4t_wanted_human][1],
            font=("Microsoft YaHei", 11), text_color="#8888cc")
        self.nano4t_human_desc.pack(anchor="w", padx=12, pady=(2, 6))

        nano4t_btn_frame = ctk.CTkFrame(scroll, corner_radius=8)
        nano4t_btn_frame.pack(fill="x", padx=8, pady=(2, 4))
        self.nano4t_apply_btn = ctk.CTkButton(nano4t_btn_frame, text="✅ 应用",
                                                font=("Microsoft YaHei", 14, "bold"),
                                                height=38, command=self._nano4t_apply,
                                                fg_color="#333333", state="disabled")
        self.nano4t_apply_btn.pack(side="left", padx=(12, 6), pady=8, expand=True)
        self.nano4t_connect_btn = ctk.CTkButton(nano4t_btn_frame, text="🔗 连接多人生化",
                                                  font=("Microsoft YaHei", 13),
                                                  height=38, command=self._nano4t_connect,
                                                  fg_color="#2a6e2a")
        self.nano4t_connect_btn.pack(side="left", padx=(6, 12), pady=8, expand=True)

    def _build_connect_button(self):
        self.btn_frame = ctk.CTkFrame(self, corner_radius=8)
        self.btn_frame.pack(fill="x", padx=12, pady=(2, 6))
        self.connect_btn = ctk.CTkButton(self.btn_frame, text="🔗 连接游戏",
                                           font=("Microsoft YaHei", 13),
                                           height=40, command=self._connect,
                                           fg_color="#2a6e2a")
        self.connect_btn.pack(fill="x", padx=12, pady=10)

    def _build_log_panel(self):
        self.log_box = ctk.CTkTextbox(self, font=("Consolas", 11),
                                        wrap="word", height=80, state="disabled")
        self.log_box.pack(fill="x", padx=12, pady=(2, 12))

    def _setup_events(self):
        self._event_bus.subscribe('log_message', self._on_log_message)
        self._event_bus.subscribe('connection_status', self._on_connection_status)
        self._event_bus.subscribe('feature_status_changed', self._on_feature_status)
        self._event_bus.subscribe('gather_result', self._on_gather_result)
        self._event_bus.subscribe('round_skipped', self._on_round_skipped)
        self._event_bus.subscribe('nano4t_event', self._on_nano4t_event)

    def _on_log_message(self, **kwargs):
        level = kwargs.get('level', 'info')
        module = kwargs.get('module', '')
        message = kwargs.get('message', '')
        icon_map = {'success': '✅', 'error': '❌', 'info': 'ℹ️', 'warn': '⚠️'}
        icon = icon_map.get(level, 'ℹ️')
        self._log(f"{icon} [{module}] {message}")

    def _on_connection_status(self, **kwargs):
        status = kwargs.get('status', 'disconnected')
        pid = kwargs.get('pid')

        def update():
            if status == 'connected':
                self._set_status("green", "已连接")
                self.pid_label.configure(text=f"PID: {pid}")
                self._ready = True
                self._pid = pid
                self._restore_features()
                threading.Thread(target=self._nano4t_auto_init_bg, daemon=True).start()
            elif status == 'not_found':
                self._set_status("yellow", "未找到游戏")
            else:
                self._set_status("red", "连接断开，正在重连...")
                self._ready = False

        self.after(0, update)

    def _on_feature_status(self, **kwargs):
        feature_id = kwargs.get('feature', '')
        enabled = kwargs.get('enabled', False)
        self._features[feature_id] = enabled
        self.after(0, lambda: self._update_switch(feature_id))

    def _on_gather_result(self, **kwargs):
        data = kwargs.get('data', {})
        ok = data.get('ok', False)
        if ok:
            bots = data.get('bots', 0)
            fail = data.get('fail', 0)
            self._log(f"✅ 聚怪结果: 传送成功{bots} 失败{fail}")
        else:
            self._log(f"❌ 聚怪失败: {data.get('msg', '未知')}")

    def _on_round_skipped(self, **kwargs):
        count = kwargs.get('count', 0)
        self._skip_count = count
        self.after(0, lambda: self.skip_count_label.configure(text=f"已跳过: {count} 回合"))
        self._log(f"⏭️ 回合已跳过! (累计: {count})")

    def _on_nano4t_event(self, **kwargs):
        event_type = kwargs.get('msg_type', '')
        payload = kwargs.get('payload', {})

        if event_type == 'nano4t_ready':
            ids = payload.get('ids', [])
            self._nano4t_ready = True
            self.after(0, lambda: self._nano4t_on_ready(len(ids)))
        elif event_type == 'nano4t_destroyed':
            if self._nano4t_ready:
                self._log("⚠ 检测到退出多人生化房间，特性系统已销毁")
            self._nano4t_ready = False
            self.after(0, self._nano4t_on_destroyed)
        elif event_type == 'nano4t_error':
            self._nano4t_ready = False
            if self._nano4t_log_errors:
                self._nano4t_log_errors = False
                m = payload.get('msg', '')
                if '未检测到游戏' in m:
                    self._log("⚠ [多人生化] 未检测到游戏进程")
                elif '未进入多人生化模式' in m:
                    self._log("⚠ [多人生化] 检测到游戏，但尚未进入「多人生化模式」")
                    self._log("  请选择多人生化模式并进入房间")
                elif '房间' in m:
                    self._log("⚠ [多人生化] 已在多人生化模式菜单，但尚未进入房间")
                else:
                    self._log(f"❌ [多人生化] {m}")
            self.after(0, lambda: self._nano4t_set_status("yellow", "未就绪"))
        elif event_type == 'nano4t_set':
            g = int(payload.get('g', 0))
            h = int(payload.get('h', 0))
            self._nano4t_wanted_ghost = g
            self._nano4t_wanted_human = h
            self._log(
                f"✅ [多人生化] 已锁定: {NANO4T_ATTRS[g][0]} + {NANO4T_ATTRS[h][0]}，下一回合生效")
            self.after(0, self._nano4t_refresh_next_label)
        elif event_type == 'nano4t_current':
            g = int(payload.get('g', -1))
            h = int(payload.get('h', -1))
            self.after(0, lambda gg=g, hh=h: self._nano4t_update_round_label(gg, hh))
        elif event_type == 'nano4t_dead':
            if self._nano4t_ready:
                self._log("⚠ [多人生化] 模式实例已失效")
                self._nano4t_ready = False
                self.after(0, self._nano4t_on_destroyed)
        elif event_type == 'nano4t_alive':
            if not self._nano4t_ready and self._ready:
                self._log("ℹ️ [多人生化] 检测到已进入多人生化模式，正在初始化...")
                threading.Thread(target=self._nano4t_auto_init_if_needed, daemon=True).start()

    def _log(self, msg):
        ts = time.strftime("%H:%M:%S")
        self.after(0, lambda: self._log_ui(ts, msg))

    def _log_ui(self, ts, msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{ts}] {msg}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _set_status(self, color, text):
        dot_map = {"green": "🟢", "yellow": "🟡", "red": "🔴", "gray": "⚫"}
        self.status_dot.configure(text=dot_map.get(color, "⚫"))
        self.status_label.configure(text=text)
        if color == "green":
            self.hint_frame.configure(fg_color="#1a3a1a")
            self.hint_label.configure(text_color="#88ff88")
            self.hint_label.configure(text="✅ 已连接！点击功能按钮开启修改")
        elif color == "red":
            self.hint_frame.configure(fg_color="#3a1a1a")
            self.hint_label.configure(text_color="#ff8888")
            self.hint_label.configure(text="连接断开，正在重连...")
        else:
            self.hint_frame.configure(fg_color="#2a2a00")
            self.hint_label.configure(text_color="#ffcc00")
            self.hint_label.configure(
                text="① 启动游戏 → ② 进入任意模式 → ③ 打开本工具 → ④ 开启功能开关")

    def _toggle_feature(self, feature_id):
        if not self._ready:
            self._log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return

        new_state = not self._features.get(feature_id, False)
        self._features[feature_id] = new_state

        if feature_id == 'knife':
            self._frida.send_toggle('knife', new_state)
            if new_state:
                self._frida.send_toggle('knife_speed', self._knife_speed)
        elif feature_id == 'movespeed':
            self._frida.send_toggle('movespeed', new_state)
            if new_state:
                self._frida.send_toggle('movespeed_speed', self._movespeed)
        elif feature_id == 'range':
            self._frida.send_toggle('range', new_state)
            if new_state:
                self._frida.send_toggle('range_config', self._range_mult)
        elif feature_id == 'gravity':
            self._frida.send_toggle('gravity', new_state)
            if new_state:
                self._do_send_gravity_config()
        else:
            self._frida.send_toggle(feature_id, new_state)

        self._sound.play_toggle_sound()
        self._update_switch(feature_id)

    def _update_switch(self, feature_id):
        switch_map = {
            'knife': self.knife_switch, 'time': self.time_switch,
            'recoil': self.recoil_switch, 'ammo': self.ammo_switch,
            'movespeed': self.move_switch, 'ammoplus': self.ammoplus_switch,
            'range': self.range_switch, 'gather': self.gather_switch,
            'gravity': self.gravity_switch, 'aim': self.aim_switch,
            'godmode': self.godmode_switch, 'speedgun': self.speedgun_switch,
            'isbot': self.isbot_switch, 'skillcd': self.skillcd_switch,
        }
        switch = switch_map.get(feature_id)
        if not switch:
            return
        enabled = self._features.get(feature_id, False)
        if enabled:
            switch.select()
        else:
            switch.deselect()

    def _on_knife_speed_change(self, value):
        self._knife_speed = round(float(value), 1)
        if self._features.get('knife'):
            self._frida.send_toggle('knife_speed', self._knife_speed)

    def _on_move_speed_change(self, value):
        self._movespeed = round(float(value), 1)
        if self._features.get('movespeed'):
            self._frida.send_toggle('movespeed_speed', self._movespeed)

    def _on_range_change(self, value):
        self._range_mult = round(float(value), 1)
        if self._features.get('range'):
            self._frida.send_toggle('range_config', self._range_mult)

    def _on_gravity_change(self, value):
        self._gravity = round(float(value), 1)
        self.gravity_label.configure(text=f"{self._gravity:.1f}")
        self._debounce_gravity_config()

    def _on_jump_change(self, value):
        self._jump = round(float(value), 1)
        self.jump_label.configure(text=f"{self._jump:.1f}")
        self._debounce_gravity_config()

    def _on_gravity_mode_change(self, value):
        self._gravity_mode = 'player_only' if value == "仅自己" else 'all'
        self._debounce_gravity_config()

    def _debounce_gravity_config(self):
        if self._gravity_debounce_timer:
            self.after_cancel(self._gravity_debounce_timer)
        self._gravity_debounce_timer = self.after(300, self._do_send_gravity_config)

    def _do_send_gravity_config(self):
        if self._features.get('gravity'):
            self._frida.send_toggle('gravity_config', {
                'g': self._gravity, 'j': self._jump, 'm': self._gravity_mode
            })

    def _gather(self):
        if not self._ready:
            self._log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return
        if not self._features.get('gather'):
            self._log("⚠ 聚怪功能未启用，请先打开「启用追踪」开关")
            return

        self._log("📍 正在聚怪（传送所有 Bot 到佣兵出生点）...")
        self.gather_btn.configure(state="disabled", text="⏳ 聚怪中...")

        def do_gather():
            try:
                result = self._frida.call_export('gather')
                if result:
                    ok = result.get('ok', False)
                    if ok:
                        bots = result.get('bots', 0)
                        fail = result.get('fail', 0)
                        self._log(f"✅ 聚怪完成! 成功{bots} 失败{fail}")
                    else:
                        self._log(f"❌ 聚怪失败: {result.get('msg', '未知错误')}")
            except Exception as e:
                self._log(f"❌ 聚怪异常: {e}")
            finally:
                self.after(0, lambda: self.gather_btn.configure(state="normal",
                                                                text="📍 一键聚怪"))

        threading.Thread(target=do_gather, daemon=True).start()

    def _skip_round(self):
        if not self._ready:
            self._log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return

        self._log("⏭️ 正在跳过当前回合...")
        self.skip_round_btn.configure(state="disabled", text="⏳ 跳转中...")

        def do_skip():
            try:
                result = self._frida.call_export('roundskip')
                if result:
                    ok = result.get('ok', False)
                    if ok:
                        self._log("✅ 回合跳过成功！")
                    else:
                        reason = result.get('reason', '未知错误')
                        if reason == 'no_instance':
                            self._log("⚠ 未能获取到游戏回合实例，请确保已进入游戏模式")
                        elif reason == 'already_zero':
                            self._log("⚠ 回合时间已为 0:00，无需跳过")
                        else:
                            self._log(f"❌ 跳过失败: {reason}")
            except Exception as e:
                self._log(f"❌ 跳过异常: {e}")
            finally:
                self.after(0, lambda: self.skip_round_btn.configure(state="normal",
                                                                     text="▶ 跳过当前回合"))

        threading.Thread(target=do_skip, daemon=True).start()

    def _connect(self):
        if self._connecting:
            return
        self._cleanup()
        threading.Thread(target=self._connect_bg, daemon=True).start()

    def _connect_bg(self):
        pid = self._frida.find_pid()
        if not pid:
            self._log("⚠ 未检测到游戏进程，请先启动 UnityCrossFire.exe")
            return
        self._do_connect(pid)

    def _do_connect(self, pid):
        with self._lock:
            if self._connecting:
                return
            self._connecting = True

        self._log(f"检测到游戏 PID:{pid}，正在连接...")
        try:
            success = self._frida.connect(pid)
            if not success:
                self._connecting = False
        except Exception as e:
            self._log(f"❌ 连接失败: {e}")
        finally:
            self._connecting = False

    def _auto_connect_bg(self):
        time.sleep(2)
        while not self._stop:
            if self._connecting:
                time.sleep(5)
                continue
            pid = self._frida.find_pid()
            if pid and not self._ready:
                self._do_connect(pid)
            time.sleep(5)

    def _monitor_connection(self):
        while not self._stop:
            time.sleep(2)
            if not self._ready:
                continue
            try:
                self._frida.call_export('getGravityStatus')
            except (frida.InvalidOperationError, frida.TransportError):
                self._on_disconnected()
            except Exception:
                pass

    def _on_disconnected(self):
        if not self._ready:
            return
        self._log("🔴 连接已断开，正在重连...")
        self._ready = False
        self._connecting = False
        self._cleanup(keep_features=True)
        pid_text = f"PID: {self._pid}" if self._pid else ""
        self.after(0, lambda: self.pid_label.configure(text=pid_text))
        self.after(0, lambda: self._set_status("red", "连接断开，正在重连..."))

    def _cleanup(self, keep_features=False):
        try:
            self._frida.disconnect()
        except Exception:
            pass
        self._ready = False
        self._nano4t_ready = False
        self.after(0, lambda: self.nano4t_round_label.configure(
            text="当前回合: 等待进入多人生化模式..."))
        if not keep_features:
            self._features = {k: False for k in self._features}
            self._skip_count = 0
            self.after(0, lambda: self.skip_count_label.configure(text="已跳过: 0 回合"))

    def _restore_features(self):
        for feature_id in list(self._features.keys()):
            if self._features[feature_id]:
                self._restore_single_feature(feature_id)
        for feature_id in self._features:
            self._update_switch(feature_id)

    def _restore_single_feature(self, feature_id):
        if feature_id in ('nano4t', 'roundskip'):
            return
        if feature_id == 'knife':
            self._frida.send_toggle('knife', True)
            self._frida.send_toggle('knife_speed', self._knife_speed)
        elif feature_id == 'movespeed':
            self._frida.send_toggle('movespeed', True)
            self._frida.send_toggle('movespeed_speed', self._movespeed)
        elif feature_id == 'range':
            self._frida.send_toggle('range', True)
            self._frida.send_toggle('range_config', self._range_mult)
        elif feature_id == 'gravity':
            self._frida.send_toggle('gravity', True)
            self._do_send_gravity_config()
        else:
            self._frida.send_toggle(feature_id, True)

    def _toggle_collapse(self):
        self._collapsed = not self._collapsed
        if self._collapsed:
            self._saved_geometry = self.geometry()
            self.hint_frame.pack_forget()
            self.tab_view.pack_forget()
            self.btn_frame.pack_forget()
            self.log_box.pack_forget()
            self.collapse_btn.configure(text="▲ 展开界面")
            self.minsize(400, 62)
            self.geometry("400x62+10+10")
        else:
            self.hint_frame.pack(fill="x", padx=12, pady=(2, 8))
            self.tab_view.pack(fill="both", padx=12, pady=4, expand=True)
            self.btn_frame.pack(fill="x", padx=12, pady=(2, 6))
            self.log_box.pack(fill="x", padx=12, pady=(2, 12))
            self.collapse_btn.configure(text="▼ 折叠界面")
            self.minsize(610, 400)
            self.geometry(self._saved_geometry)

    def _setup_tk_hotkeys(self):
        tk_key_map = {
            '<F1>': 'f1', '<F2>': 'f2', '<F3>': 'f3',
            '<Alt-Key-1>': 'alt+1', '<Alt-Key-2>': 'alt+2', '<Alt-Key-3>': 'alt+3',
        }
        for tk_key, pos in tk_key_map.items():
            self.bind(tk_key, lambda e, p=pos: self._on_tk_hotkey(p))

    def _on_tk_hotkey(self, position):
        from core.config import HOTKEY_EXCLUDED
        feature_id = self._hotkey.hotkeys.get(position)
        if feature_id and feature_id not in HOTKEY_EXCLUDED:
            self._on_hotkey_toggle(feature_id)

    def _on_hotkey_toggle(self, feature_id):
        if feature_id == 'gather':
            self._gather()
        elif feature_id == 'roundskip':
            self._skip_round()
        elif feature_id in self._features:
            self._toggle_feature(feature_id)
            self._sound.play_toggle_sound()

    def _show_settings(self):
        from ui.settings_window import SettingsWindow
        SettingsWindow(self)

    def _load_nano4t_selector(self):
        path = os.path.join(DATA_DIR, "Nano-4T-selector.json")
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {'ghost': 9, 'human': 19}

    def _save_nano4t_selector(self):
        path = os.path.join(DATA_DIR, "Nano-4T-selector.json")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({'ghost': self._nano4t_wanted_ghost,
                           'human': self._nano4t_wanted_human}, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _nano4t_on_ghost_select(self, value):
        gid = int(value.split(":")[0])
        self.nano4t_ghost_desc.configure(text="效果: " + NANO4T_ATTRS[gid][1])
        self._nano4t_wanted_ghost = gid
        self._save_nano4t_selector()
        if self._nano4t_ready:
            self.nano4t_next_label.configure(text="💡 请点击「应用」按钮生效")

    def _nano4t_on_human_select(self, value):
        hid = int(value.split(":")[0])
        self.nano4t_human_desc.configure(text="效果: " + NANO4T_ATTRS[hid][1])
        self._nano4t_wanted_human = hid
        self._save_nano4t_selector()
        if self._nano4t_ready:
            self.nano4t_next_label.configure(text="💡 请点击「应用」按钮生效")

    def _nano4t_refresh_next_label(self):
        if self._nano4t_ready:
            g = self._nano4t_wanted_ghost
            h = self._nano4t_wanted_human
            self.nano4t_next_label.configure(
                text=f"下一回合已锁定: 👻 {NANO4T_ATTRS[g][0]}  |  🛡️ {NANO4T_ATTRS[h][0]}")
        else:
            self.nano4t_next_label.configure(text="")

    def _nano4t_set_status(self, color, text):
        dot_map = {"green": "🟢", "yellow": "🟡", "red": "🔴", "gray": "⚫"}
        self.nano4t_status_dot.configure(text=dot_map.get(color, "⚫"))
        self.nano4t_status_label.configure(text=text)

    def _nano4t_on_ready(self, count):
        self._nano4t_set_status("green", "已就绪")
        self.nano4t_apply_btn.configure(state="normal", fg_color="#2563eb")
        self._log(f"✅ [多人生化] 已就绪！共 {count} 种特性")
        self._log("[多人生化] 用法: 下拉选择 → 点击应用 → 下一回合自动生效")
        self.nano4t_next_label.configure(text="💡 请选择特性后点击「应用」按钮")
        threading.Thread(target=self._nano4t_get_current_bg, daemon=True).start()
        threading.Thread(target=self._nano4t_auto_getcurrent_bg, daemon=True).start()

    def _nano4t_on_destroyed(self):
        self.nano4t_apply_btn.configure(state="disabled", fg_color="#333333")
        self._nano4t_set_status("yellow", "已退出房间")
        self.nano4t_next_label.configure(text="")
        self.nano4t_round_label.configure(text="当前回合: 等待进入多人生化模式...")

    def _nano4t_update_round_label(self, g, h):
        self._nano4t_current_ghost = g
        self._nano4t_current_human = h
        if g >= 0 and h >= 0:
            txt = f"当前回合: 👻 {NANO4T_ATTRS[g][0]}  |  🛡️ {NANO4T_ATTRS[h][0]}"
        elif self._nano4t_ready:
            txt = "当前回合: 等待回合开始..."
        else:
            txt = "当前回合: 等待进入游戏..."
        self.nano4t_round_label.configure(text=txt)

    def _nano4t_connect(self):
        if not self._ready:
            self._log("⚠ [多人生化] 请先连接游戏")
            return
        self._nano4t_log_errors = True
        self._log("[多人生化] 正在初始化多人生化特性系统...")
        threading.Thread(target=self._nano4t_connect_bg, daemon=True).start()

    def _nano4t_connect_bg(self):
        try:
            result = self._frida.call_export('nano4tinit')
            if result is None:
                self._log("❌ [多人生化] 初始化调用失败")
            elif isinstance(result, dict) and not result.get('ok', True):
                self._log("❌ [多人生化] 多人生化模块未加载，请重新连接游戏")
        except Exception as e:
            self._log(f"❌ [多人生化] 连接失败: {e}")

    def _nano4t_apply(self):
        if not self._nano4t_ready:
            self._log("⚠ [多人生化] 尚未就绪，请先进入「多人生化模式」房间")
            return
        try:
            gid = int(self.nano4t_ghost_var.get().split(":")[0])
            hid = int(self.nano4t_human_var.get().split(":")[0])
            threading.Thread(target=lambda: self._nano4t_apply_bg(gid, hid), daemon=True).start()
        except Exception as e:
            self._log(f"❌ [多人生化] 参数错误: {e}")

    def _nano4t_apply_bg(self, gid, hid):
        try:
            self._frida.call_export('nano4tset', gid, hid)
        except Exception as e:
            self._log(f"❌ [多人生化] 应用失败: {e}")
            self._nano4t_ready = False
            self.after(0, lambda: (
                self.nano4t_apply_btn.configure(state="disabled", fg_color="#333333"),
                self._nano4t_set_status("yellow", "已断开")
            ))

    def _nano4t_auto_init_bg(self):
        time.sleep(2)
        if self._frida.is_connected and not self._nano4t_ready:
            try:
                self._frida.call_export('nano4tinit')
            except Exception:
                pass

    def _nano4t_get_current_bg(self):
        if not self._frida.is_connected or not self._nano4t_ready:
            return
        try:
            self._frida.call_export('nano4tgetcurrent')
        except Exception:
            pass

    def _nano4t_auto_health_bg(self):
        time.sleep(2)
        auto_check_logged = False
        while not self._stop:
            time.sleep(2)
            if not self._frida.is_connected:
                auto_check_logged = False
                continue
            if self._nano4t_ready:
                auto_check_logged = False
                try:
                    self._frida.call_export('nano4thealthcheck')
                except Exception:
                    pass
            else:
                if not auto_check_logged:
                    auto_check_logged = True
                    self._log("ℹ️ [多人生化] 后台自动检测中，进入多人生化模式后将自动初始化")
                try:
                    self._frida.call_export('nano4tinit')
                except Exception:
                    pass

    def _nano4t_auto_getcurrent_bg(self):
        time.sleep(3)
        while not self._stop:
            time.sleep(5)
            if self._nano4t_ready and self._frida.is_connected:
                try:
                    self._frida.call_export('nano4tgetcurrent')
                except Exception:
                    pass

    def _nano4t_auto_init_if_needed(self):
        if self._frida.is_connected and not self._nano4t_ready:
            try:
                self._frida.call_export('nano4tinit')
            except Exception:
                pass

    def _on_close(self):
        self._stop = True
        self._hotkey.cleanup()
        self._cleanup()
        self._registry.save_state(DATA_DIR)
        self.destroy()
