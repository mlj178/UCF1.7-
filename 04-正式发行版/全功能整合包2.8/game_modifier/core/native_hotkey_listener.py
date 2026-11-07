import ctypes
import os
import threading
from ctypes import wintypes


WM_HOTKEY = 0x0312
WM_QUIT = 0x0012
PM_NOREMOVE = 0x0000
MOD_NOREPEAT = 0x4000

VK_BY_POSITION = {
    "f1": 0x70,
    "f2": 0x71,
}


class _Win32HotkeyApi:
    def __init__(self):
        if os.name != "nt":
            raise OSError("Windows native hotkeys require Windows")
        self._user32 = ctypes.WinDLL("user32", use_last_error=True)
        self._kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

        self._user32.RegisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int, wintypes.UINT, wintypes.UINT]
        self._user32.RegisterHotKey.restype = wintypes.BOOL
        self._user32.UnregisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int]
        self._user32.UnregisterHotKey.restype = wintypes.BOOL
        self._user32.GetMessageW.argtypes = [ctypes.POINTER(wintypes.MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT]
        self._user32.GetMessageW.restype = wintypes.BOOL
        self._user32.PeekMessageW.argtypes = [ctypes.POINTER(wintypes.MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT, wintypes.UINT]
        self._user32.PeekMessageW.restype = wintypes.BOOL
        self._user32.PostThreadMessageW.argtypes = [wintypes.DWORD, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
        self._user32.PostThreadMessageW.restype = wintypes.BOOL
        self._kernel32.GetCurrentThreadId.restype = wintypes.DWORD

    def current_thread_id(self):
        return int(self._kernel32.GetCurrentThreadId())

    def ensure_message_queue(self):
        message = wintypes.MSG()
        self._user32.PeekMessageW(ctypes.byref(message), None, 0, 0, PM_NOREMOVE)

    def register_hotkey(self, hotkey_id, modifiers, virtual_key):
        ctypes.set_last_error(0)
        return bool(self._user32.RegisterHotKey(None, hotkey_id, modifiers, virtual_key))

    def unregister_hotkey(self, hotkey_id):
        return bool(self._user32.UnregisterHotKey(None, hotkey_id))

    def next_message(self):
        message = wintypes.MSG()
        result = self._user32.GetMessageW(ctypes.byref(message), None, 0, 0)
        if result <= 0:
            return None
        return int(message.message), int(message.wParam)

    def post_quit(self, thread_id):
        return bool(self._user32.PostThreadMessageW(thread_id, WM_QUIT, 0, 0))

    @staticmethod
    def last_error():
        return ctypes.get_last_error()


class NativeHotkeyListener:
    def __init__(self, api=None):
        self._api = api
        self._thread = None
        self._thread_id = None
        self._ready = None
        self._callback = None
        self._requested = ()
        self._registration = {}
        self._errors = {}

    @property
    def errors(self):
        return dict(self._errors)

    def start(self, positions, callback, timeout=2.0):
        self.stop()
        self._callback = callback
        self._requested = tuple(position for position in positions if position in VK_BY_POSITION)
        self._registration = {position: False for position in self._requested}
        self._errors = {}
        self._ready = threading.Event()

        if not self._requested:
            return {}
        if self._api is None:
            try:
                self._api = _Win32HotkeyApi()
            except OSError:
                self._errors = {position: "unsupported_platform" for position in self._requested}
                return dict(self._registration)

        self._thread = threading.Thread(target=self._run, name="native-hotkeys", daemon=True)
        self._thread.start()
        if not self._ready.wait(timeout):
            self._errors = {position: "registration_timeout" for position in self._requested}
            self.stop()
        return dict(self._registration)

    def stop(self, timeout=2.0):
        thread = self._thread
        if thread and thread.is_alive() and self._thread_id is not None:
            self._api.post_quit(self._thread_id)
            thread.join(timeout)
        self._thread = None
        self._thread_id = None

    def _run(self):
        registered_by_id = {}
        try:
            self._thread_id = self._api.current_thread_id()
            self._api.ensure_message_queue()
            for hotkey_id, position in enumerate(self._requested, start=1):
                if self._api.register_hotkey(hotkey_id, MOD_NOREPEAT, VK_BY_POSITION[position]):
                    self._registration[position] = True
                    registered_by_id[hotkey_id] = position
                else:
                    self._errors[position] = self._api.last_error()
            self._ready.set()

            while registered_by_id:
                message = self._api.next_message()
                if message is None:
                    break
                message_id, hotkey_id = message
                position = registered_by_id.get(hotkey_id)
                if message_id == WM_HOTKEY and position:
                    try:
                        self._callback(position)
                    except Exception:
                        pass
        finally:
            for hotkey_id in registered_by_id:
                self._api.unregister_hotkey(hotkey_id)
            if self._ready is not None:
                self._ready.set()
