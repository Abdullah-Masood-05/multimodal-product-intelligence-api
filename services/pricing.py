import json
from groq import Groq
from config import settings

client = Groq(api_key=settings.groq_api_key)

async def calculate_pricing_strategy(market_data: str, twin_data: str, base_cost: str) -> dict:
    prompt = f"""You are Agent 4 — The Pricing Strategist.
Your job is to analyze market competitor data and customer psychological data to calculate the optimal pricing strategy for a product.

Base Manufacturing/Acquisition Cost: {base_cost if base_cost else "Unknown (Estimate based on market)"}

Input 1: Market Researcher Data (Competitor prices, positioning)
{market_data}

Input 2: Customer Psychologist Data (Buyer personas, purchase hesitations, objections)
{twin_data}

Instructions:
1. Analyze the competitors' pricing.
2. Evaluate the customers' willingness to pay and their biggest price-related objections.
3. Calculate the Ideal Price Point that maximizes conversion while maintaining healthy margins.
4. Assess the Margin Risk (is it a race to the bottom, or is there room for premium markup?).
5. Predict the final Conversion Probability at the ideal price point.

Return ONLY a valid JSON object exactly matching this schema:
{{
  "ideal_price_point": "string (e.g. $89.99)",
  "pricing_tier": "string (Budget, Value, Premium, Luxury)",
  "margin_risk": "string (Low, Medium, High)",
  "final_conversion_probability": "number (0-100)",
  "strategy_rationale": "string (A paragraph explaining why this price was chosen based on the market and psychological data)",
  "recommended_discount": "string (e.g. 10% off for students, or N/A)"
}}
"""

    response = client.chat.completions.create(
        model=settings.vision_model, # Using the same model for consistency, it handles text fine
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are an expert pricing strategist and econometrician AI."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=800,
        temperature=0.2 # Very low temperature for logical, calculated output
    )
    
    raw = response.choices[0].message.content
    return json.loads(raw)
