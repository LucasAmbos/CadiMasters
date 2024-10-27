# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],  # O arquivo principal do seu programa
    pathex=[],    # Caminho do seu projeto, pode ser deixado vazio se estiver na mesma pasta
    binaries=[],  # Se você tiver binários extras (não parece ser o caso)
    datas=[
        ('bats', 'bats'),                      # Inclui a pasta bats
        ('install_printer', 'install_printer'),# Inclui a pasta install_printer
        ('logs', 'logs'),                      # Inclui a pasta logs
        ('modules', 'modules'),                # Inclui a pasta modules
        ('programas.json', '.'),               # Inclui o arquivo programas.json na raiz
        ('install_program.bat', '.'),          # Inclui o arquivo install_program.bat na raiz
    ],
    hiddenimports=[],
    hookspath=[],
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
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False se for GUI, True se quiser console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='logo.ico',  # Inclui o ícone
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main'
)
