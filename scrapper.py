import os
from datetime import datetime
import requests
import csv
from config import TICKERS


class Scrapper:

    def __init__(self, _ticker):
        self.ticker = _ticker
        self.file_path = rf".\data\{_ticker}.csv"
        self.last_tick = self.check_file()
        self.start_date = self.to_timestamp(self.last_tick)
        self.end_date = self.to_timestamp(datetime.now())
        self.new_rows = self.request_rows()

    def check_file(self):
        if os.path.exists(self.file_path):
            last_tick = self.check_last_tick()
            return datetime.strptime(last_tick, "%Y-%m-%d")
        else:
            return 0

    def check_last_tick(self):
        with open(self.file_path, 'r') as tick_data:
            return tick_data.readlines()[-1].split(',')[0]

    @staticmethod
    def to_timestamp(date):
        if date != 0:
            return round(datetime.timestamp(date))
        else:
            return date

    def request_rows(self):

        response = requests.get(
            rf'https://query1.finance.yahoo.com/v7/finance/download/OIBR3.SA?period1={self.start_date}' +
            f'&period2={self.end_date}&interval=1d')

        return response.text.split('\n')[2:-1]

    def append(self):
        with open(self.file_path, 'a+', newline='') as tick_csv:
            csv_writer = csv.writer(tick_csv)
            if self.new_rows:
                for row in self.new_rows:
                    csv_writer.writerow(row.split(','))


if __name__ == '__main__':

    for ticker in TICKERS:
        scrapper = Scrapper(ticker)
        scrapper.append()
