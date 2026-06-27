# -*- mode: python ; coding: utf-8 -*-
import os
import sys

block_cipher = None

current_dir = os.path.dirname(os.path.abspath(SPEC))

# JS 脚本打包到 EXE 内部
js_file = os.path.join(current_dir, "third_person_basic_v3_14_stable_yaw.js")

datas = []
if os.path.exists(js_file):
    datas.append((js_file, "."))

a = Analysis(
    ['third_person_basic_ui_v3_14.py'],
    pathex=[current_dir],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'customtkinter',
        'frida',
        'frida_tools',
        'psutil',
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
    name='第三人称视角_v3.14',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
)
