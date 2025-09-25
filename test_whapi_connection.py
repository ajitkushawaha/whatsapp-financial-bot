#!/usr/bin/env python3
"""
Test script to check WhatsApp API (whapi.cloud) connection
"""

import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# WhatsApp API Configuration (same as in your main file)
WHAPI_TOKEN = '5neaxPl90yIwcH62CaCd7qesx6DNkylZ'
WHAPI_BASE_URL = "https://gate.whapi.cloud"

def test_whapi_connection():
    """Test the WhatsApp API connection"""
    
    print("🔍 Testing WhatsApp API Connection...")
    print(f"Token: {WHAPI_TOKEN[:10]}...")
    print(f"Base URL: {WHAPI_BASE_URL}")
    print("-" * 50)
    
    headers = {
        "Authorization": f"Bearer {WHAPI_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Test 1: Check API status
    print("1. Testing API Status...")
    try:
        url = f"{WHAPI_BASE_URL}/health"
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ API is reachable!")
            try:
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)}")
            except:
                print(f"   Response (text): {response.text}")
        else:
            print(f"   ❌ API returned error: {response.text}")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
    
    print()
    
    # Test 2: Check account/profile info
    print("2. Testing Account Info...")
    try:
        url = f"{WHAPI_BASE_URL}/me"
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Account info retrieved!")
            try:
                data = response.json()
                print(f"   Account: {json.dumps(data, indent=2)}")
            except:
                print(f"   Response (text): {response.text}")
        else:
            print(f"   ❌ Failed to get account info: {response.text}")
    except Exception as e:
        print(f"   ❌ Request failed: {e}")
    
    print()
    
    # Test 3: Check available endpoints
    print("3. Testing Available Endpoints...")
    endpoints_to_test = [
        "/settings",
        "/groups",
        "/contacts"
    ]
    
    for endpoint in endpoints_to_test:
        try:
            url = f"{WHAPI_BASE_URL}{endpoint}"
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   {endpoint}: {response.status_code} {'✅' if response.status_code == 200 else '❌'}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, list):
                        print(f"      Found {len(data)} items")
                    elif isinstance(data, dict):
                        print(f"      Keys: {list(data.keys())}")
                except:
                    pass
        except Exception as e:
            print(f"   {endpoint}: ❌ Error - {e}")
    
    print()
    print("-" * 50)
    print("🏁 Connection test completed!")
    print()
    print("📋 Next Steps:")
    print("   1. If all tests passed ✅, your API is working!")
    print("   2. Make sure your WhatsApp number is connected in whapi.cloud dashboard")
    print("   3. Set up webhook URL in whapi.cloud settings")
    print("   4. Run the FastAPI server to start receiving messages")

if __name__ == "__main__":
    test_whapi_connection()
