
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from termcolor import colored

def plot_evaluation(train, test, mape=None, mase=None):
    '''it will plot a forecast'''
    plt.figure(figsize=(10,4), dpi=100)
    plt.plot(train.price,
                label='training', color='black')
    plt.plot(test.price,
                label='actual', color='black', ls='--')
    plt.plot(test.forecast_price,
                label='forecast', color='orange')
    plt.fill_between(test.index,
                        test.lower_interval,
                        test.upper_interval,
                        label='confidence interval', color='k', alpha=.15)
    title = 'Forecast vs Actuals'
    if isinstance(mape, str):
        title +=f' MAPE:{mape}'
    if isinstance(mase, str):
        title +=f' MASE:{mase}'
    plt.title(title)
    plt.legend(loc='upper left', fontsize=8)

def plot_forecast(forecast, past):
    '''it will plot a forecast'''
    fig, ax = plt.subplots(figsize=(10,4), dpi=100)
    ax.plot(past,
            label='day-ahead',
            color='black')
    ax.plot(forecast.price,
                label='forecast',
                color='blue')
    ax.fill_between(forecast.index,
                    forecast.lower_interval,
                    forecast.upper_interval,
                    label='confidence interval',
                    color='k', alpha=.15)
    title = 'Electricity Price Forecast - next 48 hours (EUR/Mwh)'
    ax.set_title(title)
    ax.legend(loc='upper left', fontsize=8)
    ax.set_ylabel('price')
    ax.grid(True)
    ax.format_xdata = mdates.DateFormatter('%d-%H-%m')
    fig.autofmt_xdate()
    return fig
