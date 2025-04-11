import json
from typing import List, Tuple

def load_dataset() -> List[Tuple[str, str]]:
    with open("data/hotpotqa.json") as f:
        data = json.load(f)
    return [(item["question"], item["answer"]) for item in data]
