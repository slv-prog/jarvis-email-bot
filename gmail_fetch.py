import os
import base64
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def fetch_emails():
    service = get_gmail_service()
    since = (datetime.now() - timedelta(hours=24)).strftime('%Y/%m/%d')
    results = service.users().messages().list(
        userId='me', q=f'after:{since} -category:promotions -category:social'
    ).execute()
    messages = results.get('messages', [])
    emails = []
    for msg in messages[:20]:
        data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        headers = data['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        body = ''
        if 'parts' in data['payload']:
            for part in data['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')[:500]
                    break
        emails.append({'subject': subject, 'sender': sender, 'body': body})
        print(f"Found: {subject}")
    print(f"Total emails found: {len(emails)}")
    return emails

if __name__ == '__main__':
    fetch_emails()