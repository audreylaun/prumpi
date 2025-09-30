# -*- mode: python ; coding: utf-8 -*-

import sys
import os

block_cipher = None

a = Analysis(
    ['full_game.py'],
    pathex=[],
    binaries=[],
    datas=[('data', 'data')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Prumpi-World',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='data/icon.ico',   # Use a .ico for Windows!
)

# Dynamically find python DLL location
if sys.platform == "win32":
    python_dll = os.path.join(sys.base_prefix, 'python313.dll')
else:
    python_dll = None

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    # Add the Python DLL to the _internal folder if on Windows
    ('_internal', [python_dll] if python_dll else [], 'BINARY'),
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Prumpi-World'
)
