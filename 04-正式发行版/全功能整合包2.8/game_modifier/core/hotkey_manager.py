import json
import os
import functools

import keyboard

from core.config import (
    DEDICATED_HOTKEY_ACTIONS,
    HOTKEYS_FILE,
    FEATURES_INFO,
    HOTKEY_POSITIONS,
    HOTKEY_DISPLAY_NAMES,
    HOTKEY_EXCLUDED,
    ROLE_TRANSFORM_HOTKEY_ACTIONS,
    ROLE_TRANSFORM_HOTKEY_DISPLAY_NAMES,
    DIRECT_TRANSFORM_HOTKEY_ACTIONS,
    DIRECT_TRANSFORM_HOTKEY_DISPLAY_NAMES,
)
from core.config import write_json_atomic
from core.event_bus import EventBus
from core.log_manager import get_logger
from core.native_hotkey_listener import NativeHotkeyListener, VK_BY_POSITION


def binding_key(binding):
    if not isinstance(binding, dict):
        return binding
    feature_id = binding.get('feature_id')
    payload_action = (binding.get('payload') or {}).get('action')
    return f"{feature_id}:{payload_action}"


def is_role_transform_action(binding):
    return isinstance(binding, dict) and binding.get('feature_id') == 'role_transform'


class HotkeyManager:
    _instance = None

    def __init__(self):
        self._hotkeys = self._load_hotkeys()
        self._hotkey_handles = []
        self._native_hotkey_listener = NativeHotkeyListener()
        self._app = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_hotkeys(self):
        result = {pos: None for pos in HOTKEY_POSITIONS}
        if os.path.exists(HOTKEYS_FILE):
            try:
                with open(HOTKEYS_FILE, 'r', encoding='utf-8') as f:
                    saved = json.load(f)
                for pos in HOTKEY_POSITIONS:
                    if pos in DEDICATED_HOTKEY_ACTIONS:
                        result[pos] = None
                        continue
                    if pos in saved:
                        result[pos] = saved[pos]
                    else:
                        legacy_map = {
                            'ctrl+1': '1', 'ctrl+2': '2', 'ctrl+3': '3',
                            'ctrl+4': '4', 'ctrl+5': '5',
                        }
                        old_key = legacy_map.get(pos)
                        if old_key and old_key in saved:
                            result[pos] = saved[old_key]
                for pos in HOTKEY_POSITIONS:
                    if is_role_transform_action(result[pos]):
                        result[pos] = None
                    elif isinstance(result[pos], str) and result[pos] in HOTKEY_EXCLUDED:
                        result[pos] = None
                return result
            except Exception as exc:
                get_logger("HotkeyManager").warning(
                    "读取快捷键配置失败，已回退默认值 %s: %s", HOTKEYS_FILE, exc
                )
        return result

    def _save_hotkeys(self):
        try:
            write_json_atomic(HOTKEYS_FILE, self._hotkeys)
        except Exception as exc:
            get_logger("HotkeyManager").error(
                "保存快捷键配置失败 %s: %s", HOTKEYS_FILE, exc
            )

    def set_hotkey(self, position, feature_id):
        if position in DEDICATED_HOTKEY_ACTIONS:
            return False
        if is_role_transform_action(feature_id):
            return False
        if isinstance(feature_id, str) and feature_id in HOTKEY_EXCLUDED:
            return False
        old_feature = self._hotkeys.get(position)
        if binding_key(old_feature) == binding_key(feature_id):
            return True
        for pos, feat in self._hotkeys.items():
            if binding_key(feat) == binding_key(feature_id):
                self._hotkeys[pos] = None
        self._hotkeys[position] = feature_id
        return True

    def remove_hotkey(self, position):
        self._hotkeys[position] = None

    def _remove_registered_hotkeys(self):
        for handle in self._hotkey_handles:
            try:
                keyboard.remove_hotkey(handle)
            except Exception:
                pass
        self._hotkey_handles = []

    def setup_hotkeys(self, toggle_callback, silent=False):
        self._toggle_callback = toggle_callback
        self._native_hotkey_listener.stop()
        self._remove_registered_hotkeys()

        native_positions = tuple(
            pos for pos in DEDICATED_HOTKEY_ACTIONS
            if pos in VK_BY_POSITION
        )
        try:
            native_results = self._native_hotkey_listener.start(
                native_positions,
                self._on_native_hotkey_triggered,
            )
        except Exception as exc:
            native_results = {pos: False for pos in native_positions}
            bus = EventBus.get_instance()
            bus.emit(
                'log_message',
                level='warning',
                module='快捷键',
                message=f"Windows 原生快捷键初始化失败，已回退到 keyboard: {exc}",
            )

        for pos, binding in DEDICATED_HOTKEY_ACTIONS.items():
            if native_results.get(pos):
                if not silent:
                    bus = EventBus.get_instance()
                    display = HOTKEY_DISPLAY_NAMES.get(pos, pos)
                    label = binding.get('label', f"{binding.get('feature_id')}.{binding.get('action')}")
                    bus.emit('log_message', level='info', module='快捷键',
                             message=f"绑定 Windows 原生快捷键 {display} -> {label}")
                continue
            if pos in native_positions:
                error = self._native_hotkey_listener.errors.get(pos, 'unknown')
                bus = EventBus.get_instance()
                bus.emit(
                    'log_message',
                    level='warning',
                    module='快捷键',
                    message=f"Windows 原生快捷键 {HOTKEY_DISPLAY_NAMES.get(pos, pos)} 注册失败 "
                            f"(error={error})，已回退到 keyboard",
                )
            try:
                callback = functools.partial(self._on_dedicated_hotkey_triggered, binding)
                handle = keyboard.add_hotkey(pos, callback)
                self._hotkey_handles.append(handle)
                if not silent:
                    bus = EventBus.get_instance()
                    display = HOTKEY_DISPLAY_NAMES.get(pos, pos)
                    label = binding.get('label', f"{binding.get('feature_id')}.{binding.get('action')}")
                    bus.emit('log_message', level='info', module='快捷键',
                             message=f"绑定快捷键 {display} -> {label}")
            except Exception as exc:
                get_logger("HotkeyManager").warning("注册快捷键 %s 失败: %s", pos, exc)

        for actions, display_names in (
            (ROLE_TRANSFORM_HOTKEY_ACTIONS, ROLE_TRANSFORM_HOTKEY_DISPLAY_NAMES),
            (DIRECT_TRANSFORM_HOTKEY_ACTIONS, DIRECT_TRANSFORM_HOTKEY_DISPLAY_NAMES),
        ):
            for pos, binding in actions.items():
                try:
                    callback = functools.partial(self._on_dedicated_hotkey_triggered, binding)
                    handle = keyboard.add_hotkey(pos, callback)
                    self._hotkey_handles.append(handle)
                    if not silent:
                        bus = EventBus.get_instance()
                        display = display_names.get(pos, pos.upper())
                        bus.emit('log_message', level='info', module='快捷键',
                                 message=f"绑定快捷键 {display} -> {binding['label']}")
                except Exception as exc:
                    get_logger("HotkeyManager").warning("注册快捷键 %s 失败: %s", pos, exc)

        for pos in HOTKEY_POSITIONS:
            if pos in DEDICATED_HOTKEY_ACTIONS:
                continue
            feature = self._hotkeys.get(pos)
            if feature:
                try:
                    callback = functools.partial(self._on_hotkey_triggered, feature)
                    handle = keyboard.add_hotkey(pos, callback)
                    self._hotkey_handles.append(handle)
                    if not silent:
                        bus = EventBus.get_instance()
                        display = HOTKEY_DISPLAY_NAMES.get(pos, pos)
                        bus.emit('log_message', level='info', module='快捷键',
                                 message=f"绑定快捷键 {display} -> {feature}")
                except Exception as exc:
                    get_logger("HotkeyManager").warning("注册快捷键 %s 失败: %s", pos, exc)

    def _dispatch_to_ui(self, callback):
        """把回调安全地投递到 Tk 主线程。

        keyboard 回调与原生热键回调都运行在后台线程，直接调用 Tk 的 after()
        可能抛 "main thread is not in main loop"；原先的兜底是在后台线程里
        直接执行回调（跨线程操作 UI，更危险）。这里优先使用 App 提供的
        _safe_after（未进入 mainloop 时会排队、窗口销毁后直接丢弃）。
        """
        safe_after = getattr(self._app, "_safe_after", None)
        if callable(safe_after):
            try:
                safe_after(0, callback)
                return
            except Exception as exc:
                get_logger("HotkeyManager").warning("投递快捷键回调到主线程失败: %s", exc)
        try:
            self._app.after(0, callback)
        except Exception:
            callback()

    def _on_hotkey_triggered(self, feature):
        if self._app and self._toggle_callback:
            self._dispatch_to_ui(functools.partial(self._toggle_callback, feature))

    def _on_dedicated_hotkey_triggered(self, binding):
        if self._app and self._toggle_callback:
            payload = dict(binding)
            self._dispatch_to_ui(functools.partial(self._toggle_callback, payload))

    def _on_native_hotkey_triggered(self, position):
        binding = DEDICATED_HOTKEY_ACTIONS.get(position)
        if binding:
            self._on_dedicated_hotkey_triggered(binding)

    def save_and_apply(self, toggle_callback, silent=False):
        self._save_hotkeys()
        self.setup_hotkeys(toggle_callback, silent=silent)

    @property
    def hotkeys(self):
        return dict(self._hotkeys)

    def get_hotkey_config(self):
        return dict(self._hotkeys)

    def set_app(self, app):
        self._app = app

    def cleanup(self):
        self._native_hotkey_listener.stop()
        self._remove_registered_hotkeys()
