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

    def build(self, *, weapon_scroll, player_scroll, other_scroll):
        handles = {}
        handles.update(self._page.build_tab(weapon_scroll, "weapon_tab"))
        handles.update(self._page.build_tab(player_scroll, "player_tab"))
        handles.update(self._page.build_tab(other_scroll, "other_tab"))
        return handles
