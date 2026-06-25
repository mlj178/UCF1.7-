import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEXT_PATHS = [
    PROJECT_ROOT / "core",
    PROJECT_ROOT / "ui",
    PROJECT_ROOT.parent / "新增内容.md",
]

MOJIBAKE_MARKERS = (
    "\ufffd",
    "鐢",
    "锛",
    "銆",
    "鈥",
    "鈿",
    "馃",
    "绋",
    "鏂",
    "妯",
    "璧",
    "姝",
    "滆",
)


class TextEncodingGuardTests(unittest.TestCase):
    def test_user_facing_text_has_no_common_mojibake_markers(self):
        bad_hits = []
        for base_path in TEXT_PATHS:
            files = [base_path] if base_path.is_file() else base_path.rglob("*.py")
            for path in files:
                text = path.read_text(encoding="utf-8")
                for line_no, line in enumerate(text.splitlines(), 1):
                    if any(marker in line for marker in MOJIBAKE_MARKERS):
                        rel_path = path.relative_to(PROJECT_ROOT.parent)
                        bad_hits.append(f"{rel_path}:{line_no}: {line.strip()}")

        self.assertEqual([], bad_hits)


if __name__ == "__main__":
    unittest.main()
