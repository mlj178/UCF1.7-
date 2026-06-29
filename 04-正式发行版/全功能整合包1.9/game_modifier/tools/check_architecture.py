import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ORDINARY_FEATURES = {
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
    "esp_box",
    "timescale",
}


def fail(message):
    print(f"FAIL: {message}")
    return False


def check_plugin_dirs():
    ok = True
    for feature_id in sorted(ORDINARY_FEATURES):
        plugin_dir = ROOT / "features" / feature_id
        for name in ("manifest.json", "feature.py", "script.js", "panel.py"):
            if not (plugin_dir / name).exists():
                ok = fail(f"missing {plugin_dir / name}") and ok
        manifest_path = plugin_dir / "manifest.json"
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if manifest.get("feature_id") != feature_id:
                ok = fail(f"bad feature_id in {manifest_path}") and ok
    return ok


def check_ui_boundary():
    plugin_page = ROOT / "ui" / "pages" / "plugin_feature_page.py"
    feature_tabs = ROOT / "ui" / "views" / "feature_tabs_view.py"
    if not plugin_page.exists():
        return fail("missing plugin_feature_page.py")
    page_text = plugin_page.read_text(encoding="utf-8")
    tabs_text = feature_tabs.read_text(encoding="utf-8")
    ok = True
    for needle in (".by_tab(", "manifest.get(\"layout\"", "order"):
        if needle not in page_text:
            ok = fail(f"plugin page missing {needle}") and ok
    for needle in ("_build_weapon_tab", "_build_player_tab", "_build_other_tab", "_make_feature_card("):
        if needle in tabs_text:
            ok = fail(f"feature_tabs_view still contains {needle}") and ok
    return ok


def check_runtime_boundary():
    service_text = (ROOT / "core" / "services" / "feature_command_service.py").read_text(encoding="utf-8")
    frida_text = (ROOT / "core" / "frida_manager.py").read_text(encoding="utf-8")
    ok = True
    for feature_id in ORDINARY_FEATURES:
        if f'"{feature_id}"' in service_text or f"'{feature_id}'" in service_text:
            ok = fail(f"FeatureCommandService has feature branch for {feature_id}") and ok
        if feature_id != "esp_box" and f"modules.{feature_id}" in frida_text:
            ok = fail(f"FridaManager dispatcher still references modules.{feature_id}") and ok
    return ok


def check_assets():
    ok = True
    if not (ROOT / "plugins" / "universal_hook" / "Universal-ImGui-Hook.dll").exists():
        ok = fail("Universal-ImGui-Hook.dll missing") and ok
    script_count = len(list((ROOT / "scripts").glob("*.js")))
    if script_count < 20:
        ok = fail(f"legacy scripts missing, count={script_count}") and ok
    return ok


def main():
    checks = [
        check_plugin_dirs(),
        check_ui_boundary(),
        check_runtime_boundary(),
        check_assets(),
    ]
    if all(checks):
        print("ARCHITECTURE_CHECK_OK")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
