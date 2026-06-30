class GameActionService:
    def __init__(self, frida):
        self._frida = frida

    def set_battle_round_enabled(self, enabled):
        action = "enable" if enabled else "disable"
        return self._frida.plugin_call("battle_round", action, {"enabled": bool(enabled)})

    def battle_round_get_status(self):
        return self._frida.plugin_call("battle_round", "battleRoundGetStatus", {})

    def nano4t_init(self):
        return self._frida.plugin_call("nano4t", "nano4tInit", {})

    def nano4t_set(self, ghost_id, human_id):
        return self._frida.plugin_call("nano4t", "nano4tSet", {"g": ghost_id, "h": human_id})

    def nano4t_get_current(self):
        return self._frida.plugin_call("nano4t", "nano4tGetCurrent", {})

    def nano4t_init_if_connected(self, ready):
        if not self._frida.is_connected or ready:
            return False
        self.nano4t_init()
        return True

    def nano4t_get_current_if_ready(self, ready):
        if not self._frida.is_connected or not ready:
            return False
        self.nano4t_get_current()
        return True
