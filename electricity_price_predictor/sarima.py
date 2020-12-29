
from electricity_price_predictor.data import get_shifted_price, get_all
from statsmodels.tsa.stattools import adfuller
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.preprocessing import StandardScaler


def get_daily(hour=11):
    '''it gets hourly price data by calling get_shifted_price from data.py and
    returns a daily {hour} o'clock price dataframe'''
    df = get_shifted_price()
    df = df[df.index.hour==hour]
    return df

def get_mape(y_true, y_pred):
    '''it takes two lists or pd.series (y_true, y_pred) and returns
    mean absolute percentage error'''
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    mape = np.round(mape,2)
    return f'{mape}%'

def get_mase(y_true, y_pred, train_y):
    '''it takes two lists or pd.series (y_true, y_pred) and returns
    mean absolute scaled error'''
    y_true, y_pred, train_y = np.array(y_true), np.array(y_pred), np.array(train_y)
    upper = np.mean(np.abs(y_pred-y_true))
    train_t = train_y[:-1]
    train_t_1 = train_y[1:]
    lower = np.mean(np.abs(train_t-train_t_1))
    mase = np.round(upper/lower, 2)
    return str(mase)

def plot_forecast(forecast, train, test, lower_int, upper_int, mape=None, mase=None):
    '''it will plot a forecast'''
    plt.figure(figsize=(10,4), dpi=100)
    plt.plot(train, label='training', color='black')
    plt.plot(test, label='actual', color='black', ls='--')
    plt.plot(forecast, label='forecast', color='orange')
    plt.fill_between(forecast.index, lower_int, upper_int, color='k', alpha=.15)
    title = 'Forecast vs Actuals'
    if isinstance(mape, str):
        title +=f' MAPE:{mape}'
    if isinstance(mase, str):
        title +=f' MASE:{mase}'
    plt.title(title)
    plt.legend(loc='upper left', fontsize=8)

######### feature exploration and walk forward validation of sarimax ###########

def train_sarimax(data=False, hour=11,
                 split_date='2019-10-22 11:00:00',
                 n=30, exog=False):
    '''hour: hour of a day (0, 23),
    split_date: train, test splitted on this date,
    n: number of days that will be forecasted,
    exog: takes ([exog features], order, seasonal_order)
    returns forecast, upper_intervals, lower_intervals, mape, mase, test_set, train_set'''

    if isinstance(data, bool):
        if isinstance(exog, bool):
            df = get_daily(hour=hour)
        else:
            df = get_all(hour=hour)
    else:
        df=data
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
        predict_date = df[df.index == split_date[0]].index + pd.Timedelta(days=i)
        train_set = df[df.index < predict_date[0]]
        train_set.index = pd.DatetimeIndex(train_set.index.values,
                               freq=train_set.index.inferred_freq)
        # Build Model without exogenous features
        if isinstance(exog, bool):
            sarima = SARIMAX(train_set, order=(1, 1, 1),
                                        seasonal_order=(1,0,2,7))
            sarima = sarima.fit(maxiter=200)
            # Forecast
            results = sarima.get_forecast(1, alpha=0.05)
            forecast = sarima.forecast(1, alpha=0.05)
            confidence_int = results.conf_int()
        # Build Model with exogenous features
        else:
            # training model
            sarima = SARIMAX(train_set.price, exog=train_set[exog[0]],
                         order=exog[1], seasonal_order=exog[2])
            sarima = sarima.fit(maxiter=200)
            # get features for forecast
            exog_fore = test[test.index==predict_date[0]][exog[0]]
            # forecasting
            results = sarima.get_forecast(1, exog=exog_fore, alpha=0.05)
            forecast = sarima.forecast(1, exog=exog_fore, alpha=0.05)
            confidence_int = results.conf_int()
        # add forecast result into the list
        lower.append(confidence_int['lower price'][0])
        upper.append(confidence_int['upper price'][0])
        forecasts.append(forecast[0])

    # calculate the mape
    mape = get_mape(test.price, forecasts)
    mase = get_mase(test.price, forecasts, train.price)
    # create forecast df with datetimeIndex
    forecast = pd.DataFrame(forecasts, index=test.index, columns=['price'])

    return forecast, lower, upper, mape, mase, train, test
