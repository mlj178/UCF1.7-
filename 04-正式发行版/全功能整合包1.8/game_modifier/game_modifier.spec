# -*- mode: python ; coding: utf-8 -*-
import os
import sys

block_cipher = None

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(SPEC))

# 定义要包含的数据文件
datas = []

# 1. 添加资源文件（音效和图片）
resource_dir = os.path.join(os.path.dirname(current_dir), "资源")
if os.path.exists(resource_dir):
    for file in os.listdir(resource_dir):
        file_path = os.path.join(resource_dir, file)
        if os.path.isfile(file_path):
            datas.append((file_path, "资源"))

# 2. 添加 scripts 目录下的所有 JS 文件
scripts_dir = os.path.join(current_dir, "scripts")
if os.path.exists(scripts_dir):
    datas.append((scripts_dir, "game_modifier/scripts"))

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
    binaries=[],
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
        'features',
        'features.feature_01_unlimited_ammo',
        'features.feature_02_no_recoil',
        'features.feature_03_unlimited_time',
        'features.feature_04_fast_knife',
        'features.feature_05_fast_reload_buff',
        'features.feature_06_movement_speed',
        'features.feature_07_knife_attack_range',
        'features.feature_08_gather_enemies',
        'features.feature_09_high_jump_low_gravity',
        'features.feature_10_skip_round',
        'features.feature_11_auto_aim',
        'features.feature_12_invincibility',
        'features.feature_13_fire_rate_auto_sniper',
        'features.feature_14_become_bot',
        'features.feature_15_buff_selector',
        'features.feature_16_weapon_giver',
        'features.feature_17_skill_no_cooldown',
        'features.feature_18_universal_esp_box',
        'features.feature_19_battle_round',
        'features.feature_20_unity_time_acceleration',
        'core.config',
        'core.event_bus',
        'core.feature_registry',
        'core.frida_manager',
        'core.game_session_manager',
        'core.hotkey_manager',
        'core.sound_manager',
        'core.universal_hook_manager',
        'core.weapon_hotkey_manager',
        'ui.app',
        'ui.settings_window',
        'ui.widgets',
    ],
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
    name='UCF1.8修改器',
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
    icon=None,  # 如果有图标文件，可以在这里指定路径
    uac_admin=True,
)
