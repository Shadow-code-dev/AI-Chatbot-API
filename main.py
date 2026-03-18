from fastapi import FastAPI, File, UploadFile
import shutil
from typing import BinaryIO

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Ai Chatbot API is running"}

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer: # type: BinaryIO
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename}