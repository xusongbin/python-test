
from aip import AipSpeech

APP_ID = '16303559'
API_KEY = 'oLnq4TC4zLVBTqH2qiYgEQ7o'
SECRET_KEY = 'yeLqnwyTimVC9ToDS9kKKxln76U9xyMF'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# ffmpeg -i test.mp3 -f wav test.wav


def get_file_content(filepath):
    with open(filepath, 'rb') as f:
        return f.read()


rep = client.asr(get_file_content('test.wav'), 'wav', 16000, {'dev_pid': 1536})

for key in rep.keys():
    print('{}:{}'.format(key, rep[key]))
