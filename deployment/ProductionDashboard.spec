from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules


PROJECT_DIR = Path(SPECPATH).parent
BACKEND_DIR = PROJECT_DIR / "backend"
FRONTEND_DIR = PROJECT_DIR / "frontend" / "dist"


hiddenimports = (
    collect_submodules("routes")
    + collect_submodules("services")
)


a = Analysis(
    [str(BACKEND_DIR / "server.py")],
    pathex=[str(BACKEND_DIR)],
    binaries=[],
    datas=[
        (
            str(BACKEND_DIR / "reports" / "assets"),
            "reports/assets",
        ),
        (
            str(FRONTEND_DIR),
            "frontend",
        ),
    ],
    hiddenimports=hiddenimports,
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
    a.binaries,
    a.datas,
    [],
    name="ProductionDashboard",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)