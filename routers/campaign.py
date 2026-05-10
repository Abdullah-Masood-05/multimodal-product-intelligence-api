from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.ad_campaign import build_campaign
import time

router = APIRouter()

@router.post("/api/campaign")
async def generate_campaign(
    file: UploadFile = File(...),
    audience: str = Form(...),
    budget: str = Form(...),
    product_info: str = Form(default="")
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    image_bytes = await file.read()
    t0 = time.time()

    # If no product info provided, auto-analyze with vision
    if not product_info.strip():
        try:
            from services.vision import analyze_product_image
            listing, _ = await analyze_product_image(image_bytes)
            product_info = f"{listing.title}. {listing.description}. Price range: ${listing.price_min}-${listing.price_max}"
        except Exception:
            product_info = "Product visible in the image"

    try:
        result = await build_campaign(image_bytes, product_info, audience, budget)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Campaign generation failed: {str(e)}")

    result["latency_ms"] = int((time.time() - t0) * 1000)
    return result
