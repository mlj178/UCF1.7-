import os

from core.config import SCRIPTS_DIR
from core.event_bus import EventBus


class FeatureBase:
    feature_id = ''
    js_filename = None
    name = ''
    icon = ''
    category = 'other'
    has_slider = False
    slider_range = (0.0, 1.0, 0.1)
    slider_value = 0.0
    has_combo = False
    combo_options = {}
    desc = ''

    def __init__(self):
        self._enabled = False
        self._event_bus = EventBus.get_instance()

    def enable(self):
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected:
            fm.send_toggle(self.feature_id, True)

    def disable(self):
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected:
            fm.send_toggle(self.feature_id, False)

    def on_ui_toggle(self, enabled):
        if enabled:
            self._enabled = True
            self.enable()
        else:
            self._enabled = False
            self.disable()

    def on_slider_change(self, value):
        self.slider_value = value

    def on_combo_change(self, selected):
        pass

    def get_js_code(self):
        fname = self.js_filename if self.js_filename else f"{self.feature_id}.js"
        js_path = os.path.join(SCRIPTS_DIR, fname)
        if os.path.exists(js_path):
            with open(js_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ''

    def get_metadata(self):
        meta = {
            'feature_id': self.feature_id,
            'name': self.name,
            'icon': self.icon,
            'category': self.category,
            'has_slider': self.has_slider,
            'has_combo': self.has_combo,
            'desc': self.desc,
        }
        if self.has_slider:
            meta['slider_range'] = self.slider_range
            meta['slider_value'] = self.slider_value
        if self.has_combo:
            meta['combo_options'] = self.combo_options
        return meta

    def get_custom_ui(self, parent):
        return None

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value
