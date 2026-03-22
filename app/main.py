from fastapi import FastAPI
from app.routes import upload, chat
import app.config

fastapi_app = FastAPI()

fastapi_app.include_router(upload.router)
fastapi_app.include_router(chat.router)

@fastapi_app.get("/")
def home():
    return {"message": "AI Chatbot API Running!"}