from drivit.file import File, FileType
from ratelimiter import RateLimiter

class Spreadsheet(File):
    request_count = 0

    def __init__(self, name, id, drive, sheets):
        super().__init__(name, FileType.SPREADSHEET, id, drive)
        self._service = sheets.spreadsheets()
        self.spreadsheet = {}
        self.sheet_ids = {}
        self.current_row = 1
        self.row_size = 0

    @RateLimiter(max_calls=20, period=60)
    def load(self):
        metadata = self._service.get(spreadsheetId=self._id).execute()

        sheets = metadata.get('sheets', '')

        for sheet in sheets:
            title = sheet.get('properties', {}).get('title', '')
            result = self._service.values().get(spreadsheetId=self._id, range=title).execute()
            values = result.get('values', [])
            self.spreadsheet[title] = values
            sheet_id = sheet.get('properties', {}).get('sheetId', '')
            self.sheet_ids[title] = sheet_id

    def sheet(self, sheet_name):
        return self.spreadsheet[sheet_name]

    def sheet_id(self, sheet_name):
        return self.sheet_ids[sheet_name]

    @RateLimiter(max_calls=20, period=60)
    def update(self, range, values, type='USER_ENTERED'):
        body = {
            'values': values
        }
        self._service.values().update(spreadsheetId=self._id, range=range, body=body, valueInputOption=type).execute()

