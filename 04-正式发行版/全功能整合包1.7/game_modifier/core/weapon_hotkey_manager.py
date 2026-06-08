import json
import os
import functools
import time

import keyboard

from core.config import WEAPON_HOTKEYS_FILE, WEAPON_HOTKEY_POSITIONS, WEAPON_HOTKEY_DISPLAY_NAMES
from core.event_bus import EventBus


class WeaponHotkeyManager:
    """武器快捷键管理器"""
    _instance = None

    def __init__(self):
        self._weapon_hotkeys = {}      # 快捷键 -> 武器ID
        self._reverse_map = {}         # 武器ID -> 快捷键
        self._hotkey_handles = []      # keyboard库的handle
        self._give_weapon_callback = None  # 赋予武器的回调函数
        self._app = None  # 主窗口引用，用于调度到主线程
        self._enabled = False
        self._state_version = 0
        self._last_trigger_time = 0  # 上次触发时间（防抖）
        self._debounce_interval = 0.5  # 防抖间隔（秒）
        self._load_hotkeys()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_hotkeys(self):
        """加载武器快捷键配置"""
        if os.path.exists(WEAPON_HOTKEYS_FILE):
            try:
                with open(WEAPON_HOTKEYS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 加载正向映射
                for hotkey in WEAPON_HOTKEY_POSITIONS:
                    if hotkey in data and data[hotkey]:
                        weapon_id = data[hotkey]
                        self._weapon_hotkeys[hotkey] = weapon_id
                        self._reverse_map[weapon_id] = hotkey
            except Exception as e:
                bus = EventBus.get_instance()
                bus.emit('log_message', level='error', module='武器快捷键',
                         message=f'加载配置失败: {e}')

    def _save_hotkeys(self):
        """保存武器快捷键配置"""
        try:
            data = {}
            for hotkey in WEAPON_HOTKEY_POSITIONS:
                data[hotkey] = self._weapon_hotkeys.get(hotkey)
            
            with open(WEAPON_HOTKEYS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            bus = EventBus.get_instance()
            bus.emit('log_message', level='error', module='武器快捷键',
                     message=f'保存配置失败: {e}')

    def bind_weapon_hotkey(self, hotkey, weapon_id, weapon_name):
        """
        绑定武器快捷键
        返回: (success, error_msg)
        """
        # 检查快捷键是否有效
        if hotkey not in WEAPON_HOTKEY_POSITIONS:
            return (False, f"无效的快捷键: {hotkey}")
        
        # 检查是否已被其他武器占用
        if hotkey in self._weapon_hotkeys:
            existing_weapon_id = self._weapon_hotkeys[hotkey]
            if existing_weapon_id != weapon_id:
                return (False, f"快捷键已被其他武器占用")
        
        # 检查武器是否已绑定其他快捷键
        if weapon_id in self._reverse_map:
            old_hotkey = self._reverse_map[weapon_id]
            if old_hotkey != hotkey:
                # 先解绑旧的
                del self._weapon_hotkeys[old_hotkey]
        
        # 绑定新的
        self._weapon_hotkeys[hotkey] = weapon_id
        self._reverse_map[weapon_id] = hotkey
        
        # 保存
        self._save_hotkeys()
        
        # 重新注册快捷键监听
        self._rebind_hotkeys()
        
        # 日志
        bus = EventBus.get_instance()
        display_name = WEAPON_HOTKEY_DISPLAY_NAMES.get(hotkey, hotkey)
        bus.emit('log_message', level='success', module='武器快捷键',
                 message=f'{display_name} 已绑定到 {weapon_name}')
        
        return (True, None)

    def unbind_weapon_hotkey(self, weapon_id):
        """解绑武器快捷键"""
        if weapon_id not in self._reverse_map:
            return False
        
        hotkey = self._reverse_map[weapon_id]
        del self._weapon_hotkeys[hotkey]
        del self._reverse_map[weapon_id]
        
        # 保存
        self._save_hotkeys()
        
        # 重新注册快捷键监听
        self._rebind_hotkeys()
        
        # 日志
        bus = EventBus.get_instance()
        display_name = WEAPON_HOTKEY_DISPLAY_NAMES.get(hotkey, hotkey)
        bus.emit('log_message', level='info', module='武器快捷键',
                 message=f'{display_name} 已解绑')
        
        return True

    def get_weapon_hotkey(self, weapon_id):
        """获取武器绑定的快捷键，返回 None 或 'shift+1'"""
        return self._reverse_map.get(weapon_id)

    def get_weapon_by_hotkey(self, hotkey):
        """获取快捷键绑定的武器ID，返回 None 或 weapon_id"""
        return self._weapon_hotkeys.get(hotkey)

    def get_available_hotkeys(self):
        """获取可用的快捷键列表（未绑定的）"""
        available = []
        for hotkey in WEAPON_HOTKEY_POSITIONS:
            if hotkey not in self._weapon_hotkeys:
                available.append(hotkey)
        return available

    def get_all_bindings(self):
        """获取所有绑定关系，返回 {快捷键: 武器ID}"""
        return self._weapon_hotkeys.copy()

    def setup_hotkeys(self, give_weapon_callback, app=None):
        """注册所有武器快捷键监听
        
        Args:
            give_weapon_callback: 赋予武器的回调函数
            app: 主窗口引用，用于将操作调度到主线程（线程安全）
        """
        self._give_weapon_callback = give_weapon_callback
        self._app = app
        self._enabled = True
        self._state_version += 1
        self._rebind_hotkeys()

    def pause_hotkeys(self):
        """Temporarily ignore weapon hotkeys without removing saved bindings."""
        self._enabled = False
        self._state_version += 1

    def resume_hotkeys(self):
        """Resume weapon hotkeys after the game connection is ready."""
        self._enabled = True
        self._state_version += 1

    def cleanup(self):
        """Remove all registered weapon hotkey listeners."""
        for handle in self._hotkey_handles:
            try:
                keyboard.remove_hotkey(handle)
            except Exception:
                pass
        self._hotkey_handles = []
        self._give_weapon_callback = None
        self._app = None
        self._enabled = False
        self._state_version += 1

    def _rebind_hotkeys(self):
        """重新绑定所有快捷键监听"""
        # 清除旧的监听
        for handle in self._hotkey_handles:
            try:
                keyboard.remove_hotkey(handle)
            except:
                pass
        self._hotkey_handles = []
        
        # 注册新的监听
        for hotkey, weapon_id in self._weapon_hotkeys.items():
            try:
                callback = functools.partial(self._on_hotkey_triggered, weapon_id)
                handle = keyboard.add_hotkey(hotkey, callback)
                self._hotkey_handles.append(handle)
            except Exception as e:
                bus = EventBus.get_instance()
                bus.emit('log_message', level='error', module='武器快捷键',
                         message=f'注册快捷键 {hotkey} 失败: {e}')

    def _on_hotkey_triggered(self, weapon_id):
        """快捷键触发时的回调（在后台线程中执行）
        
        关键：使用防抖机制避免重复触发，并将操作调度到主线程执行
        """
        if not self._enabled:
            return

        # 防抖：检查距离上次触发的时间间隔
        current_time = time.time()
        if current_time - self._last_trigger_time < self._debounce_interval:
            # 忽略过快的重复触发
            return
        
        self._last_trigger_time = current_time
        state_version = self._state_version
        
        if self._give_weapon_callback:
            try:
                # 方案1：如果有app引用，使用after调度到主线程（线程安全）
                if self._app and hasattr(self._app, 'after'):
                    self._app.after(0, lambda: self._safe_give_weapon(weapon_id, state_version))
                else:
                    # 降级方案：直接调用（可能不安全，但至少有防抖）
                    self._safe_give_weapon(weapon_id, state_version)
            except Exception as e:
                bus = EventBus.get_instance()
                bus.emit('log_message', level='error', module='武器快捷键',
                         message=f'调度武器赋予失败: {e}')
    
    def _safe_give_weapon(self, weapon_id, state_version=None):
        """安全地执行赋予武器操作（在主线程中执行）"""
        if not self._enabled:
            return
        if state_version is not None and state_version != self._state_version:
            return
        if self._give_weapon_callback:
            try:
                self._give_weapon_callback(weapon_id)
            except Exception as e:
                bus = EventBus.get_instance()
                bus.emit('log_message', level='error', module='武器快捷键',
                         message=f'赋予武器失败: {e}')
