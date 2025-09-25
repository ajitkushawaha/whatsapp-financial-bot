#!/usr/bin/env python3
"""
Test script to send a WhatsApp message via whapi.cloud
"""

import requests
import json

# WhatsApp API Configuration
WHAPI_TOKEN = '5neaxPl90yIwcH62CaCd7qesx6DNkylZ'
WHAPI_BASE_URL = "https://gate.whapi.cloud"

def test_send_message():
    """Test sending a WhatsApp message"""
    
    print("📱 Testing WhatsApp Message Sending...")
    print("-" * 50)
    
    headers = {
        "Authorization": f"Bearer {WHAPI_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Get your own number to send a test message to yourself
    your_number = input("Enter your WhatsApp number (with country code, e.g., +919876543210): ").strip()
    
    if not your_number:
        print("❌ No phone number provided!")
        return
    
    # Remove any + or spaces and ensure proper format
    your_number = your_number.replace("+", "").replace(" ", "").replace("-", "")
    
    print(f"📞 Sending test message to: {your_number}")
    
    # Test message
    test_message = "🤖 Hello! This is a test message from your Financial Bot. If you receive this, the WhatsApp integration is working perfectly! 💰✨"
    
    try:
        url = f"{WHAPI_BASE_URL}/messages/text"
        
        payload = {
            "to": your_number,
            "body": test_message
        }
        
        print(f"📤 Sending message...")
        print(f"URL: {url}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Message sent successfully!")
            try:
                data = response.json()
                print(f"📋 Response: {json.dumps(data, indent=2)}")
            except:
                print(f"📋 Response (text): {response.text}")
        else:
            print(f"❌ Failed to send message!")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error occurred: {e}")
    
    print("-" * 50)
    print("🏁 Message test completed!")

if __name__ == "__main__":
    test_send_message()
