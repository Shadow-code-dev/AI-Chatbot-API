from fastapi import APIRouter, File, UploadFile, Depends
import shutil
from typing import BinaryIO

from app.services.pdf_service import extract_text, chunk_text
from app.services.embedding_service import get_embeddings
from app.services.faiss_service import create_faiss_index, stored_chunks, set_faiss_index
from app.services.auth_service import get_current_user

from app.db.database import SessionLocal
from app.db.models import Document

router = APIRouter()

@router.post("/upload")
def upload_file(file: UploadFile = File(...), user = Depends(get_current_user)):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer: # type: BinaryIO
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(file_path)
    chunks = chunk_text(text)
    embeddings = get_embeddings(chunks)
    index = create_faiss_index(embeddings)
    # Store Globally
    set_faiss_index(index, chunks)

    # Database Logic
    db = SessionLocal()

    try:
        docs = Document(
            filename = file.filename,
            content=text
        )

        db.add(docs)
        db.commit()
    finally:
        db.close()

    return {
        "filename": file.filename,
        "num_chunks": len(chunks)
    }