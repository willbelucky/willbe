# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2018. 1. 20.
"""
from argparse import ArgumentTypeError
from datetime import datetime


def valid_date_type(arg_date_str):
    """custom argparse *date* type for user dates values given from the command line"""
    try:
        return datetime.strptime(arg_date_str, "%Y-%m-%d")
    except ValueError:
        msg = "Given Date ({0}) not valid! Expected format, YYYY-mm-dd!".format(arg_date_str)
        raise ArgumentTypeError(msg)


def valid_datetime_type(arg_datetime_str):
    """custom argparse type for user datetime values given from the command line"""
    try:
        return datetime.strptime(arg_datetime_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        msg = "Given Datetime ({0}) not valid! Expected format, 'YYYY-mm-dd HH:MM:SS'!".format(arg_datetime_str)
        raise ArgumentTypeError(msg)
