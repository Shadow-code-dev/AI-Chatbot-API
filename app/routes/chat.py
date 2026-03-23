from fastapi import APIRouter, Body, HTTPException, Depends

from app.services.faiss_service import search_similar_chunks, get_faiss_index
from app.services.embedding_service import generate_answer
from app.services.auth_service import get_current_user

from app.db.database import SessionLocal
from app.db.models import Chat

router = APIRouter()

@router.post("/ask")
def ask_question(question: str = Body(...), user = Depends(get_current_user)):
    if get_faiss_index() is None:
        raise HTTPException(status_code=404, detail="No document uploaded yet")

    relevant_chunks = search_similar_chunks(question)
    # Combine chunks into context
    context = " ".join(relevant_chunks)
    # Generate answer
    answer = generate_answer(context, question)

    # Database Logic
    db = SessionLocal()

    try:
        chat = Chat(
            question=question,
            answer=answer
        )

        db.add(chat)
        db.commit()
    finally:
        db.close()

    return {
        "question": question,
        "answer": answer
    }