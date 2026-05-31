import json
import os
import winsound

from core.config import SETTINGS_FILE, RESOURCE_DIR
from core.event_bus import EventBus


class SoundManager:
    _instance = None

    def __init__(self):
        self._sound_enabled = self._load_sound_enabled()
        self._sound_volume = self._load_sound_volume()
        self._audio_initialized = False
        self._sound_channel = None
        self._init_pygame_mixer()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_sound_enabled(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('sound_enabled', True)
            except Exception:
                pass
        return True

    def _load_sound_volume(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    vol = data.get('sound_volume', 0.5)
                    if isinstance(vol, int) and vol > 1:
                        vol = vol / 100.0
                    return vol
            except Exception:
                pass
        return 0.5

    def _save_sound_settings(self):
        try:
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                    'sound_enabled': self._sound_enabled,
                    'sound_volume': self._sound_volume
                }, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _init_pygame_mixer(self):
        try:
            import pygame
            pygame.mixer.init()
            self._audio_initialized = True
            self._sound_channel = pygame.mixer.Channel(0)
        except Exception:
            self._audio_initialized = False

    def play_toggle_sound(self):
        if not self._sound_enabled:
            return
        try:
            if self._audio_initialized:
                import pygame
                sound_path = os.path.join(RESOURCE_DIR, "音效1.MP3")
                if os.path.exists(sound_path):
                    sound = pygame.mixer.Sound(sound_path)
                    if self._sound_channel:
                        self._sound_channel.play(sound)
                    else:
                        pygame.mixer.Sound.play(sound)
                else:
                    winsound.Beep(800, 100)
            else:
                winsound.Beep(800, 100)
        except Exception:
            try:
                winsound.Beep(800, 100)
            except Exception:
                pass

    @property
    def sound_enabled(self):
        return self._sound_enabled

    @sound_enabled.setter
    def sound_enabled(self, value):
        self._sound_enabled = value
        self._save_sound_settings()

    @property
    def sound_volume(self):
        return self._sound_volume

    @sound_volume.setter
    def sound_volume(self, value):
        self._sound_volume = value
        self._save_sound_settings()
