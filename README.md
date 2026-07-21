# AI Knowledge Assistant

An AI-powered Knowledge Assistant built with **FastAPI**, **OpenRouter**, **Embeddings**, **ChromaDB**, and **Retrieval-Augmented Generation (RAG)**.

This project demonstrates the core architecture used in many modern AI applications by combining Large Language Models (LLMs) with a Vector Database to provide accurate, context-aware answers from custom organizational knowledge.

---

# Project Overview

Traditional AI chatbots rely only on the model's training data.

This application extends LLM capabilities by allowing the model to retrieve and use information from custom documents before generating a response.

Example:

**Question**

```text
How do I get technical support?
```

**Retrieved Context**

```text
Technical support is available by emailing support@company.com.
```

**Answer**

```text
You can get technical support by emailing support@company.com.
```

This technique is known as:

```text
RAG
(Retrieval-Augmented Generation)
```

---

# Features

✅ FastAPI REST API

✅ OpenRouter Integration

✅ GPT-4o-mini Chat Completion

✅ Text Embeddings

✅ ChromaDB Vector Database

✅ Semantic Search

✅ RAG (Retrieval-Augmented Generation)

✅ Swagger API Documentation

✅ Environment Variable Management

✅ Git & GitHub Version Control

---

# Architecture Diagram

```text
                     ┌─────────────────┐
                     │ User Question   │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ FastAPI Endpoint│
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ Embedding Model │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ ChromaDB Search │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ Retrieved Context│
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ GPT-4o-mini     │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ Final Answer    │
                     └─────────────────┘
```

---

# Technologies Used

## Backend

- FastAPI
- Uvicorn
- Python 3.x

## AI / LLM

- OpenRouter
- GPT-4o-mini
- OpenAI SDK

## Vector Database

- ChromaDB

## AI Concepts

- Embeddings
- Semantic Search
- Vector Similarity Search
- Retrieval-Augmented Generation (RAG)

## Development Tools

- VS Code
- Git
- GitHub
- Swagger UI

---

# Project Structure

```text
ai-knowledge-assistant/

│
├── app.py
├── .env
├── .gitignore
│
├── documents/
│   └── company_policy.txt
│
├── venv/
│
└── README.md
```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/bilalsarwar2907/ai-knowledge-assistant-rag.git

cd ai-knowledge-assistant-rag
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install fastapi uvicorn openai chromadb python-dotenv
```

---

## 4. Configure Environment Variables

Create:

```text
.env
```

Example:

```text
OPENROUTER_API_KEY=your-api-key-here
```

---

## 5. Run Application

```bash
python -m uvicorn app:app --reload --port 8001
```

---

## 6. Open Swagger UI

```text
http://127.0.0.1:8001/docs
```

---

# API Endpoints

## Home

```http
GET /
```

Returns application status.

---

## Test LLM Connection

```http
GET /test-openai
```

Tests GPT response through OpenRouter.

---

## Ask GPT Directly

```http
GET /ask?question=YourQuestion
```

Example:

```text
/ask?question=What is FastAPI?
```

---

## Test Embeddings

```http
GET /test-embedding
```

Generates a vector embedding and returns dimensions.

Example output:

```json
{
  "dimensions": 1536
}
```

---

## Load Documents

```http
GET /load-docs
```

Loads local documents into ChromaDB.

---

## View Stored Documents

```http
GET /all-docs
```

Returns stored vector documents.

---

## Vector Search

```http
GET /search?query=support
```

Performs semantic search against the vector database.

---

## RAG Endpoint

```http
GET /ask-rag?question=How do I get technical support?
```

Workflow:

```text
Question
   ↓
Embedding
   ↓
Vector Search
   ↓
Retrieved Context
   ↓
GPT
   ↓
Answer
```

---

# Example Workflow

## Step 1

Load documents:

```http
GET /load-docs
```

---

## Step 2

Search documents:

```http
GET /search?query=support
```

---

## Step 3

Ask RAG:

```http
GET /ask-rag?question=How do I get technical support?
```

Result:

```json
{
  "answer": "You can get technical support by emailing support@company.com."
}
```

---

# Screenshots

Add screenshots here after uploading images.

## Swagger Documentation

```text
images/swagger-home.png
```

---

## Embedding Endpoint Response

```text
images/embedding-test.png
```

---

## ChromaDB Search Result

```text
images/vector-search.png
```

---

## RAG Response

```text
images/rag-response.png
```

---

# Skills Demonstrated

This project demonstrates practical experience with:

- REST API Development
- FastAPI
- OpenRouter APIs
- Prompt Engineering
- Text Embeddings
- Vector Databases
- ChromaDB
- Semantic Search
- Retrieval-Augmented Generation (RAG)
- Environment Variables
- Swagger Documentation
- Git & GitHub

---

# Lessons Learned

During development the following real-world issues were encountered and resolved:

### Virtual Environment Issues

Packages were installed globally instead of within the project's virtual environment.

### Port Conflicts

An existing FastAPI process was running on the same port.

### API Authentication

Encountered both:

```text
401 Invalid API Key
```

and

```text
429 Insufficient Quota
```

errors while integrating with external AI providers.

### ChromaDB Persistence

Learned the difference between:

```python
chromadb.Client()
```

and:

```python
chromadb.PersistentClient()
```

### Python Indentation

Python uses indentation rather than braces to define execution blocks.

---

# Future Improvements

## Phase 2

- Persistent ChromaDB storage
- Multiple documents
- Document chunking
- Metadata support

## Phase 3

- PDF Upload Support
- DOCX Upload Support
- User Authentication
- Role-Based Access

## Phase 4

- Agent Routing
- Multi-Agent Workflows
- LangGraph Integration
- Conversation Memory

## Phase 5

- Docker Containerization
- Azure Deployment
- CI/CD Pipeline
- Monitoring & Logging

---

# Author

**Hafiz Muhammad Bilal Sarwar**

GitHub:
https://github.com/bilalsarwar2907

LinkedIn:
https://linkedin.com/in/bilal-sarwar-a449a83b7

---

# License

This project is provided for educational and portfolio purposes.
