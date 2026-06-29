import threading


class RoundSkipMonitor:
    def __init__(self, app, interval_ms=1500, run_async=None):
        self._app = app
        self._interval_ms = interval_ms
        self._timer = None
        self._running = False
        self._polling = False
        self._run_async = run_async or self._start_thread

    def start(self):
        if self._running:
            return
        self._running = True
        self._schedule_poll(0)

    def stop(self):
        self._running = False
        if self._timer is not None:
            try:
                self._app.after_cancel(self._timer)
            except Exception:
                pass
            self._timer = None

    def _schedule_poll(self, delay_ms):
        if not self._running:
            return
        self._timer = self._app.after(delay_ms, self._poll_once)

    def _poll_once(self):
        self._timer = None
        if not self._should_poll():
            self.stop()
            return
        if self._polling:
            self._schedule_poll(self._interval_ms)
            return
        self._polling = True
        self._run_async(self._poll_status)

    def _poll_status(self):
        try:
            self._app._feature_service.status("roundskip")
        except Exception:
            # 预热轮询失败不打扰玩家；按钮点击时仍会给出明确失败原因。
            pass
        finally:
            self._polling = False
            try:
                self._app.after(0, lambda: self._schedule_poll(self._interval_ms))
            except Exception:
                self.stop()

    def _should_poll(self):
        connection = getattr(self._app, "_game_connection_service", None)
        return bool(
            self._running
            and getattr(self._app, "_ready", False)
            and connection is not None
            and getattr(connection, "is_connected", True)
        )

    @staticmethod
    def _start_thread(callback):
        threading.Thread(target=callback, daemon=True).start()
