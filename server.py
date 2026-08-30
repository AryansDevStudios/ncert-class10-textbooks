import http.server
import socketserver
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class FastWebViewHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom HTTP Request Handler supporting:
    1. HTTP Byte Range Requests (RFC 7233) for Fast Web View linearization
    2. Full Cross-Origin Resource Sharing (CORS) for Mozilla PDF.js Viewer
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Enable Range requests
        self.send_header('Accept-Ranges', 'bytes')
        # Enable CORS for Mozilla PDF.js and web viewers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()

def run_server():
    os.chdir(DIRECTORY)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), FastWebViewHTTPRequestHandler) as httpd:
        print("=" * 65)
        print(f"NCERT CLASS 10 DIGITAL LIBRARY SERVER RUNNING")
        print("=" * 65)
        print(f"  -> Local URL: http://localhost:{PORT}")
        print(f"  -> Mozilla PDF.js CORS: ENABLED")
        print(f"  -> Fast Web View HTTP Byte-Streaming: ENABLED")
        print("=" * 65)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    run_server()
