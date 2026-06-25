import unittest
from dataclasses import dataclass

from core.config import NANO4T_ATTRS
from ui.views.common import bind_view_handles
from ui.views.nano4t_view import (
    GRAVITY_MODE_VALUES,
    build_nano4t_option_values,
    build_nano4t_selection_copy,
)


@dataclass
class DummyHandles:
    alpha: int
    beta: str


class DummyTarget:
    pass


class ViewHelperTests(unittest.TestCase):
    def test_bind_view_handles_applies_all_attributes(self):
        target = DummyTarget()

        bind_view_handles(target, DummyHandles(alpha=1, beta="ok"))

        self.assertEqual(target.alpha, 1)
        self.assertEqual(target.beta, "ok")

    def test_build_nano4t_option_values_uses_expected_ranges(self):
        ghost_values = build_nano4t_option_values(NANO4T_ATTRS, 0, 10)
        human_values = build_nano4t_option_values(NANO4T_ATTRS, 10, 20)

        self.assertEqual(len(ghost_values), 10)
        self.assertEqual(len(human_values), 10)
        self.assertTrue(ghost_values[0].startswith("0: "))
        self.assertTrue(human_values[0].startswith("10: "))

    def test_build_nano4t_selection_copy_returns_display_and_desc(self):
        display, desc = build_nano4t_selection_copy(NANO4T_ATTRS, 10)

        self.assertEqual(display, f"10: {NANO4T_ATTRS[10][0]}")
        self.assertEqual(desc, f"效果: {NANO4T_ATTRS[10][1]}")

    def test_gravity_mode_values_remain_two_expected_choices(self):
        self.assertEqual(GRAVITY_MODE_VALUES, ("仅自己", "全部玩家"))


if __name__ == "__main__":
    unittest.main()
