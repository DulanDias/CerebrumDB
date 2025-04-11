## 📦 API Endpoints

\| Method \| Endpoint \| Description \|
\|--------\|--------------------\|--------------------------\|
\| POST   \| \`/document\`        \| Ingest document (text + meta) \|
\| PUT    \| \`/document/{id}\`   \| Update document          \|
\| DELETE \| \`/document/{id}\`   \| Delete document          \|
\| POST   \| \`/query\`           \| Semantic vector search   \|
\| POST   \| \`/feedback\`        \| Submit user feedback     \|
\| GET    \| \`/document/{id}\`   \| Retrieve full document   \|

---

## ⚙️ Configuration

You can customize your CerebrumDB setup via \`.env\` or \`config.py\`:

\`\`\`env
TRANSFORMER_MODEL=all-mpnet-base-v2
CONTINUAL_LEARNING=true
DATA_STORE_TYPE=binary  # or json
VECTOR_INDEX_PATH=vector_index/index.faiss
\`\`\`

---

## 🧪 Evaluation

CerebrumDB is benchmarked on:
- [HotpotQA](https://hotpotqa.github.io/)
- [Natural Questions](https://ai.google.com/research/NaturalQuestions)
- [MS MARCO](https://microsoft.github.io/msmarco/)

Metrics:
- 🔹 MRR@10
- 🔹 nDCG@10
- 🔹 Recall@K
- 🔹 Query latency (ms)

---

## 📁 Project Structure

\`\`\`
app/
├── core/        # Core modules: embedding, vector, document, MADB
├── routes/      # REST API endpoints
├── models/      # Pydantic schemas
├── utils/       # Helpers: logging, preprocessing, caching
├── tests/       # Unit + integration tests
├── config.py    # Global settings
\`\`\`

---

## 🧠 Continual Learning (Optional)

When enabled, CerebrumDB captures user feedback on query results:

\`\`\`json
{
  "query": "climate change policy",
  "doc_id": "abc123",
  "relevant": true
}
\`\`\`

Stored feedback is used to fine-tune the model periodically or retrain embeddings in-place.

---

## 📚 Paper

This repository accompanies our upcoming paper:

**"CerebrumDB: A Brain-Inspired Memory-Attention Semantic Database"**  
\(arXiv preprint — coming soon\)

---

## 🤝 Contributing

We welcome contributions from researchers, developers, and tinkerers exploring:
- Neural databases
- Information retrieval
- Transformer search
- Query reasoning

Please submit a pull request or open an issue to get started.

---

## 📄 License

MIT License — free for academic, commercial, and internal use.

---

## 🌐 Links

<!-- - Website: \[https://cerebrumdb.ai\]\(https://cerebrumdb.ai\) *(optional placeholder)* -->
- Docs: Coming soon
- Author: \[Dulan S. Dias\]\(https://dulandias.com\)
