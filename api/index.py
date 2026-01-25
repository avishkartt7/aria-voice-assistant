from http.server import BaseHTTPRequestHandler
import json
import os

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
                "message": "Aria Voice Assistant is working!",
                "openai_configured": bool(os.getenv('OPENAI_API_KEY'))
            }
            
            self.wfile.write(json.dumps(response).encode())
            return
        
        # 404 for other paths
        self.send_response(404)
        self.end_headers()
    
    def do_POST(self):
        # Chat endpoint
        if self.path == '/siri/chat' or self.path == '/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            try:
                data = json.loads(body)
                text = data.get('text', 'No message')
                user_id = data.get('user_id', 'jarvis')
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    "response": f"Hey! I received: {text}",
                    "user_id": user_id
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
    
    def do_OPTIONS(self):
        # CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()