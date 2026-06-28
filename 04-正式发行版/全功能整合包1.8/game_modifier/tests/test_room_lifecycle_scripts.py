import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = PROJECT_ROOT / "scripts"


class RoomLifecycleScriptTests(unittest.TestCase):
    def test_isbot_hooks_room_exit_and_refuses_stale_client_data(self):
        js = (SCRIPTS / "14-become_bot.js").read_text(encoding="utf-8")

        self.assertIn("ModeBase_ExitGame: 0xAEE850", js)
        self.assertIn("Player_OnDestroy: 0xB511C0", js)
        self.assertIn("GameManager_OnDestroy: 0xAFB6F0", js)
        self.assertIn("roomGeneration", js)
        self.assertIn("capturedGeneration", js)
        self.assertIn("if (capturedGeneration !== roomGeneration) return false;", js)
        self.assertIn("clearRoomState", js)

    def test_roundskip_clears_on_room_exit_and_checks_generation_token(self):
        js = (SCRIPTS / "10-skip_round.js").read_text(encoding="utf-8")

        self.assertIn("ModeBase_ExitGame: 0xAEE850", js)
        self.assertIn("GameManager_OnDestroy: 0xAFB6F0", js)
        self.assertIn("roomGeneration", js)
        self.assertIn("modeBaseGeneration", js)
        self.assertIn("if (modeBaseGeneration !== roomGeneration)", js)
        self.assertIn("modeBaseInstance = null", js)

    def test_gather_clears_room_cached_pointers_on_exit_or_destroy(self):
        js = (SCRIPTS / "08-gather_enemies.js").read_text(encoding="utf-8")

        self.assertIn("ModeBase_ExitGame: 0xAEE850", js)
        self.assertIn("GameManager_OnDestroy: 0xAFB6F0", js)
        self.assertIn("clearRoomState", js)
        self.assertIn("gm = null; mm = null; recentBotPlayers = {}; ntp = false;", js)

    def test_ammo_saves_attach_handle_for_detach(self):
        js = (SCRIPTS / "01-unlimited_ammo.js").read_text(encoding="utf-8")

        self.assertIn("var rpgFireHook = Interceptor.attach(addrRpgFire", js)
        self.assertIn("hooks.push({ type: 'attach', handle: rpgFireHook });", js)
        self.assertIn("hooks[i].handle.detach();", js)


if __name__ == "__main__":
    unittest.main()
