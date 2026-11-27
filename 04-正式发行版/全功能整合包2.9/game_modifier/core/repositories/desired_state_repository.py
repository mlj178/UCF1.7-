import json
from pathlib import Path

from core.config import DATA_DIR, write_json_atomic
from core.log_manager import get_logger


class DesiredStateRepository:
    def __init__(self, path=None):
        self._path = Path(path or Path(DATA_DIR) / "desired_states.json")

    def load(self):
        if not self._path.exists():
            return {}

        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
        except Exception as exc:
            get_logger("DesiredStateRepository").warning(
                "期望状态文件损坏，已按空配置处理 %s: %s", self._path, exc
            )
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
        write_json_atomic(self._path, normalized)
