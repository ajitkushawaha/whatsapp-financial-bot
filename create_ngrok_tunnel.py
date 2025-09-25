#!/usr/bin/env python3
"""
Create ngrok tunnel for WhatsApp webhook server
"""

from pyngrok import ngrok
import time
import requests

def create_tunnel():
    """Create ngrok tunnel and display webhook URL"""
    
    # Close any existing tunnels
    ngrok.kill()
    
    # Create tunnel to port 8090
    public_url = ngrok.connect(8090)
    
    print("🌐 NgRok Tunnel Created!")
    print("="*50)
    print(f"📡 Public URL: {public_url}")
    print(f"🔗 Webhook URL: {public_url}/webhook")
    print(f"🏥 Health Check: {public_url}/health")
    print("="*50)
    
    # Test the connection
    try:
        response = requests.get(f"{public_url}/health")
        if response.status_code == 200:
            print("✅ Server is accessible via ngrok!")
            print(f"📊 Health Status: {response.json()}")
        else:
            print("❌ Server not responding properly")
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
    
    print("\n📋 NEXT STEPS:")
    print(f"1. Copy this webhook URL: {public_url}/webhook")
    print("2. Go to https://whapi.cloud dashboard")
    print("3. Navigate to Settings → Webhooks")
    print("4. Add the webhook URL above")
    print("5. Set verify token: 123")
    print("6. Enable 'Messages' events")
    print("7. Save the webhook configuration")
    print("\n🚀 Then your bot will be live on WhatsApp!")
    
    print("\n⏰ Tunnel will stay active. Press Ctrl+C to stop...")
    
    try:
        # Keep the tunnel alive
        while True:
            time.sleep(10)
            print(".", end="", flush=True)
    except KeyboardInterrupt:
        print("\n\n👋 Stopping ngrok tunnel...")
        ngrok.kill()

if __name__ == "__main__":
    create_tunnel()
