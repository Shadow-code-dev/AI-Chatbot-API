from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Ai Chatbot API is running"}