"""
LLM Service
Wraps Google Gemini API for text generation.
Replaces OpenAI integration.
"""

from __future__ import annotations
import os
import logging
import google.generativeai as genai
from config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """
    Service for interacting with Google Gemini models.
    """

    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self.model = None

        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
                logger.info(f"✅ Gemini LLM service initialized with {self.model_name}")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
        else:
            logger.warning("GOOGLE_API_KEY not found. LLM features disabled.")

    @property
    def is_live(self) -> bool:
        return self.model is not None

    async def generate(self, prompt: str) -> str:
        """Generate text from prompt using Gemini."""
        if not self.is_live:
            return "LLM not configured. Please add GOOGLE_API_KEY to .env."

        try:
            # Run in executor to avoid blocking event loop
            response = await self._run_sync(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            return f"Error generating response: {e}"

    async def _run_sync(self, prompt: str):
        """Run blocking API call in thread pool."""
        import asyncio
        from functools import partial
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, 
            partial(self.model.generate_content, prompt)
        )


# Singleton
llm_service = LLMService()
