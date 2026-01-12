from drivit.file import File, FileType
from drivit.document import Document
from drivit.spreadsheet import Spreadsheet

class Folder(File):
    def __init__(self, name, id, drive, docs, sheets):
        super().__init__(name, FileType.FOLDER, id, drive)
        self._docs = docs
        self._sheets = sheets

    def create(self, file_name, type):
        if type not in [FileType.DOCUMENT, FileType.SPREADSHEET]:
            raise Exception("Cannot create file type %s" % type.name)

        file_metadata = {
            'name': file_name,
            'mimeType': type.value,
            'parents': [self._id]
        }

        file = self._drive.files().create(body=file_metadata).execute()
        if type == FileType.DOCUMENT:
            return Document(file_name, file['id'], self._drive, self._docs)
        else:
            return Spreadsheet(file_name, file['id'], self._drive, self._sheets)

    def exists(self, name):
        result = self._drive.files().list(corpora='user', q=self.query(name)).execute()
        return len(result['files']) > 0

    def open(self, file_name):
        result = self._drive.files().list(corpora='user', q=self.query(file_name)).execute()
        if len(result['files']) == 0:
            raise Exception('File %s does not exist' % file_name)
        return self.create_file(result['files'][0])

    def delete(self, file_name, type):
        if file_name == '*':
            query = '"%s" in parents and mimeType="%s" and trashed=false' % ((self._id), type.value);
        else:
            query = '"%s" in parents and name="%s" and mimeType="%s" and trashed=false' % (self._id, file_name, type.value);
        result = self._drive.files().list(corpora='user', q=query).execute()
        for file in result['files']:
            self._drive.files().delete(fileId=file['id']).execute()

    def list(self):
        result = self._drive.files().list(corpora='user', q='"%s" in parents and trashed=false' % self._id).execute()
        files = []
        for file in result['files']:
            files.append(self.create_file(file))
        return files

    def query(self, file_name):
        return '"%s" in parents and name="%s" and trashed=false' % (self._id, file_name);

    def create_file(self, file):
        mimetype = file['mimeType']
        if mimetype == FileType.FOLDER.value:
            return Folder(file['name'], file['id'], self._drive, self._docs, self._sheets)
        elif mimetype == FileType.DOCUMENT.value:
            return Document(file['name'], file['id'], self._drive, self._docs)
        elif mimetype == FileType.SPREADSHEET.value:
            spreadsheet = Spreadsheet(file['name'], file['id'], self._drive, self._sheets)
            spreadsheet.load()
            return spreadsheet
        raise Exception('Unknown file type %s for file %s' % (mimetype, file['name']))
