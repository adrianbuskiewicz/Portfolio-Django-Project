import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt


def portfolios_simulation(companies, start, end):
    companies_symbols = [company.symbol for company in companies]
    prices = yf.download(companies_symbols, start=start, end=end)
    close_prices = prices['Adj Close']

    logarithmic_rates = close_prices.pct_change().apply(lambda x: np.log(1 + x))

    cov_matrix = logarithmic_rates.cov()

    # ind_er = close_prices.resample('Y').last().pct_change().mean()
    ind_er = logarithmic_rates.mean()*250

    ann_sd = logarithmic_rates.std().apply(lambda x: x * np.sqrt(250))

    assets = pd.concat([ind_er, ann_sd], axis=1)
    assets.columns = ['RoR', 'Volatility']

    p_ret = []
    p_vol = []
    p_weights = []

    num_assets = len(close_prices.columns)
    num_portfolios = 10000

    for portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights = weights / np.sum(weights)
        p_weights.append(weights)
        returns = np.dot(weights, ind_er)

        p_ret.append(returns)
        var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()
        sd = np.sqrt(var)
        ann_sd = sd * np.sqrt(250)
        p_vol.append(ann_sd)

    data = {'RoR': p_ret, 'Volatility': p_vol}

    for counter, symbol in enumerate(close_prices.columns.tolist()):
        data[symbol] = [w[counter] for w in p_weights]

    return pd.DataFrame(data)


def mvp_calculate(companies, start, end):
    portfolios = portfolios_simulation(companies, start, end)
    mvp = portfolios.iloc[portfolios['Volatility'].idxmin()]
    ror = round(mvp.loc['RoR'] * 100, 4)
    vol = round(mvp.loc['Volatility'] * 100, 4)
    companies_weights = {symbol: round(mvp.loc[symbol] * 100, 2) for symbol in mvp.index[2:]}
    return {'rate_of_return': ror, 'volatility': vol, 'companies_weights': companies_weights}


def orp_calculate(companies, start, end, rf):
    portfolios = portfolios_simulation(companies, start, end)
    orp = portfolios.iloc[((portfolios['RoR'] - (rf/100)) / portfolios['Volatility']).idxmax()]
    ror = round(orp.loc['RoR'] * 100, 4)
    vol = round(orp.loc['Volatility'] * 100, 4)
    companies_weights = {symbol: round(orp.loc[symbol] * 100, 2) for symbol in orp.index[2:]}
    return {'rate_of_return': ror, 'volatility': vol, 'companies_weights': companies_weights}


def get_actual_price(symbol):
    start_time = dt.datetime.now() - dt.timedelta(hours=1)
    df = yf.download(tickers=symbol, start=start_time, interval='5m')
    # date = df.index[-1]
    price = df.loc[df.index[-1], 'Adj Close']
    return {'date': dt.datetime.now(), 'price': round(price, 2)}


def calculate_stocks_amount(budget, weight, symbol):
    amount = (budget*weight/100)//get_actual_price(symbol)['price']
    return amount


