# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2018. 1. 10.
"""
from unittest import TestCase
from scrapper.database_writer import *
import scrapper.database_reader as dr
from datetime import datetime


class TestSaveStockMasters(TestCase):
    def test_save_stock_masters(self):
        try:
            save_stock_masters()
        except SQLAlchemyError or EnvironmentError:
            self.fail()


class TestSaveStockDailyPrice(TestCase):
    def test_save_stock_daily_price(self):
        try:
            stock_masters = dr.get_stock_masters().reset_index()
            save_stock_daily_price(stock_masters, datetime(2018, 1, 10))
        except SQLAlchemyError or EnvironmentError:
            self.fail()


class TestSaveStockDailyPrices(TestCase):
    def test_save_stock_daily_prices(self):
        try:
            save_stock_daily_prices(end_date=datetime(2016, 11, 1))
        except SQLAlchemyError or EnvironmentError:
            self.fail()
