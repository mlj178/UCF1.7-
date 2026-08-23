import pathlib
import unittest


BASE_DIR = pathlib.Path(__file__).resolve().parent
JS_FILE = BASE_DIR / "AAAAA-healthbar_prefab_probe_min.js"
UI_FILE = BASE_DIR / "AAAAA-healthbar_prefab_probe_ui.py"
DOC_FILE = BASE_DIR / "血条Prefab探针-简要说明.md"


class HealthBarPrefabProbeStaticTests(unittest.TestCase):
    def test_expected_files_exist(self):
        self.assertTrue(JS_FILE.exists())
        self.assertTrue(UI_FILE.exists())
        self.assertTrue(DOC_FILE.exists())

    def test_js_records_verified_rvas_and_offsets(self):
        text = JS_FILE.read_text(encoding="utf-8")
        for marker in (
            "HUD_ProjectionID_Awake: 0x00AD9910",
            "HUD_ProjectionID_GetSign: 0x00AD9980",
            "HUD_Tombstone_AddHealthBar: 0x00AE1210",
            "HUD_Tombstone_Update: 0x00AE18C0",
            "SentryGun_AddHealthBar: 0x00B1C8C0",
            "GameObject_GetComponent_Type: 0x00331C10",
            "Object_GetInstanceID: 0x004E96C0",
            "Object_get_name: 0x004EA1B0",
            "GameObject_get_activeInHierarchy: 0x00331F20",
            "GameObject_get_activeSelf: 0x00331F50",
            "HUD_HealthBar_Bind: 0x00B07290",
            "RecyclableObject_Active: 0x00B1A500",
            "HUD_ProjectionSign_Recycle: 0x00AD9AD0",
            "Player_get_isMyPlayer: 0x00B55FD0",
            "Entity_get_isDead: 0x00B400E0",
            "GameManager_TypeInfo: 0x00E2933C",
            "HUD_Tombstone_otherBarPrefab: 0x0C",
            "HUD_HealthBar_entityName: 0x50",
            "HUD_HealthBar_bar: 0x54",
            "HUD_HealthBar_health: 0x58",
            "UnityObject_m_CachedPtr: 0x08",
            "Graphic_m_Material: 0x0C",
            "Image_m_Sprite: 0x80",
            "Image_m_OverrideSprite: 0x84",
            "GameManager_allPlayers: 0x1C",
            "Entity_healthData: 0x1C",
            "Il2CppArray_length: 0x0C",
            "Il2CppArray_items: 0x10",
        ):
            self.assertIn(marker, text)

    def test_active_test_is_explicit_queued_and_main_thread_consumed(self):
        text = JS_FILE.read_text(encoding="utf-8")
        for marker in (
            'pendingAction: ""',
            'function requestActiveTest(action)',
            'function consumePendingAction(hudTombstone)',
            'requestActiveTest("create")',
            'requestActiveTest("recycle")',
            'consumePendingAction(args[0])',
            'ACTIVE_TEST_REQUESTED',
            'ACTIVE_TEST_CREATED',
            'ACTIVE_TEST_RECYCLED',
            'ACTIVE_TEST_REJECTED',
            'native.hudProjectionGetSign(prefab, ptr(0))',
            'native.hudHealthBarBind(healthBar, targetInfo.player, ptr(0))',
            'native.recyclableObjectActive(healthBar, ptr(0))',
            'native.hudProjectionSignRecycle(healthBar, false, ptr(0))',
        ):
            self.assertIn(marker, text)

    def test_active_test_validates_target_and_returned_healthbar(self):
        text = JS_FILE.read_text(encoding="utf-8")
        self.assertIn("function findVisibleTargetPlayer()", text)
        self.assertIn("native.playerGetIsMyPlayer", text)
        self.assertIn("native.entityGetIsDead", text)
        self.assertIn('readClassName(healthBar) !== "HUD_HealthBar"', text)
        self.assertIn("OFF.Entity_healthData", text)
        self.assertIn("activeTestGeneration", text)

    def test_js_samples_and_runs_explicit_actions_on_hud_main_thread(self):
        text = JS_FILE.read_text(encoding="utf-8")
        self.assertIn("installHudTombstoneUpdateHook", text)
        self.assertIn("inspectHudTombstone", text)
        self.assertIn("snapshotSignature", text)
        self.assertIn("sample_interval_ms", text)
        self.assertIn('rawObjectInfo(this.prefab, "GetSign.prefab")', text)
        self.assertIn('rawObjectInfo(retval, "RecyclableObject")', text)
        self.assertIn('rawObjectInfo(retval, "HUD_HealthBar")', text)
        self.assertGreaterEqual(text.count("if (!this.probeEnabled || !Runtime.enabled) return;"), 3)
        self.assertIn("if (!Runtime.enabled) return;", text)
        self.assertNotIn("Interceptor.replace", text)
        self.assertNotIn("Module.findExportByName", text)
        self.assertNotIn("writePointer", text)
        self.assertNotIn("writeU8", text)

    def test_js_exports_standard_and_probe_rpc(self):
        text = JS_FILE.read_text(encoding="utf-8")
        self.assertIn('feature_id: "healthbar_prefab_probe"', text)
        for name in (
            "enable", "disable", "status", "cleanup", "setConfig", "setconfig",
            "reset", "debugDump", "debugdump",
        ):
            self.assertIn(f"{name}(", text)

    def test_ui_uses_customtkinter_and_standard_lifecycle(self):
        text = UI_FILE.read_text(encoding="utf-8")
        self.assertIn("customtkinter", text)
        self.assertIn("AAAAA-healthbar_prefab_probe_min.js", text)
        for marker in (
            "UnityCrossFire.exe", "setconfig", "enable", "disable", "status",
            "cleanup", "debugdump", "保存日志",
        ):
            self.assertIn(marker, text)
        self.assertIn("if enabled is not True:", text)
        self.assertIn("探针初始化失败", text)

    def test_ui_exposes_explicit_create_and_recycle_buttons(self):
        text = UI_FILE.read_text(encoding="utf-8")
        self.assertIn("主动生成测试血条", text)
        self.assertIn("回收测试血条", text)
        self.assertIn('self._call_rpc("createtestbar")', text)
        self.assertIn('self._call_rpc("recycletestbar")', text)

    def test_document_defines_required_fresh_match_timeline(self):
        text = DOC_FILE.read_text(encoding="utf-8")
        for marker in (
            "无墓碑对局", "出现墓碑前", "出现墓碑后", "PREFAB_SNAPSHOT",
            "TIMELINE", "日志回传", "主动生成测试血条", "ACTIVE_TEST_CREATED",
            "回收测试血条", "ACTIVE_TEST_RECYCLED",
        ):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
