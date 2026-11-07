import json
import sys
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = Path(r"D:\trae_project\ucf1.7-modifier\05-正式功能\18-Universal-ESP盒子\Universal-Dear-ImGui-Hook")


# ---------------------------------------------------------------------------
# 下面几个函数是 esp/named_pipe_server.cpp 里 GetJsonString / ParseBool /
# ParseHealthMode / ParseHealthDisplay 的等价实现，用来离线校验 Python 发出的
# JSON 能被 C++ 侧解析成同样的枚举值（字段名与类型必须两侧一致）。
# ---------------------------------------------------------------------------
def cpp_get_json_string(payload, key):
    search = '"' + key + '"'
    pos = payload.find(search)
    if pos < 0:
        return ""
    pos = payload.find(':', pos)
    if pos < 0:
        return ""
    while pos < len(payload) and payload[pos] in ':\t ':
        pos += 1
    if pos >= len(payload):
        return ""
    if payload[pos] == '"':
        end = payload.find('"', pos + 1)
        if end < 0:
            return ""
        return payload[pos + 1:end]
    end = pos
    while end < len(payload) and payload[end] not in ',} ':
        end += 1
    return payload[pos:end]


def cpp_parse_health_mode(raw, fallback):
    if raw == "":
        return fallback
    if raw in ("value", "1"):
        return 1
    if raw in ("percent", "percentage", "0"):
        return 0
    return fallback


def cpp_parse_bool(raw, fallback):
    if raw == "":
        return fallback
    if raw in ("true", "1"):
        return True
    if raw in ("false", "0"):
        return False
    return fallback


def cpp_parse_health_display(raw, fallback):
    if raw == "":
        return fallback
    if raw in ("text", "value_only", "1"):
        return 1
    if raw in ("both", "all", "2"):
        return 2
    if raw in ("bar", "bar_only", "0"):
        return 0
    return fallback


class EspHealthProtocolTests(unittest.TestCase):
    def setUp(self):
        if str(PACKAGE_ROOT) not in sys.path:
            sys.path.insert(0, str(PACKAGE_ROOT))
        from core.universal_hook_manager import UniversalHookManager

        self.manager = UniversalHookManager.get_instance()

    def _install_fake_pipe(self, include_health=True, include_outline=True):
        sent = {}

        def fake_send(payload, timeout_ms=None):
            sent.clear()
            sent.update(payload)
            response = {
                "ok": True,
                "esp_box": payload["esp_box"],
                "esp_all_players": payload["esp_all_players"],
                "revision": payload["revision"],
            }
            if include_health:
                response["esp_health_mode"] = payload["esp_health_mode"]
                response["esp_health_display"] = payload["esp_health_display"]
            if include_outline:
                response["esp_box_outline"] = payload["esp_box_outline"]
            return response

        self.manager._pipe = object()
        self.manager._send = fake_send
        self.manager._log = lambda *args, **kwargs: None
        self.manager._save_revision = lambda: None
        return sent

    def test_protocol_version_is_six(self):
        self.assertEqual(self.manager.PROTOCOL_VERSION, 6)
        pipe = (SOURCE_ROOT / "esp" / "named_pipe_server.cpp").read_text(encoding="utf-8")
        for part in (
            "PROTOCOL_VERSION = 6",
            'DLL_VERSION = "1.8.3"',
            "esp_box_outline",
            "esp_diag_candidates",
        ):
            self.assertIn(part, pipe)

    def test_set_state_sends_health_codes(self):
        sent = self._install_fake_pipe()
        ok = self.manager.set_esp_state(True, "all_players", "value", "text")
        self.assertTrue(ok)
        self.assertEqual(sent["cmd"], "set_state")
        self.assertEqual(sent["esp_health_mode"], 1)
        self.assertEqual(sent["esp_health_display"], 1)
        self.assertEqual(self.manager._esp_health_mode, "value")
        self.assertEqual(self.manager._esp_health_display, "text")

    def test_health_options_update_only_touches_health(self):
        sent = self._install_fake_pipe()
        self.manager.set_esp_health_options("percent", "bar")
        self.assertEqual(sent["esp_health_mode"], 0)
        self.assertEqual(sent["esp_health_display"], 0)
        self.assertEqual(self.manager._esp_health_mode, "percent")
        self.assertEqual(self.manager._esp_health_display, "bar")

    def test_box_outline_is_sent_and_synced(self):
        sent = self._install_fake_pipe()
        self.assertTrue(self.manager.set_esp_state(True, "enemy_only", "percent", "both", False))
        self.assertEqual(sent["esp_box_outline"], False)
        self.assertFalse(self.manager._esp_box_outline)

        sent = self._install_fake_pipe()
        self.assertTrue(self.manager.set_esp_box_outline(True))
        self.assertEqual(sent["esp_box_outline"], True)
        self.assertTrue(self.manager._esp_box_outline)

    def test_cpp_parser_reads_python_payload(self):
        sent = self._install_fake_pipe()
        self.manager.set_esp_state(True, "enemy_only", "value", "both", False)
        payload = json.dumps(sent, separators=(",", ":"))
        self.assertEqual(cpp_parse_health_mode(cpp_get_json_string(payload, "esp_health_mode"), -1), 1)
        self.assertEqual(cpp_parse_health_display(cpp_get_json_string(payload, "esp_health_display"), -1), 2)
        self.assertEqual(cpp_get_json_string(payload, "esp_all_players"), "false")
        self.assertEqual(cpp_parse_bool(cpp_get_json_string(payload, "esp_box_outline"), True), False)
        # 字段缺失时沿用当前状态，不能把开关意外改回 true。
        self.assertEqual(cpp_parse_bool("", False), False)
        self.assertEqual(cpp_parse_bool("", True), True)

    def test_old_dll_response_is_rejected(self):
        # 旧 DLL（协议 2）不返回血量字段：必须判失败，避免继续复用带闪退风险的旧镜像。
        self._install_fake_pipe(include_health=False)
        ok = self.manager.set_esp_state(True, "enemy_only", "percent", "both")
        self.assertFalse(ok)

    def test_protocol_four_dll_without_outline_is_rejected(self):
        # 协议 4 的旧 DLL 不认识 esp_box_outline：必须判失败（否则方框开关会静默失效）。
        self._install_fake_pipe(include_outline=False)
        ok = self.manager.set_esp_state(True, "enemy_only", "percent", "both", False)
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
