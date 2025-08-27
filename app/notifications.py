import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime
from app.database import SessionLocal
from app.models import NotificationLog
from dotenv import load_dotenv

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

async def send_email_notification(request_id: int, to_email: str, subject: str, content: str):
    if not SENDGRID_API_KEY:
        return "SendGrid API key not set"

    message = Mail(
        from_email="dku3132@gmail.com",
        to_emails=to_email,
        subject=subject,
        html_content=content,
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        status = "sent" if response.status_code in [200, 202] else f"failed: {response.status_code} - {response.body}"
    except Exception as e:
        status = f"error: {repr(e)}"

    with SessionLocal() as session:
        log = NotificationLog(
            request_id=request_id,
            channel="email",
            status=status,
            sent_at=datetime.utcnow(),
        )
        session.add(log)
        session.commit()
