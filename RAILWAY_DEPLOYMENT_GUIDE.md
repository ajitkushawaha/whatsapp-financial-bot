# 🚀 Railway Deployment Guide for WhatsApp Financial Bot

## 📋 Prerequisites
- Railway account (upgrade to paid plan required)
- GitHub repository access
- API keys ready (Gemini, whapi.cloud)

## 🎯 Quick Deployment Steps

### **Step 1: Fork/Clone Repository**
```bash
git clone https://github.com/ajitkushawaha/whatsapp-financial-bot.git
cd whatsapp-financial-bot
```

### **Step 2: Deploy to Railway**

1. **Go to Railway**: [railway.app](https://railway.app)
2. **Sign up/Login**: Use GitHub to sign in
3. **New Project**: Click "New Project"
4. **Deploy from GitHub**: 
   - Select "Deploy from GitHub repo"
   - Choose your forked repository
   - Select branch: `deployment` or `main`

### **Step 3: Configure Environment Variables**

In Railway dashboard → Your Project → Variables tab:

#### **Required Variables:**
```
GEMINI_API_KEY=your_actual_gemini_api_key
WHAPI_TOKEN=your_actual_whapi_token
WEBHOOK_VERIFY_TOKEN=your_secure_token_123
GOOGLE_API_KEY=your_actual_gemini_api_key
```

#### **Optional Variables:**
```
DATABASE_URL=sqlite:///financial_bot.db
HOST=0.0.0.0
DEBUG=False
```

### **Step 4: Deploy**

1. **Railway will automatically detect** Python app
2. **Build process** will install dependencies
3. **Deployment** will start automatically
4. **Get your URL**: Railway provides HTTPS URL

### **Step 5: Configure WhatsApp Integration**

1. **Get Railway URL**: `https://your-app-name.up.railway.app`
2. **Go to whapi.cloud**: [whapi.cloud](https://whapi.cloud)
3. **Settings → Webhooks**:
   - **URL**: `https://your-app-name.up.railway.app/webhook`
   - **Mode**: `body`
   - **Method**: `POST`
   - **Verify Token**: `your_secure_token_123`
4. **Enable Events**:
   - ✅ `messages: POST`
   - ✅ `statuses: POST`
5. **Save Configuration**

## 🧪 Testing Your Deployment

### **1. Health Check**
```bash
curl https://your-app-name.up.railway.app/health
```
**Expected Response:**
```json
{
  "status": "healthy",
  "bot_status": "active",
  "whapi_configured": true,
  "timestamp": "2025-09-25"
}
```

### **2. Test Webhook**
```bash
curl -X POST https://your-app-name.up.railway.app/webhook \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"id":"test123","type":"text","from":"1234567890","text":{"body":"Hello"}}]}'
```

### **3. Test WhatsApp Messages**
Send these to your WhatsApp number:
- **"Hello"** → Should get greeting
- **"I spent 100 on food"** → Should record transaction
- **"Show my expenses"** → Should show history
- **"What is Bitcoin?"** → Should provide info

## 🔧 Configuration Files

### **railway.json** (Already included)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 30,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 5
  }
}
```

### **requirements.txt** (Already included)
```
fastapi>=0.100.0
uvicorn>=0.20.0
requests>=2.25.0
python-dotenv>=1.0.0
pandas>=1.5.0
langchain-google-genai
google-generativeai
termcolor>=2.4.0
pyngrok>=7.0.0
SQLAlchemy>=2.0.0
```

## 🚨 Troubleshooting

### **Common Issues:**

1. **Build Fails**:
   - Check Python version (3.8+)
   - Verify requirements.txt
   - Check Railway logs

2. **Environment Variables**:
   - Ensure all required vars are set
   - Check variable names are correct
   - Verify API keys are valid

3. **Webhook Not Working**:
   - Check Railway URL is accessible
   - Verify whapi.cloud configuration
   - Check webhook logs

4. **Database Issues**:
   - SQLite database is created automatically on startup
   - Tables are initialized automatically via FastAPI startup event
   - If issues persist, run: `python init_database.py`
   - Check file permissions
   - Monitor storage usage

### **Debug Steps:**
1. **Check Railway Logs**: Project → Deployments → View Logs
2. **Test Health Endpoint**: `curl https://your-url/health`
3. **Verify Environment**: Check all variables are set
4. **Test Webhook**: Use curl command above

## 📊 Monitoring

### **Railway Dashboard:**
- **Deployments**: View build and deployment status
- **Logs**: Real-time application logs
- **Metrics**: CPU, memory, network usage
- **Variables**: Environment variable management

### **Health Monitoring:**
- **Health Check**: `/health` endpoint
- **Uptime**: Railway provides uptime monitoring
- **Alerts**: Set up alerts for failures

## 💰 Railway Pricing

### **Hobby Plan** (Recommended):
- **Cost**: $5/month
- **Features**: 
  - Unlimited deployments
  - Custom domains
  - Environment variables
  - Logs and metrics
  - 99.9% uptime SLA

### **Pro Plan**:
- **Cost**: $20/month
- **Features**: 
  - Everything in Hobby
  - Priority support
  - Advanced metrics
  - Team collaboration

## 🔒 Security Best Practices

1. **Environment Variables**:
   - Never commit API keys to code
   - Use Railway's secure variable storage
   - Rotate keys regularly

2. **Webhook Security**:
   - Use strong verify token
   - Validate incoming requests
   - Monitor webhook calls

3. **Database Security**:
   - Regular backups
   - Monitor access logs
   - Use secure connections

## 📞 Support

### **Railway Support:**
- **Documentation**: [docs.railway.app](https://docs.railway.app)
- **Discord**: Railway Discord community
- **Email**: support@railway.app

### **Bot Support:**
- **GitHub Issues**: Create issue in repository
- **Documentation**: Check README.md
- **Logs**: Check Railway deployment logs

## 🎉 Success Checklist

- [ ] Repository forked/cloned
- [ ] Railway project created
- [ ] Environment variables set
- [ ] Deployment successful
- [ ] Health check passing
- [ ] Webhook configured
- [ ] WhatsApp integration working
- [ ] Test messages responding

**Your WhatsApp Financial Bot is now live on Railway!** 🚀

---

## 📝 Quick Reference

**Railway URL**: `https://your-app-name.up.railway.app`
**Webhook URL**: `https://your-app-name.up.railway.app/webhook`
**Health Check**: `https://your-app-name.up.railway.app/health`

**Environment Variables Required:**
- `GEMINI_API_KEY`
- `WHAPI_TOKEN` 
- `WEBHOOK_VERIFY_TOKEN`
- `GOOGLE_API_KEY`
