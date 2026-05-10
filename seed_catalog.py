import os
import asyncio
import base64
from pathlib import Path
from services.embeddings import get_image_embedding
from services.vector_store import vector_store

# Mock a basic listing since we only have images, no AI analysis
def create_mock_listing(filename: str):
    return {
        "title": filename,
        "description": f"Seeded product from {filename}",
        "category": "Unknown",
        "subcategory": "Unknown",
        "tags": ["seeded", "demo"],
        "attributes": {},
        "price_min": 0.0,
        "price_max": 0.0,
        "condition_notes": "",
        "confidence": 1.0
    }

def seed_from_folder(folder_path: str):
    path = Path(folder_path)
    if not path.exists() or not path.is_dir():
        print(f"Error: Directory {folder_path} does not exist.")
        return

    valid_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    
    count = 0
    for file_path in path.iterdir():
        if count >= 500:  # Limit to 500 to keep it manageable
            break
            
        if file_path.suffix.lower() in valid_extensions:
            try:
                with open(file_path, "rb") as f:
                    image_bytes = f.read()
                
                # Get CLIP embedding
                vector = get_image_embedding(image_bytes)
                
                # Base64 encode for display in frontend
                image_b64 = base64.b64encode(image_bytes).decode("utf-8")
                
                # Upsert to Qdrant
                listing = create_mock_listing(file_path.name)
                product_id = vector_store.add_product(
                    embedding=vector,
                    listing=listing,
                    image_base64=image_b64
                )
                print(f"Seeded: {file_path.name} -> {product_id}")
                count += 1
            except Exception as e:
                print(f"Failed to process {file_path.name}: {e}")

    print(f"\nSuccessfully seeded {count} products to the catalog.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Seed the Qdrant database with product images.")
    parser.add_argument("folder", type=str, help="Path to the folder containing product images.")
    args = parser.parse_args()
    
    print(f"Seeding catalog from {args.folder}...")
    seed_from_folder(args.folder)
