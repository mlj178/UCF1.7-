import pathlib
import unittest


BASE_DIR = pathlib.Path(__file__).resolve().parent
JS_FILE = BASE_DIR / "script.js"
UI_FILE = BASE_DIR / "panel.py"
MANIFEST_FILE = BASE_DIR / "manifest.json"


class BrightnessProbeStaticTests(unittest.TestCase):
    def test_expected_files_exist(self):
        self.assertTrue(JS_FILE.exists())
        self.assertTrue(UI_FILE.exists())
        self.assertTrue(MANIFEST_FILE.exists())

    def test_js_exports_standard_and_probe_rpc(self):
        text = JS_FILE.read_text(encoding="utf-8")
        self.assertIn('feature_id: "brightness_probe"', text)
        for name in (
            "enable",
            "disable",
            "status",
            "cleanup",
            "setConfig",
            "setconfig",
            "applyBrightness",
            "applybrightness",
            "resetBrightness",
            "resetbrightness",
        ):
            self.assertIn(f"{name}(", text)
        self.assertNotIn("diagnose() {", text)
        self.assertNotIn("return diagnose();", text)

    def test_js_records_reverse_engineering_constants(self):
        text = JS_FILE.read_text(encoding="utf-8")
        for marker in (
            "Camera_get_main: 0x00328310",
            "CameraExtensions_GetUniversalAdditionalCameraData: 0x00490500",
            "CameraExtensions_UpdateVolumeStack: 0x00490820",
            "VolumeStack_GetComponent_ColorAdjustments: 0x007D3570",
            "MethodInfo_VolumeStack_GetComponent_ColorAdjustments: 0x00E24EEC",
            "VolumeStack_GetComponent_LiftGammaGain: 0x007D3570",
            "MethodInfo_VolumeStack_GetComponent_LiftGammaGain: 0x00E24FE8",
            "UniversalAdditionalCameraData_volumeStack: 0x4C",
            "ColorAdjustments_postExposure: 0x1C",
            "ColorAdjustments_contrast: 0x20",
            "ColorAdjustments_saturation: 0x2C",
            "LiftGammaGain_gamma: 0x20",
            "LiftGammaGain_gain: 0x24",
            "VolumeParameter_overrideState: 0x08",
            "VolumeParameter_floatValue: 0x0C",
            "CameraManager_TypeInfo: 0x00E263C0",
            "CameraManager_volumeProfile: 0x10",
            "VolumeProfile_components: 0x0C",
            "List_items: 0x08",
            "cameraManagerVolumeProfile",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("LiftGammaGain_lift", text)
        self.assertNotIn("force_render_post_processing", text)
        self.assertNotIn("renderPostProcessing", text)
        self.assertNotIn("Interceptor.replace", text)

    def test_js_can_apply_via_camera_manager_volume_profile(self):
        text = JS_FILE.read_text(encoding="utf-8")
        for marker in (
            "locateProfileColorAdjustments",
            "locateLiftGammaGain",
            "readIl2CppClassName",
            "readVector4Param",
            "writeVector4Param",
            'componentName === "ColorAdjustments"',
            'componentName === "LiftGammaGain"',
            'source: "camera_manager_volume_profile"',
            '"ColorAdjustments located via CameraManager.volumeProfile"',
            "profileComponents",
        ):
            self.assertIn(marker, text)

    def test_ui_uses_standard_script_and_probe_actions(self):
        text = UI_FILE.read_text(encoding="utf-8")
        manifest = MANIFEST_FILE.read_text(encoding="utf-8")
        self.assertIn("customtkinter", text)
        self.assertIn('"script": "script.js"', manifest)
        for marker in ("applybrightness", "resetbrightness", "setconfig"):
            self.assertIn(marker, text)
        for marker in ("saturation", "gamma", "gain", "恢复游戏初始值"):
            self.assertIn(marker, text)
        for marker in ("diagnose_button", "def _diagnose", "\"diagnose\"", "lift_slider", "\"lift\""):
            self.assertNotIn(marker, text)
        self.assertNotIn('"applyBrightness"', text)
        self.assertNotIn('"resetBrightness"', text)
        self.assertNotIn('"setConfig"', text)
        self.assertNotIn("overlay", text.lower())

    def test_ui_sequences_dependent_rpc_calls(self):
        text = UI_FILE.read_text(encoding="utf-8")
        self.assertIn('callbacks["action"](feature_id, "setconfig"', text)
        self.assertIn('callbacks["action"](feature_id, "applybrightness"', text)
        for marker in ("等待连接游戏", "需连接游戏", "已发送应用请求", "应用失败", "恢复失败", "强制开启相机后处理"):
            self.assertNotIn(marker, text)

    def test_manifest_declares_2_4_parameter_card(self):
        import json

        manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
        self.assertEqual(manifest["feature_id"], "brightness_probe")
        self.assertEqual(manifest["tab"], "game_parameters_tab")
        self.assertEqual(manifest["desc"], "")
        self.assertEqual(manifest["layout"]["columnspan"], 2)
        self.assertFalse(manifest["lifecycle"]["restore"])
        self.assertNotIn("force_render_post_processing", json.dumps(manifest, ensure_ascii=False))
        controls = {item.get("key", item.get("action")): item for item in manifest["controls"]}
        self.assertEqual(controls["exposure"]["default"], 1.5)
        self.assertEqual(controls["contrast"]["min"], -50.0)
        self.assertEqual(controls["saturation"]["max"], 100.0)
        self.assertEqual(controls["applybrightness"]["type"], "button")


if __name__ == "__main__":
    unittest.main()
