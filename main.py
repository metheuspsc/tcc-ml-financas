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


def get_tickers():
    with open(rf".\data\bova\BOVA11.csv", "r") as tickers:
        return [line.split(";")[0] for line in tickers.readlines()[1:]]


# TODO Regressão Lógistica
# TODO Explicar Indicadores, Análise técnica.
# TODO Objetivo comparar modelo mais clássico X Moderno


if __name__ == "__main__":

    results = pd.DataFrame(
        columns=["date", "ticker", "accuracy", "high_chance", "low_chance"]
    )

    for ticker in get_tickers():

        logging.info(f"Atualizando dados de {ticker}...")

        scrapper = Scrapper(ticker)

        logging.info(f"Calculando indicadores de {ticker}...")

        ticker_df = pd.read_csv(
            rf".\data\tickers\{ticker}.csv",
            names=["date", "open", "high", "low", "close", "adj close", "volume"],
        )

        if len(ticker_df) > 30:
            today = ticker_df.date.iat[-1]

            logging.info(f"Gerando previsão do dia {today} para {ticker}...")

            process(ticker_df)
            accuracy, high_chance, low_chance = predict_rf(ticker_df)

            results = results.append(
                {
                    "date": today,
                    "ticker": ticker,
                    "accuracy": accuracy,
                    "high_chance": high_chance,
                    "low_chance": low_chance,
                },
                ignore_index=True,
            )
        else:
            logging.info(f"Dados insuficientes de {ticker}...")

    results.to_csv(f"results-{results.date.iat[-1]}.csv", index=False)
