def build_card(scroll, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    frame, switch, _ = card_builder.make_feature_card(
        scroll,
        row,
        col,
        colspan,
        manifest,
        title_color=manifest.get("layout", {}).get("title_color"),
    )
    frame.grid_configure(sticky="nsew")
    return {manifest.get("ui_handles", {}).get("switch", f"{feature_id}_switch"): switch}
