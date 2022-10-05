from src.google_cloud_api import GoogleSheetsAPI


class TestSelfCareSheet(object):
    def test_get_scopes(self):
        g = GoogleSheetsAPI(work_sheet_name='鬱タイプ (4月)')
        assert g.get_google_api_scopes == ['https://www.googleapis.com/auth/spreadsheets.readonly',
                                           'https://www.googleapis.com/auth/drive']


