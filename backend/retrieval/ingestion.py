"""
Data Ingestion Pipeline
Ingests review embeddings and competitor features into the vector store at startup.
Uses batch upserts for fast Qdrant Cloud uploads.
"""

from __future__ import annotations
import logging
import uuid

from data.dataset import generate_reviews, get_competitor_features, ALL_PRODUCTS
from retrieval.embedding_service import embedding_service
from retrieval.vector_store import (
    vector_store, REVIEW_COLLECTION, COMPETITOR_COLLECTION,
)

logger = logging.getLogger(__name__)


async def ingest_all_data(force: bool = False):
    """
    Full ingestion pipeline. Called once at application startup.
    1. Create vector collections
    2. Embed and store all reviews (batch)
    3. Embed and store competitor features (batch)
    """
    logger.info("Starting data ingestion pipeline...")

    # Create collections
    vector_store.create_collection(REVIEW_COLLECTION, recreate=force)
    vector_store.create_collection(COMPETITOR_COLLECTION, recreate=force)

    # If collections are already populated in persistent Qdrant store, skip re-uploading
    review_count = vector_store.count(REVIEW_COLLECTION)
    competitor_count = vector_store.count(COMPETITOR_COLLECTION)
    if not force and review_count > 0 and competitor_count > 0:
        total = review_count + competitor_count
        logger.info(f"✅ Vector store already populated ({total} vectors: {review_count} reviews, {competitor_count} competitor features).")
        return total

    # Ingest reviews
    reviews = generate_reviews()
    await _ingest_reviews(reviews)

    # Ingest competitor features
    features = get_competitor_features()
    await _ingest_competitor_features(features)

    total = vector_store.count(REVIEW_COLLECTION) + vector_store.count(COMPETITOR_COLLECTION)
    logger.info(f"Ingestion complete. Total vectors: {total}")
    return total


async def _ingest_reviews(reviews: list[dict]):
    """Embed and batch store all reviews."""
    logger.info(f"Ingesting {len(reviews)} reviews...")

    # Batch embedding + batch upsert
    batch_size = 100
    for i in range(0, len(reviews), batch_size):
        batch = reviews[i:i + batch_size]
        texts = [r["review_text"] for r in batch]
        embeddings = await embedding_service.embed_batch(texts)

        items = []
        for review, embedding in zip(batch, embeddings):
            review_id = str(uuid.uuid4())[:12]
            items.append({
                "id": review_id,
                "vector": embedding,
                "payload": {
                    "brand": review["brand"],
                    "sku": review["sku"],
                    "rating": review["rating"],
                    "review_text": review["review_text"],
                    "marketplace": review["marketplace"],
                    "city": review.get("city", ""),
                    "date": review.get("date", ""),
                    "verified_purchase": review.get("verified_purchase", True),
                    "helpful_votes": review.get("helpful_votes", 0),
                },
            })

        count = vector_store.batch_upsert(REVIEW_COLLECTION, items)
        logger.info(f"  Batch {i // batch_size + 1}: {count} reviews upserted")

    total = vector_store.count(REVIEW_COLLECTION)
    logger.info(f"Ingested {total} reviews into vector store")


async def _ingest_competitor_features(features: list[dict]):
    """Embed and batch store competitor feature descriptions."""
    logger.info(f"Ingesting {len(features)} competitor feature sets...")

    texts = [f["features_text"] for f in features]
    embeddings = await embedding_service.embed_batch(texts)

    items = []
    for feature, embedding in zip(features, embeddings):
        feature_id = f"feat-{feature['sku']}"
        items.append({
            "id": feature_id,
            "vector": embedding,
            "payload": {
                "brand": feature["brand"],
                "sku": feature["sku"],
                "name": feature["name"],
                "price": feature["price"],
                "rating": feature["rating"],
                "features_text": feature["features_text"],
            },
        })

    count = vector_store.batch_upsert(COMPETITOR_COLLECTION, items)
    logger.info(f"Ingested {count} competitor feature sets")


def get_total_indexed() -> int:
    """Return total vectors in all collections."""
    return (
        vector_store.count(REVIEW_COLLECTION)
        + vector_store.count(COMPETITOR_COLLECTION)
    )


async def ingest_custom_reviews(reviews: list[dict]) -> int:
    """Embed and batch store custom user-uploaded reviews."""
    await _ingest_reviews(reviews)
    return len(reviews)

