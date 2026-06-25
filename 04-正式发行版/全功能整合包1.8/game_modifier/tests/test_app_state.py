import unittest

from ui.state.app_state import AppState


class AppStateTests(unittest.TestCase):
    def test_app_state_serializes_feature_payload(self):
        state = AppState.with_default_features(["knife", "weapon_giver"])
        state.features["knife"] = True
        state.knife_speed = 5.0
        state.weapon_giver_respawn_enabled = True
        state.battle_round_enabled = True

        self.assertEqual(
            state.to_feature_state_payload(),
            {
                "knife": {"enabled": True, "slider_value": 5.0},
                "weapon_giver": {"enabled": False, "respawn_weapon": True},
                "battle_round_always": {"enabled": True},
            },
        )


if __name__ == "__main__":
    unittest.main()
