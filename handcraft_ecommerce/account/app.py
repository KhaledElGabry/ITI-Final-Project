import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# Define the Google Drive API scopes and service account file path
SCOPES = ['https://www.googleapis.com/auth/drive']


# SERVICE_ACCOUNT_FILE = "file.json"
script_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the full path to the service account file
SERVICE_ACCOUNT_FILE = os.path.join(script_dir, "file.json")


# PARENT_FOLDER_ID="1MhL0rLJd8lvlfC5nwumvERvogXRVKam5"

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def upload_photo(file_path, file_name, PARENT_FOLDER_ID):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': file_name,
        'parents': [PARENT_FOLDER_ID]
    }

    media_body = MediaFileUpload(file_path, resumable=True)

    file = service.files().create(
        body=file_metadata,
        media_body=media_body
    ).execute()

    file_id = file['id']

    # Get the URL of the uploaded file
    file_url = f"https://drive.google.com/thumbnail?id={file_id}"

    return file_url
    

def delete_photos(file_name, PARENT_FOLDER_ID):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    # Search for all files in the parent folder with the given name
    response = service.files().list(q=f"name='{file_name}' and '{PARENT_FOLDER_ID}' in parents").execute()
    files = response.get('files', [])

    if files:
        for file in files:
            # Get the file ID of each matching file and delete it
            file_id = file['id']
            service.files().delete(fileId=file_id).execute()
            print(f"File '{file_name}' with ID {file_id} deleted successfully.")
    else:
        print(f"No files with the name '{file_name}' found in the specified folder.")