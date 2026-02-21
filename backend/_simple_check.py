import logging
import sys

# Configure logging to see the internal vector store logs
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:%(name)s:%(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

from retrieval.vector_store import vector_store

def simple_check():
    print(f"Store type: {vector_store.store_type}")
    print(f"Initial collections: {list(vector_store._fallback._collections.keys())}")
    
    vector_store.upsert("test", "1", [0.1]*384, {"name": "test point"})
    
    print(f"After upsert collections: {list(vector_store._fallback._collections.keys())}")
    print(f"Count for 'test': {vector_store.count('test')}")
    
    res = vector_store.search("test", [0.1]*384)
    print(f"Search result length: {len(res)}")

if __name__ == "__main__":
    simple_check()
