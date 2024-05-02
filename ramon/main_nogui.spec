# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main_nogui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['plugins.bezel.plugin', 'plugins.capture.plugin', 'plugins.cartridge.plugin', 'plugins.cheevocube.plugin', 'plugins.clock.plugin', 'plugins.flysim.plugin', 'plugins.logos.plugin', 'plugins.mascots.plugin', 'plugins.progressbar.plugin', 'plugins.recentunlocks.plugin', 'plugins.roulette.plugin', 'plugins.rpgchat.plugin', 'plugins.score.plugin', 'plugins.status.plugin', 'plugins.twitchchat.plugin', 'plugins.xboxcheevos.plugin', 'pywintypes', 'win32gui', 'pywin32'],
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
    name='main_nogui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
