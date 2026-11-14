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


class LifestealRuntimeLogTest(unittest.TestCase):
    """运行日志必须"能落盘、能滚动、不拖累功能"。

    背景：这个功能是靠实机试出来的（枪托重击算哪类、手雷归属是谁、致死一击回多少），
    以前只在 UI 的日志框里滚，关掉就没了，出问题只能靠回忆复述。
    现在要求：一次运行 = 一个日志文件，UI / JS 两侧的行都写进去。
    """

    def test_log_module_exists_and_is_safe(self):
        text = (BASE_DIR / "lifesteal_log.py").read_text(encoding="utf-8")
        for api in ("def start(", "def stop(", "def write(", "def info(", "def warn(", "def error("):
            self.assertIn(api, text)
        # 目录必须落在功能目录的 logs/ 下，且写不进去要能退到用户目录
        self.assertIn('os.path.join(_BASE_DIR, "logs")', text)
        self.assertIn("LOCALAPPDATA", text)
        # 日志目录最多保留 N 个文件、单文件超限滚动
        self.assertIn("MAX_FILES", text)
        self.assertIn("MAX_BYTES", text)
        self.assertIn("def _prune(", text)
        self.assertIn("def _roll(", text)

    def test_ui_persists_every_log_line(self):
        text = (BASE_DIR / "AAAAA-lifesteal_ui.py").read_text(encoding="utf-8")
        self.assertIn("import lifesteal_log", text)
        self.assertIn('lifesteal_log.start(prefix="lifesteal-ui"', text)
        self.assertIn("lifesteal_log.stop()", text)
        # _log 必须同时写文件（否则只在 UI 框里滚，关掉就没了）
        start = text.index("def _log(self, text")
        body = text[start:start + 600]
        self.assertIn("lifesteal_log.write(", body)
        self.assertIn("self.log_box.insert(", body)
        # Frida 的日志等级要带到文件里
        self.assertIn('payload.get("level")', text)

    def test_js_emits_periodic_stats(self):
        js = JS_PATH.read_text(encoding="utf-8")
        for token in ("function logStats(", "function startStatsTimer(", "function stopStatsTimer(", "stats_log_interval_ms", "SCRIPT_VERSION"):
            self.assertIn(token, js)
        # 开/关都要立刻落一条，方便判断"开关有没有生效"
        self.assertIn("logStats('enabled')", js)
        self.assertIn("logStats('disabled')", js)
        # 定时器必须能注销，且离线测试时不能把 node 进程挂住
        self.assertIn("clearInterval(StatsTimer)", js)
        self.assertIn("StatsTimer.unref()", js)
        self.assertIn("logStats('periodic')", js)
        # 统计里要有关键排查字段（否则日志等于没写）
        start = js.index("function logStats(")
        body = js[start:start + 2200]
        for field in ("hurt_hits=", "local_events=", "heal_calls=", "healed_total=", "attacker_missile=", "attacker_sentry=", "cats=", "errors="):
            self.assertIn(field, body)

    # ---- 2026-11-14 实机日志复查后的三条日志补强 + 上限调整 ----

    def test_max_pending_heal_default_is_20000(self):
        """单次回血上限必须 20000：生化/终结者模式一刀 7000~15000，5000 会截掉一大半。

        实测依据：日志里 7000/9000/13000/15000 全部只回了 5000。
        三处默认值必须一致（script.js / manifest.json / 独立 UI），否则注入后被旧值覆盖。
        """
        js = JS_PATH.read_text(encoding="utf-8")
        self.assertIn("max_pending_heal: 20000.0", js)
        self.assertNotIn("max_pending_heal: 5000.0", js)

        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(manifest["config"]["max_pending_heal"], 20000)

        ui = (BASE_DIR / "AAAAA-lifesteal_ui.py").read_text(encoding="utf-8")
        self.assertIn('"max_pending_heal": 20000,', ui)

    def test_diag_reports_hp_max(self):
        """明细必须带 hp_max，否则分不清"被我们的上限截断"还是"被满血截断"。

        实测依据：一条 damage=7000 heal=3000 无法判定成因，只能靠"满血时 Heal 只回 0
        且后面出现过 17852"反推，太绕。带上 hp_max 一眼就能看出来。
        """
        js = JS_PATH.read_text(encoding="utf-8")
        start = js.index("function logDiagnostic(")
        body = js[start:start + 1200]
        self.assertIn("hp_max=", body)
        self.assertIn("hpMax", body)
        # 调用方要把 maxHp 传进来
        call = js[js.index("function logHealOutcome("):][:900]
        self.assertIn("hpAfter.maxHp", call)

    def test_diag_and_summary_share_one_throttle(self):
        """明细与汇总必须共用同一道节流闸门，否则会错位配对 / 缺明细。

        实测依据：diag damage=21 后面跟的是另一发的 damage=36；另有一条回血只有汇总没有明细。
        """
        js = JS_PATH.read_text(encoding="utf-8")
        self.assertIn("function shouldLog(", js)
        # 汇总不再单独节流
        self.assertNotIn("'healed',", js)
        # 明细本身也不再单独节流，改由 logHealOutcome 统一放行
        self.assertNotIn("logLimited('lifesteal_diag'", js)
        start = js.index("function logHealOutcome(")
        body = js[start:start + 900]
        self.assertIn("shouldLog('heal_outcome'", body)
        that = js[:start]
        self.assertIn("function logDiagnostic(", that)
        # 结算处只调这一个入口
        self.assertIn("logHealOutcome(ctx, damage, actualHeal, hpBefore, hpAfter);", js)

    def test_ui_logs_percent_change(self):
        """滑块改比例要落一条 INFO，且值没变不重复下发/重复记。

        实测依据：注入时 10%，日志里却全是 100%，中间没有任何一行记录，事后对不上时间点。
        """
        ui = (BASE_DIR / "AAAAA-lifesteal_ui.py").read_text(encoding="utf-8")
        start = ui.index("def _on_percent_change(")
        body = ui[start:start + 900]
        self.assertIn("吸血比例", body)
        self.assertIn("if numeric == previous:", body)
        # 先比较再下发：避免拖动过程中每帧都发 RPC / 写日志
        self.assertLess(body.index("if numeric == previous:"), body.index("_schedule_config_push()"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
