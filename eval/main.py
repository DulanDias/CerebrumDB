import os
from eval.datasets import hotpotqa, natural_questions, ms_marco
from eval.runners import faiss_only, rag_dpr, cerebrum_madb_off, cerebrum_madb_on
from eval.metrics import mrr, ndcg, recall
from eval.utils.csv_exporter import export_to_csv
from eval.utils.timer import measure_latency

RESULTS_DIR = "eval/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def main():
    datasets = {
        "HotpotQA": hotpotqa.load_dataset(),
        "NaturalQuestions": natural_questions.load_dataset(),
        "MSMARCO": ms_marco.load_dataset(),
    }

    runners = {
        "FAISS-Only": faiss_only.run_query,
        "RAG-DPR": rag_dpr.run_query,
        "Cerebrum-MADB-Off": cerebrum_madb_off.run_query,
        "Cerebrum-MADB-On": cerebrum_madb_on.run_query,
    }

    metrics = {
        "MRR@10": mrr.compute_mrr,
        "nDCG@10": ndcg.compute_ndcg,
        "Recall@10": recall.compute_recall,
    }

    results = []

    for dataset_name, dataset in datasets.items():
        for runner_name, runner in runners.items():
            print(f"Evaluating {runner_name} on {dataset_name}...")
            all_metrics = {metric: [] for metric in metrics}
            latencies = []

            for query, correct_answer in dataset:
                with measure_latency() as latency:
                    retrieved = runner(query)
                latencies.append(latency)

                for metric_name, metric_fn in metrics.items():
                    score = metric_fn({"retrieved": [r["doc_id"] for r in retrieved], "relevant": correct_answer})
                    all_metrics[metric_name].append(score)

            avg_metrics = {k: sum(v) / len(v) for k, v in all_metrics.items()}
            avg_latency = sum(latencies) / len(latencies)

            results.append({
                "Model": runner_name,
                "Dataset": dataset_name,
                **avg_metrics,
                "Avg Latency (ms)": avg_latency,
            })

    export_to_csv(results, os.path.join(RESULTS_DIR, "metrics_summary.csv"))

if __name__ == "__main__":
    main()
