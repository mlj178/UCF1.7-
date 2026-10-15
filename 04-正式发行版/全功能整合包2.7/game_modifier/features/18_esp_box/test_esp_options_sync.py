import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest import mock


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = Path(
    r"D:\trae_project\ucf1.7-modifier\05-正式功能\18-Universal-ESP盒子\Universal-Dear-ImGui-Hook"
)
SESSION = PACKAGE_ROOT / "core" / "game_session_manager.py"
HOOK_MANAGER = PACKAGE_ROOT / "core" / "universal_hook_manager.py"
SERVICE = PACKAGE_ROOT / "core" / "services" / "feature_command_service.py"
PANEL = Path(__file__).parent / "panel.py"


APPLIED = {
    "esp_target_scope": "enemy_only",
    "esp_health_mode": "percent",
    "esp_health_display": "both",
    "esp_box_outline": True,
}


class _StubConfig:
    def __init__(self, data=None):
        self.data = {key: dict(value) for key, value in (data or {}).items()}

    def get(self, feature_id, default=None):
        merged = dict(self.data.get(feature_id, {}))
        if not merged and default is not None:
            return default
        return merged

    def set(self, feature_id, config):
        current = dict(self.data.get(feature_id, {}))
        current.update(config or {})
        self.data[feature_id] = current
        return current

    def remove_user_key(self, feature_id, key):
        current = dict(self.data.get(feature_id, {}))
        current.pop(key, None)
        self.data[feature_id] = current
        return current


class _StubFrida:
    def __init__(self):
        self.calls = []

    def plugin_call(self, feature_id, action, payload=None):
        self.calls.append((feature_id, action, payload))
        return True


class _StubSession:
    def __init__(self, applied):
        self.applied = applied
        self.calls = []

    def set_esp_target_scope(self, scope):
        self.calls.append(("scope", scope))
        return True

    def set_esp_health_options(self, health_mode=None, health_display=None):
        self.calls.append(("health", health_mode, health_display))
        return True

    def set_esp_box_outline(self, enabled):
        self.calls.append(("outline", enabled))
        return True

    def get_applied_esp_options(self):
        return None if self.applied is None else dict(self.applied)


class EspOptionSyncTests(unittest.TestCase):
    """所选即所得：界面配置与 DLL 实际生效值必须一致。"""

    def setUp(self):
        if str(PACKAGE_ROOT) not in sys.path:
            sys.path.insert(0, str(PACKAGE_ROOT))

    def _service(self, applied, config_data=None):
        from core.game_session_manager import GameSessionManager
        from core.services.feature_command_service import FeatureCommandService

        self.session = _StubSession(applied)
        self.frida = _StubFrida()
        self.config = _StubConfig(config_data or {"esp_box": dict(APPLIED)})
        patcher = mock.patch.object(
            GameSessionManager, "get_instance", staticmethod(lambda: self.session)
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        return FeatureCommandService(self.frida, self.config)

    def test_rejected_change_is_rolled_back_to_applied_value(self):
        service = self._service(applied=APPLIED)
        service.set_config("esp_box", {"esp_health_display": "text"})

        # 下发过（说明确实尝试生效），但 DLL 拒绝 -> 配置回退成生效值
        self.assertIn(("health", "percent", "text"), self.session.calls)
        self.assertEqual(self.config.data["esp_box"]["esp_health_display"], "both")
        self.assertEqual(self.frida.calls[-1][2]["esp_health_display"], "both")

    def test_rollback_only_touches_the_changed_key(self):
        service = self._service(applied=APPLIED)
        service.set_config("esp_box", {"esp_target_scope": "all_players"})
        self.assertEqual(self.config.data["esp_box"]["esp_target_scope"], "enemy_only")
        self.assertEqual(self.config.data["esp_box"]["esp_health_mode"], "percent")
        self.assertEqual(self.config.data["esp_box"]["esp_box_outline"], True)

    def test_successful_change_is_kept(self):
        applied = dict(APPLIED)
        applied["esp_health_display"] = "text"
        service = self._service(applied=applied)
        service.set_config("esp_box", {"esp_health_display": "text"})
        self.assertEqual(self.config.data["esp_box"]["esp_health_display"], "text")

    def test_disconnected_change_is_kept_for_next_connect(self):
        # 没有连上 DLL 时只落盘：保留用户选择，等连接时再按配置下发。
        service = self._service(applied=None)
        service.set_config("esp_box", {"esp_health_display": "text"})
        self.assertEqual(self.config.data["esp_box"]["esp_health_display"], "text")

    def test_box_outline_rolls_back_too(self):
        service = self._service(applied=APPLIED)
        service.set_config("esp_box", {"esp_box_outline": False})
        self.assertEqual(self.config.data["esp_box"]["esp_box_outline"], True)

    def test_new_options_do_not_need_to_be_present_in_config(self):
        # 配置里只有部分键时，也不能把整份配置覆盖掉。
        service = self._service(applied=APPLIED, config_data={"esp_box": {}})
        service.set_config("esp_box", {"esp_target_scope": "enemy_only"})
        self.assertEqual(self.config.data["esp_box"], {"esp_target_scope": "enemy_only"})


class EspOptionSyncStaticTests(unittest.TestCase):
    def test_every_push_path_refreshes_from_persisted_config(self):
        source = SESSION.read_text(encoding="utf-8")
        self.assertGreaterEqual(source.count("self._refresh_esp_target_scope_from_config()"), 5)

        desired = source.split("def set_desired_state", 1)[1].split(
            "def _refresh_esp_target_scope_from_config", 1
        )[0]
        # 开关路径必须带完整选项下发，不能只调会用缓存旧值的 set_esp_box()
        self.assertNotIn(".set_esp_box(", desired)
        self.assertIn("set_esp_state(", desired)

        connect = source.split("def _connect_universal_for_esp", 1)[1]
        self.assertIn("_refresh_esp_target_scope_from_config()", connect)
        self.assertLess(
            connect.index("_refresh_esp_target_scope_from_config()"),
            connect.index("set_esp_state("),
        )

    def test_applied_state_is_exposed_and_used(self):
        self.assertIn("get_applied_esp_options", SESSION.read_text(encoding="utf-8"))
        self.assertIn("def get_esp_options", HOOK_MANAGER.read_text(encoding="utf-8"))
        self.assertIn("_apply_esp_options", SERVICE.read_text(encoding="utf-8"))

    def test_panel_resyncs_widgets_from_config(self):
        panel = PANEL.read_text(encoding="utf-8")
        self.assertIn("sync_from_config", panel)
        self.assertIn("schedule_sync", panel)
        self.assertIn(".after(", panel)
        self.assertEqual(panel.count("schedule_sync()"), 5)  # 定义 1 次 + 四个回调

    def test_cpp_state_has_outline_hook_for_the_switch(self):
        state = (SOURCE_ROOT / "esp" / "esp_state.h").read_text(encoding="utf-8")
        self.assertIn("IsBoxOutlineEnabled", state)


# ---------------------------------------------------------------------------
# 用假 customtkinter 直接跑 panel.build_card()：验证「改动 -> 失败回退 -> 控件回读」
# 这条 UI 路径真的能把界面拉回实际生效值（所选即所得）。
# ---------------------------------------------------------------------------
class _FakeWidget:
    def __init__(self, *args, **kwargs):
        self._after_calls = []

    def pack(self, *args, **kwargs):
        pass

    def grid(self, *args, **kwargs):
        pass

    def configure(self, *args, **kwargs):
        pass

    def grid_columnconfigure(self, *args, **kwargs):
        pass

    def columnconfigure(self, *args, **kwargs):
        pass

    def rowconfigure(self, *args, **kwargs):
        pass

    def after(self, delay, callback):
        self._after_calls.append((delay, callback))
        return len(self._after_calls)

    def after_cancel(self, timer_id):
        pass

    def run_after(self):
        for _delay, callback in list(self._after_calls):
            callback()


class _FakeCombo(_FakeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = ""
        self.command = kwargs.get("command")

    def set(self, value):
        self._value = value

    def get(self):
        return self._value

    def choose(self, value):
        self.set(value)
        if self.command:
            self.command(value)


class _FakeSwitch(_FakeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = kwargs.get("command")
        self._on = False

    def select(self):
        self._on = True

    def deselect(self):
        self._on = False

    def get(self):
        return 1 if self._on else 0

    def toggle(self, on):
        self._on = bool(on)
        if self.command:
            self.command()


def _fake_ctk():
    module = types.ModuleType("customtkinter")
    module.CTkFrame = _FakeWidget
    module.CTkLabel = _FakeWidget
    module.CTkComboBox = _FakeCombo
    module.CTkSwitch = _FakeSwitch
    return module


MANIFEST = {
    "feature_id": "esp_box",
    "display_name": "方框透视",
    "desc": "通过 Universal DLL 显示方框透视",
    "config": {
        "esp_target_scope": "enemy_only",
        "esp_health_mode": "percent",
        "esp_health_display": "both",
        "esp_box_outline": True,
    },
    "ui_handles": {"switch": "esp_box_switch"},
    "layout": {},
}


class EspPanelSyncTests(unittest.TestCase):
    def _build(self, config):
        module = types.ModuleType("esp_panel_under_test")
        spec = importlib.util.spec_from_file_location(module.__name__, PANEL)
        with mock.patch.dict(sys.modules, {"customtkinter": _fake_ctk()}):
            spec.loader.exec_module(module)

        self.sent = []

        def set_config(feature_id, key, value):
            self.sent.append((key, value))
            config[key] = value

        callbacks = {
            "toggle": lambda *args: None,
            "set_config": set_config,
            "get_config": lambda feature_id: dict(config),
        }
        handles = module.build_card(None, MANIFEST, 0, 0, 1, callbacks, None)
        return handles

    @staticmethod
    def _run_scheduled(handles):
        """跑一遍控件上挂的 after 定时回调（sync_from_config）。"""
        for widget in handles.values():
            runner = getattr(widget, "run_after", None)
            if callable(runner):
                runner()

    def test_change_is_pushed_with_the_selected_value(self):
        config = dict(MANIFEST["config"])
        handles = self._build(config)
        handles["esp_health_display_menu"].choose("仅数值")
        self.assertEqual(self.sent[-1], ("esp_health_display", "text"))

    def test_widget_snaps_back_when_dll_rejected_the_change(self):
        config = dict(MANIFEST["config"])
        handles = self._build(config)
        combo = handles["esp_health_display_menu"]

        combo.choose("仅数值")
        self.assertEqual(combo.get(), "仅数值")

        # 模拟后端：DLL 拒绝 -> 配置回退成生效值
        config["esp_health_display"] = "both"
        self._run_scheduled(handles)
        self.assertEqual(combo.get(), "血条和数值")

    def test_outline_switch_pushes_bool_and_snaps_back(self):
        config = dict(MANIFEST["config"])
        handles = self._build(config)
        switch = handles["esp_box_outline_switch"]

        switch.toggle(False)
        self.assertEqual(self.sent[-1], ("esp_box_outline", False))

        config["esp_box_outline"] = True
        self._run_scheduled(handles)
        self.assertEqual(switch.get(), 1)

    def test_scope_and_mode_widgets_snap_back_too(self):
        config = dict(MANIFEST["config"])
        handles = self._build(config)

        scope = handles["esp_target_scope_menu"]
        scope.choose("敌人和队友")
        config["esp_target_scope"] = "enemy_only"
        self._run_scheduled(handles)
        self.assertEqual(scope.get(), "仅显示敌人")

        mode = handles["esp_health_mode_menu"]
        mode.choose("剩余数值")
        config["esp_health_mode"] = "percent"
        self._run_scheduled(handles)
        self.assertEqual(mode.get(), "百分比")


if __name__ == "__main__":
    unittest.main()
