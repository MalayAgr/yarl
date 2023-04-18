# -*- mode: python ; coding: utf-8 -*-
# https://pyinstaller.readthedocs.io/en/stable/spec-files.html
block_cipher = None
PROJECT_NAME = "yarl"

a = Analysis(
    ["yarl/main.py"],
    binaries=[],
    datas=[("assets", "assets")],  # Include all files in the 'assets' directory.
    hiddenimports=[],
    hookspath=[],
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
    [],
    exclude_binaries=True,
    name=PROJECT_NAME,  # Name of the executable.
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Set to False to disable the Windows terminal.
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=PROJECT_NAME,  # Name of the distribution directory.
)