import json
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = Path(r"D:\trae_project\ucf1.7-modifier\05-正式功能\18-Universal-ESP盒子\Universal-Dear-ImGui-Hook")


class EspTargetScopeStaticTests(unittest.TestCase):
    def test_manifest_has_enemy_only_default(self):
        manifest = json.loads((Path(__file__).parent / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["config"]["esp_target_scope"], "enemy_only")

    def test_panel_has_single_target_scope_dropdown(self):
        panel = (Path(__file__).parent / "panel.py").read_text(encoding="utf-8")
        self.assertIn("CTkComboBox", panel)
        self.assertIn("仅显示敌人", panel)
        self.assertIn("敌人和队友", panel)
        self.assertIn("esp_target_scope", panel)

    def test_config_callback_is_available_to_custom_panels(self):
        feature_tabs = (PACKAGE_ROOT / "ui" / "views" / "feature_tabs_view.py").read_text(encoding="utf-8")
        tab_builder = (PACKAGE_ROOT / "ui" / "views" / "plugin_tab_builder.py").read_text(encoding="utf-8")
        self.assertIn("on_get_config", feature_tabs)
        self.assertIn("get_config", feature_tabs)
        self.assertIn("on_get_config", tab_builder)

    def test_python_live_sync_path_exists(self):
        router = (PACKAGE_ROOT / "ui" / "controllers" / "action_router.py").read_text(encoding="utf-8")
        manager = (PACKAGE_ROOT / "core" / "universal_hook_manager.py").read_text(encoding="utf-8")
        session = (PACKAGE_ROOT / "core" / "game_session_manager.py").read_text(encoding="utf-8")
        service = (PACKAGE_ROOT / "core" / "services" / "feature_command_service.py").read_text(encoding="utf-8")
        self.assertIn('feature_id == "esp_box"', router)
        self.assertIn("set_esp_state", manager)
        self.assertIn("set_esp_target_scope", manager)
        self.assertIn("esp_all_players", manager)
        self.assertIn("set_esp_target_scope", session)
        self.assertIn("set_esp_state", session)
        self.assertIn("set_esp_target_scope", service)

    def test_native_state_and_pipe_support_target_scope(self):
        state = (SOURCE_ROOT / "esp" / "esp_state.h").read_text(encoding="utf-8")
        pipe = (SOURCE_ROOT / "esp" / "named_pipe_server.cpp").read_text(encoding="utf-8")
        renderer = (SOURCE_ROOT / "esp" / "esp_renderer.cpp").read_text(encoding="utf-8")
        self.assertIn("IsAllPlayersEnabled", state)
        self.assertIn("SetState", state)
        self.assertIn("esp_all_players", pipe)
        self.assertIn("IsAllPlayersEnabled", renderer)
        self.assertIn("GameManager::IsEnemy", renderer)
        self.assertNotIn(
            "GetPlayerTeam(player) == GameManager::GetPlayerTeam(localPlayer)",
            renderer,
        )

    def test_manifest_and_panel_have_health_options(self):
        manifest = json.loads((Path(__file__).parent / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["config"]["esp_health_mode"], "percent")
        self.assertEqual(manifest["config"]["esp_health_display"], "both")

        panel = (Path(__file__).parent / "panel.py").read_text(encoding="utf-8")
        self.assertIn("百分比", panel)
        self.assertIn("剩余数值", panel)
        self.assertIn("仅血条", panel)
        self.assertIn("仅数值", panel)
        self.assertIn("血条和数值", panel)
        self.assertIn("esp_health_mode", panel)
        self.assertIn("esp_health_display", panel)

    def test_python_live_sync_path_has_health_options(self):
        manager = (PACKAGE_ROOT / "core" / "universal_hook_manager.py").read_text(encoding="utf-8")
        session = (PACKAGE_ROOT / "core" / "game_session_manager.py").read_text(encoding="utf-8")
        service = (PACKAGE_ROOT / "core" / "services" / "feature_command_service.py").read_text(encoding="utf-8")
        self.assertIn("set_esp_health_options", manager)
        self.assertIn("esp_health_mode", manager)
        self.assertIn("esp_health_display", manager)
        self.assertIn("set_esp_health_options", session)
        self.assertIn("set_esp_health_options", service)

    def test_native_state_and_pipe_support_health_options(self):
        state = (SOURCE_ROOT / "esp" / "esp_state.h").read_text(encoding="utf-8")
        pipe = (SOURCE_ROOT / "esp" / "named_pipe_server.cpp").read_text(encoding="utf-8")
        renderer = (SOURCE_ROOT / "esp" / "esp_renderer.cpp").read_text(encoding="utf-8")
        game_manager = (SOURCE_ROOT / "esp" / "game_manager.cpp").read_text(encoding="utf-8")
        self.assertIn("GetHealthMode", state)
        self.assertIn("GetHealthDisplay", state)
        self.assertIn("esp_health_mode", pipe)
        self.assertIn("esp_health_display", pipe)
        self.assertIn("DrawHealthOverlay", renderer)
        self.assertIn("MODE_VALUE", renderer)
        self.assertIn("ObscuredInt_hidden", game_manager)

    def test_gameassembly_minhook_hooks_are_removed(self):
        """DLL 不得再对 GameAssembly 函数打 MinHook（双引擎重复挂钩闪退修复）。"""
        game_manager = (SOURCE_ROOT / "esp" / "game_manager.cpp").read_text(encoding="utf-8")
        renderer = (SOURCE_ROOT / "esp" / "esp_renderer.cpp").read_text(encoding="utf-8")
        # 注释里会记录“已删除的旧钩子及其 RVA”，因此这里校验的是“没有任何挂钩调用”。
        self.assertNotIn("MH_CreateHook", game_manager)
        self.assertNotIn("MH_EnableHook", game_manager)
        self.assertNotIn("HookedBotUpdate", game_manager)
        self.assertNotIn("HookedRoundStart", game_manager)
        self.assertNotIn("HookedNanoRoundStart", game_manager)
        self.assertNotIn("HookedGameDestroy", game_manager)
        # esp_renderer.cpp 的修复说明注释里会提到旧函数名，这里只校验“没有真正调用”。
        self.assertNotIn("GameManager::InitializeBotHook();", renderer)
        self.assertNotIn("GameManager::InitializeRoomHooks();", renderer)


if __name__ == "__main__":
    unittest.main()
