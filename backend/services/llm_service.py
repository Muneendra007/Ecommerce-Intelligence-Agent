"""
LLM Service
Wraps Groq API (primary) with Google Gemini fallback for text generation.
Uses Groq's ultra-fast inference with Llama 3.3 70B for structured JSON output.
"""

from __future__ import annotations
import os
import logging

from config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """
    Service for interacting with LLM providers.
    Priority: Groq (free, fast) → Google Gemini (fallback) → disabled.
    """

    def __init__(self):
        self.provider = None
        self.groq_client = None
        self.gemini_model = None
        self.model_name = None

        # Try Groq first (primary)
        groq_key = os.getenv("GROQ_API_KEY", "")
        if groq_key:
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=groq_key)
                self.model_name = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")
                self.provider = "groq"
                logger.info(f"✅ Groq LLM service initialized with {self.model_name}")
            except Exception as e:
                logger.error(f"Failed to initialize Groq: {e}")

        # Fallback to Google Gemini
        if not self.provider:
            google_key = os.getenv("GOOGLE_API_KEY", "")
            if google_key:
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=google_key)
                    self.model_name = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
                    self.gemini_model = genai.GenerativeModel(self.model_name)
                    self.provider = "gemini"
                    logger.info(f"✅ Gemini LLM service initialized with {self.model_name}")
                except Exception as e:
                    logger.error(f"Failed to initialize Gemini: {e}")

        if not self.provider:
            logger.warning("⚠️ No LLM API key found. LLM features disabled.")

        self.last_usage: dict[str, int] = {"input_tokens": 0, "output_tokens": 0}

    @property
    def is_live(self) -> bool:
        return self.provider is not None

    async def generate(self, prompt: str, max_tokens: int = 2500, json_mode: bool = False) -> str:
        """Generate text from prompt using the configured LLM provider."""
        if not self.is_live:
            return "LLM not configured. Please add GROQ_API_KEY or GOOGLE_API_KEY to .env."

        if self.provider == "groq":
            return await self._generate_groq(prompt, max_tokens=max_tokens, json_mode=json_mode)
        elif self.provider == "gemini":
            return await self._generate_gemini(prompt)

        return "No LLM provider available."

    async def _generate_groq(self, prompt: str, max_tokens: int = 2500, json_mode: bool = False) -> str:
        """Generate using Groq API (async via thread pool)."""
        import asyncio
        import re

        def _call():
            extra_kwargs = {}
            if json_mode:
                extra_kwargs["response_format"] = {"type": "json_object"}
            try:
                response = self.groq_client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "user", "content": prompt + ("" if "/no_think" in prompt else "\n/no_think")}
                    ],
                    temperature=0.3,
                    max_tokens=max_tokens,
                    **extra_kwargs,
                )
            except Exception as e:
                if json_mode:
                    response = self.groq_client.chat.completions.create(
                        model=self.model_name,
                        messages=[
                            {"role": "user", "content": prompt + ("" if "/no_think" in prompt else "\n/no_think")}
                        ],
                        temperature=0.3,
                        max_tokens=max_tokens,
                    )
                else:
                    raise e

            if hasattr(response, "usage") and response.usage:
                self.last_usage = {
                    "input_tokens": getattr(response.usage, "prompt_tokens", 0),
                    "output_tokens": getattr(response.usage, "completion_tokens", 0),
                }

            text = response.choices[0].message.content or ""
            text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
            return text

        try:
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, _call)
            return result
        except Exception as e:
            logger.error(f"Groq generation error: {e}")
            return f"Error generating response: {e}"

    async def _generate_gemini(self, prompt: str) -> str:
        """Generate using Google Gemini API (async via thread pool)."""
        import asyncio
        from functools import partial

        try:
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None,
                partial(self.gemini_model.generate_content, prompt)
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            return f"Error generating response: {e}"


# Singleton
llm_service = LLMService()
