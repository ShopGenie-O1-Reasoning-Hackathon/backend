from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
import os
from dotenv import load_dotenv

load_dotenv()  
class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY:str = os.getenv("SUPABASE_ANON_KEY")
    SUPABASE_BUCKET_NAME: str = os.getenv("SUPABASE_BUCKET_NAME")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    QDRANT_HOST: str = os.getenv("QDRANT_HOST")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY")
    ROBOFLOW_API_KEY: str = os.getenv("ROBOFLOW_API_KEY")
    QDRANT_COLLECTION_SHOPGENIE: str = os.getenv("COLLECTION_NAME")


settings = Settings()