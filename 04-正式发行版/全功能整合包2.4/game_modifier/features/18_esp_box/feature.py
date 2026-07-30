from core.plugin.plugin_base import PluginFeatureBase
from core.game_session_manager import GameSessionManager


class ESPBoxFeature(PluginFeatureBase):
    feature_id = 'esp_box'
    name = '方框透视'
    icon = '📦'
    category = 'other'
    desc = '通过 Universal DLL 显示方框透视'

    def __init__(self):
        super().__init__()
        self._session_manager = GameSessionManager.get_instance()

    def enable(self):
        """
        Enable ESP box.
        Only updates desired state and submits to session manager.
        Does NOT directly handle injection or connection.
        """
        # Update desired state
        self._session_manager.set_desired_state(self.feature_id, True)
        self._enabled = True
        return True

    def disable(self):
        """
        Disable ESP box.
        Only updates desired state and submits to session manager.
        """
        # Update desired state
        self._session_manager.set_desired_state(self.feature_id, False)
        self._enabled = False
        return True

    def cleanup(self, reason=None):
        """
        Cleanup on shutdown.
        Does NOT clear desired state to preserve user's preference across restarts.
        """
        # Do NOT update desired state - preserve for program restart
        self._enabled = False
