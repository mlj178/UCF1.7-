from dataclasses import dataclass, field


@dataclass
class AppState:
    features: dict = field(default_factory=dict)
    # Legacy migration fields only. New plugin feature configuration belongs in
    # data/user_config.json by feature_id, not in this dataclass.
    knife_speed: float = 5.0
    move_speed: float = 3.0
    range_mult: float = 50.0
    gravity: float = 1.0
    jump: float = 1.0
    gravity_mode: str = "player_only"
    timescale: float = 1.0
    battle_round_enabled: bool = False
    weapon_giver_respawn_enabled: bool = False
    nano4t_ghost: int = 0
    nano4t_human: int = 10

    @classmethod
    def with_default_features(cls, feature_ids):
        return cls(features={feature_id: False for feature_id in feature_ids})

    def apply_feature_state_payload(self, payload):
        for fid, config in payload.items():
            if fid == "battle_round_always":
                self.battle_round_enabled = bool(config.get("enabled", False))
                continue

            if fid not in self.features or not isinstance(config, dict):
                continue

            self.features[fid] = bool(config.get("enabled", False))

            if fid == "knife" and "slider_value" in config:
                self.knife_speed = config["slider_value"]
            elif fid == "movespeed" and "slider_value" in config:
                self.move_speed = config["slider_value"]
            elif fid == "range" and "slider_value" in config:
                self.range_mult = config["slider_value"]
            elif fid == "timescale" and "slider_value" in config:
                self.timescale = config["slider_value"]
            elif fid == "gravity":
                if "gravity_value" in config:
                    self.gravity = config["gravity_value"]
                if "jump_value" in config:
                    self.jump = config["jump_value"]
                if "gravity_mode" in config:
                    self.gravity_mode = config["gravity_mode"]
            elif fid == "weapon_giver" and "respawn_weapon" in config:
                self.weapon_giver_respawn_enabled = bool(config["respawn_weapon"])

    def apply_desired_states(self, desired_states):
        for fid, enabled in desired_states.items():
            if fid in self.features:
                self.features[fid] = bool(enabled)

    def apply_nano4t_payload(self, payload):
        self.nano4t_ghost = self._clamp_ghost(payload.get("ghost", 0))
        self.nano4t_human = self._clamp_human(payload.get("human", 10))

    def to_feature_state_payload(self, skip_feature_ids=None):
        skip_feature_ids = set(skip_feature_ids or ())
        payload = {}
        for fid, enabled in self.features.items():
            if fid in skip_feature_ids:
                continue

            item = {"enabled": enabled}
            if fid == "knife":
                item["slider_value"] = self.knife_speed
            elif fid == "movespeed":
                item["slider_value"] = self.move_speed
            elif fid == "range":
                item["slider_value"] = self.range_mult
            elif fid == "timescale":
                item["slider_value"] = self.timescale
            elif fid == "gravity":
                item["gravity_value"] = self.gravity
                item["jump_value"] = self.jump
                item["gravity_mode"] = self.gravity_mode
            elif fid == "weapon_giver":
                item["respawn_weapon"] = self.weapon_giver_respawn_enabled
            payload[fid] = item

        payload["battle_round_always"] = {"enabled": self.battle_round_enabled}
        return payload

    def to_nano4t_payload(self):
        return {
            "ghost": self._clamp_ghost(self.nano4t_ghost),
            "human": self._clamp_human(self.nano4t_human),
        }

    @staticmethod
    def _clamp_ghost(value):
        try:
            feature_id = int(value)
        except Exception:
            return 0
        return feature_id if 0 <= feature_id < 10 else 0

    @staticmethod
    def _clamp_human(value):
        try:
            feature_id = int(value)
        except Exception:
            return 10
        return feature_id if 10 <= feature_id < 20 else 10
