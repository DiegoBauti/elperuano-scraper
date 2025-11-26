from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = ['https://www.googleapis.com/auth/drive.file']
FOLDER_ID = '1DZVh2uxV6sgbzJMTDRHBTMDtt29iTSZI'


def get_drive_service():
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('drive', 'v3', credentials=creds)


def file_exists_in_drive(service, folder_id, filename):
    query = f"'{folder_id}' in parents and name = '{filename}' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return len(results.get("files", [])) > 0



def upload_to_drive(file_path):
    try:
        if not os.path.exists(file_path):
            print(f"El archivo no existe: {file_path}")
            return None
        
        service = get_drive_service()
        file_name = os.path.basename(file_path)

        if file_exists_in_drive(service, FOLDER_ID, file_name):
            print(f"El archivo YA existe en Drive: {file_name}")
            return "already-exists"
        
        file_metadata = {
            'name': file_name,
            'parents': [FOLDER_ID]
        }
        
        media = MediaFileUpload(file_path, resumable=True)
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        
        print(f"✓ Archivo subido exitosamente: {file.get('name')}")
        print(f"  Link: {file.get('webViewLink')}")
        
        return file.get('id')
        
    except Exception as e:
        print(f"✗ Error al subir: {e}")
        return None
