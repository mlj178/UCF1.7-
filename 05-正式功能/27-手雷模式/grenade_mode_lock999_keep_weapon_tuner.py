# -*- coding: utf-8 -*-
"""
feature_id: grenade_mode_lock999_keep_weapon_tuner
version: 2.12.4

基于 lock999_keep_weapon v1.1：
- 锁定手雷数量 999
- 保护当前 WPN_Throw 对象不被 Remove 删除
- 新增 UI 开关/滑块：伤害、爆炸范围、飞行速度
- v1.3 删除：距离衰减、穿墙、碰撞爆炸
- v1.3 增加：CreateExplosion 参数级 damage/range 修改
- v1.4 新增：连投就绪开关 throwReady=1
- v1.4 新增：投掷动作加速 Animator.speed
- v1.5 新增：伤害/范围/飞行速度滑块即时生效
- v1.5 调整：伤害/范围/飞行速度 UI 显示值缩小 10 倍，实际写入值不变
- v1.5 调整：投掷动作加速最大值提高到 10
- v2.0 新增：VirtualGrenadeMode Observer，只观察 PlayerWeapons 切枪链路，不拦截
- v2.1 新增：无限手雷作用范围下拉框，支持只对玩家或所有人/bot
- v2.1 新增：Bot 手雷行为观察，先统计 bot 是否拥有/选择/投掷手雷
- v2.2 新增：Bot 攻击入口观察，记录 WPN_Gun/WPN_RPG 的 BotControl 与 Fire/GunShoot 链路
- v2.3 新增：Bot 只允许手雷手雷模式，记录 bot 手雷并纠正回 slot=3
- v2.4 新增：Bot 切枪入口强重定向，Select/SetCurrentWeapon onEnter 直接改成 slot=3 手雷
- v2.5 新增：BotGrenadeRecord，只允许普通 Grenade，主控 Bot.SelectWeapon + GetValidSlot，GiveWeapon 可选拦截非手雷
- v2.5.1 修复：彻底禁用旧入口重定向，避免 RangeError 自动关闭，恢复玩家锁999稳定性
- v2.6 新增：Bot.UseWeapon 投掷驱动，按冷却调用 WPN_Throw.Throw，让bot真正扔手雷
- v2.7 新增：VirtualBotControl，在WPN_Gun/RPG BotControl层接管并转手雷Throw
- v2.10.3 调整：删除v2.10.2可见性强化内容；Bot手雷模式UI默认开启；AI驱动冷却默认1000ms
- v2.10.4 新增：Bot投掷状态机，IDLE/SELECTING/READY/THROWING/COOLDOWN
- v2.11.0 调整：默认不再阻止Bot获得非Grenade武器，保留官方武器/模型/动作状态，减少木桩、空枪、聚堆
- v2.11.1 调整：修正UI仍默认拦截非Grenade发枪的问题；伤害/爆炸范围/飞行速度新增应用对象下拉框并即时生效
- v2.11.2 调整：官方选武器优先，默认关闭Bot.SelectWeapon/GetValidSlot全局强制slot=3；仅状态机投掷阶段临时Select(3)
- v2.11.3 调整：伤害/范围/速度作用对象改为my_player/all_players；默认禁止Bot枪械原BotControl开火
- v2.11.4 新增：Bot出生/首次识别保护时间与attackTarget稳定时间，避免刚出生马上扔雷
- v2.11.5 修复：统一Bot投掷许可层，拦截AI状态机/Bot.UseWeapon/VirtualBotControl/底层Throw驱动所有路径
- v2.11.6 修复：复活/重新发枪时重置Bot生命周期，让后续复活也重新触发出生保护
- v2.12.0 终版清理：删除旧重定向/手雷模式纠正/全局选雷/GetValidSlot强制/发枪拦截/旧局部出生保护等失败方案
- v2.12.1 精简：删除死统计、UpdateAction残留、SmartAI/v2.10.1路径/距离/抛物线实验残留，并统一命名
- v2.12.2 UI清理：删除界面和启动说明里的v2.10/v2.10.1 SmartAI实验文案
- v2.12.3 修复：删除_collect_config中残留的旧距离参数旧距离配置，修复开启失败
- 只改 WPN_Throw.<Throw>b__10_0 捕获到的 missile
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional
import datetime as _dt
import json
import logging
import queue
import threading
import time
import traceback

FEATURE_ID = "grenade_mode_lock999_keep_weapon_tuner"
VERSION = "2.12.4"
DISPLAY_NAME = "手雷模式v2观察版 + 锁999保护"
SCRIPT_NAME = "grenade_mode_lock999_keep_weapon_tuner.js"
PROCESS_NAME = "UnityCrossFire.exe"

DISPLAY_SCALE: Dict[str, float] = {
    # UI 显示值缩小 10 倍，实际写入值 = UI显示值 * 10
    "damage_value": 10.0,
    "range_value": 10.0,
    "shoot_speed_value": 10.0,
}

DEFAULT_CONFIG: Dict[str, Any] = {
    "lock999_enabled": True,
    "infinite_grenade_scope": "all_players",
    "target_count": 999,
    "sync_plain_value": False,
    "force_throw_ready_enabled": False,
    "force_throw_ready_value": True,
    "force_throw_ready_on_throw_leave": True,
    "force_throw_ready_on_deploy": True,
    "force_throw_ready_on_animation_end": True,
    "throw_anim_speed_enabled": False,
    "throw_anim_speed_value": 1.6,
    "throw_anim_speed_restore_value": 1.0,
    "throw_anim_speed_restore_on_end": True,
    "lock_on_throw_enter": True,
    "lock_on_throw_leave": True,
    "lock_on_deploy": True,
    "lock_on_unDeploy": True,
    "lock_on_animation_end": True,
    "lock_on_init": True,
    "lock_on_generate_from_owner": True,
    "protect_weapon_remove": True,
    "protect_ttl_ms": 5000,
    "max_protected_weapons": 64,
    "runtime_tuner_enabled": True,
    "owner_filter": "local_only",
    "missile_ttl_ms": 8000,
    "max_tracked_missiles": 128,
    "enable_damage": True,
    "damage_value": 999.0,
    "damage_apply_scope": "my_player",
    "enable_range": True,
    "range_value": 10.0,
    "range_apply_scope": "my_player",
    "enable_shoot_speed": True,
    "shoot_speed_value": 35.0,
    "shoot_speed_apply_scope": "my_player",
    "tune_on_capture": True,
    "tune_on_set_missile_data": True,
    "tune_on_try_explosion": True,
    "tune_on_damage": True,
    "tune_on_life_timer_end": True,
    "tune_on_work": True,
    "tune_on_fixed_update": True,
    "virtual_grenade_observer_enabled": True,
    "virtual_grenade_observer_verbose": True,
    "bot_grenade_behavior_observer_enabled": True,
    "bot_attack_observer_enabled": True,
    "bot_grenade_mode_enabled": True,
    "bot_grenade_throw_slot": 3,
    "bot_grenade_force_scope_all_players": True,
    "bot_grenade_record_enabled": True,
    "virtual_grenade_giveweapon_enabled": True,
    "virtual_grenade_preserve_original_weapons": True,
    "virtual_grenade_log_interval_ms": 1000,
    "bot_throw_drive_enabled": True,
    "bot_throw_drive_useweapon_enabled": True,
    "bot_throw_drive_skip_original_useweapon_on_success": True,
    "bot_throw_drive_cooldown_ms": 2500,
    "bot_throw_drive_force_ready": True,
    "bot_throw_drive_lock_before_after": True,
    "bot_throw_drive_log_interval_ms": 1000,
    "virtual_botcontrol_enabled": True,
    "virtual_botcontrol_replace_botcontrol": True,
    "virtual_botcontrol_gun_enabled": True,
    "virtual_botcontrol_sniper_enabled": True,
    "virtual_botcontrol_rpg_enabled": True,
    "virtual_botcontrol_skip_original_on_success": True,
    "bot_suppress_gun_fire_enabled": True,
    "bot_suppress_gun_fire_when_no_grenade": True,
    "virtual_botcontrol_log_interval_ms": 1000,
    "bot_ai_probe_enabled": True,
    "bot_ai_probe_verbose": True,
    "bot_ai_hook_drive_enabled": True,
    "bot_ai_checkattack_drive_enabled": True,
    "bot_ai_camerarotation_drive_enabled": True,
    "bot_ai_trysettarget_drive_enabled": False,
    "bot_ai_hook_drive_require_target": True,
    "bot_ai_hook_drive_cooldown_ms": 1000,
    "bot_throw_state_machine_enabled": True,
    "bot_throw_state_select_delay_ms": 80,
    "bot_throw_state_ready_delay_ms": 0,
    "bot_throw_state_timeout_ms": 1200,
    "bot_throw_state_log_interval_ms": 500,
    "bot_throw_unified_gate_enabled": True,
    "bot_throw_spawn_grace_enabled": True,
    "bot_throw_spawn_grace_ms": 3000,
    "bot_throw_target_stable_enabled": True,
    "bot_throw_target_stable_ms": 700,
    "bot_throw_first_throw_extra_delay_ms": 1000,
    "bot_throw_respawn_reset_enabled": True,
    "bot_throw_respawn_reset_on_removeall": True,
    "bot_throw_respawn_reset_on_giveweapon": True,
    "bot_throw_respawn_reset_on_grenade_change": True,
    "bot_throw_respawn_reset_cooldown_ms": 1500,
    "smart_grenade_ai_enabled": True,
    "smart_grenade_require_official_visible": True,
    "smart_grenade_recent_visible_ms": 350,
    "bot_ai_probe_log_interval_ms": 1000,
    "bot_attack_summary_interval_ms": 5000,
    "bot_grenade_summary_interval_ms": 5000,
    "observe_set_current_weapon": True,
    "log_interval_ms": 1000,
    "max_error_before_disable": 14,
}

@dataclass
class CombinedFeature:
    frida_manager: Any
    logger: Any = None
    config: Dict[str, Any] = field(default_factory=lambda: dict(DEFAULT_CONFIG))
    feature_id: str = FEATURE_ID
    display_name: str = DISPLAY_NAME
    script_name: str = SCRIPT_NAME
    enabled: bool = False

    def _call_export(self, export_name: str, *args: Any) -> Any:
        manager = self.frida_manager
        if hasattr(manager, "call_export"):
            try:
                return manager.call_export(self.feature_id, export_name, *args)
            except TypeError:
                return manager.call_export(export_name, *args)
        script = getattr(manager, "script", None) or manager
        exports_sync = getattr(script, "exports_sync", None)
        if exports_sync is not None:
            fn = getattr(exports_sync, export_name, None)
            if fn is None and export_name == "set_config":
                fn = getattr(exports_sync, "setConfig", None)
            if fn is not None:
                return fn(*args)
        exports = getattr(script, "exports", None)
        if exports is not None:
            fn = getattr(exports, export_name, None)
            if fn is None and export_name == "set_config":
                fn = getattr(exports, "setConfig", None)
            if fn is not None:
                return fn(*args)
        raise AttributeError(f"cannot call RPC export: {export_name}")

    def set_config(self, config: Optional[Dict[str, Any]] = None) -> bool:
        if config:
            self.config.update({k: v for k, v in config.items() if k in DEFAULT_CONFIG})
        return bool(self._call_export("set_config", dict(self.config)))

    def enable(self, config: Optional[Dict[str, Any]] = None) -> Any:
        self.set_config(config)
        result = self._call_export("enable")
        self.enabled = True
        return result

    def disable(self) -> Any:
        try:
            return self._call_export("disable")
        finally:
            self.enabled = False

    def status(self) -> Dict[str, Any]:
        status = self._call_export("status")
        if not isinstance(status, dict):
            status = {"raw": status}
        self.enabled = bool(status.get("enabled", self.enabled))
        return status

    def cleanup(self) -> Any:
        try:
            return self._call_export("cleanup")
        finally:
            self.enabled = False

Feature = CombinedFeature

class PersistentLogger:
    def __init__(self, base_dir: Optional[Path] = None) -> None:
        self.base_dir = base_dir or Path(__file__).resolve().parent
        self.log_dir = self.base_dir / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        ts = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"{FEATURE_ID}_{ts}.log.txt"
        self.latest_file = self.log_dir / f"{FEATURE_ID}_latest.log.txt"
        self._lock = threading.RLock()
        self._logger = logging.getLogger(f"{FEATURE_ID}_{ts}")
        self._logger.setLevel(logging.INFO)
        self._logger.propagate = False
        for path, mode in [(self.log_file, "a"), (self.latest_file, "w")]:
            handler = logging.FileHandler(path, encoding="utf-8", mode=mode)
            handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
            self._logger.addHandler(handler)
        self.info("=" * 80)
        self.info(f"{DISPLAY_NAME} {FEATURE_ID} v{VERSION}")
        self.info(f"日志文件={self.log_file}")
        self.info(f"最新日志={self.latest_file}")
        self.info("=" * 80)

    def info(self, message: str) -> None:
        with self._lock:
            self._logger.info(message)
    def warning(self, message: str) -> None:
        with self._lock:
            self._logger.warning(message)
    def error(self, message: str) -> None:
        with self._lock:
            self._logger.error(message)
    def exception(self, message: str) -> None:
        with self._lock:
            self._logger.error(message)
            self._logger.error(traceback.format_exc())
    def json_line(self, prefix: str, data: Any, level: str = "INFO") -> None:
        text = prefix + " " + json.dumps(data, ensure_ascii=False, default=str)
        if level == "ERROR": self.error(text)
        elif level == "WARN": self.warning(text)
        else: self.info(text)

class StandaloneFridaManager:
    def __init__(self, logger: PersistentLogger, process_name: str = PROCESS_NAME) -> None:
        self.logger = logger
        self.process_name = process_name
        self.script_path = Path(__file__).resolve().parent / SCRIPT_NAME
        self.session: Any = None
        self.script: Any = None
        self.pid: Optional[int] = None
        self.message_queue: "queue.Queue[str]" = queue.Queue()
        self.connected = False

    def find_pid(self) -> Optional[int]:
        try:
            import psutil  # type: ignore
        except ImportError as exc:
            raise RuntimeError("缺少 psutil，请先执行：pip install psutil") from exc
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if proc.info.get("name") == self.process_name:
                    return int(proc.info["pid"])
            except Exception:
                continue
        return None

    def is_process_alive(self) -> bool:
        if self.pid is None: return False
        try:
            import psutil  # type: ignore
            return psutil.pid_exists(self.pid)
        except Exception:
            return False

    def attach_and_load(self) -> None:
        try:
            import frida  # type: ignore
        except ImportError as exc:
            raise RuntimeError("缺少 frida，请先执行：pip install frida") from exc
        if not self.script_path.exists():
            raise FileNotFoundError(f"找不到 JS 文件：{self.script_path}")
        pid = self.find_pid()
        if pid is None:
            raise RuntimeError(f"未找到进程：{self.process_name}")
        source = self.script_path.read_text(encoding="utf-8")
        self.logger.info(f"[Frida] 连接进程={self.process_name}, PID={pid}")
        self.logger.info(f"[Frida] 加载脚本={self.script_path}")
        self.session = frida.attach(pid)
        self.script = self.session.create_script(source)
        self.script.on("message", self._on_message)
        self.script.load()
        self.pid = pid
        self.connected = True
        self.logger.info("[Frida] 脚本加载完成")

    def _on_message(self, message: Dict[str, Any], data: Any) -> None:
        msg_type = message.get("type")
        if msg_type == "send":
            payload = message.get("payload")
            level = payload.get("level", "INFO") if isinstance(payload, dict) else "INFO"
            self.logger.json_line("[JS]", payload, level="ERROR" if level == "ERROR" else ("WARN" if level == "WARN" else "INFO"))
            try:
                if isinstance(payload, dict):
                    msg = payload.get("message", "")
                    pdata = payload.get("data", {})
                    if msg == "手雷数量已锁定并保护武器对象":
                        before = pdata.get("before", {})
                        after = pdata.get("after", {})
                        ui_text = f"[锁999+保护] {before.get('value')} -> {after.get('value')}"
                    elif msg == "已阻止删除当前手雷武器对象":
                        ui_text = f"[保护Remove] weapon={pdata.get('weapon')} blocked={pdata.get('blocked')}"
                    elif msg == "已捕获 WPN_Throw 生成的 missile":
                        ui_text = f"[捕获手雷missile] {pdata.get('missile')} owner_allowed={pdata.get('owner_allowed')}"
                    elif msg == "已修改手雷 missile 运行时字段":
                        ui_text = f"[字段修改] writes={pdata.get('writes')} reason={pdata.get('reason')}"
                    elif msg == "已修改 CreateExplosion 参数":
                        ui_text = f"[Create参数] damage {pdata.get('damage_before')} -> {pdata.get('damage_after')} range {pdata.get('range_before')} -> {pdata.get('range_after')}"
                    elif msg == "已修改手雷 missile 飞行速度":
                        ui_text = f"[速度] {pdata.get('before')} -> {pdata.get('after')}"
                    elif msg == "连投就绪开关已写入 throwReady":
                        ui_text = f"[连投就绪] throwReady {pdata.get('before')} -> {pdata.get('after')}"
                    elif msg == "投掷动作加速已设置 Animator.speed":
                        ui_text = f"[动作加速] speed={pdata.get('speed')}"
                    elif msg == "投掷动作加速已恢复 Animator.speed":
                        ui_text = f"[动作恢复] speed={pdata.get('restore_value')}"
                    elif msg == "VirtualGrenadeMode观察":
                        wi = pdata.get("weaponInfo") or {}
                        slot = pdata.get("slot", "")
                        ui_text = f"[模式观察] {pdata.get('name')} slot={slot} weapon={wi.get('weapon')} class={wi.get('className')} my={wi.get('isMyWeapon')}"
                    elif msg == "Bot手雷行为观察":
                        ui_text = f"[Bot观察] {pdata.get('name')} class={pdata.get('className')} weapon={pdata.get('weapon')}"
                    elif msg == "Bot手雷行为汇总":
                        ui_text = f"[Bot汇总] seen={pdata.get('bot_throw_weapon_seen')} selected={pdata.get('bot_throw_weapon_selected')} throw={pdata.get('bot_throw_method_hits')} missile={pdata.get('bot_missile_captured')}"
                    elif msg == "Bot攻击入口观察":
                        wi = pdata.get("weaponInfo") or {}
                        ui_text = f"[攻击观察] {pdata.get('name')} class={wi.get('className')} my={wi.get('isMyWeapon')} botLike={pdata.get('botLike')}"
                    elif msg == "Bot攻击入口汇总":
                        ui_text = f"[攻击汇总] gunBot={pdata.get('gun_bot_control_hits')} gunShootBot={pdata.get('gun_shoot_botlike_hits')} rpgBot={pdata.get('rpg_bot_control_hits')} throw={pdata.get('bot_throw_method_hits')}"
                    elif msg == "Bot手雷记录":
                        ui_text = f"[手雷模式记录] owner={pdata.get('owner')} grenade={pdata.get('grenadeWeapon')} class={pdata.get('className')}"
                    elif msg == "Bot手雷手雷模式纠正":
                        ui_text = f"[手雷模式纠正] owner={pdata.get('owner')} grenade={pdata.get('grenadeWeapon')} calls={pdata.get('calls')}"
                    elif msg == "Bot手雷入口重定向":
                        ui_text = f"[入口重定向] {pdata.get('oldClass')} -> grenade={pdata.get('grenadeWeapon')} success={pdata.get('success')}"
                    elif msg == "Bot手雷重定向跳过":
                        ui_text = f"[重定向跳过] {pdata.get('targetClass')} {pdata.get('note')}"
                    elif msg == "Bot手雷入口重定向失败":
                        ui_text = f"[重定向失败] {pdata.get('reason')} err={pdata.get('error')}"
                    elif msg == "Bot手雷模式自动切换作用范围":
                        ui_text = f"[作用范围] 自动切到 {pdata.get('infinite_grenade_scope')}"
                    elif msg == "BotGrenadeRecord.GetValidSlot":
                        ui_text = f"[VGL槽位] {pdata.get('oldSlot')} -> {pdata.get('newSlot')} forced={pdata.get('forced')}"
                    elif msg == "BotGrenadeRecord强制Bot选手雷":
                        ui_text = f"[VGL选手雷] grenade={pdata.get('grenadeWeapon')} ret={pdata.get('selectReturn')} forced={pdata.get('forced')}"
                    elif msg == "BotGrenadeRecord.GiveWeapon":
                        ui_text = f"[VGL发枪] idx={pdata.get('weaponIndex')} class={pdata.get('className')} block={pdata.get('block')}"
                    elif msg == "BotGrenadeRecord跳过":
                        ui_text = f"[VGL跳过] {pdata.get('note')}"
                    elif msg == "Bot投掷驱动成功":
                        ui_text = f"[投掷驱动] grenade={pdata.get('grenadeWeapon')} success={pdata.get('success')}"
                    elif msg == "Bot投掷驱动跳过":
                        ui_text = f"[投掷跳过] {pdata.get('note')}"
                    elif msg == "Bot投掷驱动失败":
                        ui_text = f"[投掷失败] {pdata.get('reason')} err={pdata.get('error')}"
                    elif msg == "Bot投掷驱动就绪":
                        ui_text = f"[投掷就绪] grenade={pdata.get('grenadeWeapon')} ready {pdata.get('before')}->{pdata.get('after')}"
                    elif msg == "VirtualBotControl投掷接管成功":
                        ui_text = f"[VBC接管] {pdata.get('name')} success={pdata.get('success')}"
                    elif msg == "VirtualBotControl未接管":
                        ui_text = f"[VBC未接管] {pdata.get('name')} {pdata.get('note')}"
                    elif msg == "BotAI观察":
                        bai = pdata.get("botAI") or {}
                        ui_text = f"[AI] {pdata.get('name')} target={bai.get('attackTarget')} grenade={bai.get('hasGrenadeRecord')}"
                    elif msg == "BotAI.UpdateAction投掷驱动成功":
                        ui_text = f"[AI投掷] target={pdata.get('attackTarget')} success={pdata.get('success')}"
                    elif msg == "BotAI触发投掷成功":
                        se = pdata.get("smartEval") or {}
                        ui_text = f"[AI触发投掷] {pdata.get('name')} success={pdata.get('success')} target={pdata.get('attackTarget')} dist={se.get('distanceXZ')}"
                    elif msg == "Bot投掷状态机":
                        ui_text = f"[投掷状态机] {pdata.get('state')} bot={pdata.get('bot')} target={pdata.get('attackTarget')}"
                    elif msg == "Bot投掷保护跳过":
                        ui_text = f"[投掷保护] {pdata.get('reason')} age={pdata.get('ageMs')} targetAge={pdata.get('targetAgeMs')}"
                    elif msg == "Bot统一投掷许可拦截":
                        ui_text = f"[统一许可拦截] {pdata.get('blockReason')} age={pdata.get('ageMs')} need={pdata.get('needMs')}"
                    elif msg == "Bot生命周期首次识别":
                        ui_text = f"[Bot首次识别] key={pdata.get('key')} grace={pdata.get('spawn_grace_ms')}"
                    elif msg == "Bot生命周期已重置":
                        ui_text = f"[复活重置] {pdata.get('reason')} count={pdata.get('respawnCount')}"
                    elif msg == "SmartGrenadeAI跳过":
                        ui_text = f"[SmartAI跳过] {pdata.get('name')} reason={pdata.get('reason')}"
                    elif msg == "BotAI触发投掷跳过":
                        ui_text = f"[AI投掷跳过] {pdata.get('name')} {pdata.get('note')}"
                    elif msg == "Bot手雷手雷模式跳过":
                        ui_text = f"[手雷模式跳过] {pdata.get('reason')} {pdata.get('note')}"
                    elif msg == "Bot手雷手雷模式失败":
                        ui_text = f"[手雷模式失败] {pdata.get('reason')} err={pdata.get('error')}"
                    elif msg == "跳过非作用范围内的手雷武器":
                        ui_text = f"[范围跳过] scope={pdata.get('scope')} weapon={pdata.get('weapon')} isMy={pdata.get('isMyWeapon')}"
                    else:
                        ui_text = f"[JS] {msg}"
                else:
                    ui_text = f"[JS] {payload}"
                self.message_queue.put(ui_text)
            except Exception:
                self.message_queue.put(str(payload))
            return
        if msg_type == "error":
            self.logger.json_line("[JS错误]", message, level="ERROR")
            desc = message.get("description") or "JS错误"
            stack = message.get("stack") or ""
            self.message_queue.put(f"[JS错误] {desc}\n{stack}")
            return
        self.logger.json_line("[JS消息]", message)
        self.message_queue.put(f"[JS消息] {message}")

    def call_export(self, feature_id: str, export_name: str, *args: Any) -> Any:
        if feature_id != FEATURE_ID:
            raise ValueError(f"未知 feature_id: {feature_id}")
        if self.script is None:
            raise RuntimeError("Frida 脚本尚未加载")
        exports_sync = getattr(self.script, "exports_sync", None)
        if exports_sync is not None:
            fn = getattr(exports_sync, export_name, None)
            if fn is None and export_name == "set_config": fn = getattr(exports_sync, "setConfig", None)
            if fn is None: raise AttributeError(f"JS 缺少 RPC：{export_name}")
            return fn(*args)
        exports = getattr(self.script, "exports", None)
        if exports is not None:
            fn = getattr(exports, export_name, None)
            if fn is None and export_name == "set_config": fn = getattr(exports, "setConfig", None)
            if fn is None: raise AttributeError(f"JS 缺少 RPC：{export_name}")
            return fn(*args)
        raise RuntimeError("当前 frida 版本没有可用 exports 接口")

    def detach(self) -> None:
        self.logger.info("[Frida] 请求断开")
        try:
            if self.script is not None:
                try: self.script.unload(); self.logger.info("[Frida] 脚本已卸载")
                except Exception as exc: self.logger.warning(f"[Frida] 脚本卸载失败：{exc}")
        finally:
            self.script = None
        try:
            if self.session is not None:
                try: self.session.detach(); self.logger.info("[Frida] 会话已断开")
                except Exception as exc: self.logger.warning(f"[Frida] 会话断开失败：{exc}")
        finally:
            self.session = None
            self.pid = None
            self.connected = False

class CombinedApp:
    def __init__(self) -> None:
        try:
            import customtkinter as ctk  # type: ignore
        except ImportError as exc:
            raise RuntimeError("缺少 customtkinter，请先执行：pip install customtkinter") from exc
        self.ctk = ctk
        self.base_dir = Path(__file__).resolve().parent
        self.logger = PersistentLogger(self.base_dir)
        self.manager = StandaloneFridaManager(self.logger)
        self.feature: Optional[CombinedFeature] = None
        self.closing = False
        self.last_ui_line: Dict[str, float] = {}
        self.last_status_log_time = 0.0
        self.live_apply_job = None
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root = ctk.CTk()
        self.root.title(f"{DISPLAY_NAME} v{VERSION}")
        self.root.geometry("1180x880")
        self.status_var = ctk.StringVar(value="未连接：等待游戏启动")
        self.log_path_var = ctk.StringVar(value=str(self.logger.latest_file))
        self.auto_enable_var = ctk.BooleanVar(value=False)
        self.enabled_var = ctk.BooleanVar(value=False)
        self.lock999_var = ctk.BooleanVar(value=True)
        self.infinite_scope_var = ctk.StringVar(value="all_players")
        self.protect_remove_var = ctk.BooleanVar(value=True)
        self.runtime_tuner_var = ctk.BooleanVar(value=True)
        self.virtual_observer_var = ctk.BooleanVar(value=True)
        self.bot_behavior_observer_var = ctk.BooleanVar(value=True)
        self.bot_attack_observer_var = ctk.BooleanVar(value=True)
        self.bot_grenade_mode_var = ctk.BooleanVar(value=True)
        self.vg_giveweapon_var = ctk.BooleanVar(value=True)
        self.bot_throw_drive_var = ctk.BooleanVar(value=True)
        self.bot_throw_drive_useweapon_var = ctk.BooleanVar(value=True)
        self.bot_throw_drive_skip_original_var = ctk.BooleanVar(value=True)
        self.bot_throw_drive_cooldown_var = ctk.StringVar(value="2500")
        self.vbc_enabled_var = ctk.BooleanVar(value=True)
        self.vbc_gun_var = ctk.BooleanVar(value=True)
        self.vbc_sniper_var = ctk.BooleanVar(value=True)
        self.vbc_rpg_var = ctk.BooleanVar(value=True)
        self.vbc_skip_original_var = ctk.BooleanVar(value=True)
        self.bot_suppress_gun_fire_var = ctk.BooleanVar(value=True)
        self.bot_suppress_gun_no_grenade_var = ctk.BooleanVar(value=True)
        self.bot_ai_probe_var = ctk.BooleanVar(value=True)
        self.bot_ai_hook_drive_var = ctk.BooleanVar(value=True)
        self.bot_ai_checkattack_drive_var = ctk.BooleanVar(value=True)
        self.bot_ai_camera_drive_var = ctk.BooleanVar(value=True)
        self.bot_ai_tryset_drive_var = ctk.BooleanVar(value=False)
        self.bot_ai_require_target_var = ctk.BooleanVar(value=True)
        self.bot_ai_cooldown_var = ctk.StringVar(value="1000")
        self.bot_throw_sm_var = ctk.BooleanVar(value=True)
        self.bot_throw_sm_select_delay_var = ctk.StringVar(value="80")
        self.bot_throw_sm_timeout_var = ctk.StringVar(value="1200")
        self.bot_spawn_grace_var = ctk.BooleanVar(value=True)
        self.bot_spawn_grace_ms_var = ctk.StringVar(value="3000")
        self.bot_target_stable_var = ctk.BooleanVar(value=True)
        self.bot_target_stable_ms_var = ctk.StringVar(value="700")
        self.bot_first_extra_delay_var = ctk.StringVar(value="1000")
        self.bot_respawn_reset_var = ctk.BooleanVar(value=True)
        self.bot_respawn_reset_cd_var = ctk.StringVar(value="1500")
        self.smart_ai_enabled_var = ctk.BooleanVar(value=True)
        self.smart_ai_official_visible_var = ctk.BooleanVar(value=True)
        self.sync_plain_var = ctk.BooleanVar(value=False)
        self.force_ready_var = ctk.BooleanVar(value=False)
        self.anim_speed_enabled_var = ctk.BooleanVar(value=False)
        self.anim_speed_var = ctk.DoubleVar(value=1.6)
        self.anim_speed_text_var = ctk.StringVar(value="1.6")
        self.target_count_var = ctk.StringVar(value="999")
        self.owner_filter_var = ctk.StringVar(value="local_only")
        self.damage_enabled_var = ctk.BooleanVar(value=True)
        self.range_enabled_var = ctk.BooleanVar(value=True)
        self.speed_enabled_var = ctk.BooleanVar(value=True)
        self.damage_var = ctk.DoubleVar(value=99.9)
        self.range_var = ctk.DoubleVar(value=1.0)
        self.speed_var = ctk.DoubleVar(value=3.5)
        self.damage_text_var = ctk.StringVar(value="99.9")
        self.range_text_var = ctk.StringVar(value="1.0")
        self.speed_text_var = ctk.StringVar(value="3.5")
        self.damage_scope_var = ctk.StringVar(value="my_player")
        self.range_scope_var = ctk.StringVar(value="my_player")
        self.speed_scope_var = ctk.StringVar(value="my_player")
        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _build_ui(self) -> None:
        ctk = self.ctk
        ctk.CTkLabel(self.root, text=f"{DISPLAY_NAME}  {FEATURE_ID}  v{VERSION}", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(14, 4))
        ctk.CTkLabel(self.root, textvariable=self.status_var).pack(pady=(0, 6))
        ctk.CTkLabel(self.root, textvariable=self.log_path_var, font=ctk.CTkFont(size=12)).pack(pady=(0, 8))
        top = ctk.CTkFrame(self.root); top.pack(fill="x", padx=14, pady=8)
        ctk.CTkButton(top, text="立即连接游戏", command=self.connect_now).pack(side="left", padx=6, pady=8)
        ctk.CTkButton(top, text="开启功能", command=self.enable_feature).pack(side="left", padx=6, pady=8)
        ctk.CTkButton(top, text="关闭功能", command=self.disable_feature).pack(side="left", padx=6, pady=8)
        ctk.CTkButton(top, text="查看状态", command=self.show_status).pack(side="left", padx=6, pady=8)
        ctk.CTkButton(top, text="清理并卸载", command=self.cleanup_feature).pack(side="left", padx=6, pady=8)
        ctk.CTkCheckBox(top, text="连接后自动开启", variable=self.auto_enable_var).pack(side="left", padx=18, pady=8)

        cfg = ctk.CTkFrame(self.root); cfg.pack(fill="x", padx=14, pady=8)
        ctk.CTkLabel(cfg, text="基于 lock999_keep_weapon v1.1：锁999 + 保护Remove；新增只改普通手雷 missile 的参数。").pack(anchor="w", padx=10, pady=(8, 4))
        row0 = ctk.CTkFrame(cfg); row0.pack(fill="x", padx=16, pady=4)
        ctk.CTkCheckBox(row0, text="锁定手雷数量", variable=self.lock999_var).pack(side="left", padx=6)
        ctk.CTkEntry(row0, textvariable=self.target_count_var, width=80).pack(side="left", padx=6)
        ctk.CTkCheckBox(row0, text="保护当前手雷对象 Remove", variable=self.protect_remove_var).pack(side="left", padx=12)
        ctk.CTkCheckBox(row0, text="运行时参数修改", variable=self.runtime_tuner_var).pack(side="left", padx=12)
        ctk.CTkCheckBox(row0, text="VirtualGrenadeMode观察", variable=self.virtual_observer_var).pack(side="left", padx=12)
        ctk.CTkCheckBox(row0, text="同步 +0x10", variable=self.sync_plain_var).pack(side="left", padx=12)
        ctk.CTkLabel(row0, text="owner:").pack(side="left", padx=(18, 4))
        ctk.CTkOptionMenu(row0, values=["local_only", "all_throw"], variable=self.owner_filter_var, width=130).pack(side="left", padx=4)

        row_scope = ctk.CTkFrame(cfg); row_scope.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(row_scope, text="无限手雷作用范围").pack(side="left", padx=(6, 4))
        ctk.CTkOptionMenu(row_scope, values=["local_only", "all_players"], variable=self.infinite_scope_var, width=150, command=lambda v: self._schedule_live_apply()).pack(side="left", padx=6)
        ctk.CTkLabel(row_scope, text="local_only=只给玩家自己；all_players=玩家+bot").pack(side="left", padx=(8, 16))
        ctk.CTkCheckBox(row_scope, text="Bot手雷行为观察", variable=self.bot_behavior_observer_var).pack(side="left", padx=12)
        ctk.CTkCheckBox(row_scope, text="Bot攻击入口观察", variable=self.bot_attack_observer_var).pack(side="left", padx=12)
        ctk.CTkCheckBox(row_scope, text="Bot手雷模式(Grenade)", variable=self.bot_grenade_mode_var).pack(side="left", padx=12)
        ctk.CTkLabel(row_scope, text="旧入口重定向已硬禁用").pack(side="left", padx=8)

        row_vg = ctk.CTkFrame(cfg); row_vg.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(row_vg, text="v2.5 BotGrenadeRecord:").pack(side="left", padx=(6, 8))
        ctk.CTkCheckBox(row_vg, text="GiveWeapon过滤", variable=self.vg_giveweapon_var).pack(side="left", padx=8)

        row_drive = ctk.CTkFrame(cfg); row_drive.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(row_drive, text="v2.6 Bot投掷驱动:").pack(side="left", padx=(6, 8))
        ctk.CTkCheckBox(row_drive, text="开启", variable=self.bot_throw_drive_var).pack(side="left", padx=8)
        ctk.CTkCheckBox(row_drive, text="Bot.UseWeapon触发Throw", variable=self.bot_throw_drive_useweapon_var).pack(side="left", padx=8)
        ctk.CTkCheckBox(row_drive, text="成功后跳过原UseWeapon", variable=self.bot_throw_drive_skip_original_var).pack(side="left", padx=8)
        ctk.CTkLabel(row_drive, text="冷却ms").pack(side="left", padx=(10, 4))
        ctk.CTkEntry(row_drive, textvariable=self.bot_throw_drive_cooldown_var, width=80).pack(side="left", padx=4)

        row_vbc = ctk.CTkFrame(cfg); row_vbc.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(row_vbc, text="v2.7 VirtualBotControl:").pack(side="left", padx=(6, 8))
        ctk.CTkCheckBox(row_vbc, text="开启", variable=self.vbc_enabled_var).pack(side="left", padx=8)
        ctk.CTkCheckBox(row_vbc, text="接管Gun.BotControl", variable=self.vbc_gun_var).pack(side="left", padx=8)
        ctk.CTkCheckBox(row_vbc, text="接管SniperBotControl", variable=self.vbc_sniper_var).pack(side="left", padx=8)
        ctk.CTkCheckBox(row_vbc, text="接管RPG.BotControl", variable=self.vbc_rpg_var).pack(side="left", padx=8)
        ctk.CTkCheckBox(row_vbc, text="成功后跳过原BotControl", variable=self.vbc_skip_original_var).pack(side="left", padx=8)
        ctk.CTkCheckBox(row_vbc, text="禁止Bot枪械开火", variable=self.bot_suppress_gun_fire_var).pack(side="left", padx=8)
        ctk.CTkCheckBox(row_vbc, text="无手雷也不许开枪", variable=self.bot_suppress_gun_no_grenade_var).pack(side="left", padx=8)

        row_ai = ctk.CTkFrame(cfg); row_ai.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(row_ai, text="v2.9 AI触发投掷:").pack(side="left", padx=(6, 8))
        ctk.CTkCheckBox(row_ai, text="观察AI链路", variable=self.bot_ai_probe_var).pack(side="left", padx=8)
        ctk.CTkCheckBox(row_ai, text="AI触发投掷", variable=self.bot_ai_hook_drive_var).pack(side="left", padx=8)
        ctk.CTkCheckBox(row_ai, text="CheckAttackTarget", variable=self.bot_ai_checkattack_drive_var).pack(side="left", padx=8)
        ctk.CTkCheckBox(row_ai, text="CameraRotation", variable=self.bot_ai_camera_drive_var).pack(side="left", padx=8)
        ctk.CTkCheckBox(row_ai, text="TrySetTarget(谨慎)", variable=self.bot_ai_tryset_drive_var).pack(side="left", padx=8)
        ctk.CTkCheckBox(row_ai, text="要求有attackTarget", variable=self.bot_ai_require_target_var).pack(side="left", padx=8)
        ctk.CTkLabel(row_ai, text="AI驱动冷却ms").pack(side="left", padx=(10, 4))
        ctk.CTkEntry(row_ai, textvariable=self.bot_ai_cooldown_var, width=80).pack(side="left", padx=4)

        row_state = ctk.CTkFrame(cfg); row_state.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(row_state, text="v2.10.4 Bot投掷状态机:").pack(side="left", padx=(6, 8))
        ctk.CTkCheckBox(row_state, text="开启", variable=self.bot_throw_sm_var).pack(side="left", padx=8)
        ctk.CTkLabel(row_state, text="选择延迟ms").pack(side="left", padx=(10, 4))
        ctk.CTkEntry(row_state, textvariable=self.bot_throw_sm_select_delay_var, width=60).pack(side="left", padx=2)
        ctk.CTkLabel(row_state, text="超时ms").pack(side="left", padx=(10, 4))
        ctk.CTkEntry(row_state, textvariable=self.bot_throw_sm_timeout_var, width=70).pack(side="left", padx=2)
        ctk.CTkCheckBox(row_state, text="出生保护", variable=self.bot_spawn_grace_var).pack(side="left", padx=(12, 4))
        ctk.CTkEntry(row_state, textvariable=self.bot_spawn_grace_ms_var, width=70).pack(side="left", padx=2)
        ctk.CTkLabel(row_state, text="ms").pack(side="left", padx=(2, 8))
        ctk.CTkCheckBox(row_state, text="目标稳定", variable=self.bot_target_stable_var).pack(side="left", padx=(8, 4))
        ctk.CTkEntry(row_state, textvariable=self.bot_target_stable_ms_var, width=60).pack(side="left", padx=2)
        ctk.CTkLabel(row_state, text="ms").pack(side="left", padx=(2, 4))
        ctk.CTkLabel(row_state, text="首次额外").pack(side="left", padx=(10, 4))
        ctk.CTkEntry(row_state, textvariable=self.bot_first_extra_delay_var, width=60).pack(side="left", padx=2)
        ctk.CTkLabel(row_state, text="ms").pack(side="left", padx=(2, 4))
        ctk.CTkCheckBox(row_state, text="复活重置", variable=self.bot_respawn_reset_var).pack(side="left", padx=(10, 4))
        ctk.CTkEntry(row_state, textvariable=self.bot_respawn_reset_cd_var, width=60).pack(side="left", padx=2)
        ctk.CTkLabel(row_state, text="ms").pack(side="left", padx=(2, 4))

        # v2.12.2：SmartAI实验UI已删除；官方可见判断保留为固定默认配置，不再显示v2.10.1实验项。
        row_ready = ctk.CTkFrame(cfg); row_ready.pack(fill="x", padx=16, pady=4)
        ctk.CTkCheckBox(row_ready, text="连投就绪开关：强制 throwReady=1", variable=self.force_ready_var).pack(side="left", padx=6)
        ctk.CTkLabel(row_ready, text="谨慎：开启后可能自动连扔；默认关闭").pack(side="left", padx=12)

        self._add_slider_row(cfg, "投掷动作加速 Animator.speed", self.anim_speed_enabled_var, self.anim_speed_var, self.anim_speed_text_var, 0.5, 10.0)

        self._add_slider_row(cfg, "伤害 expDamage（UI×10=实际）", self.damage_enabled_var, self.damage_var, self.damage_text_var, 0, 500, self.damage_scope_var)
        self._add_slider_row(cfg, "爆炸范围 expRange（UI×10=实际）", self.range_enabled_var, self.range_var, self.range_text_var, 0, 10, self.range_scope_var)
        self._add_slider_row(cfg, "飞行速度 shootSpeed（UI×10=实际）", self.speed_enabled_var, self.speed_var, self.speed_text_var, 0, 30, self.speed_scope_var)


        self.log_box = ctk.CTkTextbox(self.root, height=520); self.log_box.pack(fill="both", expand=True, padx=14, pady=(8, 14))
        self._append_ui("第一轮建议：锁999开，保护Remove开，owner=local_only；连投就绪和动作加速先默认关闭，需要时再开。")
        self._append_ui("v1.5：伤害/范围/速度滑块为缩放显示，实际写入值 = UI显示值 × 10；拖动滑块会即时生效。")
        self._append_ui("RPG/AT4/Nano 正常不应出现 [捕获手雷missile]，因为只从 WPN_Throw.<Throw>b__10_0 捕获。")
        self._append_ui("v2.0观察版：记录 PlayerWeapons.Select / SetCurrentWeapon / SetWeapon / AutoSelect / GetValidSlot，不拦截切枪。")
        self._append_ui("v2.1：新增无限手雷作用范围下拉框。local_only 只给玩家自己；all_players 包含 bot。")
        self._append_ui("v2.1：新增 Bot 手雷行为观察，用于确认 bot 是没拿到手雷、没切到手雷，还是不会执行 WPN_Throw.Throw。")
        self._append_ui("v2.2：新增 Bot 攻击入口观察，记录 WPN_Gun.BotControl / GunShoot / GenerateBullet / WPN_RPG.Fire。")
        self._append_ui("v2.3：Bot只允许手雷手雷模式默认关闭；开启后会尝试把bot纠正回slot=3手雷。")
        self._append_ui("v2.4：开启Bot手雷模式后会自动把无限手雷作用范围切到all_players，并在Select/SetCurrentWeapon入口直接重定向到手雷。")
        self._append_ui("v2.5：BotGrenadeRecord只允许普通Grenade，不包含FlashBang/Smoke；主控Bot.SelectWeapon/GetValidSlot/GiveWeapon。")
        self._append_ui("v2.5.1：旧入口重定向已硬禁用，修复RangeError导致自动关闭、玩家手雷999失效的问题。")
        self._append_ui("v2.6：Bot.UseWeapon会按冷却直接调用WPN_Throw.Throw，目标是让bot真正投掷手雷。")
        self._append_ui("v2.7：VirtualBotControl会在WPN_Gun/RPG BotControl层接管，模仿武器BotControl转为手雷Throw。")
        self._append_ui("v2.10.3：已删除v2.10.2可见性强化逻辑；Bot手雷模式默认开启；AI驱动冷却默认1000ms。")
        self._append_ui("v2.10.4：新增Bot投掷状态机，只做状态推进，不处理发枪过滤/攻击时切雷/Deploy补动作。")
        self._append_ui("v2.11：默认不再阻止Bot获得非Grenade武器，保留官方武器/模型/动作状态，减少木桩、空枪、聚堆。")
        self._append_ui("v2.11.1：伤害/范围/速度新增应用对象下拉框，my_player=玩家自己，all_players=所有人；下拉选择后即时生效。")
        self._append_ui("v2.11.2：默认放行官方选武器；GetValidSlot强制和Bot.SelectWeapon强制默认关闭，只在状态机投掷阶段临时Select(3)。")
        self._append_ui("v2.11.3：伤害/范围/速度作用对象改为my_player/all_players；默认禁止Bot枪械原BotControl开火。")
        self._append_ui("v2.11.4：新增出生保护3000ms和目标稳定700ms，避免Bot刚出生/刚看到目标马上扔雷。")
        self._append_ui("v2.11.5：修复v2.11.4只拦状态机的问题；现在AI状态机/Bot.UseWeapon/VirtualBotControl/底层Throw都走统一许可层。")
        self._append_ui("v2.11.6：复活/RemoveAll/重新发枪/手雷对象变化会重置Bot生命周期，后续复活也重新触发出生保护。")
        self._append_ui("v2.12终版：已删除旧重定向/手雷模式纠正/全局选雷/GetValidSlot强制/发枪拦截，只保留稳定主路径。")
        self._append_ui("v2.12.2：界面已移除v2.10/v2.10.1 SmartAI实验说明，只保留固定官方可见判断。")
        self._append_ui("v2.12.3：修复配置收集残留旧距离参数导致的开启失败。")
        self._append_ui("v2.12.4：修复JS初始化残留Native导致的addrOf missing argument。")

    def _add_slider_row(self, parent: Any, label: str, enabled_var: Any, value_var: Any, text_var: Any, lo: float, hi: float, scope_var: Any = None) -> None:
        ctk = self.ctk
        row = ctk.CTkFrame(parent); row.pack(fill="x", padx=16, pady=4)
        ctk.CTkCheckBox(row, text=label, variable=enabled_var, width=160).pack(side="left", padx=6)
        slider = ctk.CTkSlider(row, from_=lo, to=hi, variable=value_var, width=420, command=lambda v, vv=value_var, tv=text_var: self._on_slider_changed(vv, tv, v))
        slider.pack(side="left", padx=8)
        entry = ctk.CTkEntry(row, textvariable=text_var, width=90)
        entry.pack(side="left", padx=6)
        ctk.CTkButton(row, text="应用输入", width=80, command=lambda vv=value_var, tv=text_var, a=lo, b=hi: self._sync_entry_to_slider(vv, tv, a, b)).pack(side="left", padx=6)
        if scope_var is not None:
            ctk.CTkLabel(row, text="应用于").pack(side="left", padx=(12, 4))
            ctk.CTkOptionMenu(row, values=["my_player", "all_players"], variable=scope_var, width=120, command=lambda _v: self._schedule_live_apply()).pack(side="left", padx=4)

    def _on_slider_changed(self, value_var: Any, text_var: Any, raw_value: Any) -> None:
        try:
            v = float(raw_value)
        except Exception:
            try:
                v = float(value_var.get())
            except Exception:
                v = 0.0
        text_var.set(str(round(v, 2)))
        self._schedule_live_apply()

    def _schedule_live_apply(self) -> None:
        if self.feature is None or not self.enabled_var.get():
            return
        try:
            if self.live_apply_job is not None:
                self.root.after_cancel(self.live_apply_job)
        except Exception:
            pass
        self.live_apply_job = self.root.after(180, self._apply_config_live)

    def _apply_config_live(self) -> None:
        self.live_apply_job = None
        if self.feature is None or not self.enabled_var.get():
            return
        try:
            cfg = self._collect_config()
            self.feature.set_config(cfg)
            self.logger.json_line("[即时配置]", cfg)
            self._append_ui(
                f"已即时生效：伤害={cfg.get('damage_value')}({cfg.get('damage_apply_scope')}) 范围={cfg.get('range_value')}({cfg.get('range_apply_scope')}) 速度={cfg.get('shoot_speed_value')}({cfg.get('shoot_speed_apply_scope')}) 动作={cfg.get('throw_anim_speed_value')}",
                key="live_apply",
                interval=0.8,
            )
        except Exception as exc:
            self.logger.exception(f"[UI] 即时配置失败：{exc}")
            self._append_ui(f"即时配置失败：{exc}", key="live_apply_error", interval=2.0)

    def _sync_entry_to_slider(self, value_var: Any, text_var: Any, lo: float, hi: float) -> None:
        try:
            v = float(text_var.get().strip())
        except Exception:
            v = float(value_var.get())
        if v < lo: v = lo
        if v > hi: v = hi
        value_var.set(v)
        text_var.set(str(round(v, 2)))
        self._schedule_live_apply()

    def _append_ui(self, text: str, key: Optional[str] = None, interval: float = 0.3) -> None:
        now = time.time(); k = key or text
        if now - self.last_ui_line.get(k, 0.0) < interval: return
        self.last_ui_line[k] = now
        ts = _dt.datetime.now().strftime("%H:%M:%S")
        try:
            self.log_box.insert("end", f"[{ts}] {text}\n")
            self.log_box.see("end")
        except Exception:
            pass

    def _float_from(self, value_var: Any, text_var: Any, default: float, lo: float, hi: float) -> float:
        try: v = float(text_var.get().strip())
        except Exception:
            try: v = float(value_var.get())
            except Exception: v = default
        if v < lo: v = lo
        if v > hi: v = hi
        return v

    def _collect_config(self) -> Dict[str, Any]:
        cfg = dict(DEFAULT_CONFIG)
        cfg["lock999_enabled"] = bool(self.lock999_var.get())
        cfg["infinite_grenade_scope"] = self.infinite_scope_var.get()
        cfg["protect_weapon_remove"] = bool(self.protect_remove_var.get())
        cfg["runtime_tuner_enabled"] = bool(self.runtime_tuner_var.get())
        cfg["virtual_grenade_observer_enabled"] = bool(self.virtual_observer_var.get())
        cfg["bot_grenade_behavior_observer_enabled"] = bool(self.bot_behavior_observer_var.get())
        cfg["bot_attack_observer_enabled"] = bool(self.bot_attack_observer_var.get())
        cfg["bot_grenade_mode_enabled"] = bool(self.bot_grenade_mode_var.get())
        cfg["bot_grenade_force_scope_all_players"] = True
        cfg["bot_grenade_record_enabled"] = bool(self.bot_grenade_mode_var.get())
        cfg["virtual_grenade_giveweapon_enabled"] = bool(self.vg_giveweapon_var.get())
        cfg["virtual_grenade_preserve_original_weapons"] = True
        cfg["bot_throw_drive_enabled"] = bool(self.bot_throw_drive_var.get())
        cfg["bot_throw_drive_useweapon_enabled"] = bool(self.bot_throw_drive_useweapon_var.get())
        cfg["bot_throw_drive_skip_original_useweapon_on_success"] = bool(self.bot_throw_drive_skip_original_var.get())
        try:
            cd = int(self.bot_throw_drive_cooldown_var.get().strip())
        except Exception:
            cd = 2500
        if cd < 300: cd = 300
        if cd > 10000: cd = 10000
        cfg["bot_throw_drive_cooldown_ms"] = cd
        cfg["bot_throw_drive_force_ready"] = True
        cfg["bot_throw_drive_lock_before_after"] = True
        cfg["bot_throw_drive_log_interval_ms"] = 1000
        cfg["virtual_botcontrol_enabled"] = bool(self.vbc_enabled_var.get())
        cfg["virtual_botcontrol_replace_botcontrol"] = True
        cfg["virtual_botcontrol_gun_enabled"] = bool(self.vbc_gun_var.get())
        cfg["virtual_botcontrol_sniper_enabled"] = bool(self.vbc_sniper_var.get())
        cfg["virtual_botcontrol_rpg_enabled"] = bool(self.vbc_rpg_var.get())
        cfg["virtual_botcontrol_skip_original_on_success"] = bool(self.vbc_skip_original_var.get())
        cfg["bot_suppress_gun_fire_enabled"] = bool(self.bot_suppress_gun_fire_var.get())
        cfg["bot_suppress_gun_fire_when_no_grenade"] = bool(self.bot_suppress_gun_no_grenade_var.get())
        cfg["virtual_botcontrol_log_interval_ms"] = 1000
        cfg["bot_ai_probe_enabled"] = bool(self.bot_ai_probe_var.get())
        cfg["bot_ai_probe_verbose"] = True
        cfg["bot_ai_hook_drive_enabled"] = bool(self.bot_ai_hook_drive_var.get())
        cfg["bot_ai_checkattack_drive_enabled"] = bool(self.bot_ai_checkattack_drive_var.get())
        cfg["bot_ai_camerarotation_drive_enabled"] = bool(self.bot_ai_camera_drive_var.get())
        cfg["bot_ai_trysettarget_drive_enabled"] = bool(self.bot_ai_tryset_drive_var.get())
        cfg["bot_ai_hook_drive_require_target"] = bool(self.bot_ai_require_target_var.get())
        try:
            ai_cd = int(self.bot_ai_cooldown_var.get().strip())
        except Exception:
            ai_cd = 2500
        if ai_cd < 500: ai_cd = 500
        if ai_cd > 15000: ai_cd = 15000
        cfg["bot_ai_hook_drive_cooldown_ms"] = ai_cd
        cfg["bot_ai_probe_log_interval_ms"] = 1000
        cfg["bot_throw_state_machine_enabled"] = bool(self.bot_throw_sm_var.get())
        try:
            sm_select_delay = int(self.bot_throw_sm_select_delay_var.get().strip())
        except Exception:
            sm_select_delay = 80
        if sm_select_delay < 0: sm_select_delay = 0
        if sm_select_delay > 1000: sm_select_delay = 1000
        try:
            sm_timeout = int(self.bot_throw_sm_timeout_var.get().strip())
        except Exception:
            sm_timeout = 1200
        if sm_timeout < 300: sm_timeout = 300
        if sm_timeout > 5000: sm_timeout = 5000
        cfg["bot_throw_state_select_delay_ms"] = sm_select_delay
        cfg["bot_throw_state_ready_delay_ms"] = 0
        cfg["bot_throw_state_timeout_ms"] = sm_timeout
        cfg["bot_throw_state_log_interval_ms"] = 500
        cfg["bot_throw_unified_gate_enabled"] = True
        cfg["bot_throw_spawn_grace_enabled"] = bool(self.bot_spawn_grace_var.get())
        try:
            spawn_grace = int(self.bot_spawn_grace_ms_var.get().strip())
        except Exception:
            spawn_grace = 3000
        if spawn_grace < 0: spawn_grace = 0
        if spawn_grace > 10000: spawn_grace = 10000
        cfg["bot_throw_spawn_grace_ms"] = spawn_grace
        cfg["bot_throw_target_stable_enabled"] = bool(self.bot_target_stable_var.get())
        try:
            target_stable = int(self.bot_target_stable_ms_var.get().strip())
        except Exception:
            target_stable = 700
        if target_stable < 0: target_stable = 0
        if target_stable > 5000: target_stable = 5000
        cfg["bot_throw_target_stable_ms"] = target_stable
        try:
            first_extra = int(self.bot_first_extra_delay_var.get().strip())
        except Exception:
            first_extra = 1000
        if first_extra < 0: first_extra = 0
        if first_extra > 10000: first_extra = 10000
        cfg["bot_throw_first_throw_extra_delay_ms"] = first_extra
        cfg["bot_throw_respawn_reset_enabled"] = bool(self.bot_respawn_reset_var.get())
        cfg["bot_throw_respawn_reset_on_removeall"] = True
        cfg["bot_throw_respawn_reset_on_giveweapon"] = True
        cfg["bot_throw_respawn_reset_on_grenade_change"] = True
        try:
            respawn_reset_cd = int(self.bot_respawn_reset_cd_var.get().strip())
        except Exception:
            respawn_reset_cd = 1500
        if respawn_reset_cd < 300: respawn_reset_cd = 300
        if respawn_reset_cd > 10000: respawn_reset_cd = 10000
        cfg["bot_throw_respawn_reset_cooldown_ms"] = respawn_reset_cd
        cfg["smart_grenade_ai_enabled"] = bool(self.smart_ai_enabled_var.get())
        cfg["smart_grenade_require_official_visible"] = bool(self.smart_ai_official_visible_var.get())
        cfg["smart_grenade_recent_visible_ms"] = 350
        if cfg["bot_grenade_mode_enabled"]:
            cfg["infinite_grenade_scope"] = "all_players"
            try:
                self.infinite_scope_var.set("all_players")
            except Exception:
                pass
        cfg["sync_plain_value"] = bool(self.sync_plain_var.get())
        cfg["force_throw_ready_enabled"] = bool(self.force_ready_var.get())
        cfg["throw_anim_speed_enabled"] = bool(self.anim_speed_enabled_var.get())
        cfg["throw_anim_speed_value"] = self._float_from(self.anim_speed_var, self.anim_speed_text_var, 1.6, 0.5, 10.0)
        cfg["owner_filter"] = self.owner_filter_var.get()
        try:
            n = int(self.target_count_var.get().strip())
        except Exception:
            n = 999
        if n < 1: n = 999
        if n > 9999: n = 9999
        cfg["target_count"] = n
        cfg["enable_damage"] = bool(self.damage_enabled_var.get())
        cfg["damage_value"] = round(self._float_from(self.damage_var, self.damage_text_var, 99.9, 0, 500) * DISPLAY_SCALE["damage_value"], 4)
        cfg["damage_apply_scope"] = self.damage_scope_var.get()
        cfg["enable_range"] = bool(self.range_enabled_var.get())
        cfg["range_value"] = round(self._float_from(self.range_var, self.range_text_var, 1.0, 0, 10) * DISPLAY_SCALE["range_value"], 4)
        cfg["range_apply_scope"] = self.range_scope_var.get()
        cfg["enable_shoot_speed"] = bool(self.speed_enabled_var.get())
        cfg["shoot_speed_value"] = round(self._float_from(self.speed_var, self.speed_text_var, 3.5, 0, 30) * DISPLAY_SCALE["shoot_speed_value"], 4)
        cfg["shoot_speed_apply_scope"] = self.speed_scope_var.get()
        return cfg

    def connect_now(self) -> None:
        if self.manager.connected:
            self._append_ui("已经连接游戏。", key="already_connected"); return
        def worker() -> None:
            try:
                self.manager.attach_and_load()
                self.feature = CombinedFeature(self.manager, logger=self.logger)
                self.status_var.set(f"已连接游戏 PID={self.manager.pid}")
                self._append_ui(f"连接成功：PID={self.manager.pid}")
                if self.auto_enable_var.get(): self.enable_feature()
            except Exception as exc:
                self.status_var.set(f"连接失败：{exc}")
                self.logger.exception(f"[UI] 连接失败：{exc}")
                self._append_ui(f"连接失败：{exc}", key="connect_failed", interval=2.0)
        threading.Thread(target=worker, daemon=True).start()

    def enable_feature(self) -> None:
        if self.feature is None:
            self._append_ui("尚未连接，不能开启。", key="enable_no_connection"); return
        if self.enabled_var.get():
            self._append_ui("功能已经开启。", key="already_enabled"); return
        try:
            cfg = self._collect_config()
            self.logger.json_line("[UI功能配置]", cfg)
            result = self.feature.enable(cfg)
            self.enabled_var.set(True)
            self._append_ui(f"已开启：{result}")
        except Exception as exc:
            self.logger.exception(f"[UI] 开启失败：{exc}")
            self._append_ui(f"开启失败：{exc}")

    def disable_feature(self) -> None:
        if self.feature is None: return
        try:
            result = self.feature.disable()
            self.enabled_var.set(False)
            self._append_ui(f"功能已关闭：{result}")
        except Exception as exc:
            self.logger.exception(f"[UI] 关闭失败：{exc}")
            self._append_ui(f"关闭失败：{exc}")

    def show_status(self) -> None:
        if self.feature is None:
            self._append_ui("尚未连接。", key="status_no_connection"); return
        try:
            status = self.feature.status()
            self.logger.json_line("[手动状态]", status)
            summary = (f"开启={status.get('enabled')} 锁写={status.get('lock_writes')} "
                       f"就绪写={status.get('throw_ready_writes')} 动作速={status.get('anim_speed_writes')} "
                       f"阻止Remove={status.get('remove_blocked')} 捕获missile={status.get('capture_hits')} "
                       f"应用={status.get('tune_applied')} 字段写={status.get('grenade_field_writes')} "
                       f"Create参数={status.get('createExplosion_param_writes')} "
                       f"飞行速度写={status.get('missile_speed_writes')} 观察={status.get('observer_hits')} 手雷类={status.get('observer_grenade_class_hits')} 非手雷类={status.get('observer_non_grenade_class_hits')} Bot投掷={status.get('bot_throw_method_hits')} GunShootBot={status.get('gun_shoot_botlike_hits')} 复活重置={status.get('bot_life_respawn_reset')} 出生拦={status.get('bot_throw_gate_block_spawn')} 手雷={status.get('bot_throw_drive_success')} 错误={status.get('error_count')}")
            self._append_ui("状态：" + summary, key="manual_status", interval=0.1)
        except Exception as exc:
            self.logger.exception(f"[UI] 状态读取失败：{exc}")
            self._append_ui(f"状态读取失败：{exc}")

    def cleanup_feature(self) -> None:
        try:
            if self.feature is not None:
                result = self.feature.cleanup()
                self._append_ui(f"清理完成：{result}")
        except Exception as exc:
            msg = str(exc)
            if "script has been destroyed" in msg:
                self.logger.warning("[UI] 游戏退出后脚本已销毁，跳过 cleanup。")
                self._append_ui("游戏已退出，脚本已销毁，已跳过 cleanup。", key="script_destroyed")
            else:
                self.logger.exception(f"[UI] cleanup 失败：{exc}")
                self._append_ui(f"清理失败：{exc}")
        finally:
            self.enabled_var.set(False)

    def periodic(self) -> None:
        if self.closing: return
        try:
            if not self.manager.connected:
                pid = self.manager.find_pid()
                if pid is None: self.status_var.set(f"未连接：等待 {PROCESS_NAME}")
                else:
                    self.status_var.set(f"发现游戏 PID={pid}，正在连接...")
                    self.connect_now()
            else:
                if not self.manager.is_process_alive():
                    self.logger.warning("[监控] 游戏进程已退出")
                    self._append_ui("检测到游戏进程已退出。", key="game_exited", interval=0.5)
                    self.cleanup_feature(); self.manager.detach(); self.feature = None
                    self.status_var.set("游戏已退出，等待重新启动")
                else:
                    self._poll_messages(); self._poll_status_snapshot()
        except Exception as exc:
            self.logger.exception(f"[UI] 周期检查异常：{exc}")
            self._append_ui(f"周期检查异常：{exc}", key="periodic_error", interval=3.0)
        self.root.after(1000, self.periodic)

    def _poll_messages(self) -> None:
        count = 0
        while count < 80:
            try: msg = self.manager.message_queue.get_nowait()
            except queue.Empty: break
            count += 1
            self._append_ui(msg, key=msg[:180], interval=0.7)

    def _poll_status_snapshot(self) -> None:
        if self.feature is None: return
        try: status = self.feature.status()
        except Exception as exc:
            self.logger.exception(f"[UI] 自动状态读取失败：{exc}"); return
        self.status_var.set(f"已连接 PID={self.manager.pid} | 开启={status.get('enabled')} | 锁写={status.get('lock_writes')} | 就绪={status.get('throw_ready_writes')} | 阻止Remove={status.get('remove_blocked')} | 捕获={status.get('capture_hits')} | 观察={status.get('observer_hits')} | 手雷类={status.get('observer_grenade_class_hits')} | 非手雷={status.get('observer_non_grenade_class_hits')} | 错误={status.get('error_count')}")
        now = time.time()
        if now - self.last_status_log_time >= 5.0:
            self.last_status_log_time = now
            self.logger.json_line("[自动状态]", status)

    def on_close(self) -> None:
        self.closing = True
        self.logger.info("[UI] 正在关闭")
        try: self.cleanup_feature()
        finally:
            try: self.manager.detach()
            finally:
                self.logger.info("[UI] 已关闭")
                self.root.destroy()

    def run(self) -> None:
        self.root.after(500, self.periodic)
        self.root.mainloop()

def run_ui() -> int:
    try:
        app = CombinedApp(); app.run(); return 0
    except Exception as exc:
        print(f"[{FEATURE_ID}] 启动失败：{exc}")
        print("依赖安装：pip install frida psutil customtkinter")
        print("文件要求：py 和 js 必须放在同一目录。")
        print(traceback.format_exc())
        return 1

if __name__ == "__main__":
    raise SystemExit(run_ui())
