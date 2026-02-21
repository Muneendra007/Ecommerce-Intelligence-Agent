"""
Configuration & Environment Settings
Loads from .env and provides typed settings for the entire application.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")


class Settings:
    """Application settings loaded from environment variables."""

    # ── Google Gemini ───────────────────────────────────────
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # ── Qdrant ──────────────────────────────────────────────
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")

    # ── Cost Control ────────────────────────────────────────
    QUICK_MODE_TOKEN_BUDGET: int = int(os.getenv("QUICK_MODE_TOKEN_BUDGET", "2000"))
    DEEP_MODE_TOKEN_BUDGET: int = int(os.getenv("DEEP_MODE_TOKEN_BUDGET", "8000"))
    MAX_COST_PER_REQUEST: float = float(os.getenv("MAX_COST_PER_REQUEST", "0.50"))

    # ── Server ──────────────────────────────────────────────
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    CORS_ORIGINS: list[str] = os.getenv(
        "CORS_ORIGINS", "http://localhost:5173,http://localhost:3000"
    ).split(",")

    # ── Feature Flags ───────────────────────────────────────
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() == "true"

    @classmethod
    def is_google_configured(cls) -> bool:
        return bool(cls.GOOGLE_API_KEY)

    @classmethod
    def is_llm_configured(cls) -> bool:
        return cls.is_google_configured()

    @classmethod
    def is_qdrant_configured(cls) -> bool:
        return bool(cls.QDRANT_URL) and cls.QDRANT_URL != "http://localhost:6333"


settings = Settings()
