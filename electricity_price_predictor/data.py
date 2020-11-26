import os
import numpy as np
import pandas as pd
from datetime import timedelta

def file_names(path='../'):
    csv_files = []
    for root, direc, files in os.walk('../'):
        if 'raw_data\\' in root:
            csv_files.append(files)
    return csv_files


def get_price(path='../raw_data/price/'):
    price_files = file_names()[2]
    df = pd.read_csv(path+price_files[0])
    for file in price_files[1:]:
        df_2 = pd.read_csv(path+file)
        df = pd.concat([df, df_2])
    df = df.reset_index(drop=True)
    df.columns = ['time', 'price']
    df['time'] = df.time.str[:16]
    df = df[df.price!='-'] # filtering the timestamps till 24.11.2020
    df['time'] = pd.to_datetime(df['time'], format='%d.%m.%Y %H:%M')
    df['price'] = df.price.astype('float')
    df.set_index(pd.DatetimeIndex(df['time']), inplace=True)
    df.drop(columns=['time'], inplace=True)
    return df

def get_load(path='../raw_data/load/'):
    load_files = file_names()[1]
    df = pd.read_csv(path+load_files[0])
    for file in load_files[1:]:
        df_2 = pd.read_csv(path+file)
        df = pd.concat([df, df_2])
    df = df.reset_index(drop=True)
    df = df.drop(columns='Day-ahead Total Load Forecast [MW] - BZN|DK1')
    df.columns = ['time', 'load']
    df['time'] = df.time.str[:16]
    df = df[df.load!='-'] # filtering the timestamps till 24.11.2020
    df['time'] = pd.to_datetime(df['time'], format='%d.%m.%Y %H:%M')
    df['load'] = df.load.astype('float')
    df.set_index(pd.DatetimeIndex(df['time']), inplace=True)
    df.drop(columns=['time'], inplace=True)
    return df

def get_shifted_price():
    """Takes in dataframe and performs shift to compensate for daylight saving"""
    df = get_price()
    df_1 = df.loc['2015-01-01 00:00:00':'2015-03-29 01:00:00']
    df_2 = df.loc['2015-03-29 02:00:00':'2015-10-25 02:00:00']
    df_3 = df.loc['2015-10-25 03:00:00':'2016-03-27 01:00:00']
    df_4 = df.loc['2016-03-27 02:00:00':'2016-10-30 02:00:00']
    df_5 = df.loc['2016-10-30 03:00:00':'2017-03-26 01:00:00']
    df_6 = df.loc['2017-03-26 02:00:00':'2017-10-29 02:00:00']
    df_7 = df.loc['2017-10-29 03:00:00':'2018-03-25 01:00:00']
    df_8 = df.loc['2018-03-25 02:00:00':'2018-10-28 02:00:00']
    df_9 = df.loc['2018-10-28 03:00:00':'2019-03-31 01:00:00']
    df_10 = df.loc['2019-03-31 02:00:00':'2019-10-27 02:00:00']
    df_11 = df.loc['2019-10-27 03:00:00':'2020-03-29 01:00:00']
    df_12 = df.loc['2020-03-29 02:00:00':'2020-10-25 02:00:00']
    df_13 = df.loc['2020-10-25 03:00:00':'2020-11-24 23:00:00']

    df_shift = [df_2, df_4, df_6, df_8, df_10, df_12]
    no_shift = [df_1, df_3, df_5, df_7, df_9, df_11, df_13]

    price_df = df_1
    for data in no_shift[1:]:
        price_df = pd.concat([price_df, data])
    for data in df_shift:
        data = data.shift(periods=-1).dropna()
        price_df = pd.concat([price_df, data])

    price_df = price_df.sort_index()

    return price_df


def get_shifted_load():
    """Takes in dataframe and performs shift to compensate for daylight saving"""
    df = get_load()
    df_1 = df.loc['2015-01-01 00:00:00':'2015-03-29 01:00:00']
    df_2 = df.loc['2015-03-29 02:00:00':'2015-10-25 02:00:00']
    df_3 = df.loc['2015-10-25 03:00:00':'2016-03-27 01:00:00']
    df_4 = df.loc['2016-03-27 02:00:00':'2016-10-30 02:00:00']
    df_5 = df.loc['2016-10-30 03:00:00':'2017-03-26 01:00:00']
    df_6 = df.loc['2017-03-26 02:00:00':'2017-10-29 02:00:00']
    df_7 = df.loc['2017-10-29 03:00:00':'2018-03-25 01:00:00']
    df_8 = df.loc['2018-03-25 02:00:00':'2018-10-28 02:00:00']
    df_9 = df.loc['2018-10-28 03:00:00':'2019-03-31 01:00:00']
    df_10 = df.loc['2019-03-31 02:00:00':'2019-10-27 02:00:00']
    df_11 = df.loc['2019-10-27 03:00:00':'2020-03-29 01:00:00']
    df_12 = df.loc['2020-03-29 02:00:00':'2020-10-25 02:00:00']
    df_13 = df.loc['2020-10-25 03:00:00':'2020-11-23 16:00:00']

    df_shift = [df_2, df_4, df_6, df_8, df_10, df_12]
    no_shift = [df_1, df_3, df_5, df_7, df_9, df_11, df_13]

    load_df = df_1
    for data in no_shift[1:]:
        load_df = pd.concat([load_df, data])
    for data in df_shift:
        data = data.shift(periods=-1).dropna()
        load_df = pd.concat([load_df, data])

    load_df = load_df.sort_index()

    return load_df


def get_weather(path='../raw_data/weather_2015_2020.csv'):
    df = pd.read_csv(path)

    df['dt'] = pd.to_datetime(df.dt)

    # drop unnecessary columns
    to_drop = ['dt_iso','timezone','lat', 'lon','sea_level','grnd_level',
               'rain_1h','rain_3h', 'pressure', 'snow_1h', 'snow_3h',
               'temp_min','temp_max','weather_id', 'weather_description',
               'weather_icon']
    df = df.drop(to_drop, axis=1)

    # population of each city in the df
    pop = {'Aarhus': 349_983,
        'Odense': 204_895,
        'Aalborg': 217_075,
        'Esbjerg': 115_748,
        'Vejle': 111_743,
        'Randers': 96_559,
        'Viborg': 93_819,
        'Kolding': 89_412,
        'Silkeborg': 89_328,
        'Herning': 86_348,
        'Horsens': 83_598}

    df['population'] = [pop[city] for city in df.city_name]

    # numeric weather values as affects demand or supply
    numeric_cols = ['temp', 'feels_like', 'humidity',  'clouds_all','wind_speed', 'wind_deg']

    weather_df = pd.DataFrame()

    #for the numeric columns, group by datetime and average according to their population weight
    for col in numeric_cols:
    #group by the datecolumn for each element in the column average it by it's weight
        weather_df[col] = df.groupby(df.dt).apply(lambda x : np.average(x[col], weights=x.population))

    # check for missing indices
    missing_idx = pd.date_range(start = '2015-01-01', end = '2020-11-24', freq='H' ).difference(weather_df.index)

    # impute missing indices with average of bounding rows
    for idx in missing_idx:
        weather_df.loc[idx] = weather_df.loc[pd.to_datetime(idx) - timedelta(hours= 1)] + \
                      weather_df.loc[pd.to_datetime(idx) + timedelta(hours= 1)] / 2

    weather_df = weather_df.sort_index()

    return weather_df

