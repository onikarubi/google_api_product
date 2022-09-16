import os
import glob
import gspread
from typing import List
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.http import HttpError
from gspread import WorksheetNotFound, SpreadsheetNotFound


class GoogleCloudApi(object):
    def __init__(
        self,
        scopes=None,
        refer_path_name='SERVICE_ACCOUNT_KEY',
        env_file_path=None
    ):

        self._scopes = scopes

        # .envファイルでサービスアカウントキーのパスが記載されている定数名
        self._refer_path_name = refer_path_name

        # 何も指定されていない場合は空の配列に設定
        if self._scopes is None:
            self._scopes = []

        """
        環境変数が記載された.envファイルから、変数の内容を読み込みます。
        ディレクトリ直下に.envファイルを作成してください。
        デフォルト値 -> None
        """

        try:
            if env_file_path is None:
                self._env_file_path = os.path.abspath(glob.glob(".env")[0])

            else:
                self._env_file_path = os.path.abspath(glob.glob(env_file_path)[0])

        except:
            raise EnvironmentError('.envファイルが見つかりません。ディレクトリ直下に.envファイルを作成してください。')

        load_dotenv(self._env_file_path)

    @property
    def get_env_file_path(self) -> str:
        return self._env_file_path

    @get_env_file_path.setter
    def set_env_file_path(self, path) -> None:
        self._env_file_path = path

    """""
    scopesが引数に渡されていない場合は、空の配列として定義することでインスタンス生成時に
    インスタンスメソッドから定義可能。
    """""
    @property
    def get_google_api_scopes(self) -> List[str]:
        return self._scopes

    @get_google_api_scopes.setter
    def set_google_api_scopes(self, scopes: List[str]) -> None:
        if not len(self._scopes) > 0:
            for scope in scopes:
                self._scopes.append(scope)

        else:
            print('既にインスタンス内でスコープが指定されています。')
            return


    """
    GoogleCloudApiの認証資格を取得する

    - .envファイルの変数名から鍵ファイルを参照
    - 認証が成功したら認証証明を発行
    """

    def get_credentials(self) -> Credentials:
        try:
            service_account_key = os.environ.get(self._refer_path_name)
            return Credentials.from_service_account_file(service_account_key)

        except HttpError as error:
            print(f'{error}: GoogleAPIの認証に失敗しました。')


"""
GoogleSheetsAPIを操作

- ワークブック、ワークシートの読み込み
- 読み込み
- 書き込み
- データの取得
"""


class GoogleSheetsAPI(GoogleCloudApi):
    def __init__(
        self,
        work_sheet_name: str,
        variable_spread_key: str = 'SPREAD_KEY',
        scopes=None,
        refer_path_name='SERVICE_ACCOUNT_KEY',
    ):
        super().__init__(scopes, refer_path_name)

        """
        .envファイルからvariable_spread_keyに指定されたスプレッドキーの変数を参照.
        ※ デフォルトは'SPREAD_KEY'
        """
        self.__spread_key = os.environ.get(variable_spread_key)
        self.__spread_sheet = self.__authorize_spread_sheet()
        self.__worksheet_name = work_sheet_name


    """""
    スプレッドシートの認証
    """""

    def __authorize_spread_sheet(self) -> gspread.Spreadsheet:
        try:
            credentials = self.get_credentials()
            credential_auth = gspread.authorize(credentials=credentials)

        except SpreadsheetNotFound as error:
            print('スプレッドシートの認証に失敗しました。')
            raise error

        return credential_auth.open_by_key(self.__spread_key)

    """""
    ワークブックからワークシートを読み込む
    """""

    def read_worksheet(self) -> gspread.Worksheet:
        try:
            worksheet = self.__spread_sheet.get_worksheet(self.__worksheet_name)
            print(f'{worksheet}の読み込みが完了しました。')

        except WorksheetNotFound as not_found_error:
            print(f'{self.__worksheet_name}のワークシートが見つかりませんでした。')
            raise not_found_error

    @property
    def get_worksheet_name(self) -> gspread.Worksheet:
        if self.__worksheet_name != '':
            return self.__worksheet_name

        else:
            raise ValueError('ワークシート名が空です。')


if __name__ == '__main__':
    # メイン処理
    pass
