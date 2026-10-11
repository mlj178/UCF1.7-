import time


_NORMAL_FAILURE_REASONS = {"awaiting_room", "no_player", "invalid_player", "expired"}
_last_normal_failure_log_at = {}
_NORMAL_FAILURE_THROTTLE_SECONDS = 3.0


def _emit_log(context, level, message, audience, dev_detail):
    context.event_bus.emit(
        "log_message",
        level=level,
        module="武器赋予",
        message=message,
        audience=audience,
        dev_detail=dev_detail,
    )


def _should_log_normal_failure(reason):
    now = time.monotonic()
    last = _last_normal_failure_log_at.get(reason)
    if last is not None and now - last < _NORMAL_FAILURE_THROTTLE_SECONDS:
        return False
    _last_normal_failure_log_at[reason] = now
    return True


def handle_event(context, event, payload):
    if event == "giveWeaponResult":
        task_id = payload.get("taskId", 0)
        success = payload.get("success", False)
        reason = payload.get("reason", "")
        if success:
            _emit_log(
                context,
                "success",
                "武器赋予执行成功",
                "both",
                f"WeaponGiver task #{task_id} succeeded",
            )
        else:
            if reason in _NORMAL_FAILURE_REASONS and not _should_log_normal_failure(reason):
                return
            level = "warning" if reason in _NORMAL_FAILURE_REASONS else "error"
            message = "玩家暂不可用，已忽略本次赋予" if reason in _NORMAL_FAILURE_REASONS else "武器赋予执行失败，请稍后重试"
            _emit_log(
                context,
                level,
                message,
                "both",
                f"WeaponGiver task #{task_id} failed, reason={reason or 'unknown'}",
            )
    elif event == "weapon_acquired":
        weapon_ptr = payload.get("weaponPtr", "")
        weapon_id = payload.get("weaponId", 0)
        if not weapon_ptr:
            return
        try:
            context.feature_service.call_action(
                "speedgun",
                "notifyWeaponAcquired",
                {"weaponId": weapon_id, "weaponPtr": weapon_ptr},
            )
        except Exception as exc:
            _emit_log(
                context,
                "warning",
                "WeaponGiver speedgun bridge failed",
                "dev",
                f"weapon_acquired bridge failed weaponId={weapon_id}, weaponPtr={weapon_ptr}, error={exc}",
            )
    elif event == "playerRespawned":
        _emit_log(
            context,
            "info",
            "检测到玩家复活",
            "dev",
            "WeaponGiver detected local player respawn",
        )
    elif event == "playerRespawnedWithWeapon":
        weapon_id = payload.get("weaponId", "")
        weapon_name = payload.get("weaponName", "")
        _emit_log(
            context,
            "success",
            f"复活后已自动装备: {weapon_name}",
            "both",
            f"WeaponGiver respawn equipped weaponId={weapon_id}, weaponName={weapon_name}",
        )


def sync_hotkeys_for_current_connection(context, controller):
    if context.is_connected():
        controller.init_hotkey_manager()


def handle_lifecycle(context, event, payload):
    try:
        from .state import state

        controller = getattr(state, "controller", None)
        if not controller:
            return
        if event == "game_connected":
            sync_hotkeys_for_current_connection(context, controller)
        elif event in {"game_disconnected", "app_closing"}:
            controller.pause_hotkeys()
            if event == "app_closing":
                controller.cleanup()
    except Exception:
        pass
