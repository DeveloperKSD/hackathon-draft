import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from dotenv import load_dotenv
from loguru import logger
import sys

# Load environment variables
if os.path.exists(".env"):
    load_dotenv()
    logger.info("Loaded .env configuration")

# Verify API_KEY is set
api_key = os.getenv("API_KEY")
if not api_key or "your_gemini" in api_key or "apikey" in api_key:
    logger.warning("API_KEY in .env is missing or using placeholder! Please configure it in your .env file.")

# Import the reply bot
try:
    from XianyuAgent import XianyuReplyBot
    bot = XianyuReplyBot()
    logger.info("XianyuReplyBot initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize XianyuReplyBot: {e}")
    sys.exit(1)


class SimulatorHTTPHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Override to use loguru instead of stderr
        logger.info(f"{self.address_string()} - {format % args}")

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            # Serve the index.html file
            try:
                file_path = os.path.join(os.path.dirname(__file__), "index.html")
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            except Exception as e:
                self.send_error(500, f"Error reading index.html: {str(e)}")
        else:
            self.send_error(404, "File not found")

    def do_POST(self):
        if self.path == "/api/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode("utf-8"))
                user_msg = data.get("user_msg", "")
                item_desc = data.get("item_desc", "")
                context = data.get("context", []) # Expected list of {"role": "user"|"assistant"|"system", "content": "..."}

                logger.info(f"Received message to simulate: '{user_msg}'")
                
                # Check current env configuration
                current_model = os.getenv("MODEL_NAME", "gemini-1.5-flash")
                current_base = os.getenv("MODEL_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/")
                
                # Generate reply
                reply = bot.generate_reply(
                    user_msg=user_msg,
                    item_desc=item_desc,
                    context=context
                )
                
                # Check which intent was triggered
                detected_intent = bot.last_intent or "default"
                
                response_data = {
                    "reply": reply,
                    "intent": detected_intent,
                    "model": current_model,
                    "base_url": current_base
                }
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode("utf-8"))
                
                logger.info(f"Replied with intent '{detected_intent}': '{reply}'")
                
            except Exception as e:
                logger.error(f"Error handling /api/chat: {e}")
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_error(404, "Endpoint not found")


def run_server(port=8000):
    server_address = ("", port)
    httpd = ThreadingHTTPServer(server_address, SimulatorHTTPHandler)
    logger.info(f"Server starting on http://localhost:{port} ... Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped by user.")
        httpd.server_close()


if __name__ == "__main__":
    run_server()
