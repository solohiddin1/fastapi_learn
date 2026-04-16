import smtplib
from email.mime.text import MIMEText
from app.core.config import settings

SMTP_SERVER = settings.SMTP_HOST
SMTP_PORT = settings.SMTP_PORT
EMAIL = settings.SMTP_USER
PASSWORD = settings.SMTP_PASSWORD

def send_email(to_email: str, subject: str, body: str):
    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)