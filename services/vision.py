import base64, json, time, io
from groq import Groq
from PIL import Image
from schemas import ProductListing
from config import settings

client = Groq(api_key=settings.groq_api_key)

SYSTEM_PROMPT = """You are an expert e-commerce merchandiser.
Analyse the product image and return a complete, accurate product listing.
Be specific about visible materials, colors, dimensions, and style.
Pricing should reflect current USD market rates on Amazon or similar platforms.
Return ONLY valid JSON — no extra text, no markdown fences."""

def preprocess_image(raw_bytes: bytes, max_size: int = 1024) -> bytes:
    img = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
    img.thumbnail((max_size, max_size), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85, optimize=True)
    return buf.getvalue()

def encode_image(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")

async def analyze_product_image(image_bytes: bytes) -> tuple[ProductListing, int]:
    t0 = time.time()
    processed = preprocess_image(image_bytes)
    b64 = encode_image(processed)

    response = client.chat.completions.create(
        model=settings.vision_model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
                    },
                    {
                        "type": "text",
                        "text": """Analyse this product image and return JSON with these exact fields:
{
  "title": "SEO product title under 80 chars",
  "description": "3-5 benefit-focused bullet points separated by newlines",
  "category": "primary category",
  "subcategory": "specific subcategory",
  "tags": ["tag1", "tag2", "...8-12 tags"],
  "attributes": {"color": "...", "material": "...", "style": "..."},
  "price_min": 0.0,
  "price_max": 0.0,
  "condition_notes": "visible quality/condition notes",
  "confidence": 0.0
}"""
                    }
                ]
            }
        ],
        max_tokens=1024
    )

    raw = response.choices[0].message.content
    data = json.loads(raw)
    listing = ProductListing(**data)
    return listing, int((time.time() - t0) * 1000)
