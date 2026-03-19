from fastapi import FastAPI, File, UploadFile
import shutil
from typing import BinaryIO
from pypdf import PdfReader
from dotenv import load_dotenv
from openai import OpenAI
import os
import faiss
import numpy as np

stored_chunks = []
faiss_index = None

# Load env variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

def chunk_text(text: str, chunk_size: int = 500):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks

def get_embeddings(texts: list) -> list:
    # Clean text
    cleaned_texts = [t.strip().replace("\n", " ") for t in texts]

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=cleaned_texts
    )
    embeddings = []

    for item in response.data:
        embeddings.append(item.embedding)

    return embeddings

def create_faiss_index(embeddings: list):
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype(np.float32))
    return index

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Ai Chatbot API is running"}

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    global stored_chunks, faiss_index
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer: # type: BinaryIO
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(file_path)
    chunks = chunk_text(text)
    embeddings = get_embeddings(chunks)
    faiss_index = create_faiss_index(embeddings)
    stored_chunks = chunks

    return {"filename": file.filename,
            "num_chunks": len(chunks),
            "embedding_dimension": len(embeddings[0] if embeddings else 0),
            "message": "Embeddings stored in FAISS"
            }