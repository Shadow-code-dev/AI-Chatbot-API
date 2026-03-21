from fastapi import FastAPI
from app.routes import upload, chat
import app.config
# from dotenv import load_dotenv
# from pathlib import Path
# import os
#
# BASE_DIR = Path(__file__).resolve().parent.parent
# env_path = BASE_DIR / ".env"
#
# # Load env variables
# load_dotenv(dotenv_path=env_path)
#
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.include_router(upload.router)
app.include_router(chat.router)

@app.get("/")
def home():
    return {"message": "AI Chatbot API Running!"}