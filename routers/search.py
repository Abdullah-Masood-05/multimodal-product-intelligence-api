from fastapi import APIRouter, HTTPException
from schemas import SearchQuery
from services.embeddings import get_text_embedding
from services.vector_store import vector_store
import json

router = APIRouter()

@router.post("/api/search")
async def search(query: SearchQuery):
    try:
        embedding = get_text_embedding(query.query)
        results = vector_store.search_similar(embedding, limit=query.limit or 5)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    items = []
    for hit in results:
        payload = hit.payload or {}
        listing_raw = payload.get("listing", "{}")
        listing = json.loads(listing_raw) if isinstance(listing_raw, str) else listing_raw
        items.append({
            "id": hit.id,
            "score": hit.score,
            "listing": listing,
            "image_base64": payload.get("image_base64")
        })

    return {"results": items}
