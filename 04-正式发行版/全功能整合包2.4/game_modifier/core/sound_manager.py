import json
import os
import winsound

from core.config import SETTINGS_FILE, RESOURCE_DIR
from core.event_bus import EventBus

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")


class SoundManager:
    _instance = None

    def __init__(self):
        self._sound_enabled = self._load_sound_enabled()
        self._sound_volume = self._load_sound_volume()
        self._audio_initialized = False
        self._sound_channel = None
        self._toggle_sound = None
        self._toggle_sound_path = None
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

    def _resource_file(self, filenames):
        for filename in filenames:
            path = os.path.join(RESOURCE_DIR, filename)
            if os.path.exists(path):
                return path

        try:
            wanted = {name.lower() for name in filenames}
            for filename in os.listdir(RESOURCE_DIR):
                if filename.lower() in wanted:
                    return os.path.join(RESOURCE_DIR, filename)
        except Exception:
            pass
        return None

    def _load_toggle_sound(self):
        sound_path = self._resource_file(("音效1.MP3", "音效1.mp3", "音效1.wav", "音效1.ogg"))
        if not sound_path:
            return None
        if self._toggle_sound is not None and self._toggle_sound_path == sound_path:
            return self._toggle_sound
        try:
            import pygame
            sound = pygame.mixer.Sound(sound_path)
            sound.set_volume(max(0.0, min(1.0, float(self._sound_volume))))
            self._toggle_sound = sound
            self._toggle_sound_path = sound_path
            return sound
        except Exception:
            self._toggle_sound = None
            self._toggle_sound_path = sound_path
            return None

    def _play_with_pygame_music(self):
        sound_path = self._toggle_sound_path or self._resource_file(("音效1.MP3", "音效1.mp3", "音效1.wav", "音效1.ogg"))
        if not sound_path:
            return False
        try:
            import pygame
            pygame.mixer.music.set_volume(max(0.0, min(1.0, float(self._sound_volume))))
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
            return True
        except Exception:
            return False

    def _fallback_beep(self):
        try:
            winsound.MessageBeep(winsound.MB_OK)
        except Exception:
            try:
                winsound.Beep(800, 100)
            except Exception:
                pass

    def play_toggle_sound(self):
        if not self._sound_enabled:
            return
        try:
            if self._audio_initialized:
                sound = self._load_toggle_sound()
                if sound is not None:
                    if self._sound_channel:
                        self._sound_channel.play(sound)
                    else:
                        sound.play()
                    return
                if self._play_with_pygame_music():
                    return
                self._fallback_beep()
            else:
                self._fallback_beep()
        except Exception:
            self._fallback_beep()

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
        if self._toggle_sound is not None:
            try:
                self._toggle_sound.set_volume(max(0.0, min(1.0, float(value))))
            except Exception:
                pass
        self._save_sound_settings()
