#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import queue
import logging
from urllib import parse
from hashlib import md5
from time import time

import asyncio
from aiowebsocket.converses import AioWebSocket

import traceback
from md_logging import setup_log

setup_log()
write_log = logging.getLogger('AEX_AIOWEBSOCKET')


class Aex(object):
    url = 'wss://api.aex.zone/ws/v1'
    error = {
        0: '正常',
        # xx + 001 == == == == == == == == 系统错误码 == == == == == == == ==
        1001: '添加想要关注的交易对，删除已经关注的交易对',
        4001: '无效请求',
        5001: '未认证',
        6001: '已认证',
        7001: '系统繁忙',
        8001: '计价币不存在',
        9001: '交易币不存在',
        10001: '无效交易区',
        11001: '该币在当前交易区不可交易',
        12001: '请求频率限制',
        # xx + 002 == == == == == == == == 关注错误码 == == == == == == == ==
        1002: '关注数量超过限制',
        # xx + 006 == == == == == == == == 挂单错误码 == == == == == == == ==
        1006: '用户ID无效',
        2006: '无效交易类型',
        3006: '价格无效',
        4006: '数量无效',
        5006: '数量点位超过限制',
        6006: '数量超过最大限制',
        7006: '数量超过最小限制',
        8006: '价格超过最大限制',
        9006: '价格点位超过限制',
        10006: '交易金额小于最小限制',
        11006: '余额不足',
        12006: '数量精度配置错误',
        13006: '价格精度未配置, 或者配置错误',
        14006: '输入参数错误',
        # xx + 007 == == == == == == == == 撤销订单错误码 == == == == == == == ==
        1007: '用户ID无效',
        2007: '订单不存在',
        3007: '订单删除失败, 可能是订单被撮合, 或者已经被删除',
        4007: '订单ID无效',
        # xx + 008 == == == == == == == == 查询订单错误码 == == == == == == == ==
        1008: '订单不存在',
        # xx + 009 == == == == == == == == 查询成交记录错误码 == == == == == == == ==
        1009: '成交记录不存在'
    }
    cmd = {
        1: '深度变化通知，服务器主动通知客户端，服务器只通知已经通过2命令关注的交易对',
        2: '添加想要关注的交易对，删除已经关注的交易对',
        3: 'K线数据（尚未实现）',
        4: '签名认证',
        5: '获取所有币种余额',
        6: '下订单',
        7: '撤销订单',
        8: '根据订单ID查询单个订单信息',
        9: '根据成交ID查询单个成交记录',
        10: '根查询交易对信息',
        11: '根据tag查询多个订单信息',
        12: '根据tag查询多个成交记录信息',
        13: '查询所有有效的交易对',
        14: '查询指定交易对的成交记录',
        15: '查询指定交易对或者指定市场的行情数据'
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
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        write_log.debug('Key:{} Skey:{} Id:{}'.format(self.access_key, self.secret_key, self.account_id))

        self.qq_tx = queue.Queue()
        self.qq_rx = queue.Queue()

        self.do_command2(1, [
            {"market": "cnc", "coin": "btc"},
            {"market": "cnc", "coin": "eos"},
            {"market": "cnc", "coin": "eth"},
            {"market": "cnc", "coin": "doge"},
            {"market": "cnc", "coin": "etc"},
            {"market": "usdt", "coin": "btc"},
            {"market": "usdt", "coin": "eos"},
            {"market": "usdt", "coin": "eth"},
            {"market": "usdt", "coin": "doge"},
            {"market": "usdt", "coin": "etc"}
        ])
        # self.do_command4()
        # self.do_command5()

        self.run()

    async def startup(self):
        async with AioWebSocket(self.url) as aws:
            converse = aws.manipulator
            while True:
                if not self.qq_tx.empty():
                    data = self.qq_tx.get()
                    await converse.send(data)
                msg = await converse.receive()
                if msg:
                    print(msg)
                    self.qq_rx.put(msg)

    def run(self):
        try:
            asyncio.get_event_loop().run_until_complete(self.startup())
        except Exception as e:
            logging.error('{}\n{}'.format(e, traceback.format_exc()))

    def do_md5(self, ts):
        try:
            un_str = '{}_{}_{}_{}'.format(self.access_key, self.account_id, self.secret_key, ts)
            lw_str = parse.quote(un_str).lower()
            encryptor = md5()
            encryptor.update(lw_str.encode())
            en_str = encryptor.hexdigest()
            return en_str
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        return ''

    def do_parse_respond(self, resp):
        try:
            data = json.loads(resp)
            cmd = data['cmd']['type']
            error_num = data['cmd']['eno']
            if cmd not in self.cmd.keys():
                return '命令不存在'
            if error_num != 0:
                if error_num not in self.error.keys():
                    return '错误号未识别'
                else:
                    return self.error[error_num]
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
            return '解析数据异常'
        return data

    # 添加想要关注的交易对，删除已经关注的交易对
    def do_command2(self, _type, pairs):
        data = {
            'cmd': {
                'type': 2   # 关注交易对
            },
            # 关注类型: 1=添加关注的交易对, 2=删除关注的交易对
            'type': _type,
            # 准备关注的交易对数组(可1个以上) [{"market": "cnc","coin": "bhd"}]
            "pairs": pairs
        }
        self.qq_tx.put(json.dumps(data))

    # 签名认证
    def do_command4(self):
        ts = int(time())
        data = {
            'cmd': {
                'type': 4
            },
            'key': self.access_key,
            'time': ts,
            'md5': self.do_md5(ts)
        }
        self.qq_tx.put(json.dumps(data))

    # 获取所有币种余额
    def do_command5(self):
        data = {
            'cmd': {
                'type': 5   # 获取余额
            }
        }
        self.qq_tx.put(json.dumps(data))

    # 下订单
    def do_command6(self, price, amount, tag, market='cnc', coin='bhd', _type=1):
        data = {
            'cmd': {
                'type': 6   # 挂单
            },
            'market': market,   # 交易区, 定价币
            'coin': coin,       # 交易币
            'tag': tag,         # 用户自定义tag, 一个非负整数, 用来把订单和成交记录关联起来
            'type': _type,      # 挂单类型: 1=买单, 2=卖单
            'price': price,     # 价格
            'amount': amount    # 数量
        }
        self.qq_tx.put(json.dumps(data))

    # 撤销订单
    def do_command7(self, orderid, market='cnc', coin='bhd'):
        data = {
            'cmd': {
                'type': 7       # 撤单
            },
            'market': market,   # 交易区, 定价币
            'coin': coin,       # 交易币
            'orderid': orderid  # 订单ID
        }
        self.qq_tx.put(json.dumps(data))

    def do_command8(self, orderid, market='cnc', coin='bhd'):
        data = {
            'cmd': {
                'type': 8       # 查询订单信息
            },
            'market': market,   # 交易区, 定价币
            'coin': coin,       # 交易币
            'orderid': orderid  # 准备查询的订单ID
        }
        self.qq_tx.put(json.dumps(data))

    def do_command9(self, orderid, market='cnc', coin='bhd'):
        data = {
            'cmd': {
                'type': 9       # 查询成交记录
            },
            'market': market,   # 交易区, 定价币
            'coin': coin,       # 交易币
            'orderid': orderid  # 准备查询的成交记录ID
        }
        self.qq_tx.put(json.dumps(data))

    def do_command10(self, pairs):
        data = {
            'cmd': {
                'type': 10      # 查询交易对信息
            },
            'pairs': pairs      # 准备查询的交易对数组 [{'market': 'cnc', 'coin': 'bhd'}]
        }
        self.qq_tx.put(json.dumps(data))

    def do_command11(self, tag, since_order_id=1, market='cnc', coin='bhd'):
        data = {
            'cmd': {
                'type': 11      # 根据tag查询订单
            },
            'market': market,   # 交易区, 定价币
            'coin': coin,       # 交易币
            'tag': tag,         # 准备查询的tag
            'since_order_id': since_order_id         # 起始订单ID
        }
        self.qq_tx.put(json.dumps(data))

    # 根据tag查询多个成交记录信息
    def do_command12(self, tag, since_order_id=1, market='cnc', coin='bhd'):
        data = {
            'cmd': {
                'type': 12      # 根据tag查询成交记录
            },
            'market': market,   # 交易区, 定价币
            'coin': coin,       # 交易币
            'tag': tag,         # 准备查询的tag
            'since_order_id': since_order_id    # 起始成交记录ID
        }
        self.qq_tx.put(json.dumps(data))

    def do_command13(self):
        data = {
            'cmd': {
                'type': 13      # 查询有效交易对列表
            }
        }
        self.qq_tx.put(json.dumps(data))

    def do_command14(self, market='cnc', coin='bhd', since_order_id=1):
        data = {
            'cmd': {
                'type': 14      # 查询指定交易对的成交记录
            },
            'pair': {
                'market': market,   # 市场
                'coin': coin        # 币名
            },
            'since_order_id': since_order_id   # 从哪个成交记录ID开始查询，一次最多返回10条成交记录, 包含since_trade_id本身
        }
        self.qq_tx.put(json.dumps(data))

    def do_command15(self, market='cnc', coin='bhd'):
        data = {
            'cmd': {
                'type': 15      # 查询指定交易对或者指定市场的行情数据
            },
            'pair': {
                'market': market,   # 准备查询哪个市场的行情数据
                'coin': coin        # 准备查询哪个币的行情数据，
                # **如果coin是空字符串，则查询market指定的市场下所有正常交易的币的行情数据**
            }
        }
        self.qq_tx.put(json.dumps(data))


if __name__ == '__main__':
    aex = Aex()

