"""卡片说明文字折行（高 DPI 下不被裁字）的回归测试。

真实故障：125% 缩放下 CTkLabel 的 wraplength 会被乘 1.25，
比标签真实宽度更宽，Tk 不会重新折行，多出来的字被裁掉半截。
详见 ui/components/text_fit.py 的模块说明。
"""

import unittest
from pathlib import Path

from ui.components.text_fit import MIN_WRAP, fit_wrap_value


UI_DIR = Path(__file__).resolve().parent
TEXT_FIT = UI_DIR / "components" / "text_fit.py"
PLUGIN_FEATURE_PAGE = UI_DIR / "pages" / "plugin_feature_page.py"


class TextFitStaticTests(unittest.TestCase):
    def test_page_applies_text_fit_after_building_cards(self):
        text = PLUGIN_FEATURE_PAGE.read_text(encoding="utf-8")
        self.assertIn("from ui.components.text_fit import bind_text_wrap_tree", text)
        self.assertIn("bind_text_wrap_tree(scroll)", text)


class FitWrapValueTests(unittest.TestCase):
    """125% 缩放（用户机器的实际 DPI）下的换算。"""

    def test_shrinks_when_wrap_would_overflow_label(self):
        # 复现用户截图：卡片 330px、标签宽 304px、作者写 280 → 实际生效 350px
        value = fit_wrap_value(280, 304, 1.25)
        self.assertEqual(value, 241)
        # 换算回物理像素后必须落在标签宽度以内
        self.assertLessEqual(value * 1.25, 304)

    def test_keeps_authors_value_when_it_already_fits(self):
        # 作者故意写窄的（例如 35_room_player_count 的 190）保持原样
        self.assertEqual(fit_wrap_value(190, 600, 1.25), 190)
        self.assertEqual(fit_wrap_value(280, 600, 1.0), 280)

    def test_no_correction_before_layout(self):
        # 控件还没完成布局（winfo_width() == 1）时不要乱改
        self.assertEqual(fit_wrap_value(280, 1, 1.25), 280)
        self.assertEqual(fit_wrap_value(280, 304, 0), 280)

    def test_bound_label_keeps_the_authors_original_value(self):
        # 反复绑定不能把"第一次的值"当成新本意，否则会越收越窄
        source = TEXT_FIT.read_text(encoding="utf-8")
        self.assertIn('if getattr(label, "_wrap_base", None):', source)
        self.assertIn("label._wrap_base = base_wrap", source)

    def test_never_goes_below_minimum(self):
        self.assertEqual(fit_wrap_value(280, 40, 1.25), MIN_WRAP)

    def test_covers_every_scaling_the_layout_can_produce(self):
        for scaling in (1.0, 1.25, 1.5, 1.75, 2.0):
            for width in range(120, 700, 7):
                value = fit_wrap_value(280, width, scaling)
                self.assertLessEqual(
                    value * scaling,
                    width,
                    f"wraplength 换算后仍超出标签宽度: scaling={scaling} width={width}",
                )


if __name__ == "__main__":
    unittest.main()
