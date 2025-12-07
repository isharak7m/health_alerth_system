from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import User, Outbreak, Vaccination
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_location_notifications(state: str, district: str, notification_type: str, item_data: dict):
    db = SessionLocal()
    try:
        users_with_notifications = db.query(User).filter(
            User.notifications == True,
            User.state == state,
            User.district == district
        ).all()
        
        for user in users_with_notifications:
            send_notification_email(user, notification_type, item_data)
    finally:
        db.close()

def send_notification_email(user, notification_type: str, item_data: dict):
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")
    
    if not email_user or not email_password:
        return
    
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = user.email
    
    if notification_type == "outbreak":
        msg['Subject'] = f"Health Alert: New Outbreak in {user.district}, {user.state}"
        body = f"Dear {user.full_name},\n\n"
        body += f"A new outbreak has been reported in your area:\n\n"
        body += f"Disease: {item_data.get('disease')}\n"
        body += f"Cases: {item_data.get('cases_reported')}\n"
        body += f"Severity: {item_data.get('severity')}\n\n"
    else:  # vaccination
        msg['Subject'] = f"Vaccination Update: New Campaign in {user.district}, {user.state}"
        body = f"Dear {user.full_name},\n\n"
        body += f"A new vaccination campaign is available in your area:\n\n"
        body += f"Vaccine: {item_data.get('vaccine_name')}\n"
        body += f"Target: {item_data.get('target_population')}\n"
        body += f"Start Date: {item_data.get('start_date')}\n\n"
    
    body += "Stay safe and healthy!\n\nHealth Monitoring System"
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_user, email_password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Failed to send email to {user.email}: {e}")