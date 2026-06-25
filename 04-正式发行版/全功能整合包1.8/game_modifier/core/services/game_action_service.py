class GameActionService:
    def __init__(self, frida):
        self._frida = frida

    def gather(self):
        return self._frida.call_export("gather")

    def skip_round(self):
        return self._frida.call_export("roundskip")

    def get_round_status(self):
        return self._frida.call_export("getRoundStatus")

    def health_check(self):
        return self._frida.call_export("getGravityStatus")

    def set_battle_round_enabled(self, enabled):
        self._frida.send_toggle("battle_round_always", bool(enabled))

    def nano4t_init(self):
        return self._frida.call_export("nano4tinit")

    def nano4t_set(self, ghost_id, human_id):
        return self._frida.call_export("nano4tset", ghost_id, human_id)

    def nano4t_get_current(self):
        return self._frida.call_export("nano4tgetcurrent")

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
