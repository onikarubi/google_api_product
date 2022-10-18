import glob
import os
import pytest
from dotenv import load_dotenv

from src.gcp.services.google_cloud_api import GoogleCloudApi
class TestGoogleCloudApi(object):

    """
    .envファイルの場所をしっかり特定できるかどうか
    テストではプロジェクト配下に[config/.env]を設置
    成功するケースと失敗するケースを検証
    """
    def test_get_env_file_path(self):
        g = GoogleCloudApi(['sample.com', 'sample02.com'])
        path_exists_case1 = os.path.abspath('.env')
        path_exists_case2 = os.path.abspath(glob.glob('.env')[0])
        path_failure_case = os.path.abspath('env/config/.env')

        assert g.get_env_file_path == path_exists_case1
        assert g.get_env_file_path == path_exists_case2
        assert g.get_env_file_path != path_failure_case

        g.set_env_file_path = ''
        assert g.get_env_file_path != path_exists_case1
        assert g.get_env_file_path == ''


    # envファイルが見つからない場合の例外テスト
    def test_find_env_file_raise(self):
        with pytest.raises(EnvironmentError):
            GoogleCloudApi(['sample.com', 'sample02.com'], env_file_path='')

    """
    スコープが正しく設置されているかどうかの検証
    インスタンスの引数に指定するケースと後で入れるケースも検証
    """

    def test_get_google_api_scopes(self):
        g1 = GoogleCloudApi(scopes=["sample.com", "sample2.com"])
        g2 = GoogleCloudApi()

        # 初期状態の検証
        assert g1.get_google_api_scopes == ["sample.com", "sample2.com"]
        assert g2.get_google_api_scopes == []

        # スコープの設定検証
        g2.set_google_api_scopes = ["sample.com", "sample2.com"]
        assert g2.get_google_api_scopes == ["sample.com", "sample2.com"]

        # 既に引数でスコープが定義されている場合は動作しない
        g1.set_google_api_scopes = ["sample.com", "sample2.com"]
        assert g1.get_google_api_scopes == ["sample.com", "sample2.com"]

