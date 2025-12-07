# 🚀 DEPLOY NOW - Step-by-Step

## ⏱️ Total Time: 30 Minutes

---

## 📍 STEP 1: GitHub (5 minutes)

### 1.1 Create Repository
1. Go to: https://github.com/new
2. Repository name: `health-monitoring-system`
3. Description: `AI-powered health monitoring platform`
4. Visibility: Public or Private
5. Click **"Create repository"**

### 1.2 Push Code
```bash
cd c:/Users/ishar/Downloads/sih-bot-2
git init
git add .
git commit -m "Initial deployment"
git remote add origin https://github.com/YOUR_USERNAME/health-monitoring-system.git
git branch -M main
git push -u origin main
```

✅ **Checkpoint:** Code visible on GitHub

---

## 📍 STEP 2: Neon Database (5 minutes)

### 2.1 Create Project
1. Go to: https://console.neon.tech
2. Click **"New Project"**
3. Name: `health-monitoring-db`
4. Region: `US East (Ohio)` or closest
5. Click **"Create Project"**

### 2.2 Get Connection String
1. Click **"Connection Details"**
2. Copy the connection string
3. Should look like:
   ```
   postgresql://user:pass@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
4. **SAVE THIS** - paste in notepad

✅ **Checkpoint:** Connection string saved

---

## 📍 STEP 3: Render Backend (10 minutes)

### 3.1 Create Web Service
1. Go to: https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect account"** → Select GitHub
4. Find: `health-monitoring-system`
5. Click **"Connect"**

### 3.2 Configure Service
Fill in these fields:

| Field | Value |
|-------|-------|
| **Name** | `health-monitoring-backend` |
| **Region** | `Oregon (US West)` |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:$PORT` |
| **Instance Type** | `Free` |

### 3.3 Add Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**

Add these (one by one):

```
DATABASE_URL = <paste-your-neon-connection-string>
SECRET_KEY = <generate-below>
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30
OLLAMA_URL = http://localhost:11434
OLLAMA_MODEL = llama3
PYTHON_VERSION = 3.11.0
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3.4 Deploy
1. Click **"Create Web Service"**
2. Wait 5-10 minutes (watch logs)
3. When done, you'll see: **"Your service is live"**
4. Copy your URL: `https://health-monitoring-backend-xxxx.onrender.com`
5. **SAVE THIS URL**

### 3.5 Initialize Database
1. In Render dashboard, click **"Shell"** tab
2. Run:
   ```bash
   python init_db.py
   ```
3. Should see: "✓ Database tables created successfully!"

### 3.6 Create Admin User
In the same Shell:
```bash
python create_admin.py
```

✅ **Checkpoint:** Backend live, database initialized

---

## 📍 STEP 4: Vercel Frontend (5 minutes)

### 4.1 Create Project
1. Go to: https://vercel.com/dashboard
2. Click **"Add New..."** → **"Project"**
3. Click **"Import"** next to `health-monitoring-system`

### 4.2 Configure Project
Fill in these fields:

| Field | Value |
|-------|-------|
| **Framework Preset** | `Create React App` |
| **Root Directory** | `frontend` |
| **Build Command** | `npm run build` |
| **Output Directory** | `build` |
| **Install Command** | `npm install` |

### 4.3 Add Environment Variable
Click **"Environment Variables"**

Add:
```
REACT_APP_API_URL = <paste-your-render-backend-url>
```

Example:
```
REACT_APP_API_URL = https://health-monitoring-backend-xxxx.onrender.com
```

### 4.4 Deploy
1. Click **"Deploy"**
2. Wait 2-3 minutes
3. When done: **"Congratulations!"**
4. Copy your URL: `https://health-monitoring-system-xxxx.vercel.app`
5. **SAVE THIS URL**

✅ **Checkpoint:** Frontend live

---

## 📍 STEP 5: Update Backend CORS (2 minutes)

### 5.1 Add Frontend URL to Backend
1. Go back to Render dashboard
2. Click your backend service
3. Click **"Environment"** tab
4. Click **"Add Environment Variable"**
5. Add:
   ```
   FRONTEND_URL = <paste-your-vercel-url>
   ```
6. Service will auto-redeploy (wait 2 min)

✅ **Checkpoint:** CORS configured

---

## 📍 STEP 6: Setup Local Ollama (5 minutes)

### 6.1 Install Ollama
1. Download: https://ollama.ai/download
2. Run installer
3. Follow prompts

### 6.2 Pull LLaMA 3
Open terminal:
```bash
ollama pull llama3
```
Wait 2-3 minutes for download

### 6.3 Start Ollama
```bash
ollama serve
```
Keep this terminal open

### 6.4 Verify
Open new terminal:
```bash
curl http://localhost:11434/api/tags
```
Should see LLaMA 3 listed

✅ **Checkpoint:** Ollama running

---

## 📍 STEP 7: Test Everything (3 minutes)

### 7.1 Test Backend
```bash
curl https://your-backend.onrender.com/
```
Should return: `{"message": "Health Monitoring System API"}`

### 7.2 Test Frontend
1. Open: `https://your-app.vercel.app`
2. Should see login page
3. Click **"Register"**

### 7.3 Test Registration
1. Fill in form:
   - Email: test@example.com
   - Username: testuser
   - Password: Test123456
   - Full Name: Test User
   - State: Delhi
   - District: New Delhi
2. Click **"Register"**
3. Should redirect to login

### 7.4 Test Login
1. Login with credentials
2. Should see dashboard
3. Check for health data

### 7.5 Test AI Chat
1. Click **"Chat"** in navigation
2. Type: "What is malaria?"
3. Should get AI response (if Ollama running)

✅ **Checkpoint:** Everything working!

---

## 🎉 DEPLOYMENT COMPLETE!

### Your Live URLs:

**Frontend (Share this):**
```
https://your-app.vercel.app
```

**Backend API:**
```
https://your-backend.onrender.com
```

**API Documentation:**
```
https://your-backend.onrender.com/docs
```

---

## 📝 Save These Details

Create a file `DEPLOYMENT_INFO.txt`:

```
===========================================
HEALTH MONITORING SYSTEM - DEPLOYMENT INFO
===========================================

FRONTEND:
URL: https://your-app.vercel.app
Platform: Vercel
Status: ✅ Live

BACKEND:
URL: https://your-backend.onrender.com
Platform: Render
Status: ✅ Live

DATABASE:
Platform: Neon PostgreSQL
Connection: <your-connection-string>
Status: ✅ Active

AI SERVICE:
Platform: Local Ollama
Model: LLaMA 3
URL: http://localhost:11434
Status: ✅ Running

ADMIN CREDENTIALS:
Username: admin
Password: <from-create_admin.py>

GITHUB:
Repository: https://github.com/YOUR_USERNAME/health-monitoring-system

DEPLOYMENT DATE: <today's-date>
===========================================
```

---

## 🔄 Future Updates

To update your app:

```bash
# Make changes to code
git add .
git commit -m "Update: description"
git push origin main

# Vercel and Render will auto-deploy!
```

---

## 🐛 Troubleshooting

### Backend not responding?
- Check Render logs
- Verify DATABASE_URL format
- Wait 30s for cold start (free tier)

### Frontend blank page?
- Check browser console (F12)
- Verify REACT_APP_API_URL
- Check CORS settings

### Can't login?
- Verify backend is running
- Check network tab (F12)
- Try creating new user

### AI chat not working?
- Ensure `ollama serve` is running
- Check http://localhost:11434
- Verify LLaMA 3 is pulled

---

## 📞 Need Help?

- **Deployment Guide:** `DEPLOYMENT_GUIDE.md`
- **Quick Reference:** `QUICK_DEPLOY.md`
- **Troubleshooting:** `README_PRODUCTION.md`

---

## ✅ Final Checklist

- [x] GitHub repository created
- [x] Code pushed to GitHub
- [x] Neon database created
- [x] Render backend deployed
- [x] Database initialized
- [x] Admin user created
- [x] Vercel frontend deployed
- [x] CORS configured
- [x] Ollama installed
- [x] LLaMA 3 pulled
- [x] All services tested
- [x] Deployment info saved

---

## 🎊 SUCCESS!

**Your Health Monitoring System is now LIVE in production!**

Share your app with the world:
👉 `https://your-app.vercel.app`

Built for Smart India Hackathon 🇮🇳
