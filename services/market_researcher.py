import json
from groq import Groq
from config import settings
from services.embeddings import get_image_embedding
from services.vector_store import vector_store

client = Groq(api_key=settings.groq_api_key)

async def run_market_research(image_bytes: bytes, price: str, description: str) -> dict:
    from services.vision import preprocess_image, encode_image
    
    # Get image embedding for similar product search
    embedding = get_image_embedding(image_bytes)
    similar_points = vector_store.search_similar(embedding, limit=5)
    
    competitors = []
    for p in similar_points:
        if p.payload and "listing" in p.payload:
            try:
                listing = json.loads(p.payload["listing"])
                # Omit the image base64 to save tokens
                competitors.append({
                    "title": listing.get("title"),
                    "price_min": listing.get("price_min"),
                    "price_max": listing.get("price_max"),
                    "category": listing.get("category"),
                    "description": listing.get("description", "")[:100] # truncate
                })
            except Exception:
                pass

    # Encode target image for vision model
    processed = preprocess_image(image_bytes)
    b64_img = encode_image(processed)

    prompt = f"""You are Agent 2 — The Market Researcher.
Your job is to analyze the target product against visually similar competitors found in our database to generate structured market insights.

Target Product:
- Price: {price}
- Description: {description}

Competitor Products Found in Database:
{json.dumps(competitors, indent=2)}

Instructions:
1. Analyze the target product against the competitors.
2. Identify competitor pricing trends.
3. Determine demand positioning (e.g., Budget, Mid-range, Premium).
4. Identify missing features or competitive advantages.

Return ONLY a valid JSON object exactly matching this schema:
{{
  "market_positioning": "string (Budget, Mid-range, Premium, Luxury)",
  "competitor_analysis": [
    {{
      "competitor_name": "string",
      "price_estimate": "string",
      "threat_level": "string (Low, Medium, High)"
    }}
  ],
  "insights": {{
    "average_market_price": "string",
    "price_competitiveness": "string (Too high, Competitive, Too low)",
    "market_demand_summary": "string (A paragraph summarizing the market landscape)"
  }}
}}
"""

    response = client.chat.completions.create(
        model=settings.vision_model,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        max_tokens=1000,
        temperature=0.3 # Lower temperature for analytical data
    )
    
    raw = response.choices[0].message.content
    
    result = json.loads(raw)
    result["competitors_found"] = len(competitors)
    return result
