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

ORDINARY_SOURCES = {
    "knife": "feature_04_fast_knife.py",
    "recoil": "feature_02_no_recoil.py",
    "ammo": "feature_01_unlimited_ammo.py",
    "ammoplus": "feature_05_fast_reload_buff.py",
    "range": "feature_07_knife_attack_range.py",
    "aim": "feature_11_auto_aim.py",
    "speedgun": "feature_13_fire_rate_auto_sniper.py",
    "movespeed": "feature_06_movement_speed.py",
    "time": "feature_03_unlimited_time.py",
    "gravity": "feature_09_high_jump_low_gravity.py",
    "godmode": "feature_12_invincibility.py",
    "skillcd": "feature_17_skill_no_cooldown.py",
    "gather": "feature_08_gather_enemies.py",
    "isbot": "feature_14_become_bot.py",
    "roundskip": "feature_10_skip_round.py",
    "esp_box": "feature_18_universal_esp_box.py",
    "timescale": "feature_20_unity_time_acceleration.py",
}

EXPECTED_MANIFEST_TEXT = {
    "knife": ("快刀", "🔪", "提升挥刀速度（人类 / 生化幽灵通用）"),
    "recoil": ("无后座力", "🎯", "消除所有枪械后座力"),
    "ammo": ("无限子弹", "🔫", "子弹永不消耗"),
    "ammoplus": ("快速换弹", "⚡", "换弹速度加快"),
    "range": ("剑气化丝", "⚔️", "扩大近战攻击距离（人类 / 生化幽灵通用）"),
    "aim": ("自瞄", "🎯", "自动瞄准敌方玩家"),
    "speedgun": ("射速变快 / 连狙", "⚡", "射速10倍 | 半自动→全自动 | 狙击镜常开 | 后坐力清零"),
    "movespeed": ("滑板鞋", "👟", "提升移动速度"),
    "time": ("无限时间", "⏰", "设定时间为 9:59"),
    "gravity": ("轻重力 / 高跳", "🌌", "调整重力与跳跃倍率"),
    "godmode": ("金刚不坏", "🛡️", "角色受到攻击时不会受伤"),
    "skillcd": ("技能无冷却", "✨", "生化模式，所有技能无冷却"),
    "gather": ("聚怪", "👾", "将所有人机聚集到佣兵出生点"),
    "isbot": ("天机傀儡", "🧠", "玩家由人机控制"),
    "roundskip": ("回合跳过", "⏭️", "结束当前回合"),
    "esp_box": ("方框透视", "📦", "通过 Universal DLL 显示方框透视"),
    "timescale": ("时间加速", "⏩", "调整游戏时间倍率"),
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
            text_fields = (
                manifest.get("display_name"),
                manifest.get("icon"),
                manifest.get("desc"),
            )
            if text_fields != EXPECTED_MANIFEST_TEXT[feature_id]:
                ok = fail(f"manifest text is corrupted in {manifest_path}") and ok
            if any("?" in str(value) for value in text_fields):
                ok = fail(f"manifest text contains mojibake placeholder in {manifest_path}") and ok
        feature_text_path = plugin_dir / "feature.py"
        if feature_text_path.exists():
            feature_text = feature_text_path.read_text(encoding="utf-8")
            if "register_feature" in feature_text:
                ok = fail(f"ordinary plugin still imports/registers legacy registry: {feature_text_path}") and ok
    return ok


def check_ui_boundary():
    plugin_page = ROOT / "ui" / "pages" / "plugin_feature_page.py"
    feature_tabs = ROOT / "ui" / "views" / "feature_tabs_view.py"
    common_view = ROOT / "ui" / "views" / "common.py"
    controller = ROOT / "ui" / "controllers" / "feature_action_controller.py"
    if not plugin_page.exists():
        return fail("missing plugin_feature_page.py")
    page_text = plugin_page.read_text(encoding="utf-8")
    tabs_text = feature_tabs.read_text(encoding="utf-8")
    common_text = common_view.read_text(encoding="utf-8")
    controller_text = controller.read_text(encoding="utf-8")
    ok = True
    for needle in (".by_tab(", "manifest.get(\"layout\"", "order"):
        if needle not in page_text:
            ok = fail(f"plugin page missing {needle}") and ok
    for needle in ("build_card", "panel.py"):
        if needle not in page_text:
            ok = fail(f"plugin page missing panel dispatch {needle}") and ok
    for feature_id in ORDINARY_FEATURES:
        if f'feature_id == "{feature_id}"' in page_text or f"feature_id == '{feature_id}'" in page_text:
            ok = fail(f"plugin page still branches on {feature_id}") and ok
    for needle in ("_build_weapon_tab", "_build_player_tab", "_build_other_tab", "_make_feature_card("):
        if needle in tabs_text:
            ok = fail(f"feature_tabs_view still contains {needle}") and ok
    for needle in ("@dataclass", "class FeatureTabsHandles", "FeatureTabsHandles("):
        if needle in tabs_text:
            ok = fail(f"feature_tabs_view still has fixed handles: {needle}") and ok
    for needle in (
        "on_knife_speed_change",
        "on_move_speed_change",
        "on_range_change",
        "on_timescale_change",
        "on_gravity_change",
        "on_jump_change",
        "on_gravity_mode_change",
        "on_gather",
        "on_skip_round",
    ):
        if needle in tabs_text:
            ok = fail(f"feature_tabs_view still has fixed callback {needle}") and ok
    for needle in ('"set_config"', '"action"'):
        if needle not in tabs_text:
            ok = fail(f"feature_tabs_view missing generic callback {needle}") and ok
    for needle in ('callbacks["set_config"]', 'callbacks["action"]'):
        if needle not in page_text:
            ok = fail(f"plugin page missing generic callback {needle}") and ok
    if 'callbacks["slider"]' in page_text:
        ok = fail("plugin page still uses fixed slider callback map") and ok
    if "isinstance(handles, dict)" not in common_text:
        ok = fail("bind_view_handles does not support dict handles") and ok
    for needle in ("def set_feature_config", "def trigger_feature_action"):
        if needle not in controller_text:
            ok = fail(f"FeatureActionController missing {needle}") and ok
    return ok


def check_runtime_boundary():
    service_text = (ROOT / "core" / "services" / "feature_command_service.py").read_text(encoding="utf-8")
    frida_text = (ROOT / "core" / "frida_manager.py").read_text(encoding="utf-8")
    ok = True
    if "Agent v1.8" in frida_text or "Agent v1.9" not in frida_text:
        ok = fail("Frida Agent version log is not v1.9") and ok
    for feature_id in ORDINARY_FEATURES:
        if f'"{feature_id}"' in service_text or f"'{feature_id}'" in service_text:
            ok = fail(f"FeatureCommandService has feature branch for {feature_id}") and ok
        if feature_id != "esp_box" and f"modules.{feature_id}" in frida_text:
            ok = fail(f"FridaManager dispatcher still references modules.{feature_id}") and ok
    return ok


def check_startup_boundary():
    ok = True
    main_text = (ROOT / "main.py").read_text(encoding="utf-8")
    init_text = (ROOT / "features" / "__init__.py").read_text(encoding="utf-8")
    window_contract = (ROOT / "ui" / "window_contract.py").read_text(encoding="utf-8")
    if "import features" in main_text:
        ok = fail("main.py still imports features") and ok
    if 'APP_VERSION = "v1.9"' not in window_contract:
        ok = fail("APP_VERSION is not v1.9") and ok
    for source_name in ORDINARY_SOURCES.values():
        if Path(source_name).stem in init_text:
            ok = fail(f"features/__init__.py still manually imports {source_name}") and ok
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
        check_startup_boundary(),
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
