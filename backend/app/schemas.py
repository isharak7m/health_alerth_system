from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    state: str
    district: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    is_active: bool
    role: str
    notifications: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    notifications: Optional[bool] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class OutbreakBase(BaseModel):
    outbreak_id: str
    disease: str
    report_date: datetime
    country: str = "India"
    state: str
    district: str
    cases_reported: int
    deaths: int
    severity: str
    confirmed: bool
    source_url: Optional[str] = None
    notes: Optional[str] = None

class OutbreakCreate(OutbreakBase):
    pass

class Outbreak(OutbreakBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class VaccinationBase(BaseModel):
    campaign_id: str
    country: str = "India"
    state: str
    district: str
    start_date: datetime
    end_date: datetime
    vaccine_name: str
    target_population: str
    doses_allocated: int
    doses_administered: int
    partner_org: Optional[str] = None
    notes: Optional[str] = None

class VaccinationCreate(VaccinationBase):
    pass

class Vaccination(VaccinationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ChatMessageBase(BaseModel):
    message: str
    ollama_url: Optional[str] = None

class ChatMessage(BaseModel):
    id: int
    user_id: int
    message: str
    response: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True

class LocationData(BaseModel):
    state: str
    district: str
    outbreaks: List[Outbreak]
    vaccinations: List[Vaccination]