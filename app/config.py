import os

TRANSFORMER_MODEL = os.getenv("TRANSFORMER_MODEL", "all-mpnet-base-v2")
CONTINUAL_LEARNING = os.getenv("CONTINUAL_LEARNING", "false") == "true"
DATA_STORE_TYPE = os.getenv("DATA_STORE_TYPE", "json")
VECTOR_INDEX_PATH = os.getenv("VECTOR_INDEX_PATH", "vector_index/index.faiss")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
