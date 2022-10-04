from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    CONTENT_DIR = f"{BASE_DIR}/content"
    LAYOUT_DIR = f"{BASE_DIR}/layout"
    STATIC_SRC_PATH = f"{BASE_DIR}/static"
    DIST_SRC_PATH = f"{BASE_DIR}/dist/static"
    SITE_NAME = "PyGoose"
    SITE_DESCRIPTION = "PyGoose is awesome"