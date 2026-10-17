import customtkinter as ctk
import threading
import time
import traceback

from core.event_bus import EventBus
from core.frida_manager import FridaManager
from core.config_runtime.config_manager import ConfigManager
from core.config import DEDICATED_HOTKEY_ACTIONS
from core.plugin.plugin_registry import PluginRegistry
from core.sound_manager import SoundManager
from core.hotkey_manager import HotkeyManager
from core.game_session_manager import GameSessionManager
from core.log_manager import log_to_file, setup_logging
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
        # P0：Tk 回调异常默认只打到 stderr，发行版/无控制台时什么都看不到 → 统一落盘留痕
        self._install_tk_exception_logging()
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
        self._ui_drain_timer = None

        self._features = dict(self._persistent_state.features)
        self._migrate_plugin_config_from_persistent_state()

        self.settings_window = None
        self._disclaimer_dialog = None
        self._panel_context = PanelContext(self)
        self._event_controller = AppEventController(self)
        self._tab_builder = None

        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()
        self._load_feature_state()
        self._hotkey.set_app(self)
        self._log(STARTUP_LOG_TITLE)
        self._log("本修改器完全免费并已开源，作者从未授权任何第三方代售 —— 若为付费获取，请立即联系卖家退款")
        self._log("仅供个人学习与单机娱乐使用，禁止商业用途。非官方工具，使用风险自负", color="#ffcc00")
        self._log("正在检测游戏进程...")

        # 配置文件保持同步读取；全局快捷键在窗口显示后再注册。
        self.after(100, self._initialize_hotkeys_after_ui)
        self.after(300, self._prebuild_plugin_tabs)
        self.after(500, self._show_first_run_disclaimer)

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

    def _install_tk_exception_logging(self):
        """把 Tk 回调异常落盘留痕。

        P0：Tkinter 默认只把回调异常打到 stderr；发行版没有控制台，回调里的异常
        （例如“连接就绪 → 恢复功能”的 UI 线程处理）会完全消失，表现为功能静默不生效。
        """
        previous = getattr(self, "report_callback_exception", None)

        def _report(exc, val, tb):
            detail = "".join(traceback.format_exception(exc, val, tb)).strip().replace("\n", " | ")
            try:
                log_to_file("error", "TkCallback", f"Tk 回调异常: {val!r} | {detail}")
            except Exception:
                pass
            if callable(previous):
                try:
                    previous(exc, val, tb)
                except Exception:
                    pass

        self.report_callback_exception = _report

    def _log(self, msg, color=None):
        ts = time.strftime("%H:%M:%S")
        self._safe_after(0, lambda: self._log_ui(ts, msg, color))

    def _safe_after(self, delay_ms, callback, *args):
        """把回调投递到 Tk 主线程（线程安全）。

        P0：原实现“主循环未就绪就只入队”，而队列只被 _mark_mainloop_ready 排空一次；
        若调用线程在“读到未就绪 → 入队”之间被抢占，回调会在排空之后才入队，
        从此无人重投 —— 无日志、无提示，连接就绪处理会整体静默失效（功能全不生效）。
        现在：主循环已就绪时优先直接投递；投不进去或尚未就绪则入队，由 1 秒心跳
        （_ui_drain_heartbeat）兜底重投，把“永久丢失”降级为“最多晚 1 秒生效”。
        """
        if self._stop:
            return None
        if self._mainloop_ready:
            timer_id = self._try_after(delay_ms, callback, args)
            if timer_id is not None:
                return timer_id
        self._queue_ui_callback(delay_ms, callback, args)
        return None

    def _try_after(self, delay_ms, callback, args):
        """尝试投递一次 Tk after；跨线程被 Tk 拒绝时返回 None（交给队列重投）。"""
        try:
            return self.after(delay_ms, callback, *args)
        except RuntimeError as exc:
            if "main thread is not in main loop" not in str(exc):
                raise
            return None

    def _queue_ui_callback(self, delay_ms, callback, args):
        with self._pending_ui_lock:
            if not self._stop:
                self._pending_ui_callbacks.append((delay_ms, callback, args))

    def _take_pending_ui_callbacks(self):
        with self._pending_ui_lock:
            pending = self._pending_ui_callbacks
            self._pending_ui_callbacks = []
        return pending

    def _drain_pending_ui_callbacks(self):
        """把滞留的 UI 回调重新投递到主线程；返回本次补投成功的条数。"""
        pending = self._take_pending_ui_callbacks()
        rescued = 0
        for delay_ms, callback, args in pending:
            if self._stop:
                break
            if self._try_after(delay_ms, callback, args) is None:
                self._queue_ui_callback(delay_ms, callback, args)
            else:
                rescued += 1
        return rescued

    def _schedule_ui_drain_heartbeat(self):
        if self._stop:
            return None
        try:
            self._ui_drain_timer = self.after(1000, self._ui_drain_heartbeat)
        except RuntimeError:
            self._ui_drain_timer = None
        return self._ui_drain_timer

    def _ui_drain_heartbeat(self):
        """每秒兜底重投；一旦真的救回回调就落盘，作为“时序竞争发生过”的证据。"""
        self._ui_drain_timer = None
        if self._stop:
            return
        rescued = self._drain_pending_ui_callbacks()
        if rescued:
            log_to_file(
                "warning",
                "App",
                f"UI 回调滞留后由心跳补投 {rescued} 条（发生过主循环时序竞争，功能已自动恢复）",
            )
        self._schedule_ui_drain_heartbeat()

    def _run_in_background(self, fn):
        """在后台线程执行 RPC 等阻塞调用，避免冻结 Tk 事件循环。"""
        if self._stop:
            return
        threading.Thread(target=fn, daemon=True).start()

    def _mark_mainloop_ready(self):
        self._mainloop_ready = True
        drained = self._drain_pending_ui_callbacks()
        if drained:
            log_to_file("info", "App", f"主循环就绪，补投启动期排队的 UI 回调 {drained} 条")
        self._schedule_ui_drain_heartbeat()

    def _log_ui(self, ts, msg, color=None):
        self.log_box.configure(state="normal")
        start = self.log_box.index("end-1c")
        self.log_box.insert("end", f"[{ts}] {msg}\n")
        if color:
            # CTkTextbox 不支持 tag 配置，需取底层 tkinter.Text（同红色主题 Tab 的做法）
            tag = f"color_{color.lstrip('#')}"
            inner_text = getattr(self.log_box, "_textbox", self.log_box)
            inner_text.tag_configure(tag, foreground=color)
            inner_text.tag_add(tag, start, "end-1c")
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
            for feature_id in self._features:
                self._features[feature_id] = False

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
            '<Alt-Key-1>': 'alt+1', '<Alt-Key-2>': 'alt+2',
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
        if feature_id and (not isinstance(feature_id, str) or feature_id not in HOTKEY_EXCLUDED):
            self._on_hotkey_toggle(feature_id)

    def _on_hotkey_toggle(self, feature_id):
        if isinstance(feature_id, dict):
            action = feature_id.get("action")
            payload = feature_id.get("payload")
            if isinstance(payload, dict):
                payload = dict(payload)
            feature_id = feature_id.get("feature_id")
            if feature_id and action:
                result = self._feature_controller.trigger_feature_action(feature_id, action, payload)
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

    def _show_first_run_disclaimer(self):
        """首次启动时弹出免责声明；用户点过「我已知晓」后不再弹出。"""
        if self._stop:
            return
        from ui.disclaimer_dialog import show_if_needed
        self._disclaimer_dialog = show_if_needed(self)

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
        except Exception as exc:
            log_to_file("error", "App", f"加载功能状态失败: {exc}")

    def _apply_persistent_state(self, state):
        self._persistent_state = state
        self._features.clear()
        self._features.update(state.features)

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
        except Exception as exc:
            log_to_file("error", "App", f"保存功能状态失败: {exc}")

    def _collect_persistent_state(self):
        from core.state import AppState

        state = AppState.with_default_features(self._features.keys())
        state.features = dict(self._features)
        return state

    def _schedule_save_state(self):
        if self._stop:
            # 退出流程中不再排新的定时器，避免与 destroy() 竞争
            return
        if hasattr(self, '_save_state_timer') and self._save_state_timer:
            self.after_cancel(self._save_state_timer)
        self._save_state_timer = self.after(3000, self._save_feature_state)

    def _on_close(self):
        self._stop = True
        if getattr(self, '_save_state_timer', None):
            self.after_cancel(self._save_state_timer)
            self._save_state_timer = None
        if getattr(self, '_ui_drain_timer', None):
            self.after_cancel(self._ui_drain_timer)
            self._ui_drain_timer = None
        with self._pending_ui_lock:
            self._pending_ui_callbacks = []
        self._event_bus.emit("app_closing")
        GameSessionManager.get_instance().stop_async()
        self._hotkey.cleanup()
        self._save_feature_state()
        self._cleanup()
        self.destroy()
