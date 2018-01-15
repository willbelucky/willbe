# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2018. 1. 10.
"""
import os
import time
import traceback
from datetime import datetime
from pathlib import Path

from sqlalchemy import types
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, InterfaceError

import scrapper.database_reader as dr
from scrapper import krx
from scrapper.sql import stock_master_create_table_sql, stock_daily_price_create_table_sql, stock_trend_create_table_sql
from table.base import DATA_DIR
from util.database_supporter import get_connection
from util.date_supporter import get_business_days
from util.pandas_expansion import df_difference
from util.parallel_process_supporter import parallel_process


def save_stock_masters():
    """
    Save stock masters of date.

    """
    schema_name = 'stock_master'
    connection = get_connection()
    try:
        connection.execute(stock_master_create_table_sql)
        old_stock_masters = dr.get_stock_masters()
        new_stock_masters = krx.get_stock_masters()

        new_stock_masters = df_difference(new_stock_masters, old_stock_masters)

        try:
            # Save new_stock_masters to database.
            new_stock_masters.to_sql(schema_name, connection, if_exists='append',
                                     dtype={'code': types.VARCHAR(12), 'short_code': types.VARCHAR(9),
                                            'company_name': types.VARCHAR(255), 'market_name': types.VARCHAR(16)})

            if len(new_stock_masters) != 0:
                # Replace stock_master.csv
                stock_masters = dr.get_stock_masters()
                csv_file_path = DATA_DIR + schema_name + '.csv'
                stock_masters.to_csv(csv_file_path, encoding='utf-8')
                print('Replace {}'.format(csv_file_path))

                # Remove stock_master.h5
                hdf_file_path = DATA_DIR + schema_name + '.h5'
                if Path(hdf_file_path).exists():
                    os.remove(hdf_file_path)
                    print('Remove {}'.format(hdf_file_path))

        except IntegrityError:
            pass

    except SQLAlchemyError or EnvironmentError:
        traceback.print_exc()

    finally:
        connection.close()


def save_stock_daily_prices(start_date=datetime(1995, 5, 2), end_date=datetime.today()):
    """
    Save stock prices from start date to end date.

    :param start_date: (datetime, default=datetime(1995, 5, 2))
        datetime(1995, 5, 2) is the first day that have data.
    :param end_date: (datetime, default=datetime.today())
    """
    schema_name = 'stock_daily_price'
    start_time = time.time()
    print("Scrapping {}...".format(schema_name))

    # create a table if not exists.
    connection = get_connection()
    try:
        connection.execute(stock_daily_price_create_table_sql)
    except SQLAlchemyError or EnvironmentError:
        traceback.print_exc()

    finally:
        connection.close()

    dates = get_business_days(start_date, end_date).sort_values(ascending=False)
    parallel_process(save_stock_daily_price, dates, timeout=None)

    print(
        "Scrapping {} of {} days is done taking {} seconds!!".format(schema_name, len(dates), time.time() - start_time))


def save_stock_daily_price(date=datetime.today(), create_table=False):
    """
    Save stock prices of date.

    :param date: (datetime, default=datetime.today())
    :param create_table: whether execute create_table_sql or not.
    """
    schema_name = 'stock_daily_price'
    connection = get_connection()
    try:
        if create_table:
            # create a table if not exists.
            connection.execute(stock_daily_price_create_table_sql)

        old_stock_daily_prices = dr.get_stock_daily_prices(code=None, start_date=date, end_date=date)
        new_stock_daily_prices = krx.get_stock_daily_prices(date=date)

        new_stock_daily_prices = df_difference(new_stock_daily_prices, old_stock_daily_prices)

        try:
            new_stock_daily_prices.to_sql(schema_name, connection, if_exists='append',
                                          dtype={'code': types.VARCHAR(12)})
            print('Insert {}, count {}'.format(date, len(new_stock_daily_prices)))

        except IntegrityError:
            pass

    except SQLAlchemyError or EnvironmentError or InterfaceError or AssertionError:
        print('Exception occur in date:{}'.format(date))
        traceback.print_exc()

    finally:
        connection.close()


def save_stock_trends(start_date=datetime(1995, 5, 2), end_date=datetime.today()):
    # 날짜 구해서 역수로 돌려가며 save_stock_trend 병렬로
    schema_name = 'stock_trend'
    start_time = time.time()
    print("Scrapping {}...".format(schema_name))

    # create a table if not exists.
    connection = get_connection()
    try:
        connection.execute(stock_trend_create_table_sql)
    except SQLAlchemyError or EnvironmentError:
        traceback.print_exc()
    finally:
        connection.close()

    dates = get_business_days(start_date, end_date).sort_values(ascending=False)
    parallel_process(save_stock_trend, dates)

    print(
        "Scrapping {} of {} days is done taking {} seconds!!".format(schema_name, len(dates), time.time() - start_time))


def save_stock_trend(date):
    schema_name = 'stock_trend'
    connection = get_connection()

    try:
        # 데이터베이스에 이 날짜로 데이터 있는지 확인하고
        # 없으면 다음 진행
        count = dr.count_stock_trends(start_date=date, end_date=date)
        if count is not 0:
            return

        # 주식마스터 돌면서 데이터 크롤링해와서 모으고
        old_stock_trends = dr.get_stock_trends(code=None, start_date=date, end_date=date)
        new_stock_trends = krx.get_stock_trends(date)

        new_stock_trends = df_difference(new_stock_trends, old_stock_trends)

        # 마지막에 저장
        try:
            new_stock_trends.to_sql(schema_name, connection, if_exists='append', dtype={'code': types.VARCHAR(12)})
            print('Insert {}, count {}'.format(date, len(new_stock_trends)))
        except IntegrityError:
            pass

    except SQLAlchemyError or EnvironmentError:
        traceback.print_exc()

    finally:
        connection.close()


if __name__ == '__main__':
    # save_stock_masters()
    # save_stock_daily_prices(start_date=datetime.today())
    save_stock_trends(start_date=datetime(2017, 12, 11), end_date=datetime(2017, 12, 11))
