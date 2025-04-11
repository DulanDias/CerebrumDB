from app.core.document_store import DocumentStore

def test_document_save_load_delete():
    store = DocumentStore(path="test_store/")
    doc = {"text": "Hello World", "meta": {"lang": "en"}}
    doc_id = store.save(doc)
    loaded = store.load(doc_id)
    assert loaded["text"] == "Hello World"
    store.delete(doc_id)
