from typing import Dict
import pytest
from src.gcp.services.spread_sheet import SelfCareSheet

@pytest.fixture
def self_care_sheet_names() -> Dict[str, str]:
    return {
        'default_case1': '',
        'default_case2': '鬱タイプ',
        'case2': '鬱タイプ(11月)',
    }

@pytest.fixture
def self_care_sheet_except_names() -> Dict[str, str]:
    return {
        'base_except': '躁鬱タイプ',
        'except_case2': '鬱タイプ ',
    }

class TestSelfCareSheet(object):
    def test_get_work_sheet_name(self, self_care_sheet_names: Dict[str, str]):
        """ コンストラクタの引数に空文字が指定されていたらデフォルトの'鬱タイプ'が出力されることを確認 """

        for k, v in self_care_sheet_names.items():
            sheet = SelfCareSheet(v)
            if self_care_sheet_names[k] == '':
                assert sheet.get_worksheet_name == '鬱タイプ'

            else:
                assert sheet.get_worksheet_name == v

    def test_get_work_sheet_exception(self, self_care_sheet_except_names: Dict[str, str]):
        # 正しい値が指定されていない"躁鬱タイプ"をテスト用に指定

        with pytest.raises(TypeError):
            SelfCareSheet(work_sheet_name='躁鬱タイプ')
            SelfCareSheet(work_sheet_name='鬱タイプ (ValueException01)')
            SelfCareSheet(work_sheet_name=self_care_sheet_except_names['base_except'])
            SelfCareSheet(work_sheet_name=self_care_sheet_except_names['except_case2'])

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



