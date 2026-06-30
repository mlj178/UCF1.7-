from core.repositories import (
    DesiredStateRepository,
    FeatureStateRepository,
)
from core.state import AppState


class AppPersistenceService:
    DESIRED_FEATURE_IDS = {"esp_box"}

    def __init__(
        self,
        feature_state_repo=None,
        desired_state_repo=None,
    ):
        self._feature_state_repo = feature_state_repo or FeatureStateRepository()
        self._desired_state_repo = desired_state_repo or DesiredStateRepository()

    def load_app_state(self, feature_ids):
        state = AppState.with_default_features(feature_ids)
        state.apply_feature_state_payload(self._feature_state_repo.load())
        state.apply_desired_states(self.load_desired_states())
        return state

    def save_app_state(self, state):
        self._feature_state_repo.save(
            state.to_feature_state_payload(skip_feature_ids=self.DESIRED_FEATURE_IDS)
        )
        desired_states = self.load_desired_states()
        for feature_id in self.DESIRED_FEATURE_IDS:
            if feature_id in state.features:
                desired_states[feature_id] = bool(state.features[feature_id])
        self.save_desired_states(desired_states)

    def load_desired_states(self):
        desired_states = self._desired_state_repo.load()
        if desired_states:
            return desired_states

        legacy_state = self._feature_state_repo.load()
        esp_state = legacy_state.get("esp_box", {})
        if isinstance(esp_state, dict) and "enabled" in esp_state:
            desired_states["esp_box"] = bool(esp_state.get("enabled", False))
            self._desired_state_repo.save(desired_states)
        return desired_states

    def save_desired_states(self, desired_states):
        self._desired_state_repo.save(desired_states)

    def get_desired_state(self, feature_id):
        return self.load_desired_states().get(feature_id, False)

    def set_desired_state(self, feature_id, enabled):
        desired_states = self.load_desired_states()
        desired_states[feature_id] = bool(enabled)
        self.save_desired_states(desired_states)
