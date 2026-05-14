"""Quick test to verify all services work before starting the server."""
import sys
import PIL.Image
import io

print("Testing CLIP embeddings...")
from services.embeddings import get_image_embedding, get_text_embedding

img = PIL.Image.new('RGB', (100, 100))
buf = io.BytesIO()
img.save(buf, format='JPEG')
vec = get_image_embedding(buf.getvalue())
print(f"  ✓ Image embedding: {len(vec)}-dim vector")

tvec = get_text_embedding("blue leather bag")
print(f"  ✓ Text embedding: {len(tvec)}-dim vector")

print("\nTesting Qdrant vector store...")
from services.vector_store import vector_store

count = vector_store.count()
print(f"  ✓ Connected! {count} products indexed")

results = vector_store.search_similar(vec, limit=3)
print(f"  ✓ search_similar works. Returned {len(results)} results")

print("\nAll services OK! Safe to start uvicorn.")
