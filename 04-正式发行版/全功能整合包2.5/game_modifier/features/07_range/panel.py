import customtkinter as ctk


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    slider_control = next(
        (item for item in manifest.get("controls", []) if item.get("type") == "slider"),
        {},
    )
    key = slider_control.get("key", "range")
    slider_var = ctk.DoubleVar(value=float(slider_control.get("default", 50.0)))
    slider_range = (
        float(slider_control.get("min", 1.0)),
        float(slider_control.get("max", 50.0)),
    )

    _, switch, label = card_builder.make_feature_card(
        parent,
        row,
        col,
        colspan,
        manifest,
        slider_callback=lambda value: callbacks["set_config"](feature_id, key, value),
        slider_var=slider_var,
        slider_range=slider_range,
        title_color=manifest.get("layout", {}).get("title_color"),
    )

    handles = manifest.get("ui_handles", {})
    return {
        handles.get("switch", "range_switch"): switch,
        handles.get("slider_var", "range_var"): slider_var,
        handles.get("slider_label", "range_label"): label,
    }
