import os
from pathlib import Path

def _load_dotenv(path: str = ".env") -> None:
    """Tiny .env loader so ChaosForge works without python-dotenv."""
    p = Path(path)
    if not p.exists():
        return
    for raw in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)

_load_dotenv()

SECRET_KEY = os.getenv("CHAOSFORGE_SECRET_KEY", "dev-secret-change-me")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chaosforge.db")
ARTIFACT_ROOT = Path(os.getenv("ARTIFACT_ROOT", "artifacts"))
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

# LLM configuration. The app still runs without keys because LLM_MODE=auto falls back.
LLM_MODE = os.getenv("LLM_MODE", "auto").lower()  # off | auto | strict
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "off").lower()  # off | openai | gemini | openai-compatible
LLM_MODEL = os.getenv("LLM_MODEL", os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", os.getenv("LLM_MODEL", "gemini-1.5-flash"))
LLM_REQUEST_TIMEOUT = int(os.getenv("LLM_REQUEST_TIMEOUT", "45"))
