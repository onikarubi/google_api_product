import datetime
from email.generator import Generator
import os
import gspread
import calendar
from typing import List
from gspread import WorksheetNotFound, SpreadsheetNotFound
from gspread.client import APIError
from src.gcp.services.google_cloud_api import GoogleCloudApi

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
        self._spread_key = os.environ.get(variable_spread_key)
        self._spread_sheet = self._authorize_spread_sheet()

    """"" スプレッドシートの認証 """""

    def _authorize_spread_sheet(self) -> gspread.Spreadsheet:
        try:
            credentials = self.get_credentials()
            credential_auth = gspread.authorize(credentials=credentials)
            book = credential_auth.open_by_key(self._spread_key)
            print(f'スプレッドシートの認証が完了しました。, ワークシート名: {book.sheet1.title}')
            return book

        except APIError as error:
            print('スプレッドシートの認証に失敗しました。')
            raise error

        except SpreadsheetNotFound as error:
            print('スプレッドシートが見つかりません。')

    """"" ワークブックからワークシートを読み込む """""

    def read_worksheet(self, name: str) -> gspread.Worksheet:
        try:
            worksheet = self._spread_sheet.worksheet(name)
            print(f'{worksheet.title}の読み込みが完了しました。')
            return worksheet

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

        else:
            raise ValueError('既に値が入力されています。')


class SelfCareSheet(GoogleSheetsAPI):
    def __init__(
        self,
        work_sheet_name: str = '',
        cell_all_range: str = 'A4:AE67',
        label_title_cell_range: str = 'D4:AE4',
        label_cell_range: str = 'D5:AE5',
        date_label_cell_range: str = 'A4:C5',
        calendar_label: str = 'A1:C2',
        variable_spread_key: str = 'SPREAD_KEY', scopes=None, refer_path_name='SERVICE_ACCOUNT_KEY'
    ):
        super().__init__(work_sheet_name, variable_spread_key, scopes, refer_path_name)

        """ work_sheet名が何も指定されていなかったら、 「'鬱タイプ'」を設定する。 """
        if self._worksheet_name == '':
            self.set_work_sheet_name = '鬱タイプ'

        self.work_sheet: gspread.Worksheet = self.read_worksheet(
            self._worksheet_name)

        self._cell_all_range: str = cell_all_range
        self._label_title_cell_range = label_title_cell_range  # ラベルの上にあるタイトルのセル範囲
        self._label_cell_range = label_cell_range  # ラベルのセル範囲
        self._date_cell_rage = date_label_cell_range  # 日付

        self._category_title_labels: List[str] = [
            t for t in self.filtering_values(self._label_title_cell_range)]
        self._category_labels: List[str] = [
            l for l in self.filtering_values(self._label_cell_range)]
        self._date_labels: List[str] = [
            d for d in self.filtering_values(self._date_cell_rage)]

        self._calendar_label_value = self.work_sheet.acell(
            calendar_label).value

        self._label_data = {
            'date_labels': self._date_labels,
            'label_titles': self._category_title_labels,
            'labels': self._category_labels,
            'month': self._calendar_label_value,
            'first_month_day': self._date_type_conversion(self._calendar_label_value),
            'month_last_day': self.get_month_last_day(self._calendar_label_value)
        }

    """
    引数に指定されたセルのラベルから値を抽出し、値を文字列で返す。
    また、改行コードの'\n'といった特殊文字は空白に変換する。
    ただし、セルの値が元から空白だった場合はスキップ。
    """


    def filtering_values(self, cell_range: str = '') -> Generator(str):
        work_sheet_range = self.work_sheet.range(cell_range)

        for w in work_sheet_range:
            if not w.value == '':
                yield w.value.replace('\n', '').replace('\u3000', '')

            else:
                continue

    """ 月の値を引数に当て、yyyy/mm/dd形式で初月の年月日をs文字列で返す。 """

    def _date_type_conversion(self, date_str: str) -> str:
        try:
            date_str = date_str.replace('月', '')
            date_int = int(date_str)
            date_info = datetime.date(year=2022, month=date_int, day=1)
            return str(date_info).replace('-', '/')

        except BaseException as error:
            message = "取得した値が正しくありません。\nデータ値が1~12の数字が指定されていて、" \
                "かつ月以外の余計な文字が入っていないか確認してください。"

            raise print(f'{error} -> {message}')

    def get_month_last_day(self, date_str: str) -> datetime.datetime:
        date_int = int(date_str.replace('月', ''))
        # 日数だけ返す。
        return calendar.monthrange(2022, date_int)[1]

    @property
    def get_all_cell_range(self) -> str:
        if not self._cell_all_range == '':
            return self._cell_all_range

        else:
            raise ValueError('セルの範囲が設定されていません。')

    @get_all_cell_range.setter
    def set_cell_rage(self, begin: str, end: str) -> None:
        if self._cell_all_range == '':
            join_str = f'{begin}:{end}'
            self._cell_all_range = join_str

        else:
            print('セル範囲の値が既に設定されています。')

    @property
    def get_label_data(self): return self._label_data

if __name__ == '__main__':
    print('Success')
    # s = SelfCareSheet('鬱タイプ (ValueException01)')
    # for k, v in s.get_label_data.items():

    #     print(k, v)
