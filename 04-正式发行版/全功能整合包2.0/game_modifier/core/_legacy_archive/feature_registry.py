import threading


class FeatureRegistry:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self._features = {}
        self._lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def register(self, feature_instance):
        with self._lock:
            self._features[feature_instance.feature_id] = feature_instance

    def get_all(self):
        with self._lock:
            return list(self._features.values())

    def get(self, feature_id):
        with self._lock:
            return self._features.get(feature_id)

    def get_by_category(self, category):
        with self._lock:
            return [f for f in self._features.values() if f.category == category]


def register_feature(cls):
    instance = cls()
    FeatureRegistry.get_instance().register(instance)
    return cls
