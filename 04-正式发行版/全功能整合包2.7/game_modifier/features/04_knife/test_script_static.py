from pathlib import Path
import unittest


SCRIPT_PATH = Path(__file__).with_name("script.js")


class KnifeScriptStaticTests(unittest.TestCase):
    def test_fire_button_guard_clears_in_on_leave_after_setter_body(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        # Weapon.OnFireBtnPressed 的本体就是 _fireBtnPressed = 1（IDA 0x10B6CDA0），
        # 因此撤销必须写在 onLeave；写在 onEnter 会被本体覆盖，等于保护从未生效。
        guard = source.split("fireBtnHook = Interceptor.attach(base.add(0xB6CDA0)")[1].split("// 兜底 B")[0]
        self.assertIn("onEnter: function (args)", guard)
        self.assertIn("this.w = args[0];", guard)
        self.assertIn("onLeave: function ()", guard)
        self.assertIn("clearStuckFireBtn(this.w", guard)
        self.assertNotIn("writeU8(0)", guard)          # onEnter 里不得直接写字段
        self.assertIn("function clearStuckFireBtn(w, tag)", source)

    def test_per_frame_fallback_hook_on_wpn_knife_update(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertIn("base.add(0xB64610)", source)          # WPN_Knife.Update
        self.assertIn("clearStuckFireBtn(args[0], 'WPN_Knife.Update')", source)
        self.assertIn(
            "if (knifeUpdateHook) { try { knifeUpdateHook.detach(); } catch (e) {} knifeUpdateHook = null; }",
            source,
        )

    def test_clear_requires_physical_release_and_local_weapon(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        helper = source.split("function clearStuckFireBtn(w, tag)")[1].split("\n  }")[0]
        self.assertIn("var down = physicalLeftDown();", helper)
        self.assertIn("if (down !== false)", helper)            # 真按着 / 读不到都不动
        self.assertIn("isMyPlayer(owner, ptr(0))", helper)      # 只动本地玩家武器
        self.assertIn("w.add(0x78).writeU8(0)", helper)

    def test_physical_key_reader_uses_a_valid_frida_type_name(self):
        """回归护栏：Frida 17 不接受 'short'，会抛 invalid type specified。

        new NativeFunction(fn, 'short', ['int']) 抛出的异常被 catch 吞掉后，
        physicalLeftDown() 恒返回 null -> clearStuckFireBtn 第一道门永远拦住 ->
        整个"左键防卡死"兜底一次都不执行（2026-10 两轮"修了没用"的真凶）。
        实测：06-测试/frida-revert-probe/probe_async_keystate.py
        """
        source = SCRIPT_PATH.read_text(encoding="utf-8")
        code = "\n".join(
            line for line in source.splitlines() if not line.strip().startswith("//")
        )

        self.assertNotIn("'short'", code)
        self.assertIn("new NativeFunction(fn, 'uint16', ['int'])", code)
        # 反面护栏：不许再用 UnityEngine.Input.GetKey(0xACFA60) 兜底。
        # 实测它会抛 "access violation accessing 0x4"（走进 il2cpp_resolve_icall），
        # 在游戏进程里制造访问违例是不可接受的：解析路径上的锁可能不被释放，
        # 之后任何一次 il2cpp_resolve_icall 都会永久阻塞 => 表现就是"游戏停止响应"。
        self.assertNotIn("0xACFA60", code)
        self.assertNotIn("readUnityMouseLeft", code)
        # 读不到就什么都别做（宁可不纠正，也不去碰游戏自己的输入状态）
        helper = code.split("function physicalLeftDown()")[1].split("// 物理左键已松开")[0]
        self.assertIn("return null;", helper)

    def test_guard_diagnostics_bypass_the_per_module_log_cap(self):
        """排查通道必须绕过 sendRoutedLog 的「每模块 10 条」上限，否则日志里什么都看不到。"""
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertIn("type: 'log_file'", source)
        self.assertIn("sendDiag(", source)
        # 循环频率观测钩子：PlayKnifeAttackAnim(weapon, combo)
        self.assertIn("base.add(0xB642B0)", source)
        self.assertIn("playKnifeAnimHook.detach()", source)

    def test_heavy_attack_gate_blocks_when_physical_right_button_is_up(self):
        """重击（combo3）的唯一入口是 WPN_Knife.OnSpecialBtnDown(0xB64240)，且它没有任何状态位可清。

        IDA 实证（0x10B64240 全文 0x70 字节）：
            if (Weapon.get_isUsing(this) && this->_currentAnimTag == string.Empty)
                this->klass->vtable.PlayKnifeAttackAnim(this, 3);
        而 PlayerController.UseWeapon 是每帧 `if (Input.GetKey(324)) OnSpecialBtnDown();`
        ⇒ 游戏侧右键状态一旦卡住，重击就一击接一击无限重播（日志实证调用者 = 0xb642a1）。
        因此必须在唯一入口按"物理右键"拦截。
        """
        source = SCRIPT_PATH.read_text(encoding="utf-8")
        code = "\n".join(
            line for line in source.splitlines() if not line.strip().startswith("//")
        )

        self.assertIn("base.add(0xB64240)", code)                       # WPN_Knife.OnSpecialBtnDown
        self.assertIn("physicalRightDown()", code)
        self.assertIn("readOsKeyState(0x02)", code)                     # VK_RBUTTON
        # NativeFunction 必须在 Interceptor.replace 之前建好，之后才能调到原函数
        gate = code.split("Interceptor.replace(specialAddr")[0]
        self.assertIn("specialOrig = new NativeFunction(specialAddr", gate)
        # 物理右键没按才拦；读不到(null)时放行（不改变游戏行为）
        body = code.split("Interceptor.replace(addr, new NativeCallback(")[1].split("}, 'void', ['pointer', 'pointer']));")[0]
        self.assertIn("physicalRightDown() === false", body)
        self.assertIn("if (allow)", body)
        self.assertIn("orig(w, method)", body)
        # disable 必须 revert，且只对本地玩家武器生效
        disable_body = code.split("disable: function()")[1].split("};")[0]
        self.assertIn("Interceptor.revert(specialAddr)", disable_body)
        self.assertIn("isMyPlayer(owner2, ptr(0))", body)

    def test_anomaly_probe_uses_the_matching_mouse_button_per_combo(self):
        """combo3 是右键重击、combo1/2 是左键连招 —— 判"异常"必须用对应的键，否则会误报。"""
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertIn("var expectDown = (combo >= 3) ? physicalRightDown() : physicalLeftDown();", source)
        self.assertIn("if (combo >= 3 && diag.combo3 <= 6)", source)
        self.assertIn("keyName", source)

    def test_disable_reverts_getter_and_detaches_both_guard_hooks(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        disable_body = source.split("disable: function()")[1].split("};")[0]
        self.assertIn("Interceptor.revert(getKnifeSpeedAddr)", disable_body)
        self.assertIn("fireBtnHook.detach()", disable_body)
        self.assertIn("knifeUpdateHook.detach()", disable_body)

    def test_ghost_and_terminator_are_limited_by_IsHuman(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        # IDA 实证：NanoRoleExpand.IsHuman(0xB4E960) = role==0 || 18..27；
        # IsTerminator(0xB4EA40) = 8..17 —— 终结者落在 !IsHuman 分支，必须吃 ghost_cap。
        self.assertIn("base.add(0xB4E960)", source)   # IsHuman
        self.assertIn("base.add(0xB56200)", source)   # get_nanoRole
        self.assertIn("ghostSpeedCap", source)
        self.assertIn("if (!human && value > ghostSpeedCap) value = ghostSpeedCap;", source)


if __name__ == "__main__":
    unittest.main()
