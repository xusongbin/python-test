#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import string
import random
from urllib import request
from urllib import parse
from hashlib import md5
from time import time


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

    # 错误代码
    code_error = {
        -1: '业务执行失败',
        -99: '系统异常',
        -40001: '授权错误',
        -40003: '缺少必要的参数',
        -40004: '非法参数(类型错误)',
        -5001: '数据签名校验失败',
        -9000: '错误的请求',
        -9001: '参数取值范围错误',
        -9002: '交易对不存在',
        -9003: '币种不存在',
        -9004: '错误的日期格式',
        -9005: '余额不足无法冻结',
        -9006: '错误的签名方法',
        9000: '请求数据有效'
    }

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
        random_str = ''.join(random.sample(string.ascii_letters, random.randint(10, 20)))
        tms = int(time() * 1000)
        return random_str, tms

    def do_error_check(self, rd):
        try:
            code = int(rd['code'])
            if code == 200 and 'OK' in rd['msg'].upper():
                return rd['data']
            else:
                if code in self.code_error.keys():
                    print(self.code_error[code])
                print(rd)
        except Exception as e:
            print('do_error_check:%s' % e)
        return None

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
            self.access_key, randstr, timestamp, self.secret_key
        )
        url_str = parse.quote(signatue_key).lower()
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
            resp = request.urlopen(request.Request(self.url + self.market_history_kline + value, headers=headers))
            return self.do_error_check(json.loads(resp.read().decode()))
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
            resp = request.urlopen(request.Request(self.url + self.market_detail_merged + value, headers=headers))
            return self.do_error_check(json.loads(resp.read().decode()))
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
            resp = request.urlopen(request.Request(self.url + self.market_detail + value, headers=headers))
            return self.do_error_check(json.loads(resp.read().decode()))
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
            resp = request.urlopen(request.Request(self.url + self.market_tickers, headers=headers))
            return self.do_error_check(json.loads(resp.read().decode()))
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
            resp = request.urlopen(request.Request(self.url + self.market_depth + value, headers=headers))
            return self.do_error_check(json.loads(resp.read().decode()))
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
            resp = request.urlopen(request.Request(self.url + self.market_trade + value, headers=headers))
            return self.do_error_check(json.loads(resp.read().decode()))
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
            resp = request.urlopen(request.Request(self.url + self.market_history_trade + value, headers=headers))
            return self.do_error_check(json.loads(resp.read().decode()))
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
            resp = request.urlopen(request.Request(self.url + self.common_symbols, headers=headers))
            return self.do_error_check(json.loads(resp.read().decode()))
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
            resp = request.urlopen(request.Request(self.url + self.common_currencies, headers=headers))
            return self.do_error_check(json.loads(resp.read().decode()))
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
            resp = request.urlopen(request.Request(self.url + self.common_rate, headers=headers))
            return self.do_error_check(json.loads(resp.read().decode()))
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
            resp = request.urlopen(request.Request(self.url + self.common_timestamp, headers=headers))
            return self.do_error_check(json.loads(resp.read().decode()))
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
            self.access_key, random_str, tms, signature
        )
        try:
            resp = request.urlopen(request.Request(self.url + self.account_accounts + value, headers=headers))
            return self.do_error_check(json.loads(resp.read().decode()))
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
            self.access_key, random_str, tms, signature
        )
        try:
            resp = request.urlopen(request.Request(self.url + self.account_balance + value, headers=headers))
            return self.do_error_check(json.loads(resp.read().decode()))
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
            value = parse.urlencode(value).encode('utf-8')
            resp = request.urlopen(request.Request(self.url + self.order_create, data=value, headers=headers))
            return self.do_error_check(json.loads(resp.read().decode()))
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
            value = parse.urlencode(value).encode('utf-8')
            resp = request.urlopen(request.Request(self.url + self.order_cancel, data=value, headers=headers))
            return self.do_error_check(json.loads(resp.read().decode()))
        except Exception as e:
            print('do_order_cancel:%s' % e)
        return None

    # POST/v1/order/batch.cancel按orderid批量撤销订单(max:30)
    def do_order_batch_cancel(self, orderid):
        # 请求参数：
        # 参数名称  是否必须 类型             描述                 默认值     取值范围
        # OrderID   True    Integer($int64) 订单ID
        # AccessKey True    String          API访问KEY
        # RandStr   True    String          随机字符串
        # Timestamp True    Integer($int64) 时间戳（UTC时区）
        # Signature True    String          签名结果（非签名字段）
        #
        # 请求实例：
        # POST  /v1/order/batch.cancel {
        #  "orderid":[
        # 1000300224,
        # 1000300225
        #  ],
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
        # data      True        List[Object]    成功返回订单ID集合
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
            value = parse.urlencode(value).encode('utf-8')
            resp = request.urlopen(request.Request(self.url + self.order_batch_cancel, data=value, headers=headers))
            return self.do_error_check(json.loads(resp.read().decode()))
        except Exception as e:
            print('do_order_batch_cancel:%s' % e)
        return None

    # GET/v1/order/detail根据orderid查询订单详情
    def do_order_detail(self, orderid):
        # 请求参数：
        # 参数名称  是否必须 类型             描述                  默认值     取值范围
        # OrderID   True    Integer($int64) 订单ID
        # AccessKey True    String          API访问KEY
        # RandStr   True    String          随机字符串
        # Timestamp True    Integer($int64) 时间戳（UTC时区）
        # Signature True    String          签名结果（非签名字段）
        #
        # 请求实例：
        # GET/v1/order/detail?
        # OrderID=1000300224&
        # AccessKey=e12b3b62-8a2a-4bb0-a526-a63695485113&
        # RandStr=89320394&
        # Timestamp=1534409404916&
        # Signature=xxxxxxxxxxxxxxxxxxxxx
        #
        # 响应参数：
        # 参数名称      是否必须    类型          描述                      取值范围
        # code          True    String          请求处理响应码
        # msg           True    String          请求处理响应消息
        # ts            True    Integer($int64) 服务器响应时间戳(UTC,毫秒)
        # data          True    Object          成功返回订单信息
        # data数据结构说明
        # orderid       True    Integer($int64) 订单ID
        # ordertype     True    Integer($int32) 订单类型(1:限价单,2:市价单,3:止盈止损单)
        # direction     True    Integer($int32) 交易方向(1:买入,-1:卖出)
        # price         True    Number($double) 委托价
        # amount        True    Number($double) 委托量
        # transactionamount True    Number($double) 成交量
        # fee           True    Number($double) 手续费率
        # symbol        True    String          交易对                     btcusdt,bchbtc,rcneth…
        # orderstatus   True    Integer($int32) 订单状态
        # 订单状态(0:已提交，1:部分成交，2:已撤单，3:全部成交，4:部分成交已撤单，5：系统自动撤单)
        # updatetime    True    String($date-time)  最后成交时间（UTC时区）
        # createtime    True    String($date-time)  委托时间（UTC时区）
        # basecurrency  True    String          基础货币
        # quotecurrency True    String          计价货币
        random_str, tms = self.do_random()
        headers = {self.type_name: self.type_get}
        signature = self.do_signature(random_str, tms)
        value = '?OrderID={}&AccessKey={}&RandStr={}&Timestamp={}&Signature={}'.format(
            orderid, self.access_key, random_str, tms, signature
        )
        try:
            resp = request.urlopen(request.Request(self.url + self.order_detail + value, headers=headers))
            return self.do_error_check(json.loads(resp.read().decode()))
        except Exception as e:
            print('do_order_detail:%s' % e)
        return None

    # GET/v1/order/orders查询用户当前委托、或历史委托订单
    def do_order_orders(
            self, orderid=None, orderpye=None, orderstatus=None,
            symbol=None, direction=None, starttime=None, endtime=None,
            pageindex=1, pagesize=30
    ):
        # 请求参数：
        # 参数名称      是否必须 类型             描述      默认值         取值范围
        # OrderID       False   Integer($int64) 订单ID
        # OrderType     False   String          订单类型                Limit：限价单，Market：市价单
        # OrderStatus   False   String          订单状态
        # (0:已提交，1:部分成交，2:已撤单，3:全部成交，4:部分成交已撤单，5：系统自动撤单)例如：查询进行中的订单传0,1
        # Symbol        False   String          交易对                  btcusdt,bchbtc,rcneth…
        # Direction     False   String          交易方向                Buy：买入,Sell：卖出
        # StartTime     False   String          委托开始时间（UTC）
        # EndTime       False   String          委托结束时间（UTC）
        # PageIndex     False   Integer($int32) 当前页         1
        # PageSize      False   Integer($int32) 页大小         30          [30~500]
        # AccessKey True    String          API访问KEY
        # RandStr   True    String          随机字符串
        # Timestamp True    Integer($int64) 时间戳（UTC时区）
        # Signature True    String          签名结果（非签名字段）
        #
        # 请求实例：
        # GET/v1/order/orders?
        # OrderID=1000300224&
        # OrderType=Limit&
        # OrderStatus=0,1&
        # Symbol=btcusdt&
        # Direction=Buy&
        # StartTime=2018-08-27T08:38:56.003ZEndTime=2018-08-28T08:38:56.003Z&
        # PageIndex=1&
        # PageSize=30&
        # AccessKey=e12b3b62-8a2a-4bb0-a526-a63695485113&
        # RandStr=89320394&
        # Timestamp=1534409404916&
        # Signature=xxxxxxxxxxxxxxxxxxxxx
        #
        # 响应参数：
        # 参数名称      是否必须    类型                  描述                      取值范围
        # code          True    String                  请求处理响应码
        # msg           True    String                  请求处理响应消息
        # ts            True    Integer($int64)         服务器响应时间戳(UTC,毫秒)
        # data          True    Object                  成功返回订单信息
        # data数据结构说明
        # currentpageindex  True    Integer($int32)     当前页
        # pagesize          True    Integer($int32)     页大小
        # totalitemcount    True    Integer($int32)     总记录数
        # totalpagecount    True    Integer($int32)     总页数
        # haspreviouspage   True    Bool                是否有上一页
        # hasnextpage       True    Bool                是否有下一页
        # pagedata          True    Object              分页数据
        # pagedata数据结构说明
        # orderid           True    Integer($int64)     订单ID
        # ordertype         True    Integer($int32)     订单类型(1:限价单,2:市价单,3:止盈止损单)
        # direction         True    Integer($int32)     交易方向(1:买入,-1:卖出)
        # price             True    Number($double)     委托价
        # amount            True    Number($double)     委托量
        # transactionamount True    Number($double)     成交量
        # fee               True    Number($double)     手续费率
        # symbol            True    String              交易对         btcusdt,bchbtc,rcneth…
        # orderstatus       True    Integer($int32)     订单状态
        # 订单状态(0:已提交，1:部分成交，2:已撤单，3:全部成交，4:部分成交已撤单，5：系统自动撤单)
        # updatetime        True    String($date-time)  最后成交时间（UTC时区）
        # createtime        True    String($date-time)  委托时间（UTC时区）
        # basecurrency      True    String              基础货币
        # quotecurrency     True    String              计价货币
        random_str, tms = self.do_random()
        headers = {self.type_name: self.type_get}
        signature = self.do_signature(random_str, tms)
        value = '?'
        if orderid:
            value += 'OrderID={}&'.format(orderid)
        if orderpye:
            value += 'OrderType={}&'.format(orderpye)
        if orderstatus:
            value += 'OrderStatus={}&'.format(orderstatus)
        if symbol:
            value += 'Symbol={}&'.format(symbol)
        if direction:
            value += 'Direction={}&'.format(direction)
        if starttime and endtime:
            value += 'StartTime={}EndTime={}&'.format(starttime, endtime)
        if pageindex:
            value += 'PageIndex={}&'.format(pageindex)
        if pagesize:
            value += 'PageSize={}&'.format(pagesize)
        value += 'AccessKey={}&RandStr={}&Timestamp={}&Signature={}'.format(
            self.access_key, random_str, tms, signature
        )
        try:
            resp = request.urlopen(request.Request(self.url + self.order_orders + value, headers=headers))
            return self.do_error_check(json.loads(resp.read().decode()))
        except Exception as e:
            print('do_order_orders:%s' % e)
        return None

    # POST/v1/user/withdraw/create申请提币
    def do_user_withdraw_create(self, currency, address, amount, fee=0, addresstag=None):
        # 请求参数：
        # 参数名称  是否必须 类型             描述                 默认值     取值范围
        # Currency  True    String          币种                          btc,eth,ont...
        # Address   True    String          提币地址
        # Amount    True    Number($double) 提币数量
        # Fee       False   Number($double) 手续费
        # AddressTag    False   String      地址标签
        # AccessKey True    String          API访问KEY
        # RandStr   True    String          随机字符串
        # Timestamp True    Integer($int64) 时间戳（UTC时区）
        # Signature True    String          签名结果（非签名字段）
        #
        # 请求实例：
        # POST /v1/user/withdraw/create {
        #  "currency":"btc",
        #  "address": "13QtP7x9kbhyJCrf3UeHNgUEMoHbXhEvSt",
        #  "amount":10,
        #  "fee":0,
        #  "addresstag":"",
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
        # data数据结构说明
        # succeed       True    Bool            true:操作成功,false:操作失败
        # withdrawid    True    Integer($int64) 提币ID
        random_str, tms = self.do_random()
        headers = {self.type_name: self.type_post}
        signature = self.do_signature(random_str, tms)
        value = {
            'currency': currency,
            'address': address,
            'amount': amount,
            'fee': fee,
            'addresstag': addresstag,
            'accesskey': self.access_key,
            'randstr': random_str,
            'timestamp': tms,
            'signature': signature
        }
        try:
            value = parse.urlencode(value).encode('utf-8')
            resp = request.urlopen(request.Request(self.url + self.user_withdraw_create, data=value, headers=headers))
            return self.do_error_check(json.loads(resp.read().decode()))
        except Exception as e:
            print('do_user_withdraw_create:%s' % e)
        return None

    # POST/v1/user/withdraw/revoke撤销提币申请
    def do_user_withdraw_revoke(self, withdrawid):
        # 请求参数：
        # 参数名称      是否必须 类型             描述                 默认值     取值范围
        # WithdrawID    True    Integer($int64) 提币ID
        # AccessKey     True    String          API访问KEY
        # RandStr       True    String          随机字符串
        # Timestamp     True    Integer($int64) 时间戳（UTC时区）
        # Signature     True    String          签名结果（非签名字段）
        #
        # 请求实例：
        # POST /v1/user/withdraw/revoke {
        #  "withdrawid":245038294992,
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
        # data      True        Object          成功返回订单信息
        # data数据结构说明
        # succeed   True        Bool            true:操作成功,false:操作失败
        random_str, tms = self.do_random()
        headers = {self.type_name: self.type_post}
        signature = self.do_signature(random_str, tms)
        value = {
            'withdrawid': withdrawid,
            'accesskey': self.access_key,
            'randstr': random_str,
            'timestamp': tms,
            'signature': signature
        }
        try:
            value = parse.urlencode(value).encode('utf-8')
            resp = request.urlopen(request.Request(self.url + self.user_withdraw_create, data=value, headers=headers))
            return self.do_error_check(json.loads(resp.read().decode()))
        except Exception as e:
            print('do_user_withdraw_create:%s' % e)
        return None

    # GET/v1/user/query/deposit-withdraw查询充提记录
    def do_user_query_withdraw(self, currency, _type, pageindex=1, pagesize=30):
        # 请求参数：
        # 参数名称      是否必须     类型             描述              默认值     取值范围
        # Currency      True        String          币种
        # Type          True        String          类型                          deposit：充值、withdraw：提币
        # PageIndex     False       Integer($int32) 当前页             1
        # PageSize      False       Integer($int32) 页大小             30          [30~500]
        # AccessKey     True        String          API访问KEY
        # RandStr       True        String          随机字符串
        # Timestamp     True        Integer($int64) 时间戳（UTC时区）
        # Signature     True        String          签名结果（非签名字段）
        #
        # 请求实例：
        # GET/v1/user/query/deposit-withdraw?
        # Currency=btc&
        # Type=deposit&
        # PageIndex=1&
        # PageSize=30&
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
        # data      True        Object          成功返回订单信息
        # data数据结构说明
        # currentpageindex  True    Integer($int32)     当前页
        # pagesize          True    Integer($int32)     页大小
        # totalitemcount    True    Integer($int32)     总记录数
        # totalpagecount    True    Integer($int32)     总页数
        # haspreviouspage   True    Bool                是否有上一页
        # hasnextpage       True    Bool                是否有下一页
        # pagedata          True    Object              分页数据
        # pagedata数据结构说明
        # id        True        Integer($int64) 提币ID/充值ID
        # type      True        String          类型          deposit：充值、withdraw：提币
        # currency  True        String          币种          btc,eth,ont...
        # txhash    True        String          交易哈希
        # amount    True        Number($double) 量
        # factamount    True    Number($double) 成功到账量
        # address       True    String          地址
        # addresstag    True    String          地址标签
        # comfirmnode   True    Integer($int32) 确认节点数
        # fee           True    Number($double) 手续费
        # status        True    Integer($int32) 充值/提币状态
        # 充币状态（0:待处理,1:充币成功,2:充币失败）
        # 提币状态（0:待处理,1:提币成功,2:提币失败,3:提币审核中,4:审核不通过,5:已撤销）
        # updatetime    True    String($date-time)  最后成交时间（UTC时区）
        # createtime    True    String($date-time)  委托时间（UTC时区）
        random_str, tms = self.do_random()
        headers = {self.type_name: self.type_get}
        signature = self.do_signature(random_str, tms)
        value = ('?Currency={}&Type={}&PageIndex={}&PageSize={}&'
                 'AccessKey={}&RandStr={}&Timestamp={}&Signature={}').format(
            currency, _type, pageindex, pagesize,
            self.access_key, random_str, tms, signature
        )
        try:
            resp = request.urlopen(request.Request(self.url + self.user_query_deposit, data=value, headers=headers))
            return self.do_error_check(json.loads(resp.read().decode()))
        except Exception as e:
            print('do_user_query_withdraw:%s' % e)
        return None


def main():
    bit = BitAtm()
    sta = bit.do_market_history_kline()
    # sta = bit.do_market_detail_merged()
    # sta = bit.do_market_detail()
    # sta = bit.do_market_tickers()
    # sta = bit.do_market_depth()
    # sta = bit.do_market_trade()
    # sta = bit.do_market_history_trade()
    # print(sta)

    sta = bit.do_common_symbols()
    # sta = bit.do_common_currencies()
    # sta = bit.do_common_rate()
    # sta = bit.do_common_timestamp()
    print(sta)

    sta = bit.do_account_accounts()
    sta = bit.do_account_balance()
    print(sta)

    # sta = bit.do_order_create(symbol='burstbhd', amount=1, ordertype='Limit', direction='Buy', price=0.0002)
    # sta = bit.do_order_cancel(1)
    # sta = bit.do_order_batch_cancel([1, 2])
    # sta = bit.do_order_detail(1)
    # sta = bit.do_order_orders()
    # print(sta)


if __name__ == '__main__':
    main()
