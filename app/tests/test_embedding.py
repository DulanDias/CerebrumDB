from app.core.embedding import EmbeddingEngine

def test_embedding_shape():
    embedder = EmbeddingEngine()
    vec = embedder.encode("Test query")
    assert len(vec.shape) == 1
    assert vec.shape[0] > 0
