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

# 3. 添加 data 目录下的所有 JSON 文件
data_dir = os.path.join(current_dir, "data")
if os.path.exists(data_dir):
    datas.append((data_dir, "game_modifier/data"))

# 4. 添加 plugins 目录
plugins_dir = os.path.join(current_dir, "plugins")
if os.path.exists(plugins_dir):
    datas.append((plugins_dir, "game_modifier/plugins"))

# 5. 添加 ui 目录下的文件（如果有资源）
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
        'features.aim',
        'features.ammo',
        'features.battle_round_always',
        'features.esp_box',
        'features.gather',
        'features.godmode',
        'features.gravity',
        'features.is_bot',
        'features.knife',
        'features.knife_range',
        'features.move_speed',
        'features.nano4t',
        'features.recoil',
        'features.reload_speed',
        'features.round_skip',
        'features.skill_cd',
        'features.speed_gun',
        'features.time_freeze',
        'features.time_scale',
        'features.weapon_giver',
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
    name='UCF1.7修改器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 如果有图标文件，可以在这里指定路径
    manifest='app.manifest',  # 使用清单文件请求管理员权限
)
