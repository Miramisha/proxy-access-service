import smtplib

from email.message import EmailMessage
from app.config import settings


def send_email(
    to_email: str,
    subject: str,
    body: str
):
    message = EmailMessage()

    message["Subject"] = subject
    message["From"] = settings.EMAIL_FROM
    message["To"] = to_email

    message.set_content(body)

    with smtplib.SMTP_SSL(
        settings.SMTP_HOST,
        settings.SMTP_PORT
    ) as smtp:

        smtp.login(
            settings.SMTP_USER,
            settings.SMTP_PASSWORD
        )

        smtp.send_message(message)