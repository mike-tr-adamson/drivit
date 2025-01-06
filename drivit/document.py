import json

from drivit.file import File, FileType

class Document(File):
    def __init__(self, name, id, drive, docs):
        super().__init__(name, FileType.DOCUMENT, id, drive)
        self._service = docs.documents()
        self.index = 1
        self.requests = []
        self.tableRows = 0
        self.tableColumns = 0
        self.tableIndex = 0
        self.rowIndex = 0
        self.columnIndex = 0

    def create(self, name):
      body = { 'title': name }
      self.documentId = self.service.documents().create(body=body).execute()['documentId']

    def addLine(self, text, bold=False):
        self.addText(text + '\n', bold)

    def addText(self, text, bold=False):
        self.requests.append({'insertText':{'location':{'index': self.index},'text': text}})
        self.requests.append({
            'updateTextStyle': {
                'range': {
                    'startIndex': self.index,
                    'endIndex': self.index + len(text)
                },
                'textStyle': {
                    'bold': bold
                },
                'fields': 'bold'
            }
        })
        self.index = self.index + len(text)

    def addSizedText(self, text, size, bold=False):
        self.requests.append({'insertText':{'location':{'index': self.index},'text': text}})
        self.requests.append({
            'updateTextStyle': {
                'range': {
                    'startIndex': self.index,
                    'endIndex': self.index + len(text)
                },
                'textStyle': {
                    'bold': bold,
                    "fontSize": {
                        "magnitude": size,
                        "unit": "PT"
                    },
                    "weightedFontFamily": {
                        "fontFamily": "Arial",
                        "weight": 500
                    }
                },
                'fields': '*'
            }
        })
        self.index = self.index + len(text)

    def addSuperscriptText(self, text, size):
        self.requests.append({'insertText':{'location':{'index': self.index},'text': text}})
        self.requests.append({
            'updateTextStyle': {
                'range': {
                    'startIndex': self.index,
                    'endIndex': self.index + len(text)
                },
                'textStyle': {
                    "baselineOffset": "SUPERSCRIPT",
                    "fontSize": {
                        "magnitude": size,
                        "unit": "PT"
                    },
                    "weightedFontFamily": {
                        "fontFamily": "Arial",
                        "weight": 500
                    }
                },
                'fields': '*'
            }
        })
        self.index = self.index + len(text)

    def makeList(self, start):
        self.requests.append({
            'createParagraphBullets': {
                'range': {
                    'startIndex': start,
                    'endIndex':  self.index
                },
                'bulletPreset': 'NUMBERED_DECIMAL_NESTED',
            }
        })

    def makeBulletList(self, start):
        self.requests.append({
            'createParagraphBullets': {
                'range': {
                    'startIndex': start,
                    'endIndex':  self.index
                },
                'bulletPreset': 'BULLET_CHECKBOX',
            }
        })

    def deleteList(self, start, finish):
        self.requests.append({
            'deleteParagraphBullets': {
                'range': {
                    'startIndex': start,
                    'endIndex':  finish
                },
            }
        })

    def addBorder(self, start, finish):
        self.requests.append({
            'updateParagraphStyle': {
                'range': {
                    'startIndex': start,
                    'endIndex':  finish
                },
                'paragraphStyle': {
                    'borderLeft': {
                        'color': { 'color': { 'rgbColor': {} } },
                        'dashStyle': 'SOLID',
                        'padding': { 'magnitude': 2.0, 'unit': 'PT' },
                        'width': { 'magnitude': 1.0, 'unit': 'PT' },
                    },
                    'borderRight': {
                        'color': { 'color': { 'rgbColor': {} } },
                        'dashStyle': 'SOLID',
                        'padding': { 'magnitude': 2.0, 'unit': 'PT' },
                        'width': { 'magnitude': 1.0, 'unit': 'PT' },
                    },
                    'borderTop': {
                        'color': { 'color': { 'rgbColor': {} } },
                        'dashStyle': 'SOLID',
                        'padding': { 'magnitude': 2.0, 'unit': 'PT' },
                        'width': { 'magnitude': 1.0, 'unit': 'PT' },
                    },
                    'borderBottom': {
                        'color': { 'color': { 'rgbColor': {} } },
                        'dashStyle': 'SOLID',
                        'padding': { 'magnitude': 2.0, 'unit': 'PT' },
                        'width': { 'magnitude': 1.0, 'unit': 'PT' },
                    }
                },
                'fields': '*'
            }
        })

    def insertImage(self, image):
        self.requests.append({
            'insertInlineImage': {
                'location': {
                    'index': self.index
                },
                'uri': image,
            }
        })
        self.index = self.index + 1

    def insertPageBreak(self):
        self.requests.append({
            'insertPageBreak': {
                'location': {
                    'index': self.index
                }
            }
        })
        self.index = self.index + 1

    def createTable(self, rows, columns, widths=[]):
        self.requests.append({'insertTable':{'rows':rows,'columns':columns,'location':{'index':self.index}}})
        columnIndex = 0
        self.tableIndex = self.index + 1
        for width in widths:
            self.requests.append({
                'updateTableColumnProperties': {
                    'tableStartLocation': {'index': self.tableIndex},
                    'columnIndices': [columnIndex],
                    'tableColumnProperties': {
                        'widthType': 'FIXED_WIDTH',
                        'width': {
                            'magnitude': width,
                            'unit': 'PT'
                        }
                    },
                    'fields': '*'
                }
            })
            columnIndex += 1
        if columnIndex < columns:
            self.requests.append({
                'updateTableColumnProperties': {
                    'tableStartLocation': {'index': self.tableIndex},
                    'columnIndices': [columnIndex],
                    'tableColumnProperties': {
                        'widthType': 'EVENLY_DISTRIBUTED',
                    },
                    'fields': '*'
                }
            })

        self.tableRows = rows
        self.tableColumns = columns
        self.rowIndex = 0
        self.columnIndex = 0
        self.index = self.index + 1 + 1 + 1 + 1

    def nextCell(self):
        self.index += 2
        self.columnIndex += 1
        if self.columnIndex == self.tableColumns:
            self.rowIndex += 1
            self.columnIndex = 0
            if self.rowIndex < self.tableRows:
                self.index += 1

    def makeCellGrey(self):
        self.requests.append({
            'updateTableCellStyle': {
                'tableCellStyle': {
                    'backgroundColor': {
                        'color': {
                            'rgbColor': {
                                'blue': 0.75,
                                'green': 0.75,
                                'red': 0.75
                            }
                        }
                    }
                },
                'fields': 'backgroundColor',
                'tableRange': {
                    'columnSpan': 1,
                    'rowSpan': 1,
                    'tableCellLocation': {
                        'columnIndex': self.columnIndex,
                        'rowIndex': self.rowIndex,
                        'tableStartLocation': {
                            'index': self.tableIndex
                        }
                    }
                }
            }
        })

    def complete(self):
        self.service.documents().batchUpdate(documentId=self.documentId, body={'requests': self.requests}).execute()

    def output(self):
        result = self._service.get(documentId=self._id).execute()
        print(json.dumps(result, indent=4, sort_keys=True))
