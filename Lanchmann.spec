# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\modules\\__main__.py'],
    pathex=[],
    binaries=[],
    datas=[('src/assets/fonts', 'assets/fonts'), ('src/assets/icons', 'assets/icons'), ('src/assets/pictures', 'assets/pictures'), ('src/assets/screenshots', 'assets/screenshots'), ('src/modules/db/', 'modules/db')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Lanchmann',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
