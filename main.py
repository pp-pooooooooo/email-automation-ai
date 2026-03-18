from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os
from datetime import datetime
import email.utils

from config import SCOPES, SHEET_URL
from gmail_client import get_gmail_service, extract_body
from sheets_client import get_sheet
from summarizer import summarize_email


def get_credentials():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def run():
    creds = get_credentials()
    gmail = get_gmail_service(creds)
    sheet = get_sheet(creds, SHEET_URL)

    existing_ids = sheet.col_values(1)

    results = gmail.users().messages().list(
        userId='me',
        maxResults=50,
        q="in:inbox"
    ).execute()

    messages = results.get('messages', [])

    for msg in messages:
        msg_id = msg['id']

        if msg_id in existing_ids:
            continue

        message = gmail.users().messages().get(
            userId='me',
            id=msg_id,
            format='full'
        ).execute()

        headers = message['payload']['headers']

        subject, sender, date_raw = "", "", ""

        for h in headers:
            if h['name'] == 'Subject':
                subject = h['value']
            if h['name'] == 'From':
                sender = h['value']
            if h['name'] == 'Date':
                date_raw = h['value']

        body = extract_body(message)

        # Parse date
        dt_tuple = email.utils.parsedate_tz(date_raw)
        if dt_tuple:
            dt = datetime.fromtimestamp(email.utils.mktime_tz(dt_tuple))
            date = dt.strftime("%Y-%m-%d")
            time = dt.strftime("%H:%M:%S")
        else:
            date, time = "", ""

        summary = summarize_email(body)

        sheet.append_row([
            msg_id,
            sender.split("<")[0],
            sender,
            date,
            time,
            subject,
            body[:500],
            summary
        ])

        print(f"Saved: {subject}")


if __name__ == "__main__":
    run()