def compute_recall(results: dict) -> float:
    relevant = results["relevant"]
    retrieved = results["retrieved"]
    if not retrieved:
        return 0.0
    return 1.0 if relevant in retrieved[:10] else 0.0
