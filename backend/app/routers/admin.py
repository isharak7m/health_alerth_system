from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from .. import auth
from ..database import get_db
from ..scheduler import send_location_notifications
import pandas as pd
import io
from datetime import datetime

router = APIRouter()

@router.get("/users", response_model=List[schemas.User])
def get_all_users(admin_user: models.User = Depends(auth.require_admin), db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.delete("/users/{user_id}")
def delete_user(user_id: int, admin_user: models.User = Depends(auth.require_admin), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.post("/outbreaks", response_model=schemas.Outbreak)
def create_outbreak(outbreak: schemas.OutbreakCreate, admin_user: models.User = Depends(auth.require_admin), db: Session = Depends(get_db)):
    db_outbreak = models.Outbreak(**outbreak.dict())
    db.add(db_outbreak)
    db.commit()
    db.refresh(db_outbreak)
    
    send_location_notifications(
        db_outbreak.state, 
        db_outbreak.district, 
        "outbreak", 
        {"disease": db_outbreak.disease, "cases_reported": db_outbreak.cases_reported, "severity": db_outbreak.severity}
    )
    
    return db_outbreak

@router.put("/outbreaks/{outbreak_id}", response_model=schemas.Outbreak)
def update_outbreak(outbreak_id: int, outbreak: schemas.OutbreakCreate, admin_user: models.User = Depends(auth.require_admin), db: Session = Depends(get_db)):
    db_outbreak = db.query(models.Outbreak).filter(models.Outbreak.id == outbreak_id).first()
    if not db_outbreak:
        raise HTTPException(status_code=404, detail="Outbreak not found")
    
    for field, value in outbreak.dict().items():
        setattr(db_outbreak, field, value)
    db.commit()
    db.refresh(db_outbreak)
    
    send_location_notifications(
        db_outbreak.state, 
        db_outbreak.district, 
        "outbreak", 
        {"disease": db_outbreak.disease, "cases_reported": db_outbreak.cases_reported, "severity": db_outbreak.severity}
    )
    
    return db_outbreak

@router.delete("/outbreaks/{outbreak_id}")
def delete_outbreak(outbreak_id: int, admin_user: models.User = Depends(auth.require_admin), db: Session = Depends(get_db)):
    outbreak = db.query(models.Outbreak).filter(models.Outbreak.id == outbreak_id).first()
    if not outbreak:
        raise HTTPException(status_code=404, detail="Outbreak not found")
    db.delete(outbreak)
    db.commit()
    return {"message": "Outbreak deleted successfully"}

@router.post("/vaccinations", response_model=schemas.Vaccination)
def create_vaccination(vaccination: schemas.VaccinationCreate, admin_user: models.User = Depends(auth.require_admin), db: Session = Depends(get_db)):
    db_vaccination = models.Vaccination(**vaccination.dict())
    db.add(db_vaccination)
    db.commit()
    db.refresh(db_vaccination)
    
    send_location_notifications(
        db_vaccination.state, 
        db_vaccination.district, 
        "vaccination", 
        {"vaccine_name": db_vaccination.vaccine_name, "target_population": db_vaccination.target_population, "start_date": str(db_vaccination.start_date)}
    )
    
    return db_vaccination

@router.put("/vaccinations/{vaccination_id}", response_model=schemas.Vaccination)
def update_vaccination(vaccination_id: int, vaccination: schemas.VaccinationCreate, admin_user: models.User = Depends(auth.require_admin), db: Session = Depends(get_db)):
    db_vaccination = db.query(models.Vaccination).filter(models.Vaccination.id == vaccination_id).first()
    if not db_vaccination:
        raise HTTPException(status_code=404, detail="Vaccination not found")
    
    for field, value in vaccination.dict().items():
        setattr(db_vaccination, field, value)
    db.commit()
    db.refresh(db_vaccination)
    
    send_location_notifications(
        db_vaccination.state, 
        db_vaccination.district, 
        "vaccination", 
        {"vaccine_name": db_vaccination.vaccine_name, "target_population": db_vaccination.target_population, "start_date": str(db_vaccination.start_date)}
    )
    
    return db_vaccination

@router.delete("/vaccinations/{vaccination_id}")
def delete_vaccination(vaccination_id: int, admin_user: models.User = Depends(auth.require_admin), db: Session = Depends(get_db)):
    vaccination = db.query(models.Vaccination).filter(models.Vaccination.id == vaccination_id).first()
    if not vaccination:
        raise HTTPException(status_code=404, detail="Vaccination not found")
    db.delete(vaccination)
    db.commit()
    return {"message": "Vaccination deleted successfully"}

@router.post("/outbreaks/upload-csv")
def upload_outbreaks_csv(file: UploadFile = File(...), admin_user: models.User = Depends(auth.require_admin), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    try:
        contents = file.file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        required_columns = ['outbreak_id', 'disease', 'report_date', 'state', 'district', 'cases_reported', 'deaths', 'severity', 'confirmed']
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(status_code=400, detail=f"CSV must contain columns: {', '.join(required_columns)}")
        
        created_count = 0
        for _, row in df.iterrows():
            existing = db.query(models.Outbreak).filter(models.Outbreak.outbreak_id == row['outbreak_id']).first()
            if not existing:
                outbreak = models.Outbreak(
                    outbreak_id=row['outbreak_id'],
                    disease=row['disease'],
                    report_date=pd.to_datetime(row['report_date']),
                    country=row.get('country', 'India'),
                    state=row['state'],
                    district=row['district'],
                    cases_reported=int(row['cases_reported']),
                    deaths=int(row['deaths']),
                    severity=row['severity'],
                    confirmed=bool(row['confirmed']),
                    source_url=row.get('source_url', ''),
                    notes=row.get('notes', '')
                )
                db.add(outbreak)
                created_count += 1
                
                send_location_notifications(
                    outbreak.state,
                    outbreak.district,
                    "outbreak",
                    {"disease": outbreak.disease, "cases_reported": outbreak.cases_reported, "severity": outbreak.severity}
                )
        
        db.commit()
        return {"message": f"Successfully uploaded {created_count} outbreaks"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")

@router.post("/vaccinations/upload-csv")
def upload_vaccinations_csv(file: UploadFile = File(...), admin_user: models.User = Depends(auth.require_admin), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    try:
        contents = file.file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        required_columns = ['campaign_id', 'state', 'district', 'start_date', 'end_date', 'vaccine_name', 'target_population', 'doses_allocated', 'doses_administered']
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(status_code=400, detail=f"CSV must contain columns: {', '.join(required_columns)}")
        
        created_count = 0
        for _, row in df.iterrows():
            existing = db.query(models.Vaccination).filter(models.Vaccination.campaign_id == row['campaign_id']).first()
            if not existing:
                vaccination = models.Vaccination(
                    campaign_id=row['campaign_id'],
                    country=row.get('country', 'India'),
                    state=row['state'],
                    district=row['district'],
                    start_date=pd.to_datetime(row['start_date']),
                    end_date=pd.to_datetime(row['end_date']),
                    vaccine_name=row['vaccine_name'],
                    target_population=row['target_population'],
                    doses_allocated=int(row['doses_allocated']),
                    doses_administered=int(row['doses_administered']),
                    partner_org=row.get('partner_org', ''),
                    notes=row.get('notes', '')
                )
                db.add(vaccination)
                created_count += 1
                
                send_location_notifications(
                    vaccination.state,
                    vaccination.district,
                    "vaccination",
                    {"vaccine_name": vaccination.vaccine_name, "target_population": vaccination.target_population, "start_date": str(vaccination.start_date)}
                )
        
        db.commit()
        return {"message": f"Successfully uploaded {created_count} vaccinations"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")