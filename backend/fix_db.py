from app.database import engine
from sqlalchemy import text

# Check current table structure
with engine.connect() as conn:
    result = conn.execute(text("PRAGMA table_info(users);"))
    columns = result.fetchall()
    print("Current columns:", [col[1] for col in columns])
    
    # Check if weekly_notifications exists
    has_weekly = any(col[1] == 'weekly_notifications' for col in columns)
    has_notifications = any(col[1] == 'notifications' for col in columns)
    
    if has_weekly and not has_notifications:
        # Rename the column
        conn.execute(text("ALTER TABLE users RENAME COLUMN weekly_notifications TO notifications;"))
        conn.commit()
        print("Renamed weekly_notifications to notifications")
    elif not has_weekly and not has_notifications:
        # Add the notifications column
        conn.execute(text("ALTER TABLE users ADD COLUMN notifications BOOLEAN DEFAULT 0;"))
        conn.commit()
        print("Added notifications column")
    else:
        print("Column already exists correctly")