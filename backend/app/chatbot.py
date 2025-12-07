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
        """Generate response using AI model with fallback"""
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
                timeout=10
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
            print(f"AI Error: {e}, using fallback")
        
        # Fallback responses
        return self.get_fallback_response(message, user, db)
    

    
    def get_health_context_prompt(self, user: User) -> str:
        """Generate location-specific health context"""
        return f"""You are a health assistant specializing in:
- Disease outbreak monitoring for {user.state}, {user.district}
- Vaccination campaign information
- Health prevention and safety guidelines
- Emergency health protocols

Provide location-specific, accurate health information."""
    
    def get_fallback_response(self, message: str, user: User, db: Session) -> str:
        """Provide fallback health responses when AI is unavailable"""
        message_lower = message.lower()
        
        # Save to database
        fallback_response = ""
        
        if "malaria" in message_lower:
            fallback_response = f"Malaria is a serious disease transmitted by mosquitoes. In {user.district}, {user.state}, please take precautions: use mosquito nets, wear long sleeves, and apply repellent. Symptoms include fever, chills, and headache. Seek medical attention if you experience these symptoms."
        elif "dengue" in message_lower:
            fallback_response = f"Dengue fever is spread by Aedes mosquitoes. In {user.district}, {user.state}, prevent mosquito breeding by removing standing water. Symptoms include high fever, severe headache, pain behind eyes, and joint pain. Consult a doctor immediately if symptoms appear."
        elif "covid" in message_lower or "corona" in message_lower:
            fallback_response = f"COVID-19 prevention in {user.district}, {user.state}: Wear masks in crowded places, maintain social distancing, wash hands frequently, and get vaccinated. Symptoms include fever, cough, and difficulty breathing. Get tested if you have symptoms."
        elif "fever" in message_lower:
            fallback_response = "For fever: Rest, drink plenty of fluids, and take paracetamol if needed. If fever persists for more than 3 days or is very high (above 103°F), consult a doctor immediately."
        elif "vaccine" in message_lower or "vaccination" in message_lower:
            fallback_response = f"Check your local health center in {user.district}, {user.state} for vaccination schedules. Common vaccines include COVID-19, flu, and routine immunizations. Vaccination is safe and protects you and your community."
        elif "symptom" in message_lower:
            fallback_response = "Common health symptoms to watch for: persistent fever, severe headache, difficulty breathing, chest pain, unusual fatigue, or sudden weight loss. Always consult a healthcare provider for proper diagnosis."
        else:
            fallback_response = f"I'm a health assistant for {user.district}, {user.state}. I can help with information about diseases, symptoms, prevention, and vaccinations. Please ask specific health-related questions, and I'll do my best to assist you. For medical emergencies, please call your local emergency services or visit a hospital."
        
        # Save to database
        chat_message = ChatMessage(
            user_id=user.id,
            message=message,
            response=fallback_response
        )
        db.add(chat_message)
        db.commit()
        
        return fallback_response

chatbot = HealthChatbot()