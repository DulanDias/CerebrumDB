import csv
from typing import List, Dict

def export_to_csv(data: List[Dict], filepath: str):
    with open(filepath, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
