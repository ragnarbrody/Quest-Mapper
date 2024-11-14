# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],  # Arquivo principal
    pathex=['C:\\Users\\lucas.lima\\Desktop\\Lucas\\TestePython2'],  # Caminho do projeto
    binaries=[],
    datas=[],
    hiddenimports=[
        'pygame',  # Inclui a biblioteca pygame
        'sys',      # Inclui o sys
    ],  # Adiciono aqui as importações ocultas, se necessário
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Quest Mapper',  # Nome do executável
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],  # Adiciono aqui, exclusões do UPX se houver arquivos sensíveis
    runtime_tmpdir=None,
    console=False,  # Define como "False" para não ter uma janela de console
)