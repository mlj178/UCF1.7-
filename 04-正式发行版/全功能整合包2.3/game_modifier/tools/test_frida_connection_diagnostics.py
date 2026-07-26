import unittest


class FridaConnectionDiagnosticsTests(unittest.TestCase):
    def test_permission_denied_summary_mentions_admin_and_security_hints(self):
        from core.frida_diagnostics import FridaConnectDiagnostic, PathDiagnostic

        diagnostic = FridaConnectDiagnostic(
            code="permission_denied",
            pid=8292,
            process_name="UnityCrossFire.exe",
            is_admin=False,
            windows_version="Windows 10 build 19045",
            target_access="basic_info_ok",
            frozen=True,
            exception_type="PermissionDeniedError",
            exception_message="access denied",
            app_path=PathDiagnostic(
                drive="C:",
                writable=False,
                protected_location=True,
                sync_location=False,
                has_non_ascii=True,
                has_spaces=True,
                status="ok",
            ),
            game_path=PathDiagnostic(
                drive="D:",
                writable=None,
                protected_location=False,
                sync_location=False,
                has_non_ascii=False,
                has_spaces=True,
                status="ok",
            ),
        )

        lines = diagnostic.to_ui_lines()

        self.assertEqual(lines[0], "Frida 连接失败：权限被拒绝")
        self.assertIn("修改器权限：非管理员", lines[1])
        self.assertIn("游戏进程：UnityCrossFire.exe PID=8292", lines[1])
        self.assertIn("系统：Windows 10 build 19045", lines[1])
        self.assertIn("修改器路径：C盘/保护目录/目录不可写/含中文/含空格", lines[2])
        self.assertIn("游戏路径：D盘/含空格", lines[2])
        self.assertIn("右键修改器以管理员身份运行", lines[3])

    def test_permission_denied_when_admin_points_to_security_or_process_protection(self):
        from core.frida_diagnostics import FridaConnectDiagnostic

        diagnostic = FridaConnectDiagnostic(
            code="permission_denied",
            pid=8292,
            process_name="UnityCrossFire.exe",
            is_admin=True,
            windows_version="Windows 11 build 22631",
            target_access="basic_info_ok",
            frozen=True,
            exception_type="PermissionDeniedError",
            exception_message="access denied",
        )

        lines = diagnostic.to_ui_lines()

        self.assertIn("修改器权限：管理员", lines[1])
        self.assertIn("疑似安全软件、进程保护或系统策略拦截", lines[-1])

    def test_missing_game_path_is_reported_without_full_path(self):
        from core.frida_diagnostics import FridaConnectDiagnostic, PathDiagnostic

        diagnostic = FridaConnectDiagnostic(
            code="connection_failed",
            pid=8292,
            app_path=PathDiagnostic(drive="D:", writable=True, status="ok"),
            game_path=PathDiagnostic(status="path_unreadable"),
        )

        lines = diagnostic.to_ui_lines()

        self.assertIn("修改器路径：D盘/目录可写", lines[2])
        self.assertIn("游戏路径：路径不可读", lines[2])
        self.assertNotIn("UnityCrossFire1.7.1", "\n".join(lines))

    def test_diagnostic_logging_has_a_central_disable_switch_and_comment(self):
        from pathlib import Path

        root = Path(__file__).resolve().parents[1]
        diagnostics = (root / "core" / "frida_diagnostics.py").read_text(encoding="utf-8")
        session_manager = (root / "core" / "game_session_manager.py").read_text(encoding="utf-8")

        self.assertIn("ENABLE_FRIDA_CONNECT_DIAGNOSTICS", diagnostics)
        self.assertIn("Frida 连接诊断日志", diagnostics)
        self.assertIn("Frida 连接诊断日志", session_manager)

    def test_repeated_same_pid_and_error_is_suppressed_until_pid_changes(self):
        from core.frida_diagnostics import DiagnosticDeduper, FridaConnectDiagnostic

        deduper = DiagnosticDeduper()
        first = FridaConnectDiagnostic(code="permission_denied", pid=8292)
        repeated = FridaConnectDiagnostic(code="permission_denied", pid=8292)
        changed_pid = FridaConnectDiagnostic(code="permission_denied", pid=9001)

        self.assertTrue(deduper.should_emit(first))
        self.assertFalse(deduper.should_emit(repeated))
        self.assertTrue(deduper.should_emit(changed_pid))


if __name__ == "__main__":
    unittest.main()
