import numpy as np


def process(df):
    df['price_change'] = calc_price_change(df)
    df['rsi'] = calc_rsi(df)
    df['k_percent'], df['r_percent'] = calc_k_r(df)
    df['macd'], df['macd_ema'] = calc_macd(df)
    df['price_rate_of_change'] = calc_prc(df)
    df['predictions'] = calc_predictions(df)
    df.dropna(inplace=True)


def calc_price_change(df):
    return df['adj close'].diff()


def calc_rsi(df):
    n = 5
    delta = df[['price_change']]
    up_df, down_df = delta.copy(), delta.copy()

    up_df[up_df < 0] = 0
    down_df[down_df > 0] = 0

    ewma_up = up_df.ewm(span=n).mean()
    ewma_down = down_df.abs().ewm(span=n).mean()

    rs = ewma_up / ewma_down
    rsi = 100.0 - (100.0 / (1.0 + rs))

    return rsi


def calc_k_r(df):
    n = 14

    high_14 = df['high'].rolling(14).max()
    low_14 = df['low'].rolling(14).min()

    k_percent = 100 * ((df['close'] - low_14) / (high_14 - low_14))
    r_percent = ((high_14 - df['close']) / (high_14 - low_14)) * - 100

    return k_percent, r_percent


def calc_macd(df):
    ema_26 = df['close'].ewm(span=26).mean()
    ema_12 = df['close'].ewm(span=12).mean()
    macd = ema_12 - ema_26
    ema = macd.ewm(span=9).mean()
    return macd, ema


def calc_prc(df):
    n = 9
    return df['close'].pct_change(periods=n)


def calc_predictions(df):
    close_groups = df['close']
    close_groups = close_groups.transform(lambda x: np.sign(x.diff()))
    close_groups.loc[close_groups == 0.0] = 1.0
    return close_groups
