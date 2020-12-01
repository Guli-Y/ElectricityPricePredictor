from electricity_price_predictor.data import get_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
import joblib

def plot_forecast(forecast, train, lower, upper):
    '''it will plot a forecast'''
    plt.figure(figsize=(10,4), dpi=100)
    plt.plot(train, label='training', color='black')
    plt.plot(forecast, label='forecast', color='orange')
    plt.fill_between(lower.index, lower, upper, color='k', alpha=.15)
    title = 'Electricity Price Forecast - next 48 hours (EUR/Mwh)'
    plt.title(title)
    plt.legend(loc='upper left', fontsize=8)

def sarimax_forecast(hour=11):
    '''hour: hour of a day, range(0, 23),
    returns forecast, upper_intervals, lower_intervals, mape, mase, test, train'''
    past, future = get_data(hour=hour)
    future = future.iloc[:2,:]
    past.index = pd.DatetimeIndex(past.index.values,
                                    freq=past.index.inferred_freq)
    # Build Model
    sarima = SARIMAX(past.price, past.drop('price', axis=1),
                 order=(1,1,1), seasonal_order=(1,0,2,7))
    sarima = sarima.fit(maxiter=200)
    # save the model
    # joblib.dump(sarima, f'model_{hour}.joblib')
    # print(colored(f"model_{hour}.joblib saved locally", "green"))
    # forecasting
    results = sarima.get_forecast(2, exog=future, alpha=0.05)
    forecast = sarima.forecast(2, exog=future, alpha=0.05)
    confidence_int = results.conf_int()
    # create forecast df with datetimeIndex
    lower = confidence_int['lower price'][0]
    upper = confidence_int['upper price'][0]
    forecast = pd.DataFrame(dict(price=forecast, lower=lower, upper=upper),
                            index=future.index)
    past = past.iloc[-2:,0]
    return forecast, past

def sarimax_forecast_48():
    '''it calls sarimax_forecast function and 24 times to get hourly forecast and
    plot the forecast results using plot_forecast function'''
    forecasts = []
    pasts = []
    for i in range(1, 24):
        forecast_i, past_i = sarimax_forecast(hour=i)
        forecasts.append(forecast_i)
        pasts.append(past_i)
    # merge 24 hours
    forecast_df, past_df = sarimax_forecast(hour=0)
    for forecast, past in zip(forecasts, pasts):
        forecast_df = pd.concat([forecast_df, forecast])
        past_df = pd.concat([past_df, past])
    forecast_df = forecast_df.sort_index()
    past_df = past_df.sort_index()
    return forecast_df, past_df

def plot_sarima_forecast(hour=11):
    '''it calls sarimax_forecast function and
    plot the forecast results using plot_forecast function'''
    forecast, past = sarimax_forecast(hour=hour)
    plot_forecast(forecast.price, past, forecast.lower, forecast.upper)

def plot_sarima_forecast_48():
    '''it calls sarimax_forecast_48 function and
    plot the forecast results using plot_forecast function'''
    forecast, past = sarimax_forecast_48()
    plot_forecast(forecast.price, past, forecast.lower, forecast.upper)
