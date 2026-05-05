# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['AAAAA-bot_to_spawn_v24.py'],
    pathex=[],
    binaries=[],
    datas=[('AAAAA-bot_to_spawn_v24.js', '.')],
    hiddenimports=['customtkinter', 'frida', 'psutil'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=True,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='Bot集合器_v24',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
