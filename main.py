from scrapper import *
import logging
import pandas as pd
from process import process
from model import predict_rf


logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    level=logging.DEBUG,
                    handlers=[logging.FileHandler('progress.log'),
                              logging.StreamHandler()])


def get_tickers():
    with open(rf".\data\bova\BOVA11.csv", 'r') as tickers:
        return [line.split(';')[0] for line in tickers.readlines()[1:]]


def scrape():
    scrapper = Scrapper(ticker)
    scrapper.append()


if __name__ == '__main__':

    logging.debug('teste')

    for ticker in get_tickers():

        #scrape()

        ticker_df = pd.read_csv(rf".\data\tickers\{ticker}.csv",
                                names=['date', 'open', 'high', 'low', 'close', 'adj close', 'volume'])

        process(ticker_df)
        rf_result = predict_rf(ticker_df)

        pass