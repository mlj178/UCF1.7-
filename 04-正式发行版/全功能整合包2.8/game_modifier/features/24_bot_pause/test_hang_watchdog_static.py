from pathlib import Path
import unittest


SCRIPT_PATH = Path(__file__).with_name("script.js")


class HangWatchdogStaticTests(unittest.TestCase):
    """卡死看门狗：游戏"停止响应"时唯一的证据来源，不能再被无意删掉。

    技术前提已用 06-测试/frida-revert-probe/probe_hang_watchdog.py 实测：
    别的线程死循环（jmp $ / 或死循环调用被 Hook 的函数）时，Frida 的 JS 线程
    仍能按时触发 setInterval，并把环形缓冲里的面包屑完整倒出来。
    """

    def test_watchdog_pulses_on_main_thread_and_flushes_on_timeout(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertIn("RVA.ModeBase_Update", source)
        self.assertIn("function watchPulse()", source)
        self.assertIn("HANG_IDLE_MS", source)
        self.assertIn("setInterval", source)
        self.assertIn("function flushBreadcrumbs(", source)
        # 空缓冲不能崩（probe 里就踩过一次 "cannot read property 't' of undefined"）
        flush_body = source.split("function flushBreadcrumbs(")[1].split("function startHangWatchdog")[0]
        self.assertIn("if (!watch.buf.length)", flush_body)

    def test_breadcrumbs_are_installed_at_load_and_rate_limited(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        # 与功能开关解耦：脚本加载即安装，关掉 bot_pause 也要能留痕
        tail = source.split("sendLog('info', 'script loaded")[1]
        self.assertIn("startHangWatchdog();", tail)
        self.assertIn("installWatchdogPulseHook();", tail)
        self.assertIn("installBreadcrumbHooks();", tail)

        # 热点观测点必须限频，否则环形缓冲会被冲掉、还白堆 Hook 开销
        self.assertIn("WATCH_MIN_INTERVAL_MS", source)
        note_body = source.split("function noteBreadcrumb(")[1].split("function flushBreadcrumbs")[0]
        self.assertIn("WATCH_MIN_INTERVAL_MS", note_body)

    def test_hang_detection_only_runs_inside_a_room(self):
        """ModeBase.Update 只在房间/对局内跑，回大厅/结算时它天然不跑 —— 不能算卡死。

        上一轮实测的假警报：13:57:02 报「静默 6981ms」，其实是 13:56:56 房间已销毁（OnDestroy）。
        """
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertIn("watch.inRoom", source)
        interval_body = source.split("watch.timer = setInterval(")[1].split("}, 1000);")[0]
        self.assertIn("if (!watch.inRoom) return;", interval_body)
        self.assertIn("watch.inRoom = false;", source)     # 离开对局时关掉判定
        self.assertIn("watch.lastPulseAt = 0;", source)    # 并清掉心跳，避免用旧时间戳误判

    def test_breadcrumb_hooks_avoid_the_closure_capture_trap(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        # var 循环变量被闭包捕获会让所有面包屑都变成最后一个名字 —— 必须用工厂函数包一层
        body = source.split("function installBreadcrumbHooks(")[1].split("function attachRoomHook")[0]
        self.assertIn("(function (label, target) {", body)
        self.assertIn("noteBreadcrumb(label)", body)


if __name__ == "__main__":
    unittest.main()
