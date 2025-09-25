# 🔧 Environment Variables Template

## Required Environment Variables for Railway Deployment

Copy these variables to your Railway project settings:

### **Essential Variables:**
```
GEMINI_API_KEY=your_gemini_api_key_here
WHAPI_TOKEN=your_whapi_cloud_token_here
WEBHOOK_VERIFY_TOKEN=your_secure_verify_token_here
GOOGLE_API_KEY=your_gemini_api_key_here
```

### **Optional Variables:**
```
DATABASE_URL=sqlite:///financial_bot.db
HOST=0.0.0.0
DEBUG=False
```

## 🔑 How to Get API Keys:

### **1. Google Gemini API Key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the generated key

### **2. whapi.cloud Token:**
1. Go to [whapi.cloud](https://whapi.cloud)
2. Sign up for an account
3. Go to Dashboard → API Keys
4. Generate a new token
5. Copy the token

### **3. Webhook Verify Token:**
- Can be any secure string (e.g., "my_secure_token_123")
- Keep this secret and consistent

## ⚠️ Security Notes:
- Never commit API keys to code
- Use Railway's environment variables feature
- Rotate keys regularly
- Keep verify token secure
