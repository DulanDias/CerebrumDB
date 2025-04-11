import os
from eval.datasets import hotpotqa, natural_questions, ms_marco
from eval.runners import faiss_only, rag_dpr, cerebrum_madb_off, cerebrum_madb_on
from eval.metrics import mrr, ndcg, recall
from eval.utils.csv_exporter import export_to_csv
from eval.utils.timer import measure_latency

RESULTS_DIR = "eval/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

ACCESS_TOKEN = "your_access_token_here"  # Replace with a valid access token

def main():
    # Step 1: Load and process the dataset
    dataset_path = "eval/datasets/hotpot_dev_fullwiki_v1.json"
    data = hotpotqa.load_dataset(dataset_path)
    documents = hotpotqa.prepare_documents(data)

    # Step 2: Ingest documents into the database
    hotpotqa.ingest_documents(documents, ACCESS_TOKEN)

    # Step 3: Run evaluation using cerebrum_madb_off
    results = cerebrum_madb_off.run()

    # Step 4: Evaluate using metrics
    metrics = {
        "MRR": mrr.evaluate(results),
        "NDCG": ndcg.evaluate(results),
        "Recall": recall.evaluate(results)
    }
    print("Evaluation Metrics:", metrics)

    # Step 5: Export results to CSV
    export_to_csv(results, os.path.join(RESULTS_DIR, "hotpotqa_results.csv"))

if __name__ == "__main__":
    main()
