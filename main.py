from fastapi import FastAPI, File, UploadFile
import shutil
from typing import BinaryIO
from pypdf import PdfReader

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

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Ai Chatbot API is running"}

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer: # type: BinaryIO
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(file_path)

    chunks = chunk_text(text)

    return {"filename": file.filename,
            "num_chunks": len(chunks),
            "sample_chunks": chunks[0] if chunks else ""
            }