import json
import threading
import time
from pathlib import Path

from core.config import FEATURES_DIR
from core.log_manager import get_logger


class ScriptManager:
    """Manage one Frida JS script per feature_id."""

    def __init__(
        self,
        session_manager=None,
        manifests=None,
        features_dir=None,
        logger=None,
        message_handler=None,
    ):
        self.session_manager = session_manager
        self.features_dir = Path(features_dir or FEATURES_DIR)
        self.manifests = {item["feature_id"]: item for item in (manifests or []) if item.get("feature_id")}
        self._logger = logger or get_logger("PluginScript")
        self._message_handler = message_handler
        self._scripts = {}
        self._lock = threading.RLock()
        self._last_rpc_missing_log_at = {}
        self._log_throttle_seconds = 3.0

    def set_manifests(self, manifests):
        self.manifests = {item["feature_id"]: item for item in manifests if item.get("feature_id")}

    def _script_path(self, feature_id):
        manifest = self.manifests.get(feature_id, {})
        script_name = manifest.get("script", "script.js")
        plugin_dir = Path(manifest.get("_plugin_dir") or self.features_dir / feature_id)
        return plugin_dir / script_name

    def load(self, feature_id):
        # P2：同一 feature_id 可能被 UI 线程与功能后台线程同时 load，原实现无同步，
        # 会重复 create_script/load（重复 Hook，且先创建的句柄失去引用泄漏）。这里串行化加载。
        with self._lock:
            if feature_id in self._scripts:
                return self._scripts[feature_id]
            if not self.session_manager or not self.session_manager.session:
                raise RuntimeError("frida session is not attached")

            script_path = self._script_path(feature_id)
            with script_path.open("r", encoding="utf-8") as handle:
                js_code = handle.read()
            script = self.session_manager.session.create_script(js_code)
            if self._message_handler:
                script.on("message", self._message_handler)
            script.load()
            self._scripts[feature_id] = script
            return script

    def unload(self, feature_id):
        with self._lock:
            script = self._scripts.pop(feature_id, None)
        if not script:
            return
        try:
            script.unload()
        except Exception as exc:
            if self._is_script_destroyed_error(exc):
                self._logger.debug(f"plugin script already destroyed during unload {feature_id}: {exc}")
            else:
                self._logger.warning(f"failed to unload plugin script {feature_id}: {exc}")

    def reload(self, feature_id):
        self.unload(feature_id)
        return self.load(feature_id)

    def call(self, feature_id, action, payload=None):
        script = self._scripts.get(feature_id) or self.load(feature_id)
        exports = getattr(script, "exports_sync", None)
        if exports is None:
            raise RuntimeError(f"plugin script {feature_id} has no exports_sync")
        candidates = self._rpc_candidates(action)
        missing_errors = []
        for candidate in candidates:
            fn = getattr(exports, candidate, None)
            if fn is None:
                continue
            try:
                result = fn() if payload is None else fn(payload)
            except Exception as exc:
                if self._is_missing_rpc_method_error(exc):
                    missing_errors.append(f"{candidate}: {exc}")
                    continue
                if self._is_script_destroyed_error(exc):
                    # P1：脚本已被销毁时原实现仍把旧句柄留在 _scripts 里，之后每次调用都失败。
                    # 这里丢弃句柄，下次 call() 会自动 load() 重建。
                    self._invalidate(feature_id, script)
                raise
            if isinstance(result, str):
                try:
                    return json.loads(result)
                except (json.JSONDecodeError, TypeError):
                    return result
            return result

        message = (
            "plugin script missing rpc action: "
            f"feature_id={feature_id}, action={action}, candidates={candidates}"
        )
        if missing_errors:
            message = f"{message}, missing_errors={missing_errors}"
        self._log_missing_rpc(feature_id, action, message)
        raise AttributeError(message)

    def _invalidate(self, feature_id, script):
        with self._lock:
            self._scripts.pop(feature_id, None)
        try:
            script.unload()
        except Exception as exc:
            self._logger.debug(f"failed to unload destroyed plugin script {feature_id}: {exc}")
        self._logger.warning(
            f"plugin script {feature_id} was destroyed; handle dropped, will reload on next call"
        )

    def cleanup_all(self, reason):
        for feature_id in list(self._scripts.keys()):
            try:
                self.call(feature_id, "cleanup", {"reason": reason})
            except Exception as exc:
                if self._is_script_destroyed_error(exc):
                    self._logger.debug(f"plugin cleanup skipped for destroyed script {feature_id}: {exc}")
                else:
                    self._logger.warning(f"plugin cleanup failed for {feature_id}: {exc}")
            self.unload(feature_id)

    @staticmethod
    def _rpc_candidates(action):
        snake_action = "".join(["_" + c.lower() if c.isupper() else c for c in action]).lstrip("_")
        first_lower = action[0].lower() + action[1:] if action else action
        snake_parts = [part for part in action.split("_") if part]
        snake_camel = ""
        if snake_parts:
            snake_camel = snake_parts[0] + "".join(part[:1].upper() + part[1:] for part in snake_parts[1:])
        ordered = [
            action,
            first_lower,
            action.lower(),
            snake_action,
            snake_camel,
            action.replace("_", "").lower(),
        ]
        candidates = []
        for name in ordered:
            if name and name not in candidates:
                candidates.append(name)
        return candidates

    @staticmethod
    def _is_missing_rpc_method_error(exc):
        return "unable to find method" in str(exc).lower()

    @staticmethod
    def _is_script_destroyed_error(exc):
        message = str(exc).lower()
        return "script has been destroyed" in message or "script is destroyed" in message

    def _log_missing_rpc(self, feature_id, action, message):
        key = (feature_id, action, message)
        now = time.monotonic()
        last = self._last_rpc_missing_log_at.get(key)
        if last is not None and now - last < self._log_throttle_seconds:
            return
        self._last_rpc_missing_log_at[key] = now
        self._logger.error(message)
