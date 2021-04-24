import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import plot_roc_curve
from sklearn.metrics import accuracy_score, classification_report

logging.getLogger('main')

def predict_rf(df):

    x_cols = df[['rsi', 'k_percent', 'r_percent', 'macd', 'macd_ema', 'price_rate_of_change']]
    y_cols = df['predictions']

    x_train, x_test, y_train, y_test = train_test_split(x_cols, y_cols, random_state=0)

    rand_frst_clf = RandomForestClassifier(n_estimators=100, oob_score=True, criterion='gini', random_state=0)

    rand_frst_clf.fit(x_train,y_train)

    y_pred = rand_frst_clf.predict(x_test)

    accuracy = accuracy_score(y_test, rand_frst_clf.predict(x_test), normalize=True) * 100.0

    logging.debug(f'Assertividade (%): {accuracy}')



    pass
