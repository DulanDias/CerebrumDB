import json, os
from uuid import uuid4

class DocumentStore:
    def __init__(self, path="data_store/"):
        self.path = path
        os.makedirs(path, exist_ok=True)

    def save(self, doc):
        doc_id = str(uuid4())
        with open(f"{self.path}/{doc_id}.json", "w") as f:
            json.dump(doc, f)
        return doc_id

    def load(self, doc_id):
        with open(f"{self.path}/{doc_id}.json") as f:
            return json.load(f)

    def delete(self, doc_id):
        os.remove(f"{self.path}/{doc_id}.json")
