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
                    "break_2": "3:00 PM UAE",
                    "server_check": "4:30 PM UAE",
                    "protein": "5:00 PM UAE",
                    "logout_gym": "6:00 PM UAE"
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
            status["github"] = "Online"
        except:
            status["github"] = "Offline"
        
        # Check Vercel (your own server)
        try:
            req = urllib.request.Request(
                'https://aria-voice-assistant.vercel.app/',
                headers={'User-Agent': 'Jarvis-Assistant'}
            )
            urllib.request.urlopen(req, timeout=3)
            status["vercel"] = "Online"
        except:
            status["vercel"] = "Offline"
        
        return status
    
    def get_scheduled_message(self, hour, minute, server_status=None):
        """Generate messages based on UAE timezone schedule"""
        
        # 12:00 PM UAE - LUNCH TIME
        if hour == 12 and minute == 0:
            return "Lunch time! It's 12 PM Dubai time. Take a proper break and eat your meal. Don't forget to drink water!"
        
        # 12:30 PM UAE - LUNCH CHECK
        elif hour == 12 and minute == 30:
            return "How's your lunch going? Take at least 30 minutes away from work. Relax and enjoy your food!"
        
        # 1:00 PM UAE - BACK FROM LUNCH
        elif hour == 13 and minute == 0:
            return "Back to work! First work hour begins now at 1 PM UAE time. I'll remind you to take breaks."
        
        # 2:00 PM UAE - 1st BREAK REMINDER
        elif hour == 14 and minute == 0:
            return "Break time! 2 hours done. Quick 5 minute eye break. Look at something 20 feet away for 20 seconds!"
        
        # 3:00 PM UAE - 2nd BREAK REMINDER
        elif hour == 15 and minute == 0:
            return "Break time! 2 hours done. Quick 5 minute eye break. Look at something 20 feet away for 20 seconds!"
        
        # 4:00 PM UAE - AFTERNOON CHECK
        elif hour == 16 and minute == 0:
            return "It's 4 PM UAE. Stay focused! One more hour until protein time. Keep hydrated and take short breaks."
        
        # ⭐ 4:30 PM UAE - SERVER CHECK + HYDRATION
        elif hour == 16 and minute == 30:
            server_msg = ""
            if server_status:
                github_status = server_status.get("github", "Unknown")
                vercel_status = server_status.get("vercel", "Unknown")
                server_msg = f"Server status check: GitHub is {github_status}. Vercel is {vercel_status}."
            
            messages = [
                f"4:30 PM UAE. {server_msg} Time to check your code and stay hydrated! Drink some water now!",
                f"Server check time! {server_msg} Don't forget to drink water. Hydration keeps you sharp!",
                f"4:30 PM check in. {server_msg} Quick reminder: Have you had water recently? Stay hydrated!"
            ]
            return random.choice(messages)
        
        # ⭐ 5:00 PM UAE - PROTEIN TIME
        elif hour == 17 and minute == 0:
            messages = [
                "Protein time! It's 5 PM UAE. Take your protein shake now! Important for muscle recovery. Stay hydrated too!",
                "5 PM protein reminder! Don't skip your shake. Your muscles need it for growth and recovery!",
                "Time for protein! It's 5 PM. Grab your protein shake quickly. Remember to drink water with it!"
            ]
            return random.choice(messages)
        
        # 5:30 PM UAE - PROTEIN CHECK
        elif hour == 17 and minute == 30:
            messages = [
                "Hey! Did you take your protein? I reminded you at 5, just following up. Please let me know, my boy!",
                "Quick check! Did you grab that protein shake? I mentioned it at 5 PM. Just making sure you didn't forget, my boy!",
                "Hey my boy! Just checking in. Did you take your protein? I reminded you 30 minutes ago. Don't skip it!"
            ]
            return random.choice(messages)
        
        # ⭐ 6:00 PM UAE - LOGOUT + GYM REMINDER
        elif hour == 18 and minute == 0:
            messages = [
                "Logout time! It's 6 PM UAE. Time to go home and rest. But don't forget, you have gym today! I want to see that aesthetic body. No excuses!",
                "6 PM! Office time is over. Head home, take some rest, then hit the gym! Remember, consistency builds that aesthetic physique you want!",
                "Logout now! It's 6 PM. Go home, relax a bit, but gym is calling! Don't skip it. Your future aesthetic body depends on today's workout!"
            ]
            return random.choice(messages)
        
        # 6:30 PM UAE - GYM REMINDER
        elif hour == 18 and minute == 30:
            messages = [
                "Gym check! It's 6:30 PM. Are you at the gym yet? Don't skip! Every workout counts for that aesthetic body!",
                "6:30 PM! You should be heading to gym now. No excuses. Push yourself today!",
                "Gym time check! Get moving if you haven't already. Your aesthetic goals need consistency!"
            ]
            return random.choice(messages)
        
        # 7:00 PM UAE - GYM MOTIVATION
        elif hour == 19 and minute == 0:
            return "7 PM! Hope you're crushing your workout. Focus on form, push your limits. That aesthetic body is being built right now!"
        
        # 9:00 PM UAE - EVENING CHECK
        elif hour == 21 and minute == 0:
            return "Evening check at 9 PM UAE! Great job today. Review your day, plan for tomorrow, eat well, and get good sleep for recovery."
        
        # Morning greetings (7 AM - 11 AM)
        elif 7 <= hour <= 11 and minute == 0:
            greetings = [
                f"Good morning! It's {hour} AM UAE time. Your first scheduled reminder is at 12 PM for lunch.",
                f"Morning check at {hour} AM UAE. Stay productive! Schedule starts at 12 PM.",
                f"Jarvis here! {hour} AM UAE. Have a great morning. Reminders begin at lunch time."
            ]
            return random.choice(greetings)
        
        # Default message for other times
        else:
            # Calculate next scheduled time
            next_times = [
                (12, 0, "12:00 PM - Lunch"),
                (12, 30, "12:30 PM - Lunch Check"),
                (13, 0, "1:00 PM - Back to Work"),
                (14, 0, "2:00 PM - Break"),
                (15, 0, "3:00 PM - Break"),
                (16, 0, "4:00 PM - Afternoon"),
                (16, 30, "4:30 PM - Server Check"),
                (17, 0, "5:00 PM - Protein"),
                (17, 30, "5:30 PM - Protein Check"),
                (18, 0, "6:00 PM - Logout & Gym"),
                (18, 30, "6:30 PM - Gym Check"),
                (19, 0, "7:00 PM - Gym Motivation"),
                (21, 0, "9:00 PM - Evening")
            ]
            
            # Find next scheduled time
            for h, m, desc in next_times:
                if (hour < h) or (hour == h and minute < m):
                    time_str = f"{h}:{m:02d}"
                    am_pm = "AM" if h < 12 else "PM"
                    if h > 12:
                        time_str = f"{h-12}:{m:02d}"
                    elif h == 12:
                        time_str = "12:00"
                    return f"Jarvis active at {hour:02d}:{minute:02d} UAE. Next reminder: {desc.split(' - ')[1]} at {time_str} {am_pm}."
            
            # If past all schedules
            return f"Jarvis check at {hour:02d}:{minute:02d} UAE. All reminders completed for today. Rest well! Tomorrow starts fresh."
    
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
            github = status.get("github", "Unknown")
            vercel = status.get("vercel", "Unknown")
            return f"Server status at {current_time} UAE: GitHub is {github}. Vercel is {vercel}. All systems checked!"
        
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
            return f"Current UAE time is {current_time}. Your next reminder is at {next_sched}."
        
        # Schedule queries
        elif any(word in text for word in ["schedule", "reminder", "today plan", "agenda"]):
            return "Your UAE schedule: Lunch 12 PM, Breaks 2 PM and 3 PM, Server Check 4:30 PM, Protein 5 PM, Logout and Gym 6 PM, Evening 9 PM."
        
        # Next reminder
        elif any(word in text for word in ["next", "when", "upcoming"]):
            next_sched = self.get_next_schedule(hour, minute)
            return f"Next reminder at {next_sched} UAE time."
        
        # Help
        elif any(word in text for word in ["help", "what can you do", "feature"]):
            return "I'm Jarvis! I manage your daily schedule in UAE time. I remind you about lunch, breaks, server checks, protein, gym, and more. Try asking 'server status' or 'what's my schedule?'"
        
        # Default response
        else:
            responses = [
                f"I heard: '{text}'. It's {current_time} UAE. How can I help?",
                f"At {current_time} UAE. Need help with your reminders?",
                f"Jarvis here! {current_time} UAE. Would you like to check your schedule?"
            ]
            return random.choice(responses)
    
    def get_next_schedule(self, current_hour, current_minute):
        """Get next scheduled time as string"""
        schedules = [
            (12, 0, "12:00 PM"),
            (12, 30, "12:30 PM"),
            (13, 0, "1:00 PM"),
            (14, 0, "2:00 PM"),
            (15, 0, "3:00 PM"),
            (16, 0, "4:00 PM"),
            (16, 30, "4:30 PM"),
            (17, 0, "5:00 PM"),
            (17, 30, "5:30 PM"),
            (18, 0, "6:00 PM"),
            (18, 30, "6:30 PM"),
            (19, 0, "7:00 PM"),
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