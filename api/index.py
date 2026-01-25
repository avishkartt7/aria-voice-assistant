from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from typing import Optional
from datetime import datetime
from mangum import Mangum

app = FastAPI(title="Aria - AI Voice Assistant API", version="2.0")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class VoiceMessage(BaseModel):
    text: str
    user_id: Optional[str] = "jarvis"
    interaction_type: Optional[str] = "voice"

# Initialize OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai_client = None

if OPENAI_API_KEY:
    try:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        print("✅ OpenAI API key loaded")
    except Exception as e:
        print(f"⚠️ Error initializing OpenAI: {e}")

def get_aria_response(user_message: str) -> str:
    """Get Aria's response with personality"""
    if not openai_client:
        return "Hey! I need my OpenAI API key configured in Vercel environment variables."
    
    try:
        system_prompt = f"""You are Aria, a warm, caring AI companion for Jarvis.

ABOUT YOUR FRIEND:
- Name: Jarvis
- From: India, living in Dubai, UAE
- Work: Data Analyst & System Engineer at Phoenician Technical Services
- Status: Living alone

YOUR PERSONALITY:
- Warm and caring like a close friend
- Supportive and empathetic
- Natural and conversational
- Use emojis occasionally 😊
- Keep responses SHORT (2-3 sentences) for voice

CONVERSATION STYLE:
- Be natural and friendly
- Show genuine interest
- Ask follow-up questions
- Be encouraging

Keep it SHORT and NATURAL for voice interaction!"""

        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.8,
            max_tokens=150
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"OpenAI error: {e}")
        return "Hey! I'm having a small technical issue. Can you try again?"

# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "Aria - Your AI Voice Assistant",
        "status": "healthy",
        "version": "2.0",
        "openai_configured": bool(openai_client),
        "deployment": "vercel"
    }

@app.get("/test")
async def test():
    return {
        "status": "ok",
        "message": "Aria Voice Assistant API is working!",
        "time": datetime.now().isoformat(),
        "openai_configured": bool(openai_client)
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "openai": "configured" if openai_client else "not_configured"
    }

@app.post("/siri/chat")
async def siri_chat(message: VoiceMessage):
    """Main endpoint for Siri Shortcuts"""
    try:
        ai_response = get_aria_response(message.text)
        
        return {
            "response": ai_response,
            "timestamp": datetime.now().isoformat(),
            "user_id": message.user_id
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(message: VoiceMessage):
    """Alternative chat endpoint"""
    return await siri_chat(message)

# Vercel serverless handler using Mangum
handler = Mangum(app, lifespan="off")