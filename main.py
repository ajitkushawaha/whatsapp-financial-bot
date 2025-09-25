#!/usr/bin/env python3
"""
WhatsApp Financial Bot - Main Server
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import requests
import os
from dotenv import load_dotenv
import json
import asyncio
from enhanced_financial_bot import EnhancedFinancialBot
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="WhatsApp Financial Bot", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    try:
        from add_data_in_database import create_tables
        create_tables()
        logger.info("Database tables initialized successfully on startup")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")

# WhatsApp API Configuration
WHAPI_TOKEN = os.getenv("WHAPI_TOKEN", "5neaxPl90yIwcH62CaCd7qesx6DNkylZ")
WHAPI_BASE_URL = "https://gate.whapi.cloud"
WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "123")

# Initialize database tables
from add_data_in_database import create_tables
create_tables()
logger.info("Database tables initialized successfully")

# Initialize the financial bot
financial_bot = EnhancedFinancialBot()

# Message deduplication to prevent double responses
processed_messages = set()

class WhatsAppHandler:
    def __init__(self):
        self.base_url = WHAPI_BASE_URL
        self.token = WHAPI_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    async def send_message(self, phone_number: str, message: str):
        """Send a message to WhatsApp number via whapi.cloud"""
        try:
            url = f"{self.base_url}/messages/text"
            
            payload = {
                "to": phone_number,
                "body": message
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                logger.info(f"Message sent successfully to {phone_number}")
                return True
            else:
                logger.error(f"Failed to send message: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False

    async def send_typing_indicator(self, phone_number: str):
        """Send typing indicator to show bot is processing"""
        try:
            url = f"{self.base_url}/messages/typing"
            
            payload = {
                "to": phone_number,
                "typing": True
            }
            
            requests.post(url, headers=self.headers, json=payload)
        except Exception as e:
            logger.error(f"Error sending typing indicator: {e}")

# Initialize WhatsApp handler
whatsapp_handler = WhatsAppHandler()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "WhatsApp Financial Bot is running!", 
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/webhook")
async def verify_webhook(request: Request):
    """Webhook verification for WhatsApp (GET request)"""
    try:
        mode = request.query_params.get("hub.mode")
        token = request.query_params.get("hub.verify_token")
        challenge = request.query_params.get("hub.challenge")
        
        if mode == "subscribe" and token == WEBHOOK_VERIFY_TOKEN:
            logger.info("Webhook verified successfully")
            return int(challenge)
        else:
            logger.error("Webhook verification failed")
            raise HTTPException(status_code=403, detail="Forbidden")
            
    except Exception as e:
        logger.error(f"Webhook verification error: {e}")
        raise HTTPException(status_code=400, detail="Bad Request")

@app.post("/webhook")
async def handle_webhook(request: Request):
    """Handle incoming WhatsApp messages (POST request)"""
    try:
        body = await request.json()
        logger.info(f"Received webhook: {json.dumps(body, indent=2)}")
        
        if "messages" in body:
            for message_data in body["messages"]:
                await process_whatsapp_message(message_data)
        
        return JSONResponse(content={"status": "success"}, status_code=200)
        
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

async def process_whatsapp_message(message_data: dict):
    """Process individual WhatsApp message"""
    try:
        message_type = message_data.get("type")
        from_number = message_data.get("from")
        message_id = message_data.get("id")
        
        # Check for duplicate messages
        if message_id in processed_messages:
            logger.info(f"Skipping duplicate message: {message_id}")
            return
        
        # Add to processed messages
        processed_messages.add(message_id)
        
        # Clean old processed messages (keep only last 100)
        if len(processed_messages) > 100:
            processed_messages.clear()
        
        # Only process text messages
        if message_type != "text":
            logger.info(f"Ignoring non-text message type: {message_type}")
            return
        
        message_text = message_data.get("text", {}).get("body", "").strip()
        
        if not message_text:
            logger.info("Empty message received")
            return
        
        logger.info(f"Processing message from {from_number}: {message_text}")
        
        # Send typing indicator
        await whatsapp_handler.send_typing_indicator(from_number)
        
        # Process message with financial bot
        bot_response = financial_bot.process_message(message_text, from_number)
        
        # Send response back to user
        success = await whatsapp_handler.send_message(from_number, bot_response)
        
        if success:
            logger.info(f"Response sent to {from_number}")
        else:
            logger.error(f"Failed to send response to {from_number}")
            
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        try:
            error_message = "Sorry buddy! 😅 I'm having some technical difficulties. Please try again in a moment."
            await whatsapp_handler.send_message(message_data.get("from"), error_message)
        except:
            pass

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "bot_status": "active",
        "whapi_configured": bool(WHAPI_TOKEN),
        "timestamp": financial_bot.today.isoformat()
    }

if __name__ == "__main__":
    if not WHAPI_TOKEN:
        logger.error("WHAPI_TOKEN not found in environment variables!")
        exit(1)
    
    logger.info("WhatsApp Financial Bot initialized")
    logger.info(f"Webhook verify token: {WEBHOOK_VERIFY_TOKEN}")
    
    # Get port from environment variable (for deployment platforms)
    port = int(os.getenv("PORT", 8090))
    logger.info(f"Run with: uvicorn main:app --host 0.0.0.0 --port {port} --reload")
