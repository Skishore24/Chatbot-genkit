# API Endpoint Specification 📡

## Base URL: `http://127.0.0.1:8000/api`

### 🔑 Authentication Routes (`/auth`)

| Method | Endpoint             | Description                                 | Auth Required |
| ------ | -------------------- | ------------------------------------------- | ------------- |
| POST   | `/api/auth/register` | Register a new user                         | No            |
| POST   | `/api/auth/login`    | Authenticate user & get JWT token           | No            |
| GET    | `/api/auth/me`       | Retrieve current authenticated user profile | Yes (Bearer)  |

### 💬 Chat Routes (`/chat`)

| Method | Endpoint                          | Description                              | Auth Required |
| ------ | --------------------------------- | ---------------------------------------- | ------------- |
| POST   | `/api/chat/message`               | Send prompt to AI chatbot & get response | Yes (Bearer)  |
| GET    | `/api/chat/sessions`              | List user's active chat sessions         | Yes (Bearer)  |
| POST   | `/api/chat/sessions`              | Create a new chat session                | Yes (Bearer)  |
| GET    | `/api/chat/history/{session_id}`  | Retrieve chat history for a session      | Yes (Bearer)  |
| DELETE | `/api/chat/sessions/{session_id}` | Delete a chat session                    | Yes (Bearer)  |

### ⚙️ Admin & Document Routes (`/admin`)

| Method | Endpoint                        | Description                                       | Auth Required |
| ------ | ------------------------------- | ------------------------------------------------- | ------------- |
| GET    | `/api/admin/metrics`            | Retrieve system, GPU/CPU, and vector DB stats     | Yes (Admin)   |
| GET    | `/api/admin/documents`          | List all indexed RAG documents                    | Yes (Bearer)  |
| POST   | `/api/admin/upload`             | Upload PDF/DOCX document and trigger RAG indexing | Yes (Bearer)  |
| DELETE | `/api/admin/documents/{doc_id}` | Remove document from RAG index                    | Yes (Bearer)  |
