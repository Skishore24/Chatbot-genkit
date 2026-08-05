# Genkit-AI-Chatbot 🤖⚡

An end-to-end full-stack AI Chatbot application featuring a custom **PyTorch Transformer** core, a **Retrieval-Augmented Generation (RAG)** pipeline, a **FastAPI** backend with SQLite/SQLAlchemy, and an ultra-modern **React + Vite** frontend UI with dark glassmorphic styling.

---

## 🌟 Key Features

- **Custom PyTorch Transformer Engine**: Self-contained Multi-Head Attention, Encoder-Decoder architecture, learned positional embeddings, BPE Tokenizer, and top-k/top-p nucleus sampling generator.
- **RAG Vector Search Pipeline**: Document chunking (PDF & DOCX), dense embeddings vector database, cosine similarity retriever, and context reranker.
- **FastAPI REST & Streaming Backend**: User authentication (JWT & bcrypt), Chat session management, sliding window memory, Admin analytics dashboard, and dynamic PDF/DOCX ingestion.
- **Modern React Frontend**: Designed with a sleek dark glassmorphic UI, real-time message streaming visualization, interactive workspace dashboard, active RAG context preview, and admin control metrics.

---

## 📁 Directory Structure

```text
Genkit-AI-Chatbot/
├── backend/
│   ├── api/
│   │   ├── routes/ (auth.py, chat.py, admin.py)
│   │   └── auth/   (handler.py)
│   ├── ai/
│   │   ├── tokenizer/    (tokenizer.py, train_tokenizer.py)
│   │   ├── embeddings/   (embedding.py)
│   │   ├── transformer/  (attention.py, encoder.py, decoder.py, transformer.py)
│   │   ├── training/     (train.py, dataset.py)
│   │   ├── inference/    (generate.py)
│   │   ├── rag/          (chunking.py, embeddings.py, vector_database.py, retriever.py, reranker.py)
│   │   └── memory/       (chat_memory.py)
│   ├── database/         (models.py, database.py, crud.py)
│   ├── services/         (chatbot_service.py, document_service.py)
│   ├── uploads/          (pdf/, docx/)
│   ├── utils/            (helpers.py)
│   ├── config.py
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/  (Navbar, Chat, Sidebar, Loader, Message)
│   │   ├── pages/       (Home, Login, Register, Dashboard, Admin)
│   │   ├── services/    (api.js, authService.js, chatService.js, docService.js)
│   │   ├── hooks/       (useAuth.js, useChat.js)
│   │   ├── store/       (authContext.jsx, chatContext.jsx)
│   │   ├── styles/      (variables.css, global.css)
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── datasets/             (company_data.json, conversations.json)
├── docs/                 (ARCHITECTURE.md, API_DOCS.md)
├── scripts/              (setup_env.ps1, run_backend.py)
├── docker/               (Dockerfile.backend, Dockerfile.frontend)
├── docker-compose.yml
├── .env
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python**: 3.10+
- **Node.js**: 18+ & npm
- **Docker** (Optional, for containerized running)

---

### Backend Setup

1. **Navigate to the root or backend directory**:

   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   # On Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Tokenizer & Train Default Transformer Model**:

   ```bash
   python ai/training/train.py
   ```

5. **Start the FastAPI Backend Server**:
   ```bash
   python main.py
   ```
   _Backend runs on `http://127.0.0.1:8000` (Swagger docs available at `http://127.0.0.1:8000/docs`)._

---

### Frontend Setup

1. **Navigate to the frontend directory**:

   ```bash
   cd frontend
   ```

2. **Install Node dependencies**:

   ```bash
   npm install
   ```

3. **Launch Vite Development Server**:
   ```bash
   npm run dev
   ```
   _Frontend UI opens at `http://localhost:5173`._

---

### 🐳 Running with Docker Compose

```bash
docker-compose up --build
```

---

## 📜 License

MIT License. Designed & Built for modern AI applications.
