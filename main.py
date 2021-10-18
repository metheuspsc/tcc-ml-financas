from dataclasses import dataclass

from scrapper import *
import logging
import pandas as pd
from process import process
from model import predict_rf

logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,
    handlers=[logging.FileHandler("progress.log"), logging.StreamHandler()],
)

# TODO Regressão Lógistica
# TODO Explicar Indicadores, Análise técnica.
# TODO Objetivo comparar modelo mais clássico X Moderno


if __name__ == "__main__":

    results = pd.DataFrame()

    tickers = pd.read_csv(rf".\data\bova\BOVA11.csv", sep=";")

    for index, ticker in tickers.iterrows():

        logging.info(f"Atualizando dados de {ticker['name']}...")

        scrapper = Scrapper(ticker["code"])

        logging.info(f"Calculando indicadores de {ticker['name']}...")

        ticker_df = pd.read_csv(
            rf".\data\tickers\{ticker['code']}.csv",
            names=["date", "open", "high", "low", "close", "adj close", "volume"],
        )

        if len(ticker_df) > 30:
            today = ticker_df.date.iat[-1]

            logging.info(f"Gerando previsão do dia {today} para {ticker['name']}...")

            process(ticker_df)
            folds = predict_rf(ticker_df)

            result = pd.DataFrame(
                {
                    "date": today,
                    "ticker": ticker["code"],
                    "company": ticker["name"],
                    "sector": ticker["sector"],
                }
                , index=[0]
            )

            result = pd.concat([result, folds], axis=1)

            results = results.append(result)
        else:
            logging.info(f"Dados insuficientes de {ticker}...")

    results.to_csv(rf"data\results\results-{results.date.iat[-1]}.csv", index=False)
