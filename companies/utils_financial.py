import pandas_datareader.data as web
import pandas as pd


def company_df(symbols=None):
    df = web.DataReader(symbols, 'yahoo')
    df = df['Adj Close']
    df.fillna('mean')
    return df


def df_mean_price(symbol):
    df = company_df(symbol)
    return df.mean()


def df_vol_price(symbol):
    df = company_df(symbol)
    return df.std()
