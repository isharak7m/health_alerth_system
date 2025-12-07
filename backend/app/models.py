from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")  # user, admin
    state = Column(String)
    district = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    notifications = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    chat_messages = relationship("ChatMessage", back_populates="user")

class Outbreak(Base):
    __tablename__ = "outbreaks"
    
    id = Column(Integer, primary_key=True, index=True)
    outbreak_id = Column(String, unique=True, index=True)
    disease = Column(String, index=True)
    report_date = Column(DateTime)
    country = Column(String)
    state = Column(String, index=True)
    district = Column(String, index=True)
    cases_reported = Column(Integer)
    deaths = Column(Integer)
    severity = Column(String)  # low, moderate, high
    confirmed = Column(Boolean)
    source_url = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Vaccination(Base):
    __tablename__ = "vaccinations"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(String, unique=True, index=True)
    country = Column(String)
    state = Column(String, index=True)
    district = Column(String, index=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    vaccine_name = Column(String, index=True)
    target_population = Column(String)
    doses_allocated = Column(Integer)
    doses_administered = Column(Integer)
    partner_org = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
    response = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="chat_messages")