"""伤害吸血（lifesteal）· 整合包 2.8 静态契约测试。

只做静态检查：目录结构、manifest 契约、RVA、RPC、配置键、实现红线、
以及"能不能被 2.8 的通用 UI / 配置 / 持久化链路接住"。

运行（在功能目录内，避免中文路径被 unittest 当成模块名）：
    python test_lifesteal_static.py
"""

import json
import re
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
JS_PATH = BASE_DIR / "script.js"
MANIFEST_PATH = BASE_DIR / "manifest.json"

# 与 core/plugin/plugin_contract.py 的 REQUIRED_FIELDS 保持一致
CONTRACT_REQUIRED_FIELDS = (
    "feature_id",
    "canonical_id",
    "display_name",
    "category",
    "tab",
    "order",
    "desc",
    "script",
    "layout",
    "controls",
    "config",
    "rpc",
    "lifecycle",
)

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

# 全部来源分类（JS 与 manifest.config 都必须有）
SOURCE_CATEGORIES = (
    "gun_primary",
    "gun_secondary",
    "gun_stock",
    "knife",
    "grenade",
    "special",
    "infect",
)

# 出控件的来源分类：感染从 UI 下线（Entity.OnEntityHurt 对 type==4 直接 return，
# 永远走不到 HealthData.Hurt，开关拖了也不生效），只保留配置键。
VISIBLE_SOURCE_CATEGORIES = tuple(k for k in SOURCE_CATEGORIES if k != "infect")


def load_manifest():
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


class BundleStructureTest(unittest.TestCase):
    """整合包插件目录结构：该有的都在，单功能专用的东西一个都别带进来。"""

    def test_required_files_exist(self):
        for name in (
            "script.js",
            "manifest.json",
            "feature.py",
            "panel.py",
            "events.py",
            "__init__.py",
            "test_lifesteal_runtime.js",
        ):
            self.assertTrue((BASE_DIR / name).is_file(), name)

    def test_single_feature_only_files_are_not_copied(self):
        """独立 UI / 独立日志模块属于 05 开发期工具，整合包不需要也不该带。

        整合包里日志走 core/log_manager.py（开发版写 logs/game_modifier.log，
        发行版按既有策略不落盘），不需要功能自带 lifesteal_log.py。
        """
        names = {p.name for p in BASE_DIR.iterdir()}
        self.assertFalse([n for n in names if n.startswith("AAAAA")], names)
        self.assertNotIn("lifesteal_log.py", names)
        self.assertNotIn("伤害吸血-简要说明.md", names)
        # __pycache__ 是 import 生成的，不算产物；但别把 .pyc / logs 拷进来
        self.assertFalse([n for n in names if n.endswith(".pyc")], names)
        self.assertNotIn("logs", names)

    def test_no_legacy_names(self):
        names = {p.name for p in BASE_DIR.iterdir()}
        self.assertFalse(any("_min.js" in n for n in names))
        self.assertNotIn("launcher.py", names)


class BundleContractTest(unittest.TestCase):
    """能不能被 2.8 的通用 UI / 配置 / 持久化链路直接接住。"""

    def setUp(self):
        self.manifest = load_manifest()

    def test_manifest_has_every_contract_field(self):
        for field in CONTRACT_REQUIRED_FIELDS:
            self.assertIn(field, self.manifest)

    def test_placed_in_player_tab(self):
        self.assertEqual(self.manifest["category"], "player")
        self.assertEqual(self.manifest["tab"], "player_tab")
        self.assertEqual(self.manifest["tab_title"], "人物属性")
        self.assertEqual(self.manifest["tab_order"], 20)
        # 人物属性页现有 order：10/20/30/40/50，本功能排在最后一张卡
        self.assertEqual(self.manifest["order"], 55)

    def test_layout_is_wide_card(self):
        layout = self.manifest["layout"]
        self.assertEqual(layout["card_type"], "wide")
        self.assertEqual(layout["columnspan"], 2)

    def test_runtime_script_path_matches_directory(self):
        runtime_path = self.manifest["source"]["runtime_script_js"]
        self.assertEqual(runtime_path, "features/41_lifesteal/script.js")
        self.assertEqual(BASE_DIR.name, "41_lifesteal")
        self.assertEqual(self.manifest["script"], "script.js")

    def test_lifecycle_fields(self):
        lifecycle = self.manifest["lifecycle"]
        self.assertTrue(lifecycle["cleanup"])
        self.assertTrue(lifecycle["restore"])
        self.assertFalse(lifecycle["requires_room_ready_reapply"])
        # 不申请进房二次应用就必须写明理由，否则会被规范检查拦下
        self.assertTrue(lifecycle.get("room_ready_reapply_exempt_reason"))

    def test_ui_handles_match_generic_sync_convention(self):
        """app._sync_plugin_controls_from_config 按 f"{key}_var" / f"{key}_label" 找句柄。

        命名对不上就会「重启后滑块/开关回到默认值」，这是最常见的接入事故。
        """
        handles = self.manifest["ui_handles"]
        self.assertEqual(handles["switch"], "lifesteal_switch")
        for control in self.manifest["controls"]:
            key = control.get("key")
            if not key:
                continue
            if control["type"] == "slider":
                self.assertIn(key + "_var", handles, key)
                self.assertIn(key + "_label", handles, key)
            elif control["type"] == "switch":
                self.assertIn(key + "_var", handles, key)

    def test_every_control_key_has_config_default(self):
        """panel.py 用 manifest.config 搭默认值，缺键会显示成假状态。"""
        config = self.manifest["config"]
        for control in self.manifest["controls"]:
            key = control.get("key")
            if key:
                self.assertIn(key, config, key)

    def test_rpc_whitelist(self):
        """rpc_client 只放行 manifest.rpc 里列出的动作。"""
        rpc = set(self.manifest["rpc"])
        for action in ("enable", "disable", "setConfig", "set_config", "setconfig", "status", "cleanup"):
            self.assertIn(action, rpc)

    def test_percent_slider_range(self):
        slider = next(
            c for c in self.manifest["controls"]
            if c.get("type") == "slider" and c.get("key") == "lifesteal_percent"
        )
        self.assertEqual(float(slider["min"]), 0.0)
        self.assertEqual(float(slider["max"]), 100.0)
        self.assertEqual(float(slider["default"]), 10.0)
        self.assertEqual(self.manifest["config"]["lifesteal_percent"], 10)

    def test_source_switches_match_config(self):
        controls = {c.get("key"): c for c in self.manifest["controls"] if c.get("type") == "switch"}
        config = self.manifest["config"]
        for key in VISIBLE_SOURCE_CATEGORIES:
            cfg_key = "src_" + key + "_enabled"
            self.assertIn(cfg_key, controls, cfg_key)
            self.assertIn(cfg_key, config, cfg_key)
        self.assertTrue(config["only_enemy_victim"])

    def test_infect_switch_removed_from_ui_but_key_kept(self):
        """感染开关必须从 controls / ui_handles 下线，但配置键要留着。

        理由：感染伤害（type=4）在 Entity.OnEntityHurt 里直接 return，永远不会调用
        HealthData.Hurt，所以这个开关不可能生效——摆出来只会让人以为功能坏了。
        JS 的 infect 分支与配置键保留，万一以后从别的链路进来还能用。
        """
        controls = {c.get("key") for c in self.manifest["controls"]}
        self.assertNotIn("src_infect_enabled", controls)
        self.assertNotIn("src_infect_enabled_var", self.manifest["ui_handles"])
        self.assertNotIn("src_infect_enabled_switch", self.manifest["ui_handles"])
        self.assertIn("src_infect_enabled", self.manifest["config"])
        self.assertFalse(self.manifest["config"]["src_infect_enabled"])


class LifestealJsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.js = JS_PATH.read_text(encoding="utf-8")

    def test_feature_id(self):
        self.assertIn("feature_id: 'lifesteal'", self.js)

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
        for write in ("writeFloat(", "writeS32(", "writeU8(", "writeU32(", "writePointer("):
            self.assertNotIn(write, self.js)

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
        self.assertNotIn("customtkinter", self.js)

    def test_local_player_is_pure_memory_read(self):
        """本地玩家必须读 GameManager.myPlayer 静态字段，不能调游戏托管方法。"""
        self.assertIn("function readStaticMyPlayer()", self.js)
        self.assertIn("GameManager_TypeInfo", self.js)
        self.assertIn("Il2CppClass_staticFields", self.js)
        self.assertIn("GameManager_myPlayer", self.js)
        self.assertNotIn("native.isMyPlayer", self.js)
        self.assertNotIn("singletonGetter", self.js)
        self.assertNotIn("Player_get_isMyPlayer", self.js)

    def test_no_shared_hook_with_grenade_mode(self):
        """不能再 Hook 26 手雷模式用到的地址（0xB663C0 / 0xB1E030）。"""
        self.assertNotIn("RVA.WPN_Missile_SetWeaponData", self.js)
        self.assertNotIn("RVA.SentryGun_SetData", self.js)
        self.assertNotIn("attachHook('WPN_Missile.SetWeaponData'", self.js)
        self.assertNotIn("attachHook('SentryGun.SetData'", self.js)
        self.assertIn("function resolveEffectiveAttacker(", self.js)
        self.assertIn("OFF.Missile_owner", self.js)
        self.assertIn("OFF.Sentry_owner", self.js)
        self.assertNotIn("rememberOwner", self.js)
        self.assertNotIn("Runtime.missileOwners", self.js)

    def test_hook_count_is_minimal(self):
        """只允许 3 个伤害链 Hook + 3 个生命周期 Hook，不能再多。"""
        self.assertIn("attachDamageContextHook('Entity.OnEntityHurt'", self.js)
        self.assertIn("attachDamageContextHook('Player.OnEntityHurt'", self.js)
        self.assertEqual(self.js.count("attachDamageContextHook("), 3)
        self.assertIn("attachHook('HealthData.Hurt'", self.js)
        self.assertEqual(self.js.count("attachHook('"), 1)
        for lifecycle in ("GameManager.GameRoundEnd", "GameManager.NewGameRoundStart", "GameManager.OnDestroy"):
            self.assertIn(lifecycle, self.js)

    def test_native_calls_are_game_thread_only(self):
        self.assertIn("native.heal(", self.js)
        self.assertIn("native.isDead(", self.js)
        self.assertNotIn("native.singletonGetter", self.js)
        for name in ("native.heal(", "native.isDead("):
            idx = self.js.index(name)
            self.assertLess(self.js.index("function onHealthHurt("), idx)
            self.assertLess(idx, self.js.index("function attachHook("))

    # ---- 运行日志（选项 A：只用整合包 dev 日志，不带独立日志文件）----

    def test_js_emits_periodic_stats(self):
        for token in ("function logStats(", "function startStatsTimer(", "function stopStatsTimer(", "stats_log_interval_ms", "SCRIPT_VERSION"):
            self.assertIn(token, self.js)
        self.assertIn("logStats('enabled')", self.js)
        self.assertIn("logStats('disabled')", self.js)
        self.assertIn("clearInterval(StatsTimer)", self.js)
        self.assertIn("StatsTimer.unref()", self.js)
        self.assertIn("logStats('periodic')", self.js)
        body = self.js[self.js.index("function logStats("):]
        body = body[:2200]
        for field in ("hurt_hits=", "local_events=", "heal_calls=", "healed_total=", "attacker_missile=", "attacker_sentry=", "cats=", "errors="):
            self.assertIn(field, body)

    def test_no_own_log_file(self):
        """选项 A：功能不自己开日志文件。

        2.8 的 log_manager 在发行版（exe）里一律不落盘，功能侧也不该绕过这条策略
        自己去写文件。日志走 send({type:'log'})：开发版进 logs/game_modifier.log，
        发行版只在内存/界面层，不产生 .log。
        """
        self.assertNotIn("new File(", self.js)
        self.assertNotIn("log_to_file", self.js)
        for token in ("type: 'log'", "module: Runtime.feature_id"):
            self.assertIn(token, self.js)

    def test_max_pending_heal_matches_manifest(self):
        self.assertIn("max_pending_heal: 20000.0", self.js)
        self.assertEqual(load_manifest()["config"]["max_pending_heal"], 20000)

    def test_diag_and_summary_share_one_throttle(self):
        self.assertIn("function shouldLog(", self.js)
        self.assertIn("function logHealOutcome(", self.js)
        self.assertIn("shouldLog('heal_outcome'", self.js)
        self.assertIn("logHealOutcome(ctx, damage, actualHeal, hpBefore, hpAfter);", self.js)
        self.assertIn("hp_max=", self.js)


class LifestealPythonTest(unittest.TestCase):
    def test_feature_py(self):
        text = (BASE_DIR / "feature.py").read_text(encoding="utf-8")
        self.assertIn("PluginFeatureBase", text)
        self.assertIn('feature_id = "lifesteal"', text)
        self.assertIn('js_filename = "script.js"', text)

    def test_panel_signature_matches_builder(self):
        """ui/pages/plugin_feature_page.py 调用 build_card(parent, manifest, row, col, colspan, callbacks, card_builder)。"""
        text = (BASE_DIR / "panel.py").read_text(encoding="utf-8")
        self.assertIn("def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):", text)

    def test_panel_categories(self):
        text = (BASE_DIR / "panel.py").read_text(encoding="utf-8")
        self.assertIn('f"src_{key}_enabled"', text)
        for key in VISIBLE_SOURCE_CATEGORIES:
            self.assertIn('("' + key + '"', text)
        # 感染不再出控件（HIDDEN_CATEGORY_KEYS 里仍有 "infect"，所以按完整行判断）
        self.assertNotIn('("infect", "感染"', text)
        self.assertIn("HIDDEN_CATEGORY_KEYS", text)
        self.assertIn("lifesteal_percent", text)

    def test_sources_section_is_collapsed_by_default(self):
        """六个来源开关默认收起，卡片只留 比例 / 来源摘要 / 只吸敌人 三行。

        收起只是不 pack，控件照建：这样 app._sync_plugin_controls_from_config
        仍能把持久化的开关值回填到隐藏控件上，重启不会丢配置。
        """
        text = (BASE_DIR / "panel.py").read_text(encoding="utf-8")
        self.assertIn("def set_advanced(", text)
        self.assertIn("def toggle_advanced(", text)
        self.assertIn("set_advanced(False)", text)          # 默认收起
        self.assertIn("source_frame.pack_forget()", text)   # 收起实现
        self.assertIn("source_frame.pack(", text)           # 展开实现
        self.assertIn("展开 ▾", text)
        # 收起状态不能让容器一开始就 pack 出来
        head = text[: text.index("def set_advanced(")]
        self.assertNotIn("source_frame.pack(fill", head)
        # 摘要行要能看出关了哪几类
        self.assertIn("def refresh_source_hint(", text)
        self.assertIn("已关闭：", text)

    def test_panel_uses_generic_callbacks_only(self):
        """panel 只能通过 callbacks 调功能，不能自己碰 Frida。"""
        text = (BASE_DIR / "panel.py").read_text(encoding="utf-8")
        self.assertNotIn("Interceptor", text)
        self.assertNotIn("frida_manager", text)
        self.assertNotIn("exports_sync", text)
        for cb in ('callbacks["toggle"]', 'callbacks["set_config"]'):
            self.assertIn(cb, text)

    def test_events_module_is_local_only(self):
        text = (BASE_DIR / "events.py").read_text(encoding="utf-8")
        self.assertIn("def handle_event(", text)
        self.assertNotIn("lifesteal_log", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
