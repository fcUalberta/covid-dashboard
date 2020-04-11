# HWES example
from statsmodels.tsa.arima_model import ARIMA
from random import random

from statsmodels.tsa.holtwinters import ExponentialSmoothing
from random import random
# SARIMA example
from statsmodels.tsa.statespace.sarimax import SARIMAX
# contrived dataset
# data = [x + random() for x in range(1, 100)]
# print(data)
def forecast(data):
    predictions = []
    for i in range(7):
        # model = ARIMA(data, order=(1, 1, 1))
        # model_fit = model.fit(disp=False,transparams=False)
        # # make prediction
        model = SARIMAX(data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 1),
        trace=True, error_action="ignore")
        model_fit = model.fit(disp=False)

        yhat = model_fit.predict(len(data), len(data))
        # print(yhat)
        data.append(int(yhat))
        predictions.append(int(yhat))
    return predictions
# data = [x + random() for x in range(1, 5)]
# print(forecast(data))



# def create_movingAverage(df):
#
#     df['SimpleMAvg'] = df.iloc[:,1].rolling(window=7).mean()
#     df['CumulativeMAvg'] = df_T.expanding(min_periods=7).mean()
#     df['ExponentialMAvg'] = df_T.iloc[:,0].ewm(span=40,adjust=False).mean()
