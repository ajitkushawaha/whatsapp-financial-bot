#!/bin/bash
# WhatsApp Financial Bot Startup Script

echo "🤖 Starting WhatsApp Financial Bot..."
echo "=================================="

# Check if conda environment exists
if ! conda info --envs | grep -q whisper-env; then
    echo "❌ Error: whisper-env conda environment not found!"
    echo "Please create the environment first:"
    echo "conda create -n whisper-env python=3.9"
    exit 1
fi

# Function to start the main server
start_server() {
    echo "🚀 Starting main server on port 8090..."
    conda deactivate && conda activate whisper-env && python main.py
}

# Function to start ngrok tunnel
start_tunnel() {
    echo "🌐 Starting ngrok tunnel..."
    conda deactivate && conda activate whisper-env && python start_ngrok.py
}

# Check command line argument
case "$1" in
    "server")
        start_server
        ;;
    "tunnel")
        start_tunnel
        ;;
    "both")
        echo "🚀 Starting both server and tunnel..."
        echo "📝 Server will start in background, tunnel in foreground"
        echo "📝 Use Ctrl+C to stop tunnel, then 'pkill -f main.py' to stop server"
        start_server &
        sleep 3
        start_tunnel
        ;;
    *)
        echo "Usage: $0 {server|tunnel|both}"
        echo ""
        echo "Commands:"
        echo "  server  - Start only the main server"
        echo "  tunnel  - Start only the ngrok tunnel (server must be running)"
        echo "  both    - Start both server and tunnel"
        echo ""
        echo "Examples:"
        echo "  $0 server    # Start server only"
        echo "  $0 tunnel    # Start tunnel only"
        echo "  $0 both      # Start both (recommended for development)"
        echo ""
        echo "Manual commands:"
        echo "  conda deactivate && conda activate whisper-env && python main.py"
        echo "  conda deactivate && conda activate whisper-env && python start_ngrok.py"
        exit 1
        ;;
esac
