import json
from pathlib import Path

from core.config import DATA_DIR


class DesiredStateRepository:
    def __init__(self, path=None):
        self._path = Path(path or Path(DATA_DIR) / "desired_states.json")

    def load(self):
        if not self._path.exists():
            return {}

        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
        except Exception:
            return {}

        if not isinstance(data, dict):
            return {}
        return {str(feature_id): bool(enabled) for feature_id, enabled in data.items()}

    def save(self, payload):
        normalized = {
            str(feature_id): bool(enabled)
            for feature_id, enabled in (payload or {}).items()
        }
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps(normalized, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
