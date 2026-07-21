from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
import os

# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()

# ==========================================================
# CREATE FASTAPI APP
# ==========================================================

app = FastAPI(
    title="AI Knowledge Assistant",
    version="1.0"
)

# ==========================================================
# OPENROUTER CLIENT
# ==========================================================

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# ==========================================================
# CHROMADB
# ==========================================================
# In-memory for learning.
# Later we will switch to PersistentClient.
# ==========================================================

chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(
    name="company_docs"
)

# ==========================================================
# HOME
# ==========================================================

@app.get("/")
def home():

    return {
        "status": "ok",
        "message": "AI Knowledge Assistant Running"
    }

# ==========================================================
# TEST LLM CONNECTION
# ==========================================================

@app.get("/test-openai")
def test_openai():

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "Say hello"
            }
        ]
    )

    return {
        "answer": response.choices[0].message.content
    }

# ==========================================================
# ASK GPT DIRECTLY
# ==========================================================

@app.get("/ask")
def ask(question: str):

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return {
        "answer": response.choices[0].message.content
    }

# ==========================================================
# TEST EMBEDDINGS
# ==========================================================

@app.get("/test-embedding")
def test_embedding():

    response = client.embeddings.create(
        model="openai/text-embedding-3-small",
        input="What is our refund policy?"
    )

    embedding = response.data[0].embedding

    return {
        "dimensions": len(embedding),
        "first_5_values": embedding[:5]
    }

# ==========================================================
# LOAD DOCUMENT INTO VECTOR DATABASE
# ==========================================================

@app.get("/load-docs")
def load_docs():

    with open(
        "documents/company_policy.txt",
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()

    embedding_response = client.embeddings.create(
        model="openai/text-embedding-3-small",
        input=text
    )

    embedding = embedding_response.data[0].embedding

    try:
        collection.delete(ids=["policy_1"])
    except:
        pass

    collection.add(
        ids=["policy_1"],
        documents=[text],
        embeddings=[embedding]
    )

    return {
        "message": "Document loaded into ChromaDB"
    }

# ==========================================================
# DISPLAY ALL DOCUMENTS
# ==========================================================

@app.get("/all-docs")
def all_docs():

    return collection.get()

# ==========================================================
# VECTOR SEARCH
# ==========================================================

@app.get("/search")
def search(query: str):

    query_embedding = client.embeddings.create(
        model="openai/text-embedding-3-small",
        input=query
    )

    results = collection.query(
        query_embeddings=[
            query_embedding.data[0].embedding
        ],
        n_results=1
    )

    return results

@app.get("/agent")
def agent(question: str):

    company_keywords = [
        "refund",
        "support",
        "employee",
        "remote",
        "policy"
    ]

    use_rag = any(
        keyword in question.lower()
        for keyword in company_keywords
    )

    # Use RAG
    if use_rag:

        query_embedding = client.embeddings.create(
            model="openai/text-embedding-3-small",
            input=question
        )

        results = collection.query(
            query_embeddings=[
                query_embedding.data[0].embedding
            ],
            n_results=1
        )

        if (
            not results["documents"]
            or not results["documents"][0]
        ):
            return {
                "error": "No documents found"
            }

        context = results["documents"][0][0]

        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"Answer only from this context:\n\n{context}"
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        return {
            "agent_decision": "RAG",
            "answer": response.choices[0].message.content
        }

    # Use GPT directly
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return {
        "agent_decision": "GPT",
        "answer": response.choices[0].message.content
    }

@app.get("/evaluate")
def evaluate():

    return [
        {
            "question": "How do I get technical support?",
            "expected": "support@company.com",
            "status": "manual test passed"
        },
        {
            "question": "What is the refund policy?",
            "expected": "30 days",
            "status": "manual test passed"
        }
    ]

# ==========================================================
# RAG (Retrieval Augmented Generation)
# ==========================================================
#
# Question
#    ↓
# Embedding
