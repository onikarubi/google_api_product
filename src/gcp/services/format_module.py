from typing import Dict, Tuple
from spread_sheet import SelfCareSheet
from gspread_formatting import *
from gspread import Worksheet
from gspread.exceptions import APIError

"""
セルのフォーマット

- セル範囲を指定
- セルフケアシートのプロパティ(month)から指定されている月の末日を取得
- 28日 ~ 31日の間で末尾が存在しない場合はセルの値を空白にして、BackGroundColorを全て白(デフォルト)にする
"""

def cell_format(work_sheet: Worksheet, cell_range: str, rgba: Tuple[int] = (1, 1, 1, 1)) -> bool:
    rgba = transform_rgba_color(rgba[0], rgba[1], rgba[2], rgba[3])
    fmt = CellFormat(
        backgroundColor=Color(
            red=rgba['red'],
            green=rgba['green'],
            blue=rgba['blue'],
            alpha=rgba['alpha']
        )
    )

    try:
        format_cell_range(work_sheet, cell_range, fmt)
        print('フォーマットの変更に成功しました。', f'result -> {cell_range}')
        return True

    except APIError as error:
        print(error, 'フォーマットの変更に失敗しました。')
        return False

def transform_rgba_color(red: int, green: int, blue: int, alpha: int = 1) -> Dict[str, float]:
    calculating_value = lambda x: x / 256

    colors = {
        "red": calculating_value(red),
        "green": calculating_value(green),
        "blue": calculating_value(blue),
        "alpha": alpha
    }

    return colors

if __name__ == '__main__':
    MAX_ROW = 31
    step_number = 2
    cell_left_num = 6
    cell_right_num = 7
    s = SelfCareSheet('鬱タイプ(検証用)')

    for i in range(1, MAX_ROW + 1):
        if not i == 1:
            cell_left_num += 2
            cell_right_num += 2

        cell_format(work_sheet=s.work_sheet, cell_range=f'A{cell_left_num}:AE{cell_right_num}', rgba=(0, 76, 256, 1))

