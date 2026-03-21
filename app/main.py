from fastapi import FastAPI
from app.routes import upload, chat

app = FastAPI()

app.include_router(upload.router)
app.include_router(chat.router)

@app.get("/")
def home():
    return {"message": "AI Chatbot API Running!"}