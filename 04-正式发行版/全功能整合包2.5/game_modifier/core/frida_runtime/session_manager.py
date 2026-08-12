import threading

from core.log_manager import get_logger


class SessionManager:
    """Own a Frida session for future per-plugin scripts."""

    def __init__(self, frida_module=None, logger=None):
        self._frida = frida_module
        self._logger = logger or get_logger("FridaSession")
        self._lock = threading.RLock()
        self._session = None
        self._pid = None

    @property
    def session(self):
        return self._session

    @property
    def pid(self):
        return self._pid

    def attach(self, pid):
        if self._frida is None:
            import frida

            self._frida = frida
        with self._lock:
            if self._session and self._pid == pid:
                return self._session
            self.detach()
            self._session = self._frida.attach(pid)
            self._pid = pid
            return self._session

    def detach(self):
        with self._lock:
            session = self._session
            self._session = None
            self._pid = None
        if session:
            try:
                session.detach()
            except Exception as exc:
                self._logger.warning(f"frida session detach failed: {exc}")
