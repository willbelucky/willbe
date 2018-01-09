# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2018. 1. 7.
"""
from datetime import datetime
from unittest import TestCase

from numpy import testing

from table.tables import *


class TestStockMaster(TestCase):
    def test_get_stock_masters(self):
        stock_masters = StockMaster.instance().select().values()
        self.assertIsNotNone(stock_masters)
        self.assertEqual(2317, len(stock_masters))
        testing.assert_array_equal(['code'], stock_masters.index.names)
        testing.assert_array_equal(['short_code', 'company_name', 'market_name'], stock_masters.columns.values)

    def test_get_one_stock_master_by_code(self):
        stock_masters = StockMaster.instance().select().where(code='KR7005930003').values()
        self.assertIsNotNone(stock_masters)
        print(stock_masters)
        self.assertEqual(1, len(stock_masters))
        testing.assert_array_equal(['code'], stock_masters.index.names)
        testing.assert_array_equal(['short_code', 'company_name', 'market_name'], stock_masters.columns.values)


class TestStockDailyPrice(TestCase):
    def test_get_all_stock_daily_prices(self):
        stock_daily_prices = StockDailyPrice.instance().select().values()
        self.assertIsNotNone(stock_daily_prices)
        self.assertEqual(507006, len(stock_daily_prices))
        testing.assert_array_equal(['code', 'date'], stock_daily_prices.index.names)
        testing.assert_array_equal(['volume', 'open', 'high', 'low', 'close'],
                                   stock_daily_prices.columns.values)

    def test_get_one_company_one_week_stock_daily_prices(self):
        stock_masters = StockMaster.instance().select().where(code='KR7005930003').values()
        stock_daily_prices = StockDailyPrice.instance().select().where(stock_masters=stock_masters,
                                                                       from_date=datetime(2017, 1, 1),
                                                                       to_date=datetime(2017, 1, 8)).values()
        self.assertIsNotNone(stock_daily_prices)
        self.assertEqual(5, len(stock_daily_prices))
        testing.assert_array_equal(['code', 'date'], stock_daily_prices.index.names)
        testing.assert_array_equal(['volume', 'open', 'high', 'low', 'close'],
                                   stock_daily_prices.columns.values)


class TestStockMinutePrice(TestCase):
    def test_get_all_stock_minute_prices(self):
        stock_minute_prices = StockMinutePrice.instance().select().values()
        self.assertIsNotNone(stock_minute_prices)
        self.assertEqual(353861652, len(stock_minute_prices))
        testing.assert_array_equal(['code', 'date'], stock_minute_prices.index.names)
        testing.assert_array_equal(['open', 'high', 'low', 'close', 'volume'],
                                   stock_minute_prices.columns.values)

    def test_get_one_company_one_week_stock_minute_prices(self):
        stock_masters = StockMaster.instance().select().where(code='KR7005930003').values()
        stock_minute_prices = StockMinutePrice.instance().select().where(stock_masters=stock_masters,
                                                                         from_date=datetime(2017, 1, 1),
                                                                         to_date=datetime(2017, 1, 8)).values()
        self.assertIsNotNone(stock_minute_prices)
        self.assertEqual(1853, len(stock_minute_prices))
        testing.assert_array_equal(['code', 'date'], stock_minute_prices.index.names)
        testing.assert_array_equal(['open', 'high', 'low', 'close', 'volume'],
                                   stock_minute_prices.columns.values)
