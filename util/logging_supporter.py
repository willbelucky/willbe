# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2018. 1. 20.
"""
import logging as lg
import os

# Set the root directory to your working directory.
# For example, /Users/willbe/PycharmProjects/willbe
LOG_DIR = os.getcwd().replace(chr(92), '/') + '/logs/'

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0


def get_logger(logger_name, file_name, level):
    """
    logger = logging.get_logger('evaluationLogger', flags.log_dir, 'evaluation', logging.INFO)
    logger.info("Write logs here.")

    :param logger_name: The name of logger.
    :param file_name: The name of the file where the logger write logs.
    :param level: Set the logging level of this logger.
    :return logger: The logger that we set.
    """
    logger = lg.getLogger(logger_name)
    fomatter = lg.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s >\t%(message)s')

    # 스트림과 파일로 로그를 출력하는 핸들러를 각각 만든다.
    file_handler = lg.FileHandler(LOG_DIR + file_name + '.log')
    stream_handler = lg.StreamHandler()

    # 각 핸들러에 포매터를 지정한다.
    file_handler.setFormatter(fomatter)
    stream_handler.setFormatter(fomatter)

    # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(level)

    return logger
