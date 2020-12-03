from electricity_price_predictor.data import get_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.statespace.sarimax import SARIMAX
import joblib

def plot_forecast(forecast, train, lower, upper):
    '''it will plot a forecast'''
    fig, ax = plt.subplots(figsize=(10,4), dpi=100)
    ax.plot(train, label='past', color='black')
    ax.plot(forecast, label='forecast', color='blue')
    ax.fill_between(lower.index, lower, upper, label='confidence interval',
                    color='k', alpha=.15)
    title = 'Electricity Price Forecast - next 48 hours (EUR/Mwh)'
    ax.set_title(title)
    ax.legend(loc='upper left', fontsize=8)
    ax.set_ylabel('price')
    ax.grid(True)
    ax.format_xdata = mdates.DateFormatter('%d-%H-%m')
    fig.autofmt_xdate()
    plt.savefig('../forecast_data/forecast.png')


def sarimax_forecast(hour=11):
    '''hour: hour of a day, range(0, 23),
    returns forecast, upper_intervals, lower_intervals, mape, mase, test, train'''
    past, future = get_data(hour=hour)
    future = future.iloc[:1,:]
    if future.temp.isnull()[0]:
        forecast = np.array([np.nan])
        confidence_int =pd.DataFrame({'lower price':np.nan, 'upper price':np.nan}, index=['x'])

    else:
        past.index = pd.DatetimeIndex(past.index.values,
                                        freq=past.index.inferred_freq)
        # Build Model
        sarima = SARIMAX(past.price, past.drop('price', axis=1),
                     order=(1,1,1), seasonal_order=(1,0,2,7))
        sarima = sarima.fit(maxiter=300)
        # forecasting
        results = sarima.get_forecast(1, exog=future, alpha=0.05)
        forecast = sarima.forecast(1, exog=future, alpha=0.05)
        confidence_int = results.conf_int()
    # create forecast df with datetimeIndex
    lower = confidence_int['lower price'][0]
    upper = confidence_int['upper price'][0]
    forecast = pd.DataFrame(dict(price=forecast, lower=lower, upper=upper),
                            index=future.index)
    past = past.iloc[-1:,0]
    return forecast, past

def sarimax_forecast_24():
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

def plot_sarimax_forecast(hour=11):
    '''it calls sarimax_forecast function and
    plot the forecast results using plot_forecast function'''
    forecast, past = sarimax_forecast(hour=hour)
    plot_forecast(forecast.price, past, forecast.lower, forecast.upper)

def plot_sarimax_forecast_24():
    '''it calls sarimax_forecast_24 function and
    plot the forecast results using plot_forecast function'''
    forecast, past = sarimax_forecast_24()
    forecast.to_csv('../forecast_data/forecast_data.csv')
    plot_forecast(forecast.price, past, forecast.lower, forecast.upper)
