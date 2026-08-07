import customtkinter as ctk
import threading
import time

from core.event_bus import EventBus
from core.frida_manager import FridaManager
from core.config_runtime.config_manager import ConfigManager
from core.config import DEDICATED_HOTKEY_ACTIONS
from core.plugin.plugin_registry import PluginRegistry
from core.sound_manager import SoundManager
from core.hotkey_manager import HotkeyManager
from core.game_session_manager import GameSessionManager
from core.log_manager import setup_logging
from core.services import (
    AppPersistenceService,
    FeatureCommandService,
    GameConnectionService,
)
from ui.controllers import (
    AppEventController,
    FeatureActionController,
)
from ui.panel_context import PanelContext
from ui.views import AppShellView
from ui.views.plugin_tab_builder import PluginTabBuilder
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
        self._game_connection_service = GameConnectionService(self._frida)
        self._persistence_service = AppPersistenceService()
        self._feature_ids = [feature.manifest["feature_id"] for feature in self._plugin_registry.all()]
        self._restorable_feature_ids = self._collect_restorable_feature_ids()
        self._persistent_state = self._persistence_service.load_app_state(
            self._feature_ids,
            restorable_feature_ids=self._restorable_feature_ids,
        )
        self._feature_controller = FeatureActionController(self)
        self._shell_view = AppShellView(
            self,
            on_settings=self._show_settings,
            on_toggle_collapse=self._toggle_collapse,
        )

        self._connecting = False
        self._ready = False
        self._lock = threading.Lock()
        self._stop = False
        self._collapsed = False
        self._saved_geometry = MAIN_WINDOW_GEOMETRY
        self._pid = None
        self._monitoring = True
        self._ui_ready = False
        self._early_log_messages = []
        self._mainloop_ready = False
        self._pending_ui_callbacks = []
        self._pending_ui_lock = threading.Lock()

        self._features = dict(self._persistent_state.features)
        self._migrate_plugin_config_from_persistent_state()

        self.settings_window = None
        self._panel_context = PanelContext(self)
        self._event_controller = AppEventController(self)
        self._tab_builder = None

        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()
        self._load_feature_state()
        self._hotkey.set_app(self)
        self._log(STARTUP_LOG_TITLE)
        self._log("正在检测游戏进程...")

        # 配置文件保持同步读取；全局快捷键在窗口显示后再注册。
        self.after(100, self._initialize_hotkeys_after_ui)
        self.after(300, self._prebuild_plugin_tabs)

        for feature_id in self._features:
            self._update_switch(feature_id)
        self.after(0, self._sync_initial_session_state)
        self.after(0, self._mark_mainloop_ready)

    def _build_ui(self):
        self._build_status_bar()
        self._build_hint_bar()
        # 基础状态区就绪后立即开始检测游戏，不等待完整功能页面构建。
        self._setup_events()
        GameSessionManager.get_instance().start()
        self._build_tab_view()
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
        self._tab_builder = PluginTabBuilder(
            host=self,
            plugin_registry=self._plugin_registry,
            panel_context=self._panel_context,
            callbacks={
                "toggle": self._feature_controller.toggle_feature,
                "set_config": self._feature_controller.set_feature_config,
                "action": self._feature_controller.trigger_feature_action,
            },
            logger=self._log,
            is_connected=lambda: self._ready,
            is_enabled=lambda feature_id: self._features.get(feature_id, False),
        )
        self.tab_view = self._tab_builder.build()

    def _on_tab_changed(self):
        if self._tab_builder:
            self._tab_builder.on_tab_changed()

    def _prebuild_plugin_tabs(self):
        if self._stop or not self._tab_builder:
            return
        self._tab_builder.prebuild_lazy_tabs()

    def _build_log_panel(self):
        self.log_box = self._shell_view.build_log_panel()

    def _setup_events(self):
        self._event_controller.register(self._event_bus)

    def _log(self, msg):
        ts = time.strftime("%H:%M:%S")
        self._safe_after(0, lambda: self._log_ui(ts, msg))

    def _safe_after(self, delay_ms, callback, *args):
        if self._stop:
            return None
        if not self._mainloop_ready:
            self._queue_ui_callback(delay_ms, callback, args)
            return None
        try:
            return self.after(delay_ms, callback, *args)
        except RuntimeError as exc:
            if "main thread is not in main loop" not in str(exc):
                raise
            self._queue_ui_callback(delay_ms, callback, args)
            return None

    def _queue_ui_callback(self, delay_ms, callback, args):
        with self._pending_ui_lock:
            if not self._stop:
                self._pending_ui_callbacks.append((delay_ms, callback, args))

    def _run_in_background(self, fn):
        """在后台线程执行 RPC 等阻塞调用，避免冻结 Tk 事件循环。"""
        if self._stop:
            return
        threading.Thread(target=fn, daemon=True).start()

    def _mark_mainloop_ready(self):
        self._mainloop_ready = True
        with self._pending_ui_lock:
            pending = self._pending_ui_callbacks
            self._pending_ui_callbacks = []
        for delay_ms, callback, args in pending:
            if not self._stop:
                self.after(delay_ms, callback, *args)

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

    def _cleanup(self, keep_features=False):
        self._ready = False
        self._event_bus.emit("game_disconnected")
        if not keep_features:
            self._features = {k: False for k in self._features}

    def _toggle_collapse(self):
        self._collapsed = not self._collapsed
        if self._collapsed:
            self._saved_geometry = self.geometry()
            self.hint_frame.pack_forget()
            self.tab_view.pack_forget()
            self.log_box.pack_forget()
            self.collapse_btn.configure(text="▲ 展开界面")
            self.minsize(*COLLAPSED_WINDOW_SIZE)
            self.geometry(collapsed_geometry_for(self._saved_geometry))
        else:
            self.hint_frame.pack(fill="x", padx=12, pady=(2, 8))
            self.tab_view.pack(fill="both", padx=12, pady=4, expand=True)
            self.log_box.pack(fill="x", padx=12, pady=(2, 12))
            self.collapse_btn.configure(text="▼ 折叠界面")
            self.minsize(*MAIN_WINDOW_MIN_SIZE)
            self.geometry(self._saved_geometry)

    def _setup_tk_hotkeys(self):
        tk_key_map = {
            '<F1>': 'f1', '<F2>': 'f2', '<F3>': 'f3',
            '<Alt-Key-1>': 'alt+1', '<Alt-Key-2>': 'alt+2', '<Alt-Key-3>': 'alt+3', '<Alt-Key-4>': 'alt+4',
        }
        for tk_key, pos in tk_key_map.items():
            self.bind(tk_key, lambda e, p=pos: self._on_tk_hotkey(p))

    def _on_tk_hotkey(self, position):
        from core.config import HOTKEY_EXCLUDED
        dedicated_action = DEDICATED_HOTKEY_ACTIONS.get(position)
        if dedicated_action:
            self._on_hotkey_toggle(dedicated_action)
            return
        feature_id = self._hotkey.hotkeys.get(position)
        if feature_id and feature_id not in HOTKEY_EXCLUDED:
            self._on_hotkey_toggle(feature_id)

    def _on_hotkey_toggle(self, feature_id):
        if isinstance(feature_id, dict):
            action = feature_id.get("action")
            feature_id = feature_id.get("feature_id")
            if feature_id and action:
                result = self._feature_controller.trigger_feature_action(feature_id, action)
                if result is not False:
                    self._sound.play_toggle_sound()
            return
        action = self._plugin_hotkey_action(feature_id)
        if action:
            result = self._feature_controller.trigger_feature_action(feature_id, action)
            if result is not False:
                self._sound.play_toggle_sound()
        elif feature_id in self._features:
            self._feature_controller.toggle_feature(feature_id)

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
            state = self._persistence_service.load_app_state(
                self._feature_ids,
                restorable_feature_ids=self._restorable_feature_ids,
            )
            self._apply_persistent_state(state)
            self._sync_plugin_controls_from_config()
            for fid in self._features:
                self._update_switch(fid)
        except Exception:
            pass

    def _apply_persistent_state(self, state):
        self._persistent_state = state
        self._features = dict(state.features)

        self._sync_plugin_controls_from_config()

    def _collect_restorable_feature_ids(self):
        restorable = set()
        for feature in self._plugin_registry.all():
            manifest = feature.manifest
            fid = manifest["feature_id"]
            if fid in AppPersistenceService.DESIRED_FEATURE_IDS:
                continue
            if manifest.get("lifecycle", {}).get("restore", True) is False:
                continue
            if any(control.get("type") == "switch" for control in manifest.get("controls", [])):
                restorable.add(fid)
        return restorable

    def _migrate_plugin_config_from_persistent_state(self):
        return

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
                    self._format_slider_value(control, value),
                )
            for control in controls:
                control_type = control.get("type")
                if control_type == "switch" and control.get("key"):
                    key = control.get("key")
                    handle_name = self._control_handle_name(manifest, key, "switch_var", False)
                    handle = getattr(self, handle_name, None)
                    if handle and hasattr(handle, "set"):
                        handle.set(bool(config.get(key, control.get("default", False))))
                    continue
                if control_type not in {"combo", "select"}:
                    continue
                key = control.get("key", "value")
                value = config.get(key, control.get("default"))
                handle_type = "select" if control_type == "select" else "combo_var"
                self._set_control_value(
                    self._control_handle_name(manifest, key, handle_type, False),
                    self._format_combo_value(control, value),
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
        if handle_type == "select":
            return handles.get(f"{key}_select") or handles.get(f"{key}_var") or f"{feature_id}_{key}_select"
        if handle_type == "switch_var":
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

    def _format_slider_value(self, control, value):
        numeric = float(value)
        suffix = control.get("suffix", "x")
        return f"{numeric:.1f}{suffix}"

    def _format_combo_value(self, control, value):
        return control.get("display_values", {}).get(value, value)

    def _save_feature_state(self):
        try:
            self._persistence_service.save_app_state(
                self._collect_persistent_state(),
                restorable_feature_ids=self._restorable_feature_ids,
            )
        except Exception:
            pass

    def _collect_persistent_state(self):
        from core.state import AppState

        state = AppState.with_default_features(self._features.keys())
        state.features = dict(self._features)
        return state

    def _schedule_save_state(self):
        if hasattr(self, '_save_state_timer') and self._save_state_timer:
            self.after_cancel(self._save_state_timer)
        self._save_state_timer = self.after(3000, self._save_feature_state)

    def _on_close(self):
        self._stop = True
        with self._pending_ui_lock:
            self._pending_ui_callbacks = []
        self._event_bus.emit("app_closing")
        GameSessionManager.get_instance().stop_async()
        self._hotkey.cleanup()
        self._save_feature_state()
        self._cleanup()
        self.destroy()
