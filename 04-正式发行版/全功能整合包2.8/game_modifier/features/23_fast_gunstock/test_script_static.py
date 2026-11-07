from pathlib import Path
import unittest


SCRIPT_PATH = Path(__file__).with_name("script.js")


class FastGunstockNaturalDamageTests(unittest.TestCase):
    def test_unlocks_only_after_the_original_natural_damage_event(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertIn("KnifeAttackEvent: 0xB62730", source)
        self.assertIn("自然伤害完成", source)
        self.assertIn("unlockAttack(atk, '自然伤害完成')", source)
        self.assertIn("onLeave: function ()", source)
        self.assertNotIn("knifeAttackEventFn(atk.weapon", source)
        self.assertNotIn("function doEarlyDamage", source)
        self.assertNotIn("earlyDamageDelayMs", source)

    def test_phantom_attack_is_cancelled_when_select_animation_ends(self):
        """切枪 select 期右键没有真正起手：select 退出必须立即取消，不能等 900ms 兜底。"""
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertIn("onanimationexit:select", source)
        self.assertIn("掏枪动画结束，未起手取消", source)

    def test_keeps_an_exception_only_guard_without_a_fixed_attack_cadence(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertIn("maxGuardMs", source)
        self.assertNotIn("unlockDelayMs", source)
        self.assertIn("最大保护窗口", source)

    def test_skips_when_local_player_is_nano_ghost(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertIn("Player_get_isNanoGhost: 0xB56050", source)
        self.assertIn("owner: 0x30", source)
        self.assertIn("isLocalPlayerNanoGhost(w)", source)
        self.assertIn("本地玩家为生化幽灵，极速枪托不生效", source)
        self.assertIn("ghostSkips", source)

    def test_disable_leaves_no_pending_action_for_after_close(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        # 关闭 = 同步交还自写锁 + 清空运行态；不得再挂 pending（否则关闭后还会补调
        # WPN_Gun.OnKnifeAttackExit，也就是本功能的加速动作）
        disable_body = source.split("function disable()")[1].split("function cleanup()")[0]
        self.assertIn("releaseGuardLock('功能关闭')", disable_body)
        self.assertIn("resetRuntime('disable')", disable_body)
        self.assertNotIn("forceClear(", disable_body)
        self.assertNotIn("pendingForceClear = true", disable_body)

    def test_enable_resets_runtime_before_installing_hooks(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        enable_body = source.split("function enable()")[1].split("function disable()")[0]
        self.assertIn("resetRuntime('enable')", enable_body)
        self.assertIn("if (st.enabled) return true;", enable_body)
        self.assertIn("st.pendingForceClear = false;", source)
        self.assertIn("st.pendingForceUnlock = false;", source)

    def test_every_installed_hook_checks_enabled(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        parts = source.split("st.hooks.push(Interceptor.attach(")[1:]
        self.assertEqual(len(parts), 8, "Hook 数量变化时需要同步复核 enabled 门控")
        for part in parts:
            head = part[:800]
            self.assertTrue(
                "if (!st.enabled) return;" in head or "st.enabled &&" in head,
                "保留的 Hook 必须在入口判断 st.enabled（保留 Hook 也可以，但必须判断 enabled）",
            )

    def test_fire_button_guard_clears_in_on_leave_after_setter_body(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        # Weapon.OnFireBtnPressed 的本体就是 _fireBtnPressed = 1（IDA 0x10B6CDA0），
        # 撤销写在 onEnter 会被本体覆盖 —— 必须放 onLeave。
        guard = source.split("RVA.Weapon_OnFireBtnPressed")[1].split("st.hooks.push(Interceptor.attach(m.base.add(RVA.OnSpecialBtnDown)")[0]
        self.assertIn("onEnter: function (args)", guard)
        self.assertIn("this.w = args[0];", guard)
        self.assertIn("onLeave: function ()", guard)
        self.assertIn("clearStuckFireBtn(this.w)", guard)
        self.assertNotIn("writeU8(0)", guard)
        self.assertIn("function clearStuckFireBtn(w)", source)

    def test_physical_key_reader_uses_a_valid_frida_type_name(self):
        """回归护栏：Frida 17 不接受 'short'，会抛 invalid type specified。

        new NativeFunction(fn, 'short', ['int']) 的异常被 catch 吞掉后 physicalLeftDown()
        恒返回 null -> clearStuckFireBtn 的第一道门永远拦住 -> 该兜底从未执行过
        （2026-10「修了没用」的真凶）。实测：06-测试/frida-revert-probe/probe_async_keystate.py
        """
        source = SCRIPT_PATH.read_text(encoding="utf-8")
        code = "\n".join(
            line for line in source.splitlines() if not line.strip().startswith("//")
        )

        self.assertNotIn("'short'", code)
        self.assertIn("new NativeFunction(fn, 'uint16', ['int'])", code)
        # 反面护栏：不许再用 UnityEngine.Input.GetKey(0xACFA60) 兜底（实测抛访问违例，
        # 会走进 il2cpp_resolve_icall；在游戏进程里制造访问违例可能导致后续永久阻塞）
        self.assertNotIn("0xACFA60", code)
        self.assertNotIn("readUnityMouseLeft", code)

    def test_guard_diagnostics_bypass_the_per_module_log_cap(self):
        """诊断必须走 raw log_file（MAX_LOGS_PER_MODULE=3 会把 guard 日志全部吃掉）。"""
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertIn("type: 'log_file'", source)
        self.assertIn("sendDiag(", source)
        self.assertIn("0xB642B0", source)               # WPN_Knife.PlayKnifeAttackAnim 观测钩子


if __name__ == "__main__":
    unittest.main()
