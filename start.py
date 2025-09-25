#!/usr/bin/env python3
"""
Production startup script for WhatsApp Financial Bot on Railway
"""
import os
import uvicorn
import logging

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    # Get port from Railway environment variable
    port = int(os.getenv("PORT", 8090))
    
    # Production configuration
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        workers=1,  # Single worker for Railway
        log_level="info",
        access_log=True,
        reload=False  # Disable reload in production
    )
