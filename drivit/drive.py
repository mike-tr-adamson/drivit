from drivit.service import DriveService, SheetsService, DocsService
from drivit.folder import Folder
from drivit.document import Document
from drivit.spreadsheet import Spreadsheet
    
class Drive(object):
    def __init__(self, credentials='~/.drivit/service_token.json'):
        self.drive = DriveService(credentials).service()
        self.docs = DocsService(credentials).service()
        self.sheets = SheetsService(credentials).service()

    def open(self, name):
        result = self.drive.files().list(corpora='user', q='name="%s" and trashed=false' % name).execute()
        if len(result['files']) == 0:
            raise Exception('File %s does not exist' % name)
        mimetype = result['files'][0]['mimeType']
        if mimetype.endswith('folder'):
            folder = Folder(name, result['files'][0]['id'], self.drive, self.docs, self.sheets)
            return folder
        elif mimetype.endswith('document'):
            document = Document(name, result['files'][0]['id'], self.drive, self.docs)
            return document
        elif mimetype.endswith('spreadsheet'):
            spreadsheet = Spreadsheet(name, result['files'][0]['id'], self.drive, self.sheets)
            spreadsheet.load()
            return spreadsheet
