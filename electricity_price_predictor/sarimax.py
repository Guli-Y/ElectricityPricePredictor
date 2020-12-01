from electricity_price_predictor.data import get_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

def plot_forecast(forecast, train, lower_int, upper_int):
    '''it will plot a forecast'''
    plt.figure(figsize=(10,4), dpi=100)
    plt.plot(train, label='training', color='black')
    plt.plot(forecast, label='forecast', color='orange')
    plt.fill_between(forecast.index, lower_int, upper_int, color='k', alpha=.15)
    title = 'Electricity Price Forecast'
    plt.title(title)
    plt.legend(loc='upper left', fontsize=8)

def sarimax_forecast(hour=11):
    '''hour: hour of a day, range(0, 23),
    returns forecast, upper_intervals, lower_intervals, mape, mase, test, train'''
    df = get_data(hour=hour)
    # Build Model
    sarima = SARIMAX(df.price, df.drop('price', axis=1),
                 order=(1,1,1), seasonal_order=(1,0,2,7))
    sarima = sarima.fit(maxiter=200)
    # get features for forecast
    features = ????
    # forecasting
    results = sarima.get_forecast(1, exog=features, alpha=0.05)
    forecast = sarima.forecast(1, exog=features, alpha=0.05)
    confidence_int = results.conf_int()
    # create forecast df with datetimeIndex
    lower = confidence_int['lower price'][0]
    upper = confidence_int['upper price'][0]
    forecast = pd.DataFrame(forecasts, index=features.index, columns=['price'])
    history = df.iloc[-7:,0]
    return forecast, history, lower, upper

def plot_sarima_forecast(hour=11):
    '''it uses sarima model and walk forward validation to forecast elect_price
    on hour=11 for next n=30 days and plot the forecast results'''
    forecast, history, lower, upper = sarimax_forecast(hour=hour)
    plot_forecast(forecast, history, test, lower, upper)
