from fastapi import APIRouter
from services.vector_store import vector_store
import json

router = APIRouter()

@router.get("/api/catalog")
async def get_catalog(limit: int = 20):
    try:
        results, _ = vector_store.client.scroll(
            collection_name=vector_store.collection_name,
            limit=limit,
            with_payload=True,
            with_vectors=False,
        )
    except Exception:
        results = []

    items = []
    for point in results:
        payload = point.payload or {}
        listing_raw = payload.get("listing", "{}")
        listing = json.loads(listing_raw) if isinstance(listing_raw, str) else listing_raw
        items.append({
            "id": str(point.id),
            "listing": listing,
            "image_base64": payload.get("image_base64")
        })

    return {"items": items, "total": len(items)}
