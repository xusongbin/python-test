
import sys
import time
import json
import hashlib
import struct
import urllib.request
Host = 'http://127.0.0.1:8081/'


class TtApi(object):
    def __init__(self, account_key, secret_key):
        self.account_key = account_key
        self.secret_key = secret_key
        self.jm = ''

    @staticmethod
    def __fill(value, lens, fill_byte):
        if len(value) >= lens:
            return value
        else:
            fill_size = lens - len(value)
        return value + chr(fill_byte) * fill_size

    @staticmethod
    def __doXOr(s, value):
        slist = list(s.decode('utf-8'))
        for index in range(len(slist)):
            slist[index] = chr(ord(slist[index]) ^ value)
        return "".join(slist)

    def __hmacSign(self, aValue, aKey):
        keyb = struct.pack("%ds" % len(aKey), aKey.encode('utf-8'))
        value = struct.pack("%ds" % len(aValue), aValue.encode('utf-8'))
        k_ipad = self.__doXOr(keyb, 0x36)
        k_opad = self.__doXOr(keyb, 0x5c)
        k_ipad = self.__fill(k_ipad, 64, 54)
        k_opad = self.__fill(k_opad, 64, 92)
        m = hashlib.md5()
        m.update(k_ipad.encode('utf-8'))
        m.update(value)
        dg = m.digest()
        
        m = hashlib.md5()
        m.update(k_opad.encode('utf-8'))
        subStr = dg[0:16]
        m.update(subStr)
        dg = m.hexdigest()
        return dg

    def __api_call(self, path, params=''):
        try:
            sign = self.__hmacSign(params, self.secret_key)
            self.jm = sign
            reqTime = int(time.time()*1000)
            params += '&sign=%s&reqTime=%d'%(sign, reqTime)
            url = 'https:/api.ttex.com/' + path + '?' + params
            # url = Host + path + '?' + params
            req = urllib.request.Request(url)
            res = urllib.request.urlopen(req, timeout=10)
            doc = json.loads(res.read().decode("utf-8").replace('\0', ''))
            return doc
        except Exception as ex:
            print(sys.stderr, 'tt request ex: ', ex)
            return None

    def query_account(self):
        try:
            params = "accessKey="+self.account_key
            path = '/member/getAccount'

            obj = self.__api_call(path, params)
            # print(obj)
            return obj
        except Exception as ex:
            print(sys.stderr, 'tt query_account exception,',ex)
            return None

    def buy_price(self, symbol, num, price):
        try:
            params = "accessKey="+self.account_key+"&num="+str(num)+"&price="+str(price)+"&symbol="+symbol
            path = "currency/trade/buy"
            obj = self.__api_call(path,params)
            return obj
        except Exception as ex:
            print(sys.stderr, 'tt buy_price exception,', ex)
            return None

    def sell_price(self, symbol, num, price):
        try:
            params = "accessKey="+self.account_key+"&num="+str(num)+"&price="+str(price)+"&symbol="+symbol
            path = "currency/trade/sell"
            obj = self.__api_call(path, params)
            return obj
        except Exception as ex:
            print(sys.stderr, 'tt buy_price exception,', ex)
            return None

        
if __name__ == '__main__':
    access_key = 'accessKey'
    access_secret = 'secreteKey'

    api = TtApi(access_key, access_secret)
    print(api.query_account())
    # print(api.buy_price("eth_usdt",1.23,443.0))
