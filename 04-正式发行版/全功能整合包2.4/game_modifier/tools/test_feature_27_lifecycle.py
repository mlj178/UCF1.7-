import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FEATURES = ROOT / "features"
MANIFEST = FEATURES / "27_game_mode_override" / "manifest.json"
APP = ROOT / "ui" / "app.py"
RELEASE_ROOT = ROOT.parents[1]
PERSISTENCE_DOC = RELEASE_ROOT / "功能开关与参数持久化记录.md"
INTEGRATION_SPEC = RELEASE_ROOT / "00-正式发行版功能接入规范.md"
PROGRAM_SPEC = RELEASE_ROOT / "程序规范.md"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path):
    return path.read_text(encoding="utf-8")


class MemoryFeatureStateRepo:
    def __init__(self, payload=None):
        self.payload = dict(payload or {})

    def load(self):
        return dict(self.payload)

    def save(self, payload):
        self.payload = dict(payload)


class MemoryDesiredStateRepo:
    def __init__(self, payload=None):
        self.payload = dict(payload or {})

    def load(self):
        return dict(self.payload)

    def save(self, payload):
        self.payload = dict(payload)


class RecordingConfigManager:
    def __init__(self, initial=None):
        self.payload = dict(initial or {})
        self.writes = []
        self.removed_keys = []

    def get(self, feature_id, default=None):
        return dict(self.payload.get(feature_id, default or {}))

    def set(self, feature_id, config):
        self.writes.append((feature_id, dict(config or {})))
        current = self.get(feature_id)
        current.update(config or {})
        self.payload[feature_id] = current
        return dict(current)

    def remove_user_key(self, feature_id, key):
        self.removed_keys.append((feature_id, key))
        current = self.get(feature_id)
        current.pop(key, None)
        self.payload[feature_id] = current
        return dict(current)


class RecordingFridaManager:
    def __init__(self):
        self.calls = []

    def plugin_call(self, feature_id, action, payload=None):
        self.calls.append((feature_id, action, dict(payload or {})))
        return {"ok": True}


class Feature27LifecycleTests(unittest.TestCase):
    def test_game_mode_keeps_mode_key_but_does_not_restore_enabled_switch(self):
        manifest = read_json(MANIFEST)

        self.assertEqual(manifest["feature_id"], "27_game_mode_override")
        self.assertEqual(manifest["canonical_id"], "game_mode_override")
        self.assertIn("mode_key", manifest["config"])
        self.assertEqual(manifest["config"]["enabled"], False)
        self.assertFalse(manifest["state"]["sync_enabled_from_config"])
        self.assertFalse(manifest["lifecycle"]["restore"])

    def test_app_syncs_select_controls_from_saved_config(self):
        text = read_text(APP)

        self.assertIn('control_type not in {"combo", "select"}', text)
        self.assertIn('handle_type = "select" if control_type == "select" else "combo_var"', text)
        self.assertIn('handles.get(f"{key}_select")', text)

    def test_special_manual_features_keep_params_but_do_not_auto_restore_switch(self):
        expected = {
            "18_esp_box": "esp_box",
            "25_free_camera": "free_camera",
            "26_grenade_mode": "grenade_mode_lock999_keep_weapon_tuner",
        }

        for dirname, feature_id in expected.items():
            with self.subTest(dirname=dirname):
                manifest = read_json(FEATURES / dirname / "manifest.json")
                self.assertEqual(manifest["feature_id"], feature_id)
                self.assertFalse(manifest["state"]["sync_enabled_from_config"])
                self.assertFalse(manifest["lifecycle"]["restore"])

    def test_persistence_record_doc_and_integration_spec_are_kept_in_sync(self):
        doc = read_text(PERSISTENCE_DOC)
        spec = read_text(INTEGRATION_SPEC)
        program_spec = read_text(PROGRAM_SPEC)

        self.assertIn("# 功能开关与参数持久化记录", doc)
        for feature_name in ("自由视角", "手雷模式", "方框透视", "游戏模式切换", "调整伤害倍率"):
            self.assertIn(feature_name, doc)
        self.assertIn("新增或迁移功能时，必须同步更新", spec)
        self.assertIn("功能开关与参数持久化记录.md", spec)
        for feature_id in ("free_camera", "grenade_mode_lock999_keep_weapon_tuner", "27_game_mode_override"):
            self.assertIn(feature_id, program_spec)

    def test_persistence_record_is_indexed_and_old_enabled_rules_are_removed(self):
        spec = read_text(INTEGRATION_SPEC)
        program_spec = read_text(PROGRAM_SPEC)

        for text in (spec, program_spec):
            self.assertIn("功能开关与参数持久化记录.md", text)
            self.assertIn("data/user_config.json", text)
            self.assertIn("data/feature_state.json", text)
            self.assertIn("普通开关", text)

        stale_rules = (
            "user_config.json 会记录上一次程序运行时各功能的 `enabled` 状态",
            "用 `user_config.json` 覆盖需要同步的功能状态",
            "enable 时先保存 enabled=true",
            "中心 UI 只负责保存 enabled",
            "user_config.json 记录并恢复 `enabled`",
        )
        for stale in stale_rules:
            with self.subTest(stale=stale):
                self.assertNotIn(stale, spec)
                self.assertNotIn(stale, program_spec)

    def test_persistence_doc_records_esp_desired_state_special_case(self):
        doc = read_text(PERSISTENCE_DOC)

        self.assertIn("ESP 特殊 desired state", doc)
        self.assertIn("desired_states.json", doc)
        self.assertIn("18-方框透视", doc)

    def test_feature_state_only_loads_and_saves_restorable_switches(self):
        from core.services.app_persistence_service import AppPersistenceService

        feature_repo = MemoryFeatureStateRepo(
            {
                "free_camera": {"enabled": True},
                "damage_multiplier": {"enabled": True},
            }
        )
        desired_repo = MemoryDesiredStateRepo()
        service = AppPersistenceService(
            feature_state_repo=feature_repo,
            desired_state_repo=desired_repo,
        )

        state = service.load_app_state(
            ["free_camera", "damage_multiplier"],
            restorable_feature_ids={"damage_multiplier"},
        )

        self.assertFalse(state.features["free_camera"])
        self.assertTrue(state.features["damage_multiplier"])

        state.features["free_camera"] = True
        state.features["damage_multiplier"] = True
        service.save_app_state(state, restorable_feature_ids={"damage_multiplier"})

        self.assertNotIn("free_camera", feature_repo.payload)
        self.assertEqual(feature_repo.payload["damage_multiplier"], {"enabled": True})

    def test_normal_feature_commands_do_not_persist_enabled_in_user_config(self):
        from core.services.feature_command_service import FeatureCommandService

        config = RecordingConfigManager(
            {"free_camera": {"enabled": True, "moveSpeed": 30.0}}
        )
        frida = RecordingFridaManager()
        service = FeatureCommandService(frida, config)

        service.enable("free_camera")
        service.disable("free_camera")

        self.assertNotIn(("free_camera", {"enabled": True}), config.writes)
        self.assertNotIn(("free_camera", {"enabled": False}), config.writes)
        self.assertEqual(
            config.removed_keys,
            [("free_camera", "enabled"), ("free_camera", "enabled")],
        )
        self.assertEqual(
            frida.calls,
            [
                ("free_camera", "enable", {"moveSpeed": 30.0}),
                ("free_camera", "disable", {}),
            ],
        )


if __name__ == "__main__":
    unittest.main()
