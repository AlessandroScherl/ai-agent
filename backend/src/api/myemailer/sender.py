import os
import smtplib
from email.message import EmailMessage # built into python


EMAIL_ADRESS=os.environ.get("EMAIL_ADRESS")
EMAIL_PASSWORD=os.environ.get("EMAIL_PASSWORD")
EMAIL_HOST=os.environ.get("EMAIL_HOST") or "smtp.gmail.com"
EMAIL_PORT=os.environ.get("EMAIL_PORT") or 465


def send_mail(subject: str="No subject provided", content:str="No message provided", to_email:str=EMAIL_ADRESS, from_email:str=EMAIL_ADRESS):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(content)
    with smtplib.SMTP_SSL(EMAIL_HOST,EMAIL_PORT) as smtp:
        smtp.login(EMAIL_ADRESS,EMAIL_PASSWORD)
        return smtp.send_message(msg)