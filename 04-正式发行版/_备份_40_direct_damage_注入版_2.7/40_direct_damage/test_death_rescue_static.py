import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
JS_FILE = BASE_DIR / "script.js"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class DeathRescueStaticTests(unittest.TestCase):
    """复活兜底（death_fix_respawn）只能作用于"我方直伤打断了死亡流程"的情况。

    回归背景：生化幽灵被**近战武器**打死（= 游戏自己正常结算的死亡：广播完整返回、
    游戏也没排复活）以前会被兜底在 6 秒后强行复活，表现成"打死了又爬起来"。
    """

    def test_rescue_gate_only_allows_our_kills_or_interrupted_broadcast(self):
        text = read_text(JS_FILE)

        self.assertIn("function shouldRescueDeath(entry)", text)
        self.assertIn("return entry.ours === true || entry.bcDone === false;", text)

    def test_rescue_tick_skips_game_native_deaths(self):
        text = read_text(JS_FILE)

        self.assertIn("if (!shouldRescueDeath(entry)) continue;", text)

    def test_ours_flag_comes_from_injection_state_not_label(self):
        text = read_text(JS_FILE)

        # 注入路径里 TakeDamage 可能在死亡广播之前就抛异常，广播钩子不会登记，
        # 所以 ours 必须取调用现场的 Runtime.inDirectDamage，不能看 label。
        self.assertIn("var oursFlag = ours === true;", text)
        self.assertIn("ours: oursFlag,", text)
        self.assertIn("if (oursFlag) prev.ours = true;", text)
        self.assertIn("registerDeathWatch(victim, sourceLabel, note, false, Runtime.inDirectDamage === true);", text)
        self.assertIn("registerDeathWatch(dead, Runtime.inDirectDamage ? '[ours]' : '[game]', 'deathIn', true,", text)

    def test_round_boundaries_clear_cross_round_state(self):
        """上一回合的死亡观察窗口 / 补发队列不能留到下一回合。

        回归背景：新回合倒计时还没结束，上一回合死掉的生化幽灵就被兜底复活出来了。
        """
        text = read_text(JS_FILE)

        for token in [
            "GameManager_GameRoundEnd: 0x00AFAA40",
            "GameManager_NewGameRoundStart: 0x00AEBCB0",
            "GameManager_OnDestroy: 0x00AEBD40",
            "function clearRoundScopedState(reason)",
            "clearRoundScopedState('game_round_end')",
            "clearRoundScopedState('new_game_round_start')",
            "clearRoundScopedState('game_manager_destroy')",
            "Runtime.deathWatch = {};",
            "Runtime.cache.rebroadcastQueue = null;",
        ]:
            self.assertIn(token, text, f"script.js missing {token}")

    def test_watchdog_keep_retrying_respects_rescue_gate(self):
        text = read_text(JS_FILE)

        self.assertIn("var keepRetrying = (shouldRescueDeath(entry) && !entry.rescued &&", text)


if __name__ == "__main__":
    unittest.main()
