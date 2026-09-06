import json
from pathlib import Path

from core.config import DATA_DIR


class FeatureStateRepository:
    def __init__(self, path=None):
        self._path = Path(path or Path(DATA_DIR) / "feature_state.json")

    def load(self):
        if not self._path.exists():
            return {}

        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
        except Exception:
            return {}

        return data if isinstance(data, dict) else {}

    def save(self, payload):
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
