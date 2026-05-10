import json
import base64
from groq import Groq
from config import settings

client = Groq(api_key=settings.groq_api_key)

async def simulate_customer_twins(image_bytes: bytes, price: str, description: str, audience: str) -> dict:
    from services.vision import preprocess_image, encode_image
    
    # Process and encode the image
    processed = preprocess_image(image_bytes)
    b64_img = encode_image(processed)

    prompt = f"""You are an advanced AI Customer Twin Simulator. Your job is to simulate the buying behavior and reactions of synthetic shoppers based on the product provided.

Product Details:
- Price: {price}
- Description: {description}
- Target Audience: {audience}

Instructions:
1. Analyze the product image and details.
2. Generate 3 distinct synthetic shopper personas (twins) that fit the target audience.
3. Simulate their reaction to the product (quote).
4. Assign a purchase probability (0 to 100).
5. Extract overall marketing insights.

Return ONLY a valid JSON object exactly matching this schema:
{{
  "twins": [
    {{
      "name": "string (e.g. Ali)",
      "age": "number",
      "occupation": "string",
      "profile": "string (short description of their preferences)",
      "reaction": "string (a direct quote reacting to the product)",
      "purchase_probability": "number (0-100)"
    }}
  ],
  "insights": {{
    "biggest_objection": "string",
    "strongest_selling_point": "string",
    "best_audience": "string",
    "predicted_conversion_score": "number (0.0 to 10.0)"
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
        temperature=0.7
    )
    
    raw = response.choices[0].message.content
    return json.loads(raw)
