from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class ProductListing(BaseModel):
    title: str = Field(..., description="SEO product title under 80 chars")
    description: str = Field(..., description="3-5 benefit-focused bullet points separated by newlines")
    category: str = Field(..., description="primary category")
    subcategory: str = Field(..., description="specific subcategory")
    tags: List[str] = Field(..., description="8-12 tags")
    attributes: Dict[str, Any] = Field(..., description="attributes like color, material, style")
    price_min: float = Field(..., description="minimum price estimation")
    price_max: float = Field(..., description="maximum price estimation")
    condition_notes: str = Field(..., description="visible quality/condition notes")
    confidence: float = Field(..., description="confidence score between 0.0 and 1.0")

class SearchQuery(BaseModel):
    query: str
    limit: Optional[int] = 5

class CatalogItem(BaseModel):
    id: str
    listing: ProductListing
    image_base64: Optional[str] = None
