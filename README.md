# Multimodal Product Intelligence API

AI-powered product analysis backend using **Groq Vision (Llama 4 Scout)**, **CLIP embeddings**, and **Qdrant vector search**.

Upload any product image → get instant AI-generated listings with titles, descriptions, tags, pricing, and visual similarity search.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **API Framework** | FastAPI |
| **Vision AI** | Groq LPU — Llama 4 Scout 17B (free tier, ~800 tok/s) |
| **Embeddings** | OpenAI CLIP ViT-L/14 (local, zero cost) |
| **Vector DB** | Qdrant (self-hosted via Docker) |
| **Language** | Python 3.11+ |

## Architecture

```
POST /api/analyze (image upload)
    ├── Groq Vision → structured product listing (JSON)
    ├── CLIP → 768-dim image embedding
    └── Qdrant → store embedding + metadata

POST /api/search (text query)
    ├── CLIP → text embedding
    └── Qdrant → cosine similarity search

GET /api/catalog
    └── Qdrant → paginated product listing
```

## Project Structure

```
├── main.py              ← FastAPI entry point
├── config.py            ← Environment & model configuration
├── schemas.py           ← Pydantic request/response models
├── routers/
│   ├── analyze.py       ← /api/analyze — image analysis endpoint
│   ├── search.py        ← /api/search — semantic search endpoint
│   └── catalog.py       ← /api/catalog — browse all products
├── services/
│   ├── vision.py        ← Groq Vision API integration
│   ├── embeddings.py    ← CLIP embedding generation
│   └── vector_store.py  ← Qdrant vector operations
├── requirements.txt
└── .env.example
```

## Quick Start

### Prerequisites
- Python 3.11+
- Docker (for Qdrant)
- Free Groq API key from [console.groq.com](https://console.groq.com)

### 1. Start Qdrant
```bash
docker run -d -p 6333:6333 qdrant/qdrant:latest
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 4. Run the Server
```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. Interactive docs at `/docs`.

## API Endpoints

### `POST /api/analyze`
Upload a product image for AI analysis.
- **Input**: Multipart form data with image file
- **Output**: Product listing (title, description, tags, price range, confidence score) + vector stored in Qdrant

### `POST /api/search`
Semantic text search across all indexed products.
- **Input**: `{ "query": "red leather handbag", "limit": 5 }`
- **Output**: Ranked list of similar products with similarity scores

### `GET /api/catalog?limit=20`
Browse all indexed products.

## Frontend

Pair this with the [Multimodal Product Intelligence Frontend](https://github.com/Abdullah-Masood-05/multimodal-product-intelligence-frontend) — a Next.js app with drag-and-drop upload and real-time results display.

## License

MIT
