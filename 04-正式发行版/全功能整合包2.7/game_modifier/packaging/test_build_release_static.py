import unittest
from pathlib import Path


BUILD_SCRIPT = Path(__file__).with_name("build_release.ps1")
NON_DESTRUCTIVE_BUILD_SCRIPT = Path(__file__).with_name("build_release_non_destructive.ps1")
ONEDIR_SPEC = Path(__file__).parent.parent / "game_modifier_onedir.spec"
INSTALLER_SCRIPT = Path(__file__).with_name("installer.iss")


class BuildReleaseStaticTests(unittest.TestCase):
    def test_installer_filename_is_app_name_without_chinese_suffix(self):
        text = BUILD_SCRIPT.read_text(encoding="utf-8")

        self.assertIn('$installerPath = Join-Path $releaseDir "${appExeName}.exe"', text)
        self.assertNotIn('安装器.exe', text)

    def test_ui_data_collection_excludes_cache_and_test_files(self):
        text = ONEDIR_SPEC.read_text(encoding="utf-8")

        self.assertIn('dirs[:] = [name for name in dirs if name != "__pycache__"]', text)
        self.assertIn('if file.endswith((".py", ".pyc", ".pyo")) or file.startswith("test_") or file.endswith("_test"):', text)

    def test_installer_accepts_overridable_build_and_release_directories(self):
        text = INSTALLER_SCRIPT.read_text(encoding="utf-8")

        self.assertIn("#ifndef BuildDistDir", text)
        self.assertIn("#ifndef ReleaseOutputDir", text)

    def test_release_exe_name_follows_package_folder_name(self):
        """2.7 起 exe 统一叫“全功能整合包x.x”，spec / iss / 构建脚本三处必须一致。"""
        spec_text = ONEDIR_SPEC.read_text(encoding="utf-8")
        iss_text = INSTALLER_SCRIPT.read_text(encoding="utf-8")
        script_text = BUILD_SCRIPT.read_text(encoding="utf-8")

        self.assertIn('app_name = f"全功能整合包{package_version}"', spec_text)
        self.assertIn('#define AppExeName "全功能整合包" + AppVersion', iss_text)
        self.assertIn('$appExeName = "全功能整合包${packageVersion}"', script_text)
        self.assertIn("OutputBaseFilename={#AppName}", iss_text)

    def test_spec_ships_qr_code_and_win7_notice_into_resource_folder(self):
        spec_text = ONEDIR_SPEC.read_text(encoding="utf-8")

        self.assertIn('"UCF1.7Q群1095388251.jpg"', spec_text)
        self.assertIn('"win7用不了，只有win10和11能用.txt"', spec_text)
        self.assertIn('datas.append((extra_path, "资源"))', spec_text)

    def test_non_destructive_builder_uses_timestamped_output_and_never_removes_prior_release_dirs(self):
        self.assertTrue(NON_DESTRUCTIVE_BUILD_SCRIPT.is_file())
        text = NON_DESTRUCTIVE_BUILD_SCRIPT.read_text(encoding="utf-8")

        self.assertIn('Get-Date -Format "yyyyMMdd-HHmmss"', text)
        self.assertNotIn("Remove-Item", text)


if __name__ == "__main__":
    unittest.main()
