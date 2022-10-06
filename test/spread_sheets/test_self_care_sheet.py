from src.g_spread_sheets.google_cloud_api import SelfCareSheet


class TestSelfCareSheet(object):
    def test_get_work_sheet_name(self):
        s = SelfCareSheet()
        assert s.get_worksheet_name == '鬱タイプ'
