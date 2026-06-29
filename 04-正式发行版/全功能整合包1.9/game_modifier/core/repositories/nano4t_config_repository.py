import json
from pathlib import Path

from core.config import NANO4T_FILE


class Nano4tConfigRepository:
    def __init__(self, path=None):
        self._path = Path(path or NANO4T_FILE)

    def load(self):
        if not self._path.exists():
            return self._default_payload()

        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
        except Exception:
            return self._default_payload()

        ghost = data.get("ghost", 0)
        human = data.get("human", 10)

        if ghost < 0 or ghost >= 10:
            ghost = 0
        if human < 10 or human >= 20:
            human = 10

        return {"ghost": ghost, "human": human}

    def save(self, payload):
        normalized = {
            "ghost": payload.get("ghost", 0),
            "human": payload.get("human", 10),
        }
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps(normalized, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def _default_payload():
        return {"ghost": 0, "human": 10}
