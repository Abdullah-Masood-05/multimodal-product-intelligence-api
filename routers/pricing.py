from fastapi import APIRouter, Form, HTTPException
from services.pricing import calculate_pricing_strategy
import time

router = APIRouter()

@router.post("/api/pricing")
async def pricing_endpoint(
    market_data: str = Form(...),
    twin_data: str = Form(...),
    base_cost: str = Form(default="")
):
    t0 = time.time()

    try:
        result = await calculate_pricing_strategy(
            market_data=market_data,
            twin_data=twin_data,
            base_cost=base_cost
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pricing strategy failed: {str(e)}")

    result["latency_ms"] = int((time.time() - t0) * 1000)
    return result
