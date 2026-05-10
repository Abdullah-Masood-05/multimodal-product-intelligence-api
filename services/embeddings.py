import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from config import settings
import io

_model = None
_processor = None

def _load_model():
    global _model, _processor
    if _model is None:
        print(f"Loading CLIP model: {settings.clip_model}")
        _model = CLIPModel.from_pretrained(settings.clip_model)
        _processor = CLIPProcessor.from_pretrained(settings.clip_model)
        _model.eval()
    return _model, _processor

def _extract_tensor(output):
    """Handle both raw tensors and structured output objects from transformers v5+."""
    if hasattr(output, 'image_embeds'):
        return output.image_embeds
    if hasattr(output, 'text_embeds'):
        return output.text_embeds
    if hasattr(output, 'pooler_output'):
        return output.pooler_output
    # Already a raw tensor
    return output

def get_image_embedding(image_bytes: bytes) -> list[float]:
    model, processor = _load_model()
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    inputs = processor(images=img, return_tensors="pt")
    with torch.no_grad():
        raw = model.get_image_features(**inputs)
        features = _extract_tensor(raw)
        features = features / features.norm(dim=-1, keepdim=True)
    return features[0].tolist()

def get_text_embedding(text: str) -> list[float]:
    model, processor = _load_model()
    inputs = processor(text=[text], return_tensors="pt", padding=True)
    with torch.no_grad():
        raw = model.get_text_features(**inputs)
        features = _extract_tensor(raw)
        features = features / features.norm(dim=-1, keepdim=True)
    return features[0].tolist()
