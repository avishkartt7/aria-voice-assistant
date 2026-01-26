from http.server import BaseHTTPRequestHandler
import json
import os
from datetime import datetime
import random

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
        """Your exact schedule"""
        
        # 12:00 PM - LUNCH TIME
        if hour == 12 and minute == 0:
            return "🚨 Lunch Time! It's 12 PM. Take a break and eat properly. Remember to hydrate!"
        
        # 12:30 PM - LUNCH CHECK
        if hour == 12 and minute == 30:
            return "How's your lunch going? You should take at least 30 minutes break from work."
        
        # 1:00 PM - BACK FROM LUNCH
        if hour == 13 and minute == 0:
            return "Back to work! First hour begins now. I'll remind you to take breaks."
        
        # 2:00 PM - 1st BREAK REMINDER
        if hour == 14 and minute == 0:
            return "⏰ Break Time! You've worked 1 hour. Take 5 minutes - stretch or walk around."
        
        # 3:00 PM - 2nd BREAK REMINDER  
        if hour == 15 and minute == 0:
            return "⏰ Break Time! 2 hours done. Look away from screen for 5 minutes."
        
        # 4:00 PM - PROTEIN TIME
        if hour == 16 and minute == 0:
            return "💪 PROTEIN TIME! It's 4 PM. Have you taken your protein shake? Should I set alarm for 5 PM if not?"
        
        # 4:30 PM - PROTEIN REMINDER
        if hour == 16 and minute == 30:
            return "Reminder: Don't skip protein! Good for muscle recovery."
        
        # 5:00 PM - LOGOUT TIME
        if hour == 17 and minute == 0:
            return "🏠 LOGOUT TIME! It's 5 PM. Start wrapping up your work."
        
        # 5:30 PM - GO HOME TIME
        if hour == 17 and minute == 30:
            return "You should be leaving office now! Go home and prepare for gym."
        
        # 6:00 PM - GYM TIME
        if hour == 18 and minute == 0:
            return "🏋️ GYM TIME! It's 6 PM. Time to hit the gym! Don't skip workout."
        
        # 6:30 PM - GYM CHECK
        if hour == 18 and minute == 30:
            return "Are you at the gym? Complete your workout properly!"
        
        # 9:00 PM - EVENING CHECK
        if hour == 21 and minute == 0:
            return "Evening check! Plan tomorrow and get good sleep."
        
        # Default message for testing
        return f"Jarvis check at {hour:02d}:{minute:02d}. Your next scheduled message is coming up!"
    
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