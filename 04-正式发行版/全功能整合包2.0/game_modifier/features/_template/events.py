def handle_event(context, event, payload):
    """Optional plugin_event handler for this feature.

    Keep event handling feature-local. Use only safe PanelContext methods here.
    """
    if event == "enabled":
        context.log("模板功能已启用")
