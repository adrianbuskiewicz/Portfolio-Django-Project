import yfinance as yf
import numpy as np


def company_df(symbols=None, date_from=None, date_to=None):
    df = yf.download(
        symbols,
        start=date_from,
        end=date_to,
    )
    df = df['Adj Close']
    df = np.log(df/df.shift(1))*100
    return df


def df_mean_price(symbol, date_from=None, date_to=None):
    df = company_df(symbol, date_from=date_from, date_to=date_to)
    return round(df.mean(), 4)


def df_vol_price(symbol, date_from=None, date_to=None):
    df = company_df(symbol, date_from=date_from, date_to=date_to)
    return round(df.std(), 4)


def corr_matrix(rates_df, style):
    corr_mat = rates_df.corr()
    corr_mat = corr_mat.to_html()
    corr_mat = corr_mat.replace('class="dataframe"', style)
    return corr_mat
