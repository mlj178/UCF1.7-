import unittest

from core.log_router import LogRoute, build_log_route


class LogRouterTests(unittest.TestCase):
    def test_user_log_is_shown_but_not_written_to_dev_log_by_default(self):
        route = build_log_route(
            level="info",
            module="连接",
            message="已连接游戏",
            audience="user",
        )

        self.assertEqual(route, LogRoute(
            level="info",
            module="连接",
            user_message="已连接游戏",
            dev_message="",
            show_in_ui=True,
            write_to_dev_log=False,
        ))

    def test_dev_log_keeps_bilingual_detail_out_of_ui(self):
        route = build_log_route(
            level="warn",
            module="回合跳过",
            message="捕获失败",
            audience="dev",
            dev_detail="RoundSkip no_instance: hook已安装，但 modeBaseInstance为空",
        )

        self.assertFalse(route.show_in_ui)
        self.assertTrue(route.write_to_dev_log)
        self.assertEqual(route.dev_message, "捕获失败 | RoundSkip no_instance: hook已安装，但 modeBaseInstance为空")

    def test_both_log_uses_user_message_for_ui_and_dev_detail_for_file(self):
        route = build_log_route(
            level="error",
            module="武器赋予",
            message="赋予失败，请稍后重试",
            audience="both",
            dev_detail="WeaponGiver failed: player pointer invalid",
        )

        self.assertTrue(route.show_in_ui)
        self.assertTrue(route.write_to_dev_log)
        self.assertEqual(route.user_message, "赋予失败，请稍后重试")
        self.assertEqual(route.dev_message, "赋予失败，请稍后重试 | WeaponGiver failed: player pointer invalid")


if __name__ == "__main__":
    unittest.main()
