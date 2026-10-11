"""静态回归测试：手雷模式必须"按配置分组安装 Hook/Replace"。

背景（真实故障，2026-10-11）：
    只开"手雷强化"三个选项时，脚本仍然把 45 个 Hook + 6 个 Replace 全部装上，
    其中 Interceptor.replace(PlayerWeapons.Remove) / Interceptor.replace(GameManager.GiveWeapon)
    落在人类→终结者的武器切换链路上。我们自己的 JS 回调里用 NativeFunction 回call原函数，
    原函数此刻抛出的是 il2cpp 的托管异常（C++ EH），Frida 的异常处理器先抓到它并变成
    JS 的 "Error: system error"（Frida 内部异常类型表：arithmetic error /
    breakpoint triggered / single-step triggered / system error），
    游戏自己的异常处理帧再也收不到 → 发枪/收枪被静默中断 →
    手上武器 isUsing=0、fireBtn=1、animTag 卡在 KnifeAtk → 轻击/重击动作卡住、无法攻击。
日志实证（14:13:51.070/071）：
    异常：PlayerWeapons.Remove.replacement | Error: system error
    异常：GameManager.GiveWeapon.replacement | Error: system error
    异常：GameManager.GiveWeapon.original_after_error | Error: system error

因此下列不变量必须一直成立：
  1) 只有当前配置真正需要的分组才安装；
  2) 武器切换链路（Remove / GiveWeapon）上不能有"配置不需要"的 Replace；
  3) GiveWeapon 只观察（attach），不替换；
  4) 必须替换的 Remove 守卫回调内不做任何游戏方法调用，出错立刻撤销替换。
"""

import unittest
from pathlib import Path


FEATURE_DIR = Path(__file__).parent
SCRIPT = (FEATURE_DIR / "script.js").read_text(encoding="utf-8")


def function_body(name: str, source: str = SCRIPT) -> str:
    """抽出 `function name(...) {` 到下一个顶层 `\n}` 之间的文本。"""
    marker = f"function {name}("
    start = source.index(marker)
    end = source.index("\n}\n", start)
    return source[start:end]


def strip_line_comments(text: str) -> str:
    """去掉整行注释，避免注释里提到的危险写法被误判。"""
    return "\n".join(line for line in text.splitlines() if not line.strip().startswith("//"))


class GrenadeInstallGatingTests(unittest.TestCase):
    def test_install_hooks_syncs_groups_instead_of_installing_everything(self):
        body = function_body("installHooks")
        self.assertIn("syncInstalledGroups(", body)
        # 旧的"一次性全装"写法必须消失
        self.assertNotIn("installRemoveGuard();", body)
        self.assertNotIn("installBotGrenadeRecordControls();", body)
        self.assertNotIn("installVirtualBotControlControls();", body)

    def test_every_replacement_and_hook_group_is_declared(self):
        for group in (
            "throwLock",
            "capture",
            "tuner",
            "animSpeed",
            "observers",
            "removeGuard",
            "botRecord",
            "botDrive",
            "vbc",
            "botAI",
        ):
            self.assertIn(f'"{group}"', SCRIPT, f"分组 {group} 未声明")
        # 安装器表必须覆盖 computeGroupNeeds 的每一个键
        needs = function_body("computeGroupNeeds")
        for group in ("throwLock", "capture", "tuner", "animSpeed", "observers", "removeGuard", "botRecord", "botDrive", "vbc", "botAI"):
            self.assertIn(f"{group}:", needs, f"computeGroupNeeds 缺少 {group}")

    def test_remove_guard_requires_infinite_grenade_and_weapon_protection(self):
        needs = function_body("computeGroupNeeds")
        self.assertIn("removeGuard: !!(c.lock999_enabled && c.protect_weapon_remove)", needs)

    def test_grenade_enhancements_alone_install_no_replacements(self):
        """只开手雷强化（伤害/范围/速度）时，期望的替换数为 0。"""
        needs = function_body("computeGroupNeeds")
        # 三个强化 -> 只需要 tuner + capture 两组；都是 attach-only
        for group in ("throwLock", "observers", "removeGuard", "botRecord", "botDrive", "vbc", "botAI"):
            self.assertNotIn(f"{group}: true", needs)
        # tuner/capture 由 enable_* 决定
        self.assertIn("const anyEnhance = !!(c.enable_damage || c.enable_range || c.enable_shoot_speed);", needs)
        self.assertIn("tuner: tuner", needs)
        self.assertIn("capture: !!(tuner || botMode)", needs)

    def test_giveweapon_is_observed_not_replaced(self):
        give_block = strip_line_comments(function_body("installBotGrenadeRecordControls"))
        self.assertIn('addHook("GameManager.GiveWeapon"', give_block)
        self.assertNotIn("Interceptor.replace(", give_block)
        self.assertNotIn("Interceptor.replace", give_block)
        self.assertNotIn("new NativeCallback", give_block)
        self.assertNotIn("GameManager_GiveWeapon_Original", give_block)
        # 危险的"预览发枪"必须删除：GameManager.GetWeapon 内部会 Instantiate/Init 并可能抛托管异常
        self.assertNotIn("previewWeapon", give_block)

    def test_remove_guard_body_never_calls_into_game_methods(self):
        guard = function_body("installRemoveGuard")
        for forbidden in (
            "readWeaponInfo(",
            "readPlayerWeaponsInfo(",
            "throwWeaponAllowedByScope(",
            "Weapon_get_isMyWeapon",
            "GameManager_",
        ):
            self.assertNotIn(forbidden, guard, f"Remove 守卫回调里不允许出现 {forbidden}")
        self.assertIn("readWeaponClassOnly(weapon)", guard)

    def test_remove_guard_self_heals_when_original_raises_managed_exception(self):
        guard = function_body("installRemoveGuard")
        self.assertIn("Interceptor.revert(address)", guard)
        self.assertIn("remove_guard_reverted", guard)
        self.assertIn("remove_original_error", guard)

    def test_animator_hooks_are_gated_by_throw_anim_speed(self):
        needs = function_body("computeGroupNeeds")
        self.assertIn("animSpeed: !!c.throw_anim_speed_enabled", needs)

    def test_config_change_resyncs_installed_groups(self):
        body = function_body("setConfig")
        self.assertIn("syncInstalledGroups(", body)

    def test_replacement_installs_go_through_the_group_helper(self):
        # 直接调用 Interceptor.replace 的地方必须只在 replaceFunction 里
        occurrences = SCRIPT.count("Interceptor.replace(")
        self.assertEqual(occurrences, 1, "除 replaceFunction 外不应再有裸 Interceptor.replace 调用")
        self.assertIn("function replaceFunction(", SCRIPT)


if __name__ == "__main__":
    unittest.main()
