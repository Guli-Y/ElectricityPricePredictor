from electricity_price_predictor.data import get_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.statespace.sarimax import SARIMAX

def plot_forecast(forecast, past):
    '''it will plot a forecast'''
    fig, ax = plt.subplots(figsize=(10,4), dpi=100)
    ax.plot(past, label='past', color='black')
    ax.plot(forecast.price, label='forecast', color='blue')
    ax.fill_between(forecast.index, forecast.lower, forecast.upper, label='confidence interval',
                    color='k', alpha=.15)
    title = 'Electricity Price Forecast - next 48 hours (EUR/Mwh)'
    ax.set_title(title)
    ax.legend(loc='upper left', fontsize=8)
    ax.set_ylabel('price')
    ax.grid(True)
    ax.format_xdata = mdates.DateFormatter('%d-%H-%m')
    fig.autofmt_xdate()
    # save the forecast plot for heroku webpage
    print('############## saving forecast plot ##############')
    plt.savefig('../forecast_data/forecast.png')


def sarimax_forecast(df):
    '''it takes a dataframe with past and future values and split it into
    train/forecast sets based on the availability of price and returns
    forecast dataframe and past prices'''

    # split past and furture
    past = df[~df.price.isnull()]
    future = df[df.price.isnull()].drop('price', axis=1)
    # forecast for next time point only
    future = future.iloc[:1,:]
    if future.temp.isnull()[0]: # when weather forecast data is not available for that hour
        forecast = np.array([np.nan])
        lower = np.array([np.nan])
        upper = np.array([np.nan])
        print('weather data is not available')
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
        lower = results.conf_int()['lower price'][0]
        upper = results.conf_int()['upper price'][0]

    # create forecast df with datetimeIndex
    forecast = pd.DataFrame(dict(price=forecast, lower=lower, upper=upper),
                            index=future.index)
    past = past.iloc[-1:,0]
    return forecast, past

def sarimax_forecast_24():
    '''it calls sarimax_forecast function and 24 times to get hourly forecast and
    plot the forecast results using plot_forecast function'''
    df = get_data()
    forecasts = []
    pasts = []
    # loop over to get forecast for each hour
    for i in range(1, 24):
        print(f"############## forecasting for {str(i)}:00 o'clock ##############")
        df_i = df[df.index.hour==i]
        forecast_i, past_i = sarimax_forecast(df_i)
        forecasts.append(forecast_i)
        pasts.append(past_i)
    # merge 24 hours
    print('############## Merging forecasts data ##############')
    df_0 = df[df.index.hour==0]
    forecast_df, past_df = sarimax_forecast(df_0)
    for forecast, past in zip(forecasts, pasts):
        forecast_df = pd.concat([forecast_df, forecast])
        past_df = pd.concat([past_df, past])
    # sort the index
    forecast_df = forecast_df.sort_index()
    past_df = past_df.sort_index()
    return forecast_df, past_df

def plot_sarimax_forecast_24():
    '''it calls sarimax_forecast_24 function and
    plot the forecast results using plot_forecast function'''
    forecast, past = sarimax_forecast_24()
    # save the forecast results
    print('############## saving forecast results ##############')
    forecast.to_csv('../forecast_data/forecast_data.csv')
    # plot the forecast results
    print('############## plotting forecast results ##############')
    plot_forecast(forecast, past)
