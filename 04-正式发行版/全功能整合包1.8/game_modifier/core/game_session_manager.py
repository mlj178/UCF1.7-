"""
Game Session Manager - Unified coordinator for game connection and feature synchronization

This module provides a single point of control for:
- Game process detection and monitoring
- Frida connection lifecycle
- Universal DLL connection lifecycle
- Feature state synchronization

Core state machine:
NO_GAME -> WAITING_GAME_READY -> CONNECTING_FRIDA -> READY -> DISCONNECTED
Universal DLL is optional and handled inside READY only when ESP is desired.
"""

import threading
import time
import psutil
from enum import Enum
from typing import Optional, Dict, Any, Callable
from .event_bus import EventBus
from .log_manager import log_to_file
from .services import AppPersistenceService


class SessionState(Enum):
    NO_GAME = "no_game"
    WAITING_GAME_READY = "waiting_game_ready"
    CONNECTING_FRIDA = "connecting_frida"
    READY = "ready"
    DISCONNECTED = "disconnected"


class GameSessionManager:
    _instance = None
    _singleton_lock = threading.Lock()
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._singleton_lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        self._bus = EventBus.get_instance()
        self._state = SessionState.NO_GAME
        self._pid = None
        self._pid_create_time = None
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._wake_event = threading.Event()
        self._worker_thread = None
        self._frida_manager = None
        self._universal_manager = None
        self._persistence_service = AppPersistenceService()
        
        # Desired feature states (persisted)
        self._desired_states = {}
        
        # Applied feature states (runtime, from DLL)
        self._applied_states = {}
        
        # Retry configuration
        self._retry_delays = [1, 2, 4, 8, 16]  # Exponential backoff
        self._retry_index = 0
        self._last_universal_retry = 0.0
        self._universal_retry_interval = 10.0  # seconds between DLL reconnect attempts
        self._injection_attempt_identity = None
        self._next_retry_at = 0.0
        self._process_detected_at = 0.0
        
        # Process stability check
        self._stability_wait = 0.5  # Wait 0.5 seconds after process detection
        
        self._process_poll_interval = 0.8
        self._ready_check_interval = 3.0
        
    def start(self):
        """Start the session manager worker thread"""
        if self._worker_thread and self._worker_thread.is_alive():
            return

        self._load_desired_states()
        self._stop_event.clear()
        self._wake_event.clear()
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()

    def reconnect(self):
        """Request a reconnect without creating another attach worker."""
        self._reset_session()

    def disconnect(self):
        """Request a managed disconnect of the current game session."""
        self._reset_session()
    
    def stop(self):
        """Stop the session manager"""
        log_to_file("info", "系统", "GameSessionManager stopping")
        self._stop_event.set()
        self._wake_event.set()
        try:
            if self._worker_thread:
                self._worker_thread.join(timeout=5)
                if self._worker_thread.is_alive():
                    log_to_file("warning", "系统", "GameSessionManager worker did not stop within timeout")
                else:
                    log_to_file("info", "系统", "GameSessionManager worker stopped")

            if self._universal_manager:
                try:
                    self._universal_manager.unload()
                    log_to_file("info", "系统", "Universal hook manager unloaded")
                except Exception as e:
                    log_to_file("warning", "系统", f"Universal hook manager unload failed: {e}")

            if self._frida_manager:
                try:
                    self._frida_manager.disconnect()
                    log_to_file("info", "系统", "Frida manager disconnected")
                except Exception as e:
                    log_to_file("warning", "系统", f"Frida manager disconnect failed: {e}")
        finally:
            self._universal_manager = None
            self._frida_manager = None
            log_to_file("info", "系统", "GameSessionManager stopped")
    
    def set_desired_state(self, feature_id: str, enabled: bool):
        """Set desired feature state (user intent)"""
        with self._lock:
            self._desired_states[feature_id] = enabled
            self._save_desired_states()

        if feature_id == 'esp_box' and self._universal_manager:
            if self._universal_manager.set_esp_box(enabled):
                with self._lock:
                    self._applied_states[feature_id] = enabled
        self._wake_event.set()
    
    def get_desired_state(self, feature_id: str) -> bool:
        """Get desired feature state"""
        with self._lock:
            return self._desired_states.get(feature_id, False)
    
    def get_applied_state(self, feature_id: str) -> bool:
        """Get applied feature state (actual state in DLL)"""
        with self._lock:
            return self._applied_states.get(feature_id, False)
    
    def get_state(self) -> SessionState:
        """Get current session state"""
        with self._lock:
            return self._state
    
    def get_pid(self) -> Optional[int]:
        """Get current game PID"""
        with self._lock:
            return self._pid
    
    def _worker_loop(self):
        """Run transitions immediately; wait only when the current state has no progress."""
        while not self._stop_event.is_set():
            with self._lock:
                before = self._state
            try:
                self._state_machine_step()
            except Exception as e:
                self._bus.emit('log_message', level='error', module='SessionManager',
                              message=f'State machine error: {e}')
            with self._lock:
                after = self._state

            if after != before:
                continue

            wait_time = self._ready_check_interval if after == SessionState.READY else self._process_poll_interval
            if after == SessionState.DISCONNECTED and self._next_retry_at > 0:
                wait_time = max(0.05, min(wait_time, self._next_retry_at - time.monotonic()))
            self._wake_event.wait(max(0.05, wait_time))
            self._wake_event.clear()
    
    def _state_machine_step(self):
        """Execute one step of the state machine"""
        with self._lock:
            current_state = self._state
        
        if current_state == SessionState.NO_GAME:
            self._step_no_game()
        elif current_state == SessionState.WAITING_GAME_READY:
            self._step_waiting_game_ready()
        elif current_state == SessionState.CONNECTING_FRIDA:
            self._step_connecting_frida()
        elif current_state == SessionState.READY:
            self._step_ready()
        elif current_state == SessionState.DISCONNECTED:
            self._step_disconnected()
    
    def _step_no_game(self):
        """Step: No game process detected"""
        pid, create_time = self._find_game_process()
        
        if pid is None:
            return
        
        with self._lock:
            if (pid, create_time) != (self._pid, self._pid_create_time):
                self._injection_attempt_identity = None
            self._pid = pid
            self._pid_create_time = create_time
            self._process_detected_at = time.monotonic()
            self._state = SessionState.WAITING_GAME_READY
        
        self._bus.emit('log_message', level='info', module='SessionManager',
                      message=f'检测到游戏进程 PID:{pid}')
    
    def _step_waiting_game_ready(self):
        """Step: Wait for game process to stabilize"""
        pid, create_time = self._find_game_process()
        
        # Check if PID changed
        with self._lock:
            old_pid = self._pid
            old_create_time = self._pid_create_time
        
        if pid != old_pid or create_time != old_create_time:
            # PID changed, reset
            with self._lock:
                self._pid = pid
                self._pid_create_time = create_time
                self._process_detected_at = time.monotonic()
            self._bus.emit('log_message', level='info', module='SessionManager',
                          message=f'游戏进程变化 PID:{pid}')
            return
        
        # Check if process is terminating
        if not self._is_process_stable(pid):
            with self._lock:
                self._state = SessionState.NO_GAME
                self._pid = None
                self._pid_create_time = None
            self._bus.emit('log_message', level='warning', module='SessionManager',
                          message='游戏进程不稳定，重新检测')
            return
        
        # Non-blocking stability window; the worker wakes again after the short poll interval.
        if time.monotonic() - self._process_detected_at < self._stability_wait:
            return
        
        # Check again after wait
        if not self._is_process_stable(pid):
            with self._lock:
                self._state = SessionState.NO_GAME
                self._pid = None
                self._pid_create_time = None
            return
        
        # Core features become available first. Universal DLL is handled later in READY.
        with self._lock:
            self._state = SessionState.CONNECTING_FRIDA
    
    def _step_connecting_frida(self):
        """Step: Connect Frida to game process"""
        with self._lock:
            pid = self._pid
        
        if pid is None:
            with self._lock:
                self._state = SessionState.NO_GAME
            return
        
        # Import here to avoid circular dependency
        from .frida_manager import FridaManager
        frida = FridaManager.get_instance()
        
        try:
            success, reason = frida.connect(pid)
            if success:
                self._frida_manager = frida
                with self._lock:
                    self._state = SessionState.READY
                self._retry_index = 0
                self._bus.emit(
                    'connection_status',
                    status='connected',
                    pid=pid,
                )
                self._bus.emit('log_message', level='success', module='SessionManager',
                              message='Frida 连接成功')
            else:
                # Handle specific error reasons
                if reason == 'process_terminating':
                    self._bus.emit('log_message', level='warning', module='SessionManager',
                                  message='游戏进程正在终止，重新检测')
                    with self._lock:
                        self._state = SessionState.NO_GAME
                        self._pid = None
                        self._pid_create_time = None
                    return
                
                self._handle_connection_failure(f"Frida 连接失败: {reason}")
        except Exception as e:
            error_msg = str(e)
            
            # Check for specific error codes
            if '0xc000010a' in error_msg or 'STATUS_PROCESS_IS_TERMINATING' in error_msg:
                self._bus.emit('log_message', level='warning', module='SessionManager',
                              message='游戏进程正在终止，重新检测')
                with self._lock:
                    self._state = SessionState.NO_GAME
                    self._pid = None
                    self._pid_create_time = None
                return
            
            self._handle_connection_failure(f"Frida 连接异常: {e}")
    
    def _step_ready(self):
        """Step: Monitor game process and connection health"""
        with self._lock:
            pid = self._pid
            old_create_time = self._pid_create_time
        
        # Check if game process still exists
        current_pid, current_create_time = self._find_game_process()
        
        if current_pid != pid or current_create_time != old_create_time:
            # Game process changed
            self._bus.emit('log_message', level='info', module='SessionManager',
                          message='游戏进程变化，重新连接')
            self._reset_session()
            return
        
        # Check Frida connection
        if self._frida_manager and not self._frida_manager.is_ready():
            self._bus.emit('log_message', level='warning', module='SessionManager',
                          message='Frida 连接断开')
            self._reset_session()
            return
        
        if self._universal_manager:
            if not self._universal_manager.ping():
                self._universal_manager.disconnect()
                self._universal_manager = None
                self._bus.emit(
                    'universal_status',
                    status='unavailable',
                    pid=pid,
                )

        with self._lock:
            esp_wanted = bool(self._desired_states.get('esp_box', False))

        # ESP关闭时不连接、不注入DLL；普通Frida功能不受影响。
        if not esp_wanted or self._universal_manager:
            return

        if time.time() - self._last_universal_retry < self._universal_retry_interval:
            return

        self._last_universal_retry = time.time()
        self._connect_universal_for_esp(pid)
    
    def _step_disconnected(self):
        """Step: Handle disconnection without blocking the worker thread."""
        if time.monotonic() < self._next_retry_at:
            return
        with self._lock:
            self._state = SessionState.NO_GAME
    
    def _handle_connection_failure(self, reason: str):
        """Handle connection failure with retry"""
        self._bus.emit('log_message', level='error', module='SessionManager',
                      message=reason)
        
        delay = self._retry_delays[min(self._retry_index, len(self._retry_delays) - 1)]
        self._retry_index = min(self._retry_index + 1, len(self._retry_delays) - 1)
        self._next_retry_at = time.monotonic() + delay
        with self._lock:
            self._state = SessionState.DISCONNECTED

    def _connect_universal_for_esp(self, pid: int):
        """Connect or inject Universal DLL only after Frida is ready and ESP is desired."""
        from .universal_hook_manager import UniversalHookManager

        universal = UniversalHookManager.get_instance()
        if universal.try_connect_existing(pid):
            self._universal_manager = universal
            with self._lock:
                esp_wanted = bool(self._desired_states.get('esp_box', False))
            if universal.set_esp_box(esp_wanted):
                with self._lock:
                    self._applied_states['esp_box'] = esp_wanted
            self._bus.emit('log_message', level='success', module='SessionManager',
                          message='ESP DLL 已连接')
            return

        identity = (pid, self._pid_create_time)
        if self._injection_attempt_identity == identity:
            return

        connected = universal.inject_and_connect(pid)
        if universal.last_injection_attempted:
            self._injection_attempt_identity = identity
        if not connected:
            self._mark_universal_unavailable('ESP DLL 注入失败')
            return

        self._universal_manager = universal
        with self._lock:
            esp_wanted = bool(self._desired_states.get('esp_box', False))
        if universal.set_esp_box(esp_wanted):
            with self._lock:
                self._applied_states['esp_box'] = esp_wanted
        self._bus.emit('log_message', level='success', module='SessionManager',
                      message='ESP DLL 已在后台就绪')

    def _mark_universal_unavailable(self, reason: str):
        """Continue with Frida while keeping ESP unavailable for this process."""
        self._bus.emit(
            'log_message',
            level='warning',
            module='SessionManager',
            message=f'{reason}，普通功能保持可用，方框模块稍后重试',
        )
        self._bus.emit(
            'universal_status',
            status='unavailable',
            pid=self._pid,
        )
        self._universal_manager = None
        self._last_universal_retry = time.time()
        with self._lock:
            self._state = (
                SessionState.READY
                if self._frida_manager
                else SessionState.CONNECTING_FRIDA
            )
    
    def _reset_session(self):
        """Reset session state"""
        frida = self._frida_manager
        universal = self._universal_manager

        with self._lock:
            self._state = SessionState.NO_GAME
            self._pid = None
            self._pid_create_time = None
            self._process_detected_at = 0.0
            self._applied_states.clear()
        
        if universal:
            universal.disconnect()
        if frida:
            frida.disconnect()

        self._frida_manager = None
        self._universal_manager = None
        self._retry_index = 0
        self._next_retry_at = 0.0
        self._wake_event.set()
        self._bus.emit('connection_status', status='disconnected')
    
    def _find_game_process(self) -> tuple:
        """Find game process and return (pid, create_time)"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'create_time']):
                name = proc.info.get('name') or ''
                if name.lower() == 'unitycrossfire.exe':
                    return proc.info['pid'], proc.info['create_time']
        except Exception:
            pass
        return None, None
    
    def _is_process_stable(self, pid: int) -> bool:
        """Check if process is stable (not terminating)

        Non-blocking: only verifies the process still exists and is running.
        The terminating state (STATUS_PROCESS_IS_TERMINATING) is detected later
        by FridaManager.connect() via the 0xc000010a error code, so we don't
        need a blocking cpu_percent() sample here.
        """
        try:
            proc = psutil.Process(pid)
            return proc.is_running()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False
    
    def _save_desired_states(self):
        """Persist desired states to file"""
        try:
            self._persistence_service.save_desired_states(self._desired_states)
        except Exception:
            pass
    
    def _load_desired_states(self):
        """Load persisted desired states"""
        try:
            self._desired_states = self._persistence_service.load_desired_states()
        except Exception:
            pass
