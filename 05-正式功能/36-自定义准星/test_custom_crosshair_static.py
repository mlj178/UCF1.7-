import pathlib
import unittest


FEATURE_DIR = pathlib.Path(__file__).parent
SCRIPT = FEATURE_DIR / "AAAAA-custom_crosshair_min.js"
UI = FEATURE_DIR / "AAAAA-custom_crosshair_ui.py"


class CustomCrosshairStaticTests(unittest.TestCase):
    def test_core_script_declares_verified_hud_crosshair_contract(self):
        text = SCRIPT.read_text(encoding="utf-8")

        required = (
            "FEATURE_ID = 'custom_crosshair'",
            "HudCrosshair_Awake: 0x00B049E0",
            "HudCrosshair_Update: 0x00B05390",
            "HudCrosshair_SetType: 0x00B05180",
            "HudCrosshair_OnDestroy: 0x00B05000",
            "HudCrosshair_crosshair1_horizontal: 0x20",
            "HudCrosshair_crosshair1_vertical: 0x24",
            "RectTransform_set_anchoredPosition_Injected: 0x004F4B60",
            "RectTransform_set_sizeDelta_Injected: 0x004F5060",
            "function applyConfiguredCrosshair",
            "function restoreOriginals",
            "function resetRuntime",
            "enable:function",
            "disable:function",
            "status:function",
            "cleanup:function",
            "setconfig:function",
        )
        for item in required:
            self.assertIn(item, text)

    def test_core_script_uses_post_update_reapply_and_lifecycle_cleanup(self):
        text = SCRIPT.read_text(encoding="utf-8")

        update_section = text.split("attachHook('HUD_Crosshair.Update'", 1)[1].split(
            "attachHook('HUD_Crosshair.SetType'", 1
        )[0]
        self.assertIn("onLeave", update_section)
        self.assertIn("applyConfiguredCrosshair", update_section)
        self.assertIn("attachHook('HUD_Crosshair.OnDestroy'", text)
        self.assertIn("resetRuntime('HUD_Crosshair.OnDestroy')", text)
        self.assertNotIn("Interceptor.replace", text)

    def test_rect_transform_calls_use_injected_vector2_abis(self):
        text = SCRIPT.read_text(encoding="utf-8")
        for item in (
            "RectTransform_get_anchoredPosition_Injected: 0x004F47D0",
            "RectTransform_get_sizeDelta_Injected: 0x004F4920",
            "RectTransform_set_anchoredPosition_Injected: 0x004F4B60",
            "RectTransform_set_sizeDelta_Injected: 0x004F5060",
            "RVA.RectTransform_get_anchoredPosition_Injected",
            "RVA.RectTransform_get_sizeDelta_Injected",
            "RVA.RectTransform_set_anchoredPosition_Injected",
            "RVA.RectTransform_set_sizeDelta_Injected",
            "getPos(rt, v2, ptr(0))",
            "getSize(rt, v2, ptr(0))",
        ):
            self.assertIn(item, text)

    def test_graphic_color_uses_by_value_color_abi(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("Graphic_set_color),'void',['pointer','float','float','float','float','pointer']", text)
        self.assertIn("setColor(image,c.r,c.g,c.b,c.a,ptr(0))", text)
        self.assertNotIn("setColor(image,color,ptr(0))", text)
        self.assertIn("Graphic.set_color wrote", text)

    def test_probe_enumerates_direct_and_child_graphic_candidates(self):
        text = SCRIPT.read_text(encoding="utf-8")
        for item in (
            "Component_GetComponentInChildren: 0x0032CC90",
            "function resolveUiType",
            "function inspectGraphicTargets",
            "getComponentInChildren(rt,type,1,ptr(0))",
            "['UnityEngine.UI','Image']",
            "['UnityEngine.UI','RawImage']",
            "['UnityEngine.UI','Graphic']",
            "graphic_candidates",
        ):
            self.assertIn(item, text)

    def test_probe_walks_ancestor_transforms_for_graphics(self):
        text = SCRIPT.read_text(encoding="utf-8")
        for item in (
            "Transform_get_parent: 0x003F31D0",
            "function inspectAncestorTargets",
            "getParent(cursor,ptr(0))",
            "ancestor_graphic_candidates",
        ):
            self.assertIn(item, text)

    def test_probe_covers_non_ugui_renderers_and_all_crosshair_objects(self):
        text = SCRIPT.read_text(encoding="utf-8")
        for item in (
            "HudCrosshair_allCrosshair: 0x1C",
            "GameObject_GetComponent: 0x00331C10",
            "GameObject_GetComponentInChildren: 0x00331B80",
            "function resolveType",
            "'CanvasRenderer'",
            "'SpriteRenderer'",
            "'MeshRenderer'",
            "function inspectAllCrosshair",
            "all_crosshair",
        ):
            self.assertIn(item, text)

    def test_probe_enumerates_actual_component_class_names(self):
        text = SCRIPT.read_text(encoding="utf-8")
        for item in (
            "GameObject_GetComponentsInternal: 0x00331C40",
            "function enumerateComponents",
            "il2cpp_object_get_class",
            "il2cpp_class_get_name",
            "il2cpp_class_get_namespace",
            "actual_components",
        ):
            self.assertIn(item, text)

    def test_ui_uses_only_standard_rpc_and_exposes_core_settings(self):
        text = UI.read_text(encoding="utf-8")

        for item in (
            "customtkinter",
            "enable",
            "disable",
            "status",
            "cleanup",
            "setconfig",
            "offset_x",
            "offset_y",
            "scale",
            "DEFAULT_CONFIG",
        ):
            self.assertIn(item, text)

    def test_ui_does_not_shadow_ctk_window_state_method(self):
        text = UI.read_text(encoding="utf-8")
        self.assertNotIn("self.state=", text)
        self.assertIn("self.status_label", text)

    def test_ui_has_game_attach_and_reconnect_flow(self):
        text = UI.read_text(encoding="utf-8")
        for item in (
            "import frida",
            "psutil",
            "GAME_PROCESS_NAME = \"UnityCrossFire.exe\"",
            "def find_game_pid",
            "frida.attach(pid)",
            "session.create_script",
            "script.load()",
            "def _connect_worker",
            "def _on_frida_detached",
            "exports_sync.status()",
            "exports_sync.cleanup()",
        ):
            self.assertIn(item, text)

    def test_runtime_probe_is_available_and_ui_surfaces_its_log(self):
        script = SCRIPT.read_text(encoding="utf-8")
        ui = UI.read_text(encoding="utf-8")

        for item in (
            "RectTransform_get_anchoredPosition",
            "RectTransform_get_sizeDelta",
            "function buildProbeSnapshot",
            "debugdump:function",
            "HUD_Crosshair.Update first hit",
            "probe:",
        ):
            self.assertIn(item, script)
        for item in (
            "def run_probe",
            "exports_sync.debugdump()",
            "message.get(\"type\")==\"send\"",
            "CTkTextbox",
            "[custom_crosshair]",
        ):
            self.assertIn(item, ui)

    def test_ui_persists_and_analyzes_probe_log(self):
        text = UI.read_text(encoding="utf-8")
        for item in (
            'LOG_PATH = pathlib.Path(__file__).with_name("custom_crosshair.log")',
            "def append_log",
            "LOG_PATH.open(\"a\", encoding=\"utf-8\")",
            "def analyze_saved_log",
            "LOG_PATH.read_text(encoding=\"utf-8\")",
            "ast.literal_eval",
            "command=self.analyze_saved_log",
        ):
            self.assertIn(item, text)

    def test_ui_auto_runs_probe_after_hud_first_hit(self):
        text = UI.read_text(encoding="utf-8")
        self.assertIn('"HUD_Crosshair.Update first hit"', text)
        self.assertIn('("auto_probe",None)', text)
        self.assertIn('elif kind=="auto_probe": self.run_probe()', text)

    def test_large_probe_is_saved_off_the_ui_thread_as_json(self):
        text = UI.read_text(encoding="utf-8")
        for item in (
            'PROBE_PATH = pathlib.Path(__file__).with_name("custom_crosshair_probe.json")',
            'PROBE_PATH.write_text(json.dumps(snapshot, ensure_ascii=False), encoding="utf-8")',
            'PROBE_PATH.read_text(encoding="utf-8")',
            'def trim_log_box',
        ):
            self.assertIn(item, text)
        script = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("log('probe: '+JSON.stringify(snapshot))", script)


if __name__ == "__main__":
    unittest.main()
