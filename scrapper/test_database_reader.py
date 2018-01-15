# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2018. 1. 14.
"""
from unittest import TestCase

import numpy as np
from numpy import testing
from datetime import datetime

from scrapper.database_reader import *


class TestStockMasters(TestCase):
    def test_get_stock_masters(self):
        stock_masters = get_stock_masters()
        self.assertIsNotNone(stock_masters)
        testing.assert_array_equal(['code'], stock_masters.index.names)
        testing.assert_array_equal(['short_code', 'company_name', 'market_name'], stock_masters.columns.values)


class TestStockDailyPrices(TestCase):
    def test_count_stock_daily_prices(self):
        stock_daily_prices_count = count_stock_daily_prices(code='KR7005930003', end_date=datetime(2018, 1, 10))
        self.assertEqual(5598, stock_daily_prices_count)

    def test_get_stock_daily_prices(self):
        stock_daily_prices = get_stock_daily_prices(code='KR7005930003', end_date=datetime(2018, 1, 10))
        self.assertIsNotNone(stock_daily_prices)
        self.assertEqual(5598, len(stock_daily_prices))
        testing.assert_array_equal(['code', 'date'], stock_daily_prices.index.names)
        testing.assert_array_equal(
            ['volume', 'open', 'high', 'low', 'close', 'market_capitalization', 'listed_stocks_number', 'adj_close'],
            stock_daily_prices.columns.values)


class TestStockTrends(TestCase):
    def test_count_stock_trends(self):
        stock_trends_count = count_stock_trends(code='KR7005930003', start_date=datetime(2017, 8, 1),
                                                end_date=datetime(2018, 1, 10))
        self.assertEqual(107, stock_trends_count)

    def test_get_stock_trends(self):
        stock_daily_prices = get_stock_trends(code='KR7005930003', start_date=datetime(2017, 8, 1),
                                              end_date=datetime(2018, 1, 10))
        self.assertIsNotNone(stock_daily_prices)
        self.assertEqual(107, len(stock_daily_prices))
        testing.assert_array_equal(['code', 'date'], stock_daily_prices.index.names)
        testing.assert_array_equal(
            ['bank_buy', 'bank_sell', 'foreigner_buy', 'foreigner_sell', 'government_buy',
             'government_sell', 'individual_buy', 'individual_sell', 'insurance_buy',
             'insurance_sell', 'investing_organization_buy',
             'investing_organization_sell', 'investment_trust_buy',
             'investment_trust_sell', 'other_corporation_buy', 'other_corporation_sell',
             'other_finance_buy', 'other_finance_sell', 'other_foreigner_buy',
             'other_foreigner_sell', 'pension_fund_buy', 'pension_fund_sell',
             'private_equity_fund_buy', 'private_equity_fund_sell'],
            stock_daily_prices.columns.values)
