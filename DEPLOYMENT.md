# 🚀 WhatsApp Financial Bot - Deployment Guide

## 📋 **Prerequisites**
- GitHub repository with your code
- API keys ready (Gemini, whapi.cloud)
- Domain name (optional, for custom webhook URL)

## 🌟 **Recommended Platforms**

### 1. **Railway** (⭐ **RECOMMENDED**)
**Best for**: Easy deployment, good free tier, Python-friendly

#### Steps:
1. **Sign up**: Go to [railway.app](https://railway.app)
2. **Connect GitHub**: Link your repository
3. **Deploy**: Click "Deploy from GitHub repo"
4. **Environment Variables**:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   WHAPI_TOKEN=your_whapi_token
   WEBHOOK_VERIFY_TOKEN=123
   GOOGLE_API_KEY=your_gemini_api_key
   ```
5. **Get URL**: Railway provides HTTPS URL automatically
6. **Configure whapi.cloud**: Use Railway URL + `/webhook`

**Cost**: Free tier ($5 credit) → $5-20/month
**URL Format**: `https://your-app-name.railway.app`

---

### 2. **Render** (⭐ **EXCELLENT**)
**Best for**: Reliable, good free tier, FastAPI support

#### Steps:
1. **Sign up**: Go to [render.com](https://render.com)
2. **New Web Service**: Connect GitHub repo
3. **Configuration**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables**: Add all required vars
5. **Deploy**: Click "Create Web Service"

**Cost**: Free tier → $7-25/month
**URL Format**: `https://your-app-name.onrender.com`

---

### 3. **Heroku** (⭐ **POPULAR**)
**Best for**: Most popular, lots of documentation

#### Steps:
1. **Install Heroku CLI**: [devcenter.heroku.com](https://devcenter.heroku.com)
2. **Login**: `heroku login`
3. **Create App**: `heroku create your-bot-name`
4. **Environment Variables**:
   ```bash
   heroku config:set GEMINI_API_KEY=your_key
   heroku config:set WHAPI_TOKEN=your_token
   heroku config:set WEBHOOK_VERIFY_TOKEN=123
   heroku config:set GOOGLE_API_KEY=your_key
   ```
5. **Deploy**: `git push heroku main`

**Cost**: $7-25/month
**URL Format**: `https://your-app-name.herokuapp.com`

---

### 4. **DigitalOcean App Platform**
**Best for**: Good performance, managed services

#### Steps:
1. **Sign up**: [cloud.digitalocean.com](https://cloud.digitalocean.com)
2. **Create App**: Connect GitHub repo
3. **Configure**: Select Python, add environment variables
4. **Deploy**: Automatic deployment

**Cost**: $12-25/month
**URL Format**: `https://your-app-name.ondigitalocean.app`

---

## 🔧 **Deployment Checklist**

### Before Deployment:
- [ ] Code pushed to GitHub
- [ ] Environment variables ready
- [ ] Database requirements checked
- [ ] Dependencies in requirements.txt

### After Deployment:
- [ ] Test health endpoint: `https://your-url.com/health`
- [ ] Test webhook: `https://your-url.com/webhook`
- [ ] Configure whapi.cloud with new URL
- [ ] Test with real WhatsApp messages

---

## 🌐 **WhatsApp Integration Setup**

### 1. **Get Your Deployed URL**
After deployment, you'll get a URL like:
- Railway: `https://your-app.railway.app`
- Render: `https://your-app.onrender.com`
- Heroku: `https://your-app.herokuapp.com`

### 2. **Configure whapi.cloud**
1. **Login**: Go to [whapi.cloud dashboard](https://whapi.cloud)
2. **Settings → Webhooks**:
   - **URL**: `https://your-deployed-url.com/webhook`
   - **Mode**: `body`
   - **Method**: `POST`
   - **Verify Token**: `123`
3. **Enable Events**:
   - ✅ `messages: POST`
   - ✅ `statuses: POST`
4. **Save Configuration**

### 3. **Test Integration**
Send a WhatsApp message to your bot:
- "Hello" → Should get greeting
- "I spent 100 on food" → Should record transaction
- "Show my expenses" → Should show history

---

## 🔒 **Security Considerations**

### Environment Variables:
- Never commit API keys to code
- Use platform's environment variable system
- Rotate keys regularly

### Webhook Security:
- Use strong verify token
- Validate incoming requests
- Log all webhook calls

---

## 📊 **Monitoring & Maintenance**

### Health Checks:
- Monitor: `https://your-url.com/health`
- Set up uptime monitoring (UptimeRobot, etc.)

### Logs:
- Check platform logs regularly
- Monitor error rates
- Set up alerts for failures

### Database:
- Regular backups (if using external DB)
- Monitor storage usage

---

## 💰 **Cost Comparison**

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Railway** | $5 credit | $5-20/mo | Easy setup |
| **Render** | 750 hours | $7-25/mo | Reliability |
| **Heroku** | 550 hours | $7-25/mo | Popularity |
| **DigitalOcean** | None | $12-25/mo | Performance |

---

## 🚨 **Troubleshooting**

### Common Issues:
1. **Port Issues**: Use `$PORT` environment variable
2. **Environment Variables**: Check all are set correctly
3. **Dependencies**: Ensure requirements.txt is complete
4. **Webhook**: Verify URL is accessible from internet

### Debug Steps:
1. Check platform logs
2. Test health endpoint
3. Verify environment variables
4. Test webhook manually

---

## 🎯 **Quick Start (Railway)**

1. **Push to GitHub**: `git push origin main`
2. **Railway**: Connect repo → Deploy
3. **Environment**: Add all API keys
4. **Get URL**: Copy provided URL
5. **whapi.cloud**: Configure webhook URL
6. **Test**: Send WhatsApp message

**Your bot will be live in 5 minutes!** 🚀

---

## 📞 **Support**

If you encounter issues:
1. Check platform documentation
2. Review logs for errors
3. Test endpoints manually
4. Verify environment variables

**Happy Deploying!** 🎉
