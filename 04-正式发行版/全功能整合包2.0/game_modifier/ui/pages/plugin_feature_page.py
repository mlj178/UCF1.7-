from pathlib import Path

import customtkinter as ctk

from core.plugin.module_loader import load_plugin_module
from ui.components.feature_card import FeatureCardBuilder


class PluginFeaturePage:
    def __init__(self, registry, callbacks):
        self.registry = registry
        self.callbacks = callbacks
        self.card_builder = FeatureCardBuilder(callbacks)
        self._panel_builders = {}

    def build_tab(self, scroll, tab_id):
        for i in range(2):
            scroll.grid_columnconfigure(i, weight=1, uniform=f"{tab_id}_col")

        handles = {}
        row = 0
        col = 0
        features = sorted(
            self.registry.by_tab(tab_id),
            key=lambda feature: int(feature.manifest.get("order", 0)),
        )
        for feature in features:
            manifest = feature.manifest
            layout = manifest.get("layout", {})
            colspan = int(layout.get("columnspan", 1))
            if colspan >= 2 and col == 1:
                row += 1
                col = 0

            new_handles = self._build_card(scroll, manifest, row, col, colspan)
            handles.update(new_handles)

            if colspan >= 2 or col == 1:
                row += 1
                col = 0
            else:
                col = 1
        return handles

    def _build_card(self, scroll, manifest, row, col, colspan):
        panel_builder = self._load_panel_builder(manifest)
        if panel_builder:
            return panel_builder(
                scroll,
                manifest,
                row,
                col,
                colspan,
                self.callbacks,
                self.card_builder,
            )
        return self._build_default_card(scroll, manifest, row, col, colspan)

    def _load_panel_builder(self, manifest):
        feature_id = manifest["feature_id"]
        if feature_id in self._panel_builders:
            return self._panel_builders[feature_id]

        plugin_dir = Path(manifest.get("_plugin_dir", "")) if manifest.get("_plugin_dir") else None
        if plugin_dir is None:
            plugin_dir = Path("features") / feature_id
        panel_path = plugin_dir / "panel.py"
        builder = None
        if panel_path.exists():
            module = load_plugin_module(plugin_dir, "panel")
            builder = getattr(module, "build_card", None)
        self._panel_builders[feature_id] = builder
        return builder

    def _build_default_card(self, scroll, manifest, row, col, colspan):
        feature_id = manifest["feature_id"]
        slider_control = self._first_control(manifest, "slider")
        button_control = self._first_control(manifest, "button")
        slider_var = None
        callback = None
        slider_range = None
        if slider_control:
            slider_var = ctk.DoubleVar(value=float(slider_control.get("default", 1.0)))
            slider_range = (float(slider_control["min"]), float(slider_control["max"]))
            key = slider_control.get("key", "value")
            callback = lambda value, fid=feature_id, cfg_key=key: self.callbacks["set_config"](
                fid,
                cfg_key,
                value,
            )

        frame, switch, label = self.card_builder.make_feature_card(
            scroll,
            row,
            col,
            colspan,
            manifest,
            slider_callback=callback,
            slider_var=slider_var,
            slider_range=slider_range,
            title_color=manifest.get("layout", {}).get("title_color"),
        )

        ui_handles = manifest.get("ui_handles", {})
        handles = {ui_handles.get("switch", f"{feature_id}_switch"): switch}
        if slider_var is not None:
            handles[ui_handles.get("slider_var", f"{feature_id}_var")] = slider_var
        if label is not None:
            handles[ui_handles.get("slider_label", f"{feature_id}_label")] = label
        if button_control:
            action = button_control.get("action", "enable")
            button = ctk.CTkButton(
                frame,
                text=button_control.get("label", manifest.get("display_name", "")),
                font=("Microsoft YaHei", 14, "bold"),
                height=40,
                command=lambda fid=feature_id, act=action: self.callbacks["action"](fid, act),
                fg_color="#b45309",
                hover_color="#92400e",
            )
            button.pack(fill="x", padx=12, pady=(0, 8))
            handles[ui_handles.get("button", f"{feature_id}_btn")] = button
        return handles

    @staticmethod
    def _first_control(manifest, control_type):
        for control in manifest.get("controls", []):
            if control.get("type") == control_type:
                return control
        return None
