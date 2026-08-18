from pathlib import Path

from waitress import serve

from app import create_app


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend" / "dist"

app = create_app(frontend_dir=FRONTEND_DIR)


if __name__ == "__main__":
    serve(
        app,
        host="127.0.0.1",
        port=5000,
        threads=8,
    )