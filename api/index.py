from http.server import BaseHTTPRequestHandler
import json
import os
from datetime import datetime
import random
from datetime import datetime, timezone, timedelta
import pytz  # You'll need to add this package
class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        # **NEW: Auto-talk endpoint**
        if self.path == '/auto-talk':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            current_time = datetime.now()
            hour = current_time.hour
            minute = current_time.minute
            
            message = self.get_scheduled_message(hour, minute)
            
            response = {
                "time": f"{hour:02d}:{minute:02d}",
                "message": message,
                "hour": hour,
                "minute": minute
            }
            
            self.wfile.write(json.dumps(response).encode())
            return
        
        # Keep existing endpoints
        if self.path == '/' or self.path == '/test':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "status": "ok",
                "message": "Jarvis Auto-Talk Ready!",
                "endpoints": {
                    "chat": "/siri/chat",
                    "auto_talk": "/auto-talk"
                }
            }   
            
            self.wfile.write(json.dumps(response).encode())
            return
        
        self.send_response(404)
        self.end_headers()
    
    def get_scheduled_message(self, hour, minute):
        """Your schedule - NOW WITH TIMEZONE SUPPORT"""
        
        # Set your timezone (Asia/Kolkata = India)
        india_tz = pytz.timezone('Asia/Kolkata')
        india_time = datetime.now(india_tz)
        hour = india_time.hour
        minute = india_time.minute
        
        # Your schedule in IST (India Time)
        # 12:00 PM IST - LUNCH TIME
        if hour == 12 and minute == 0:
            return "🍽️ Lunch Time! It's 12 PM. Take a break and eat properly..."
        
        # 12:30 PM IST - LUNCH CHECK
        if hour == 12 and minute == 30:
            return "How's your lunch going? Take at least 30 minutes..."
        
        # 1:00 PM IST - BACK FROM LUNCH
        if hour == 13 and minute == 0:
            return "Back to work! First hour begins now..."
        
        # 2:00 PM IST - 1st BREAK
        if hour == 14 and minute == 0:
            return "⏰ Break Time! You've worked 1 hour..."
        
        # 3:00 PM IST - 2nd BREAK  
        if hour == 15 and minute == 0:
            return "⏰ Break Time! 2 hours done..."
        
        # 4:00 PM IST - PROTEIN TIME
        if hour == 16 and minute == 0:
            return "💪 PROTEIN TIME! It's 4 PM. Protein shake?"
        
        # 4:30 PM IST - PROTEIN REMINDER
        if hour == 16 and minute == 30:
            return "Reminder: Don't skip protein!"
        
        # 5:00 PM IST - LOGOUT TIME
        if hour == 17 and minute == 0:
            return "🏠 LOGOUT TIME! It's 5 PM..."
        
        # 5:30 PM IST - GO HOME
        if hour == 17 and minute == 30:
            return "You should be leaving office now!"
        
        # 6:00 PM IST - GYM TIME
        if hour == 18 and minute == 0:
            return "🏋️ GYM TIME! It's 6 PM..."
        
        # 6:30 PM IST - GYM CHECK
        if hour == 18 and minute == 30:
            return "Are you at the gym?"
        
        # 9:00 PM IST - EVENING CHECK
        if hour == 21 and minute == 0:
            return "Evening check! Plan tomorrow..."
        
        return f"Jarvis check at {hour:02d}:{minute:02d} IST. Next scheduled message coming up!"
    
    # KEEP YOUR EXISTING do_POST METHOD (for chat)
    def do_POST(self):
        if self.path == '/siri/chat' or self.path == '/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            try:
                data = json.loads(body)
                text = data.get('text', '').lower()
                user_id = data.get('user_id', 'jarvis')
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                # Intelligent responses
                if "hello" in text or "hi" in text or "jarvis" in text:
                    response_text = "Hello! Jarvis here. I'm managing your daily schedule."
                elif "time" in text:
                    current = datetime.now().strftime("%I:%M %p")
                    response_text = f"Current time is {current}"
                elif "schedule" in text:
                    response_text = "Your schedule: Lunch 12PM, Breaks 2PM & 3PM, Protein 4PM, Logout 5PM, Gym 6PM"
                else:
                    response_text = f"Jarvis: I'll help with your schedule. For auto-reminders, check /auto-talk"
                
                response = {
                    "response": response_text,
                    "user_id": user_id
                }
                
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return
        
        self.send_response(404)
        self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()