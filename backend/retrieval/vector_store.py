"""
Vector Store — Qdrant integration with in-memory fallback.

Collections:
  - reviews: Review embeddings with metadata (brand, SKU, rating, marketplace)
  - competitor_features: Competitor product feature embeddings
  - user_memory: User preference memory

Supports cosine similarity search with metadata filtering.
"""

from __future__ import annotations
import logging
import uuid
from typing import Optional

from config import settings

logger = logging.getLogger(__name__)

REVIEW_COLLECTION = "reviews"
COMPETITOR_COLLECTION = "competitor_features"
MEMORY_COLLECTION = "user_memory"


class InMemoryVectorStore:
    """
    In-memory vector store fallback when Qdrant is unavailable.
    Implements cosine similarity search with metadata filtering.
    """

    def __init__(self):
        self._collections: dict[str, list[dict]] = {}
        logger.info("Using in-memory vector store (Qdrant fallback)")

    def create_collection(self, name: str, vector_size: int = 1536):
        """Create a new collection."""
        if name not in self._collections:
            self._collections[name] = []
            logger.info(f"Created collection: {name}")

    def upsert(self, collection: str, point_id: str, vector: list[float],
               payload: dict) -> str:
        """Insert or update a vector with metadata."""
        logger.info(f"Upserting to InMemoryStore ({hex(id(self))}) - Collection: {collection}")
        self.create_collection(collection)
        # Remove existing if same id
        self._collections[collection] = [
            v for v in self._collections[collection] if v["id"] != point_id
        ]
        self._collections[collection].append({
            "id": point_id,
            "vector": vector,
            "payload": payload,
        })
        return point_id

    def search(self, collection: str, query_vector: list[float],
               limit: int = 10, filters: Optional[dict] = None) -> list[dict]:
        """
        Cosine similarity search with optional metadata filtering.
        Filters: {"brand": "GlowSkin", "rating": {"gte": 4}}
        """
        logger.info(f"Searching InMemoryStore ({hex(id(self))}) - Collection: {collection}")
        if collection not in self._collections:
            logger.warning(f"Collection '{collection}' not found in {list(self._collections.keys())}")
            return []

        candidates = self._collections[collection]
        # Applied filters
        if filters:
            candidates = self._apply_filters(candidates, filters)

        # Cosine similarity
        results = []
        for item in candidates:
            score = self._cosine_sim(query_vector, item["vector"])
            results.append({
                "id": item["id"],
                "score": score,
                "payload": item["payload"],
            })

        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

    def get_all(self, collection: str, filters: Optional[dict] = None) -> list[dict]:
        """Get all entries from a collection with optional filtering."""
        if collection not in self._collections:
            return []

        candidates = self._collections[collection]
        if filters:
            candidates = self._apply_filters(candidates, filters)

        return [{"id": c["id"], "payload": c["payload"]} for c in candidates]

    def count(self, collection: str) -> int:
        """Count entries in a collection."""
        return len(self._collections.get(collection, []))

    def delete(self, collection: str, point_id: str):
        """Delete by id."""
        if collection in self._collections:
            self._collections[collection] = [
                v for v in self._collections[collection] if v["id"] != point_id
            ]

    @staticmethod
    def _apply_filters(candidates: list[dict], filters: dict) -> list[dict]:
        """Apply metadata filters to candidates."""
        filtered = candidates
        for key, value in filters.items():
            if isinstance(value, dict):
                # Range filter: {"rating": {"gte": 4}}
                if "gte" in value:
                    filtered = [c for c in filtered
                                if c["payload"].get(key, 0) >= value["gte"]]
                if "lte" in value:
                    filtered = [c for c in filtered
                                if c["payload"].get(key, 0) <= value["lte"]]
            else:
                # Exact match
                filtered = [c for c in filtered
                            if c["payload"].get(key) == value]
        return filtered

    @staticmethod
    def _cosine_sim(a: list[float], b: list[float]) -> float:
        """Compute cosine similarity between two vectors."""
        dot = sum(x * y for x, y in zip(a, b))
        mag_a = sum(x * x for x in a) ** 0.5
        mag_b = sum(x * x for x in b) ** 0.5
        if mag_a == 0 or mag_b == 0:
            return 0.0
        return dot / (mag_a * mag_b)


class QdrantVectorStore:
    """
    Qdrant-backed vector store.
    Falls back to InMemoryVectorStore if Qdrant is unavailable.
    """

    # Namespace UUID for deterministic ID generation
    _NS = uuid.UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567890")

    def __init__(self):
        self._qdrant_client = None
        self._fallback = InMemoryVectorStore()
        self._use_fallback = True

        if settings.is_qdrant_configured():
            try:
                from qdrant_client import QdrantClient
                self._qdrant_client = QdrantClient(
                    url=settings.QDRANT_URL,
                    api_key=settings.QDRANT_API_KEY or None,
                    timeout=30,
                )
                self._qdrant_client.get_collections()
                self._use_fallback = False
                logger.info(f"✅ Connected to Qdrant Cloud: {settings.QDRANT_URL}")
            except Exception as e:
                logger.warning(f"Qdrant unavailable: {e}. Using in-memory fallback.")
        else:
            logger.info("Qdrant not configured. Using in-memory vector store.")

    @property
    def store_type(self) -> str:
        return "qdrant" if not self._use_fallback else "in-memory"

    def _to_uuid(self, id_str: str) -> str:
        """Convert any string ID to a deterministic UUID string for Qdrant."""
        return str(uuid.uuid5(self._NS, id_str))

    def create_collection(self, name: str, vector_size: int = 384, recreate: bool = False):
        """Create collection in active store."""
        if self._use_fallback:
            self._fallback.create_collection(name, vector_size)
        else:
            from qdrant_client.models import Distance, VectorParams, PayloadSchemaType
            try:
                # Check if collection exists first
                collections = self._qdrant_client.get_collections().collections
                existing = [c.name for c in collections]
                if name in existing and not recreate:
                    logger.info(f"Qdrant collection '{name}' already exists. Skipping recreation.")
                    return
                if name in existing and recreate:
                    # Delete and recreate for clean state
                    self._qdrant_client.delete_collection(name)
                self._qdrant_client.create_collection(
                    collection_name=name,
                    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
                )
                logger.info(f"Created Qdrant collection: {name}")

                # Create payload indexes for fast and reliable filtering
                indexed_fields = {
                    "sku": PayloadSchemaType.KEYWORD,
                    "brand": PayloadSchemaType.KEYWORD,
                    "rating": PayloadSchemaType.INTEGER,
                    "marketplace": PayloadSchemaType.KEYWORD,
                }
                for field, schema in indexed_fields.items():
                    try:
                        self._qdrant_client.create_payload_index(
                            collection_name=name,
                            field_name=field,
                            field_schema=schema,
                        )
                    except Exception:
                        pass
            except Exception as e:
                logger.error(f"Failed to create Qdrant collection: {e}")

    def upsert(self, collection: str, id: str, vector: list[float],
               payload: dict) -> str:
        """Upsert vector with metadata."""
        if self._use_fallback:
            return self._fallback.upsert(collection, id, vector, payload)

        from qdrant_client.models import PointStruct
        try:
            point_id = self._to_uuid(id)
            self._qdrant_client.upsert(
                collection_name=collection,
                points=[PointStruct(id=point_id, vector=vector, payload=payload)],
            )
            # MIRROR: Always also upsert to local in-memory store
            self._fallback.upsert(collection, id, vector, payload)
            return id
        except Exception as e:
            logger.error(f"Qdrant upsert failed: {e}")
            return self._fallback.upsert(collection, id, vector, payload)

    def batch_upsert(self, collection: str, items: list[dict]) -> int:
        """
        Batch upsert multiple vectors at once.
        Each item: {"id": str, "vector": list[float], "payload": dict}
        Returns the number of successfully upserted items.
        """
        if not items:
            return 0

        if self._use_fallback:
            for item in items:
                self._fallback.upsert(collection, item["id"], item["vector"], item["payload"])
            return len(items)

        from qdrant_client.models import PointStruct
        try:
            points = [
                PointStruct(
                    id=self._to_uuid(item["id"]),
                    vector=item["vector"],
                    payload=item["payload"],
                )
                for item in items
            ]
            self._qdrant_client.upsert(
                collection_name=collection,
                points=points,
            )
            # MIRROR: Always also upsert all to local in-memory store
            for item in items:
                self._fallback.upsert(collection, item["id"], item["vector"], item["payload"])
            return len(items)
        except Exception as e:
            logger.error(f"Qdrant batch upsert failed: {e}")
            # Fallback: store in memory (already handled by mirror)
            for item in items:
                self._fallback.upsert(collection, item["id"], item["vector"], item["payload"])
            return len(items)


    def search(self, collection: str, query_vector: list[float],
               limit: int = 10, filters: Optional[dict] = None) -> list[dict]:
        """Search with optional filters."""
        if self._use_fallback:
            return self._fallback.search(collection, query_vector, limit, filters)

        from qdrant_client.models import Filter, FieldCondition, MatchValue, Range
        try:
            qdrant_filter = None
            if filters:
                conditions = []
                for key, value in filters.items():
                    if isinstance(value, dict):
                        conditions.append(FieldCondition(
                            key=key, range=Range(**value)
                        ))
                    else:
                        conditions.append(FieldCondition(
                            key=key, match=MatchValue(value=value)
                        ))
                qdrant_filter = Filter(must=conditions)

            results = self._qdrant_client.search(
                collection_name=collection,
                query_vector=query_vector,
                limit=limit,
                query_filter=qdrant_filter,
            )
            return [
                {"id": str(r.id), "score": r.score, "payload": r.payload}
                for r in results
            ]
        except Exception as e:
            logger.error(f"Qdrant search failed: {e}")
            return self._fallback.search(collection, query_vector, limit, filters)

    def get_all(self, collection: str, filters: Optional[dict] = None) -> list[dict]:
        """Get all from collection."""
        if self._use_fallback:
            return self._fallback.get_all(collection, filters)
        try:
            results, _ = self._qdrant_client.scroll(
                collection_name=collection, limit=1000,
            )
            entries = [{"id": str(r.id), "payload": r.payload} for r in results]
            if filters:
                entries = [
                    e for e in entries
                    if all(e["payload"].get(k) == v for k, v in filters.items()
                           if not isinstance(v, dict))
                ]
            return entries
        except Exception:
            return self._fallback.get_all(collection, filters)

    def count(self, collection: str) -> int:
        """Count collection entries."""
        if self._use_fallback:
            return self._fallback.count(collection)
        try:
            info = self._qdrant_client.get_collection(collection)
            return info.points_count or 0
        except Exception:
            return 0

    def delete(self, collection: str, id: str):
        """Delete entry."""
        if self._use_fallback:
            self._fallback.delete(collection, id)
        else:
            from qdrant_client.models import PointIdsList
            point_id = self._to_uuid(id)
            self._qdrant_client.delete(
                collection_name=collection,
                points_selector=PointIdsList(points=[point_id]),
            )


# Singleton
vector_store = QdrantVectorStore()
