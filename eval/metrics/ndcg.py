import math

def compute_ndcg(results: dict) -> float:
    relevant = results["relevant"]
    retrieved = results["retrieved"]
    if not retrieved:
        return 0.0
    dcg = 0.0
    for rank, doc_id in enumerate(retrieved[:10], start=1):
        if doc_id == relevant:
            dcg += 1 / math.log2(rank + 1)
    idcg = 1.0  # Ideal DCG is 1 if the relevant doc is ranked first
    return dcg / idcg
