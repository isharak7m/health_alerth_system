"""
Database initialization script for Neon PostgreSQL
Run this after deploying to Render to create all tables
"""
import os
from dotenv import load_dotenv
from app.database import engine
from app import models

load_dotenv()

def init_database():
    """Create all database tables"""
    print("Creating database tables...")
    models.Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully!")
    print("\nTables created:")
    print("  - users")
    print("  - outbreaks")
    print("  - vaccinations")
    print("  - chat_messages")

if __name__ == "__main__":
    init_database()
