from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash

def create_test_user():
    db = SessionLocal()
    try:
        test_user = db.query(User).filter(User.username == "Isharak").first()
        if not test_user:
            test_user = User(
                email="isharak@test.com",
                username="Isharak",
                hashed_password=get_password_hash("password123"),
                full_name="Isharak Test User",
                role="user",
                state="Delhi",
                district="New Delhi",
                notifications=True,
                is_active=True
            )
            db.add(test_user)
            db.commit()
            print("Test user created: username=Isharak, password=password123")
        else:
            print("Test user already exists")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()