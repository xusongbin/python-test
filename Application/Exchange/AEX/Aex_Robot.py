#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import queue
import threading
from time import time, sleep, strftime, localtime

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from AEX.Aex_websocket import Aex
from md_logging import *
from AEX.Aex_Robot_ui import Ui_Form

setup_log()
write_log = logging.getLogger('ROBOT')


class Robot(QWidget):
    coin_market = ['cnc', 'usdt']
    # coin_table = ['btc', 'eos', 'eth', 'doge', 'etc', 'bts', 'xlm']
    coin_table = ['btc', 'eos', 'eth', 'bts', 'etc']
    coin_count = coin_market + coin_table
    usdt_to_ask = 7.01
    usdt_to_bid = 7.11
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
        self.balance_tms = time()
        self.work_status = 'SIGN'
        self.work_stasub = 'STA1'
        self.work_statms = time()
        self.do_set_work_status()
        self.depth_qq = queue.Queue()
        self.message_qq = queue.Queue()
        self.strategy_im = {}
        for coin in self.coin_table:
            self.strategy_im[coin] = [0.0, 0.0]
        self.order_flow = None

        self.aex = Aex(False)
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

    def on_income_cnc2usdt(self, coin):
        try:
            # 取值范围：6个小数点
            # my_balance：钱包余额
            # my_balance = float('{:.6f}'.format(self.balance_now['cnc']['val']))
            my_balance = 100000
            # bid_price：市场上可立即买入的价格     bid_amount：市场上课立即买入的价格对应的数量
            bid_price = float('{:.6f}'.format(self.coin_info[coin]['cnc']['asks'][0]['price']))
            bid_amount = float('{:.6f}'.format(self.coin_info[coin]['cnc']['asks'][0]['amount']))
            # ask_price：市场上可立即卖出的价格     ask_amount：市场上课立即卖出的价格对应的数量
            ask_price = float('{:.6f}'.format(self.coin_info[coin]['usdt']['bids'][0]['price']))
            ask_amount = float('{:.6f}'.format(self.coin_info[coin]['usdt']['bids'][0]['amount']))
            if ask_amount <= 0.001 or bid_amount <= 0.001:  # 买卖单的数量大于一定的数值才会计算是否盈利
                return False
            # 账户余额可买的数量       balance_buy_amount = my_balance / bid_price
            # 当前可买入的数量         min_buy_amount = min(balance_buy_amount,bid_amount)
            # 买入币后的实际数量       real_recv_amount=min_buy_amount*(1-0.001)
            # 持币与买盘可交易的数量   real_sell_amount=min(real_recv_amount, ask_amount)
            balance_buy_amount = my_balance / bid_price        # 账户余额可买的数量
            min_buy_amount = min(balance_buy_amount, bid_amount)    # 可买入的数量：取市场上可买入的币数量与余额可买入的币数量最小
            real_recv_amount = min_buy_amount * (1 - 0.001)       # 买入币之后有效的数量：需要扣除手续费
            real_sell_amount = min(real_recv_amount, ask_amount)    # 实际卖出时的有效数量：取买入的有效数量和市场卖出时买盘的数量最小
            buy_need_money = min_buy_amount * bid_price          # 买币需要的资金
            sell_inc_money = real_sell_amount * ask_price          # 卖币获取到的资金
            sell_real_money = sell_inc_money * (1 - 0.001) * self.usdt_to_ask
            earn_money = sell_real_money - buy_need_money           # 操作交易后可盈利的金额
            if earn_money < -10:       # 盈利小于一定范围不考虑实施量化交易
                return False
            # 成本价卖出：市场会以最优价成交，此价格有效提高成交率
            # ask_price = round((buy_need_money / real_sell_amount) + 0.000005, 5)
            if earn_money != self.strategy_im[coin][0]:
                self.strategy_im[coin][0] = earn_money
                show_bid_price = '{:.6f}'.format(bid_price)
                show_bid_amount = '{:.6f}'.format(min_buy_amount)
                show_ask_price = '{:.6f}'.format(ask_price)
                show_ask_amount = '{:.6f}'.format(real_recv_amount)
                show_buy_need_money = '{:.6f}'.format(buy_need_money)
                show_inc_money = '{:.6f}'.format(earn_money)
                ts = strftime("%Y-%m-%d %H:%M:%S", localtime())
                msg = '{} CNC->{}->USDT 买：{:>13}/{:<13} 卖：{:>13}/{:<13} 额：{:>13}CNC  预期盈利：{:>13}CNC'.format(
                    ts, coin.upper(),
                    show_bid_price, show_bid_amount,
                    show_ask_price, show_ask_amount,
                    show_buy_need_money, show_inc_money
                )
                write_log.info(msg)
                self.do_display_message(msg)
                order_flow = [
                    {'market': 'cnc', 'coin': coin, 'price': bid_price, 'amount': min_buy_amount},
                    {'market': 'usdt', 'coin': coin, 'price': ask_price, 'amount': min_buy_amount}
                ]
                self.order_flow = order_flow
                write_log.debug('获取CNC-USDT策略成功')
                return True
        except:
            return False
        return False

    def on_income_usdt2cnc(self, coin):
        try:
            # 取值范围：6个小数点
            # my_balance：钱包余额
            # my_balance = float('{:.6f}'.format(self.balance_now['usdt']['val']))
            my_balance = 100000
            # bid_price：市场上可立即买入的价格     bid_amount：市场上课立即买入的价格对应的数量
            bid_price = float('{:.6f}'.format(self.coin_info[coin]['usdt']['asks'][0]['price']))
            bid_amount = float('{:.6f}'.format(self.coin_info[coin]['usdt']['asks'][0]['amount']))
            # ask_price：市场上可立即卖出的价格     ask_amount：市场上课立即卖出的价格对应的数量
            ask_price = float('{:.6f}'.format(self.coin_info[coin]['cnc']['bids'][0]['price']))
            ask_amount = float('{:.6f}'.format(self.coin_info[coin]['cnc']['bids'][0]['amount']))
            if ask_amount <= 0.001 or bid_amount <= 0.001:  # 买卖单的数量大于一定的数值才会计算是否盈利
                return False
            # 账户余额可买的数量       balance_buy_amount = my_balance / bid_price
            # 当前可买入的数量         min_buy_amount = min(balance_buy_amount,bid_amount)
            # 买入币后的实际数量       real_recv_amount=min_buy_amount*(1-0.001)
            # 持币与买盘可交易的数量   real_sell_amount=min(real_recv_amount, ask_amount)
            balance_buy_amount = my_balance / bid_price        # 账户余额可买的数量
            min_buy_amount = min(balance_buy_amount, bid_amount)    # 可买入的数量：取市场上可买入的币数量与余额可买入的币数量最小
            real_recv_amount = min_buy_amount * (1 - 0.001)       # 买入币之后有效的数量：需要扣除手续费
            real_sell_amount = min(real_recv_amount, ask_amount)    # 实际卖出时的有效数量：取买入的有效数量和市场卖出时买盘的数量最小
            buy_need_money = min_buy_amount * bid_price                  # 买币需要的资金
            buy_need_money = buy_need_money * self.usdt_to_bid
            sell_inc_money = real_sell_amount * ask_price * (1 - 0.001)    # 卖币获取到的资金
            earn_money = sell_inc_money - buy_need_money                   # 操作交易后可盈利的金额
            if earn_money < -10:       # 盈利小于一定范围不考虑实施量化交易
                return False
            # 成本价卖出：市场会以最优价成交，此价格有效提高成交率
            # ask_price = round((buy_need_money / real_sell_amount) + 0.000005, 5)
            if earn_money != self.strategy_im[coin][0]:
                self.strategy_im[coin][0] = earn_money
                show_bid_price = '{:.6f}'.format(bid_price)
                show_bid_amount = '{:.6f}'.format(min_buy_amount)
                show_ask_price = '{:.6f}'.format(ask_price)
                show_ask_amount = '{:.6f}'.format(real_recv_amount)
                show_buy_need_money = '{:.6f}'.format(buy_need_money)
                show_inc_money = '{:.6f}'.format(earn_money)
                ts = strftime("%Y-%m-%d %H:%M:%S", localtime())
                msg = '{} USDT->{}->CNC 买：{:>13}/{:<13} 卖：{:>13}/{:<13} 额：{:>13}USDT 预期盈利：{:>13}CNC'.format(
                    ts, coin.upper(),
                    show_bid_price, show_bid_amount,
                    show_ask_price, show_ask_amount,
                    show_buy_need_money, show_inc_money
                )
                write_log.info(msg)
                self.do_display_message(msg)
                order_flow = [
                    {'market': 'cnc', 'coin': coin, 'price': bid_price, 'amount': min_buy_amount},
                    {'market': 'usdt', 'coin': coin, 'price': ask_price, 'amount': min_buy_amount}
                ]
                self.order_flow = order_flow
                write_log.debug('获取USDT-CNC策略成功')
                return True
        except:
            return False
        return False

    def on_thread_work(self):
        while True:
            msg = self.do_parse_message()
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
                    if self.on_income_cnc2usdt(coin):
                        # self.do_set_work_status('ORDER')
                        continue
                    if self.on_income_usdt2cnc(coin):
                        # self.do_set_work_status('ORDER')
                        continue
            elif self.work_status == 'ORDER':
                if self.work_stasub == 'STA1':
                    write_log.debug('工作流程：买单 价：{} 量：{} 市场：{} 币：{}')
                    self.aex.do_command6(
                        self.order_flow[0]['price'], self.order_flow[0]['amount'],
                        self.order_flow[0]['market'], self.order_flow[0]['coin'], 1
                    )
                    self.do_set_work_status(sub='STA2')
                elif self.work_stasub == 'STA2':
                    if (time() - self.work_statms) >= 10:
                        write_log.debug('工作流程：策略超时退出！')
                        self.do_set_work_status('IDLE')
                    if not msg:
                        continue
                    if msg['cmd']['type'] == 9:
                        pass
                    write_log.debug('工作流程：等待成交然后卖出')
            elif self.work_status == 'SIGN':
                if self.work_stasub == 'STA1':
                    write_log.debug('工作流程：签名')
                    self.aex.do_command4()
                    self.do_set_work_status(sub='STA2')
                elif self.work_stasub == 'STA2':
                    if (time() - self.work_statms) >= 10:
                        write_log.error('工作流程：签名超时！')
                        return False
                elif self.work_stasub == 'STA3':
                    write_log.debug('工作流程：签名成功！')
                    self.do_set_work_status('FOCUS')
                    continue
            elif self.work_status == 'FOCUS':
                if self.work_stasub == 'STA1':
                    write_log.debug('工作流程：关注交易对')
                    pairs = []
                    for market in self.coin_market:
                        for coin in self.coin_table:
                            d = {'market': market, 'coin': coin}
                            pairs.append(d)
                    self.aex.do_command2(1, pairs)
                    self.do_set_work_status(sub='STA2')
                elif self.work_stasub == 'STA2':
                    if (time() - self.work_statms) >= 10:
                        write_log.error('工作流程：关注交易超时！')
                        return False
                elif self.work_stasub == 'STA3':
                    write_log.debug('工作流程：关注交易对成功')
                    self.do_set_work_status('BALANCE')
            elif self.work_status == 'BALANCE':
                if self.work_stasub == 'STA1':
                    write_log.debug('工作流程：获取钱包信息')
                    self.aex.do_command5()
                    self.do_set_work_status(sub='STA2')
                elif self.work_stasub == 'STA2':
                    if (time() - self.work_statms) >= 10:
                        write_log.error('工作流程：获取钱包信息超时！')
                        return False
                elif self.work_stasub == 'STA3':
                    write_log.debug('工作流程：获取钱包信息成功')
                    self.do_set_work_status('IDLE')
            sleep(0.01)

    def do_set_work_status(self, sta=None, sub='STA1'):
        if sta:
            self.work_status = sta
        self.work_stasub = sub
        self.work_statms = time()

    def do_parse_message(self):
        if self.aex.qq_rx.empty():
            return None
        self.balance_tms = time()
        try:
            msg = json.loads(self.aex.qq_rx.get())
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
            return None
        if 'cmd' not in msg.keys():
            write_log.error('do_parse_message not found cmd')
            return None
        cmd = msg['cmd']
        if cmd['eno'] not in self.aex.error.keys():
            write_log.error('do_parse_message cmd["eno"] unknown')
            return None
        if cmd['type'] != 1:
            write_log.debug('接收响应：{}'.format(self.aex.cmd[cmd['type']]))
            write_log.debug('响应状态：{}'.format(self.aex.error[cmd['eno']]))
        # if cmd['eno'] != 0:
        #     return None
        if cmd['type'] == 1:
            self.do_msg_depth_change(msg)
        elif cmd['type'] == 2:
            self.do_msg_subscribe(msg)
        elif cmd['type'] == 4:
            self.do_msg_signtrue(msg)
        elif cmd['type'] == 5:
            self.do_msg_my_balance(msg)
        elif cmd['type'] == 6:
            self.do_msg_order_commit(msg)
        elif cmd['type'] == 9:
            self.do_msg_order_record(msg)
        return msg

    def do_msg_depth_change(self, msg):
        # market = msg['market']
        # coin = msg['coin']
        # self.do_display_message('更新=>{} {}'.format(market, coin))
        self.coin_info[msg['coin']][msg['market']]['bids'] = msg['bids']
        self.coin_info[msg['coin']][msg['market']]['asks'] = msg['asks']
        self.depth_qq.put(msg)

    def do_msg_subscribe(self, msg):
        self.do_set_work_status(sub='STA3')

    def do_msg_signtrue(self, msg):
        self.do_set_work_status(sub='STA3')

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
        self.do_set_work_status(sub='STA3')

    def do_msg_order_commit(self, msg):
        data = msg['data']
        msg = '部分成交 市场：{:<5} 币：{:<5} 方向：{} 订单号：{:<10} 价格：{:<10} 数量：{:<17}'.format(
            data['market'], data['coin'], '买入' if data['type'] == 1 else '卖出',
            data['orderid'], data['price'], data['amount']
        )
        write_log.info(msg)
        self.do_display_message(msg)

    def do_msg_order_record(self, msg):
        data = msg['data']
        msg = '全部成交 市场：{:<5} 币：{:<5} 方向：{} 订单号：{:<10} 价格：{:<10} 数量：{:<17}'.format(
            data['market'], data['coin'], '买入' if data['type'] == 1 else '卖出',
            data['tradeid'], data['price'], data['amount']
        )
        write_log.info(msg)
        self.do_display_message(msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    rb = Robot()
    sys.exit(app.exec_())
