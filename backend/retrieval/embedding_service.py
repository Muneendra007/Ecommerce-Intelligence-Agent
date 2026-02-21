"""
Embedding Service
Converts text to vector embeddings using OpenAI or deterministic hash fallback.
Separates embedding logic from retrieval logic (dependency injection ready).
"""

from __future__ import annotations
import hashlib
import logging
from typing import Optional

from config import settings

logger = logging.getLogger(__name__)

# Embedding dimension
EMBEDDING_DIM = 1536


class EmbeddingService:
    """
    Generate embeddings for text content.
    Uses local SentenceTransformer ('all-MiniLM-L6-v2') for fast, free embeddings.
    Falls back to deterministic hash if model fails to load.
    """

    def __init__(self):
        self.model = None
        self.model_name = "all-MiniLM-L6-v2"

        try:
            from sentence_transformers import SentenceTransformer
            # Load local model (downloads on first run)
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"✅ Local embedding model loaded: {self.model_name}")
        except Exception as e:
            logger.warning(f"Failed to load sentence-transformers: {e}. Using hash fallback.")
        
        # Simple cache for query embeddings
        self._cache: dict[str, list[float]] = {}

    @property
    def is_live(self) -> bool:
        return self.model is not None

    async def embed_text(self, text: str) -> list[float]:
        """Generate embedding for a single text string."""
        if text in self._cache:
            return self._cache[text]

        if not self.is_live:
            res = self._hash_embedding(text)
            self._cache[text] = res
            return res

        try:
            # Generate embedding (synchronous, but fast on CPU for single text)
            embedding = self.model.encode(text, convert_to_numpy=True).tolist()
            self._cache[text] = embedding  # Update cache
            return embedding
        except Exception as e:
            logger.error(f"Embedding error: {e}")
            res = self._hash_embedding(text)
            self._cache[text] = res
            return res

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        if not self.is_live:
            return [self._hash_embedding(t) for t in texts]

        try:
            # Batch embedding
            embeddings = self.model.encode(texts, convert_to_numpy=True).tolist()
            return embeddings
        except Exception as e:
            logger.error(f"Batch embedding error: {e}")
            return [self._hash_embedding(t) for t in texts]

    @staticmethod
    def _hash_embedding(text: str) -> list[float]:
        """
        Deterministic hash-based embedding for fallback.
        Produces consistent vectors for meaningful demo search.
        """
        # Use multiple hash rounds to simulate dimensions
        vectors = []
        # Target dimension for MiniLM is 384, but if we need 1536 (OpenAI compat) we can pad/repeat.
        # For now, let's keep it compatible with whatever vector store expects.
        # Note: If we switch model, we MUST recreate collection or it will fail dimension check.
        # MiniLM is 384 dim. OpenAI is 1536. 
        # We should update vector_store to use 384 dim for new collections.
        
        target_dim = 384 
        
        for salt in range(target_dim // 32 + 1):
            h = hashlib.sha256(f"{salt}:{text}".encode()).digest()
            vectors.extend(b / 255.0 - 0.5 for b in h)
        embedding = vectors[:target_dim]

        # Normalize
        magnitude = sum(v * v for v in embedding) ** 0.5
        if magnitude > 0:
            embedding = [v / magnitude for v in embedding]

        return embedding


# Singleton
embedding_service = EmbeddingService()
