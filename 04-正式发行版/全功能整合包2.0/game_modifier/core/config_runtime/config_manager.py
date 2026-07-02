import json
from pathlib import Path

from core.config import DATA_DIR
from core.log_manager import get_logger


class ConfigManager:
    """Manage default_config.json and user_config.json by feature_id."""

    def __init__(self, data_dir=None, logger=None):
        self.data_dir = Path(data_dir or DATA_DIR)
        self.default_path = self.data_dir / "default_config.json"
        self.user_path = self.data_dir / "user_config.json"
        self._logger = logger or get_logger("ConfigRuntime")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._default = self._read_json(self.default_path)
        self._user = self._read_json(self.user_path)

    def _warning(self, message):
        if callable(self._logger):
            self._logger(message)
            return
        self._logger.warning(message)

    def _read_json(self, path):
        if not path.exists():
            return {}
        try:
            with path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            return data if isinstance(data, dict) else {}
        except Exception as exc:
            self._warning(f"failed to read config {path}: {exc}")
            return {}

    def _write_user(self):
        with self.user_path.open("w", encoding="utf-8") as handle:
            json.dump(self._user, handle, ensure_ascii=False, indent=2)

    def get(self, feature_id, default=None):
        merged = {}
        if isinstance(self._default.get(feature_id), dict):
            merged.update(self._default[feature_id])
        if isinstance(self._user.get(feature_id), dict):
            merged.update(self._user[feature_id])
        if not merged and default is not None:
            return default
        return merged

    def set(self, feature_id, config):
        current = self.get(feature_id)
        current.update(config or {})
        self._user[feature_id] = current
        self._write_user()
        return current

    def has_user_config(self, feature_id):
        return feature_id in self._user

    def all(self):
        feature_ids = set(self._default.keys()) | set(self._user.keys())
        return {feature_id: self.get(feature_id) for feature_id in sorted(feature_ids)}
