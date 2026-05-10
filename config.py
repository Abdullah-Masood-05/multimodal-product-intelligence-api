from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    groq_api_key: str
    qdrant_url: str = "http://localhost:6333"
    vision_model: str = "meta-llama/llama-4-scout-17b-16e-instruct"
    clip_model: str = "openai/clip-vit-large-patch14"

    class Config:
        env_file = ".env"

settings = Settings()
