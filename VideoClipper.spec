# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, copy_metadata

# 收集imageio相关数据文件
datas = []
datas += collect_data_files('imageio')
datas += collect_data_files('imageio_ffmpeg')
datas += copy_metadata('imageio')
datas += copy_metadata('imageio-ffmpeg')

a = Analysis(
    ['video_clipper.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['imageio', 'imageio_ffmpeg', 'imageio.core', 'imageio.plugins'],
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
    name='VideoClipper_v1.1.0',
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
    version='file_version_info.txt',
    icon=None,
)
