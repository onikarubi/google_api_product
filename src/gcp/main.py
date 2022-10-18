class Main(object):
    def __init__(self, val='') -> None:
        self.val = val

        if self.val == '':
            self.val = 'test'

    def get_val(self):
        return self.val

m = Main(None)
print(m.val)
