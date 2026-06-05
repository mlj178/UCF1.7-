import ctypes
import ctypes.wintypes
import json
import os
import subprocess
import threading
import time

import psutil

from core.config import APP_DIR
from core.event_bus import EventBus


# Windows API type declarations
kernel32 = ctypes.windll.kernel32

kernel32.CreateFileW.restype = ctypes.wintypes.HANDLE
kernel32.CreateFileW.argtypes = [
    ctypes.wintypes.LPCWSTR,  # lpFileName
    ctypes.wintypes.DWORD,    # dwDesiredAccess
    ctypes.wintypes.DWORD,    # dwShareMode
    ctypes.wintypes.LPVOID,   # lpSecurityAttributes
    ctypes.wintypes.DWORD,    # dwCreationDisposition
    ctypes.wintypes.DWORD,    # dwFlagsAndAttributes
    ctypes.wintypes.HANDLE,   # hTemplateFile
]

kernel32.CloseHandle.restype = ctypes.wintypes.BOOL
kernel32.CloseHandle.argtypes = [ctypes.wintypes.HANDLE]

kernel32.WriteFile.restype = ctypes.wintypes.BOOL
kernel32.WriteFile.argtypes = [
    ctypes.wintypes.HANDLE,        # hFile
    ctypes.wintypes.LPCVOID,       # lpBuffer
    ctypes.wintypes.DWORD,         # nNumberOfBytesToWrite
    ctypes.POINTER(ctypes.wintypes.DWORD),  # lpNumberOfBytesWritten
    ctypes.wintypes.LPVOID,        # lpOverlapped
]

kernel32.ReadFile.restype = ctypes.wintypes.BOOL
kernel32.ReadFile.argtypes = [
    ctypes.wintypes.HANDLE,        # hFile
    ctypes.wintypes.LPVOID,        # lpBuffer
    ctypes.wintypes.DWORD,         # nNumberOfBytesToRead
    ctypes.POINTER(ctypes.wintypes.DWORD),  # lpNumberOfBytesRead
    ctypes.wintypes.LPVOID,        # lpOverlapped
]

kernel32.SetNamedPipeHandleState.restype = ctypes.wintypes.BOOL
kernel32.SetNamedPipeHandleState.argtypes = [
    ctypes.wintypes.HANDLE,                    # hNamedPipe
    ctypes.POINTER(ctypes.wintypes.DWORD),     # lpMode
    ctypes.POINTER(ctypes.wintypes.DWORD),     # lpMaxCollectionCount
    ctypes.POINTER(ctypes.wintypes.DWORD),     # lpCollectDataTimeout
]

kernel32.CreateEventW.restype = ctypes.wintypes.HANDLE
kernel32.CreateEventW.argtypes = [
    ctypes.wintypes.LPVOID,   # lpEventAttributes
    ctypes.wintypes.BOOL,     # bManualReset
    ctypes.wintypes.BOOL,     # bInitialState
    ctypes.wintypes.LPCWSTR,  # lpName
]

kernel32.WaitForSingleObject.restype = ctypes.wintypes.DWORD
kernel32.WaitForSingleObject.argtypes = [
    ctypes.wintypes.HANDLE,  # hHandle
    ctypes.wintypes.DWORD,   # dwMilliseconds
]

kernel32.GetOverlappedResult.restype = ctypes.wintypes.BOOL
kernel32.GetOverlappedResult.argtypes = [
    ctypes.wintypes.HANDLE,                    # hFile
    ctypes.wintypes.LPVOID,                    # lpOverlapped
    ctypes.POINTER(ctypes.wintypes.DWORD),     # lpNumberOfBytesTransferred
    ctypes.wintypes.BOOL,                      # bWait
]

kernel32.CancelIo.restype = ctypes.wintypes.BOOL
kernel32.CancelIo.argtypes = [ctypes.wintypes.HANDLE]

INFINITE = 0xFFFFFFFF
WAIT_OBJECT_0 = 0
WAIT_TIMEOUT = 0x00000102


class UniversalHookManager:
    PIPE_NAME = r"\\.\pipe\ucf_universal_hook"
    PIPE_READMODE_MESSAGE = 0x02
    PIPE_TIMEOUT_MS = 3000  # 3 seconds timeout for pipe operations

    def __init__(self):
        self._bus = EventBus.get_instance()
        self._pipe = None
        self._injected = False
        self._lock = threading.Lock()
        self._dll_path = os.path.join(APP_DIR, "plugins", "universal_hook", "Universal-ImGui-Hook.dll")

    @property
    def injected(self):
        return self._injected

    def find_pid(self):
        for proc in psutil.process_iter(["pid", "name"]):
            name = proc.info.get("name") or ""
            if name.lower() == "unitycrossfire.exe":
                return proc.info["pid"]
        return None

    def ensure_ready(self):
        with self._lock:
            if self._pipe and self.ping():
                return True

            if not os.path.exists(self._dll_path):
                self._log("error", f"Universal DLL not found: {self._dll_path}")
                return False

            pid = self.find_pid()
            if not pid:
                self._log("error", "UnityCrossFire.exe not found")
                return False

            if not self._injected:
                if not self._inject(pid):
                    return False

            if not self._connect_pipe(timeout=5.0):
                self._log("error", "Universal pipe not ready")
                return False

            return True

    def set_esp_box(self, enabled):
        if not self.ensure_ready():
            return False
        result = self._send({"cmd": "set_feature", "feature": "esp_box", "enabled": bool(enabled)})
        ok = bool(result.get("ok"))
        if ok:
            self._log("success", "方框透视已开启" if enabled else "方框透视已关闭")
        else:
            self._log("error", result.get("error", "方框透视设置失败"))
        return ok

    def ping(self):
        try:
            return bool(self._send({"cmd": "ping"}).get("ok"))
        except Exception:
            return False

    def shutdown(self):
        try:
            if self._pipe:
                self._send({"cmd": "shutdown"})
        except Exception:
            pass
        self._close_pipe()
        self._injected = False

    def _inject(self, pid):
        inject_exe = os.path.join(APP_DIR, "plugins", "universal_hook", "inject.exe")
        if not os.path.exists(inject_exe):
            self._log("error", f"inject.exe not found: {inject_exe}")
            return False

        self._log("info", "正在加载 Universal Hook...")
        result = subprocess.run(
            [inject_exe, "UnityCrossFire", self._dll_path],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode != 0:
            self._log("error", result.stderr or result.stdout or "Universal Hook 注入失败")
            return False

        self._injected = True
        self._log("success", "Universal Hook 已加载")
        return True

    def _connect_pipe(self, timeout):
        deadline = time.time() + timeout
        while time.time() < deadline:
            handle = kernel32.CreateFileW(
                self.PIPE_NAME,
                0xC0000000,  # GENERIC_READ | GENERIC_WRITE
                0,
                None,
                3,  # OPEN_EXISTING
                0,
                None,
            )
            if handle and handle != ctypes.wintypes.HANDLE(-1).value:
                # Set pipe to message mode to match server
                mode = ctypes.wintypes.DWORD(self.PIPE_READMODE_MESSAGE)
                if kernel32.SetNamedPipeHandleState(handle, ctypes.byref(mode), None, None):
                    self._pipe = handle
                    return True
                # Failed to set mode, close and retry
                kernel32.CloseHandle(handle)
            time.sleep(0.1)
        return False

    def _send(self, payload, timeout_ms=None):
        if not self._pipe:
            raise RuntimeError("pipe not connected")

        if timeout_ms is None:
            timeout_ms = self.PIPE_TIMEOUT_MS

        data = json.dumps(payload, separators=(",", ":")).encode("utf-8")

        # Write with timeout
        write_event = kernel32.CreateEventW(None, True, False, None)
        if not write_event:
            raise RuntimeError("failed to create write event")

        try:
            write_overlapped = self._make_overlapped(write_event)
            written = ctypes.wintypes.DWORD(0)

            ok = kernel32.WriteFile(
                self._pipe, data, len(data), ctypes.byref(written), ctypes.byref(write_overlapped)
            )
            if not ok:
                err = ctypes.get_last_error()
                if err != 997:  # ERROR_IO_PENDING
                    self._close_pipe()
                    raise RuntimeError(f"pipe write failed: {err}")

                wait_result = kernel32.WaitForSingleObject(write_event, timeout_ms)
                if wait_result != WAIT_OBJECT_0:
                    kernel32.CancelIo(self._pipe)
                    self._close_pipe()
                    raise RuntimeError("pipe write timeout")

                if not kernel32.GetOverlappedResult(
                    self._pipe, ctypes.byref(write_overlapped), ctypes.byref(written), False
                ):
                    self._close_pipe()
                    raise RuntimeError("pipe write result failed")
        finally:
            kernel32.CloseHandle(write_event)

        # Read with timeout
        read_event = kernel32.CreateEventW(None, True, False, None)
        if not read_event:
            raise RuntimeError("failed to create read event")

        try:
            read_overlapped = self._make_overlapped(read_event)
            buffer = ctypes.create_string_buffer(4096)
            read_bytes = ctypes.wintypes.DWORD(0)

            ok = kernel32.ReadFile(
                self._pipe, buffer, 4096, ctypes.byref(read_bytes), ctypes.byref(read_overlapped)
            )
            if not ok:
                err = ctypes.get_last_error()
                if err != 997:  # ERROR_IO_PENDING
                    self._close_pipe()
                    raise RuntimeError(f"pipe read failed: {err}")

                wait_result = kernel32.WaitForSingleObject(read_event, timeout_ms)
                if wait_result != WAIT_OBJECT_0:
                    kernel32.CancelIo(self._pipe)
                    self._close_pipe()
                    raise RuntimeError("pipe read timeout")

                if not kernel32.GetOverlappedResult(
                    self._pipe, ctypes.byref(read_overlapped), ctypes.byref(read_bytes), False
                ):
                    self._close_pipe()
                    raise RuntimeError("pipe read result failed")

            return json.loads(buffer.raw[:read_bytes.value].decode("utf-8"))
        finally:
            kernel32.CloseHandle(read_event)

    def _make_overlapped(self, event):
        class OVERLAPPED(ctypes.Structure):
            _fields_ = [
                ("Internal", ctypes.wintypes.LPVOID),
                ("InternalHigh", ctypes.wintypes.LPVOID),
                ("Offset", ctypes.wintypes.DWORD),
                ("OffsetHigh", ctypes.wintypes.DWORD),
                ("hEvent", ctypes.wintypes.HANDLE),
            ]
        return OVERLAPPED(0, 0, 0, 0, event)

    def _close_pipe(self):
        if self._pipe:
            kernel32.CloseHandle(self._pipe)
            self._pipe = None

    def _log(self, level, message):
        self._bus.emit("log_message", level=level, module="Universal", message=message)
