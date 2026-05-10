from fastapi import APIRouter, UploadFile, File, HTTPException
from services.vision import analyze_product_image
from services.embeddings import get_image_embedding
from services.vector_store import vector_store
import base64

router = APIRouter()

@router.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    image_bytes = await file.read()

    try:
        listing, latency_ms = await analyze_product_image(image_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vision analysis failed: {str(e)}")

    try:
        embedding = get_image_embedding(image_bytes)
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        product_id = vector_store.add_product(
            embedding=embedding,
            listing=listing.model_dump(),
            image_base64=image_b64
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding/storage failed: {str(e)}")

    return {
        "id": product_id,
        "listing": listing,
        "latency_ms": latency_ms
    }
