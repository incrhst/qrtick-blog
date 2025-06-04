#!/usr/bin/env python3
"""
Simple HTTP server for viewing the QRTick blog locally
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

def main():
    # Change to the blog_html directory
    blog_dir = Path("blog_html")
    if not blog_dir.exists():
        print("❌ blog_html directory not found. Run 'python blog_generator.py' first.")
        return
    
    os.chdir(blog_dir)
    
    PORT = 8000
    
    # Find an available port
    while PORT < 8010:
        try:
            with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
                print(f"🚀 Starting server at http://localhost:{PORT}")
                print(f"📝 Serving blog from: {blog_dir.absolute()}")
                print(f"🌐 Open http://localhost:{PORT} in your browser")
                print("📊 Press Ctrl+C to stop the server")
                
                # Try to open browser automatically
                try:
                    webbrowser.open(f"http://localhost:{PORT}")
                except:
                    pass
                
                httpd.serve_forever()
        except OSError:
            PORT += 1
    
    print("❌ Could not find an available port between 8000-8009")

if __name__ == "__main__":
    main()