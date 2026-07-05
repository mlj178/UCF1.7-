# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import fnmatch
import shutil
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(SPEC))

# 定义要包含的数据文件
datas = []
binaries = []

# customtkinter 已安装在本机 Python 环境中；显式收集主题、字体等资源，避免缺少 hook 时遗漏。
datas += collect_data_files("customtkinter")

def add_data_tree(source_dir, target_dir, excludes=()):
    """Collect a local data directory without copying it into the project."""
    if not os.path.isdir(source_dir):
        return
    for root, dirs, files in os.walk(source_dir):
        dirs[:] = [name for name in dirs if not any(fnmatch.fnmatch(name, pattern) for pattern in excludes)]
        relative_dir = os.path.relpath(root, source_dir)
        destination = target_dir if relative_dir == "." else os.path.join(target_dir, relative_dir)
        for filename in files:
            if any(fnmatch.fnmatch(filename, pattern) for pattern in excludes):
                continue
            datas.append((os.path.join(root, filename), destination))


def copy_data_tree(source_dir, target_dir, excludes=()):
    if os.path.isdir(target_dir):
        shutil.rmtree(target_dir)
    ignore = shutil.ignore_patterns(*excludes) if excludes else None
    shutil.copytree(source_dir, target_dir, ignore=ignore)


# 使用本机 Python 安装里的 Tcl/Tk 资源，不再依赖项目内复制的 Tcl/Tk 目录。
# 目标目录名保持 PyInstaller 标准值，便于内置 pyi_rth__tkinter.py 在 exe 启动时自动定位。
python_tcl_dir = os.path.join(sys.base_prefix, "tcl")
local_tcl_library = os.path.join(python_tcl_dir, "tcl8.6")
local_tk_library = os.path.join(python_tcl_dir, "tk8.6")
local_tcl_modules = os.path.join(python_tcl_dir, "tcl8")

if not os.path.isfile(os.path.join(local_tcl_library, "init.tcl")):
    raise FileNotFoundError("本机 Python 缺少 Tcl init.tcl，请修复 Python Tcl/Tk 安装后再打包")
if not os.path.isfile(os.path.join(local_tk_library, "tk.tcl")):
    raise FileNotFoundError("本机 Python 缺少 Tk tk.tcl，请修复 Python Tcl/Tk 安装后再打包")

tcl_staging_dir = os.path.join(current_dir, "build", "_tcltk_staging")
staged_tcl_library = os.path.join(tcl_staging_dir, "tcl8.6")
staged_tk_library = os.path.join(tcl_staging_dir, "tk8.6")
staged_tcl_modules = os.path.join(tcl_staging_dir, "tcl8")
os.makedirs(tcl_staging_dir, exist_ok=True)
copy_data_tree(local_tcl_library, staged_tcl_library, excludes=("demos", "*.lib", "tclConfig.sh"))
copy_data_tree(local_tk_library, staged_tk_library, excludes=("demos", "*.lib", "tkConfig.sh"))
copy_data_tree(local_tcl_modules, staged_tcl_modules)

os.environ["TCL_LIBRARY"] = staged_tcl_library
os.environ["TK_LIBRARY"] = staged_tk_library
add_data_tree(staged_tcl_library, "_tcl_data")
add_data_tree(staged_tk_library, "_tk_data")
add_data_tree(staged_tcl_modules, "tcl8")

# 显式带上 Tk 相关二进制，避免 tkinter 被环境探测误判后遗漏。
python_dlls_dir = os.path.join(sys.base_prefix, "DLLs")
for binary_name in ("_tkinter.pyd", "tcl86t.dll", "tk86t.dll"):
    binary_path = os.path.join(python_dlls_dir, binary_name)
    if os.path.isfile(binary_path):
        binaries.append((binary_path, "."))

# 1. 添加资源文件（音效和图片）
resource_dir = os.path.join(os.path.dirname(current_dir), "资源")
if os.path.exists(resource_dir):
    for file in os.listdir(resource_dir):
        file_path = os.path.join(resource_dir, file)
        if os.path.isfile(file_path):
            datas.append((file_path, "资源"))

# 2. 添加插件目录（manifest / script.js / panel.py）
features_dir = os.path.join(current_dir, "features")
if os.path.exists(features_dir):
    datas.append((features_dir, "features"))

# 2.1 添加 data 目录（配置文件）
data_dir = os.path.join(current_dir, "data")
if os.path.exists(data_dir):
    # 排除运行时生成/本机用户记录文件，只打包基础配置
    for file in os.listdir(data_dir):
        if file.endswith('.json') and file not in {'user_config.json', 'feature_state.json'}:
            file_path = os.path.join(data_dir, file)
            datas.append((file_path, "data"))

# 3. 只添加 Universal Hook 运行所需文件，不打包运行日志
plugins_dir = os.path.join(current_dir, "plugins")
universal_hook_dir = os.path.join(plugins_dir, "universal_hook")
for plugin_file in ("inject.exe", "Universal-ImGui-Hook.dll", "universal_hook.json"):
    plugin_path = os.path.join(universal_hook_dir, plugin_file)
    if os.path.isfile(plugin_path):
        datas.append((plugin_path, "game_modifier/plugins/universal_hook"))

# 4. 添加 ui 目录下的文件（如果有资源）
ui_dir = os.path.join(current_dir, "ui")
if os.path.exists(ui_dir):
    for root, dirs, files in os.walk(ui_dir):
        for file in files:
            if not file.endswith('.py'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(root, current_dir)
                datas.append((file_path, rel_path))

a = Analysis(
    ['main.py'],
    pathex=[current_dir],
    binaries=binaries,
    datas=datas,
    hiddenimports=[
        'customtkinter',
        'frida',
        'frida_tools',
        'psutil',
        'pynput',
        'keyboard',
        'pygame',
        'PIL',
        'core.config',
        'core.event_bus',
        'core.frida_manager',
        'core.game_session_manager',
        'core.hotkey_manager',
        'core.sound_manager',
        'core.universal_hook_manager',
        'core.weapon_hotkey_manager',
        'core.weapon_catalog',
        'core.log_manager',
        'core.log_router',
        'core.plugin.plugin_registry',
        'core.plugin.manifest_loader',
        'core.plugin.plugin_base',
        'core.plugin.plugin_contract',
        'core.repositories.desired_state_repository',
        'core.repositories.feature_state_repository',
        'core.services.app_persistence_service',
        'core.services.feature_command_service',
        'core.services.game_connection_service',
        'core.lifecycle.feature_lifecycle',
        'core.lifecycle.shutdown_manager',
        'core.frida_runtime.rpc_client',
        'core.frida_runtime.script_manager',
        'core.frida_runtime.session_manager',
        'core.config_runtime.config_manager',
        'ui.app',
        'ui.settings_window',
        'ui.panel_context',
        'ui.views.shell_view',
        'ui.views.plugin_tab_builder',
        'ui.views.feature_tabs_view',
        'ui.views.nano4t_view',
        'ui.views.weapon_giver_view',
        'ui.pages.plugin_feature_page',
        'ui.components.feature_card',
        'ui.controllers.action_router',
        'ui.controllers.app_event_controller',
        'ui.controllers.feature_action_controller',
        'ui.controllers.plugin_event_router',
        'ui.controllers.plugin_lifecycle_router',
        'ui.state.app_state',
    ] + collect_submodules('features') + collect_submodules('core') + collect_submodules('ui') + collect_submodules('tkinter'),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='UCF2.0修改器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    uac_admin=True,
)
