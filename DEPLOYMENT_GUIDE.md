# 🚀 Complete Deployment Guide

## Architecture Overview

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   VERCEL        │ ───> │   RENDER         │ ───> │   NEON          │
│   (Frontend)    │      │   (Backend)      │      │   (Database)    │
│   React + Tail  │      │   FastAPI        │      │   PostgreSQL    │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   USER'S LOCAL   │
                         │   OLLAMA + LLaMA │
                         └──────────────────┘
```

---

## 📋 Prerequisites

- ✅ GitHub account (for code repository)
- ✅ Vercel account (Google login)
- ✅ Render account (Google login)
- ✅ Neon account (Google login)
- ✅ Ollama installed locally

---

## STEP 1: Setup GitHub Repository

### 1.1 Create Repository
```bash
cd c:/Users/ishar/Downloads/sih-bot-2
git init
git add .
git commit -m "Initial commit - Health Monitoring System"
```

### 1.2 Push to GitHub
```bash
# Create new repository on GitHub: health-monitoring-system
git remote add origin https://github.com/YOUR_USERNAME/health-monitoring-system.git
git branch -M main
git push -u origin main
```

---

## STEP 2: Deploy Database on Neon

### 2.1 Create Neon Project
1. Go to https://console.neon.tech
2. Click **"New Project"**
3. Project name: `health-monitoring-db`
4. Region: Choose closest to you (e.g., `US East (Ohio)`)
5. PostgreSQL version: `15` (default)
6. Click **"Create Project"**

### 2.2 Get Connection String
1. In your Neon dashboard, click **"Connection Details"**
2. Copy the connection string (looks like):
   ```
   postgresql://username:password@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
3. **SAVE THIS** - you'll need it for Render

### 2.3 Database Configuration
- Database name: `neondb` (default)
- Connection pooling: Enabled (default)
- Auto-suspend: Enabled (saves resources on free tier)

---

## STEP 3: Deploy Backend on Render

### 3.1 Create Web Service
1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select: `health-monitoring-system`

### 3.2 Configure Service
```
Name: health-monitoring-backend
Region: Oregon (US West)
Branch: main
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:$PORT
Instance Type: Free
```

### 3.3 Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**

Add these variables:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `postgresql://username:password@ep-xxx.neon.tech/neondb?sslmode=require` |
| `SECRET_KEY` | Generate random 32+ char string |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |
| `OLLAMA_URL` | `http://localhost:11434` |
| `OLLAMA_MODEL` | `llama3` |
| `FRONTEND_URL` | Leave empty for now (add after Vercel) |
| `PYTHON_VERSION` | `3.11.0` |

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3.4 Deploy
1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment
3. Your backend URL: `https://health-monitoring-backend.onrender.com`
4. **SAVE THIS URL** - you'll need it for frontend

### 3.5 Initialize Database
After deployment completes:
1. Go to Render dashboard → Your service → **"Shell"**
2. Run:
   ```bash
   python init_db.py
   ```
3. Verify tables created successfully

### 3.6 Create Admin User
In Render Shell:
```bash
python create_admin.py
```

---

## STEP 4: Deploy Frontend on Vercel

### 4.1 Create Project
1. Go to https://vercel.com/dashboard
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository: `health-monitoring-system`

### 4.2 Configure Project
```
Framework Preset: Create React App
Root Directory: frontend
Build Command: npm run build
Output Directory: build
Install Command: npm install
```

### 4.3 Environment Variables
Click **"Environment Variables"**

Add:
| Key | Value |
|-----|-------|
| `REACT_APP_API_URL` | `https://health-monitoring-backend.onrender.com` |

### 4.4 Deploy
1. Click **"Deploy"**
2. Wait 2-3 minutes
3. Your frontend URL: `https://health-monitoring-system.vercel.app`

### 4.5 Update Backend CORS
1. Go back to Render dashboard
2. Add environment variable:
   - Key: `FRONTEND_URL`
   - Value: `https://health-monitoring-system.vercel.app`
3. Service will auto-redeploy

---

## STEP 5: Setup Local Ollama

### 5.1 Install Ollama
**Windows:**
```bash
# Download from: https://ollama.ai/download
# Run installer
```

**Verify installation:**
```bash
ollama --version
```

### 5.2 Pull LLaMA 3 Model
```bash
ollama pull llama3
```

### 5.3 Start Ollama Service
```bash
ollama serve
```

Keep this running in background. Ollama will be available at `http://localhost:11434`

### 5.4 Test Ollama
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "What is malaria?",
  "stream": false
}'
```

---

## STEP 6: Configure Frontend for Local Ollama

### 6.1 Update Chat Component
Users need to configure their local Ollama URL in the chat interface.

The backend accepts `ollama_url` parameter in chat requests:
```javascript
axios.post('/api/chat/message', {
  message: "What are dengue symptoms?",
  ollama_url: "http://localhost:11434"  // User's local Ollama
})
```

### 6.2 User Instructions
Add to your app's help section:
```
To use AI chat:
1. Install Ollama: https://ollama.ai
2. Run: ollama pull llama3
3. Start: ollama serve
4. Chat will connect to your local AI
```

---

## STEP 7: Verify Deployment

### 7.1 Test Backend
```bash
curl https://health-monitoring-backend.onrender.com/
# Should return: {"message": "Health Monitoring System API"}
```

### 7.2 Test Frontend
1. Open: `https://health-monitoring-system.vercel.app`
2. Register new user
3. Login
4. View dashboard

### 7.3 Test Database
1. Create outbreak/vaccination
2. Verify data persists
3. Check Neon dashboard for data

### 7.4 Test AI Chat (Local)
1. Ensure Ollama running locally
2. Open chat interface
3. Send message
4. Verify response from local LLaMA

---

## 🔄 Automatic Deployments

### Frontend (Vercel)
- **Trigger:** Push to `main` branch
- **Auto-deploy:** Yes
- **Build time:** ~2 minutes

### Backend (Render)
- **Trigger:** Push to `main` branch
- **Auto-deploy:** Yes
- **Build time:** ~5 minutes
- **Note:** Free tier may spin down after inactivity (cold start ~30s)

---

## 🔐 Security Checklist

- ✅ DATABASE_URL contains `?sslmode=require`
- ✅ SECRET_KEY is 32+ random characters
- ✅ No credentials in code
- ✅ CORS configured for production domain
- ✅ Environment variables set in Render/Vercel
- ✅ `.env` files in `.gitignore`

---

## 📊 Free Tier Limits

### Neon (Database)
- ✅ 3 GB storage
- ✅ 1 project
- ✅ Auto-suspend after inactivity
- ✅ Unlimited queries

### Render (Backend)
- ✅ 750 hours/month
- ✅ 512 MB RAM
- ✅ Spins down after 15 min inactivity
- ✅ Cold start: ~30 seconds

### Vercel (Frontend)
- ✅ 100 GB bandwidth/month
- ✅ Unlimited deployments
- ✅ Instant global CDN
- ✅ Automatic HTTPS

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Render logs
# Common issues:
# 1. DATABASE_URL format incorrect
# 2. Missing environment variables
# 3. Requirements.txt dependencies failed
```

### Frontend can't connect to backend
```bash
# Check:
# 1. REACT_APP_API_URL is correct
# 2. Backend CORS allows frontend domain
# 3. Backend is running (not spun down)
```

### Database connection fails
```bash
# Verify:
# 1. Neon project is active
# 2. Connection string includes ?sslmode=require
# 3. Database tables created (run init_db.py)
```

### AI chat not working
```bash
# Local Ollama must be running:
ollama serve

# Verify:
curl http://localhost:11434/api/tags
```

---

## 🔄 Update Deployment

### Update Backend
```bash
git add backend/
git commit -m "Update backend"
git push origin main
# Render auto-deploys in ~5 minutes
```

### Update Frontend
```bash
git add frontend/
git commit -m "Update frontend"
git push origin main
# Vercel auto-deploys in ~2 minutes
```

---

## 📱 Production URLs

After deployment, you'll have:

- **Frontend:** `https://health-monitoring-system.vercel.app`
- **Backend:** `https://health-monitoring-backend.onrender.com`
- **Database:** `ep-xxx.us-east-2.aws.neon.tech`
- **AI Service:** `http://localhost:11434` (user's machine)

---

## ✅ Deployment Complete!

Your Health Monitoring System is now live and production-ready! 🎉

**Next Steps:**
1. Share frontend URL with users
2. Document Ollama setup for users
3. Monitor Render/Vercel dashboards
4. Set up custom domain (optional)

---

## 📞 Support

- Vercel Docs: https://vercel.com/docs
- Render Docs: https://render.com/docs
- Neon Docs: https://neon.tech/docs
- Ollama Docs: https://ollama.ai/docs
