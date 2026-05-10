from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.simulator import simulate_customer_twins
import time

router = APIRouter()

@router.post("/api/simulate")
async def run_simulation(
    file: UploadFile = File(...),
    price: str = Form(...),
    description: str = Form(...),
    audience: str = Form(...)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    image_bytes = await file.read()
    t0 = time.time()

    try:
        result = await simulate_customer_twins(
            image_bytes=image_bytes,
            price=price,
            description=description,
            audience=audience
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

    result["latency_ms"] = int((time.time() - t0) * 1000)
    return result
