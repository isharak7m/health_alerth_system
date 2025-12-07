from app.database import engine
from app import models
from datetime import datetime

def setup_database():
    # Create all tables
    models.Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    
    # Add sample data
    from app.database import SessionLocal
    db = SessionLocal()
    
    try:
        # Add sample outbreaks
        if not db.query(models.Outbreak).first():
            sample_outbreaks = [
                models.Outbreak(
                    outbreak_id="OUT001",
                    disease="Dengue",
                    report_date=datetime.now(),
                    country="India",
                    state="Delhi",
                    district="New Delhi",
                    cases_reported=150,
                    deaths=2,
                    severity="moderate",
                    confirmed=True,
                    notes="Monsoon-related outbreak"
                ),
                models.Outbreak(
                    outbreak_id="OUT002",
                    disease="Malaria",
                    report_date=datetime.now(),
                    country="India",
                    state="Maharashtra",
                    district="Mumbai",
                    cases_reported=89,
                    deaths=1,
                    severity="low",
                    confirmed=True,
                    notes="Urban area outbreak"
                )
            ]
            for outbreak in sample_outbreaks:
                db.add(outbreak)
        
        # Add sample vaccinations
        if not db.query(models.Vaccination).first():
            sample_vaccinations = [
                models.Vaccination(
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
                    partner_org="WHO",
                    notes="Booster campaign"
                ),
                models.Vaccination(
                    campaign_id="VAC002",
                    country="India",
                    state="Maharashtra",
                    district="Mumbai",
                    start_date=datetime.now(),
                    end_date=datetime(2024, 12, 31),
                    vaccine_name="Hepatitis B",
                    target_population="Children 0-5",
                    doses_allocated=5000,
                    doses_administered=3200,
                    partner_org="UNICEF",
                    notes="Childhood vaccination"
                )
            ]
            for vaccination in sample_vaccinations:
                db.add(vaccination)
        
        db.commit()
        print("Sample data added successfully!")
        
    finally:
        db.close()

if __name__ == "__main__":
    setup_database()