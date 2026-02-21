"""
User Preference Memory Store
Persists user preferences in the vector store for automatic reuse.

Stored preferences:
  - preferred_kpi: margin, growth, revenue
  - preferred_marketplace: Amazon
  - focus: negative_reviews, all_reviews
  - last_sku: most recently queried SKU
"""

from __future__ import annotations
import logging
from typing import Optional

from retrieval.embedding_service import embedding_service
from retrieval.vector_store import vector_store, MEMORY_COLLECTION

logger = logging.getLogger(__name__)

# Default user preferences
DEFAULT_PREFERENCES = {
    "preferred_kpi": "growth",
    "preferred_marketplace": "Amazon",
    "focus": "all_reviews",
    "last_sku": None,
    "business_goal": "growth",
}


class PreferenceStore:
    """
    Manages persistent user preferences.
    Stores in vector DB for semantic retrieval and exact key lookup.
    Auto-applies stored preferences in future queries.
    """

    def __init__(self):
        self._cache: dict[str, str] = dict(DEFAULT_PREFERENCES)
        self._initialized = False

    async def initialize(self):
        """Create memory collection and load cached preferences."""
        vector_store.create_collection(MEMORY_COLLECTION)
        self._initialized = True
        logger.info("Preference store initialized")

    async def set_preference(self, key: str, value: str):
        """Store a user preference."""
        self._cache[key] = value

        # Also persist to vector store for semantic retrieval
        text = f"User preference: {key} = {value}"
        embedding = await embedding_service.embed_text(text)
        vector_store.upsert(
            collection=MEMORY_COLLECTION,
            id=f"pref-{key}",
            vector=embedding,
            payload={"key": key, "value": value, "type": "preference"},
        )
        logger.info(f"Stored preference: {key} = {value}")

    async def get_preference(self, key: str) -> Optional[str]:
        """Retrieve a preference by key."""
        return self._cache.get(key)

    async def get_all_preferences(self) -> dict[str, str]:
        """Return all current preferences."""
        return dict(self._cache)

    async def get_context_for_query(self, query: str) -> dict:
        """
        Auto-apply stored preferences to enrich a query context.
        Returns a dict of preferences relevant to the current query.
        """
        context = dict(self._cache)

        # Semantic search for any relevant stored memories
        try:
            query_embedding = await embedding_service.embed_text(query)
            results = vector_store.search(
                collection=MEMORY_COLLECTION,
                query_vector=query_embedding,
                limit=3,
            )
            for r in results:
                if r["payload"].get("type") == "preference":
                    context[r["payload"]["key"]] = r["payload"]["value"]
        except Exception as e:
            logger.warning(f"Memory search failed: {e}")

        return context

    async def update_from_query(self, sku: Optional[str] = None,
                                 goal: Optional[str] = None):
        """Update preferences based on the latest query."""
        if sku:
            await self.set_preference("last_sku", sku)
        if goal:
            await self.set_preference("business_goal", goal)


# Singleton
preference_store = PreferenceStore()
