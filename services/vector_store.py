from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Query
from config import settings
import uuid
import json

DUPLICATE_THRESHOLD = 0.92

class VectorStore:
    def __init__(self):
        self.client = QdrantClient(url=settings.qdrant_url)
        self.collection_name = "products"
        self._ensure_collection()

    def _ensure_collection(self):
        collections = self.client.get_collections().collections
        if not any(c.name == self.collection_name for c in collections):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE),
            )

    def add_product(self, embedding: list[float], listing: dict, image_base64: str = None) -> str:
        point_id = str(uuid.uuid4())
        payload = {"listing": json.dumps(listing)}
        if image_base64:
            payload["image_base64"] = image_base64

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=payload
                )
            ]
        )
        return point_id

    def search_similar(self, query_embedding: list[float], limit: int = 5):
        """Search for similar vectors using the new query_points API (qdrant-client v1.7+)."""
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=limit,
            with_payload=True,
        )
        return results.points

    def count(self) -> int:
        """Return total number of indexed products."""
        return self.client.count(collection_name=self.collection_name).count

vector_store = VectorStore()
