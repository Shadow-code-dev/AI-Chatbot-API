from fastapi import APIRouter, Body, HTTPException

from app.services.faiss_service import search_similar_chunks, get_faiss_index
from app.services.embedding_service import generate_answer

router = APIRouter()

@router.post("/ask")
def ask_question(question: str = Body(...)):
    if get_faiss_index() is None:
        raise HTTPException(status_code=404, detail="No document uploaded yet")

    relevant_chunks = search_similar_chunks(question)
    # Combine chunks into context
    context = " ".join(relevant_chunks)
    # Generate answer
    answer = generate_answer(context, question)

    return {
        "question": question,
        "answer": answer
    }