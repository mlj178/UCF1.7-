import tempfile
import unittest
from pathlib import Path

from core.repositories.feature_state_repository import FeatureStateRepository
from core.repositories.nano4t_config_repository import Nano4tConfigRepository


class RepositoryTests(unittest.TestCase):
    def test_nano4t_repository_clamps_invalid_values(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = Nano4tConfigRepository(Path(tmp_dir) / "Nano-4T-selector.json")
            repo.save({"ghost": 99, "human": -1})

            self.assertEqual(repo.load(), {"ghost": 0, "human": 10})

    def test_feature_state_repository_round_trips_state(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = FeatureStateRepository(Path(tmp_dir) / "feature_state.json")
            payload = {
                "knife": {"enabled": True, "slider_value": 5.0},
                "battle_round_always": {"enabled": False},
            }

            repo.save(payload)

            self.assertEqual(repo.load(), payload)


if __name__ == "__main__":
    unittest.main()
