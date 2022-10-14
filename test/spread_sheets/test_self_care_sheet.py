import pytest
from src.gcp.services.google_cloud_api import SelfCareSheet
s = SelfCareSheet()

class TestSelfCareSheet(object):
    def test_get_work_sheet_name(self):
        s2 = SelfCareSheet(work_sheet_name='鬱タイプ(11月)')
        assert s.get_worksheet_name == '鬱タイプ'
        assert not s2.get_worksheet_name == '鬱タイプ'

        assert s2.get_worksheet_name == '鬱タイプ(11月)'

    def test_get_work_sheet_exception(self):
        # 正しい値が指定されていない"躁鬱タイプ"をテスト用に指定

        with pytest.raises(TypeError):
            SelfCareSheet(work_sheet_name='躁鬱タイプ')
            SelfCareSheet(work_sheet_name='鬱タイプ (ValueException01)')

    def test_get_cell_all_range_and_raise_exception(self):
        """
        セルの全範囲が設定されている場合はそのまま値を返し、
        何も指定されていない場合はValueExceptionを返す
        """
        begin_value = 'A1'
        end_value = 'E5'

        s2 = SelfCareSheet(cell_all_range=f'{begin_value}:{end_value}')

        assert s2.get_all_cell_range == f'{begin_value}:{end_value}'

        with pytest.raises(ValueError):
            s3 = SelfCareSheet(cell_all_range='')
            cell_range = s3.get_all_cell_range
            print(cell_range)



