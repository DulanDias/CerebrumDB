from sentence_transformers import SentenceTransformer
from app.config import TRANSFORMER_MODEL, CHUNK_SIZE, CHUNKING_ENABLED
from app.utils.preprocessor import Preprocessor
import numpy as np

class EmbeddingEngine:
    def __init__(self, model_name=TRANSFORMER_MODEL):
        self.model = SentenceTransformer(model_name)
        self.preprocessor = Preprocessor()

    def encode(self, text: str, is_query: bool = False):
        # Preprocess and chunk the text
        cleaned_text = self.preprocessor.clean_text(text)
        if is_query or not CHUNKING_ENABLED:
            # Skip chunking for queries
            chunks = [cleaned_text]
        else:
            chunks = self.preprocessor.chunk_text(cleaned_text, CHUNK_SIZE)

        # Encode each chunk
        embeddings = [self.model.encode(chunk, normalize_embeddings=True) for chunk in chunks]

        # Ensure consistent vector shape by padding or truncating
        max_dim = max(embedding.shape[0] for embedding in embeddings)
        embeddings = [np.pad(embedding, (0, max_dim - embedding.shape[0])) if embedding.shape[0] < max_dim else embedding[:max_dim] for embedding in embeddings]

        # For queries, return a single vector (average of chunks)
        if is_query:
            return np.mean(embeddings, axis=0)

        return embeddings, chunks
