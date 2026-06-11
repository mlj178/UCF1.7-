import ctypes
import ctypes.wintypes
import json
import os
import subprocess
import threading
import time

import psutil

from core.config import APP_DIR, PLUGINS_DIR
from core.event_bus import EventBus


# Windows API type declarations
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)


class OVERLAPPED(ctypes.Structure):
    _fields_ = [
        ("Internal", ctypes.c_void_p),
        ("InternalHigh", ctypes.c_void_p),
        ("Offset", ctypes.wintypes.DWORD),
        ("OffsetHigh", ctypes.wintypes.DWORD),
        ("hEvent", ctypes.wintypes.HANDLE),
    ]

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

kernel32.CreateEventW.restype = ctypes.wintypes.HANDLE
kernel32.CreateEventW.argtypes = [
    ctypes.wintypes.LPVOID,
    ctypes.wintypes.BOOL,
    ctypes.wintypes.BOOL,
    ctypes.wintypes.LPCWSTR,
]

kernel32.WaitForSingleObject.restype = ctypes.wintypes.DWORD
kernel32.WaitForSingleObject.argtypes = [
    ctypes.wintypes.HANDLE,
    ctypes.wintypes.DWORD,
]

kernel32.GetOverlappedResult.restype = ctypes.wintypes.BOOL
kernel32.GetOverlappedResult.argtypes = [
    ctypes.wintypes.HANDLE,
    ctypes.POINTER(OVERLAPPED),
    ctypes.POINTER(ctypes.wintypes.DWORD),
    ctypes.wintypes.BOOL,
]

kernel32.CancelIoEx.restype = ctypes.wintypes.BOOL
kernel32.CancelIoEx.argtypes = [
    ctypes.wintypes.HANDLE,
    ctypes.POINTER(OVERLAPPED),
]

kernel32.SetNamedPipeHandleState.restype = ctypes.wintypes.BOOL
kernel32.SetNamedPipeHandleState.argtypes = [
    ctypes.wintypes.HANDLE,                    # hNamedPipe
    ctypes.POINTER(ctypes.wintypes.DWORD),     # lpMode
    ctypes.POINTER(ctypes.wintypes.DWORD),     # lpMaxCollectionCount
    ctypes.POINTER(ctypes.wintypes.DWORD),     # lpCollectDataTimeout
]


class UniversalHookManager:
    _instance = None
    _singleton_lock = threading.Lock()
    PIPE_READMODE_MESSAGE = 0x02
    PIPE_TIMEOUT_MS = 3000  # 3 seconds timeout for pipe operations
    PROTOCOL_VERSION = 2  # Must match DLL
    FILE_FLAG_OVERLAPPED = 0x40000000
    ERROR_IO_PENDING = 997
    WAIT_OBJECT_0 = 0
    WAIT_TIMEOUT = 258

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._singleton_lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._bus = EventBus.get_instance()
        self._pipe = None
        self._pid = None  # Current connected PID
        self._lock = threading.RLock()  # Use RLock to allow reentrant calls
        self._dll_path = os.path.join(PLUGINS_DIR, "universal_hook", "Universal-ImGui-Hook.dll")
        self._pending_dll_path = self._dll_path + ".pending"
        self._revision_file = os.path.join(APP_DIR, "data", "universal_revision.json")
        self._revision = self._load_revision()  # Load revision from file
        self.last_injection_attempted = False

    def _load_revision(self):
        """Load revision from file to support program restart takeover"""
        try:
            if os.path.exists(self._revision_file):
                with open(self._revision_file, 'r') as f:
                    data = json.load(f)
                    return data.get('revision', 0)
        except Exception:
            pass
        return 0

    def _save_revision(self):
        """Save revision to file"""
        try:
            os.makedirs(os.path.dirname(self._revision_file), exist_ok=True)
            with open(self._revision_file, 'w') as f:
                json.dump({'revision': self._revision}, f)
        except Exception:
            pass

    @property
    def injected(self):
        # Check if pipe is connected to a valid process
        return self._pipe is not None and self._pid is not None

    def _get_pipe_name(self, pid):
        """Generate PID-specific pipe name"""
        return f"\\\\.\\pipe\\ucf_universal_hook_{pid}"

    def try_connect_existing(self, pid):
        """
        Try to connect to existing DLL in process.
        Returns True if connected to existing DLL with valid hello response.
        """
        with self._lock:
            # Close existing pipe if any
            self._close_pipe()
            
            # Try to connect to PID-specific pipe
            pipe_name = self._get_pipe_name(pid)
            
            # Try to connect (short timeout)
            handle = kernel32.CreateFileW(
                pipe_name,
                0xC0000000,  # GENERIC_READ | GENERIC_WRITE
                0,
                None,
                3,  # OPEN_EXISTING
                self.FILE_FLAG_OVERLAPPED,
                None,
            )
            
            if not handle or handle == ctypes.wintypes.HANDLE(-1).value:
                return False
            
            # Set pipe to message mode
            mode = ctypes.wintypes.DWORD(self.PIPE_READMODE_MESSAGE)
            if not kernel32.SetNamedPipeHandleState(handle, ctypes.byref(mode), None, None):
                kernel32.CloseHandle(handle)
                return False
            
            self._pipe = handle
            
            # Send hello to verify
            try:
                response = self._send({"cmd": "hello"})
                if not response.get("ok"):
                    self._close_pipe()
                    return False
                
                # Verify PID matches
                if response.get("pid") != pid:
                    self._log("error", f"PID mismatch: expected {pid}, got {response.get('pid')}")
                    self._close_pipe()
                    return False
                
                # Verify protocol version
                if response.get("protocol") != self.PROTOCOL_VERSION:
                    self._log("error", f"Protocol mismatch: expected {self.PROTOCOL_VERSION}, got {response.get('protocol')}")
                    self._close_pipe()
                    return False
                
                self._pid = pid
                self._sync_revision_from_dll()
                self._log("success", f"连接到现有 DLL (PID: {pid})")
                return True
                
            except Exception as e:
                self._log("error", f"Hello failed: {e}")
                self._close_pipe()
                return False

    def inject_and_connect(self, pid):
        """
        Inject DLL and connect to it.
        Returns True if injection and connection both succeed.
        """
        with self._lock:
            self.last_injection_attempted = False
            self._apply_pending_update()

            # Check if DLL is already loaded
            if self._is_dll_loaded(pid):
                self._log("info", "DLL already loaded, connecting...")
                return self.try_connect_existing(pid)
            
            # Inject DLL
            self.last_injection_attempted = True
            if not self._inject(pid):
                return False
            
            # Wait for pipe to be ready
            if not self._connect_pipe(pid, timeout=10.0):
                self._log("error", "DLL injected but pipe not ready")
                return False
            
            # Send hello to verify
            try:
                response = self._send({"cmd": "hello"})
                if not response.get("ok"):
                    self._log("error", "Hello failed after injection")
                    self._close_pipe()
                    return False
                
                # Verify PID matches
                if response.get("pid") != pid:
                    self._log("error", f"PID mismatch after injection: expected {pid}, got {response.get('pid')}")
                    self._close_pipe()
                    return False
                
                # Verify protocol version
                if response.get("protocol") != self.PROTOCOL_VERSION:
                    self._log("error", f"Protocol mismatch: expected {self.PROTOCOL_VERSION}, got {response.get('protocol')}")
                    self._close_pipe()
                    return False
                
                self._pid = pid
                self._sync_revision_from_dll()
                self._log("success", f"DLL 注入成功 (PID: {pid})")
                return True
                
            except Exception as e:
                self._log("error", f"Hello failed after injection: {e}")
                self._close_pipe()
                return False

    def _is_dll_loaded(self, pid):
        """Check if DLL is already loaded in process"""
        try:
            proc = psutil.Process(pid)
            for dll in proc.memory_maps():
                if "Universal-ImGui-Hook.dll" in dll.path:
                    return True
        except Exception:
            pass
        return False

    def _apply_pending_update(self):
        """Install a staged DLL once the previous image is no longer locked."""
        if not os.path.exists(self._pending_dll_path):
            return False
        try:
            os.replace(self._pending_dll_path, self._dll_path)
            self._log("success", "Universal DLL 更新已应用")
            return True
        except OSError:
            return False

    def set_esp_box(self, enabled):
        """Set ESP box state"""
        if not self._pipe:
            return False
        
        with self._lock:
            try:
                # Use set_state with revision for conflict prevention
                self._revision += 1
                self._save_revision()  # Persist revision
                response = self._send({
                    "cmd": "set_state",
                    "revision": self._revision,
                    "esp_box": bool(enabled)
                })
                
                ok = (
                    bool(response.get("ok"))
                    and response.get("esp_box") is bool(enabled)
                    and response.get("revision", -1) >= self._revision
                )
                if ok:
                    self._log("success", "方框透视已开启" if enabled else "方框透视已关闭")
                else:
                    self._log("error", response.get("error", "方框透视设置失败"))
                return ok
            except Exception as e:
                self._log("error", f"设置失败: {e}")
                return False

    def get_state(self):
        """Get current state from DLL"""
        if not self._pipe:
            return None
        
        with self._lock:
            try:
                return self._send({"cmd": "get_state"})
            except Exception:
                return None

    def ping(self):
        """Ping the DLL"""
        if not self._pipe:
            return False
        try:
            return bool(self._send({"cmd": "ping"}).get("ok"))
        except Exception:
            return False

    def unload(self):
        """Disable ESP and safely unload the injected DLL."""
        with self._lock:
            if not self._pipe:
                return False

            ok = False
            try:
                response = self._send({"cmd": "unload"})
                ok = bool(response.get("ok"))
            except Exception:
                pass
            finally:
                self._close_pipe()
                self._pid = None
                self._revision = 0
                self._save_revision()
            return ok

    def disconnect(self):
        """Close the client pipe without stopping the injected DLL."""
        with self._lock:
            self._close_pipe()
            self._pid = None

    def _sync_revision_from_dll(self):
        state = self._send({"cmd": "get_state"})
        if state.get("ok"):
            self._revision = max(self._revision, int(state.get("revision", 0)))
            self._save_revision()

    def _inject(self, pid):
        """Inject DLL into process"""
        inject_exe = os.path.join(PLUGINS_DIR, "universal_hook", "inject.exe")
        if not os.path.exists(inject_exe):
            self._log("error", f"inject.exe not found: {inject_exe}")
            return False

        if not os.path.exists(self._dll_path):
            self._log("error", f"Universal DLL not found: {self._dll_path}")
            return False

        # Check if process is still alive
        try:
            proc = psutil.Process(pid)
            if not proc.is_running():
                self._log("error", f"Process {pid} is not running")
                return False
        except psutil.NoSuchProcess:
            self._log("error", f"Process {pid} not found")
            return False

        self._log("info", "正在注入 Universal Hook...")
        result = subprocess.run(
            [inject_exe, str(pid), self._dll_path],
            capture_output=True,
            text=True,
            timeout=15,
        )

        # Check return code first
        if result.returncode != 0:
            self._log("error", result.stderr or result.stdout or "Universal Hook 注入失败")
            return False

        # Verify output contains success marker and no error markers
        output = result.stdout or ""
        if "[ERROR]" in output or "LoadLibraryW返回NULL" in output:
            self._log("error", f"DLL 加载失败: {output}")
            return False

        if "DLL注入成功" not in output and "already_loaded" not in output:
            self._log("error", f"注入结果未知: {output}")
            return False

        if "already_loaded" in output:
            self._log("info", "DLL 已加载")
        else:
            self._log("success", f"DLL 注入成功 (PID: {pid})")
        
        return True

    def _connect_pipe(self, pid, timeout):
        """Connect to PID-specific pipe"""
        pipe_name = self._get_pipe_name(pid)
        deadline = time.time() + timeout
        
        while time.time() < deadline:
            # Use synchronous mode to match DLL's PIPE_WAIT server
            handle = kernel32.CreateFileW(
                pipe_name,
                0xC0000000,  # GENERIC_READ | GENERIC_WRITE
                0,
                None,
                3,  # OPEN_EXISTING
                self.FILE_FLAG_OVERLAPPED,
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

        timeout_ms = timeout_ms or self.PIPE_TIMEOUT_MS
        data = json.dumps(payload, separators=(",", ":")).encode("utf-8")

        self._overlapped_io(
            kernel32.WriteFile,
            ctypes.create_string_buffer(data),
            len(data),
            "write",
            timeout_ms,
        )

        buffer = ctypes.create_string_buffer(4096)
        read_bytes = self._overlapped_io(
            kernel32.ReadFile,
            buffer,
            4096,
            "read",
            timeout_ms,
        )

        return json.loads(buffer.raw[:read_bytes].decode("utf-8"))

    def _overlapped_io(self, fn, buffer, size, operation, timeout_ms):
        event = kernel32.CreateEventW(None, True, False, None)
        if not event:
            raise RuntimeError(f"pipe {operation} event failed: {ctypes.get_last_error()}")

        overlapped = OVERLAPPED()
        overlapped.hEvent = event
        transferred = ctypes.wintypes.DWORD(0)

        try:
            ok = fn(
                self._pipe,
                buffer,
                size,
                ctypes.byref(transferred),
                ctypes.byref(overlapped),
            )
            if ok:
                return transferred.value

            err = ctypes.get_last_error()
            if err != self.ERROR_IO_PENDING:
                self._close_pipe()
                raise RuntimeError(f"pipe {operation} failed: {err}")

            wait = kernel32.WaitForSingleObject(event, timeout_ms)
            if wait == self.WAIT_TIMEOUT:
                kernel32.CancelIoEx(self._pipe, ctypes.byref(overlapped))
                self._close_pipe()
                raise RuntimeError(f"pipe {operation} timed out")
            if wait != self.WAIT_OBJECT_0:
                kernel32.CancelIoEx(self._pipe, ctypes.byref(overlapped))
                self._close_pipe()
                raise RuntimeError(f"pipe {operation} wait failed: {ctypes.get_last_error()}")

            if not kernel32.GetOverlappedResult(
                self._pipe,
                ctypes.byref(overlapped),
                ctypes.byref(transferred),
                False,
            ):
                err = ctypes.get_last_error()
                self._close_pipe()
                raise RuntimeError(f"pipe {operation} result failed: {err}")
            return transferred.value
        finally:
            kernel32.CloseHandle(event)

    def _close_pipe(self):
        if self._pipe:
            kernel32.CloseHandle(self._pipe)
            self._pipe = None

    def _log(self, level, message):
        self._bus.emit("log_message", level=level, module="Universal", message=message)
