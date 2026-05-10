from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import analyze, search, catalog

app = FastAPI(title="ProductIQ API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router)
app.include_router(search.router)
app.include_router(catalog.router)

@app.get("/")
async def root():
    return {"status": "ok", "message": "ProductIQ API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
