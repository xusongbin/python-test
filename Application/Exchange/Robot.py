#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import queue
import threading
import pandas as pd
from time import time, sleep, strftime, localtime

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Aex_websocket import Aex
from md_logging import *
from Robot_ui import Ui_Form

setup_log()
write_log = logging.getLogger('ROBOT')


class Robot(QWidget):
    coin_market = ['cnc', 'usdt']
    # coin_table = ['btc', 'eos', 'eth', 'doge', 'etc', 'bts', 'xlm']
    coin_table = ['btc', 'eos', 'eth', 'bts', 'etc']
    coin_count = coin_market + coin_table
    cnc_cny = 0.995
    usdt_cny = 6.84
    coin_info = {}
    for coin in coin_table:
        coin_info[coin] = {
            'cnc': {'bids': {'price': 0, 'amount': 0}, 'asks': {'price': 0, 'amount': 0}},
            'usdt': {'bids': {'price': 0, 'amount': 0}, 'asks': {'price': 0, 'amount': 0}}
        }
    transaction_strategy = [
        [
            # 策略解析：
            # 1、CNC买入BTC，CNC金额上限为100
            # 2、BTC买入USDT，BTC金额上限为0.0015
            # 策略实现思路：
            # 1、获取CNC市场上BTC的卖单价格BP和数量BA，获取USDT市场上BTC的买单价格AP和数量AA
            # 2、计算买单金额上
            {'market': 'cnc', 'coin': 'btc', 'method': 'bid', 'up_limit': 100},
            {'market': 'usdt', 'coin': 'btc', 'method': 'ask', 'up_limit': 0.0015}
        ]
    ]

    def __init__(self):
        super().__init__()
        self.balance_now = None
        self.balance_per = None
        self.work_status = 'SIGN'
        self.depth_qq = queue.Queue()
        self.message_qq = queue.Queue()

        self.aex = Aex()
        self.aex.start()

        self.work_ui = Ui_Form()
        self.work_ui.setupUi(self)
        self.do_work_ui_init()

        self.timer_work_ui = QTimer()
        self.timer_work_ui.timeout.connect(self.on_timer_work_ui)
        self.timer_work_ui.start(10)

        self.thread_work = threading.Thread(target=self.on_thread_work)
        self.thread_work.setDaemon(True)
        self.thread_work.start()

        self.show()

    def do_work_ui_init(self):
        self.work_ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.work_ui.tableWidget.setColumnCount(len(self.coin_count))
        for idx, d in enumerate(self.coin_count):
            coin = QTableWidgetItem(d.upper())
            coin.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.work_ui.tableWidget.setItem(0, idx, coin)
            for row in range(1, 11):
                self.work_ui.tableWidget.setItem(row, idx, QTableWidgetItem(0))

    def do_display_message(self, msg):
        self.message_qq.put(msg)

    def on_timer_work_ui(self):
        if self.balance_now != self.balance_per:
            self.balance_per = self.balance_now
            for idx, coin in enumerate(self.coin_count):
                if coin not in self.balance_per.keys():
                    val = 0
                    locked = 0
                else:
                    val = self.balance_per[coin]['val']
                    locked = self.balance_per[coin]['locked']
                # val = QTableWidgetItem('{:.8f}'.format(val))
                # locked = QTableWidgetItem('{:.8f}'.format(locked))
                # val.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                # locked.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                # self.work_ui.tableWidget.setItem(idx, 1, val)
                # self.work_ui.tableWidget.setItem(idx, 2, locked)
                self.work_ui.tableWidget.item(1, idx).setText('{:.8f}'.format(val))
                self.work_ui.tableWidget.item(2, idx).setText('{:.8f}'.format(locked))

        while not self.depth_qq.empty():
            data = self.depth_qq.get()
            market = data['market']
            coin = data['coin']
            bid_price = data['bids'][0]['price']
            bid_amount = data['bids'][0]['amount']
            ask_price = data['asks'][0]['price']
            ask_amount = data['asks'][0]['amount']
            row = 3 + self.coin_market.index(market) * 4
            col = 2 + self.coin_table.index(coin)
            self.work_ui.tableWidget.item(row, col).setText('{:.8f}'.format(bid_price))
            self.work_ui.tableWidget.item(row + 1, col).setText('{:.8f}'.format(bid_amount))
            self.work_ui.tableWidget.item(row + 2, col).setText('{:.8f}'.format(ask_price))
            self.work_ui.tableWidget.item(row + 3, col).setText('{:.8f}'.format(ask_amount))

        while not self.message_qq.empty():
            msg = self.message_qq.get()
            self.work_ui.plainTextEdit.appendPlainText(msg)

    def on_thread_work(self):
        while True:
            self.do_parse_message()
            if self.work_status == 'IDLE':
                for strategy in self.transaction_strategy:      # 轮询各个策略
                    # {'market': 'cnc', 'coin': 'btc', 'method': 'bid', 'up_limit': 100},
                    # {'market': 'usdt', 'coin': 'btc', 'method': 'ask', 'up_limit': 0.0015}
                    for step in strategy:       # 按步骤验证交易策略是否盈利
                        # 判断是否盈利CNC-CNY=cnc_cny USDT-CNY=usdt_cny
                        # 判断交易方向，取市场上代币的价格及数量

            elif self.work_status == 'SIGN':
                self.aex.do_command4()
                self.work_status = 'BALANCE'
            elif self.work_status == 'BALANCE':
                self.aex.do_command5()
                self.work_status = 'FOCUS'
            elif self.work_status == 'FOCUS':
                pairs = []
                for market in self.coin_market:
                    for coin in self.coin_table:
                        d = {'market': market, 'coin': coin}
                        pairs.append(d)
                self.aex.do_command2(1, pairs)
                self.work_status = 'IDLE'
            sleep(0.01)

    def do_parse_message(self):
        if self.aex.qq_rx.empty():
            return
        try:
            msg = json.loads(self.aex.qq_rx.get())
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
            return
        if 'cmd' not in msg.keys():
            write_log.error('do_parse_message not found cmd')
            return
        cmd = msg['cmd']
        if cmd['eno'] not in self.aex.error.keys():
            write_log.error('do_parse_message cmd["eno"] unknown')
            return
        write_log.debug('接收响应：{}'.format(self.aex.cmd[cmd['type']]))
        write_log.debug('响应状态：{}'.format(self.aex.error[cmd['eno']]))
        if cmd['eno'] != 0:
            return
        if cmd['type'] == 1:
            self.do_msg_depth_change(msg)
        elif cmd['type'] == 5:
            self.do_msg_my_balance(msg)

    def do_msg_depth_change(self, msg):
        # market = msg['market']
        # coin = msg['coin']
        # self.do_display_message('更新=>{} {}'.format(market, coin))
        self.coin_info[msg['coin']][msg['market']]['bids'] = msg['bids']
        self.coin_info[msg['coin']][msg['market']]['asks'] = msg['asks']
        self.depth_qq.put(msg)

    def do_msg_my_balance(self, msg):
        balances = msg['balances']
        balance_dict = {}
        for info in balances:
            balance_dict[info['coin']] = {'val': info['val'], 'locked': info['locked']}
        if balance_dict != self.balance_now:
            self.balance_now = balance_dict
            self.do_display_message('更新钱包信息成功')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    rb = Robot()
    sys.exit(app.exec_())
