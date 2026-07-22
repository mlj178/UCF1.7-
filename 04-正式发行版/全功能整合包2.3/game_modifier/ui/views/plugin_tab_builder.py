from pathlib import Path

import customtkinter as ctk

from core.plugin.module_loader import load_plugin_module
from ui.views.feature_tabs_view import FeatureTabsView
from ui.views.common import bind_view_handles


class PluginTabBuilder:
    """Build ordinary and special plugin tabs from manifests."""

    def __init__(
        self,
        *,
        host,
        plugin_registry,
        panel_context,
        callbacks,
        logger,
        is_connected,
        is_enabled,
    ):
        self._host = host
        self._registry = plugin_registry
        self._panel_context = panel_context
        self._callbacks = callbacks
        self._logger = logger
        self._is_connected = is_connected
        self._is_enabled = is_enabled
        self._special_tabs = {}
        self._built_special_tabs = set()

    def build(self):
        tab_view = ctk.CTkTabview(self._host, corner_radius=8, command=self.on_tab_changed)
        tab_view.pack(fill="both", padx=12, pady=4, expand=True)

        ordinary_scrolls = {}
        for tab in self._ordinary_tabs():
            ordinary_scrolls[tab["id"]] = self._add_scroll_tab(tab_view, tab["title"])

        feature_tabs_view = FeatureTabsView(
            plugin_registry=self._registry,
            on_toggle_feature=self._callbacks["toggle"],
            on_set_config=self._callbacks["set_config"],
            on_action=self._callbacks["action"],
            logger=self._logger,
            is_connected=self._is_connected,
            is_enabled=self._is_enabled,
        )
        bind_view_handles(
            self._host,
            feature_tabs_view.build(tab_scrolls=ordinary_scrolls),
        )

        for feature in self._special_page_features():
            title = feature.manifest.get("ui", {}).get("tab_title") or feature.manifest.get("display_name")
            scroll = self._add_scroll_tab(tab_view, title)
            self._special_tabs[title] = {"feature": feature, "scroll": scroll}
            if not feature.manifest.get("ui", {}).get("lazy_build", False):
                self._build_special_tab(title)

        return tab_view

    def on_tab_changed(self):
        if not self._special_tabs:
            return
        current = self._host.tab_view.get()
        self._build_special_tab(current)

    def prebuild_lazy_tabs(self):
        for title in list(self._special_tabs.keys()):
            self._build_special_tab(title)

    def _add_scroll_tab(self, tab_view, title):
        tab = tab_view.add(title)
        scroll = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=2, pady=2)
        return scroll

    def _special_page_features(self):
        features = [
            feature
            for feature in self._registry.all()
            if feature.manifest.get("ui", {}).get("mode") == "special_page"
        ]
        return sorted(features, key=lambda feature: feature.manifest.get("ui", {}).get("tab_order", feature.manifest.get("order", 0)))

    def _ordinary_tabs(self):
        tabs = {}
        for feature in self._registry.all():
            manifest = feature.manifest
            ui = manifest.get("ui", {})
            if ui.get("mode") in {"special_page", "embedded_panel"}:
                continue
            tab_id = manifest.get("tab")
            if not tab_id:
                continue
            item = tabs.setdefault(
                tab_id,
                {
                    "id": tab_id,
                    "title": manifest.get("tab_title") or ui.get("tab_title") or tab_id,
                    "order": manifest.get("tab_order", ui.get("tab_order", manifest.get("order", 0))),
                },
            )
            item["order"] = min(item["order"], manifest.get("tab_order", item["order"]))
        return sorted(tabs.values(), key=lambda item: (item["order"], item["title"], item["id"]))

    def _build_special_tab(self, title):
        if title in self._built_special_tabs or title not in self._special_tabs:
            return None
        item = self._special_tabs[title]
        feature = item["feature"]
        plugin_dir = Path(feature.manifest.get("_plugin_dir", ""))
        panel_path = plugin_dir / "panel.py"
        if not panel_path.exists():
            return None
        module = load_plugin_module(plugin_dir, "panel")
        build_panel = getattr(module, "build_panel", None)
        if not callable(build_panel):
            return None
        self._built_special_tabs.add(title)
        return build_panel(
            self._panel_context.for_feature(feature.manifest["feature_id"]),
            item["scroll"],
        )
