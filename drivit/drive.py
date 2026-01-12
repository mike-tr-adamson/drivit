from drivit.service import DriveService, SheetsService, DocsService
from drivit.folder import Folder

class Drive(Folder):
    def __init__(self, credentials='~/.drivit/service_token.json'):
        super().__init__('My Drive',
                         'root',
                         DriveService(credentials).service(),
                         DocsService(credentials).service(),
                         SheetsService(credentials).service())

    def create(self, file_name, type):
        raise Exception("Cannot create a file in the root folder")

    def query(self, file_name):
        return 'name="%s" and trashed=false' % file_name;
