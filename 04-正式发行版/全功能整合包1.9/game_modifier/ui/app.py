import customtkinter as ctk
import importlib.util
import os
import threading
import time

from core.config import FEATURES_INFO, NANO4T_ATTRS
from core.event_bus import EventBus
from core.frida_manager import FridaManager
from core.config_runtime.config_manager import ConfigManager
from core.plugin.plugin_registry import PluginRegistry
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
from ui.panel_context import PanelContext
from ui.views import AppShellView, FeatureTabsView
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
        self._config_manager = ConfigManager()
        self._plugin_registry = PluginRegistry(config_manager=self._config_manager)
        self._plugin_registry.load()
        self._sound = SoundManager.get_instance()
        self._hotkey = HotkeyManager.get_instance()
        self._feature_service = FeatureCommandService(self._frida, self._config_manager)
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
        self._migrate_plugin_config_from_persistent_state()
        self._apply_plugin_config_values()

        # LEGACY_COMPAT_ONLY: existing special-page runtime state.
        # New features must keep state in features/<feature_id>/ config, panel,
        # events, or a feature-local controller; do not add app._<feature> fields.
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

        # LEGACY_COMPAT_ONLY: special-page handles and state kept for the
        # existing UI contract. New plugin panels must use PanelContext only.
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
        self._panel_context = PanelContext(self)
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
            plugin_registry=self._plugin_registry,
            on_toggle_feature=self._feature_controller.toggle_feature,
            on_set_config=self._feature_controller.set_feature_config,
            on_action=self._feature_controller.trigger_feature_action,
            logger=self._log,
            is_connected=lambda: self._ready,
            is_enabled=lambda feature_id: self._features.get(feature_id, False),
        )
        bind_view_handles(
            self,
            feature_tabs_view.build(
                weapon_scroll=tab_weapon_scroll,
                player_scroll=tab_player_scroll,
                other_scroll=tab_other_scroll,
            ),
        )

        self._build_special_plugin_panel("nano4t", tab_nano4t_scroll)
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
        self._build_special_plugin_panel("weapon_giver", scroll)

    def _build_special_plugin_panel(self, feature_id, parent):
        feature = self._plugin_registry.get(feature_id)
        if not feature:
            return None
        plugin_dir = feature.manifest.get("_plugin_dir")
        if not plugin_dir:
            return None
        panel_path = os.path.join(plugin_dir, "panel.py")
        if not os.path.exists(panel_path):
            return None
        module_name = f"_game_modifier_panel_{feature_id}"
        spec = importlib.util.spec_from_file_location(module_name, panel_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        build_panel = getattr(module, "build_panel", None)
        if not callable(build_panel):
            return None
        return build_panel(self._panel_context.for_feature(feature_id), parent)

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
        feature = self._plugin_registry.get(feature_id)
        ui_handles = feature.manifest.get("ui_handles", {}) if feature else {}
        switch_name = ui_handles.get("switch", f"{feature_id}_switch")
        switch = getattr(self, switch_name, None)
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
        GameSessionManager.get_instance().reconnect()

    def _cleanup(self, keep_features=False):
        try:
            self._roundskip_monitor.stop()
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
        action = self._plugin_hotkey_action(feature_id)
        if action:
            self._feature_controller.trigger_feature_action(feature_id, action)
        elif feature_id in self._features:
            self._feature_controller.toggle_feature(feature_id)
            self._sound.play_toggle_sound()

    def _plugin_hotkey_action(self, feature_id):
        feature = self._plugin_registry.get(feature_id)
        if not feature:
            return None
        for control in feature.manifest.get("controls", []):
            if control.get("type") == "button":
                return control.get("action", "enable")
        return None

    def _show_settings(self):
        from ui.settings_window import SettingsWindow
        SettingsWindow(self)

    def _load_feature_state(self):
        try:
            state = self._persistence_service.load_app_state(FEATURES_INFO.keys())
            self._apply_persistent_state(state)
            self._apply_plugin_config_values()
            self._sync_plugin_controls_from_config()
            for fid in self._features:
                self._update_switch(fid)
        except Exception:
            pass

    def _apply_persistent_state(self, state):
        self._persistent_state = state
        self._features = dict(state.features)
        self._battle_round_enabled = state.battle_round_enabled
        self._weapon_giver_respawn_enabled = state.weapon_giver_respawn_enabled
        self._nano4t_temp_ghost = state.nano4t_ghost
        self._nano4t_temp_human = state.nano4t_human

        if hasattr(self, "respawn_weapon_var"):
            self.respawn_weapon_var.set(self._weapon_giver_respawn_enabled)
        if self._battle_round_enabled:
            self.battle_round_switch.select()

        self._apply_plugin_config_values()
        self._sync_plugin_controls_from_config()

    def _apply_plugin_config_values(self):
        for feature in self._plugin_registry.all():
            fid = feature.manifest["feature_id"]
            if fid == "esp_box":
                continue
            config = self._config_manager.get(fid)
            if "enabled" in config:
                self._features[fid] = bool(config.get("enabled"))

    def _migrate_plugin_config_from_persistent_state(self):
        # Legacy app-state migration only. New ordinary features must provide
        # defaults in manifest/config files and should not be added here.
        state = self._persistent_state
        migration = {
            "knife": {"enabled": self._features.get("knife", False), "speed": state.knife_speed},
            "movespeed": {"enabled": self._features.get("movespeed", False), "speed": state.move_speed},
            "range": {"enabled": self._features.get("range", False), "range": state.range_mult},
            "timescale": {"enabled": self._features.get("timescale", False), "speed": state.timescale},
            "gravity": {
                "enabled": self._features.get("gravity", False),
                "gravity": state.gravity,
                "jump": state.jump,
                "mode": state.gravity_mode,
            },
        }
        for feature in self._plugin_registry.all():
            fid = feature.manifest["feature_id"]
            if fid == "esp_box":
                continue
            if self._config_manager.has_user_config(fid):
                continue
            payload = migration.get(fid, {"enabled": self._features.get(fid, False)})
            self._config_manager.set(fid, payload)

    def _on_plugin_config_changed(self, feature_id, key, value):
        if key == "enabled":
            self._features[feature_id] = bool(value)
        self._sync_plugin_controls_from_config(feature_id)

    def _sync_plugin_controls_from_config(self, feature_id=None):
        features = [self._plugin_registry.get(feature_id)] if feature_id else self._plugin_registry.all()
        for feature in features:
            if not feature:
                continue
            manifest = feature.manifest
            fid = manifest["feature_id"]
            config = self._config_manager.get(fid)
            controls = manifest.get("controls", [])
            if any(control.get("type") == "switch" for control in controls) and "enabled" in config:
                self._features[fid] = bool(config.get("enabled"))
                self._update_switch(fid)
            sliders = [control for control in controls if control.get("type") == "slider"]
            single_slider = len(sliders) == 1
            for control in sliders:
                key = control.get("key", "value")
                value = config.get(key, control.get("default", 1.0))
                self._set_control_value(
                    self._control_handle_name(manifest, key, "slider_var", single_slider),
                    value,
                )
                self._set_control_label(
                    self._control_handle_name(manifest, key, "slider_label", single_slider),
                    self._format_slider_value(key, value),
                )
            for control in controls:
                if control.get("type") != "combo":
                    continue
                key = control.get("key", "value")
                value = config.get(key, control.get("default"))
                self._set_control_value(
                    self._control_handle_name(manifest, key, "combo_var", False),
                    self._format_combo_value(key, value),
                )

    def _control_handle_name(self, manifest, key, handle_type, single_slider):
        feature_id = manifest["feature_id"]
        handles = manifest.get("ui_handles", {})
        if handle_type == "slider_var":
            return handles.get(f"{key}_var") or (
                handles.get("slider_var") if single_slider else None
            ) or f"{key}_var"
        if handle_type == "slider_label":
            return handles.get(f"{key}_label") or (
                handles.get("slider_label") if single_slider else None
            ) or f"{key}_label"
        if handle_type == "combo_var":
            return handles.get(f"{key}_var") or f"{feature_id}_{key}_var"
        return handles.get(handle_type, f"{feature_id}_{handle_type}")

    def _set_control_value(self, handle_name, value):
        handle = getattr(self, handle_name, None)
        if handle and hasattr(handle, "set"):
            handle.set(value)

    def _set_control_label(self, handle_name, text):
        handle = getattr(self, handle_name, None)
        if handle:
            handle.configure(text=text)

    def _format_slider_value(self, key, value):
        numeric = float(value)
        suffix = "" if key in {"gravity", "jump"} else "x"
        return f"{numeric:.1f}{suffix}"

    def _format_combo_value(self, key, value):
        if key == "mode":
            return "\u4ec5\u81ea\u5df1" if value == "player_only" else "\u5168\u90e8\u73a9\u5bb6"
        return value

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
        feature = self._plugin_registry.get('esp_box')
        if feature and hasattr(feature, 'cleanup'):
            feature.cleanup()
        self._cleanup()
        self.destroy()
