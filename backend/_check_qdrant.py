from retrieval.vector_store import vector_store

async def check_qdrant():
    print(f"Store type: {vector_store.store_type}")
    try:
        if vector_store.store_type == "qdrant":
            client = vector_store._qdrant_client
            collections = client.get_collections().collections
            print(f"Collections: {[c.name for c in collections]}")
            
            for coll_name in ["reviews"]:
                print(f"\n--- Checking Collection: {coll_name} ---")
                try:
                    info = client.get_collection(coll_name)
                    print(f"Points count: {info.points_count}")
                    
                    # Test match filter
                    from qdrant_client.models import Filter, FieldCondition, MatchValue
                    sku_to_test = "VITC30"
                    q_filter = Filter(must=[FieldCondition(key="sku", match=MatchValue(value=sku_to_test))])
                    
                    print(f"Searching for sku='{sku_to_test}'...")
                    results = client.search(
                        collection_name=coll_name,
                        query_vector=[0.0] * 384,
                        query_filter=q_filter,
                        limit=5
                    )
                    print(f"Found {len(results)} matches for '{sku_to_test}'")
                except Exception as ex:
                    print(f"Error checking collection {coll_name}: {ex}")
        else:
            print("Currently using in-memory store. Check config.py if this is unexpected.")
    except Exception as e:
        print(f"Fatal error in diagnostic: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import asyncio
    asyncio.run(check_qdrant())
