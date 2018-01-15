import pandas as pd


def df_difference(df1, df2):
    """
    Get a difference of sets df1 from df2, and return it.

    :param df1: (DataFrame) something we want to have partially.
    :param df2: (DataFrame) something we want to filter.
    :return differences: (DataFrame) a difference of sets df1 from df2.
    """
    differences = df1.loc[df1.index.difference(df2.index).values]
    return differences


def df_cross_join(df1, df2, **kwargs):
    df1['_tmpkey'] = 1
    df2['_tmpkey'] = 1

    res = pd.merge(df1, df2, on='_tmpkey', **kwargs).drop('_tmpkey', axis=1)
    res.index = pd.MultiIndex.from_product((df1.index, df2.index))

    df1.drop('_tmpkey', axis=1, inplace=True)
    df2.drop('_tmpkey', axis=1, inplace=True)

    return res
