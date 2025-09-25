#!/usr/bin/env python3
"""
Railway startup script for WhatsApp Financial Bot
"""
import os
import uvicorn

if __name__ == "__main__":
    # Get port from Railway environment variable
    port = int(os.getenv("PORT", 8090))
    
    # Start the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
