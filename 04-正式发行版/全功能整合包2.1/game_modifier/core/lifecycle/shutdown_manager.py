from core.log_manager import get_logger


class ShutdownManager:
    """Collect shutdown hooks without changing existing application shutdown."""

    def __init__(self, logger=None):
        self._hooks = []
        self._logger = logger or get_logger("Shutdown")

    def register(self, callback):
        self._hooks.append(callback)
        return callback

    def cleanup(self, reason="shutdown"):
        for callback in reversed(self._hooks):
            try:
                callback(reason)
            except Exception as exc:
                self._logger.warning(f"shutdown hook failed: {exc}")
