import pathlib
import unittest


BASE_DIR = pathlib.Path(__file__).resolve().parent
JS_FILE = BASE_DIR / "AAAAA-brightness_probe_min.js"
UI_FILE = BASE_DIR / "AAAAA-brightness_probe_ui.py"
DOC_FILE = BASE_DIR / "亮度调节探针-经验记录.md"


class BrightnessProbeStaticTests(unittest.TestCase):
    def test_expected_files_exist(self):
        self.assertTrue(JS_FILE.exists())
        self.assertTrue(UI_FILE.exists())
        self.assertTrue(DOC_FILE.exists())

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
            "UniversalAdditionalCameraData_renderPostProcessing: 0x30",
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
        self.assertIn("customtkinter", text)
        self.assertIn("AAAAA-brightness_probe_min.js", text)
        for marker in ("applybrightness", "resetbrightness", "setconfig", "cleanup"):
            self.assertIn(marker, text)
        for marker in ("saturation_slider", "gamma_slider", "gain_slider", "恢复游戏初始值"):
            self.assertIn(marker, text)
        for marker in ("diagnose_button", "def _diagnose", "\"diagnose\"", "lift_slider", "\"lift\""):
            self.assertNotIn(marker, text)
        self.assertNotIn('"applyBrightness"', text)
        self.assertNotIn('"resetBrightness"', text)
        self.assertNotIn('"setConfig"', text)
        self.assertNotIn("overlay", text.lower())

    def test_ui_sequences_dependent_rpc_calls(self):
        text = UI_FILE.read_text(encoding="utf-8")
        self.assertIn("def _call_rpc_sequence", text)
        self.assertIn('("setconfig", self._current_config())', text)
        self.assertIn('("applybrightness", float(self.exposure_slider.get()))', text)

    def test_document_preserves_result_template(self):
        text = DOC_FILE.read_text(encoding="utf-8")
        for marker in (
            "目标",
            "探针位置",
            "关键依据",
            "运行方式",
            "游戏内实测记录",
            "后续判断",
            "覆盖层式提亮",
            "CameraManager.volumeProfile -> VolumeProfile.components -> ColorAdjustments",
            "ColorAdjustments.saturation",
            "LiftGammaGain.gamma",
            "LiftGammaGain.gain",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("LiftGammaGain.lift", text)


if __name__ == "__main__":
    unittest.main()
