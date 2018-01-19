# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2018. 1. 19.
"""
from fake_useragent import UserAgent

ua = UserAgent()


def get_random_user_agent():
    return ua.random
