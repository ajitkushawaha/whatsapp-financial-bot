# 🤖 WhatsApp Financial Bot

A smart WhatsApp bot that helps you track expenses, income, and get financial information using AI-powered responses.

## 🚀 Features

- **💰 Expense Tracking**: "I spent 500 on groceries"
- **📊 Income Recording**: "I earned 2000 from freelancing"
- **📈 Transaction History**: "Show my expenses this month"
- **🔍 Financial Information**: "What is cryptocurrency?"
- **💱 Live Rates**: "Gold price today"
- **🧠 Smart Conversations**: Follow-up questions and context awareness
- **📱 WhatsApp Integration**: Works directly through WhatsApp messages

## 📋 Prerequisites

- Python 3.8+
- Conda environment
- WhatsApp Business Account
- whapi.cloud account
- ngrok (for local development)

## 🛠 Installation

### 1. Clone and Setup Environment

```bash
# Navigate to your project directory
cd /path/to/your/project

# Activate your conda environment
conda deactivate && conda activate whisper-env

# Install required packages (if not already installed)
pip install fastapi uvicorn requests python-dotenv pandas langchain-google-genai google-generativeai termcolor pyngrok
```

### 2. Environment Configuration

Create a `.env` file in your project root:

```bash
# .env file
GEMINI_API_KEY=your_gemini_api_key_here
WHAPI_TOKEN=your_whapi_cloud_token_here
WEBHOOK_VERIFY_TOKEN=123
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 3. Database Setup

The bot will automatically create a SQLite database (`financial_bot.db`) on first run.

## 🏃‍♂️ Running the Bot

### Method 1: Run Main Server Only

```bash
# Activate environment and run server with uvicorn
conda deactivate && conda activate whisper-env && uvicorn main:app --host 0.0.0.0 --port 8090 --reload
```

The server will start on `http://localhost:8090` with auto-reload enabled.

### Method 2: Run with ngrok (for WhatsApp integration)

**Terminal 1 - Start Main Server:**
```bash
conda deactivate && conda activate whisper-env && uvicorn main:app --host 0.0.0.0 --port 8090 --reload
```

**Terminal 2 - Start ngrok Tunnel:**
```bash
conda deactivate && conda activate whisper-env && python start_ngrok.py
```

### Quick Commands Summary

```bash
# Start main server with auto-reload
conda deactivate && conda activate whisper-env && uvicorn main:app --host 0.0.0.0 --port 8090 --reload

# Start ngrok tunnel (in separate terminal)
conda deactivate && conda activate whisper-env && python start_ngrok.py

# Test connection
curl http://localhost:8090/health

# Alternative: Run without reload (production)
conda deactivate && conda activate whisper-env && uvicorn main:app --host 0.0.0.0 --port 8090
```

## 🌐 WhatsApp Integration Setup

### 1. Get Your ngrok URL

When you run `start_ngrok.py`, you'll get output like:
```
📡 Public URL: https://abc123.ngrok-free.app
🔗 Webhook URL: https://abc123.ngrok-free.app/webhook
```

### 2. Configure whapi.cloud

1. **Login to [whapi.cloud dashboard](https://whapi.cloud)**
2. **Go to Settings → Webhooks**
3. **Configure webhook:**
   - **URL**: `https://your-ngrok-url.ngrok-free.app/webhook`
   - **Mode**: `body`
   - **Method**: `POST`
   - **Verify Token**: `123`

4. **Enable Events:**
   - ✅ `messages: POST`
   - ✅ `statuses: POST` (optional)

5. **Enable Auto Download:**
   - ✅ `image`
   - ✅ `document`
   - ✅ `audio`

6. **Click Save**

## 🧪 Testing

### 1. Test Server Health

```bash
curl http://localhost:8090/health
```

Expected response:
```json
{
  "status": "healthy",
  "bot_status": "active",
  "whapi_configured": true,
  "timestamp": "2025-08-13"
}
```

### 2. Test WhatsApp Integration

Send a message to your WhatsApp number:
- "Hello" → Bot responds with greeting
- "I spent 500 on food" → Bot records transaction
- "Show my expenses" → Bot shows transaction history
- "What is Bitcoin?" → Bot searches and provides info

## 📝 Usage Examples

### Recording Transactions

```
User: "I spent 200 rupees on groceries"
Bot: "Got it, buddy! 📝 I've recorded 1 transaction(s) for you. Your financial tracking game is strong! 💪"

User: "I earned 5000 from freelancing"
Bot: "Got it, buddy! 📝 I've recorded 1 transaction(s) for you. Your financial tracking game is strong! 💪"
```

### Checking History

```
User: "What did I spend this month?"
Bot: "Hey buddy! 👋 Here's your financial summary for this month:
📊 Total Transactions: 15
💸 Total Expenses: ₹8,500
💰 Total Income: ₹25,000
📈 Net Savings: ₹16,500"
```

### Financial Information

```
User: "What is cryptocurrency?"
Bot: "Hey buddy! 🔍 Here's what I found:
Cryptocurrency is a digital or virtual currency that uses cryptography for security..."
```

## 🗂 Project Structure

```
BOT/
├── main.py                              # Main WhatsApp webhook server
├── enhanced_financial_bot.py            # Core bot logic and AI processing
├── create_ngrok_tunnel.py              # ngrok tunnel helper
├── add_data_in_database.py             # Database operations
├── config.py                           # Configuration settings
├── csv_operation.py                    # CSV operations
├── test_whatsapp_connection.py         # Connection testing
├── test_send_message.py               # Message testing
├── financial_bot.db                   # SQLite database (auto-created)
├── .env                              # Environment variables
└── README.md                         # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `WHAPI_TOKEN` | whapi.cloud token | Required |
| `WEBHOOK_VERIFY_TOKEN` | Webhook verification token | `123` |
| `GOOGLE_API_KEY` | Same as GEMINI_API_KEY | Required |

### Server Settings

- **Default Port**: 8090
- **Host**: 0.0.0.0 (accessible from all networks)
- **Reload**: Enabled (auto-restart on code changes)

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill process on port 8090
   sudo lsof -ti:8090 | xargs kill -9
   ```

2. **ngrok Not Working**
   ```bash
   # Install ngrok if not available
   pip install pyngrok
   ```

3. **Database Issues**
   ```bash
   # Delete and recreate database
   rm financial_bot.db
   python main.py  # Will recreate database
   ```

4. **WhatsApp Not Responding**
   - Check ngrok tunnel is active
   - Verify webhook URL in whapi.cloud
   - Check server logs for errors

### Logs

The bot provides detailed logging:
- Server startup and webhook registration
- Incoming message processing
- Bot responses and errors
- WhatsApp API interactions

## 📊 API Endpoints

### Health Check
```
GET /health
Response: {"status": "healthy", "bot_status": "active", ...}
```

### Webhook Verification
```
GET /webhook?hub.mode=subscribe&hub.verify_token=123&hub.challenge=12345
Response: 12345
```

### Message Processing
```
POST /webhook
Body: WhatsApp webhook payload
Response: {"status": "success"}
```

## 🔒 Security

- Webhook verification token prevents unauthorized access
- Environment variables keep sensitive data secure
- Input validation and error handling
- Logging for audit trails

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review server logs
3. Test individual components
4. Verify WhatsApp integration settings

---

**🎉 Enjoy your WhatsApp Financial Bot!** 

Your personal finance assistant is now just a WhatsApp message away! 💬💰
# whatsapp-financial-bot
