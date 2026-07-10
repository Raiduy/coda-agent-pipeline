import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class Settings:
    # LiteLLM Configuration
    CHAT_MODEL: str = os.getenv("CHAT_MODEL", "FAST.gpt-oss:120b")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "Qwen3-Embedding-8B")
    LITELLM_API_KEY: str = os.getenv("LITELLM_API_KEY", "mock-key-if-not-required")
    LITELLM_BASE_URL: str = os.getenv("LITELLM_BASE_URL", "http://localhost:4000")
    
    TEMPERATURE: float = 0.0

    DEBUG_LEVEL: str = os.getenv("DEBUG_LEVEL", "DEBUG")
    
    CHUNK_SIZE: int = 2000
    CHUNK_OVERLAP: int = 200

settings = Settings()
