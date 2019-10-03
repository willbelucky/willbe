# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2018. 1. 10.
"""
from unittest import TestCase

from numpy import testing
import numpy as np

from scrapper.krx import *


class TestGetStockMasters(TestCase):
    def test_get_stock_masters(self):
        stock_masters = get_stock_masters()
        self.assertIsNotNone(stock_masters)
        self.assertFalse(np.any(stock_masters.duplicated()))
        testing.assert_array_equal(['code'], stock_masters.index.names)
        testing.assert_array_equal(['company_name', 'market_name', 'short_code'], stock_masters.columns.values)


class TestGetStockDailyPrices(TestCase):
    def test_get_stock_daily_prices(self):
        stock_daily_prices = get_stock_daily_prices(datetime(2019, 10, 2))
        self.assertIsNotNone(stock_daily_prices)
        self.assertEqual(2422, len(stock_daily_prices))
        testing.assert_array_equal(['날짜', '종목코드'], stock_daily_prices.index.names)


class TestGetStockTrends(TestCase):
    def test_get_stock_trends(self):
        stock_trends = get_stock_trends(datetime(2018, 1, 10))
        self.assertIsNotNone(stock_trends)
        self.assertEqual(2313, len(stock_trends))
        testing.assert_array_equal(['code', 'date'], stock_trends.index.names)
        testing.assert_array_equal(
            ['bank_buy', 'bank_sell', 'foreigner_buy', 'foreigner_sell', 'government_buy',
             'government_sell', 'individual_buy', 'individual_sell', 'insurance_buy',
             'insurance_sell', 'investing_organization_buy',
             'investing_organization_sell', 'investment_trust_buy',
             'investment_trust_sell', 'other_corporation_buy', 'other_corporation_sell',
             'other_finance_buy', 'other_finance_sell', 'other_foreigner_buy',
             'other_foreigner_sell', 'pension_fund_buy', 'pension_fund_sell',
             'private_equity_fund_buy', 'private_equity_fund_sell'],
            stock_trends.columns.values)


class TestGetStockTrend(TestCase):
    def test_get_stock_trend(self):
        stock_trend = get_stock_trend(datetime(2018, 1, 10), 'KR7005930003', 'A005930', '삼성전자')
        self.assertIsNotNone(stock_trend)
        self.assertEqual(1, len(stock_trend))
        testing.assert_array_equal(['code', 'date'], stock_trend.index.names)
        testing.assert_array_equal(
            ['bank_buy', 'bank_sell', 'foreigner_buy', 'foreigner_sell', 'government_buy',
             'government_sell', 'individual_buy', 'individual_sell', 'insurance_buy',
             'insurance_sell', 'investing_organization_buy',
             'investing_organization_sell', 'investment_trust_buy',
             'investment_trust_sell', 'other_corporation_buy', 'other_corporation_sell',
             'other_finance_buy', 'other_finance_sell', 'other_foreigner_buy',
             'other_foreigner_sell', 'pension_fund_buy', 'pension_fund_sell',
             'private_equity_fund_buy', 'private_equity_fund_sell'],
            stock_trend.columns.values)
