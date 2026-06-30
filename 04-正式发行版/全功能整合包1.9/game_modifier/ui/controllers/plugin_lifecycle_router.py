import importlib.util
from pathlib import Path


class PluginLifecycleRouter:
    """Route app lifecycle events to feature-local events.py handlers."""

    def __init__(self, registry, context):
        self._registry = registry
        self._context = context
        self._handlers = {}

    def register(self, event_bus):
        event_bus.subscribe("game_connected", self._on_game_connected)
        event_bus.subscribe("game_disconnected", self._on_game_disconnected)
        event_bus.subscribe("game_not_found", self._on_game_not_found)
        event_bus.subscribe("app_closing", self._on_app_closing)

    def _on_game_connected(self, **payload):
        self._route_all("game_connected", payload)

    def _on_game_disconnected(self, **payload):
        self._route_all("game_disconnected", payload)

    def _on_game_not_found(self, **payload):
        self._route_all("game_not_found", payload)

    def _on_app_closing(self, **payload):
        self._route_all("app_closing", payload)

    def _route_all(self, event_name, payload):
        for feature in self._registry.all():
            feature_id = feature.manifest.get("feature_id", "")
            handler = self._load_handler(feature_id)
            if not handler:
                continue
            try:
                handler(self._context.for_feature(feature_id), event_name, payload or {})
            except Exception as exc:
                self._context.emit(
                    "log_message",
                    level="error",
                    module="PluginLifecycleRouter",
                    message=f"插件生命周期处理失败: {feature_id}.{event_name}",
                    audience="dev",
                    dev_detail=str(exc),
                )

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
            spec = importlib.util.spec_from_file_location(f"_plugin_lifecycle_{feature_id}", events_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            handler = getattr(module, "handle_lifecycle", None)
            self._handlers[feature_id] = handler if callable(handler) else None
        except Exception as exc:
            self._handlers[feature_id] = None
            self._context.emit(
                "log_message",
                level="error",
                module="PluginLifecycleRouter",
                message=f"插件生命周期模块加载失败: {feature_id}",
                audience="dev",
                dev_detail=str(exc),
            )
        return self._handlers[feature_id]
