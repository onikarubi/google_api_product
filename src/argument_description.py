
def push_list(lst=[]):
    # 関数の引数にデフォルト値で設定した空の配列に対して、'追加'という文字を追加する
    lst.append("追加")

    return lst


func1 = push_list()
print(func1)  # 出力結果 -> ['追加']

func2 = push_list()
print(func2)  # 出力結果 -> ['追加', '追加']


"""
インスタンス生成時にコンストラクタメソッドが2回呼び出されるため、
インスタンス変数(lst)に'追加'という文字が2回格納される。
"""


class SampleClass(object):
    def __init__(self, lst=[]):
        self.lst = lst
        self.lst.append('追加')


sample_class1 = SampleClass()
sample_class2 = SampleClass()

print(sample_class1.lst)  # 出力結果 -> ['追加', '追加']
print(sample_class2.lst)  # 出力結果 -> ['追加', '追加']


def push_list2(lst=None):
    if lst is None:
        lst = []

    lst.append('追加')
    return lst


func3 = push_list2()
print(func3)  # 出力結果 -> ['追加']
func4 = push_list2()
print(func4)  # 出力結果 -> ['追加']
