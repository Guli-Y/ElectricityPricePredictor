import pandas as pd
from datetime import timedelta, date, timezone, datetime
import requests
import json
from geopy.geocoders import Nominatim
import xmltodict
import time
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

ENSTOSE_API_KEY = os.getenv('ENSTOSE_API_KEY')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

def call_dayahead_price(start, stop, key=ENSTOSE_API_KEY ):
    """Returns dataframe with day-ahead electricity prices for DK1 within specified date range.
       start and stop should be datetime objects
       e.g.
       start = datetime.today()
       stop = start + timedelta(days=1)
       """
    #CONVERT TO UTC
    start_utc = start.astimezone(timezone.utc)
    stop_utc = stop.astimezone(timezone.utc)
    #convert to string
    period_start = datetime.strftime(start_utc, "%Y%m%d%H%M")
    period_stop = datetime.strftime(stop_utc, "%Y%m%d%H%M")
    #get response
    url = "https://transparency.entsoe.eu/api?"
    params = dict(
        securityToken= key,
        documentType= "A44",
        processType= "A01",
        in_Domain= "10YDK-1--------W",
        out_Domain= "10YDK-1--------W",
        periodStart= period_start,
        periodEnd= period_stop
    )
    response = requests.get(url, params) # XML forma
    # converted to json
    result = json.loads(
        json.dumps(
            xmltodict.parse(response.text)
        ))['Publication_MarketDocument']['TimeSeries']['Period']
    # get prices
    price = result['Point']
    price = pd.DataFrame(price)['price.amount']
    #Get time index
    begin = result['timeInterval']['start']
    end = result['timeInterval']['end']
    time_index = pd.date_range(begin, end, freq="H", closed='left')
    #conv to local
    time_index = time_index.tz_convert('Europe/Copenhagen')
    # format extra strings at the end
    time_index = pd.Series(time_index).apply(lambda x: str(x)[:19])
    price_df = price.to_frame(name='price').set_index(pd.DatetimeIndex(time_index))
    return price_df

def call_past_weather(city, date_, key=OPENWEATHER_API_KEY):
    """calls openweather api and returns the weather for a given DK1 city on (date_ - 1 day)"""
    # city coordinates
    geolocator = Nominatim(user_agent="dk_explorer")
    location = geolocator.geocode('Aalborg')
    lat = location.latitude
    lon = location.longitude
    # time
    t_unix = int(time.mktime(date_.timetuple()))
    # weather endpoint
    url = f'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={t_unix}&appid={key}&units=metric'
    result = requests.get(url).json()['hourly']   # hourly data points
    # json to dataframe
    df = pd.DataFrame(result)
    df['city_name'] = city
    # convert to datetime and DK timezone
    times = pd.to_datetime(df['dt'], unit='s', origin='unix')
    df['dt'] = times.dt.tz_localize('UTC').dt.tz_convert('Europe/Copenhagen').dt.strftime('%Y-%m-%d %H:%M:%S')
    return df

def call_weather_forecast(city, key=OPENWEATHER_API_KEY):
    """returns 48 hours weather forecast for a given DK1 city in json format"""
    geolocator = Nominatim(user_agent="dk_explorer")
    location = geolocator.geocode(city + ' DK')
    lat = location.latitude
    lon = location.longitude
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={key}&units=metric'
    result = requests.get(url).json()
    return result
