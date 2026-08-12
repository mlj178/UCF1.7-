from core.log_manager import get_logger


class FeatureLifecycle:
    """Coordinate enable/disable/config/cleanup calls for plugin features."""

    def __init__(self, registry, logger=None):
        self.registry = registry
        self._logger = logger or get_logger("FeatureLifecycle")

    def enable(self, feature_id):
        feature = self.registry.get(feature_id)
        if not feature:
            self._logger.warning(f"unknown plugin feature: {feature_id}")
            return None
        return feature.enable()

    def disable(self, feature_id):
        feature = self.registry.get(feature_id)
        if not feature:
            self._logger.warning(f"unknown plugin feature: {feature_id}")
            return None
        return feature.disable()

    def set_config(self, feature_id, config):
        feature = self.registry.get(feature_id)
        if not feature:
            self._logger.warning(f"unknown plugin feature: {feature_id}")
            return None
        return feature.set_config(config)

    def cleanup_all(self, reason):
        for feature in self.registry.all():
            try:
                feature.cleanup(reason)
            except Exception as exc:
                self._logger.warning(f"feature cleanup failed for {feature.feature_id}: {exc}")

