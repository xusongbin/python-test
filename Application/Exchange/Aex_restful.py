#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
from urllib.parse import quote
from hashlib import md5
from time import time


class Aex(object):
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 6.1; WOW64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/70.0.3538.25 '
            'Safari/537.36 Core/1.70.3719.400 '
            'QQBrowser/10.5.3715.400'
        )
    }

    def __init__(self):
        self.access_key = ''
        self.secret_key = ''
        self.account_id = 0
        try:
            with open('Aex.log', 'r') as f:
                key = json.load(f)
            self.access_key = key['Access_key']
            self.secret_key = key['Secret_key']
            self.account_id = key['Account_id']
        except Exception as e:
            print('Load key except: %s' % e)
        print(self.access_key)
        print(self.secret_key)
        print(self.account_id)

    def get_md5(self, ts):
        # md5(key_用戶ID_skey_time)
        un_str = '{}_{}_{}_{}'.format(self.access_key, self.account_id, self.secret_key, ts)
        lw_str = quote(un_str).lower()
        encryptor = md5()
        encryptor.update(lw_str.encode())
        en_str = encryptor.hexdigest()
        return en_str

    def get_my_balance(self):
        url = 'https://api.aex.zone/getMyBalance.php'
        ts = int(time())
        en_str = self.get_md5(ts)
        data = {
            'key': self.access_key,
            'time': ts,
            'md5': en_str
        }
        session = requests.session()
        resp = session.post(url, headers=self.headers, data=data)
        print(resp.text)


if __name__ == '__main__':
    aex = Aex()
    aex.get_my_balance()
