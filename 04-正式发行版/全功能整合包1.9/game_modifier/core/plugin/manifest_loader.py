import json
from pathlib import Path

from core.config import APP_DIR
from core.log_manager import get_logger


class ManifestLoader:
    """Load feature plugin manifests from features/*/manifest.json."""

    def __init__(self, features_dir=None, logger=None):
        self.features_dir = Path(features_dir or Path(APP_DIR) / "features")
        self._logger = logger or get_logger("PluginManifest")

    def _warning(self, message):
        if callable(self._logger):
            self._logger(message)
            return
        self._logger.warning(message)

    def load(self):
        manifests = []
        if not self.features_dir.exists():
            self._warning(f"features directory not found: {self.features_dir}")
            return manifests

        for manifest_path in sorted(self.features_dir.glob("*/manifest.json")):
            if manifest_path.parent.name == "_template":
                continue
            try:
                with manifest_path.open("r", encoding="utf-8") as handle:
                    manifest = json.load(handle)
                manifest.setdefault("_plugin_dir", str(manifest_path.parent))
                manifests.append(manifest)
            except Exception as exc:
                self._warning(f"failed to read manifest {manifest_path}: {exc}")
        return manifests

