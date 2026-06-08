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
from core.game_session_manager import GameSessionManager

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

WEAPON_LIST = [
    ("120", "NANOKNIFE", "NANOKNIFE", "近战"),
    ("195", "幽灵之刃", "幽灵之刃", "英雄"),
    ("210", "诅咒娃娃手雷", "诅咒娃娃手雷", "投掷"),
    ("237", "圣诞M4A1", "圣诞M4A1", "步枪"),
    ("341", "AK47-茉莉", "AK47-茉莉", "步枪"),
    ("390", "FAL CAMO", "FAL CAMO", "步枪"),
    ("413", "AK47-万圣节", "AK47-万圣节", "步枪"),
    ("415", "M4A1-万圣节", "M4A1-万圣节", "步枪"),
    ("428", "圣诞AK47", "圣诞AK47", "步枪"),
    ("540", "Terminator", "终结者", "英雄"),
    ("585", "M4A1-战龙", "M4A1-战龙", "步枪"),
    ("586", "Barrett-战龙", "Barrett-战龙", "狙击"),
    ("588", "MG3-银色杀手", "MG3-银色杀手", "机枪"),
    ("606", "M4A1-轻骑兵", "M4A1-轻骑兵", "步枪"),
    ("615", "百城M4A1", "百城M4A1", "步枪"),
    ("617", "百城AK47", "百城AK47", "步枪"),
    ("622", "M4A1-蓝水晶", "M4A1-蓝水晶", "步枪"),
    ("672", "GrandTerminator", "大终结者", "英雄"),
    ("730", "AK47-火麒麟", "AK47-火麒麟", "步枪"),
    ("758", "Barrett-翔龙", "Barrett-翔龙", "狙击"),
    ("761", "MG3-翔龙", "MG3-翔龙", "机枪"),
    ("764", "拳击手套", "拳击手套", "近战"),
    ("855", "M4A1-黑龙", "M4A1-黑龙", "步枪"),
    ("856", "M4A1-雷神", "M4A1-雷神", "步枪"),
    ("880", "纯金AK-47", "纯金AK-47", "步枪"),
    ("938", "汤姆逊-烈龙", "汤姆逊-烈龙", "冲锋"),
    ("994", "尼泊尔-红水晶", "尼泊尔-红水晶", "近战"),
    ("1002", "M4A1-黑骑士", "M4A1-黑骑士", "步枪"),
    ("1003", "屠龙", "屠龙", "近战"),
    ("1004", "AK47-苍龙", "AK47-苍龙", "步枪"),
    ("1005", "Barrett-苍龙", "Barrett-苍龙", "狙击"),
    ("1061", "M4A1-玫瑰精灵", "M4A1-玫瑰精灵", "步枪"),
    ("1069", "Ghost Blade-Normal form", "幽灵之刃", "英雄"),
    ("1070", "Armored Terminator", "装甲终结者", "英雄"),
    ("1097", "Fear", "恐惧", "英雄"),
    ("1168", "沙鹰-修罗", "沙鹰-修罗", "手枪"),
    ("1508", "M4A1-死神", "M4A1-死神", "步枪"),
    ("1621", "惨叫鸡", "惨叫鸡", "近战"),
    ("2568", "M82A1-水枪", "M82A1-水枪", "狙击"),
    ("2759", "M4A1-水枪", "M4A1-水枪", "步枪"),
    ("2975", "地狱终结者", "地狱终结者", "英雄"),
    ("2976", "终极猎手", "终极猎手", "英雄"),
    ("2977", "震撼弹", "震撼弹", "投掷"),
    ("2978", "FN FAL榴弹版", "FN FAL榴弹版", "步枪"),
    ("3017", "生化手雷", "生化手雷", "投掷"),
    ("3494", "Nano AT4", "Nano AT4", "特殊"),
    ("3495", "时空猎手", "时空猎手", "英雄"),
    ("3496", "钢铁终结者", "钢铁终结者", "英雄"),
    ("3831", "圣拳猎手", "圣拳猎手", "英雄"),
    ("3832", "虚空之刃", "虚空之刃", "英雄"),
    ("3928", "M14EBR-能量核心", "M14EBR-能量核心", "步枪"),
    ("4850", "机械英雄", "机械英雄", "英雄"),
    ("4851", "XM214重机枪", "XM214重机枪", "机枪"),
    ("4852", "奥术手榴弹", "奥术手榴弹", "投掷"),
    ("4853", "机枪守卫", "机枪守卫", "特殊"),
    ("4854", "不法终结者", "不法终结者", "英雄"),
    ("5361", "蝴蝶刀-枪王排位", "蝴蝶刀-枪王排位", "近战"),
    ("5384", "斯泰尔-枪娘暗刃", "斯泰尔-枪娘暗刃", "冲锋"),
]

TYPE_COLORS = {
    "步枪": "#1e3a5f",
    "英雄": "#3a1e5f",
    "近战": "#1e5f3a",
    "投掷": "#5f4a1e",
    "狙击": "#1e5f5f",
    "机枪": "#5f3a1e",
    "冲锋": "#4a1e5f",
    "特殊": "#3a3a3a",
    "手枪": "#4a5f1e",
}


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("游戏修改器控制台 - 全功能整合包 v1.7")
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
        self._timescale = 1.0

        self._nano4t_ready = False
        # 多人生化选择器状态变量
        _nano4t_cfg = self._load_nano4t_selector()
        # 临时变量：UI选择的值（用于保存到配置文件）
        self._nano4t_temp_ghost = _nano4t_cfg.get('ghost', 0)
        self._nano4t_temp_human = _nano4t_cfg.get('human', 10)
        # 如果配置文件中是-1，使用默认值
        if self._nano4t_temp_ghost < 0 or self._nano4t_temp_ghost >= 10:
            self._nano4t_temp_ghost = 0
        if self._nano4t_temp_human < 10 or self._nano4t_temp_human >= 20:
            self._nano4t_temp_human = 10
        # 实际生效的值（-1表示未激活）
        self._nano4t_wanted_ghost = -1
        self._nano4t_wanted_human = -1
        self._nano4t_activated = False  # 是否已激活
        self._nano4t_current_ghost = -1
        self._nano4t_current_human = -1
        self._nano4t_log_errors = False
        self._nano4t_apply_cooldown = 0  # 应用按钮防抖（时间戳）

        self.settings_window = None
        
        # 武器快捷键徽章字典 {weapon_id: badge_frame}
        self._weapon_hotkey_badges = {}
        # 武器卡片top_frame字典 {weapon_id: top_frame}
        self._weapon_top_frames = {}

        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()
        self._load_feature_state()
        self._hotkey.set_app(self)
        self._hotkey.setup_hotkeys(self._on_hotkey_toggle, silent=True)
        self._setup_tk_hotkeys()
        self._setup_events()
        self._log("游戏修改器控制台 v1.7 — 全功能整合包")
        self._log("正在检测游戏进程...")

        # Start unified session manager (replaces old _auto_connect_bg)
        session = GameSessionManager.get_instance()
        session.start()
        self._features['esp_box'] = session.get_desired_state('esp_box')
        self._update_switch('esp_box')

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
        tab_weapon_giver = self.tab_view.add("赋予武器")

        tab_weapon_scroll = ctk.CTkScrollableFrame(tab_weapon, corner_radius=0, fg_color="transparent")
        tab_weapon_scroll.pack(fill="both", expand=True, padx=2, pady=2)
        tab_player_scroll = ctk.CTkScrollableFrame(tab_player, corner_radius=0, fg_color="transparent")
        tab_player_scroll.pack(fill="both", expand=True, padx=2, pady=2)
        tab_other_scroll = ctk.CTkScrollableFrame(tab_other, corner_radius=0, fg_color="transparent")
        tab_other_scroll.pack(fill="both", expand=True, padx=2, pady=2)
        tab_nano4t_scroll = ctk.CTkScrollableFrame(tab_nano4t, corner_radius=0, fg_color="transparent")
        tab_nano4t_scroll.pack(fill="both", expand=True, padx=2, pady=2)
        tab_weapon_giver_scroll = ctk.CTkScrollableFrame(tab_weapon_giver, corner_radius=0, fg_color="transparent")
        tab_weapon_giver_scroll.pack(fill="both", expand=True, padx=2, pady=2)

        self._build_weapon_tab(tab_weapon_scroll)
        self._build_player_tab(tab_player_scroll)
        self._build_other_tab(tab_other_scroll)
        self._build_nano4t_tab(tab_nano4t_scroll)
        self._build_weapon_giver_tab(tab_weapon_giver_scroll)

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
            scroll, 2, 0, 1, "#3a1a1a", 'godmode', '🛡️', '金刚不坏',
            '角色受到攻击时不会受伤', title_color="#E74C3C")

        _, self.skillcd_switch, _ = self._make_feature_card(
            scroll, 2, 1, 1, "#3a2a3a", 'skillcd', '✨', '技能无冷却',
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

        # 方框透视 - 自定义卡片布局（与时间加速高度匹配）
        esp_box_frame = ctk.CTkFrame(scroll, corner_radius=6, fg_color="#3a3a3a",
                                      border_width=1, border_color="#555555", cursor="hand2")
        esp_box_frame.grid(row=3, column=0, sticky="ew", padx=3, pady=3)
        esp_box_frame.bind("<Button-1>", lambda e: self._toggle_feature('esp_box'))

        # 第一行：标题 + 开关
        esp_box_top = ctk.CTkFrame(esp_box_frame, fg_color="transparent")
        esp_box_top.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(esp_box_top, text="📦 方框透视", font=("Microsoft YaHei", 15, "bold"),
                     text_color="#60A5FA").pack(side="left", padx=4)
        self.esp_box_switch = ctk.CTkSwitch(esp_box_top, text="", font=("Microsoft YaHei", 12),
                                             width=50, command=lambda: self._toggle_feature('esp_box'))
        self.esp_box_switch.pack(side="right", padx=6)

        # 第二行：占位（与时间加速滑块行对齐）
        esp_box_placeholder = ctk.CTkFrame(esp_box_frame, fg_color="transparent", height=28)
        esp_box_placeholder.pack(fill="x", padx=8, pady=(4, 0))
        esp_box_placeholder.pack_propagate(False)  # 固定高度

        # 第三行：文字说明
        ctk.CTkLabel(esp_box_frame, font=("Microsoft YaHei", 15), text="开启敌人方框显示",
                     text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(
            fill="x", expand=False, padx=8, pady=(2, 6))

        # 时间加速 - 自定义卡片布局
        timescale_frame = ctk.CTkFrame(scroll, corner_radius=6, fg_color="#3a3a3a",
                                        border_width=1, border_color="#555555", cursor="hand2")
        timescale_frame.grid(row=3, column=1, sticky="ew", padx=3, pady=3)
        timescale_frame.bind("<Button-1>", lambda e: self._toggle_feature('timescale'))

        # 第一行：标题 + 开关
        timescale_top = ctk.CTkFrame(timescale_frame, fg_color="transparent")
        timescale_top.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(timescale_top, text="⏩ 时间加速", font=("Microsoft YaHei", 15, "bold"),
                     text_color="#00CED1").pack(side="left", padx=4)
        self.timescale_switch = ctk.CTkSwitch(timescale_top, text="", font=("Microsoft YaHei", 12),
                                               width=50, command=lambda: self._toggle_feature('timescale'))
        self.timescale_switch.pack(side="right", padx=6)

        # 第二行：滑块 + 数值显示
        timescale_slider_frame = ctk.CTkFrame(timescale_frame, fg_color="transparent")
        timescale_slider_frame.pack(fill="x", padx=8, pady=(4, 0))
        self.timescale_var = ctk.DoubleVar(value=1.0)
        self.timescale_slider = ctk.CTkSlider(timescale_slider_frame, from_=0.1, to=10.0,
                                               variable=self.timescale_var, number_of_steps=99,
                                               command=self._on_timescale_change, width=150)
        self.timescale_slider.pack(side="left", padx=4)
        self.timescale_label = ctk.CTkLabel(timescale_slider_frame, text="1.0x",
                                             font=("Microsoft YaHei", 12), text_color="#e0e0e0", width=50)
        self.timescale_label.pack(side="left", padx=4)

        # 第三行：文字说明
        ctk.CTkLabel(timescale_frame, font=("Microsoft YaHei", 15), text="调整游戏时间倍速",
                     text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(
            fill="x", expand=False, padx=8, pady=(2, 6))

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

        # 方案B：添加状态指示器
        nano4t_ghost_header = ctk.CTkFrame(nano4t_ghost_frame, fg_color="transparent")
        nano4t_ghost_header.pack(anchor="w", padx=12, pady=(6, 2))
        ctk.CTkLabel(nano4t_ghost_header, text="👻 幽灵方特性",
                     font=("Microsoft YaHei", 14, "bold"), text_color="#ff6666").pack(side="left")
        self.nano4t_ghost_status_label = ctk.CTkLabel(nano4t_ghost_header, text="[未激活]",
                                                       font=("Microsoft YaHei", 11), text_color="#888888")
        self.nano4t_ghost_status_label.pack(side="left", padx=(8, 0))

        # 使用临时变量显示初始值
        ghost_display_id = self._nano4t_temp_ghost
        ghost_display_text = f"{ghost_display_id}: {NANO4T_ATTRS[ghost_display_id][0]}"
        ghost_desc_text = "效果: " + NANO4T_ATTRS[ghost_display_id][1]

        self.nano4t_ghost_var = ctk.StringVar(value=ghost_display_text)
        self.nano4t_ghost_combo = ctk.CTkComboBox(
            nano4t_ghost_frame,
            values=[f"{i}: {NANO4T_ATTRS[i][0]}" for i in range(10)],
            variable=self.nano4t_ghost_var, font=("Microsoft YaHei", 13),
            dropdown_font=("Microsoft YaHei", 12), height=34, state="readonly",
            command=self._nano4t_on_ghost_select)
        self.nano4t_ghost_combo.pack(fill="x", padx=12, pady=(4, 2))
        self.nano4t_ghost_desc = ctk.CTkLabel(
            nano4t_ghost_frame,
            text=ghost_desc_text,
            font=("Microsoft YaHei", 11), text_color="#cc8888")
        self.nano4t_ghost_desc.pack(anchor="w", padx=12, pady=(2, 6))

        nano4t_human_frame = ctk.CTkFrame(nano4t_sel_frame, corner_radius=6, fg_color="#1a1a3a",
                                            height=170)
        nano4t_human_frame.grid(row=0, column=1, sticky="nsew", padx=(4, 8), pady=(6, 4))
        nano4t_human_frame.grid_propagate(False)

        # 方案B：添加状态指示器
        nano4t_human_header = ctk.CTkFrame(nano4t_human_frame, fg_color="transparent")
        nano4t_human_header.pack(anchor="w", padx=12, pady=(6, 2))
        ctk.CTkLabel(nano4t_human_header, text="🛡️ 人类方特性",
                     font=("Microsoft YaHei", 14, "bold"), text_color="#6688ff").pack(side="left")
        self.nano4t_human_status_label = ctk.CTkLabel(nano4t_human_header, text="[未激活]",
                                                       font=("Microsoft YaHei", 11), text_color="#888888")
        self.nano4t_human_status_label.pack(side="left", padx=(8, 0))

        # 使用临时变量显示初始值
        human_display_id = self._nano4t_temp_human
        human_display_text = f"{human_display_id}: {NANO4T_ATTRS[human_display_id][0]}"
        human_desc_text = "效果: " + NANO4T_ATTRS[human_display_id][1]

        self.nano4t_human_var = ctk.StringVar(value=human_display_text)
        self.nano4t_human_combo = ctk.CTkComboBox(
            nano4t_human_frame,
            values=[f"{i}: {NANO4T_ATTRS[i][0]}" for i in range(10, 20)],
            variable=self.nano4t_human_var, font=("Microsoft YaHei", 13),
            dropdown_font=("Microsoft YaHei", 12), height=34, state="readonly",
            command=self._nano4t_on_human_select)
        self.nano4t_human_combo.pack(fill="x", padx=12, pady=(4, 2))
        self.nano4t_human_desc = ctk.CTkLabel(
            nano4t_human_frame,
            text=human_desc_text,
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

    def _build_weapon_giver_tab(self, scroll):
        weapon_giver_frame = ctk.CTkFrame(scroll, corner_radius=8, fg_color="#2b2b2b")
        weapon_giver_frame.pack(fill="x", padx=8, pady=(8, 4))
        
        top_frame = ctk.CTkFrame(weapon_giver_frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkLabel(top_frame, text="🔫 武器赋予", font=("Microsoft YaHei", 16, "bold"),
                     text_color="#FF6B6B").pack(side="left", padx=4)
        
        tools_frame = ctk.CTkFrame(weapon_giver_frame, fg_color="transparent")
        tools_frame.pack(fill="x", padx=8, pady=(4, 4))
        
        self.respawn_weapon_var = ctk.BooleanVar(value=False)
        self.respawn_weapon_check = ctk.CTkCheckBox(tools_frame, text="复活自动装备武器",
                                                     font=("Microsoft YaHei", 11),
                                                     variable=self.respawn_weapon_var,
                                                     command=self._on_respawn_weapon_toggle)
        self.respawn_weapon_check.pack(side="left", padx=4)
        
        self.current_weapon_label = ctk.CTkLabel(tools_frame, text="当前武器: 无",
                                                  font=("Microsoft YaHei", 11), text_color="#2ecc71")
        self.current_weapon_label.pack(side="left", padx=8)
        
        self._build_weapon_list(weapon_giver_frame)

    def _build_weapon_list(self, parent):
        weapons_by_type = {}
        for weapon in WEAPON_LIST:
            weapon_id, en_name, cn_name, weapon_type = weapon
            if weapon_type not in weapons_by_type:
                weapons_by_type[weapon_type] = []
            weapons_by_type[weapon_type].append(weapon)
        
        type_counts = [(t, len(weapons_by_type[t])) for t in weapons_by_type]
        type_counts.sort(key=lambda x: x[1], reverse=True)
        sorted_types = [t for t, _ in type_counts]
        
        for weapon_type in sorted_types:
            weapons = weapons_by_type[weapon_type]
            if not weapons:
                continue
            
            type_color = TYPE_COLORS.get(weapon_type, "#2b2b2b")
            
            type_section = ctk.CTkFrame(parent, fg_color=type_color, corner_radius=6)
            type_section.pack(fill="x", padx=4, pady=(6, 3))
            
            type_header = ctk.CTkLabel(type_section, text=f"【{weapon_type}】(共{len(weapons)}个)",
                                        font=("Microsoft YaHei", 12, "bold"), text_color="#ecf0f1", anchor="w")
            type_header.pack(fill="x", padx=10, pady=(6, 3))
            
            cards_frame = ctk.CTkFrame(type_section, fg_color="transparent")
            cards_frame.pack(fill="x", padx=6, pady=(0, 6))
            
            for i, weapon in enumerate(weapons):
                weapon_id, en_name, cn_name, w_type = weapon
                is_hero = (w_type == "英雄")
                
                row = i // 4
                col = i % 4
                
                card = ctk.CTkFrame(cards_frame, fg_color="#1a1a2e" if not is_hero else "#2c3e50", corner_radius=4)
                card.grid(row=row, column=col, padx=3, pady=3, sticky="ew")
                
                cards_frame.grid_columnconfigure(col, weight=1)
                
                # 顶部框架：武器名称 + 快捷键徽章
                top_frame = ctk.CTkFrame(card, fg_color="transparent")
                top_frame.pack(fill="x", padx=3, pady=(3, 0))
                
                # 保存top_frame引用，用于后续更新徽章
                self._weapon_top_frames[weapon_id] = top_frame
                
                name_label = ctk.CTkLabel(top_frame, text=cn_name,
                                           font=("Microsoft YaHei", 10, "bold"), text_color="#ecf0f1")
                name_label.pack(side="left", padx=3)
                
                # 快捷键徽章
                hotkey_badge = self._create_hotkey_badge(top_frame, weapon_id, cn_name)
                if hotkey_badge:
                    hotkey_badge.pack(side="right", padx=3)
                    self._weapon_hotkey_badges[weapon_id] = hotkey_badge
                
                # 底部框架：赋予按钮 + 绑定按钮
                btn_frame = ctk.CTkFrame(card, fg_color="transparent")
                btn_frame.pack(padx=3, pady=(0, 3))
                
                give_btn = ctk.CTkButton(btn_frame, text="赋予", width=50, height=20,
                                          font=("Microsoft YaHei", 9),
                                          command=lambda wid=weapon_id, name=cn_name: self._give_weapon_by_id(wid, name),
                                          fg_color="#3498db" if not is_hero else "#e74c3c",
                                          hover_color="#2980b9" if not is_hero else "#c0392b")
                give_btn.pack(side="left", padx=2)
                
                # 绑定快捷键按钮
                bind_btn = ctk.CTkButton(btn_frame, text="⌨", width=20, height=20,
                                          font=("Microsoft YaHei", 9),
                                          command=lambda wid=weapon_id, name=cn_name: self._bind_weapon_hotkey_dialog(wid, name),
                                          fg_color="#9b59b6", hover_color="#8e44ad")
                bind_btn.pack(side="left", padx=2)

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
                
                # 初始化武器快捷键管理器
                self._init_weapon_hotkey_manager()
            elif status == 'not_found':
                self._set_status("yellow", "未找到游戏")
            else:
                self._set_status("red", "连接断开，正在重连...")
                self._ready = False
                try:
                    from core.weapon_hotkey_manager import WeaponHotkeyManager
                    WeaponHotkeyManager.get_instance().pause_hotkeys()
                except Exception:
                    pass

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
            self._nano4t_activated = False  # 重置激活状态
            self.after(0, self._nano4t_on_destroyed)
            # 重置状态指示器
            self.after(0, lambda: self.nano4t_ghost_status_label.configure(text="[未激活]", text_color="#888888"))
            self.after(0, lambda: self.nano4t_human_status_label.configure(text="[未激活]", text_color="#888888"))
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
            self._nano4t_activated = True  # 标记为已激活
            self._log(
                f"✅ [多人生化] 已锁定: {NANO4T_ATTRS[g][0]} + {NANO4T_ATTRS[h][0]}，下一回合生效")
            self.after(0, self._nano4t_refresh_next_label)
            # 更新状态指示器
            self.after(0, lambda: self.nano4t_ghost_status_label.configure(text="[已激活]", text_color="#88ff88"))
            self.after(0, lambda: self.nano4t_human_status_label.configure(text="[已激活]", text_color="#88ff88"))
        elif event_type == 'nano4t_current':
            g = int(payload.get('g', -1))
            h = int(payload.get('h', -1))
            self.after(0, lambda gg=g, hh=h: self._nano4t_update_round_label(gg, hh))
        elif event_type == 'nano4t_dead':
            if self._nano4t_ready:
                self._log("⚠ [多人生化] 模式实例已失效")
                self._nano4t_ready = False
                self._nano4t_activated = False  # 重置激活状态
                self.after(0, self._nano4t_on_destroyed)
                # 重置状态指示器
                self.after(0, lambda: self.nano4t_ghost_status_label.configure(text="[未激活]", text_color="#888888"))
                self.after(0, lambda: self.nano4t_human_status_label.configure(text="[未激活]", text_color="#888888"))
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
        if feature_id != 'esp_box' and not self._ready:
            self._log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return

        new_state = not self._features.get(feature_id, False)

        # Special handling for esp_box (Universal DLL) - run in background thread
        if feature_id == 'esp_box':
            # Disable switch during operation to prevent duplicate clicks
            switch = getattr(self, 'esp_box_switch', None)
            if switch:
                switch.configure(state="disabled")

            def run_in_background():
                try:
                    feature = self._registry.get('esp_box')
                    ok = feature.enable() if new_state else feature.disable()
                    self._features[feature_id] = bool(ok and new_state)
                    # Schedule UI update on main thread
                    self.after(0, lambda: self._on_esp_box_complete(feature_id, ok))
                except Exception as e:
                    self.after(0, lambda: self._on_esp_box_error(feature_id, str(e)))

            import threading
            thread = threading.Thread(target=run_in_background, daemon=True)
            thread.start()
            return

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
        elif feature_id == 'timescale':
            params = {'speed': self._timescale} if new_state else None
            self._frida.send_toggle('timescale', new_state, extra_params=params)
        else:
            self._frida.send_toggle(feature_id, new_state)

        self._sound.play_toggle_sound()
        self._update_switch(feature_id)
        self._schedule_save_state()

    def _update_switch(self, feature_id):
        switch_map = {
            'knife': self.knife_switch, 'time': self.time_switch,
            'recoil': self.recoil_switch, 'ammo': self.ammo_switch,
            'movespeed': self.move_switch, 'ammoplus': self.ammoplus_switch,
            'range': self.range_switch, 'gather': self.gather_switch,
            'gravity': self.gravity_switch, 'aim': self.aim_switch,
            'godmode': self.godmode_switch, 'speedgun': self.speedgun_switch,
            'isbot': self.isbot_switch, 'skillcd': self.skillcd_switch,
            'esp_box': self.esp_box_switch, 'timescale': self.timescale_switch,
        }
        switch = switch_map.get(feature_id)
        if not switch:
            return
        enabled = self._features.get(feature_id, False)
        if enabled:
            switch.select()
        else:
            switch.deselect()

    def _on_esp_box_complete(self, feature_id, ok):
        """Called on main thread after ESP box operation completes."""
        self._update_switch(feature_id)
        self._schedule_save_state()
        # Re-enable switch
        switch = getattr(self, 'esp_box_switch', None)
        if switch:
            switch.configure(state="normal")
        if ok:
            self._sound.play_toggle_sound()

    def _on_esp_box_error(self, feature_id, error_msg):
        """Called on main thread if ESP box operation fails."""
        self._log(f"⚠ 方框透视操作失败: {error_msg}")
        self._features[feature_id] = False
        self._update_switch(feature_id)
        # Re-enable switch
        switch = getattr(self, 'esp_box_switch', None)
        if switch:
            switch.configure(state="normal")

    def _on_knife_speed_change(self, value):
        self._knife_speed = round(float(value), 1)
        if self._features.get('knife'):
            self._frida.send_toggle('knife_speed', self._knife_speed)
        self._schedule_save_state()

    def _on_move_speed_change(self, value):
        self._movespeed = round(float(value), 1)
        if self._features.get('movespeed'):
            self._frida.send_toggle('movespeed_speed', self._movespeed)
        self._schedule_save_state()

    def _on_range_change(self, value):
        self._range_mult = round(float(value), 1)
        if self._features.get('range'):
            self._frida.send_toggle('range_config', self._range_mult)
        self._schedule_save_state()

    def _on_timescale_change(self, value):
        self._timescale = round(float(value), 1)
        self.timescale_label.configure(text=f"{self._timescale:.1f}x")
        if self._features.get('timescale'):
            self._frida.send_toggle('timescale_speed', self._timescale)
        self._schedule_save_state()

    def _on_gravity_change(self, value):
        self._gravity = round(float(value), 1)
        self.gravity_label.configure(text=f"{self._gravity:.1f}")
        self._debounce_gravity_config()
        self._schedule_save_state()

    def _on_jump_change(self, value):
        self._jump = round(float(value), 1)
        self.jump_label.configure(text=f"{self._jump:.1f}")
        self._debounce_gravity_config()
        self._schedule_save_state()

    def _on_gravity_mode_change(self, value):
        self._gravity_mode = 'player_only' if value == "仅自己" else 'all'
        self._debounce_gravity_config()
        self._schedule_save_state()

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

    def _quick_give_weapon(self, weapon_id):
        if not self._ready:
            self._log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return
        
        self._log(f"🔫 快速赋予武器 ID={weapon_id}...")
        
        def do_give_weapon():
            try:
                result = self._frida.call_export('giveweapon', weapon_id, True, True)
                if result and result.get('ok'):
                    if result.get('result', '').startswith('pending:'):
                        self._log(f"✅ 武器赋予任务已提交，等待主线程执行...")
                    else:
                        self._log(f"✅ 武器赋予成功！")
                else:
                    self._log(f"❌ 武器赋予失败: {result.get('msg', '未知错误')}")
            except Exception as e:
                self._log(f"❌ 武器赋予异常: {e}")
        
        threading.Thread(target=do_give_weapon, daemon=True).start()

    def _give_weapon_by_id(self, weapon_id, weapon_name=""):
        if not self._ready:
            self._log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return
        
        self.current_weapon_label.configure(text=f"当前武器: {weapon_name} (ID: {weapon_id})")
        self._log(f"🔫 正在赋予武器: {weapon_name} (ID: {weapon_id})...")
        
        if self.respawn_weapon_var.get():
            self._set_respawn_weapon(weapon_id, weapon_name)
        
        def do_give_weapon():
            try:
                result = self._frida.call_export('giveweapon', weapon_id, True, True)
                if result and result.get('ok'):
                    if result.get('result', '').startswith('pending:'):
                        self._log(f"✅ 武器赋予任务已提交，等待主线程执行...")
                    else:
                        self._log(f"✅ 武器赋予成功: {weapon_name}")
                else:
                    self._log(f"❌ 武器赋予失败: {weapon_name} - {result.get('msg', '未知错误')}")
            except Exception as e:
                self._log(f"❌ 武器赋予异常: {e}")
        
        threading.Thread(target=do_give_weapon, daemon=True).start()

    def _set_respawn_weapon(self, weapon_id, weapon_name):
        if not self._ready:
            return
        
        def do_set():
            try:
                result = self._frida.call_export('setrespawnweapon', weapon_id, weapon_name)
                if result and result.get('ok'):
                    self._log(f"✅ 已设置复活自动装备: {weapon_name} (ID: {weapon_id})")
                else:
                    self._log(f"❌ 设置复活武器失败")
            except Exception as e:
                self._log(f"❌ 设置复活武器失败: {e}")
        
        threading.Thread(target=do_set, daemon=True).start()

    def _on_respawn_weapon_toggle(self):
        if not self._ready:
            self._log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return
        
        if self.respawn_weapon_var.get():
            self._log("✅ 复活自动装备已启用，点击武器卡片赋予时会自动设置")
        else:
            self._clear_respawn_weapon()
        self._schedule_save_state()
    
    def _create_hotkey_badge(self, parent, weapon_id, weapon_name):
        """创建快捷键徽章，返回 None 或 Frame"""
        from core.weapon_hotkey_manager import WeaponHotkeyManager
        from core.config import WEAPON_HOTKEY_DISPLAY_NAMES
        
        whm = WeaponHotkeyManager.get_instance()
        hotkey = whm.get_weapon_hotkey(weapon_id)
        
        if not hotkey:
            return None
        
        # 创建徽章框架
        badge_frame = ctk.CTkFrame(parent, fg_color="#3498db", corner_radius=3)
        
        # 快捷键文本
        display_name = WEAPON_HOTKEY_DISPLAY_NAMES.get(hotkey, hotkey)
        hotkey_label = ctk.CTkLabel(badge_frame, text=f"⌨ {display_name}",
                                     font=("Microsoft YaHei", 8), text_color="white")
        hotkey_label.pack(side="left", padx=2)
        
        # 删除按钮
        remove_btn = ctk.CTkButton(badge_frame, text="✕", width=15, height=15,
                                    font=("Microsoft YaHei", 7),
                                    command=lambda: self._unbind_weapon_hotkey(weapon_id, weapon_name),
                                    fg_color="transparent", hover_color="#e74c3c",
                                    text_color="white")
        remove_btn.pack(side="left", padx=1)
        
        return badge_frame
    
    def _unbind_weapon_hotkey(self, weapon_id, weapon_name):
        """解绑武器快捷键"""
        from core.weapon_hotkey_manager import WeaponHotkeyManager
        
        whm = WeaponHotkeyManager.get_instance()
        success = whm.unbind_weapon_hotkey(weapon_id)
        
        if success:
            # 更新UI：移除徽章
            if weapon_id in self._weapon_hotkey_badges:
                badge = self._weapon_hotkey_badges[weapon_id]
                badge.destroy()
                del self._weapon_hotkey_badges[weapon_id]
    
    def _bind_weapon_hotkey_dialog(self, weapon_id, weapon_name):
        """打开绑定快捷键对话框"""
        from core.weapon_hotkey_manager import WeaponHotkeyManager
        from core.config import WEAPON_HOTKEY_DISPLAY_NAMES, WEAPON_HOTKEY_POSITIONS
        
        # 创建弹出窗口
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"绑定快捷键 - {weapon_name}")
        dialog.geometry("300x200")
        dialog.transient(self)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - dialog.winfo_width()) // 2
        y = self.winfo_y() + (self.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = ctk.CTkLabel(dialog, text=f"为 {weapon_name} 绑定快捷键",
                                    font=("Microsoft YaHei", 12, "bold"))
        title_label.pack(pady=15)
        
        # 获取可用快捷键
        whm = WeaponHotkeyManager.get_instance()
        available_hotkeys = whm.get_available_hotkeys()
        
        # 如果当前武器已绑定，也要包含在选项中
        current_hotkey = whm.get_weapon_hotkey(weapon_id)
        if current_hotkey and current_hotkey not in available_hotkeys:
            available_hotkeys.insert(0, current_hotkey)
        
        # 转换为显示名称
        available_display = [WEAPON_HOTKEY_DISPLAY_NAMES.get(h, h) for h in available_hotkeys]
        
        # 下拉菜单
        hotkey_var = ctk.StringVar(value=available_display[0] if available_display else "无可用快捷键")
        hotkey_menu = ctk.CTkOptionMenu(dialog, variable=hotkey_var,
                                         values=available_display if available_display else ["无可用快捷键"],
                                         width=200)
        hotkey_menu.pack(pady=10)
        
        # 按钮框架
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=15)
        
        def on_confirm():
            display_name = hotkey_var.get()
            # 反向查找快捷键
            hotkey = None
            for h, d in WEAPON_HOTKEY_DISPLAY_NAMES.items():
                if d == display_name:
                    hotkey = h
                    break
            
            if hotkey:
                success, error_msg = whm.bind_weapon_hotkey(hotkey, weapon_id, weapon_name)
                if success:
                    # 更新UI：添加徽章
                    self._update_weapon_badge(weapon_id, weapon_name)
                    dialog.destroy()
                else:
                    self._log(f"❌ {error_msg}")
        
        confirm_btn = ctk.CTkButton(btn_frame, text="确定", width=80, command=on_confirm)
        confirm_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(btn_frame, text="取消", width=80, command=dialog.destroy)
        cancel_btn.pack(side="left", padx=10)
    
    def _update_weapon_badge(self, weapon_id, weapon_name):
        """更新武器快捷键徽章（实时显示）"""
        from core.weapon_hotkey_manager import WeaponHotkeyManager
        
        # 移除旧徽章
        if weapon_id in self._weapon_hotkey_badges:
            old_badge = self._weapon_hotkey_badges[weapon_id]
            old_badge.destroy()
            del self._weapon_hotkey_badges[weapon_id]
        
        # 获取对应的top_frame
        if weapon_id in self._weapon_top_frames:
            top_frame = self._weapon_top_frames[weapon_id]
            
            # 创建新徽章
            new_badge = self._create_hotkey_badge(top_frame, weapon_id, weapon_name)
            if new_badge:
                new_badge.pack(side="right", padx=3)
                self._weapon_hotkey_badges[weapon_id] = new_badge
    
    def _refresh_weapon_list(self):
        """刷新武器列表（更新徽章）"""
        # 简化方案：重新构建武器赋予页面
        # 这里可以优化为只更新徽章部分
        pass  # 暂时不实现，因为徽章会在下次打开页面时自动更新
    
    def _init_weapon_hotkey_manager(self):
        """初始化武器快捷键管理器"""
        from core.weapon_hotkey_manager import WeaponHotkeyManager
        
        whm = WeaponHotkeyManager.get_instance()
        # 传递self引用，用于将快捷键操作调度到主线程（线程安全）
        whm.setup_hotkeys(self._give_weapon_by_id_from_hotkey, app=self)
        
        # 显示已绑定的快捷键
        bindings = whm.get_all_bindings()
        if bindings:
            self._log(f"✅ 武器快捷键已加载: {len(bindings)} 个绑定")
    
    def _give_weapon_by_id_from_hotkey(self, weapon_id):
        """快捷键触发的赋予武器"""
        # 查找武器名称
        weapon_name = self._get_weapon_name_by_id(weapon_id)
        self._give_weapon_by_id(weapon_id, weapon_name)
    
    def _get_weapon_name_by_id(self, weapon_id):
        """根据武器ID查找武器名称"""
        for weapon in WEAPON_LIST:
            wid, en_name, cn_name, w_type = weapon
            if wid == weapon_id:
                return cn_name
        return f"武器{weapon_id}"

    def _clear_respawn_weapon(self):
        if not self._ready:
            return
        
        self._log("🔫 清除复活自动装备武器")
        
        def do_clear():
            try:
                result = self._frida.call_export('clearrespawnweapon')
                if result and result.get('ok'):
                    self._log(f"✅ 已清除复活自动装备")
                else:
                    self._log(f"❌ 清除失败")
            except Exception as e:
                self._log(f"❌ 清除异常: {e}")
        
        threading.Thread(target=do_clear, daemon=True).start()

    def _connect(self):
        self._log("正在重新检测游戏进程...")
        GameSessionManager.get_instance().reconnect()

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
        try:
            from core.weapon_hotkey_manager import WeaponHotkeyManager
            WeaponHotkeyManager.get_instance().pause_hotkeys()
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
        if feature_id in ('nano4t', 'roundskip', 'esp_box'):
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
        elif feature_id == 'timescale':
            self._frida.send_toggle('timescale', True, extra_params={'speed': self._timescale})
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
        """加载配置文件，如果不存在或无效则返回默认值"""
        path = os.path.join(DATA_DIR, "Nano-4T-selector.json")
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 验证配置文件中的值是否有效
                    ghost = data.get('ghost', 0)
                    human = data.get('human', 10)
                    # 如果值无效，使用默认值
                    if ghost < 0 or ghost >= 10:
                        ghost = 0
                    if human < 10 or human >= 20:
                        human = 10
                    return {'ghost': ghost, 'human': human}
            except Exception:
                pass
        # 默认值：幽灵方=0（强化），人类方=10（救世主）
        return {'ghost': 0, 'human': 10}

    def _save_nano4t_selector(self):
        """保存用户选择的特性到配置文件（保存临时变量）"""
        path = os.path.join(DATA_DIR, "Nano-4T-selector.json")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({'ghost': self._nano4t_temp_ghost,
                           'human': self._nano4t_temp_human}, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _nano4t_on_ghost_select(self, value):
        """下拉框选择回调：更新临时变量"""
        try:
            gid = int(value.split(":")[0])
            # 验证范围
            if gid < 0 or gid >= 10:
                self._log(f"⚠ [多人生化] 幽灵方特性ID无效: {gid}")
                return
            # 更新临时变量
            self._nano4t_temp_ghost = gid
            # 更新UI描述
            self.nano4t_ghost_desc.configure(text="效果: " + NANO4T_ATTRS[gid][1])
            # 保存到配置文件
            self._save_nano4t_selector()
            # 提示用户
            if self._nano4t_ready:
                self.nano4t_next_label.configure(text="💡 请点击「应用」按钮生效")
        except Exception as e:
            self._log(f"❌ [多人生化] 幽灵方选择错误: {e}")

    def _nano4t_on_human_select(self, value):
        """下拉框选择回调：更新临时变量"""
        try:
            hid = int(value.split(":")[0])
            # 验证范围
            if hid < 10 or hid >= 20:
                self._log(f"⚠ [多人生化] 人类方特性ID无效: {hid}")
                return
            # 更新临时变量
            self._nano4t_temp_human = hid
            # 更新UI描述
            self.nano4t_human_desc.configure(text="效果: " + NANO4T_ATTRS[hid][1])
            # 保存到配置文件
            self._save_nano4t_selector()
            # 提示用户
            if self._nano4t_ready:
                self.nano4t_next_label.configure(text="💡 请点击「应用」按钮生效")
        except Exception as e:
            self._log(f"❌ [多人生化] 人类方选择错误: {e}")

    def _nano4t_refresh_next_label(self):
        if self._nano4t_ready and self._nano4t_activated:
            g = self._nano4t_wanted_ghost
            h = self._nano4t_wanted_human
            if g >= 0 and h >= 0:
                self.nano4t_next_label.configure(
                    text=f"下一回合已锁定: 👻 {NANO4T_ATTRS[g][0]}  |  🛡️ {NANO4T_ATTRS[h][0]}")
            else:
                self.nano4t_next_label.configure(text="请选择特性并点击「应用」")
        elif self._nano4t_ready:
            self.nano4t_next_label.configure(text="请选择特性并点击「应用」")
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
        self._log("[多人生化] 当前未激活，游戏将正常运行。选择特性后点击应用 → 下一回合生效")
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
        """应用按钮：验证参数并调用Frida"""
        if not self._nano4t_ready:
            self._log("⚠ [多人生化] 尚未就绪，请先进入「多人生化模式」房间")
            return
        
        # 防抖检查（0.5秒内只能点击一次）
        import time
        current_time = time.time()
        if current_time - self._nano4t_apply_cooldown < 0.5:
            self._log("⚠ [多人生化] 请勿频繁点击")
            return
        self._nano4t_apply_cooldown = current_time
        
        # 验证临时变量范围
        gid = self._nano4t_temp_ghost
        hid = self._nano4t_temp_human
        
        if gid < 0 or gid >= 10:
            self._log(f"❌ [多人生化] 幽灵方特性ID无效: {gid}（有效范围: 0-9）")
            return
        if hid < 10 or hid >= 20:
            self._log(f"❌ [多人生化] 人类方特性ID无效: {hid}（有效范围: 10-19）")
            return
        
        # 调用Frida（后台线程）
        threading.Thread(target=lambda: self._nano4t_apply_bg(gid, hid), daemon=True).start()

    def _nano4t_apply_bg(self, gid, hid):
        """后台线程：调用Frida设置特性"""
        try:
            # 调用Frida RPC（增加超时保护）
            result = self._frida.call_export('nano4tset', gid, hid)
            # 更新实际生效的值
            self._nano4t_wanted_ghost = gid
            self._nano4t_wanted_human = hid
        except Exception as e:
            self._log(f"❌ [多人生化] 应用失败: {e}")
            self._nano4t_ready = False
            self.after(0, lambda: (
                self.nano4t_apply_btn.configure(state="disabled", fg_color="#333333"),
                self._nano4t_set_status("yellow", "已断开"),
                self.nano4t_ghost_status_label.configure(text="[未激活]", text_color="#888888"),
                self.nano4t_human_status_label.configure(text="[未激活]", text_color="#888888")
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

    def _load_feature_state(self):
        path = os.path.join(DATA_DIR, "feature_state.json")
        if not os.path.exists(path):
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                state = json.load(f)
            for fid, s in state.items():
                if fid == 'esp_box':
                    continue
                if fid not in self._features or not isinstance(s, dict):
                    continue
                self._features[fid] = s.get('enabled', False)
                if 'slider_value' in s:
                    if fid == 'knife':
                        self._knife_speed = s['slider_value']
                        self.knife_speed_var.set(s['slider_value'])
                    elif fid == 'movespeed':
                        self._movespeed = s['slider_value']
                        self.move_speed_var.set(s['slider_value'])
                    elif fid == 'range':
                        self._range_mult = s['slider_value']
                        self.range_var.set(s['slider_value'])
                    elif fid == 'timescale':
                        self._timescale = s['slider_value']
                        self.timescale_var.set(s['slider_value'])
                        self.timescale_label.configure(text=f"{s['slider_value']:.1f}x")
                if fid == 'gravity':
                    if 'gravity_value' in s:
                        self._gravity = s['gravity_value']
                        self.gravity_var.set(self._gravity)
                        self.gravity_label.configure(text=f"{self._gravity:.1f}")
                    if 'jump_value' in s:
                        self._jump = s['jump_value']
                        self.jump_var.set(self._jump)
                        self.jump_label.configure(text=f"{self._jump:.1f}")
                    if 'gravity_mode' in s:
                        self._gravity_mode = s['gravity_mode']
                        mode_text = "仅自己" if self._gravity_mode == 'player_only' else "全部玩家"
                        self.gravity_mode_var.set(mode_text)
                if fid == 'weapon_giver':
                    if 'respawn_weapon' in s:
                        self.respawn_weapon_var.set(s['respawn_weapon'])
            for fid in self._features:
                self._update_switch(fid)
        except Exception:
            pass

    def _save_feature_state(self):
        state = {}
        for fid in self._features:
            if fid == 'esp_box':
                continue
            s = {'enabled': self._features.get(fid, False)}
            if fid == 'knife':
                s['slider_value'] = self._knife_speed
            elif fid == 'movespeed':
                s['slider_value'] = self._movespeed
            elif fid == 'range':
                s['slider_value'] = self._range_mult
            elif fid == 'timescale':
                s['slider_value'] = self._timescale
            if fid == 'gravity':
                s['gravity_value'] = self._gravity
                s['jump_value'] = self._jump
                s['gravity_mode'] = self._gravity_mode
            if fid == 'weapon_giver':
                s['respawn_weapon'] = self.respawn_weapon_var.get()
            state[fid] = s
        path = os.path.join(DATA_DIR, "feature_state.json")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _schedule_save_state(self):
        if hasattr(self, '_save_state_timer') and self._save_state_timer:
            self.after_cancel(self._save_state_timer)
        self._save_state_timer = self.after(3000, self._save_feature_state)

    def _on_close(self):
        self._stop = True
        GameSessionManager.get_instance().stop()
        self._hotkey.cleanup()
        try:
            from core.weapon_hotkey_manager import WeaponHotkeyManager
            WeaponHotkeyManager.get_instance().cleanup()
        except Exception:
            pass
        self._save_feature_state()
        # Cleanup Universal ESP feature
        feature = self._registry.get('esp_box')
        if feature and hasattr(feature, 'cleanup'):
            feature.cleanup()
        self._cleanup()
        self.destroy()
