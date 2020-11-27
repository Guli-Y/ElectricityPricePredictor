
from electricity_price_predictor.data import get_shifted_price
from statsmodels.tsa.stattools import adfuller
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX

def get_daily(hour=11):
    df = get_shifted_price()
    df = df[df.index.hour==hour]
    return df

def get_mape(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    mape = np.round(mape,2)
    return f'{mape}%'

def plot_forecast(forecast, train, test, lower_int, upper_int, mape=None):
    plt.figure(figsize=(10,4), dpi=100)
    plt.plot(train, label='training', color='black')
    plt.plot(test, label='actual', color='black', ls='--')
    plt.plot(forecast, label='forecast', color='orange')
    plt.fill_between(forecast.index, lower_int, upper_int, color='k', alpha=.15)
    if isinstance(mape, str):
        plt.title(f'Forecast vs Actuals, MAPE:{mape}')
    else:
        plt.title('Forecast vs Actuals')
    plt.legend(loc='upper left', fontsize=8)

def train_sarima(hour=11, split_date = '2019-10-22 11:00:00', n=30):
    '''take hour, date and a number(n) and forecast for next n days and returns
    forecast, upper_intervals, lower_intervals, mape, test'''

    df = get_daily(hour=hour)
    # formating split_date
    split_date = pd.DatetimeIndex(np.array([split_date]))

    # get train and test for plotting only
    train = df[(df.index <= split_date[0])]
    test = df[(df.index > split_date[0]) & \
                      (df.index <= (split_date + pd.Timedelta(days=n))[0])]

    # will collect following information from forecast
    forecasts = []
    upper = []
    lower = []

    # loop over to get walk forward forecast for n days
    for i in range(1, n+1):

        # walk one day forward to set train_set
        new_date = df[df.index == split_date[0]].index + pd.Timedelta(days=i)
        train_set = df[df.index < new_date[0]]

        # Build Model
        sarima = SARIMAX(train_set, order=(1, 1, 1), seasonal_order=(1,0,1,7), freq='D')
        sarima = sarima.fit()

        # Forecast
        results = sarima.get_forecast(1, alpha=0.05)
        forecast = sarima.forecast(1, alpha=0.05)
        confidence_int = results.conf_int()

        # add forecast result into the list
        lower.append(confidence_int['lower price'][0])
        upper.append(confidence_int['upper price'][0])
        forecasts.append(forecast[0])

    # calculate the mape
    mape = get_mape(test.price, forecasts)

    # create forecast df with datetimeIndex
    forecast = pd.DataFrame(forecasts, index=test.index, columns=['price'])

    return forecast, lower, upper, mape, train, test

def plot_sarima_forecast(hour=11, split_date = '2019-10-22 11:00:00', n=30):
    forecast, lower, upper, mape, train, test = \
    train_sarima(hour=hour, split_date=split_date, n=n)
    plot_forecast(forecast, train.iloc[-150:], test, lower, upper, mape=mape)

