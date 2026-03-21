from openai import OpenAI
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embeddings(texts: list) -> list:
    # Clean text
    cleaned_texts = [t.strip().replace("\n", " ") for t in texts if t.strip()]

    if not cleaned_texts:
        return []

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=cleaned_texts
    )
    embeddings = []

    for item in response.data:
        embeddings.append(item.embedding)

    return embeddings


# Answer Generation Function
def generate_answer(context: str, question: str):
    context = context.strip()

    if not context:
        return "I don't know"

    prompt = f"""
    Answer the question based ONLY on the context below.
    If the answer is not in the context, say "I don't know".

    Context:
    {context}

    Question:
    {question}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content