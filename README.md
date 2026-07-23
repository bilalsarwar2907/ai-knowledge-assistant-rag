 AI Knowledge Assistant

A production-style **Full-Stack AI Knowledge Assistant** built with **Vue.js**, **FastAPI**, **OpenRouter**, **GPT-4o-mini**, **Embeddings**, **ChromaDB**, **Retrieval-Augmented Generation (RAG)**, **Agent Routing**, **JWT Authentication**, **Docker**, and **GitHub Actions CI/CD**.

This project demonstrates how modern AI applications are built by combining Large Language Models (LLMs) with Vector Databases, Semantic Search, Retrieval-Augmented Generation, Authentication, Evaluation Frameworks, and a modern frontend experience.

The application allows users to upload, retrieve, search, and chat with organizational knowledge while showcasing production-oriented AI engineering patterns.


 Project Overview

Traditional AI chatbots rely solely on a model's pre-trained knowledge.

The AI Knowledge Assistant extends LLM capabilities by retrieving relevant information from custom documents before generating responses.

Supported knowledge sources include:

* Text Documents
* PDF Documents
* Chunked Knowledge Bases
* Vector Embeddings
* ChromaDB Collections

The system combines:

```text
LLM Intelligence
+
Vector Search
+
Custom Knowledge
+
Conversation Memory
=
Domain-Aware AI Assistant
```

Example:

### User Question

```text
What sector is excluded?
```

### Retrieved Context

```text
The Airlines sector is excluded from this policy.
```

### RAG Response

```text
The Airlines sector is excluded.
```

***

# Key Features

### AI & LLM Features

✅ GPT-4o-mini Integration

✅ OpenRouter Integration

✅ Text Embeddings

✅ Vector Similarity Search

✅ Retrieval-Augmented Generation (RAG)

✅ Multi-Document RAG

✅ PDF Ingestion

✅ Chunked Retrieval

✅ Agent-Based Routing

✅ Conversation Memory

✅ Semantic Search

✅ Evaluation Framework

***

### Backend Features

✅ FastAPI REST APIs

✅ Swagger Documentation

✅ JWT Authentication

✅ Protected Endpoints

✅ Persistent ChromaDB Storage

✅ Environment Variable Configuration

✅ Modular AI Services

***

### Frontend Features

✅ Vue 3

✅ Vue Router

✅ Axios API Integration

✅ Login System

✅ Chat Interface

✅ Agent Testing Interface

✅ Search Interface

✅ Document Management Interface

✅ Evaluation Dashboard

✅ Modern Responsive UI

***

### DevOps Features

✅ Docker Containerization

✅ Docker Build Validation

✅ GitHub Actions CI/CD

✅ Automated Build Pipelines

✅ Source Control via Git & GitHub

***

# Architecture

```text
┌─────────────────────────────┐
│         Vue Frontend        │
│                             │
│  Login                      │
│  Chat                       │
│  Agent                      │
│  Search                     │
│  Documents                  │
│  Evaluation                 │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│       FastAPI Backend       │
│                             │
│  JWT Authentication         │
│  RAG Service                │
│  Agent Routing              │
│  PDF Processing             │
│  Vector Search              │
│  Evaluation Engine          │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│         OpenRouter          │
│                             │
│  GPT-4o-mini               │
│  Embedding Models          │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│         ChromaDB            │
│                             │
│  Persistent Storage         │
│  Embeddings                 │
│  Chunked Documents          │
│  Similarity Search          │
└─────────────────────────────┘
```

***

# Technologies Used

## Frontend

* Vue 3
* Vue Router
* Axios
* JavaScript
* CSS

## Backend

* FastAPI
* Python
* Uvicorn
* Pydantic

## AI & LLM

* OpenRouter
* GPT-4o-mini
* OpenAI SDK
* Text Embeddings

## Vector Database

* ChromaDB
* Persistent Collections
* Vector Similarity Search

## Authentication

* JWT
* python-jose
* bcrypt
* passlib

## Document Processing

* PyPDF
* PDF Text Extraction
* Document Chunking

## DevOps

* Docker
* GitHub Actions
* Git
* GitHub

***

# Core AI Concepts Demonstrated

This project demonstrates practical implementation of:

* Large Language Models (LLMs)
* Embeddings
* Vector Databases
* Similarity Search
* Semantic Search
* Retrieval-Augmented Generation (RAG)
* Multi-Document Retrieval
* Chunking Strategies
* Agent Routing
* Conversation Memory
* AI Evaluation
* Authentication for AI Applications
* Production AI Architecture

***

# Current Application Pages

### Login

Authenticate users using JWT tokens.

### Chat

Interact with the RAG-powered knowledge base.

### Agent

Visualize GPT vs RAG routing decisions.

### Documents

Manage loaded knowledge sources and review stored chunks.

### Search

Perform standalone vector similarity searches and inspect retrieval quality.

### Evaluation

Validate AI responses against expected outcomes and measure answer quality.

***

# API Endpoints

### General

```http
GET /
GET /count
```

### LLM

```http
GET /test-openai
GET /ask
```

### Embeddings

```http
GET /test-embedding
```

### Knowledge Base

```http
GET /load-docs
GET /load-pdfs
GET /all-docs
GET /search
```

### RAG

```http
GET /ask-rag
```

### Agent

```http
GET /agent
```

### Evaluation

```http
GET /evaluate
```

### Authentication

```http
GET /login
GET /protected
```

***

# Project Structure

```text
ai-knowledge-assistant/
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── views/
│   └── router/
│
├── documents/
│   ├── faq.pdf
│   ├── handbook.pdf
│   └── company_policy.txt
│
├── chroma_db/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── docker-build.yml
│
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .env
├── README.md
│
└── venv/
```

***

# Resume Highlights

This project demonstrates experience with:

* FastAPI
* Vue.js
* GPT Integration
* OpenRouter APIs
* Embeddings
* ChromaDB
* Vector Search
* Retrieval-Augmented Generation (RAG)
* Multi-Document Knowledge Retrieval
* Chunking Strategies
* Agent Routing
* Conversation Memory
* JWT Authentication
* AI Evaluation Frameworks
* Docker
* GitHub Actions CI/CD
* Full-Stack AI Application Development

***

# Future Enhancements

### High Priority

* User PDF Upload
* Persistent Conversation Memory (SQLite/PostgreSQL)
* User Profile Page

### Cloud & Production

* Azure App Service Deployment
* Azure Static Web Apps
* Azure OpenAI Integration
* Azure AI Search
* Enterprise RAG
* Monitoring & Logging

### Advanced AI

* Semantic Kernel
* Multi-Agent Workflows
* Azure AI Foundry
* Copilot Studio Integration

***

# Author

**Hafiz Muhammad Bilal Sarwar**

GitHub:  
[BilalSarwar2907](https://github.com/bilalsarwar2907)

LinkedIn:  
[Bilal Sarwar](https://linkedin.com/in/bilal-sarwar-a449a83b7)

***

# License

This project is provided for educational, learning, and portfolio purposes.
