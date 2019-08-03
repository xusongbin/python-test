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
    usdt_ask = 6.9
    usdt_bid = 6.99
    coin_info = {}
    for coin in coin_table:
        coin_info[coin] = {
            'cnc': {'bids': [{'price': 0, 'amount': 0}], 'asks': [{'price': 0, 'amount': 0}]},
            'usdt': {'bids': [{'price': 0, 'amount': 0}], 'asks': [{'price': 0, 'amount': 0}]}
        }
    transaction_strategy = [
        [
            # 策略解析：
            # 1、CNC买入BTC，CNC金额上限为100
            # 2、BTC买入USDT，BTC金额上限为0.0015
            # 策略实现思路：
            # 1、获取CNC市场上BTC的卖单价格BP和数量BA，获取USDT市场上BTC的买单价格AP和数量AA
            # 2、计算买卖单的数量NA=BA>AA?AA:BA
            # 3、计算买入BTC需要的资金BM=BP*AA*(1+0.001)
            # 4、计算卖出BTC获取到的资金AM=AP*AA*(1-0.001)*UTC     UTC=usdt_cny
            # 5、计算盈利IM=AM-BM，IM为正数表示盈利，IM为负数表示亏损
            {'market': 'cnc', 'coin': 'btc', 'method': 'bid', 'up_limit': 100},
            {'market': 'usdt', 'coin': 'btc', 'method': 'ask', 'up_limit': 0.0015}
        ]
    ]

    def __init__(self):
        super().__init__()
        self.balance_now = None
        self.balance_per = None
        self.balance_sta = False
        self.balance_tms = time()
        self.work_status = 'SIGN'
        self.work_substa = 0
        self.depth_qq = queue.Queue()
        self.message_qq = queue.Queue()
        self.strategy_im = {}
        for coin in self.coin_table:
            self.strategy_im[coin] = [0.0, 0.0]
        self.order_flow = None

        self.aex = Aex(True)
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

    def on_income_cnc_usdt(self, coin):
        try:
            balance_now = self.balance_now['cnc']['val']
            if balance_now < 150:
                return False
            balance_now = 150
            bid_price = self.coin_info[coin]['cnc']['asks'][0]['price']
            bid_amount = self.coin_info[coin]['cnc']['asks'][0]['amount']
            ask_price = self.coin_info[coin]['usdt']['bids'][0]['price']
            ask_amount = self.coin_info[coin]['usdt']['bids'][0]['amount']
            bid_price = float('{:.6f}'.format(bid_price))
            bid_amount = float('{:.6f}'.format(bid_amount))
            ask_price = float('{:.6f}'.format(ask_price))
            ask_amount = float('{:.6f}'.format(ask_amount))
            if ask_amount == 0 or bid_amount == 0:
                return False
            balance_amount = balance_now / bid_price
            balance_amount = balance_amount * (1 - 0.001)
            now_amount = ask_amount if bid_amount > ask_amount else bid_amount
            now_amount = now_amount if balance_amount > now_amount else balance_amount
            now_amount = float('{:.6f}'.format(now_amount))
            bid_money = bid_price * now_amount * (1 + 0.001)
            ask_money = ask_price * now_amount * (1 - 0.001) * self.usdt_bid
            inc_money = ask_money - bid_money
            if inc_money < 0.1:
                return False
            if inc_money != self.strategy_im[coin][0]:
                self.strategy_im[coin][0] = inc_money
                bid_money = '{:.6f}'.format(bid_money)
                ask_money = '{:.6f}'.format(ask_money)
                inc_money = '{:.6f}'.format(inc_money)
                ctl_amount = '{:.6f}'.format(now_amount)
                ts = strftime("%Y-%m-%d %H:%M:%S", localtime())
                tag = int(time() * 1000)
                msg = '{} CNC->{}->USDT 买：{:<13} 卖：{:<13} 量：{:<13} 盈利：{:<13} TAG：{}'.format(
                    ts, coin.upper(), bid_money, ask_money, ctl_amount, inc_money, tag
                )
                write_log.info(msg)
                self.do_display_message(msg)
                order_flow = [
                    {'method': 'bid', 'market': 'cnc', 'coin': coin, 'price': bid_price, 'amount': now_amount, 'tag': 0},
                    {'method': 'ask', 'market': 'usdt', 'coin': coin, 'price': ask_price, 'amount': now_amount - 0.000001, 'tag': 0}
                ]
                self.order_flow = order_flow
                write_log.debug('获取CNC-USDT策略成功')
                return True
        except:
            return False
        return False

    def on_income_usdt_cnc(self, coin):
        try:
            balance_now = self.balance_now['usdt']['val']
            if balance_now < 20:
                return False
            balance_now = 15
            bid_price = self.coin_info[coin]['usdt']['asks'][0]['price']
            bid_amount = self.coin_info[coin]['usdt']['asks'][0]['amount']
            ask_price = self.coin_info[coin]['cnc']['bids'][0]['price']
            ask_amount = self.coin_info[coin]['cnc']['bids'][0]['amount']
            bid_price = float('{:.6f}'.format(bid_price))
            bid_amount = float('{:.6f}'.format(bid_amount))
            ask_price = float('{:.6f}'.format(ask_price))
            ask_amount = float('{:.6f}'.format(ask_amount))
            if ask_amount == 0 or bid_amount == 0:
                return False
            balance_amount = balance_now / bid_price
            balance_amount = balance_amount * (1 - 0.001)
            now_amount = ask_amount if bid_amount > ask_amount else bid_amount
            now_amount = now_amount if balance_amount > now_amount else balance_amount
            now_amount = float('{:.6f}'.format(now_amount))
            bid_money = bid_price * now_amount * (1 + 0.001) * self.usdt_ask
            ask_money = ask_price * now_amount * (1 - 0.001)
            inc_money = ask_money - bid_money
            if inc_money < 0.1:
                return False
            if inc_money != self.strategy_im[coin][1]:
                self.strategy_im[coin][1] = inc_money
                bid_money = '{:.6f}'.format(bid_money)
                ask_money = '{:.6f}'.format(ask_money)
                inc_money = '{:.6f}'.format(inc_money)
                ctl_amount = '{:.6f}'.format(now_amount)
                ts = strftime("%Y-%m-%d %H:%M:%S", localtime())
                tag = int(time() * 1000)
                msg = '{} USDT->{}->CNC 买：{:<13} 卖：{:<13} 量：{:<13} 盈利：{:<13} TAG：{}'.format(
                    ts, coin.upper(), bid_money, ask_money, ctl_amount, inc_money, tag
                )
                write_log.info(msg)
                self.do_display_message(msg)
                order_flow = [
                    {'method': 'bid', 'market': 'cnc', 'coin': coin, 'price': bid_price, 'amount': now_amount, 'tag': 0},
                    {'method': 'ask', 'market': 'usdt', 'coin': coin, 'price': ask_price, 'amount': now_amount - 0.000001, 'tag': 0}
                ]
                self.order_flow = order_flow
                write_log.debug('获取USDT-CNC策略成功')
                return True
        except:
            return False
        return False

    def on_thread_work(self):
        while True:
            self.do_parse_message()
            if self.work_status == 'IDLE':
                if (time() - self.balance_tms) >= 30:
                    self.balance_tms = time()
                    self.work_status = 'BALANCE'
                    continue
                # 策略实现思路：
                # 1、获取CNC市场上BTC的卖单价格BP和数量BA，获取USDT市场上BTC的买单价格AP和数量AA
                # 2、计算买卖单的数量NA=BA>AA?AA:BA，账户可买
                # 3、计算买入BTC需要的资金BM=BP*NA*(1+0.001)
                # 4、计算卖出BTC获取到的资金AM=AP*NA*(1-0.001)*UTC     UTC=usdt_cny
                # 5、计算盈利IM=AM-BM，IM为正数表示盈利，IM为负数表示亏损
                # pass
                for coin in self.coin_table:
                    if self.on_income_cnc_usdt(coin):
                        self.work_status = 'ORDER'
                        self.work_substa = 1
                        continue
                    if self.on_income_usdt_cnc(coin):
                        self.work_status = 'ORDER'
                        self.work_substa = 1
                        continue
            elif self.work_status == 'ORDER':
                if self.work_substa == 1:
                    write_log.debug('工作流程：下买单')
                    self.aex.do_command6(
                        self.order_flow[0]['price'],
                        self.order_flow[0]['amount'],
                        self.order_flow[0]['tag'],
                        self.order_flow[0]['market'],
                        self.order_flow[0]['coin'],
                        1 if self.order_flow[0]['method'] == 'bid' else 2
                    )
                    self.work_substa = 2
                elif self.work_substa == 3:
                    write_log.debug('工作流程：下卖单')
                    self.aex.do_command6(
                        self.order_flow[1]['price'] * 0.8,
                        self.order_flow[1]['amount'],
                        self.order_flow[1]['tag'],
                        self.order_flow[1]['market'],
                        self.order_flow[1]['coin'],
                        1 if self.order_flow[1]['method'] == 'bid' else 2
                    )
                    self.work_substa = 4
                elif self.work_substa > 4:
                    self.work_status = 'BALANCE'
            elif self.work_status == 'SIGN':
                write_log.debug('工作流程：签名')
                self.aex.do_command4()
                self.work_status = 'FOCUS'
            elif self.work_status == 'FOCUS':
                write_log.debug('工作流程：关注交易对')
                pairs = []
                for market in self.coin_market:
                    for coin in self.coin_table:
                        d = {'market': market, 'coin': coin}
                        pairs.append(d)
                self.aex.do_command2(1, pairs)
                self.work_status = 'BALANCE'
            elif self.work_status == 'BALANCE':
                write_log.debug('工作流程：获取钱包信息')
                self.balance_sta = False
                self.aex.do_command5()
                self.work_status = 'UTC'
            elif self.work_status == 'UTC':
                if not self.balance_sta:
                    continue
                try:
                    usdt_val = self.balance_now['usdt']['val']
                    cnc_val = self.balance_now['cnc']['val']
                    if usdt_val * self.usdt_ask > cnc_val:
                        write_log.debug('工作流程：需要操作卖出USDT')
                        usdt_val = usdt_val / 2
                        usdt_val = float('{:.6f}'.format(usdt_val)) - 0.000001
                        self.aex.do_command6(6.7, usdt_val, 0, 'cnc', 'usdt', 2)
                        self.work_status = 'BALANCE'
                    else:
                        write_log.debug('工作流程：获取钱包信息存在金额')
                        self.work_status = 'IDLE'
                except:
                    pass
            # sleep(0.01)

    def do_parse_message(self):
        if self.aex.qq_rx.empty():
            return
        self.balance_tms = time()
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
        if cmd['type'] != 1:
            write_log.debug('接收响应：{}'.format(self.aex.cmd[cmd['type']]))
            write_log.debug('响应状态：{}'.format(self.aex.error[cmd['eno']]))
        if cmd['eno'] != 0:
            self.work_status = 'BALANCE'
            return
        if cmd['type'] == 9:
            self.do_msg_order_record(msg)
        elif cmd['type'] == 6:
            self.do_msg_order_commit(msg)
        elif cmd['type'] == 5:
            self.do_msg_my_balance(msg)
        elif cmd['type'] == 1:
            self.do_msg_depth_change(msg)
        elif cmd['type'] == 7:
            self.work_substa += 1

    def do_msg_order_record(self, msg):
        data = msg['data']
        msg = '全部成交 市场：{:<5} 币：{:<5} 方向：{} 订单号：{:<10} 价格：{:<10} 数量：{:<17}'.format(
            data['market'], data['coin'], '买入' if data['type'] == 1 else '卖出',
            data['tradeid'], data['price'], data['amount']
        )
        write_log.info(msg)
        self.do_display_message(msg)
        self.work_substa += 1

    def do_msg_order_commit(self, msg):
        data = msg['data']
        msg = '部分成交 市场：{:<5} 币：{:<5} 方向：{} 订单号：{:<10} 价格：{:<10} 数量：{:<17}'.format(
            data['market'], data['coin'], '买入' if data['type'] == 1 else '卖出',
            data['orderid'], data['price'], data['amount']
        )
        write_log.info(msg)
        self.do_display_message(msg)
        # self.aex.do_command7(data['orderid'], data['market'], data['coin'])
        # self.work_substa += 1

    def do_msg_my_balance(self, msg):
        balances = msg['balances']
        balance_dict = {}
        for info in balances:
            balance_dict[info['coin']] = {'val': info['val'], 'locked': info['locked']}
        if balance_dict != self.balance_now:
            self.balance_now = balance_dict
            self.do_display_message('更新钱包信息成功： CNC={} USDT={}'.format(
                balance_dict['cnc']['val'], balance_dict['usdt']['val']
            ))
            self.balance_sta = True

    def do_msg_depth_change(self, msg):
        # market = msg['market']
        # coin = msg['coin']
        # self.do_display_message('更新=>{} {}'.format(market, coin))
        self.coin_info[msg['coin']][msg['market']]['bids'] = msg['bids']
        self.coin_info[msg['coin']][msg['market']]['asks'] = msg['asks']
        self.depth_qq.put(msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    rb = Robot()
    sys.exit(app.exec_())
