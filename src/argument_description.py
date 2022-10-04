from ast import Dict
from typing import List
import openpyxl
import pykakasi

kakasi = pykakasi.kakasi()
convert = kakasi.convert('吾輩は猫である。名前はまだ無い。')
print(convert)
result = ''.join([i['passport'] if i['passport'] != 'ha' else 'wa' for i in convert]).capitalize()
list_result = list(result)

for r in range(len(list_result)):
    if not r == 0:
        if list_result[r - 1] == '.':
            list_result[r] = list_result[r].upper()

result = ''.join(list_result)

print(result)

class ControlExcel(object):
    def __init__(self, xlsx_path) -> None:
        self.xlsx_path = xlsx_path
        self._words: List[Dict[str, str]] = self.get_words

    def get_words(self, str):
        return kakasi.convert(str)




