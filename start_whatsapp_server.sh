#!/bin/bash

# Financial Bot WhatsApp Server Startup Script

echo "🚀 Starting Financial Bot WhatsApp Server..."
echo "=================================="

# Activate conda environment
echo "📦 Activating whisper-env conda environment..."
conda deactivate && conda activate whisper-env

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found! Creating from template..."
    cp .env.template .env
    echo "📝 Please edit .env file with your actual API tokens before running!"
    echo "   - WHAPI_TOKEN: Get from whapi.cloud dashboard"
    echo "   - WEBHOOK_VERIFY_TOKEN: Create a random secure token"
    echo "   - GEMINI_API_KEY: Your Google Gemini API key"
    exit 1
fi

# Check if required tokens are set
if grep -q "your_whapi_token_here" .env; then
    echo "❌ Please update WHAPI_TOKEN in .env file"
    exit 1
fi

if grep -q "your_gemini_api_key_here" .env; then
    echo "❌ Please update GEMINI_API_KEY in .env file"
    exit 1
fi

echo "✅ Environment configured"
echo "🌐 Starting FastAPI server on http://0.0.0.0:8000"
echo "📱 WhatsApp webhook endpoint: http://your-domain.com:8000/webhook"
echo "📊 Health check: http://your-domain.com:8000/health"
echo "📚 API docs: http://your-domain.com:8000/docs"
echo ""
echo "🛑 Press Ctrl+C to stop the server"
echo "=================================="

# Start the server
python whatsapp_webhook_server.py
