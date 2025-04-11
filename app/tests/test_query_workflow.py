from app.core.vector_store import VectorStore
from app.core.embedding import EmbeddingEngine

def test_query_workflow():
    embedder = EmbeddingEngine()
    vstore = VectorStore()

    # Add a document
    doc_text = "Quantum physics revolutionized science."
    doc_vector = embedder.encode(doc_text)
    vstore.add("doc1", doc_vector)

    # Query the document
    query_text = "Quantum physics"
    query_vector = embedder.encode(query_text)
    results = vstore.search(query_vector, top_k=1)

    print(f"Results: {results}")

    assert len(results) > 0, "No results found for the query."
    assert results[0] == "doc1", "The returned document ID does not match."