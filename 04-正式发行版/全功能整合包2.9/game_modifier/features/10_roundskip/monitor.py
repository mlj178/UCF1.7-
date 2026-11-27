import threading


class RoundSkipMonitor:
    def __init__(self, context, interval_ms=1500, run_async=None):
        self._context = context
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
                self._context.after_cancel(self._timer)
            except Exception:
                pass
            self._timer = None

    def _schedule_poll(self, delay_ms):
        if not self._running:
            return
        self._timer = self._context.after(delay_ms, self._poll_once)

    def _poll_once(self):
        self._timer = None
        if not self._should_poll():
            self.stop()
            return
        # P1：在主线程（after 回调里）排下一次，避免工作线程调 Tk after 的跨线程问题
        self._schedule_poll(self._interval_ms)
        if self._polling:
            return
        self._polling = True
        self._run_async(self._poll_status)

    def _poll_status(self):
        result = None
        try:
            result = self._context.feature_service.status("roundskip")
        except Exception:
            result = None
        finally:
            self._polling = False
        if result is None:
            # P1：脚本已销毁/连接断开 → 停止轮询，避免持续刷 "script has been destroyed"
            try:
                self._context.after(0, self.stop)
            except Exception:
                self.stop()

    def _should_poll(self):
        return bool(self._running and self._context.is_connected())

    @staticmethod
    def _start_thread(callback):
        threading.Thread(target=callback, daemon=True).start()
