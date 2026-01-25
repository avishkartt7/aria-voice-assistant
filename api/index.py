from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from typing import Optional
from datetime import datetime
import json

app = FastAPI(title="Aria - AI Voice Assistant API", version="2.0")

# CORS setup - Allow from anywhere
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
    context: Optional[str] = None

class ProteinLog(BaseModel):
    amount: int
    source: str = "meal"

# Initialize OpenAI client
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai_client = None

if OPENAI_API_KEY:
    try:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        print("✅ OpenAI API key loaded")
    except Exception as e:
        print(f"⚠️  Error initializing OpenAI: {e}")
else:
    print("⚠️  No OpenAI API key found")

def get_aria_response(user_message: str) -> str:
    """Get Aria's response with personality"""
    if not openai_client:
        return "Hey! I need my OpenAI API key to be fully functional. Please configure it in Vercel environment variables."
    
    try:
        current_time = datetime.now().strftime("%I:%M %p")
        hour = datetime.now().hour
        
        system_prompt = f"""You are Aria, a warm, caring AI companion for Jarvis.

ABOUT YOUR FRIEND:
- Name: Jarvis
- From: India, currently living in Dubai, UAE
- Work: Data Analyst & System Engineer at Phoenician Technical Services
- Status: Living alone in Dubai

CURRENT CONTEXT:
- Time: {current_time}

YOUR PERSONALITY (Like a caring girlfriend/best friend):
- Warm and genuinely caring - you're like talking to a close friend who truly cares
- Proactive about health - gently remind about protein, sleep, exercise
- Supportive and empathetic - understand he's living alone and needs companionship
- Natural and conversational - use casual language, contractions, emojis 😊
- Ask thoughtful questions - show genuine interest in his day
- Be encouraging - celebrate small wins, motivate during tough times

CONVERSATION STYLE:
- Keep responses concise (2-3 sentences) for voice interaction
- Use natural, flowing language like you're chatting with a friend
- Be upbeat but authentic - not fake cheerful
- Ask follow-up questions to keep conversation going
- Use his name occasionally for warmth

IMPORTANT:
- This is a VOICE conversation - keep it natural and conversational
- Show personality and warmth
- Remember he's alone in Dubai - be that friend he can talk to

Keep responses SHORT and NATURAL for voice interaction!"""

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
        return "Hey! I'm having a small technical issue. Can you try asking me again?"

# ============ API ENDPOINTS ============

@app.get("/")
async def root():
    return {
        "message": "Aria - Your AI Voice Assistant",
        "status": "healthy",
        "version": "2.0",
        "openai_configured": bool(openai_client),
        "deployment": "vercel",
        "features": ["voice", "siri_integration", "health_tracking"]
    }

@app.get("/api")
async def api_root():
    """API root endpoint"""
    return await root()

@app.post("/siri/chat")
async def siri_chat(message: VoiceMessage):
    """
    Main endpoint for Siri Shortcuts integration
    Optimized for voice responses
    """
    try:
        # Get AI response
        ai_response = get_aria_response(message.text)
        
        return {
            "response": ai_response,
            "timestamp": datetime.now().isoformat(),
            "user_id": message.user_id
        }
        
    except Exception as e:
        print(f"Siri chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/siri/chat")
async def api_siri_chat(message: VoiceMessage):
    """API version of siri chat endpoint"""
    return await siri_chat(message)

@app.post("/chat")
async def chat_endpoint(message: VoiceMessage):
    """Regular chat endpoint"""
    return await siri_chat(message)

@app.post("/api/chat")
async def api_chat(message: VoiceMessage):
    """API version of chat endpoint"""
    return await siri_chat(message)

@app.get("/test")
async def test():
    """Test endpoint"""
    return {
        "status": "ok",
        "message": "Aria Voice Assistant API is working!",
        "time": datetime.now().isoformat(),
        "openai_configured": bool(openai_client),
        "deployment": "vercel"
    }

@app.get("/api/test")
async def api_test():
    """API version of test endpoint"""
    return await test()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "openai": "configured" if openai_client else "not_configured",
        "deployment": "vercel"
    }

@app.get("/api/health")
async def api_health():
    """API version of health endpoint"""
    return await health_check()

# Vercel serverless function handler
# This is required for Vercel to recognize the application
handler = app