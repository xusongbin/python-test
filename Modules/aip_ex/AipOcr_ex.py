
# 百度API，文字识别

from aip import AipOcr

SDK = 'https://cloud.baidu.com/doc/OCR/OCR-Python-SDK.html#.E9.80.9A.E7.94.A8.E6.96.87.E5.AD.97.E8.AF.86.E5.88.AB'

APP_ID = '16318689'
API_KEY = '0VPqwji3gCrEBrnPq2iQy68G'
SECRET_KEY = 'GVecLAXZZfAavDW3crGPQFM0EeUppXAe'


def get_file_content(filepath):
    with open(filepath, 'rb') as f:
        return f.read()


def run():
    filepath = 'image/code.jpg'
    content = get_file_content(filepath)
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    string = client.basicGeneral(content)
    print(string)


if __name__ == '__main__':
    run()
