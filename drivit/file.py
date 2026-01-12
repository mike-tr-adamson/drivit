from enum import Enum

FileType = Enum('FileType', [
                                ('FOLDER', 'application/vnd.google-apps.folder'),
                                ('DOCUMENT', 'application/vnd.google-apps.document'),
                                ('SPREADSHEET', 'application/vnd.google-apps.spreadsheet')
                            ])

class File(object):
    def __init__(self, name, type, id, drive):
        self._name = name
        self._type = type
        self._id = id
        self._drive = drive

    def __str__(self):
        return '%s[%s][%s]' % (self._name, self._type, self._id)
