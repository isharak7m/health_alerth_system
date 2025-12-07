# ⚡ Quick Deploy Checklist

## 🎯 30-Minute Deployment

### ✅ Step 1: Neon Database (5 min)
1. Go to https://console.neon.tech
2. New Project → `health-monitoring-db`
3. Copy connection string
4. ✓ Done

### ✅ Step 2: Render Backend (10 min)
1. Go to https://dashboard.render.com
2. New Web Service → Connect GitHub
3. Configure:
   - Root: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:$PORT`
4. Add env vars (DATABASE_URL, SECRET_KEY, etc.)
5. Deploy → Wait 5 min
6. Run in Shell: `python init_db.py`
7. ✓ Done

### ✅ Step 3: Vercel Frontend (5 min)
1. Go to https://vercel.com/dashboard
2. New Project → Import GitHub
3. Root: `frontend`
4. Add env: `REACT_APP_API_URL=https://your-backend.onrender.com`
5. Deploy → Wait 2 min
6. ✓ Done

### ✅ Step 4: Update Backend CORS (2 min)
1. Render → Environment Variables
2. Add: `FRONTEND_URL=https://your-app.vercel.app`
3. ✓ Done

### ✅ Step 5: Local Ollama (5 min)
```bash
# Install Ollama
# Download: https://ollama.ai

# Pull model
ollama pull llama3

# Start service
ollama serve
```
✓ Done

---

## 🔑 Environment Variables Quick Reference

### Render (Backend)
```
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require
SECRET_KEY=<generate-random-32-chars>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3
FRONTEND_URL=https://your-app.vercel.app
PYTHON_VERSION=3.11.0
```

### Vercel (Frontend)
```
REACT_APP_API_URL=https://your-backend.onrender.com
```

---

## 🧪 Quick Test

### Test Backend
```bash
curl https://your-backend.onrender.com/
```

### Test Frontend
Open: `https://your-app.vercel.app`

### Test Database
Register user → Login → Create outbreak

### Test AI
Start Ollama → Open chat → Send message

---

## 🚨 Common Issues

| Issue | Solution |
|-------|----------|
| Backend 500 error | Check DATABASE_URL format |
| Frontend blank | Check REACT_APP_API_URL |
| CORS error | Add FRONTEND_URL to Render |
| AI not working | Start `ollama serve` locally |
| Cold start slow | Free tier - wait 30s |

---

## ✅ Deployment Checklist

- [ ] GitHub repo created and pushed
- [ ] Neon database created
- [ ] Render backend deployed
- [ ] Database tables initialized
- [ ] Vercel frontend deployed
- [ ] Backend CORS updated
- [ ] Ollama installed locally
- [ ] LLaMA 3 model pulled
- [ ] All services tested
- [ ] Admin user created

---

## 🎉 You're Live!

**Frontend:** https://your-app.vercel.app  
**Backend:** https://your-backend.onrender.com  
**Database:** Neon PostgreSQL  
**AI:** Local Ollama + LLaMA 3
