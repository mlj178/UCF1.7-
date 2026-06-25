class FeatureCommandService:
    def __init__(self, frida_manager):
        self._frida = frida_manager

    def toggle_feature(
        self,
        feature_id,
        enabled,
        *,
        slider_value=None,
        knife_speed=None,
        move_speed=None,
        range_mult=None,
        gravity_config=None,
        timescale=None,
    ):
        if knife_speed is None and feature_id == "knife":
            knife_speed = slider_value
        if timescale is None and feature_id == "timescale":
            timescale = slider_value

        if feature_id == "knife":
            self._frida.send_toggle("knife", enabled)
            if enabled and knife_speed is not None:
                self.set_knife_speed(knife_speed)
            return

        if feature_id == "movespeed":
            self._frida.send_toggle("movespeed", enabled)
            if enabled and move_speed is not None:
                self.set_move_speed(move_speed)
            return

        if feature_id == "range":
            self._frida.send_toggle("range", enabled)
            if enabled and range_mult is not None:
                self.set_range(range_mult)
            return

        if feature_id == "gravity":
            self._frida.send_toggle("gravity", enabled)
            if enabled and gravity_config is not None:
                self.send_gravity_config(**gravity_config)
            return

        if feature_id == "timescale":
            params = {"speed": timescale} if enabled and timescale is not None else None
            self._frida.send_toggle("timescale", enabled, extra_params=params)
            return

        self._frida.send_toggle(feature_id, enabled)

    def set_knife_speed(self, value):
        self._frida.send_toggle("knife_speed", value)

    def set_move_speed(self, value):
        self._frida.send_toggle("movespeed_speed", value)

    def set_range(self, value):
        self._frida.send_toggle("range_config", value)

    def set_timescale_speed(self, value):
        self._frida.send_toggle("timescale_speed", value)

    def send_gravity_config(self, g, j, m):
        self._frida.send_toggle("gravity_config", {"g": g, "j": j, "m": m})

    def restore_feature(self, feature_id, *, knife_speed=None, move_speed=None, range_mult=None,
                        gravity_config=None, timescale=None):
        self.toggle_feature(
            feature_id,
            True,
            knife_speed=knife_speed,
            move_speed=move_speed,
            range_mult=range_mult,
            gravity_config=gravity_config,
            timescale=timescale,
        )
