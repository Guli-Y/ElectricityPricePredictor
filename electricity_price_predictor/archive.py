################### functions used during feature exploration ##################
import pandas as pd
import os
from electricity_price_predictor.data import get_shifted_price, get_updated_weather, get_holidays

PATH = os.path.dirname(os.path.abspath(__file__))

def fetch_files(path=PATH):
    '''it gets the csv file names from raw_data directory'''
    path = os.path.join(path, '..')
    csv_files = []
    for root, direc, files in os.walk(path):
        if 'raw_data\\' in root:
            csv_files.append(files)
    return csv_files

def get_load(path='../raw_data/load/'):
    load_files = fetch_files()[1]
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

def get_coal_price(path='../raw_data/coal_price.xls'):
    """return daily coal prices from 25-NOV-15 till 24-NOV-20"""
    df = pd.read_excel(path, skiprows=2)
    df = df.rename(columns={'Unnamed: 0':'time',
                            'ROTTERDAM COAL': 'coal_price'})
    df.time = pd.to_datetime(df.time)
    df = df.set_index('time').sort_index()
    df.fillna(method='ffill', inplace=True)

    return df

def get_wind_prod(path="../raw_data/productionconsumptionsettlement.csv"):
    """Returns a feature-engineered dataframe including:
    1. Wind production
    2. Wind share of total production
    """
    data = pd.read_csv(path)
    # columns with actual (needed) prod values
    measures = data.drop(columns=["HourUTC","HourDK"]).columns
    df = data[["HourDK"] + list(measures)]
    # convert to datetime and set time index
    df['time'] = pd.to_datetime(df['HourDK'].replace("T", " "))
    df = df.drop(columns="HourDK").sort_values(by="time").set_index("time").loc["2015-01-01":]
    # columns to be engineered
    wind = ["OffshoreWindLt100MW_MWh", "OffshoreWindGe100MW_MWh",
            "OnshoreWindLt50kW_MWh", "OnshoreWindGe50kW_MWh"]

    non_wind = ["CentralPowerMWh", "LocalPowerMWh", "HydroPowerMWh",
                "SolarPowerLt10kW_MWh", "SolarPowerGe10Lt40kW_MWh",
                "SolarPowerGe40kW_MWh", "TransmissionLossMWh"]

    irrelevant_cols = ["PriceArea","ExchangeGE_MWh","PowerToHeatMWh",
                       "ExchangeNO_MWh","ExchangeSE_MWh", "ExchangeNL_MWh",
                       "GrossConsumptionMWh","ExchangeGreatBelt_MWh",
                       "LocalPowerSelfConMWh"]

    substract_cols = "SolarPowerSelfConMWh"

    part_null_cols = ["SolarPowerGe10Lt40kW_MWh","SolarPowerGe40kW_MWh",
                      "SolarPowerLt10kW_MWh","TransmissionLossMWh"]

    # drop irrelevant
    df = df.drop(columns=irrelevant_cols)
    # deal with NaNs
    df[substract_cols] = df[substract_cols].fillna(0)
    df[part_null_cols] = df[part_null_cols].fillna(0)
    # wind_prod & non_wind engineered from sum off all wind / nonwind cols
    df['wind_prod'] = df[wind].sum(axis=1)
    df["non_wind_prod"] = df[non_wind].sum(axis=1)
    # total prod and wind percentage of total defined
    df["total_prod"] = df["wind_prod"] + df["non_wind_prod"] - df[substract_cols]
    df["wind_share"] = df["wind_prod"] / df["total_prod"]
    # final df with needed engineered cols
    final_df = df[["total_prod", "wind_prod", "wind_share"]]

    return final_df

def get_all():
    '''it returns a merged df that contains the hourly values for price, weather,
    wind production, total production, coal price, and holidays'''
    df_price = get_shifted_price()
    df_load = get_shifted_load()
    df_weather = get_updated_weather()
    df_wind = get_wind_prod()
    # change the index of df_coal so that it can be joined with others
    df_coal = get_coal_price()
    df_coal = df_coal.resample('H').pad()
    # change the index of df_holidays so that it can be joined with others
    df_holidays = get_holidays().drop(columns=['holiday_name'])
    df_holidays = df_holidays.resample('H').pad()
    # joining all the dataframes
    dfs = dict(load=df_load, weather=df_weather, wind=df_wind, coal=df_coal, holidays=df_holidays)
    # merge all features
    df_all = df_price
    for df in dfs.values():
        df_all = df_all.join(df, how='inner')
    df_all.dropna(inplace=True)
    return df_all

def get_daily_data(hour=11):
    df = get_all()
    df = df[df.index.hour==hour]
    return df
