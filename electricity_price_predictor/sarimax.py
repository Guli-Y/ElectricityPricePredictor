from electricity_price_predictor.data import get_data
from electricity_price_predictor.plot import plot_forecast
import pandas as pd
import numpy as np
from termcolor import colored
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import date
import matplotlib.pyplot as plt
from google.cloud import storage
import os

BUCKET_NAME = 'electricity_price_predictor'

def sarimax_forecast(df):
    '''it takes a dataframe split it into train/forecast sets based on
    the availability of price and then forecasts electricity price for next hour.
    it returns forecast dataframe ('price','lower_interval', 'upper_interval') and
    historical price dataframe ('price')'''

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
    forecast = pd.DataFrame(dict(price=forecast, lower_interval=lower,
                                    upper_interval=upper), index=future.index)
    past = past.iloc[-1:,0]
    return forecast, past

def sarimax_forecast_24(df=None):
    '''it calls sarimax_forecast function 24 times to get hourly forecast for
    next day '''
    if df is None:
        print(colored('############## loading data ##############', 'blue'))
        df = get_data()
    # loop over to get forecast for each hour
    forecasts = []
    pasts = []
    for i in range(1, 24):
        print(colored(f"############## forecasting for {str(i)}:00 o'clock ##############", 'green'))
        df_i = df[df.index.hour==i]
        forecast_i, past_i = sarimax_forecast(df_i)
        forecasts.append(forecast_i)
        pasts.append(past_i)
    # merge 24 hours
    print(colored('############## merging forecast data ##############', 'red'))
    df_0 = df[df.index.hour==0]
    forecast_df, past_df = sarimax_forecast(df_0)
    for forecast, past in zip(forecasts, pasts):
        forecast_df = pd.concat([forecast_df, forecast])
        past_df = pd.concat([past_df, past])
    # sort the index
    forecast_df = forecast_df.sort_index()
    past_df = past_df.sort_index()
    return forecast_df, past_df

if __name__=='__main__':
    forecast, past = sarimax_forecast_24()
    # save the forecast results locally
    today = date.today()
    data = f'forecast_{today}.csv'
    fig = f'forecast_{today}.png'
    forecast.to_csv(data)
    fig = plot_forecast(forecast, past)
    fig.savefig(fig)
    # upload to GCP cloud storage
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
        # forecast data
    blob = bucket.blob('forecast/'+data)
    blob.upload_from_filename(data)
    location = f'gs://{BUCKET_NAME}/forecast/{data}'
    print(colored(f'forecast data uploaded to cloud storage \n => {location}', 'green'))
        # forecast figure
    blob = bucket.blob('forecast/'+fig)
    blob.upload_from_filename(fig)
    location = f'gs://{BUCKET_NAME}/forecast/{fig}'
    print(colored(f'forecast figure uploaded to cloud storage \n => {location}', 'blue'))
    os.remove(data)
    os.remove(fig)
