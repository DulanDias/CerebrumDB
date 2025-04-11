from sentence_transformers import SentenceTransformer
from app.config import TRANSFORMER_MODEL, CHUNK_SIZE, CHUNKING_ENABLED
from app.utils.preprocessor import Preprocessor

class EmbeddingEngine:
    def __init__(self, model_name=TRANSFORMER_MODEL):
        self.model = SentenceTransformer(model_name)
        self.preprocessor = Preprocessor()

    def encode(self, text: str):
        # Preprocess and chunk the text
        cleaned_text = self.preprocessor.clean_text(text)
        chunks = self.preprocessor.chunk_text(cleaned_text, CHUNK_SIZE) if CHUNKING_ENABLED else [cleaned_text]

        # Encode each chunk
        embeddings = [self.model.encode(chunk, normalize_embeddings=True) for chunk in chunks]
        return embeddings, chunks
