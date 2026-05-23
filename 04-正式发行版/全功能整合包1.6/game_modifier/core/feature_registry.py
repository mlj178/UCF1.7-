import threading
import json
import os


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

    def load_state(self, data_dir):
        path = os.path.join(data_dir, "feature_state.json")
        if not os.path.exists(path):
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                state = json.load(f)
            for fid, s in state.items():
                feature = self.get(fid)
                if feature:
                    if s.get('enabled', False):
                        feature._enabled = True
                    if 'slider_value' in s and feature.has_slider:
                        feature.slider_value = s['slider_value']
        except Exception:
            pass

    def save_state(self, data_dir):
        state = {}
        for feature in self.get_all():
            s = {'enabled': getattr(feature, '_enabled', False)}
            if feature.has_slider:
                s['slider_value'] = feature.slider_value
            state[feature.feature_id] = s
        path = os.path.join(data_dir, "feature_state.json")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except Exception:
            pass


def register_feature(cls):
    instance = cls()
    FeatureRegistry.get_instance().register(instance)
    return cls
