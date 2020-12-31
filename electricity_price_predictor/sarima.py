
from electricity_price_predictor.data import get_shifted_price
from electricity_price_predictor.archive import get_daily_data
from electricity_price_predictor.metrics import get_mape, get_mase
from electricity_price_predictor.plot import plot_evaluation
import pandas as pd
import numpy as np
from datetime import timedelta
from termcolor import colored
from statsmodels.tsa.statespace.sarimax import SARIMAX

def get_daily_price(hour=11):
    '''it gets hourly price data by calling get_shifted_price from data.py and
    returns a daily {hour} o'clock price dataframe'''
    df = get_shifted_price()
    df = df[df.index.hour==hour]
    return df

def train_sarimax(data=False, exog=False, hour=11,
                    split_date='2019-10-22 11:00:00', n=30):
    '''
    hour: hour of a day (0, 23),
    exog: takes ([exog features], order, seasonal_order)
    split_date: train, test splitted on this date,
    n: number of days to forecast,
    returns test('price', 'forecast_price', 'lower_interval', 'upper_interval'),
    train('price') and MAPE, MASE'''

    if isinstance(data, bool):
        if isinstance(exog, bool):
            df = get_daily_price(hour=hour)
        else:
            df = get_daily_data(hour=hour)
    else:
        df=data
    # formating split_date
    split_date = pd.DatetimeIndex(np.array([split_date]))
    split_date = split_date[0]
    # get train and test for plotting only
    train = df[(df.index <= split_date)]
    test = df[(df.index > split_date) & \
                      (df.index <= (split_date + timedelta(days=n)))].copy()
    # loop over to get walk forward forecast for n days
    for i in range(1, n+1):
        print(colored(f'################# forecasting for day {i} ##################', 'blue'))
        # walk one day forward to define train_set
        predict_date = split_date + timedelta(days=i)
        train_set = df[df.index < predict_date]
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
            exog_fore = test[test.index==predict_date][exog[0]]
            # forecasting
            results = sarima.get_forecast(1, exog=exog_fore, alpha=0.05)
            forecast = sarima.forecast(1, exog=exog_fore, alpha=0.05)
            confidence_int = results.conf_int()
        # add forecast result into the list
        test.loc[predict_date, 'forecast_price'] = forecast[0]
        test.loc[predict_date, 'lower_interval'] = confidence_int['lower price'][0]
        test.loc[predict_date, 'upper_interval'] = confidence_int['upper price'][0]

    train = train[['price']]
    test = test[['price', 'forecast_price', 'upper_interval', 'lower_interval']]
    # calculate the mape
    mape = get_mape(test.price, test.forecast_price)
    mase = get_mase(test.price, test.forecast_price, train.price)

    return train, test, mape, mase

if __name__=='__main__':
    train, test, mape, mase = train_sarimax()
    plot_evaluation(train, test, mape=None, mase=None)
