import os

TRANSFORMER_MODEL = os.getenv("TRANSFORMER_MODEL", "all-mpnet-base-v2")
CONTINUAL_LEARNING = os.getenv("CONTINUAL_LEARNING", "false") == "true"
DATA_STORE_TYPE = os.getenv("DATA_STORE_TYPE", "json")
VECTOR_INDEX_PATH = os.getenv("VECTOR_INDEX_PATH", "vector_index/index.faiss")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6380")
REFRESH_TOKEN_EXPIRE_HOURS = int(os.getenv("REFRESH_TOKEN_EXPIRE_HOURS", 24))  # Default: 24 hours
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 180))  # Default: 3 hours
CHUNKING_ENABLED = os.getenv("CHUNKING_ENABLED", "true") == "true"
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 100))  # Default chunk size: 100 words