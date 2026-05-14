# Autonomous Multi-Agent Product Intelligence API

An enterprise-grade, multi-agent AI backend that transforms raw product images into comprehensive market strategies. Built with **FastAPI**, **Groq Vision (Llama 4 Scout)**, **CLIP embeddings**, and **Qdrant vector search**.

This system operates as a pipeline of 5 specialized autonomous agents:

1. 🔍 **Agent 1: Vision Analyst** — Extracts structural data (title, category, price tier) directly from an image.
2. 📊 **Agent 2: Market Researcher** — Performs vector similarity searches against a database of competitors and generates structured market positioning insights.
3. 🤖 **Agent 3: Customer Psychologist (Twin Simulator)** — Synthesizes synthetic shopper personas, simulates their emotional reactions, and calculates purchase probability.
4. 💰 **Agent 4: Pricing Strategist** — Cross-references market competitor data with psychological pushback to calculate the mathematical ideal price point and margin risk.
5. 📢 **Agent 5: Ad Strategist** — Uses concurrent threading (`asyncio`) to simultaneously generate 5 bespoke marketing campaigns (Facebook, Instagram, Google Shopping, WhatsApp, Email).

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **API Framework** | FastAPI (Python 3.11+) |
| **Agent LLM** | Groq LPU — Llama 4 Scout 17B (JSON Mode, ~800 tok/s) |
| **Concurrency** | `asyncio.to_thread` for parallel agent execution |
| **Embeddings** | OpenAI CLIP ViT-L/14 (Local GPU inference) |
| **Vector DB** | Qdrant v1.17+ (Self-hosted via Docker) |

## Project Structure

```text
├── main.py              ← FastAPI entry point & CORS config
├── config.py            ← Environment & model configuration
├── schemas.py           ← Pydantic validation models
├── routers/
│   ├── analyze.py       ← Agent 1 endpoint
│   ├── market.py        ← Agent 2 endpoint
│   ├── simulator.py     ← Agent 3 endpoint
│   ├── pricing.py       ← Agent 4 endpoint
│   ├── campaign.py      ← Agent 5 endpoint
│   └── search.py/catalog.py ← Vector DB utilities
├── services/
│   ├── vision.py        ← Llama 4 Vision prompting
│   ├── market_researcher.py
│   ├── simulator.py
│   ├── pricing.py
│   ├── ad_campaign.py   ← 5-channel concurrent generation
│   ├── embeddings.py    ← CLIP embedding pipeline
│   └── vector_store.py  ← Qdrant operations
├── requirements.txt
└── .env.example
```

## Quick Start

### 1. Start Qdrant (Vector Database)
Ensure Docker is running, then spin up the Qdrant container:
```bash
docker run -d -p 6333:6333 -v qdrant_data:/qdrant/storage qdrant/qdrant:latest
```

### 2. Install Dependencies
```bash
python -m venv myenv
source myenv/bin/activate  # Or `myenv\Scripts\activate` on Windows
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
```
Edit `.env` and add your `GROQ_API_KEY`.

### 4. Run the Server
```bash
uvicorn main:app --reload --port 8000
```
The API is now live at `http://localhost:8000`. Interactive OpenAPI documentation is available at `http://localhost:8000/docs`.

## Database Seeding
To test Agent 2 (Market Researcher) and duplicate detection, you need data in Qdrant. Use the provided seeder script:
```bash
python seed_catalog.py /path/to/your/image/folder
```

## Frontend
Pair this with the **[Multimodal Product Intelligence Frontend](https://github.com/Abdullah-Masood-05/multimodal-product-intelligence-frontend)** — a Next.js App Router application built with Tailwind CSS that provides a stunning UI for interacting with all 5 agents.

## License
MIT
