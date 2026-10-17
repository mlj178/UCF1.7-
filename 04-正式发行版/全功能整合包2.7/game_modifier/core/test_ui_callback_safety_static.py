import unittest
from pathlib import Path


GAME_MODIFIER_DIR = Path(__file__).resolve().parent.parent
APP_FILE = GAME_MODIFIER_DIR / "ui" / "app.py"
EVENT_BUS_FILE = Path(__file__).with_name("event_bus.py")
FRIDA_FILE = Path(__file__).with_name("frida_manager.py")
APP_EVENT_FILE = GAME_MODIFIER_DIR / "ui" / "controllers" / "app_event_controller.py"
NANO4T_RUNTIME = GAME_MODIFIER_DIR / "features" / "15_nano4t" / "runtime.py"


def read(path):
    return path.read_text(encoding="utf-8")


class UiCallbackSafetyStaticTests(unittest.TestCase):
    """P0 护栏：「连接就绪链路」不允许再出现静默失效。"""

    def test_ui_callbacks_are_retried_by_a_heartbeat(self):
        text = read(APP_FILE)

        # 滞留回调必须有人兜底重投，而不是只靠 _mark_mainloop_ready 排空一次
        self.assertIn("self._ui_drain_timer = self.after(1000, self._ui_drain_heartbeat)", text)
        self.assertIn("def _drain_pending_ui_callbacks(self):", text)
        self.assertIn("def _take_pending_ui_callbacks(self):", text)
        self.assertIn("由心跳补投", text)
        # 心跳要随窗口关闭一起取消
        self.assertIn("self.after_cancel(self._ui_drain_timer)", text)

    def test_tk_callback_exceptions_are_written_to_the_log(self):
        text = read(APP_FILE)

        self.assertIn("self.report_callback_exception = _report", text)
        self.assertIn("TkCallback", text)
        self.assertIn("traceback.format_exception", text)

    def test_connection_ready_has_a_log_anchor(self):
        text = read(APP_EVENT_FILE)

        # 日志里缺这条 = 连接事件没跑到 UI 线程（功能会整体不生效）
        self.assertIn("UI 已就绪", text)

    def test_event_bus_records_dropped_events(self):
        text = read(EVENT_BUS_FILE)

        self.assertIn("def _report_dropped_event(self, event_type, callback):", text)
        self.assertIn("self._report_dropped_event(event_type, callback)", text)
        self.assertIn("事件队列已满", text)

    def test_plugin_rpc_short_circuit_is_logged(self):
        text = read(FRIDA_FILE)

        self.assertIn("def _log_plugin_call_skipped(self, feature_id, action, reason):", text)
        self.assertIn("self._log_plugin_call_skipped(", text)
        self.assertIn("插件 RPC 客户端不可用", text)

    def test_nano4t_init_skips_are_logged(self):
        text = read(NANO4T_RUNTIME)

        self.assertIn("def _log_skipped(self, action, reason):", text)
        # 未连接 / 异常两条路径都必须留痕，不允许裸吞
        self.assertIn('self._log_skipped("nano4tInit", "is_connected()==False")', text)
        self.assertIn('self._log_skipped("nano4tInit", f"exception: {exc}")', text)
        self.assertIn('self._log_skipped("nano4tGetCurrent", f"exception: {exc}")', text)


if __name__ == "__main__":
    unittest.main()
