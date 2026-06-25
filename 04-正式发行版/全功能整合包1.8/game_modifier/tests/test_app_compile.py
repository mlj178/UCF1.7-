import py_compile
import unittest
from pathlib import Path


class AppCompileTests(unittest.TestCase):
    def test_app_module_compiles(self):
        app_path = Path(__file__).resolve().parents[1] / "ui" / "app.py"

        py_compile.compile(str(app_path), doraise=True)


if __name__ == "__main__":
    unittest.main()
