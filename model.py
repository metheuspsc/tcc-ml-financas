import logging

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit
from sklearn.model_selection import train_test_split

logging.getLogger("main")


def model_params(df):
    today = df.tail(1)[
        [
            "rsi",
            "k_percent",
            "r_percent",
            "macd",
            "macd_ema",
            "price_rate_of_change",
        ]
    ]
    df.dropna(inplace=True)

    x_cols = df[
        [
            "rsi",
            "k_percent",
            "r_percent",
            "macd",
            "macd_ema",
            "price_rate_of_change",
        ]
    ]
    y_cols = df["predictions"]

    # x_train, x_test, y_train, y_test = train_test_split(
    #     x_cols, y_cols, random_state=0, shuffle=False
    # )

    return today, x_cols, y_cols


def rf_metrics(model, y_test, y_pred, x_cols):
    accuracy = accuracy_score(y_test, y_pred, normalize=True) * 100.0

    logging.info(f"Assertividade (%): {accuracy}")

    # feature_imp = pd.Series(model.feature_importances_, index=x_cols.columns).sort_values(ascending=False)
    #
    # print(feature_imp)


def predict_rf(df):
    rand_frst_clf = RandomForestClassifier(
        n_estimators=1600,
        max_features="log2",
        min_samples_split=10,
        min_samples_leaf=7,
        oob_score=False,
        criterion="gini",
        max_depth=10,
        bootstrap=True,
        random_state=0,
    )

    today, x_cols, y_cols = model_params(df)

    ts_split = TimeSeriesSplit(n_splits=5)
    folds = pd.DataFrame()
    for fold, (train_index, test_index) in enumerate(ts_split.split(x_cols)):
        x_train, x_test = x_cols.iloc[train_index], x_cols.iloc[test_index]
        y_train, y_test = y_cols.iloc[train_index], y_cols.iloc[test_index]

        rand_frst_clf.fit(x_train, y_train)

        y_pred = rand_frst_clf.predict(x_test)

        accuracy = accuracy_score(y_test, y_pred, normalize=True) * 100.0

        logging.info(f"Assertividade (%): {accuracy}")

        next = rand_frst_clf.predict_proba(today)[0]

        if len(next) == 1:
            low_chance = 1
            high_chance = 1
        else:
            low_chance = next[0]
            high_chance = next[1]

        logging.info(f"Previsão[{fold}] (%): Baixa :{low_chance}, Alta :{high_chance}")

        to_join = pd.DataFrame(
            {
                f"accuracy[{fold}]": accuracy,
                f"low_chance[{fold}]": low_chance,
                f"high_chance[{fold}]": high_chance,
            },
            index=[0]
        )
        folds = pd.concat([folds, to_join], axis=1)
    return folds


def get_random_grid():
    n_estimators = list(range(100, 2000, 100))

    max_features = ["auto", None, "log2"]

    max_depth = list(range(10, 110, 10))
    max_depth.append(None)

    min_samples_split = [2, 5, 10, 20, 30, 40]

    min_samples_leaf = [1, 2, 7, 12, 14, 16, 20]

    bootstrap = [True, False]

    return {
        "n_estimators": n_estimators,
        "max_features": max_features,
        "max_depth": max_depth,
        "min_samples_split": min_samples_split,
        "min_samples_leaf": min_samples_leaf,
        "bootstrap": bootstrap,
    }


def random_rf(df):
    rand_frst_clf = RandomForestClassifier()

    ts_split = TimeSeriesSplit(n_splits=5)

    # https://stackoverflow.com/questions/37583263/scikit-learn-cross-validation-custom-splits-for-time-series-data

    rf_random = RandomizedSearchCV(
        estimator=rand_frst_clf,
        param_distributions=get_random_grid(),
        n_iter=100,
        cv=ts_split,
        verbose=2,
        random_state=42,
        n_jobs=-1,
    )

    today, x_cols, y_cols, x_train, x_test, y_train, y_test = model_params(df)

    rf_random.fit(x_train, y_train)

    y_pred = rf_random.predict(x_test)

    best_params = rf_random.best_params_
    best_estim = rf_random.best_estimator_
    best_score = rf_random.best_score_
    best_index = rf_random.best_index_

    accuracy = accuracy_score(y_test, y_pred, normalize=True) * 100.0

    logging.info(f"Assertividade (%): {accuracy}")

    next = rf_random.predict_proba(today)
