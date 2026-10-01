"""Shared Gemini client + helper used by all three AI modules."""
import os
import time
from functools import lru_cache

from google import genai

from app.config import get_api_key

BUSY_ERRORS = ("503", "UNAVAILABLE", "500", "INTERNAL", "overloaded", "high demand")
ATTEMPTS_PER_MODEL = 3   # tries per model when Google is busy (503)
WAIT_SECONDS = 6         # waits 6s, then 12s between tries

# Backup models, tried in order if the main model is busy / out of quota / not found.
DEFAULT_BACKUPS = ["gemini-flash-latest", "gemini-flash-lite-latest", "gemini-3.8-flash-lite"]


class GeminiError(Exception):
    """Raised when the Gemini API cannot be used or returns nothing."""


@lru_cache(maxsize=1)
def _client() -> genai.Client:
    key = get_api_key()
    if not key:
        raise GeminiError(
            "Gemini API key not found. Create a .env file in the project root with "
            "GOOGLE_API_KEY=<your key> and restart the server."
        )
    return genai.Client(api_key=key)


def _model_list(primary: str) -> list:
    raw = os.getenv("GEMINI_FALLBACK_MODELS") or os.getenv("GEMINI_FALLBACK_MODEL") or ""
    backups = [m.strip() for m in raw.split(",") if m.strip()] or DEFAULT_BACKUPS
    models = []
    for m in [primary] + backups:
        if m not in models:
            models.append(m)
    return models


def _try_model(client, model: str, prompt: str):
    """Returns (text, problem). Exactly one of them is None."""
    for attempt in range(ATTEMPTS_PER_MODEL):
        try:
            response = client.models.generate_content(model=model, contents=prompt)
        except Exception as exc:
            msg = str(exc)
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                return None, "quota used up"
            if "404" in msg or "NOT_FOUND" in msg:
                return None, "not available for your key"
            if any(b in msg for b in BUSY_ERRORS):
                if attempt < ATTEMPTS_PER_MODEL - 1:
                    time.sleep(WAIT_SECONDS * (attempt + 1))
                    continue
                return None, "busy"
            raise GeminiError(f"Gemini request failed ({model}): {exc}") from exc

        text = (getattr(response, "text", None) or "").strip()
        if text:
            return text, None
        return None, "empty response"
    return None, "busy"


def generate_text(model_name: str, prompt: str) -> str:
    """Send a prompt to Gemini, moving to backup models when needed.
    Always returns a non-empty string, or raises GeminiError."""
    client = _client()
    problems = []

    for model in _model_list(model_name):
        text, problem = _try_model(client, model, prompt)
        if text:
            return text
        problems.append(f"{model} ({problem})")

    raise GeminiError(
        "All Gemini models are busy or out of free quota right now. "
        "Please wait a few minutes and try again. Tried: " + "; ".join(problems)
    )