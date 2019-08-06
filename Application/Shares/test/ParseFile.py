
import time


class ParseFile(object):
    def __init__(self):
        self.f_data = b''
        self.d_head = ''
        self.d_count = 0
        self.d_start = 0
        self.d_length = 0
        self.d_column = 0
        self.d_string = ''

    def data_get_head(self):
        return self.f_data[0:6].decode()

    def data_get_count(self):
        return int.from_bytes(self.f_data[6:10], byteorder='little')

    def data_get_start(self):
        return int.from_bytes(self.f_data[10:12], byteorder='little')

    def data_get_length(self):
        return int.from_bytes(self.f_data[12:14], byteorder='little')

    def data_get_column(self):
        return int.from_bytes(self.f_data[14:16], byteorder='little')

    def data_get_string(self):
        # print(self.f_data[16:16+self.d_length].hex().upper())
        _start = 16
        _str = ''
        for i in range(0, self.d_length, 4):
            _str += '%d\t' % int.from_bytes(self.f_data[_start+i:_start+i+3], byteorder='little')
        return _str

    def load(self, f_name):
        with open(f_name, 'rb') as f:
            self.f_data = f.read()
        self.d_head = self.data_get_head()
        self.d_count = self.data_get_count()
        self.d_start = self.data_get_start()
        self.d_length = self.data_get_length()
        self.d_column = self.data_get_column()
        self.d_string = self.data_get_string()

    def show(self):
        print('文件标识：%s' % self.d_head)
        print('记录数量：%d' % self.d_count)
        print('起始位置：%d' % self.d_start)
        print('记录长度：%d' % self.d_length)
        print('总列数量：%d' % self.d_column)
        print('每列标签：%s' % self.d_string)


if __name__ == '__main__':
    pf = ParseFile()
    pf.load('1A0001.mn5')
    pf.show()
