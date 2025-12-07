from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from .. import auth
from ..database import get_db
from ..chatbot import chatbot

router = APIRouter()

@router.post("/message", response_model=schemas.ChatMessage)
def send_message(message: schemas.ChatMessageBase, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    # Use custom ollama_url if provided, otherwise use default
    ollama_url = getattr(message, 'ollama_url', None)
    response = chatbot.generate_response(message.message, current_user, db, ollama_url=ollama_url)
    
    chat_message = models.ChatMessage(
        user_id=current_user.id,
        message=message.message,
        response=response
    )
    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    return chat_message

@router.get("/history", response_model=List[schemas.ChatMessage])
def get_chat_history(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return db.query(models.ChatMessage).filter(
        models.ChatMessage.user_id == current_user.id
    ).order_by(models.ChatMessage.timestamp.desc()).limit(20).all()