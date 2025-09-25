# 🤖 WhatsApp Financial Bot - Client Deployment Guide

## 🚀 Quick Start for Railway Deployment

This is a production-ready WhatsApp Financial Bot that can be deployed on Railway with minimal setup.

### **What This Bot Does:**
- 💰 **Expense Tracking**: "I spent 500 on groceries"
- 📊 **Income Recording**: "I earned 2000 from freelancing"  
- 📈 **Transaction History**: "Show my expenses this month"
- 🔍 **Financial Information**: "What is cryptocurrency?"
- 💱 **Live Rates**: "Gold price today"
- 🧠 **Smart Conversations**: Context-aware responses

## 📋 Prerequisites

1. **Railway Account** (Paid plan required - $5/month)
2. **GitHub Account**
3. **API Keys**:
   - Google Gemini API Key
   - whapi.cloud Token

## 🎯 One-Click Deployment

### **Step 1: Fork This Repository**
1. Go to: https://github.com/ajitkushawaha/whatsapp-financial-bot
2. Click "Fork" button
3. This creates your own copy

### **Step 2: Deploy to Railway**
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your forked repository
5. Railway will auto-detect Python app

### **Step 3: Add Environment Variables**
In Railway dashboard → Variables tab:

```
GEMINI_API_KEY=your_gemini_api_key_here
WHAPI_TOKEN=your_whapi_cloud_token_here
WEBHOOK_VERIFY_TOKEN=your_secure_token_123
GOOGLE_API_KEY=your_gemini_api_key_here
```

### **Step 4: Get Your URL**
Railway will provide: `https://your-app-name.up.railway.app`

### **Step 5: Configure WhatsApp**
1. Go to [whapi.cloud](https://whapi.cloud)
2. Settings → Webhooks:
   - **URL**: `https://your-app-name.up.railway.app/webhook`
   - **Verify Token**: `your_secure_token_123`
3. Enable message events

## 🔑 Getting API Keys

### **Google Gemini API:**
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key

### **whapi.cloud Token:**
1. Visit: https://whapi.cloud
2. Sign up for account
3. Go to Dashboard → API Keys
4. Generate new token
5. Copy the token

## 🧪 Testing

### **Health Check:**
```bash
curl https://your-app-name.up.railway.app/health
```

### **Test Webhook:**
```bash
curl -X POST https://your-app-name.up.railway.app/webhook \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"id":"test","type":"text","from":"1234567890","text":{"body":"Hello"}}]}'
```

## 📱 WhatsApp Integration

After deployment, send these messages to test:
- **"Hello"** → Bot greeting
- **"I spent 100 on food"** → Records expense
- **"Show my expenses"** → Shows transaction history
- **"What is Bitcoin?"** → Provides financial info

## 🔧 Configuration Files

- `railway.json` - Railway deployment config
- `requirements.txt` - Python dependencies
- `Procfile` - Process configuration
- `main.py` - Main application
- `enhanced_financial_bot.py` - Bot logic

## 🚨 Troubleshooting

### **Common Issues:**
1. **Build fails**: Check Python version (3.8+)
2. **Environment variables**: Ensure all are set correctly
3. **Webhook not working**: Check URL and verify token
4. **Database issues**: SQLite is auto-created

### **Debug Steps:**
1. Check Railway logs in dashboard
2. Test health endpoint
3. Verify environment variables
4. Check whapi.cloud configuration

## 📊 Monitoring

- **Railway Dashboard**: View logs, metrics, deployments
- **Health Endpoint**: `/health` for uptime monitoring
- **WhatsApp Logs**: Check message processing

## 💰 Costs

- **Railway**: $5/month (Hobby plan)
- **whapi.cloud**: Check their pricing
- **Google Gemini**: Check Google's pricing

## 🔒 Security

- Environment variables are encrypted in Railway
- Webhook verification prevents unauthorized access
- All API keys are stored securely
- HTTPS enabled automatically

## 📞 Support

- **Railway Docs**: https://docs.railway.app
- **GitHub Issues**: Create issue in repository
- **Bot Documentation**: See README.md

## ✅ Success Checklist

- [ ] Repository forked
- [ ] Railway project created
- [ ] Environment variables added
- [ ] Deployment successful
- [ ] Health check passing
- [ ] WhatsApp webhook configured
- [ ] Test messages working

**Your WhatsApp Financial Bot is now live!** 🎉

---

## 📝 Quick Reference

**Deploy URL**: https://railway.app
**Bot URL**: `https://your-app-name.up.railway.app`
**Webhook**: `https://your-app-name.up.railway.app/webhook`
**Health**: `https://your-app-name.up.railway.app/health`

**Required Environment Variables:**
- `GEMINI_API_KEY`
- `WHAPI_TOKEN`
- `WEBHOOK_VERIFY_TOKEN`
- `GOOGLE_API_KEY`
