def _emit_log(context, level, message, audience, dev_detail):
    context.event_bus.emit(
        "log_message",
        level=level,
        module="武器赋予",
        message=message,
        audience=audience,
        dev_detail=dev_detail,
    )


def handle_event(context, event, payload):
    if event == "giveWeaponResult":
        task_id = payload.get("taskId", 0)
        success = payload.get("success", False)
        if success:
            _emit_log(
                context,
                "success",
                "武器赋予执行成功",
                "both",
                f"WeaponGiver task #{task_id} succeeded",
            )
        else:
            _emit_log(
                context,
                "error",
                "武器赋予执行失败，请稍后重试",
                "both",
                f"WeaponGiver task #{task_id} failed",
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
