import requests
import time
import datetime
from geopy.geocoders import Nominatim
import pandas as pd

def get_weather_forecast(city):
    """returns the weather forecast for a given Danish city
    in json format"""

    key = '7028ef7cb1384c020af39dc40e0e14b5'

    geolocator = Nominatim(user_agent="dk_explorer")
    location = geolocator.geocode(city + ' DK')
    lat = location.latitude
    lon = location.longitude

    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={key}&units=metric'
    result = requests.get(url).json()

    return result

def weather_to_df():
    """returns a dataframe with average (weighted) weather for next 48 hours
    in DK1 zone
    """
    # cities in DK1 region
    cities = ['Aalborg', 'Aarhus', 'Esbjerg', 'Herning',
              'Horsens', 'Kolding','Odense', 'Randers',
              'Silkeborg', 'Vejle', 'Viborg']

    # retireive weather for each city with get_weather_forecast
    weather = {}
    for city in cities:
        weather[city] = get_weather_forecast(city)['hourly']

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

    appended_df['population'] = [pop[city] for city in appended_df.city_name]

    # numeric weather values as affects demand or supply
    numeric_cols = ['temp', 'humidity', 'wind_speed']

    weather_df = pd.DataFrame()

    #for the numeric columns, group by datetime and average according to their population weight
    for col in numeric_cols:
    #group by the datecolumn for each element in the column average it by it's weight
        weather_df[col] = appended_df.groupby(appended_df.dt).apply(lambda x : np.average(x[col], weights=x.population))

    return weather_df
