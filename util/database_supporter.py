# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2018. 1. 10.
"""
import argparse
import os

from sqlalchemy import create_engine

database = 'willbe'

aws_endpoint = 'findb.cay7taoqqrm6.ap-northeast-2.rds.amazonaws.com'
aws_user = 'jaekyoungkim'
aws_password = 'willbelucky'
aws_engine = create_engine(
    'mysql+mysqlconnector://{}:{}@{}/{}'.format(aws_user, aws_password, aws_endpoint, database),
    encoding='utf-8', pool_recycle=1, pool_size=2 * (os.cpu_count() or 1))

engine_pool = {
    'aws': aws_engine,
}


def get_connection(engine_key=None):
    """
    Get connection of the script parameter's db. If there is no script parameter, default db is local.

    :return Connection:
    """
    if engine_key is None:
        engine_key = _get_engine_key()

    if engine_key not in engine_pool.keys():
        raise EnvironmentError("{} is not in engine_pool. Please check your script parameters.".format(engine_key))

    return engine_pool[engine_key].connect()


def _get_engine_key():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--engine_key',
        type=str,
        default='aws',
        help='Directory to put the log data.'
    )

    flags, unparsed = parser.parse_known_args()
    return flags.engine_key
