# AI Chatbot API (RAG-based)

A production-ready AI chatbot backend that can answer questions from uploaded documents using Retrieval-Augmented Generation (RAG).

## Live Demo
👉 https://ai-chatbot-api-qomp.onrender.com/docs

---

## Features

- 📄 Upload PDF documents
- 🔍 Semantic search using embeddings
- 🤖 AI-generated answers (RAG pipeline)
- 🔐 JWT Authentication (Signup/Login)
- 💬 Chat history stored in database
- 📦 Dockerized for easy deployment
- ☁️ Deployed on Render

---

## Tech Stack

- **Backend:** FastAPI
- **Database:** SQLite + SQLAlchemy
- **AI:** OpenAI (Embeddings + LLM)
- **Vector DB:** FAISS
- **Auth:** JWT (python-jose)
- **Deployment:** Render
- **Containerization:** Docker

---

## Architecture

User → Upload PDF → Extract Text → Chunking → Embeddings → FAISS  
User Query → Embedding → Similarity Search → Context → LLM → Answer

---

## Authentication Flow

- User Signup/Login
- JWT Token generated
- Protected routes using Bearer token

---

## Installation

```bash
git clone https://github.com/Shadow-code-dev/AI-Chatbot-API.git
cd AI-Chatbot-API

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:fastapi_app --reload