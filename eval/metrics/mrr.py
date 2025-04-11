def compute_mrr(results: dict) -> float:
    relevant = results["relevant"]
    retrieved = results["retrieved"]
    if not retrieved:
        return 0.0
    for rank, doc_id in enumerate(retrieved[:10], start=1):
        if doc_id == relevant:
            return 1 / rank
    return 0.0
