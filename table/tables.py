# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2018. 1. 1.
"""
import pandas as pd

from table.base import Table

idx = pd.IndexSlice


class StockMaster(Table):
    def __init__(self):
        table_name = 'stock_master'
        csv_file_remote_address = 'https://www.dropbox.com/s/2m8lc1nirln014g/stock_master.csv?dl=1'
        index = ['code']
        super().__init__(table_name, csv_file_remote_address, index)


class StockDailyPrice(Table):
    def __init__(self):
        table_name = 'stock_daily_price'
        csv_file_remote_address = 'https://www.dropbox.com/s/xqcpwavozoyjw4m/stock_daily_price.csv?dl=1'
        index = ['code', 'date']
        super().__init__(table_name, csv_file_remote_address, index)


class StockMinutePrice(Table):
    def __init__(self):
        table_name = 'stock_minute_price'
        csv_file_remote_address = 'https://www.dropbox.com/s/x6ledb2y0r4s1tj/stock_minute_price.csv?dl=1'
        index = ['code', 'date']
        super().__init__(table_name, csv_file_remote_address, index)
