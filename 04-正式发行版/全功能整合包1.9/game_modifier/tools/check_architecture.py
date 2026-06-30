import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FEATURES_DIR = ROOT / "features"
RUNTIME_DIRS = ("core", "ui", "features")
ORDINARY_FEATURE_IDS = {
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
SPECIAL_FEATURE_IDS = {"nano4t", "weapon_giver", "battle_round"}
KNOWN_FEATURE_IDS = ORDINARY_FEATURE_IDS | SPECIAL_FEATURE_IDS


def fail(message):
    print(f"FAIL: {message}")
    return False


def warn(message):
    print(f"WARNING: {message}")


def runtime_files(pattern):
    for dirname in RUNTIME_DIRS:
        base = ROOT / dirname
        if not base.exists():
            continue
        for path in base.rglob(pattern):
            parts = set(path.relative_to(ROOT).parts)
            if "_legacy_archive" in parts or "_template" in parts:
                continue
            yield path


def plugin_dirs():
    return sorted(
        path
        for path in FEATURES_DIR.iterdir()
        if path.is_dir() and not path.name.startswith("_")
    )


def read(path):
    return path.read_text(encoding="utf-8")


def check_scripts_directory():
    ok = True
    scripts_dir = ROOT / "scripts"
    if not scripts_dir.exists():
        return ok
    for path in scripts_dir.iterdir():
        if path.name != "README.md":
            ok = fail(f"scripts directory still contains runtime-looking file: {path}") and ok
    return ok


def check_common_js_removed_from_runtime():
    ok = True
    if (ROOT / "scripts" / "_common.js").exists():
        ok = fail("runtime scripts/_common.js still exists") and ok
    if (FEATURES_DIR / "_shared" / "common.js").exists():
        ok = fail("runtime features/_shared/common.js still exists") and ok
    archive_common = FEATURES_DIR / "_legacy_archive" / "scripts" / "_common.js"
    if not archive_common.exists():
        ok = fail("historical _common.js is not archived") and ok
    for path in runtime_files("*"):
        if path.suffix not in {".py", ".js", ".json", ".md", ".spec"}:
            continue
        text = read(path)
        for needle in ("scripts/_common.js", "scripts\\\\_common.js", "features/_shared/common.js"):
            if needle in text:
                ok = fail(f"runtime file references shared common js: {path}") and ok
    return ok


def check_manifest_loader():
    path = ROOT / "core" / "plugin" / "manifest_loader.py"
    text = read(path)
    ok = True
    if "startswith(\"_\")" not in text and "startswith('_')" not in text:
        ok = fail("ManifestLoader does not skip all underscore feature directories") and ok
    return ok


def check_script_manager():
    path = ROOT / "core" / "frida_runtime" / "script_manager.py"
    text = read(path)
    ok = True
    for needle in ("SCRIPTS_DIR", "_common.js", "features/_shared/common.js"):
        if needle in text:
            ok = fail(f"ScriptManager references forbidden shared source: {needle}") and ok
    if "manifest.get(\"script\"" not in text and "manifest.get('script'" not in text:
        ok = fail("ScriptManager does not read script from manifest") and ok
    if "_script_path" not in text or "_plugin_dir" not in text:
        ok = fail("ScriptManager does not resolve features/<feature_id>/script.js path") and ok
    return ok


def check_frida_manager():
    path = ROOT / "core" / "frida_manager.py"
    text = read(path)
    ok = True
    forbidden = (
        "ORDINARY_PLUGIN_FEATURE_IDS",
        "core.feature_registry",
        "_build_rpc_exports",
        "_build_dispatcher",
        "_build_js_code",
        "_ensure_special_features_registered",
        "nano4tinit",
        "giveweapon",
        "setrespawnweapon",
        "clearrespawnweapon",
        "battleRoundGetStatus",
    )
    for needle in forbidden:
        if needle in text:
            ok = fail(f"FridaManager still contains legacy branch/export: {needle}") and ok
    for deprecated in ("send_toggle", "call_export"):
        if deprecated in text and "DEPRECATED" not in text:
            ok = fail(f"FridaManager contains {deprecated} without DEPRECATED marker") and ok
    for feature_id in KNOWN_FEATURE_IDS:
        if f'"{feature_id}"' in text or f"'{feature_id}'" in text:
            ok = fail(f"FridaManager contains concrete feature id: {feature_id}") and ok
    return ok


def check_feature_action_controller():
    ok = True
    for filename in ("feature_action_controller.py", "action_router.py"):
        path = ROOT / "ui" / "controllers" / filename
        text = read(path)
        for feature_id in KNOWN_FEATURE_IDS:
            if f'"{feature_id}"' in text or f"'{feature_id}'" in text:
                ok = fail(f"{filename} contains concrete feature id: {feature_id}") and ok
        for legacy_action in ("gather()", "skip_round()", "on_knife_speed_change", "on_gravity_change"):
            if legacy_action in text:
                ok = fail(f"{filename} contains legacy dedicated action: {legacy_action}") and ok
    return ok


def check_core_config_manifest_source():
    path = ROOT / "core" / "config.py"
    text = read(path)
    ok = True
    if re.search(r"FEATURES_INFO\s*=\s*\{", text):
        ok = fail("core/config.py still hardcodes FEATURES_INFO dict") and ok
    if "manifest.json" not in text or "features" not in text:
        ok = fail("core/config.py does not build feature info from manifests") and ok
    return ok


def check_plugin_files_and_manifests():
    ok = True
    required_files = ("manifest.json", "feature.py", "script.js", "panel.py")
    for plugin_dir in plugin_dirs():
        feature_id = plugin_dir.name
        for filename in required_files:
            if not (plugin_dir / filename).exists():
                ok = fail(f"missing {plugin_dir / filename}") and ok

        manifest_path = plugin_dir / "manifest.json"
        if not manifest_path.exists():
            continue
        try:
            manifest = json.loads(read(manifest_path))
        except Exception as exc:
            ok = fail(f"manifest cannot be parsed: {manifest_path}: {exc}") and ok
            continue
        if manifest.get("feature_id") != feature_id:
            ok = fail(f"manifest feature_id mismatch: {manifest_path}") and ok
        if "rpc" not in manifest:
            ok = fail(f"manifest missing rpc: {manifest_path}") and ok
        for required in (
            "feature_id",
            "display_name",
            "script",
            "controls",
            "config",
            "rpc",
            "lifecycle",
        ):
            if required not in manifest:
                ok = fail(f"manifest missing {required}: {manifest_path}") and ok
        if manifest.get("runtime", {}).get("type") != "plugin_script":
            ok = fail(f"manifest runtime.type must be plugin_script: {manifest_path}") and ok

        script_path = plugin_dir / "script.js"
        if script_path.exists() and "rpc.exports" not in read(script_path):
            ok = fail(f"script.js missing rpc.exports: {script_path}") and ok
    return ok


def check_plugin_python_boundaries():
    ok = True
    for plugin_dir in plugin_dirs():
        feature_py = plugin_dir / "feature.py"
        panel_py = plugin_dir / "panel.py"
        if feature_py.exists():
            text = read(feature_py)
            legacy_patterns = {
                "register_feature": r"\bregister_feature\b",
                "FeatureBase": r"(?<!Plugin)\bFeatureBase\b",
                "core.feature_registry": r"core\.feature_registry",
            }
            for name, pattern in legacy_patterns.items():
                if re.search(pattern, text):
                    ok = fail(f"feature.py uses legacy runtime {name}: {feature_py}") and ok
        if panel_py.exists():
            text = read(panel_py)
            if "FridaManager" in text or "core.frida_manager" in text:
                ok = fail(f"panel.py imports FridaManager: {panel_py}") and ok
            if "app._" in text or "build_panel(app" in text:
                ok = fail(f"panel.py depends on full app/private fields: {panel_py}") and ok
    return ok


def check_app_state_legacy_boundary():
    path = ROOT / "core" / "state" / "app_state.py"
    text = read(path)
    ok = True
    if "Legacy migration fields only" not in text:
        ok = fail("AppState concrete feature fields are not marked as legacy migration") and ok
    allowed_fields = {
        "features",
        "knife_speed",
        "move_speed",
        "range_mult",
        "gravity",
        "jump",
        "gravity_mode",
        "timescale",
        "battle_round_enabled",
        "weapon_giver_respawn_enabled",
        "nano4t_ghost",
        "nano4t_human",
    }
    fields = set(re.findall(r"^\s{4}([a-zA-Z_][a-zA-Z0-9_]*)\s*:", text, re.MULTILINE))
    extra = fields - allowed_fields
    if extra:
        ok = fail(f"AppState has new concrete fields: {sorted(extra)}") and ok
    return ok


def check_template_is_plugin_self_contained():
    ok = True
    template_dir = FEATURES_DIR / "_template"
    for filename in ("manifest.json", "feature.py", "script.js", "panel.py", "README.md"):
        if not (template_dir / filename).exists():
            ok = fail(f"template missing {filename}") and ok
    script_path = template_dir / "script.js"
    if script_path.exists():
        script = read(script_path)
        if "rpc.exports" not in script:
            ok = fail("template script.js missing rpc.exports") and ok
        for needle in ("common.js", "scripts/_common.js", "require("):
            if needle in script:
                ok = fail(f"template script.js references shared JS: {needle}") and ok
    panel_path = template_dir / "panel.py"
    if panel_path.exists():
        panel = read(panel_path)
        for needle in ("FridaManager", "app._"):
            if needle in panel:
                ok = fail(f"template panel.py uses forbidden dependency: {needle}") and ok
        for callback_name in ('callbacks["toggle"]', 'callbacks["set_config"]', 'callbacks["action"]'):
            if callback_name not in panel:
                ok = fail(f"template panel.py missing {callback_name}") and ok
    return ok


def check_script_helper_warnings():
    warnings = []
    for plugin_dir in plugin_dirs():
        script_path = plugin_dir / "script.js"
        if not script_path.exists():
            continue
        text = read(script_path)
        for match in re.finditer(r"\bfunction\s+([A-Za-z_$][\w$]*)\s*\(", text):
            name = match.group(1)
            if name.startswith("__plugin") or name in {"enable", "disable", "setConfig", "status", "cleanup"}:
                continue
            if len(re.findall(rf"\b{re.escape(name)}\b", text)) <= 1:
                warnings.append(f"possible unused JS helper in {script_path}: {name}")
    for message in warnings[:20]:
        warn(message)
    if len(warnings) > 20:
        warn(f"{len(warnings) - 20} more possible unused JS helpers omitted")


def check_runtime_old_script_references():
    ok = True
    forbidden = [
        "scripts/01-",
        "scripts/02-",
        "scripts/03-",
        "scripts/04-",
        "scripts/05-",
        "scripts/06-",
        "scripts/07-",
        "scripts/08-",
        "scripts/09-",
        "scripts/10-",
        "scripts/11-",
        "scripts/12-",
        "scripts/13-",
        "scripts/14-",
        "scripts/15-",
        "scripts/16-",
        "scripts/17-",
        "scripts/18-",
        "scripts/19-",
        "scripts/20-",
        "scripts\\\\01-",
        "scripts\\\\02-",
        "scripts\\\\03-",
        "scripts\\\\04-",
        "scripts\\\\05-",
        "scripts\\\\06-",
        "scripts\\\\07-",
        "scripts\\\\08-",
        "scripts\\\\09-",
        "scripts\\\\10-",
        "scripts\\\\11-",
        "scripts\\\\12-",
        "scripts\\\\13-",
        "scripts\\\\14-",
        "scripts\\\\15-",
        "scripts\\\\16-",
        "scripts\\\\17-",
        "scripts\\\\18-",
        "scripts\\\\19-",
        "scripts\\\\20-",
    ]
    for path in runtime_files("*"):
        if path.suffix not in {".py", ".js", ".spec"}:
            continue
        text = read(path)
        for needle in forbidden:
            if needle in text:
                ok = fail(f"runtime file references old scripts entrypoint: {path}: {needle}") and ok
    return ok


def check_no_mainline_legacy_runtime_files():
    ok = True
    if (ROOT / "core" / "feature_registry.py").exists():
        ok = fail("core/feature_registry.py still exists in mainline") and ok
    if (FEATURES_DIR / "base.py").exists():
        ok = fail("features/base.py still exists in mainline") and ok
    for path in FEATURES_DIR.glob("feature_*.py"):
        ok = fail(f"legacy feature module still exists in mainline: {path}") and ok
    return ok


def check_assets():
    ok = True
    if not (ROOT / "plugins" / "universal_hook" / "Universal-ImGui-Hook.dll").exists():
        ok = fail("Universal-ImGui-Hook.dll missing") and ok
    if not (FEATURES_DIR / "_legacy_archive" / "scripts").exists():
        ok = fail("legacy script archive missing") and ok
    return ok


def main():
    checks = [
        check_scripts_directory(),
        check_common_js_removed_from_runtime(),
        check_manifest_loader(),
        check_script_manager(),
        check_frida_manager(),
        check_feature_action_controller(),
        check_core_config_manifest_source(),
        check_plugin_files_and_manifests(),
        check_plugin_python_boundaries(),
        check_app_state_legacy_boundary(),
        check_template_is_plugin_self_contained(),
        check_runtime_old_script_references(),
        check_no_mainline_legacy_runtime_files(),
        check_assets(),
    ]
    check_script_helper_warnings()
    if all(checks):
        print("ARCHITECTURE_CHECK_OK")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
