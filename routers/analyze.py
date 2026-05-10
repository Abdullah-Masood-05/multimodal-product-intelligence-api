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
        embedding = get_image_embedding(image_bytes)
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        
        # Check for duplicates
        similar_results = vector_store.search_similar(embedding, limit=1)
        is_duplicate = False
        duplicate_score = 0.0
        if similar_results and similar_results[0].score > 0.92:
            is_duplicate = True
            duplicate_score = similar_results[0].score
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")

    try:
        listing, latency_ms = await analyze_product_image(image_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vision analysis failed: {str(e)}")

    try:
        product_id = vector_store.add_product(
            embedding=embedding,
            listing=listing.model_dump(),
            image_base64=image_b64
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Storage failed: {str(e)}")

    return {
        "id": product_id,
        "listing": listing,
        "latency_ms": latency_ms,
        "is_duplicate": is_duplicate,
        "duplicate_score": duplicate_score
    }
