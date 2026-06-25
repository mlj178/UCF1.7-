import unittest

from core.services.feature_command_service import FeatureCommandService
from core.services.weapon_giver_service import WeaponGiverService


class FakeFrida:
    def __init__(self):
        self.toggle_calls = []
        self.export_calls = []

    def send_toggle(self, feature, enable, extra_params=None):
        self.toggle_calls.append((feature, enable, extra_params))

    def call_export(self, name, *args):
        self.export_calls.append((name, args))
        return {"ok": True}


class ServiceTests(unittest.TestCase):
    def test_feature_command_service_sends_toggle_and_config_calls(self):
        frida = FakeFrida()
        service = FeatureCommandService(frida)

        service.toggle_feature("knife", True, slider_value=5.0)
        service.toggle_feature("timescale", True, slider_value=1.5)

        self.assertEqual(
            frida.toggle_calls,
            [
                ("knife", True, None),
                ("knife_speed", 5.0, None),
                ("timescale", True, {"speed": 1.5}),
            ],
        )

    def test_weapon_giver_service_uses_expected_exports(self):
        frida = FakeFrida()
        service = WeaponGiverService(frida)

        service.give_weapon("120")
        service.set_respawn_weapon("120", "NANOKNIFE")
        service.clear_respawn_weapon()

        self.assertEqual(
            frida.export_calls,
            [
                ("giveweapon", ("120", True, True)),
                ("setrespawnweapon", ("120", "NANOKNIFE")),
                ("clearrespawnweapon", ()),
            ],
        )


if __name__ == "__main__":
    unittest.main()
