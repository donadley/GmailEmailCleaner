import os
import datetime
import google.auth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError

# If modifying or deleting data, make sure the scope includes 'https://www.googleapis.com/auth/gmail.modify'
SCOPES = ['https://mail.google.com/']

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

def authenticate_gmail_api():
    """Authenticate and return a Gmail service instance using OAuth 2.0."""
    creds = None
    # Use token.pickle to store the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, log in via browser
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Build the Gmail API service
    service = build('gmail', 'v1', credentials=creds)
    return service


def list_old_emails(service, age_in_days=600):
    now = datetime.datetime.utcnow()
    two_years_ago = now - datetime.timedelta(days=age_in_days)
    query = f"before:{two_years_ago.strftime('%Y/%m/%d')} -in:trash"
    print(f"Running query: {query}")

    all_messages = []
    next_page_token = None

    try:
        while True:
            response = service.users().messages().list(
                userId='me',
                q=query,
                pageToken=next_page_token
            ).execute()

            messages = response.get('messages', [])
            all_messages.extend(messages)

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        print(f"\n✅ Total matching emails: {len(all_messages)}")

        if not all_messages:
            print("No old emails found.")
            return []

        # print("\n📬 Subject Lines & Dates:")
        # for msg in all_messages:
        #     msg_detail = service.users().messages().get(
        #         userId='me',
        #         id=msg['id'],
        #         format='metadata',
        #         metadataHeaders=['Subject', 'Date']
        #     ).execute()

        #     headers = msg_detail['payload'].get('headers', [])
        #     subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
        #     date = next((h['value'] for h in headers if h['name'] == 'Date'), '(No Date)')
        #     print(f"- [{date}] {subject}")

        return all_messages

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def delete_email(service, msg_id):
    """Delete an email by message ID."""
    try:
        service.users().messages().delete(userId='me', id=msg_id).execute()
        print(f'Email {msg_id} deleted successfully.')
    except HttpError as error:
        print(f'An error occurred: {error}')

def delete_old_emails(service):
    """Delete emails older than 2 years."""
    messages = list_old_emails(service)
    if not messages:
        print("No old emails found.")
    else:
        for message in messages:
            delete_email(service, message['id'])

def main():
    """Main function to run the Gmail cleanup task."""
    service = authenticate_gmail_api()
    delete_old_emails(service)

if __name__ == '__main__':
    main()
