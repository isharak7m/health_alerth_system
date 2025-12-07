import requests
import json
import os
from typing import List
from sqlalchemy.orm import Session
from .models import ChatMessage, User

class HealthChatbot:
    def __init__(self):
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.model_name = os.getenv("OLLAMA_MODEL", "your-fine-tuned-model:latest")
    
    def get_conversation_history(self, db: Session, user_id: int, limit: int = 5) -> str:
        """Get recent conversation history for context"""
        messages = db.query(ChatMessage).filter(
            ChatMessage.user_id == user_id
        ).order_by(ChatMessage.timestamp.desc()).limit(limit).all()
        
        conversation = []
        for msg in reversed(messages):
            conversation.append(f"User: {msg.message}")
            if msg.response:
                conversation.append(f"Assistant: {msg.response}")
        
        return "\n".join(conversation)
    
    def generate_response(self, message: str, user: User, db: Session, ollama_url: str = None) -> str:
        """Generate response using AI model"""
        # Use provided ollama_url or fall back to default
        active_ollama_url = ollama_url or self.ollama_url
        
        try:
            system_prompt = f"You are a health assistant for {user.district}, {user.state}, India. Answer health questions accurately and concisely. Question: {message}"

            response = requests.post(
                f"{active_ollama_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": system_prompt,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                bot_response = result.get("response", "").strip()
                
                if bot_response:
                    chat_message = ChatMessage(
                        user_id=user.id,
                        message=message,
                        response=bot_response
                    )
                    db.add(chat_message)
                    db.commit()
                    return bot_response
                
        except Exception as e:
            print(f"AI Error: {e}")
            
        return "I encountered an error while processing your request. Please ensure the health AI model is running."
    

    
    def get_health_context_prompt(self, user: User) -> str:
        """Generate location-specific health context"""
        return f"""You are a health assistant specializing in:
- Disease outbreak monitoring for {user.state}, {user.district}
- Vaccination campaign information
- Health prevention and safety guidelines
- Emergency health protocols

Provide location-specific, accurate health information."""

chatbot = HealthChatbot()