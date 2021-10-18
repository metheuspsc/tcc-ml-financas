import logging
import os
from datetime import datetime, date
import requests
import pandas as pd

logging.getLogger("main")


class Scrapper:
    def __init__(self, _ticker):
        self.ticker = _ticker
        self.base_url = "https://query1.finance.yahoo.com/v7/finance/download"
        self.file_path = rf".\data\tickers\{_ticker}.csv"
        self.last_tick = self.check_file()
        self.today = datetime.now()
        self.start_date = self.to_timestamp(self.last_tick)
        self.end_date = self.to_timestamp(self.today)
        self.df = pd.DataFrame(
            columns=["date", "open", "high", "low", "close", "adj close", "volume"]
        )
        self.request_rows()
        self.append()

    def check_file(self):
        if os.path.exists(self.file_path):
            last_tick = self.check_last_tick()
            return datetime.strptime(last_tick, "%Y-%m-%d")
        else:
            return 0

    def check_last_tick(self):
        with open(self.file_path, "r") as tick_data:
            return tick_data.readlines()[-1].split(",")[0]

    @staticmethod
    def to_timestamp(date):
        if date != 0:
            return round(datetime.timestamp(date))
        else:
            return date

    def request_rows(self):

        logging.info(
            f"Atualizando dados do ticker {self.ticker} a partir de {self.last_tick}"
        )

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(
            f"{self.base_url}/{self.ticker}.SA?period1={self.start_date}&period2={self.end_date}&interval=1d",
            headers=headers,
        )

        if response.status_code == 200:

            row_list = response.text.split("\n")[2:-1]

            if row_list:
                for row in row_list:
                    row = row.split(",")
                    self.df.loc[len(self.df)] = row
            else:
                logging.info(f"Dados do ticker {self.ticker} já são os mais atuais.")
        else:
            logging.info(f"Falha no request")

    def append(self):
        try:

            self.df.to_csv(self.file_path, mode="a", index=False, header=False)

            logging.info(
                f"Dados do ticker {self.ticker} atualizados no arquivo {self.file_path}"
            )

        except Exception as e:

            logging.warning(f"Erro {e} ao escrever arquivo {self.file_path}")
