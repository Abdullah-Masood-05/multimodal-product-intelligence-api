from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.market_researcher import run_market_research
import time

router = APIRouter()

@router.post("/api/market")
async def market_research_endpoint(
    file: UploadFile = File(...),
    price: str = Form(...),
    description: str = Form(...)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    image_bytes = await file.read()
    t0 = time.time()

    try:
        result = await run_market_research(
            image_bytes=image_bytes,
            price=price,
            description=description
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market research failed: {str(e)}")

    result["latency_ms"] = int((time.time() - t0) * 1000)
    return result
