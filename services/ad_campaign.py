import base64
import json
import asyncio
from groq import Groq
from config import settings

client = Groq(api_key=settings.groq_api_key)

AD_CHANNELS = {
    "facebook": {
        "prompt": "Facebook ad: primary text 125 chars, headline 40 chars, description 30 chars. Emotional hook. 3 variants for A/B testing.",
        "format": '{"variant_1":{"primary_text":"...","headline":"...","description":"..."},"variant_2":{...},"variant_3":{...}}'
    },
    "instagram": {
        "prompt": "Instagram caption: engaging hook first line, benefit-focused body, CTA, 15 hashtags. Max 300 chars before 'more'.",
        "format": '{"caption":"...","hashtags":["..."],"story_text":"short 5-word sticker text"}'
    },
    "google_shopping": {
        "prompt": "Google Shopping: title 150 chars keyword-rich, description 5000 chars benefit-focused, no superlatives without proof.",
        "format": '{"title":"...","description":"...","product_type":"..."}'
    },
    "whatsapp": {
        "prompt": "WhatsApp broadcast: conversational, urgent, personal. Emoji usage. Max 200 chars. Include price + CTA.",
        "format": '{"message":"..."}'
    },
    "email": {
        "prompt": "Email marketing: 5 subject line variants (curiosity/urgency/benefit/question/number-based), preview text.",
        "format": '{"subjects":["...x5"],"preview_text":"..."}'
    }
}

def _generate_channel_sync(b64_img: str, product_info: str,
                           audience: str, budget: str,
                           channel: str, spec: dict) -> dict:
    """Synchronous Groq call for a single channel."""
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
                        "text": f"""You are a world-class performance marketing copywriter.
Create {channel.replace('_', ' ').title()} ad copy for this product.

Product info: {product_info}
Target audience: {audience}
Daily budget: {budget}
Campaign goal: maximize conversions

{spec['prompt']}

Return ONLY valid JSON matching this format:
{spec['format']}"""
                    }
                ]
            }
        ],
        max_tokens=800
    )
    raw = response.choices[0].message.content
    return {channel: json.loads(raw)}


async def generate_channel(b64_img: str, product_info: str,
                           audience: str, budget: str,
                           channel: str, spec: dict) -> dict:
    """Run the sync Groq call in a thread for true async parallelism."""
    return await asyncio.to_thread(
        _generate_channel_sync,
        b64_img, product_info, audience, budget, channel, spec
    )


async def build_campaign(image_bytes: bytes, product_info: str,
                         audience: str, budget: str) -> dict:
    """Generate ad copy for all 5 channels in parallel."""
    from services.vision import preprocess_image, encode_image
    processed = preprocess_image(image_bytes)
    b64 = encode_image(processed)

    tasks = [
        generate_channel(b64, product_info, audience, budget, ch, spec)
        for ch, spec in AD_CHANNELS.items()
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    campaign = {}
    errors = []
    for r in results:
        if isinstance(r, Exception):
            errors.append(str(r))
        else:
            campaign.update(r)

    return {
        "campaign": campaign,
        "audience": audience,
        "budget": budget,
        "channels_generated": len(campaign),
        "channels_failed": len(errors),
        "errors": errors if errors else None
    }
