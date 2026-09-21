import json
import threading
import time

import frida
import psutil

from core.event_bus import EventBus
from core.frida_diagnostics import FridaConnectDiagnostic
from core.frida_runtime.rpc_client import RpcClient
from core.frida_runtime.script_manager import ScriptManager
from core.log_manager import log_to_file
from core.plugin.manifest_loader import ManifestLoader


class _FridaSessionAdapter:
    def __init__(self, frida_manager):
        self._frida_manager = frida_manager

    @property
    def session(self):
        return self._frida_manager.session


class LogManager:
    """日志文件管理器 - bridges to standard logging"""

    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def write_log(self, module, level, message):
        log_to_file(level, module, message)

    def write_log_unified(self, level, module, message):
        log_to_file(level, module, message)


class FridaManager:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self._session = None
        self._ready = False
        self._connecting = False
        self._disconnecting = False
        self._pid = None
        self._script_manager = None
        self._rpc_client = None
        self._last_rpc_error_log_at = {}
        self._rpc_error_log_throttle_seconds = 3.0
        self._lock = threading.Lock()
        self._event_bus = EventBus.get_instance()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @property
    def is_connected(self):
        return self._ready and self._session is not None

    @property
    def pid(self):
        return self._pid

    @property
    def session(self):
        return self._session

    def is_ready(self):
        return self.is_connected

    def find_pid(self):
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if proc.info["name"] and "unitycrossfire" in proc.info["name"].lower():
                    return proc.info["pid"]
            except Exception:
                pass
        return None

    def connect(self, pid):
        with self._lock:
            if self._connecting:
                return False, "already_connecting"
            self._connecting = True

        session = None
        try:
            try:
                session = frida.attach(pid)
            except frida.ProcessNotFoundError as e:
                return False, FridaConnectDiagnostic.collect("process_not_found", pid, e)
            except frida.PermissionDeniedError as e:
                return False, FridaConnectDiagnostic.collect("permission_denied", pid, e)
            except frida.TransportError as e:
                error_msg = str(e)
                if "0xc000010a" in error_msg or "STATUS_PROCESS_IS_TERMINATING" in error_msg:
                    return False, "process_terminating"
                if "architecture" in error_msg.lower():
                    return False, FridaConnectDiagnostic.collect("architecture_mismatch", pid, e)
                return False, FridaConnectDiagnostic.collect("connection_failed", pid, e)

            manifests = ManifestLoader().load()
            script_manager = ScriptManager(
                session_manager=_FridaSessionAdapter(self),
                manifests=manifests,
                message_handler=self._on_message,
            )
            rpc_client = RpcClient(script_manager)

            self._session = session
            self._pid = pid
            self._script_manager = script_manager
            self._rpc_client = rpc_client
            self._ready = True
            self._event_bus.emit(
                "log_message",
                level="info",
                module="系统",
                message="全功能整合包插件运行时 v2.6 已就绪",
                audience="dev",
                dev_detail="Frida session attached; plugin scripts load on demand",
            )
            return True, "success"

        except Exception as e:
            if session:
                try:
                    session.detach()
                except Exception:
                    pass
            error_msg = str(e)
            if "0xc000010a" in error_msg or "STATUS_PROCESS_IS_TERMINATING" in error_msg:
                return False, "process_terminating"
            return False, FridaConnectDiagnostic.collect("connection_failed", pid, e)

        finally:
            self._connecting = False

    def disconnect(self):
        with self._lock:
            if self._disconnecting:
                return
            self._disconnecting = True
            session = self._session
            script_manager = self._script_manager
            self._session = None
            self._ready = False
            self._pid = None
            self._script_manager = None
            self._rpc_client = None

        try:
            if script_manager:
                try:
                    script_manager.cleanup_all("python_disconnect")
                    log_to_file("info", "系统", "Plugin scripts cleaned up before Frida detach")
                except Exception as e:
                    log_to_file("warning", "系统", f"Plugin script cleanup failed: {e}")

            if session:
                try:
                    session.detach()
                    log_to_file("info", "系统", "Frida session detached")
                except Exception as e:
                    log_to_file("warning", "系统", f"Frida session detach failed: {e}")
        finally:
            with self._lock:
                self._disconnecting = False

    def plugin_call(self, feature_id, action, payload=None):
        with self._lock:
            if self._disconnecting or not self._rpc_client:
                return None
            rpc_client = self._rpc_client
        try:
            return rpc_client.call(feature_id, action, payload)
        except Exception as e:
            if self._should_log_rpc_error(feature_id, action, e):
                self._event_bus.emit(
                    "log_message",
                    level="error",
                    module="Plugin",
                    message=f"{feature_id} 调用失败",
                    audience="both",
                    dev_detail=f"Plugin RPC failed: {feature_id}.{action}: {e}",
                )
            return None

    def plugin_cleanup_all(self, reason):
        with self._lock:
            script_manager = self._script_manager
        if not script_manager:
            return None
        return script_manager.cleanup_all(reason)

    def _on_message(self, msg, data):
        if msg["type"] != "send":
            return
        payload = msg["payload"]
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except (json.JSONDecodeError, TypeError):
                return

        msg_type = payload.get("type", "")

        if msg_type == "log":
            self._event_bus.emit(
                "log_message",
                level=payload.get("level", "info"),
                module=payload.get("module", ""),
                message=payload.get("message", ""),
                audience=payload.get("audience", "dev"),
                dev_detail=payload.get("dev_detail", ""),
            )

        elif msg_type == "log_file":
            self._event_bus.emit(
                "log_message",
                level=payload.get("level", "info"),
                module=payload.get("module", ""),
                message=payload.get("message", ""),
                audience=payload.get("audience", "dev"),
                dev_detail=payload.get("dev_detail", ""),
            )

        elif msg_type == "status":
            self._event_bus.emit(
                "feature_status_changed",
                feature=payload.get("feature", ""),
                enabled=payload.get("enabled", False),
            )

        elif msg_type == "plugin_event":
            self._event_bus.emit(
                "plugin_event",
                feature=payload.get("feature", ""),
                event=payload.get("event", ""),
                payload=payload.get("payload", {}),
                audience=payload.get("audience", "dev"),
            )

        else:
            self._event_bus.emit(
                "log_message",
                level="warning",
                module="Frida",
                message=f"未知插件消息类型: {msg_type}",
                audience="dev",
                dev_detail=f"Unknown Frida message payload: {payload}",
            )

    def restore_features(self, features_state):
        for feature_id, enabled in features_state.items():
            if enabled:
                self.plugin_call(feature_id, "enable", {})

    def _should_log_rpc_error(self, feature_id, action, error):
        key = (feature_id, action, str(error))
        now = time.monotonic()
        last = self._last_rpc_error_log_at.get(key)
        if last is not None and now - last < self._rpc_error_log_throttle_seconds:
            return False
        self._last_rpc_error_log_at[key] = now
        return True
