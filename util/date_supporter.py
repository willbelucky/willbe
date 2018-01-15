import pandas as pd


def get_business_days(start_date, end_date):
    return pd.date_range(start_date, end_date, freq='B')
