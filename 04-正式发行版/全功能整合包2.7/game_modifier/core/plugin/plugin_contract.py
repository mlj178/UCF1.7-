from core.log_manager import get_logger


class PluginContract:
    """Validate manifest shape without blocking application startup."""

    REQUIRED_FIELDS = (
        "feature_id",
        "canonical_id",
        "display_name",
        "category",
        "tab",
        "order",
        "desc",
        "script",
        "layout",
        "controls",
        "config",
        "rpc",
        "lifecycle",
    )

    def __init__(self, logger=None):
        self._logger = logger or get_logger("PluginContract")

    def _warning(self, message):
        if callable(self._logger):
            self._logger(message)
            return
        self._logger.warning(message)

    def validate(self, manifest):
        missing = [field for field in self.REQUIRED_FIELDS if field not in manifest]
        if missing:
            feature_id = manifest.get("feature_id", "<unknown>")
            self._warning(
                f"plugin manifest {feature_id} missing required fields: {', '.join(missing)}"
            )
            return False
        return True
