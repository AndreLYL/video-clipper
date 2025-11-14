# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['video_clipper.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'imageio',
        'imageio_ffmpeg',
        'imageio.plugins',
        'imageio.plugins.ffmpeg',
        'imageio.core',
        'moviepy.video.fx.all',
        'moviepy.audio.fx.all',
        'moviepy.video.io.ffmpeg_reader',
        'moviepy.video.io.ffmpeg_writer',
        'PIL._tkinter_finder',
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

# 添加imageio的元数据
import os
import imageio
imageio_path = os.path.dirname(imageio.__file__)
a.datas += [
    ('imageio', imageio_path, 'DATA'),
]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='视频裁剪工具',
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
    icon=None,
)

