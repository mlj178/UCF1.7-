def build_card(scroll, manifest, row, col, colspan, callbacks, card_builder):
    """Optional custom card entrypoint.

    Use only the generic callbacks:
    - callbacks["toggle"](feature_id)
    - callbacks["set_config"](feature_id, key, value)
    - callbacks["action"](feature_id, action)
    """
    feature_id = manifest["feature_id"]
    frame, switch, label = card_builder.make_feature_card(
        scroll,
        row,
        col,
        colspan,
        manifest,
        slider_callback=lambda value: callbacks["set_config"](feature_id, "value", value),
    )
    switch.configure(command=lambda: callbacks["toggle"](feature_id))
    return {
        manifest.get("ui_handles", {}).get("switch", f"{feature_id}_switch"): switch,
        f"{feature_id}_frame": frame,
        f"{feature_id}_label": label,
    }
