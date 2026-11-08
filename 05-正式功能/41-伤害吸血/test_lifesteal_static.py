"""伤害吸血（lifesteal）静态契约测试。

只做静态检查：文件结构、feature_id、RVA、RPC、配置键、实现红线。
运行：
    python -m unittest "05-正式功能\41-伤害吸血\test_lifesteal_static.py" -v
"""

import json
import re
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parents[1]
JS_PATH = BASE_DIR / "script.js"
MANIFEST_PATH = BASE_DIR / "manifest.json"

REQUIRED_RVA = {
    "Entity_OnEntityHurt": "0x00B3F470",
    "Player_OnEntityHurt": "0x00B516B0",
    "HealthData_Hurt": "0x00AE45B0",
    "HealthData_Heal": "0x00AE44F0",
    "HealthData_get_isDead": "0x00AE4830",
    "GameManager_TypeInfo": "0x00E2933C",
    "GameManager_GameRoundEnd": "0x00AFAA40",
    "GameManager_NewGameRoundStart": "0x00AEBCB0",
    "GameManager_OnDestroy": "0x00AEBD40",
}

SOURCE_CATEGORIES = (
    "gun_primary",
    "gun_secondary",
    "gun_stock",
    "knife",
    "grenade",
    "special",
    "infect",
)


class LifestealStructureTest(unittest.TestCase):
    def test_required_files_exist(self):
        for name in (
            "script.js",
            "manifest.json",
            "feature.py",
            "panel.py",
            "events.py",
            "__init__.py",
            "AAAAA-lifesteal_ui.py",
            "test_lifesteal_runtime.js",
        ):
            self.assertTrue((BASE_DIR / name).is_file(), name)

    def test_no_legacy_names(self):
        names = {p.name for p in BASE_DIR.iterdir()}
        self.assertFalse(any("_min.js" in n for n in names))
        self.assertNotIn("launcher.py", names)

    def test_manifest_identity(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(manifest["feature_id"], "lifesteal")
        self.assertEqual(manifest["canonical_id"], "lifesteal")
        self.assertEqual(manifest["display_name"], "伤害吸血")
        self.assertEqual(manifest["script"], "script.js")
        self.assertTrue(manifest["lifecycle"]["cleanup"])
        for rpc in ("enable", "disable", "status", "cleanup", "setConfig", "set_config", "setconfig"):
            self.assertIn(rpc, manifest["rpc"])

    def test_manifest_percent_slider(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        slider = next(
            c for c in manifest["controls"]
            if c.get("type") == "slider" and c.get("key") == "lifesteal_percent"
        )
        self.assertEqual(float(slider["min"]), 0.0)
        self.assertEqual(float(slider["max"]), 100.0)
        self.assertEqual(float(slider["default"]), 10.0)
        self.assertEqual(manifest["config"]["lifesteal_percent"], 10)

    def test_manifest_source_switches_match_config(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        controls = {c.get("key"): c for c in manifest["controls"] if c.get("type") == "switch"}
        for key in SOURCE_CATEGORIES:
            cfg_key = "src_" + key + "_enabled"
            self.assertIn(cfg_key, controls)
            self.assertIn(cfg_key, manifest["config"])
        self.assertFalse(manifest["config"]["src_infect_enabled"])
        self.assertTrue(manifest["config"]["only_enemy_victim"])


class LifestealJsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.js = JS_PATH.read_text(encoding="utf-8")

    def test_feature_id(self):
        self.assertIn('feature_id: \'lifesteal\'', self.js)

    def test_required_rva(self):
        for name, value in REQUIRED_RVA.items():
            self.assertRegex(
                self.js,
                re.escape(name) + r"\s*:\s*" + re.escape(value),
                msg=name,
            )

    def test_rpc_exports(self):
        for name in ("enable", "disable", "status", "cleanup", "setConfig", "set_config", "setconfig", "reset"):
            self.assertRegex(self.js, r"\b" + re.escape(name) + r"\s*:\s*function")

    def test_only_attach_no_replace(self):
        self.assertIn("Interceptor.attach", self.js)
        self.assertNotIn("Interceptor.replace", self.js)
        self.assertNotIn("Interceptor.revert", self.js)

    def test_damage_event_on_stack(self):
        self.assertIn("stackContext.esp.add(8)", self.js)

    def test_hurt_is_the_actual_damage_stage(self):
        self.assertIn("HealthData_Hurt: 0x00AE45B0", self.js)
        self.assertIn("HealthData_Heal: 0x00AE44F0", self.js)
        self.assertIn("native.heal(", self.js)
        # 不允许抬上限式的加血；吸血必须封顶在 maxHealth。
        self.assertNotIn("AddHealthMax", self.js)

    def test_never_writes_health_fields_directly(self):
        # 本功能只读 ObscuredInt；写血量必须走 HealthData.Heal。
        self.assertNotIn("writeFloat(", self.js)
        self.assertNotIn("writeS32(", self.js)
        self.assertNotIn("writeU8(", self.js)
        self.assertNotIn("writeU32(", self.js)

    def test_percent_clamp(self):
        self.assertIn("clampFloat(Runtime.config.lifesteal_percent, 0.0, 100.0)", self.js)

    def test_lifecycle_reset(self):
        self.assertIn("function resetRuntime(reason)", self.js)
        self.assertIn("Runtime.contexts = []", self.js)
        self.assertIn("Runtime.pendingHeal = 0.0", self.js)
        for name in ("GameManager_GameRoundEnd", "GameManager_NewGameRoundStart", "GameManager_OnDestroy"):
            self.assertIn(name, self.js)

    def test_category_config_keys(self):
        for key in SOURCE_CATEGORIES:
            self.assertIn("src_" + key + "_enabled", self.js)

    def test_self_and_mate_victim_guard(self):
        self.assertIn("skippedSelfVictim", self.js)
        self.assertIn("skippedMateVictim", self.js)
        self.assertIn("only_enemy_victim", self.js)

    def test_no_hardcoded_ui(self):
        # JS 只能通过 setConfig 接收配置，不能直接读 UI。
        self.assertNotIn("customtkinter", self.js)

    def test_local_player_is_pure_memory_read(self):
        """本地玩家必须读 GameManager.myPlayer 静态字段，不能调游戏托管方法。

        背景：get_isMyPlayer 内部就是 Object.op_Equality(GameManager.myPlayer, this)，
        但它是托管方法，从 Frida RPC 线程调用属于 2.7 修过的“错误线程调游戏函数”。
        """
        self.assertIn("function readStaticMyPlayer()", self.js)
        self.assertIn("GameManager_TypeInfo", self.js)
        self.assertIn("Il2CppClass_staticFields", self.js)
        self.assertIn("GameManager_myPlayer", self.js)
        self.assertNotIn("native.isMyPlayer", self.js)
        self.assertNotIn("singletonGetter", self.js)
        self.assertNotIn("Player_get_isMyPlayer", self.js)

    def test_no_shared_hook_with_grenade_mode(self):
        """不能再 Hook 26 手雷模式用到的地址，否则两个功能在同一函数上叠加监听。

        0x00B663C0 WPN_Missile.SetWeaponData：26 tuner 组在这里改写 missile 字段；
        0x00B1E030 SentryGun.SetData：30 伤害倍率也挂这里。
        本功能改为结算时直接读 missile/sentry 的 owner 字段（纯内存读，零 Hook）。
        """
        # 注释里可以提地址（说明为什么不挂），但不能再有 RVA 常量 / Hook 调用。
        self.assertNotIn("RVA.WPN_Missile_SetWeaponData", self.js)
        self.assertNotIn("RVA.SentryGun_SetData", self.js)
        self.assertNotIn("attachHook('WPN_Missile.SetWeaponData'", self.js)
        self.assertNotIn("attachHook('SentryGun.SetData'", self.js)

        # 攻击者还原仍然保留，但必须是纯读对象字段
        self.assertIn("function resolveEffectiveAttacker(", self.js)
        self.assertIn("OFF.Missile_owner", self.js)
        self.assertIn("OFF.Sentry_owner", self.js)
        self.assertNotIn("rememberOwner", self.js)
        self.assertNotIn("Runtime.missileOwners", self.js)

    def test_hook_count_is_minimal(self):
        """只允许 3 个伤害链 Hook + 3 个生命周期 Hook，不能再多。"""
        self.assertIn("attachDamageContextHook('Entity.OnEntityHurt'", self.js)
        self.assertIn("attachDamageContextHook('Player.OnEntityHurt'", self.js)
        self.assertEqual(self.js.count("attachDamageContextHook("), 3)  # 1 次定义 + 2 次调用
        self.assertIn("attachHook('HealthData.Hurt'", self.js)
        self.assertEqual(self.js.count("attachHook('"), 1)  # 生命周期走同一循环，不单独调用
        for lifecycle in ("GameManager.GameRoundEnd", "GameManager.NewGameRoundStart", "GameManager.OnDestroy"):
            self.assertIn(lifecycle, self.js)

    def test_native_calls_are_game_thread_only(self):
        """只剩两个原生调用：Heal / get_isDead，且只出现在 Hurt 结算里。"""
        self.assertIn("native.heal(", self.js)
        self.assertIn("native.isDead(", self.js)
        self.assertNotIn("native.singletonGetter", self.js)
        body = self.js
        for name in ("native.heal(", "native.isDead("):
            idx = body.index(name)
            # 都在 onHealthHurt 内（Hurt hook 回调 = 游戏线程）
            self.assertLess(body.index("function onHealthHurt("), idx)
            self.assertLess(idx, body.index("function attachHook("))


class LifestealPythonTest(unittest.TestCase):
    def test_feature_py(self):
        text = (BASE_DIR / "feature.py").read_text(encoding="utf-8")
        self.assertIn("PluginFeatureBase", text)
        self.assertIn('feature_id = "lifesteal"', text)
        self.assertIn('js_filename = "script.js"', text)

    def test_panel_categories(self):
        text = (BASE_DIR / "panel.py").read_text(encoding="utf-8")
        self.assertIn("def build_card(", text)
        self.assertIn('f"src_{key}_enabled"', text)
        for key in SOURCE_CATEGORIES:
            self.assertIn('("' + key + '"', text)
        self.assertIn("lifesteal_percent", text)

    def test_debug_ui_contract(self):
        text = (BASE_DIR / "AAAAA-lifesteal_ui.py").read_text(encoding="utf-8")
        self.assertIn("UnityCrossFire.exe", text)
        self.assertIn('JS_FILE = os.path.join(BASE_DIR, "script.js")', text)
        self.assertIn("exports_sync.cleanup()", text)
        self.assertIn("exports_sync.setconfig", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
