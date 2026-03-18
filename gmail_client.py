from googleapiclient.discovery import build
import base64
from bs4 import BeautifulSoup

def get_gmail_service(creds):
    return build('gmail', 'v1', credentials=creds)


def extract_body(message):
    try:
        parts = message['payload'].get('parts', [])

        for part in parts:
            if part['mimeType'] in ['text/plain', 'text/html']:
                data = part['body'].get('data')
                if data:
                    text = base64.urlsafe_b64decode(data).decode('utf-8')
                    soup = BeautifulSoup(text, "html.parser")
                    return soup.get_text().strip()

    except:
        return "No body found"

    return "No body found"