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

    return {"filename": file.filename,
            "text_preview": text[:500] # first 500 chars
            }