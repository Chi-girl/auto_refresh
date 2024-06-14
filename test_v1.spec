# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['test_v1.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', './assets'), ('C:/Users/gabriel.lacanilao.jr/Desktop/TULIP SAMPLE/Bootleg/venv/Lib/site-packages/fastparquet.libs', './fastparquet.libs')],
    hiddenimports=['pkg_resources.py2_warn', 'importlib_resources'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='test_v1',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\accenture_logo.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='test_v1',
)
