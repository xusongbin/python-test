#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import threading
import pandas as pd
from time import time, sleep, strftime, localtime

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Aex_restful import Aex
from md_logging import *
from Robot_ui import Ui_Form

setup_log()
write_log = logging.getLogger('ROBOT')


class Robot(QWidget):
    coin_market = ['cnc', 'usdt']
    coin_table = ['btc', 'eos', 'eth', 'doge', 'etc', 'bts', 'xlm']

    def __init__(self):
        super().__init__()
        self.my_balance = {}

        self.work_ui = Ui_Form()
        self.work_ui.setupUi(self)
        self.work_ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)

        self.aex = Aex()
        # print(self.do_get_ticker_vol())

        self.timer_work_ui = QTimer()
        self.timer_work_ui.timeout.connect(self.on_timer_work_ui)
        self.timer_work_ui.start(50)

        self.thread_work = threading.Thread(target=self.on_thread_work)
        self.thread_work.setDaemon(True)
        self.thread_work.start()

        self.show()

    def on_timer_work_ui(self):
        self.work_ui.tableWidget.setRowCount(len(self.my_balance.keys()))
        for idx, key in enumerate(self.my_balance.keys()):
            coin = QTableWidgetItem(key)
            balance = QTableWidgetItem('{:.8f}'.format(self.my_balance[key][0]))
            lock = QTableWidgetItem('{:.8f}'.format(self.my_balance[key][1]))
            coin.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            balance.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            lock.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.work_ui.tableWidget.setItem(idx, 0, coin)
            self.work_ui.tableWidget.setItem(idx, 1, balance)
            self.work_ui.tableWidget.setItem(idx, 2, lock)

    def do_get_balance(self):
        balances = self.aex.do_get_mybalance()
        if not balances:
            return False
        for key in balances.keys():
            if '_lock' in key:
                continue
            coin = key.split('_')[0].upper()
            balance = float(balances[key])
            lock = float(balances[key+'_lock'])
            self.my_balance[coin] = [balance, lock]
        return True

    def do_get_ticker_vol(self):
        ticker = self.aex.do_get_ticker('all', 'cnc')
        volume = []
        coin = [x for x in ticker.keys()]
        for key in coin:
            vol = ticker[key]['ticker']['vol'] * ticker[key]['ticker']['last']
            volume.append(vol)
        cnc_pd = pd.DataFrame({'cnc': coin, 'vol': volume})
        cnc_pd.sort_values(by='vol', inplace=True, ascending=False)
        cnc_pd.reset_index(inplace=True, drop=True)
        cnc_pd.drop(['vol'], axis=1, inplace=True)
        ticker = self.aex.do_get_ticker('all', 'usdt')
        volume = []
        coin = [x for x in ticker.keys()]
        for key in coin:
            vol = ticker[key]['ticker']['vol'] * ticker[key]['ticker']['last']
            volume.append(vol)
        usdt_pd = pd.DataFrame({'usdt': coin, 'vol': volume})
        usdt_pd.sort_values(by='vol', inplace=True, ascending=False)
        usdt_pd.reset_index(inplace=True, drop=True)
        usdt_pd.drop(['vol'], axis=1, inplace=True)
        ticker = self.aex.do_get_ticker('all', 'btc')
        volume = []
        coin = [x for x in ticker.keys()]
        for key in coin:
            vol = ticker[key]['ticker']['vol'] * ticker[key]['ticker']['last']
            volume.append(vol)
        btc_pd = pd.DataFrame({'btc': coin, 'vol': volume})
        btc_pd.sort_values(by='vol', inplace=True, ascending=False)
        btc_pd.reset_index(inplace=True, drop=True)
        btc_pd.drop(['vol'], axis=1, inplace=True)
        ticker = self.aex.do_get_ticker('all', 'eth')
        volume = []
        coin = [x for x in ticker.keys()]
        for key in coin:
            vol = ticker[key]['ticker']['vol'] * ticker[key]['ticker']['last']
            volume.append(vol)
        eth_pd = pd.DataFrame({'eth': coin, 'vol': volume})
        eth_pd.sort_values(by='vol', inplace=True, ascending=False)
        eth_pd.reset_index(inplace=True, drop=True)
        eth_pd.drop(['vol'], axis=1, inplace=True)
        print(cnc_pd)
        total_pd = cnc_pd
        total_pd['usdt'] = usdt_pd['usdt']
        total_pd['btc'] = btc_pd['btc']
        total_pd['eth'] = eth_pd['eth']
        return total_pd.head(20)

    def on_thread_work(self):
        while True:
            self.do_get_balance()
            sleep(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    rb = Robot()
    sys.exit(app.exec_())
