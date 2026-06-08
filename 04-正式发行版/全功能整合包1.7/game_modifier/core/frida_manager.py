import threading
import json
import os

import frida
import psutil

from core.config import SCRIPTS_DIR
from core.event_bus import EventBus


class FridaManager:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self._session = None
        self._script = None
        self._ready = False
        self._connecting = False
        self._pid = None
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

    if (featureName === 'knife_speed') {
      if (modules.knife) modules.knife.setSpeed(enable);
    } else if (featureName === 'movespeed_speed') {
      if (modules.movespeed) modules.movespeed.setSpeed(enable);
    } else if (featureName === 'gravity_config') {
      if (modules.gravity) modules.gravity.setconfig(enable.g, enable.j, enable.m);
    } else if (featureName === 'timescale_speed') {
      if (modules.timescale) modules.timescale.setSpeed(enable);
    } else if (featureName === 'timescale') {
      // 特殊处理：enable 时通过 data.speed 传递倍速，避免竞态
      if (modules.timescale) {
        if (enable) {
          var speed = (typeof data.speed === 'number') ? data.speed : 1.0;
          modules.timescale.setSpeed(speed);
          modules.timescale.enable();
        } else {
          modules.timescale.disable();
        }
      }
    } else if (featureName === 'range_config') {
      if (modules.range) modules.range.setRange(enable);
    } else if (featureName === 'nano4t_init') {
      if (modules.nano4t) modules.nano4t.init();
    } else if (featureName === 'nano4t_set') {
      if (modules.nano4t) modules.nano4t.set(enable.g, enable.h);
    } else if (featureName === 'roundskip_skip') {
      if (modules.roundskip) { modules.roundskip.enable(); modules.roundskip.skipround(); }
    } else if (featureName === 'gather_trigger') {
      if (modules.gather) modules.gather.gather();
    } else if (modules[featureName]) {
      var actionText = enable ? '已开启' : '已关闭';
      sendLog('success', '系统', featureName + ' ' + actionText);
      if (enable) {
        modules[featureName].enable();
      } else {
        modules[featureName].disable();
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
  gather: function() {
    if (!modules.gather) return JSON.stringify({ ok: false, msg: '聚怪模块未加载' });
    var result = modules.gather.gather();
    send(JSON.stringify({ type: 'gather_result', data: result }));
    return JSON.stringify(result);
  },
  setGravityConfig: function(g, j, m) {
    if (!modules.gravity) return JSON.stringify({ ok: false });
    return JSON.stringify(modules.gravity.setconfig(g, j, m));
  },
  resetGravity: function() {
    if (!modules.gravity) return JSON.stringify({ ok: false });
    return JSON.stringify(modules.gravity.resetall());
  },
  getGravityStatus: function() {
    if (!modules.gravity) return JSON.stringify({ enabled: false });
    return JSON.stringify(modules.gravity.getstatus());
  },
  roundskip: function() {
    if (!modules.roundskip) return JSON.stringify({ ok: false, reason: 'module_not_loaded' });
    modules.roundskip.enable();
    return JSON.stringify(modules.roundskip.skipround());
  },
  getRoundStatus: function() {
    if (!modules.roundskip) return JSON.stringify({ ok: false });
    modules.roundskip.enable();
    return JSON.stringify(modules.roundskip.getstatus());
  },
  resetRound: function() {
    if (!modules.roundskip) return JSON.stringify({ ok: false });
    return JSON.stringify(modules.roundskip.reset());
  },
  setRange: function(multiplier) {
    if (!modules.range) return JSON.stringify({ ok: false });
    modules.range.setRange(multiplier);
    return JSON.stringify({ ok: true });
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
  }
};
"""

    def _build_init_message(self):
        return r"""
sendLog('info', '系统', '游戏修改器 Agent v1.7 已加载');
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
        try:
            if self._script:
                self._script.unload()
                self._script = None
            if self._session:
                self._session.detach()
                self._session = None
        except Exception:
            pass
        
        self._ready = False
        self._pid = None  # Clear PID on disconnect

    def send_toggle(self, feature, enable, extra_params=None):
        if not self._script:
            return
        try:
            msg = {'type': 'toggle', 'feature': feature, 'enable': enable}
            if extra_params:
                msg.update(extra_params)
            self._script.post(msg)
        except Exception as e:
            self._event_bus.emit('log_message', level='error', module='系统',
                                 message=f'发送指令失败: {e}')

    def call_export(self, name, *args):
        if not self._script:
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
        except Exception as e:
            return None

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
                                 message=payload.get('message', ''))

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
                                     message=f'赋予武器任务 #{task_id} 执行成功')
            else:
                self._event_bus.emit('log_message', level='error', module='武器赋予',
                                     message=f'赋予武器任务 #{task_id} 执行失败')

        elif msg_type == 'playerRespawned':
            self._event_bus.emit('log_message', level='info', module='武器赋予',
                                 message='检测到玩家复活')

        elif msg_type == 'playerRespawnedWithWeapon':
            weapon_id = payload.get('weaponId', '')
            weapon_name = payload.get('weaponName', '')
            self._event_bus.emit('log_message', level='success', module='武器赋予',
                                 message=f'复活自动装备武器: {weapon_name} (ID: {weapon_id})')

        elif msg_type.startswith('nano4t_'):
            self._event_bus.emit('nano4t_event',
                                 msg_type=msg_type,
                                 payload=payload)

    def restore_features(self, features_state):
        for feature_id, enabled in features_state.items():
            if enabled:
                self.send_toggle(feature_id, True)
