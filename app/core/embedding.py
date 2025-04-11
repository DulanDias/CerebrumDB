from sentence_transformers import SentenceTransformer
from app.config import TRANSFORMER_MODEL

class EmbeddingEngine:
    def __init__(self, model_name=TRANSFORMER_MODEL):
        self.model = SentenceTransformer(model_name)

    def encode(self, text: str):
        return self.model.encode(text, normalize_embeddings=True)
