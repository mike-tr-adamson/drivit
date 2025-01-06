from drivit.file import File, FileType

class Folder(File):
    def __init__(self, name, id, drive, docs, sheets):
        super().__init__(name, FileType.FOLDER, id, drive)
        self._docs = docs
        self._sheets = sheets
