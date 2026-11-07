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
    # 3 = 增加 esp_health_mode / esp_health_display（血量显示格式与内容）。
    # 必须与 DLL 一致；不匹配时拒绝复用进程内的旧 DLL（旧版带双引擎重复挂钩风险）。
    # v4：血量数值模式只显示剩余值（不再 "当前/上限"）。
    # v5：新增 esp_box_outline（方框轮廓开关，关闭后仍画血条/数值）。
    # v6：会话自愈（定期重取单例 + 无本地玩家看门狗）、来源策略兜底、esp_diag_* 诊断字段。
    # 旧 DLL 必须重启游戏后重新注入。
    PROTOCOL_VERSION = 6  # Must match DLL
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
        self._esp_box_enabled = False
        self._esp_target_scope = "enemy_only"
        # 血量显示：percent=百分比 / value=剩余数值（只显示当前血量）；bar=仅血条 / text=仅数值 / both=血条+数值
        self._esp_health_mode = "percent"
        self._esp_health_display = "both"
        self._esp_box_outline = True  # 方框轮廓开关
        self.last_injection_attempted = False
        self._last_ping_time = 0.0
        self._ping_interval = 15.0  # minimum seconds between pings

    def _load_revision(self):
        """Load revision from file to support program restart takeover"""
        try:
            if os.path.exists(self._revision_file):
                with open(self._revision_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('revision', 0)
        except Exception as e:
            self._log("warning", f"Universal revision read failed: {e}")
        return 0

    def _save_revision(self):
        """Save revision to file"""
        try:
            os.makedirs(os.path.dirname(self._revision_file), exist_ok=True)
            with open(self._revision_file, 'w', encoding='utf-8') as f:
                json.dump({'revision': self._revision}, f, ensure_ascii=False)
        except Exception as e:
            self._log("warning", f"Universal revision write failed: {e}")

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
                    self._log(
                        "error",
                        f"Protocol mismatch: expected {self.PROTOCOL_VERSION}, got {response.get('protocol')}；"
                        "游戏中是旧版 DLL，请重启游戏后重新注入",
                    )
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
                    self._log(
                        "error",
                        f"Protocol mismatch: expected {self.PROTOCOL_VERSION}, got {response.get('protocol')}；"
                        "游戏中是旧版 DLL，请重启游戏后重新注入",
                    )
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

    HEALTH_MODE_CODES = {"percent": 0, "value": 1}
    HEALTH_DISPLAY_CODES = {"bar": 0, "text": 1, "both": 2}

    @classmethod
    def _normalize_health_mode(cls, mode):
        return mode if mode in cls.HEALTH_MODE_CODES else "percent"

    @classmethod
    def _normalize_health_display(cls, display):
        return display if display in cls.HEALTH_DISPLAY_CODES else "both"

    def set_esp_box(self, enabled):
        """Set ESP box state"""
        return self.set_esp_state(enabled, self._esp_target_scope)

    def set_esp_target_scope(self, scope):
        """Set which non-local players the native ESP should draw."""
        normalized = "all_players" if scope == "all_players" else "enemy_only"
        self._esp_target_scope = normalized
        return self.set_esp_state(self._esp_box_enabled, normalized)

    def set_esp_health_options(self, health_mode=None, health_display=None):
        """Set native ESP health readout format/content and push it immediately."""
        if health_mode is not None:
            self._esp_health_mode = self._normalize_health_mode(health_mode)
        if health_display is not None:
            self._esp_health_display = self._normalize_health_display(health_display)
        return self.set_esp_state(self._esp_box_enabled, self._esp_target_scope)

    def set_esp_box_outline(self, enabled):
        """Turn the ESP box outline on/off and push it immediately."""
        self._esp_box_outline = bool(enabled)
        return self.set_esp_state(self._esp_box_enabled, self._esp_target_scope)

    def get_esp_options(self):
        """返回上一次成功下发到 DLL 的选项（失败不更新，故等于 DLL 当前生效值）。"""
        return {
            "esp_target_scope": self._esp_target_scope,
            "esp_health_mode": self._esp_health_mode,
            "esp_health_display": self._esp_health_display,
            "esp_box_outline": bool(self._esp_box_outline),
        }

    def fetch_diagnostics(self):
        """读取 DLL 最近一帧的渲染诊断；管道不可用/失败时返回 None。

        用来回答"方框为什么没画出来"：没有候选、被来源策略拒了、还是被死活/敌我过滤拒了。
        """
        if not self._pipe:
            return None
        try:
            with self._lock:
                state = self._send({"cmd": "get_state"})
        except Exception:
            return None
        if not state or not state.get("ok"):
            return None
        return {
            "game_mode": state.get("esp_diag_mode", -1),
            "epoch": state.get("esp_diag_epoch", 0),
            "round_over": state.get("esp_diag_round_over", 0),
            "candidates": state.get("esp_diag_candidates", 0),
            "rejected_source": state.get("esp_diag_rejected_source", 0),
            "rejected_object": state.get("esp_diag_rejected_object", 0),
            "rejected_team": state.get("esp_diag_rejected_team", 0),
            "drawn": state.get("esp_diag_drawn", 0),
            "relaxed_drawn": state.get("esp_diag_relaxed_drawn", 0),
        }

    def set_esp_state(self, enabled, scope, health_mode=None, health_display=None,
                      box_outline=None):
        """Set ESP enabled state, target scope, box outline and health options at once."""
        normalized = "all_players" if scope == "all_players" else "enemy_only"
        mode = self._normalize_health_mode(health_mode) if health_mode is not None else self._esp_health_mode
        display = (
            self._normalize_health_display(health_display)
            if health_display is not None
            else self._esp_health_display
        )
        outline = bool(box_outline) if box_outline is not None else self._esp_box_outline
        return self._set_esp_state(bool(enabled), normalized, mode, display, outline)

    def _set_esp_state(self, enabled, scope, health_mode, health_display, box_outline):
        if not self._pipe:
            return False

        mode_code = self.HEALTH_MODE_CODES[health_mode]
        display_code = self.HEALTH_DISPLAY_CODES[health_display]

        with self._lock:
            try:
                # Use set_state with revision for conflict prevention
                self._revision += 1
                self._save_revision()  # Persist revision
                response = self._send({
                    "cmd": "set_state",
                    "revision": self._revision,
                    "esp_box": bool(enabled),
                    "esp_all_players": scope == "all_players",
                    "esp_health_mode": mode_code,
                    "esp_health_display": display_code,
                    "esp_box_outline": bool(box_outline),
                })

                ok = (
                    bool(response.get("ok"))
                    and bool(response.get("esp_box")) == bool(enabled)
                    and bool(response.get("esp_all_players")) == (scope == "all_players")
                    # 必须显式回读布尔值：旧 DLL 不认识该字段（None）时必须判失败，
                    # 否则方框开关会静默失效。
                    and response.get("esp_box_outline") == bool(box_outline)
                    and response.get("esp_health_mode") == mode_code
                    and response.get("esp_health_display") == display_code
                    and response.get("revision", -1) >= self._revision
                )
                if ok:
                    self._esp_box_enabled = bool(enabled)
                    self._esp_target_scope = scope
                    self._esp_health_mode = health_mode
                    self._esp_health_display = health_display
                    self._esp_box_outline = bool(box_outline)
                    # 记录 DLL 回读确认后的实际生效值：日志里能直接看到"界面选了什么、
                    # 游戏里就生效什么"，排查选项不一致时不用再猜。
                    self._log(
                        "success",
                        "方框透视{}：显示对象={}，血量={}/{}，方框={}，rev={}".format(
                            "已开启" if enabled else "已关闭",
                            scope,
                            health_mode,
                            health_display,
                            "开" if box_outline else "关",
                            self._revision,
                        ),
                    )
                else:
                    # 下发失败时调用方会把配置回退为 DLL 当前生效值，保证界面与实际一致。
                    self._log(
                        "error",
                        response.get("error")
                        or "方框透视选项下发失败，界面已回退为游戏当前值",
                    )
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
        """Ping the DLL (throttled to avoid excessive I/O)"""
        if not self._pipe:
            return False
        now = time.time()
        if now - self._last_ping_time < self._ping_interval:
            return True  # assume alive if recently pinged
        try:
            result = bool(self._send({"cmd": "ping"}).get("ok"))
            if result:
                self._last_ping_time = now
            return result
        except Exception:
            return False

    def unload(self):
        """Development/maintenance unload path.

        Normal modifier shutdown must not call this while the game is running:
        the DLL hooks D3D and GameAssembly, and FreeLibrary during gameplay can
        crash the game. Normal shutdown only disables ESP and disconnects pipe.
        """
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
            self._esp_box_enabled = bool(state.get("esp_box", False))
            self._esp_target_scope = "all_players" if state.get("esp_all_players", False) else "enemy_only"
            self._esp_health_mode = {0: "percent", 1: "value"}.get(
                state.get("esp_health_mode"), self._esp_health_mode
            )
            self._esp_health_display = {0: "bar", 1: "text", 2: "both"}.get(
                state.get("esp_health_display"), self._esp_health_display
            )
            self._esp_box_outline = bool(state.get("esp_box_outline", self._esp_box_outline))
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
        try:
            # inject.exe 是 .NET 控制台程序，按系统控制台代码页（中文 Windows 为 cp936/GBK）
            # 输出中文标记；此处保持 text=True 的原生解码，只加 errors="replace" 兜底，
            # 避免异常字节序列抛 UnicodeDecodeError（不能改成 utf-8，否则中文标记会乱码）。
            result = subprocess.run(
                [inject_exe, str(pid), self._dll_path],
                capture_output=True,
                text=True,
                errors="replace",
                timeout=15,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0x08000000
            )
        except subprocess.TimeoutExpired:
            # P2：注入挂起时 subprocess.run 会抛 TimeoutExpired；原实现未捕获，
            # 会冒泡到会话状态机并被记成笼统的 "State machine error"（子进程已由 subprocess.run 终止）。
            self._log("error", "Universal Hook 注入超时")
            return False
        except OSError as e:
            self._log("error", f"Universal Hook 注入进程启动失败: {e}")
            return False

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

        # P1：原来固定 4096 字节，状态/诊断响应更长时会截断或报 ERROR_MORE_DATA
        read_size = 65536
        buffer = ctypes.create_string_buffer(read_size)
        read_bytes = self._overlapped_io(
            kernel32.ReadFile,
            buffer,
            read_size,
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
        # audience="both"：这类控制面消息既显示在界面日志里，也写进
        # logs/game_modifier.log，方便事后离线排查方框透视问题（默认 user 只进界面）。
        self._bus.emit(
            "log_message",
            level=level,
            module="Universal",
            message=message,
            audience="both",
        )
