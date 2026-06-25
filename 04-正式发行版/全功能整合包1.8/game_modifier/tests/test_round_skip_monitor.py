import unittest

from ui.controllers.round_skip_monitor import RoundSkipMonitor


class FakeRoundSkipActionService:
    def __init__(self):
        self.calls = []

    def get_round_status(self):
        self.calls.append("getRoundStatus")
        return {"ok": True, "hasInstance": False}


class FakeRoundSkipConnectionService:
    is_connected = True


class FakeRoundSkipApp:
    def __init__(self):
        self._ready = True
        self._game_action_service = FakeRoundSkipActionService()
        self._game_connection_service = FakeRoundSkipConnectionService()
        self.after_calls = []
        self.cancelled = []
        self.logs = []

    def after(self, delay, callback):
        timer_id = f"timer-{len(self.after_calls) + 1}"
        self.after_calls.append((timer_id, delay, callback))
        return timer_id

    def after_cancel(self, timer_id):
        self.cancelled.append(timer_id)

    def _log(self, message):
        self.logs.append(message)


class RoundSkipMonitorTests(unittest.TestCase):
    def test_start_polls_round_status_to_preinstall_hook(self):
        app = FakeRoundSkipApp()
        monitor = RoundSkipMonitor(app, interval_ms=1500, run_async=lambda fn: fn())

        monitor.start()
        _timer_id, delay, callback = app.after_calls.pop(0)
        callback()

        self.assertEqual(delay, 0)
        self.assertEqual(app._game_action_service.calls, ["getRoundStatus"])

        _timer_id, delay, callback = app.after_calls.pop(0)
        callback()
        self.assertEqual(app.after_calls[-1][1], 1500)

    def test_stop_cancels_pending_poll(self):
        app = FakeRoundSkipApp()
        monitor = RoundSkipMonitor(app, interval_ms=1500, run_async=lambda fn: fn())

        monitor.start()
        first_timer = app.after_calls[0][0]
        monitor.stop()

        self.assertEqual(app.cancelled, [first_timer])


if __name__ == "__main__":
    unittest.main()
