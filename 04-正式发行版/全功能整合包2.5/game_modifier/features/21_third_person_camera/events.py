def handle_event(context, event, payload):
    payload = payload or {}

    if event == "enabled":
        context.log("✅ [第三人称视角] 已开启")
    elif event == "disabled":
        reason = payload.get("reason")
        context.log(f"ℹ️ [第三人称视角] 已关闭{f'：{reason}' if reason else ''}")
    elif event == "config_applied":
        config = payload.get("config", {})
        distance = config.get("distance")
        pivot_height = config.get("pivotHeight")
        context.log(f"✅ [第三人称视角] 参数已应用 distance={distance}, pivotHeight={pivot_height}")
    elif event == "runtime_ready":
        context.log("✅ [第三人称视角] 运行时已就绪")
    elif event == "runtime_error":
        context.log(f"❌ [第三人称视角] {payload.get('message', '运行时错误')}")
    elif event == "session_destroyed":
        context.log(f"ℹ️ [第三人称视角] 会话已销毁：{payload.get('reason', 'unknown')}")
    elif event == "state_changed":
        context.log(
            f"ℹ️ [第三人称视角] 状态变化 {payload.get('oldState')} -> {payload.get('newState')}"
        )
