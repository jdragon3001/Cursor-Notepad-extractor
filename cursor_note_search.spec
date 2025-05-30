# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['note_search_gui.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        # Include documentation files
        ('README.md', '.'),
        ('PORTABILITY_GUIDE.md', '.'),
        ('STRUCTURE.md', '.'),
        ('PROBLEM_LOG.txt', '.'),
        ('requirements.txt', '.'),
        # Include module directories
        ('database', 'database'),
        ('utils', 'utils'),
    ],
    hiddenimports=[
        # Ensure all our modules are included
        'database.cursor_db',
        'utils.config',
        'note_finder',
        'note_parser',
        # tkinter dependencies
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        # Standard library modules we use
        'sqlite3',
        'pathlib',
        'json',
        'threading',
        'datetime',
        'os',
        're',
        'time',
        # Optional dependencies (gracefully handled if missing)
        'reportlab',
        'reportlab.lib.pagesizes',
        'reportlab.platypus',
        'reportlab.lib.styles',
        'docx',
        'docx.shared',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'cv2',
        'tensorflow',
        'torch',
        'jupyter',
        'IPython',
    ],
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
    name='CursorNoteSearch',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI application (no console window)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # You could add an icon file here if you have one
) 