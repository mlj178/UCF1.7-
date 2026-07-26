# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
import os
import sys


block_cipher = None
current_dir = os.path.dirname(os.path.abspath(SPEC))
entry_file = os.path.join(current_dir, "AAAAA-player_profile_editor_ui.py")

datas = collect_data_files("customtkinter")
env_tcl86_dir = os.environ.get("TCL_LIBRARY")
env_tk86_dir = os.environ.get("TK_LIBRARY")

if env_tcl86_dir and env_tk86_dir and os.path.isdir(env_tcl86_dir) and os.path.isdir(env_tk86_dir):
    datas.append((env_tcl86_dir, os.path.join("tcl", "tcl8.6")))
    datas.append((env_tk86_dir, os.path.join("tcl", "tk8.6")))

python_dir_candidates = [
    os.path.dirname(sys.executable),
    os.path.dirname(os.path.dirname(sys.executable)),
]

if not (env_tcl86_dir and env_tk86_dir):
    for python_dir in python_dir_candidates:
        tcl_dir = os.path.join(python_dir, "tcl")
        tcl86_dir = os.path.join(tcl_dir, "tcl8.6")
        tk86_dir = os.path.join(tcl_dir, "tk8.6")
        if os.path.isdir(tcl86_dir) and os.path.isdir(tk86_dir):
            datas.append((tcl86_dir, os.path.join("tcl", "tcl8.6")))
            datas.append((tk86_dir, os.path.join("tcl", "tk8.6")))
            break

a = Analysis(
    [entry_file],
    pathex=[current_dir],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "customtkinter",
        "tkinter",
        "tkinter.filedialog",
        "tkinter.messagebox",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[os.path.join(current_dir, "pyi_tcl_runtime_hook.py")],
    excludes=[
        "test_player_profile_service",
        "unittest",
    ],
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
    name="玩家信息修改器",
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
    icon=None,
    uac_admin=True,
)
