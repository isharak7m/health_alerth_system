from app.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text('ALTER TABLE users RENAME COLUMN weekly_notifications TO notifications;'))
    conn.commit()
    print("Database updated successfully")