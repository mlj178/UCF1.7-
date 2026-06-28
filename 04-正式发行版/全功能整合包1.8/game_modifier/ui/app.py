import customtkinter as ctk
import frida
import os
import threading
import time

from core.config import FEATURES_INFO, NANO4T_ATTRS
from core.event_bus import EventBus
from core.frida_manager import FridaManager
from core.feature_registry import FeatureRegistry
from core.sound_manager import SoundManager
from core.hotkey_manager import HotkeyManager
from core.game_session_manager import GameSessionManager
from core.log_manager import setup_logging
from core.services import (
    AppPersistenceService,
    FeatureCommandService,
    GameActionService,
    GameConnectionService,
    WeaponGiverService,
)
from core.state import AppState
from ui.controllers import (
    AppEventController,
    BattleRoundController,
    FeatureActionController,
    Nano4tRuntimeController,
    Nano4tSelectionController,
    RoundSkipMonitor,
    WeaponInteractionController,
)
from ui.views import AppShellView, FeatureTabsView, Nano4tView, WeaponGiverView
from ui.views.common import bind_view_handles
from ui.window_contract import (
    APP_TITLE,
    COLLAPSED_WINDOW_SIZE,
    MAIN_WINDOW_GEOMETRY,
    MAIN_WINDOW_MIN_SIZE,
    STARTUP_LOG_TITLE,
    collapsed_geometry_for,
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Initialize file logging first
        setup_logging()
        self.title(APP_TITLE)
        self.geometry(MAIN_WINDOW_GEOMETRY)
        self.resizable(True, True)
        self.minsize(*MAIN_WINDOW_MIN_SIZE)
        self.attributes('-topmost', True)
        self.attributes('-alpha', 0.92)

        self._event_bus = EventBus.get_instance()
        self._frida = FridaManager.get_instance()
        self._registry = FeatureRegistry.get_instance()
        self._sound = SoundManager.get_instance()
        self._hotkey = HotkeyManager.get_instance()
        self._feature_service = FeatureCommandService(self._frida)
        self._game_action_service = GameActionService(self._frida)
        self._game_connection_service = GameConnectionService(self._frida)
        self._weapon_giver_service = WeaponGiverService(self._frida)
        self._persistence_service = AppPersistenceService()
        self._persistent_state = self._persistence_service.load_app_state(FEATURES_INFO.keys())
        self._nano4t_selector = Nano4tSelectionController(self._persistence_service, NANO4T_ATTRS)
        self._feature_controller = FeatureActionController(self)
        self._shell_view = AppShellView(
            self,
            on_settings=self._show_settings,
            on_toggle_collapse=self._toggle_collapse,
            on_connect=self._connect,
        )

        self._connecting = False
        self._ready = False
        self._lock = threading.Lock()
        self._stop = False
        self._collapsed = False
        self._saved_geometry = MAIN_WINDOW_GEOMETRY
        self._pid = None
        self._gravity_debounce_timer = None
        self._monitoring = True
        self._ui_ready = False
        self._early_log_messages = []

        self._features = dict(self._persistent_state.features)
        self._knife_speed = self._persistent_state.knife_speed
        self._movespeed = self._persistent_state.move_speed
        self._range_mult = self._persistent_state.range_mult
        self._gravity = self._persistent_state.gravity
        self._jump = self._persistent_state.jump
        self._gravity_mode = self._persistent_state.gravity_mode
        self._timescale = self._persistent_state.timescale

        self._nano4t_ready = False
        self._nano4t_temp_ghost = self._persistent_state.nano4t_ghost
        self._nano4t_temp_human = self._persistent_state.nano4t_human
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

        # 强制决战回合状态变量
        self._battle_round_enabled = self._persistent_state.battle_round_enabled  # 开关状态（持久化）
        self._battle_round_active = False   # 实际生效状态
        self._battle_mode_active = False    # 是否已精确识别为多人生化房间
        self._nano4t_runtime_controller = Nano4tRuntimeController(self)
        self._battle_round_controller = BattleRoundController(self)

        self._isbot_state = 'off'
        self.settings_window = None
        self._weapon_giver_tab_built = False
        self._weapon_giver_tab_name = "赋予武器"
        self._weapon_giver_tab_scroll = None
        self._weapon_giver_respawn_enabled = self._persistent_state.weapon_giver_respawn_enabled
        
        # 武器快捷键徽章字典 {weapon_id: badge_frame}
        self._weapon_hotkey_badges = {}
        # 武器卡片top_frame字典 {weapon_id: top_frame}
        self._weapon_top_frames = {}
        self._weapon_controller = WeaponInteractionController(self)
        self._roundskip_monitor = RoundSkipMonitor(self)
        self._event_controller = AppEventController(self)

        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()
        self._load_feature_state()
        self._battle_round_controller.update_button_state()
        self._hotkey.set_app(self)
        self._log(STARTUP_LOG_TITLE)
        self._log("正在检测游戏进程...")

        # 配置文件保持同步读取；全局快捷键在窗口显示后再注册。
        self.after(100, self._initialize_hotkeys_after_ui)
        self.after(300, self._prebuild_weapon_giver_tab)

        self._update_switch('esp_box')
        self.after(0, self._sync_initial_session_state)

    def _build_ui(self):
        self._build_status_bar()
        self._build_hint_bar()
        # 基础状态区就绪后立即开始检测游戏，不等待完整功能页面构建。
        self._setup_events()
        GameSessionManager.get_instance().start()
        self._build_tab_view()
        self._build_connect_button()
        self._build_log_panel()
        self._ui_ready = True
        for message in self._early_log_messages:
            self._log(message)
        self._early_log_messages = []

    def _initialize_hotkeys_after_ui(self):
        if self._stop:
            return
        self._hotkey.setup_hotkeys(self._on_hotkey_toggle, silent=True)
        self._setup_tk_hotkeys()

    def _sync_initial_session_state(self):
        """补偿完整UI构建期间可能已经完成的后台连接事件。"""
        if not self._ready and self._game_connection_service.is_connected:
            self._event_controller.on_connection_status(status='connected', pid=self._game_connection_service.pid)

    def _build_status_bar(self):
        handles = self._shell_view.build_status_bar()
        self.status_frame = handles.frame
        self.status_dot = handles.status_dot
        self.status_label = handles.status_label
        self.settings_btn = handles.settings_btn
        self.collapse_btn = handles.collapse_btn
        self.pid_label = handles.pid_label

    def _build_hint_bar(self):
        handles = self._shell_view.build_hint_bar()
        self.hint_frame = handles.frame
        self.hint_label = handles.label

    def _build_tab_view(self):
        self.tab_view = ctk.CTkTabview(self, corner_radius=8, command=self._on_tab_changed)
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
        self._weapon_giver_tab_name = self.tab_view._name_list[-1]
        self._weapon_giver_tab_scroll = tab_weapon_giver_scroll

        feature_tabs_view = FeatureTabsView(
            on_toggle_feature=self._feature_controller.toggle_feature,
            on_knife_speed_change=self._feature_controller.on_knife_speed_change,
            on_move_speed_change=self._feature_controller.on_move_speed_change,
            on_range_change=self._feature_controller.on_range_change,
            on_timescale_change=self._feature_controller.on_timescale_change,
            on_gravity_change=self._feature_controller.on_gravity_change,
            on_jump_change=self._feature_controller.on_jump_change,
            on_gravity_mode_change=self._feature_controller.on_gravity_mode_change,
            on_gather=self._feature_controller.gather,
            on_skip_round=self._feature_controller.skip_round,
        )
        bind_view_handles(
            self,
            feature_tabs_view.build(
                weapon_scroll=tab_weapon_scroll,
                player_scroll=tab_player_scroll,
                other_scroll=tab_other_scroll,
            ),
        )

        nano4t_view = Nano4tView(
            attrs=NANO4T_ATTRS,
            temp_ghost=self._nano4t_temp_ghost,
            temp_human=self._nano4t_temp_human,
            on_ghost_select=self._nano4t_runtime_controller.on_ghost_select,
            on_human_select=self._nano4t_runtime_controller.on_human_select,
            on_apply=self._nano4t_runtime_controller.apply,
            on_toggle_battle_round=self._battle_round_controller.toggle,
        )
        bind_view_handles(self, nano4t_view.build(tab_nano4t_scroll))
        self._ensure_weapon_giver_tab_built(initial=False)

    def _on_tab_changed(self):
        if self.tab_view.get() == self._weapon_giver_tab_name:
            self._ensure_weapon_giver_tab_built(initial=True)

    def _prebuild_weapon_giver_tab(self):
        if self._stop:
            return
        self._ensure_weapon_giver_tab_built(initial=True)

    def _ensure_weapon_giver_tab_built(self, initial):
        if self._weapon_giver_tab_built or self._weapon_giver_tab_scroll is None:
            return
        if not initial:
            return
        self._weapon_giver_tab_built = True
        self._build_weapon_giver_tab(self._weapon_giver_tab_scroll)

    def _build_weapon_giver_tab(self, scroll):
        view = WeaponGiverView(
            respawn_enabled=self._weapon_giver_respawn_enabled,
            on_respawn_toggle=self._weapon_controller.on_respawn_weapon_toggle,
            on_give_weapon=self._weapon_controller.give_weapon_by_id,
            on_bind_hotkey=self._weapon_controller.bind_weapon_hotkey_dialog,
            create_hotkey_badge=self._weapon_controller.create_hotkey_badge,
            weapon_top_frames=self._weapon_top_frames,
            weapon_hotkey_badges=self._weapon_hotkey_badges,
        )
        handles = view.build(scroll)
        self.respawn_weapon_var = handles.respawn_weapon_var
        self.respawn_weapon_check = handles.respawn_weapon_check
        self.current_weapon_label = handles.current_weapon_label

    def _build_connect_button(self):
        self.btn_frame, self.connect_btn = self._shell_view.build_connect_button()

    def _build_log_panel(self):
        self.log_box = self._shell_view.build_log_panel()

    def _setup_events(self):
        self._event_controller.register(self._event_bus)

    def _log(self, msg):
        ts = time.strftime("%H:%M:%S")
        self.after(0, lambda: self._log_ui(ts, msg))

    def _log_ui(self, ts, msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{ts}] {msg}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _set_status(self, color, text):
        self._shell_view.apply_status(
            status_dot=self.status_dot,
            status_label=self.status_label,
            hint_frame=self.hint_frame,
            hint_label=self.hint_label,
            color=color,
            text=text,
        )

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

    def _set_isbot_state(self, state):
        self._isbot_state = state
        if not hasattr(self, 'isbot_status_label'):
            return
        if state == 'awaiting_room':
            self.isbot_status_label.configure(text="状态: 已预约，等待进房", text_color="#f39c12")
        elif state == 'awaiting_reenter':
            self.isbot_status_label.configure(text="状态: 已预约，等待重进房间生效", text_color="#f39c12")
        elif state == 'active':
            self.isbot_status_label.configure(text="状态: 已生效", text_color="#2ecc71")
        else:
            self.isbot_status_label.configure(text="状态: 已关闭", text_color="#888888")

    def _connect(self):
        self._log("正在重新检测游戏进程...")
        GameSessionManager.get_instance().reconnect()

    def _connect_bg(self):
        pid = self._game_connection_service.find_pid()
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
            success = self._game_connection_service.connect(pid)
            ok = success[0] if isinstance(success, tuple) else bool(success)
            if not ok:
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
                self._game_action_service.health_check()
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
            self._roundskip_monitor.stop()
            self._game_connection_service.disconnect()
        except Exception:
            pass
        self._weapon_controller.pause_hotkeys()
        self._ready = False
        self._nano4t_ready = False
        self.after(0, lambda: self.nano4t_round_label.configure(
            text="当前回合: 等待进入多人生化模式..."))
        if not keep_features:
            self._features = {k: False for k in self._features}

    def _toggle_collapse(self):
        self._collapsed = not self._collapsed
        if self._collapsed:
            self._saved_geometry = self.geometry()
            self.hint_frame.pack_forget()
            self.tab_view.pack_forget()
            self.btn_frame.pack_forget()
            self.log_box.pack_forget()
            self.collapse_btn.configure(text="▲ 展开界面")
            self.minsize(*COLLAPSED_WINDOW_SIZE)
            self.geometry(collapsed_geometry_for(self._saved_geometry))
        else:
            self.hint_frame.pack(fill="x", padx=12, pady=(2, 8))
            self.tab_view.pack(fill="both", padx=12, pady=4, expand=True)
            self.btn_frame.pack(fill="x", padx=12, pady=(2, 6))
            self.log_box.pack(fill="x", padx=12, pady=(2, 12))
            self.collapse_btn.configure(text="▼ 折叠界面")
            self.minsize(*MAIN_WINDOW_MIN_SIZE)
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
            self._feature_controller.gather()
        elif feature_id == 'roundskip':
            self._feature_controller.skip_round()
        elif feature_id in self._features:
            self._feature_controller.toggle_feature(feature_id)
            self._sound.play_toggle_sound()

    def _show_settings(self):
        from ui.settings_window import SettingsWindow
        SettingsWindow(self)

    def _load_feature_state(self):
        try:
            state = self._persistence_service.load_app_state(FEATURES_INFO.keys())
            self._apply_persistent_state(state)
            for fid in self._features:
                self._update_switch(fid)
        except Exception:
            pass

    def _apply_persistent_state(self, state):
        self._persistent_state = state
        self._features = dict(state.features)
        self._knife_speed = state.knife_speed
        self._movespeed = state.move_speed
        self._range_mult = state.range_mult
        self._gravity = state.gravity
        self._jump = state.jump
        self._gravity_mode = state.gravity_mode
        self._timescale = state.timescale
        self._battle_round_enabled = state.battle_round_enabled
        self._weapon_giver_respawn_enabled = state.weapon_giver_respawn_enabled
        self._nano4t_temp_ghost = state.nano4t_ghost
        self._nano4t_temp_human = state.nano4t_human

        self.knife_speed_var.set(self._knife_speed)
        self.move_speed_var.set(self._movespeed)
        self.range_var.set(self._range_mult)
        self.timescale_var.set(self._timescale)
        self.timescale_label.configure(text=f"{self._timescale:.1f}x")
        self.gravity_var.set(self._gravity)
        self.gravity_label.configure(text=f"{self._gravity:.1f}")
        self.jump_var.set(self._jump)
        self.jump_label.configure(text=f"{self._jump:.1f}")
        mode_text = "仅自己" if self._gravity_mode == "player_only" else "全部玩家"
        self.gravity_mode_var.set(mode_text)
        if hasattr(self, "respawn_weapon_var"):
            self.respawn_weapon_var.set(self._weapon_giver_respawn_enabled)
        if self._battle_round_enabled:
            self.battle_round_switch.select()

    def _save_feature_state(self):
        try:
            self._persistence_service.save_app_state(self._collect_persistent_state())
        except Exception:
            pass

    def _collect_persistent_state(self):
        if hasattr(self, "respawn_weapon_var"):
            self._weapon_giver_respawn_enabled = bool(self.respawn_weapon_var.get())

        state = AppState.with_default_features(self._features.keys())
        state.features = dict(self._features)
        state.knife_speed = self._knife_speed
        state.move_speed = self._movespeed
        state.range_mult = self._range_mult
        state.gravity = self._gravity
        state.jump = self._jump
        state.gravity_mode = self._gravity_mode
        state.timescale = self._timescale
        state.battle_round_enabled = self._battle_round_enabled
        state.weapon_giver_respawn_enabled = self._weapon_giver_respawn_enabled
        state.nano4t_ghost = self._nano4t_temp_ghost
        state.nano4t_human = self._nano4t_temp_human
        return state

    def _schedule_save_state(self):
        if hasattr(self, '_save_state_timer') and self._save_state_timer:
            self.after_cancel(self._save_state_timer)
        self._save_state_timer = self.after(3000, self._save_feature_state)

    def _on_close(self):
        self._stop = True
        GameSessionManager.get_instance().stop()
        self._hotkey.cleanup()
        self._weapon_controller.cleanup()
        self._save_feature_state()
        # Cleanup Universal ESP feature
        feature = self._registry.get('esp_box')
        if feature and hasattr(feature, 'cleanup'):
            feature.cleanup()
        self._cleanup()
        self.destroy()
