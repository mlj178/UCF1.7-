import threading
import weakref
from collections import defaultdict


class EventBus:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self._subscribers = defaultdict(list)
        self._lock = threading.Lock()

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

        for ref in subscribers:
            callback = self._resolve_ref(ref)
            if callback is None:
                continue
            try:
                threading.Thread(target=callback, kwargs=kwargs, daemon=True).start()
            except Exception:
                pass

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
                pass

    def clear(self):
        with self._lock:
            self._subscribers.clear()

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
