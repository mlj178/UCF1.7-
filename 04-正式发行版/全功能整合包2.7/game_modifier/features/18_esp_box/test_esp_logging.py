import sys
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
HOOK_MANAGER = PACKAGE_ROOT / "core" / "universal_hook_manager.py"
SESSION = PACKAGE_ROOT / "core" / "game_session_manager.py"
LOG_ROUTER = PACKAGE_ROOT / "core" / "log_router.py"


class EspLoggingTests(unittest.TestCase):
    """方框透视的控制面日志必须能落盘：否则出问题只能靠猜。"""

    def setUp(self):
        if str(PACKAGE_ROOT) not in sys.path:
            sys.path.insert(0, str(PACKAGE_ROOT))

    def test_both_audience_writes_to_dev_log(self):
        from core.log_router import build_log_route

        route = build_log_route(
            level="success", module="Universal", message="x", audience="both"
        )
        self.assertTrue(route.write_to_dev_log)
        self.assertTrue(route.show_in_ui)

        # 默认 user 只进界面、不落盘（这正是之前日志里看不到方框透视的原因）
        default_route = build_log_route(level="success", module="Universal", message="x")
        self.assertFalse(default_route.write_to_dev_log)

    def test_universal_logger_sends_audience_both(self):
        source = HOOK_MANAGER.read_text(encoding="utf-8")
        block = source.split("def _log(self, level, message):", 1)[1].split("def ", 1)[0]
        self.assertIn('module="Universal"', block)
        self.assertIn('audience="both"', block)

    def test_push_result_logs_confirmed_values(self):
        source = HOOK_MANAGER.read_text(encoding="utf-8")
        # 成功下发后把 DLL 回读确认的生效值写进日志
        for token in ("显示对象={}", "血量={}/{}", "方框={}", "rev={}"):
            self.assertIn(token, source)
        # 失败也要落盘（走 _log -> audience both）
        self.assertIn("方框透视选项下发失败", source)

    def test_session_manager_esp_logs_reach_dev_log(self):
        source = SESSION.read_text(encoding="utf-8")
        for token in (
            "message='ESP DLL 已连接', audience='both'",
            "message='ESP DLL 已在后台就绪', audience='both'",
            "audience='both',",
        ):
            self.assertIn(token, source)
        self.assertIn("方框模块稍后重试", source)

    def test_render_diagnostics_reach_the_log(self):
        manager = HOOK_MANAGER.read_text(encoding="utf-8")
        session = SESSION.read_text(encoding="utf-8")
        self.assertIn("def fetch_diagnostics", manager)
        self.assertIn("esp_diag_candidates", manager)
        self.assertIn("_log_esp_diagnostics", session)
        self.assertIn("方框透视诊断", session)

    def test_event_controller_writes_universal_message(self):
        """端到端：Universal 的 log_message 经 AppEventController 落到 log_writer。"""
        import types

        from core.event_bus import EventBus
        from ui.controllers.app_event_controller import AppEventController

        written = []
        app = types.SimpleNamespace(
            _plugin_registry={},
            _panel_context=None,
            _ui_ready=True,
            _early_log_messages=[],
            _log=lambda message: None,
        )
        controller = AppEventController(app, log_writer=lambda level, module, message: written.append((level, module, message)))

        bus = EventBus.get_instance()
        controller.register(bus)
        # EventBus.emit 是异步的（工作线程 + 队列），测试用 emit_sync 保证确定性
        bus.emit_sync(
            "log_message",
            level="success",
            module="Universal",
            message="方框透视已开启：显示对象=all_players",
            audience="both",
        )

        self.assertEqual(len(written), 1)
        self.assertEqual(written[0][1], "Universal")
        self.assertIn("显示对象=all_players", written[0][2])


if __name__ == "__main__":
    unittest.main()
