from fastapi import APIRouter, File, UploadFile
import shutil
from typing import BinaryIO

from app.services.pdf_service import extract_text, chunk_text
from app.services.embedding_service import get_embeddings
from app.services.faiss_service import create_faiss_index, stored_chunks, set_faiss_index

router = APIRouter()

@router.post("/upload")
def upload_file(file: UploadFile = File(...)):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer: # type: BinaryIO
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(file_path)
    chunks = chunk_text(text)
    embeddings = get_embeddings(chunks)
    index = create_faiss_index(embeddings)
    # Store Globally
    set_faiss_index(index, chunks)

    return {
        "filename": file.filename,
        "num_chunks": len(chunks)
    }