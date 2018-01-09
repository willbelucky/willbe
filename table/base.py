# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2018. 1. 1.
"""
import os
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

idx = pd.IndexSlice

# Set the root directory to your working directory.
# For example, /Users/willbe/PycharmProjects/willbe
DATA_DIR = os.getcwd().replace(chr(92), '/') + '/data/'

# Datetime format
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class SingletonInstance:
    __instance = None

    @classmethod
    def __get_instance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kwargs):
        # noinspection PyArgumentList
        cls.__instance = cls(*args, **kwargs)
        cls.instance = cls.__get_instance
        return cls.__instance


class Table(SingletonInstance):
    """
    Example
    -------
    stock_minute_price_table = StockMinutePrice.instance()
    stock_minute_price = stock_minute_price_table.select()
                                                .where(from_date=datetime(2016, 1, 1), to_date=datetime(2016, 12, 31))
                                                .values()

    """
    __table_name = None
    __csv_file_remote_address = None
    __csv_file_dir = None
    __hdf_file_dir = None
    __table = None
    __selected_table = None
    __index = None
    __parse_dates = None

    @classmethod
    def __init__(cls, table_name, csv_file_remote_address, index=None, parse_dates=None):
        cls.__table_name = table_name
        cls.__csv_file_remote_address = csv_file_remote_address
        cls.__index = index
        cls.__parse_dates = parse_dates
        cls.__csv_file_dir = DATA_DIR + cls.__table_name + '.csv'
        cls.__hdf_file_dir = DATA_DIR + cls.__table_name + '.h5'

    @classmethod
    def __download_csv(cls, parse_dates=None):
        if cls.__csv_file_remote_address is not None:
            table = pd.read_csv(cls.__csv_file_remote_address, parse_dates=parse_dates, low_memory=False,
                                encoding='utf-8')
            print('Download {} from {}.'.format(cls.__table_name, cls.__csv_file_remote_address))
        else:
            raise FileNotFoundError('Both {} and {} is not exist.'.format(cls.__hdf_file_dir, cls.__csv_file_dir))

        return table

    @classmethod
    def __load_csv(cls, index=None, parse_dates=None):
        if cls.__csv_file_dir is None:
            raise AttributeError("{} doesn't have a csv file dir. Check __csv_file_dir of {}.".format(cls.__table_name,
                                                                                                      cls.__table_name))

        if Path(cls.__csv_file_dir).exists():
            table = pd.read_csv(cls.__csv_file_dir, parse_dates=parse_dates, low_memory=False, encoding='utf-8')
        else:
            table = cls.__download_csv(parse_dates=parse_dates)

        # Parse datetime format columns.
        if parse_dates is not None:
            for parse_date in parse_dates:
                table[parse_date] = pd.to_datetime(table[parse_date])

        # Set index.
        if index is not None:
            # Check the table has duplicated elements.
            if np.any(table.duplicated()):
                raise KeyError("{} has some duplicated elements.".format(cls.__table_name))
            table = table.set_index(index)
            table = table.sort_index()

        return table

    @classmethod
    def __load_hdf(cls):
        if cls.__hdf_file_dir is None:
            raise AttributeError("{} doesn't have a hdf file dir. Check __hdf_file_dir of {}.".format(cls.__table_name,
                                                                                                      cls.__table_name))
        table = pd.read_hdf(cls.__hdf_file_dir, 'table', encoding='utf-8')

        return table

    @classmethod
    def select(cls):
        assert cls.__table_name is not None

        # If this class did not cache a table, load the table and cache it.
        if cls.__table is None:

            # Before try csv format, try hdf format first because of speed issue.
            if Path(cls.__hdf_file_dir).exists():
                cls.__table = cls.__load_hdf()

            else:
                cls.__table = cls.__load_csv(index=cls.__index, parse_dates=cls.__parse_dates)

                # If the table has market_capitalization and listed_stocks_number,
                # adjust open, high, low, close fields.
                if 'market_capitalization' in cls.__table.columns and 'listed_stocks_number' in cls.__table.columns:
                    cls.__table['adj_close'] = cls.__table['market_capitalization'] / cls.__table[
                        'listed_stocks_number']
                    cls.__table['open'] = cls.__table['adj_close'] / cls.__table['close'] * cls.__table['open']
                    cls.__table['high'] = cls.__table['adj_close'] / cls.__table['close'] * cls.__table['high']
                    cls.__table['low'] = cls.__table['adj_close'] / cls.__table['close'] * cls.__table['low']
                    cls.__table['close'] = cls.__table['adj_close']
                    cls.__table = cls.__table.drop('adj_close', axis=1)
                    cls.__table = cls.__table.drop('market_capitalization', axis=1)
                    cls.__table = cls.__table.drop('listed_stocks_number', axis=1)

                # Save a hdf file.
                cls.__table.to_hdf(cls.__hdf_file_dir, 'table', encoding='utf-8')
                print('Create {}.'.format(cls.__hdf_file_dir))

        cls.__selected_table = cls.__table
        return cls

    @classmethod
    def where(cls,
              code=None, short_code=None, company_name=None,  # For StockMaster
              stock_masters=None, from_date=None, to_date=None  # For StockMinutePrice, StockDailyPrice
              ):
        assert cls.__table_name is not None

        if cls.__table is None:
            raise ValueError('__table of {} is None. Call select() first.'.format(cls.__table_name))

        # For StockMaster
        if code is not None:
            cls.__selected_table = cls.__selected_table.loc[idx[[code]], :]

        if short_code is not None:
            cls.__selected_table = cls.__selected_table.loc[cls.__selected_table['short_code'] == short_code]

        if company_name is not None:
            cls.__selected_table = cls.__selected_table.loc[cls.__selected_table['company_name'] == company_name]

        # For StockMinutePrice, StockDailyPrice
        if stock_masters is not None:
            cls.__selected_table = cls.__selected_table.loc[idx[stock_masters.index.values, :], :]

        if from_date is not None:
            cls.__selected_table = cls.__selected_table.loc[idx[:, from_date.strftime(DATETIME_FORMAT):], :]

        if to_date is not None:
            _to_date = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59)
            cls.__selected_table = cls.__selected_table.loc[idx[:, :_to_date.strftime(DATETIME_FORMAT)], :]

        return cls

    @classmethod
    def values(cls):
        assert cls.__table_name is not None

        if cls.__selected_table is None:
            raise ValueError('{}.__selected_table is None. Call select() first.'.format(cls.__table_name))

        # Reset __where_table to None.
        where_table = cls.__selected_table
        cls.__selected_table = None
        return where_table
