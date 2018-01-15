# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2018. 1. 10.
"""
import traceback
from datetime import datetime

import pandas as pd
from sqlalchemy.exc import SQLAlchemyError

from util.database_supporter import get_connection


def count_stock_master():
    schema_name = 'stock_master'
    select_sql = "SELECT COUNT(*) as count FROM {}".format(schema_name)
    count = 0
    connection = get_connection()

    try:
        # get all stock codes from the db.
        count = int(pd.read_sql(select_sql, connection).iloc[0]['count'])

    except SQLAlchemyError or EnvironmentError:
        traceback.print_exc()

    finally:
        connection.close()

    return count


def get_stock_masters():
    """
    Get stock masters from MySQL and return them.

    :return stock_masters: (DataFrame)
        index       code            | (string) 12 length string code of stock.
        columns     short_code      | (string) 7 length string code of stock.
                    company_name    | (string) The name of company.
                    market_name     | (string) The name of market.
    """
    schema_name = 'stock_master'
    select_sql = "SELECT * FROM {}".format(schema_name)
    stock_masters = pd.DataFrame()
    connection = get_connection()

    try:
        # get all stock codes from the db.
        stock_masters = pd.read_sql(select_sql, connection)
        stock_masters.set_index('code', inplace=True)

    except SQLAlchemyError or EnvironmentError:
        traceback.print_exc()

    finally:
        connection.close()

    return stock_masters


def count_stock_daily_prices(code=None, start_date=datetime(1995, 5, 2), end_date=datetime.today()):
    """
    Get the number of stock prices from start_date to end_date.

    :param code: (string, default=None) 12 length string code of stock. If code is None, select all stock codes.
    :param start_date: (datetime, default=datetime(1995, 5, 2))
        datetime(1995, 5, 2) is the first day of KRX stock data.
    :param end_date: (datetime, default=datetime.today())

    :return count: (integer) The number of stock prices from start_date to end_date.
    """
    schema_name = 'stock_daily_price'
    select_sql = "SELECT COUNT(*) as `count` FROM {}".format(schema_name)
    count = 0
    connection = get_connection()

    # WHERE clause
    _end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
    select_sql += " WHERE `date` BETWEEN '{}' AND '{}'".format(start_date, _end_date)
    if code:
        if code is not None:
            select_sql += " AND `code` = '{}'".format(code)

    try:
        # get all stock codes from the db.
        count = int(pd.read_sql(select_sql, connection).iloc[0]['count'])

    except SQLAlchemyError or EnvironmentError:
        traceback.print_exc()

    finally:
        connection.close()

    return count


def get_stock_daily_prices(code=None, start_date=datetime(1995, 5, 2), end_date=datetime.today()):
    """
    Get all stock prices from MySQL and return them.

    :param code: (string, default=None)
        6 digit number string code of stock. If code is None, select all stock codes.
    :param start_date: (datetime, default=datetime(1995, 5, 2))
        datetime(1995, 5, 2) is the first day of KRX stock data.
    :param end_date: (datetime, default=datetime.today())

    :return stock_daily_prices: (DataFrame)
        index       code                    | (string) 6 digit number string code of stock.
                    date                    | (datetime)
        columns     volume                  | (bigint)
                    open                    | (float)
                    high                    | (float)
                    low                     | (float)
                    close                   | (float)
                    market_capitalization   | (bigint)
                    listed_stocks_number    | (bigint)
                    adj_close               | (float)
    """
    schema_name = 'stock_daily_price'
    select_sql = "SELECT * FROM {}".format(schema_name)
    stock_daily_prices = pd.DataFrame()
    connection = get_connection()

    # WHERE clause
    _end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
    select_sql += " WHERE `date` BETWEEN '{}' AND '{}'".format(start_date, _end_date)
    if code:
        if code is not None:
            select_sql += " AND `code` = '{}'".format(code)

    try:
        # get all stock codes from the db.
        stock_daily_prices = pd.read_sql(select_sql, connection, parse_dates=['date'])
        stock_daily_prices.set_index(['code', 'date'], inplace=True)
        stock_daily_prices['adj_close'] = stock_daily_prices['market_capitalization'] / stock_daily_prices[
            'listed_stocks_number']

    except SQLAlchemyError or EnvironmentError:
        traceback.print_exc()

    finally:
        connection.close()

    return stock_daily_prices


def count_stock_trends(code=None, start_date=datetime(1995, 5, 2), end_date=datetime.today()):
    """
    Get the number of stock trends from start_date to end_date.

    :param code: (string, default=None)
        6 digit number string code of stock. If code is None, select all stock codes.
    :param start_date: (datetime, default=datetime(1995, 5, 2))
        datetime(1995, 5, 2) is the first day of KRX stock data.
    :param end_date: (datetime, default=datetime.today())

    :return count: (integer) The number of stock prices from start_date to end_date.
    """
    schema_name = 'stock_trend'
    select_sql = "SELECT COUNT(*) as `count` FROM {}".format(schema_name)
    count = 0
    connection = get_connection()

    # WHERE clause
    _end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
    select_sql += " WHERE `date` BETWEEN '{}' AND '{}'".format(start_date, _end_date)
    if code:
        if code is not None:
            select_sql += " AND `code` = '{}'".format(code)

    try:
        # get all stock codes from the db.
        count = int(pd.read_sql(select_sql, connection).iloc[0]['count'])

    except SQLAlchemyError or EnvironmentError:
        traceback.print_exc()

    finally:
        connection.close()

    return count


def get_stock_trends(code=None, start_date=datetime(1995, 5, 2), end_date=datetime.today()):
    """
    Get all stock trends from start_date to end_date.

    :param code: (string, default=None)
        6 digit number string code of stock. If code is None, select all stock codes.
    :param start_date: (datetime, default=datetime(1995, 5, 2))
        datetime(1995, 5, 2) is the first day of KRX stock data.
    :param end_date: (datetime, default=datetime.today())

    :return stock_trends: (DataFrame)
        index       code                    | (string) 6 digit number string code of stock.
                    date                    | (datetime)
        columns     volume                  | (bigint)
                    open                    | (float)
                    high                    | (float)
                    low                     | (float)
                    close                   | (float)
                    market_capitalization   | (bigint)
                    listed_stocks_number    | (bigint)
                    adj_close               | (float)
    """
    schema_name = 'stock_trend'
    select_sql = "SELECT * FROM {}".format(schema_name)
    stock_trends = pd.DataFrame()
    connection = get_connection()

    # WHERE clause
    _end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
    select_sql += " WHERE `date` BETWEEN '{}' AND '{}'".format(start_date, _end_date)
    if code:
        if code is not None:
            select_sql += " AND `code` = '{}'".format(code)

    try:
        # get all stock codes from the db.
        stock_trends = pd.read_sql(select_sql, connection, parse_dates=['date'])
        stock_trends.set_index(['code', 'date'], inplace=True)

    except SQLAlchemyError or EnvironmentError:
        traceback.print_exc()

    finally:
        connection.close()

    return stock_trends
