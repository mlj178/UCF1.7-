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
            return False
        handler(self._context, event, payload or {})
        return True

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
        spec = importlib.util.spec_from_file_location(f"_plugin_events_{feature_id}", events_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        handler = getattr(module, "handle_event", None)
        self._handlers[feature_id] = handler if callable(handler) else None
        return self._handlers[feature_id]
