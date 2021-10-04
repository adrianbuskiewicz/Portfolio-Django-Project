import yfinance as yf
import numpy as np


def company_df(symbols=None, date_from=None, date_to=None):
    df = yf.download(
        symbols,
        start=date_from,
        end=date_to,
    )
    df = df['Adj Close']
    # Shifting allows as to divide n value by (n-1)
    df = np.log(df/df.shift(1))
    df.fillna(df.mean())
    return df


def df_mean_price(symbol, date_from=None, date_to=None):
    df = company_df(symbol, date_from=date_from, date_to=date_to)
    return round(df.mean()*100, 4)


def df_vol_price(symbol, date_from=None, date_to=None):
    df = company_df(symbol, date_from=date_from, date_to=date_to)
    return round(df.std()*100, 4)


def corr_matrix(rates_df, style):
    corr_mat = rates_df.corr()
    corr_mat = corr_mat.to_html()
    # This line of code allows to change df style in the template
    corr_mat = corr_mat.replace('class="dataframe"', style)
    return corr_mat
