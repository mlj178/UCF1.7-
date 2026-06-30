from ui.pages.plugin_feature_page import PluginFeaturePage


class FeatureTabsView:
    def __init__(
        self,
        *,
        plugin_registry,
        on_toggle_feature,
        on_set_config,
        on_action,
        logger=None,
        is_connected=None,
        is_enabled=None,
    ):
        callbacks = {
            "toggle": on_toggle_feature,
            "set_config": on_set_config,
            "action": on_action,
            "log": logger or (lambda _message: None),
            "is_connected": is_connected or (lambda: False),
            "is_enabled": is_enabled or (lambda _feature_id: False),
        }
        self._page = PluginFeaturePage(plugin_registry, callbacks)

    def build(self, tab_scrolls=None, **legacy_scrolls):
        tab_scrolls = tab_scrolls or legacy_scrolls
        handles = {}
        for tab_id, scroll in tab_scrolls.items():
            handles.update(self._page.build_tab(scroll, tab_id))
        return handles
