
from aip import AipOcr

APP_ID = '16318689'
API_KEY = '0VPqwji3gCrEBrnPq2iQy68G'
SECRET_KEY = 'GVecLAXZZfAavDW3crGPQFM0EeUppXAe'


def get_file_content(filepath):
    with open(filepath, 'rb') as f:
        return f.read()


def run():
    filepath = 'timg.jpg'
    content = get_file_content(filepath)
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    string = client.basicGeneral(content)
    print(string)


if __name__ == '__main__':
    run()
