import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Define the Google Drive API scopes and service account file path
SCOPES = ['https://www.googleapis.com/auth/drive']


# SERVICE_ACCOUNT_FILE = "file.json"
script_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the full path to the service account file
SERVICE_ACCOUNT_FILE = os.path.join(script_dir, "file.json")


PARENT_FOLDER_ID="1-unemYftqFaK7qGJtfvNyA1VpbTBwsAG"

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def upload_photo(file_path,userId):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    
    file_metadata = {
        'name': userId,
        'parents': [PARENT_FOLDER_ID]
    }

    file = service.files().create(
        body=file_metadata,
        media_body=file_path
    ).execute()

upload_photo(os.path.join(script_dir, "3.jpg"),555)