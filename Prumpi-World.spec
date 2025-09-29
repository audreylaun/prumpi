# -*- mode: python ; coding: utf-8 -*-
import sys

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

pyz = PYZ(a.pure)

# Select the correct icon for the platform
if sys.platform == "darwin":
    exe_icon = "data/icon.icns"
elif sys.platform == "win32":
    exe_icon = "data/icon.ico"
else:
    exe_icon = None

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
    console=False,       # False for GUI apps
    windowed=True,       # hides console on Windows
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=exe_icon,
    onefile=True,        # produce a single executable
)

# macOS app bundle (only runs on macOS)
if sys.platform == "darwin":
    app = BUNDLE(
        exe,
        a.binaries,
        a.datas,
        name='Prumpi-World.app',
        icon=exe_icon,
        bundle_identifier="com.yourname.prumpiworld",
    )


