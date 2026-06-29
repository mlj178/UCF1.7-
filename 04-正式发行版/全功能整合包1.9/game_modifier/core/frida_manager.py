import threading
import json
import os
from datetime import datetime

import frida
import psutil

from core.config import SCRIPTS_DIR
from core.event_bus import EventBus
from core.log_manager import log_to_file, get_logger
from core.frida_runtime.rpc_client import RpcClient
from core.frida_runtime.script_manager import ScriptManager
from core.plugin.manifest_loader import ManifestLoader


ORDINARY_PLUGIN_FEATURE_IDS = {
    "knife",
    "recoil",
    "ammo",
    "ammoplus",
    "range",
    "aim",
    "speedgun",
    "movespeed",
    "time",
    "gravity",
    "godmode",
    "skillcd",
    "gather",
    "isbot",
    "roundskip",
    "timescale",
}


class _FridaSessionAdapter:
    def __init__(self, frida_manager):
        self._frida_manager = frida_manager

    @property
    def session(self):
        return self._frida_manager.session


class LogManager:
    """日志文件管理器 - bridges to standard logging"""
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def write_log(self, module, level, message):
        """写入日志到文件 (via standard logging)"""
        log_to_file(level, module, message)

    def write_log_unified(self, level, module, message):
        """写入日志到统一文件 (via standard logging)"""
        log_to_file(level, module, message)


class FridaManager:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self._session = None
        self._script = None
        self._ready = False
        self._connecting = False
        self._disconnecting = False
        self._pid = None
        self._script_manager = None
        self._rpc_client = None
        self._lock = threading.Lock()
        self._event_bus = EventBus.get_instance()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @property
    def is_connected(self):
        return self._ready and self._script is not None

    @property
    def pid(self):
        return self._pid

    @property
    def session(self):
        return self._session
    
    def is_ready(self):
        """Check if Frida is ready (called by GameSessionManager)"""
        return self._ready and self._script is not None

    def _build_js_code(self):
        parts = []
        common_path = os.path.join(SCRIPTS_DIR, '_common.js')
        if os.path.exists(common_path):
            with open(common_path, 'r', encoding='utf-8') as f:
                parts.append(f.read())

        from core.feature_registry import FeatureRegistry
        registry = FeatureRegistry.get_instance()
        for feature in registry.get_all():
            if feature.feature_id in ORDINARY_PLUGIN_FEATURE_IDS:
                continue
            js_code = feature.get_js_code()
            if js_code:
                parts.append(js_code)

        parts.append(self._build_dispatcher())
        parts.append(self._build_rpc_exports())
        parts.append(self._build_init_message())

        return '\n\n'.join(parts)

    def _build_dispatcher(self):
        return r"""
function onToggle(data) {
  try {
    var featureName = data.feature;
    var enable = data.enable;

    if (featureName === 'nano4t_init') {
      if (modules.nano4t) modules.nano4t.init();
    } else if (featureName === 'nano4t_set') {
      if (modules.nano4t) modules.nano4t.set(enable.g, enable.h);
    } else if (featureName === 'battle_round_always') {
      if (modules.battle_round_always) {
        if (enable) {
          modules.battle_round_always.enable();
        } else {
          modules.battle_round_always.disable();
        }
      }
    } else {
      sendLog('error', '系统', '未知功能: ' + featureName);
    }
  } catch(e) {
    sendLog('error', '系统', 'toggle异常: ' + (e.message || e));
  } finally {
    recv('toggle', onToggle);
  }
}

recv('toggle', onToggle);
"""

    def _build_rpc_exports(self):
        return r"""
rpc.exports = {
  cleanup: function(reason) {
    if (typeof cleanupAll === 'function') {
      return cleanupAll(reason || 'rpc_cleanup');
    }
    return JSON.stringify({ ok: false, reason: 'cleanupAll_missing' });
  },
  nano4tinit: function() {
    if (!modules.nano4t) {
      send(JSON.stringify({ type: 'nano4t_error', msg: '多人生化模块未加载' }));
      return JSON.stringify({ ok: false });
    }
    modules.nano4t.init();
    return JSON.stringify({ ok: true });
  },
  nano4tset: function(g, h) {
    if (!modules.nano4t) return JSON.stringify({ ok: false });
    modules.nano4t.set(g, h);
    return JSON.stringify({ ok: true });
  },
  nano4tgetcurrent: function() {
    if (!modules.nano4t) return JSON.stringify({ type: 'nano4t_current', g: -1, h: -1, ok: false });
    return modules.nano4t.getCurrent();
  },
  nano4thealthcheck: function() {
    if (!modules.nano4t) return JSON.stringify({ type: 'nano4t_dead' });
    return modules.nano4t.healthCheck();
  },
  giveweapon: function(weaponId, autoGiveUp, autoSelect) {
    if (!modules.weapon_giver) return JSON.stringify({ ok: false, msg: '武器赋予模块未加载' });
    var result = modules.weapon_giver.giveweapon(weaponId, autoGiveUp, autoSelect);
    return JSON.stringify({ ok: result ? true : false, result: result });
  },
  setrespawnweapon: function(weaponId, weaponName) {
    if (!modules.weapon_giver) return JSON.stringify({ ok: false });
    var result = modules.weapon_giver.setrespawnweapon(weaponId, weaponName);
    return JSON.stringify({ ok: result });
  },
  clearrespawnweapon: function() {
    if (!modules.weapon_giver) return JSON.stringify({ ok: false });
    var result = modules.weapon_giver.clearrespawnweapon();
    return JSON.stringify({ ok: result });
  },
  battleRoundGetStatus: function() {
    if (!modules.battle_round_always) return JSON.stringify({ enabled: false, hookInstalled: false, currentIsBattleRound: -1 });
    return modules.battle_round_always.getStatus();
  }
};
"""

    def _build_init_message(self):
        return r"""
sendLog('info', '系统', '全功能整合包 Agent v1.8 已加载');
sendLog('info', '系统', '请先附加到游戏进程，然后开启对应功能');
sendLog('info', '系统', '架构: ' + Process.arch + ', 平台: ' + Process.platform);
setTimeout(function() { getGameAssembly(); }, 100);
"""

    def find_pid(self):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and 'unitycrossfire' in proc.info['name'].lower():
                    return proc.info['pid']
            except Exception:
                pass
        return None

    def connect(self, pid):
        """
        Connect to game process (called by GameSessionManager)
        
        Returns:
            True if connected successfully
            False with error category
            
        Error categories:
            - 'process_not_found': Process does not exist
            - 'process_terminating': Process is terminating (0xc000010a)
            - 'permission_denied': Access denied
            - 'architecture_mismatch': 32/64 bit mismatch
            - 'connection_failed': General connection failure
        """
        with self._lock:
            if self._connecting:
                return False, 'already_connecting'
            self._connecting = True

        session = None
        script = None
        
        try:
            # Attach to process
            try:
                session = frida.attach(pid)
            except frida.ProcessNotFoundError:
                return False, 'process_not_found'
            except frida.PermissionDeniedError:
                return False, 'permission_denied'
            except frida.TransportError as e:
                error_msg = str(e)
                if '0xc000010a' in error_msg or 'STATUS_PROCESS_IS_TERMINATING' in error_msg:
                    return False, 'process_terminating'
                if 'architecture' in error_msg.lower():
                    return False, 'architecture_mismatch'
                return False, 'connection_failed'
            
            # Create and load script
            js_code = self._build_js_code()
            script = session.create_script(js_code)
            script.on('message', self._on_message)
            script.load()

            # Success - update state
            self._session = session
            self._script = script
            self._pid = pid
            self._ready = True
            manifests = [
                manifest
                for manifest in ManifestLoader().load()
                if manifest.get("feature_id") in ORDINARY_PLUGIN_FEATURE_IDS
            ]
            self._script_manager = ScriptManager(
                session_manager=_FridaSessionAdapter(self),
                manifests=manifests,
                message_handler=self._on_message,
            )
            self._rpc_client = RpcClient(self._script_manager)

            return True, 'success'

        except Exception as e:
            # Clean up on failure
            if script:
                try:
                    script.unload()
                except Exception:
                    pass
            if session:
                try:
                    session.detach()
                except Exception:
                    pass
            
            error_msg = str(e)
            if '0xc000010a' in error_msg or 'STATUS_PROCESS_IS_TERMINATING' in error_msg:
                return False, 'process_terminating'
            
            return False, 'connection_failed'
            
        finally:
            self._connecting = False

    def disconnect(self):
        """Disconnect from game process"""
        with self._lock:
            if self._disconnecting:
                return
            self._disconnecting = True
            script = self._script
            session = self._session
            self._script = None
            self._session = None
            self._ready = False
            self._pid = None
            script_manager = self._script_manager
            self._script_manager = None
            self._rpc_client = None

        try:
            if script_manager:
                try:
                    script_manager.cleanup_all("python_disconnect")
                    log_to_file("info", "系统", "Plugin scripts cleaned up before Frida detach")
                except Exception as e:
                    log_to_file("warning", "系统", f"Plugin script cleanup failed: {e}")

            if script:
                try:
                    script.exports_sync.cleanup("python_disconnect")
                    log_to_file("info", "系统", "Frida JS cleanup completed before unload")
                except Exception as e:
                    log_to_file("warning", "系统", f"Frida JS cleanup failed before unload: {e}")

                try:
                    script.unload()
                    log_to_file("info", "系统", "Frida script unloaded")
                except Exception as e:
                    log_to_file("warning", "系统", f"Frida script unload failed: {e}")

            if session:
                try:
                    session.detach()
                    log_to_file("info", "系统", "Frida session detached")
                except Exception as e:
                    log_to_file("warning", "系统", f"Frida session detach failed: {e}")
        finally:
            with self._lock:
                self._disconnecting = False

    def send_toggle(self, feature, enable, extra_params=None):
        with self._lock:
            if self._disconnecting or not self._script:
                return
            try:
                msg = {'type': 'toggle', 'feature': feature, 'enable': enable}
                if extra_params:
                    msg.update(extra_params)
                self._script.post(msg)
            except Exception as e:
                self._event_bus.emit('log_message', level='error', module='System',
                                     message='Frida command failed, reconnect to the game and try again',
                                     audience='both',
                                     dev_detail=f'Frida send_toggle failed: {e}')

    def call_export(self, name, *args):
        with self._lock:
            if self._disconnecting or not self._script:
                return None
            try:
                fn = getattr(self._script.exports_sync, name)
                result = fn(*args)
                try:
                    return json.loads(result)
                except (json.JSONDecodeError, TypeError):
                    return result
            except (frida.InvalidOperationError, frida.TransportError):
                raise
            except Exception:
                return None

    def plugin_call(self, feature_id, action, payload=None):
        with self._lock:
            if self._disconnecting or not self._rpc_client:
                return None
            rpc_client = self._rpc_client
        try:
            return rpc_client.call(feature_id, action, payload)
        except Exception as e:
            self._event_bus.emit('log_message', level='error', module='Plugin',
                                 message=f'{feature_id} 调用失败',
                                 audience='both',
                                 dev_detail=f'Plugin RPC failed: {feature_id}.{action}: {e}')
            return None

    def plugin_cleanup_all(self, reason):
        with self._lock:
            script_manager = self._script_manager
        if not script_manager:
            return None
        return script_manager.cleanup_all(reason)

    def _on_message(self, msg, data):
        if msg['type'] != 'send':
            return
        payload = msg['payload']
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except (json.JSONDecodeError, TypeError):
                return

        msg_type = payload.get('type', '')

        if msg_type == 'log':
            self._event_bus.emit('log_message',
                                 level=payload.get('level', 'info'),
                                 module=payload.get('module', ''),
                                 message=payload.get('message', ''),
                                 audience=payload.get('audience', 'dev'),
                                 dev_detail=payload.get('dev_detail', ''))

        elif msg_type == 'log_file':
            self._event_bus.emit('log_message',
                                 level=payload.get('level', 'info'),
                                 module=payload.get('module', ''),
                                 message=payload.get('message', ''),
                                 audience=payload.get('audience', 'dev'),
                                 dev_detail=payload.get('dev_detail', ''))

        elif msg_type == 'status':
            self._event_bus.emit('feature_status_changed',
                                 feature=payload.get('feature', ''),
                                 enabled=payload.get('enabled', False))

        elif msg_type == 'gather_result':
            self._event_bus.emit('gather_result',
                                 data=payload.get('data', {}))

        elif msg_type == 'round_skipped':
            self._event_bus.emit('round_skipped',
                                 count=payload.get('count', 0),
                                 from_time=payload.get('from', ''))

        elif msg_type == 'giveWeaponResult':
            task_id = payload.get('taskId', 0)
            success = payload.get('success', False)
            if success:
                self._event_bus.emit('log_message', level='success', module='武器赋予',
                                     message='武器赋予执行成功',
                                     audience='both',
                                     dev_detail=f'WeaponGiver task #{task_id} succeeded')
            else:
                self._event_bus.emit('log_message', level='error', module='武器赋予',
                                     message='武器赋予执行失败，请稍后重试',
                                     audience='both',
                                     dev_detail=f'WeaponGiver task #{task_id} failed')

        elif msg_type == 'playerRespawned':
            self._event_bus.emit('log_message', level='info', module='武器赋予',
                                 message='检测到玩家复活',
                                 audience='dev',
                                 dev_detail='WeaponGiver detected local player respawn')

        elif msg_type == 'playerRespawnedWithWeapon':
            weapon_id = payload.get('weaponId', '')
            weapon_name = payload.get('weaponName', '')
            self._event_bus.emit('log_message', level='success', module='武器赋予',
                                 message=f'复活后已自动装备: {weapon_name}',
                                 audience='both',
                                 dev_detail=f'WeaponGiver respawn equipped weaponId={weapon_id}, weaponName={weapon_name}')

        elif msg_type.startswith('nano4t_'):
            self._event_bus.emit('nano4t_event',
                                 msg_type=msg_type,
                                 payload=payload)

        elif msg_type.startswith('battle_round_'):
            self._event_bus.emit('battle_round_event',
                                 msg_type=msg_type,
                                 payload=payload)

        elif msg_type == 'isbot_state':
            self._event_bus.emit('isbot_event',
                                 state=payload.get('state', 'off'),
                                 payload=payload)

    def restore_features(self, features_state):
        for feature_id, enabled in features_state.items():
            if enabled:
                self.send_toggle(feature_id, True)
