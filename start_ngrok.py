#!/usr/bin/env python3
"""
Simple ngrok tunnel runner for WhatsApp bot
Run this after starting main.py to expose your webhook publicly
"""

from pyngrok import ngrok
import time

def start_tunnel(port=8090):
    """Start ngrok tunnel for the specified port"""
    try:
        # Kill any existing tunnels
        ngrok.kill()
        
        # Create new tunnel
        tunnel = ngrok.connect(port)
        public_url = str(tunnel).replace("NgrokTunnel: ", "").replace('"', '').split(" -> ")[0]
        
        print("🌐 ngrok Tunnel Active!")
        print("=" * 50)
        print(f"📡 Public URL: {public_url}")
        print(f"🔗 Webhook URL: {public_url}/webhook")
        print(f"🏥 Health Check: {public_url}/health")
        print("=" * 50)
        print("\n📋 Copy this webhook URL to whapi.cloud:")
        print(f"   {public_url}/webhook")
        print("\n⏰ Tunnel is active. Press Ctrl+C to stop...")
        
        # Keep tunnel alive
        try:
            while True:
                time.sleep(30)
                print(".", end="", flush=True)
        except KeyboardInterrupt:
            print("\n\n👋 Stopping tunnel...")
            ngrok.kill()
            print("✅ Tunnel stopped.")
            
    except Exception as e:
        print(f"❌ Error starting tunnel: {e}")
        print("Make sure your main server is running on port 8090")

if __name__ == "__main__":
    start_tunnel()
