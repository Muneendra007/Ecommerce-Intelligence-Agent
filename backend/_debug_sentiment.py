"""Diagnostic script for review retrieval."""
import asyncio
import logging
import sys
import os

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add current directory to path so we can import modules
sys.path.append(os.getcwd())

from services.reasoning import reasoning_engine
from retrieval.vector_store import vector_store
from retrieval.embedding_service import embedding_service
from retrieval.ingestion import ingest_all_data

async def run_diagnostic():
    # Ensure data is present if in-memory
    if vector_store.store_type == "in-memory":
        print("Initializing in-memory store...")
        await ingest_all_data()

    # 0. Inspect First Entry
    print("\n0. Inspecting first entry in REVIEW_COLLECTION...")
    all_entries = vector_store.get_all("reviews")
    if all_entries:
        first = all_entries[0]
        print(f"   Total entries: {len(all_entries)}")
        print(f"   First Payload Keys: {list(first['payload'].keys())}")
        print(f"   First SKU: '{first['payload'].get('sku')}'")
        print(f"   First Brand: '{first['payload'].get('brand')}'")
    else:
        print("   NO ENTRIES FOUND IN COLLECTION 'reviews'")

    query = "Why are returns high for the serum?"
    sku = "VITC30"
    
    print(f"\n--- Diagnostic for Query: '{query}' ---")
    
    # 1. Check Embedding
    embedding = await embedding_service.embed_text(query)
    print(f"1. Embedding generated: {len(embedding)} dimensions")
    
    # 2. Check Raw Vector Search (WITH FILTER)
    print("\n2. Performing raw vector search in REVIEW_COLLECTION WITH FILTER...")
    results = vector_store.search(
        collection="reviews", 
        query_vector=embedding, 
        limit=5,
        filters={"sku": sku}
    )
    print(f"   Found {len(results)} results with filter sku={sku}")
    
    # 2b. Check Raw Vector Search (WITHOUT FILTER)
    print("\n2b. Performing raw vector search in REVIEW_COLLECTION WITHOUT FILTER...")
    results_no_filter = vector_store.search(
        collection="reviews", 
        query_vector=embedding, 
        limit=5
    )
    print(f"   Found {len(results_no_filter)} results without filter")
    for i, res in enumerate(results_no_filter):
        payload = res.get("payload", {})
        print(f"   [{i}] Score: {res.get('score'):.4f}, SKU: {payload.get('sku')}, Text: {payload.get('review_text')[:40]}...")

    # 3. Check ReasoningEngine's internal retrieval
    print("\n3. Testing ReasoningEngine._retrieve_reviews_with_embedding...")
    reviews = await reasoning_engine._retrieve_reviews_with_embedding(query, sku, embedding)
    print(f"   ReasoningEngine retrieved {len(reviews)} reviews")
    
    # 4. Check Sentiment Computation
    print("\n4. Testing ReasoningEngine._compute_sentiment...")
    sentiment = reasoning_engine._compute_sentiment(reviews)
    print(f"   Sentiment Breakdown:")
    for cluster in sentiment:
        print(f"   - {cluster.label}: {cluster.percentage}% ({cluster.review_count} reviews)")
        if cluster.sample_reviews:
            print(f"     Sample: {cluster.sample_reviews[0][:60]}...")

if __name__ == "__main__":
    asyncio.run(run_diagnostic())
