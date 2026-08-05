# Genkit-AI-Chatbot Technical Architecture Documentation 🏗️

## 1. System Overview

Genkit-AI-Chatbot is a full-stack platform designed to demonstrate modern LLM architecture, vector retrieval (RAG), FastAPI service orchestration, and modern React web UI design.

```text
[ React Frontend (Vite) ]
       │
       ▼ (HTTP / JSON / JWT)
[ FastAPI Main Router ]
       ├── Auth Handler (JWT / Bcrypt)
       ├── Admin Controller
       ├── Document Ingestion Engine (PDF / DOCX)
       └── Chatbot Orchestrator Service
               ├── Sliding Window Memory
               ├── RAG Retriever & Vector DB
               └── Custom PyTorch Transformer Engine
                       ├── Tokenizer (Subword / BPE)
                       ├── Learned Embeddings & Positional Encoding
                       ├── Encoder Block (Multi-Head Attention)
                       ├── Decoder Block (Causal Mask + Cross Attention)
                       └── Top-K / Top-P Generation Sampler
```

## 2. AI & Transformer Pipeline

- **Tokenizer**: Custom BPE/WordPiece tokenizer (`backend/ai/tokenizer/tokenizer.py`) managing vocabulary indexing.
- **Embedding Module**: Combines `nn.Embedding(vocab_size, d_model)` with learned positional encodings.
- **Transformer Architecture**:
  - `attention.py`: Multi-Head Attention mechanism scaled by $\sqrt{d_k}$.
  - `encoder.py`: Encoder layers with residual connections and layer normalization.
  - `decoder.py`: Masked self-attention and cross-attention blocks over retrieved context.
- **Inference Engine**: `generate.py` performs auto-regressive text generation using temperature, repetition penalty, top-k, and nucleus (top-p) sampling.

## 3. RAG Pipeline (Retrieval-Augmented Generation)

1. **Ingestion**: Documents (PDF/DOCX/JSON) parsed in `document_service.py`.
2. **Chunking**: `chunking.py` creates 300-token chunks with 50-token overlap.
3. **Embeddings & Vector Index**: `vector_database.py` generates TF-IDF / dense embeddings and builds a cosine similarity matrix.
4. **Retrieval & Reranking**: `retriever.py` fetches top candidate chunks, and `reranker.py` filters context relevance before feeding into the prompt memory.

## 4. Database Schema (SQLite / SQLAlchemy)

- `users`: ID, username, email, hashed_password, role, created_at.
- `chat_sessions`: ID, user_id, title, created_at, updated_at.
- `chat_messages`: ID, session_id, sender (user/bot), text, context_used, timestamp.
- `documents`: ID, filename, file_type, file_path, chunk_count, uploaded_at.
