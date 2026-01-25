from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mangum import Mangum
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple model
class Message(BaseModel):
    text: str
    user_id: str = "jarvis"

# Check OpenAI
OPENAI_KEY = os.getenv('OPENAI_API_KEY')

@app.get("/")
def root():
    return {
        "message": "Aria Voice Assistant",
        "status": "healthy",
        "openai_configured": bool(OPENAI_KEY)
    }

@app.get("/test")
def test():
    return {
        "status": "ok",
        "message": "API is working!",
        "openai_configured": bool(OPENAI_KEY)
    }

@app.post("/siri/chat")
def siri_chat(message: Message):
    # Simple response for now
    return {
        "response": f"Hey! I got your message: {message.text}",
        "user_id": message.user_id
    }

@app.post("/chat")
def chat(message: Message):
    return siri_chat(message)

# Vercel handler
handler = Mangum(app)