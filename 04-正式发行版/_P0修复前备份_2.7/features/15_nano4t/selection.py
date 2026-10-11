from dataclasses import dataclass


@dataclass
class Nano4tSelectionResult:
    ok: bool
    feature_id: int | None = None
    description: str = ""
    error: str = ""


class Nano4tSelectionController:
    def __init__(self, attrs, state, on_save):
        self._attrs = attrs
        self._state = state
        self._on_save = on_save

    def select_ghost(self, value):
        feature_id = self._parse_id(value)
        if feature_id is None or feature_id < 0 or feature_id >= 10:
            return Nano4tSelectionResult(False, error=f"幽灵方特性ID无效: {feature_id}")
        self._state.temp_ghost = feature_id
        self._on_save()
        return Nano4tSelectionResult(
            True,
            feature_id=feature_id,
            description="效果: " + self._attrs[feature_id][1],
        )

    def select_human(self, value):
        feature_id = self._parse_id(value)
        if feature_id is None or feature_id < 10 or feature_id >= 20:
            return Nano4tSelectionResult(False, error=f"人类方特性ID无效: {feature_id}")
        self._state.temp_human = feature_id
        self._on_save()
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
