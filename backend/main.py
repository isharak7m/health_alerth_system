from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import os
from app.database import engine, get_db
from app import models, auth, schemas
from app.routers import users, admin, chat, health_data

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Health Monitoring System", version="1.0.0")

# CORS configuration for production and development
allowed_origins = [
    "http://localhost:3000",
    "https://*.vercel.app",
    os.getenv("FRONTEND_URL", "http://localhost:3000")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(health_data.router, prefix="/api/health", tags=["health"])



@app.get("/")
async def root():
    return {"message": "Health Monitoring System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)