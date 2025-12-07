from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from .. import auth
from ..database import get_db

router = APIRouter()

@router.get("/location-data", response_model=schemas.LocationData)
def get_location_health_data(filter_location: bool = False, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if filter_location:
        outbreaks = db.query(models.Outbreak).filter(
            models.Outbreak.state == current_user.state,
            models.Outbreak.district == current_user.district
        ).all()
        
        vaccinations = db.query(models.Vaccination).filter(
            models.Vaccination.state == current_user.state,
            models.Vaccination.district == current_user.district
        ).all()
    else:
        outbreaks = db.query(models.Outbreak).all()
        vaccinations = db.query(models.Vaccination).all()
    
    return schemas.LocationData(
        state=current_user.state,
        district=current_user.district,
        outbreaks=outbreaks,
        vaccinations=vaccinations
    )

@router.get("/alerts")
def get_user_alerts(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    recent_outbreaks = db.query(models.Outbreak).filter(
        models.Outbreak.state == current_user.state,
        models.Outbreak.district == current_user.district,
        models.Outbreak.severity.in_(["high", "moderate"])
    ).limit(3).all()
    
    recent_vaccinations = db.query(models.Vaccination).filter(
        models.Vaccination.state == current_user.state,
        models.Vaccination.district == current_user.district
    ).limit(3).all()
    
    alerts = []
    for outbreak in recent_outbreaks:
        alerts.append({
            "type": "outbreak",
            "title": f"{outbreak.disease} Alert",
            "message": f"{outbreak.cases_reported} cases reported in {outbreak.district}",
            "severity": outbreak.severity
        })
    
    for vaccination in recent_vaccinations:
        alerts.append({
            "type": "vaccination",
            "title": f"{vaccination.vaccine_name} Available",
            "message": f"Vaccination campaign for {vaccination.target_population}",
            "severity": "info"
        })
    
    return {"alerts": alerts}

@router.get("/outbreaks")
def get_outbreaks(page: int = 1, limit: int = 10, state: str = None, district: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Outbreak)
    if state:
        query = query.filter(models.Outbreak.state == state)
    if district:
        query = query.filter(models.Outbreak.district == district)
    
    total = query.count()
    outbreaks = query.offset((page - 1) * limit).limit(limit).all()
    
    return {
        "items": outbreaks,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }

@router.get("/vaccinations")
def get_vaccinations(page: int = 1, limit: int = 10, state: str = None, district: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Vaccination)
    if state:
        query = query.filter(models.Vaccination.state == state)
    if district:
        query = query.filter(models.Vaccination.district == district)
    
    total = query.count()
    vaccinations = query.offset((page - 1) * limit).limit(limit).all()
    
    return {
        "items": vaccinations,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }