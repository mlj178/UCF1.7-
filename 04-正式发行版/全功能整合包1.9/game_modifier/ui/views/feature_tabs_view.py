from ui.pages.plugin_feature_page import PluginFeaturePage


class FeatureTabsView:
    def __init__(
        self,
        *,
        plugin_registry,
        on_toggle_feature,
        on_set_config,
        on_action,
    ):
        callbacks = {
            "toggle": on_toggle_feature,
            "set_config": on_set_config,
            "action": on_action,
        }
        self._page = PluginFeaturePage(plugin_registry, callbacks)

    def build(self, *, weapon_scroll, player_scroll, other_scroll):
        handles = {}
        handles.update(self._page.build_tab(weapon_scroll, "weapon_tab"))
        handles.update(self._page.build_tab(player_scroll, "player_tab"))
        handles.update(self._page.build_tab(other_scroll, "other_tab"))
        return handles
