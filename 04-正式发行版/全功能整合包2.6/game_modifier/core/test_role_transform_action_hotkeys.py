import importlib
import unittest
from unittest import mock
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
APP_FILE = PROJECT_DIR / "ui" / "app.py"
SETTINGS_FILE = PROJECT_DIR / "ui" / "settings_window.py"


class RoleTransformActionHotkeyTests(unittest.TestCase):
    def test_config_defines_four_distinct_role_transform_actions(self):
        config = importlib.import_module("core.config")
        actions = getattr(config, "ROLE_TRANSFORM_HOTKEY_ACTIONS", None)

        self.assertIsNotNone(actions)
        self.assertEqual(
            ("alt+q", "alt+w", "alt+e", "alt+r"),
            tuple(actions),
        )
        self.assertEqual(
            {
                "local_hero",
                "local_terminator",
                "bot_hero",
                "bot_terminator",
            },
            {item["payload"]["action"] for item in actions.values()},
        )
        self.assertTrue(
            all(
                item["feature_id"] == "role_transform"
                and item["action"] == "trigger"
                for item in actions.values()
            )
        )
        self.assertEqual(
            {
                "本地玩家：选择英雄",
                "本地玩家：选择超级终结者",
                "所有 Bot：随机英雄",
                "所有 Bot：随机超级终结者",
            },
            {item["label"] for item in actions.values()},
        )

    def test_settings_keeps_role_transform_actions_out_of_ctrl_dropdowns(self):
        source = SETTINGS_FILE.read_text(encoding="utf-8")

        self.assertNotIn("for action_binding in ROLE_TRANSFORM_HOTKEY_ACTIONS", source)
        self.assertIn("角色变身固定快捷键", source)
        self.assertIn("ROLE_TRANSFORM_HOTKEY_DISPLAY_NAMES", source)

    def test_hotkey_manager_allows_distinct_actions_and_deduplicates_same_action(self):
        manager_module = importlib.import_module("core.hotkey_manager")
        binding_key = getattr(manager_module, "binding_key", None)

        self.assertIsNotNone(binding_key)
        self.assertEqual("role_transform:local_hero", binding_key({
            "feature_id": "role_transform",
            "action": "trigger",
            "payload": {"action": "local_hero"},
        }))
        self.assertNotEqual(
            binding_key({
                "feature_id": "role_transform",
                "action": "trigger",
                "payload": {"action": "local_hero"},
            }),
            binding_key({
                "feature_id": "role_transform",
                "action": "trigger",
                "payload": {"action": "bot_hero"},
            }),
        )

    def test_hotkey_manager_rejects_role_transform_actions_in_ctrl_slots(self):
        manager_module = importlib.import_module("core.hotkey_manager")
        manager = manager_module.HotkeyManager.__new__(manager_module.HotkeyManager)
        manager._hotkeys = {"ctrl+1": None, "ctrl+2": None}
        local_hero = {
            "feature_id": "role_transform",
            "action": "trigger",
            "payload": {"action": "local_hero"},
        }
        bot_hero = {
            "feature_id": "role_transform",
            "action": "trigger",
            "payload": {"action": "bot_hero"},
        }

        self.assertFalse(manager.set_hotkey("ctrl+1", local_hero))
        self.assertFalse(manager.set_hotkey("ctrl+2", bot_hero))
        self.assertIsNone(manager.hotkeys["ctrl+1"])
        self.assertIsNone(manager.hotkeys["ctrl+2"])

    def test_hotkey_manager_removes_old_keyboard_handles_on_cleanup(self):
        manager_module = importlib.import_module("core.hotkey_manager")
        manager = manager_module.HotkeyManager.__new__(manager_module.HotkeyManager)
        first_handle = object()
        second_handle = object()

        class NativeListener:
            @staticmethod
            def stop():
                return None

        manager._native_hotkey_listener = NativeListener()
        manager._hotkey_handles = [first_handle, second_handle]

        with mock.patch("core.hotkey_manager.keyboard.remove_hotkey") as remove_hotkey:
            manager.cleanup()

        remove_hotkey.assert_has_calls([
            mock.call(first_handle),
            mock.call(second_handle),
        ])
        self.assertEqual([], manager._hotkey_handles)

    def test_app_forwards_role_transform_payload_to_trigger_action(self):
        source = APP_FILE.read_text(encoding="utf-8")

        self.assertIn("payload = feature_id.get(\"payload\")", source)
        self.assertIn(
            "trigger_feature_action(feature_id, action, payload)",
            source,
        )


if __name__ == "__main__":
    unittest.main()
