from dataclasses import dataclass


@dataclass
class Nano4tSelectionResult:
    ok: bool
    feature_id: int | None = None
    description: str = ""
    error: str = ""


class Nano4tSelectionController:
    def __init__(self, store, attrs):
        self._store = store
        self._attrs = attrs
        cfg = self._load_payload()
        self.temp_ghost = cfg.get("ghost", 0)
        self.temp_human = cfg.get("human", 10)

    def load(self):
        cfg = self._load_payload()
        self.temp_ghost = cfg.get("ghost", 0)
        self.temp_human = cfg.get("human", 10)
        return {"ghost": self.temp_ghost, "human": self.temp_human}

    def save(self):
        self._save_payload({"ghost": self.temp_ghost, "human": self.temp_human})

    def select_ghost(self, value):
        feature_id = self._parse_id(value)
        if feature_id is None or feature_id < 0 or feature_id >= 10:
            return Nano4tSelectionResult(False, error=f"幽灵方特性ID无效: {feature_id}")
        self.temp_ghost = feature_id
        self.save()
        return Nano4tSelectionResult(
            True,
            feature_id=feature_id,
            description="效果: " + self._attrs[feature_id][1],
        )

    def select_human(self, value):
        feature_id = self._parse_id(value)
        if feature_id is None or feature_id < 10 or feature_id >= 20:
            return Nano4tSelectionResult(False, error=f"人类方特性ID无效: {feature_id}")
        self.temp_human = feature_id
        self.save()
        return Nano4tSelectionResult(
            True,
            feature_id=feature_id,
            description="效果: " + self._attrs[feature_id][1],
        )

    @staticmethod
    def _parse_id(value):
        try:
            return int(str(value).split(":", 1)[0])
        except Exception:
            return None

    def _load_payload(self):
        if hasattr(self._store, "load_nano4t_selection"):
            return self._store.load_nano4t_selection()
        return self._store.load()

    def _save_payload(self, payload):
        if hasattr(self._store, "save_nano4t_selection"):
            self._store.save_nano4t_selection(payload)
            return
        self._store.save(payload)
