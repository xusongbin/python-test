#!/usr/bin/env python
# -*- coding: utf-8 -*-
from huobi import RequestClient

request_client = RequestClient()

print(request_client.get_exchange_timestamp())

# trade_statistics = request_client.get_24h_trade_statistics("btcusdt")
# print("---- Statistics ----")
# print("Timestamp: " + str(trade_statistics.timestamp))
# print("High: " + str(trade_statistics.high))
# print("Low: " + str(trade_statistics.low))
# print("Open: " + str(trade_statistics.open))
# print("Close: " + str(trade_statistics.close))
# print("Volume: " + str(trade_statistics.volume))
