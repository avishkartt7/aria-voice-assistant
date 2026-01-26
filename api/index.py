from http.server import BaseHTTPRequestHandler
import json
import os
from datetime import datetime
import random
import pytz

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        # Root endpoint
        if self.path == '/' or self.path == '/test':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "status": "ok",
                "message": "Jarvis Voice Assistant - UAE Timezone Ready!",
                "timezone": "Asia/Dubai (GMT+4)",
                "endpoints": {
                    "chat": "/siri/chat (POST)",
                    "auto_talk": "/auto-talk (GET)"
                },
                "schedule": {
                    "lunch": "12:00 PM UAE",
                    "break_1": "2:00 PM UAE",
                    "server_check": "2:30 PM UAE",
                    "break_2": "3:00 PM UAE",
                    "protein": "4:00 PM UAE",
                    "logout": "5:00 PM UAE",
                    "gym": "6:00 PM UAE"
                }
            }
            
            self.wfile.write(json.dumps(response).encode())
            return
        
        # Auto-talk endpoint (GET) - UAE timezone
        if self.path == '/auto-talk':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Get UAE/Dubai time (GMT+4)
            uae_tz = pytz.timezone('Asia/Dubai')
            uae_time = datetime.now(uae_tz)
            hour = uae_time.hour
            minute = uae_time.minute
            current_time_str = uae_time.strftime("%I:%M %p")
            
            # Get server status
            server_status = self.check_server_status()
            
            message = self.get_scheduled_message(hour, minute, server_status)
            
            response = {
                "time": f"{hour:02d}:{minute:02d}",
                "time_12hr": current_time_str,
                "message": message,
                "hour": hour,
                "minute": minute,
                "timezone": "Asia/Dubai",
                "utc_offset": "+04:00",
                "server_check": {
                    "github": server_status.get("github", "unknown"),
                    "vercel": server_status.get("vercel", "unknown"),
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            self.wfile.write(json.dumps(response).encode())
            return
        
        # 404 for other paths
        self.send_response(404)
        self.end_headers()
    
    def check_server_status(self):
        """Check if servers are responding"""
        import urllib.request
        import ssl
        
        status = {}
        
        # Check GitHub
        try:
            req = urllib.request.Request(
                'https://api.github.com',
                headers={'User-Agent': 'Jarvis-Assistant'}
            )
            urllib.request.urlopen(req, timeout=3)
            status["github"] = "✅ Online"
        except:
            status["github"] = "❌ Offline"
        
        # Check Vercel (your own server)
        try:
            req = urllib.request.Request(
                'https://aria-voice-assistant.vercel.app/',
                headers={'User-Agent': 'Jarvis-Assistant'}
            )
            urllib.request.urlopen(req, timeout=3)
            status["vercel"] = "✅ Online"
        except:
            status["vercel"] = "❌ Offline"
        
        return status
    
    def get_scheduled_message(self, hour, minute, server_status=None):
        """Generate messages based on UAE timezone schedule"""
        
        # 12:00 PM UAE - LUNCH TIME
        if hour == 12 and minute == 0:
            return "🍽️ LUNCH TIME! It's 12:00 PM Dubai time. Take a proper break and eat your meal. Don't forget to drink water!"
        
        # 12:30 PM UAE - LUNCH CHECK
        elif hour == 12 and minute == 30:
            return "How's your lunch going? You should take at least 30 minutes away from work. Relax and enjoy your food!"
        
        # 1:00 PM UAE - BACK FROM LUNCH
        elif hour == 13 and minute == 0:
            return "Back to work! First work hour begins now at 1:00 PM UAE time. I'll remind you to take breaks."
        
        # 2:00 PM UAE - 1st BREAK REMINDER
        elif hour == 14 and minute == 0:
            return "⏰ BREAK TIME! You've worked 1 hour. Take 5 minutes - stretch your legs, look away from screen, or walk around."
        
        # 2:30 PM UAE - SERVER CHECK + BREAK REMINDER ⭐ NEW!
        elif hour == 14 and minute == 30:
            server_msg = ""
            if server_status:
                github_status = server_status.get("github", "❓")
                vercel_status = server_status.get("vercel", "❓")
                server_msg = f" Server status: GitHub {github_status}, Vercel {vercel_status}."
            
            messages = [
                f"🔧 2:30 PM UAE - Server check complete.{server_msg} Have you taken your break yet? If not, stand up and walk for 2 minutes!",
                f"⏰ 2:30 PM UAE - Break check!{server_msg} Did you take your 5-minute break? Time to drink some water! 💧",
                f"✅ 2:30 PM UAE - Systems check.{server_msg} Remember: Micro-breaks improve productivity! Look away from screen for 60 seconds."
            ]
            return random.choice(messages)
        
        # 3:00 PM UAE - 2nd BREAK REMINDER
        elif hour == 15 and minute == 0:
            return "⏰ BREAK TIME! 2 hours done. Quick 5-minute eye break. Look at something 20 feet away for 20 seconds!"
        
        # 4:00 PM UAE - PROTEIN TIME
        elif hour == 16 and minute == 0:
            return "💪 PROTEIN TIME! It's 4:00 PM UAE. Have you taken your protein shake? Important for muscle recovery!"
        
        # 4:30 PM UAE - PROTEIN REMINDER
        elif hour == 16 and minute == 30:
            return "Protein reminder at 4:30 PM UAE! Don't skip it. Should I set an alarm for 5:00 PM if you haven't taken it yet?"
        
        # 5:00 PM UAE - LOGOUT TIME
        elif hour == 17 and minute == 0:
            return "🏠 LOGOUT TIME! It's 5:00 PM UAE. Start wrapping up your work. Begin closing tabs and saving files."
        
        # 5:30 PM UAE - GO HOME TIME
        elif hour == 17 and minute == 30:
            return "You should be leaving office now! 5:30 PM UAE time. Go home and prepare for gym. Don't forget your stuff!"
        
        # 6:00 PM UAE - GYM TIME
        elif hour == 18 and minute == 0:
            return "🏋️ GYM TIME! It's 6:00 PM UAE. Time to hit the gym! Don't skip workout. Remember to warm up properly."
        
        # 6:30 PM UAE - GYM CHECK
        elif hour == 18 and minute == 30:
            return "Are you at the gym yet? 6:30 PM UAE. Complete your workout properly! Need your workout playlist?"
        
        # 9:00 PM UAE - EVENING CHECK
        elif hour == 21 and minute == 0:
            return "Evening check at 9:00 PM UAE! Review your day, plan for tomorrow, and get good sleep. Need me to set morning alarms?"
        
        # Morning greetings (7 AM - 11 AM)
        elif 7 <= hour <= 11 and minute == 0:
            greetings = [
                f"Good morning! It's {hour}:00 AM UAE time. Your first scheduled message is at 12:00 PM for lunch.",
                f"Morning check at {hour}:00 AM UAE. Your schedule starts at 12:00 PM.",
                f"Jarvis here! {hour}:00 AM UAE. Reminders begin at lunch time 12:00 PM."
            ]
            return random.choice(greetings)
        
        # Default message for other times
        else:
            # Calculate next scheduled time
            next_times = [
                (12, 0, "12:00 PM - Lunch"),
                (12, 30, "12:30 PM - Lunch Check"),
                (13, 0, "1:00 PM - Back to Work"),
                (14, 0, "2:00 PM - 1st Break"),
                (14, 30, "2:30 PM - Server Check"),  # ⭐ NEW!
                (15, 0, "3:00 PM - 2nd Break"),
                (16, 0, "4:00 PM - Protein Time"),
                (16, 30, "4:30 PM - Protein Reminder"),
                (17, 0, "5:00 PM - Logout"),
                (17, 30, "5:30 PM - Go Home"),
                (18, 0, "6:00 PM - Gym"),
                (18, 30, "6:30 PM - Gym Check"),
                (21, 0, "9:00 PM - Evening Check")
            ]
            
            # Find next scheduled time
            for h, m, desc in next_times:
                if (hour < h) or (hour == h and minute < m):
                    time_str = f"{h}:{m:02d}"
                    am_pm = "AM" if h < 12 else "PM"
                    if h > 12:
                        time_str = f"{h-12}:{m:02d}"
                    return f"✅ Jarvis active at {hour:02d}:{minute:02d} UAE. Next: {time_str} {am_pm} ({desc.split('-')[1].strip()})"
            
            # If past all schedules
            return f"✅ Jarvis check at {hour:02d}:{minute:02d} UAE. All scheduled messages completed for today. Next reminders tomorrow!"
    
    def do_POST(self):
        # Chat endpoint (POST)
        if self.path == '/siri/chat' or self.path == '/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            try:
                data = json.loads(body)
                text = data.get('text', '').lower()
                user_id = data.get('user_id', 'jarvis')
                
                # Get UAE time for context
                uae_tz = pytz.timezone('Asia/Dubai')
                uae_time = datetime.now(uae_tz)
                hour = uae_time.hour
                minute = uae_time.minute
                current_time = uae_time.strftime("%I:%M %p")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                # Generate response based on input
                response_text = self.generate_chat_response(text, hour, minute, current_time)
                
                response = {
                    "response": response_text,
                    "user_id": user_id,
                    "uae_time": current_time,
                    "timezone": "Asia/Dubai"
                }
                
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return
        
        # 404 for other paths
        self.send_response(404)
        self.end_headers()
    
    def generate_chat_response(self, text, hour, minute, current_time):
        """Generate intelligent chat responses with UAE time context"""
        
        # Server check command
        if any(word in text for word in ["server", "status", "check server", "github", "vercel"]):
            status = self.check_server_status()
            github = status.get("github", "❓")
            vercel = status.get("vercel", "❓")
            return f"Server status at {current_time} UAE: GitHub {github}, Vercel {vercel}. All systems operational!"
        
        # Greetings
        if any(word in text for word in ["hello", "hi", "hey", "jarvis"]):
            greetings = [
                f"Hello! Jarvis here. Current UAE time is {current_time}.",
                f"Hi! I'm Jarvis. It's {current_time} in Dubai.",
                f"Hey! Jarvis at your service. The time is {current_time} UAE."
            ]
            return random.choice(greetings)
        
        # Time queries
        elif any(word in text for word in ["time", "clock", "what time"]):
            next_sched = self.get_next_schedule(hour, minute)
            return f"Current UAE (Dubai) time is {current_time}. Your next scheduled message is at {next_sched}."
        
        # Schedule queries
        elif any(word in text for word in ["schedule", "reminder", "today plan", "agenda"]):
            return "Your UAE schedule: Lunch 12:00 PM, Breaks 2:00 PM & 3:00 PM, Server Check 2:30 PM, Protein 4:00 PM, Logout 5:00 PM, Gym 6:00 PM, Evening 9:00 PM"
        
        # Next reminder
        elif any(word in text for word in ["next", "when", "upcoming"]):
            next_sched = self.get_next_schedule(hour, minute)
            return f"Next reminder at {next_sched} UAE time."
        
        # Help
        elif any(word in text for word in ["help", "what can you do", "feature"]):
            return "I'm Jarvis! I manage your daily schedule in UAE time, give reminders for lunch, breaks, server checks, protein, gym, and more. Try asking 'server status' or 'what's my schedule?'"
        
        # Default response
        else:
            responses = [
                f"I heard: '{text}'. It's {current_time} UAE. How can I help with your schedule?",
                f"At {current_time} UAE: '{text}'. Need help with your daily reminders?",
                f"Jarvis here! {current_time} UAE. Regarding '{text}', would you like to check your next schedule?"
            ]
            return random.choice(responses)
    
    def get_next_schedule(self, current_hour, current_minute):
        """Get next scheduled time as string"""
        schedules = [
            (12, 0, "12:00 PM"),
            (12, 30, "12:30 PM"),
            (13, 0, "1:00 PM"),
            (14, 0, "2:00 PM"),
            (14, 30, "2:30 PM"),  # ⭐ NEW!
            (15, 0, "3:00 PM"),
            (16, 0, "4:00 PM"),
            (16, 30, "4:30 PM"),
            (17, 0, "5:00 PM"),
            (17, 30, "5:30 PM"),
            (18, 0, "6:00 PM"),
            (18, 30, "6:30 PM"),
            (21, 0, "9:00 PM")
        ]
        
        for h, m, desc in schedules:
            if (current_hour < h) or (current_hour == h and current_minute < m):
                return desc
        
        return "tomorrow 12:00 PM"
    
    def do_OPTIONS(self):
        # CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()