import os
import numpy as np
import pandas as pd
from datetime import timedelta, date, timezone, datetime
import holidays
from electricity_price_predictor.tools import call_dayahead_price, call_past_weather, call_weather_forecast

PATH = os.path.dirname(os.path.abspath(__file__))

########################## get price data ######################################
def get_updated_price(path=PATH):
    ''' it calls enstsoe api to get dayahead prices and updates the historical
    dayahead prices then returns a df which contains dayahead prices of electricity
    from 01-01-2015 till tomorrow'''
    # get past price
    file = os.path.join(path, 'data', 'updated_price.csv')
    df = pd.read_csv(file, parse_dates=True, index_col='time')
    dayahead = date.today() + timedelta(days=1)
    try: # after 13:00 day-ahead price is available
        while df.index[-1].date() < dayahead:
            # get the rest including day-ahead by calling api
            start = df.index[-1].date() + timedelta(days=1)
            start = datetime.combine(start, datetime.min.time())  # initialize to midnight
            stop = start + timedelta(days=1)
            new_price = call_dayahead_price(start, stop)
            new_price.index.name = 'time'
            new_price.set_index(pd.DatetimeIndex(new_price.index), inplace=True)
            # update the price csv
            df = pd.concat([df, new_price])
            df.to_csv(file)
    except: # before 13:00 day-ahead price is not availeble
        pass
    return df

def get_shifted_price():
    """get price data and performs shift according to daylight saving"""
    df = get_updated_price()
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
    df_13 = df.loc['2020-10-25 03:00:00':]

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

############################ get weather data ##################################

POPULATION = {'Aarhus': 349_983,
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
# cities in DK1 region
CITIES = [key for key in POPULATION.keys()]

def get_historical_weather(path=PATH, selected_features=False):
    file = os.path.join(path, '..', 'raw_data', 'weather_2015_2020.csv')
    df = pd.read_csv(file)
    df['dt'] = pd.to_datetime(df.dt)
    # selecting useful columns
    cols = ['temp', 'feels_like', 'humidity',  'clouds_all', 'wind_speed']
    df = df[cols]
    df['population'] = [POPULATION[city] for city in df.city_name]
    #group by datetime and average weather values according to city population
    weather_df = pd.DataFrame()
    for col in cols:
        weather_df[col] = df.groupby(df.dt).apply(lambda x : np.average(x[col], weights=x.population))
    # check for missing indices
    missing_idx = pd.date_range(start = '2015-01-01', end = '2020-11-24', freq='H' ).difference(weather_df.index)
    # impute missing indices with average of bounding rows
    for idx in missing_idx:
        weather_df.loc[idx] = weather_df.loc[pd.to_datetime(idx) - timedelta(hours=1)] + \
                      weather_df.loc[pd.to_datetime(idx) + timedelta(hours=1)] / 2
    weather_df.set_index(pd.DatetimeIndex(weather_df.index), inplace=True)
    weather_df = weather_df.sort_index()
    return weather_df

def get_past_weather(date_):
    """returns weather data for DK1 region on date (date_ - 1 day) by calling openweather api"""
    # retireive weather for each city
    weather = {}
    for city in CITIES:
        weather[city] = call_past_weather(city, date_)
    # concat the cities in weather dict into one df
    concat_cities = []
    for key, value in weather.items():
        concat_cities.append(value)
    df_main = pd.concat(concat_cities)
    # get population column
    df_main['population'] = [POPULATION[city] for city in df_main.city_name]
    past_weather_df = pd.DataFrame()
    # features affecting the price
    cols = ['temp', 'humidity', 'wind_speed']
    #for the numeric columns, group by datetime and average according to their population weight
    for col in cols:
        #group by the datecolumn for each element in the column average it by it's weight
        past_weather_df[col] = df_main.groupby(df_main.dt).apply(lambda x : np.average(x[col], weights=x.population))
    past_weather_df.set_index(pd.DatetimeIndex(past_weather_df.index), inplace=True)
    past_weather_df = past_weather_df.sort_index()
    return past_weather_df

def get_weather_forecast():
    """returns a dataframe with average (weighted) weather for next 48 hours
    in DK1 zone
    """
    # retireive weather for each city with get_weather_forecast
    weather = {}
    for city in CITIES:
        weather[city] = call_weather_forecast(city)['hourly']
    # create df
    appended_df = []
    for key, value in weather.items():
        city = str(key)
        df = pd.DataFrame(value)
        df['city_name'] = city
        df = df[['dt', 'temp', 'wind_speed', 'humidity', 'city_name']]
        # datetime covert
        times = pd.to_datetime(df['dt'], unit='s', origin='unix')
        df['dt'] = times.dt.tz_localize('UTC').dt.tz_convert('Europe/Copenhagen').dt.strftime('%Y-%m-%d %H:%M:%S')
    appended_df.append(df)
    appended_df = pd.concat(appended_df)
    appended_df['population'] = [POPULATION[city] for city in appended_df.city_name]
    weather_df = pd.DataFrame()
    # numeric weather values as affects demand or supply
    numeric_cols = ['temp', 'humidity', 'wind_speed']
    for col in numeric_cols:
    #group by the datecolumn for each element in the column average it by it's weight
      weather_df[col] = appended_df.groupby(appended_df.dt).apply(lambda x : np.average(x[col], weights=x.population))
    weather_df.set_index(pd.DatetimeIndex(weather_df.index), inplace=True)
    weather_df = weather_df.sort_index()
    return weather_df

def get_updated_weather(path=PATH):
    '''it gets historical weather data and merge it with weather forecast for next 48h,
    and saves the updated data to updated_data.csv and returns the up to date weather data.
    This function needs to be called at least once in every 48 hours to keep weather data complete'''
    file = os.path.join(path, '..', 'raw_data', 'updated_weather.csv')
    # collect historical weather data
    df_hist = pd.read_csv(file, parse_dates=True, index_col='dt')
    # get forecasted weather data
    df_forecast = get_weather_forecast()
    # concat forecast weather with historical weather
    df_hist = df_hist[df_hist.index < df_forecast.index[0]]
    df = pd.concat([df_hist, df_forecast])
    # update last two days' weather with historical weather
    for i in range(3):
        day = date.today()-timedelta(days=i)
        past = get_past_weather(day)
        columns = ['temp', 'humidity', 'wind_speed']
        for col in columns:
            df.at[past.index[0]:past.index[-1], col] = past.loc[past.index[0]:past.index[-1], col]
    # save the updated_data
    df.to_csv(file)
    return df

#############################   get holidays   #################################
def get_holidays(start='2015-01-01', country='DK', frequency='D'):
    """
    Takes in a start date and a country.
    Produces a dataframe with a daily date time index and columns:
    day_of_week - numerical day of the week identifier 0 for monday
    holiday_bool - boolean true or false for holiday
    holiday_name - name of the holiday if holiday_bool is true
    Returns a dataframe
    """
    # get end date
    end = str(date.today()+timedelta(3))
    #generate the range of daily dates
    dates = pd.date_range(start=start, end=end, freq=frequency)
    #create the holiday object
    country_holidays = holidays.CountryHoliday(country)
    #create a list for the holiday bool and name
    holiday_list = []
    #loop through the dates
    for d in dates:
        #true if holiday in object, false otherwise
        holiday_bool = d in country_holidays
        holiday_names = country_holidays.get(d)
        holiday_list.append([holiday_bool, holiday_names])
    #create return dataframe
    holidays_data = pd.DataFrame(holiday_list, index=dates, columns=['holiday', 'holiday_name'])
    holidays_data.holiday=holidays_data.holiday.astype('int')
    # add whether it is weekend
    holidays_data['weekend'] = 0
    holidays_data.loc[(holidays_data.index.dayofweek==5) | (holidays_data.index.dayofweek==6), 'weekend'] = 1
    return holidays_data

######################## get merged dataframe ##################################

def get_data(hour=False):
    '''it returns hourly data for price, weather and holidays.
    When an integer (0, 24) is given to hour param, it returns daily data.
    It need to be called at least once every 48 hours'''
    df_price = get_shifted_price()
    df_weather = get_updated_weather()
    # change the daily holidays data to hourly data so that it can be joined with others
    df_holidays = get_holidays().drop(columns=['holiday_name'])
    df_holidays = df_holidays.resample('H').pad()
    # joining the dataframes
    dfs = dict(weather=df_weather, holidays=df_holidays)
    # merge all features
    df_merged= df_price
    for df in dfs.values():
        df_merged = df_merged.join(df, how='outer')
    if not hour: # meaning if hour=False
        pass
    else:
        df_merged = df_merged[df_merged.index.hour==hour]
    return df_merged
