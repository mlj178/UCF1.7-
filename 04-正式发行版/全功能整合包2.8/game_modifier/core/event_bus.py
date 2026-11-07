import queue
import threading
import time
import traceback
import weakref
from collections import defaultdict


class EventBus:
    _instance = None
    _lock = threading.Lock()

    MAX_QUEUE = 2000
    WORKERS = 2

    def __init__(self):
        self._subscribers = defaultdict(list)
        self._lock = threading.Lock()
        self._event_queue = queue.Queue(maxsize=self.MAX_QUEUE)
        self._workers = []
        self._dropped_events = 0
        self._stopping = False
        self._error_log_at = {}
        self._drop_log_at = {}
        self._error_log_throttle_seconds = 3.0

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def subscribe(self, event_type, callback):
        with self._lock:
            ref = weakref.WeakMethod(callback) if hasattr(callback, '__self__') else callback
            self._subscribers[event_type].append(ref)

    def unsubscribe(self, event_type, callback):
        with self._lock:
            if event_type in self._subscribers:
                self._subscribers[event_type] = [
                    ref for ref in self._subscribers[event_type]
                    if not self._is_same_callback(ref, callback)
                ]

    def emit(self, event_type, **kwargs):
        with self._lock:
            subscribers = list(self._subscribers.get(event_type, []))
        if not subscribers:
            return

        # P1：原来每条事件对每个订阅者都新建一个线程，日志量大时会造成线程风暴。
        # 改为固定 2 个工作线程 + 有界队列；队列满时丢弃并计数，保证不拖垮 UI。
        # P0：丢弃必须留痕 —— 原实现只加计数，连 connection_status 这类关键事件被丢掉
        # 也毫无记录，表现为“功能整体不生效且日志空白”。
        self._ensure_workers()
        for ref in subscribers:
            callback = self._resolve_ref(ref)
            if callback is None:
                continue
            try:
                self._event_queue.put_nowait((callback, kwargs))
            except queue.Full:
                self._dropped_events += 1
                self._report_dropped_event(event_type, callback)

    def _ensure_workers(self):
        with self._lock:
            if self._stopping:
                return
            self._workers = [w for w in self._workers if w.is_alive()]
            while len(self._workers) < self.WORKERS:
                worker = threading.Thread(
                    target=self._worker_loop,
                    name=f"event-bus-{len(self._workers) + 1}",
                    daemon=True,
                )
                worker.start()
                self._workers.append(worker)

    def _worker_loop(self):
        while True:
            try:
                item = self._event_queue.get()
            except Exception:
                continue
            if item is None:
                return
            callback, kwargs = item
            try:
                callback(**kwargs)
            except Exception:
                self._report_subscriber_error(callback)

    @property
    def dropped_events(self):
        return self._dropped_events

    def emit_sync(self, event_type, **kwargs):
        with self._lock:
            subscribers = list(self._subscribers.get(event_type, []))

        for ref in subscribers:
            callback = self._resolve_ref(ref)
            if callback is None:
                continue
            try:
                callback(**kwargs)
            except Exception:
                self._report_subscriber_error(callback)

    def clear(self):
        with self._lock:
            self._subscribers.clear()

    def shutdown(self, timeout=2.0):
        """Stop the worker threads explicitly; safe to call more than once."""
        with self._lock:
            if self._stopping:
                return
            self._stopping = True
            workers = list(self._workers)
            self._workers = []
        self.clear()
        for _ in workers:
            try:
                self._event_queue.put_nowait(None)
            except queue.Full:
                break
        for worker in workers:
            if worker.is_alive():
                worker.join(timeout)

    def _report_dropped_event(self, event_type, callback):
        """队列满导致事件被丢弃时落盘（按事件类型限频），避免关键事件静默消失。"""
        try:
            key = ("dropped", str(event_type))
            now = time.monotonic()
            last = self._drop_log_at.get(key)
            if last is not None and now - last < self._error_log_throttle_seconds:
                return
            self._drop_log_at[key] = now
            from core.log_manager import log_to_file
            name = (
                getattr(callback, "__qualname__", None)
                or getattr(callback, "__name__", None)
                or repr(callback)
            )
            log_to_file(
                "error",
                "EventBus",
                f"事件队列已满，已丢弃事件 {event_type} → {name}"
                f"（累计丢弃 {self._dropped_events} 条；该订阅者本次不会收到通知）",
            )
        except Exception:
            pass

    def _report_subscriber_error(self, callback):
        """Isolate subscriber failures; report them throttled instead of swallowing."""
        try:
            key = id(callback)
            now = time.monotonic()
            last = self._error_log_at.get(key)
            if last is not None and now - last < self._error_log_throttle_seconds:
                return
            self._error_log_at[key] = now
            from core.log_manager import log_to_file
            name = (
                getattr(callback, "__qualname__", None)
                or getattr(callback, "__name__", None)
                or repr(callback)
            )
            detail = traceback.format_exc(limit=3).strip().replace("\n", " | ")
            log_to_file("error", "EventBus", f"事件订阅者异常 {name}: {detail}")
        except Exception:
            pass

    @staticmethod
    def _is_same_callback(ref, callback):
        if isinstance(ref, weakref.WeakMethod):
            target = ref()
            return target is callback
        return ref is callback

    @staticmethod
    def _resolve_ref(ref):
        if isinstance(ref, weakref.WeakMethod):
            return ref()
        return ref


def on_event(event_type):
    def decorator(func):
        EventBus.get_instance().subscribe(event_type, func)
        return func
    return decorator
