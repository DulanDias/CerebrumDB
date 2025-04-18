import json
import requests
from typing import List, Dict

API_URL = "http://localhost:8000/document"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTc0NDQxNjAwM30.jk8Q5x8MKBjkzqvpGVk6DPJhF5M93Do6UKOhCJ7fUzE"  # Replace with a valid access token

def load_dataset(file_path: str) -> List[Dict]:
    """
    Load the HotpotQA dataset from the given file path.
    """
    with open(file_path, "r") as f:
        data = json.load(f)
    return data

def prepare_documents(data: List[Dict]) -> List[Dict]:
    """
    Prepare documents for ingestion by combining question and context.
    """
    documents = []
    for item in data:
        text = f"Question: {item['question']}\nContext: {item['context']}"
        document = {
            "text": text,
            "meta": {"source": "hotpotqa", "id": item["_id"]}
        }
        documents.append(document)
    return documents

def ingest_documents(documents: List[Dict], access_token: str):
    """
    Ingest documents into the CerebrumDB database.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    for document in documents:
        response = requests.post(API_URL, json=document, headers=headers)
        if response.status_code == 200:
            print(f"Document added successfully: {response.json()}")
        else:
            print(f"Failed to add document: {response.status_code}, {response.text}")
