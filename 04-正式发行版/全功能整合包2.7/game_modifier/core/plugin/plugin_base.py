import os
import sys


class PluginFeatureBase:
    """Base class for future feature plugins."""

    feature_id = ""
    js_filename = "script.js"
    name = ""
    icon = ""
    category = "other"
    has_slider = False
    slider_range = (0.0, 1.0, 0.1)
    slider_value = 0.0
    has_combo = False
    combo_options = {}
    desc = ""

    def __init__(self, manifest=None, rpc_client=None, config_manager=None):
        self.manifest = manifest or {}
        if self.manifest.get("feature_id"):
            self.feature_id = self.manifest.get("feature_id", self.feature_id)
        self.rpc_client = rpc_client
        self.config_manager = config_manager
        self._enabled = False
        self._config = dict(self.manifest.get("config") or {})

    def enable(self):
        self._enabled = True
        if self.rpc_client:
            return self.rpc_client.call(self.feature_id, "enable")
        return {"ok": True, "enabled": True}

    def disable(self):
        self._enabled = False
        if self.rpc_client:
            return self.rpc_client.call(self.feature_id, "disable")
        return {"ok": True, "enabled": False}

    def set_config(self, config):
        self._config.update(config or {})
        if self.config_manager:
            self.config_manager.set(self.feature_id, self._config)
        if self.rpc_client:
            return self.rpc_client.call(self.feature_id, "setConfig", self._config)
        return {"ok": True, "config": dict(self._config)}

    def status(self):
        if self.rpc_client:
            return self.rpc_client.call(self.feature_id, "status")
        return {"enabled": self._enabled, "config": dict(self._config)}

    def cleanup(self, reason):
        self._enabled = False
        if self.rpc_client:
            return self.rpc_client.call(self.feature_id, "cleanup", {"reason": reason})
        return {"ok": True, "reason": reason}

    def on_ui_toggle(self, enabled):
        if enabled:
            self._enabled = True
            return self.enable()
        self._enabled = False
        return self.disable()

    def on_slider_change(self, value):
        self.slider_value = value

    def on_combo_change(self, selected):
        pass

    def get_js_code(self):
        module = sys.modules.get(self.__class__.__module__)
        module_file = getattr(module, "__file__", "")
        if module_file:
            js_path = os.path.join(os.path.dirname(os.path.abspath(module_file)), "script.js")
            if os.path.exists(js_path):
                with open(js_path, "r", encoding="utf-8") as handle:
                    return handle.read()
        return ""

    def get_metadata(self):
        meta = {
            "feature_id": self.feature_id,
            "name": self.name,
            "icon": self.icon,
            "category": self.category,
            "has_slider": self.has_slider,
            "has_combo": self.has_combo,
            "desc": self.desc,
        }
        if self.has_slider:
            meta["slider_range"] = self.slider_range
            meta["slider_value"] = self.slider_value
        if self.has_combo:
            meta["combo_options"] = self.combo_options
        return meta

    def get_custom_ui(self, parent):
        return None

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value
