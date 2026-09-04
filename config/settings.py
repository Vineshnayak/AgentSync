import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen/qwen3.8-27b")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///agentsync_memory.db")
    
    @classmethod
    def validate(cls):
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set. Please set it in your .env file.")

settings = Settings()
