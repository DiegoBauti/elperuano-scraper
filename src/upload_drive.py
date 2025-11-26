import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_drive_service():
    # Cargar token desde GitHub Secrets
    token_data = os.getenv("GOOGLE_TOKEN")
    
    if not token_data:
        raise Exception("GOOGLE_TOKEN no está configurado como secret en GitHub.")

    creds_dict = json.loads(token_data)
    creds = Credentials.from_authorized_user_info(creds_dict, SCOPES)

    # Refrescar token automáticamente
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return build('drive', 'v3', credentials=creds)
