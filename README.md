# 🧠 CerebrumDB

> A brain-inspired, schema-flexible semantic database with transformer-based memory-attention retrieval.

**CerebrumDB** is a next-generation database engine designed for intelligent querying of unstructured data. It combines schema-free storage, dense vector indexing, and transformer-powered attention mechanisms to enable semantic search that feels like reasoning — not just matching.

Built from scratch — no external databases — CerebrumDB includes integrated access control, disk-optimized vector search, transformer configurability, structured logging, optional continual learning, and blazing-fast REST APIs.

---

## 🔍 Features

- ✅ Schema-free document and metadata store (JSON or binary)
- ✅ Transformer-based embedding (`BGE`, `MPNet`, `SBERT`, etc.)
- ✅ Attention-powered retrieval with MADB (Memory-Attention DB)
- ✅ High-performance vector search using FAISS (disk-based with mmap)
- ✅ Fine-grained user/role access control (ACL)
- ✅ RESTful API (FastAPI + Gunicorn/Uvicorn)
- ✅ Optional continual learning loop
- ✅ Embedding caching + structured logging
- ✅ Input validation and sanitization

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/your-username/cerebrumdb.git
cd cerebrumdb

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload

# Run in production
gunicorn app.main:app -k uvicorn.workers.UvicornWorker --workers 4 --bind 0.0.0.0:8000
```
---

## 📦 API Endpoints

| Method | Endpoint | Description |
|--------|--------------------|--------------------------|
| POST   | `/document`        | Ingest document (text + meta) |
| PUT    | `/document/{id}`   | Update document          |
| DELETE | `/document/{id}`   | Delete document          |
| POST   | `/query`           | Semantic vector search   |
| POST   | `/feedback`        | Submit user feedback     |
| GET    | `/document/{id}`   | Retrieve full document   |

---
## 📘 Using the API: Step-by-Step Workflow

This section walks through how to consume the CerebrumDB API from initialization to querying.

---

### 🧑‍💻 Step 1: Initialize the User Database

```bash
POST /user/init
```

Initializes a secure user database on disk. Run once.

---

### 👤 Step 2: Create a New User

```bash
POST /user/create
Content-Type: application/json

{
  "user_id": "alice",
  "password": "secret123",
  "role": "editor"
}
```

Roles supported:
- `admin`: full access
- `editor`: can add/update docs
- `viewer`: read-only and query access

---

### 🔑 Step 3: Login and Get Access Token

```bash
POST /user/token
Content-Type: application/x-www-form-urlencoded

user_id=alice&password=secret123
```

Returns:

```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer"
}
```

Use this token in the `Authorization` header:

```http
Authorization: Bearer <access_token>
```

---

### 📄 Step 4: Add a Document

```bash
POST /document
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "text": "Quantum physics explains the nature of particles.",
  "meta": { "category": "science", "author": "alice" }
}
```

---

### 🔍 Step 5: Perform a Semantic Query

```bash
POST /query
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "query": "nature of subatomic particles",
  "top_k": 3
}
```

Returns ranked documents with scores and metadata.

---

### 📝 Step 6: Submit Relevance Feedback

```bash
POST /feedback
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "query": "nature of subatomic particles",
  "doc_id": "xyz123",
  "relevant": true
}
```

This logs user-labeled feedback to support future model fine-tuning.

---

### 🔄 Optional: Update or Delete a Document

```bash
PUT /document/{id}
DELETE /document/{id}
```

Requires `admin` or `editor` role for PUT, `admin` for DELETE.

---

All endpoints follow RESTful design and require valid JWT tokens for access.

You can explore the API interactively at:

```
http://localhost:8000/docs
```

### 🔄 Refresh Access Token

```bash
POST /user/refresh
Content-Type: application/x-www-form-urlencoded

refresh_token=<refresh_token>
```

Returns:
```bash
{
  "access_token": "new_access_token",
  "token_type": "bearer"
}
```

---
## ⚙️ Configuration

You can customize your CerebrumDB setup via `.env` or `config.py`:

```env
TRANSFORMER_MODEL=all-mpnet-base-v2
CONTINUAL_LEARNING=true
DATA_STORE_TYPE=binary  # or json
VECTOR_INDEX_PATH=vector_index/index.faiss
```

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

```
app/
├── core/        # Core modules: embedding, vector, document, MADB
├── routes/      # REST API endpoints
├── models/      # Pydantic schemas
├── utils/       # Helpers: logging, preprocessing, caching
├── tests/       # Unit + integration tests
├── config.py    # Global settings
```

---

## 🧠 Continual Learning (Optional)

When enabled, CerebrumDB captures user feedback on query results:

```json
{
  "query": "climate change policy",
  "doc_id": "abc123",
  "relevant": true
}
```

Stored feedback is used to fine-tune the model periodically or retrain embeddings in-place.

---

## 📚 Paper

This repository accompanies our upcoming paper:

**"CerebrumDB: A Brain-Inspired Memory-Attention Semantic Database"**  
(arXiv preprint — coming soon)

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

<!-- - Website: [https://cerebrumdb.com](https://cerebrumdb.com)-->
- Docs: Coming soon
- Author: [Dulan S. Dias](https://dulandias.com)
