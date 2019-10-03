# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2018. 1. 10.
"""
import json
from datetime import datetime
from io import BytesIO, StringIO

import pandas as pd
import requests

from table.tables import StockMaster
import scrapper.database_reader as dr

delisted_stock_master_usecols = {'isu_cd': 'code', 'shrt_isu_cd': 'short_code', 'isu_nm': 'company_name',
                                 'market_name': 'market_name'}
stock_master_index = ['code']


def get_stock_masters():
    """
    Get stock_master of the date by scrapping KRX.

    :return stock_masters: (DataFrame)
        index       code        | (string) with 6 length numbers.
        columns     name        | (string)
    """
    # Listed Stock Master
    # STEP 01: Generate OTP
    gen_otp_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
    gen_otp_data = {
        'bld': 'COM/finder_stkisu',
        'name': 'form',
        '_': '1515578494324',
    }

    r = requests.get(url=gen_otp_url, params=gen_otp_data)
    code = r.content

    # STEP 02: download
    down_url = 'http://marketdata.krx.co.kr/contents/MKD/99/MKD99000001.jspx'
    down_data = {
        'no': 'P1',
        'mktsel': 'ALL',
        'pagePath': '/contents/COM/FinderStkIsu.jsp',
        'code': code,
        'pageFirstCall': 'Y'
    }

    r = requests.post(down_url, down_data)
    dict_stock_masters = json.loads(str(BytesIO(r.content).getvalue()))['block1']
    listed_stock_masters = pd.DataFrame(dict_stock_masters)
    listed_stock_masters = listed_stock_masters.rename(columns={'full_code': 'code',
                                                                'codeName': 'company_name',
                                                                'marketName': 'market_name'})

    # Delisted Stock Master
    # STEP 01: Generate OTP
    gen_otp_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
    gen_otp_data = {
        'bld': 'COM/finder_dellist_isu',
        'name': 'form',
        '_': '1515817443613',
    }

    r = requests.post(gen_otp_url, gen_otp_data)
    code = r.content

    # STEP 02: download
    down_url = 'http://marketdata.krx.co.kr/contents/MKD/99/MKD99000001.jspx'
    down_data = {
        'isuCd': '',
        'mktsel': 'ALL',
        'searchText': '',
        'pagePath': '/contents/COM/FinderDelListIsu.jsp',
        'code': code,
        'pageFirstCall': 'Y'
    }

    r = requests.post(down_url, down_data)
    dict_stock_masters = json.loads(BytesIO(r.content).getvalue())['result']
    delisted_stock_masters = pd.DataFrame(dict_stock_masters)
    delisted_stock_masters = delisted_stock_masters[list(delisted_stock_master_usecols.keys())]
    delisted_stock_masters = delisted_stock_masters.rename(columns=delisted_stock_master_usecols)

    stock_masters = pd.concat([listed_stock_masters, delisted_stock_masters])
    stock_masters.set_index(stock_master_index, inplace=True, verify_integrity=True)

    return stock_masters

stock_daily_price_index = ['code', 'date']


def get_stock_daily_prices(date=datetime.today()):
    """
    Get stock_daily_price of the date by scrapping KRX.

    :param date: (datetime)

    :return stock_daily_prices: (DataFrame)
        index       date                    | (datetime)
                    code                    | (string)
        columns     volume                  | (integer)
                    open                    | (float)
                    high                    | (float)
                    low                     | (float)
                    close                   | (float)
                    market_capitalization   | (integer)
                    listed_stocks_number    | (integer)
    """
    str_date = date.strftime("%Y%m%d")

    # STEP 01: Generate OTP
    gen_otp_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
    gen_otp_data = {
        'name': 'fileDown',
        'filetype': 'xls',
        'url': 'MKD/04/0404/04040200/mkd04040200_01',
        'market_gubun': 'ALL',  # 시장구분: ALL=전체
        'indx_ind_cd': '',
        'sect_tp_cd': 'ALL',
        'schdate': str_date,
        'pagePath': '/contents/MKD/04/0404/04040200/MKD04040200.jsp',
    }

    r = requests.post(url=gen_otp_url, data=gen_otp_data)
    code = r.content

    # STEP 02: download
    down_url = 'http://file.krx.co.kr/download.jspx'
    down_data = {
        'code': code,
    }
    headers = {
        'referer': gen_otp_url,
    }

    r = requests.post(down_url, down_data, headers=headers)
    stock_daily_prices = pd.read_excel(BytesIO(r.content), thousands=',')

    stock_daily_prices['날짜'] = date

    stock_daily_prices = stock_daily_prices.set_index(['날짜', '종목코드'])

    return stock_daily_prices


stock_trend_usecols = {'투자자명': 'investor', '거래량_매수': 'buy', '거래량_매도': 'sell'}
stock_trend_columns = ['투자자명', '거래량_매수', '거래량_매도']


def get_stock_trends(date):
    """
    Get korean stock trends from start_date to end_date by scrapping KRX.

    :param date: (datetime)
    :return stock_trends: (DataFrame)
        index       date                            | (datetime)
                    code                            | (string)
        columns     bank_buy                        | (int64)
                    bank_sell                       | (int64)
                    foreigner_buy                   | (int64)
                    foreigner_sell                  | (int64)
                    government_buy                  | (int64)
                    government_sell                 | (int64)
                    individual_buy                  | (int64)
                    individual_sell                 | (int64)
                    insurance_buy                   | (int64)
                    insurance_sell                  | (int64)
                    investing_organization_buy      | (int64)
                    investing_organization_sell     | (int64)
                    investment_trust_buy            | (int64)
                    investment_trust_sell           | (int64)
                    other_corporation_buy           | (int64)
                    other_corporation_sell          | (int64)
                    other_finance_buy               | (int64)
                    other_finance_sell              | (int64)
                    other_foreigner_buy             | (int64)
                    other_foreigner_sell            | (int64)
                    pension_fund_buy                | (int64)
                    pension_fund_sell               | (int64)
                    private_equity_fund_buy         | (int64)
                    private_equity_fund_sell        | (int64)
    """
    if dr.count_stock_daily_prices(start_date=date, end_date=date) == 0:
        return pd.DataFrame()

    stock_masters = StockMaster.instance().select().values()

    stock_daily_prices = dr.get_stock_daily_prices(start_date=date, end_date=date)

    if len(stock_daily_prices) == 0:
        return pd.DataFrame()

    results = []
    for index, row in stock_daily_prices.iterrows():
        code = index[0]

        # Set the short_code by stock_masters.
        short_code = stock_masters.loc[code, 'short_code']
        company_name = stock_masters.loc[code, 'company_name']

        results.append(get_stock_trend(date, code, short_code, company_name))

    # Concat results
    if len(results) > 0:
        stock_trends = pd.concat(results)
    else:
        raise RuntimeError("{} has no result.".format(date))

    return stock_trends


def get_stock_trend(date, code, short_code, company_name):
    # STEP 01: Generate OTP
    gen_otp_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
    gen_otp_data = {
        'name': 'fileDown',
        'filetype': 'csv',
        'url': 'MKD/10/1002/10020101/mkd10020101',
        'isu_cdnm': '{}/{}'.format(short_code, company_name),
        'isu_cd': '{}'.format(code),
        'isu_srt_cd': '{}'.format(short_code),
        'fromdate': date.strftime('%Y%m%d'),
        'todate': date.strftime('%Y%m%d'),
        'pagePath': '/contents/MKD/10/1002/10020101/MKD10020101.jsp',
    }

    r = requests.get(url=gen_otp_url, params=gen_otp_data)
    request_code = r.content

    # STEP 02: download
    down_url = 'http://file.krx.co.kr/download.jspx'
    down_data = {
        'code': request_code,
    }

    csv_str = requests.post(down_url, down_data).text

    # Remove the last row, which has sum.
    csv_str = '\n'.join(csv_str.split('\n')[:-1])

    # Return empty DataFrame if stock_trends are empty.
    if csv_str is "":
        return pd.DataFrame()

    one_company_trend = pd.read_csv(StringIO(csv_str), thousands=',', engine='python')

    one_company_trend = one_company_trend[stock_trend_columns]
    # Change column names.
    one_company_trend.rename(columns=stock_trend_usecols, inplace=True)
    investing_organization_buy = one_company_trend[one_company_trend['investor'] == '금융투자']['buy'].iloc[0]
    investing_organization_sell = one_company_trend[one_company_trend['investor'] == '금융투자']['sell'].iloc[0]
    insurance_buy = one_company_trend[one_company_trend['investor'] == '보험']['buy'].iloc[0]
    insurance_sell = one_company_trend[one_company_trend['investor'] == '보험']['sell'].iloc[0]
    investment_trust_buy = one_company_trend[one_company_trend['investor'] == '투신']['buy'].iloc[0]
    investment_trust_sell = one_company_trend[one_company_trend['investor'] == '투신']['sell'].iloc[0]
    private_equity_fund_buy = one_company_trend[one_company_trend['investor'] == '사모']['buy'].iloc[0]
    private_equity_fund_sell = one_company_trend[one_company_trend['investor'] == '사모']['sell'].iloc[0]
    bank_buy = one_company_trend[one_company_trend['investor'] == '은행']['buy'].iloc[0]
    bank_sell = one_company_trend[one_company_trend['investor'] == '은행']['sell'].iloc[0]
    other_finance_buy = one_company_trend[one_company_trend['investor'] == '기타금융']['buy'].iloc[0]
    other_finance_sell = one_company_trend[one_company_trend['investor'] == '기타금융']['sell'].iloc[0]
    pension_fund_buy = one_company_trend[one_company_trend['investor'] == '연기금']['buy'].iloc[0]
    pension_fund_sell = one_company_trend[one_company_trend['investor'] == '연기금']['sell'].iloc[0]
    government_buy = one_company_trend[one_company_trend['investor'] == '국가.지자체']['buy'].iloc[0]
    government_sell = one_company_trend[one_company_trend['investor'] == '국가.지자체']['sell'].iloc[0]
    other_corporation_buy = one_company_trend[one_company_trend['investor'] == '기타법인']['buy'].iloc[0]
    other_corporation_sell = one_company_trend[one_company_trend['investor'] == '기타법인']['sell'].iloc[0]
    individual_buy = one_company_trend[one_company_trend['investor'] == '개인']['buy'].iloc[0]
    individual_sell = one_company_trend[one_company_trend['investor'] == '개인']['sell'].iloc[0]
    foreigner_buy = one_company_trend[one_company_trend['investor'] == '외국인']['buy'].iloc[0]
    foreigner_sell = one_company_trend[one_company_trend['investor'] == '외국인']['sell'].iloc[0]
    other_foreigner_buy = one_company_trend[one_company_trend['investor'] == '기타외국인']['buy'].iloc[0]
    other_foreigner_sell = one_company_trend[one_company_trend['investor'] == '기타외국인']['sell'].iloc[0]

    stock_trend = pd.DataFrame(data={
        'investing_organization_buy': [investing_organization_buy],
        'investing_organization_sell': [investing_organization_sell],
        'insurance_buy': [insurance_buy],
        'insurance_sell': [insurance_sell],
        'investment_trust_buy': [investment_trust_buy],
        'investment_trust_sell': [investment_trust_sell],
        'private_equity_fund_buy': [private_equity_fund_buy],
        'private_equity_fund_sell': [private_equity_fund_sell],
        'bank_buy': [bank_buy],
        'bank_sell': [bank_sell],
        'other_finance_buy': [other_finance_buy],
        'other_finance_sell': [other_finance_sell],
        'pension_fund_buy': [pension_fund_buy],
        'pension_fund_sell': [pension_fund_sell],
        'government_buy': [government_buy],
        'government_sell': [government_sell],
        'other_corporation_buy': [other_corporation_buy],
        'other_corporation_sell': [other_corporation_sell],
        'individual_buy': [individual_buy],
        'individual_sell': [individual_sell],
        'foreigner_buy': [foreigner_buy],
        'foreigner_sell': [foreigner_sell],
        'other_foreigner_buy': [other_foreigner_buy],
        'other_foreigner_sell': [other_foreigner_sell],
    })

    # Set a code of the company.
    stock_trend['code'] = code

    # Set date.
    stock_trend['date'] = date

    # Set index.
    stock_trend = stock_trend.set_index(['code', 'date'])

    return stock_trend
