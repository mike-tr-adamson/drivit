import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account

class Service(object):
    def __init__(self, credentials, name, version, scope):
        creds = service_account.Credentials.from_service_account_file(os.path.expanduser(credentials), scopes=[scope])
        self._service = build(name, version, credentials=creds)

    def service(self):
        return self._service

class DriveService(Service):
    def __init__(self, credentials):
        super().__init__(credentials, 'drive', 'v3', 'https://www.googleapis.com/auth/drive')

class SheetsService(Service):
    def __init__(self, credentials):
        super().__init__(credentials, 'sheets', 'v4', 'https://www.googleapis.com/auth/spreadsheets')

class DocsService(Service):
    def __init__(self, credentials):
        super().__init__(credentials, 'docs', 'v1', 'https://www.googleapis.com/auth/drive')
