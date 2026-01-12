import os
from dotenv import load_dotenv

load_dotenv()

VERBOSE = True

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
APP_URL = os.getenv("APP_URL", "http://localhost")
APP_NAME = os.getenv("APP_NAME", "plant-kg-user-plant-mvp")

EMBED_MODEL = os.getenv("EMBED_MODEL", "openai/text-embedding-3-small")
LLM_MODEL = os.getenv("LLM_MODEL", "openai/gpt-5-nano")

MEMORY_PATH = os.getenv("MEMORY_PATH", "agent_memory.json")

CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "chroma_db_user_plant_v1")
CHROMA_COLLECTION_NAME = os.getenv(
    "CHROMA_COLLECTION_NAME",
    "agent_memory_notes_user_plant_v1"
)
