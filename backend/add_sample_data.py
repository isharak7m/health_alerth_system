from app.database import SessionLocal
from app.models import Outbreak, Vaccination
from datetime import datetime

def add_sample_data():
    db = SessionLocal()
    try:
        # Add sample outbreaks
        outbreaks = [
            Outbreak(
                outbreak_id="OUT001",
                disease="Dengue",
                report_date=datetime.now(),
                country="India",
                state="Delhi",
                district="New Delhi",
                cases_reported=45,
                deaths=2,
                severity="moderate",
                confirmed=True,
                notes="Monsoon-related outbreak"
            ),
            Outbreak(
                outbreak_id="OUT002", 
                disease="Chikungunya",
                report_date=datetime.now(),
                country="India",
                state="Delhi",
                district="New Delhi",
                cases_reported=23,
                deaths=0,
                severity="low",
                confirmed=True,
                notes="Vector-borne disease"
            )
        ]
        
        # Add sample vaccinations
        vaccinations = [
            Vaccination(
                campaign_id="VAC001",
                country="India",
                state="Delhi",
                district="New Delhi",
                start_date=datetime.now(),
                end_date=datetime(2024, 12, 31),
                vaccine_name="COVID-19 Booster",
                target_population="Adults 18+",
                doses_allocated=10000,
                doses_administered=7500,
                partner_org="Delhi Health Department"
            ),
            Vaccination(
                campaign_id="VAC002",
                country="India", 
                state="Delhi",
                district="New Delhi",
                start_date=datetime.now(),
                end_date=datetime(2024, 12, 31),
                vaccine_name="Hepatitis B",
                target_population="Healthcare Workers",
                doses_allocated=5000,
                doses_administered=3200,
                partner_org="AIIMS Delhi"
            )
        ]
        
        for outbreak in outbreaks:
            existing = db.query(Outbreak).filter(Outbreak.outbreak_id == outbreak.outbreak_id).first()
            if not existing:
                db.add(outbreak)
        
        for vaccination in vaccinations:
            existing = db.query(Vaccination).filter(Vaccination.campaign_id == vaccination.campaign_id).first()
            if not existing:
                db.add(vaccination)
        
        db.commit()
        print("Sample data added successfully")
        
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_data()