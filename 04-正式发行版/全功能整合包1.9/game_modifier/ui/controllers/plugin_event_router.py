import importlib.util
from pathlib import Path


class PluginEventRouter:
    def __init__(self, registry, context):
        self._registry = registry
        self._context = context
        self._handlers = {}

    def route(self, feature_id, event, payload):
        handler = self._load_handler(feature_id)
        if not handler:
            self._context.emit(
                "log_message",
                level="info",
                module="PluginEventRouter",
                message=f"未找到插件事件处理器: {feature_id}.{event}",
                audience="dev",
            )
            return False
        try:
            handler(self._context.for_feature(feature_id), event, payload or {})
            return True
        except Exception as exc:
            self._context.emit(
                "log_message",
                level="error",
                module="PluginEventRouter",
                message=f"插件事件处理失败: {feature_id}.{event}",
                audience="dev",
                dev_detail=str(exc),
            )
            return False

    def _load_handler(self, feature_id):
        if feature_id in self._handlers:
            return self._handlers[feature_id]
        feature = self._registry.get(feature_id)
        if not feature:
            self._handlers[feature_id] = None
            return None
        plugin_dir = Path(feature.manifest.get("_plugin_dir", ""))
        events_path = plugin_dir / "events.py"
        if not events_path.exists():
            self._handlers[feature_id] = None
            return None
        try:
            spec = importlib.util.spec_from_file_location(f"_plugin_events_{feature_id}", events_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            handler = getattr(module, "handle_event", None)
            self._handlers[feature_id] = handler if callable(handler) else None
        except Exception as exc:
            self._handlers[feature_id] = None
            self._context.emit(
                "log_message",
                level="error",
                module="PluginEventRouter",
                message=f"插件事件模块加载失败: {feature_id}",
                audience="dev",
                dev_detail=str(exc),
            )
        return self._handlers[feature_id]
