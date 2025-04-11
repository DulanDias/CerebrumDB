import json
from typing import List, Tuple

def load_dataset() -> List[Tuple[str, str]]:
    with open("data/ms_marco.json") as f:
        data = json.load(f)
    return [(item["query"], item["answer"]) for item in data]
