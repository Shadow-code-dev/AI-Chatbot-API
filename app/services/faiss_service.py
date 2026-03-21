import faiss
import numpy as np

faiss_index = None
stored_chunks = []

def create_faiss_index(embeddings: list):
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype(np.float32))
    return index

def set_faiss_index(index, chunks):
    global faiss_index, stored_chunks
    faiss_index = index
    stored_chunks = chunks

def get_faiss_index():
    return faiss_index

def search_similar_chunks(query: str, k: int = 3) -> list:
    from app.services.embedding_service import get_embeddings

    # Converting query -> embedding
    query_embedding = get_embeddings([query])[0]

    # Search in FAISS
    distances, indices = faiss_index.search(
        np.array([query_embedding]).astype(np.float32),
        k
    )

    # Get relevant chunks
    results = [stored_chunks[i] for i in indices[0]]

    return results