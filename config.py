"""Central configuration: paths, environment variables, model names."""
import os
from pathlib import Path

from dotenv import load_dotenv

# Project root = the folder that contains "app/"
BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"

load_dotenv(BASE_DIR / ".env")

TEMPLATE_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"

# SQLite file lives in the project root (auto-created on first run)
DATABASE_URL = os.getenv("FITBUDDY_DB_URL", f"sqlite:///{(BASE_DIR / 'fitbuddy.db').as_posix()}")

# Gemini Pro  -> workout generation + feedback updates
# Gemini Flash -> nutrition / recovery tips
GEMINI_PRO_MODEL = os.getenv("GEMINI_PRO_MODEL", "gemini-2.5-pro")
GEMINI_FLASH_MODEL = os.getenv("GEMINI_FLASH_MODEL", "gemini-2.5-flash")


def get_api_key() -> str | None:
    """Return the Gemini API key (GOOGLE_API_KEY preferred, GEMINI_API_KEY accepted)."""
    key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if key and key.strip() and key.strip() != "your_gemini_api_key_here":
        return key.strip()
    return None
