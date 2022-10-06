import os
import glob
import gspread
from typing import List
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.http import HttpError
from gspread import WorksheetNotFound, SpreadsheetNotFound
from gspread.client import APIError


class _GoogleCloudApi(object):
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
                self._env_file_path = os.path.abspath(
                    glob.glob(env_file_path)[0])

        except:
            raise EnvironmentError(
                '.envファイルが見つかりません。ディレクトリ直下に.envファイルを作成してください。')

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
            file_path = os.environ.get(self._refer_path_name)
            account_file = Credentials.from_service_account_file(
                file_path)
            credentials = account_file.with_scopes(scopes=self._scopes)
            return credentials

        except HttpError as error:
            print(f'{error}: GoogleAPIの認証に失敗しました。')


"""
GoogleSheetsAPIを操作

- ワークブック、ワークシートの読み込み
- 読み込み
- 書き込み
- データの取得
"""


class GoogleSheetsAPI(_GoogleCloudApi):
    def __init__(
        self,
        work_sheet_name: str = '',
        variable_spread_key: str = 'SPREAD_KEY',
        scopes=None,
        refer_path_name='SERVICE_ACCOUNT_KEY',
    ):
        super().__init__(scopes, refer_path_name)

        if len(self._scopes) == 0:
            self._scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly',
                            'https://www.googleapis.com/auth/drive']

        """
        .envファイルからvariable_spread_keyに指定されたスプレッドキーの変数を参照.
        ※ デフォルトは'SPREAD_KEY'
        """
        self._worksheet_name = work_sheet_name
        self.__spread_key = os.environ.get(variable_spread_key)
        self.__spread_sheet = self._authorize_spread_sheet()

    """"" スプレッドシートの認証 """""

    def _authorize_spread_sheet(self) -> gspread.Spreadsheet:
        try:
            credentials = self.get_credentials()
            credential_auth = gspread.authorize(credentials=credentials)
            sheet = credential_auth.open_by_key(self.__spread_key)
            print('スプレッドシートの認証が完了しました。')
            return sheet

        except APIError as error:
            print('スプレッドシートの認証に失敗しました。')
            raise error

        except SpreadsheetNotFound as error:
            print('スプレッドシートが見つかりません。')

    """"" ワークブックからワークシートを読み込む """""

    def read_worksheet(self) -> gspread.Worksheet:
        try:
            worksheet = self.__spread_sheet.get_worksheet(
                self._worksheet_name)
            print(f'{worksheet}の読み込みが完了しました。')

        except WorksheetNotFound as not_found_error:
            print(f'{self._worksheet_name}のワークシートが見つかりませんでした。')
            raise not_found_error

    @property
    def get_worksheet_name(self) -> gspread.Worksheet:
        return self._worksheet_name

    @get_worksheet_name.setter
    def set_work_sheet_name(self, name: str) -> None:
        if self._worksheet_name == '':
            self._worksheet_name = name
            return

        else:
            raise ValueError('既に値が入力されています。')


class SelfCareSheet(GoogleSheetsAPI):
    def __init__(self, work_sheet_name: str = '', variable_spread_key: str = 'SPREAD_KEY', scopes=None, refer_path_name='SERVICE_ACCOUNT_KEY'):
        super().__init__(work_sheet_name, variable_spread_key, scopes, refer_path_name)
        """
        work_sheet名が何も指定されていなかったら、
        「'鬱タイプ'」を設定する。
        """
        if self._worksheet_name == '':
            self.set_work_sheet_name = '鬱タイプ'
