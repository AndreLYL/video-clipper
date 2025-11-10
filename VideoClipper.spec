# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, copy_metadata

block_cipher = None

# 收集imageio相关的数据文件和元数据
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
    name='VideoClipper_v1.0.0',
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
    icon=None,
    version_info={
        'version': '1.0.0.0',
        'company_name': 'andre.li',
        'file_description': '视频裁剪工具',
        'product_name': 'VideoClipper',
        'product_version': '1.0.0',
        'copyright': 'Copyright (c) 2025 andre.li'
    }
)

