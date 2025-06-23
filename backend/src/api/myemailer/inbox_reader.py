import os
from api.myemailer.gmail_imap_parser import GmailImapParser

# pip install python-dotenv
# from dotenv import load_dotenv
# load_dotenv()

# Initialize


EMAIL_ADRESS=os.environ.get("EMAIL_ADRESS")
EMAIL_PASSWORD=os.environ.get("EMAIL_PASSWORD")


def read_inbox(hours_ago=24, unread_only=True, verbose=False):
    parser = GmailImapParser(
    email_address=EMAIL_ADRESS,
    app_password=EMAIL_PASSWORD
)

    # Fetch unread emails from last 24 hours
    emails = parser.fetch_emails(hours=hours_ago, unread_only=unread_only)

    if verbose:
        for email in emails:
            print(f"From: {email['from']}")
            print(f"Subject: {email['subject']}")
            print(f"Date: {email['timestamp']}")
            print("---")
    return emails