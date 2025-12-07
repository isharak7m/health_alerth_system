from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash

def create_admin_user():
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_user = User(
                email="admin@health.gov",
                username="admin",
                hashed_password=get_password_hash("admin123"),
                full_name="System Administrator",
                role="admin",
                state="Delhi",
                district="New Delhi",
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("Admin user created: username=admin, password=admin123")
        else:
            print("Admin user already exists")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()