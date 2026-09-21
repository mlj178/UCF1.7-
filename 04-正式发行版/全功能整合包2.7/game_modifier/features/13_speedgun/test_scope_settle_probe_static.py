import pathlib
import unittest


BASE_DIR = pathlib.Path(__file__).resolve().parent
JS_FILE = BASE_DIR / "script.js"


class ScopeSettleProbeStaticTests(unittest.TestCase):
    def test_speedgun_contains_read_only_scope_settle_probe(self):
        text = JS_FILE.read_text(encoding="utf-8")

        for marker in (
            "ScopeSettleProbe",
            "scopeSettleProbeIntervalsMs",
            "scheduleScopeSettleProbe",
            "collectScopeSettleSnapshot",
            "ScopeSettleProbe candidate",
            "0, 150, 350, 750, 1200, 1800, 2200",
        ):
            self.assertIn(marker, text)

    def test_probe_only_reads_candidate_memory(self):
        text = JS_FILE.read_text(encoding="utf-8")
        probe_block = text.split("// ===== ScopeSettleProbe", 1)[1].split("// ===== 开镜即时稳定修正", 1)[0]

        self.assertIn("readFloat", probe_block)
        self.assertNotIn("writeFloat", probe_block)
        self.assertNotIn("writeS32", probe_block)
        self.assertNotIn("writeU8", probe_block)

    def test_probe_starts_from_runtime_discovered_zoom_methods(self):
        text = JS_FILE.read_text(encoding="utf-8")
        for marker in (
            "installScopeSettleZoomMethodHooks",
            "il2cpp_domain_get",
            "il2cpp_class_get_methods",
            "WPN_Gun",
            "zoom_method",
            "discoverScopeSettleObjects",
            "scopeObject",
        ):
            self.assertIn(marker, text)

    def test_shot_fallback_freezes_this_shots_recoil_pointer(self):
        text = JS_FILE.read_text(encoding="utf-8")
        for marker in (
            "pendingScopeSettleWeapon",
            "scheduleScopeSettleProbe(pendingScopeSettleWeapon, 'shoot_ray', args[1])",
            "frozenRecoil",
            "collectScopeSettleSnapshot(weapon, frozenRecoil)",
            "scopeObject+0x",
        ):
            self.assertIn(marker, text)

    def test_probe_records_final_local_shot_ray_without_writing_it(self):
        text = JS_FILE.read_text(encoding="utf-8")
        for marker in (
            "readScopeRayDirection",
            "ScopeSettleProbe final_ray",
            "this.retBuffer = args[0]",
            "direction.x = retBuffer.add(0x0C).readFloat()",
        ):
            self.assertIn(marker, text)

    def test_scope_correction_writes_final_local_ray_from_camera_forward(self):
        text = JS_FILE.read_text(encoding="utf-8")

        for marker in (
            "applyInstantScopeStability",
            "cacheScopeCamera",
            "readScopeCameraForward",
            "Brain.PushStateToUnityCamera",
            "ScopeSettleCorrection applied",
            "retBuffer.add(0x0C).writeFloat(direction.x)",
            "retBuffer.add(0x10).writeFloat(direction.y)",
            "retBuffer.add(0x14).writeFloat(direction.z)",
        ):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
