#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import string
import random
import requests
from urllib.parse import quote
from hashlib import md5
from time import time, strftime, localtime


class BitAtm(object):
    # 市场行情
    market_history_kline = '/market/history.kline'  # K线
    market_detail_merged = '/market/detail.merged'  # 单个symbol滚动24小时交易和最优报价聚合行情
    market_detail = '/market/detail'                # 单个symbol滚动24小时交易聚合行情
    market_tickers = '/market/tickers'              # 全部symbol的交易行情
    market_depth = '/market/depth'                  # 单个symbol市场深度行情
    market_trade = '/market/trade'                  # 单个symbol最新成交记录
    market_history_trade = '/market/history.trade'  # 单个symbol批量成交记录

    # 通用
    common_symbols = '/v1/common/symbols'           # 交易品种的计价货币和报价精度
    common_currencies = '/v1/common/currencies'     # 交易币种列表
    common_rate = '/v1/common/rate'                 # 汇率
    common_timestamp = '/v1/common/timestamp'       # 查询当前系统时间(UTC时间戳)

    # 账户
    account_accounts = '/v1/account/accounts'       # 查询用户的所有账户状态
    account_balance = '/v1/account/balance'         # 查询指定账户余额

    # 订单
    order_create = '/v1/order/create'               # 下单
    order_cancel = '/v1/order/cancel'               # 撤销一个订单
    order_batch_cancel = '/v1/order/batch.cancel'   # 按orderid批量撤销订单(max:30)
    order_detail = '/v1/order/detail'               # 根据orderid查询订单详情
    order_orders = '/v1/order/orders'               # 查询用户当前委托、或历史委托订单

    # 用户
    user_withdraw_create = '/v1/user/withdraw/create'   # 申请提币
    user_withdraw_revoke = '/v1/user/withdraw/revoke'   # 撤销提币申请
    user_query_deposit = '/v1/user/query/deposit-withdraw'  # 查询充提记录

    def __init__(self):
        self.access_key = ''
        self.secret_key = ''
        try:
            with open('BitATM.log', 'r') as f:
                key = json.load(f)
            self.access_key = key['Access_key']
            self.secret_key = key['Secret_key']
        except Exception as e:
            print('Load key except: %s' % e)
        self.type_name = 'Content-Type'
        self.type_get = 'application/x-www-form-urlencoded'
        self.type_post = 'application/json'
        self.url = 'https://open.bitatm.com'

    @staticmethod
    def do_random():
        random_str = ''.join(random.sample(string.ascii_letters, 10))
        tms = int(time() * 1000)
        return random_str, tms

    # 获取签名
    def do_signature(self, randstr, timestamp):
        # Signature=MD5(urlencode(sortedlist(p1=xxx&p2=xxx&...&secretkey=您的密钥).lower(),'utf-8'))
        # Signature：签名计算后的结果(32位长度的字符串，此参数必须传递到请求中，服务器端通过此参数验证请求的合法性)，
        # 注意：（&secretkey=您的密钥）是放在最后
        #
        # MD5()：加密方法，请勿遗漏；
        # urlencode()：参数字符串编码方式，采用utf-8编码；
        # sortedlist()：以参数的字母升序排序(a-z)，注意：secretkey不参与排序;
        # lower()：字符串转小写；
        # 以上计算公式为伪代码，具体签名方式请看代码实例。
        #
        # 案例：查询指定账户余额
        # 第一步签名参数：
        # accesskey=c4c93b56-7bf1-4b11-8fa4-db6075f096b2&
        # randstr=22fe319c-505a-11e9-a16c-f44d30581234&timestamp=1561628611&
        # secretkey=577d2b39-5c9e-426d-b912-06ce4b5bb18d
        # 第二步urlencode：
        # accesskey%3dc4c93b56-7bf1-4b11-8fa4-db6075f096b2%26
        # randstr%3d22fe319c-505a-11e9-a16c-f44d30581234%26
        # timestamp%3d1561628611%26
        # secretkey%3d577d2b39-5c9e-426d-b912-06ce4b5bb18d
        #
        # 第三步MD5签名结果为：
        # 54771913787c7e4390acc0fccbd51ffe
        #
        # 第四步请求URL为：
        # https://open.bitatm.com/v1/account/balance?
        # AccessKey=c4c93b56-7bf1-4b11-8fa4-db6075f096b2&
        # RandStr=22fe319c-505a-11e9-a16c-f44d30581234&
        # Timestamp=1561628611&
        # Signature=54771913787c7e4390acc0fccbd51ffe
        signatue_key = 'accesskey={}&randstr={}&timestamp={}&secretkey={}'.format(
            self.access_key,
            randstr,
            timestamp,
            self.secret_key
        )
        url_str = quote(signatue_key).lower()
        url_byte = url_str.encode()
        md5_maker = md5()
        md5_maker.update(url_byte)
        signatue_str = md5_maker.hexdigest()
        return signatue_str

    # GET/market/history.kline K线
    def do_market_history_kline(self, symbol='burstbhd', period='1min', size=500):
        # 请求参数：
        # 参数名称  是否必须 类型             描述      默认值   取值范围
        # Symbol    True    String          交易对              btcusdt,bchbtc,rcneth…
        # Period    True    String          K线类型             1min,5min,15min,30min,60min,1day,1week,1mon
        # Size      False   Integer($int32) 获取数量    500     [1~1000]
        #
        # 请求实例：
        # GET /market/history.kline?Symbol=btcusdt&Period=1min&Size=200
        #
        # 响应参数：
        # 参数名称  是否必须 类型            描述                       取值范围
        # code      True    String          请求处理响应码
        # msg       True    String          请求处理响应消息
        # ts        True    Integer($int64) 服务器响应时间戳(UTC,毫秒)
        # data      True    Object          响应数据
        # data数据结构说明
        # symbol    True    String          交易对                     btcusdt,bchbtc,rcneth…
        # amount    True    Number($double) 成交量
        # open      True    Number($double) 开盘价
        # close     True    Number($double) 收盘价（当K线为最晚的一根时，是最新成交价）
        # low       True    Number($double) 最低价
        # high      True    Number($double) 最高价
        # ts        True    Integer($int64) 时间戳
        headers = {self.type_name: self.type_get}
        value = '?Symbol={}&Period={}&Size={}'.format(symbol, period, size)
        try:
            resp = requests.get(self.url + self.market_history_kline + value, headers=headers)
            rd = json.loads(resp.text)
            if rd['code'] == '200' and rd['msg'].upper() == 'OK.':
                return rd['data']
            else:
                print(rd)
        except Exception as e:
            print('do_market_history_kline:%s' % e)
        return None

    # GET/market/detail.merged单个symbol滚动24小时交易和最优报价聚合行情
    def do_market_detail_merged(self, symbol='burstbhd'):
        # 请求参数：
        # 参数名称  是否必须 类型     描述      默认值  取值范围
        # Symbol    True    String   交易对            btcusdt,bchbtc,rcneth…
        #
        # 请求实例：
        # GET/market/detail.merged?Symbol=btcusdt
        #
        # 响应参数：
        # 参数名称  是否必须    类型          描述                      取值范围
        # code      True    String          请求处理响应码
        # msg       True    String          请求处理响应消息
        # ts        True    Integer($int64) 服务器响应时间戳(UTC,毫秒)
        # data      True    Object          响应数据
        # data数据结构说明
        # symbol    True    String          交易对                     btcusdt,bchbtc,rcneth…
        # amount    True    Number($double) 成交量
        # open      True    Number($double) 开盘价
        # close     True    Number($double) 收盘价（当K线为最晚的一根时，是最新成交价）
        # low       True    Number($double) 最低价
        # high      True    Number($double) 最高价
        # ts        True    Integer($int64) 时间戳
        headers = {self.type_name: self.type_get}
        value = '?Symbol={}'.format(symbol)
        try:
            resp = requests.get(self.url + self.market_detail_merged + value, headers=headers)
            rd = json.loads(resp.text)
            if rd['code'] == '200' and rd['msg'].upper() == 'OK.':
                return rd['data']
            else:
                print(rd)
        except Exception as e:
            print('do_market_detail_merged:%s' % e)
        return None

    # GET/market/detail单个symbol滚动24小时交易聚合行情
    def do_market_detail(self, symbol='burstbhd'):
        # 请求参数：
        # 参数名称  是否必须 类型     描述      默认值  取值范围
        # Symbol    True    String   交易对            btcusdt,bchbtc,rcneth…
        #
        # 请求实例：
        # GET/market/detail?Symbol=btcusdt
        #
        # 响应参数：
        # 参数名称  是否必须    类型          描述                      取值范围
        # code      True    String          请求处理响应码
        # msg       True    String          请求处理响应消息
        # ts        True    Integer($int64) 服务器响应时间戳(UTC,毫秒)
        # data      True    Object          响应数据
        # data数据结构说明
        # symbol    True    String          交易对                     btcusdt,bchbtc,rcneth…
        # amount    True    Number($double) 成交量
        # open      True    Number($double) 开盘价
        # close     True    Number($double) 收盘价（当K线为最晚的一根时，是最新成交价）
        # low       True    Number($double) 最低价
        # high      True    Number($double) 最高价
        # ts        True    Integer($int64) 时间戳
        headers = {self.type_name: self.type_get}
        value = '?Symbol={}'.format(symbol)
        try:
            resp = requests.get(self.url + self.market_detail + value, headers=headers)
            rd = json.loads(resp.text)
            if rd['code'] == '200' and rd['msg'].upper() == 'OK.':
                return rd['data']
            else:
                print(rd)
        except Exception as e:
            print('do_market_detail:%s' % e)
        return None

    # GET/market/tickers全部symbol的交易行情
    def do_market_tickers(self):
        # 请求参数：
        # 参数名称  是否必须    类型  描述  默认值 取值范围
        #
        # 请求实例：
        # GET/market/tickers
        #
        # 响应数据：
        # 参数名称  是否必须     类型             描述                      取值范围
        # code      True        String          请求处理响应码
        # msg       True        String          请求处理响应消息
        # ts        True        Integer($int64) 服务器响应时间戳(UTC,毫秒)
        # data      True        List[Object]    响应数据
        # data数据结构说明
        # symbol    True        String          交易对                     btcusdt,bchbtc,rcneth…
        # amount    True        Number($double) 成交量
        # open      True        Number($double) 开盘价
        # close     True        Number($double) 收盘价（当K线为最晚的一根时，是最新成交价）
        # low       True        Number($double) 最低价
        # high      True        Number($double) 最高价
        # ts        True        Integer($int64) 时间戳
        headers = {self.type_name: self.type_get}
        try:
            resp = requests.get(self.url + self.market_tickers, headers=headers)
            rd = json.loads(resp.text)
            if rd['code'] == '200' and rd['msg'].upper() == 'OK.':
                return rd['data']
            else:
                print(rd)
        except Exception as e:
            print('do_market_tickers:%s' % e)
        return None

    # GET/market/depth单个symbol市场深度行情
    def do_market_depth(self, symbol='burstbhd'):
        # 请求参数：
        # 参数名称  是否必须     类型         描述      默认值         取值范围
        # Symbol    True        String      交易对                 btcusdt,bchbtc,rcneth…
        #
        # 请求实例：
        # GET/market/depth?Symbol=btcusdt
        #
        # 响应数据：
        # 参数名称  是否必须     类型             描述                      取值范围
        # code      True        String          请求处理响应码
        # msg       True        String          请求处理响应消息
        # ts        True        Integer($int64) 服务器响应时间戳(UTC,毫秒)
        # data      True        Object          响应数据
        # data数据结构说明
        # bids      True        List[Object]    买盘信息[{price:成交价,amount:成交量}]按price降序
        # asks      True        List[Object]    卖盘信息[{price:成交价,amount:成交量}]按price升序
        # ts        True        Integer($int64) 时间戳
        headers = {self.type_name: self.type_get}
        value = '?Symbol={}'.format(symbol)
        try:
            resp = requests.get(self.url + self.market_depth + value, headers=headers)
            rd = json.loads(resp.text)
            if rd['code'] == '200' and rd['msg'].upper() == 'OK.':
                return rd['data']
            else:
                print(rd)
        except Exception as e:
            print('do_market_depth:%s' % e)
        return None

    # GET/market/trade单个symbol最新成交记录
    def do_market_trade(self, symbol='burstbhd'):
        # 请求参数：
        # 参数名称  是否必须     类型     描述      默认值         取值范围
        # Symbol    True        String  交易对                 btcusdt,bchbtc,rcneth…
        #
        # 请求参数：
        # GET/market/trade?Symbol=btcusdt
        #
        # 响应参数：
        # 参数名称  是否必须     类型             描述                          取值范围
        # code      True        String          请求处理响应码
        # msg       True        String          请求处理响应消息
        # ts        True        Integer($int64) 服务器响应时间戳(UTC,毫秒)
        # data      True        Object          响应数据
        # data数据结构说明
        # price     True        Number($double) 成交价
        # amount    True        Number($double) 成交量
        # direction True        Integer($int32) 主动成交方向(1:买入,-1:卖出)  [1,-1]
        # ts        True        Integer($int64) 时间戳
        headers = {self.type_name: self.type_get}
        value = '?Symbol={}'.format(symbol)
        try:
            resp = requests.get(self.url + self.market_trade + value, headers=headers)
            rd = json.loads(resp.text)
            if rd['code'] == '200' and rd['msg'].upper() == 'OK.':
                return rd['data']
            else:
                print(rd)
        except Exception as e:
            print('do_market_trade:%s' % e)
        return None

    # GET/market/history.trade单个symbol批量成交记录
    def do_market_history_trade(self, symbol='burstbhd', size=1):
        # 请求参数：
        # 参数名称  是否必须     类型             描述              默认值         取值范围
        # Symbol    True        String          交易对                         btcusdt,bchbtc,rcneth…
        # Size      False       Integer($int32) 获取交易记录的数量   1           [1~1000]
        #
        # 请求参数：
        # GET/market/history.trade?Symbol=btcusdt&Size=200
        #
        # 响应参数：
        # 参数名称  是否必须     类型             描述                          取值范围
        # code      True        String          请求处理响应码
        # msg       True        String          请求处理响应消息
        # ts        True        Integer($int64) 服务器响应时间戳(UTC,毫秒)
        # data      True        List[Object]    响应数据
        # data数据结构说明
        # price     True        Number($double) 成交价
        # amount    True        Number($double) 成交量
        # direction True        Integer($int32) 主动成交方向(1:买入,-1:卖出)  [1,-1]
        # ts        True        Integer($int64) 时间戳
        headers = {self.type_name: self.type_get}
        value = '?Symbol={}&Size={}'.format(symbol, size)
        try:
            resp = requests.get(self.url + self.market_history_trade + value, headers=headers)
            rd = json.loads(resp.text)
            if rd['code'] == '200' and rd['msg'].upper() == 'OK.':
                return rd['data']
            else:
                print(rd)
        except Exception as e:
            print('do_market_history_trade:%s' % e)
        return None

    # GET/v1/common/symbols交易品种的计价货币和报价精度
    def do_common_symbols(self):
        # 请求参数：
        # 参数名称  是否必须     类型     描述      默认值         取值范围
        #
        # 请求实例：
        # GET/v1/common/symbols
        #
        # 响应参数：
        # 参数名称  是否必须     类型             描述                          取值范围
        # code      True        String          请求处理响应码
        # msg       True        String          请求处理响应消息
        # ts        True        Integer($int64) 服务器响应时间戳(UTC,毫秒)
        # data      True        List[Object]    响应数据
        # data数据结构说明
        # id        True        Integer($int64) 交易ID
        # basecurrency  True    String          基础币种
        # quotecurrency True    String          计价币种
        # symbol        True    String          交易对
        # priceprecision    True    String      价格精度位数（0为个位）
        # amountprecision   True    String      数量精度位数（0为各位）
        headers = {self.type_name: self.type_get}
        try:
            resp = requests.get(self.url + self.common_symbols, headers=headers)
            rd = json.loads(resp.text)
            if rd['code'] == '200' and rd['msg'].upper() == 'OK.':
                return rd['data']
            else:
                print(rd)
        except Exception as e:
            print('do_common_symbols:%s' % e)
        return None

    # GET/v1/common/currencies交易币种列表
    def do_common_currencies(self):
        # 请求参数：
        # 参数名称  是否必须     类型     描述      默认值         取值范围
        #
        # 请求实例：
        # GET/v1/common/currencies
        #
        # 响应参数：
        # 参数名称  是否必须     类型             描述                          取值范围
        # code      True        String          请求处理响应码
        # msg       True        String          请求处理响应消息
        # ts        True        Integer($int64) 服务器响应时间戳(UTC,毫秒)
        # data      True        List[Object]    响应数据
        # data数据结构说明
        # id        True        Integer($int64) 交易ID
        # currencyname  True    String          币种名称
        headers = {self.type_name: self.type_get}
        try:
            resp = requests.get(self.url + self.common_currencies, headers=headers)
            rd = json.loads(resp.text)
            if rd['code'] == '200' and rd['msg'].upper() == 'OK.':
                return rd['data']
            else:
                print(rd)
        except Exception as e:
            print('do_common_currencies:%s' % e)
        return None

    # GET/v1/common/rate汇率
    def do_common_rate(self):
        # 请求参数：
        # 参数名称  是否必须     类型     描述      默认值         取值范围
        #
        # 请求实例：
        # GET/v1/common/rate
        #
        # 响应参数：
        # 参数名称  是否必须     类型             描述                          取值范围
        # code      True        String          请求处理响应码
        # msg       True        String          请求处理响应消息
        # ts        True        Integer($int64) 服务器响应时间戳(UTC,毫秒)
        # data      True        List[Object]    响应数据
        # data数据结构说明
        # currencyname  True    String          币种名称
        # rate          True    Number($double) 汇率
        # ts            True    Integer($int64) 更新时间戳
        headers = {self.type_name: self.type_get}
        try:
            resp = requests.get(self.url + self.common_rate, headers=headers)
            rd = json.loads(resp.text)
            if rd['code'] == '200' and rd['msg'].upper() == 'OK.':
                return rd['data']
            else:
                print(rd)
        except Exception as e:
            print('do_common_rate:%s' % e)
        return None

    # GET/v1/common/timestamp查询当前系统时间(UTC时间戳)
    def do_common_timestamp(self):
        # 请求参数：
        # 参数名称  是否必须     类型     描述      默认值         取值范围
        #
        # 请求实例：
        # GET/v1/common/timestamp
        #
        # 响应参数：
        # 参数名称  是否必须     类型             描述                          取值范围
        # code      True        String          请求处理响应码
        # msg       True        String          请求处理响应消息
        # ts        True        Integer($int64) 服务器响应时间戳(UTC,毫秒)
        # data      True        Object          响应数据(当前系统时间戳UTC)
        headers = {self.type_name: self.type_get}
        try:
            resp = requests.get(self.url + self.common_timestamp, headers=headers)
            rd = json.loads(resp.text)
            if rd['code'] == '200' and rd['msg'].upper() == 'OK.':
                return rd['data']
            else:
                print(rd)
        except Exception as e:
            print('do_common_timestamp:%s' % e)
        return None

    # GET/v1/account/accounts查询用户的所有账户状态
    def do_account_accounts(self):
        # 请求参数：
        # 参数名称  是否必须   类型           描述              默认值         取值范围
        # AccessKey True    String          API访问KEY
        # RandStr   True    String          随机字符串
        # Timestamp True    Integer($int64) 时间戳（UTC时区）
        # Signature True    String          签名结果（非签名字段）
        #
        # 请求实例：
        # GET/v1/account/accounts?
        # AccessKey=e12b3b62-8a2a-4bb0-a526-a63695485113&
        # RandStr=89320394&
        # Timestamp=1534409404916&
        # Signature=xxxxxxxxxxxxxxxxxxxxx
        #
        # 响应参数：
        # 参数名称  是否必须     类型             描述              取值范围
        # code      True        String          请求处理响应码
        # msg       True        String          请求处理响应消息
        # ts        True        Integer($int64) 服务器响应时间戳(UTC,毫秒)
        # data      True        List[Object]    响应数据
        # data数据结构说明
        # userid    True        Integer($int64) 用户id
        # type      True        String          账户类型
        # status    True        String          账户状态(pending:审核中,notpass:审核不通过,working:正常,frozen:已冻结)
        random_str, tms = self.do_random()
        headers = {self.type_name: self.type_get}
        signature = self.do_signature(random_str, tms)
        value = '?AccessKey={}&RandStr={}&Timestamp={}&Signature={}'.format(
            self.access_key,
            random_str,
            tms,
            signature
        )
        try:
            resp = requests.get(self.url + self.account_accounts + value, headers=headers)
            rd = json.loads(resp.text)
            if rd['code'] == '200' and rd['msg'].upper() == 'OK.':
                return rd['data']
            else:
                print(rd)
        except Exception as e:
            print('do_market_history_kline:%s' % e)
        return None

    # GET/v1/account/balance查询指定账户余额
    def do_account_balance(self):
        # 请求参数：
        # 参数名称  是否必须   类型           描述              默认值         取值范围
        # AccessKey True    String          API访问KEY
        # RandStr   True    String          随机字符串
        # Timestamp True    Integer($int64) 时间戳（UTC时区）
        # Signature True    String          签名结果（非签名字段）
        #
        # 请求实例：
        # GET/v1/account/balance?
        # AccessKey=e12b3b62-8a2a-4bb0-a526-a63695485113&
        # RandStr=89320394&
        # Timestamp=1534409404916&
        # Signature=xxxxxxxxxxxxxxxxxxxxx
        #
        # 响应参数：
        # 参数名称  是否必须     类型             描述                      取值范围
        # code      True        String          请求处理响应码
        # msg       True        String          请求处理响应消息
        # ts        True        Integer($int64) 服务器响应时间戳(UTC,毫秒)
        # data      True        List[Object]    响应数据
        # data数据结构说明
        # currency  True        String          币种名称
        # balance   True        Number($double) 余额
        # frozen    True        Number($double) 冻结
        random_str, tms = self.do_random()
        headers = {self.type_name: self.type_get}
        signature = self.do_signature(random_str, tms)
        value = '?AccessKey={}&RandStr={}&Timestamp={}&Signature={}'.format(
            self.access_key,
            random_str,
            tms,
            signature
        )
        try:
            resp = requests.get(self.url + self.account_balance + value, headers=headers)
            rd = json.loads(resp.text)
            if rd['code'] == '200' and rd['msg'].upper() == 'OK.':
                return rd['data']
            else:
                print(rd)
        except Exception as e:
            print('do_account_balance:%s' % e)
        return None

    # POST/v1/order/create下单
    def do_order_create(self, symbol='burstbhd', amount=0, ordertype='Limit', direction='Buy', price=0.0):
        # 请求参数：
        # 参数名称  是否必须 类型             描述                              默认值     取值范围
        # Symbol    True    String          交易对                                       btcusdt,bchbtc,rcneth…
        # Amount    True    Number($double) 限价单表示下单数量，市价买单时表示买多少钱，市价卖单时表示卖多少币
        # OrderType True    String          订单类型(limit限价单,market市价单)            [Limit,Market]
        # Direction True    String          交易方向(buy:买,sell:卖)                      [Buy,Sell]
        # Price     False   Number($double) 下单价格，市价单不传该参数
        # Source    False   String          订单来源
        # AccessKey True    String          API访问KEY
        # RandStr   True    String          随机字符串
        # Timestamp True    Integer($int64) 时间戳（UTC时区）
        # Signature True    String          签名结果（非签名字段）
        #
        # 请求实例：
        # POST/v1/order/create  {
        #  "symbol":"btcusdt",
        #  "amount":10,
        #  "ordertype":"Limit",
        #  "direction":"Buy",
        #  "price":2020,
        #  "source":"",
        #  "accesskey":"e12b3b62-8a2a-4bb0-a526-a63695485113",
        #  "randstr":"89320394",
        #  "timestamp":1534409404916,
        #  "signature":"xxxxxxxxxxxxxxxxxxxxx"
        # }
        #
        # 响应参数：
        # 参数名称  是否必须     类型             描述                      取值范围
        # code      True        String          请求处理响应码
        # msg       True        String          请求处理响应消息
        # ts        True        Integer($int64) 服务器响应时间戳(UTC,毫秒)
        # data      True        Integer($int64) 成功返回订单ID
        random_str, tms = self.do_random()
        headers = {self.type_name: self.type_post}
        signature = self.do_signature(random_str, tms)
        if ordertype == 'Market':
            price = 0
        value = {
            'symbol': symbol,
            'amount': amount,
            'ordertype': ordertype,
            'direction': direction,
            'price': price,
            'source': '',
            'accesskey': self.access_key,
            'randstr': random_str,
            'timestamp': tms,
            'signature': signature
        }
        try:
            session = requests.session()
            resp = session.post(self.url + self.order_create, data=value, headers=headers)
            rd = json.loads(resp.text)
            if rd['code'] == '200' and rd['msg'].upper() == 'OK.':
                return rd['data']
            else:
                print(rd)
        except Exception as e:
            print('do_order_create:%s' % e)
        return None

    # POST/v1/order/cancel撤销一个订单
    def do_order_cancel(self, orderid):
        # 请求参数：
        # 参数名称  是否必须 类型             描述                 默认值     取值范围
        # OrderID   True    Integer($int64) 订单ID
        # AccessKey True    String          API访问KEY
        # RandStr   True    String          随机字符串
        # Timestamp True    Integer($int64) 时间戳（UTC时区）
        # Signature True    String          签名结果（非签名字段）
        #
        # 请求实例：
        # POST  /v1/order/cancel {
        #  "orderid":129332000293,
        #  "accesskey":"e12b3b62-8a2a-4bb0-a526-a63695485113",
        #  "randstr":"89320394",
        #  "timestamp":1534409404916,
        #  "signature":"xxxxxxxxxxxxxxxxxxxxx "
        # }
        #
        # 响应参数：
        # 参数名称  是否必须     类型             描述                      取值范围
        # code      True        String          请求处理响应码
        # msg       True        String          请求处理响应消息
        # ts        True        Integer($int64) 服务器响应时间戳(UTC,毫秒)
        # data      True        Integer($int64) 成功返回订单ID
        random_str, tms = self.do_random()
        headers = {self.type_name: self.type_post}
        signature = self.do_signature(random_str, tms)
        value = {
            'orderid': orderid,
            'accesskey': self.access_key,
            'randstr': random_str,
            'timestamp': tms,
            'signature': signature
        }
        try:
            session = requests.session()
            resp = session.post(self.url + self.order_cancel, data=value, headers=headers)
            rd = json.loads(resp.text)
            if rd['code'] == '200' and rd['msg'].upper() == 'OK.':
                return rd['data']
            else:
                print(rd)
        except Exception as e:
            print('do_order_cancel:%s' % e)
        return None


def main():
    bit = BitAtm()
    sta = bit.do_order_create(symbol='burstbhd', amount=1, ordertype='Limit', direction='Buy', price=0.0001)
    # sta = bit.do_account_balance()
    print(sta)


if __name__ == '__main__':
    main()
