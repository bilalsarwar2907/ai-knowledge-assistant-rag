from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
import os
from pypdf import PdfReader
from rich import text
from jose import jwt
from jose import JWTError
from datetime import datetime, timedelta

SECRET_KEY = "my-super-secret-key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

conversation_history = []

# ==========================================================
# OPENROUTER CLIENT
# ==========================================================

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def extract_pdf_text(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text

def chunk_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks

# ==========================================================
# CHROMADB
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

chroma_client = chromadb.PersistentClient(
    path=os.path.join(BASE_DIR, "chroma_db")
)

collection = chroma_client.get_or_create_collection(
    name="company_docs"
)

@app.get("/login")
def login():

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    token = jwt.encode(
        {
            "sub": "bilal",
            "exp": expire
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token
    }

@app.get("/protected")
def protected(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return {
            "message": "Access granted",
            "user": payload["sub"]
        }

    except JWTError:

        return {
            "message": "Invalid token"
        }

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

    conversation_history.append(
        {
            "role": "user",
            "content": question
        }
    )

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=conversation_history
    )

    conversation_history.append(
        {
            "role": "assistant",
            "content": response.choices[0].message.content
        }
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

@app.get("/count")
def count_docs():

    return {
        "count": collection.count()
    }


@app.get("/load-pdfs")
def load_pdfs():

    pdf_files = [
        f for f in os.listdir("documents")
        if f.endswith(".pdf")
    ]

    count = 0

    for pdf in pdf_files:

        file_path = os.path.join("documents", pdf)

        text = extract_pdf_text(file_path)

        chunks = chunk_text(text)

        for index, chunk in enumerate(chunks):

            embedding_response = client.embeddings.create(
                model="openai/text-embedding-3-small",
                input=chunk
            )

            embedding = embedding_response.data[0].embedding

            collection.add(
                ids=[f"{pdf}_{index}"],
                documents=[chunk],
                embeddings=[embedding]
            )

            count += 1

    return {
        "loaded_chunks": count
    }

@app.get("/ask-rag")
def ask_rag(question: str):

    embedding_response = client.embeddings.create(
        model="openai/text-embedding-3-small",
        input=question
    )

    question_embedding = embedding_response.data[0].embedding

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=1
    )

    context = results["documents"][0][0]

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"Answer only using this context:\n\n{context}"
            },
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
# RAG (Retrieval Augmented Generation)
# ==========================================================
#
# Question
#    ↓
# Embedding
