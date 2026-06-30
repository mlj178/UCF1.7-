from dataclasses import dataclass, field


@dataclass
class AppState:
    features: dict = field(default_factory=dict)

    @classmethod
    def with_default_features(cls, feature_ids):
        return cls(features={feature_id: False for feature_id in feature_ids})

    def apply_feature_state_payload(self, payload):
        for fid, config in payload.items():
            if fid not in self.features or not isinstance(config, dict):
                continue

            self.features[fid] = bool(config.get("enabled", False))

    def apply_desired_states(self, desired_states):
        for fid, enabled in desired_states.items():
            if fid in self.features:
                self.features[fid] = bool(enabled)

    def to_feature_state_payload(self, skip_feature_ids=None):
        skip_feature_ids = set(skip_feature_ids or ())
        payload = {}
        for fid, enabled in self.features.items():
            if fid in skip_feature_ids:
                continue
            payload[fid] = {"enabled": enabled}
        return payload
